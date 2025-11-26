# DIY Dictionary - 项目设置与运行指南

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- pip / npm

### 后端设置（本地开发）

#### 1. 安装依赖

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv vvv

# 激活虚拟环境
# macOS/Linux:
source vvv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 2. 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env，填入你的 API 密钥
# IMPORTANT: 选择你要使用的 LLM 提供商
# - Claude (推荐): LLM_PROVIDER=claude
# - OpenAI: LLM_PROVIDER=openai
# - Google Gemini: LLM_PROVIDER=gemini
```

#### 3. 运行开发服务器

```bash
# 从 backend 目录 uvicorn 直接运行
uvicorn app.main:app --reload (--port port_num)
```

服务器将在 `http://localhost:8000` 启动

#### 4. 验证后端正在运行

```bash
# 检查健康状态
curl http://localhost:8000/health # 失败
curl http://127.0.0.1:8000/health 
# 查看 API 文档
# 浏览器打开 http://localhost:8000/docs
```

### 前端设置（本地开发）

#### 1. 初始化项目

```bash
# 从项目根目录
bash init-frontend.sh
```

#### 2. 安装依赖

```bash
cd frontend
npm install
```

#### 3. 运行开发服务器

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动

#### 4. 构建生产版本

```bash
npm run build
```

## 项目结构

```
DIY-Dictionary/
├── backend/              # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py       # 应用入口
│   │   ├── config.py     # 配置管理
│   │   ├── services/     # 业务逻辑（LLM 调用等）
│   │   ├── api/          # API 端点
│   │   ├── db/           # 数据库配置
│   │   └── models/       # 数据模型
│   ├── tests/            # 单元测试
│   ├── .env.example      # 环境变量模板
│   └── requirements*.txt  # 依赖列表
│
├── frontend/             # Vue 3 + TypeScript 前端
│   ├── src/
│   │   ├── main.ts       # 应用入口
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 可复用组件
│   │   ├── services/     # API 服务
│   │   ├── stores/       # Pinia 状态管理
│   │   └── types/        # TypeScript 类型
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── docs/                 # 项目文档
```

## 开发工作流

### 后端开发

```bash
cd backend

# 运行测试
pytest

# 运行单个测试
pytest tests/test_translation.py

# 代码格式化
black app/

# Linting
flake8 app/
```

### LLM 功能

- `translate()`: 翻译英文到中文
- `explain_grammar()`: 解释语法
- `explain_vocabulary()`: 解释词汇（包括熟词生义）

## 数据库

### 本地开发（SQLite）

数据库文件自动创建在 `backend/diy_dictionary.db`


## 下一步

1.  后端框架搭建完成
2.  前端框架搭建完成
3.  实现 MVP 功能（句意翻译）
