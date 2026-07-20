from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
import time
import re
import os

# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="News Classifier API",
    description="Classifies news text into categories using facebook/bart-large-mnli",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Render deployment
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# ─── Port (7860 for HF Spaces, 8000 for local) ────────────────────────────────
PORT = int(os.environ.get("PORT", 7860))

# ─── Model Loading ─────────────────────────────────────────────────────────────
print("🔄 Loading Hugging Face model (facebook/bart-large-mnli)...")
print("   This may take a moment on first run while the model downloads...")

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
)

print("✅ Model loaded successfully!")

# ─── Category Labels ───────────────────────────────────────────────────────────
CATEGORIES = [
    "Politics",
    "Sports",
    "Business",
    "Technology",
    "Health",
    "Entertainment",
    "Science",
    "World News",
]

# ─── Schemas ───────────────────────────────────────────────────────────────────
class ClassifyRequest(BaseModel):
    text: str


class CategoryScore(BaseModel):
    label: str
    score: float
    percentage: float


class ClassifyResponse(BaseModel):
    top_category: str
    top_score: float
    categories: list[CategoryScore]
    word_count: int
    char_count: int
    processing_time_ms: float
    text_preview: str


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "model": "facebook/bart-large-mnli", "categories": CATEGORIES}


@app.post("/classify", response_model=ClassifyResponse)
def classify_news(req: ClassifyRequest):
    text = req.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Text is too short to classify. Please enter at least 10 characters.")

    if len(text) > 10000:
        raise HTTPException(status_code=400, detail="Text is too long. Please limit to 10,000 characters.")

    # Truncate to first 512 tokens worth of text for performance
    truncated = text[:2000]

    start_time = time.time()

    try:
        result = classifier(truncated, candidate_labels=CATEGORIES, multi_label=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")

    elapsed_ms = (time.time() - start_time) * 1000

    # Build category score list sorted by score descending
    scores = sorted(
        zip(result["labels"], result["scores"]),
        key=lambda x: x[1],
        reverse=True,
    )

    categories = [
        CategoryScore(
            label=label,
            score=round(score, 6),
            percentage=round(score * 100, 2),
        )
        for label, score in scores
    ]

    # Word count (basic)
    word_count = len(re.findall(r"\b\w+\b", text))

    # Short preview
    text_preview = text[:120] + "..." if len(text) > 120 else text

    return ClassifyResponse(
        top_category=categories[0].label,
        top_score=categories[0].score,
        categories=categories,
        word_count=word_count,
        char_count=len(text),
        processing_time_ms=round(elapsed_ms, 1),
        text_preview=text_preview,
    )


# ─── Serve frontend static files (must be mounted AFTER all API routes) ────────
_frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
