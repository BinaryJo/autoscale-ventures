from datetime import datetime
from .trend_scout import propose_topics
from .product_forge import plan_assets, build_assets
from .publisher import deploy_assets
from .growth_ops import syndicate
from .analytics import capture_kpis
from .finance_guard import spending_locked, evaluate_unlocks, disable_llm

def main():
    print("[orchestrator] start", datetime.utcnow().isoformat())
    if spending_locked():
        disable_llm()
        print("[finance] spending locked; running in zero-cost mode")
    topics = propose_topics(limit=3)
    print(f"[trend_scout] proposed topics: {topics}")
    for brief in topics:
        plan = plan_assets(brief)
        artifacts = build_assets(plan)
        deploy_assets(artifacts)
        syndicate(artifacts)
    capture_kpis()
    evaluate_unlocks()
    print("[orchestrator] done")

if __name__ == "__main__":
    main()
