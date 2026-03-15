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
- 将会议纪要文件移动到 `{项目名称}/06会议纪要/`
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

**会议分析报告**（保存到 06会议纪要/）：
- 会议基本信息
- SPIN分析结果
- 销售阶段判断
- 客户痛点总结
- 下一步行动建议

**销售话术**（保存到 09沟通话术/）：
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
| file_path | string | ❌ | auto | 会议纪要文件路径，不指定则扫描06会议纪要目录 |
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
| file_path | 文件存在 | 不存在则扫描06会议纪要目录或返回错误 |

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

检查项目目录是否存在：
```bash
test -d "{project_name}" && echo "EXISTS" || echo "NOT_EXISTS"
```

如果不存在，提示用户先初始化项目。

#### 步骤 2: 会议纪要文件处理

**2.1 文件定位**：
- 如果提供了 file_path，使用指定文件
- 如果未提供，扫描 `{project_name}/06会议纪要/` 目录

**2.2 文件移动**（如果文件不在项目目录）：
```bash
# 移动文件到项目目录
mv "{file_path}" "{project_name}/06会议纪要/会议纪要-{date}.{ext}"
```

**2.3 文件读取**：
调用 document-processor skill 读取文件内容

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

保存位置：`{project_name}/06会议纪要/会议分析-{date}.md`

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

保存位置：`{project_name}/09沟通话术/话术-会议跟进-{date}.md`

#### 步骤 6: 更新项目状态

调用 project-status-updater skill：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "当前状态",
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
✅ 会议分析报告 - {project_name}/06会议纪要/会议分析-{date}.md
✅ 销售话术文件 - {project_name}/09沟通话术/话术-会议跟进-{date}.md
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
| document-processor | 读取会议纪要文件 | 步骤2 |
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
2. 移动会议纪要文件到06会议纪要/
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
✅ 会议分析报告 - 农夫山泉-CMDB项目/06会议纪要/会议分析-20260215.md
✅ 销售话术文件 - 农夫山泉-CMDB项目/09沟通话术/话术-会议跟进-20260215.md
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
- 未提供 file_path，自动扫描 `招商银行-监控平台/06会议纪要/` 目录
- 选择最新的会议纪要文件进行分析

---

**版本**: 1.1
**最后更新**: 2026-03-15
**更新内容**:
- **v1.1 (2026-03-15) - 添加输入校验防幻觉**:
  - ✅ 新增步骤 0: 输入完整性校验（必须执行）
  - ✅ 添加必需参数检查（project_name、file_path）
  - ✅ 添加校验失败错误输出格式
  - ✅ 定义校验结果处理流程
- **v1.0 (2026-02-15)**:
  - 初始版本，基于SPIN销售法分析会议纪要
**作者**: AI Solutions Expert Team
**依赖**: document-processor, spin-analysis, sales-script, project-status-updater
