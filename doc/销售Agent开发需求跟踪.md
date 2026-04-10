# 销售 Agent 开发需求跟踪

---

## 看板

**高优先级**
- [ ] **BUG-001** 项目状态文件更新不及时 `待分配`

**中优先级**
- (暂无)

**低优先级**
- (暂无)

---

## Bug 详情

### BUG-001: 项目状态文件更新不及时

**问题**：中证指数空间的项目状态 md 文件更新不及时

**现象**：
1. 人员信息未持续更新
2. 跟进记录未追加
3. 最后更新日期未刷新

**根因**：

| 问题 | 原因 | 涉及 |
|------|------|------|
| 人员未同步 | `stakeholder-input` 只更新 `项目相关方.md`，未同步到 `项目状态.md` | stakeholder-input |
| 记录未追加 | `project-status-updater` 被动调用，无自动捕获机制 | project-status-updater |
| 日期未刷新 | 只追加"更新日志"表格，未更新头部"最后更新"字段 | project-status-updater |

**修复方案**：
1. `stakeholder-input` 更新后调用 `project-status-updater` 同步
2. `project-status-updater` 每次更新时刷新"最后更新"字段

**进展**：2026-04-08 完成根因分析

---

## 已完成

| 日期 | 名称 | 说明 |
|------|------|------|
| 04-04 | 日报周末判断修复 | 判断"昨天"而非"今天"（v1.4.1）|
| 04-04 | 日报会话查询修复 | dateEnd 参数自动加一天（v1.4.1）|
| 04-03 | FABE 方案生成 | 新增 skill，支持 Markdown 和 Word（v1.4.0）|

---

## 相关链接

- [发布日志](./release_note.md)
- [Plugin 测试报告分析](./Plugin测试报告分析.md)
- [技能开发规范](../agent-teams/plugin-dev-team/context/plugin-standards.md)
