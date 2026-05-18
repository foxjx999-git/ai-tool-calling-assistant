from tools import calculate_study_hours, save_learning_log, read_learning_logs


def run_tool(tool_name: str, arguments: dict) -> dict:
    """
    根据模型请求的工具名，执行对应的 Python 函数。
    无论工具成功还是失败，都返回 dict，
    避免程序因为工具错误直接崩溃。
    """
    try:
        if tool_name == "calculate_study_hours":
            return calculate_study_hours(
                days=arguments["days"],
                hours_per_day=arguments["hours_per_day"],
            )
        if tool_name == "save_learning_log":
            return save_learning_log(
                date=arguments["date"],
                topic=arguments["topic"],
                minutes=arguments["minutes"],
                summary=arguments["summary"],
            )
        if tool_name =="read_learning_logs":
            return read_learning_logs()
        return {
            "error": f"未知工具：{tool_name}"
        }
    except KeyError as e:
        return {
            "status": "error",
            "message": f"工具参数缺失：{str(e)}",
            "tool_name": tool_name,
            "arguments": arguments,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"工具执行缺失：{str(e)}",
            "tool_name": tool_name,
            "arguments": arguments,
        }
