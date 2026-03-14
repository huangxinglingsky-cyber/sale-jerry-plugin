---
name: cmdb-project-report
description: CMDB立项报告生成技能，根据知识库中的立项报告模板，自动生成定制化的CMDB立项报告文档。用户只需输入企业名称，即可生成包含当前日期、企业定制内容的Word格式立项报告。当用户说"生成立项报告"、"创建立项报告"、"生成CMDB报告"、"制作立项文档"时触发。
category: document-generation
priority: high
---

# CMDB Project Report（CMDB立项报告生成技能）

## Purpose

为销售和售前团队提供快速生成CMDB立项报告的能力，基于知识库中的标准模板，自动填充企业名称、日期等信息，生成专业的Word格式立项报告。

**核心功能**:
- 自动读取知识库中的立项报告模板
- 智能替换企业名称和日期
- 保持模板原有格式和结构
- 生成标准 Word (.docx) 格式文档
- 支持自定义输出路径

**核心价值**:
- ✅ **高效便捷**：一键生成专业立项报告，节省大量文档编写时间
- ✅ **标准规范**：基于统一模板，确保报告格式和内容的一致性
- ✅ **专业定制**：自动填充企业信息，生成专属定制报告
- ✅ **即下即用**：输出 Word 格式，方便编辑和分享

## When to Use

在以下情况下使用此技能：
- 销售需要为客户准备立项报告
- 售前需要快速输出项目方案文档
- 需要基于标准模板生成定制化报告
- 需要生成 Word 格式的正式文档

## Capabilities

### 1. 模板智能读取
- 自动定位知识库中的立项报告模板
- 支持 .docx 格式模板文件
- 保留模板的格式、样式和表格结构

### 2. 内容智能替换
- 自动替换企业名称占位符
- 自动填充当前日期
- 支持其他动态字段替换

### 3. 文档生成
- 生成标准 Word (.docx) 格式
- 保持原文档的所有格式
- 支持自定义文件名和输出路径

### 4. 错误处理
- 模板文件不存在时的友好提示
- 参数缺失时的智能提示
- 文件保存失败时的重试建议

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| company_name | string | ✅ | - | 企业名称，将替换模板中的企业名称占位符 |
| output_path | string | ❌ | ./ | 输出文件保存路径，默认为当前工作目录 |
| output_filename | string | ❌ | 自动生成 | 输出文件名，默认为"{企业名称}-CMDB立项报告-{日期}.docx" |
| template_file | string | ❌ | 默认模板 | 自定义模板文件路径，不指定则使用知识库默认模板 |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的文档生成助手，专门帮助销售和售前团队快速生成标准化的立项报告文档。

**你的任务目标**：
根据用户输入的企业名称，基于知识库中的标准模板，快速生成定制化的CMDB立项报告。

**核心原则**：
- 准确性：确保企业名称和日期正确填充
- 完整性：保持模板的完整结构和格式
- 高效性：快速完成文档生成
- 可用性：生成的文档可直接使用和编辑

### 执行步骤

#### 步骤 1: 参数验证

**1.1 检查企业名称参数**
- 检查用户是否提供了 `company_name` 参数
- 如果未提供，向用户询问企业名称

```
请提供企业名称，我将为您生成定制化的CMDB立项报告。
例如：某某银行、某某证券、某某科技
```

**1.2 确定输出路径**
- 如果用户未指定输出路径，使用当前工作目录
- 如果用户未指定文件名，使用默认命名规则：`{企业名称}-CMDB立项报告-{日期}.docx`

#### 步骤 2: 读取模板文件

**2.1 定位知识库模板**

知识库模板位置：`/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx`

使用 Python 读取模板：

```python
from docx import Document
import os

# 模板文件路径
TEMPLATE_PATH = "/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx"

# 备用模板
BACKUP_TEMPLATE_PATH = "/shared/sale-kb/项目资料/模板-自动化运维平台立项报告v1.0.doc"

def load_template(template_path=None):
    """加载模板文件"""
    path = template_path or TEMPLATE_PATH

    if not os.path.exists(path):
        # 尝试备用模板
        if os.path.exists(BACKUP_TEMPLATE_PATH):
            path = BACKUP_TEMPLATE_PATH
        else:
            raise FileNotFoundError(f"模板文件不存在: {path}")

    return Document(path)
```

#### 步骤 3: 替换动态内容

**3.1 替换企业名称**

遍历文档中的所有段落和表格，替换企业名称相关占位符：

```python
from datetime import datetime

def replace_content(doc, company_name):
    """替换文档中的动态内容"""
    current_date = datetime.now().strftime("%Y年%m月")

    # 需要替换的占位符映射
    replacements = {
        "优维科技（深圳）有限公司": company_name,
        "优维科技": company_name,
        "2025年6月": current_date,
        "2025年": datetime.now().strftime("%Y年"),
    }

    # 替换段落中的内容
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                # 保留格式进行替换
                for run in para.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)

    # 替换表格中的内容
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old, new in replacements.items():
                        if old in para.text:
                            for run in para.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)

    return doc
```

**3.2 更新文档标题（如有需要）**

```python
def update_title(doc, company_name):
    """更新文档标题"""
    # 遍历第一个段落（通常是标题）
    if doc.paragraphs:
        first_para = doc.paragraphs[0]
        if "立项" in first_para.text or "建设" in first_para.text:
            # 可以根据需要修改标题
            pass
    return doc
```

#### 步骤 4: 保存文档

**4.1 生成输出文件名**

```python
def generate_output_filename(company_name, output_path="./"):
    """生成输出文件名"""
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{company_name}-CMDB立项报告-{date_str}.docx"
    return os.path.join(output_path, filename)
```

**4.2 保存文档**

```python
def save_document(doc, output_path):
    """保存文档到指定路径"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # 保存文档
    doc.save(output_path)
    return output_path
```

#### 步骤 5: 验证与输出

**5.1 验证文件生成**

```bash
# 检查文件是否存在且大小合理
ls -la "{output_path}"
```

**5.2 输出结果**

向用户报告生成结果：

```markdown
✅ CMDB立项报告生成成功

## 文档信息
- **企业名称**: {company_name}
- **生成日期**: {current_date}
- **文件路径**: {output_path}
- **文件大小**: {file_size} KB

## 文档内容概要
该立项报告包含以下主要章节：
1. 项目建设背景
2. 项目建设目标
3. 项目建设范围
4. 平台建设路线
5. 平台总体架构设计
6. ...

## 后续操作
1. 下载文件进行查看和编辑
2. 根据实际项目情况调整内容
3. 补充客户特定的需求细节

📥 **下载路径**: `{output_path}`
```

### 完整执行代码

```python
from docx import Document
from datetime import datetime
import os

def generate_cmdb_project_report(company_name, output_path="./", output_filename=None, template_file=None):
    """
    生成CMDB立项报告

    Args:
        company_name: 企业名称
        output_path: 输出路径
        output_filename: 自定义文件名
        template_file: 自定义模板路径

    Returns:
        生成的文件路径
    """
    # 默认模板路径
    DEFAULT_TEMPLATE = "/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx"
    BACKUP_TEMPLATE = "/shared/sale-kb/项目资料/模板-自动化运维平台立项报告v1.0.doc"

    # 1. 确定模板文件
    template_path = template_file or DEFAULT_TEMPLATE
    if not os.path.exists(template_path):
        if os.path.exists(BACKUP_TEMPLATE):
            template_path = BACKUP_TEMPLATE
        else:
            raise FileNotFoundError("未找到立项报告模板文件")

    print(f"📖 正在读取模板: {template_path}")

    # 2. 加载模板
    doc = Document(template_path)

    # 3. 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月")
    current_year = datetime.now().strftime("%Y年")

    # 4. 定义替换规则
    replacements = {
        "优维科技（深圳）有限公司": company_name,
        "优维科技": company_name,
        "2025年6月": current_date,
        "2025年": current_year,
        "2024年": current_year,
        "2023年": current_year,
    }

    # 5. 替换段落内容
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                for run in para.runs:
                    if old in run.text:
                        run.text = run.text.replace(old, new)

    # 6. 替换表格内容
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for old, new in replacements.items():
                        if old in para.text:
                            for run in para.runs:
                                if old in run.text:
                                    run.text = run.text.replace(old, new)

    # 7. 生成输出文件名
    if not output_filename:
        date_str = datetime.now().strftime("%Y%m%d")
        output_filename = f"{company_name}-CMDB立项报告-{date_str}.docx"

    full_output_path = os.path.join(output_path, output_filename)

    # 8. 确保输出目录存在
    if output_path and not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    # 9. 保存文档
    doc.save(full_output_path)

    print(f"✅ 报告已生成: {full_output_path}")

    return full_output_path

# 执行生成
if __name__ == "__main__":
    # 获取用户输入的企业名称
    company_name = input("请输入企业名称: ")

    # 生成报告
    output_file = generate_cmdb_project_report(
        company_name=company_name,
        output_path="/workspace/tmp/"
    )

    print(f"\n📥 下载文件: {output_file}")
```

## Output Format

### 成功输出

```markdown
✅ CMDB立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | {company_name} |
| 生成日期 | {current_date} |
| 文件名 | {filename} |
| 文件路径 | {output_path} |
| 文件大小 | {file_size} KB |

## 📋 文档内容结构
1. 项目建设背景
2. 项目建设目标
3. 项目建设范围
4. 平台建设路线
   - 平台建设方法体系
   - 平台设计理念
   - 平台设计技术路线
5. 平台总体架构设计
6. 功能模块设计
7. 项目实施计划
8. 投资估算
9. 预期效益

## 💡 使用建议
1. 下载文件后，根据客户实际情况调整内容
2. 补充客户特定的业务场景和数据
3. 调整项目范围和时间节点
4. 完善投资估算和效益分析

📥 **文件下载路径**: `{output_path}`
```

### 错误输出

**缺少企业名称参数**:
```markdown
⚠️ 缺少必要参数

请提供企业名称以生成定制化的CMDB立项报告。

**使用示例**:
```
请为"某某银行"生成CMDB立项报告
```
```

**模板文件不存在**:
```markdown
❌ 模板文件不存在

未找到立项报告模板文件，请联系管理员检查知识库配置。

预期模板路径: `/shared/sale-kb/项目资料/一体化运维平台建设立项报告v2.0.docx`
```

**文件保存失败**:
```markdown
❌ 文件保存失败

保存路径可能没有写入权限，请尝试指定其他输出路径。

**建议**:
- 使用 `/workspace/tmp/` 目录
- 检查磁盘空间
- 确认目录权限
```

## Integration

### 与其他 Skills 的协作

| Skill | 协作方式 | 说明 |
|-------|---------|------|
| company-research | 前置调研 | 先调研企业信息，再生成报告 |
| project-init | 项目初始化 | 生成报告后可初始化项目目录 |
| sales-prep | 销售准备 | 作为销售准备材料的一部分 |
| document-processor | 文档处理 | 可进一步处理生成的文档 |

### 使用场景

| 场景 | 说明 |
|------|------|
| 项目立项 | 为客户项目准备立项申请材料 |
| 方案汇报 | 作为方案汇报的基础文档 |
| 招投标 | 作为投标文档的基础模板 |
| 内部审批 | 作为内部项目审批的参考材料 |

## Best Practices

### 企业名称输入规范
- ✅ 使用完整企业名称：`某某银行股份有限公司`
- ✅ 可使用简称：`某某银行`
- ❌ 避免使用缩写或不规范名称

### 输出路径建议
- ✅ 使用 `/workspace/tmp/` 目录便于下载
- ✅ 文件名包含日期便于版本管理
- ❌ 避免使用系统目录

### 文档后续处理
1. **内容调整**: 根据客户实际情况调整项目范围
2. **数据填充**: 补充客户的IT资产数据
3. **时间规划**: 调整项目实施时间节点
4. **预算调整**: 根据实际情况调整投资估算

## Notes

1. **模板位置**: 知识库默认模板位于 `/shared/sale-kb/项目资料/` 目录
2. **日期格式**: 自动使用当前日期，格式为 `YYYY年MM月`
3. **格式保持**: 生成的文档保持模板原有的所有格式和样式
4. **可编辑性**: 生成的 .docx 文件可直接用 Word 或 WPS 编辑
5. **多次生成**: 同一企业可多次生成，文件名自动包含日期区分

## Examples

### 示例 1: 基本使用

**用户输入**:
```
请为"招商银行"生成CMDB立项报告
```

**执行结果**:
```markdown
✅ CMDB立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 招商银行 |
| 生成日期 | 2026年3月 |
| 文件名 | 招商银行-CMDB立项报告-20260314.docx |
| 文件路径 | /workspace/tmp/招商银行-CMDB立项报告-20260314.docx |
| 文件大小 | 156 KB |

📥 **文件下载路径**: `/workspace/tmp/招商银行-CMDB立项报告-20260314.docx`
```

### 示例 2: 指定输出路径

**用户输入**:
```
请为"华安证券"生成CMDB立项报告，保存到 /workspace/项目文档/ 目录
```

**执行结果**:
```markdown
✅ CMDB立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 华安证券 |
| 生成日期 | 2026年3月 |
| 文件名 | 华安证券-CMDB立项报告-20260314.docx |
| 文件路径 | /workspace/项目文档/华安证券-CMDB立项报告-20260314.docx |

📥 **文件下载路径**: `/workspace/项目文档/华安证券-CMDB立项报告-20260314.docx`
```

### 示例 3: 完整企业名称

**用户输入**:
```
请为"农夫山泉股份有限公司"生成一份CMDB立项报告
```

**执行结果**:
```markdown
✅ CMDB立项报告生成成功

## 📄 文档信息
| 项目 | 内容 |
|------|------|
| 企业名称 | 农夫山泉股份有限公司 |
| 生成日期 | 2026年3月 |
| 文件名 | 农夫山泉股份有限公司-CMDB立项报告-20260314.docx |
| 文件路径 | /workspace/tmp/农夫山泉股份有限公司-CMDB立项报告-20260314.docx |

📥 **文件下载路径**: `/workspace/tmp/农夫山泉股份有限公司-CMDB立项报告-20260314.docx`
```

---

**版本**: 1.0
**最后更新**: 2026-03-14
**作者**: AI Solutions Expert Team
**依赖**: python-docx
