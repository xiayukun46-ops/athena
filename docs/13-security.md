# 13 — Security Architecture

> Athena 的安全设计。零信任、纵深防御、AI 特化。

**详细设计见**: [architecture/security.md](architecture/security.md)

---

## 安全原则

1. **零信任**: 默认不信任任何输入——包括 AI 的输出
2. **纵深防御**: 多层防护，单层被突破不会导致全系统沦陷
3. **最小权限**: 每个组件只能访问自己需要的资源
4. **安全左移**: 安全从设计阶段开始，不是上线前的检查项

---

## 威胁模型

### 通用威胁

| 威胁 | 防护 |
|------|------|
| SQL 注入 | 参数化查询（SQLAlchemy 2.0 默认） |
| XSS | CSP Header + 输出编码 |
| CSRF | SameSite Cookie + CSRF Token |
| DDoS | API Gateway 限流 |
| 密钥泄露 | `.env` gitignore + Gitleaks CI 扫描 |

### AI 特化威胁

| 威胁 | 风险 | 防护 |
|------|------|------|
| Prompt Injection | Critical | 输入净化 + 工具白名单 + Agent 沙箱 |
| 知识投毒 | High | Statement 审核 + 来源可信度 + 冲突检测 |
| 模型数据泄露 | High | 输入/输出 PII 脱敏 + 审计 |
| 过度依赖 AI 输出 | Medium | 置信度标注 + 人工审核通道 |

---

## 认证与授权

### 多层认证

```
用户 → JWT (OAuth 2.0 + OIDC)
服务 → mTLS + API Key
插件 → Plugin Identity Token
Agent → Scoped Token (受限权限)
```

### 授权模型

| 模型 | 适用 | 说明 |
|------|------|------|
| RBAC | 基础权限 | 角色: Anonymous, User, Moderator, Admin |
| ABAC | 动态策略 | 时间/IP/设备 → 条件访问 |
| ReBAC | 数据级权限 | 基于知识图谱关系的权限（Phase 3+） |

---

## 数据安全

### 加密

| 层 | 算法 | 说明 |
|----|------|------|
| 传输 | TLS 1.3 | 强制，不允许降级 |
| 密码 | bcrypt (cost=12) | 不可逆哈希 |
| API Key | SHA-256 | 只存哈希 |
| PII | AES-256-GCM | KMS 密钥管理 |
| 密钥 | 90 天轮换 | 密钥不落地 |

### 数据脱敏

- 日志中自动脱敏 email、phone、IP
- AI Prompt 中脱敏 PII 后发外部模型
- API 响应按角色过滤敏感字段

---

## Agent 安全

**最高优先级**——Agent 拥有工具调用能力，是攻击面最大的组件。

```
Agent 权限声明:
  scope: [read:articles, write:entities]
  max_tokens_per_day: 500000
  allowed_models: [gpt-5-mini]
  allowed_tools: [search_knowledge_graph, create_entity]
  requires_approval: [merge_entities, delete_entity]

沙箱:
  Docker 容器
  CPU: 2 vCore, Memory: 4GB, Timeout: 5min
  网络: 白名单控制
  磁盘: 只写临时目录
```

---

## 安全检查清单

每次 PR / 发布前：

- [ ] Trivy 依赖漏洞扫描（无 HIGH/CRITICAL）
- [ ] Gitleaks 密钥扫描
- [ ] SAST 静态分析
- [ ] AI Prompt 注入测试
- [ ] 认证/授权测试
- [ ] 审计日志完整性

---

## 相关文档

- [02-constitution.md](02-constitution.md) — Security First 原则
- [10-agent-system.md](10-agent-system.md) — Agent 安全设计
- [architecture/security.md](architecture/security.md) — 完整威胁模型
