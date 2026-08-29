# AGENTS.md

Guidance for coding agents working in this repository.

## Project

Standalone **PHP Upgrade Agent** for WordPress agencies evaluating PHP 8.3/8.4 readiness. Python 3.11+ CLI with three modes: `baseline`, `agent`, `eval`.

## Layout

- `src/php_upgrade_agent/` — package (`cli.py`, `baseline.py`, `agent.py`, `rules.py`, `php_tokenizer.py`, `eval_runner.py`)
- `fixtures/` — labeled PHP cases + `expected.json`
- `tests/` — pytest (fixture pack F1 regression)
- `artifacts/` — eval output and agent trajectories (gitignored)
- `memory/` — agent progress log and decision record

## Commands

```bash
python -m pip install -e ".[dev]"
php_upgrade_agent baseline fixtures/
php_upgrade_agent agent fixtures/
php_upgrade_agent eval
pytest
```

## Conventions

- Default path is **deterministic** — no API keys required.
- Optional `OPENAI_API_KEY` may be wired later for LLM refinement; do not make it required for eval.
- Match existing style: small modules, dataclasses, typed functions.
- When adding rules, update `rules.py`, fixtures, and `expected.json` together.
- Run `php_upgrade_agent eval` after rule changes; agent F1 must stay above baseline.

## Do not

- Copy WP Guru / WPG PHP Scanner code.
- Commit secrets or `artifacts/` outputs.
- Invent eval scores in README — run eval and paste real numbers.
