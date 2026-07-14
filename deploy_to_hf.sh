#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
#  deploy_to_hf.sh — Deploy News Classifier to Hugging Face Spaces
#
#  Usage:
#    export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
#    bash deploy_to_hf.sh
# ──────────────────────────────────────────────────────────────────────────────
set -e

HF_USER="Gaurav2212"
SPACE_NAME="news-classifier"
REPO_ID="${HF_USER}/${SPACE_NAME}"
HF_REMOTE="https://huggingface.co/spaces/${REPO_ID}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 News Classifier — Deploy to Hugging Face Spaces"
echo "  Space: https://huggingface.co/spaces/${REPO_ID}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Check HF_TOKEN ──────────────────────────────────────────────────────────
if [ -z "$HF_TOKEN" ]; then
  echo ""
  echo "❌  HF_TOKEN is not set."
  echo ""
  echo "  1. Go to: https://huggingface.co/settings/tokens"
  echo "  2. Create a token with WRITE access"
  echo "  3. Run:  export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx"
  echo "  4. Then re-run this script"
  exit 1
fi

echo ""
echo "✅  HF_TOKEN found."

# ── Create the Space (idempotent) ───────────────────────────────────────────
echo ""
echo "📡  Creating / verifying Space on Hugging Face..."
"${PROJECT_DIR}/.venv/bin/python" "${PROJECT_DIR}/create_space.py"

# ── Set up Git remote ───────────────────────────────────────────────────────
cd "$PROJECT_DIR"
git config --global init.defaultBranch main 2>/dev/null || true

# Configure git identity if missing
if [ -z "$(git config user.email)" ]; then
  git config user.email "gauravyadav@users.noreply.huggingface.co"
  git config user.name "Gaurav Yadav"
fi

# Add or update the HF remote (embed token in URL for auth)
HF_REMOTE_AUTH="https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${REPO_ID}"
if git remote get-url hf-space &>/dev/null; then
  git remote set-url hf-space "$HF_REMOTE_AUTH"
  echo "🔄  Updated existing 'hf-space' remote."
else
  git remote add hf-space "$HF_REMOTE_AUTH"
  echo "➕  Added 'hf-space' remote."
fi

# ── Stage deployment files ──────────────────────────────────────────────────
echo ""
echo "📦  Staging files for deployment..."

git add \
  main.py \
  requirements.txt \
  Dockerfile \
  README.md \
  frontend/index.html \
  frontend/style.css \
  frontend/app.js

git status --short

# ── Commit ──────────────────────────────────────────────────────────────────
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
if git diff --cached --quiet; then
  echo ""
  echo "ℹ️   No changes to commit — files already up to date."
else
  git commit -m "deploy: News Classifier to HF Spaces [${TIMESTAMP}]"
  echo "✅  Committed."
fi

# ── Push to HF Spaces ────────────────────────────────────────────────────────
echo ""
echo "⬆️   Pushing to Hugging Face Spaces..."
echo "    (This triggers a Docker build — may take 3-10 minutes)"
git push hf-space HEAD:main --force

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅  DEPLOYED!"
echo ""
echo "  🌐 Space URL : https://huggingface.co/spaces/${REPO_ID}"
echo "  🏗️  Build logs: https://huggingface.co/spaces/${REPO_ID}/logs"
echo ""
echo "  The Space is now building the Docker image."
echo "  This will take ~5-10 minutes on first deploy (model download)."
echo "  Once status changes to '🟢 Running', your app is live!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
