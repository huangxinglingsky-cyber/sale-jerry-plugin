#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例库转换脚本 - 使用Win32 COM接口
从 case.xlsx 读取案例信息，生成 Markdown 格式的案例库
"""

import sys
import win32com.client as win32
from datetime import datetime
import os
import re

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 文件路径
excel_path = r"d:\workspace\pulgins\sale-1.0.0\skills\company-research\resource\data\case.xlsx"
output_path = r"d:\workspace\pulgins\sale-1.0.0\skills\company-research\resource\data\caseLibrary.md"

# 模块关键词列表（用于从商机中提取）
MODULE_KEYWORDS = [
    'CMDB',
    'ITSM',
    'IT服务中心',
    '自动化运维',
    '自动化',
    'DevOps',
    '监控',
    'IT数据人行上报',
    '人行上报',
    '金融业科技信息综合管理平台',
    'CD',
    '持续交付',
    'CI/CD',
    '低代码',
    '统一IT门户',
    'IT门户',
    '配置管理',
    '运维管理平台',
    '一体化运维',
    '智能运维',
]

# 行业分类关键词（按优先级排序）
INDUSTRY_KEYWORDS = {
    '金融-银行': [
        '银行', '农商行', '农村商业银行', '城商行', '城市商业银行',
        '农信社', '农村信用社', '信用联社', '村镇银行'
    ],
    '金融-证券': [
        '证券', '券商', '期货', '交易所', '中信证券', '国信证券',
        '华泰证券', '广发证券', '招商证券', '中金公司'
    ],
    '金融-基金': [
        '基金', '资产管理', '资管', '理财'
    ],
    '金融-保险': [
        '保险', '人寿', '财险', '太平', '平安'
    ],
    '金融-租赁': [
        '租赁', '融资租赁', '金融租赁'
    ],
    '金融-信托': [
        '信托', '信达'
    ],
    '金融-其他': [
        '消费金融', '小额贷款', '担保', '典当'
    ],
    '制造-汽车': [
        '汽车', '车辆', '上汽', '一汽', '东风', '比亚迪', '吉利',
        '长城', '奇瑞', '长安', '广汽', '北汽', '江淮', '沃尔沃',
        '福特', '通用', '丰田', '本田', '日产', '大众', '奔驰',
        '宝马', '奥迪', '特斯拉', '蔚来', '小鹏', '理想', '问界',
        '智己', '岚图', '飞凡', '埃安', '赛力斯', '延锋', '座椅'
    ],
    '制造-电子': [
        '电子', '半导体', '芯片', '集成电路', 'TCL', '小天才',
        '传音', '龙旗', '研祥'
    ],
    '制造-化工': [
        '化工', '三宁化工', '中烟'
    ],
    '制造-其他': [
        '制造', '工业', '生产', '施耐德', '福耀玻璃'
    ],
    '互联网-电商': [
        '电商', '淘宝', '天猫', '京东', '拼多多', '唯品会',
        '壹药网', '111集团', '111健康'
    ],
    '互联网-游戏': [
        '游戏', '网络游戏', '百度游戏', '多酷'
    ],
    '互联网-其他': [
        '互联网', '科技', '网络', '中移互联', '字节', '腾讯',
        '阿里', '百度', '美团', '滴滴'
    ],
    '通信-运营商': [
        '移动', '联通', '电信', '中国移动', '中国联通', '中国电信',
        '广东移动', '山东移动', '浙江移动'
    ],
    '能源-电力': [
        '电力', '电网', '南方电网', '国家电网', '国网', '供电',
        '电站', '发电'
    ],
    '能源-石油': [
        '石油', '中石油', '中石化', '中海油', '石油化工'
    ],
    '能源-其他': [
        '能源', '煤炭', '淮河能源', '淮南矿业', '新能源', '金风'
    ],
    '交通-航空': [
        '航空', '航天', '机场', '春秋航空', '吉祥航空', '海航'
    ],
    '交通-铁路': [
        '铁路', '高铁', '地铁', '轨道', '广州地铁', '重庆轨道'
    ],
    '交通-物流': [
        '物流', '快递', '德邦', '顺丰', '圆通', '中通', '申通'
    ],
    '房地产': [
        '地产', '房地产', '置业', '碧桂园', '万科', '恒大', '融创',
        '保利', '龙湖', '中海', '华润', '金茂', '龙光', '建工'
    ],
    '零售-百货': [
        '沃尔玛', '家乐福', '大润发', '百货', '商场', '超市'
    ],
    '零售-餐饮': [
        '餐饮', '百胜', '肯德基', '必胜客', '麦当劳', '星巴克',
        '海底捞', '西贝', '锦江', '酒店', '东呈'
    ],
    '零售-服装': [
        '服装', '服饰', '安踏', '李宁', '特步', '361', 'LVMH',
        '百丽', '屈臣氏', '维达', '名创优品'
    ],
    '零售-其他': [
        '零售', '连锁', '商贸', '贸易', '国贸'
    ],
    '教育': [
        '教育', '学校', '大学', '学院', '培训', '新东方', '好未来',
        '精锐', '上海财经大学', '深圳职业'
    ],
    '医疗': [
        '医疗', '医院', '诊所', '卫生', '药', '健康', '生物', '医药'
    ],
    '政府-海关': [
        '海关'
    ],
    '政府-其他': [
        '政府', '公安', '税务', '工商', '市场监管', '环保',
        '生态环境', '住房公积金'
    ],
    '军工': [
        '军工', '中国工程物理研究院', '一飞院', '603所', '航空工业'
    ],
    '建筑-工程': [
        '建设', '建筑', '工程', '设计院', '勘测', '中国电建',
        '中建', '中铁', '中交', '市政'
    ],
    '农业': [
        '农业', '农林', '畜牧', '渔业', '种植', '国元农'
    ],
    'IT服务': [
        '软件', '信息技术', '数据', '云计算', '大数据', '人工智能',
        '微创', '复深蓝', '华青融天', '精鸿', '蒙帕', '鼎茂',
        '优易', '云霁', '维致', '先云', '荣景', '智创', '龙智'
    ],
}

def identify_industry_from_customer(customer_name):
    """根据客户名称识别行业"""
    if not customer_name or str(customer_name).strip() in ['', 'None', 'nan']:
        return ""

    customer_name = str(customer_name)

    # 按优先级检查关键词
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in customer_name:
                return industry

    return ""

def is_maintenance_contract(contract_name):
    """判断是否为维保合同"""
    if not contract_name or str(contract_name).strip() in ['', 'None', 'nan']:
        return False

    contract_name = str(contract_name)

    # 维保合同关键词
    maintenance_keywords = [
        '维保', '维护', '售后服务', '售后维保', '运维服务',
        '技术服务合同', '维保服务', '维保费', '系统维护',
        '运行维护', '维护服务', '保养', '保修', '质保'
    ]

    # 检查是否包含维保关键词
    for keyword in maintenance_keywords:
        if keyword in contract_name:
            return True

    return False

def extract_modules_from_text(text):
    """从文本中提取模块关键词"""
    if not text or str(text).strip() in ['', 'None', 'nan']:
        return ""

    text = str(text)
    found_modules = []

    # 按优先级检查关键词
    for keyword in MODULE_KEYWORDS:
        if keyword in text and keyword not in found_modules:
            found_modules.append(keyword)

    # 如果没找到，尝试一些组合模式
    if not found_modules:
        if '运维' in text and '平台' in text:
            found_modules.append('自动化运维')
        elif 'CMDB' in text.upper():
            found_modules.append('CMDB')
        elif '监控' in text:
            found_modules.append('监控')

    return '+'.join(found_modules) if found_modules else ""

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

        # 读取表头并找到列索引
        headers = {}
        for col in range(1, cols + 1):
            header = str(worksheet.Cells(1, col).Value or "").strip()
            if header:
                headers[header] = col

        print(f"找到的列: {list(headers.keys())}")

        # 调试：详细显示每个列名
        print(f"\n详细列信息:")
        for col in range(1, cols + 1):
            header = str(worksheet.Cells(1, col).Value or "").strip()
            print(f"  第{col}列: '{header}' (长度:{len(header)})")

        # 确定需要的列（使用更灵活的匹配）
        def find_column(names):
            """在headers中查找列，支持多个候选名称"""
            for name in names:
                if name in headers:
                    return headers[name]
            return None

        required_columns = {
            '客户名称': find_column(['客户名称', '客户']),
            '行业细分': find_column(['行业细分', '行业', '所属行业']),
            '模块': find_column(['模块', '产品模块', '业务模块']),
            '合同名称': find_column(['合同名称', '商机', '项目名称']),
            '合同金额': find_column(['合同金额', '金额', '项目金额']),
            '合同时间': find_column(['合同时间', '签约日期', '时间', '日期', '签订时间']),
            '是否直签': find_column(['是否直签', '签约类型', '合作类型']),
            '代理商': find_column(['代理商', '合作伙伴', '渠道商']),
            '商机': find_column(['商机', '合同名称', '项目名称']),  # 用于提取模块关键字
        }

        print(f"\n列映射:")
        for name, col in required_columns.items():
            print(f"  {name}: 第{col}列" if col else f"  {name}: 未找到")

        # 生成Markdown内容
        markdown_content = []
        markdown_content.append("# 客户案例库\n")
        markdown_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        markdown_content.append(f"**案例总数**: {rows - 1}个\n")
        markdown_content.append("**数据来源**: case.xlsx\n")
        markdown_content.append("\n---\n")
        markdown_content.append("\n## 📊 案例列表\n")
        markdown_content.append("\n| 客户名称 | 行业细分 | 模块 | 合同名称 | 合同金额(万) | 合同时间 | 是否直签 | 代理商 |")
        markdown_content.append("\n|---------|---------|------|---------|------------|---------|---------|--------|")

        # 读取数据行
        case_count = 0
        module_extracted_count = 0
        industry_identified_count = 0
        maintenance_filtered_count = 0

        for row in range(2, rows + 1):
            try:
                # 读取客户名称
                customer_col = required_columns.get('客户名称')
                if not customer_col:
                    continue
                customer = str(worksheet.Cells(row, customer_col).Value or "").strip()

                # 跳过空行
                if not customer:
                    continue

                # 读取合同名称（用于判断是否为维保合同）
                contract_col = required_columns.get('合同名称')
                contract = str(worksheet.Cells(row, contract_col).Value or "").strip() if contract_col else ""

                # 过滤维保合同
                if is_maintenance_contract(contract):
                    maintenance_filtered_count += 1
                    continue

                # 读取行业细分
                industry_col = required_columns.get('行业细分')
                industry = str(worksheet.Cells(row, industry_col).Value or "").strip() if industry_col else ""

                # 如果行业细分为空，从客户名称自动识别
                if not industry or industry in ['None', 'nan', '']:
                    identified_industry = identify_industry_from_customer(customer)
                    if identified_industry:
                        industry = identified_industry
                        industry_identified_count += 1

                # 读取模块
                module_col = required_columns.get('模块')
                module = str(worksheet.Cells(row, module_col).Value or "").strip() if module_col else ""

                # 如果模块为空，从商机字段提取
                if not module or module in ['None', 'nan', '']:
                    opportunity_col = required_columns.get('商机')
                    if opportunity_col:
                        opportunity_text = str(worksheet.Cells(row, opportunity_col).Value or "")
                        extracted_module = extract_modules_from_text(opportunity_text)
                        if extracted_module:
                            module = extracted_module
                            module_extracted_count += 1
                            print(f"  行{row}: 从商机提取模块 [{extracted_module}]")

                # 处理金额
                amount_col = required_columns.get('合同金额')
                if amount_col:
                    amount_val = worksheet.Cells(row, amount_col).Value
                    if amount_val is None or amount_val == "":
                        amount = "-"
                    else:
                        # 尝试格式化为数字
                        try:
                            amount_num = float(str(amount_val).replace('万', '').replace(',', ''))
                            amount = f"{amount_num:.0f}"
                        except:
                            amount = str(amount_val).strip()
                else:
                    amount = "-"

                # 处理时间
                time_col = required_columns.get('合同时间')
                if time_col:
                    time_val = worksheet.Cells(row, time_col).Value
                    if time_val is None or time_val == "":
                        contract_time = "-"
                    else:
                        # 处理日期对象
                        if isinstance(time_val, datetime):
                            # Excel日期格式，转换为YYYY年MM月格式
                            contract_time = time_val.strftime('%Y年%m月')
                        else:
                            # 字符串格式，尝试解析并转换
                            time_str = str(time_val).strip()
                            if time_str and time_str not in ['None', 'nan', '-']:
                                # 尝试解析 YYYY-MM-DD 格式
                                try:
                                    match = re.match(r'(\d{4})-(\d{2})-(\d{2})', time_str)
                                    if match:
                                        year, month, day = match.groups()
                                        contract_time = f"{year}年{int(month):02d}月"
                                    else:
                                        contract_time = time_str
                                except:
                                    contract_time = time_str
                            else:
                                contract_time = "-"
                else:
                    contract_time = "-"

                # 是否直签
                direct_col = required_columns.get('是否直签')
                if direct_col:
                    is_direct_val = str(worksheet.Cells(row, direct_col).Value or "").strip()
                    # 处理"签约类型"字段：直签/代理商
                    if '直签' in is_direct_val or '直接' in is_direct_val:
                        is_direct = "是"
                    elif '代理' in is_direct_val or '渠道' in is_direct_val:
                        is_direct = "否"
                    elif is_direct_val.lower() in ['是', 'yes', 'y', '1', 'true', '1.0']:
                        is_direct = "是"
                    elif is_direct_val.lower() in ['否', 'no', 'n', '0', 'false', '0.0']:
                        is_direct = "否"
                    else:
                        # 如果有代理商，则为代理
                        agent_col_temp = required_columns.get('代理商')
                        if agent_col_temp:
                            agent_check = str(worksheet.Cells(row, agent_col_temp).Value or "").strip()
                            if agent_check and agent_check not in ["None", "nan", "-"]:
                                is_direct = "否"
                            else:
                                is_direct = "是"
                        else:
                            is_direct = "是"
                else:
                    # 如果没有"是否直签"列，根据代理商列判断
                    agent_col_temp = required_columns.get('代理商')
                    if agent_col_temp:
                        agent_check = str(worksheet.Cells(row, agent_col_temp).Value or "").strip()
                        if agent_check and agent_check not in ["None", "nan", "-", ""]:
                            is_direct = "否"
                        else:
                            is_direct = "是"
                    else:
                        is_direct = "是"

                # 代理商
                agent_col = required_columns.get('代理商')
                if agent_col:
                    agent_val = str(worksheet.Cells(row, agent_col).Value or "").strip()
                    if not agent_val or agent_val in ["None", "nan"]:
                        if is_direct == "否":
                            agent = "待补充"
                        else:
                            agent = "-"
                    else:
                        agent = agent_val
                else:
                    agent = "-"

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
        markdown_content.append("\n- **数据来源**: case.xlsx")
        markdown_content.append("\n- **更新方式**: 运行 `python scripts/convert_cases.py` 脚本自动生成")
        markdown_content.append("\n- **注意事项**: 直接编辑此文件的修改会在下次运行脚本时被覆盖")
        markdown_content.append(f"\n- **模块自动提取**: 本次从商机字段自动提取了 {module_extracted_count} 个模块")
        markdown_content.append(f"\n- **行业自动识别**: 本次从客户名称自动识别了 {industry_identified_count} 个行业")

        markdown_content.append("\n\n---\n")
        markdown_content.append(f"\n**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        markdown_content.append("\n**维护者**: AI Solutions Expert Team\n")

        # 写入文件
        final_content = ''.join(markdown_content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"\n✅ 成功生成案例库文件: {output_path}")
        print(f"📊 共处理 {case_count} 条案例")
        print(f"🔍 自动提取模块 {module_extracted_count} 次")
        print(f"🏢 自动识别行业 {industry_identified_count} 次")

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
