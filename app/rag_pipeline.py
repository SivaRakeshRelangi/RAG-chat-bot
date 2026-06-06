from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore
from app.reranker import Reranker
from app.cache import get_cache, set_cache
from app.llm import LLM

class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.reranker = Reranker()
        self.vector_store = None
        self.generator = LLM()   # 🔥 NEW

    def build_index(self, chunks):
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.embed(texts)

        self.vector_store = VectorStore(len(embeddings[0]))
        self.vector_store.add(embeddings, chunks)
        self.vector_store.save()

    def query(self, question):
    cached = get_cache(question)
    if cached:
        return cached

    query_embedding = self.embedder.embed([question])[0]
    retrieved = self.vector_store.search(query_embedding)
    retrieved = self.reranker.rerank(question, retrieved)

    context = "\n".join([r["text"] for r in retrieved])

    prompt = f"""
                You are a helpful assistant.

                Answer ONLY from the context below.
                If answer not found, say "Not found in documents".

                Context:
            {context}

            Question:
            {question}

            Answer:
            """

    output = self.generator.generate(prompt)

    result = {
        "answer": output.strip(),
        "sources": [
            {"file": r.get("source"), "page": r.get("page")}
            for r in retrieved
        ]
    }

    set_cache(question, result)
    return result