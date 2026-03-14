---
name: document-processor
description: 综合文档处理工具，支持Excel、Word、图片、Markdown、TXT等多种文件格式的读取、解析、提取和转换。适用于需要处理客户需求文档、会议纪要、报告等各类文档的场景。
category: document-processing
priority: high
---

# Document Processor（文档处理技能）

## Purpose

提供全面的文档处理能力，支持Excel、Word、图片、Markdown、TXT等多种文件格式的智能解析和数据提取。

**核心功能**:
- Excel文件读取与数据提取
- Word文档内容解析
- 图片文字识别（OCR）
- Markdown文档解析
- 文本文件处理
- 文档格式转换
- 表格数据结构化

**核心价值**:
- ✅ **多格式支持**：一次性处理Excel、Word、图片、Markdown、TXT等主流格式
- ✅ **智能提取**：自动识别表格、段落、列表等结构化内容
- ✅ **OCR识别**：支持从图片中提取文字内容
- ✅ **数据结构化**：将非结构化文档转换为结构化数据

## When to Use

在以下情况下使用此技能：
- 处理客户上传的需求文档（Excel需求清单、Word需求说明）
- 解析会议纪要（扫描件、Word、PDF等）
- 提取表格数据并进行分析
- 将图片中的文字内容提取出来
- 批量处理多种格式的文档
- 将文档内容转换为结构化JSON/CSV格式

## Capabilities

### 1. Excel文件处理
- 读取工作表（支持.xlsx、.xls格式）
- 提取表头和数据行
- 识别合并单元格
- 提取多个工作表内容
- 转换为CSV或JSON格式
- 处理公式和计算结果

### 2. Word文档处理
- 提取文本内容（支持.docx、.doc格式）
- 识别段落结构
- 提取表格数据
- 识别标题和列表
- 提取图片和超链接
- 保留格式信息（粗体、斜体、颜色等）

### 3. 图片文字识别（OCR）
- 支持PNG、JPG、JPEG、BMP等格式
- 中英文混合识别
- 表格识别
- 手写文字识别
- 批量图片处理
- 指定识别区域

### 4. PDF文件处理
- 提取文本内容（支持.pdf格式）
- 提取表格数据
- 识别文档结构
- OCR识别扫描版PDF
- 合并和分割PDF
- 提取元数据

### 5. Markdown文档处理
- 解析Markdown语法
- 提取标题层级
- 识别列表、表格、代码块
- 转换为HTML或纯文本
- 提取链接和图片

### 6. 文本文件处理
- 读取TXT、CSV、JSON等格式
- 自动编码检测（UTF-8、GBK等）
- 按行/段落分割
- 提取特定模式的内容（正则表达式）
- 批量文本处理

### 6. 文档格式转换
- Excel → CSV/JSON
- Word → Markdown/TXT
- PDF → TXT/Excel
- 图片 → TXT（OCR）
- Markdown → HTML
- 多种格式统一转换为结构化数据

### 7. 批量文件处理
- 扫描目录并识别文件类型
- 批量处理多个文件
- 支持多种格式混合处理
- 统一输出格式
- 错误处理和日志记录

### 8. 专用解析器
- 需求清单结构识别
- 评分表结构识别
- 会议纪要结构识别
- 自动提取关键字段

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| file_path | string | ✅ | - | 文件路径（支持绝对路径或相对路径） |
| file_type | string | ❌ | auto | 文件类型（excel/word/pdf/image/markdown/txt，auto为自动识别） |
| extract_type | string | ❌ | all | 提取类型（text/table/all） |
| output_format | string | ❌ | json | 输出格式（json/csv/markdown/text） |
| ocr_language | string | ❌ | chi_sim+eng | OCR识别语言（chi_sim=简体中文，eng=英文） |
| encoding | string | ❌ | auto | 文本文件编码（auto/utf-8/gbk等） |
| parser_type | string | ❌ | generic | 解析器类型（generic/requirement/scoring/meeting） |

## Instructions

### 核心处理流程

**步骤1：文件类型识别**
- 根据文件扩展名自动识别类型
- 验证文件是否存在且可读
- 返回文件基本信息（大小、修改时间等）

**步骤2：文件内容解析**
- 根据文件类型调用对应的解析器
- 提取文本、表格、图片等内容
- 识别文档结构（标题、段落、列表等）

**步骤3：数据结构化**
- 将提取的内容转换为结构化格式
- 识别表格的表头和数据行
- 提取关键信息字段

**步骤4：输出结果**
- 根据指定格式输出结果
- 提供内容摘要
- 返回处理状态和错误信息（如有）

---

## 详细使用指南

### Excel文件处理

#### 基础读取

```python
import pandas as pd
import openpyxl

# 方法1：使用pandas读取Excel（推荐）
df = pd.read_excel("需求清单.xlsx", sheet_name="Sheet1")
print(f"行数: {len(df)}, 列数: {len(df.columns)}")
print(df.head())

# 方法2：使用openpyxl读取（更多控制）
wb = openpyxl.load_workbook("需求清单.xlsx")
ws = wb.active
for row in ws.iter_rows(min_row=1, max_row=10, values_only=True):
    print(row)
```

#### 读取多个工作表

```python
# 读取所有工作表
excel_file = pd.ExcelFile("需求清单.xlsx")
print(f"工作表列表: {excel_file.sheet_names}")

# 读取所有工作表内容
all_sheets = {}
for sheet_name in excel_file.sheet_names:
    all_sheets[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"工作表 '{sheet_name}' 有 {len(all_sheets[sheet_name])} 行数据")
```

#### 提取特定行列

```python
# 读取指定行范围
df = pd.read_excel("需求清单.xlsx", skiprows=2, nrows=20)  # 跳过前2行，读取20行

# 读取指定列
df = pd.read_excel("需求清单.xlsx", usecols=["需求编号", "需求描述", "优先级"])

# 按条件筛选
high_priority = df[df["优先级"] == "高"]
print(f"高优先级需求: {len(high_priority)} 条")
```

#### 处理表头和数据

```python
# 识别表头
df = pd.read_excel("需求清单.xlsx", header=0)  # 第一行作为表头
headers = df.columns.tolist()
print(f"表头: {headers}")

# 转换为字典列表
data_list = df.to_dict('records')
for i, record in enumerate(data_list[:5]):
    print(f"第 {i+1} 条: {record}")

# 转换为JSON
json_data = df.to_json(orient='records', force_ascii=False)
with open("需求清单.json", "w", encoding="utf-8") as f:
    f.write(json_data)
```

#### 处理合并单元格

```python
import openpyxl

wb = openpyxl.load_workbook("需求清单.xlsx")
ws = wb.active

# 获取合并单元格信息
merged_cells = ws.merged_cells.ranges
print(f"合并单元格区域: {list(merged_cells)}")

# 展开合并单元格
for merged_cell in merged_cells:
    min_col, min_row, max_col, max_row = merged_cell.bounds
    # 获取合并单元格的值
    value = ws.cell(min_row, min_col).value
    # 填充到所有单元格
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            ws.cell(row, col).value = value
```

---

### Word文档处理

#### 基础读取

```python
from docx import Document

# 读取Word文档
doc = Document("需求说明.docx")

# 提取所有段落文本
full_text = []
for para in doc.paragraphs:
    if para.text.strip():  # 跳过空段落
        full_text.append(para.text)

print(f"总段落数: {len(full_text)}")
print("\n".join(full_text[:10]))  # 打印前10段
```

#### 识别文档结构

```python
# 识别标题和正文
for para in doc.paragraphs:
    if para.style.name.startswith('Heading'):
        level = para.style.name.replace('Heading ', '')
        print(f"[标题{level}] {para.text}")
    else:
        print(f"[正文] {para.text[:50]}...")  # 只打印前50字
```

#### 提取表格数据

```python
# 提取所有表格
tables_data = []
for i, table in enumerate(doc.tables):
    print(f"\n=== 表格 {i+1} ===")
    table_content = []
    for row in table.rows:
        row_data = [cell.text for cell in row.cells]
        table_content.append(row_data)

    # 转换为DataFrame
    if table_content:
        df = pd.DataFrame(table_content[1:], columns=table_content[0])
        tables_data.append(df)
        print(df)

# 保存所有表格
for i, df in enumerate(tables_data):
    df.to_excel(f"表格_{i+1}.xlsx", index=False)
```

#### 提取格式信息

```python
# 提取粗体、斜体等格式
for para in doc.paragraphs:
    for run in para.runs:
        if run.bold:
            print(f"[粗体] {run.text}")
        if run.italic:
            print(f"[斜体] {run.text}")
        if run.font.color.rgb:
            print(f"[彩色] {run.text}")
```

#### 提取图片

```python
from docx.opc.constants import RELATIONSHIP_TYPE as RT

# 提取文档中的所有图片
for rel in doc.part.rels.values():
    if "image" in rel.target_ref:
        image_data = rel.target_part.blob
        image_name = rel.target_ref.split('/')[-1]
        with open(f"extracted_{image_name}", "wb") as f:
            f.write(image_data)
        print(f"提取图片: {image_name}")
```

---

### 图片文字识别（OCR）

#### 基础OCR识别

```python
import pytesseract
from PIL import Image

# 读取图片并识别
image = Image.open("需求截图.png")
text = pytesseract.image_to_string(image, lang='chi_sim+eng')
print("识别结果:")
print(text)

# 保存识别结果
with open("识别结果.txt", "w", encoding="utf-8") as f:
    f.write(text)
```

#### 表格识别

```python
# 表格识别（使用table-transformer或paddleocr）
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)
result = ocr.ocr("表格图片.png", cls=True)

# 提取文字和位置
for line in result[0]:
    box = line[0]  # 坐标
    text = line[1][0]  # 文字
    confidence = line[1][1]  # 置信度
    print(f"[{confidence:.2f}] {text}")
```

#### 指定区域识别

```python
from PIL import Image

# 裁剪指定区域
image = Image.open("全图.png")
cropped = image.crop((100, 100, 500, 300))  # (left, top, right, bottom)

# 识别裁剪区域
text = pytesseract.image_to_string(cropped, lang='chi_sim')
print(f"识别结果: {text}")
```

#### 批量图片处理

```python
import os

image_files = [f for f in os.listdir(".") if f.endswith(('.png', '.jpg', '.jpeg'))]

results = {}
for image_file in image_files:
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        results[image_file] = text
        print(f"✅ {image_file}: 识别完成")
    except Exception as e:
        print(f"❌ {image_file}: {str(e)}")

# 保存所有结果
with open("批量识别结果.txt", "w", encoding="utf-8") as f:
    for filename, text in results.items():
        f.write(f"=== {filename} ===\n")
        f.write(text)
        f.write("\n\n")
```

---

### Markdown文档处理

#### 基础解析

```python
import markdown
from bs4 import BeautifulSoup

# 读取Markdown文件
with open("README.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# 转换为HTML
html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'html.parser')
```

#### 提取标题层级

```python
import re

# 提取所有标题
headers = re.findall(r'^(#{1,6})\s+(.+)$', md_content, re.MULTILINE)
for level, title in headers:
    indent = "  " * (len(level) - 1)
    print(f"{indent}- {title}")
```

#### 提取表格

```python
# 提取Markdown表格
tables = re.findall(r'(\|.+\|[\r\n]+\|[-:\s|]+\|[\r\n]+(?:\|.+\|[\r\n]+)*)', md_content)

for i, table_text in enumerate(tables):
    print(f"\n=== 表格 {i+1} ===")
    lines = table_text.strip().split('\n')
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]

    # 解析数据行
    data_rows = []
    for line in lines[2:]:  # 跳过表头和分隔行
        row = [cell.strip() for cell in line.split('|')[1:-1]]
        data_rows.append(row)

    df = pd.DataFrame(data_rows, columns=headers)
    print(df)
```

#### 提取代码块

```python
# 提取代码块
code_blocks = re.findall(r'```(\w+)?\n(.*?)```', md_content, re.DOTALL)
for language, code in code_blocks:
    print(f"\n=== {language or '未指定语言'} ===")
    print(code.strip())
```

---

### PDF文档处理

#### 基础文本提取

```python
from pypdf import PdfReader
import pdfplumber

# 方法1：使用pypdf提取文本（快速）
reader = PdfReader("商务评分表.pdf")
print(f"总页数: {len(reader.pages)}")

full_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    full_text += f"\n=== 第 {i+1} 页 ===\n{text}\n"

print(full_text)

# 方法2：使用pdfplumber提取文本（更准确）
with pdfplumber.open("商务评分表.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"\n=== 第 {i+1} 页 ===\n{text}")
```

#### 提取PDF中的表格

```python
import pdfplumber
import pandas as pd

# 使用pdfplumber提取表格（推荐）
with pdfplumber.open("商务评分表.pdf") as pdf:
    all_tables = []
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            if table:
                print(f"\n=== 第 {i+1} 页 表格 {j+1} ===")
                # 转换为DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                print(df)
                all_tables.append(df)

# 保存所有表格
for i, df in enumerate(all_tables):
    df.to_excel(f"表格_{i+1}.xlsx", index=False)
```

#### PDF元数据提取

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata

print(f"标题: {meta.title}")
print(f"作者: {meta.author}")
print(f"主题: {meta.subject}")
print(f"创建者: {meta.creator}")
print(f"创建时间: {meta.creation_date}")
print(f"修改时间: {meta.modification_date}")
```

#### OCR识别扫描版PDF

```python
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# 将PDF转换为图片
images = convert_from_path('扫描版PDF.pdf', dpi=300)

# OCR识别每一页
full_text = ""
for i, image in enumerate(images):
    print(f"正在识别第 {i+1} 页...")
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')
    full_text += f"\n=== 第 {i+1} 页 ===\n{text}\n"

# 保存识别结果
with open("OCR识别结果.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
```

#### PDF页面操作

```python
from pypdf import PdfReader, PdfWriter

# 合并PDF
def merge_pdfs(pdf_files, output_file):
    writer = PdfWriter()
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)

# 使用示例
merge_pdfs(["文件1.pdf", "文件2.pdf", "文件3.pdf"], "合并后.pdf")

# 分割PDF
def split_pdf(input_file, output_prefix):
    reader = PdfReader(input_file)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        with open(f"{output_prefix}_page_{i+1}.pdf", "wb") as f:
            writer.write(f)

# 使用示例
split_pdf("大文件.pdf", "分割")

# 提取特定页面
def extract_pages(input_file, pages, output_file):
    """提取指定页码的页面
    pages: 页码列表，如 [0, 2, 4] 表示第1、3、5页
    """
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page_num in pages:
        writer.add_page(reader.pages[page_num])
    with open(output_file, "wb") as f:
        writer.write(f)

# 使用示例
extract_pages("文档.pdf", [0, 1, 2], "前三页.pdf")
```

#### PDF与Excel互转

```python
# PDF表格转Excel
import pdfplumber
import pandas as pd

with pdfplumber.open("评分表.pdf") as pdf:
    # 创建Excel写入器
    with pd.ExcelWriter("评分表.xlsx", engine='openpyxl') as writer:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for j, table in enumerate(tables):
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    sheet_name = f"Page{i+1}_Table{j+1}"
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

print("✅ PDF表格已转换为Excel")
```

---

### 文本文件处理
for language, code in code_blocks:
    print(f"\n=== {language or '未指定语言'} ===")
    print(code.strip())
```

---

### 文本文件处理

#### 智能编码检测

```python
import chardet

# 检测文件编码
with open("文档.txt", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']
    print(f"检测到编码: {encoding} (置信度: {confidence:.2%})")

# 使用检测到的编码读取
with open("文档.txt", "r", encoding=encoding) as f:
    content = f.read()
    print(content)
```

#### 按行处理

```python
# 逐行读取和处理
with open("需求列表.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if line:  # 跳过空行
            print(f"第 {i} 行: {line}")
```

#### 正则表达式提取

```python
import re

# 提取特定模式的内容
with open("文档.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 提取所有邮箱地址
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
print(f"找到 {len(emails)} 个邮箱: {emails}")

# 提取所有手机号
phones = re.findall(r'1[3-9]\d{9}', content)
print(f"找到 {len(phones)} 个手机号: {phones}")

# 提取需求编号（如 REQ-001）
req_ids = re.findall(r'REQ-\d{3,}', content)
print(f"找到 {len(req_ids)} 个需求编号: {req_ids}")
```

#### CSV文件处理

```python
import csv

# 读取CSV文件
with open("需求.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# 使用pandas读取（更强大）
df = pd.read_csv("需求.csv", encoding="utf-8")
print(df.head())
```

---

## 文档格式转换

### Excel → JSON

```python
# 将Excel转换为JSON
df = pd.read_excel("需求清单.xlsx")
json_data = df.to_json(orient='records', force_ascii=False, indent=2)

with open("需求清单.json", "w", encoding="utf-8") as f:
    f.write(json_data)
```

### Word → Markdown

```python
from docx import Document

doc = Document("需求说明.docx")
md_lines = []

for para in doc.paragraphs:
    if para.style.name.startswith('Heading'):
        level = int(para.style.name.replace('Heading ', ''))
        md_lines.append(f"{'#' * level} {para.text}")
    else:
        md_lines.append(para.text)
    md_lines.append("")  # 空行

# 保存为Markdown
with open("需求说明.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
```

### 图片 → 文本（OCR）

```python
from PIL import Image
import pytesseract

# 批量转换图片为文本
image_files = ["截图1.png", "截图2.jpg", "截图3.jpeg"]

for image_file in image_files:
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')

    # 保存为txt
    output_file = image_file.rsplit('.', 1)[0] + '.txt'
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ {image_file} → {output_file}")
```

---

## 综合示例：处理客户需求文档

```python
import os
import pandas as pd
from docx import Document
from PIL import Image
import pytesseract

def process_document(file_path):
    """
    智能处理文档，根据文件类型自动选择处理方式
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    result = {
        "file_name": os.path.basename(file_path),
        "file_type": ext,
        "content": None,
        "tables": [],
        "requirements": []
    }

    try:
        if ext in ['.xlsx', '.xls']:
            # Excel文件
            df = pd.read_excel(file_path)
            result["content"] = df.to_dict('records')
            result["tables"].append(df)

            # 提取需求列表
            if "需求描述" in df.columns or "需求" in df.columns:
                req_col = "需求描述" if "需求描述" in df.columns else "需求"
                result["requirements"] = df[req_col].tolist()

        elif ext in ['.docx', '.doc']:
            # Word文件
            doc = Document(file_path)

            # 提取文本
            text_content = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            result["content"] = "\n".join(text_content)

            # 提取表格
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    table_data.append([cell.text for cell in row.cells])
                if table_data:
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])
                    result["tables"].append(df)

        elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
            # 图片文件（OCR）
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            result["content"] = text

        elif ext in ['.txt', '.md']:
            # 文本文件
            with open(file_path, 'r', encoding='utf-8') as f:
                result["content"] = f.read()

        result["status"] = "success"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result

# 使用示例
file_path = "客户需求清单.xlsx"
result = process_document(file_path)

print(f"文件名: {result['file_name']}")
print(f"文件类型: {result['file_type']}")
print(f"处理状态: {result['status']}")
print(f"提取到 {len(result['tables'])} 个表格")
print(f"提取到 {len(result['requirements'])} 条需求")
```

---

## 常见问题处理

### 1. 文件编码问题

```python
# 尝试多种编码
encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
content = None

for encoding in encodings:
    try:
        with open("文档.txt", "r", encoding=encoding) as f:
            content = f.read()
        print(f"✅ 成功使用编码: {encoding}")
        break
    except UnicodeDecodeError:
        continue

if content is None:
    print("❌ 无法识别文件编码")
```

### 2. Excel工作表为空

```python
df = pd.read_excel("文件.xlsx", sheet_name="Sheet1")
if df.empty:
    print("⚠️ 工作表为空或无数据")
else:
    print(f"✅ 读取到 {len(df)} 行数据")
```

### 3. OCR识别率低

```python
from PIL import Image, ImageEnhance

# 图像预处理提高识别率
image = Image.open("模糊图片.png")

# 转换为灰度图
image = image.convert('L')

# 增强对比度
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2.0)

# 识别
text = pytesseract.image_to_string(image, lang='chi_sim')
```

---

## 批量文件处理

### 扫描目录并批量处理

```python
import os
import glob

def scan_and_process_documents(directory, file_patterns=['*.xlsx', '*.docx', '*.pdf', '*.md']):
    """
    扫描目录并批量处理文档

    Args:
        directory: 要扫描的目录路径
        file_patterns: 文件模式列表

    Returns:
        处理结果字典
    """
    results = {
        'success': [],
        'failed': [],
        'total': 0
    }

    # 扫描所有匹配的文件
    all_files = []
    for pattern in file_patterns:
        files = glob.glob(os.path.join(directory, '**', pattern), recursive=True)
        all_files.extend(files)

    results['total'] = len(all_files)
    print(f"找到 {len(all_files)} 个文件")

    # 批量处理
    for file_path in all_files:
        try:
            print(f"\n处理: {file_path}")
            result = process_document(file_path)
            results['success'].append({
                'file': file_path,
                'result': result
            })
            print(f"✅ 成功")
        except Exception as e:
            results['failed'].append({
                'file': file_path,
                'error': str(e)
            })
            print(f"❌ 失败: {str(e)}")

    # 输出统计
    print(f"\n=== 处理完成 ===")
    print(f"总文件数: {results['total']}")
    print(f"成功: {len(results['success'])}")
    print(f"失败: {len(results['failed'])}")

    return results

# 使用示例
results = scan_and_process_documents("./项目文档", ['*.xlsx', '*.docx', '*.pdf'])
```

### 批量格式转换

```python
def batch_convert_to_json(directory, output_dir="output"):
    """批量将文档转换为JSON格式"""
    os.makedirs(output_dir, exist_ok=True)

    # 支持的文件类型
    file_types = {
        '.xlsx': process_excel_to_json,
        '.xls': process_excel_to_json,
        '.docx': process_word_to_json,
        '.pdf': process_pdf_to_json,
        '.md': process_markdown_to_json
    }

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in file_types:
                input_path = os.path.join(root, file)
                output_file = os.path.splitext(file)[0] + '.json'
                output_path = os.path.join(output_dir, output_file)

                try:
                    print(f"转换: {file}")
                    data = file_types[ext](input_path)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print(f"✅ 已保存: {output_path}")
                except Exception as e:
                    print(f"❌ 失败: {str(e)}")

# 使用示例
batch_convert_to_json("./需求文档", "./json_output")
```

---

## 专用解析器

### 需求清单解析器

```python
def parse_requirement_list(file_path):
    """
    专用于解析需求清单文档
    自动识别需求编号、需求描述、优先级等字段

    Returns:
        {
            'requirements': [
                {
                    'id': 'REQ-001',
                    'description': '需求描述',
                    'priority': '高',
                    'module': 'CMDB',
                    'status': '待开发'
                },
                ...
            ],
            'summary': {
                'total': 25,
                'high_priority': 15,
                'medium_priority': 8,
                'low_priority': 2
            }
        }
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    requirements = []

    if ext in ['.xlsx', '.xls']:
        # Excel格式需求清单
        df = pd.read_excel(file_path)

        # 智能识别列名（支持多种变体）
        column_mapping = {
            'id': ['需求编号', '编号', 'ID', 'No', '序号'],
            'description': ['需求描述', '需求内容', '需求', '描述', 'Description'],
            'priority': ['优先级', 'Priority', '重要性'],
            'module': ['模块', 'Module', '所属模块', '功能模块'],
            'status': ['状态', 'Status', '进度']
        }

        # 映射实际列名
        actual_columns = {}
        for key, variants in column_mapping.items():
            for variant in variants:
                if variant in df.columns:
                    actual_columns[key] = variant
                    break

        # 提取需求
        for _, row in df.iterrows():
            req = {}
            for key, col_name in actual_columns.items():
                req[key] = str(row[col_name]) if pd.notna(row[col_name]) else ''
            requirements.append(req)

    elif ext in ['.docx', '.doc']:
        # Word格式需求清单
        doc = Document(file_path)

        # 提取表格中的需求
        for table in doc.tables:
            headers = [cell.text.strip() for cell in table.rows[0].cells]
            for row in table.rows[1:]:
                req = {}
                for i, cell in enumerate(row.cells):
                    if i < len(headers):
                        req[headers[i]] = cell.text.strip()
                requirements.append(req)

    # 统计信息
    summary = {
        'total': len(requirements),
        'high_priority': sum(1 for r in requirements if r.get('priority', '').startswith('高')),
        'medium_priority': sum(1 for r in requirements if r.get('priority', '').startswith('中')),
        'low_priority': sum(1 for r in requirements if r.get('priority', '').startswith('低'))
    }

    return {
        'requirements': requirements,
        'summary': summary
    }

# 使用示例
result = parse_requirement_list("客户需求清单.xlsx")
print(f"总需求数: {result['summary']['total']}")
print(f"高优先级: {result['summary']['high_priority']}")
for req in result['requirements'][:5]:
    print(f"- {req.get('id')}: {req.get('description')}")
```

### 评分表解析器

```python
def parse_scoring_table(file_path):
    """
    专用于解析商务评分表
    自动识别评分项、分值、评分标准、门槛条件等

    Returns:
        {
            'threshold_conditions': [  # 门槛条件
                {
                    'condition': '必须具备软件企业认定证书',
                    'type': '废标项',
                    'severity': 'critical'
                },
                ...
            ],
            'scoring_items': [  # 评分项
                {
                    'category': '企业资质',
                    'item': 'ISO9001认证',
                    'score': 3,
                    'criteria': '提供得3分，不提供得0分'
                },
                ...
            ],
            'summary': {
                'total_score': 40,
                'threshold_count': 5,
                'scoring_items_count': 15
            }
        }
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    threshold_conditions = []
    scoring_items = []
    total_score = 0

    if ext in ['.xlsx', '.xls']:
        # Excel格式评分表
        df = pd.read_excel(file_path)

        # 识别门槛条件（包含关键词）
        threshold_keywords = ['必须', '应当', '不得低于', '废标', '不合格', '资格否决']

        for _, row in df.iterrows():
            row_text = ' '.join([str(v) for v in row.values if pd.notna(v)])

            # 检查是否为门槛条件
            is_threshold = any(keyword in row_text for keyword in threshold_keywords)
            if is_threshold:
                threshold_conditions.append({
                    'condition': row_text,
                    'type': '废标项' if '废标' in row_text else '必备资格',
                    'severity': 'critical'
                })
                continue

            # 提取评分项
            # 假设列结构：评分项 | 分值 | 评分标准
            if len(row) >= 3:
                try:
                    score = float(row.iloc[1]) if pd.notna(row.iloc[1]) else 0
                    if score > 0:
                        scoring_items.append({
                            'category': str(row.iloc[0]) if pd.notna(row.iloc[0]) else '',
                            'item': str(row.iloc[0]) if pd.notna(row.iloc[0]) else '',
                            'score': score,
                            'criteria': str(row.iloc[2]) if pd.notna(row.iloc[2]) else ''
                        })
                        total_score += score
                except:
                    pass

    elif ext == '.pdf':
        # PDF格式评分表
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if not table:
                        continue

                    # 跳过表头
                    for row in table[1:]:
                        if not row or len(row) < 2:
                            continue

                        row_text = ' '.join([str(cell) for cell in row if cell])

                        # 识别门槛条件
                        threshold_keywords = ['必须', '应当', '不得低于', '废标', '不合格']
                        is_threshold = any(keyword in row_text for keyword in threshold_keywords)

                        if is_threshold:
                            threshold_conditions.append({
                                'condition': row_text,
                                'type': '废标项' if '废标' in row_text else '必备资格',
                                'severity': 'critical'
                            })
                        else:
                            # 尝试提取分值
                            try:
                                score = float(row[1]) if len(row) > 1 and row[1] else 0
                                if score > 0:
                                    scoring_items.append({
                                        'category': row[0] if row[0] else '',
                                        'item': row[0] if row[0] else '',
                                        'score': score,
                                        'criteria': row[2] if len(row) > 2 and row[2] else ''
                                    })
                                    total_score += score
                            except:
                                pass

    return {
        'threshold_conditions': threshold_conditions,
        'scoring_items': scoring_items,
        'summary': {
            'total_score': total_score,
            'threshold_count': len(threshold_conditions),
            'scoring_items_count': len(scoring_items)
        }
    }

# 使用示例
result = parse_scoring_table("商务评分表.xlsx")
print(f"总分: {result['summary']['total_score']}")
print(f"门槛条件: {result['summary']['threshold_count']} 个")
print(f"评分项: {result['summary']['scoring_items_count']} 个")

print("\n门槛条件:")
for condition in result['threshold_conditions']:
    print(f"- [{condition['type']}] {condition['condition']}")

print("\n评分项:")
for item in result['scoring_items'][:5]:
    print(f"- {item['item']}: {item['score']}分")
```

### 会议纪要解析器

```python
def parse_meeting_minutes(file_path):
    """
    专用于解析会议纪要
    自动提取会议时间、参会人员、讨论内容、行动项等

    Returns:
        {
            'meeting_info': {
                'date': '2026-01-22',
                'time': '14:00-16:00',
                'location': '会议室A',
                'attendees': ['张三', '李四', '王五']
            },
            'topics': [
                {
                    'title': '需求讨论',
                    'content': '...',
                    'decisions': ['决定1', '决定2']
                },
                ...
            ],
            'action_items': [
                {
                    'task': '准备技术方案',
                    'owner': '张三',
                    'deadline': '2026-01-25'
                },
                ...
            ]
        }
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    meeting_info = {}
    topics = []
    action_items = []

    if ext in ['.docx', '.doc']:
        doc = Document(file_path)
        full_text = '\n'.join([para.text for para in doc.paragraphs])

        # 提取会议时间
        import re
        date_pattern = r'(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)'
        dates = re.findall(date_pattern, full_text)
        if dates:
            meeting_info['date'] = dates[0]

        # 提取参会人员
        attendee_keywords = ['参会人员', '参加人员', '出席人员', '与会人员']
        for para in doc.paragraphs:
            if any(keyword in para.text for keyword in attendee_keywords):
                # 提取人名（简单实现）
                names = re.findall(r'[\u4e00-\u9fa5]{2,4}', para.text)
                meeting_info['attendees'] = names
                break

        # 提取行动项（包含"负责人"、"截止时间"等关键词）
        action_keywords = ['行动项', 'TODO', '待办', '任务']
        for para in doc.paragraphs:
            if any(keyword in para.text for keyword in action_keywords):
                action_items.append({
                    'task': para.text,
                    'owner': '',
                    'deadline': ''
                })

    elif ext == '.pdf':
        # PDF格式会议纪要
        with pdfplumber.open(file_path) as pdf:
            full_text = ''
            for page in pdf.pages:
                full_text += page.extract_text() + '\n'

            # 类似的提取逻辑
            import re
            date_pattern = r'(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)'
            dates = re.findall(date_pattern, full_text)
            if dates:
                meeting_info['date'] = dates[0]

    return {
        'meeting_info': meeting_info,
        'topics': topics,
        'action_items': action_items
    }

# 使用示例
result = parse_meeting_minutes("会议纪要-20260122.docx")
print(f"会议日期: {result['meeting_info'].get('date')}")
print(f"参会人员: {', '.join(result['meeting_info'].get('attendees', []))}")
print(f"行动项: {len(result['action_items'])} 个")
```

---

## Quick Reference

| 文件类型 | 推荐工具 | 主要用途 |
|---------|---------|---------|
| Excel (.xlsx/.xls) | pandas, openpyxl | 表格数据提取、数据分析 |
| Word (.docx) | python-docx | 文档内容提取、表格提取 |
| PDF (.pdf) | pdfplumber, pypdf | PDF文本提取、表格提取 |
| 图片 (.png/.jpg) | pytesseract, paddleocr | OCR文字识别 |
| Markdown (.md) | markdown, regex | 结构化内容提取 |
| 文本 (.txt) | chardet, regex | 文本解析、模式匹配 |
| CSV | pandas | 结构化数据处理 |

## 专用解析器使用场景

| 解析器类型 | 适用场景 | 主要功能 |
|-----------|---------|---------|
| 需求清单解析器 | requirement-analysis agent | 自动识别需求编号、描述、优先级 |
| 评分表解析器 | bid-strategist agent | 识别门槛条件、评分项、分值 |
| 会议纪要解析器 | 会议记录处理 | 提取会议时间、参会人员、行动项 |
| 通用解析器 | 其他场景 | 标准的表格和文本提取 |

## Version

**版本**: 1.5
**最后更新**: 2026-02-02
**更新内容**:
- **v1.5 (2026-02-02) - 去除安装说明**:
  - ✅ 移除 Installation 章节，默认认为依赖已具备
  - ✅ 移除 Dependencies 章节
  - ✅ 简化文档结构，聚焦功能使用
- **v1.4 (2026-02-02) - 简化安装**:
  - 移除离线部署功能，简化安装流程
  - 移除 `load_dependencies.py` 依赖加载器
  - 移除打包脚本，统一使用标准 pip 安装方式
- **v1.3 (2026-02-01) - 离线部署支持** (已移除)
- **v1.2 (2026-02-01) - 依赖管理优化** (已移除)
- **v1.1 (2026-01-22)**:
  - 新增 PDF 文件处理能力
  - 新增批量文件处理功能
  - 新增专用解析器（需求清单、评分表、会议纪要）
**作者**: AI Solutions Expert Team
