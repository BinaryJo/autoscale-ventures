# Brain Bridge — Implementation Plan (v0.1)

## 1) Architecture stack decisions
- **Frontend:** Flutter 3.x (Dart) with Riverpod/Bloc, go_router navigation, Isar/SQLite offline cache, platform channels for system calendars/notifications. UI kit includes high-contrast + low-stimulation themes, typography scales, and reduced-motion defaults.
- **Backend:** FastAPI gateway + Python-based microservices; async I/O via httpx/asyncpg. gRPC/Protobuf contracts for connectors and AI orchestrator. Background jobs with Celery/Redis or Temporal for durable workflows (sync, summaries).
- **Data stores:** PostgreSQL (RLS per user), Redis (cache/queues), S3-compatible blob store (attachments, transcripts), optional Qdrant/pgvector for semantic search.
- **Identity & auth:** OAuth 2.0/OIDC (PKCE) for all external providers; first-party auth via email/pass or passkey; device binding with refresh-token rotation. Fine-grained consents stored as signed grants.
- **AI layer:** Pluggable providers (OpenAI, Anthropic, Vertex) behind a safety middleware that enforces redaction templates and role-specific guardrails. SSE/WebSocket streaming to clients.

## 2) Core workstreams
1. **Identity & consent** — implement auth service, consent ledger, device trust, and care-team roles (owner, supporter, clinician-readonly).
2. **Connector SDK** — shared base client (retry, backoff, scope minimization, webhook handling) plus provider adapters (Google, Microsoft Graph, Slack/Teams, Zoom/Meet, Drive/Dropbox/Box, Notion).
3. **Messaging & calendar bridge** — unified inbox + calendar APIs, conflict resolution, buffer-time rules, triage labels, and multi-account routing.
4. **Tasks/routines & journaling** — CRUD APIs, offline sync, mood tags, export pipelines, and routine templates tuned for ASD/ADHD/CPTSD/anxiety/depression use cases.
5. **Meetings & captions** — pre-call checklist, live transcription (cloud first, device fallback), summary generation with safety filters.
6. **AI co-pilot** — context fetcher that requires explicit user confirmation before data use; prompt library for personas; safety classifier before returning responses.
7. **Experience system** — sensory presets, notification pacing, grounding toolkit, and crisis shortcuts.
8. **Reliability & observability** — OpenTelemetry traces/metrics, privacy-aware logs, chaos tests on sync flows, synthetic monitors for connector health.

## 3) API surface (v1 sketch)
- `POST /v1/auth/oauth/start|callback` — provider onboarding with PKCE + consent scopes.
- `GET /v1/accounts` — list linked accounts; includes sensory preference profile per account.
- `GET /v1/mail` / `POST /v1/mail/triage` — fetch/label emails with AI recommendations and user override signals.
- `GET /v1/calendar/events` / `POST /v1/calendar/sync` — two-way sync, buffer enforcement, and conflict resolution.
- `GET|POST /v1/tasks` — tasks and routines with pacing hints.
- `GET|POST /v1/journal` — encrypted notes, mood tags, export options.
- `POST /v1/meetings/summarize` — summaries with trigger filtering and redaction logs.
- `POST /v1/ai/chat` — chat with consented context retrieval; persona + safety flags in payload.

## 4) Data model highlights
- **User** (id, diagnosis tags, sensory preset, crisis contacts, consent flags).
- **AccountConnection** (provider, scopes, tokens, consent grant id, last sync cursor, status).
- **MailItem/CalendarEvent/Task/Note** with `origin_provider`, `sensitivity`, `redaction_policy`, `synced_at`, and optional `care_team_visibility`.
- **ConsentGrant** (actor, resource type, scope, expiry, signed hash, audit trail).
- **AIInteraction** (persona, prompt hash, redaction summary, provider used, safety verdict, tokens).

## 5) Safety-by-design measures
- Default deny for sharing context into AI; per-request confirmation with visible redaction preview.
- Safety classifier on AI outputs; blocklists for clinical or crisis directives; escalation copy shown only after user opt-in.
- Data residency configuration; encryption at rest and in transit; key rotation and hardware-backed storage on device.
- Human-in-the-loop option for clinicians/supporters to review summaries before sharing.

## 6) Delivery milestones & owners (suggested)
- **M0-M1:** Auth/consent foundations, Google Workspace + Microsoft Graph mail/calendar connectors, journaling MVP. Owner: Platform.
- **M2:** Unified inbox + calendar bridge, routines engine, AI co-pilot with redaction, Flutter shell with accessibility presets. Owners: Product + Mobile.
- **M3:** Meeting assistant (captions + summaries), storage connectors (Drive/Dropbox/Box), care-team roles, safety classifier GA. Owners: Product + AI.
- **M4:** HealthKit/Fit optional sync, Web/PWA beta, reliability/SLO targets, crisis toolkit refinement. Owners: Platform + Mobile.

## 7) Testing & QA
- Contract tests for each connector using recorded fixtures and scope-enforcement tests.
- E2E mobile tests with Flutter integration test + golden image comparisons for accessibility modes.
- Load tests for inbox/calendar sync; fuzz tests for consent parsing; red-team prompts for AI safety layer.

## 8) Rollout & analytics
- Feature flags per connector and AI persona; staged rollouts with kill-switches.
- Metrics: success/failure per sync job, AI safety deflections, routine completion rate, dwell time in calming modes, DAU/WAU retention.
- Qualitative: in-app surveys focused on overwhelm reduction and comprehension; support ticket volume by category.

## 9) Open risks & mitigations
- **Provider limits/quotas:** implement adaptive rate limiting and backoff; cache aggressively; graceful degradation notices.
- **Crisis liability:** strong disclaimers, no autonomous outreach; partner with crisis orgs for referral links.
- **Data locality/compliance:** partition deployments by region; optional on-device-only journaling mode.
- **AI drift/latency:** model-agnostic orchestration with health checks; caching + partial responses when context is large.
