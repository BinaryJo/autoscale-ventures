import os, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "ops" / "policies" / "finance.json"

def _policy():
    if POLICY.exists():
        return json.loads(POLICY.read_text(encoding="utf-8"))
    return {"spending_locked": True, "principal_usd": 100.0}

def spending_locked() -> bool:
    return bool(_policy().get("spending_locked", True))

def disable_llm():
    if "LLM_API_KEY" in os.environ:
        del os.environ["LLM_API_KEY"]

def evaluate_unlocks():
    print(f"[finance] current policy -> {_policy()}")
