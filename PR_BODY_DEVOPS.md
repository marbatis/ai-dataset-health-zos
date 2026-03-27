**feat(ci): dev requirements, weekly health check, and RAT helpers**

**Why**
- Keep **CI green** and reproducible by separating dev tools from runtime deps.
- Provide a **weekly scheduled health run** (no heavy external calls) to surface regressions early.
- Make it easier for contributors to run the **RAT notebooks** locally.

**What changed**
- New: `requirements-dev.txt` with `ruff`, `black`, `pytest`, `nbstripout`.
- New: `.github/workflows/weekly-health.yml` — runs lint/format/tests weekly + uploads a small health artifact.
- Makefile (appended by this PR script): add `rat-setup`, `rat-notebooks`, `rat-notebooks-all` targets.
- CI: Install both runtime and dev requirements during the main workflow.

**How to validate**
- Local: `pip install -r requirements.txt -r requirements-dev.txt && ruff check . && black --check . && pytest -q`
- In GitHub: Workflows → run **Weekly health check** manually (workflow_dispatch).

**Notes**
- The weekly job does not call external data services; it only installs deps, lints, and runs unit tests.
