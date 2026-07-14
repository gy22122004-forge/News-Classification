"""
Transformer (HuggingFace) for News Classification
Model   : facebook/bart-large-mnli (406M params)
Task    : Zero-Shot Classification via NLI Entailment
Paper   : "Attention Is All You Need" — Vaswani et al. (2017)
"""

from transformers import pipeline
import time

print("=" * 65)
print("  Transformer (HuggingFace) News Classifier")
print("  Model  : facebook/bart-large-mnli (406M params)")
print("  Task   : Zero-Shot Classification (NO training data needed!)")
print("=" * 65)

print("\nLoading facebook/bart-large-mnli from Hugging Face...")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1,
)
print("✓ Model loaded!\n")

CATEGORIES = [
    "Politics", "Sports", "Business", "Technology",
    "Health", "Entertainment", "Science", "World News",
]

def classify(text: str, verbose: bool = True) -> dict:
    start  = time.time()
    result = classifier(
        text[:2000],
        candidate_labels=CATEGORIES,
        multi_label=False,
    )
    elapsed_ms = (time.time() - start) * 1000

    output = {
        "top_category": result["labels"][0],
        "confidence":   round(result["scores"][0] * 100, 2),
        "elapsed_ms":   round(elapsed_ms, 1),
        "all_scores": {
            label: round(score * 100, 2)
            for label, score in zip(result["labels"], result["scores"])
        },
    }

    if verbose:
        print(f"\n{'─'*65}")
        print(f"  Text      : {text[:80]}...")
        print(f"{'─'*65}")
        print(f"  Category  : {output['top_category']}")
        print(f"  Confidence: {output['confidence']}%")
        print(f"  Time      : {output['elapsed_ms']:.0f} ms\n")
        for label, pct in sorted(output["all_scores"].items(), key=lambda x: -x[1]):
            bar    = "█" * int(pct / 4) + "░" * (25 - int(pct / 4))
            print(f"    {label:<15} {bar} {pct:.1f}%")

    return output

DEMO_ARTICLES = [
    ("Technology", "Apple unveiled its next-generation M4 Pro chip at WWDC, claiming a 40% performance boost."),
    ("Sports", "Manchester City defeated Real Madrid 3-1 in the UEFA Champions League final at Wembley."),
    ("Politics", "The Senate passed a landmark $370 billion climate bill with a 62-38 bipartisan vote."),
]

if __name__ == "__main__":
    for expected, text in DEMO_ARTICLES:
        result = classify(text, verbose=False)
        got    = result["top_category"]
        match  = "✓" if got == expected else "✗"
        print(f"  {match}  Expected: {expected:<15} Got: {got:<15} ({result['confidence']}%)")
