import json
import os 
from datetime import datetime

from pdf_rag import search_pdf_chunks

def calculate_study_hours(days: int, hours_per_day: float) ->dict:
    total_hours = days * hours_per_day

    return {
        "status": "success",
        "message": "学习总时长计算完成",
        "data": {
            "days": days,
            "hours_per_day": hours_per_day,
            "total_hours": total_hours,
        },
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

    return {
        "status": "success",
        "message": "学习记录已保存",
        "data": {
            "record": record,
        },
    }

def read_learning_logs() -> dict:
    """
    读取所有学习记录。
    """
    file_path = "data/learning_log.json"

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {
            "status": "empty",
            "message": "暂无学习记录",
            "data": {
                "count": 0,
                "logs": [],
            },
        }
    
    with open(file_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    return {
        "status": "success",
        "message": "学习记录读取成功",
        "data": {
            "count": len(logs),
            "logs": logs,
        },
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
        "data": {
            "logs": [],
        },
    }


def tokenize_text(text: str) -> set:
    """
    简单分词函数：
    把文本转成小写，并按常见分隔符拆成关键词集合。
    """
    separators = [
        " ",
        "，",
        "。",
        "？",
        "?",
        "！",
        "!",
        "、",
        "：",
        ":",
        "；",
        ";",
        "（",
        "）",
        "(",
        ")",
        "\n",
    ]

    text = text.lower()

    for sep in separators:
        text = text.replace(sep, " ")

    words = text.split()

    stop_words = {
        "的",
        "了",
        "和",
        "是",
        "什么",
        "怎么",
        "如何",
        "一下",
        "请问",
        "有",
    }

    return {
        word for word in words
        if word and word not in stop_words
    }



def search_learning_notes(query: str) -> dict:
    """
    从本地 learning_notes.json 中检索学习笔记。
    简单相似度版：根据关键词重合度排序。
    """
    file_path = "data/learning_notes.json"

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return {
            "status": "empty",
            "message": "学习笔记知识库为空或文件不存在",
            "data": {
                "query": query,
                "count": 0,
                "results": [],
            },
        }

    with open(file_path, "r", encoding="utf-8") as f:
        notes = json.load(f)

    query_tokens = tokenize_text(query)

    scored_results = []

    for note in notes:
        title = note.get("title", "")
        content = note.get("content", "")
        note_text = f"{title} {content}"

        note_tokens = tokenize_text(note_text)

        overlap = query_tokens & note_tokens
        score = len(overlap)

        if score > 0:
            scored_results.append(
                {
                    "score": score,
                    "matched_keywords": list(overlap),
                    "source": {
                        "file": "data/learning_notes.json",
                        "id": note.get("id"),
                        "title": note.get("title"),
                    },
                    "content": content,
                }
            )

    scored_results.sort(key=lambda item: item["score"], reverse=True)

    top_results = scored_results[:3]

    if not top_results:
        return {
            "status": "empty",
            "message": "本地学习笔记中没有找到相关内容",
            "data": {
                "query": query,
                "query_tokens": list(query_tokens),
                "total_matches": 0,
                "count": 0,
                "results": [],
            },
        }

    return {
        "status": "success",
        "message": "学习笔记检索完成",
        "data": {
            "query": query,
            "query_tokens": list(query_tokens),
            "total_matches": len(scored_results),
            "count": len(top_results),
            "results": top_results,
        },
    }

def search_pdf_knowledge_base(query: str) -> dict:
    """
    从 PDF 知识库中检索相关内容。
    当前是占位版本，后续会接入 ChromaDB。
    """
    return search_pdf_chunks(query=query, top_k=3)