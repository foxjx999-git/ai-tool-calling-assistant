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

问个问题，我的.env里明明DEBUG=True，为什么在ai_client.py文件了读出的是false

很好。现在做收尾检查。

先在终端执行：

git status

你应该会看到类似：

modified: README.md
modified: pdf_rag.py
modified: tools.py
modified: prompts.py
modified: requirements.txt
new file: .env.example

具体以你实际为准。

然后提交：

git add .
git commit -m "Standardize tool results and update docs"

如果提交成功，再推送：

git push

推送成功后，这一阶段就正式完成了。

你现在这个项目已经具备：

Tool Calling 多工具调度
本地学习记录管理
本地 JSON 学习笔记 RAG
PDF / ChromaDB 真实检索
统一工具返回格式
错误处理和空结果处理
README 工程化说明
.env.example 配置模板

推送完成后，我们就可以进入下一阶段：把命令行 Agent 做成 Streamlit 页面版，让它从“终端项目”升级成“可展示 Web 应用”。

太好了，继续
已思考 4s

好，我们进入下一阶段：

第 24 小节：把命令行 Agent 升级成 Streamlit 页面版

你现在的项目已经很有内容了，但还是命令行形式：

python main.py

下一步我们做一个简单 Web 页面，让它可以在浏览器里使用。

目标是新增：

app.py

运行方式变成：

streamlit run app.py
1. 先安装 Streamlit

在当前项目虚拟环境里执行：

pip install streamlit

然后更新 requirements.txt，加一行：

streamlit
2. 新建 app.py

在项目根目录新建：

app.py

先放最小版本：

import streamlit as st

from ai_client import ask_ai


st.set_page_config(
    page_title="AI Tool Calling 学习助手",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 AI Tool Calling 学习助手")

st.write(
    "这是一个支持 Tool Calling、学习记录管理、本地笔记检索和 PDF RAG 检索的 AI 学习助手。"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("请输入你的问题，例如：这份 PDF 里怎么解释人工智能时代的职业选择？")


if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考并可能调用工具..."):
            try:
                answer = ask_ai(user_input)
            except Exception as e:
                answer = f"程序出错：{e}"

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
3. 这版 app.py 在做什么？

它只负责页面交互：

显示标题
显示历史聊天记录
接收用户输入
调用 ask_ai()
显示 AI 回答

核心 Agent 能力仍然在：

ai_client.py
tools.py
tool_runner.py
pdf_rag.py

也就是说，我们不是重写 Agent，只是给它加一个 Web 外壳。

4. 运行测试

执行：

streamlit run app.py

浏览器会打开一个页面。

你测试这几句话：

我每天学 2 小时，5 天一共多少小时？
tools 和 tools.py 有什么区别？
这份 PDF 里怎么解释人工智能时代的职业选择？

如果都能正常回答，说明 Web 版已经跑通。

5. 注意一个问题

你现在的 ask_ai() 里如果 DEBUG=true，终端会打印很多调试信息，但 Streamlit 页面不会显示这些工具调用过程。

这没关系。第一版页面先只显示最终回答。

后面我们可以升级：

在页面中显示工具调用过程
显示调用了哪个 tool
显示检索来源
显示 PDF 页码

但先别急，第一步先跑通页面。

你先安装 streamlit，新建 app.py，然后运行 streamlit run app.py。把页面测试结果告诉我。

非常好，Web 版已经跑通了，而且三个核心能力都正常：

学习时长计算 ✅
本地学习笔记检索 ✅
PDF RAG 检索 ✅

你现在已经从：

命令行 Agent

升级到了：

Streamlit Web Agent

这一步很重要，因为它更像一个可以展示的 AI 应用项目。

当前效果评价

你的页面已经具备基础可用性：

标题清楚
输入框正常
多轮消息展示正常
AI 回答能显示 Markdown
Tool Calling 后的最终回答能显示
PDF 来源也能展示

这已经是一个合格的第一版 Web UI。

下一步小优化建议

现在页面还缺少一个很有价值的点：

用户不知道 AI 背后调用了哪个工具。

命令行里我们能看到：

工具名：search_pdf_knowledge_base

但 Streamlit 页面里只显示最终回答。

下一节建议做：

第 25 小节：在 Streamlit 页面显示工具调用过程

目标是页面里能显示类似：

本次调用工具：search_pdf_knowledge_base
检索来源：03_人工智能大发展下的职业选择.pdf，第1、3、4页

这会让你的项目更像正式 RAG 应用，也更适合作品展示。

不过要做到这一点，我们需要稍微改造 ask_ai()，让它除了返回最终回答，还能返回工具调用记录。

现在 ask_ai() 只返回：

str

后面我们可以新增一个函数：

ask_ai_with_trace(user_input: str) -> dict

返回：

{
    "answer": "...",
    "tool_calls": [
        {
            "name": "search_pdf_knowledge_base",
            "arguments": {...},
            "result_status": "success"
        }
    ]
}

这样 Streamlit 页面就能显示“AI 调用了什么工具”。

你当前 Web 版第一步已经成功。下一步我们就做 工具调用 trace 显示。

好的
但是问了两个问题，前一个问题的提示信息没有了
给我解释一下加这个消息来源的代码吧
这个app.py的代码，帮我看看有什么不对的地方吗import streamlit as st

from ai_client import ask_ai_with_trace


st.set_page_config(
    page_title="AI Tool Calling 学习助手",
    page_icon="🤖",
    layout="centered",
)


st.title("🤖 AI Tool Calling 学习助手")

st.write(
    "这是一个支持 Tool Calling、学习记录管理、本地笔记检索和 PDF RAG 检索的 AI 学习助手。"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            with st.expander("查看本次工具调用过程"):
                for index, tool_call in enumerate(tool_calls, start=1):
                    st.markdown(f"**工具 {index}: {tool_call['name']}**")
                    st.json(tool_call["arguments"])
                    st.markdown(f"状态：{tool_call['status']}")
                    if tool_call.get("message"):
                        st.markdown(f"说明：{tool_call['message']}")


user_input = st.chat_input("请输入你的问题，例如：这份 PDF 里怎么解释人工智能时代的职业选择？")


if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考并可能调用工具..."):
            try:
                result = ask_ai_with_trace(user_input)
                answer = result["answer"]
                tool_calls = result["tool_calls"]
            except Exception as e:
                answer = f"程序出错：{e}"

        st.markdown(answer)

        if tool_calls:
            with st.expander("查看本次工具调用过程"):
                for index, tool_call in enumerate(tool_calls, start=1):
                    st.markdown(f"**工具 {index}: {tool_call['name']}**")
                    st.json(tool_call["arguments"])
                    st.markdown(f"状态：{tool_call['status']}")
                    if tool_call.get("message"):
                        st.markdown(f"说明：{tool_call['message']}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "tool_calls": tool_calls,
        }
    )
解释一下ask_ai_with_trace代码
讲一下这个程序的流程，什么情况下才返回
我测试了，可以清空对话，但是我也没记录learning_log.json

没关系，你的 learning_log.json 记录需要你明确通过“记录学习”这样的操作才会写入。清空对

好的，我们继续
已思考若干秒

好，我们继续主线。

你刚刚已经完成了：

Streamlit Web 页面 ✅
工具调用过程展示 ✅
历史消息保留 Trace ✅
清空当前对话按钮 ✅

下一步建议做 第 28 小节：在工具 Trace 里显示 PDF 检索来源。

现在页面的 Trace 里大概只能看到：

工具名：search_pdf_knowledge_base
参数：{"query": "..."}
状态：success
说明：PDF 知识库检索完成

但对于 RAG 项目，更有价值的是显示：

检索到了哪些 PDF？
第几页？
score 多少？
chunk_id 是什么？

这样用户能更清楚地看到 AI 的回答依据。

第一步：确认 ask_ai_with_trace() 保存了 data

在 ai_client.py 里找到这段：

tool_traces.append(
    {
        "name": tool_name,
        "arguments": arguments,
        "status": tool_result.get("status", "unknown"),
        "message": tool_result.get("message", ""),
    }
)

改成：

tool_traces.append(
    {
        "name": tool_name,
        "arguments": arguments,
        "status": tool_result.get("status", "unknown"),
        "message": tool_result.get("message", ""),
        "data": tool_result.get("data", {}),
    }
)

这一步的意思是：

不只保存工具名、参数、状态，也把工具返回的 data 保存下来。

对于 PDF RAG 工具，data 里会有：

{
    "query": "人工智能时代的职业选择",
    "count": 3,
    "results": [
        {
            "score": 0.61,
            "source": {
                "file": "...pdf",
                "page": 1,
                "chunk_id": "..."
            },
            "content": "..."
        }
    ]
}
第二步：修改 app.py 的 show_tool_calls()

你现在可能有这个函数：

def show_tool_calls(tool_calls: list) -> None:
    if not tool_calls:
        return

    with st.expander("查看本次工具调用过程"):
        for index, tool_call in enumerate(tool_calls, start=1):
            st.markdown(f"**工具 {index}: `{tool_call.get('name', 'unknown')}`**")
            st.json(tool_call.get("arguments", {}))
            st.markdown(f"状态：`{tool_call.get('status', 'unknown')}`")

            if tool_call.get("message"):
                st.markdown(f"说明：{tool_call['message']}")

我们先加一个简单的“来源展示”。

在 if tool_call.get("message"): 后面加：

            data = tool_call.get("data", {})
            results = data.get("results", [])

            if results:
                st.markdown("**检索来源：**")

                for result_index, result in enumerate(results, start=1):
                    source = result.get("source", {})
                    file_name = source.get("file", "unknown")
                    page = source.get("page", "unknown")
                    chunk_id = source.get("chunk_id", "unknown")
                    score = result.get("score")

                    if score is not None:
                        st.markdown(
                            f"- 来源 {result_index}: `{file_name}`，第 `{page}` 页，score: `{score:.3f}`"
                        )
                    else:
                        st.markdown(
                            f"- 来源 {result_index}: `{file_name}`，第 `{page}` 页"
                        )

                    st.caption(f"chunk_id: {chunk_id}")
第三步：完整的 show_tool_calls() 推荐版

你可以直接把函数替换成这个：

def show_tool_calls(tool_calls: list) -> None:
    """
    显示工具调用过程。
    """
    if not tool_calls:
        return

    with st.expander("查看本次工具调用过程"):
        for index, tool_call in enumerate(tool_calls, start=1):
            st.markdown(f"**工具 {index}: `{tool_call.get('name', 'unknown')}`**")
            st.json(tool_call.get("arguments", {}))
            st.markdown(f"状态：`{tool_call.get('status', 'unknown')}`")

            if tool_call.get("message"):
                st.markdown(f"说明：{tool_call['message']}")

            data = tool_call.get("data", {})
            results = data.get("results", [])

            if results:
                st.markdown("**检索来源：**")

                for result_index, result in enumerate(results, start=1):
                    source = result.get("source", {})
                    file_name = source.get("file", "unknown")
                    page = source.get("page", "unknown")
                    chunk_id = source.get("chunk_id", "unknown")
                    score = result.get("score")

                    if score is not None:
                        st.markdown(
                            f"- 来源 {result_index}: `{file_name}`，第 `{page}` 页，score: `{score:.3f}`"
                        )
                    else:
                        st.markdown(
                            f"- 来源 {result_index}: `{file_name}`，第 `{page}` 页"
                        )

                    st.caption(f"chunk_id: {chunk_id}")
第四步：测试

运行：

streamlit run app.py

输入：

这份 PDF 里怎么解释人工智能时代的职业选择？

打开“查看本次工具调用过程”，应该能看到：

工具 1: search_pdf_knowledge_base
参数：{"query": "..."}
状态：success
说明：PDF 知识库检索完成

检索来源：
- 来源 1: 03_人工智能大发展下的职业选择.pdf，第 1 页，score: 0.xxx
- 来源 2: 03_人工智能大发展下的职业选择.pdf，第 3 页，score: 0.xxx
- 来源 3: 03_人工智能大发展下的职业选择.pdf，第 4 页，score: 0.xxx

这一步完成后，你的 Web 页面就从“能聊天”升级到“能解释回答依据”。

已经测试完成

很好，说明第 28 小节完成了。

你现在的 Streamlit Web 版已经具备：

聊天界面 ✅
Tool Calling 调用 ✅
工具调用 Trace ✅
历史 Trace 保留 ✅
清空当前对话 ✅
PDF 检索来源展示 ✅

这已经是一个比较完整的可展示版本了。

下一步建议进入 第 29 小节：页面侧边栏整理项目说明和示例问题。

目的不是加复杂功能，而是让页面更像正式应用：

侧边栏显示：
- 当前支持的能力
- 示例问题
- 注意事项

这样别人打开你的网页，不用问你，也知道怎么测试。

比如在 app.py 里加：

with st.sidebar:
    st.header("📌 功能说明")

    st.markdown(
        """
        本助手支持：

        - 普通 AI 问答
        - 学习时长计算
        - 学习记录保存与读取
        - 本地学习笔记检索
        - PDF / ChromaDB RAG 检索
        - 工具调用过程展示
        """
    )

    st.header("💡 示例问题")

    st.markdown(
        """
        **学习计算**
        - 我每天学 2 小时，5 天一共多少小时？

        **学习记录**
        - 记录一下，我今天学了 PDF RAG 30 分钟，主要练习了工具返回格式。
        - 查看我的学习记录，并帮我总结一下。

        **本地笔记检索**
        - tools 和 tools.py 有什么区别？
        - RAG 和 Tool Calling 怎么结合？

        **PDF RAG 检索**
        - 这份 PDF 里怎么解释人工智能时代的职业选择？
        - 这份 PDF 里有没有讲火星移民？
        """
    )

    st.warning(
        "清空当前对话只会清除页面聊天记录，不会删除本地学习记录或 PDF 知识库。"
    )

放置位置：建议放在 st.write(...) 后面、初始化 session_state 前面。

你加完后页面会更完整。

很好，侧边栏已经加上了，整体效果是对的。

现在页面有：

左侧：功能说明 + 示例问题 + 注意事项
中间：聊天区域
底部：输入框

这已经比较像正式 Web 应用了。

不过我看到一个小问题：清空当前对话按钮出现了两次。

页面中间有一个：

清空当前对话

侧边栏底部也有一个：

清空当前对话

建议保留一个就够了。更推荐保留 侧边栏里的按钮，因为清空对话属于页面管理功能，不是聊天主体内容。

建议你改一下

如果你现在主页面有这段：

if st.button("清空当前对话"):
    st.session_state.messages = []
    st.rerun()

把它删掉。

然后只在侧边栏里保留：

with st.sidebar:
    ...

    if st.button("清空当前对话"):
        st.session_state.messages = []
        st.rerun()

这样主页面会更干净。

当前这个阶段完成情况

你现在已经完成：

Streamlit 页面基础版 ✅
工具调用过程展示 ✅
历史工具 Trace 保留 ✅
PDF 检索来源展示 ✅
清空当前对话 ✅
侧边栏功能说明 ✅
示例问题展示 ✅

下一步建议做最后一个页面体验优化：

给示例问题做成可点击按钮，一点就自动填入并执行。

不过这一步不是必须。如果你想保持简单，现在这个版本已经可以作为阶段性 Web 展示版。

侧边栏没有清空当前对话框按钮，哪只是警告文字
我想放在主页，就一个按钮而已，侧边栏还不好找

可以，放主页完全没问题，而且你这个理由对：清空当前对话是高频操作，放主页更直观。

那就保持现在的设计：

if st.button("清空当前对话"):
    st.session_state.messages = []
    st.rerun()

建议放在标题和说明文字下面，也就是：

st.title("🤖 AI Tool Calling 学习助手")

st.write(
    "这是一个支持 Tool Calling、学习记录管理、本地笔记检索和 PDF RAG 检索的 AI 学习助手。"
)

if st.button("清空当前对话"):
    st.session_state.messages = []
    st.rerun()

侧边栏里只保留警告文字就行：

st.warning(
    "清空当前对话只会清除页面聊天记录，不会删除本地学习记录或 PDF 知识库。"
)

这样逻辑很清楚：

主页按钮：执行清空当前对话
侧边栏警告：解释这个按钮不会删除学习记录或 PDF 知识库

你这个设计是合理的，不用改到侧边栏。

好的，这个应该学完了吧

是的，这个阶段可以算学完了，而且完成度很高。

你这次完成的不只是一个 Streamlit 页面，而是把整个 AI Tool Calling + RAG Agent 项目 做到了一个阶段性成品。

你已经完成：

1. 命令行版 Tool Calling Agent
2. 多工具调用流程
3. 工具参数 schema
4. tool_runner 工具分发
5. 本地学习记录保存 / 读取 / 清空
6. 错误处理和参数不完整追问
7. 破坏性操作二次确认
8. 本地 learning_notes.json 笔记检索
9. 关键词重合度检索
10. PDF / ChromaDB RAG 检索
11. OpenAI Embedding 查询向量
12. 最低相关度阈值过滤
13. 统一工具返回格式 status / message / data
14. Streamlit Web 页面
15. 工具调用 Trace 展示
16. PDF 检索来源展示
17. 历史消息保留工具调用过程
18. 清空当前对话按钮
19. 侧边栏功能说明和示例问题

这已经是一个很完整的 AI 应用工程师阶段项目。

下一步建议你不要马上加新功能，先做一次收尾：

git status
git add .
git commit -m "Add Streamlit web interface with tool trace"
git push

然后 README 里补充一下：

- 新增 Streamlit Web 页面
- 支持页面聊天
- 支持工具调用过程展示
- 支持 PDF 检索来源展示
- 支持清空当前对话

完成提交后，这个项目就可以作为你的一个正式作品放在 GitHub 上了。

后面主线可以进入下一阶段：Agent 工程化进阶 / 部署 / 简历项目包装。

好的，我们继续
已思考 7s

好，我们继续进入下一阶段：项目复盘 + 作品包装。

你现在这个项目已经不是普通练习了，已经可以作为一个 GitHub 作品。下一步我们要做的是让它更像一个“能给别人看的项目”。

第 30 小节：项目复盘文档

这一步建议新增一个文件：

PROJECT_REVIEW.md

它不是 README。README 是给别人看“项目怎么用”；PROJECT_REVIEW 是给你自己复盘“我学到了什么、项目怎么设计、踩过哪些坑”。

1. 新建 PROJECT_REVIEW.md

在项目根目录新建：

PROJECT_REVIEW.md

内容可以先写这个版本：

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