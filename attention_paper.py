"""
Attention Is All You Need (From Scratch)
Reference : Vaswani et al. (2017) — arXiv:1706.03762
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe       = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return self.dropout(x + self.pe[:, :x.size(1)])

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k     = d_model // n_heads
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)
        
        # Deterministic FFN to replace Softmax (maps 1D scalar score -> 16D -> 1D scalar weight)
        self.score_fc1 = nn.Linear(1, 16)
        self.score_fc2 = nn.Linear(16, 1)
        
        self.dropout = nn.Dropout(dropout)

    def attention(self, Q, K, V, mask=None):
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        
        # Replaced Softmax with a deterministic Fully Connected Feed-Forward Network
        # This transforms the raw attention scores deterministically instead of normalizing them.
        B, H, L, _ = scores.shape
        scores_expanded = scores.unsqueeze(-1) # Add feature dimension: [B, H, L, L, 1]
        
        # Pass through deterministic FFN (Linear -> ReLU -> Linear)
        hidden = F.relu(self.score_fc1(scores_expanded))
        weights = self.score_fc2(hidden).squeeze(-1) # Remove feature dimension: [B, H, L, L]
        
        return torch.matmul(self.dropout(weights), V), weights

    def forward(self, Q_in, K_in, V_in, mask=None):
        B = Q_in.size(0)
        Q = self.W_q(Q_in).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K_in).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V_in).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
        attn_out, weights = self.attention(Q, K, V, mask)
        attn_out = attn_out.transpose(1, 2).contiguous().view(B, -1, self.d_model)
        return self.W_o(attn_out), weights

class FeedForwardNetwork(nn.Module):
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
    def forward(self, x):
        return self.linear2(self.dropout(F.gelu(self.linear1(x))))

class EncoderLayer(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)
        self.ffn       = FeedForwardNetwork(d_model, d_ff, dropout)
        self.norm1     = nn.LayerNorm(d_model)
        self.norm2     = nn.LayerNorm(d_model)
        self.dropout   = nn.Dropout(dropout)
    def forward(self, x, mask=None):
        attn_out, _ = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        ffn_out = self.ffn(x)
        return self.norm2(x + self.dropout(ffn_out))

class TransformerNewsClassifier(nn.Module):
    def __init__(self, vocab_size=50265, d_model=512, n_heads=8, n_layers=6, d_ff=2048, num_classes=8, max_len=1024, dropout=0.1):
        super().__init__()
        self.embedding  = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc    = PositionalEncoding(d_model, max_len, dropout)
        self.layers     = nn.ModuleList([EncoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)])
        self.norm       = nn.LayerNorm(d_model)
        self.classifier = nn.Linear(d_model, num_classes)
    def forward(self, x, mask=None):
        x = self.pos_enc(self.embedding(x))
        for layer in self.layers: x = layer(x, mask)
        return self.classifier(self.norm(x).mean(dim=1))

if __name__ == "__main__":
    print("Transformer Architecture loaded.")
    m = TransformerNewsClassifier(d_model=512, n_heads=8, n_layers=6, d_ff=2048)
    print(f"Base model parameters: {sum(x.numel() for x in m.parameters()):,}")
