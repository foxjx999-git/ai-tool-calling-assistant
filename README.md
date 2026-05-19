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
├── tools.py             # 工具函数层，放真实执行的 Python 函数
├── tool_schemas.py      # 工具说明书，定义给模型看的 tools
├── tool_runner.py       # 工具分发层，根据 tool_name 调用真实函数
├── prompts.py           # Prompt 配置层，定义 system prompt
├── data/                # 本地学习记录数据
├── .env                 # 环境变量文件，不上传 GitHub
├── .gitignore
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

新建 `.env` 文件：

```env
OPENAI_API_KEY=你的 API Key
OPENAI_MODEL=gpt-4.1
```

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
- `RAG` 检索可以被封装成 `Tool Calling` 中的一个工具
- 检索工具不仅要返回内容，也应该返回来源信息
- 当检索不到内容时，要明确说明本地知识库没有相关资料
- 关键词重合度检索是向量检索前的简化版检索思想

## 后续计划

后续可以继续改进：

- 增加更多学习工具
- 增加学习计划生成工具
- 增加 `Streamlit` 页面
- 部署为在线 `AI` 学习助手