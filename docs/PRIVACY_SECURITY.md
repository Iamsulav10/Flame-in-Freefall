# Privacy, cookies and security

## Current behavior

The application processes the question on its Python server and keeps the current question, answer and request timestamps in Streamlit session state. The app adds no database, accounts, uploads, advertising, analytics code or query logs. It does not intentionally persist these values to disk. Exact memory cleanup depends on the framework session lifecycle; this is not a retention guarantee.

No external AI provider is implemented, configured or called. API usage and model spend are zero for this release. ChatGPT/Codex assistance during development is a separate activity disclosed in `AI_ASSISTANCE.md`.

Optional framework usage statistics are disabled in `.streamlit/config.toml`. CORS and XSRF protections stay enabled. Installed Streamlit 1.67.0's configuration describes an XSRF security cookie and SameSite=Lax. Initial HTTP cookie observations are in `reports/http-check.json`; they do not establish every browser or host cookie. Do not turn off XSRF merely to remove a cookie.

Community Cloud separately documents viewer analytics, including counts and recent viewer activity. Its analytics, logs, cookies and retention cannot be inferred from our app configuration. No public host or live retention settings were inspected. Before publishing, inspect the actual host's privacy documentation and cookies, update the notice in `app.py`, and determine whether an optional-cookie consent choice is needed. The current local build adds no optional-cookie consent banner because it adds no optional tracking. This is not a legal determination for an unconfigured host.

Sources:

- https://docs.streamlit.io/develop/api-reference/configuration/config.toml — usage statistics, CORS/XSRF, SameSite and error-detail options; rechecked against installed code.
- https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-analytics — host viewer analytics; reviewed 14 November 2026.

## Controls implemented

- Questions have a 600-character limit in the UI and retrieval function. Ask allows at most 10 submissions per minute per session, with a 2-second minimum gap. This limits accidental repetition; opening new sessions bypasses it. Host-level connection limits would still be needed for a large public service.
- The app reads only the packaged evidence JSON. It does not fetch visitor-supplied URLs, execute commands, load uploaded files, or give a model access to a shell or secrets.
- NASA source URLs use HTTPS and a specific hostname allowlist. User and claim bodies render as plain text. They are never passed to HTML, eval or a command interpreter.
- The optional future selector interface accepts only existing claim IDs. Fault-injection tests prove its errors and invalid selections fall back to local evidence. It is not a working provider integration or a live outage test.
- Public framework error details are disabled. Loading errors produce a short message. The fallback never displays exception strings that could include sensitive data.
- `.streamlit/secrets.toml`, environment files, environments and logs are excluded from Git. This version needs no secret. Never paste credentials into chat or screenshots.
- Dependencies are pinned. The runtime audit and source/history scans are documented in `reports/VALIDATION.md`.

## If adding an external AI service later

Choose a provider and verify its current API data-use/retention terms before implementation. Explain exactly what question and evidence text are sent. Use a server-side secret store, a fixed approved API endpoint, bounded response tokens and timeout, a global daily cost budget plus per-session limits, no tools, and a structured list of approved claim IDs. Do not accept generated scientific claims merely because they carry a citation. Test timeout, malformed output, invalid IDs, budget exhaustion, injection and redacted errors before enabling it. Keep local retrieval available when disabled or unavailable. Update both the privacy notice and AI disclosure with the integration actually used.

Known-advisory and secret-pattern scans are limited checks. They do not prove zero vulnerabilities or protection against all future attacks.
