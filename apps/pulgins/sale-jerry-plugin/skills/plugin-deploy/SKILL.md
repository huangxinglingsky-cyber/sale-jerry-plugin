---
name: plugin-deploy
description: Plugin 打包部署技能，将 Plugin 目录打包为 zip 压缩包并上传到服务器。当用户要求"打包插件"、"部署插件"、"上传插件"、"发布插件"时触发
category: development
priority: high
---

# Plugin Deploy (Plugin 打包部署技能)

## Purpose

将 Plugin 目录打包为 zip 压缩包，并通过 API 上传到服务器，实现 Plugin 的快速部署。

**核心功能**:
- 自动打包指定 Plugin 目录为 zip 压缩包
- 通过 API 上传到服务器
- 使用 Bearer Token 认证
- 支持自定义 Plugin ID 和目录路径

**核心价值**:
- 一键打包部署，简化发布流程
- 自动化认证，无需手动处理 Token
- 清晰的执行反馈，便于问题排查

## When to Use

在以下情况下使用此技能：
- 开发完成后需要部署 Plugin 到服务器
- 需要更新服务器上的 Plugin 版本
- 用户要求"打包插件"、"部署插件"、"上传插件"、"发布插件"

## Capabilities

### 1. 目录打包

将指定的 Plugin 目录打包为 zip 压缩包：
- 使用 Python zipfile 模块打包（兼容性更好）
- 排除 `.git` 目录、`__pycache__`、`.pyc` 文件
- 生成的压缩包名称：`{plugin_name}.zip`

### 2. API 上传

通过 REST API 上传压缩包：
- 接口：`PUT /api/v1/plugins/{plugin_id}/reupload`
- 认证：Bearer Token（从环境变量 `$JAVIS_AUTH_TOKEN` 获取）
- 参数：`stripFirstLevel=true`（去除压缩包根目录层级）
- 文件字段：`file`

### 3. 错误处理

完善的错误处理机制：
- 目录不存在检查
- Token 未设置检查
- API 调用失败处理
- 详细的错误信息输出

## Parameters

| 参数 | 类型 | 必须 | 默认值 | 描述 |
|------|------|------|--------|------|
| plugin_id | string | ❌ | cmk3oovu1002m4prviw8mqq21 | Plugin ID，用于 API 上传 |
| plugin_dir | string | ❌ | apps/pulgins/sale-jerry-plugin | Plugin 目录路径（相对于工作空间根目录） |
| output_dir | string | ❌ | /tmp | 压缩包输出目录 |
| skip_upload | boolean | ❌ | false | 是否跳过上传（仅打包） |

## Instructions

### 执行角色与核心原则

**你的角色定位**：
你是一位 Plugin 部署助手，负责将 Plugin 打包并上传到服务器。

**你的任务目标**：
快速、可靠地完成 Plugin 的打包和部署工作。

**核心原则**：
- 安全第一：妥善处理认证 Token
- 清晰反馈：每个步骤都有明确的执行结果反馈
- 错误处理：遇到问题立即停止并提示用户

### 执行步骤

#### 步骤 1: 参数验证

**1.1 检查环境变量**

验证必要的认证 Token：

```bash
if [ -z "$JAVIS_AUTH_TOKEN" ]; then
  echo "错误: JAVIS_AUTH_TOKEN 环境变量未设置"
  echo "请确保已正确配置认证环境变量"
  exit 1
fi
```

**1.2 检查 Plugin 目录**

验证 Plugin 目录是否存在：

```bash
PLUGIN_DIR="{plugin_dir}"

if [ ! -d "$PLUGIN_DIR" ]; then
  echo "错误: Plugin 目录不存在: $PLUGIN_DIR"
  exit 1
fi
```

#### 步骤 2: 打包 Plugin 目录

**2.1 确定压缩包名称和父目录**

从 Plugin 目录名称提取压缩包名称和父目录：

```bash
PLUGIN_DIR="{plugin_dir}"
PLUGIN_NAME=$(basename "$PLUGIN_DIR")
PLUGIN_PARENT=$(dirname "$PLUGIN_DIR")
ZIP_FILE="{output_dir}/${PLUGIN_NAME}.zip"
```

**2.2 执行打包（使用 Python）**

进入 Plugin 父目录后打包，确保压缩包内路径为 `sale-jerry-plugin/...`：

```bash
python3 << 'EOF'
import zipfile
import os

plugin_dir = "{plugin_dir}"
plugin_name = os.path.basename(plugin_dir)
plugin_parent = os.path.dirname(plugin_dir)
zip_file = "{output_dir}/" + plugin_name + ".zip"

# 删除旧的 zip 文件
if os.path.exists(zip_file):
    os.remove(zip_file)

# 切换到 Plugin 父目录
original_dir = os.getcwd()
os.chdir(plugin_parent)

file_count = 0
# 创建 zip 文件，打包时以 plugin_name 为根目录
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(plugin_name):
        # 排除 .git 目录
        if '.git' in root:
            continue
        # 排除 __pycache__ 目录
        if '__pycache__' in root:
            continue
        for file in files:
            # 排除 .pyc 文件
            if file.endswith('.pyc'):
                continue
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path)
            file_count += 1

# 恢复原目录
os.chdir(original_dir)

# 获取文件大小
size = os.path.getsize(zip_file)
print(f"✅ 打包完成: {zip_file} ({size / 1024:.1f}KB, {file_count} 个文件)")
EOF
```

**2.3 验证打包结果**

```bash
if [ ! -f "$ZIP_FILE" ]; then
  echo "错误: 打包失败，压缩包未生成"
  exit 1
fi

# 显示压缩包内容（验证路径是否正确）
python3 -c "
import zipfile
with zipfile.ZipFile('$ZIP_FILE', 'r') as zipf:
    print('=== 压缩包内容 ===')
    for info in zipf.infolist()[:15]:
        print(f'  {info.filename}')
    if len(zipf.infolist()) > 15:
        print(f'  ... 共 {len(zipf.infolist())} 个文件')
"
```

#### 步骤 3: 上传到服务器（如果未跳过）

**3.1 构建请求**

使用 curl 发送 PUT 请求上传压缩包：

```bash
PLUGIN_ID="{plugin_id}"
API_URL="${JAVIS_FRONTEND_BASE_URL}/api/v1/plugins/${PLUGIN_ID}/reupload"

echo "正在上传到: $API_URL"

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  -H "Authorization: Bearer $JAVIS_AUTH_TOKEN" \
  -F "file=@$ZIP_FILE" \
  -F "stripFirstLevel=true" \
  "$API_URL")

HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP 状态码: $HTTP_CODE"
echo "响应内容: $BODY"
```

**3.2 处理响应**

根据 HTTP 状态码处理结果：

```bash
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
  echo "✅ Plugin 上传成功"
else
  echo "❌ Plugin 上传失败"
  echo "错误信息: $BODY"
  exit 1
fi
```

#### 步骤 4: 清理临时文件

可选清理（保留压缩包供用户查看）：

```bash
# 如需清理，取消注释以下代码
# rm -f "$ZIP_FILE"
# echo "临时文件已清理"
```

#### 步骤 5: 发布通知到钉钉群

**5.1 读取最新版本特性**

从 Release Note 中获取最新版本的特性内容：

```bash
# 读取 Release Note 文件
RELEASE_NOTE="/workspace/doc/release_note.md"

if [ ! -f "$RELEASE_NOTE" ]; then
  echo "⚠️ Release Note 文件不存在，跳过通知"
else
  # 提取最新版本内容（第一个版本块）
  LATEST_VERSION=$(sed -n '/^## v/,/^---$/p' "$RELEASE_NOTE" | head -n -1 | head -30)
  echo "最新版本特性已获取"
fi
```

**5.2 发送钉钉通知**

通过 Webhook 发送 Markdown 消息到钉钉群：

```bash
# 读取钉钉 Webhook 配置
DINGTALK_CONFIG=~/.dingtalk-skills/config
WEBHOOK_URL=$(grep '^DINGTALK_WEBHOOK_URL=' "$DINGTALK_CONFIG" 2>/dev/null | cut -d= -f2-)

if [ -z "$WEBHOOK_URL" ]; then
  echo "⚠️ 钉钉 Webhook 未配置，跳过通知"
  echo "如需启用通知，请配置 DINGTALK_WEBHOOK_URL"
else
  # 发送 Markdown 消息
  curl -s -X POST "$WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d '{
      "msgtype": "markdown",
      "markdown": {
        "title": "JavisSales Release Note",
        "text": "# JavisSales Release Note\n\n'"$(echo "$LATEST_VERSION" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')"'"\n"
      }
    }'

  echo "✅ 钉钉通知已发送"
fi
```

**5.3 通知内容格式**

发送的消息格式为：

```markdown
# JavisSales Release Note

## v1.1.0 (2026-03-16)

### 新增功能
- `skill-developer` (+) 功能描述
- ...

### 优化改进
- `bid-strategist` (~) 优化描述
- ...
```

**5.4 错误处理**

- 如果 Release Note 文件不存在，跳过通知步骤
- 如果钉钉 Webhook 未配置，跳过通知步骤
- 通知失败不影响部署结果

#### 步骤 6: 输出执行结果

向用户输出完整的执行结果：

```markdown
✅ Plugin 部署完成

## 打包信息
- Plugin 目录: {plugin_dir}
- 压缩包路径: {zip_file}
- 压缩包大小: {size}

## 上传信息
- Plugin ID: {plugin_id}
- API 地址: {api_url}
- 上传状态: 成功

## 发布通知
- 钉钉通知: 已发送/已跳过

## 后续操作
- 前往管理后台查看 Plugin 状态
- 测试 Plugin 功能是否正常
```

## Output Format

**成功输出**:
```markdown
✅ Plugin 部署完成

## 打包信息
- Plugin 目录: apps/pulgins/sale-jerry-plugin
- 压缩包路径: /tmp/sale-jerry-plugin.zip
- 压缩包大小: 125KB

## 上传信息
- Plugin ID: cmk3oovu1002m4prviw8mqq21
- API 地址: http://localhost:8000/api/v1/plugins/cmk3oovu1002m4prviw8mqq21/reupload
- 上传状态: 成功

## 发布通知
- 钉钉通知: ✅ 已发送
```

**失败输出**（目录不存在）:
```markdown
❌ Plugin 打包失败

错误信息: Plugin 目录不存在: apps/pulgins/sale-jerry-plugin

请检查目录路径是否正确。
```

**失败输出**（Token 未设置）:
```markdown
❌ 认证失败

错误信息: JAVIS_AUTH_TOKEN 环境变量未设置

请确保已正确配置认证环境变量。
```

**失败输出**（上传失败）:
```markdown
❌ Plugin 上传失败

错误信息: HTTP 401 - Unauthorized

请检查 Token 是否有效或已过期。
```

## Integration

### 与其他 Skills 的协作

此 Skill 通常在以下场景使用：

| 场景 | 前置操作 | 说明 |
|------|---------|------|
| Plugin 开发完成 | plugin-auditor | 先审计配置，再部署 |
| Plugin 更新 | 代码修改后 | 直接打包部署 |
| 版本发布 | Git 打标签 | 记录版本号后部署 |

### 使用场景

| 场景 | 使用时机 |
|------|---------|
| 开发完成 | Plugin 开发完成后部署到服务器 |
| 更新发布 | 修改代码后重新部署 |
| 测试验证 | 部署到测试环境验证功能 |

## Best Practices

### 打包建议
- 确保所有代码已保存并提交
- 检查 `.gitignore` 中的排除项
- 打包前运行 `plugin-auditor` 进行审计

### 上传建议
- 确保 Token 有效且未过期
- 检查网络连接正常
- 大文件上传可能需要较长时间

### 版本管理
- 建议在部署前打 Git 标签
- 记录每次部署的版本号和时间
- 保留旧版本以备回滚

## Notes

1. **Token 安全**: 不要在日志中输出完整 Token
2. **目录路径**: 支持相对路径和绝对路径
3. **压缩格式**: 使用 zip 格式，兼容性好
4. **排除规则**: 自动排除 `.git`、`__pycache__` 等
5. **stripFirstLevel**: 参数为 true 时，去除压缩包根目录层级
6. **钉钉通知**: 部署成功后自动发送 Release Note 到钉钉群，需配置 `DINGTALK_WEBHOOK_URL`
7. **通知跳过**: 如钉钉 Webhook 未配置，不影响部署，仅跳过通知步骤

## Examples

### 示例 1: 默认部署

**输入**:
```javascript
Skill(
  skill: "plugin-deploy"
)
```

**执行流程**:
1. 验证环境变量和目录
2. 打包 `apps/pulgins/sale-jerry-plugin` 目录
3. 上传到 Plugin ID `cmk3oovu1002m4prviw8mqq21`
4. 输出结果

**输出**:
```markdown
✅ Plugin 部署完成

## 打包信息
- Plugin 目录: apps/pulgins/sale-jerry-plugin
- 压缩包路径: /tmp/sale-jerry-plugin.zip
- 压缩包大小: 125KB

## 上传信息
- Plugin ID: cmk3oovu1002m4prviw8mqq21
- 上传状态: 成功

## 发布通知
- 钉钉通知: ✅ 已发送
```

### 示例 2: 指定 Plugin ID

**输入**:
```javascript
Skill(
  skill: "plugin-deploy",
  args: {
    "plugin_id": "another-plugin-id-123"
  }
)
```

**执行流程**:
1. 使用指定的 Plugin ID 上传

### 示例 3: 仅打包不上传

**输入**:
```javascript
Skill(
  skill: "plugin-deploy",
  args: {
    "skip_upload": true
  }
)
```

**执行流程**:
1. 打包 Plugin 目录
2. 跳过上传步骤
3. 仅输出压缩包信息

**输出**:
```markdown
✅ Plugin 打包完成（已跳过上传）

## 打包信息
- Plugin 目录: apps/pulgins/sale-jerry-plugin
- 压缩包路径: /tmp/sale-jerry-plugin.zip
- 压缩包大小: 125KB
```

### 示例 4: 自定义目录

**输入**:
```javascript
Skill(
  skill: "plugin-deploy",
  args: {
    "plugin_dir": "plugins/my-custom-plugin",
    "output_dir": "./dist"
  }
)
```

**执行流程**:
1. 打包 `plugins/my-custom-plugin` 目录
2. 压缩包输出到 `./dist/my-custom-plugin.zip`
3. 上传到服务器

---

**版本**: 1.1
**最后更新**: 2026-03-16
**作者**: AI Solutions Expert Team
**依赖**: Python 3, curl
**变更记录**:
- v1.1 (2026-03-16): 新增发布后自动通知钉钉群功能
- v1.0 (2026-03-14): 初始版本
