import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from tool_runner import run_tool
from tool_schemas import tools
from prompts import SYSTEM_PROMPT


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
            "content": SYSTEM_PROMPT,
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


def ask_ai_with_trace(user_input: str) -> dict:
    """
    支持多轮 Tool Calling，并返回工具调用过程 trace。
    """
    input_list = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    tool_traces = []

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
            return {
                "answer": response.output_text,
                "tool_calls": tool_traces,
            }

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

            tool_traces.append(
                {
                    "name": tool_name,
                    "arguments": arguments,
                    "status": tool_result.get("status", "unknown"),
                    "message": tool_result.get("message", ""),
                    "data": tool_result.get("data", {}),
                }
            )

            if tool_result.get("status") == "error":
                return {
                    "answer": f"工具调用失败：{tool_result.get('message')}",
                    "tool_calls": tool_traces,
                }

            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(tool_result, ensure_ascii=False),
                }
            )