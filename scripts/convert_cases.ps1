# PowerShell脚本：从case.xlsx生成案例库Markdown文件
param(
    [string]$ExcelPath = "$PSScriptRoot\..\skills\company-research\resource\data\case.xlsx",
    [string]$OutputPath = "$PSScriptRoot\..\skills\company-research\resource\data\caseLibrary.md"
)

# 模块关键词列表
$ModuleKeywords = @(
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
    '智能运维'
)

function Extract-ModulesFromText {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return ""
    }

    $foundModules = @()

    foreach ($keyword in $ModuleKeywords) {
        if ($Text.Contains($keyword) -and $foundModules -notcontains $keyword) {
            $foundModules += $keyword
        }
    }

    # 如果没找到，尝试组合模式
    if ($foundModules.Count -eq 0) {
        if ($Text -match '运维.*平台') {
            $foundModules += '自动化运维'
        }
        elseif ($Text -match 'CMDB') {
            $foundModules += 'CMDB'
        }
        elseif ($Text -match '监控') {
            $foundModules += '监控'
        }
    }

    return ($foundModules -join '+')
}

Write-Host "正在读取Excel文件: $ExcelPath"

# 检查 Excel 是否已安装
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
} catch {
    Write-Host "❌ 错误: 未安装 Microsoft Excel 或无法创建 Excel COM 对象"
    Write-Host "请使用 Python 版本: python scripts/convert_cases.py"
    exit 1
}

try {
    # 打开工作簿
    $workbook = $excel.Workbooks.Open($ExcelPath)
    $worksheet = $workbook.Worksheets.Item(1)

    # 获取使用范围
    $usedRange = $worksheet.UsedRange
    $rowCount = $usedRange.Rows.Count
    $colCount = $usedRange.Columns.Count

    Write-Host "找到 $rowCount 行数据（含表头），$colCount 列"

    # 读取表头并创建列映射
    $headers = @{}
    for ($col = 1; $col -le $colCount; $col++) {
        $header = $worksheet.Cells.Item(1, $col).Text.Trim()
        if ($header) {
            $headers[$header] = $col
        }
    }

    Write-Host "找到的列: $($headers.Keys -join ', ')"

    # 确定需要的列
    $colMap = @{
        '客户名称' = $headers['客户名称']
        '行业细分' = $headers['行业细分']
        '模块' = $headers['模块']
        '合同名称' = if ($headers['合同名称']) { $headers['合同名称'] } else { $headers['商机'] }
        '合同金额' = if ($headers['合同金额']) { $headers['合同金额'] } elseif ($headers['金额']) { $headers['金额'] } else { $null }
        '合同时间' = if ($headers['合同时间']) { $headers['合同时间'] } elseif ($headers['时间']) { $headers['时间'] } else { $null }
        '是否直签' = $headers['是否直签']
        '代理商' = $headers['代理商']
        '商机' = if ($headers['商机']) { $headers['商机'] } else { $headers['合同名称'] }
    }

    Write-Host "`n列映射:"
    foreach ($key in $colMap.Keys) {
        if ($colMap[$key]) {
            Write-Host "  $key`: 第$($colMap[$key])列"
        } else {
            Write-Host "  $key`: 未找到"
        }
    }

    # 准备Markdown内容
    $markdown = @()
    $markdown += "# 客户案例库`n"
    $markdown += "**生成时间**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
    $markdown += "**案例总数**: $($rowCount - 1)个`n"
    $markdown += "**数据来源**: case.xlsx`n"
    $markdown += "`n---`n"
    $markdown += "`n## 📊 案例列表`n"
    $markdown += "`n| 客户名称 | 行业细分 | 模块 | 合同名称 | 合同金额(万) | 合同时间 | 是否直签 | 代理商 |"
    $markdown += "`n|---------|---------|------|---------|------------|---------|---------|--------|"

    # 读取数据行
    $caseCount = 0
    $moduleExtractedCount = 0

    for ($row = 2; $row -le $rowCount; $row++) {
        try {
            # 读取客户名称
            if (-not $colMap['客户名称']) { continue }
            $customer = $worksheet.Cells.Item($row, $colMap['客户名称']).Text.Trim()

            # 跳过空行
            if ([string]::IsNullOrWhiteSpace($customer)) { continue }

            # 读取行业细分
            $industry = ""
            if ($colMap['行业细分']) {
                $industry = $worksheet.Cells.Item($row, $colMap['行业细分']).Text.Trim()
            }

            # 读取模块
            $module = ""
            if ($colMap['模块']) {
                $module = $worksheet.Cells.Item($row, $colMap['模块']).Text.Trim()
            }

            # 如果模块为空，从商机字段提取
            if ([string]::IsNullOrWhiteSpace($module) -and $colMap['商机']) {
                $opportunityText = $worksheet.Cells.Item($row, $colMap['商机']).Text
                $extractedModule = Extract-ModulesFromText -Text $opportunityText
                if ($extractedModule) {
                    $module = $extractedModule
                    $moduleExtractedCount++
                    Write-Host "  行$row`: 从商机提取模块 [$extractedModule]"
                }
            }

            # 读取合同名称
            $contract = ""
            if ($colMap['合同名称']) {
                $contract = $worksheet.Cells.Item($row, $colMap['合同名称']).Text.Trim()
            }

            # 处理金额
            $amount = "-"
            if ($colMap['合同金额']) {
                $amountText = $worksheet.Cells.Item($row, $colMap['合同金额']).Text.Trim()
                if (-not [string]::IsNullOrWhiteSpace($amountText)) {
                    $amount = $amountText -replace '万', '' -replace ',', ''
                }
            }

            # 处理时间
            $time = "-"
            if ($colMap['合同时间']) {
                $timeText = $worksheet.Cells.Item($row, $colMap['合同时间']).Text.Trim()
                if (-not [string]::IsNullOrWhiteSpace($timeText)) {
                    $time = $timeText
                }
            }

            # 是否直签
            $isDirect = "是"
            if ($colMap['是否直签']) {
                $directText = $worksheet.Cells.Item($row, $colMap['是否直签']).Text.Trim()
                if ($directText -match '是|yes|y|1|true') {
                    $isDirect = "是"
                } elseif ($directText -match '否|no|n|0|false') {
                    $isDirect = "否"
                }
            }

            # 代理商
            $agent = "-"
            if ($colMap['代理商']) {
                $agentText = $worksheet.Cells.Item($row, $colMap['代理商']).Text.Trim()
                if (-not [string]::IsNullOrWhiteSpace($agentText)) {
                    $agent = $agentText
                } elseif ($isDirect -eq "否") {
                    $agent = "待补充"
                }
            } elseif ($isDirect -eq "否") {
                $agent = "待补充"
            }

            $markdown += "`n| $customer | $industry | $module | $contract | $amount | $time | $isDirect | $agent |"
            $caseCount++

        } catch {
            Write-Host "处理第 $row 行时出错: $_"
        }
    }

    # 添加说明部分
    $markdown += "`n`n---`n"
    $markdown += "`n## 📋 字段说明`n"
    $markdown += "`n| 字段 | 说明 |"
    $markdown += "`n|------|------|"
    $markdown += "`n| 客户名称 | 签约客户的公司全称或简称 |"
    $markdown += "`n| 行业细分 | 格式：大类-细分（如：金融-银行、政府-事业单位） |"
    $markdown += "`n| 模块 | 项目涉及的产品模块（CMDB、自动化运维、监控等） |"
    $markdown += "`n| 合同名称 | 合同/项目的官方名称 |"
    $markdown += "`n| 合同金额(万) | 合同金额，单位：万元 |"
    $markdown += "`n| 合同时间 | 合同签订时间，格式：YYYY-MM |"
    $markdown += "`n| 是否直签 | 是=优维直接签约；否=通过代理商签约 |"
    $markdown += "`n| 代理商 | 如非直签，填写代理商名称；直签则为 - |"

    $markdown += "`n`n---`n"
    $markdown += "`n## 🔍 使用说明`n"
    $markdown += "`n### 案例筛选规则`n"
    $markdown += "`n1. **行业匹配**: 精确匹配行业细分字段（如：金融-银行）"
    $markdown += "`n2. **模块匹配**: 模糊匹配模块字段（如：搜索CMDB会匹配`"CMDB`"、`"CMDB+自动化`"等）"
    $markdown += "`n3. **时间筛选**: 根据合同时间筛选（一年内/三年内）"
    $markdown += "`n4. **排序规则**: 按合同时间降序排列（最新的在前）"

    $markdown += "`n`n### 数据维护`n"
    $markdown += "`n- **更新频率**: 建议每月更新一次"
    $markdown += "`n- **数据来源**: case.xlsx"
    $markdown += "`n- **更新方式**: 运行 ``python scripts/convert_cases.py`` 脚本自动生成"
    $markdown += "`n- **注意事项**: 直接编辑此文件的修改会在下次运行脚本时被覆盖"
    $markdown += "`n- **模块自动提取**: 本次从商机字段自动提取了 $moduleExtractedCount 个模块"

    $markdown += "`n`n---`n"
    $markdown += "`n**最后更新**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    $markdown += "`n**维护者**: AI Solutions Expert Team`n"

    # 写入文件
    $markdown -join "" | Out-File -FilePath $OutputPath -Encoding UTF8

    Write-Host "`n✅ 成功生成案例库文件: $OutputPath"
    Write-Host "📊 共处理 $caseCount 条案例"
    Write-Host "🔍 自动提取模块 $moduleExtractedCount 次"

} catch {
    Write-Host "❌ 错误: $_"
    Write-Host $_.Exception.Message
    Write-Host $_.ScriptStackTrace
} finally {
    # 关闭Excel
    if ($workbook) {
        $workbook.Close($false)
    }
    if ($excel) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
