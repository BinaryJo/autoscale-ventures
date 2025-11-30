# Brain Bridge — Product & Architecture Blueprint

## 1) Problem & goal
Neurodivergent and neurotypical users with diagnosed mental health conditions often bounce between Google Workspace (and competing suites), messaging tools, and AI helpers without a single, calming surface. Brain Bridge provides a unified, accessibility-first workspace with automation and AI support tuned for autism spectrum disorder (ASD), ADHD, CPTSD, anxiety disorder, and major depression, with a path to cover additional conditions.

## 2) Target users & accessibility principles
- Adults and adolescents with confirmed diagnoses who already use Google Workspace or alternatives (Microsoft 365, Zoho, Notion, Slack, etc.).
- Care teams (therapists, coaches, guardians) who need read-only or co-pilot access with tight consent controls.
- Accessibility guardrails: WCAG 2.2 AA, large tap targets, predictable navigation, offline-first notes, crisis shortcuts, sensory load controls (reduced motion/audio, color themes), optional plain-language summaries.

## 3) Cross-platform approach
- **Client stack:** Flutter 3.x for iOS, Android, macOS, Windows, and Linux; leverages a shared Dart codebase plus platform channels for OS-specific capabilities (notifications, keychain/KeyStore, file pickers).
- **Desktop packaging:** Use Flutter desktop builds for macOS/Windows/Linux; leverage Rust-powered plugins (via FFI) where low-latency encryption or file I/O is needed.
- **Distribution:** App Store, Play Store, Microsoft Store, side-loadable desktop binaries, and a Web build (PWA) for early testers.

## 4) Core feature set (v1)
- **Unified account hub:** OAuth connection manager for Google Workspace plus alternates (Microsoft 365/Outlook, Zoho Mail, Proton, Box/Dropbox/Drive, Slack/Teams, Zoom/Meet). Multi-account switching with profile-level sensory preferences.
- **Inbox + calendar bridge:** Priority inbox with AI triage, calming view options (reduced density), and calendaring that aligns with sensory needs (buffer times, daylight constraints). Two-way sync for events, tasks, and reminders.
- **Tasks & routines:** Lightweight task board with templates for recurring routines (meds, appointments, executive-function scaffolds). AI suggestions respect user-defined energy/overwhelm scales.
- **Notes & journaling:** Secure notes with offline mode, mood tagging, and optional AI-assisted rephrasing into therapist-friendly language. Export to Drive/Docs/Notion.
- **Meetings & live support:** Pre-call checklists, real-time captioning (device + cloud), and AI-generated summaries with trigger/overwhelm detection toggles.
- **AI co-pilot:** Chat interface that can pull context from connected services with explicit consent prompts and redaction rules. Supports "coach" (motivation), "scribe" (summaries), and "explainer" (plain-language) personas.
- **Safety & escalation:** Quick-access coping plans, emergency contacts, and optional geofenced crisis cards. No automated emergency outreach without explicit consent.

## 5) System architecture
- **Clients (Flutter):** State managed with Riverpod/Bloc; offline cache via SQLite/Isar; encrypted local vault for tokens (Keychain/KeyStore/DPAPI).
- **API gateway:** FastAPI (Python) fronting a gRPC microservice layer; rate limiting, audit logging, and schema validation (Pydantic v2). Deployable on Fly.io/K8s.
- **Service modules:**
  - *Auth & consent*: OAuth flows, PKCE, device verification, and signed data-sharing grants for care-team roles.
  - *Connector services*: Per-provider adapters for Google Workspace, Microsoft 365, Slack, Zoom, Notion, Box/Dropbox/Drive; webhook ingestion for Gmail/Outlook/Calendar/Slack.
  - *AI orchestration*: Policy layer that redacts PII, scopes documents by user consent, and supports pluggable LLMs (OpenAI/Anthropic/Vertex). Streaming responses via Server-Sent Events.
  - *Content safety*: Prompt templates that avoid clinical advice; lightweight sentiment/trigger detection; safety classifier before AI output reaches client.
  - *Engagement & routines*: Task engine, reminders, and routines scheduler with sensory-aware pacing.
- **Data layer:** PostgreSQL (primary), Redis for queues/caching, S3-compatible object store for attachments. Event bus via NATS/Redis Streams.
- **Observability:** OpenTelemetry traces/metrics, privacy-preserving logs with field-level redaction.
- **Security:** End-to-end TLS, encrypted secrets (SOPS), row-level security per user, periodic key rotation. Minimal scopes requested per connector.

## 6) Integrations (initial set)
- **Google Workspace:** Gmail, Calendar, Drive, Docs, Meet; use incremental sync via Gmail push notifications and Calendar webhooks.
- **Alternatives:** Microsoft 365 (Graph), Zoho Mail/Calendar, Proton Mail (Bridge), Slack/Teams messaging, Zoom/Meet, Box/Dropbox storage, Notion databases.
- **Health & journaling:** Apple HealthKit / Google Fit (opt-in), local-only mood tracking when health data is denied.
- **AI providers:** OpenAI GPT-4.x / GPT-4o, Anthropic Claude 3.x, Vertex PaLM as configurable backends; safety middleware keeps model choice transparent.

## 7) Data, consent, and safety
- No clinical diagnosis or emergency adjudication. AI outputs are framed as supportive, not medical directives.
- Consent ledger for every data access; explicit per-connector scopes; care-team roles default to read-only.
- User-controlled redaction templates (e.g., strip names/locations from AI context). Local-first storage of journals with cloud sync opt-in.
- Crisis UX shortcuts: grounding techniques, pre-written scripts, and optional sharing of current location with trusted contacts.

## 8) Personalization for focus & sensory needs
- Adjustable stimulation presets: "Calm", "Focused", "High contrast", "Low light"; per-context overrides (inbox vs. meetings).
- Executive function aids: chunked tasks, time-blindness helpers (progress bars, visual timers), body-doubling sessions via Meet/Zoom links.
- Predictable navigation with breadcrumbs, undo stacks, and delayed-send by default.

## 9) Deployment & environment strategy
- **Environments:** dev/staging/prod with separate projects and secrets; seed data limited to synthetic fixtures.
- **Mobile CI/CD:** Fastlane + GitHub Actions for signing, build, and store submissions. Feature-flagged rollouts and staged publish.
- **Backend CI/CD:** Lint, type-check, tests, SAST, and IaC validation. Blue/green deploys with canary users.

## 10) Phase roadmap
1. **Foundations (Month 0-2):** Identity/consent, Google Workspace + Microsoft 365 connectors, journaling + tasks, AI co-pilot with strict redaction, Flutter shell with accessibility presets.
2. **Collaboration (Month 3-4):** Care-team roles, meeting assistant (captions + summaries), routines scheduler, expanded storage connectors.
3. **Supportive automation (Month 5+):** Trigger detection tuning, proactive pacing suggestions, HealthKit/Fit integration, Web/PWA GA.

## 11) Success metrics (examples)
- Daily/weekly active users, streaks on routines, completion rates for scheduled tasks.
- Reduction in unread emails/events post-triage; time-to-join for meetings with checklists completed.
- Opt-in survey scores on overwhelm reduction and perceived control; crash-free sessions and latency SLAs.

## 12) Open questions
- Jurisdictional compliance scope (HIPAA/PHIPA/GDPR) based on launch markets.
- Preferred default LLM provider and on-device options for privacy-sensitive users.
- Care-team onboarding model (clinic partnerships vs. individual invites) and liability posture.
