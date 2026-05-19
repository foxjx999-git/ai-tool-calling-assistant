import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "pdf_chunks")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

client = OpenAI()

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

def search_pdf_chunks(query:str, top_k: int = 3) ->dict:
    """
    从旧 RAG 项目的 ChromaDB 中检索 PDF chunks。
    """
    if not CHROMA_DB_PATH:
        return {
            "status": "error",
            "message": "CHROMA_DB_PATH 未配置，请检查 .env 文件。",
            "results": [],
        }
    
    chroma_client  = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)

    query_embedding = get_query_embedding(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    ids = result.get("ids", [[]])[0]

    results = []

    for index, document in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index <len(distances) else None
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

    return {
        "status": "success",
        "query": query,
        "count": len(results),
        "results": results,
    }