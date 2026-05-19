tools = [
    {
        "type": "function",
        "name": "calculate_study_hours",
        "description": "计算学习总时长。当用户问每天学习多少小时、学习多少天后一共多少小时时，使用这个工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                },
                "hours_per_day": {
                    "type": "number",
                    "description": "每天学习小时数",
                },
            },
            "required": ["days", "hours_per_day"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "save_learning_log",
        "description": (
            "保存用户的一条学习记录。"
            "只有当用户明确提供学习日期或表示今天、学习主题、学习时长、学习内容总结时，才使用这个工具。"
            "如果缺少学习时长、主题或总结，不要调用工具，应先让用户补充信息。"
        ),
        "parameters": {
            "type": "object",
            "properties":{
                "date": {
                    "type": "string",
                    "description": "学习日期，格式为 YYYY-MM-DD。如果用户说今天，就使用 2026-05-16。",
                },
                "topic": {
                    "type": "string",
                    "description": "学习主题，例如 Tool Calling、RAG、Prompt Engineering。",
                },
                "minutes": {
                    "type": "integer",
                    "description": "学习时长，单位是分钟。",
                },
                "summary": {
                    "type": "string",
                    "description": "学习内容总结。",
                },
            },
            "required": ["date", "topic", "minutes", "summary"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_learning_logs",
        "description": "读取用户已经保存的学习记录。当用户问查看学习记录、我最近学了什么、总结我的学习进度、学习历史时，使用这个工具。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "clear_learning_logs",
        "descriptiopn": (
            "清空用户所有学习记录。"
            "这是不可恢复的破坏性操作。"
            "只有当用户明确输入“确认清空学习记录”或“确认清空”时，才可以调用这个工具。"
            "如果用户只是说“清空我的学习记录”或“删除学习记录”，不要调用工具，应先要求用户确认。"
        ),
        "parameters":{
            "type": "object",
            "properties": {},
            "required":[],
            "additionalProperties": False,
        },
        "strict": True,
    },
]