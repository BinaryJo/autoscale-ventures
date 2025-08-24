import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KPIS = ROOT / "ops" / "kpis"

def capture_kpis():
    KPIS.mkdir(parents=True, exist_ok=True)
    snapshot = {"ts": datetime.utcnow().isoformat(),"pageviews": 0,"api_calls": 0,"revenue_today": 0.0,"mrr": 0.0,"notes": "baseline snapshot v2"}
    out = KPIS / f"kpi-{datetime.utcnow().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"[analytics] kpi snapshot saved -> {out}")
