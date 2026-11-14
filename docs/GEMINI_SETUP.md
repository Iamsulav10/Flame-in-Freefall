# Optional Gemini integration

## Before configuring
Revoke any key shared in chat. The exposed key was not used, saved or tested. Create a replacement privately in Google AI Studio; never put it in GitHub, source code or screenshots.

Google's current terms require API users to be 18+ and exclude API clients directed towards or likely accessed by under-18s. This public student-facing project needs an eligible deployment arrangement before enabling Gemini. A visitor checkbox is not a solution to that restriction. Free-tier clients also have regional restrictions (paid services required for users in EEA, Switzerland and UK). Keep public AI disabled until these are resolved.

## Configuration for an eligible deployment
Streamlit Community Cloud: open the app's Settings > Secrets. Locally use .streamlit/secrets.toml (already ignored by Git). Set these top-level values:

```toml
GEMINI_ENABLED = false
GEMINI_API_KEY = "REPLACE_PRIVATELY_WITH_NEW_KEY"
GEMINI_MODEL = "REPLACE_WITH_AVAILABLE_GENERATECONTENT_MODEL_ID"
```

Choose an available text model supporting the generateContent API and JSON output from your project's model list. Check its free-tier quota and pricing. No model has been live-tested here; an unsupported model safely falls back. Set GEMINI_ENABLED to true only for an eligible deployment with the new key. The app does not enable billing or accept Google terms for you.

Upload app.py, insights.py and gemini_client.py together to the repository root. Keep evidence.py, data and requirements.txt. Upload the accompanying docs, tests and reports. No new dependencies. Run `python -m streamlit run app.py` locally.

## Actual journey
Ask > enter the smoke-detection demo question > select the explicit Gemini transmission checkbox > Find evidence. Confirm the label says Gemini-generated synthesis and inspect the citation links. Without opt-in, the request stays local. An error, quota limit, bad model or invalid response shows local evidence instead. Seeing the fallback does not prove an AI call succeeded.

## Security and privacy
Only the question and selected approved records (text, context, type, source ID and locator) are sent to Google's fixed HTTPS endpoint. The key is in an HTTP header, never the URL or model context. Redirects are rejected. There are no model tools, browsing, file uploads or shell access. Neither prompts nor provider exceptions are intentionally logged by application code.

Input: 600 characters. Existing session limit: 10 searches/minute with a 2-second interval. Additional AI limit: 5 attempts/minute and 100/day per Python process; attempts count even when they fail. These limits reset on restart and are not an account-wide billing cap. Provider quotas still apply. Output: 1800 tokens, 64 KiB response maximum, 20-second socket timeout, no automatic retries. Hosting logs and Google processing are separate.

Free-tier input/output can be used for product improvement and human review. Google's abuse-monitoring documentation specifies 55-day retention for prompts, context and output; this does not establish a universal deletion period for all processing. Do not send personal, confidential or sensitive data.

Output must contain 1–5 short typed statements with allowed claim IDs and a limitation. Unknown IDs, new numeric tokens, links/HTML, malformed responses and incomplete generations are rejected. This validation does NOT prove scientific entailment or eliminate prompt injection/hallucinations. Review the visible underlying evidence. Ranking stays deterministic; AI writes summaries and interpretations only.

## Validation and limits
Automated provider tests use mocked responses, not a real API. Live model availability, authentication, provider quota and output quality remain untested. Deployed and mobile visual tests remain pending. The earlier dependency audit applies: requirements unchanged, no new packages.

## Official references checked 15 November 2026 Nepal time
- https://ai.google.dev/api/generate-content
- https://ai.google.dev/gemini-api/terms
- https://ai.google.dev/gemini-api/docs/usage-policies
- https://ai.google.dev/gemini-api/docs/pricing
