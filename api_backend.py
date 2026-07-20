"""
FastAPI Backend REST API
Model   : facebook/bart-large-cnn (HuggingFace)
Run     : uvicorn api_backend:app --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import pipeline
import time

app = FastAPI(title="News Classifier API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading facebook/bart-large-cnn...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-cnn")
print("✓ Model ready!\n")

CATEGORIES = ["Politics", "Sports", "Business", "Technology", "Health", "Entertainment", "Science", "World News"]

class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000)

@app.post("/classify")
def classify_news(req: ClassifyRequest):
    text = req.text.strip()
    truncated = text[:2000]
    
    start_time = time.time()
    result = classifier(truncated, candidate_labels=CATEGORIES, multi_label=False)
    elapsed_ms = (time.time() - start_time) * 1000

    scores_sorted = sorted(zip(result["labels"], result["scores"]), key=lambda x: x[1], reverse=True)
    categories = [{"label": l, "score": round(s, 6), "percentage": round(s * 100, 2)} for l, s in scores_sorted]

    return {
        "top_category": categories[0]["label"],
        "top_score": categories[0]["score"],
        "categories": categories,
        "processing_time_ms": round(elapsed_ms, 1),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_backend:app", host="0.0.0.0", port=8000, reload=True)
