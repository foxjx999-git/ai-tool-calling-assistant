import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from tool_runner import run_tool
from tool_schemas import tools

load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"


client = OpenAI()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")



def ask_ai(user_input: str) -> str:
    """
    支持多轮 Tool Calling 的 AI 调用流程。

    流程：
    1. 用户输入
    2. 模型判断是否需要调用工具
    3. 如果需要，Python 执行工具
    4. 把工具结果返回给模型
    5. 如果模型继续调用工具，就继续执行
    6. 如果模型返回普通文本，就结束
    """
    input_list = [
        {
            "role": "system",
            "content": (
                "你是一个 AI 应用工程师学习助手。"
                "你可以回答学习问题，也可以在需要时调用工具。"
                "当用户要求计算学习时长时，使用 calculate_study_hours。"
                "当用户要求记录学习进度时，使用 save_learning_log。"
                "当用户要求查看或总结学习记录时，使用 read_learning_logs。"
                "当用户要求记录学习进度，但缺少学习时长、主题或总结时，不要调用 save_learning_log，要先追问用户补充信息。"
                "如果工具返回 status 为 error，不要假装工具执行成功，要把错误原因告诉用户。"
                "最终回答要用中文，简洁清楚。"
            ),
        },
        {
            "role": "user",
            "content":user_input,
        },
    ]
    while True:
        response = client.responses.create(
            model=MODEL,
            input=input_list,
            tools=tools,
        )

        if DEBUG:
            print("\n====== 模型返回 ======")
            print(response.output)

        input_list += response.output

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            return response.output_text

        for tool_call in tool_calls:
            tool_name = tool_call.name
            
            arguments = json.loads(tool_call.arguments)
            
            if DEBUG:
                print("\n====== 模型请求调用工具 ======")
                print("工具名：", tool_name)
                print("参数：", arguments)

            tool_result = run_tool(tool_name, arguments)

            if DEBUG:
                print("\n====== Python 执行工具结果 ======")
                print(tool_result)

            if tool_result.get("status") == "error":
                return f"工具调用失败：{tool_result.get('message')}"

            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(tool_result, ensure_ascii=False),
                }
            )   


