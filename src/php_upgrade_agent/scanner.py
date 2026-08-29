"""Token-aware scanner used by the agent verify pass."""

from __future__ import annotations

from pathlib import Path

from php_upgrade_agent.models import Finding
from php_upgrade_agent.php_tokenizer import TokenKind, line_at_offset, tokenize_php
from php_upgrade_agent.rules import RULES, RULE_BY_ID


def _snippet_for_line(content: str, line_no: int) -> str:
    lines = content.splitlines()
    if not lines:
        return ""
    idx = max(0, line_no - 1)
    return lines[idx] if idx < len(lines) else ""


def scan_file_tokens(path: Path, root: Path) -> list[Finding]:
    rel = str(path.relative_to(root))
    content = path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []
    dollar_rule = RULE_BY_ID["dollar_brace_var"]
    for token in tokenize_php(content):
        if token.kind == TokenKind.CODE:
            rules = RULES
        elif token.kind == TokenKind.STRING and token.text.startswith('"'):
            rules = [dollar_rule]
        else:
            continue
        for rule in rules:
            if token.kind == TokenKind.CODE and rule.id == "dollar_brace_var":
                continue
            for match in rule.pattern.finditer(token.text):
                abs_offset = token.start + match.start()
                line = line_at_offset(content, abs_offset)
                findings.append(
                    Finding(
                        file=rel,
                        line=line,
                        rule_id=rule.id,
                        message=rule.message,
                        severity=rule.severity,
                        snippet=_snippet_for_line(content, line),
                        verified=True,
                    )
                )
    return findings


def scan_directory_tokens(target: Path) -> list[Finding]:
    target = target.resolve()
    findings: list[Finding] = []
    php_files = sorted(target.rglob("*.php"))
    if target.is_file() and target.suffix == ".php":
        php_files = [target]
        root = target.parent
    else:
        root = target
    for php_file in php_files:
        findings.extend(scan_file_tokens(php_file, root))
    return findings
