---
name: daily-report
description: 日报生成技能，通过扫描工作空间文件变化，自动识别前一天新增或修改的文件，智能分析文件内容生成工作日报
category: productivity
priority: medium
---

# Daily Report (日报生成技能)

## Purpose

为销售和项目团队提供自动化的日报生成能力，通过分析项目状态文件的会话轨迹和文件系统变化来客观准确地汇总工作成果。

**核心功能**:
- 优先分析项目状态.md中的会话轨迹章节（最准确）
- 自动扫描 /workspace 目录的文件变化（补充）
- 识别前一天新增或修改的文件
- 智能分析文件内容，提取关键信息
- 自动分类和优先级排序
- 生成简洁的工作日报
- 自动保存并同步到 Javis 平台

**核心优势**:
- ✅ **双数据源**：会话轨迹（优先）+ 文件变化（补充），确保准确性
- ✅ **客观准确**：基于实际的工作记录和文件系统变化
- ✅ **自动化**：无需手动整理，自动扫描和分析
- ✅ **智能化**：自动识别项目、提取关键数据
- ✅ **结构化**：标准格式，便于快速阅读和追溯

## When to Use

在以下情况下使用此技能：
- 每天工作结束时需要生成日报
- 需要快速汇总当天的工作成果
- 需要向上级或团队汇报当天进展

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| date | string | ❌ | 今天 | 日报日期，格式：YYYY-MM-DD，默认为当天 |
| output_path | string | ❌ | /workspace/日报/ | 日报保存路径 |

**文件名格式**：
- 格式：`{创建者姓名}-{空间名称}-{日期}.md`
- 示例：`黄星玲-越南银行-2026-03-02.md`
- 创建者姓名通过 Javis API 获取（`/api/v1/workspaces/{id}`）
- 空间名称从环境变量 `JAVIS_WORKSPACE_NAME` 获取
- 如果 API 调用失败，使用 `JAVIS_LOGIN_USERNAME` 作为备选

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的工作日报助手，擅长从文件系统变化中提取关键工作事项，生成简洁清晰的工作汇报。

**核心原则**：
1. **简洁性优先**：只记录完成事项和待办事项
2. **结果导向**：关注实际产出的文件和成果，而非过程细节
3. **结构清晰**：使用标准格式，便于快速阅读
4. **客观准确**：基于文件系统的实际变化，而非主观记录

### 执行流程

#### 第一步：确定日期和获取用户信息

```bash
# 获取当前日期（今天）
current_date=$(date +%Y-%m-%d)

# 检查是否为工作日（周一到周五）
day_of_week=$(date +%u)  # 1=周一, 7=周日
if [ "$day_of_week" -gt 5 ]; then
    echo "ℹ️ 今天是周末，无需生成日报。"
    exit 0
fi

# 计算前一天的日期（日报统计的是前一天的工作）
yesterday=$(date -d "yesterday" +%Y-%m-%d)
yesterday_timestamp=$(date -d "yesterday" +%s)

# 获取空间创建者姓名和空间名称
workspace_id="${JAVIS_WORKSPACE_ID}"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${workspace_id}"


# 通过API获取创建者姓名（带重试机制）
creator_name=""
max_retries=3
retry_count=0

while [ $retry_count -lt $max_retries ] && [ -z "$creator_name" ]; do
    retry_count=$((retry_count + 1))
    echo "🔄 正在获取创建者姓名（第 ${retry_count}/${max_retries} 次尝试）..."

    creator_name=$(curl -s -H "Authorization: Bearer ${auth_token}" "${api_url}" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['data']['creator']['name'])" 2>/dev/null)

    # 如果获取失败且未达到最大重试次数，等待1秒后重试
    if [ -z "$creator_name" ] && [ $retry_count -lt $max_retries ]; then
        sleep 1
    fi
done

# 如果3次尝试都失败，使用"未知用户"
if [ -z "$creator_name" ]; then
    creator_name="未知用户"
    echo "⚠️ 无法获取创建者姓名，使用默认值：未知用户"
fi

workspace_name="${JAVIS_WORKSPACE_NAME:-未知空间}"

# 创建日报目录
mkdir -p /workspace/日报
```

#### 第二步：扫描工作空间文件变化

**使用 find 命令扫描前一天新增或修改的文件**：

```bash
# 扫描 /workspace 目录下前一天新增或修改的文件
# 排除特定目录和文件类型
echo "🔍 正在扫描 /workspace 目录的文件变化..."

# 查找前一天（24小时内）修改的文件
# -type f: 只查找文件
# -mtime -1: 24小时内修改的文件
# ! -path: 排除特定目录
changed_files=$(find /workspace \
  -type f \
  -mtime -1 \
  ! -path "*/日报/*" \
  ! -path "*/.git/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/.*" \
  ! -name "*.log" \
  ! -name "*.tmp" \
  2>/dev/null)

# 检查是否有文件变化
if [ -z "$changed_files" ]; then
    echo "ℹ️ 昨日（${yesterday}）无文件变化记录，无需生成日报。"
    exit 0
fi

# 统计文件数量
file_count=$(echo "$changed_files" | wc -l)
echo "📊 发现 ${file_count} 个文件在昨日有变化"
```

**文件分类和优先级**：

按照文件类型和所在目录进行分类，识别工作重点：

```bash
# 定义文件分类规则
declare -A file_categories

# 项目文档类（高优先级）
project_docs=$(echo "$changed_files" | grep -E "项目状态\.md|项目相关方\.md|会议纪要.*\.md|需求.*\.md|方案.*\.md")

# 案例和报告类（高优先级）
case_reports=$(echo "$changed_files" | grep -E "案例匹配报告|商务分析|需求分析|会议分析|POC.*\.md")

# 话术和准备资料（中优先级）
sales_materials=$(echo "$changed_files" | grep -E "话术|销售准备|拜访资料")

# 其他工作文件（中优先级）
other_files=$(echo "$changed_files" | grep -E "\.md$|\.docx$|\.xlsx$" | grep -v -E "项目状态|案例匹配|商务分析|需求分析|会议分析|话术")

# 按优先级合并文件列表
priority_files=$(printf "%s\n%s\n%s\n%s" "$project_docs" "$case_reports" "$sales_materials" "$other_files" | grep -v "^$")
```

#### 第三步：智能分析文件内容

**优先分析项目状态.md中的会话轨迹**：

```bash
# 存储完成事项
declare -a completed_tasks

# 第一优先级：从项目状态.md的会话轨迹章节提取工作记录
echo "🔍 分析项目状态文件的会话轨迹..."

# 查找所有项目的项目状态文件
status_files=$(find /workspace -name "项目状态.md" -type f ! -path "*/日报/*" 2>/dev/null)

while IFS= read -r status_file; do
    if [ ! -f "$status_file" ]; then
        continue
    fi

    project_name=$(dirname "$status_file" | xargs basename)

    # 提取会话轨迹章节中昨天的记录
    # 会话轨迹格式：| 时间 | Agent/Skill | 会话简要总结 |

    # 使用 awk 提取会话轨迹章节
    in_session_section=0
    while IFS= read -r line; do
        # 检测会话轨迹章节开始
        if [[ "$line" =~ ^##[[:space:]]*🔄[[:space:]]*会话轨迹 ]]; then
            in_session_section=1
            continue
        fi

        # 检测下一个章节开始（会话轨迹章节结束）
        if [[ "$in_session_section" -eq 1 ]] && [[ "$line" =~ ^##[[:space:]] ]]; then
            break
        fi

        # 在会话轨迹章节内，提取昨天的记录
        if [[ "$in_session_section" -eq 1 ]] && [[ "$line" =~ ^\|[[:space:]]*${yesterday} ]]; then
            # 提取表格行：| 时间 | Agent/Skill | 会话简要总结 |
            summary=$(echo "$line" | awk -F'|' '{print $4}' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

            if [ -n "$summary" ]; then
                completed_tasks+=("${project_name}: ${summary}")
            fi
        fi
    done < "$status_file"

done <<< "$status_files"

echo "✅ 从会话轨迹提取到 ${#completed_tasks[@]} 项记录"

# 第二优先级：如果会话轨迹没有记录，则分析文件变化
if [ ${#completed_tasks[@]} -eq 0 ]; then
    echo "📋 会话轨迹无记录，开始分析文件变化..."

    # 分析每个文件，提取关键信息
    while IFS= read -r file_path; do
        if [ ! -f "$file_path" ]; then
            continue
        fi

        # 获取文件名和所在目录
        file_name=$(basename "$file_path")
        dir_name=$(dirname "$file_path" | xargs basename)

        # 根据文件类型和内容智能生成工作描述
        case "$file_path" in
            *"项目状态.md")
                # 项目状态更新
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                completed_tasks+=("更新项目状态：${project_name}")
                ;;
            *"案例匹配报告"*)
                # 案例匹配
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                # 从文件中提取匹配数量
                case_count=$(grep -oP "共匹配:\s*\K\d+" "$file_path" 2>/dev/null | head -1)
                if [ -n "$case_count" ]; then
                    completed_tasks+=("完成${project_name}案例匹配分析（匹配${case_count}个案例）")
                else
                    completed_tasks+=("完成${project_name}案例匹配分析")
                fi
                ;;
            *"需求分析"*|*"需求匹配"*)
                # 需求分析
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                # 从文件中提取需求数量和匹配度
                req_count=$(grep -oP "需求总数:\s*\K\d+" "$file_path" 2>/dev/null | head -1)
                match_rate=$(grep -oP "匹配度:\s*\K[\d.]+%" "$file_path" 2>/dev/null | head -1)
                if [ -n "$req_count" ] && [ -n "$match_rate" ]; then
                    completed_tasks+=("完成${project_name}需求分析（${req_count}条需求，匹配度${match_rate}）")
                else
                    completed_tasks+=("完成${project_name}需求分析")
                fi
                ;;
            *"会议分析"*|*"会议纪要"*)
                # 会议分析
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                meeting_date=$(grep -oP "会议时间:\s*\K[\d-]+" "$file_path" 2>/dev/null | head -1)
                if [ -n "$meeting_date" ]; then
                    completed_tasks+=("分析${project_name}会议纪要（${meeting_date}）")
                else
                    completed_tasks+=("分析${project_name}会议纪要")
                fi
                ;;
            *"商务分析"*)
                # 商务分析
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                score=$(grep -oP "预估得分:\s*\K[\d.]+" "$file_path" 2>/dev/null | head -1)
                if [ -n "$score" ]; then
                    completed_tasks+=("完成${project_name}商务评分分析（预估得分${score}分）")
                else
                    completed_tasks+=("完成${project_name}商务评分分析")
                fi
                ;;
            *"话术"*)
                # 销售话术
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                completed_tasks+=("生成${project_name}销售话术")
                ;;
            *"方案"*)
                # 方案文档
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                completed_tasks+=("编写${project_name}方案文档")
                ;;
            *)
                # 其他文件，根据目录名称推断
                project_name=$(echo "$file_path" | sed 's|/workspace/||' | cut -d'/' -f1)
                if [[ "$project_name" != "日报" ]] && [[ "$project_name" != "." ]]; then
                    completed_tasks+=("更新${project_name}项目文档（${file_name}）")
                fi
                ;;
        esac
    done <<< "$priority_files"

    echo "✅ 从文件变化提取到 ${#completed_tasks[@]} 项记录"
fi

# 去重和排序
completed_tasks=($(printf '%s\n' "${completed_tasks[@]}" | sort -u))

# 检查是否有实质性工作内容
if [ ${#completed_tasks[@]} -eq 0 ]; then
    echo "ℹ️ 昨日（${yesterday}）无实质性工作记录，无需生成日报。"
    exit 0
fi

echo "✅ 最终提取到 ${#completed_tasks[@]} 项完成事项"
```

**智能分析策略**：
1. **第一优先级**: 从所有项目的"项目状态.md"文件中提取"会话轨迹"章节
2. **精确匹配**: 只提取日期为`${yesterday}`的会话记录
3. **格式解析**: 解析表格格式 `| 时间 | Agent/Skill | 会话简要总结 |`
4. **项目关联**: 自动关联项目名称，格式为"项目名: 会话总结"
5. **第二优先级**: 如果会话轨迹没有记录，则分析文件系统变化作为补充

#### 第四步：识别待办事项

**从项目状态文件中提取待办事项**：

```bash
# 存储待办事项
declare -a todo_tasks

# 查找所有项目的项目状态文件
status_files=$(find /workspace -name "项目状态.md" -type f ! -path "*/日报/*" 2>/dev/null)

while IFS= read -r status_file; do
    if [ ! -f "$status_file" ]; then
        continue
    fi

    project_name=$(dirname "$status_file" | xargs basename)

    # 从项目状态文件中提取待办事项
    # 1. 查找"会话轨迹"章节中的待办事项标识
    # 2. 查找标记为"待办"、"TODO"、"计划"的内容
    # 3. 查找未完成的checkbox项 "- [ ]"

    # 提取未完成的待办事项
    pending_items=$(grep -E "\- \[ \]" "$status_file" 2>/dev/null)

    while IFS= read -r item; do
        if [ -n "$item" ]; then
            # 清理格式，只保留内容
            clean_item=$(echo "$item" | sed 's/- \[ \] //' | sed 's/^\s*//')
            if [ -n "$clean_item" ]; then
                todo_tasks+=("$clean_item")
            fi
        fi
    done <<< "$pending_items"

done <<< "$status_files"

# 如果没有找到待办事项，添加默认提示
if [ ${#todo_tasks[@]} -eq 0 ]; then
    todo_tasks+=("持续跟进客户项目进展")
    todo_tasks+=("准备下一阶段工作资料")
fi

# 去重
todo_tasks=($(printf '%s\n' "${todo_tasks[@]}" | sort -u | head -10))

echo "📋 提取到 ${#todo_tasks[@]} 项待办事项"
```

**待办事项来源**：
- 项目状态文件中的未完成checkbox
- 项目状态文件中标记为"待办"的内容
- 如果没有明确的待办事项，生成通用的跟进提示

**日报模板**：

```markdown
# 工作日报 - {日期}

## ✅ 今日完成
{列出当天完成的主要任务，每项1行}
1. 任务1：简要描述和结果
2. 任务2：简要描述和结果
3. 任务3：简要描述和结果

## 📌 待办事项
{列出待办任务，每项1行}
- [ ] 待办1
- [ ] 待办2
- [ ] 待办3

---
*生成时间: {时间戳}*
```

#### 第五步：生成日报

**日报模板**：

```bash
# 构建日报内容
report_content="# 工作日报 - ${yesterday}

## ✅ 今日完成

"

# 添加完成事项（编号列表）
index=1
for task in "${completed_tasks[@]}"; do
    report_content="${report_content}${index}. ${task}
"
    index=$((index + 1))
done

report_content="${report_content}
## 📌 待办事项

"

# 添加待办事项（checkbox列表）
for todo in "${todo_tasks[@]}"; do
    report_content="${report_content}- [ ] ${todo}
"
done

# 添加时间戳
current_time=$(date +"%Y-%m-%d %H:%M:%S")

# 确定数据来源
if [ ${#completed_tasks[@]} -gt 0 ]; then
    data_source="会话轨迹 (优先) + 文件变化 (补充)"
else
    data_source="文件变化分析"
fi

report_content="${report_content}
---
*生成时间: ${current_time}*
*统计日期: ${yesterday}*
*文件变更数: ${file_count}个*
*数据来源: ${data_source}*
"

echo "📝 日报内容生成完成"
```

**日报格式说明**：
- 标题使用统计日期（昨天）
- 完成事项使用编号列表（1. 2. 3.）
- 待办事项使用checkbox列表（- [ ]）
- 包含生成时间和统计日期
- 显示文件变更数量

#### 第六步：保存日报并同步到 Javis

```bash
# 保存日报到本地
# 注意：日报文件名使用工作日期（昨天），与日报内容统计日期保持一致
output_file="/workspace/日报/${creator_name}-${workspace_name}-${yesterday}.md"
echo "$report_content" > "$output_file"
echo "✅ 日报已生成: $output_file"

# 同步到 Javis 平台
daily_report_workspace_id="cmm8se74z049g30s5eeazl02d"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${daily_report_workspace_id}/files/text-file"

# 构建请求体
file_name="${creator_name}-${workspace_name}-${yesterday}.md"
parent_path="会议纪要内容/日报周报内容"

# 调用 API 上传日报
curl -X POST "${api_url}" \
  -H "Authorization: Bearer ${auth_token}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${file_name}\",
    \"parentPath\": \"${parent_path}\",
    \"content\": $(echo "$report_content" | jq -Rs .)
  }"

echo "✅ 日报已同步到 Javis 平台: ${parent_path}/${file_name}"
echo ""
echo "📊 统计摘要："
echo "  - 统计日期: ${yesterday}"
echo "  - 文件变更: ${file_count}个"
echo "  - 完成事项: ${#completed_tasks[@]}项"
echo "  - 待办事项: ${#todo_tasks[@]}项"
```

### 输出示例

**完整日报示例**：

```markdown
# 工作日报 - 2026-03-04

## ✅ 今日完成

1. 招商银行-CMDB项目: 完成企业调研（金融-银行），匹配8个案例，生成销售话术
2. 招商银行-CMDB项目: 分析45条需求，匹配度79.8%，识别3项定制化需求
3. 国家电网-监控平台: 分析商务评分表，预估得分85分，识别2个风险项
4. 中国移动-ITSM项目: 分析会议纪要，识别客户痛点：性能问题、运维效率低。销售阶段：需求探索

## 📌 待办事项

- [ ] 跟进招商银行CMDB项目技术澄清
- [ ] 完成国家电网投标方案编写
- [ ] 准备中国移动项目二次拜访资料
- [ ] 持续跟进客户项目进展

---
*生成时间: 2026-03-05 09:00:15*
*统计日期: 2026-03-04*
*文件变更数: 12个*
*数据来源: 会话轨迹 (优先) + 文件变化 (补充)*
```

## Best Practices

### 内容提取原则

**数据来源优先级**：
1. **第一优先级 - 会话轨迹**：从项目状态.md的"会话轨迹"章节提取
   - 优势：最准确、最详细的工作记录
   - 格式：`| 时间 | Agent/Skill | 会话简要总结 |`
   - 只提取日期匹配的记录
2. **第二优先级 - 文件变化**：扫描文件系统变化作为补充
   - 优势：即使没有会话轨迹也能生成日报
   - 通过文件类型和内容智能推断工作内容

**DO（推荐做法）**：
- ✅ 优先使用会话轨迹，数据最准确
- ✅ 会话轨迹格式为"项目名: 会话总结"
- ✅ 文件变化作为补充数据源
- ✅ 保持简洁明了，一行一项
- ✅ 自动关联项目名称和文件类型

**DON'T（避免做法）**：
- ❌ 不要包含日报生成相关的文件
- ❌ 不要记录技术配置文件的变化
- ❌ 不要包含临时文件和日志文件
- ❌ 不要重复记录相同的工作事项

### 文件扫描规范

**包含的文件类型**：
- Markdown文档（.md）
- Word文档（.docx）
- Excel文档（.xlsx）
- 项目状态文件
- 会议纪要、需求文档、方案文档等

**排除的目录和文件**：
- 日报目录（/workspace/日报/）
- Git目录（.git/）
- 依赖目录（node_modules/, __pycache__/）
- 隐藏文件和目录（.*）
- 日志文件（*.log）
- 临时文件（*.tmp）

### 格式规范

- 使用Markdown格式
- 使用emoji增强可读性（✅📌）
- 使用列表而非段落
- 包含时间戳

## Examples

### 示例1：标准日报生成

**输入**：
```
用户：生成今天的日报
```

**系统执行**：
1. 扫描 /workspace 目录
2. 发现12个文件在昨天有变化
3. 分析文件内容，提取4项完成事项
4. 从项目状态文件提取4项待办事项
5. 生成日报并同步

**输出**：
```
🔍 正在扫描 /workspace 目录的文件变化...
📊 发现 12 个文件在昨日有变化
🔍 分析项目状态文件的会话轨迹...
✅ 从会话轨迹提取到 4 项记录
✅ 最终提取到 4 项完成事项
📋 提取到 4 项待办事项
📝 日报内容生成完成
✅ 日报已生成: /workspace/日报/黄星玲-越南银行-2026-03-04.md
✅ 日报已同步到 Javis 平台: 会议纪要内容/日报周报内容/黄星玲-越南银行-2026-03-04.md

📊 统计摘要：
  - 统计日期: 2026-03-04
  - 文件变更: 12个
  - 完成事项: 4项
  - 待办事项: 4项
```

### 示例2：无工作内容

**输入**：
```
用户：生成今天的日报
```

**场景**：昨天没有文件变化

**输出**：
```
🔍 正在扫描 /workspace 目录的文件变化...
ℹ️ 昨日（2026-03-04）无文件变化记录，无需生成日报。
```

### 示例3：周末提示

**输入**：
```
用户：生成今天的日报
```

**场景**：今天是周六或周日

**输出**：
```
ℹ️ 今天是周末，无需生成日报。
```

---

*Skill Version: 3.0.0*
*Last Updated: 2026-03-05*
*Major Change: 从会话分析改为文件系统扫描*
