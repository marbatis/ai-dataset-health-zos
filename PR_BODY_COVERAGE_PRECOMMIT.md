**feat(tooling): coverage gate & pre-commit hooks**

**Why**
- Enforce a basic test coverage floor and prevent noisy notebook diffs in PRs.
- Make formatting/linting consistent pre-commit.

**Changes**
- Add **pytest-cov** and **pre-commit** to dev deps.
- Configure **coverage** via `pyproject.toml` addopts (80% floor).
- Add `.pre-commit-config.yaml` with **black**, **ruff --fix**, **nbstripout**, and basic hygiene hooks.
- Makefile targets: `precommit-install`, `precommit-run`.
- (Optional) Instructions to upload coverage XML in CI.

**How to use**
```bash
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
pytest -q
```
