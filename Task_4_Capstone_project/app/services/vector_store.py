import chromadb
import uuid
import logging
from fastapi import HTTPException, status
from app.core.config import settings  

# Initialize Logger
logger = logging.getLogger(__name__)

# --- 1. INITIALIZE CLIENT SAFELY ---

try:
    client = chromadb.PersistentClient(
        path=str(settings.CHROMA_DB_DIR)
    )
    
    collection = client.get_or_create_collection(
        name=settings.COLLECTION_NAME
    )
    logger.info(f"Connected to ChromaDB at {settings.CHROMA_DB_DIR}")

except Exception as e:
    logger.critical(f"Failed to connect to ChromaDB: {e}")
    raise RuntimeError("Database connection failed")

def store_chunks(chunks: list[dict], embeddings: list[list[float]], session_id: str):
    """
    Store text chunks and their embeddings in ChromaDB safely.
    Requires session_id to isolate user data.
    """

    if not chunks or not embeddings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chunks or embeddings are empty"
        )
    
    if len(chunks) != len(embeddings):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Mismatch between chunks and embeddings count"
        )
    
    ids = []
    documents = []
    metadatas = []
    
   
    valid_embeddings = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        text = chunk.get("text", "").strip()

        if not text:
            logger.warning(f"Skipping empty chunk at index {idx}")
            continue

        ids.append(str(uuid.uuid4()))
        documents.append(text)
        valid_embeddings.append(embedding)

        metadatas.append({
            "page": chunk.get("page"),
            "source": chunk.get("source", "uploaded_pdf"),
            "session_id": session_id 
        })
    
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="No valid text content found to store"
        )

    try:
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=valid_embeddings, 
            metadatas=metadatas
        )
        logger.info(f"Stored {len(documents)} chunks for session {session_id}")

    except Exception as e:
        logger.exception("Failed to store chunks in ChromaDB")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector store failed: {str(e)}"
        )

def search_similar(query_embedding: list[float], session_id: str, top_k: int = settings.TOP_K):
    """
    Search for similar documents using vector similarity.
    Filters strictly by session_id.
    """

    if not query_embedding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query embedding is empty"
        )

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k, 
            where={"session_id": session_id}  # <--- SESSION FILTERING
        )
        
        if not results or not results.get("documents"):
            logger.warning(f"No matching documents found for session {session_id}")
            
        return results

    except Exception as e:
        logger.exception("Vector search failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector search failed: {str(e)}"
        )