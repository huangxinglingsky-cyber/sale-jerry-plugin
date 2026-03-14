# Context 使用示例

## 示例 1：基础使用 - 单次销售准备

### 场景
用户请求：为"广州银行 CMDB"准备销售资料

### Agent 执行流程

1. **创建会话**
```json
// context/sessions/sess_20260106_001.json
{
  "session_id": "sess_20260106_001",
  "created_at": "2026-01-06T14:30:00Z",
  "agent_type": "sales-prep",
  "status": "in_progress",
  "context": {
    "company_name": "广州银行",
    "module": "CMDB",
    "completed_steps": [],
    "next_step": "company_research"
  }
}
```

2. **执行企业调研**
```json
// context/companies/广州银行/basic_info.json
{
  "company_name": "广州银行",
  "industry": "金融-银行",
  "basic_info": {
    "full_name": "广州银行股份有限公司",
    "founded_year": 1996
  },
  "last_updated": "2026-01-06"
}
```

更新会话：
```json
{
  "completed_steps": ["company_research"],
  "next_step": "case_matching",
  "intermediate_results": {
    "company_cache_path": "context/companies/广州银行/"
  }
}
```

3. **案例匹配**
```json
// context/cases/金融-银行_CMDB.json
{
  "industry": "金融-银行",
  "module": "CMDB",
  "matched_cases": [...],
  "total_count": 16,
  "last_updated": "2026-01-06"
}
```

更新会话：
```json
{
  "completed_steps": ["company_research", "case_matching"],
  "next_step": "script_generation",
  "intermediate_results": {
    "company_cache_path": "context/companies/广州银行/",
    "matched_cases_count": 16
  }
}
```

4. **话术生成**
```markdown
// context/scripts/运维部门初访_广州银行.md
# 销售话术：广州银行 CMDB 项目
...
```

更新会话：
```json
{
  "completed_steps": ["company_research", "case_matching", "script_generation"],
  "status": "completed"
}
```

5. **记录工作流历史**
```json
// context/shared/workflow_history.json
{
  "workflows": [
    {
      "id": "wf_20260106_001",
      "type": "sales-prep",
      "company": "广州银行",
      "status": "completed",
      "duration_seconds": 125,
      "steps": [
        {"step": "company_research", "duration": 48, "status": "success"},
        {"step": "case_matching", "duration": 15, "status": "success"},
        {"step": "script_generation", "duration": 62, "status": "success"}
      ],
      "output_path": "report/销售准备包-广州银行-2026-01-06.md"
    }
  ]
}
```

---

## 示例 2：缓存复用 - 连续处理多个银行

### 场景
用户连续请求：
1. "广州银行 CMDB 相关案例只列出2024年的"
2. "深圳银行 CMDB 相关案例只列出2024年的"
3. "上海银行 CMDB 相关案例只列出2024年的"

### 执行流程

#### 第一次请求（广州银行）

1. **案例匹配** - 无缓存，执行匹配
```json
// context/cases/金融-银行_CMDB_2024.json
{
  "industry": "金融-银行",
  "module": "CMDB",
  "year_filter": "2024",
  "matched_cases": [
    {"customer": "中国光大银行", "amount": "399万", "date": "2024-10"},
    {"customer": "吉林银行", "amount": "73万", "date": "2024-09"},
    ...
  ],
  "total_count": 7,
  "last_updated": "2026-01-06T14:30:00Z"
}
```

**耗时**：15秒

#### 第二次请求（深圳银行）

1. **案例匹配** - **命中缓存**，直接读取
```json
// 直接读取 context/cases/金融-银行_CMDB_2024.json
```

**耗时**：0.5秒（节省97%时间）

#### 第三次请求（上海银行）

1. **案例匹配** - **命中缓存**，直接读取

**耗时**：0.5秒（节省97%时间）

### 缓存统计

```json
// context/cases/index.json 更新
{
  "indexes": [
    {
      "key": "金融-银行_CMDB_2024",
      "hit_count": 2,
      "created_at": "2026-01-06T14:30:00Z",
      "last_hit": "2026-01-06T14:50:00Z"
    }
  ],
  "total_cached": 1,
  "cache_hit_rate": 0.67  // 3次请求，2次命中
}
```

---

## 示例 3：断点续传 - 处理中断

### 场景
用户请求为"中国银行 CMDB"准备资料，但在话术生成环节中断

### 执行流程

#### 初次执行（中断前）

```json
// context/sessions/active_session.json
{
  "session_id": "sess_20260106_002",
  "created_at": "2026-01-06T15:00:00Z",
  "last_updated": "2026-01-06T15:02:30Z",
  "agent_type": "sales-prep",
  "status": "in_progress",
  "context": {
    "company_name": "中国银行",
    "module": "CMDB",
    "completed_steps": ["company_research", "case_matching"],
    "next_step": "script_generation",
    "intermediate_results": {
      "company_cache_path": "context/companies/中国银行/",
      "matched_cases_count": 16,
      "research_report_path": "context/companies/中国银行/research_report.md"
    }
  }
}
```

**中断原因**：网络超时 / 用户手动停止

#### 恢复执行

用户再次请求："继续为中国银行准备资料"

Agent 检测到 `active_session.json`：
1. 读取会话上下文
2. 识别已完成步骤：`company_research`, `case_matching`
3. 直接从 `script_generation` 继续执行
4. 复用已缓存的企业调研和案例匹配结果

**优势**：
- 节省时间：无需重新调研和匹配案例
- 保证一致性：使用相同的中间结果
- 用户体验好：无缝续传

---

## 示例 4：多 Agent 协作

### 场景
使用多个 Agent 协同完成销售准备

### 协作流程

#### Step 1: company-research agent 独立执行

```bash
用户：请调研"华为技术有限公司"
```

**company-research agent** 执行：
```json
// context/companies/华为技术有限公司/basic_info.json
{
  "company_name": "华为技术有限公司",
  "industry": "制造-电子通信",
  "basic_info": {...},
  "last_updated": "2026-01-06"
}
```

#### Step 2: sales-script agent 独立执行

```bash
用户：为华为生成运维部门初访话术
```

**sales-script agent** 执行：
1. 检查 `context/companies/华为技术有限公司/` - **存在缓存**
2. 直接读取企业信息
3. 生成话术

```markdown
// context/scripts/运维部门初访_华为技术有限公司.md
...
```

#### Step 3: sales-prep agent 整合

```bash
用户：为华为 CMDB 准备完整销售资料
```

**sales-prep agent** 执行：
1. 检查 `context/companies/华为技术有限公司/` - **存在缓存**，跳过企业调研
2. 执行案例匹配
3. 检查 `context/scripts/运维部门初访_华为技术有限公司.md` - **存在缓存**
4. 询问用户是否复用话术或重新生成
5. 整合生成最终报告

**协作优势**：
- 各 Agent 独立工作，结果互相复用
- 避免重复劳动
- 支持渐进式准备（先调研，后话术，最后整合）

---

## 示例 5：缓存失效与更新

### 场景
案例库更新后，自动失效相关缓存

### 操作流程

#### 案例库更新

```bash
运维人员：更新 skills/company-research/resource/data/caseLibrary.md
添加了 10 个新案例（2024年第四季度）
```

#### 缓存失效检测

系统自动检测案例库文件变更：
```json
// context/cases/index.json 更新
{
  "case_library_version": "v2.1",  // 从 v2.0 更新到 v2.1
  "last_case_library_update": "2026-01-06T16:00:00Z",
  "invalidated_caches": [
    "金融-银行_CMDB_2024",
    "金融-证券_自动化运维",
    ...
  ]
}
```

#### 下次请求自动重建

```bash
用户：为北京银行 CMDB 准备销售资料（2024年案例）
```

Agent 执行：
1. 检查 `context/cases/金融-银行_CMDB_2024.json`
2. 发现缓存已失效（案例库版本不匹配）
3. 自动重新匹配案例（使用最新的案例库）
4. 更新缓存

**结果**：
- 自动获取最新案例
- 无需手动清理缓存
- 保证数据时效性

---

## 最佳实践

### 1. 定期维护

```bash
# 每周执行一次缓存清理
cd d:\workspace\pulgins\sale-1.0.0\context
python scripts/cleanup_expired_cache.py
```

### 2. 监控缓存命中率

```json
// context/shared/agent_state.json
{
  "sales-prep": {
    "cache_hit_rate": 0.75,  // 75% 命中率
    "avg_time_with_cache": 45,
    "avg_time_without_cache": 120
  }
}
```

### 3. 备份重要缓存

```bash
# 备份企业调研缓存（重要客户）
cp -r context/companies/重要客户名 backups/
```

### 4. 清理敏感信息

```bash
# 删除特定公司的缓存
rm -rf context/companies/敏感公司名/
```

---

**版本**: 1.0
**创建日期**: 2026-01-06
**维护者**: AI Solutions Expert Team
