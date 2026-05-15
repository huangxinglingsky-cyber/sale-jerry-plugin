---
name: fabe-proposal
description: 基于FABE方法论生成正式售前方案，支持Markdown和Word两种输出格式，优先引用知识库产品功能清单，输入不足时引导用户补充信息而非编造
user-invocable: true
---

# fabe-proposal（FABE售前方案生成）

基于FABE方法论（Feature/特征 → Advantage/优势 → Benefit/利益 → Evidence/证据），生成正式、严谨的售前方案。支持输出 Markdown 和 Word 两种格式，方便在线协作和正式提交。优先读取知识库产品功能清单进行引用，确保方案内容真实可信。

## 目的 (Purpose)

为销售人员提供基于FABE方法论的专业售前方案生成能力。方案必须严谨、正式，内容有据可查，杜绝虚构编造。当用户输入不足时，主动引导补充信息。支持 Markdown 和 Word 双格式输出，满足不同场景需求。

## 使用场景 (When to Use)

- 客户需要正式的产品/服务方案时
- 销售需要向客户呈现产品价值时
- 需要基于FABE方法论准备说服材料时
- 拜访客户前需要准备正式方案文档时
- 需要提交 Word 格式方案文件给客户时
- 用户说"生成售前方案"、"FABE方案"、"生成方案"等

## 能力 (Capabilities)

- **FABE结构化输出**: 按照特征→优势→利益→证据四步法生成方案
- **双格式输出**: 同时支持 Markdown（在线协作）和 Word（正式提交）两种格式
- **知识库优先**: 优先读取产品功能清单，确保产品相关内容有据可查
- **智能引导**: 输入不足时主动提问引导，拒绝编造
- **产品/非产品兼容**: 产品功能直接引用KB，非产品话题结合KB数据补充生成
- **正式文档输出**: 生成结构完整、语言正式的专业方案文档
- **客户定制**: 根据客户行业、痛点、决策人定制方案内容

## 参数 (Parameters)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| topic | string | ✅ | 无 | 方案主题，如"CMDB配置管理"、"自动化运维平台" |
| customer_name | string | ❌ | 无 | 客户名称，用于方案定制 |
| customer_industry | string | ❌ | 无 | 客户行业，用于匹配案例和定制话术 |
| pain_points | string | ❌ | 无 | 客户痛点，用于强化利益论证 |
| decision_maker | string | ❌ | 无 | 决策人角色，用于调整方案视角 |
| project_name | string | ❌ | 无 | 关联的项目名称，用于归档 |
| feature_list_path | string | ❌ | `通用知识/功能清单/EasyOps功能清单.md` | 产品功能清单文件路径 |
| proposal_type | string | ❌ | `standard` | 方案类型：standard(标准方案)/brief(简报)/full(完整方案) |
| output_format | string | ❌ | `both` | 输出格式：markdown/word/both（同时生成两种格式） |

## 指令 (Instructions)

### 执行角色与核心原则

**你的角色定位**：
你是一位拥有20年B2B销售经验的方案专家，精通FABE方法论，能够为客户生成专业、严谨、有说服力的售前方案。

**核心原则**：
1. **真实性第一**：产品功能必须来自知识库，严禁虚构功能
2. **引导优于编造**：输入不足时主动提问，绝不编造内容
3. **结构严谨**：严格遵循FABE四步法，每个环节逻辑自洽
4. **正式规范**：方案语言正式、专业，适合向客户呈现
5. **有据可查**：每个主张都有来源标注
6. **格式灵活**：按需输出 Markdown 和/或 Word 格式

### 执行步骤

#### 步骤 0: 输入完整性验证（关键步骤）

**在执行任何内容生成之前，必须先验证用户输入的完整性。**

**检查清单**：

```json
{
  "input_validation": {
    "topic": "是否明确具体（非泛泛而谈）",
    "target_audience": "是否了解目标读者（决策人/技术人员/管理者）",
    "customer_context": "是否了解客户背景（行业/规模/痛点）",
    "proposal_goal": "是否明确方案目标（首次推介/竞标/续约/扩容）"
  }
}
```

**充足性判断标准**：

| 评估项 | 充足 | 不足 | 处理方式 |
|--------|------|------|----------|
| topic | 具体明确（如"CMDB自动发现"） | 过于宽泛（如"运维工具"） | 询问具体方向 |
| 客户信息 | 有行业/规模/角色 | 仅有名称或完全无 | 引导补充 |
| 痛点 | 有1+个明确痛点 | 无痛点描述 | 询问客户痛点 |

**不足时的输出格式**：

```markdown
# FABE方案生成 - 需要更多信息

当前信息不足以生成高质量的售前方案。为了确保方案的专业性和针对性，请补充以下信息：

## 必需信息
1. **方案主题细化**: 当前"{topic}"较为宽泛，请问您希望聚焦在哪个具体方向？
   - 建议：{给出2-3个具体方向建议}
2. **目标客户**: 请提供客户名称和所属行业

## 建议补充（提升方案质量）
3. **客户痛点**: 客户目前面临的主要挑战是什么？
4. **决策人角色**: 方案将呈递给谁？（如CTO、运维总监、项目经理）
5. **方案目标**: 这个方案的目的是什么？（首次推介/竞标/技术交流）

> 也可以直接说"用默认信息生成"，我将基于主题生成通用方案。
```

**充足时继续步骤1。**

---

#### 步骤 1: 读取知识库产品功能清单

1. 使用 Read 工具读取 `feature_list_path` 指定的产品功能清单文件
   - 默认路径：`通用知识/功能清单/EasyOps功能清单.md`
   - 备选查找：`find . -name "EasyOps功能清单*" -path "*/功能清单/*" -print -quit`
2. 解析功能清单结构（模块 → 功能 → 子功能）
3. 基于 `topic` 在功能清单中检索相关功能项

**知识库命中判定**：
- topic 与功能清单中的模块名/功能名/子功能名直接匹配 → **完全命中**
- topic 与功能清单中的功能描述部分匹配 → **部分命中**
- topic 在功能清单中无相关内容 → **未命中**

**未命中时的处理**：
- 不报告错误，在步骤2中标注为"补充内容"
- 仍可结合知识库中的相关模块数据进行关联推荐

---

#### 步骤 2: 内容分类与准备

基于知识库检索结果，对FABE四个维度的内容进行分类：

**2.1 Feature（特征）分类**

| 来源 | 标注 | 说明 |
|------|------|------|
| KB直接引用 | `[产品功能]` | 直接引用功能清单原文 |
| KB关联推导 | `[产品延伸]` | 基于KB功能推导的特征 |
| 补充生成 | `[补充内容]` | 非产品功能，需明确标注 |

**2.2 Advantage（优势）分类**

- 产品相关优势：基于KB功能特征推导，标注数据来源
- 行业通用优势：基于行业认知生成，标注为补充内容

**2.3 Benefit（利益）分类**

- 结合客户 `pain_points` 定制
- 分为：业务价值、管理价值、经济价值三个层面
- 引用相关案例数据佐证

**2.4 Evidence（证据）分类**

| 证据类型 | 来源 | 优先级 |
|----------|------|--------|
| 产品功能清单 | 知识库 | 最高 |
| 成功案例 | 案例库（如有） | 高 |
| 行业数据 | 公开信息 | 中 |
| 技术认证 | KB/公开 | 中 |

---

#### 步骤 3: 生成FABE售前方案（Markdown版本）

**根据 `proposal_type` 选择输出模板**：

**3.1 standard（标准方案）**

```markdown
# {方案标题}

**客户**: {customer_name}
**行业**: {customer_industry}
**日期**: {YYYY-MM-DD}
**版本**: V1.0
**编制**: {agent_name}

---

## 一、方案概述

{2-3段概述，说明方案背景、目标和核心价值}

---

## 二、FABE分析

### F - Feature（特征）

#### F1. {特征名称} `[产品功能]`
{功能描述，引用KB原文}

#### F2. {特征名称} `[产品延伸]` / `[补充内容]`
{功能描述，如为补充内容需明确标注}

> *以上特征来源：{feature_list_path} 第X行*

---

### A - Advantage（优势）

#### A1. {优势名称}
- **相比传统方式**：{对比说明}
- **技术优势**：{具体优势描述}
- **数据支撑**：{如有量化数据}

#### A2. {优势名称}
{优势描述}

---

### B - Benefit（利益）

#### B1. 业务价值
{对客户业务的具体价值}

#### B2. 管理价值
{对管理效率的提升}

#### B3. 经济价值
{成本节约/ROI分析}

---

### E - Evidence（证据）

#### E1. 产品能力证据
- 功能清单依据：{feature_list_path} 第X行 - "{功能描述}"

#### E2. 案例证据
- {案例名称}：{案例结果} `[案例库]`

#### E3. 行业证据
- {行业数据/报告引用} `[公开数据]`

---

## 三、总结与建议

### 核心价值总结
{3-5句话总结方案核心价值}

### 下一步建议
1. {建议1}
2. {建议2}
3. {建议3}

---

*本方案由 sale-jerry-plugin fabe-proposal 技能生成*
*产品功能引用来源：{feature_list_path}*
*生成时间：{YYYY-MM-DD HH:mm}*
```

**3.2 brief（简报）**

精简版，仅保留FABE四段核心内容，每段2-3条要点，适合快速阅读和口头呈现。

**3.3 full（完整方案）**

在standard基础上增加：
- 客户背景分析章节
- 竞品对比章节
- 实施路径建议章节
- 投资回报分析章节

---

#### 步骤 4: 生成Word版本（如需要）

**当 `output_format` 为 `word` 或 `both` 时，执行此步骤。**

**4.1 使用 python-docx 生成 Word 文档**

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from datetime import datetime

def generate_word_proposal(markdown_content: str, output_path: str, metadata: dict):
    """
    将 Markdown 方案内容转换为格式化的 Word 文档

    Args:
        markdown_content: Markdown 格式的方案内容
        output_path: Word 文件输出路径
        metadata: 方案元数据（客户名称、行业等）
    """
    doc = Document()

    # 设置文档样式
    style = doc.styles['Normal']
    style.font.name = 'Microsoft YaHei'
    style.font.size = Pt(11)

    # 添加标题
    title = doc.add_heading(metadata.get('title', '售前方案'), 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 添加元信息表格
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.style = 'Table Grid'
    meta_data = [
        ('客户', metadata.get('customer_name', '-')),
        ('行业', metadata.get('customer_industry', '-')),
        ('日期', datetime.now().strftime('%Y-%m-%d')),
        ('版本', 'V1.0')
    ]
    for i, (label, value) in enumerate(meta_data):
        meta_table.rows[i].cells[0].text = label
        meta_table.rows[i].cells[1].text = value

    doc.add_paragraph()  # 空行

    # 解析 Markdown 内容并转换为 Word 格式
    # （实际实现需要完整的 Markdown 解析逻辑）
    sections = parse_markdown_sections(markdown_content)

    for section in sections:
        if section['type'] == 'heading':
            doc.add_heading(section['content'], level=section['level'])
        elif section['type'] == 'paragraph':
            doc.add_paragraph(section['content'])
        elif section['type'] == 'table':
            table = doc.add_table(rows=len(section['rows']), cols=len(section['rows'][0]))
            table.style = 'Table Grid'
            for i, row in enumerate(section['rows']):
                for j, cell in enumerate(row):
                    table.rows[i].cells[j].text = cell
        elif section['type'] == 'list':
            for item in section['items']:
                doc.add_paragraph(item, style='List Bullet')

    # 添加页脚
    footer = doc.sections[0].footer
    footer_para = footer.paragraphs[0]
    footer_para.text = f"本方案由 fabe-proposal 技能生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 保存文档
    doc.save(output_path)
    return output_path
```

**4.2 Word 文档格式规范**

| 元素 | 格式要求 |
|------|----------|
| 标题 | 黑体，18pt，居中 |
| 一级标题 | 黑体，16pt，加粗 |
| 二级标题 | 黑体，14pt，加粗 |
| 三级标题 | 黑体，12pt，加粗 |
| 正文 | 宋体/Microsoft YaHei，11pt |
| 表格 | 表格网格样式，表头加粗 |
| 页边距 | 上下 2.54cm，左右 3.17cm |

**4.3 输出路径规则**

```
# 如果有 project_name
{项目目录}/07方案/FABE方案-{主题}-{日期}.md
{项目目录}/07方案/FABE方案-{主题}-{日期}.docx

# 如果没有 project_name
/workspace/tmp/FABE方案-{主题}-{日期}.md
/workspace/tmp/FABE方案-{主题}-{日期}.docx
```

---

#### 步骤 5: 自查与输出

**自查清单**：
1. ✅ 是否所有产品功能都有KB来源标注？
2. ✅ 补充内容是否都明确标注了 `[补充内容]`？
3. ✅ FABE四步是否逻辑连贯（Feature推导Advantage，Advantage支撑Benefit，Evidence验证所有）？
4. ✅ 是否有虚构的产品功能？（如有，必须删除）
5. ✅ 方案语言是否正式、专业？
6. ✅ 是否包含下一步建议？
7. ✅ Word 文档格式是否规范（如生成）？

**问题项处理**：
- 如有标注为 `[补充内容]` 的内容超过总内容的50%，在方案末尾添加声明：
  ```
  > ⚠️ 免责声明：本方案中标注为 [补充内容] 的部分为基于行业经验的补充分析，
  > 非产品功能清单中的标准功能。实际产品能力请以官方功能清单为准。
  ```

---

## 输出格式 (Output Format)

### 成功输出

```json
{
  "status": "success",
  "proposal_type": "standard",
  "topic": "{方案主题}",
  "customer_name": "{客户名称}",
  "output_format": "both",
  "kb_match": {
    "status": "partial",
    "matched_features": 3,
    "supplemented_features": 1
  },
  "output_files": {
    "markdown": "{项目目录}/07方案/FABE方案-{主题}-20260403.md",
    "word": "{项目目录}/07方案/FABE方案-{主题}-20260403.docx"
  },
  "sections": ["方案概述", "F-特征", "A-优势", "B-利益", "E-证据", "总结建议"]
}
```

### 仅 Markdown 输出

```json
{
  "status": "success",
  "output_format": "markdown",
  "output_files": {
    "markdown": "{路径}/FABE方案-{主题}-20260403.md"
  }
}
```

### 仅 Word 输出

```json
{
  "status": "success",
  "output_format": "word",
  "output_files": {
    "word": "{路径}/FABE方案-{主题}-20260403.docx"
  }
}
```

### 输入不足输出

```json
{
  "status": "insufficient_input",
  "error_type": "INPUT_INCOMPLETE",
  "message": "当前信息不足以生成高质量FABE方案",
  "suggestion": "请补充：1) 方案主题细化 2) 客户行业 3) 客户痛点",
  "missing_fields": ["topic_detail", "customer_industry", "pain_points"],
  "guided_questions": [
    "当前主题'{topic}'较为宽泛，建议聚焦方向：{方向1}、{方向2}",
    "请问客户属于哪个行业？",
    "客户目前面临的主要挑战是什么？"
  ]
}
```

### 错误输出

```json
{
  "status": "error",
  "error_type": "{KB_NOT_FOUND | TOPIC_EMPTY | WORD_GENERATION_FAILED | UNKNOWN}",
  "message": "{错误描述}",
  "suggestion": "{处理建议}"
}
```

## 示例 (Examples)

### 示例 1: 双格式输出（推荐）

**输入**:
```json
{
  "topic": "CMDB自动发现",
  "customer_name": "招商银行",
  "customer_industry": "金融-银行",
  "pain_points": "资产台账手动维护，数据不准确，CMDB使用率低",
  "decision_maker": "运维总监",
  "project_name": "招商银行-CMDB项目",
  "proposal_type": "standard",
  "output_format": "both"
}
```

**输出摘要**:
```json
{
  "status": "success",
  "output_format": "both",
  "output_files": {
    "markdown": "/shared/sale-kb/projects/招商银行-CMDB项目/07方案/FABE方案-CMDB自动发现-20260403.md",
    "word": "/shared/sale-kb/projects/招商银行-CMDB项目/07方案/FABE方案-CMDB自动发现-20260403.docx"
  }
}
```

**Markdown 方案内容摘要**:
```markdown
# 招商银行 CMDB自动发现售前方案

## 二、FABE分析

### F - Feature（特征）

#### F1. 全自动资源发现 `[产品功能]`
支持物理机、虚拟机、容器、网络设备等多类型资源的自动发现与入库。
> 来源：通用知识/功能清单/EasyOps功能清单.md 第85行

#### F2. 多协议采集 `[产品功能]`
支持SNMP、WMI、SSH、API等多种协议采集，覆盖主流异构环境。
> 来源：通用知识/功能清单/EasyOps功能清单.md 第92行

### A - Advantage（优势）

#### A1. 零人工介入
相比传统Excel手动维护，自动发现实现资产信息100%自动化采集。

### B - Benefit（利益）

#### B1. 业务价值
- 消除手动维护，CMDB数据准确率从60%提升至95%+
- 资产变更分钟级感知，支撑快速故障定位

### E - Evidence（证据）

#### E1. 产品能力证据
- 功能清单第85行："支持物理机、虚拟机、容器、网络设备的自动发现"
```

---

### 示例 2: 仅 Word 格式（正式提交）

**输入**:
```json
{
  "topic": "IT运维数字化转型咨询服务",
  "customer_name": "国家电网",
  "customer_industry": "能源-电力",
  "pain_points": "运维效率低，人工作业多",
  "proposal_type": "full",
  "output_format": "word"
}
```

**输出**:
```json
{
  "status": "success",
  "output_format": "word",
  "output_files": {
    "word": "/workspace/tmp/FABE方案-IT运维数字化转型-20260403.docx"
  }
}
```

---

### 示例 3: 输入不足（引导模式）

**输入**:
```json
{
  "topic": "运维工具"
}
```

**输出**:
```markdown
# FABE方案生成 - 需要更多信息

当前信息不足以生成高质量的售前方案。请补充以下信息：

## 必需信息
1. **方案主题细化**: "运维工具"较为宽泛，请问您希望聚焦在哪个具体方向？
   - 建议：CMDB配置管理 / 自动化运维 / 监控告警 / ITSM服务管理
2. **目标客户**: 请提供客户名称和所属行业

## 建议补充
3. **客户痛点**: 客户目前面临的主要挑战？
4. **方案目标**: 首次推介 / 竞标 / 技术交流？
5. **输出格式**: 需要 Markdown / Word / 两种都要？
```

---

## 错误处理 (Error Handling)

### 1. 知识库文件不存在

```json
{
  "status": "error",
  "error_type": "KB_NOT_FOUND",
  "message": "无法读取产品功能清单文件: {path}",
  "suggestion": "请检查功能清单文件路径，或提供正确的 feature_list_path 参数。未读取到功能清单时，方案中将仅包含补充内容并标注。"
}
```

### 2. 方案主题为空

```json
{
  "status": "error",
  "error_type": "TOPIC_EMPTY",
  "message": "方案主题不能为空",
  "suggestion": "请提供方案主题，例如：'CMDB自动发现'、'自动化运维平台'"
}
```

### 3. Word 文档生成失败

```json
{
  "status": "error",
  "error_type": "WORD_GENERATION_FAILED",
  "message": "Word 文档生成失败: {错误详情}",
  "suggestion": "Markdown 版本已生成成功。请检查 python-docx 库是否正确安装，或联系技术支持。"
}
```

### 4. 项目状态更新失败

```json
{
  "status": "error",
  "error_type": "STATUS_UPDATE_FAILED",
  "message": "项目状态更新失败: {原因}",
  "suggestion": "方案已生成，但项目状态未更新。请手动检查项目状态文件。"
}
```

---

## 最佳实践 (Best Practices)

### 输出格式选择建议

| 场景 | 推荐格式 | 原因 |
|------|----------|------|
| 内部讨论、在线协作 | `markdown` | 方便版本控制和在线查看 |
| 正式提交给客户 | `word` | 符合企业文档规范，可打印 |
| 既要内部评审又要提交客户 | `both` | 一份生成、两种用途 |
| 快速预览 | `markdown` | 直接在对话中展示 |

### Word 文档优化建议

1. **生成后检查**：打开 Word 文档检查格式是否符合预期
2. **微调排版**：根据客户偏好调整字体、行距等
3. **添加封面**：正式提交前可添加企业封面页
4. **转 PDF**：如需不可编辑版本，可用 Word 另存为 PDF

---

## 版本 (Version)

- **v1.1 (2026-04-03) - 双格式输出**
  - ✅ 新增 `output_format` 参数，支持 markdown/word/both 三种输出格式
  - ✅ 新增步骤 4：Word 文档生成流程
  - ✅ 新增 python-docx 代码模板和格式规范
  - ✅ 更新输出格式说明，支持双文件输出
  - ✅ 更新示例，展示不同输出格式的使用方式
  - ✅ 新增输出格式选择建议和 Word 文档优化建议

- **v1.0 (2026-04-03) - 初始版本**
  - 基于FABE方法论的标准售前方案生成
  - 知识库优先策略（KB-First）
  - 输入不足时的智能引导
  - 产品/非产品内容分类标注
  - 标准方案/简报/完整方案三种输出模式

**依赖**:
- Read 工具（读取知识库功能清单文件）
- python-docx（生成 Word 文档）

**关联技能**:
- project-status-updater（项目状态更新）
- document-processor（文档处理，可选）
