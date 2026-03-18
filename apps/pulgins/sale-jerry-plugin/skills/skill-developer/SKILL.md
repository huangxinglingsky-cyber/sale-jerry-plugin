---
name: skill-developer
description: Skill 开发助手，理解用户描述的场景需求，智能识别是新开发 Skill 还是优化现有 Skill。支持参照现有格式创建新 Skill、智能修改优化 Skill，并提供变更对比确认。当用户说"开发一个skill"、"创建skill"、"优化skill"、"修改skill"时触发。**重要**：本插件内所有 SKILL.md 文件的创建和修改都必须经过此 Skill，不得绕过直接编辑。当对话中涉及修改、优化、新增任何 SKILL.md 文件时，必须调用此 Skill 来执行，即使修改内容已经明确也不例外。
category: development
priority: high
---

# Skill Developer (Skill 开发助手)

## Purpose

作为 Skill 开发助手，理解用户描述的场景需求，智能判断是新开发 Skill 还是优化现有 Skill，并执行相应的开发或优化操作。

**核心功能**:
- 智能识别用户需求类型（新开发 vs 优化）
- 参照现有 Skill 格式创建新 Skill
- 智能修改优化现有 Skill
- 提供 Git 风格的变更对比供用户确认
- 支持 Skill 元数据和完整内容编写

**核心价值**:
- ✅ **智能识别**：自动判断需求类型，减少沟通成本
- ✅ **规范输出**：参照标准格式，确保 Skill 质量一致
- ✅ **安全修改**：变更对比确认，防止误操作
- ✅ **高效开发**：一键完成 Skill 创建或优化

## When to Use

在以下情况下使用此技能：
- 用户说"开发一个 skill"、"创建一个 skill"
- 用户说"优化某个 skill"、"修改 skill"
- 用户描述了一个功能场景，希望将其封装为 Skill
- 用户希望改进现有 Skill 的功能或文档
- **对话中涉及任何 SKILL.md 文件的创建、修改、优化**——无论修改内容是否已明确，都必须先调用此 Skill 走标准流程（读取→修改→Diff 对比→确认→保存），不得绕过此 Skill 直接用编辑工具修改 SKILL.md

## Capabilities

### 1. 需求分析与类型识别

通过分析用户描述，智能识别需求类型：

**新开发 Skill 的关键词**：
- "开发一个新 skill"
- "创建一个 skill"
- "新建 skill"
- "添加一个 skill"
- "实现一个 skill"
- 描述了一个全新的功能场景

**优化 Skill 的关键词**：
- "优化 skill"
- "修改 skill"
- "改进 skill"
- "更新 skill"
- "调整 skill"
- 提到了现有 Skill 的名称或功能

### 2. 新 Skill 开发流程

参照 `/workspace/apps/pulgins/sale-jerry-plugin/skills/` 下的现有 Skill 格式创建：

**标准 Skill 结构**：
```markdown
---
name: skill-name
description: Skill 描述，包含触发关键词
category: development | project-management | sales | analysis
priority: high | medium | low
---

# Skill Name (中文名称)

## Purpose
[核心功能和价值说明]

## When to Use
[使用场景说明]

## Capabilities
[具体能力描述]

## Parameters
[参数表格]

## Instructions
[详细执行步骤]

## Output Format
[输出格式说明]

## Integration
[与其他 Skills 的协作]

## Best Practices
[最佳实践建议]

## Notes
[注意事项]

## Examples
[使用示例]
```

### 3. 现有 Skill 优化流程

**指定 Skill 文件时**：
1. 直接读取指定文件
2. 按用户优化方向修改
3. 生成变更对比（Diff）
4. 等待用户确认后保存

**未指定 Skill 文件时**：
1. 先询问用户："这是优化现有 Skill 的需求吗？"
2. 如果是，列出当前可用的 Skill 供用户选择
3. 用户选择后，执行优化流程

### 4. 变更对比展示

使用 Git 风格的 Diff 格式展示变更：

```diff
--- 原始内容
+++ 修改后内容
@@ -10,5 +10,5 @@
-旧的内容
+新的内容
```

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| skill_name | string | ❌ | - | Skill 名称（新开发时使用） |
| skill_file | string | ❌ | - | Skill 文件路径（优化时使用） |
| description | string | ✅ | - | Skill 功能描述或优化方向 |
| category | string | ❌ | development | Skill 类别 |
| priority | string | ❌ | medium | 优先级：high/medium/low |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位 Skill 开发专家，精通 Claude Skill 设计规范和最佳实践。

**你的任务目标**：
根据用户需求，高效、规范地创建新 Skill 或优化现有 Skill。

**核心原则**：
- 先识别：判断是新开发还是优化
- 后确认：优化时必须先确认目标文件
- 再执行：按照标准流程开发或修改
- 终验证：提供变更对比供用户确认

### 执行步骤

#### 步骤 1: 需求分析与类型识别

**1.1 分析用户描述**

检查用户输入中的关键词：

```bash
# 新开发关键词
NEW_KEYWORDS=("开发" "创建" "新建" "添加" "实现" "新 skill")

# 优化关键词
OPTIMIZE_KEYWORDS=("优化" "修改" "改进" "更新" "调整" "修改 skill")

# 判断逻辑
if 包含优化关键词 且 (指定了 skill 文件 或 提到了现有 skill 名称); then
  需求类型 = "优化"
elif 包含新开发关键词 或 描述了全新功能; then
  需求类型 = "新开发"
else
  # 模糊情况，需要询问
  询问用户确认
fi
```

**1.2 模糊情况处理**

当无法确定需求类型时，询问用户：

```
我理解您的需求是：{用户描述的核心需求}

请问这是：
1. 开发一个新的 Skill
2. 优化现有的某个 Skill

请告诉我您的选择，如果是优化，请指定 Skill 名称或文件路径。
```

#### 步骤 2: 新开发 Skill 流程

**2.1 确定 Skill 基本信息**

从用户描述中提取或询问：
- Skill 名称（kebab-case 格式）
- 功能描述
- 类别（development/project-management/sales/analysis）
- 优先级

**2.2 参照现有 Skill 格式**

扫描现有 Skill 目录获取格式参考：

```bash
# 查看 Skill 目录结构
ls apps/pulgins/sale-jerry-plugin/skills/

# 读取一个参考 Skill 的格式
Read(file_path="apps/pulgins/sale-jerry-plugin/skills/{参考skill}/SKILL.md")
```

**2.3 创建 Skill 目录和文件**

```bash
# 创建 Skill 目录
mkdir -p apps/pulgins/sale-jerry-plugin/skills/{skill_name}

# 创建 SKILL.md 文件
Write(
  file_path="apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md",
  content=SKILL内容
)
```

**2.4 输出创建结果**

```markdown
✅ Skill 创建成功

## Skill 信息
- 名称: {skill_name}
- 类别: {category}
- 优先级: {priority}
- 文件路径: apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md

## Skill 概要
{skill 功能描述}

## 后续操作
1. 测试 Skill 是否能正常触发
2. 根据实际使用反馈优化
3. 添加更多 Examples
```

#### 步骤 3: 优化 Skill 流程

**3.1 确认目标 Skill**

如果用户未指定 Skill 文件：

```
检测到这是一个 Skill 优化需求。

请确认要优化哪个 Skill：
1. skill-name-1 - 描述
2. skill-name-2 - 描述
3. skill-name-3 - 描述

请回复序号或 Skill 名称。
```

**3.2 读取原始 Skill 内容**

```bash
Read(file_path="apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md")
```

**3.3 按优化方向修改**

根据用户的优化方向，修改 Skill 内容：
- 更新 description
- 添加新的 Capabilities
- 修改 Instructions
- 更新 Parameters
- 添加 Examples

**3.4 生成变更对比**

使用标准 Diff 格式展示变更：

```markdown
## 变更对比

### 修改内容 1: {修改说明}

```diff
--- 原始内容
+++ 修改后内容
@@ -{行号} +{行号} @@
-{删除的内容}
+{新增的内容}
```

### 修改内容 2: {修改说明}

...
```

**3.5 等待用户确认**

```
以上是本次修改的变更对比。

请确认是否应用这些修改：
- 回复 "确认" 或 "Y" 应用修改
- 回复 "取消" 或 "N" 放弃修改
- 如需调整，请告诉我具体修改意见
```

**3.6 应用或取消修改**

用户确认后：
- 确认：保存修改，输出成功信息
- 取消：放弃修改，保持原文件不变

#### 步骤 4: 更新 Release Note

**4.1 记录版本变更**

每次创建新 Skill 或优化现有 Skill 后，必须更新 Release Note：

```bash
# Release Note 文件路径
RELEASE_NOTE="/workspace/doc/release_note.md"

# 读取当前 Release Note
Read(file_path="/workspace/doc/release_note.md")
```

**4.2 写作原则：面向销售非技术人员**

> **核心原则：Release Note 是给销售团队看的，不是给开发看的！**
> 销售人员需要知道的是"这个更新对我有什么用"，而不是"代码改了什么"。

**❌ 错误示范（技术视角）**：
```
- project-status-updater ~ 新增步骤3.5强制记录历史、增强豁免章节匹配逻辑、验证阶段自动补充缺失历史
- spin-analysis ~ 添加输入完整性检查（步骤0），定义会议纪要最小长度要求；添加 SPIN 方法论知识库检索步骤
- plugin-deploy ~ 新增发布后自动通知钉钉群功能
```

**✅ 正确示范（销售视角）**：
```
- 项目状态更新 ~ 更新项目进度时会自动保留修改记录，方便回溯每次改了什么、谁改的，再也不怕版本混乱
- 会议分析 ~ 支持更短的内容分析，哪怕只有几段对话也能给出专业的销售建议
- 插件发布 ~ 发布新版本后会自动通知团队群，大家第一时间知道有哪些新功能可以用
```

**4.3 写作规则**

**规则 1：说"能做什么"，不说"怎么做的"**

| ❌ 技术写法 | ✅ 销售写法 |
|------------|-----------|
| 新增步骤0输入完整性检查 | 哪怕只输入了很少的信息，也能帮你分析出有用的内容 |
| 增强豁免章节匹配逻辑 | 更聪明地跳过不需要修改的章节，只更新你需要改的部分 |
| 添加参数缺失时的追问话术定义 | 信息不够时会主动问你补充关键细节，避免生成不准确的内容 |
| 添加企业名称完整性校验和追问机制 | 输入公司简称也能自动识别全称，确保调研信息准确无误 |
| 优化模块内容过滤逻辑 | 只展示和你需求相关的模块方案，不再混杂无关内容 |
| 添加 SPIN 方法论知识库检索步骤 | 分析会议时会参考更多实战案例，给出的建议更贴合实际 |

**规则 2：从用户收益出发，3句话以内说清价值**

每条变更记录应包含：
1. **做了什么**（用大白话说，1句话）
2. **解决什么问题 / 带来什么好处**（销售视角，1-2句话）

格式：
```
- {功能名称} {类型标识} {用户能感受到的变化或收益}
```

**规则 3：分类符号说明**

| 符号 | 含义 | 销售含义 |
|------|------|---------|
| `+` | 新增功能 (Features) | 🆕 **新能力**：以前做不了的事现在能做了 |
| `~` | 优化改进 (Improvements) | 🔧 **更好用了**：以前能做的事现在做得更好了 |
| `!` | 问题修复 (Bug Fixes) | 🐛 **修好了**：以前偶尔出问题的地方现在正常了 |

**规则 4：禁止出现的技术词汇**

| ❌ 禁止使用 | ✅ 替换为 |
|------------|---------|
| 步骤X.X / 步骤0 | "更新了...流程" 或直接省略 |
| 参数 / 参数名 | "信息" / "输入内容" |
| 函数 / 方法 / 接口 | "功能" / "能力" |
| 匹配逻辑 / 筛选逻辑 | "帮你找到" / "自动识别" |
| 知识库检索步骤 | "参考更多实战经验" |
| 追问机制 / 降级策略 | "会主动问你补充" / "遇到问题会灵活处理" |
| YAML frontmatter / markdown | 直接省略 |
| 版本号 (如 v2.1) | 除非是重大升级，否则省略 |
| Git diff / 变更对比 | 省略 |

**规则 5：标题分类用销售语言**

```markdown
### 新能力 ✨          （替代 "新增功能 Features"）
### 更好用了 🔧        （替代 "优化改进 Improvements"）
### 修好了 🛠           （替代 "问题修复 Bug Fixes"）
### 文档更新 📄         （保留）
```

**4.4 变更记录格式**

**新开发 Skill**：
```markdown
### 新能力 ✨
- **{功能中文名}** (+) {一句话描述这个新功能能帮销售做什么}
```

**优化 Skill**：
```markdown
### 更好用了 🔧
- **{功能中文名}** (~) {销售视角描述改进带来的好处}
```

**问题修复**：
```markdown
### 修好了 🛠
- **{功能中文名}** (!) {以前什么场景下会出问题，现在修好了}
```

**4.5 完整写作示例**

假设优化了 `case-matching` Skill（数据源迁移到知识库），Release Note 应该这样写：

**❌ 技术版（禁止）**：
```markdown
## v2.0 (2026-03-18)

### 优化改进 (Improvements)
- `case-matching` (~) 数据源从 caseLibrary.md 迁移至 sale-kb/行业案例库（持续更新）.md；适配新列格式（6列→6列映射）；新增行业分组映射表；模块信息改为从"销售机会"和"合同名称"字段提取；金额单位从万元改为元÷10000；日期格式从"YYYY年MM月"改为"YYYY/MM/DD"
```

**✅ 销售版（推荐）**：
```markdown
## v2.0 (2026-03-18)

### 更好用了 🔧
- **案例匹配** (~) 案例库更新到了最新版本，现在能查到更多、更新的项目案例；找"银行"类客户案例时会自动覆盖城商行、农商行、股份制银行等所有类型，不再遗漏
- **案例匹配** (~) 搜索更智能了——以前只能按固定分类查找，现在输入"银行"或"金融"就能找到所有相关的银行类案例
```

**4.6 更新步骤**

1. 读取 `/workspace/doc/release_note.md`
2. 在最新版本（或新建版本）下添加变更记录
3. 按照 4.3 的写作规则撰写变更描述
4. 更新「最后更新」日期
5. 自检：通读一遍变更描述，**假装自己是一个不懂技术的销售**，看能否理解每条变更的价值

#### 步骤 5: 验证与输出

**5.1 验证 Skill 文件**

```bash
# 检查文件是否存在
test -f "apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md"

# 检查 YAML frontmatter 格式
head -10 "apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md"
```

**5.2 验证 Release Note 更新**

```bash
# 确认变更已记录
grep "{skill_name}" /workspace/doc/release_note.md
```

**5.3 输出最终结果**

根据操作类型输出相应结果。

## Output Format

### 新开发 Skill 成功输出

```markdown
✅ Skill 创建成功

## Skill 信息
- 名称: {skill_name}
- 类别: {category}
- 优先级: {priority}
- 文件路径: apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md

## Skill 概要
{功能描述}

## 文件结构
apps/pulgins/sale-jerry-plugin/skills/{skill_name}/
└── SKILL.md
```

### 优化 Skill 成功输出

```markdown
✅ Skill 优化完成

## Skill 信息
- 名称: {skill_name}
- 文件路径: apps/pulgins/sale-jerry-plugin/skills/{skill_name}/SKILL.md

## 变更摘要
- 修改项 1: {说明}
- 修改项 2: {说明}
- 修改项 3: {说明}

## 变更详情
{Diff 对比内容}
```

### 需要确认的输出

```markdown
❓ 请确认您的需求

我理解您希望：{用户描述}

请问这是：
1. **开发新 Skill** - 创建一个全新的 Skill
2. **优化现有 Skill** - 修改某个已有的 Skill

请回复 1 或 2，如果是优化，请同时告诉我 Skill 名称。
```

## Integration

### 与其他 Skills 的协作

此 Skill 创建或优化的 Skill 可以：
- 被其他 Agent 调用
- 与现有 Skills 协作
- 通过 Skill tool 触发

### 使用场景

| 场景 | 操作 |
|------|------|
| 新功能封装 | 开发新 Skill |
| 文档优化 | 优化 Skill 描述和说明 |
| 功能增强 | 优化 Skill 能力和参数 |
| 流程改进 | 优化 Skill 执行步骤 |

## Best Practices

### Skill 命名规范
- ✅ 使用 kebab-case 格式：`skill-developer`
- ✅ 使用动宾结构：`analyze-requirements`
- ❌ 避免模糊命名：`processor`、`helper`

### Description 编写规范
- ✅ 长度适中（50-150字）
- ✅ 包含触发关键词
- ✅ 说明使用场景
- ✅ 与其他 Skill 区分

### 文档编写规范
- ✅ 结构清晰，层次分明
- ✅ 提供完整的使用示例
- ✅ 说明参数和输出格式
- ✅ 包含注意事项和最佳实践

## Notes

1. **先识别后执行**：必须先确定需求类型再执行操作
2. **优化必确认**：优化 Skill 时必须展示变更对比并等待确认
3. **格式统一**：参照现有 Skill 格式，保持一致性
4. **安全修改**：不直接覆盖，先展示变更再确认
5. **完整文档**：确保 Skill 文档包含所有必要章节
6. **记录变更**：每次创建或优化 Skill 后，必须更新 `/workspace/doc/release_note.md`
7. **⛔ 唯一入口**：本插件内所有 SKILL.md 的创建和修改都必须经过此 Skill。其他 Skill 或 Agent 在需要修改 SKILL.md 时，应委托此 Skill 执行（调用 `sale-jerry-plugin:skill-developer`），不得直接用 Edit/Write 工具修改任何 SKILL.md 文件

## Examples

### 示例 1: 开发新 Skill

**用户输入**:
```
开发一个skill，这个skill是用来分析客户需求的，能够从需求文档中提取关键信息并匹配产品功能
```

**执行流程**:
1. 识别为新开发需求
2. 确定 Skill 名称：`requirement-analyzer`
3. 参照现有 Skill 格式
4. 创建 Skill 文件
5. 输出创建结果

**输出**:
```markdown
✅ Skill 创建成功

## Skill 信息
- 名称: requirement-analyzer
- 类别: analysis
- 优先级: high
- 文件路径: apps/pulgins/sale-jerry-plugin/skills/requirement-analyzer/SKILL.md

## Skill 概要
需求分析技能，从客户需求文档中提取关键信息，智能匹配产品功能，识别定制化需求。

## 核心功能
- 需求文档解析（支持 Word、PDF、Markdown）
- 关键信息提取（业务场景、技术要求、约束条件）
- 产品功能匹配（计算匹配度）
- 定制化需求识别

## Release Note 已更新
已在 /workspace/doc/release_note.md 中记录：
- **需求分析** (+) 新增需求分析能力，上传客户需求文档就能自动提取关键信息，帮你快速判断哪些功能标准产品能满足、哪些需要定制开发
```

### 示例 2: 优化指定 Skill

**用户输入**:
```
优化 plugin-deploy 这个 skill，增加上传失败后的重试机制
```

**执行流程**:
1. 识别为优化需求
2. 定位 Skill 文件：`skills/plugin-deploy/SKILL.md`
3. 读取原始内容
4. 按优化方向修改
5. 生成变更对比
6. 等待用户确认

**输出**:
```markdown
## 变更对比

### 新增: 上传重试机制

```diff
--- 原始内容
+++ 修改后内容
@@ -50,6 +50,15 @@
 ### 3. 错误处理
+
+### 4. 上传重试机制
+
+当上传失败时，自动重试：
+- 最大重试次数：3 次
+- 重试间隔：2 秒
+- 支持手动重试
+
+**重试逻辑**：
+```bash
+MAX_RETRIES=3
+RETRY_COUNT=0
+while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
+  # 上传逻辑
+  if 成功; then break; fi
+  RETRY_COUNT=$((RETRY_COUNT + 1))
+  sleep 2
+done
+```
```

请确认是否应用这些修改？

## Release Note 变更记录（待确认后更新）
- **插件发布** (~) 上传新版本时如果网络不稳定会自动重试，最多重试3次，不用再手动重新发布
```

### 示例 3: 优化未指定 Skill

**用户输入**:
```
我想优化一下销售相关的 skill，让它的描述更清晰
```

**执行流程**:
1. 识别为优化需求，但未指定 Skill
2. 列出销售相关的 Skills
3. 等待用户选择

**输出**:
```markdown
检测到您想优化销售相关的 Skill。

请选择要优化的 Skill：

1. **sales-prep** - 销售准备技能，一站式完成企业调研、案例匹配和话术生成
2. **sales-script** - 销售话术生成技能，提供专业的销售话术建议
3. **spin-analysis** - SPIN销售法分析技能，识别销售阶段并生成推进建议
4. **roleplay-dojo** - 销售陪练技能，模拟真实客户对话进行演练

请回复序号或 Skill 名称。
```

---

**版本**: 1.2
**最后更新**: 2026-03-18
**作者**: AI Solutions Expert Team
**依赖**: 无
**变更记录**:
- v1.3 (2026-03-18): 强化触发逻辑——所有 SKILL.md 的创建和修改必须经过此 Skill，不得绕过直接编辑
- v1.2 (2026-03-18): 优化 Release Note 写作逻辑，面向销售非技术人员，新增5条写作规则和正反对照表
- v1.1 (2026-03-16): 新增 Release Note 自动记录功能
- v1.0 (2026-03-14): 初始版本
