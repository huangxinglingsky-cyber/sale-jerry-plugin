# Plugin 开发团队 (plugin-dev-team)

这是一个专注于 Claude Code Plugin 开发的 AI Agent 团队，由 5 个专业 Agent 组成，覆盖从需求分析到文档发布的完整开发生命周期。

## 团队成员

| Agent | 职责 | 调用方式 |
|-------|------|---------|
| **team-lead** | 主控 Agent，识别任务阶段并调度其他 Agent | 首选入口 |
| **requirements-agent** | 需求分析，输出 PRD 和 Skill/Agent 拆解清单 | 直接调用或由 team-lead 调度 |
| **dev-agent** | 开发实现，生成 SKILL.md 和 agent.md 文件 | 直接调用或由 team-lead 调度 |
| **test-agent** | 质量审查，输出测试报告和问题清单 | 直接调用或由 team-lead 调度 |
| **docs-agent** | 文档编写，生成 README、示例和使用指南 | 直接调用或由 team-lead 调度 |

## 快速开始

### 方式一：通过 team-lead（推荐）

直接用自然语言描述需求，team-lead 会自动识别阶段并调度合适的 Agent：

```
# 需求分析
帮我分析 sale-jerry-plugin 需要新增的合同审查功能

# 开发实现
帮我开发一个合同风险分析的 Skill

# 测试验证
帮我测试 contract-risk-analyzer 这个 Skill

# 文档编写
帮我给 contract-risk-analyzer 写使用文档
```

### 方式二：直接调用专项 Agent

```
# 明确需要需求分析
@requirements-agent 分析 sale-jerry-plugin 的投标功能需求

# 明确需要开发
@dev-agent 开发 bid-analysis Skill，参考需求文档 XXX

# 明确需要测试
@test-agent 测试 f:/workspace/sale-jerry-plugin/skills/bid-analysis/SKILL.md
```

## 开发流程

```
用户需求
   │
   ▼
requirements-agent  →  需求文档 + Skill/Agent 清单
   │
   ▼
dev-agent           →  SKILL.md / agent.md 文件
   │
   ▼
test-agent          →  测试报告（PASS/FAIL）
   │
   ▼
docs-agent          →  README / 使用文档
```

## Plugin 标准规范

- **Agent 定义**: 放在 `agents/` 目录，文件名为 `{agent-name}.md`
- **Skill 定义**: 放在 `skills/{skill-name}/SKILL.md`，支持同目录下放置 context 文件
- **Context 文件**: 放在 `context/` 目录，供 Agent 参考的共享知识
- **命名规范**: 文件名使用 kebab-case（如 `bid-analysis`、`contract-parser`）

## 团队 Agent 位置

Agent 定义文件统一维护在：
- **源文件**: `agent-teams/plugin-dev-team/agents/*.md`（开发维护用）
- **生效位置**: `.claude/agents/*.md`（Claude Code 自动发现）

> 修改 Agent 后需要将变更同步到 `.claude/agents/`
