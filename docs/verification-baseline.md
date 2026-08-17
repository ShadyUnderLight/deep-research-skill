# Verification baseline (issue #375)

This document records the pytest collection scope and the reasoning behind
every exclusion, so that "CI green" and "local `python3 -m pytest -q` green"
mean the same thing.

## Primary commands

- `python3 -m pytest -q` — full suite (the CI primary gate).
- `python3 -m pytest --collect-only -q` — shows the collection scope.
- `python3 scripts/test_validator_regression.py` — CLI runner for the
  validator regression set (also collected by pytest; both styles coexist).
- `python3 scripts/test_cjk_pdf_pipeline.py` — CLI runner for the CJK PDF
  pipeline checks (needs Chromium; runs in the CI `smoke` job).
- `bash scripts/validate-docs-structure.sh`
- `python3 scripts/validate_route_manifest.py`
- `python3 scripts/validate_eval_registry.py`
- `python3 scripts/run_forward_evals.py --offline --check-baseline`
- `actionlint .github/workflows/ci.yml` (CI `workflow-lint` job)

## Collection scope

Configured in `pyproject.toml` (`[tool.pytest.ini_options]`):

| Path | Collected? | Why |
|---|---|---|
| `tests/test_*.py` | yes | Formal pytest modules. |
| `scripts/test_*.py` | yes | Validator regression/contract tests. Many also expose a `main()` CLI entry; pytest and CLI run the same assertions. |
| `scripts/validate_*.py`, `scripts/*.py` without `test_` prefix | no | Validators/renderers, exercised through the tests above. |
| File-based CJK pipeline checks (`scripts/test_cjk_pdf_pipeline.py::_test_file_pipeline`) | no | Parameterized by a file list inside `main()`; cannot be collected by pytest. Renamed with `_` prefix so pytest never collects it. Run via the CLI in the `smoke` job. |

`addopts = "-ra --strict-markers"`:

- `-ra` — summary distinguishes failed vs errored tests (collection/fixture
  errors are reported as `ERROR`, so CI can classify failure kinds).
- `--strict-markers` — any unregistered marker fails the run (fail-closed).

## Excluded on purpose

- No conftest/pytest config beyond `pyproject.toml`.
- The `smoke` job's browser-dependent checks are not pytest tests; they are
  explicit steps in `.github/workflows/ci.yml`.
- Markdown/docs/eval-case files are not Python; they are covered by
  `scripts/validate-docs-structure.sh` and the eval contract tests.
- The executable forward-eval subset is stored in `evals/registry.json` and
  replays local report/Research Pack snapshots without paid models or external
  search channels.

## CI layout (`.github/workflows/ci.yml`)

- `pytest` — full pytest suite from `requirements.lock`; the primary gate.
- `cli-checks` — per-script CLI runs, supplements the pytest gate.
- `workflow-lint` — actionlint validation of the workflow itself.
- `smoke` — Chromium/PDF pipeline checks.

Push triggers use `branches: [main]` (explicit; `[$default-branch]` was a
literal string that never matched). Python 3.12 + `requirements.lock`
(regenerate: `pip install -r requirements.txt && pip freeze`).

## Dependency reproducibility

`requirements.lock` pins the full transitive closure. Keep
`requirements.txt` as the human-readable minimum-version entry point.
Documented compatibility: Python 3.12 (CI) / 3.14 (local), Playwright pinned
in the lock — Chromium binaries are downloaded per Playwright version.
