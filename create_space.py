#!/usr/bin/env python3
"""
Creates the HF Space (if it doesn't exist) using the HF API.
Run this once with a valid HF_TOKEN.
"""
import sys
import os

try:
    from huggingface_hub import HfApi, create_repo
except ImportError:
    print("ERROR: huggingface_hub not installed. Run: pip install huggingface_hub")
    sys.exit(1)

HF_TOKEN   = os.environ.get("HF_TOKEN", "").strip()
HF_USER    = "Gaurav2212"
SPACE_NAME = "news-classifier"
REPO_ID    = f"{HF_USER}/{SPACE_NAME}"

if not HF_TOKEN:
    print("ERROR: Set HF_TOKEN environment variable first.")
    print("  export HF_TOKEN=hf_xxxxxxxxxxxxxxxx")
    sys.exit(1)

api = HfApi(token=HF_TOKEN)

print(f"Creating Space: {REPO_ID} ...")
try:
    url = create_repo(
        repo_id=REPO_ID,
        repo_type="space",
        space_sdk="docker",
        exist_ok=True,
        token=HF_TOKEN,
        private=False,
    )
    print(f"✅  Space ready: {url}")
except Exception as e:
    print(f"ERROR creating space: {e}")
    sys.exit(1)
