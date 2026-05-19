# AI Tool Calling 学习助手

这是一个基于 `OpenAI Tool Calling` 的命令行 `AI` 学习助手项目。

项目目标是学习和理解 `AI Agent` 的基础能力：让模型根据用户输入自动判断是否需要调用工具，由 `Python` 程序执行真实工具函数，再把工具结果返回给模型生成最终回答。

## 项目功能

目前支持以下功能：

- 普通 `AI` 问答
- 自动判断是否需要调用工具
- 计算学习总时长
- 保存学习记录到本地 `JSON` 文件
- 读取学习记录并总结
- 支持一个问题触发多个工具调用
- 工具执行失败时返回结构化错误信息
- 用户信息不完整时先追问，不直接保存
- 清空本地学习记录
- 对清空记录这类破坏性操作进行二次确认
- 从本地学习笔记 `learning_notes.json` 中检索相关内容
- 支持关键词重合度检索和相关性排序
- 检索结果包含来源信息，包括文件、笔记 ID 和标题
- 当本地笔记中没有相关内容时，明确提示未找到，避免假装基于资料回答
- 支持从 `PDF ChromaDB` 知识库中检索内容
- 支持从本地学习笔记 `learning_notes.json` 中检索相关内容
- 支持从 PDF / ChromaDB 知识库中检索真实 PDF 片段
- 支持回答中引用 PDF 文件名、页码和 chunk 来源
- 支持最低相关度阈值过滤，减少不相关检索结果
- 所有工具返回格式统一为 `status / message / data`
- 新增 `search_pdf_knowledge_base` 工具
- 新增 `pdf_rag.py` 负责 `PDF` 向量检索
- 使用 `OpenAI Embedding` 生成 `query embedding`
- 使用 `ChromaDB` 检索 `PDF chunks`
- 回答中返回 `PDF` 文件名和页码来源

## 技术栈

- `Python`
- `OpenAI API`
- `Responses API`
- `Tool Calling / Function Calling`
- `python-dotenv`
- `JSON` 本地存储

## 项目结构

```text
ai-tool-calling-assistant/
├── main.py              # 程序入口，负责命令行交互
├── ai_client.py         # AI 调用层，负责 Tool Calling 主流程
├── prompts.py           # Prompt 配置层，定义 system prompt
├── tools.py             # 工具函数层，放真实执行的 Python 函数
├── tool_schemas.py      # 工具说明书，定义给模型看的 tools
├── tool_runner.py       # 工具分发层，根据 tool_name 调用真实函数
├── pdf_rag.py           # PDF RAG 检索层，连接 ChromaDB 并检索 PDF chunks
├── data/                # 本地学习记录和学习笔记数据
├── .env                 # 环境变量文件，不上传 GitHub
├── .env.example         # 环境变量模板，可上传 GitHub
├── .gitignore
├── requirements.txt
└── README.md
```

## 核心流程

`Tool Calling` 的核心流程如下：

```text
用户输入
↓
模型第一次判断是否需要调用工具
↓
如果不需要工具，直接返回普通回答
↓
如果需要工具，模型返回 function_call
↓
Python 程序读取工具名和参数
↓
tool_runner.py 分发到真实工具函数
↓
tools.py 执行 Python 函数
↓
把工具执行结果作为 function_call_output 返回给模型
↓
模型基于工具结果生成最终回答
```

## 工具返回格式

为了方便 `ai_client.py` 统一处理工具结果，项目中的工具返回值统一采用以下结构：

```python
{
    "status": "success | empty | error",
    "message": "工具执行结果说明",
    "data": {
        "具体业务数据": "..."
    }
}
```
其中：

- success 表示工具执行成功
- empty 表示工具执行成功，但没有找到相关数据
- error 表示工具执行失败，需要由程序或用户处理

例如，PDF RAG 检索工具成功时会返回：

```python
{
    "status": "success",
    "message": "PDF 知识库检索完成",
    "data": {
        "query": "人工智能时代的职业选择",
        "count": 3,
        "results": [
            {
                "score": 0.61,
                "source": {
                    "file": "03_人工智能大发展下的职业选择.pdf",
                    "page": 1,
                    "chunk_id": "..."
                },
                "content": "PDF 中检索到的相关片段..."
            }
        ]
    }
}
```

## 当前工具

### 1. `calculate_study_hours`
用于计算学习总时长。

示例：

```text
我每天学 2.5 小时，12 天一共多少小时？
```

模型会调用：

```text
calculate_study_hours
```

并返回：

```text
30 小时
```

### 2. `save_learning_log`

用于保存学习记录到本地 `JSON` 文件。

示例：

```text
记录一下，我今天学了 Tool Calling 60 分钟，主要理解了多工具选择流程。
```

模型会调用：

```text
save_learning_log
```

并把记录保存到：

```text
data/learning_log.json
```

### 3. `read_learning_logs`

用于读取学习记录并让模型总结。

示例：

```text
查看我的学习记录，并帮我总结一下。
```

模型会调用：

```text
read_learning_logs
```

然后根据本地记录生成总结。

### 4. `clear_learning_logs`

用于清空本地所有学习记录。

这是一个破坏性操作，所以不会在用户第一次提出“清空学习记录”时直接执行。  
系统会先提醒用户该操作不可恢复，并要求用户明确回复“确认清空”或“确认清空学习记录”。

示例：

```text
清空我的学习记录
```
模型不会立即调用工具，而是先提醒确认：

```text
清空学习记录是不可恢复的操作。
如果你确定要清空，请回复“确认清空”或者“确认清空学习记录”。
```

当用户输入：

```text
确认清空
```
模型才会调用：

```text
clear_learning_logs
```

并把 `data/learning_log.json` 清空为：

```text
[]
```

### 5. `search_learning_notes`

用于从本地学习笔记知识库中检索相关内容。

该工具会读取 `data/learning_notes.json`，根据用户问题和笔记内容的关键词重合度进行简单检索，并返回最相关的笔记内容及来源信息。

返回内容包括：

- 匹配分数 `score`
- 匹配关键词 `matched_keywords`
- 来源文件 `source.file`
- 笔记 ID `source.id`
- 笔记标题 `source.title`
- 笔记内容 `content`

### 6. `search_pdf_knowledge_base`

用于从 PDF / ChromaDB 知识库中检索相关 PDF 片段。

该工具会调用 `pdf_rag.py` 中的检索逻辑：

1. 使用 OpenAI Embedding 将用户问题转换成向量
2. 连接旧 RAG 项目的 ChromaDB 向量库
3. 在 `pdf_chunks` collection 中检索相关 PDF chunks
4. 返回相关片段、相似度分数、PDF 文件名、页码和 chunk ID

示例：

```text
这份 PDF 里怎么解释人工智能时代的职业选择？
```

## 多工具调用示例

用户输入：

```text
查看我的学习记录，并且如果我接下来 7 天每天学 2 小时，一共还能学多少小时？
```

模型会同时调用：

```text
read_learning_logs
calculate_study_hours
```

程序会分别执行两个工具，然后把两个结果都返回给模型，最后生成综合回答。

## 安装与运行
### 1. 创建虚拟环境

```bash
python -m venv venv
```

Windows PowerShell：

```bash
.\venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install openai python-dotenv
```

### 3. 配置环境变量

项目不会上传真实 `.env` 文件。请复制 `.env.example` 并重命名为 `.env`：

```bash
copy .env.example .env
```
然后在 `.env` 中填写自己的 `OpenAI API Key` 和 `ChromaDB` 路径。

### 4. 运行项目

```bash
python main.py
```

退出程序：

```bash
exit
```

如果你已经把 `q` 和 `quit` 也加进退出判断，也可以输入：

```bash
q
quit
```

## 核心学习点

通过这个项目，重点理解了：

- `tools` 是给模型看的工具说明书，不是真正执行的函数
- `properties` 是工具参数清单，模型会根据它生成 `arguments`
- `function_call` 是模型发出的工具调用请求
- 真正执行工具的是 `Python` 程序
- `call_id` 用来对应某一次工具调用和工具执行结果
- `function_call_output` 用来把工具执行结果返回给模型
- 将 system prompt 单独拆分到 `prompts.py`，让 AI 调用流程和提示词配置解耦
- 一个用户问题可以触发多个工具调用
- 使用 `while True` 可以循环处理工具调用，直到模型返回最终文本
- 工具调用失败时，需要在代码层做兜底处理
- `Agent` 不应该在信息不足时强行调用工具，而应该先向用户追问
- 读操作、写操作、删除操作应该采用不同的安全策略
- 保存记录这类写操作需要确保用户信息完整
- 清空记录这类破坏性操作需要二次确认
- 工具分发逻辑要放在未知工具处理之前，否则对应工具永远不会执行
- RAG 检索可以被封装成 Tool Calling 中的一个工具
- 可以通过 `search_pdf_knowledge_base` 让 Agent 按需检索 PDF 知识库
- 查询 PDF 向量库时，query embedding 的模型必须和入库时使用的 embedding 模型一致
- 使用 `get_collection` 比 `get_or_create_collection` 更适合读取已有知识库，避免误创建空 collection
- 工具返回格式统一为 `status / message / data` 后，主流程更容易处理成功、空结果和错误
- 检索工具应返回来源信息，例如文件名、页码、chunk ID，方便回答时引用来源

## 后续计划

后续可以继续改进：

- 增加更多学习工具
- 增加学习计划生成工具
- 增加 `Streamlit` 页面
- 部署为在线 `AI` 学习助手