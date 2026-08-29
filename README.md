# PHP Upgrade Agent

Standalone PHP upgrade readiness scanner for **WordPress agencies** deciding whether a client site is safe to move to **PHP 8.3 or 8.4**.

Built for the [micro1 Frontier Engineering Challenge 2026](https://www.hackerearth.com/challenges/hackathon/agentic-workflows-hackathon/) (HackerEarth Agentic Workflows Hackathon). Clean-room implementation — no WP Guru / WPG PHP Scanner code.

## Who & bottleneck

**User:** freelance and agency WordPress developers before a host-enforced PHP upgrade.

**Bottleneck:** WP Engine’s PHP Compatibility Checker is abandoned (timeouts, false positives). `phpcs` with PHPCompatibility rules hangs on real plugin trees. Pasting one file into ChatGPT misses the rest of the codebase. Clients then get a white screen on upgrade day.

**Why this repo:** a one-command, deterministic CLI that scans a plugin/theme directory, separates real code issues from comment/string noise, and emits a client-ready go/no-go report — without API keys.

## Primary metric

**F1** on labeled `(file, rule_id)` pairs in `fixtures/expected.json`, comparing:

| Mode | What it does |
|------|----------------|
| **baseline** | Naive regex over raw file text — fast, noisy |
| **agent** | Token-aware scan + verify pass — drops comment/string false positives |

Higher F1 with fewer false positives is the goal. Run `php_upgrade_agent eval` to reproduce.

## Results (fixture pack, cloud VM 2026-08-29)

| Metric | Baseline | Agent | Change |
|--------|----------|-------|--------|
| **F1** | 0.821 | **1.000** | +0.179 |
| Precision | 0.696 | 1.000 | +0.304 |
| Recall | 1.000 | 1.000 | 0.000 |
| True positives | 16 | 16 | 0 |
| False positives | 7 | 0 | −7 |
| False negatives | 0 | 0 | 0 |

The agent eliminates all seven baseline false positives (mostly deprecated API names mentioned only in comments or single-quoted strings) while keeping full recall on real issues.

## Quick start

```bash
python3 -m pip install -e ".[dev]"

# Fast noisy scan
php_upgrade_agent baseline path/to/plugin

# Token-aware agent + client report
php_upgrade_agent agent path/to/plugin

# Score baseline vs agent on fixtures
php_upgrade_agent eval
pytest
```

Outputs land in `artifacts/` (`eval.json`, `report.md`, `trajectories/*.json`).

**Judges:** committed representative traces are in `examples/` — `eval.json`, `report.md`, and `trajectories/agent_fixtures.json`.
These files come from a real run of `php_upgrade_agent eval` and `php_upgrade_agent agent fixtures/` in the cloud VM.
`artifacts/` stays gitignored for local runs; use `examples/` when reviewing on GitHub.

## Architecture

```
php_upgrade_agent baseline   →  regex rules on raw text
php_upgrade_agent agent      →  plan → list_php_files → scan_tokens → verify → write_report
php_upgrade_agent eval       →  same fixtures, F1 table, artifacts/eval.json
```

**Agent tools:** `list_php_files`, `read_file`, `scan_tokens`, `record_finding`, `mark_verified`, `write_report`.

**Rules (PHP 8.3+ target):** `create_function`, `mysql_*`, `each()`, `utf8_encode`/`utf8_decode`, `strftime`, `${var}` interpolation, implicit nullable parameters, `FILTER_SANITIZE_STRING`.

## Optional LLM refinement

Not required. The default agent loop is fully deterministic. You may set `OPENAI_API_KEY` in a future iteration to re-rank borderline findings; eval and CI should pass without it.

## Fixtures

12 labeled PHP files under `fixtures/` covering: `create_function`, `mysql_*`, `each()`, `utf8_encode`, `strftime`, `${var}`, implicit nullable, `FILTER_SANITIZE_STRING`, a clean file, a hard false-positive case, a WordPress plugin skeleton, and a multi-issue file.

## Docs

- [REPRODUCE.md](REPRODUCE.md) — one-command reproduction
- [CHANGELOG.md](CHANGELOG.md) — iteration history
- [HOT_TAKE.md](HOT_TAKE.md) — opinionated notes
- [FAILURE_MODE.md](FAILURE_MODE.md) — known limits
- [AGENTS.md](AGENTS.md) — coding-agent guidance

## License

MIT — see [LICENSE](LICENSE).
