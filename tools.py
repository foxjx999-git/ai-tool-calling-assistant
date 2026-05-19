import json
import os 
from datetime import datetime

def calculate_study_hours(days: int, hours_per_day: float) ->dict:
    total_hours = days * hours_per_day

    return {
        "days": days,
        "hours_per_day": hours_per_day,
        "total_hours": total_hours
    }

def save_learning_log(date: str, topic: str, minutes: int, summary: str) -> dict:
    """
    保存学习记录到本地 JSON 文件。
    """
    os.makedirs("data", exist_ok=True)

    file_path = "data/learning_log.json"

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path,"r", encoding="utf-8") as f:
            logs = json.load(f)

    else:
        logs = []

    record = {
        "date": date,
        "topic": topic,
        "minutes": minutes,
        "summary": summary,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    logs.append(record)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    return{
        "status": "success",
        "message": "学习记录已保存",
        "record": record,
    }

def read_learning_logs() -> dict:
    """
    读取所有学习记录。
    """
    file_path = "data/learning_log.json"

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {
            "status": "empty",
            "count": 0,
            "logs": [],
        }
    
    with open(file_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    return {
        "status": "success",
        "count": len(logs),
        "logs": logs,
    }

def clear_learning_logs() -> dict:
    """
    清空所有学习记录。
    """
    os.makedirs("data",exist_ok=True)
    file_path = "data/learning_log.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

    return {
        "status": "success",
        "message": "学习记录已清空",
        "logs": [],
    }