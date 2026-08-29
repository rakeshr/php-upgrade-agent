# FAILURE_MODE

Known ways this scanner fails or misleads — read before trusting a **GO** on production.

## False negatives (missed real issues)

| Mode | Risk |
|------|------|
| **Rule coverage** | Only eight constructs are checked. Undefined constants, PHP 8.4 property hooks, incompatible third-party binaries, and custom C extensions are invisible. |
| **Dynamic calls** | `call_user_func('mysql_connect', ...)` or `$fn = 'each'; $fn()` are not matched. |
| **Generated PHP** | Twig/Blade-compiled templates, webpack-inlined PHP, or minified deploy artifacts may hide patterns from the lexer. |
| **Double-quoted edge cases** | `${var}` is scanned inside `"` strings only. Complex interpolation (`"$foo{$bar[0]}"`) may be missed. |

## False positives (noise)

| Mode | Risk |
|------|------|
| **baseline** | Flags deprecated names in comments, docblocks, and strings. Use `agent` for real reports. |
| **`each` rule** | Matches `each(` in code; rare identifiers like a custom `each()` method on a non-array object are not semantically validated. |

## Operational limits

- **No runtime execution** — syntax-level static scan only; fatal errors from type mismatches at runtime are not detected.
- **No dependency graph** — composer packages in `vendor/` are scanned if present; there is no “reachable from WordPress bootstrap” analysis.
- **Encoding** — files read as UTF-8 with replacement; odd encodings may desync line numbers.
- **Scale** | Tested on the 12-file fixture pack. Very large trees (&gt;10k PHP files) are unbenchmarked; memory is proportional to file size per scan.

## When to escalate

If the agent reports **NO-GO**, fix listed issues and re-scan. If it reports **GO**, still run staging on the target PHP version with representative traffic — this tool reduces risk; it does not eliminate it.

## Reporting bugs

Add a minimal fixture under `fixtures/` with `expected.json` entry and a failing pytest assertion. That keeps F1 honest.
