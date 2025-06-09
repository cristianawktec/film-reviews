import faiss
import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mock index FAISS (em produção, usar persistência)
dimension = 1536
index = faiss.IndexFlatL2(dimension)
texts = ["Filme ótimo", "Muito ruim", "Excelente atuação"]
embeddings = []

def embed_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def search_similar_reviews(query):
    query_embedding = np.array([embed_text(query)], dtype=np.float32)
    if not index.is_trained:
        for t in texts:
            emb = embed_text(t)
            embeddings.append(emb)
        index.add(np.array(embeddings, dtype=np.float32))
    D, I = index.search(query_embedding, k=2)
    return [texts[i] for i in I[0]]
