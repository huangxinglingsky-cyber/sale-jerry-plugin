# Sale-Jerry-Plugin Release Note

> 记录 sale-jerry-plugin 每次版本发布的特性变更

---

## v1.1.0 (2026-03-16)

### 新增功能 (Features)
- `skill-developer` (+) Skill 开发助手，智能识别是新开发 Skill 还是优化现有 Skill，支持参照现有格式创建新 Skill、智能修改优化 Skill，并提供变更对比确认
- `skill-logic-auditor` (+) 技能逻辑审查官，审计 Plugin 中其他 Skill 的定义与逻辑，诊断"信息缺失时强行输出结论"或"未充分利用知识库"的问题，输出审查报告与优化方案
### 优化功能 (Features)
- `bid-strategist` (~) 添加知识库无结果时的降级策略
- `meeting-analysis` (~) 添加会议纪要最小输入长度校验；集成 SPIN 方法论知识库检索
- `requirement-matching` (~) 添加知识库未命中时的降级策略
---

## v1.0.1 (2026-03-15)


### 优化改进 (Improvements)
- `project-report` (~) 优化模块内容过滤逻辑，只输出用户指定模块的相关内容，不再包含无关模块
- `company-research` (~) 添加企业名称完整性校验和追问机制，当输入模糊时引导用户补充信息；添加"无法确定唯一企业"时的降级策略
- `spin-analysis` (~) 添加输入完整性检查（步骤0），定义会议纪要最小长度要求；添加 SPIN 方法论知识库检索步骤
- `sales-script` (~) 添加场景信息完整性检查；添加产品知识库和话术案例检索步骤
- `case-matching` (~) 在 Output Format 中添加案例来源标注要求，确保案例可追溯
- `bid-analysis` (~) 添加参数缺失时的追问话术定义

- `roleplay-dojo` (~) 添加项目数据完整性校验，数据不完整时引导用户补充

### 文档更新 (Documentation)
- # 生成《Skill 开发与发布指导文档》，包含开发 Skill、优化 Skill、打包发布的完整流程

---

## v1.0.0 (2026-03-14)

### 新增功能 (Features)

#### Skills 清单（21个）

**销售核心技能**
- `company-research` (+) 企业信息调研，智能分析企业背景信息
- `case-matching` (+) 案例智能匹配，多维度筛选成功案例
- `sales-script` (+) 销售话术生成，提供专业销售话术建议
- `sales-prep` (+) 销售准备，一站式完成企业调研、案例匹配和话术生成

**项目全生命周期**
- `project-init` (+) 项目初始化，创建标准化目录结构
- `project-status-updater` (+) 项目状态更新，安全读写状态文件
- `stakeholder-input` (+) 项目相关方录入，智能识别人员信息
- `meeting-analysis` (+) 会议纪要分析，基于SPIN销售法
- `spin-analysis` (+) SPIN销售法分析，识别销售阶段
- `daily-report` (+) 日报生成，自动扫描文件变化生成报告

**招投标专项**
- `bid-analysis` (+) 招投标分析，智能分析招标商务评分表
- `bid-strategist` (+) 商务控标分析，提供控标优化建议
- `requirement-matching` (+) 需求匹配分析，计算产品功能匹配度

**销售赋能**
- `roleplay-dojo` (+) 销售陪练，模拟真实客户对话演练
- `jargon-decoder` (+) 技术黑话解码，翻译技术术语为销售语言
- `document-processor` (+) 综合文档处理，支持多格式文件解析

**项目协作**
- `project-report` (+) 立项报告生成，根据企业名称和模块名称智能搜索知识库模板，自动生成定制化立项报告

**开发/运维**
- `plugin-auditor` (+) Plugin架构审计，全面审查配置和定义
- `plugin-deploy` (+) Plugin打包部署，将 Plugin 目录打包为 zip 压缩包并上传到服务器
- `skill-developer` (+) Skill开发助手，创建和优化Skill
- `skill-logic-auditor` (+) 技能逻辑审查，诊断Skill定义问题

### 文档更新 (Documentation)
- # 新增 `docs/SKILL-清单功能描述.md` - 21个Skill完整功能描述
- # 新增 `docs/初级销售使用手册.md` - 初级销售人员使用指南

---

## 版本记录模板

> 以下模板供后续版本使用

```markdown
## v{x.y.z} (YYYY-MM-DD)

### 新增功能 (Features)
- `[skill-name]` (+) 功能描述

### 优化改进 (Improvements)
- `[skill-name]` (~) 优化内容描述

### 问题修复 (Bug Fixes)
- `[skill-name]` (!) 修复内容描述

### 文档更新 (Documentation)
- # 更新内容描述

### 其他变更 (Others)
- * 变更内容描述
```

---

## 变更类型说明

| 类型 | 标识 | 说明 |
|------|------|------|
| 新增功能 | `+` | 新增 Skill 或新增功能特性 |
| 优化改进 | `~` | 现有功能优化、性能提升 |
| 问题修复 | `!` | Bug 修复、异常处理 |
| 文档更新 | `#` | 文档新增或更新 |
| 其他变更 | `*` | 配置、依赖等其他变更 |

---

## 版本历史总览

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| v1.1.0 | 2026-03-16 | skill-developer 新增 Release Note 自动记录功能 |
| v1.0.1 | 2026-03-15 | 新增 skill-developer、skill-logic-auditor；批量优化 10 个 Skill（输入校验、知识库集成、降级策略） |
| v1.0.0 | 2026-03-14 | 初始版本，发布 21 个 Skill；新增两份用户文档 |

---

**维护者**: AI Solutions Expert Team
**最后更新**: 2026-03-16
