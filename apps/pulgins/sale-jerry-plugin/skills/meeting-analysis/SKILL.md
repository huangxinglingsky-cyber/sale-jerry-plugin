---
name: meeting-analysis
description: 会议纪要分析技能，基于SPIN销售法分析会议内容，判断销售阶段并生成推进建议。自动生成会议分析报告和销售话术，保存到项目目录
category: sales
priority: high
---

# Meeting Analysis (会议纪要分析技能)

## Purpose

基于SPIN销售法分析销售会议纪要，自动判断销售阶段并提供针对性的推进建议。

**核心功能**:
- 会议纪要文件解读（支持 PDF、Word、图片格式）
- SPIN销售法分析（S-P-I-N四维度识别）
- 销售阶段智能判断
- 生成会议分析报告
- 生成销售话术
- 自动更新项目状态

**核心价值**:
- ✅ **专业分析**：基于SPIN销售法的科学分析框架
- ✅ **阶段判断**：准确识别客户所处的销售阶段
- ✅ **推进建议**：提供具体可执行的下一步行动
- ✅ **自动归档**：所有文件自动保存到项目目录
- ✅ **真实性第一**：严格基于会议纪要实际内容，禁止虚构

## When to Use

在以下情况下使用此技能：
- 客户会议结束后需要分析会议内容
- 需要判断客户当前的销售阶段
- 需要生成会议分析报告
- 需要基于会议内容生成销售话术

## Capabilities

### 1. 会议纪要文件处理

**支持格式**：
- PDF文件
- Word文档（.docx/.doc）
- 图片文件（OCR识别）
- Markdown文件

**自动归档**：
- 将会议纪要文件移动到 `{项目名称}/售前阶段/05_会议纪要/`
- 保持原文件名或按日期重命名

### 2. SPIN销售法分析

**SPIN四维度**：
- **S (Situation)**: 背景问题 - 了解客户现状
- **P (Problem)**: 难点问题 - 挖掘客户痛点
- **I (Implication)**: 暗示问题 - 放大问题影响
- **N (Need-payoff)**: 需求-效益问题 - 展示解决方案价值

**分析内容**：
- 提取会议中的SPIN信息
- 识别客户痛点和需求
- 分析客户关注点
- 评估客户意向强度

### 3. 销售阶段判断

**支持的销售阶段**：
- 需求调研 - 了解客户背景和需求
- 立项中 - 客户内部立项流程进行中
- 已立项 - 项目已获批准，进入采购流程
- POC - 概念验证阶段
- 招投标 - 正式招投标流程
- 实施中 - 项目实施阶段
- 验收中 - 项目验收阶段
- 已完成 - 项目已完成

**判断依据**：
- 会议中客户的明确表述
- 讨论的主题和深度
- 客户的决策进度
- 下一步行动计划

### 4. 报告和话术生成

**会议分析报告**（保存到 售前阶段/05_会议纪要/）：
- 会议基本信息
- SPIN分析结果
- 销售阶段判断
- 客户痛点总结
- 下一步行动建议

**销售话术**（保存到 售前阶段/11_通用资料/）：
- 基于会议内容的定制化话术
- 针对客户痛点的解决方案呈现
- 推进项目的具体话术
- 异议处理话术

### 5. 项目状态更新

**自动更新内容**：
- 更新项目当前阶段
- 记录会议分析历史
- 更新下一步行动计划

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| project_name | string | ✅ | - | 完整的项目名称，格式：`客户名称-项目名称` |
| file_path | string | ❌ | auto | 会议纪要文件路径，不指定则扫描05_会议纪要目录 |
| meeting_date | string | ❌ | today | 会议日期，格式：YYYY-MM-DD |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位资深的销售分析专家，精通SPIN销售法，专门分析销售会议纪要并提供推进建议。

**你的任务目标**：
基于会议纪要进行SPIN分析，判断销售阶段，生成分析报告和销售话术。

**核心原则**：
- 真实性第一：严格基于会议纪要实际内容
- 禁止虚构：不编造任何不存在的信息
- 完整流程：必须完成所有步骤，不得中途停止

---

### 步骤 0: 输入完整性校验（必须执行）

**⚠️ 重要：在开始会议分析前，必须先校验输入有效性**

**0.1 检查必需参数**

| 参数 | 检查项 | 处理方式 |
|------|-------|---------|
| project_name | 不能为空 | 为空则返回错误，要求提供项目名称 |
| project_name | 项目目录存在 | 不存在则提示先初始化项目 |
| file_path | 文件存在 | 不存在则扫描05_会议纪要目录或返回错误 |

**0.2 校验结果处理**

```json
// 校验失败 - project_name 为空
{
  "status": "error",
  "error_type": "missing_project_name",
  "message": "请提供项目名称（project_name 参数）",
  "suggestion": "项目名称格式：客户名称-项目名称，如 'XX银行-CMDB项目'"
}

// 校验失败 - 项目目录不存在
{
  "status": "error",
  "error_type": "project_not_found",
  "message": "项目目录不存在: {project_name}",
  "suggestion": "请先使用 project-init skill 初始化项目目录"
}
```

---

### 步骤 1: 项目验证

使用 Glob 工具检查项目目录是否存在：
```
Glob(pattern: "{project_name}")
```

如果不存在，提示用户先初始化项目。

#### 步骤 2: 会议纪要文件处理

**2.1 文件定位**：
- 如果提供了 file_path，使用指定文件
- 如果未提供，扫描 `{project_name}/售前阶段/05_会议纪要/` 目录

**2.2 文件移动**（如果文件不在项目目录）：
```bash
# 移动文件到项目目录
mv "{file_path}" "{project_name}/售前阶段/05_会议纪要/会议纪要-{date}.{ext}"
```

**2.3 文件读取**：
- Markdown / TXT：直接使用大模型原生能力读取文本内容
- 图片：直接使用大模型原生 OCR 能力识别文字
- PDF / Word 等其他格式：调用 document-processor skill 读取文件内容

#### 步骤 3: SPIN销售法分析

调用 spin-analysis skill 进行分析：
```javascript
Skill(
  skill: "spin-analysis",
  args: {
    "meeting_content": "{会议纪要内容}",
    "customer_name": "{客户名称}"
  }
)
```

获取SPIN分析结果：
- S维度信息
- P维度信息
- I维度信息
- N维度信息
- 销售阶段判断

#### 步骤 4: 生成会议分析报告

保存位置：`{project_name}/售前阶段/05_会议纪要/会议分析-{date}.md`

报告格式：
```markdown
# 会议分析报告

**项目名称**: {project_name}
**会议日期**: {meeting_date}
**分析时间**: {YYYY-MM-DD HH:MM:SS}

---

## 📊 SPIN分析

### S (Situation) - 背景问题
{S维度分析结果}

### P (Problem) - 难点问题
{P维度分析结果}

### I (Implication) - 暗示问题
{I维度分析结果}

### N (Need-payoff) - 需求-效益问题
{N维度分析结果}

---

## 🎯 销售阶段判断

**当前阶段**: {销售阶段}
**判断依据**: {判断依据}

---

## 💡 下一步行动建议

{推进建议}

---

*本报告由 meeting-analysis skill 自动生成*
```

#### 步骤 5: 生成销售话术

调用 sales-script skill 生成话术：
```javascript
Skill(
  skill: "sales-script",
  args: {
    "customer_info": "{客户信息}",
    "spin_analysis": "{SPIN分析结果}",
    "scenario": "meeting_followup"
  }
)
```

保存位置：`{project_name}/售前阶段/11_通用资料/话术-会议跟进-{date}.md`

#### 步骤 6: 更新项目状态

调用 project-status-updater skill：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "当前阶段",
    "content": "{销售阶段}",
    "operation": "replace"
  }
)
```

添加更新日志：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "更新日志",
    "content": "| {date} | meeting-analysis | 完成会议分析，当前阶段：{阶段} |",
    "operation": "append"
  }
)
```

**添加会话轨迹记录**（推荐）：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "会话轨迹",
    "content": "| {YYYY-MM-DD HH:mm:ss} | meeting-analysis | 分析会议纪要，识别客户痛点：{痛点摘要}。销售阶段：{销售阶段} |",
    "operation": "append",
    "agent_name": "meeting-analysis"
  }
)
```

#### 步骤 7: 返回执行结果

**⚠️ 用户可见输出规范（必须严格执行）**

在完成所有步骤后，**必须**以结构化摘要形式向用户展示关键成果，**禁止**仅输出文件路径列表而不展示业务结果摘要。

**必须包含的摘要内容**：
| 摘要项 | 内容要求 |
|--------|---------|
| 分析结论 | 销售阶段 + 判断依据（一句话） |
| 客户痛点 | 从SPIN分析中提取的top 3痛点关键词 |
| 话术要点 | 生成的销售话术的核心策略（1-2句话） |
| 文件路径 | 所有输出文件的完整路径列表 |
| 下一步建议 | 基于分析结论的2-3条行动建议 |

**⚠️ 内部执行过程输出约束（零例外）**

**禁止在面向用户的最终输出中包含以下内容**：

| 禁止输出 | 说明 |
|---------|------|
| 工具调用过程 | 如「正在调用 spin-analysis skill...」、「Skill调用完成」 |
| 步骤编号自述 | 如「步骤1：项目验证」、「步骤3：SPIN分析」 |
| 文件移动日志 | 如「已将文件从...移动到...」 |
| 内部判断过程 | 如「检测到项目目录存在」、「扫描到以下文件」 |
| Skill 调用日志 | 如「正在调用 sales-script skill 生成话术」 |
| 错误恢复过程 | 如「文件读取失败，尝试备用方案...」 |

**允许输出的内容**：
- 分析结论和判断结果
- 文件保存路径列表
- 销售阶段和建议
- SPIN分析要点
- 话术核心策略

**输出格式**：
```markdown
✅ 会议分析完成

## 分析结论
- **项目**: {project_name}
- **会议日期**: {meeting_date}
- **销售阶段**: {销售阶段}
- **判断依据**: {一句话总结}

## 客户痛点
1. {痛点1}
2. {痛点2}
3. {痛点3}

## 话术要点
{1-2句话概括核心策略}

## 输出文件
- 会议分析报告: {project_name}/售前阶段/05_会议纪要/会议分析-{date}.md
- 销售话术: {project_name}/售前阶段/11_通用资料/话术-会议跟进-{date}.md
- 项目状态: 已更新

## 下一步建议
1. {建议1}
2. {建议2}
3. {建议3}
```

返回结构化结果：
```json
{
  "status": "success",
  "project_name": "{project_name}",
  "meeting_date": "{date}",
  "sales_stage": "{销售阶段}",
  "output_files": {
    "analysis_report": "{path}",
    "sales_script": "{path}"
  }
}
```

## Output Format

**成功输出**：
```markdown
✅ 会议分析完成

## 📊 分析结果
- **项目名称**: {project_name}
- **会议日期**: {meeting_date}
- **销售阶段**: {销售阶段}

## 📄 输出文件
✅ 会议分析报告 - {project_name}/售前阶段/05_会议纪要/会议分析-{date}.md
✅ 销售话术文件 - {project_name}/售前阶段/11_通用资料/话术-会议跟进-{date}.md
✅ 项目状态已更新 - {project_name}/项目状态.md

## 💡 下一步建议
{推进建议}
```

**失败输出**（项目未初始化）：
```markdown
❌ 项目未初始化

项目目录不存在: {project_name}

请先使用 project-init skill 初始化项目目录。
```

## Integration

### 与其他 Skills 的协作

| Skill | 用途 | 调用时机 |
|-------|------|---------|
| document-processor | 读取会议纪要文件（PDF/Word等） | 步骤2 |
| spin-analysis | SPIN销售法分析 | 步骤3 |
| sales-script | 生成销售话术 | 步骤5 |
| project-status-updater | 更新项目状态 | 步骤6 |

### 与 Agents 的协作

| Agent | 使用场景 |
|-------|---------|
| sales-master | 会议跟进阶段调用此 Skill |

## Best Practices

### 会议纪要准备
- 尽量提供完整的会议记录
- 包含客户的原话和关键表述
- 记录客户的疑虑和异议
- 记录下一步行动计划

### 分析准确性
- 基于会议实际内容，不虚构
- 如果信息不明确，标注"待定"
- 保持客观，避免过度解读

### 文件管理
- 会议纪要按日期命名
- 定期归档历史会议记录
- 保持项目目录整洁

## 工具调用优化规则

**⚠️ 减少冗余工具调用（必须遵循）**

| 规则 | 说明 |
|------|------|
| 文件定位 | 使用 Glob 一次性定位 `05_会议纪要/` 目录下的文件，禁止用 Bash find 多次搜索 |
| 项目验证 | 使用 Glob 检查项目目录是否存在，禁止用 Bash test 命令 |
| 文件读取 | Markdown/TXT 直接用 Read 工具，禁止用 Bash cat；PDF/Word 调用 document-processor skill |
| 状态更新 | 步骤6的3次 project-status-updater 调用必须顺序执行，禁止并行调用（避免文件写入冲突） |
| Skill 调用 | spin-analysis → sales-script 必须顺序执行，sales-script 依赖 spin-analysis 的结果 |

**禁止的冗余调用**：
- ❌ 同一目录多次 Bash find 搜索
- ❌ 已通过 Glob 确认文件存在后再次 Bash 验证
- ❌ 用 Bash cat 读取文本文件（应使用 Read 工具）
- ❌ 用 Bash ls 列出目录（应使用 Glob 工具）

## Notes

1. **真实性第一**：严格基于会议纪要实际内容，禁止虚构
2. **完整流程**：必须完成所有7个步骤，不得中途停止
3. **SPIN分析**：如果某个维度信息不足，标注"会议中未详细讨论"
4. **阶段判断**：基于明确依据，避免主观臆断
5. **文件归档**：所有文件自动保存到项目目录

## Examples

### 示例 1: 基础使用

**输入**:
```javascript
Skill(
  skill: "meeting-analysis",
  args: {
    "project_name": "农夫山泉-CMDB项目",
    "file_path": "d:\\temp\\会议纪要-20260215.pdf"
  }
)
```

**执行流程**:
1. 验证项目目录存在
2. 移动会议纪要文件到售前阶段/05_会议纪要/
3. 读取会议纪要内容
4. 调用 spin-analysis 进行SPIN分析
5. 生成会议分析报告
6. 生成销售话术
7. 更新项目状态

**输出**:
```markdown
✅ 会议分析完成

## 📊 分析结果
- **项目名称**: 农夫山泉-CMDB项目
- **会议日期**: 2026-02-15
- **销售阶段**: 已立项

## 📄 输出文件
✅ 会议分析报告 - 农夫山泉-CMDB项目/售前阶段/05_会议纪要/会议分析-20260215.md
✅ 销售话术文件 - 农夫山泉-CMDB项目/售前阶段/11_通用资料/话术-会议跟进-20260215.md
✅ 项目状态已更新 - 农夫山泉-CMDB项目/项目状态.md

## 💡 下一步建议
- 准备技术方案PPT
- 安排POC演示
- 跟进采购流程
```

### 示例 2: 自动扫描会议纪要

**输入**:
```javascript
Skill(
  skill: "meeting-analysis",
  args: {
    "project_name": "招商银行-监控平台"
  }
)
```

**说明**：
- 未提供 file_path，自动扫描 `招商银行-监控平台/售前阶段/05_会议纪要/` 目录
- 选择最新的会议纪要文件进行分析

---

**版本**: 1.2
**最后更新**: 2026-04-13
**更新内容**:
- **v1.2 (2026-04-13) - 输出规范与工具优化**:
  - ✅ 新增结构化摘要输出规范（5项必须包含的摘要内容：分析结论/客户痛点/话术要点/文件路径/下一步建议）
  - ✅ 新增内部执行过程输出约束（6类禁止输出项 + 5类允许输出项，区分内部执行和用户可见输出）
  - ✅ 新增工具调用优化规则（5条工具选择规则 + 4类禁止的冗余调用）
- **v1.1 (2026-03-15) - 添加输入校验防幻觉**:
  - ✅ 新增步骤 0: 输入完整性校验（必须执行）
  - ✅ 添加必需参数检查（project_name、file_path）
  - ✅ 添加校验失败错误输出格式
  - ✅ 定义校验结果处理流程
- **v1.0 (2026-02-15)**:
  - 初始版本，基于SPIN销售法分析会议纪要
**作者**: AI Solutions Expert Team
**依赖**: document-processor, spin-analysis, sales-script, project-status-updater
