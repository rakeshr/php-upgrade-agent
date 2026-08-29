"""Known PHP 8.3+ compatibility rules (deprecated / removed constructs)."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern[str]
    message: str
    severity: str = "error"
    target_php: str = "8.3"


RULES: list[Rule] = [
    Rule(
        id="create_function",
        pattern=re.compile(r"\bcreate_function\s*\("),
        message="create_function() was removed in PHP 8.0; use anonymous functions",
        severity="error",
    ),
    Rule(
        id="mysql_extension",
        pattern=re.compile(r"\bmysql_(connect|select_db|query|fetch_array|fetch_assoc|fetch_row|num_rows|real_escape_string|close|pconnect|error|errno)\s*\("),
        message="mysql_* functions were removed in PHP 7.0; use mysqli or PDO",
        severity="error",
    ),
    Rule(
        id="each",
        pattern=re.compile(r"\beach\s*\("),
        message="each() was removed in PHP 8.0; use foreach",
        severity="error",
    ),
    Rule(
        id="utf8_encode",
        pattern=re.compile(r"\butf8_(encode|decode)\s*\("),
        message="utf8_encode/decode deprecated in 8.2, removed in 8.4; use mb_convert_encoding",
        severity="warning",
    ),
    Rule(
        id="strftime",
        pattern=re.compile(r"\bstrftime\s*\("),
        message="strftime() deprecated in PHP 8.1; use IntlDateFormatter or DateTime::format",
        severity="warning",
    ),
    Rule(
        id="dollar_brace_var",
        pattern=re.compile(r"\$\{[a-zA-Z_][a-zA-Z0-9_]*\}"),
        message="${var} string interpolation deprecated in PHP 8.2; use {$var}",
        severity="warning",
    ),
    Rule(
        id="implicit_nullable",
        pattern=re.compile(
            r"function\s+\w+\s*\([^)]*\b(?:string|int|float|bool|array|object|callable|iterable)\s+\$\w+\s*=\s*null"
        ),
        message="Implicit nullable parameter types deprecated in PHP 8.4; use ?Type",
        severity="warning",
    ),
    Rule(
        id="filter_sanitize_string",
        pattern=re.compile(r"FILTER_SANITIZE_STRING\b"),
        message="FILTER_SANITIZE_STRING removed in PHP 8.1; use htmlspecialchars or custom filter",
        severity="error",
    ),
]

RULE_BY_ID = {rule.id: rule for rule in RULES}
