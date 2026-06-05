# sale-jerry-plugin 能力清单与知识库分析

> 生成时间：2026-05-27 | 版本：v1.0.19

---

## 一、Agent（1个）

**`sales-master`** — 销售主控代理，覆盖 B2B 销售全生命周期：项目启动 → 销售准备 → 需求分析 → 会议跟进 → 投标策略 → 销售演练 → 方案生成。

---

## 二、Skills（20个）

| # | Skill | 能力简述 |
|---|-------|---------|
| 1 | `project-init` | 标准化项目目录创建（售前阶段11个子目录 + 模板文件） |
| 2 | `sales-prep` | 一站式销售准备（企业调研 + 案例匹配 + 话术生成） |
| 3 | `company-research` | 企业背景调研、行业分类、案例匹配 |
| 4 | `case-matching` | 多维度智能案例匹配（行业 + 模块 + 时间 + 金额） |
| 5 | `requirement-matching` | 客户需求与产品功能清单精确匹配、匹配度计算 |
| 6 | `meeting-analysis` | 会议纪要 SPIN 分析、销售阶段判断、推进建议 |
| 7 | `spin-analysis` | SPIN 销售法四维度深度分析 |
| 8 | `bid-strategist` | 商务投标分析（废标项审查、评分策略、攻防控标） |
| 9 | `fabe-proposal` | FABE 方法论售前方案生成（Markdown + Word） |
| 10 | `roleplay-dojo` | 销售陪练（侧写 → 演练 → 复盘三阶段模拟） |
| 11 | `stakeholder-input` | 项目相关方智能识别与录入 |
| 12 | `project-status-updater` | 项目状态文件自动更新 |
| 13 | `project-report` | 立项报告自动生成（Word 格式） |
| 14 | `daily-report` | 日报自动生成与 Javis 平台同步 |
| 15 | `sales-script` | 销售话术生成 |
| 16 | `jargon-decoder` | 行业术语解析 |
| 17 | `document-processor` | 多格式文档读取（Excel/Word/PDF/图片/Markdown） |
| 18 | `dingtalk-ai-table` | 钉钉 AI 表格 CRUD 操作 |
| 19 | `ai-feasibility-analysis` | AI 需求落地可行性分析（9章报告） |
| 20 | `project-report` | 立项报告生成（Word 格式，含知识库检索） |

---

## 三、知识库路径引用汇总

以下 Skill 引用了固定路径的知识文件，路径集中、规律，适配新用户只需替换对应文件内容即可：

| Skill | 引用路径 | 用途 |
|-------|---------|------|
| `case-matching` | `通用知识/行业案例/公司案例库（持续更新）.md` | 案例匹配数据源 |
| `company-research` | `通用知识/行业案例/公司案例库（持续更新）.md` | 企业调研案例参考 |
| `bid-strategist` | `通用知识/行业案例/公司案例库（持续更新）.md` | 投标案例参考 |
| `bid-strategist` | `通用知识/资质相关/资质清单.md` | 资质评分依据 |
| `sales-prep` | `通用知识/行业案例/公司案例库（持续更新）.md` | 销售准备案例匹配 |
| `requirement-matching` | `通用知识/功能清单/EasyOps功能清单.md` | 需求匹配功能对照 |
| `fabe-proposal` | `通用知识/功能清单/EasyOps功能清单.md` | 方案生成功能引用 |
| `project-report` | `/shared/通用知识`（Python 常量） | 知识库搜索根路径 |
| `project-report` | `/shared/通用知识/项目资料/一体化运维平台建设立项报告v2.0.docx` | 立项报告 Word 模板 |
| `daily-report` | `/workspace/日报/` | 日报输出目录 |

**核心依赖只有 3 个文件**：案例库、功能清单、资质清单。`project-report` 使用了绝对路径，其余均为相对路径，适配成本很低。

---

## 四、知识库初始化结构

适配新用户只需准备以下文件，替换内容即可，目录结构不变：

```
通用知识/
├── 行业案例/
│   └── 公司案例库（持续更新）.md      ← 替换为目标客户的案例数据
├── 功能清单/
│   └── EasyOps功能清单.md            ← 替换为目标产品的功能列表
├── 资质相关/
│   └── 资质清单.md                   ← 替换为对应公司的资质证书
└── 项目资料/
    └── 一体化运维平台建设立项报告v2.0.docx  ← 替换为对应的立项报告模板
```

---

## 五、不修改 Skill 的情况下如何初始化知识库

当前各 Skill 的路径均为硬编码，只要按照以下结构在工作区根目录准备好对应文件，所有 Skill 即可直接运行，无需任何代码改动。

### 5.1 必须准备的文件（最小可用集）

```
{工作区根目录}/
└── 通用知识/
    ├── 行业案例/
    │   └── 公司案例库（持续更新）.md
    ├── 功能清单/
    │   └── EasyOps功能清单.md
    └── 资质相关/
        └── 资质清单.md
```

准备好这 3 个文件后，`case-matching`、`company-research`、`bid-strategist`、`sales-prep`、`requirement-matching`、`fabe-proposal` 共 6 个 Skill 均可正常运行。

### 5.2 各文件内容格式参考

**`公司案例库（持续更新）.md`**
```markdown
## 案例：XX银行运维平台建设

- 客户：XX银行
- 行业：金融
- 规模：500人IT团队
- 实施模块：CMDB、监控、变更
- 上线时间：2024-06
- 客户收益：故障平均处理时长从4小时降至40分钟
```

**`EasyOps功能清单.md`**
```markdown
## CMDB 配置管理

- 自动发现：支持主动/被动两种模式，覆盖物理机、虚拟机、容器
- 关系拓扑：可视化展示资源依赖关系
- 变更追踪：记录所有配置项变更历史
```

**`资质清单.md`**
```markdown
## 资质列表

| 资质名称 | 级别 | 有效期 | 适用场景 |
|---------|------|--------|---------|
| ISO 27001 | — | 2026-12 | 信息安全类投标 |
| CMMI | 3级 | 2025-09 | 软件开发类投标 |
```

### 5.3 `project-report` 的特殊处理

`project-report` 使用的是绝对路径 `/shared/通用知识`，与其他 Skill 的相对路径不同。在不修改代码的情况下，有两种处理方式：

| 方式 | 操作 | 适用场景 |
|------|------|---------|
| 挂载共享目录 | 将 `通用知识/` 挂载到 `/shared/通用知识` | 有 Docker/NFS 挂载能力的环境 |
| 创建软链接 | `ln -s {工作区}/通用知识 /shared/通用知识` | 本地开发环境 |

如果两种方式都不可行，`project-report` 需要单独修改路径常量，其余 Skill 不受影响。

---

## 六、通用化改造方向：配置文件 + Skill 启动加载

如需将 Plugin 完全通用化、支持多用户快速适配，可以将所有路径和环境参数抽取到一个统一配置文件，并要求每个 Skill 在启动时强制读取。

### 5.1 配置文件结构

在知识库根目录新增 `通用知识/plugin-config.md`，集中管理所有可变参数：

```markdown
# sale-jerry-plugin 配置

## 知识库路径
- 案例库: 通用知识/行业案例/公司案例库（持续更新）.md
- 功能清单: 通用知识/功能清单/EasyOps功能清单.md
- 资质清单: 通用知识/资质相关/资质清单.md
- 立项报告模板: 通用知识/项目资料/一体化运维平台建设立项报告v2.0.docx

## 输出路径
- 日报目录: /workspace/日报/
- 临时文件: /workspace/tmp/

## 服务配置
- Javis 日报工作区 ID: cmm8se74z049g30s5eeazl02d
- 公司名称: EasyOps
- 产品名称: EasyOps 一体化运维平台
```

### 5.2 Skill 启动时强制加载配置

每个 Skill 的 Instructions 第一步改为强制读取配置，配置不存在则中止执行并提示用户初始化：

```
### Step 0：加载配置（必须，不可跳过）
读取 `通用知识/plugin-config.md`，提取本 Skill 所需的路径变量。
若配置文件不存在，停止执行并提示：「请先初始化知识库配置，参考 plugin-config.md 模板」。
```

### 5.3 各 Skill 改动量

| Skill | 改动内容 | 工作量 |
|-------|---------|--------|
| `case-matching` | Step 0 加载配置，路径变量化 | ~5 行 |
| `company-research` | 同上 | ~5 行 |
| `bid-strategist` | 同上（2 个路径） | ~5 行 |
| `sales-prep` | 同上 | ~5 行 |
| `requirement-matching` | 同上 | ~5 行 |
| `fabe-proposal` | 同上 | ~5 行 |
| `project-report` | Python 常量改为读配置文件 | ~10 行 |
| `daily-report` | Javis workspace ID 改为读配置 | ~5 行 |

全部改动约 1-2 小时，之后适配新用户只需更新 `plugin-config.md` 一个文件。

---

### ⚠️ 注意：配置强制加载会引入使用门槛

改造后，Agent 运行前必须先完成知识库配置，否则所有依赖知识库的 Skill 均无法启动。这对新用户意味着：

- 首次使用需要一次性完成 `plugin-config.md` 的初始化配置
- 知识库文件路径填写错误会导致 Skill 静默失败或报错中止
- 对于不熟悉目录结构的用户，初始化步骤需要有引导文档配合

**建议**：如果推进此改造，同步提供一份初始化引导（onboarding checklist），明确告知用户在首次运行前需要准备哪些文件，降低上手摩擦。

