# AI Tool Calling 学习助手项目复盘

## 1. 项目目标

本项目的目标是学习 AI Agent / Tool Calling 的核心流程，并逐步将其扩展为一个支持本地学习记录、本地笔记检索、PDF RAG 检索和 Streamlit Web 页面展示的 AI 学习助手。

项目重点不是单纯调用大模型，而是理解：

- 模型如何判断是否需要调用工具
- Python 如何执行真实工具函数
- 工具结果如何返回给模型
- RAG 检索如何封装成 Agent 工具
- Web 页面如何展示工具调用过程

## 2. 当前已实现功能

- 普通 AI 问答
- 学习时长计算
- 学习记录保存、读取和清空
- 清空学习记录前二次确认
- 本地学习笔记检索
- PDF / ChromaDB 知识库检索
- OpenAI Embedding 查询向量
- 工具调用错误处理
- 空检索结果处理
- 工具返回格式统一为 `status / message / data`
- Streamlit Web 页面
- 工具调用 Trace 展示
- PDF 检索来源展示
- 清空当前对话

## 3. 项目结构设计

项目采用分层结构：

```text
main.py              命令行入口
app.py               Streamlit Web 页面
ai_client.py         AI 调用和 Tool Calling 主流程
prompts.py           System Prompt 配置
tool_schemas.py      给模型看的工具说明书
tool_runner.py       根据工具名分发到真实函数
tools.py             真实工具函数
pdf_rag.py           PDF / ChromaDB 检索逻辑
data/                本地 JSON 数据
```

这样的好处是：

- 页面逻辑和 AI 调用逻辑分离
- 工具说明和工具实现分离
- PDF RAG 检索独立封装
- 后续增加工具时结构更清晰

## 4. 核心流程

Tool Calling 核心流程：

```text
用户输入
↓
模型判断是否需要工具
↓
如果不需要，直接回答
↓
如果需要，返回 function_call
↓
Python 根据 tool_name 执行真实工具
↓
工具结果作为 function_call_output 返回模型
↓
模型基于工具结果生成最终回答
```

PDF RAG Agent 流程：

```text
用户询问 PDF 内容
↓
模型调用 search_pdf_knowledge_base
↓
Python 使用 OpenAI Embedding 生成 query 向量
↓
ChromaDB 检索 PDF chunks
↓
返回 source + content + score
↓
模型基于检索结果回答并引用来源
```

## 5. 关键学习点

### 5.1 tools 不是工具函数本身

`tool_schemas.py` 里的 `tools` 是给模型看的工具说明书。

真正执行工具的是 `tools.py` 里的 Python 函数。


### 5.2 Tool Calling 需要 Python 兜底

模型可能会绕过工具错误自行回答，所以关键错误不能只靠 Prompt 约束，需要代码层拦截。

例如：

```python
if tool_result.get("status") == "error":
    return ...
```

### 5.3 写操作和删除操作要更谨慎
- 保存学习记录：需要信息完整
- 清空学习记录：需要二次确认
- 读取学习记录：可以直接执行

这让我理解到不同工具要有不同安全策略。

### 5.4 RAG 可以封装成工具

本项目将两类 RAG 都封装成工具：

- `search_learning_notes`
- `search_pdf_knowledge_base`

这说明 RAG 不一定是固定流程，也可以作为 Agent 可调用的能力。

### 5.5 Embedding 模型必须一致

旧 ChromaDB 入库时使用的是：

```python
text-embedding-3-small
```

所以查询时也必须使用同一个 Embedding 模型，否则会出现维度不一致错误。

### 5.6 工具返回格式要统一

统一后的格式：

```python
{
    "status": "success | empty | error",
    "message": "...",
    "data": {...}
}
```

这样前端和 AI 调用层都更容易处理。

## 6. 遇到的问题和解决方式

### 问题 1：工具 schema 报错

原因：

- `additionalProperties` 拼写错误
- `required` 没有包含所有 `properties` 字段

解决：

- 使用 `additionalProperties: False`
- 确保 `required` 和 `properties` 一致

### 问题 2：工具返回 error，但模型仍然自己回答

原因：

- 模型看到参数后自己推理了结果

解决：

- 在代码层判断 `status == "error"` 后直接返回错误提示

### 问题 3：清空学习记录工具无法执行

原因：

- `clear_learning_logs` 的分发逻辑写在了未知工具 return 后面

解决：

- 把工具判断放在未知工具 return 前面

### 问题 4：ChromaDB embedding 维度不一致

原因：

- ChromaDB 默认 embedding 是 384 维
- 旧项目 OpenAI embedding 是 1536 维

解决：

- 手动使用 OpenAI 生成 query embedding
- 使用 `query_embeddings` 查询，而不是 `query_texts`

### 问题 5：OpenAI client 和 Chroma client 混用

原因：

- 两个对象都叫 client

解决：

- 改成 openai_client
- 改成 chroma_client

### 问题 6：Streamlit 历史消息丢失工具调用 Trace

原因：

- 只保存了 answer，没有保存 tool_calls

解决：

- assistant 消息中同时保存：

```python
{
    "role": "assistant",
    "content": answer,
    "tool_calls": tool_calls
}
```

## 7. 项目亮点

- 不只是简单聊天，而是具备多工具调用能力
- 同时支持 JSON 知识库和 PDF 向量知识库
- 支持工具调用过程可视化
- 支持 PDF 来源展示
- 具备错误处理、空结果处理、二次确认等工程化细节
 代码分层清晰，后续可扩展

## 8. 后续优化方向

- 增加登录或用户区分
- 增加学习记录删除单条功能
- 增加 PDF 上传和自动入库功能
- 增加更漂亮的 Streamlit 页面
- 部署到 Streamlit Community Cloud
- 将项目包装为个人 AI 应用工程师作品集