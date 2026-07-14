# ── Base ──────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# HF Spaces requires the app to run as a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /home/user/app

# ── Dependencies ───────────────────────────────────────────────────────────────
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Pre-download the model so startup is instant ───────────────────────────────
# This bakes the model weights into the image (~1.6 GB).
# HF Spaces caches Docker layers, so this only downloads once.
RUN python -c "\
from transformers import pipeline; \
print('Downloading facebook/bart-large-mnli...'); \
pipeline('zero-shot-classification', model='facebook/bart-large-mnli'); \
print('Model cached.')"

# ── Application code ───────────────────────────────────────────────────────────
COPY --chown=user . .

# ── Runtime ────────────────────────────────────────────────────────────────────
# HF Spaces requires port 7860
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
