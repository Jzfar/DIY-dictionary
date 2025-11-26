# API 规范

## 基础信息

- **基础 URL**: `http://localhost:8000` (本地) / `https://api.diydict.com` (生产)
- **API 版本**: v1
- **内容类型**: `application/json`
- **认证**: 无 (MVP 阶段，未来添加 JWT)

## 端点

### 1. 翻译

**端点**: `POST /api/v1/translate`

**描述**: 将英文句子翻译成中文

**请求体**:
```json
{
  "text": "The quick brown fox jumps over the lazy dog",
  "source_lang": "en",
  "target_lang": "zh"
}
```

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `text` | string | ✅ | 要翻译的英文文本 |
| `source_lang` | string | ❌ | 源语言（默认: "en"） |
| `target_lang` | string | ❌ | 目标语言（默认: "zh"） |

**响应** (200 OK):
```json
{
  "original": "The quick brown fox jumps over the lazy dog",
  "translation": "敏捷的棕色狐狸跳过了懒狗",
  "source_lang": "en",
  "target_lang": "zh"
}
```

**错误响应** (400 Bad Request):
```json
{
  "detail": "Text cannot be empty"
}
```

**示例** (curl):
```bash
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "How are you?",
    "source_lang": "en",
    "target_lang": "zh"
  }'
```

---

### 2. 语法解释

**端点**: `POST /api/v1/explain-grammar`

**描述**: 提供句子或其选定部分的语法解释

**请求体**:
```json
{
  "text": "She has been working here for 5 years",
  "selected_text": "has been working"
}
```

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `text` | string | ✅ | 完整的英文句子 |
| `selected_text` | string | ❌ | 需要解释的特定部分（如果为空，解释整句） |

**响应** (200 OK):
```json
{
  "text": "She has been working here for 5 years",
  "selected_text": "has been working",
  "explanation": "这是现在完成进行时态。'has been' 是辅助动词，'working' 是现在分词。表示从过去某个时间开始直到现在一直在进行的动作。"
}
```

**错误响应** (400 Bad Request):
```json
{
  "detail": "Selected text not found in the main text"
}
```

**示例** (curl):
```bash
curl -X POST "http://localhost:8000/api/v1/explain-grammar" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I have finished my work",
    "selected_text": "have finished"
  }'
```

---

### 3. 词汇解释

**端点**: `POST /api/v1/explain-vocabulary`

**描述**: 解释单个单词的含义，支持多种解释模式

**请求体**:
```json
{
  "word": "bank",
  "context": "I went to the bank to withdraw money",
  "explanation_type": "context_meaning"
}
```

| 字段 | 类型 | 必需 | 值 | 描述 |
|------|------|------|---|------|
| `word` | string | ✅ | - | 要解释的单词 |
| `context` | string | ✅ | - | 单词所在的句子 |
| `explanation_type` | string | ❌ | `context_meaning` (默认) | 这个单词在此上下文中的含义 |
| | | | `common_meanings` | 单词的常见含义及在此上下文中的含义 |
| | | | `familiar_new` | 熟词生义 - 常见词的不寻常用法 |

**响应** (200 OK):
```json
{
  "word": "bank",
  "context": "I went to the bank to withdraw money",
  "explanation_type": "context_meaning",
  "explanation": "在这个句子中，'bank' 是指金融机构，你可以在那里存取钱。"
}
```

**示例** - 常见含义:
```json
{
  "word": "run",
  "context": "She runs a successful business",
  "explanation_type": "common_meanings"
}
```

**响应**:
```json
{
  "word": "run",
  "context": "She runs a successful business",
  "explanation_type": "common_meanings",
  "explanation": "'Run' 的常见含义包括：\n1. 跑步（运动）\n2. 经营/管理（业务）\n\n在此句子中，'run' 表示第二种含义：经营或管理一个成功的业务。"
}
```

**错误响应** (400 Bad Request):
```json
{
  "detail": "Word must not be empty"
}
```

**示例** (curl):
```bash
curl -X POST "http://localhost:8000/api/v1/explain-vocabulary" \
  -H "Content-Type: application/json" \
  -d '{
    "word": "bank",
    "context": "The river bank is beautiful",
    "explanation_type": "familiar_new"
  }'
```

---

### 4. 健康检查

**端点**: `GET /health`

**描述**: 检查服务器是否正常运行

**响应** (200 OK):
```json
{
  "status": "healthy"
}
```

---

### 5. 根路径

**端点**: `GET /`

**描述**: 获取应用信息

**响应** (200 OK):
```json
{
  "status": "ok",
  "app": "DIY Dictionary",
  "version": "0.1.0",
  "environment": "dev"
}
```

## 错误处理

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

常见 HTTP 状态码：

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误（通常是 LLM API 问题） |

## LLM 集成细节

### API 密钥验证
如果 `LLM_API_KEY` 环境变量未设置，所有 LLM 端点将返回：

```json
{
  "detail": "LLM_API_KEY environment variable not set. Please configure your LLM provider."
}
```

### 超时
- 翻译和语法解释：通常 10-30 秒
- 词汇解释：通常 5-20 秒

## 分页与速率限制

当前版本（MVP）不支持分页和速率限制。

计划在 1.0 版本中添加：
- 速率限制 (500 请求/小时 per IP)
- 可选的用户认证
- 用户配额管理

## API 文档

### 自动生成的文档

启动后端后，访问以下 URL 获取交互式 API 文档：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 向后兼容性

API v1 遵循 semantic versioning。破坏性变更将在新的主版本中引入（如 `/api/v2/`）。

## 示例：完整工作流

```bash
# 1. 翻译句子
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The book is on the table"
  }'

# 2. 理解语法结构
curl -X POST "http://localhost:8000/api/v1/explain-grammar" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The book is on the table",
    "selected_text": "is on"
  }'

# 3. 学习词汇
curl -X POST "http://localhost:8000/api/v1/explain-vocabulary" \
  -H "Content-Type: application/json" \
  -d '{
    "word": "book",
    "context": "The book is on the table",
    "explanation_type": "context_meaning"
  }'
```
