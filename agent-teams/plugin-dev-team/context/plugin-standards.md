# Plugin 开发规范

本文档定义 Claude Code Plugin 的开发标准，供团队所有 Agent 参考。

## 目录结构规范

```
{plugin-name}/
├── agents/
│   └── {agent-name}.md          # Agent 定义文件
├── skills/
│   └── {skill-name}/
│       ├── SKILL.md             # Skill 定义文件（必须）
│       └── {context-file}.md    # Skill 专属 context（可选）
├── context/
│   └── {shared-context}.md      # 跨 Skill 共享知识
└── CLAUDE.md                    # Plugin 说明（可选）
```

## SKILL.md 必需字段

```yaml
---
name: {skill-name}          # kebab-case，与目录名一致
description: {一句话描述}   # 包含核心能力关键词，供 Agent 选择时参考
category: {分类}            # 如: analysis / generation / search
priority: {high/medium/low} # 调用优先级
---
```

## SKILL.md 必需章节

| 章节 | 说明 |
|------|------|
| `## Purpose` | 功能目的，2-3句 |
| `## When to Use` | 使用场景列表 |
| `## Parameters` | 参数表格（名称/类型/必须/默认值/描述） |
| `## Instructions` | 详细执行步骤，必须可直接执行 |
| `## Output Format` | 输出模板，含成功和失败格式 |
| `## Examples` | 至少1个完整示例 |
| `## Error Handling` | 错误场景和处理方式 |

## Agent.md 必需字段

```yaml
---
name: {agent-name}          # kebab-case
description: {功能描述}     # 包含触发场景关键词示例，如 "use proactively when..."
---
```

## 参数命名规范

- 参数名: `snake_case`（如 `plugin_path`, `target_file`）
- 文件名: `kebab-case`（如 `bid-analysis`, `contract-parser`）
- 禁止缩写（如用 `description` 不用 `desc`）

## 指令编写原则

**必须具体到可执行，不能模糊**:

```
❌ "分析文件内容"
✅ "使用 Read 工具读取 {file_path}，提取其中 ## Parameters 部分的所有参数行"

❌ "处理错误"
✅ "如果文件不存在，立即返回: {status: 'error', message: '文件不存在: {path}', suggestion: '请检查路径是否正确'}"
```

## 错误输出格式约定

所有 Skill 的错误输出统一使用以下 JSON 格式：

```json
{
  "status": "error",
  "error_type": "MISSING_PARAMETER | FILE_NOT_FOUND | INVALID_FORMAT | UNKNOWN",
  "message": "具体说明什么出了问题",
  "suggestion": "用户应该如何修复"
}
```

## 成功输出格式约定

成功输出优先使用 Markdown 格式（方便用户阅读），数据部分可使用 JSON。

## 质量门禁（dev-agent 自检 + test-agent 验证）

- [ ] frontmatter 完整（name + description 必填）
- [ ] 必需参数有校验步骤
- [ ] 指令步骤具体可执行（无模糊动词）
- [ ] 输出有完整模板
- [ ] 至少1个使用示例
- [ ] 主要错误场景有处理
- [ ] 无硬编码业务数据
