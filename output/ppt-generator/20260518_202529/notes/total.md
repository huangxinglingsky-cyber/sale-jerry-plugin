# 演讲备注

## 第1页：封面
欢迎大家参加今天的培训，主题是 Claude Code Plugin 的目录结构详解。我们将从零开始理解 Plugin 的骨架和运转机制。

## 第2页：Plugin 是什么
Claude Code Plugin 是一个可安装的扩展包，为 AI Agent 提供额外能力。它通过目录结构来组织，Claude Code 会自动发现和加载。一个 Plugin 就是一组相关能力的集合。

## 第3页：标准目录结构总览
这是 Plugin 的标准目录结构。注意，只有 .claude-plugin/plugin.json 是必须的，其他目录按需创建。

## 第4页：plugin.json 详解
plugin.json 是 Plugin 的身份证，Claude Code 通过读取这个文件来注册和识别插件。左边是一个实际示例，右边是每个字段的含义。

## 第5页：agents/ 目录
Agent 是有角色的智能调度器。它定义在 agents/ 目录下，每个 Agent 一个 .md 文件。Agent 的核心是理解用户意图，然后调度合适的 Skill 来完成任务。

## 第6页：skills/ 目录
Skill 是单一职责的可执行指令集，定义在 skills/ 目录下。每个 Skill 一个子目录，其中 SKILL.md 是必须的。Skill 目录下还可以放辅助资源。

## 第7页：.mcp.json 配置
MCP Server 是外部服务的适配器，让 AI Agent 能调用外部工具和数据源。在 .mcp.json 中声明 Plugin 依赖的 MCP Server。

## 第8页：commands/ 目录
Command 是用户侧的快捷方式，通过 /xxx 触发。注意 Command 和 Skill 的区别：Command 是入口，Skill 是实际执行逻辑。

## 第9页：运转机制
这是 Plugin 的完整运转机制。从 Claude Code 启动加载，到 Agent 识别意图调度 Skill，再到执行返回结果。Skill 有三种触发方式。

## 第10页：开发步骤拆解
最后是开发步骤。最小可用 Plugin 只需 plugin.json + 一个 SKILL.md。Agent 和 MCP 按需添加。蓝色是必须步骤，橙色可选但推荐，绿色是收尾。
