# Deploy the tested Streamlit app

No production URL has been created. GitHub and compatible hosting access were not established in this session. Available Sites hosting supports static/Worker applications, not this Python Streamlit server, so we retained the requested stack. An installed, authorized GitHub/Streamlit integration was not available. The source package is complete enough to run independently.

## Streamlit Community Cloud route

1. Sign in to a **team-owned GitHub account or organization**. Create a repository, for example `team-thu-flame`. Keep this project folder's contents at the repository root, including `.streamlit/config.toml`, `data/`, `requirements.txt`, license and documentation. Do not upload `.venv`, secret files, logs or private preparation materials. A public source repository is a practical option for judge review after the team checks the content.
2. Sign in to https://share.streamlit.io/ using the team's account. Authorize only the intended repository. Review any account/hosting terms yourselves.
3. Choose **Create app**, the repository and branch, and entrypoint **app.py**. In advanced settings choose **Python 3.12**. No secrets are required. Keep the privacy configuration committed; do not disable CORS/XSRF to fix deployment problems.
4. Deploy, then open the actual URL in a signed-out/private browser. Check Ask → smoke question → SAME-R → NASA source, Explore filters, Compare, and an unsupported question. Test a phone or a 390-pixel-wide browser viewport. Record the URL and any host analytics/cookies actually observed.
5. Set the demo's visibility so judges can access it without your account. Inspect the host privacy notice and update `app.py` and `PRIVACY_SECURITY.md` before sharing. A private preview is not sufficient for signed-out judges.
6. Replace the missing links in `SUBMISSION_DRAFT.md` only with the URLs you tested. The demo-video link and final-project link may be different fields; check the current official form.

Official instructions reviewed:

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-analytics

If a button label has changed, follow the equivalent repository/branch/entrypoint flow in the current documentation. Do not put an API key in a repository, URL, issue, chat or screenshot.

## Verify before publication

Run `python -m unittest discover -s tests -v` in the app environment. In a separate tooling environment install `pip-audit` and `detect-secrets`, then audit the complete `requirements.txt` and scan the source and every commit. Inspect findings, fix confirmed issues and rerun the affected checks. The included reports describe this build; rerun after dependency or code changes.

The remaining deployment inputs are the **team repository URL**, authorized access to a **Streamlit-compatible host**, and a **tested public demo URL**. An AI API key is not needed for the current release.
