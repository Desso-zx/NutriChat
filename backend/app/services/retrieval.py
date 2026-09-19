import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings

_collection = None

def load_vector_store():
    """Connect to the persisted Chroma vector store built in the notebook."""
    global _collection

    client = chromadb.PersistentClient(path=settings.vector_db_path)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model
    )

    _collection = client.get_or_create_collection(
        name=settings.collection_name,
        embedding_function=embedding_func,
    )

    return _collection

def retrieve(query: str, top_k: int | None = None):
    """Query the Chroma collection and return chunks + metadata + distances."""
    if _collection is None:
        raise RuntimeError(
            "Vector store not loaded. load_vector_store() must run at startup."
        )

    k = top_k if top_k is not None else settings.top_k
    results = _collection.query(query_texts=[query], n_results=k)

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return list(zip(chunks, metadatas, distances))