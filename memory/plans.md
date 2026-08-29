# Plans & decisions

## Architecture

- **Baseline vs agent**: Baseline is intentionally noisy (regex on raw text). Agent adds token-aware `scan_tokens` plus a verify pass that drops comment/string false positives.
- **No phpcs**: Rejected for v1 — hangs on large WP trees and needs PHP installed. Hypothesis: Python tokenizer + verify pass is enough for the fixture pack.
- **No required LLM**: Agent loop is deterministic. Optional OpenAI refinement deferred; eval must pass without keys.
- **Scoring**: File-level F1 on `(file, rule_id)` pairs from `fixtures/expected.json`.

## Iterations tried

1. Baseline-only regex — fast but unacceptable false positives on `false_positive_comment.php`.
2. Token-aware scan — fixed most comment/string FPs; agent F1 > baseline.
3. **Removed experiment**: Running baseline first and unioning all hits without verify — recall matched agent but precision collapsed; dropped.

## Next (post-v1)

- Optional `OPENAI_API_KEY` pass to re-rank uncertain findings.
- WordPress-specific rules (e.g. `$wpdb->prepare` misuse) as separate rule pack.
- SARIF export for CI.
