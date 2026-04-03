---
name: daily-report
description: 日报生成技能，通过claude-mem获取前一天会话记录，智能总结成面向客户推进方向的工作日报（不超过300字）
category: productivity
priority: medium
---

# Daily Report (日报生成技能)

## Purpose

为销售和项目团队提供自动化的日报生成能力，基于 claude-mem 记录的前一天会话内容，智能总结成面向客户推进方向的工作日报。

**核心功能**:
- 通过 claude-mem 获取前一天的工作会话记录
- 智能分析会话内容，提取客户推进相关的工作事项
- 生成简洁的工作总结（不超过300字）
- 面向客户推进方向，突出销售进展和价值
- 自动保存并同步到 Javis 平台

**核心优势**:
- ✅ **会话驱动**：基于真实的会话记录，反映实际工作内容
- ✅ **客户导向**：总结聚焦于客户推进方向，而非技术细节
- ✅ **简洁高效**：300字以内，快速阅读
- ✅ **智能终止**：无会话记录时自动终止，不生成空日报

## When to Use

在以下情况下使用此技能：
- 每天工作结束时需要生成日报
- 需要快速汇总当天的客户推进工作
- 需要向上级或团队汇报当天进展
- 用户说"生成日报"、"今天的日报"、"写日报"等

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| date | string | ❌ | 昨天 | 日报统计日期，格式：YYYY-MM-DD，默认为昨天 |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位专业的销售工作日报助手，擅长从会话记录中提取客户推进相关的工作事项，生成简洁清晰的工作汇报。

**核心原则**：
1. **客户导向**：只记录与客户推进相关的工作内容
2. **简洁性优先**：总结不超过300字
3. **结果导向**：关注客户进展和推进成果
4. **无会话即终止**：没有会话记录时不生成日报

### 执行流程

#### 步骤 1: 确定日期

```bash
# 计算前一天的日期（日报统计的是前一天的工作）
yesterday=$(date -d "yesterday" +%Y-%m-%d)

# 检查是否为工作日（周一到周五）
day_of_week=$(date +%u)  # 1=周一, 7=周日
if [ "$day_of_week" -gt 5 ]; then
    echo "ℹ️ 今天是周末，无需生成日报。"
    exit 0
fi

echo "📅 正在生成 ${yesterday} 的工作日报..."
```

#### 步骤 2: 获取前一天会话记录

**使用 claude-mem 的 search 工具获取会话记录**：

```bash
# 调用 claude-mem search 获取前一天的会话
# dateStart 和 dateEnd 设置为同一天（昨天）
echo "🔍 正在从 claude-mem 获取 ${yesterday} 的会话记录..."

# 使用 Skill 工具调用 claude-mem:mem-search
# 参数：
# - query: 畺空或使用通配符，获取所有记录
# - dateStart: ${yesterday}
# - dateEnd: ${yesterday}
# - limit: 100
# - type: sessions（只获取会话）
```

**调用示例**：
```json
{
  "skill": "claude-mem:mem-search",
  "args": {
    "query": "",
    "dateStart": "2026-04-02",
    "dateEnd": "2026-04-02",
    "limit": 100,
    "type": "sessions"
  }
}
```

#### 步骤 3: 检查会话记录是否存在

**如果没有任何会话记录，直接终止任务**：

```markdown
# 检查结果
if [ ${#sessions} -eq 0 ]; then
    echo "ℹ️ 昨日（${yesterday}）无会话记录，不生成日报。"
    echo ""
    echo "💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。"
    exit 0
fi

echo "✅ 找到 ${#sessions} 条会话记录"
```

**终止条件**：
- claude-mem 返回空结果
- 返回的会话数量为 0
- 所有会话都与客户推进无关（如纯技术调试）

#### 步骤 4: 分析会话内容，生成客户推进总结

**分析维度**：

从会话记录中提取以下客户推进相关信息：
1. **客户名称**：涉及哪些客户
2. **项目进展**：项目推进到什么阶段
3. **关键动作**：做了哪些推进动作（调研、分析、方案、会议等）
4. **阶段性成果**：取得了什么进展或成果
5. **下一步计划**：接下来要做什么

**总结模板（面向客户推进）**：

```markdown
# 工作日报 - {日期}

## 客户推进总结

{不超过300字的客户推进工作总结，聚焦于：}
{- 拜访/跟进的客户}
{- 完成的分析/方案工作}
{- 项目阶段性进展}
{- 关键成果或突破}

---
*统计日期: {日期}*
*会话数: {N}条*
```

**总结写作规范**：

1. **聚焦客户**：每句话都与客户推进相关
2. **动词开头**：使用"完成"、"推进"、"分析"、"生成"等动词
3. **量化成果**：尽可能用数字说话（"匹配5个案例"、"分析20条需求"）
4. **简洁明了**：每项工作1句话，总计不超过300字
5. **不记录技术细节**：不记录代码调试、环境配置等技术工作

**示例总结**：

```markdown
# 工作日报 - 2026-04-02

## 客户推进总结

1. **招商银行-CMDB项目**：完成企业调研，识别客户为金融行业城商行，IT规模约500人；匹配8个金融行业案例；生成针对性销售话术。

2. **国家电网-监控平台项目**：分析招标商务评分表，预估得分82分，识别2个风险项（资质缺失），输出控标建议3条。

3. **中国移动-ITSM项目**：分析会议纪要，识别客户痛点为"流程效率低、工单处理慢"，判断销售阶段为"需求探索期"，生成下一步推进建议。

---
*统计日期: 2026-04-02*
*会话数: 5条*
```

#### 步骤 5: 获取用户信息并保存日报

```bash
# 获取空间创建者姓名和空间名称
workspace_id="${JAVIS_WORKSPACE_ID}"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${workspace_id}"

# 通过API获取创建者姓名
creator_name=$(curl -s -H "Authorization: Bearer ${auth_token}" "${api_url}" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['data']['creator']['name'])" 2>/dev/null)

if [ -z "$creator_name" ]; then
    creator_name="未知用户"
fi

workspace_name="${JAVIS_WORKSPACE_NAME:-未知空间}"

# 创建日报目录
mkdir -p /workspace/日报

# 保存日报到本地
output_file="/workspace/日报/${creator_name}-${workspace_name}-${yesterday}.md"
echo "$report_content" > "$output_file"
echo "✅ 日报已生成: $output_file"
```

#### 步骤 6: 同步到 Javis 平台（可选）

```bash
# 同步到 Javis 平台
daily_report_workspace_id="cmm8se74z049g30s5eeazl02d"
auth_token="${JAVIS_AUTH_TOKEN}"
api_url="https://javis.elevo.vip/api/v1/workspaces/${daily_report_workspace_id}/files/text-file"

file_name="${creator_name}-${workspace_name}-${yesterday}.md"
parent_path="会议纪要内容/日报周报内容"

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
    # 步骤1: 确定日期
    yesterday = get_yesterday_date()

    # 步骤2: 获取会话记录
    sessions = call_skill("claude-mem:mem-search", {
        "dateStart": yesterday,
        "dateEnd": yesterday,
        "limit": 100,
        "type": "sessions"
    })

    # 步骤3: 检查会话是否存在
    if sessions is empty:
        print("ℹ️ 昨日（${yesterday}）无会话记录，不生成日报。")
        return  # 直接终止，不生成任何文件

    # 步骤4: 分析会话，生成客户推进总结
    summary = analyze_sessions_for_customer_progress(sessions)

    if summary is empty or not related_to_customer:
        print("ℹ️ 昨日会话与客户推进无关，不生成日报。")
        return

    # 限制300字
    summary = truncate(summary, max_length=300)

    # 步骤5: 获取用户信息
    user_info = get_user_info_from_javis()

    # 步骤6: 生成并保存日报
    report = generate_report(summary, yesterday, len(sessions))
    save_report(report, user_info)

    # 步骤7: 同步到 Javis
    sync_to_javis(report, user_info)

    print("✅ 日报生成完成")
```

## Output Format

### 成功输出

```markdown
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
✅ 找到 5 条会话记录
📝 正在分析会话内容，生成客户推进总结...
✅ 日报已生成: /workspace/日报/黄星玲-销售工作空间-2026-04-02.md
✅ 日报已同步到 Javis 平台

📊 统计摘要：
  - 统计日期: 2026-04-02
  - 会话数: 5条
  - 涉及客户: 3个
```

### 无会话记录（终止）

```markdown
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
ℹ️ 昨日（2026-04-02）无会话记录，不生成日报。

💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。
```

### 周末（终止）

```markdown
ℹ️ 今天是周末，无需生成日报。
```

## Best Practices

### 客户推进总结写作规范

**DO（推荐做法）**：
- ✅ 聚焦客户推进相关的工作
- ✅ 使用动词开头：完成、推进、分析、生成、拜访
- ✅ 量化成果：匹配N个案例、分析N条需求、得分N分
- ✅ 关联项目名称
- ✅ 控制在300字以内

**DON'T（避免做法）**：
- ❌ 记录纯技术工作（代码调试、环境配置）
- ❌ 记录内部工具使用（除非与客户直接相关）
- ❌ 过于详细的流程描述
- ❌ 超过300字
- ❌ 生成没有实质内容的日报

### 会话分析与过滤

**保留的会话类型**：
- 客户调研、企业分析
- 案例匹配、需求分析
- 方案生成、话术准备
- 会议分析、销售准备
- 投标分析、控标策略

**过滤的会话类型**：
- 纯代码开发、调试
- 环境配置、工具安装
- 与客户无关的技术讨论
- 内部测试、实验

## Examples

### 示例1：正常日报生成

**输入**：
```
用户：生成今天的日报
```

**系统执行**：
1. 确定昨天日期：2026-04-02
2. 调用 claude-mem 获取5条会话记录
3. 分析会话，提取3个客户的推进工作
4. 生成300字以内的总结
5. 保存并同步

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

### 示例2：无会话记录

**输入**：
```
用户：生成今天的日报
```

**场景**：昨天没有使用 Agent

**输出**：
```
📅 正在生成 2026-04-02 的工作日报...
🔍 正在从 claude-mem 获取 2026-04-02 的会话记录...
ℹ️ 昨日（2026-04-02）无会话记录，不生成日报。

💡 提示：日报基于会话记录生成，请在工作日使用 Agent 进行工作。
```

### 示例3：周末

**输入**：
```
用户：生成今天的日报
```

**场景**：今天是周六

**输出**：
```
ℹ️ 今天是周末，无需生成日报。
```

---

## Version

**版本**: 4.0.0
**最后更新**: 2026-04-03
**更新内容**:
- **v4.0 (2026-04-03) - 会话驱动模式**:
  - ✅ 移除文件扫描逻辑，改用 claude-mem 获取会话记录
  - ✅ 日报内容改为面向客户推进方向的总结
  - ✅ 限制总结不超过300字
  - ✅ 无会话记录时直接终止，不生成日报
  - ✅ 新增会话分析与过滤逻辑
- v3.0 (2026-03-05): 从会话分析改为文件系统扫描
- v2.0 (2026-03-01): 新增会话轨迹优先策略
- v1.0 (2026-02-20): 初始版本

**依赖**:
- claude-mem:mem-search（获取会话记录）
- Javis API（获取用户信息、同步日报）
