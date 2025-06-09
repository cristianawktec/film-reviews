from fastapi import FastAPI
from gpt_analysis import analyze_sentiment
from faiss_search import search_similar_reviews

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API de Análise de Reviews com GenAI"}

@app.get("/analyze/")
def analyze(text: str):
    return analyze_sentiment(text)

@app.get("/search/")
def search(text: str):
    return search_similar_reviews(text)
