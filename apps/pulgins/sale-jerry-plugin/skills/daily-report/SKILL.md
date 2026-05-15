---
name: daily-report
description: 日报生成技能，通过claude-mem获取前一天的sessions记录，智能总结成面向客户推进方向的工作日报（不超过300字）
category: productivity
priority: medium
---
# Daily Report (日报生成技能)

## Purpose

为销售和项目团队提供自动化的日报生成能力，基于 claude-mem 记录的前一天会话内容，智能总结成面向客户推进方向的工作日报。

**核心功能**:

* 通过 claude-mem 获取前一天的工作会话记录

* 智能分析会话内容，提取客户推进相关的工作事项

* 生成简洁的工作总结（不超过300字）

* 面向客户推进方向，突出销售进展和价值

* 自动保存并同步到 Javis 平台

**核心优势**:

* ✅ **会话驱动**：基于真实的会话记录，反映实际工作内容

* ✅ **客户导向**：总结聚焦于客户推进方向，而非技术细节

* ✅ **简洁高效**：300字以内，快速阅读

* ✅ **智能终止**：周末或无会话记录时自动终止，不生成空日报

## When to Use

在以下情况下使用此技能：

* 每天工作结束时需要生成日报

* 需要快速汇总前一天的客户推进工作

* 需要向上级或团队汇报进展

* 用户说"生成日报"、"今天的日报"、"写日报"等

**日期规则**：

* 日报日期始终为**前一个日历日**（昨天）

* **检测昨天的星期几**：如果昨天是周末则直接终止

* 周六执行 → 昨天周五是工作日 → 正常生成日报

* 周日执行 → 昨天周六是周末 → 终止，不生成日报

* 周一执行 → 昨天周日是周末 → 终止，不生成日报

## Parameters

| 参数   | 类型     | 必须 | 默认值 | 描述                                 |
| ---- | ------ | -- | --- | ---------------------------------- |
| date | string | ❌  | 昨天  | 日报统计日期，格式：YYYY-MM-DD，默认为前一个日历日（昨天） |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的销售工作日报助手，擅长从会话记录中提取客户推进相关的工作事项，生成简洁清晰的工作汇报。

**核心原则**：

1. **客户导向**：只记录与客户推进相关的工作内容
2. **简洁性优先**：总结不超过300字
3. **结果导向**：关注客户进展和推进成果
4. **周末不生成**：昨天是周末时直接终止
5. **无会话即终止**：没有会话记录时不生成日报

### 执行流程

#### 步骤 1: 确定日期并检测周末

```bash
# 计算前一天的日期（日报统计的是前一天的工作）
yesterday=$(date -d "yesterday" +%Y-%m-%d)

# 获取昨天的星期几（1=周一, 7=周日）
yesterday_day_of_week=$(date -d "yesterday" +%u)

# 检查昨天是否为周末
if [ "$yesterday_day_of_week" -gt 5 ]; then
    echo "ℹ️ 昨天（${yesterday}）是周末，无需生成日报。"
    exit 0
fi

echo "📅 正在生成 ${yesterday} 的工作日报..."
```

**日期规则说明**：

* 日报记录的是**昨天**的工作，所以检测**昨天**的星期几

* 周六执行 → 昨天周五（1-5）→ 是工作日 → 继续生成日报

* 周日执行 → 昨天周六（6）→ 是周末 → 终止

* 周一执行 → 昨天周日（7）→ 是周末 → 终止

#### 步骤 2: 获取前一天会话记录

**⚠️ 前置检查：claude-mem MCP Server 可用性检测（必须执行，禁止跳过）**

在调用 `claude-mem:mem-search` 之前，**必须先确认当前环境已配置 claude-mem MCP Server**。检测方法：

```
调用 mcp__plugin_claude-mem_mcp-search__search 工具（任意简单参数即可，如 query="test", limit=1）：
- 如果调用成功（正常返回结果或空结果）→ MCP Server 可用，继续步骤 2
- 如果调用失败（工具不存在、连接超时、MCP Server 未启动等）→ 等待 1 分钟后重试
- 最多重试 3 次，3 次全部失败 → 触发降级处理
```

**重试逻辑（伪代码）**：

```python
MAX_RETRIES = 3
mcp_available = False

for attempt in range(1, MAX_RETRIES + 1):
    try:
        result = call_tool("mcp__plugin_claude-mem_mcp-search__search", {"query": "test", "limit": 1})
        mcp_available = True
        break  # 成功，退出重试循环
    except Exception as e:
        print(f"⚠️ 第 {attempt}/{MAX_RETRIES} 次检测失败: {e}")
        if attempt < MAX_RETRIES:
            print(f"   等待 1 分钟后重试...")
            sleep(60)

if not mcp_available:
    # 3 次全部失败 → 降级处理（见下方）
    ...
```

**⚠️ 降级处理（3 次重试全部失败后）**：

3 次检测全部失败后，**禁止继续获取会话记录**，但**不直接终止**——而是将以下友好提示嵌入日报正文中生成并保存：

```markdown
⚠️ 记忆系统不可用

当前空间未启用记忆系统（claude-mem），无法获取会话记录，日报内容无法自动生成。

💡 解决方法：请前往 **设置 → AI模型 → 记忆系统**，打开记忆系统开关并配置 claude-mem MCP Server，之后重新生成日报。

---
*统计日期: {yesterday}*
*状态: MCP Server 不可用（已重试 3 次）*
```

**判断依据**：
- MCP Server 工具调用报错（如 `tool not found`、`MCP server not connected`）
- 工具调用超时无响应
- 返回结果中包含 MCP 连接错误信息

> **注意**：此检查**禁止跳过**，即使日期检查已通过也必须执行。未配置 claude-mem 时不应生成空日报，而应生成包含提示信息的日报文件。

---

**使用 claude-mem 的 search 工具获取会话记录**：

```bash
# 调用 claude-mem search 获取前一天的会话
# ⚠️ 重要：dateEnd 必须比 dateStart 多一天！
# 当 dateStart == dateEnd 时，API 返回空结果
echo "🔍 正在从 claude-mem 获取 ${yesterday} 的会话记录..."

# 使用 Skill 工具调用 claude-mem:mem-search
# 参数：
# - query: 留空或使用通配符，获取所有记录
# - dateStart: ${yesterday}
# - dateEnd: ${yesterday + 1}  ← 注意：要比 dateStart 多一天
# - limit: 100
# - type: sessions（只获取会话）
```

**调用示例（sessions）**：

```json
{
  "skill": "claude-mem:mem-search",
  "args": {
    "query": "",
    "dateStart": "2026-04-02",
    "dateEnd": "2026-04-03",
    "limit": 100,
    "type": "sessions"
  }
}
```

> **说明**：dateEnd 设为 dateStart + 1天（如查4月2日，dateEnd 设为4月3日）。通过 sessions 记录对话会话来生成日报。

#### 步骤 3: 检查会话记录是否存在

**sessions 为空时终止任务**：

```markdown
# 检查结果
if [ ${#sessions} -eq 0 ]; then
    echo "ℹ️ 昨日（${yesterday}）无会话记录，不生成日报。"
    echo ""
    echo "💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。"
    exit 0
fi

echo "✅ 找到 ${#sessions} 条原始会话记录"
```

**终止条件**：

* claude-mem MCP Server 未配置或不可用（提示用户前往设置启用记忆系统）

* 昨天是周末（周六或周日）

* claude-mem 的 sessions 返回空结果

* sessions 数量为 0

> **注意**：会话记录是日报的唯一数据来源，sessions 为空时不生成日报。

#### 步骤 3.5: 过滤无效会话（⚠️ 重要）

**⚠️ 必须过滤掉日报生成技能自身及交付实施类的 sessions，确保日报仅包含售前销售推进相关工作。**

**过滤规则**：

遍历所有会话记录，**排除**符合以下任一条件的会话：

| 过滤类型 | 匹配关键词/模式 | 说明 |
| --------------- | --------------------------------------- | ------------------------- |
| 日报生成技能执行 | `daily-report`、`日报生成`、`生成日报` | 执行 daily-report skill 的会话 |
| 日报系统验证 | `日报系统验证`、`验证系统日期`、`周末检测逻辑` | 系统定时验证任务的会话 |
| 日报相关查询 | `日报` + `生成`/`查看`/`查询` | 查询或生成日报的会话 |
| claude-mem 日报查询 | `daily report`、`get session` + `report` | 从 claude-mem 获取日报数据的会话 |
| 交付验收类 | `交付文档`、`交付验收`、`项目交付`、`交付物` | 售后交付验收阶段工作 |
| 实施部署类 | `实施部署`、`实施配置`、`实施方案`、`实施计划` | 售后实施部署阶段工作 |
| 上线运维类 | `上线`、`部署`、`运维`、`巡检`、`故障处理` | 售后上线运维阶段工作 |
| 项目管理类 | `甘特图`、`项目计划`、`里程碑`、`排期` | 项目经理排期计划工作 |
| 定制开发类 | `定制化开发`、`定制化需求`、`调研清单`、`开发任务` | 售后定制化开发工作 |
| 测试验证类 | `性能测试`、`专项测试`、`UAT`、`测试计划`、`测试用例` | 售后测试验证阶段工作 |
| 文档迭代类 | `实施方案.*迭代`、`V\d+\.\d+.*升级`、`文档格式统一` | 交付文档多版本迭代工作 |

**过滤逻辑伪代码**：

```python
def filter_daily_report_sessions(sessions):
    """过滤掉日报生成相关及交付实施类的会话"""

    # 定义过滤关键词
    filter_keywords = [
        "daily-report",
        "日报生成",
        "生成日报",
        "日报系统验证",
        "验证系统日期",
        "周末检测逻辑",
        "daily report",
        # --- 交付实施类 ---
        "交付文档",
        "交付验收",
        "项目交付",
        "交付物",
        "实施部署",
        "实施配置",
        "实施方案",
        "实施计划",
        "上线",
        "运维",
        "巡检",
        "故障处理",
        # --- 项目管理类 ---
        "甘特图",
        "项目计划",
        "里程碑",
        "排期",
        # --- 定制开发类 ---
        "定制化开发",
        "定制化需求",
        "调研清单",
        "开发任务",
        # --- 测试验证类 ---
        "性能测试",
        "专项测试",
        "测试计划",
        "测试用例",
        "UAT",
        # --- 文档迭代类 ---
        "文档格式统一",
        "发布管理",
    ]

    # 定义过滤模式（请求或完成内容中包含）
    filter_patterns = [
        "日报.*生成",
        "生成.*日报",
        "日报系统",
        # --- 交付实施模式 ---
        "交付.*验收",
        "实施.*方案",
        "实施.*部署",
        "实施.*配置",
        "实施.*迭代",
        "部署.*上线",
        "运维.*巡检",
        # --- 定制开发模式 ---
        "定制化.*开发",
        "定制化.*需求",
        # --- 文档版本迭代模式 ---
        r"V\d+\.\d+.*V\d+\.\d+",   # 如 V1.9→V2.0
        r"V\d+\.\d+.*升级",
        "甘特图.*优化",
        "甘特图.*迭代",
        "文档格式.*统一",
        "调研清单",
        r"调研报告.*V\d",             # 如 调研报告从V1升级到V2
    ]

    filtered_sessions = []
    filtered_count = 0

    for session in sessions:
        request = session.get("request", "").lower()
        completed = session.get("completed", "").lower()
        combined_text = f"{request} {completed}"

        # 检查是否命中过滤条件
        should_filter = False

        # 关键词匹配
        for keyword in filter_keywords:
            if keyword.lower() in combined_text:
                should_filter = True
                break

        # 正则模式匹配
        if not should_filter:
            import re
            for pattern in filter_patterns:
                if re.search(pattern, combined_text):
                    should_filter = True
                    break

        if should_filter:
            filtered_count += 1
            print(f"  🚫 过滤: {request[:50]}...")
        else:
            filtered_sessions.append(session)

    print(f"📊 过滤结果: 原始 {len(sessions)} 条 → 过滤 {filtered_count} 条 → 保留 {len(filtered_sessions)} 条")

    return filtered_sessions
```

**过滤后检查**：

```markdown
# 过滤日报相关会话后，检查是否还有有效数据
sessions = filter_daily_report_sessions(sessions)

if [ ${#sessions} -eq 0 ]; then
    echo "ℹ️ 昨日（${yesterday}）过滤日报会话后无有效工作记录，不生成日报。"
    echo ""
    echo "💡 提示：昨日可能仅执行了日报生成任务，无其他工作内容。"
    exit 0
fi

echo "✅ 过滤后保留 ${#sessions} 条有效会话记录"
```

**⚠️ 重要提醒**：

* 此步骤是**必须执行**的，不能跳过

* 过滤逻辑应在分析会话内容之前执行

* 如果过滤后没有会话，应终止日报生成

#### 步骤 4: 分析会话内容，生成工作总结

**会话聚合分组**：

在分析内容之前，先对 sessions 按主题相似度进行聚合分组，避免逐条列举产生流水账：

**聚合规则**：
- 将 sessions 按主题相似度合并（如同一客户的多次操作、同一功能的多个步骤）
- 每个任务组只生成一条总结，子步骤作为补充说明嵌入其中
- 主题判断依据：客户名称、项目名称、功能模块、工作类型（调研/方案/开发/修复等）

**聚合示例**：

❌ 流水账写法（逐条列举）：
```
1. 打开招商银行项目文件
2. 修改了客户名称
3. 补充了IT规模信息
4. 生成了销售话术
5. 验证了话术内容
```

✅ 聚合写法（合并为一条）：
```
1. **招商银行-CMDB项目**：完成企业调研并生成销售话术（补充IT规模约500人，验证话术针对性）。
```

**分类判断**：

先判断 sessions 的内容是否与客户推进相关，再选择对应的总结策略：

* **与客户推进相关** → 按"客户推进总结"模板，分析推进进展、阶段性成果和待办事项

* **与客户推进无关**（如技术调试、工具开发、环境配置）→ 按"工作内容总结"模板，简述完成的工作和产出

**分析维度（客户推进相关）**：

从 sessions 中提取以下客户推进相关信息：

1. **客户名称**：涉及哪些客户
2. **项目进展**：项目推进到什么阶段
3. **关键动作**：做了哪些推进动作（调研、分析、方案、会议等）
4. **阶段性成果**：取得了什么进展或成果
5. **下一步计划**：接下来要做什么

**总结模板（客户推进相关）**：

```markdown
## 客户推进总结

{不超过300字，聚焦于：}
{- 拜访/跟进的客户}
{- 完成的分析/方案工作}
{- 项目阶段性进展}
{- 待办事项/下一步计划}

---
*统计日期: {日期}*
*会话数: {N}条*
```

**总结模板（非客户推进相关）**：

```markdown
## 工作内容总结

{不超过300字，简述：}
{- 完成的主要工作}
{- 产出物/成果}
{- 待办事项/下一步计划}

---
*统计日期: {日期}*
*会话数: {N}条*
```

**总结写作规范**：

1. **动词开头**：使用"完成"、"推进"、"分析"、"生成"、"修复"等动词
2. **量化成果**：尽可能用数字说话（"匹配5个案例"、"分析20条需求"）
3. **简洁明了**：每项工作1句话，总计不超过300字
4. **包含待办**：末尾列出下一步计划或待办事项

**聚合写作规范**：

1. 同一会话产生的多个操作步骤，合并为一条总结
2. 主句描述任务目标/产出，从句或括号内补充关键细节
3. 一个任务只占一条编号，避免"写了方案→改了客户名→验证了PPT"式的流水账拆分

**示例总结（客户推进相关）**：

```markdown
## 客户推进总结

1. **招商银行-CMDB项目**：完成企业调研，识别客户为金融行业城商行，IT规模约500人；匹配8个金融行业案例；生成针对性销售话术。待办：准备下周拜访材料。

2. **国家电网-监控平台项目**：分析招标商务评分表，预估得分82分，识别2个风险项（资质缺失），输出控标建议3条。待办：与招标方沟通资质要求。

---
*统计日期: 2026-04-02*
*会话数: 5条*
```

**示例总结（非客户推进相关）**：

```markdown
## 工作内容总结

1. **Plugin 开发团队搭建**：完成 agent-teams 目录创建，定义 team-lead、dev-agent、test-agent 等5个 Agent，输出完整 Agent 定义文件。待办：编写集成测试用例。

2. **bid-strategist 合并优化**：将 bid-analysis 合并到 bid-strategist，消除冗余，更新全量引用。待办：提交并推送到 GitHub。

---
*统计日期: 2026-04-03*
*会话数: 3条*
```

#### 步骤 5: 获取空间创建者信息并保存日报

**⚠️ 重要：日报文件命名必须使用【空间创建者】名称，而非执行用户名称！**

**命名规则**：

* 文件格式：`{空间创建者姓名}-{空间名称}-{日期}.md`

* 示例：`张三-华能信息IT资产运维管理平台-2026-04-03.md`

* ❌ 错误示例：`黄星玲-华能信息IT资产运维管理平台-2026-04-03.md`（使用了执行用户）

**获取空间创建者的方法**：

```bash
# 获取空间创建者姓名（注意：必须是创建者，不是当前执行用户！）
workspace_id="${JAVIS_WORKSPACE_ID}"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${workspace_id}"

# ⚠️ 添加重试机制（最多5次，每次间隔30秒）
MAX_RETRIES=5
RETRY_COUNT=0
creator_name=""

echo "📋 正在获取空间创建者信息..."

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ -z "$creator_name" ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "   尝试第 $RETRY_COUNT/$MAX_RETRIES 次..."
    
    # 调用 API 获取工作空间详情
    workspace_response=$(curl -s -H "Authorization: Bearer ${auth_token}" "${api_url}")
    
    # 解析空间创建者姓名（⚠️ 使用 creator.name，不是当前用户！）
    creator_name=$(echo "$workspace_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    # 获取空间创建者姓名（不是执行用户）
    creator = data.get('data', {}).get('creator', {})
    name = creator.get('name', '')
    if name:
        print(name)
    else:
        print('ERROR: creator name not found')
except Exception as e:
    print(f'ERROR: {str(e)}')
" 2>/dev/null)
    
    # 检查本次是否获取成功
    if [ -z "$creator_name" ] || [[ "$creator_name" == "ERROR:"* ]]; then
        echo "   ⚠️ 第 $RETRY_COUNT 次获取失败"
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "   等待 30 秒后重试..."
            sleep 30
        fi
    else
        echo "   ✅ 成功获取空间创建者姓名"
    fi
done

# 重试全部失败后的处理
if [ -z "$creator_name" ]; then
    echo "❌ 重试 $MAX_RETRIES 次后仍无法获取空间创建者姓名"
    echo "   ⚠️ 使用默认值：未知用户"
    creator_name="未知用户"
fi

# 获取空间名称
workspace_name="${JAVIS_WORKSPACE_NAME:-未知空间}"

# 输出调试信息（帮助排查问题）
echo "📋 日报命名信息："
echo "  - 空间创建者: ${creator_name}"
echo "  - 空间名称: ${workspace_name}"
echo "  - 日报日期: ${yesterday}"

# 创建日报目录
mkdir -p /workspace/日报

# 生成文件名（格式：空间创建者-空间名称-日期.md）
output_file="/workspace/日报/${creator_name}-${workspace_name}-${yesterday}.md"
echo "$report_content" > "$output_file"
echo "✅ 日报已生成: $output_file"
```

**⚠️ 常见错误排查**：

| 错误现象                | 原因           | 解决方案                        |
| ------------------- | ------------ | --------------------------- |
| 文件名用"黄星玲"开头         | 使用了执行用户而非创建者 | 确保读取 `creator.name` 而非当前用户  |
| 文件名格式如"黄星玲-mike-日期" | 命名逻辑错误       | 格式应为"创建者-空间名-日期"，检查拼接逻辑     |
| 创建者显示"未知创建者"        | API 调用失败     | 检查 JAVIS\_AUTH\_TOKEN 和网络连接 |

**API 响应示例**：

```json
{
  "data": {
    "id": "xxx",
    "name": "华能信息IT资产运维管理平台",
    "creator": {
      "id": "user_xxx",
      "name": "张三",        // ← 这是空间创建者姓名
      "email": "zhangsan@xxx.com"
    }
  }
}
```

#### 步骤 6: 同步到 Javis 平台（可选）

```bash
# 同步到 Javis 平台
daily_report_workspace_id="cmm8se74z049g30s5eeazl02d"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${daily_report_workspace_id}/files/text-file"

file_name="${creator_name}-${workspace_name}-${yesterday}.md"
parent_path="会议纪要内容/日报周报内容/${yesterday}"

curl -X POST "${api_url}" \
  -H "Authorization: Bearer ${auth_token}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${file_name}\",
    \"parentPath\": \"${parent_path}\",
    \"content\": $(echo "$report_content" | jq -Rs .)
  }"

echo "✅ 日报已同步到 Javis 平台"
```

### 完整执行逻辑伪代码

```
function generate_daily_report():
    # 步骤1: 确定日期并检测昨天是否为周末
    yesterday = get_yesterday_date()
    yesterday_day_of_week = get_day_of_week(yesterday)  # 1=周一, 7=周日

    if yesterday_day_of_week > 5:  # 周六=6, 周日=7
        print("ℹ️ 昨天（${yesterday}）是周末，无需生成日报。")
        return

    # 步骤2 前置: 检测 claude-mem MCP Server 是否可用（最多重试3次，每次间隔1分钟）
    MAX_RETRIES = 3
    mcp_available = False
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            call_tool("mcp__plugin_claude-mem_mcp-search__search", {"query": "test", "limit": 1})
            mcp_available = True
            break
        except:
            if attempt < MAX_RETRIES:
                sleep(60)  # 等待1分钟后重试

    if not mcp_available:
        # 3次全部失败 → 生成包含提示信息的日报文件（不直接终止）
        report_content = f"""⚠️ 记忆系统不可用

当前空间未启用记忆系统（claude-mem），无法获取会话记录，日报内容无法自动生成。

💡 解决方法：请前往 **设置 → AI模型 → 记忆系统**，打开记忆系统开关并配置 claude-mem MCP Server，之后重新生成日报。

---
*统计日期: {yesterday}*
*状态: MCP Server 不可用（已重试 3 次）*"""
        save_report(report_content, file_name)
        sync_to_javis(report_content, file_name)
        return

    # 步骤2: 获取会话记录
    # ⚠️ 注意：dateEnd 必须比 dateStart 多1天
    sessions = call_skill("claude-mem:mem-search", {
        "dateStart": yesterday,
        "dateEnd": add_days(yesterday, 1),
        "limit": 100,
        "type": "sessions"
    })

    # 步骤3: 检查是否存在（sessions 为空则终止）
    if sessions is empty:
        print("ℹ️ ${yesterday} 无会话记录，不生成日报。")
        return

    # 步骤3.5: ⚠️ 过滤日报生成相关及交付实施类的会话（必须执行）
    sessions = filter_daily_report_sessions(sessions)

    # 过滤关键词：日报生成相关 + 交付/实施/上线/运维/项目管理/定制开发/测试类
    # sessions 检查 request/completed 字段

    if sessions is empty after filter:
        print("ℹ️ ${yesterday} 过滤日报会话后无有效工作记录，不生成日报。")
        print("💡 提示：昨日可能仅执行了日报生成任务，无其他工作内容。")
        return

    # 步骤4: 分析会话内容，生成工作总结
    # 4.1 按主题相似度聚合分组，避免流水账
    sessions = aggregate_by_topic(sessions)
    # 4.2 判断内容类型并生成总结
    if sessions are related to customer_progress:
        summary = generate_customer_progress_summary(sessions)
    else:
        summary = generate_general_work_summary(sessions)

    if summary is empty:
        print("ℹ️ ${yesterday} 会话内容无法生成有效总结，不生成日报。")
        return

    # 限制300字
    summary = truncate(summary, max_length=300)

    # 步骤5: 获取空间创建者信息（⚠️ 必须是创建者，不是执行用户！）
    workspace_info = call_javis_api("/workspaces/${JAVIS_WORKSPACE_ID}")
    creator_name = workspace_info.data.creator.name  # ← 空间创建者姓名
    workspace_name = workspace_info.data.name  # ← 空间名称

    # 调试输出
    print("📋 日报命名信息：")
    print(f"  - 空间创建者: {creator_name}")
    print(f"  - 空间名称: {workspace_name}")

    # 步骤6: 生成并保存日报（以实际会话日期命名）
    # ⚠️ 文件名格式：空间创建者-空间名称-日期.md
    file_name = f"{creator_name}-{workspace_name}-{yesterday}.md"
    report = generate_report(summary, yesterday, len(sessions))
    save_report(report, file_name)

    # 步骤7: 同步到 Javis
    sync_to_javis(report, file_name)

    print("✅ 日报生成完成")


function filter_daily_report_sessions(sessions):
    """过滤掉日报生成相关及交付实施类的会话"""
    filter_keywords = [
        "daily-report",
        "日报生成",
        "生成日报",
        "日报系统验证",
        "验证系统日期",
        "周末检测逻辑",
        "daily report",
        # --- 交付实施类 ---
        "交付文档", "交付验收", "项目交付", "交付物",
        "实施部署", "实施配置", "实施方案", "实施计划",
        "上线", "运维", "巡检", "故障处理",
        # --- 项目管理类 ---
        "甘特图", "项目计划", "里程碑", "排期",
        # --- 定制开发类 ---
        "定制化开发", "定制化需求", "调研清单", "开发任务",
        # --- 测试验证类 ---
        "性能测试", "专项测试", "测试计划", "测试用例", "UAT",
        # --- 文档迭代类 ---
        "文档格式统一", "发布管理",
    ]

    filter_patterns = [
        "交付.*验收", "实施.*方案", "实施.*部署", "实施.*配置", "实施.*迭代",
        "部署.*上线", "运维.*巡检", "定制化.*开发", "定制化.*需求",
        r"V\d+\.\d+.*V\d+\.\d+", r"V\d+\.\d+.*升级",
        "甘特图.*优化", "甘特图.*迭代", "文档格式.*统一", "调研清单", r"调研报告.*V\d",
    ]

    filtered_sessions = []
    for session in sessions:
        text = (session.request + " " + session.completed).lower()
        should_filter = any(kw.lower() in text for kw in filter_keywords)

        if not should_filter:
            import re
            for pattern in filter_patterns:
                if re.search(pattern, text):
                    should_filter = True
                    break

        if should_filter:
            print(f"  🚫 过滤: {session.request[:50]}...")
        else:
            filtered_sessions.append(session)

    return filtered_sessions
```

function aggregate_by_topic(sessions):
    """按主题相似度聚合会话，合并同一任务的多个操作步骤"""
    # 聚合依据：客户名称、项目名称、功能模块、工作类型
    # 同一主题的多条 session 合并为一个任务组
    # 每个任务组输出一条总结，子步骤作为补充说明嵌入
    return grouped_sessions  # 聚合后的任务组列表
```

## Output Format

### 成功输出

```markdown
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
✅ 找到 5 条原始会话记录
🔍 正在过滤日报生成相关会话...
  🚫 过滤: 日报系统验证：执行日报生成技能...
📊 过滤结果: 原始 5 条 → 过滤 1 条 → 保留 4 条
✅ 过滤后保留 4 条有效会话记录
📝 正在分析会话内容，生成客户推进总结...
📋 日报命名信息：
  - 空间创建者: 张三
  - 空间名称: 华能信息IT资产运维管理平台
  - 日报日期: 2026-04-02
✅ 日报已生成: /workspace/日报/张三-华能信息IT资产运维管理平台-2026-04-02.md
✅ 日报已同步到 Javis 平台

📊 统计摘要：
  - 统计日期: 2026-04-02
  - 原始会话: 5条
  - 过滤: 1条（日报生成相关）
  - 有效会话: 4条
  - 涉及客户: 3个
```

### 周末终止

```markdown
ℹ️ 昨天（2026-04-05）是周末，无需生成日报。
```

### 无会话记录（终止）

```markdown
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
ℹ️ 昨日（2026-04-02）无会话记录，不生成日报。

💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。
```

### 过滤后无有效会话（终止）

```markdown
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
✅ 找到 3 条原始会话记录
🔍 正在过滤日报生成相关会话...
  🚫 过滤: 日报系统验证：执行日报生成技能...
  🚫 过滤: 生成日报：为销售工作空间生成工作日报...
  🚫 过滤: daily-report 执行：验证日期计算逻辑...
📊 过滤结果: 原始 3 条 → 过滤 3 条 → 保留 0 条
ℹ️ 昨日（2026-04-02）过滤日报会话后无有效工作记录，不生成日报。

💡 提示：昨日可能仅执行了日报生成任务，无其他工作内容。
```

## Best Practices

### 客户推进总结写作规范

**DO（推荐做法）**：

* ✅ 聚焦客户推进相关的工作

* ✅ 使用动词开头：完成、推进、分析、生成、拜访

* ✅ 量化成果：匹配N个案例、分析N条需求、得分N分

* ✅ 关联项目名称

* ✅ 控制在300字以内

**DON'T（避免做法）**：

* ❌ 超过300字

* ❌ 生成没有实质内容的日报

* ❌ 因会话内容与客户推进无关而跳过（只要有会话就应生成日报）

* ❌ 过于详细的技术实现描述

### 会话分析与过滤

**⚠️ 首先过滤无效会话**（必须执行）：

在分析会话内容之前，**必须先过滤掉**以下类型的无效会话：

* 执行 `daily-report` skill 的会话
* 日报系统验证、测试相关的会话
* 包含"日报生成"、"生成日报"关键词的会话
* 包含"交付"、"实施"、"上线"、"运维"、"甘特图"、"定制化开发"、"测试计划"等关键词的售后阶段会话

**过滤关键词列表**：

| 关键词 | 说明 |
| -------------- | ------ |
| `daily-report` | 技能名称 |
| `日报生成` | 中文技能名 |
| `生成日报` | 动作描述 |
| `日报系统验证` | 系统验证任务 |
| `验证系统日期` | 系统验证任务 |
| `周末检测逻辑` | 系统验证任务 |
| `daily report` | 英文关键词 |
| `交付文档/验收/交付物` | 售后交付阶段 |
| `实施部署/配置/方案/计划` | 售后实施阶段 |
| `上线/运维/巡检/故障处理` | 售后运维阶段 |
| `甘特图/项目计划/里程碑/排期` | 项目管理阶段 |
| `定制化开发/定制化需求/调研清单` | 售后定制开发 |
| `性能测试/专项测试/测试计划/UAT` | 售后测试验证 |

**保留的会话类型**（客户推进相关）：

* 客户调研、企业分析

* 案例匹配、需求分析

* 方案生成、话术准备

* 会议分析、销售准备

* 投标分析、控标策略

**保留的会话类型**（非客户推进，但记录工作内容）：

* Plugin/Skill 开发与调试

* 工具搭建、环境配置

* 内部流程优化

* 文档编写

**终止条件**：

* 昨天是周末（周六或周日）

* 完全无会话记录

* ⚠️ **过滤日报相关会话后无有效会话**（如昨日仅执行了日报生成任务）

**⚠️ 重要**：过滤无效会话是必须执行的步骤，不能跳过。如果跳过，日报内容将变成"日报系统验证"或"实施方案迭代"等售后阶段内容，偏离售前销售日报定位。

## Examples

### 示例1：正常日报生成

**输入**：

```
用户：生成今天的日报
```

**系统执行**：

1. 确定昨天日期：2026-04-02
2. 检测昨天星期几：周四（4），是工作日
3. 调用 claude-mem 获取5条会话记录
4. 分析会话，提取3个客户的推进工作
5. 生成300字以内的总结
6. 保存并同步

**输出**：

```markdown
# 工作日报 - 2026-04-02

## 客户推进总结

1. **招商银行-CMDB项目**：完成企业调研，识别客户为金融行业城商行；匹配8个金融案例；生成销售话术。

2. **国家电网-监控平台**：分析招标评分表，预估得分82分，识别2个风险项，输出控标建议。

3. **中国移动-ITSM项目**：分析会议纪要，识别痛点，判断销售阶段，生成推进建议。

---
*统计日期: 2026-04-02*
*会话数: 5条*
```

### 示例2：周六生成周五日报

**输入**：

```
用户：生成今天的日报
```

**场景**：今天是周六（2026-04-04），昨天是周五（2026-04-03）

**系统执行**：

1. 确定昨天日期：2026-04-03
2. 检测昨天星期几：周五（5），是工作日
3. 调用 claude-mem 获取周五的会话记录
4. 分析会话，生成日报

**输出**：

```markdown
📅 正在生成 2026-04-03 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-03 的会话记录...
✅ 找到 3 条会话记录
✅ 日报已生成: /workspace/日报/黄星玲-销售工作空间-2026-04-03.md
```

### 示例3：周日终止（昨天周六是周末）

**输入**：

```
用户：生成今天的日报
```

**场景**：今天是周日（2026-04-05），昨天是周六（2026-04-04）

**系统执行**：

1. 确定昨天日期：2026-04-04
2. 检测昨天星期几：周六（6），是周末
3. 终止，不生成日报

**输出**：

```
ℹ️ 昨天（2026-04-04）是周末，无需生成日报。
```

### 示例4：周一终止（昨天周日是周末）

**输入**：

```
用户：生成今天的日报
```

**场景**：今天是周一（2026-04-06），昨天是周日（2026-04-05）

**系统执行**：

1. 确定昨天日期：2026-04-05
2. 检测昨天星期几：周日（7），是周末
3. 终止，不生成日报

**输出**：

```
ℹ️ 昨天（2026-04-05）是周末，无需生成日报。
```

### 示例5：无会话记录

**输入**：

```
用户：生成今天的日报
```

**场景**：昨天是工作日但没有使用 Agent

**输出**：

```
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
ℹ️ 昨日（2026-04-02）无会话记录，不生成日报。

💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。
```

***

## Version

**版本**: 4.14.0
**最后更新**: 2026-05-15

| 版本 | 日期 | 说明 |
|------|------|------|
| v4.14 | 2026-05-15 | 步骤 3.5 新增交付实施类会话过滤规则，排除售后阶段工作（交付/实施/上线/运维/项目管理/定制开发/测试验证/文档迭代） |
| v4.13 | 2026-04-24 | 步骤 4 新增会话聚合分组逻辑和聚合写作规范，避免流水账式日报 |
| v4.12 | 2026-04-24 | 移除 observations 数据源，回归 sessions 单一数据源，降低复杂度 |
| v4.11 | 2026-04-18 | 新增 observations 作为补充数据源，sessions 为空时也能生成日报 |
| v4.10 | 2026-04-18 | 增强 MCP Server 可用性检测，支持 3 次重试和降级生成提示日报 |
| v4.9 | 2026-04-18 | 新增 claude-mem MCP Server 可用性前置检查，未配置时生成提示文件 |
| v4.8 | 2026-04-18 | 修复 mem-search 缺少 project 参数导致跨空间数据泄露的问题 |
| v4.7 | 2026-04-08 | 日报同步路径改为按日期动态归档 |
| v4.6 | 2026-04-08 | 获取空间创建者信息新增 5 次重试机制，失败时降级为"未知用户" |
| v4.5 | 2026-04-08 | 修复日报文件命名错误使用执行用户而非空间创建者的问题 |
| v4.4 | 2026-04-08 | 新增日报生成相关会话过滤逻辑，防止日报内容包含无效系统记录 |
| v4.3 | 2026-04-04 | 修复 dateEnd 参数错误导致 API 返回空结果的问题 |
| v4.2 | 2026-04-04 | 修复周末检测逻辑，改为检测昨天而非今天的星期几 |
| v4.1 | 2026-04-04 | 移除硬编码周末拦截，改为基于会话内容自然判断 |
| v4.0 | 2026-04-03 | 重构为会话驱动模式，通过 claude-mem 获取会话记录生成日报 |
| v3.0 | 2026-03-05 | 改为文件系统扫描模式 |
| v2.0 | 2026-03-01 | 新增会话轨迹优先策略 |
| v1.0 | 2026-02-20 | 初始版本 |

**依赖**:

* claude-mem:mem-search（获取会话记录）

* Javis API（获取用户信息、同步日报）
