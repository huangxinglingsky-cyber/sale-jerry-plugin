# 📋 Plugin Skills 批量审计报告

## 审计概览
- **审计时间**: 2026-03-26
- **审计范围**: /workspace/apps/pulgins/sale-jerry-plugin/skills/
- **Skill 总数**: 20 个（排除 skill-logic-auditor 自身）
- **发现问题**: 33 个

---

## 📊 问题统计

| Skill 名称 | 类型 | Logic Bug | 幻觉风险 | 数据源 | 输入校验 | 降级策略 | 总风险 |
|-----------|------|-----------|---------|--------|---------|---------|--------|
| bid-analysis | 数据分析类 | 🔴参数名不匹配 | 🟡 | ⚠️ | ✅ | ⚠️ | 🟡中等 |
| bid-strategist | 流程编排类 | 🔴参数名不匹配 | ✅ | ⚠️ | ⚠️ | ✅ | 🔴严重 |
| case-matching | 数据分析类 | ⚠️ | 🟡 | ⚠️ | ⚠️ | ✅ | 🟢轻微 |
| company-research | 内容生成类 | ⚠️ | 🟡 | ⚠️ | ✅ | ✅ | 🟢轻微 |
| daily-report | 流程编排类 | 🔴死代码 | ✅ | ⚠️ | ⚠️ | ✅ | 🟡中等 |
| document-processor | 工具平台类 | 🔴函数未定义 | ✅ | ✅ | ⚠️ | ⚠️ | 🟡中等 |
| jargon-decoder | 内容生成类 | ⚠️ | 🟡 | ✅ | ⚠️ | ⚠️ | 🟡中等 |
| meeting-analysis | 流程编排类 | 🔴章节名不匹配 | 🟡 | ⚠️ | ⚠️ | ❌ | 🟡中等 |
| plugin-auditor | 审计管理类 | ✅ | 🟡 | ✅ | ⚠️ | ❌ | 🟢轻微 |
| plugin-deploy | 工具平台类 | 🔴引用不存在的skill | ✅ | ⚠️ | ✅ | ⚠️ | 🟡中等 |
| project-init | 流程编排类 | 🔴变量名bug | ✅ | ⚠️ | ✅ | ✅ | 🟢轻微 |
| **project-report** | **内容生成类** | **🔴多处** | **🟡** | **🔴路径不存在** | **✅** | **⚠️** | **🔴严重** |
| project-status-updater | 工具平台类 | ✅ | ✅ | ✅ | ✅ | ✅ | 🟢轻微 |
| requirement-matching | 数据分析类 | 🔴参数未定义 | 🟡 | ⚠️ | ✅ | ✅ | 🟡中等 |
| roleplay-dojo | 流程编排类 | 🔴未读取文件 | 🟡 | ⚠️ | ✅ | ✅ | 🟡中等 |
| sales-prep | 流程编排类 | 🔴伪代码 | 🟡 | ⚠️ | ✅ | ❌ | 🟡中等 |
| sales-script | 内容生成类 | 🔴变量未定义 | 🟡 | ✅ | ✅ | ⚠️ | 🟡中等 |
| skill-developer | 工具平台类 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | 🟢轻微 |
| spin-analysis | 数据分析类 | ✅ | 🟡 | ✅ | ✅ | ✅ | 🟢轻微 |
| stakeholder-input | 工具平台类 | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | 🟢轻微 |

---

## 🔴 严重问题清单 (P0 - 需立即修复)

### 1. bid-strategist - 调用 bid-analysis 时参数名不匹配

**问题位置**: 第 210-221 行
**问题描述**: 步骤 4 调用 bid-analysis skill 时使用参数名 `case_library`/`qualification_list`/`customer_name`，但 bid-analysis Parameters 定义的是 `case_library_path`/`qualification_list_path`，且 `customer_name` 在 bid-analysis 中不存在
**风险**: bid-analysis 收到未知参数名，核心分析逻辑无法正确执行
**建议修复**: 将参数名改为 `case_library_path`/`qualification_list_path`，移除 `customer_name`

### 2. bid-analysis - 变量名未定义

**问题位置**: 第 504 行
**问题描述**: 变量 `defense_tactics`/`attack_tactics` 在步骤 5 引用但未在前文步骤中定义，步骤 3 输出格式使用的是 `defensive_suggestions`/`offensive_suggestions`
**建议修复**: 统一变量名为 `defensive_suggestions`/`offensive_suggestions`

### 3. document-processor - 4 个函数未定义

**问题位置**: 第 967-978 行
**问题描述**: `batch_convert_to_json` 函数引用了 `process_excel_to_json`/`process_word_to_json`/`process_pdf_to_json`/`process_markdown_to_json` 4 个函数，但均未定义
**建议修复**: 补充 4 个函数定义或移除 `batch_convert_to_json` 调用

### 4. plugin-deploy - 引用不存在的 skill

**问题位置**: 第 273 行
**问题描述**: `Skill(skill="dingtalk-message", ...)` 引用了不存在的 skill，项目中无 dingtalk 相关文件。即使 DDWEBHOOK 已配置也会调用失败
**建议修复**: 改为直接使用 curl 调用钉钉 Webhook API，不依赖 dingtalk-message skill

### 5. project-init - 变量名不一致

**问题位置**: 第 312 行
**问题描述**: 步骤 6 验证使用 `ls -la "{base_path}/{project_name}"`，但实际创建的目录名为 `{FINAL_PROJECT_NAME}`。当智能处理改变了项目名称时验证会检查错误目录
**建议修复**: 将 `{project_name}` 改为 `{FINAL_PROJECT_NAME}`

### 6. project-report - 知识库路径不存在

**问题位置**: 第 185 行、第 503 行
**问题描述**: `/shared/通用知识` 目录不存在，所有知识库搜索将返回空结果。DEFAULT_TEMPLATE 路径 `/shared/通用知识/项目资料/...docx` 同样不存在，无模板时 `Document(template_path)` 直接崩溃
**风险**: Skill 核心功能完全不可用
**建议修复**: 确认知识库实际挂载路径，更新 SKILL.md 中的所有路径引用

### 7. project-report - extract_case_info() 未定义

**问题位置**: 第 389 行
**问题描述**: `add_case_section()` 中调用了 `extract_case_info(cases[:3])`，但该函数从未定义
**建议修复**: 补充函数定义或移除调用

### 8. project-report - 年份替换破坏历史数据

**问题位置**: 第 324-327 行
**问题描述**: `"2024年": current_year, "2023年": current_year` 会将模板中所有历史年份替换为当前年份
**建议修复**: 仅替换特定占位符，不进行全文档年份替换

### 9. requirement-matching - project_name 参数未定义

**问题位置**: 第 472 行、第 485 行
**问题描述**: 步骤 6 调用 project-status-updater 时使用 `{project_name}`，但 Parameters 表中未定义该参数
**建议修复**: 在 Parameters 表中添加 `project_name` 可选参数

### 10. requirement-matching - 文档中 skill 名称错误

**问题位置**: 第 560 行
**问题描述**: 调用方说明引用 skill 名称为 `requirement-analysis`，但实际 name 为 `requirement-matching`，调用方使用错误名称无法触发
**建议修复**: 将 `requirement-analysis` 改为 `requirement-matching`

### 11. roleplay-dojo - 仅获取文件名未读取内容

**问题位置**: 第 228-238 行
**问题描述**: 步骤 2.2/2.3/2.4 仅用 `ls | head -1` 获取文件名，从未调用 Read 读取文件内容。步骤 3"生成客户画像"需要会议纪要、话术等内容，但数据为空
**风险**: 客户画像和演练内容将完全基于文件名虚构
**建议修复**: 在获取文件名后添加 Read 读取文件内容

### 12. sales-script - 变量未定义且 project_name 缺失

**问题位置**: 第 706-708 行
**问题描述**: 步骤 6 引用 `cases_provided`/`case_count` 变量但未定义；`{project_name}` 未在 Parameters 表中声明
**建议修复**: 移除未定义变量引用，在 Parameters 表添加 `project_name`

### 13. meeting-analysis - project-status-updater 章节名不匹配

**问题位置**: 第 278-281 行
**问题描述**: 调用 project-status-updater 时 section 传入 `"当前状态"`，但目标 skill 章节映射表中该关键词对应 `## 📊 当前阶段`，会导致更新失败
**建议修复**: 将 `"当前状态"` 改为 `"当前阶段"`

---

## 🟡 中等问题清单 (P1 - 建议修复)

### 1. daily-report - 死代码
- L448-452: data_source 判断逻辑 else 分支为死代码

### 2. daily-report - 环境变量无降级
- L84-86: `JAVIS_WORKSPACE_ID`/`JAVIS_AUTH_TOKEN` 未定义时 API 直接失败

### 3. daily-report - 硬编码 workspace_id
- L482: 硬编码值 `cmm8se74z049g30s5eeazl02d` 不可移植

### 4. document-processor - 章节编号重复
- L87: Capabilities 部分有两个"6"，L624-631 有重复的"文本文件处理"标题

### 5. jargon-decoder - project_name 参数缺失
- L604-640: 会话轨迹更新需要 project_name 但未在 Parameters 中定义

### 6. plugin-deploy - sed 正则脆弱
- L255: `sed -n '/^## v/,/^---$/p'` 假设版本标题严格格式

### 7. project-report - 函数引用顺序
- L237/256: 步骤 2.2/2.3 引用 `get_module_keywords()` 但定义在步骤 3.2

### 8. roleplay-dojo - 相对路径
- L158: 项目目录检查使用相对路径，应使用绝对路径

### 9. roleplay-dojo - 缺少 agent_name
- L360-374: 调用 project-status-updater 时缺少 agent_name 参数

### 10. sales-prep - 参数矛盾
- L197-211: 步骤 4 同时传递 case_library_path 又说"无需手动指定"

### 11. sales-prep - 缺少子 Skill 失败降级
- 步骤 2-5 任何子 Skill 调用失败时无降级策略

### 12. meeting-analysis - file_path 校验矛盾
- L140: file_path 在参数表为可选但校验要求"文件存在"

### 13. bid-strategist - 扫描目录无文件选择逻辑
- L197: 扫描 04 报价文件目录后若多文件未定义选择逻辑

---

## 🟢 轻微问题清单 (P2 - 可选优化)

### 1. case-matching - 行业分类数量不一致
- L1443: 列出 24 个行业但标题写"共 23 个"

### 2. case-matching - 模板字符串变量可能 undefined
- L989: `statistics.price_range` 可能为 undefined

### 3. company-research - "基于常识推断"表述
- L195: 诱导 AI 编造企业信息

### 4. company-research - 示例步骤编号跳过
- L499: 示例 3 步骤编号从 1 跳到 4

### 5. plugin-auditor - Examples 检查标准不匹配
- L65-67: 引用 Agent 格式标准审计 Skill 文件

### 6. stakeholder-input - 手机号正则不一致
- L264 vs L283: `1\d{10}` vs `1[3-9]\d{9}`

### 7. spin-analysis - 知识库路径模糊
- L206: `knowledge/` 为相对路径未明确根目录

### 8. spin-analysis - 阶段判断无量化标准
- L339-351: "信息充分"/"信息较少"缺乏可量化定义

---

## 📋 优先修复建议

| 优先级 | Skill | 问题 | 影响 |
|--------|-------|------|------|
| P0 | project-report | 知识库路径不存在 | 核心功能不可用 |
| P0 | bid-strategist | 参数名不匹配 | 核心分析无法执行 |
| P0 | roleplay-dojo | 未读取文件内容 | 客户画像完全虚构 |
| P0 | sales-script | 变量未定义 | 项目状态更新失败 |
| P0 | document-processor | 4 个函数未定义 | 批量转换功能不可用 |
| P0 | plugin-deploy | 引用不存在的 skill | 通知功能必然失败 |
| P0 | meeting-analysis | 章节名不匹配 | 状态更新失败 |
| P0 | project-init | 变量名 bug | 验证检查错误目录 |
| P0 | requirement-matching | 参数未定义 | 状态更新失败 |
| P0 | project-report | extract_case_info 未定义 | 案例章节不可用 |
| P0 | project-report | 年份替换破坏数据 | 历史信息被篡改 |

---

## 📊 风险分布

```
总风险分布:
🔴 严重: 2 个 (bid-strategist, project-report)
🟡 中等: 10 个 (bid-analysis, daily-report, document-processor, jargon-decoder, meeting-analysis, plugin-deploy, requirement-matching, roleplay-dojo, sales-prep, sales-script)
🟢 轻微: 8 个 (case-matching, company-research, plugin-auditor, project-init, project-status-updater, skill-developer, spin-analysis, stakeholder-input)
```

---

**审计完成** | 扫描: 20 个 Skill | 发现: 33 个问题 | P0: 13 个 | P1: 13 个 | P2: 7 个
