"""Shared data models for findings and reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    file: str
    line: int
    rule_id: str
    message: str
    severity: str = "error"
    snippet: str = ""
    verified: bool = False

    def key(self) -> tuple[str, str, int]:
        return (self.file, self.rule_id, self.line)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    mode: str = "baseline"

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.file, f.line, f.rule_id))

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "finding_count": len(self.findings),
            "findings": [f.to_dict() for f in self.sorted_findings()],
        }


@dataclass
class ClientReport:
    go_no_go: str
    summary: str
    findings: list[Finding]
    files_scanned: int

    def to_markdown(self) -> str:
        lines = [
            "# PHP Upgrade Readiness Report",
            "",
            f"**Decision:** {self.go_no_go}",
            "",
            self.summary,
            "",
            f"Files scanned: {self.files_scanned}",
            f"Issues found: {len(self.findings)}",
            "",
        ]
        if self.findings:
            lines.append("## Issues")
            lines.append("")
            for f in self.sorted_findings:
                lines.append(
                    f"- `{f.file}:{f.line}` [{f.severity}] **{f.rule_id}** — {f.message}"
                )
                if f.snippet:
                    lines.append(f"  ```php\n  {f.snippet.strip()}\n  ```")
            lines.append("")
        else:
            lines.append("No blocking compatibility issues detected.")
            lines.append("")
        return "\n".join(lines)

    @property
    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda x: (x.file, x.line, x.rule_id))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
