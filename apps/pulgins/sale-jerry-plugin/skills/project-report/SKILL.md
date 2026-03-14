---
name: project-report
description: 立项报告生成技能，根据企业名称和模块名称，智能搜索知识库中的相关模板和资料，自动生成定制化的立项报告文档。支持CMDB、ITSM、自动化运维、监控等各类运维模块。当用户说"生成立项报告"、"创建立项报告"、"生成项目报告"、"制作立项文档"时触发。
category: document-generation
priority: high
---

# Project Report（立项报告生成技能）

## Purpose

为销售和售前团队提供智能化的立项报告生成能力。根据用户输入的企业名称和模块名称，自动搜索知识库中的相关模板、解决方案和案例资料，综合生成专业的Word格式立项报告。

**核心功能**:
- 智能搜索知识库中的相关模板和资料
- 支持 CMDB、ITSM、自动化运维、监控等多种模块
- 自动整合解决方案、案例和最佳实践
- 生成专业的 Word (.docx) 格式报告

**核心价值**:
- ✅ **智能检索**：自动搜索知识库中的相关模板和资料
- ✅ **内容丰富**：整合解决方案、案例、最佳实践等多源内容
- ✅ **模块通用**：支持各类运维模块，不限于单一领域
- ✅ **专业输出**：生成结构完整、内容专业的立项报告

## When to Use

在以下情况下使用此技能：
- 销售需要为客户准备特定模块的立项报告
- 售前需要快速输出专业方案文档
- 需要基于知识库资料生成综合报告
- 需要生成 Word 格式的正式立项文档

## Capabilities

### 1. 智能资料检索
- 根据模块名称搜索知识库中的相关模板
- 检索相关的解决方案文档
- 查找匹配的案例资料
- 搜索最佳实践和规范文档

### 2. 内容智能整合
- 整合多源资料生成完整报告
- 按标准结构组织内容
- 保持内容的逻辑性和连贯性
- 自动填充企业名称和日期

### 3. 模块支持范围
- CMDB（配置管理数据库）
- ITSM（IT服务管理）
- 自动化运维
- 监控告警
- DevOps
- 日志分析
- 其他运维相关模块

### 4. 文档生成
- 生成标准 Word (.docx) 格式
- 保持专业的文档格式
- 支持自定义输出路径

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| company_name | string | ✅ | - | 企业名称，将填充到报告中 |
| module_name | string | ✅ | - | 模块名称，如 CMDB、ITSM、自动化运维、监控等 |
| output_path | string | ❌ | /workspace/tmp/ | 输出文件保存路径 |
| output_filename | string | ❌ | 自动生成 | 输出文件名，默认为"{企业名称}-{模块名称}立项报告-{日期}.docx" |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的方案文档生成专家，精通运维领域各类模块的方案编写，能够智能整合知识库资料生成立项报告。

**你的任务目标**：
根据用户输入的企业名称和模块名称，搜索知识库相关资料，生成专业、完整的立项报告。

**核心原则**：
- 智能检索：充分搜索知识库中的相关资料
- 内容准确：基于真实资料，不编造内容
- 结构清晰：按照标准立项报告结构组织内容
- 专业输出：生成可直接使用的高质量文档

### 执行步骤

#### 步骤 1: 参数验证

**1.1 检查必要参数**

检查用户是否提供了 `company_name` 和 `module_name` 参数：

```python
def validate_params(company_name, module_name):
    """验证必要参数"""
    missing = []

    if not company_name:
        missing.append("企业名称")

    if not module_name:
        missing.append("模块名称（如：CMDB、ITSM、自动化运维、监控等）")

    if missing:
        return False, f"请提供以下信息：{', '.join(missing)}"

    return True, None
```

如果参数缺失，向用户询问：

```
请提供以下信息以生成立项报告：

1. 企业名称：例如"某某银行"、"某某证券"
2. 模块名称：例如"CMDB"、"ITSM"、"自动化运维"、"监控"等

示例：请为"招商银行"生成"CMDB"模块的立项报告
```

#### 步骤 2: 知识库资料检索

**2.1 搜索相关模板**

根据模块名称搜索知识库中的立项报告模板：

```python
KNOWLEDGE_BASE_PATH = "/shared/sale-kb"

def search_templates(module_name):
    """搜索相关立项报告模板"""
    import os

    templates = []
    project_path = os.path.join(KNOWLEDGE_BASE_PATH, "项目资料")

    # 模板关键词映射
    template_keywords = {
        "cmdb": ["cmdb", "配置管理", "资产"],
        "itsm": ["itsm", "服务管理", "流程"],
        "自动化": ["自动化", "automation"],
        "监控": ["监控", "monitor", "告警"],
        "devops": ["devops", "持续集成"],
        "日志": ["日志", "log"],
    }

    # 根据模块名称确定搜索关键词
    keywords = []
    module_lower = module_name.lower()
    for key, words in template_keywords.items():
        if key in module_lower:
            keywords = words
            break

    if not keywords:
        keywords = [module_name]

    # 搜索匹配的模板文件
    for file in os.listdir(project_path):
        file_lower = file.lower()
        if any(kw in file_lower for kw in keywords) and (file.endswith(".doc") or file.endswith(".docx")):
            if "立项" in file or "报告" in file or "方案" in file:
                templates.append(os.path.join(project_path, file))

    return templates
```

**2.2 搜索相关解决方案**

```python
def search_solutions(module_name):
    """搜索相关解决方案文档"""
    import os

    solutions = []
    solution_path = os.path.join(KNOWLEDGE_BASE_PATH, "解决方案")

    # 搜索关键词
    keywords = get_module_keywords(module_name)

    for file in os.listdir(solution_path):
        file_lower = file.lower()
        if any(kw in file_lower for kw in keywords):
            solutions.append(os.path.join(solution_path, file))

    return solutions
```

**2.3 搜索相关案例**

```python
def search_cases(module_name, industry=None):
    """搜索相关案例"""
    import os

    cases = []
    case_path = os.path.join(KNOWLEDGE_BASE_PATH, "行业案例")

    keywords = get_module_keywords(module_name)

    for file in os.listdir(case_path):
        file_lower = file.lower()
        if any(kw in file_lower for kw in keywords):
            cases.append(os.path.join(case_path, file))

    return cases
```

#### 步骤 3: 内容整合与报告生成

**3.1 确定报告结构**

标准立项报告结构：

```markdown
1. 项目建设背景
2. 项目建设目标
3. 项目建设范围
4. 平台建设路线
   - 建设方法体系
   - 设计理念
   - 技术路线
5. 平台总体架构设计
   - 功能架构
   - 技术架构
6. 功能模块设计
7. 项目实施计划
8. 投资估算
9. 预期效益
10. 成功案例（从知识库获取）
```

**3.2 读取并整合资料**

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os

def generate_report(company_name, module_name, templates, solutions, cases):
    """生成立项报告"""

    # 优先使用匹配的模板，否则使用默认模板
    if templates:
        template_path = templates[0]
    else:
        template_path = "/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx"

    print(f"📖 使用模板: {template_path}")

    # 加载模板
    doc = Document(template_path)

    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月")
    current_year = datetime.now().strftime("%Y年")

    # 模块名称标准化
    module_title = standardize_module_name(module_name)

    # 替换规则
    replacements = {
        "优维科技（深圳）有限公司": company_name,
        "优维科技": company_name,
        "2025年6月": current_date,
        "2025年": current_year,
        "2024年": current_year,
        "2023年": current_year,
        "一体化运维": module_title,
        "运维平台": f"{module_title}平台",
    }

    # 替换文档内容
    replace_document_content(doc, replacements)

    # 如果有案例资料，添加案例章节
    if cases:
        add_case_section(doc, cases, module_name)

    return doc

def standardize_module_name(module_name):
    """标准化模块名称"""
    name_map = {
        "cmdb": "CMDB配置管理",
        "itsm": "IT服务管理",
        "自动化": "自动化运维",
        "监控": "监控告警",
        "devops": "DevOps",
    }

    module_lower = module_name.lower()
    for key, value in name_map.items():
        if key in module_lower:
            return value

    return module_name

def replace_document_content(doc, replacements):
    """替换文档内容"""
    # 替换段落
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                for run in para.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)

    # 替换表格
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old, new in replacements.items():
                        if old in para.text:
                            for run in para.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)
```

**3.3 添加案例章节**

```python
def add_case_section(doc, cases, module_name):
    """添加相关案例章节"""
    # 找到合适的位置插入案例章节
    # 通常在"预期效益"之前

    # 读取案例资料并提取关键信息
    case_info = extract_case_info(cases[:3])  # 最多使用3个案例

    # 添加案例章节标题
    heading = doc.add_heading('成功案例', level=1)

    # 添加案例内容
    for case in case_info:
        doc.add_heading(case['name'], level=2)
        doc.add_paragraph(case['description'])
```

#### 步骤 4: 保存文档

**4.1 生成文件名并保存**

```python
def save_report(doc, company_name, module_name, output_path="/workspace/tmp/"):
    """保存报告"""
    import os

    # 生成文件名
    date_str = datetime.now().strftime("%Y%m%d")
    module_standard = standardize_module_name(module_name)
    filename = f"{company_name}-{module_standard}立项报告-{date_str}.docx"

    # 确保目录存在
    os.makedirs(output_path, exist_ok=True)

    # 保存
    full_path = os.path.join(output_path, filename)
    doc.save(full_path)

    return full_path
```

#### 步骤 5: 输出结果

**5.1 输出生成结果**

```markdown
✅ 立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | {company_name} |
| 模块名称 | {module_name} |
| 生成日期 | {current_date} |
| 文件名 | {filename} |
| 文件路径 | {output_path} |
| 文件大小 | {file_size} KB |

## 📚 使用的知识库资料

### 模板文件
- {template_name}

### 解决方案参考
- {solution_1}
- {solution_2}

### 案例参考
- {case_1}
- {case_2}

## 📋 文档内容结构
1. 项目建设背景
2. 项目建设目标
3. 项目建设范围
4. 平台建设路线
5. 平台总体架构设计
6. 功能模块设计
7. 项目实施计划
8. 投资估算
9. 预期效益
10. 成功案例

📥 **文件下载路径**: `{output_path}`
```

## 模块内容映射表

**核心功能章节与模块对应关系**：

| 模块类型 | 保留的功能章节 | 移除的功能章节 |
|---------|---------------|---------------|
| CMDB | IT资源管理 | 统一监控告警管理、IT服务流程管理、自动化运维、可视化管理 |
| 监控 | 统一监控告警管理 | IT资源管理、IT服务流程管理、自动化运维、可视化管理 |
| ITSM | IT服务流程管理 | IT资源管理、统一监控告警管理、自动化运维、可视化管理 |
| 自动化 | 自动化运维 | IT资源管理、统一监控告警管理、IT服务流程管理、可视化管理 |
| DevOps | 自动化运维 + IT服务流程管理 | IT资源管理、统一监控告警管理、可视化管理 |

**通用章节（始终保留）**：
- 项目建设背景
- 项目建设目标
- 项目建设范围
- 平台建设路线
- 平台总体架构设计
- 系统创新点
- 项目实施计划
- 项目风险及应急预案
- 效益分析

### 完整执行代码

```python
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
import os
import re
import copy

# 知识库路径
KNOWLEDGE_BASE = "/shared/sale-kb"
DEFAULT_TEMPLATE = "/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx"

# 模块-章节映射（定义各模块需要保留的功能章节）
MODULE_SECTION_MAP = {
    "cmdb": {
        "title": "CMDB配置管理",
        "keywords": ["cmdb", "配置管理", "资产"],
        "keep_sections": ["IT资源管理"],
        "remove_sections": ["统一监控告警管理", "IT服务流程管理", "自动化运维", "可视化管理"],
        # 创新点内容过滤
        "keep_innovations": ["图数据库", "模型设计", "自动采集", "Agent能力", "API能力"],
        "remove_innovations": ["自动化运维标准化", "可视化能力", "故障影响"]
    },
    "监控": {
        "title": "监控告警管理",
        "keywords": ["监控", "告警", "monitor"],
        "keep_sections": ["统一监控告警管理"],
        "remove_sections": ["IT资源管理", "IT服务流程管理", "自动化运维", "可视化管理"],
        "keep_innovations": ["监控", "告警", "可视化", "API能力"],
        "remove_innovations": ["图数据库", "模型设计"]
    },
    "itsm": {
        "title": "IT服务管理",
        "keywords": ["itsm", "服务管理", "流程"],
        "keep_sections": ["IT服务流程管理"],
        "remove_sections": ["IT资源管理", "统一监控告警管理", "自动化运维", "可视化管理"],
        "keep_innovations": ["流程", "服务", "API能力"],
        "remove_innovations": []
    },
    "自动化": {
        "title": "自动化运维",
        "keywords": ["自动化", "automation"],
        "keep_sections": ["自动化运维"],
        "remove_sections": ["IT资源管理", "统一监控告警管理", "IT服务流程管理", "可视化管理"],
        "keep_innovations": ["自动化", "Agent能力", "API能力"],
        "remove_innovations": ["图数据库", "模型设计", "可视化"]
    },
    "devops": {
        "title": "DevOps持续交付",
        "keywords": ["devops", "持续集成"],
        "keep_sections": ["自动化运维", "IT服务流程管理"],
        "remove_sections": ["IT资源管理", "统一监控告警管理", "可视化管理"],
        "keep_innovations": ["自动化", "Agent能力", "流程", "API能力"],
        "remove_innovations": ["图数据库"]
    }
}

# 始终保留的通用章节
COMMON_SECTIONS = [
    "项目建设背景", "项目建设目标", "项目建设范围",
    "平台建设路线", "平台总体架构设计", "系统创新点",
    "项目实施计划", "项目风险及应急预案", "效益分析"
]

def get_module_config(module_name):
    """根据模块名称获取配置"""
    module_lower = module_name.lower()

    for key, config in MODULE_SECTION_MAP.items():
        if key in module_lower:
            return config

    # 默认返回CMDB配置
    return MODULE_SECTION_MAP["cmdb"]

def standardize_module_name(module_name):
    """标准化模块名称"""
    config = get_module_config(module_name)
    return config["title"]

def get_module_keywords(module_name):
    """获取模块相关的搜索关键词"""
    config = get_module_config(module_name)
    return config["keywords"]

def find_heading_index(doc, heading_text, start_idx=0):
    """查找指定标题的段落索引"""
    for i, para in enumerate(doc.paragraphs[start_idx:], start=start_idx):
        if para.style.name.startswith('Heading') and heading_text in para.text:
            return i
    return -1

def get_heading_level(para):
    """获取标题级别"""
    if para.style.name.startswith('Heading'):
        try:
            return int(para.style.name.replace('Heading ', ''))
        except:
            return 1
    return 0

def find_section_range(doc, section_title, start_idx=0):
    """找到章节的开始和结束索引"""
    start = find_heading_index(doc, section_title, start_idx)
    if start == -1:
        return None, None

    # 获取章节标题的级别
    section_level = get_heading_level(doc.paragraphs[start])

    # 找到下一个同级或更高级标题
    end = len(doc.paragraphs)
    for i in range(start + 1, len(doc.paragraphs)):
        level = get_heading_level(doc.paragraphs[i])
        if level > 0 and level <= section_level:
            end = i
            break

    return start, end

def remove_section(doc, section_title):
    """移除指定章节及其子内容"""
    start, end = find_section_range(doc, section_title)

    if start is None:
        return 0

    # 从后向前删除段落
    for i in range(end - 1, start - 1, -1):
        p = doc.paragraphs[i]._element
        p.getparent().remove(p)

    return end - start

def filter_content_by_module(doc, module_name):
    """根据模块过滤文档内容"""
    config = get_module_config(module_name)
    removed_count = 0

    # 移除不需要的功能章节
    for section in config["remove_sections"]:
        count = remove_section(doc, section)
        if count > 0:
            print(f"   ✓ 移除章节: {section} ({count}段)")
            removed_count += count

    # 过滤系统创新点中的不相关内容
    innovation_removed = filter_innovation_section(doc, module_name)
    if innovation_removed > 0:
        print(f"   ✓ 过滤创新点: 移除 {innovation_removed} 项不相关内容")
        removed_count += innovation_removed

    return removed_count

def filter_innovation_section(doc, module_name):
    """过滤系统创新点章节中与模块无关的内容"""
    config = get_module_config(module_name)
    remove_keywords = config.get("remove_innovations", [])

    if not remove_keywords:
        return 0

    # 找到系统创新点章节范围
    start, end = find_section_range(doc, "系统创新点")
    if start is None:
        return 0

    removed = 0
    # 从后向前删除不相关的子标题（Heading 2）
    for i in range(end - 1, start, -1):
        para = doc.paragraphs[i]
        level = get_heading_level(para)

        if level == 2:  # 只处理二级标题
            text = para.text.strip()
            should_remove = False
            for kw in remove_keywords:
                if kw in text:
                    should_remove = True
                    break

            if should_remove:
                p = para._element
                p.getparent().remove(p)
                removed += 1

    return removed

def update_section_content(doc, module_name):
    """更新章节内容以适配模块"""
    config = get_module_config(module_name)
    module_title = config["title"]

    # 如果只有一个保留章节，将其提升为"平台功能设计"
    if len(config["keep_sections"]) == 1:
        keep_section = config["keep_sections"][0]
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading 2') and keep_section in para.text:
                # 改为功能设计
                para.clear()
                run = para.add_run(f"{module_title}功能设计")
                break

def search_files(directory, keywords, extensions):
    """搜索匹配的文件"""
    if not os.path.exists(directory):
        return []

    results = []
    for file in os.listdir(directory):
        file_lower = file.lower()
        if any(ext in file_lower for ext in extensions):
            if any(kw in file_lower for kw in keywords):
                results.append(os.path.join(directory, file))

    return results

def generate_project_report(company_name, module_name, output_path="/workspace/tmp/"):
    """
    生成立项报告

    Args:
        company_name: 企业名称
        module_name: 模块名称（CMDB/ITSM/自动化/监控等）
        output_path: 输出路径

    Returns:
        生成的文件路径
    """
    print(f"🚀 开始生成立项报告...")
    print(f"   企业: {company_name}")
    print(f"   模块: {module_name}")

    # 获取模块配置
    module_config = get_module_config(module_name)
    module_title = module_config["title"]
    print(f"   模块标准化名称: {module_title}")

    # 1. 搜索相关模板
    print("\n📖 搜索知识库模板...")
    templates = search_files(
        os.path.join(KNOWLEDGE_BASE, "项目资料"),
        get_module_keywords(module_name),
        [".doc", ".docx"]
    )
    if templates:
        print(f"   找到模板: {os.path.basename(templates[0])}")

    # 2. 搜索相关解决方案
    print("\n📚 搜索解决方案资料...")
    solutions = search_files(
        os.path.join(KNOWLEDGE_BASE, "解决方案"),
        get_module_keywords(module_name),
        [".pdf", ".pptx", ".docx"]
    )
    print(f"   找到 {len(solutions)} 份相关资料")

    # 3. 搜索相关案例
    print("\n🏆 搜索相关案例...")
    cases = search_files(
        os.path.join(KNOWLEDGE_BASE, "行业案例"),
        get_module_keywords(module_name),
        [".pdf", ".pptx"]
    )
    print(f"   找到 {len(cases)} 个相关案例")

    # 4. 加载模板
    template_path = templates[0] if templates else DEFAULT_TEMPLATE
    print(f"\n📝 使用模板: {os.path.basename(template_path)}")
    doc = Document(template_path)

    # 5. 内容过滤 - 核心改进！
    print(f"\n🔧 内容过滤 (保留{module_title}相关内容)...")
    removed_count = filter_content_by_module(doc, module_name)
    print(f"   共移除 {removed_count} 段非相关内容")

    # 6. 更新章节标题
    update_section_content(doc, module_name)

    # 7. 内容替换
    current_date = datetime.now().strftime("%Y年%m月")
    current_year = datetime.now().strftime("%Y年")

    replacements = {
        "优维科技（深圳）有限公司": company_name,
        "优维科技": company_name,
        "2025年6月": current_date,
        "2025年": current_year,
        "2024年": current_year,
        "2023年": current_year,
        "一体化运维": module_title,
        "运维平台": f"{module_title}平台",
    }

    replace_count = 0
    # 替换段落
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                for run in para.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)
                        replace_count += 1

    # 替换表格
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old, new in replacements.items():
                        if old in para.text:
                            for run in para.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)

    print(f"   内容替换: {replace_count} 处")

    # 8. 保存文档
    os.makedirs(output_path, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{company_name}-{module_title}立项报告-{date_str}.docx"
    full_path = os.path.join(output_path, filename)
    doc.save(full_path)

    file_size = os.path.getsize(full_path) / 1024
    print(f"\n✅ 报告生成成功!")
    print(f"   文件名: {filename}")
    print(f"   文件路径: {full_path}")
    print(f"   文件大小: {file_size:.1f} KB")

    return full_path, templates, solutions, cases

def main():
    """主函数 - 用于测试"""
    import sys

    # 从命令行参数或使用默认值
    company = sys.argv[1] if len(sys.argv) > 1 else "测试企业"
    module = sys.argv[2] if len(sys.argv) > 2 else "CMDB"

    generate_project_report(company, module)

if __name__ == "__main__":
    main()
```

## Output Format

### 成功输出

```markdown
✅ 立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | {company_name} |
| 模块名称 | {module_name} |
| 生成日期 | {current_date} |
| 文件名 | {filename} |
| 文件路径 | {output_path} |
| 文件大小 | {file_size} KB |

## 📚 使用的知识库资料

### 模板文件
- {template_name}

### 解决方案参考
- {solution_1}
- {solution_2}

### 案例参考
- {case_1}
- {case_2}

## 📋 文档结构
1. 项目建设背景
2. 项目建设目标
3. 项目建设范围
4. 平台建设路线
5. 平台总体架构设计
6. 功能模块设计
7. 项目实施计划
8. 预期效益

📥 **下载路径**: `{output_path}`
```

### 缺少参数输出

```markdown
⚠️ 请提供完整信息

生成立项报告需要以下信息：

1. **企业名称** - 例如：某某银行、某某证券
2. **模块名称** - 例如：CMDB、ITSM、自动化运维、监控

**使用示例**:
```
请为"招商银行"生成"CMDB"模块的立项报告
请为"华安证券"生成"自动化运维"的立项报告
```

### 模板未找到输出

```markdown
⚠️ 未找到专用模板

未找到"{module_name}"模块的专用模板，将使用通用立项报告模板生成。

如需更专业的内容，建议：
1. 在知识库中添加相关模块的模板
2. 手动补充模块特定的内容
```

## Integration

### 与其他 Skills 的协作

| Skill | 协作方式 | 说明 |
|-------|---------|------|
| company-research | 前置调研 | 先调研企业背景，丰富报告内容 |
| case-matching | 案例匹配 | 智能匹配相关案例加入报告 |
| project-init | 项目初始化 | 生成报告后可初始化项目目录 |
| sales-prep | 销售准备 | 作为销售准备材料的一部分 |

### 模块关键词映射

| 用户输入 | 标准名称 | 搜索关键词 |
|---------|---------|-----------|
| CMDB、配置管理 | CMDB配置管理 | cmdb, 配置, 资产, 资源 |
| ITSM、服务管理 | IT服务管理 | itsm, 服务, 流程, 工单 |
| 自动化、Automation | 自动化运维 | 自动化, automation |
| 监控、告警 | 监控告警 | 监控, monitor, 告警 |
| DevOps、持续集成 | DevOps | devops, 持续, ci/cd |

## Best Practices

### 参数输入规范
- ✅ 企业名称：使用完整或常用简称
- ✅ 模块名称：使用标准术语或常用简称
- ❌ 避免使用模糊或不规范的名称

### 输出路径建议
- ✅ 使用 `/workspace/tmp/` 便于下载
- ✅ 文件名包含日期便于版本管理
- ❌ 避免使用系统目录

### 文档后续处理
1. 根据客户实际情况调整项目范围
2. 补充客户的IT资产数据
3. 调整项目实施时间节点
4. 根据实际情况调整投资估算

## Notes

1. **智能检索**：自动搜索知识库中的相关模板和资料
2. **模块通用**：支持各类运维模块，自动匹配关键词
3. **资料整合**：整合模板、解决方案、案例等多源内容
4. **日期自动**：使用当前日期，无需手动输入
5. **格式保持**：生成的文档保持模板原有的格式和样式

## Examples

### 示例 1: CMDB 模块

**用户输入**:
```
请为"招商银行"生成CMDB模块的立项报告
```

**执行过程**:
```
🚀 开始生成立项报告...
   企业: 招商银行
   模块: CMDB

📖 搜索知识库模板...
   找到模板: 一体化运维平台建设立项报告v2.0.docx

📚 搜索解决方案资料...
   找到 2 份相关资料

🏆 搜索相关案例...
   找到 3 个相关案例

📝 使用模板: 一体化运维平台建设立项报告v2.0.docx

✅ 报告生成成功!
```

**输出**:
```markdown
✅ 立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 招商银行 |
| 模块名称 | CMDB配置管理 |
| 文件名 | 招商银行-CMDB配置管理立项报告-20260314.docx |
| 文件路径 | /workspace/tmp/招商银行-CMDB配置管理立项报告-20260314.docx |

📥 **下载路径**: `/workspace/tmp/招商银行-CMDB配置管理立项报告-20260314.docx`
```

### 示例 2: 自动化运维模块

**用户输入**:
```
请为"华安证券"生成自动化运维的立项报告
```

**输出**:
```markdown
✅ 立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 华安证券 |
| 模块名称 | 自动化运维 |
| 文件名 | 华安证券-自动化运维立项报告-20260314.docx |
| 文件路径 | /workspace/tmp/华安证券-自动化运维立项报告-20260314.docx |

📥 **下载路径**: `/workspace/tmp/华安证券-自动化运维立项报告-20260314.docx`
```

### 示例 3: ITSM 模块

**用户输入**:
```
请为"农夫山泉"生成ITSM的立项报告
```

**输出**:
```markdown
✅ 立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 农夫山泉 |
| 模块名称 | IT服务管理 |
| 文件名 | 农夫山泉-IT服务管理立项报告-20260314.docx |
| 文件路径 | /workspace/tmp/农夫山泉-IT服务管理立项报告-20260314.docx |

📥 **下载路径**: `/workspace/tmp/农夫山泉-IT服务管理立项报告-20260314.docx`
```

---

**版本**: 1.0
**最后更新**: 2026-03-14
**作者**: AI Solutions Expert Team
**依赖**: python-docx
