# AI Dataset Health for z/OS — Proposal

## Project Name
**ai-dataset-health-zos**

## Description
Small, open-source Python tool that:
- Lists repository files (future: z/OS datasets via z/OSMF)
- Computes a simple **dataset health score** (zero-byte rule)
- CLI (`list_files.py --health`) with readable output
- CI: Ruff, Black, MyPy, Pytest (coverage), health smoke artifact

## Problem / Motivation
Teams lack lightweight, open, CI-friendly dataset health checks. This provides an approachable baseline that can evolve to z/OSMF + AI.

## Current Status (MVP)
- File listing with include/exclude, `max_depth`, hidden handling  
- `compute_health()` + `--health` flag  
- CI gates (≥80% coverage) + smoke artifact

Repo: https://github.com/marbatis/ai-dataset-health-zos

## Roadmap
- 0–3 mo: more rules; JSON output; mock z/OSMF in tests  
- 3–6 mo: z/OSMF (Jobs & Files) in OMP env; small ONNX scoring  
- 6–12 mo: dashboards; contributor docs

## License
Apache-2.0

## Maintainers
- **Marcelo Silveira** (@marbatis)

## Community Benefits
Minimal starting point for dataset health on Z; CI-first; open to extensions and AI integration.

## Resources Requested
OMP open z/OS env (z/OSMF) and a Slack channel

## Proposal Type
**Sandbox**
