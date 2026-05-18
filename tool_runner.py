from tools import calculate_study_hours, save_learning_log, read_learning_logs


def run_tool(tool_name: str, arguments: dict) -> dict:
    """
    根据模型请求的工具名，执行对应的 Python 函数。
    """
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
