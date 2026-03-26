---
name: sales-prep
description: 销售准备技能，一站式完成企业调研、案例匹配和话术生成的完整流程。为客户项目自动生成销售准备资料包，包括企业背景分析、匹配案例报告和定制化销售话术
category: sales
priority: high
---

# Sales Prep (销售准备技能)

## Purpose

为B2B销售团队提供一站式的销售准备服务，自动完成从企业调研到案例匹配再到话术生成的完整流程。

**核心功能**:
- 企业背景调研与分析（基于 company-research）
- 智能模块识别（从项目名称提取技术关键词）
- 案例智能匹配（基于 case-matching）
- 销售话术生成（基于 sales-script）
- 文件自动保存到项目目录
- 项目状态自动更新

**核心价值**:
- ✅ **一站式服务**：一次调用完成所有销售准备工作
- ✅ **智能化**：自动识别模块、匹配案例、生成话术
- ✅ **标准化**：统一的输出格式和文件组织
- ✅ **高效性**：节省销售人员80%的准备时间
- ✅ **可追溯**：所有资料保存到项目目录，便于查阅

## When to Use

在以下情况下使用此技能：
- 新客户项目启动，需要准备销售资料
- 需要了解目标客户背景和行业特点
- 需要找到同行业、同模块的成功案例
- 需要生成定制化的销售话术
- 需要为客户会议做准备

## Capabilities

### 1. 企业背景调研

**调研内容**：
- 企业基本信息（全称、行业、规模、成立时间）
- 行业细分识别（如"金融-银行"、"制造-食品"）
- 企业特点分析

**数据来源**：
- 公开工商信息
- 行业数据库
- 企业官网信息

**输出格式**：
- 结构化的企业信息 JSON
- 详细的调研报告 Markdown

### 2. 智能模块识别

**识别逻辑**：
- 从项目名称中提取技术关键词
- 从项目描述中识别模块需求
- 按关注度排序，取前3个模块

**支持的模块**：
- CMDB、自动化运维、DevOps、监控、ITSM
- IT数据人行上报、CD、低代码、统一IT门户

### 3. 案例智能匹配

**匹配维度**：
- 行业匹配（优先同行业）
- 模块匹配（必须包含目标模块）
- 时间筛选（优先一年内，不足则扩展）

**匹配策略**：
- 精确匹配：行业 + 模块 + 一年内
- 扩展匹配：行业 + 模块 + 五年内
- 降级匹配：仅模块匹配

**输出内容**：
- 匹配案例列表（客户名称、模块、金额、时间）
- 统计分析（价格范围、时间分布）
- 洞察建议（成功模式、差异化要点）

### 4. 销售话术生成

**话术内容**：
- 案例引入策略（如何自然引用案例）
- 项目阶段探查问题（SPIN提问）
- 会议预约话术
- 量化价值呈现

**定制化**：
- 基于客户行业特点
- 结合匹配的案例
- 针对识别的模块

### 5. 文件管理

**自动保存**：
- 案例匹配报告 → `{项目名称}/03相关案例/`
- 销售话术文件 → `{项目名称}/09沟通话术/`
- 企业调研报告 → `context/companies/{企业名}/`

**状态更新**：
- 更新项目状态文件 → `{项目名称}/项目状态.md`
- 记录准备工作历史

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| project_name | string | ✅ | - | 完整的项目名称，格式：`客户名称-项目名称`（如"农夫山泉-CMDB项目"） |
| force_refresh | boolean | ❌ | false | 是否强制刷新缓存（忽略已有的企业调研数据） |
| time_range | string | ❌ | auto | 案例时间范围：auto/1year/3year/5year |
| modules | array | ❌ | auto | 指定关注的模块列表，不指定则自动识别 |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的销售准备助手，专门为B2B销售人员提供一站式的客户项目准备服务。

**你的任务目标**：
快速完成企业调研、案例匹配和话术生成，为销售人员提供完整的销售准备资料包。

**核心原则**：
- 数据真实：所有信息来自可验证的公开渠道
- 准确匹配：严格按照匹配规则筛选案例
- 实用导向：生成的话术可直接用于销售实战
- 完整流程：必须完成所有步骤，不得中途停止

### 执行步骤

#### 步骤 1: 参数解析与验证

1. 从 project_name 中提取信息：
   - 客户名称：中划线"-"前的部分
   - 项目描述：中划线"-"后的部分

2. 验证项目名称格式：
   - 必须包含"-"分隔符
   - 推荐格式：`客户名称-项目名称`

3. 检查项目目录是否存在：
   ```bash
   test -d "{project_name}" && echo "EXISTS" || echo "NOT_EXISTS"
   ```
   - 如果不存在，提示需要先初始化项目

#### 步骤 2: 企业背景调研

**调用 company-research Skill**：
```javascript
Skill(
  skill: "company-research",
  args: {
    "company_name": "{客户名称}",
    "output_path": "context/companies/{客户名称}/"
  }
)
```

**获取调研结果**：
- 企业全称
- 所属行业（行业细分）
- 基本信息（注册资本、成立时间等）

**缓存检查**：
- 检查 `context/companies/{客户名称}/` 是否存在
- 如果存在且未过期（7天内），询问是否复用
- 如果 force_refresh=true，忽略缓存重新调研

#### 步骤 3: 智能模块识别

**识别逻辑**：
1. 优先级1：用户显式指定的 modules 参数
2. 优先级2：从项目描述中提取关键词
   - CMDB、监控、DevOps、自动化、ITSM等

**识别方法**：
```javascript
// 从项目描述中提取模块关键词
const projectDesc = "{项目描述}";
const keywords = ["CMDB", "监控", "DevOps", "自动化", "ITSM", "低代码"];
const matchedModules = keywords.filter(k => projectDesc.includes(k));
```

**输出**：
- 识别到的模块列表（最多3个）
- 按关注度排序

#### 步骤 4: 案例智能匹配

**调用 case-matching Skill**：
```javascript
Skill(
  skill: "case-matching",
  args: {
    "case_library_path": "通用知识/行业案例/公司案例库（持续更新）.md",
    "target_industry": "{从步骤2获取的行业细分}",
    "target_modules": "{从步骤3识别的模块列表}",
    "time_range": "{time_range参数或auto}",
    "project_name": "{project_name}"
  }
)
```

**案例库路径**：
知识库统一维护，路径为 `通用知识/行业案例/公司案例库（持续更新）.md`。
case-matching Skill 的 `case_library_path` 参数已有默认值，无需手动指定。

**获取匹配结果**：
- matched_cases：匹配的案例列表
- statistics：统计信息（总数、价格范围）
- insights：洞察分析（成功模式、差异化要点）

#### 步骤 5: 销售话术生成

**调用 sales-script Skill**：
```javascript
Skill(
  skill: "sales-script",
  args: {
    "customer_info": "{从步骤2获取的企业信息}",
    "matched_cases": "{从步骤4获取的案例列表}",
    "target_modules": "{从步骤3识别的模块}",
    "scenario": "initial_visit"  // 初次拜访场景
  }
)
```

**话术内容**：
- 案例引入策略
- 项目阶段探查问题
- 会议预约话术
- 量化价值呈现

#### 步骤 6: 文件保存

**6.1 保存案例匹配报告**

保存位置：`{project_name}/03相关案例/案例匹配报告-{YYYYMMDD}.md`

文件格式：
```markdown
# 案例匹配报告

**生成时间**: {YYYY-MM-DD HH:MM:SS}
**目标客户**: {客户名称}
**关注模块**: {模块列表}

---

## 📊 匹配统计

- ✅ 行业细分: {行业}
- ✅ 模块包含: {模块}
- 🕒 时间范围: {一年内/五年内}
- 📊 共匹配: {数量}个高度相关案例

---

## 📋 匹配的案例列表

{案例表格}

---

## 💡 案例价值分析

{统计分析和洞察建议}

---

*本报告由 sales-prep skill 自动生成*
```

**6.2 保存销售话术文件**

保存位置：`{project_name}/09沟通话术/话术-{YYYYMMDD}.md`

文件格式：
```markdown
# 销售话术 - {客户名称}

**生成时间**: {YYYY-MM-DD HH:MM:SS}
**目标客户**: {客户名称}
**关注模块**: {模块列表}
**匹配案例数**: {数量}个

---

{完整话术内容}

---

*本话术由 sales-prep skill 自动生成*
```

#### 步骤 7: 项目状态更新

**调用 project-status-updater Skill**：

**7.1 添加企业信息**：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "企业信息",
    "content": "- **客户全称**: {企业全称}\n- **所属行业**: {行业细分}\n- **调研时间**: {YYYY-MM-DD}",
    "operation": "replace"
  }
)
```

**7.2 添加更新日志**：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "更新日志",
    "content": "| {YYYY-MM-DD HH:mm:ss} | sales-prep | 完成企业调研和案例匹配，生成销售话术 |",
    "operation": "append"
  }
)
```

**7.3 添加会话轨迹记录**（推荐）：
```javascript
Skill(
  skill: "project-status-updater",
  args: {
    "project_name": "{project_name}",
    "section": "会话轨迹",
    "content": "| {YYYY-MM-DD HH:mm:ss} | sales-prep | 完成企业调研（{行业}），匹配{count}个案例，生成销售话术 |",
    "operation": "append",
    "agent_name": "sales-prep"
  }
)
```

#### 步骤 8: 返回执行结果

返回包含以下信息的结构化结果：
```json
{
  "status": "success",
  "project_name": "{project_name}",
  "customer_name": "{客户名称}",
  "industry": "{行业细分}",
  "modules": ["{模块列表}"],
  "matched_cases_count": 12,
  "output_files": {
    "case_report": "{project_name}/03相关案例/案例匹配报告-{date}.md",
    "sales_script": "{project_name}/09沟通话术/话术-{date}.md"
  },
  "execution_time": "125s"
}
```

## Output Format

**成功输出**：
```markdown
✅ 销售准备完成

## 📊 执行结果
- **项目名称**: {project_name}
- **目标客户**: {客户名称}
- **所属行业**: {行业细分}
- **关注模块**: {模块列表}
- **匹配案例**: {数量}个

## 📄 输出文件
✅ 案例匹配报告 - {project_name}/03相关案例/案例匹配报告-{date}.md
✅ 销售话术文件 - {project_name}/09沟通话术/话术-{date}.md
✅ 项目状态已更新 - {project_name}/项目状态.md

## 💡 后续建议
- 查看案例匹配报告，了解同行业成功案例
- 学习销售话术，准备客户沟通
- 根据实际情况调整话术内容
```

**失败输出**（项目未初始化）：
```markdown
❌ 项目未初始化

项目目录不存在: {project_name}

请先使用 project-init skill 初始化项目目录。
```

**失败输出**（企业调研失败）：
```markdown
❌ 企业调研失败

无法获取企业"{客户名称}"的公开信息。

可能原因：
1. 企业名称不准确
2. 无法访问公开数据源
3. 网络连接问题

建议：
1. 检查企业名称是否正确（建议使用全称）
2. 重试请求
3. 手动提供企业基本信息
```

## Integration

### 与其他 Skills 的协作

此 Skill 依赖以下 Skills：

| Skill | 用途 | 调用时机 |
|-------|------|---------|
| company-research | 企业背景调研 | 步骤2 |
| case-matching | 案例智能匹配 | 步骤4 |
| sales-script | 销售话术生成 | 步骤5 |
| project-status-updater | 项目状态更新 | 步骤7 |

### 与 Agents 的协作

此 Skill 可被以下 Agents 调用：

| Agent | 使用场景 | 说明 |
|-------|---------|------|
| sales-master | 销售准备阶段 | 主控 Agent 调用此 Skill 完成销售准备 |
| project-init | 项目初始化后 | 初始化完成后自动准备销售资料 |

## Best Practices

### 项目命名建议
- ✅ 标准格式: `客户名称-项目名称`
- ✅ 推荐示例:
  - "农夫山泉-CMDB项目"
  - "中国银行-监控平台建设"
  - "国投证券-DevOps体系建设"
- ❌ 避免使用特殊字符（除了 `-`）

### 模块识别建议
- 在项目名称中明确包含技术关键词
- 示例：
  - "农夫山泉-CMDB一期项目" → 自动识别 CMDB
  - "招商银行-监控平台建设" → 自动识别 监控
  - "华为-DevOps+CMDB建设" → 自动识别 DevOps、CMDB

### 缓存使用建议
- 企业调研数据默认缓存7天
- 如需最新数据，设置 force_refresh=true
- 案例匹配结果不缓存（案例库可能更新）

### 执行时机建议
- 项目初始化后立即执行
- 客户会议前1-2天执行
- 需求变更时重新执行

## Notes

1. **数据真实性**：所有数据必须来自可验证的公开渠道，严禁编造
2. **完整流程**：必须完成所有8个步骤，不得中途停止
3. **文件管理**：所有输出文件保存到项目目录，便于查阅和归档
4. **状态同步**：执行完成后必须更新项目状态文件
5. **错误处理**：任何步骤失败都要给出明确的错误提示和建议

## Examples

### 示例 1: 基础使用

**输入**:
```javascript
Skill(
  skill: "sales-prep",
  args: {
    "project_name": "农夫山泉-CMDB项目"
  }
)
```

**执行流程**:
1. 解析项目名称：客户=农夫山泉，项目=CMDB项目
2. 调研农夫山泉企业背景（行业：制造-食品）
3. 识别模块：CMDB
4. 匹配案例：找到12个制造业CMDB案例
5. 生成销售话术
6. 保存文件到项目目录
7. 更新项目状态

**输出**:
```markdown
✅ 销售准备完成

## 📊 执行结果
- **项目名称**: 农夫山泉-CMDB项目
- **目标客户**: 农夫山泉
- **所属行业**: 制造-食品
- **关注模块**: CMDB
- **匹配案例**: 12个

## 📄 输出文件
✅ 案例匹配报告 - 农夫山泉-CMDB项目/03相关案例/案例匹配报告-20260215.md
✅ 销售话术文件 - 农夫山泉-CMDB项目/09沟通话术/话术-20260215.md
✅ 项目状态已更新 - 农夫山泉-CMDB项目/项目状态.md
```

### 示例 2: 指定模块和时间范围

**输入**:
```javascript
Skill(
  skill: "sales-prep",
  args: {
    "project_name": "招商银行-IT运维平台",
    "modules": ["CMDB", "监控", "自动化"],
    "time_range": "3year"
  }
)
```

**执行流程**:
1. 解析项目名称：客户=招商银行
2. 调研招商银行企业背景（行业：金融-银行）
3. 使用指定模块：CMDB、监控、自动化
4. 匹配案例：三年内的金融业案例
5. 生成销售话术
6. 保存文件并更新状态

**输出**:
```markdown
✅ 销售准备完成

## 📊 执行结果
- **项目名称**: 招商银行-IT运维平台
- **目标客户**: 招商银行
- **所属行业**: 金融-银行
- **关注模块**: CMDB, 监控, 自动化
- **匹配案例**: 8个

## 📄 输出文件
✅ 案例匹配报告 - 招商银行-IT运维平台/03相关案例/案例匹配报告-20260215.md
✅ 销售话术文件 - 招商银行-IT运维平台/09沟通话术/话术-20260215.md
✅ 项目状态已更新 - 招商银行-IT运维平台/项目状态.md
```

### 示例 3: 强制刷新缓存

**输入**:
```javascript
Skill(
  skill: "sales-prep",
  args: {
    "project_name": "华为-DevOps建设",
    "force_refresh": true
  }
)
```

**说明**：
- 即使 context/companies/华为/ 目录存在，也会重新调研
- 确保获取最新的企业信息

---

**版本**: 1.1
**最后更新**: 2026-03-25
**作者**: AI Solutions Expert Team
**依赖**: company-research, case-matching, sales-script, project-status-updater
**变更记录**:
- v1.1 (2026-03-25): 案例库数据源迁移至知识库 `通用知识/行业案例/公司案例库（持续更新）.md`，移除旧的 caseLibrary.md 路径
- v1.0 (2026-02-15): 初始版本
