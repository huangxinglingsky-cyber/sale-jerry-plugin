# Context 目录说明

## 目的

Context 目录用于存储 Agent 的执行上下文和记忆，使多个 Agent 能够：
- **保留执行记忆**：记录已完成的任务、生成的数据、关键决策
- **协作共享**：不同 Agent 之间共享上下文信息
- **持久化状态**：保存中间结果，支持断点续传
- **知识积累**：积累企业调研、案例匹配、销售话术等可复用信息

## 目录结构

```
context/
├── README.md                           # 本说明文件
├── sessions/                           # 会话记忆
│   ├── {session_id}.json              # 单次会话的完整上下文
│   └── active_session.json            # 当前活跃会话
├── companies/                          # 企业调研缓存
│   ├── {company_name}/
│   │   ├── basic_info.json            # 基本信息
│   │   ├── research_report.md         # 调研报告
│   │   └── last_updated.txt           # 更新时间
├── cases/                              # 案例匹配缓存
│   ├── {industry}_{module}.json       # 按行业和模块缓存匹配结果
│   └── index.json                     # 案例索引
├── scripts/                            # 销售话术缓存
│   ├── {scenario}_{company}.md        # 按场景和公司缓存话术
│   └── templates/                     # 话术模板
└── shared/                             # 共享数据
    ├── agent_state.json               # Agent 状态
    └── workflow_history.json          # 工作流历史
```

## 使用方式

### 1. 会话记忆 (sessions/)

**用途**：记录完整的会话上下文，支持多轮对话和断点续传

**格式示例**：
```json
{
  "session_id": "sess_20260106_001",
  "created_at": "2026-01-06T10:30:00Z",
  "last_updated": "2026-01-06T10:45:00Z",
  "agent_type": "sales-prep",
  "status": "in_progress",
  "context": {
    "company_name": "长沙银行",
    "module": "CMDB",
    "year_filter": "2024",
    "completed_steps": [
      "task_confirmation",
      "company_research",
      "case_matching"
    ],
    "next_step": "script_generation",
    "intermediate_results": {
      "research_report_path": "context/companies/长沙银行/research_report.md",
      "matched_cases": [
        {"customer": "中国光大银行", "amount": "399万", "date": "2024-10"},
        {"customer": "吉林银行", "amount": "73万", "date": "2024-09"}
      ]
    }
  }
}
```

### 2. 企业调研缓存 (companies/)

**用途**：避免重复调研同一企业，提高效率

**格式示例**：
```json
{
  "company_name": "长沙银行",
  "industry": "金融-银行",
  "basic_info": {
    "full_name": "长沙银行股份有限公司",
    "founded_year": 1997,
    "registered_capital": "XX亿元",
    "status": "上市公司"
  },
  "it_info": {
    "team_size": "1200+",
    "tech_stack": ["虚拟化", "Linux", "MySQL", "国产数据库"],
    "digitalization_level": "高度数字化"
  },
  "last_updated": "2026-01-06",
  "data_sources": [
    "企查查",
    "政府采购网",
    "BOSS直聘"
  ]
}
```

### 3. 案例匹配缓存 (cases/)

**用途**：缓存常用的案例匹配结果，加速查询

**格式示例**：
```json
{
  "industry": "金融-银行",
  "module": "CMDB",
  "year_filter": "2024",
  "matched_cases": [
    {
      "customer": "中国光大银行",
      "module": "CMDB+自动化+低代码",
      "contract_name": "全栈云运营数据治理专项项目服务合同",
      "amount": "399万",
      "date": "2024-10"
    }
  ],
  "total_count": 7,
  "price_range": {
    "min": "20万",
    "max": "399万",
    "median": "73万"
  },
  "last_updated": "2026-01-06"
}
```

### 4. 销售话术缓存 (scripts/)

**用途**：缓存生成的销售话术，支持修改和复用

**文件命名**：`{scenario}_{company}.md`

**示例**：`运维部门初访_长沙银行.md`

### 5. 共享数据 (shared/)

**agent_state.json** - Agent 状态跟踪：
```json
{
  "sales-prep": {
    "last_execution": "2026-01-06T10:45:00Z",
    "total_executions": 15,
    "success_rate": 0.93,
    "avg_duration_seconds": 120
  },
  "company-research": {
    "cached_companies": 25,
    "last_update": "2026-01-06"
  }
}
```

**workflow_history.json** - 工作流历史：
```json
{
  "workflows": [
    {
      "id": "wf_20260106_001",
      "type": "sales-prep",
      "company": "长沙银行",
      "status": "completed",
      "duration_seconds": 118,
      "steps": [
        {"step": "company_research", "duration": 45, "status": "success"},
        {"step": "case_matching", "duration": 12, "status": "success"},
        {"step": "script_generation", "duration": 61, "status": "success"}
      ],
      "output_path": "report/销售准备包-长沙银行-2026-01-06.md"
    }
  ]
}
```

## Agent 协作机制

### 协作流程

1. **sales-prep agent** 启动：
   - 检查 `context/sessions/active_session.json` 是否有活跃会话
   - 如有，读取上下文继续执行；如无，创建新会话

2. **company-research** 执行：
   - 先检查 `context/companies/{company_name}/` 是否有缓存
   - 如有且未过期（7天内），直接使用缓存
   - 如无或已过期，执行新调研并更新缓存

3. **case-matching** 执行：
   - 先检查 `context/cases/{industry}_{module}.json` 是否有缓存
   - 根据时间筛选条件返回结果

4. **script-generation** 执行：
   - 检查 `context/scripts/{scenario}_{company}.md` 是否有缓存
   - 如有，询问是否复用或重新生成

5. **完成时**：
   - 更新 `shared/agent_state.json`
   - 记录到 `shared/workflow_history.json`
   - 清理或归档会话记录

### 协作示例

**场景**：用户连续为多个银行生成 CMDB 销售资料

```
用户输入1: "广州银行 CMDB 相关案例只列出2024年的"
→ sales-prep agent 执行
→ 缓存: context/cases/金融-银行_CMDB_2024.json
→ 输出报告

用户输入2: "深圳银行 CMDB 相关案例只列出2024年的"
→ sales-prep agent 执行
→ **复用缓存**: 直接读取 context/cases/金融-银行_CMDB_2024.json
→ 只需调研深圳银行，节省90%的案例匹配时间
→ 输出报告
```

## 缓存策略

### 缓存有效期

| 数据类型 | 有效期 | 说明 |
|---------|--------|------|
| 企业基本信息 | 30天 | 工商信息变化慢 |
| IT与运维信息 | 7天 | 招聘、技术栈变化较快 |
| 招投标信息 | 3天 | 实时性要求高 |
| 案例匹配结果 | 永久 | 案例库更新时重新匹配 |
| 销售话术 | 永久 | 可手动修改和复用 |

### 缓存失效策略

- **时间失效**：超过有效期自动失效
- **手动失效**：用户明确要求重新生成
- **版本失效**：案例库更新后，案例匹配缓存失效

## 数据安全

### 敏感信息处理

- **不缓存**：客户的联系方式、内部价格、商业机密
- **加密存储**：如需缓存敏感信息，使用加密
- **定期清理**：会话记录保留30天后自动清理

### 访问控制

- Context 目录仅 Agent 可读写
- 用户通过 Agent 接口间接访问
- 支持导出和备份

## 维护与监控

### 定期维护任务

1. **每天**：清理失效缓存
2. **每周**：归档历史会话
3. **每月**：统计 Agent 性能，优化缓存策略

### 监控指标

- 缓存命中率
- Agent 执行成功率
- 平均执行时间
- 存储空间使用

---

**版本**: 1.0
**创建日期**: 2026-01-06
**维护者**: AI Solutions Expert Team
