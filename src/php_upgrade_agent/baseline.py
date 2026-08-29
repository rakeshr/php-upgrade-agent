"""Naive regex baseline scanner — fast, comment/string blind."""

from __future__ import annotations

from pathlib import Path

from php_upgrade_agent.models import Finding, ScanResult
from php_upgrade_agent.rules import RULES


def _snippet_for_line(content: str, line_no: int, context: int = 0) -> str:
    lines = content.splitlines()
    if not lines:
        return ""
    idx = max(0, line_no - 1)
    start = max(0, idx - context)
    end = min(len(lines), idx + context + 1)
    return "\n".join(lines[start:end])


def scan_file_baseline(path: Path, root: Path) -> list[Finding]:
    rel = str(path.relative_to(root))
    content = path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []
    for rule in RULES:
        for match in rule.pattern.finditer(content):
            line = content.count("\n", 0, match.start()) + 1
            findings.append(
                Finding(
                    file=rel,
                    line=line,
                    rule_id=rule.id,
                    message=rule.message,
                    severity=rule.severity,
                    snippet=_snippet_for_line(content, line),
                    verified=False,
                )
            )
    return findings


def run_baseline(target: Path) -> ScanResult:
    target = target.resolve()
    result = ScanResult(mode="baseline")
    php_files = sorted(target.rglob("*.php"))
    if target.is_file() and target.suffix == ".php":
        php_files = [target]
    for php_file in php_files:
        for finding in scan_file_baseline(php_file, target if target.is_dir() else target.parent):
            result.add(finding)
    return result
