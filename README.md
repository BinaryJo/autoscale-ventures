# AutoScale Ventures — v2 Template

Updated template with four Workers (slugify, csv2json, tzslots, schedule),
OpenAPI specs, landing pages, daily orchestrator, and principal-protection guardrails.

## Quickstart
1) Fork repo and add optional secrets (SUPABASE_URL/KEY, CF_API_TOKEN, etc.).
2) Enable **Daily Orchestrator** workflow.
3) (Optional) Deploy Workers with `npx wrangler deploy` in each worker folder.

## Zero-Dependency Note
This build avoids non-stdlib dependencies so it runs in this environment. FinanceGuard reads JSON policy.
