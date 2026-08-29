"""Agent tool implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from php_upgrade_agent.models import ClientReport, Finding
from php_upgrade_agent.scanner import scan_file_tokens


@dataclass
class AgentState:
    target: Path
    findings: list[Finding] = field(default_factory=list)
    verified_keys: set[tuple[str, str, int]] = field(default_factory=set)
    trajectory: list[dict[str, Any]] = field(default_factory=list)
    files_scanned: list[str] = field(default_factory=list)

    def log(self, step: str, **payload: Any) -> None:
        self.trajectory.append({"step": step, **payload})


class AgentTools:
    def __init__(self, target: Path) -> None:
        self.target = target.resolve()
        self.root = self.target if self.target.is_dir() else self.target.parent
        self.state = AgentState(target=self.target)

    def list_php_files(self) -> list[str]:
        if self.target.is_file() and self.target.suffix == ".php":
            files = [str(self.target.relative_to(self.root))]
        else:
            files = [
                str(p.relative_to(self.root))
                for p in sorted(self.target.rglob("*.php"))
            ]
        self.state.files_scanned = files
        self.state.log("list_php_files", files=files)
        return files

    def read_file(self, rel_path: str) -> str:
        path = self.root / rel_path
        content = path.read_text(encoding="utf-8", errors="replace")
        self.state.log("read_file", path=rel_path, bytes=len(content))
        return content

    def scan_tokens(self, rel_path: str) -> list[dict[str, Any]]:
        path = self.root / rel_path
        findings = scan_file_tokens(path, self.root)
        payload = [f.to_dict() for f in findings]
        self.state.log("scan_tokens", path=rel_path, findings=payload)
        return payload

    def record_finding(self, finding: dict[str, Any]) -> None:
        item = Finding(
            file=finding["file"],
            line=int(finding["line"]),
            rule_id=finding["rule_id"],
            message=finding.get("message", ""),
            severity=finding.get("severity", "error"),
            snippet=finding.get("snippet", ""),
            verified=False,
        )
        self.state.findings.append(item)
        self.state.log("record_finding", finding=item.to_dict())

    def mark_verified(self, file: str, rule_id: str, line: int, keep: bool) -> None:
        key = (file, rule_id, line)
        self.state.verified_keys.add(key)
        if not keep:
            self.state.findings = [f for f in self.state.findings if f.key() != key]
        else:
            for f in self.state.findings:
                if f.key() == key:
                    f.verified = True
        self.state.log("mark_verified", file=file, rule_id=rule_id, line=line, keep=keep)

    def write_report(self) -> ClientReport:
        errors = [f for f in self.state.findings if f.severity == "error"]
        warnings = [f for f in self.state.findings if f.severity == "warning"]
        if errors:
            decision = "NO-GO"
            summary = (
                f"Found {len(errors)} blocking error(s) and {len(warnings)} warning(s). "
                "Resolve errors before upgrading to PHP 8.3+."
            )
        elif warnings:
            decision = "CAUTION"
            summary = (
                f"No blocking errors, but {len(warnings)} deprecation warning(s) "
                "should be addressed before PHP 8.4."
            )
        else:
            decision = "GO"
            summary = "No known PHP 8.3+ compatibility issues detected in scanned files."

        report = ClientReport(
            go_no_go=decision,
            summary=summary,
            findings=self.state.findings,
            files_scanned=len(self.state.files_scanned),
        )
        self.state.log("write_report", decision=decision, finding_count=len(self.state.findings))
        return report
