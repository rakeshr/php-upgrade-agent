# HOT_TAKE

**You do not need phpcs to ship a useful PHP upgrade preflight for WordPress agencies.**

The industry default — PHPCompatibility sniffs via `phpcs` — is the right long-term answer for exhaustive standards coverage. It is the wrong default for a **Friday-afternoon go/no-go check** before a host flips PHP on Monday:

1. **It needs PHP installed** and tuned sniff paths; agency laptops are heterogeneous.
2. **It hangs** on large `vendor/` + ACF + Woo trees — exactly the sites that scare you most.
3. **Its output is not client-ready** without another formatting pass.

A hybrid **Python tokenizer + small rule pack + verify pass** gets you 80% of the value in 20% of the complexity for the *specific* question agencies ask: “Will this site white-screen on 8.3?”

The abandoned WP Engine checker died because it tried to be exhaustive in one browser request. This agent inverts that: **narrow rules, fast scan, explicit false-positive handling, client report.**

The next step is not more regex — it is **WordPress-shaped context** (hook registrations, `$wpdb->prepare`, block theme `theme.json` PHP snippets). But that should be a second rule pack, not a reason to drag phpcs into v1.

Optional LLM refinement is for narrative (“tell the client why `each()` matters”), not detection. Detection must stay deterministic for CI.
