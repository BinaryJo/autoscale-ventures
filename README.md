# Brain Bridge

Brain Bridge is a cross-platform assistant (iOS, Android, desktop, and web) that connects Google Workspace and alternative suites
with an AI copilot to support people with neurodivergent and mental health diagnoses. The app focuses on guided tasking,
context-aware nudges, and safe data handling for autism spectrum disorder, ADHD, CPTSD, anxiety, and major depression, with
expansion planned for additional conditions.

## Project assets
- Product and architecture blueprint: `docs/brain-bridge/brain_bridge_blueprint.md`
- Delivery and implementation plan: `docs/brain-bridge/implementation_plan.md`

## Repository structure
- `docs/brain-bridge/` — planning and design documents
- `agents/` — automation agents and helpers
- `infra/` — static site assets and deployment artifacts
- `ops/` — operational guardrails and policies
- `scripts/` — utilities such as documentation prefill
- `data/` — supporting datasets (if any)

## Getting started
1. Install Python requirements: `pip install -r requirements.txt`
2. Review the blueprint and implementation plan in `docs/brain-bridge/`
3. Use the agents in `agents/` to prototype integrations and workflows
