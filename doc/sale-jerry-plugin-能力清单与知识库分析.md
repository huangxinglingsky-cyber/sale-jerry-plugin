# Sale-Jerry-Plugin 能力全景图

## 一、Agent（1个）

| Agent | 文件 | 角色定位 |
|-------|------|----------|
| **sales-master** | `agents/sales-master.md` | 销售主控代理，智能识别销售阶段并调度对应 Skill |

sales-master 覆盖销售全生命周期：项目启动 → 销售准备 → 需求分析 → 会议跟进 → 投标策略 → 销售演练 → 方案生成。

---

## 二、Skills（19个）

| # | Skill 名称 | 能力简述 |
|---|-----------|---------|
| 1 | **project-init** | 标准化项目目录创建（售前阶段11个子目录 + 模板文件） |
| 2 | **sales-prep** | 一站式销售准备（企业调研 + 案例匹配 + 话术生成） |
| 3 | **company-research** | 企业背景调研、行业分类、案例匹配 |
| 4 | **case-matching** | 多维度智能案例匹配（行业+模块+时间+金额） |
| 5 | **requirement-matching** | 客户需求与产品功能清单精确匹配、匹配度计算 |
| 6 | **meeting-analysis** | 会议纪要 SPIN 分析、销售阶段判断、推进建议 |
| 7 | **spin-analysis** | SPIN 销售法四维度深度分析 |
| 8 | **bid-strategist** | 商务投标分析（废标项审查、评分策略、攻防控标） |
| 9 | **fabe-proposal** | FABE 方法论售前方案生成（Markdown + Word） |
| 10 | **roleplay-dojo** | 销售陪练（侧写→演练→复盘三阶段模拟） |
| 11 | **stakeholder-input** | 项目相关方智能识别与录入 |
| 12 | **project-status-updater** | 项目状态文件自动更新 |
| 13 | **project-report** | 立项报告自动生成（Word格式） |
| 14 | **daily-report** | 日报自动生成与 Javis 平台同步 |
| 15 | **sales-script** | 销售话术生成 |
| 16 | **jargon-decoder** | 行业术语解析 |
| 17 | **document-processor** | 文档处理 |
| 18 | **dingtalk-ai-table** | 钉钉智能表格集成 |
| 19 | **AIFeasibility-analysis** | AI需求落地可行性分析（Agent/Skill模式） |

---

## 三、硬编码知识库路径引用汇总

以下 Skill 中存在对固定路径知识文件的硬编码引用：

| Skill | 引用的知识库路径 | 用途 |
|-------|-----------------|------|
| **case-matching** | `通用知识/行业案例/公司案例库（持续更新）.md` | 案例匹配数据源 |
| **company-research** | `通用知识/行业案例/公司案例库（持续更新）.md` | 企业调研案例数据源 |
| **bid-strategist** | `通用知识/行业案例/公司案例库（持续更新）.md` | 投标评分案例参考 |
| **bid-strategist** | `通用知识/资质相关/资质清单.md` | 资质评分依据 |
| **sales-prep** | `通用知识/行业案例/公司案例库（持续更新）.md` | 销售准备案例匹配 |
| **requirement-matching** | `通用知识/功能清单/EasyOps功能清单.md` | 需求匹配功能对照 |
| **fabe-proposal** | `通用知识/功能清单/EasyOps功能清单.md` | 方案生成功能引用 |
| **project-report** | `/shared/通用知识/项目资料/一体化运维平台建设立项报告v2.0.docx` | 立项报告模板 |
| **project-report** | `/shared/通用知识` (KNOWLEDGE_BASE_PATH) | 知识库搜索根路径 |
| **daily-report** | `/workspace/日报/` | 日报输出目录 |

---

## 四、知识库初始化结构

如果要完整初始化销售知识库，需要创建以下目录和文件结构：

```
通用知识/
├── 行业案例/
│   └── 公司案例库（持续更新）.md      ← 核心！案例数据（客户名、行业、模块、金额、时间）
├── 功能清单/
│   └── EasyOps功能清单.md            ← 核心！产品各模块功能逐项列表
├── 资质相关/
│   └── 资质清单.md                   ← 公司资质证书列表
└── 项目资料/
    └── 一体化运维平台建设立项报告v2.0.docx  ← Word模板文件
```


- 当前有 **6个 Skill** 硬编码引用了 **4个知识库文件**
- 核心依赖是「案例库」和「功能清单」两个 `.md` 文件
- 最小可用知识库只需准备这两个文件即可支撑大部分 Skill 运行
- 建议通过环境变量 + 存在性检测 + 降级策略三层机制解耦知识库硬依赖
