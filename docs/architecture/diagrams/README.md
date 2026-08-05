# Architecture Diagrams — Index

> Athena Knowledge Platform 架构可视化
> 共 12 张 Mermaid 图

---

## 图示索引

| # | 图名 | 文件 | 类型 |
|---|------|------|------|
| 1 | System Context | [c4-model.md](c4-model.md) | C4 Level 1 |
| 2 | Container Diagram | [c4-model.md](c4-model.md) | C4 Level 2 |
| 3 | Component Diagram | [c4-model.md](c4-model.md) | C4 Level 3 |
| 4 | Knowledge Pipeline | [pipeline-diagrams.md](pipeline-diagrams.md) | Flowchart |
| 5 | Event Pipeline | [pipeline-diagrams.md](pipeline-diagrams.md) | Flowchart |
| 6 | Deployment Diagram | [deployment-domain.md](deployment-domain.md) | Topology |
| 7 | Domain Diagram | [deployment-domain.md](deployment-domain.md) | Context Map |
| 8 | Plugin Architecture | [plugin-agent.md](plugin-agent.md) | Structure |
| 9 | Agent Architecture | [plugin-agent.md](plugin-agent.md) | Structure |
| 10 | Data Flow | [dataflow-sequence.md](dataflow-sequence.md) | Flowchart |
| 11 | Database ER | [dataflow-sequence.md](dataflow-sequence.md) | ER Diagram |
| 12 | Sequence Diagram | [dataflow-sequence.md](dataflow-sequence.md) | Sequence |

---

## 阅读顺序建议

1. **System Context** → 理解 Athena 在生态系统中的位置
2. **Container Diagram** → 理解内部容器和通信
3. **Domain Diagram** → 理解业务领域的划分
4. **Knowledge Pipeline** → 理解核心数据处理流程
5. **Data Flow** → 理解数据如何在组件间流动
6. **Event Pipeline** → 理解异步通信机制
7. **Component Diagram** → 理解应用服务器内部结构
8. **Plugin Architecture** → 理解扩展机制
9. **Agent Architecture** → 理解 AI 自主运行方式
10. **Deployment Diagram** → 理解生产环境拓扑
11. **Sequence Diagram** → 理解端到端用户流程
12. **Database ER** → 理解数据存储结构

---

## 相关文档

- [../overview.md](../overview.md) — 架构总览
- [../../BLUEPRINT.md](../../BLUEPRINT.md) — 施工蓝图
- [../../database/er-diagram.md](../../database/er-diagram.md) — 完整 ER 图
- [../../domain/graph-model.md](../../domain/graph-model.md) — Neo4j 图模型
