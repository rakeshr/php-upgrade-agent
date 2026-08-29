"""Deterministic tool-using agent loop (no API key required)."""

from __future__ import annotations

from pathlib import Path

from php_upgrade_agent.baseline import scan_file_baseline
from php_upgrade_agent.models import ClientReport, Finding, ScanResult, write_json
from php_upgrade_agent.tools import AgentTools
from php_upgrade_agent.verify import line_is_only_non_code, offset_in_non_code


def run_agent(
    target: Path, artifacts_dir: Path | None = None
) -> tuple[ScanResult, ClientReport]:
    """Plan → scan → verify uncertain findings → report."""
    tools = AgentTools(target)
    result = ScanResult(mode="agent")

    tools.state.log("plan", message="Enumerate PHP files and token-scan each one")
    php_files = tools.list_php_files()

    for rel_path in php_files:
        tools.state.log("plan", message=f"Token-scan {rel_path}")
        for raw in tools.scan_tokens(rel_path):
            tools.record_finding(raw)

    tools.state.log("plan", message="Verify baseline-only hits; drop comment/string false positives")
    root = tools.root
    for rel_path in php_files:
        path = root / rel_path
        content = path.read_text(encoding="utf-8", errors="replace")
        token_keys = {(f.file, f.rule_id, f.line) for f in tools.state.findings}
        for hit in scan_file_baseline(path, root):
            if hit.key() in token_keys:
                tools.mark_verified(hit.file, hit.rule_id, hit.line, keep=True)
                continue
            offset = _offset_for_line(content, hit.line, hit.rule_id)
            drop = (
                line_is_only_non_code(content, hit.line)
                or (offset is not None and offset_in_non_code(content, offset))
            )
            tools.mark_verified(hit.file, hit.rule_id, hit.line, keep=not drop)
            tools.state.log(
                "verify",
                action="dropped_false_positive" if drop else "confirmed_miss",
                file=hit.file,
                line=hit.line,
                rule_id=hit.rule_id,
                kept=not drop,
            )

    report = tools.write_report()
    for f in report.findings:
        result.add(f)

    if artifacts_dir is not None:
        traj_dir = artifacts_dir / "trajectories"
        traj_dir.mkdir(parents=True, exist_ok=True)
        slug = target.name.replace("/", "_") or "scan"
        traj_path = traj_dir / f"agent_{slug}.json"
        write_json(
            traj_path,
            {
                "target": str(target),
                "trajectory": tools.state.trajectory,
                "report": report.to_markdown(),
                "findings": [f.to_dict() for f in report.sorted_findings],
            },
        )

    return result, report


def _offset_for_line(content: str, line_no: int, rule_id: str) -> int | None:
    lines = content.splitlines(keepends=True)
    if line_no < 1 or line_no > len(lines):
        return None
    line_start = sum(len(lines[i]) for i in range(line_no - 1))
    line_text = lines[line_no - 1]
    idx = line_text.find(rule_id)
    if idx < 0 and rule_id == "mysql_extension":
        for needle in ("mysql_connect", "mysql_query", "mysql_select_db"):
            idx = line_text.find(needle)
            if idx >= 0:
                break
    if idx < 0:
        return None
    return line_start + idx
