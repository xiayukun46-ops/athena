# Security Architecture v1.0

## 概述

Athena 的安全架构遵循 **Security First** 原则和**零信任模型**。每个组件、每次通信、每个数据访问都需经过认证和授权。

---

## 1. 威胁模型

### 1.1 攻击面分析

```
┌─────────────────────────────────────────────────────────┐
│                    攻击面                                │
├─────────────────────┬───────────────────────────────────┤
│ 外部威胁            │ 内部威胁                          │
│ • DDoS              │ • 内部用户越权                    │
│ • API 注入          │ • AI Agent 越权                  │
│ • 爬虫/数据抓取     │ • 插件恶意行为                   │
│ • 账号接管          │ • 配置错误                       │
│ • AI Prompt 注入    │ • 供应链攻击                     │
│ • 模型投毒          │ • 密钥泄露                       │
└─────────────────────┴───────────────────────────────────┘
```

### 1.2 Athena 特殊威胁

| 威胁 | 风险等级 | 缓解措施 |
|------|---------|----------|
| AI Prompt Injection | Critical | 输入净化 + 输出验证 + 权限受限 Agent |
| 知识投毒（虚假信息注入） | High | 来源可信度评估 + 声明冲突检测 |
| 模型数据泄露 | High | 数据脱敏 + 审计日志 |
| 图遍历攻击 | Medium | Cypher 查询超时 + 深度限制 |
| Web Scraping 法律风险 | Medium | robots.txt 尊重 + 速率限制 |

---

## 2. 零信任架构

### 2.1 核心原则

```
默认不信任 → 持续验证 → 最小权限 → 假设已被入侵
```

### 2.2 认证体系

```
┌──────────────────────────────────────────────┐
│              认证边界                         │
│                                              │
│  用户 → JWT (OAuth 2.0 + OIDC)               │
│  服务 → mTLS + API Key                       │
│  插件 → Plugin Identity Token                │
│  Agent → Agent Scoped Token (受限权限)       │
│                                              │
├──────────────────────────────────────────────┤
│              授权策略                         │
│                                              │
│  RBAC:  角色 → 权限集合                      │
│  ABAC:  属性 → 动态策略（时间/IP/资源类型）  │
│  ReBAC: 关系 → 数据级权限（基于知识图谱）    │
└──────────────────────────────────────────────┘
```

### 2.3 角色定义

| 角色 | 权限范围 |
|------|----------|
| Anonymous | 只读公开内容，搜索，无 AI 配额 |
| User | 个性化，收藏，AI 配额（有限） |
| Moderator | 审核声明，管理实体合并 |
| Admin | 系统配置，插件管理，用户管理 |
| System Agent | 自动化任务，受限域内操作 |

---

## 3. 数据安全

### 3.1 数据分类

| 级别 | 示例 | 保护要求 |
|------|------|----------|
| Public | 公开文章、实体信息 | 无特殊要求 |
| Internal | 用户偏好、使用统计 | 访问控制 |
| Confidential | 用户邮箱、API Key | 加密存储 + 审计 |
| Restricted | 密码哈希、支付信息 | 最高级别加密 + 最小访问 |

### 3.2 加密策略

```
传输层: TLS 1.3 (强制，不允许降级)
存储层: AES-256-GCM
  - 用户密码: bcrypt (cost=12)
  - API Key: SHA-256 哈希存储
  - PII: 加密存储，密钥在 KMS
密钥管理: 密钥轮换 90 天，密钥不落地
```

### 3.3 数据脱敏

- 日志中自动脱敏 email、phone、IP
- AI Prompt 中脱敏 PII 后再发送至外部模型
- API 响应中按角色过滤敏感字段

---

## 4. API 安全

### 4.1 防护层

```
Client → WAF → API Gateway → Service → Database
           │        │            │          │
           │  DDoS  │  Rate      │  AuthZ   │  Encryption
           │  WAF   │  Limit     │  Log     │  at Rest
           │  rules │            │          │
```

### 4.2 输入验证

- 所有输入在 API Gateway 边界验证（Pydantic / Zod）
- SQL 查询参数化（禁止字符串拼接）
- Cypher 查询参数化（禁止字符串拼接）
- AI Prompt 输入净化（移除注入模式）

### 4.3 速率限制

参见 [API Design](api-design.md) 第 11 节。

---

## 5. Agent 安全

### 5.1 权限模型

```python
# Agent 权限声明
class AgentPermission:
    scope: list[PermissionScope]    # read:articles, write:entities
    max_tokens_per_day: int
    allowed_models: list[str]
    allowed_tools: list[str]        # 工具白名单
    requires_approval: list[str]    # 需要人工审批的操作
```

### 5.2 沙箱执行

- Agent 代码在 Docker 容器中运行
- 网络出口白名单控制
- CPU 限制: 2 vCPU, Memory: 4GB
- 磁盘写入只允许临时目录
- 超时: 单任务 ≤ 5 分钟

### 5.3 AI 安全措施

| 措施 | 说明 |
|------|------|
| Prompt 模板化 | 禁止 Agent 直接拼接用户输入到 System Prompt |
| Output 验证 | AI 输出在写入数据库前通过 Schema 验证 |
| 敏感信息检测 | AI 输入/输出扫描 PII 和密钥模式 |
| 审计日志 | 所有 Agent 操作全量记录 |

---

## 6. 插件安全

### 6.1 插件签名验证

```
Plugin Package → SHA-256 Hash → Maintainer Signature → Registry
                                                          │
                                              安装时验证签名链
```

### 6.2 插件权限声明

```json
{
  "permissions": {
    "network": ["api.example.com"],
    "filesystem": "read_only",
    "database": ["content.articles:read"],
    "ai": false,
    "user_data": false
  }
}
```

---

## 7. 安全运维

### 7.1 监控与告警

| 指标 | 阈值 | 动作 |
|------|------|------|
| 失败认证率 | > 10/min | 告警 + IP 封禁 |
| API 异常流量 | > 正常值 5x | 告警 + 限流 |
| AI Token 异常消耗 | > 正常值 3x | 告警 + 暂停 |
| 敏感操作频率 | > 正常值 10x | 告警 + 审计 |
| 插件异常行为 | 任意检测 | 告警 + 隔离 |

### 7.2 事件响应

1. **检测**: 自动化告警 / 人工报告
2. **分类**: Severity (P0-P3)
3. **遏制**: 隔离受影响组件
4. **根因分析**: 5 Whys / Post-mortem
5. **修复**: 补丁 + 回归测试
6. **回顾**: 更新威胁模型和规则

### 7.3 合规

- **GDPR**: 数据驻留选择（EU / Asia）、删除权、数据可携带性
- **SOC 2 Type II**: 就绪架构（Phase 4 认证）
- **ISO 27001**: Phase 5 目标

---

## 8. 安全检查清单（每次发布前）

- [ ] 依赖漏洞扫描 (Trivy / Dependabot)
- [ ] 密钥扫描 (Gitleaks)
- [ ] SAST 静态分析
- [ ] DAST 动态分析（Phase 3+）
- [ ] AI Prompt 注入测试
- [ ] 速率限制测试
- [ ] 认证/授权测试
- [ ] 日志审计完整性

---

*安全架构每季度 Review，威胁模型随新功能更新。*
