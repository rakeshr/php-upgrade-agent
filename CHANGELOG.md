# Changelog

All notable changes to this project are documented here.

## [0.1.0] — 2026-08-29

### Added

- **`baseline` command** — regex scan for eight PHP 8.3+ compatibility rules across `.php` files.
- **`agent` command** — deterministic tool loop with JSON trajectories in `artifacts/trajectories/`.
- **`eval` command** — F1 scoring on `fixtures/`; writes `artifacts/eval.json`.
- **12 fixture files** with `expected.json` gold labels.
- **Python PHP tokenizer** — splits source into code, comment, string, and heredoc regions.
- **Docs:** README, REPRODUCE, HOT_TAKE, FAILURE_MODE, AGENTS.md.

### Iteration 1 — baseline only

Shipped naive regex. Fast (full fixture pack &lt;100 ms) but **7 false positives** on the labeled set — mostly deprecated function names appearing in block comments and single-quoted documentation strings (`false_positive_comment.php`).

### Iteration 2 — token-aware agent

Added `scan_tokens` over code regions plus a verify pass that drops baseline-only hits in comments/strings. Agent reached **F1 0.933** — perfect precision but missed `${var}` inside double-quoted strings (tokenizer correctly excluded strings from generic rules).

### Removed experiment — baseline ∪ agent union

Tried merging all baseline hits with token hits without selective verify. Recall stayed at 1.0 but precision regressed to baseline levels. **Removed** — union without verify is not an upgrade path.

### Iteration 3 — interpolation-aware scan

Scan double-quoted strings for `${var}` only; keep other rules on code tokens. Final eval: **baseline F1 0.821 → agent F1 1.000** (16 TP, 0 FP, 0 FN).

### Optional LLM path

Documented but not implemented — eval must remain key-free for hackathon scoring.
