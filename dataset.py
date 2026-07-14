import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

class NewsDataset(Dataset):
    """AG News dataset wrapper for PyTorch DataLoader."""

    def __init__(self, data, vocab, tokenizer, max_len=256):
        self.data      = list(data)
        self.vocab     = vocab
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        label, text = self.data[idx]
        tokens = self.vocab(self.tokenizer(text))[: self.max_len]
        return torch.tensor(tokens, dtype=torch.long), torch.tensor(label - 1)

def collate_fn(batch):
    """Pad sequences to same length within a batch."""
    texts, labels = zip(*batch)
    texts = nn.utils.rnn.pad_sequence(texts, batch_first=True, padding_value=0)
    return texts, torch.stack(list(labels))

def get_dataloaders(vocab, tokenizer, batch_size=64):
    """Build train + test DataLoaders for AG News."""
    from torchtext.datasets import AG_NEWS
    train_iter, test_iter = AG_NEWS()
    train_ds = NewsDataset(train_iter, vocab, tokenizer)
    test_ds  = NewsDataset(test_iter,  vocab, tokenizer)
    train_loader = DataLoader(train_ds, batch_size, shuffle=True,  collate_fn=collate_fn)
    test_loader  = DataLoader(test_ds,  batch_size, shuffle=False, collate_fn=collate_fn)
    return train_loader, test_loader
