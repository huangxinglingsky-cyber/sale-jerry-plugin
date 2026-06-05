# sale-jerry-plugin 架构分析报告

> 扫描时间：2026-05-27 | Plugin 版本：1.0.19

---

## 一、Agent 清单

当前 Plugin 包含 **1 个 Agent**。

### sales-master（销售主控代理）

| 属性 | 说明 |
|------|------|
| 文件 | `agents/sales-master.md` |
| 角色 | 销售主控代理，智能识别销售阶段并自动调度相应的 Skills |
| 核心能力 | 理解用户意图 → 判断当前销售阶段 → 选择并调用合适的 Skill 执行 |
| 知识库约束 | `通用知识/` 为只读知识库，Agent 不应修改知识库内容 |

**编排的 7 个销售阶段与 9 个 Skill：**

| 阶段 | 调度的 Skill |
|------|-------------|
| 1. 项目初始化 | `project-init` |
| 2. 销售准备 | `sales-prep` |
| 3. 需求分析 | `jargon-decoder`, `requirement-matching` |
| 4. 会议跟进 | `meeting-analysis` |
| 5. 投标策略 | `bid-strategist` |
| 6. 销售演练 | `roleplay-dojo` |
| 7. 方案输出 | `fabe-proposal` |

**安全约束（5 项）：**
- S1: 禁止编造客户信息，必须基于知识库或用户提供的数据
- S2: 禁止承诺无法兑现的技术功能
- S3: 合同金额、折扣等敏感信息需用户确认
- S4: 禁止自动发送邮件或消息给客户
- S5: 知识库文件只读

---

## 二、Skill 清单

当前 Plugin 包含 **20 个 Skill**。

### 2.1 销售流程类

| Skill | 文件路径 | 能力说明 |
|-------|---------|---------|
| `project-init` | `skills/project-init/SKILL.md` | 项目初始化，创建标准化目录结构（行业自动识别） |
| `sales-prep` | `skills/sales-prep/SKILL.md` | 销售准备一站站式（企业调研+案例匹配+话术生成） |
| `jargon-decoder` | `skills/jargon-decoder/SKILL.md` | 术语标准化，将客户术语映射为产品术语 |
| `requirement-matching` | `skills/requirement-matching/SKILL.md` | 需求匹配，对比客户需求与功能清单的覆盖度 |
| `meeting-analysis` | `skills/meeting-analysis/SKILL.md` | 会议纪要分析，SPIN 识别+销售阶段判断+跟进建议 |
| `bid-strategist` | `skills/bid-strategist/SKILL.md` | 商务控标分析，评分表算分+控标策略建议 |
| `roleplay-dojo` | `skills/roleplay-dojo/SKILL.md` | 销售演练，角色扮演+复盘打分 |
| `fabe-proposal` | `skills/fabe-proposal/SKILL.md` | FABE 售前方案生成（Feature-Advantage-Benefit-Evidence） |

### 2.2 调研分析类

| Skill | 文件路径 | 能力说明 |
|-------|---------|---------|
| `company-research` | `skills/company-research/SKILL.md` | 企业调研，案例匹配+IT 痛点识别+竞品分析 |
| `case-matching` | `skills/case-matching/SKILL.md` | 案例智能匹配，行业+模块+时间多维度检索 |
| `spin-analysis` | `skills/spin-analysis/SKILL.md` | SPIN 销售法分析（Situation-Problem-Implication-Need） |
| `ai-feasibility-analysis` | `skills/ai-feasibility-analysis/SKILL.md` | AI 可行性分析，评估客户场景的 AI 落地可行性 |

### 2.3 文档与报告类

| Skill | 文件路径 | 能力说明 |
|-------|---------|---------|
| `daily-report` | `skills/daily-report/SKILL.md` | 日报自动生成（claude-mem sessions 驱动），过滤无效会话 |
| `project-report` | `skills/project-report/SKILL.md` | 立项报告生成，基于知识库模板输出 docx |
| `sales-script` | `skills/sales-script/SKILL.md` | 销售话术生成 |
| `document-processor` | `skills/document-processor/SKILL.md` | 文档处理（格式转换、内容提取等） |

### 2.4 项目管理类

| Skill | 文件路径 | 能力说明 |
|-------|---------|---------|
| `project-status-updater` | `skills/project-status-updater/SKILL.md` | 项目状态更新 |
| `stakeholder-input` | `skills/stakeholder-input/SKILL.md` | 干系人输入分析 |

### 2.5 集成工具类

| Skill | 文件路径 | 能力说明 |
|-------|---------|---------|
| `dingtalk-ai-table` | `skills/dingtalk-ai-table/SKILL.md` | 钉钉 AI 表格操作（读写表格数据） |

---

## 三、硬编码知识库路径引用

### 3.1 路径总览

共发现 **7 个硬编码路径**，分布在 **8 个 Skill** 中。

| 编号 | 硬编码路径 | 引用该路径的 Skill |
|------|-----------|-------------------|
| P1 | `通用知识/行业案例/公司案例库（持续更新）.md` | `company-research`、`case-matching`、`bid-strategist`、`sales-prep` |
| P2 | `通用知识/资质相关/资质清单.md` | `bid-strategist` |
| P3 | `通用知识/功能清单/EasyOps功能清单.md` | `requirement-matching`、`fabe-proposal` |
| P4 | `/shared/通用知识/`（目录） | `project-report` |
| P5 | `/shared/通用知识/项目资料/一体化运维平台建设立项报告v2.0.docx` | `project-report` |
| P6 | `context/companies/{企业名}/` | `sales-prep` |
| P7 | `/workspace/日报/` | `daily-report` |

### 3.2 详细引用分析

#### P1: `通用知识/行业案例/公司案例库（持续更新）.md`

**引用方式：** 作为参数默认值传入，内容为 6 列 Markdown 表格

| 列名 | 说明 |
|------|------|
| 签约日期 | 合同签约时间 |
| 客户名称 | 客户公司名称 |
| 销售机会 | 对应销售机会编号/名称 |
| 合同名称 | 具体合同名称 |
| 行业 | 客户所属行业 |
| 合同金额 | 合同总金额 |

**引用详情：**
- `company-research`：step 2 读取案例库，匹配客户行业的已有案例
- `case-matching`：`case_library_path` 参数默认值，核心数据源
- `bid-strategist`：`case_library_path` 参数默认值，用于控标策略中的案例支撑
- `sales-prep`：调用 case-matching 时传递该路径

#### P2: `通用知识/资质相关/资质清单.md`

**引用方式：** `bid-strategist` 的 `qualification_path` 参数默认值

**用途：** 投标评分时读取公司资质信息，用于资质得分计算

#### P3: `通用知识/功能清单/EasyOps功能清单.md`

**引用方式：** 作为参数默认值传入

**引用详情：**
- `requirement-matching`：`feature_list_path` 参数默认值，用于需求与功能对比
- `fabe-proposal`：`feature_list_path` 参数默认值，用于 FABE 方案生成时引用功能特性

#### P4 & P5: `/shared/通用知识/` 及其子文件

**引用方式：** `project-report` 的 `KNOWLEDGE_BASE_PATH` 和 `DEFAULT_TEMPLATE`

**用途：** 立项报告生成时读取知识库中的模板文件作为输出基础

#### P6: `context/companies/{企业名}/`

**引用方式：** `sales-prep` 用于缓存企业调研结果

**用途：** 已调研过的企业信息缓存目录，避免重复调研

#### P7: `/workspace/日报/`

**引用方式：** `daily-report` 的日报输出目录

**用途：** 生成的日报 markdown 文件保存路径

---

## 四、知识库初始化结构

### 4.1 推荐初始化目录树

```
通用知识/
├── 行业案例/
│   └── 公司案例库（持续更新）.md
├── 资质相关/
│   └── 资质清单.md
├── 功能清单/
│   └── EasyOps功能清单.md
└── 项目资料/
    └── 一体化运维平台建设立项报告v2.0.docx
```

### 4.2 文件内容要求

#### `公司案例库（持续更新）.md`

格式：Markdown 表格，6 列固定结构

```markdown
| 签约日期 | 客户名称 | 销售机会 | 合同名称 | 行业 | 合同金额 |
|---------|---------|---------|---------|------|---------|
| 2025-01 | XX银行 | OPS-001 | 智能运维平台建设合同 | 金融 | 200万 |
```

#### `资质清单.md`

格式：Markdown 文档，列出公司拥有的资质证书

建议结构：
```markdown
# 资质清单

## 等级资质
- CMMI 5级
- ISO 27001
- ...

## 行业资质
- 金融行业安全认证
- ...
```

#### `EasyOps功能清单.md`

格式：Markdown 文档/表格，列出产品功能模块

建议结构：
```markdown
# EasyOps 功能清单

## 监控管理
| 功能模块 | 功能点 | 说明 |
|---------|-------|------|
| 基础监控 | 主机监控 | 支持 SNMP/Agent 采集 |

## 自动化运维
...
```

#### `一体化运维平台建设立项报告v2.0.docx`

格式：Word 文档，作为立项报告的模板文件

### 4.3 路径挂载说明

`project-report` 引用的是 `/shared/通用知识/` 路径，而其他 Skill 引用的是相对路径 `通用知识/`。需确保两个路径都指向同一份知识库内容，或在项目初始化时将 `通用知识/` 目录复制/软链到 `/shared/` 下。

---

## 五、不初始化知识库的影响与优化建议

### 5.1 各 Skill 影响评估

| Skill | 影响程度 | 说明 |
|-------|---------|------|
| `case-matching` | **严重** | 核心数据源缺失，无法进行案例匹配 |
| `company-research` | **严重** | 无法匹配历史案例，调研结果不完整 |
| `bid-strategist` | **严重** | 无法读取案例库和资质清单，控标分析无数据支撑 |
| `requirement-matching` | **严重** | 无法对比功能清单，需求匹配无法执行 |
| `fabe-proposal` | **严重** | 无法引用功能特性，方案生成质量大幅下降 |
| `sales-prep` | **中等** | 依赖 case-matching 和 company-research，间接影响 |
| `project-report` | **中等** | 找不到模板文件，需要用户提供替代模板 |
| `daily-report` | **无影响** | 日报目录不存在时会自动创建 |

### 5.2 优化建议

#### 方案 A：统一路径管理（推荐）

将硬编码路径提取为 Skill 的可配置参数，支持从环境变量或配置文件读取：

```
建议新增配置文件：.claude-plugin/knowledge-config.json
{
  "knowledge_base_path": "通用知识/",
  "case_library": "行业案例/公司案例库（持续更新）.md",
  "qualification_list": "资质相关/资质清单.md",
  "feature_list": "功能清单/EasyOps功能清单.md",
  "project_template": "项目资料/一体化运维平台建设立项报告v2.0.docx",
  "daily_report_output": "/workspace/日报/"
}
```

**优点：** 路径集中管理，修改一处即全局生效；支持不同项目使用不同知识库
**缺点：** 需要修改所有相关 Skill 的路径引用方式

#### 方案 B：Skill 降级策略

在每个引用知识库的 Skill 中增加降级逻辑：

1. 检测知识库文件是否存在
2. 若不存在，提示用户上传或提供数据
3. 提供无知识库模式的最小能力输出（如基于通用知识生成，而非历史案例）

**示例（以 case-matching 为例）：**
```
若 案例库文件不存在:
  → 提示："未检测到案例库文件，案例匹配功能受限。请将案例库文件放置到 {path}"
  → 降级为基于用户输入的案例描述进行匹配
  → 输出中标注"未参考历史案例库"
```

**优点：** 不初始化知识库也能基本使用
**缺点：** 输出质量会下降，但优于直接报错

#### 方案 C：知识库初始化向导

在 `project-init` Skill 中增加知识库初始化步骤：

1. 检测知识库目录是否已存在
2. 若不存在，引导用户上传或创建知识库文件
3. 提供模板文件供用户填写
4. 验证知识库结构完整性

**优点：** 首次使用时有引导，降低门槛
**缺点：** 增加 project-init 的复杂度

### 5.3 综合建议

**短期（立即可做）：**
- 实施方案 B（降级策略），确保知识库不存在时 Skill 不会报错，而是给出明确提示
- 在 `sales-master` Agent 中增加知识库状态检查，初始化对话时提示用户配置状态

**中期（1-2 周）：**
- 实施方案 A（统一路径管理），将硬编码路径集中化
- 解决 `/shared/通用知识/` 和 `通用知识/` 双路径问题，统一为一个路径

**长期（按需）：**
- 实施方案 C（初始化向导），提供完整的新手引导体验

---

## 附录：文件统计

| 指标 | 数量 |
|------|------|
| Agent | 1 |
| Skill | 20 |
| 硬编码知识库路径 | 7 |
| 涉及知识库引用的 Skill | 8 |
| 安全约束规则 | 5 |
| 编排的销售阶段 | 7 |
