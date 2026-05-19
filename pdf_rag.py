import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "pdf_chunks")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
MIN_PDF_SCORE = float(os.getenv("MIN_PDF_SCORE", "0.55"))

client = OpenAI()

def validate_pdf_rag_config() -> dict:
    """
    检查 PDF RAG 相关配置是否完整。
    """
    missing = []

    if not CHROMA_DB_PATH:
        missing.append("CHROMA_DB_PATH")

    if not CHROMA_COLLECTION_NAME:
        missing.append("CHROMA_COLLECTION_NAME")

    if not EMBEDDING_MODEL:
        missing.append("EMBEDDING_MODEL")

    if missing:
        return {
            "status": "error",
            "message": f"缺少 PDF RAG 配置：{', '.join(missing)}",
        }

    return {
        "status": "success",
        "message": "PDF RAG 配置完整",
    }

def get_query_embedding(query: str) -> list[float]:
    """
    使用 OpenAI Embedding 模型把用户问题转成向量。
    这个向量维度要和旧 RAG 项目入库时使用的 embedding 模型一致。
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    return response.data[0].embedding

def search_pdf_chunks(query: str, top_k: int = 3) -> dict:
    """
    从旧 RAG 项目的 ChromaDB 中检索 PDF chunks。
    """
    config_check = validate_pdf_rag_config()

    if config_check["status"] == "error":
        return {
            "status": "error",
            "message": config_check["message"],
            "data": {
                "query": query,
                "count": 0,
                "results": [],
            },
        }

    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = chroma_client.get_collection(
        name=CHROMA_COLLECTION_NAME
    )

    query_embedding = get_query_embedding(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    ids = result.get("ids", [[]])[0]

    if not documents:
        return {
            "status": "empty",
            "message": "PDF 知识库中没有找到相关内容",
            "data": {
                "query": query,
                "count": 0,
                "results": [],
            },
        }

    results = []

    for index, document in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None
        chunk_id = ids[index] if index < len(ids) else index

        results.append(
            {
                "score": None if distance is None else 1 / (1 + distance),
                "source": {
                    "file": metadata.get("source", metadata.get("file", "unknown")),
                    "page": metadata.get("page", "unknown"),
                    "chunk_id": chunk_id,
                },
                "content": document,
            }
        )

    if not results:
        return {
            "status": "empty",
            "message": "PDF 知识库中没有找到相关内容",
            "data": {
                "query": query,
                "count": 0,
                "results": [],
            },
        }

    filtered_results = [
        item for item in results
        if item["score"] is not None and item["score"] >= MIN_PDF_SCORE
    ]

    if not filtered_results:
        return {
            "status": "empty",
            "message": "PDF 知识库中没有找到足够相关的内容",
            "data": {
                "query": query,
                "count": 0,
                "results": [],
            },
        }

    return {
        "status": "success",
        "message": "PDF 知识库检索完成",
        "data": {
            "query": query,
            "count": len(filtered_results),
            "results": filtered_results,
        },
    }