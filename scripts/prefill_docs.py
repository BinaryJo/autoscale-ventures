#!/usr/bin/env python3
import os, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG_FILE = ROOT / "ops" / "config" / "worker_urls.json"

TOKENS = {
    "SLUGIFY_URL":   ("infra/site/posts/slugify-tool.html",      r"\{\{SLUGIFY_URL\}\}"),
    "CSV2JSON_URL":  ("infra/site/posts/csv-to-json.html",       r"\{\{CSV2JSON_URL\}\}"),
    "TZSLOTS_URL":   ("infra/site/posts/timezone-slots.html",    r"\{\{TZSLOTS_URL\}\}"),
    "SCHEDULE_URL":  ("infra/site/posts/recurring-schedule-generator.html", r"\{\{SCHEDULE_URL\}\}"),
}

def load_config():
    cfg = {}
    if CFG_FILE.exists():
        try:
            cfg = json.loads(CFG_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[prefill] WARN: cannot read {CFG_FILE}: {e}")
    for k in list(TOKENS.keys()):
        if os.getenv(k):
            cfg[k] = os.getenv(k)
    return cfg

def patch_file(path: Path, token_pattern: str, replacement: str) -> bool:
    txt = path.read_text(encoding="utf-8")
    new = re.sub(token_pattern, replacement, txt)
    if new != txt:
        path.write_text(new, encoding="utf-8")
        return True
    return False

def main():
    cfg = load_config()
    changed = False
    for key, (rel, pat) in TOKENS.items():
        p = ROOT / rel
        if not p.exists():
            print(f"[prefill] missing page: {rel}")
            continue
        url = cfg.get(key, "").strip()
        if url:
            if patch_file(p, pat, url):
                print(f"[prefill] updated {rel} with {key} = {url}")
                changed = True
        else:
            print(f"[prefill] {key} not provided; leaving placeholder in {rel}")
    print("[prefill] done; changes:", changed)

if __name__ == "__main__":
    main()
