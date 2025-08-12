# AGENTS

## Guidelines
- Keep pull requests small and focused.
- Do not introduce any Db2 dependencies.
- Use only z/OSMF Jobs and Files APIs; avoid other z/OS services.
- Update the PR description with the checklist below.

## PR Checklist
- [ ] `ruff .`
- [ ] `black --check .`
- [ ] `pytest`
