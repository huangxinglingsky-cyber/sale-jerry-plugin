# Claude Code Plugin 目录结构详解

## 第1页：封面

标题：Claude Code Plugin 目录结构详解
副标题：从零理解 Plugin 的骨架与运转机制
日期：2026-05-18

---

## 第2页：Plugin 是什么

- Claude Code Plugin 是一个可安装的扩展包，为 AI Agent 提供额外的能力（Skills）和角色（Agents）
- Plugin 通过目录结构来组织，Claude Code 会自动发现并加载这些文件
- 一个 Plugin = 一组相关能力的集合（如"销售辅助"、"开发工具"）

---

## 第3页：标准目录结构总览

展示标准结构树：

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin 元数据（必须）
├── .mcp.json            # MCP Server 配置（可选）
├── commands/            # 斜杠命令（可选）
├── agents/              # Agent 定义（可选）
├── skills/              # Skill 定义（可选）
└── README.md            # 文档说明（可选）
```

标注：只有 .claude-plugin/plugin.json 是必须的，其余按需创建

---

## 第4页：.claude-plugin/plugin.json — Plugin 的身份证

- 唯一必须存在的文件，定义 Plugin 的核心元数据
- 包含字段：name（插件名）、version（版本号）、description（描述）、author（作者）、agents（Agent 文件路径列表）、skills（Skill 目录路径）
- Claude Code 通过读取此文件来注册和识别 Plugin
- 示例 JSON：

```json
{
  "name": "sale-jerry-plugin",
  "version": "1.0.16",
  "description": "sale",
  "author": {
    "name": "UwinTech-销售经理",
    "email": "jerry@easyops.cn"
  },
  "license": "MIT",
  "agents": ["./agents/sales-master.md"],
  "skills": "./skills/"
}
```

---

## 第5页：agents/ — Agent 定义目录

- 定位：定义具有独立角色和判断能力的 AI 代理
- 放置文件：每个 Agent 一个 .md 文件（如 sales-master.md）
- Agent 的核心要素：身份（Identity）、能力（Capabilities）、工作流程（Workflow）、指令（Instructions）
- Agent 可以智能判断场景并自动调度 Skills
- 名词解释：Agent = 有角色的智能调度器，能理解上下文并编排多个 Skill 完成复杂任务
- 文件格式：YAML frontmatter（name + description） + Markdown 正文

---

## 第6页：skills/ — Skill 定义目录

- 定位：定义具体的原子能力，每个 Skill 是一个独立的可执行任务单元
- 目录结构：每个 Skill 一个子目录，子目录中必须包含 SKILL.md
- SKILL.md 的核心要素：Purpose（目的）、Parameters（参数）、Instructions（执行指令）、Examples（示例）
- Skill 目录下可包含辅助资源：references/（参考文档）、scripts/（脚本）、config/（配置）、resource/（资源文件）
- 名词解释：Skill = 单一职责的可执行指令集，类似一个"工具"或"能力卡片"

---

## 第7页：.mcp.json — MCP Server 配置

- 定位：声明 Plugin 依赖的外部 MCP Server（Model Context Protocol）
- 放置文件：一个 .mcp.json 文件在 Plugin 根目录
- 用途：当 Plugin 需要访问外部服务（如数据库、API、记忆系统）时，通过 MCP Server 桥接
- 示例：claude-mem（记忆系统）、钉钉 API 等
- 名词解释：MCP Server = 外部服务的适配器，让 AI Agent 能调用外部工具和数据源

---

## 第8页：commands/ — 斜杠命令目录（可选）

- 定位：定义用户可通过 /command 触发的快捷命令
- 放置文件：每个命令一个 .md 文件
- 与 Skills 的区别：Commands 是用户主动触发的快捷入口，Skills 是被调用的能力单元
- 名词解释：Command = 用户侧的快捷方式，输入 /xxx 即可触发对应流程

---

## 第9页：Plugin 运转机制

- 加载流程：Claude Code 启动 → 读取 plugin.json → 注册 Agents 和 Skills → 用户对话时自动匹配
- Agent 调度：用户发消息 → Agent 识别意图 → 选择合适的 Skill → 执行 Skill 指令 → 返回结果
- Skill 被触发的方式：1) Agent 自动调度 2) 用户通过 /skill-name 手动调用 3) 其他 Skill 内部调用
- 数据流：用户输入 → Agent（理解意图）→ Skill（执行任务）→ 输出结果

---

## 第10页：开发步骤拆解

- 步骤1：创建 plugin.json，定义插件名称和基本信息
- 步骤2：规划 Skill 拆分，每个独立功能点对应一个 Skill
- 步骤3：编写 SKILL.md，定义参数、指令、输出格式和示例
- 步骤4：（可选）创建 Agent，编排多个 Skill 的调度逻辑
- 步骤5：（可选）配置 .mcp.json 接入外部服务
- 步骤6：本地测试 → 打包部署 → 发布上线
