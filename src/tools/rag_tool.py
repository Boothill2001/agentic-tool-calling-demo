from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from config import DOCS_DIR, EMBEDDING_DIM
from src.embeddings import embed_texts, embed_query
from src.llm import llm_call
from src.schema import ToolResult

_client: QdrantClient | None = None
_chunks: list[dict] = []
COLLECTION = "policy_docs"


def _init_rag():
    global _client, _chunks
    if _client is not None:
        return

    _client = QdrantClient(":memory:")
    _client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )

    _chunks = []
    for f in sorted(DOCS_DIR.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for para in paragraphs:
            _chunks.append({"text": para, "source": f.name})

    texts = [c["text"] for c in _chunks]
    vectors = embed_texts(texts)

    points = [
        PointStruct(id=i, vector=vectors[i].tolist(), payload={"text": _chunks[i]["text"], "source": _chunks[i]["source"]})
        for i in range(len(_chunks))
    ]
    _client.upsert(collection_name=COLLECTION, points=points)


def rag_search(query: str, top_k: int = 3) -> ToolResult:
    _init_rag()

    query_vec = embed_query(query)
    results = _client.query_points(
        collection_name=COLLECTION,
        query=query_vec.tolist(),
        limit=top_k,
    )

    context_chunks = []
    for i, pt in enumerate(results.points):
        context_chunks.append(f"[{i + 1}] ({pt.payload['source']})\n{pt.payload['text']}")

    context = "\n\n".join(context_chunks)

    system_prompt = """You are a helpful customer service assistant. Answer the user's question based ONLY on the provided context.
Use citations like [1], [2] to reference your sources. If the context doesn't contain enough information, say so."""

    user_msg = f"Context:\n{context}\n\nQuestion: {query}"

    try:
        answer = llm_call(system_prompt, user_msg)
    except Exception:
        answer = "Based on the retrieved documents:\n\n" + "\n\n".join(
            f"From {pt.payload['source']}:\n{pt.payload['text'][:300]}"
            for pt in results.points[:2]
        )

    return ToolResult(
        success=True,
        tool_name="rag_search",
        data={
            "answer": answer,
            "sources": [{"source": pt.payload["source"], "score": round(pt.score, 4), "text": pt.payload["text"][:200]} for pt in results.points],
        },
    )
