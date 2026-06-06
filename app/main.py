from fastapi import FastAPI
import os
from app.ingestion import extract_text
from app.chunking import chunk_text
from app.rag_pipeline import RAGPipeline

app = FastAPI()
rag = RAGPipeline()

@app.post("/ingest/")
def ingest():
    all_chunks = []

    for file in os.listdir("data/raw_pdfs"):
        if file.endswith(".pdf"):
            pages = extract_text(f"data/raw_pdfs/{file}")
            chunks = chunk_text(pages)

            for c in chunks:
                c["source"] = file

            all_chunks.extend(chunks)

    rag.build_index(all_chunks)

    return {"status": "done", "chunks": len(all_chunks)}

@app.post("/query/")
def query(q: str):
    return rag.query(q)

@app.post("/debug/")
def debug(q: str):
    emb = rag.embedder.embed([q])[0]
    return rag.vector_store.search(emb, top_k=5)