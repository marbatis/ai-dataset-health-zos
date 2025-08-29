# Contributing

Thanks for helping!

- Open PRs against `main`, keep them small.
- CI must pass: Ruff (lint), Black (format), MyPy (types), Pytest (coverage ≥ 80%).
- Add or adjust tests when behavior changes.

## Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -s -m "feat: change"
```

This adds a line like:

```
Signed-off-by: Your Name <you@example.com>
```

## Local checks

```bash
ruff check .
black .
mypy .
PYTHONPATH=. pytest -q
```
