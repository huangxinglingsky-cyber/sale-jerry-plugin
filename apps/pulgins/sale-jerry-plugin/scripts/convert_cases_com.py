#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例库转换脚本 - 使用Win32 COM接口
通过Excel COM对象读取Excel文件，生成 Markdown 格式的案例库
"""

import sys
import win32com.client as win32
from datetime import datetime
import os

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 文件路径
excel_path = r"d:\workspace\pulgins\sale-1.0.0\skills\company-research\resource\data\案例信息.xlsx"
output_path = r"d:\workspace\pulgins\sale-1.0.0\skills\company-research\resource\data\caseLibrary.md"

def convert_to_markdown():
    """从Excel转换为Markdown格式的案例库"""

    print(f"正在读取Excel文件: {excel_path}")

    # 创建Excel应用对象
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    try:
        # 打开工作簿
        workbook = excel.Workbooks.Open(os.path.abspath(excel_path))
        worksheet = workbook.Worksheets(1)

        # 获取使用区域
        used_range = worksheet.UsedRange
        rows = used_range.Rows.Count
        cols = used_range.Columns.Count

        print(f"找到 {rows} 行数据（含表头），{cols} 列")

        # 读取表头
        headers = []
        for col in range(1, cols + 1):
            header = str(worksheet.Cells(1, col).Value or "").strip()
            headers.append(header)

        print(f"列名: {headers}")

        # 生成Markdown内容
        markdown_content = []
        markdown_content.append("# 客户案例库\n")
        markdown_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        markdown_content.append(f"**案例总数**: {rows - 1}个\n")
        markdown_content.append("**数据来源**: 案例信息.xlsx\n")
        markdown_content.append("\n---\n")
        markdown_content.append("\n## 📊 案例列表\n")
        markdown_content.append("\n| 客户名称 | 行业细分 | 模块 | 合同名称 | 合同金额(万) | 合同时间 | 是否直签 | 代理商 |")
        markdown_content.append("\n|---------|---------|------|---------|------------|---------|---------|--------|")

        # 读取数据行
        case_count = 0
        for row in range(2, rows + 1):
            try:
                customer = str(worksheet.Cells(row, 1).Value or "").strip()

                # 跳过空行
                if not customer:
                    continue

                industry = str(worksheet.Cells(row, 2).Value or "").strip()
                module = str(worksheet.Cells(row, 3).Value or "").strip()
                contract = str(worksheet.Cells(row, 4).Value or "").strip()

                # 处理金额
                amount_val = worksheet.Cells(row, 5).Value
                if amount_val is None or amount_val == "":
                    amount = "-"
                else:
                    amount = str(amount_val).strip()

                # 处理时间
                time_val = worksheet.Cells(row, 6).Value
                if time_val is None or time_val == "":
                    contract_time = "-"
                else:
                    contract_time = str(time_val).strip()

                # 是否直签
                is_direct_val = str(worksheet.Cells(row, 7).Value or "").strip()
                if is_direct_val.lower() in ['是', 'yes', 'y', '1', 'true', '1.0']:
                    is_direct = "是"
                elif is_direct_val.lower() in ['否', 'no', 'n', '0', 'false', '0.0']:
                    is_direct = "否"
                else:
                    is_direct = "是"  # 默认为直签

                # 代理商
                agent_val = str(worksheet.Cells(row, 8).Value or "").strip()
                if not agent_val or agent_val == "None":
                    if is_direct == "否":
                        agent = "待补充"
                    else:
                        agent = "-"
                else:
                    agent = agent_val

                markdown_content.append(f"\n| {customer} | {industry} | {module} | {contract} | {amount} | {contract_time} | {is_direct} | {agent} |")
                case_count += 1

            except Exception as e:
                print(f"处理第 {row} 行时出错: {e}")
                continue

        # 添加说明部分
        markdown_content.append("\n\n---\n")
        markdown_content.append("\n## 📋 字段说明\n")
        markdown_content.append("\n| 字段 | 说明 |")
        markdown_content.append("\n|------|------|")
        markdown_content.append("\n| 客户名称 | 签约客户的公司全称或简称 |")
        markdown_content.append("\n| 行业细分 | 格式：大类-细分（如：金融-银行、政府-事业单位） |")
        markdown_content.append("\n| 模块 | 项目涉及的产品模块（CMDB、自动化运维、监控等） |")
        markdown_content.append("\n| 合同名称 | 合同/项目的官方名称 |")
        markdown_content.append("\n| 合同金额(万) | 合同金额，单位：万元 |")
        markdown_content.append("\n| 合同时间 | 合同签订时间，格式：YYYY-MM |")
        markdown_content.append("\n| 是否直签 | 是=优维直接签约；否=通过代理商签约 |")
        markdown_content.append("\n| 代理商 | 如非直签，填写代理商名称；直签则为 - |")

        markdown_content.append("\n\n---\n")
        markdown_content.append("\n## 🔍 使用说明\n")
        markdown_content.append("\n### 案例筛选规则\n")
        markdown_content.append("\n1. **行业匹配**: 精确匹配行业细分字段（如：金融-银行）")
        markdown_content.append("\n2. **模块匹配**: 模糊匹配模块字段（如：搜索CMDB会匹配\"CMDB\"、\"CMDB+自动化\"等）")
        markdown_content.append("\n3. **时间筛选**: 根据合同时间筛选（一年内/三年内）")
        markdown_content.append("\n4. **排序规则**: 按合同时间降序排列（最新的在前）")

        markdown_content.append("\n\n### 数据维护\n")
        markdown_content.append("\n- **更新频率**: 建议每月更新一次")
        markdown_content.append("\n- **数据来源**: 案例信息.xlsx")
        markdown_content.append("\n- **更新方式**: 运行 scripts/convert_cases_com.py 脚本自动生成")
        markdown_content.append("\n- **注意事项**: 直接编辑此文件的修改会在下次运行脚本时被覆盖")

        markdown_content.append("\n\n---\n")
        markdown_content.append(f"\n**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        markdown_content.append("\n**维护者**: AI Solutions Expert Team\n")

        # 写入文件
        final_content = ''.join(markdown_content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"\n✅ 成功生成案例库文件: {output_path}")
        print(f"📊 共处理 {case_count} 条案例")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭工作簿和Excel
        try:
            workbook.Close(False)
            excel.Quit()
        except:
            pass

if __name__ == "__main__":
    try:
        convert_to_markdown()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
