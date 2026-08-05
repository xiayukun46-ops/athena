# RFC-009: Plugin Lifecycle & Hot Reload

## Metadata

| 字段 | 值 |
|------|-----|
| RFC ID | RFC-009 |
| Status | Draft |
| Priority | P2 |
| Target Phase | Phase 2-3 |

---

## 1. Background

Athena 的架构以 Plugin 为核心扩展机制。插件需要明确的生命周期管理。Phase 3+ 需要支持热加载（无需重启即可加载/卸载插件）。

## 2. Problem

当前 Plugin 规范定义了 5 类插件接口和生命周期阶段（Register→Configure→Init→Activate→Deactivate→Dispose），但未细化：如何检测插件更新、如何安全卸载运行中的插件、热加载的实现策略。

## 3. Goals

- [ ] P0: 完整的生命周期状态机实现（Phase 2）
- [ ] P1: 插件异常隔离——一个插件崩溃不影响其他插件和核心
- [ ] P2: 热加载——运行时加载/卸载/更新插件（Phase 3+）

## 4. Non-goals

- 不在 Phase 2 实现热加载
- 不在此 RFC 中定义插件市场的分发机制（Phase 5）

## 5. Proposal

**Phase 2: 实现完整生命周期 + 异常隔离。Phase 3: 基于文件监控的热加载。**

生命周期状态机：
```
[Discovered] → Registered → Configured → Initialized → Active ⇄ Inactive → Disposed
                   ↑                          ↓
                   └──── Error ───────────────┘
```

热加载策略（Phase 3）：
1. 文件监控：`watchdog` 监控 `plugins/` 目录
2. 新 plugin.json 出现 → 自动发现 → 走正常生命周期
3. plugin.json 被修改 → 走 Deactivate → Dispose → 重新 Register
4. 请求路由：正在处理的请求完成后再卸载

## 6. Alternatives

| 方案 | 优点 | 缺点 | 为什么不选 |
|------|------|------|-----------|
| 文件监控 + 生命周期 | 简单可靠；不侵入核心代码 | 卸载时有短暂服务中断 | **采用** |
| 微服务隔离（每个插件独立进程） | 最强隔离；独立扩展 | Phase 0-3 运维复杂度过高 | Phase 5 评估 |
| WASM 沙箱 | 跨语言；安全性最强 | 性能开销；Python 生态不支持 | 未来方向，非当前可行 |

## 7. Risks

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 热加载时请求丢失 | 中 | 中 | Graceful Shutdown — 等待活跃请求完成 |
| 插件更新后不兼容旧数据 | 低 | 中 | Plugin 版本声明 + 兼容性检查 |

---

## 8. References

- [Plugin Specification](../architecture/plugin-specification.md)
- [09-plugin-system.md](../09-plugin-system.md)
