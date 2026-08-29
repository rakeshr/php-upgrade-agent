# REPRODUCE

One-command reproduction of eval scores from a clean checkout.

## Requirements

- Python 3.11+
- No API keys
- No PHP runtime (scanner is pure Python)

## Steps

```bash
git clone https://github.com/rakeshr/php-upgrade-agent.git
cd php-upgrade-agent
python3 -m pip install -e ".[dev]"
php_upgrade_agent eval
pytest -q
```

## Expected output

Eval prints a table; agent F1 should exceed baseline F1:

```
Metric          | Baseline | Agent | Change
----------------+----------+-------+-------
F1              | 0.821    | 1.000 | +0.179
Precision       | 0.696    | 1.000 | +0.304
Recall          | 1.000    | 1.000 | +0.000
...
```

`artifacts/eval.json` contains full finding lists and per-mode metrics.

## Manual smoke tests

```bash
# Noisy but fast
php_upgrade_agent baseline fixtures/false_positive_comment.php

# Should report zero issues (comment/string only)
php_upgrade_agent agent fixtures/false_positive_comment.php

# Multi-issue legacy plugin
php_upgrade_agent agent fixtures/multi_issue.php
```

## Trajectories

After `php_upgrade_agent agent fixtures/`, inspect:

```
artifacts/trajectories/agent_fixtures.json
```

Each step (`list_php_files`, `scan_tokens`, `verify`, `write_report`) is logged with payloads.
