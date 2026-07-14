from torchtext.datasets   import AG_NEWS
from torchtext.data.utils import get_tokenizer
from torchtext.vocab      import build_vocab_from_iterator

from rnn_model import RNNClassifier
from dataset   import get_dataloaders
from train     import run_training
from predict   import predict, AG_NEWS_LABELS
import torch

def build_vocab(tokenizer):
    """Build vocabulary from AG News training data."""
    print("Building vocabulary...")
    train_iter, _ = AG_NEWS()
    vocab = build_vocab_from_iterator(
        map(lambda x: tokenizer(x[1]), train_iter),
        specials=["<unk>", "<pad>"],
    )
    vocab.set_default_index(vocab["<unk>"])
    print(f"Vocabulary: {len(vocab):,} tokens")
    return vocab

if __name__ == "__main__":
    print("=" * 50)
    print("  RNN Full Training Run")
    print("  Dataset: AG News | Model: Bi-LSTM")
    print("=" * 50 + "\n")

    device    = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    tokenizer = get_tokenizer("basic_english")
    vocab     = build_vocab(tokenizer)

    train_loader, test_loader = get_dataloaders(vocab, tokenizer, batch_size=64)
    model = RNNClassifier(vocab_size=len(vocab), num_classes=4)
    model = run_training(model, train_loader, test_loader, epochs=10)

    print("\nSample Predictions:")
    samples = [
        "Apple unveiled the M4 chip with a built-in AI neural engine.",
        "Manchester City won the Champions League final 3-1.",
        "Federal Reserve raises interest rates by 25 basis points.",
    ]
    for text in samples:
        cat = predict(text, model, vocab, tokenizer, device)
        print(f"  [{cat:<10}] {text[:60]}...")
