import torch
import torch.nn as nn

class RNNClassifier(nn.Module):
    """
    Bidirectional LSTM News Classifier.

    Architecture:
      Token IDs → Embedding (128-dim)
               → Bi-LSTM (256-dim × 2 directions)
               → Concat [fwd_hidden, bwd_hidden]
               → Dropout → Linear → Prediction
    """

    def __init__(self, vocab_size=95811, embed_dim=128,
                 hidden_dim=256, num_classes=8, num_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers,
                            batch_first=True, dropout=dropout, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        embedded = self.dropout(self.embedding(x))       # [B, L, E]
        _, (h_n, _) = self.lstm(embedded)               # h_n: [layers*2, B, H]
        hidden = torch.cat((h_n[-2], h_n[-1]), dim=1)   # concat fwd + bwd
        return self.fc(self.dropout(hidden))             # [B, num_classes]

if __name__ == "__main__":
    model = RNNClassifier()
    total = sum(p.numel() for p in model.parameters())
    print(f"RNN Model created — {total:,} parameters")
