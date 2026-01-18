# AI Agent System (FastAPI + Memory + RAG)

一个从零构建的 **AI Agent 后端系统**，基于 FastAPI，对外提供标准 API，
实现了 **Planner + Executor + Memory + RAG** 的完整 Agent 架构。

> 本项目侧重于 **工程化落地**，而非简单 Prompt 调用，适合作为 AI Agent / LLM 后端实践项目。

---

## ✨ 核心能力

### 🤖 Agent 架构
- **Planner**：负责分析用户问题并生成执行计划
- **Executor / PlanExecutor**：执行规划步骤（可扩展工具调用）
- **Synthesizer**：整合执行结果，生成最终回答

### 🧠 Memory 机制
- **Short-Term Memory**
  - 维护多轮对话上下文
  - 用于连续追问场景
- **Long-Term Memory**
  - 基于向量的长期记忆（FAISS + Embedding）
  - 将历史对话摘要存入向量库，支持语义检索

### 📚 RAG（Retrieval-Augmented Generation）
- 文档加载、切分、向量化
- 基于语义检索的知识增强生成
- 与 Memory 解耦，便于扩展不同数据源

### 🌐 API 服务
- 基于 **FastAPI**
- 提供标准 HTTP 接口
- 可被前端 / 其他后端服务直接调用

### 🔌 LLM 可替换
- 当前接入 **DeepSeek**
- 设计上支持切换 OpenAI / 其他模型

---

## 🏗 项目结构
```bash
ai-app/
├── app/
│   ├── agent/            # Agent 核心（Planner / Executor / Memory）
│   ├── api/              # FastAPI 路由
│   ├── core/             # 配置管理
│   ├── llm/              # LLM Client（DeepSeek）
│   ├── prompt/           # Prompt 模板
│   ├── rag/              # RAG 模块（Embedding / Retriever / VectorStore）
│   ├── service/          # 业务服务层
│   └── main.py           # FastAPI 启动入口
│
├── data/                 # 示例知识库数据
│   └── java_gc.txt
│
├── test_*.py             # 各模块测试脚本
├── requirements.txt
└── README.md
```
---
## 🛠 技术栈

- **Python** 3.11
- **FastAPI**
- **Uvicorn**
- **Pydantic v2**
- **DeepSeek LLM**
- **FAISS**
- **Sentence-Transformers**

---

## 🚀 本地运行

### 1️⃣ 创建虚拟环境

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```
2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```
3️⃣ 配置环境变量

在项目根目录创建 .env（不要提交到 GitHub）：
DEEPSEEK_API_KEY=your_api_key_here
4️⃣ 启动服务
```bash
uvicorn app.main:app --reload
```
启动成功后访问：
	•	Swagger 文档：http://127.0.0.1:8000/docs

📡 API 使用示例

Agent Chat 接口
```bash
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是 JVM GC？"}'
```
多轮对话示例（Memory 生效）：
```bash
curl -X POST http://127.0.0.1:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "那为什么要分代收集？"}'
```

🧪 测试说明

项目中提供了多个测试脚本，用于验证核心模块：
	•	test_planner.py
	•	test_plan_executor.py
	•	test_short-term-memory.py
	•	test_long_term_memory.py
	•	test_rag.py

示例运行：
```bash
python test_long_term_memory.py
```


⸻

🧠 设计要点
	•	Agent 是架构，不是 Prompt
	•	Memory 是一等公民
	•	在规划阶段注入历史信息
	•	RAG 与对话记忆解耦
	•	文档知识 ≠ 对话记忆
	•	面向扩展设计，支持多 Agent / 多会话演进

⸻

🔮 后续规划
	•	多会话支持（session_id）
	•	Multi-Agent 协作（Planner / Critic / Executor）
	•	Docker 化与部署
	•	Web / 前端交互界面

⸻

📌 说明

本项目为个人工程实践项目，持续迭代中。
