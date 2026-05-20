import streamlit as st

from ai_client import ask_ai_with_trace


st.set_page_config(
    page_title="AI Tool Calling 学习助手",
    page_icon="🤖",
    layout="centered",
)


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


st.title("🤖 AI Tool Calling 学习助手")

st.write(
    "这是一个支持 Tool Calling、学习记录管理、本地笔记检索和 PDF RAG 检索的 AI 学习助手。"
)

if st.button("清空当前对话"):
    st.session_state.messages = []
    st.rerun()

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




if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        show_tool_calls(message.get("tool_calls", []))


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
                tool_calls = []

        st.markdown(answer)
        show_tool_calls(tool_calls)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "tool_calls": tool_calls,
        }
    )