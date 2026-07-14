import torch

AG_NEWS_LABELS = {0: "World", 1: "Sports", 2: "Business", 3: "Sci/Tech"}

def predict(text, model, vocab, tokenizer, device, max_len=256):
    """
    Predict category for one news article.
    """
    model.eval()
    tokens = vocab(tokenizer(text))[:max_len]
    tensor = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).to(device)
    with torch.no_grad():
        pred = model(tensor).argmax(1).item()
    return AG_NEWS_LABELS[pred]

def predict_batch(texts, model, vocab, tokenizer, device):
    """Predict categories for a list of articles."""
    return [predict(t, model, vocab, tokenizer, device) for t in texts]

if __name__ == "__main__":
    print("RNN Prediction Demo (requires trained model)\n")
    sample_texts = [
        "Apple unveiled the M4 chip with 38T ops/sec AI engine.",
        "Man City won the Champions League final 3-1.",
        "The Fed raised interest rates by 25 basis points.",
        "Harvard reversed cellular aging in mice by 30%.",
    ]
    expected = ["Sci/Tech", "Sports", "Business", "Sci/Tech"]
    for text, exp in zip(sample_texts, expected):
        print(f"  Expected [{exp:<10}] | '{text[:55]}...'")
