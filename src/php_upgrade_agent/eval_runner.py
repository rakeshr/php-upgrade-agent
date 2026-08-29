"""Evaluation harness — F1 on fixture pack."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from php_upgrade_agent.agent import run_agent
from php_upgrade_agent.baseline import run_baseline
from php_upgrade_agent.models import Finding, write_json


@dataclass
class ExpectedIssue:
    file: str
    rule_id: str
    line: int | None = None


@dataclass
class EvalMetrics:
    precision: float
    recall: float
    f1: float
    tp: int
    fp: int
    fn: int

    def as_row(self) -> str:
        return f"{self.f1:.3f} (P={self.precision:.3f} R={self.recall:.3f} tp={self.tp} fp={self.fp} fn={self.fn})"


def load_expected(fixtures_dir: Path) -> list[ExpectedIssue]:
    manifest = fixtures_dir / "expected.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    issues: list[ExpectedIssue] = []
    for entry in data["fixtures"]:
        for issue in entry.get("issues", []):
            issues.append(
                ExpectedIssue(
                    file=entry["file"],
                    rule_id=issue["rule_id"],
                    line=issue.get("line"),
                )
            )
    return issues


def _normalize_findings(findings: list[Finding]) -> set[tuple[str, str]]:
    return {(f.file, f.rule_id) for f in findings}


def _normalize_expected(expected: list[ExpectedIssue]) -> set[tuple[str, str]]:
    return {(e.file, e.rule_id) for e in expected}


def score(findings: list[Finding], expected: list[ExpectedIssue]) -> EvalMetrics:
    pred = _normalize_findings(findings)
    gold = _normalize_expected(expected)
    tp = len(pred & gold)
    fp = len(pred - gold)
    fn = len(gold - pred)
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return EvalMetrics(precision=precision, recall=recall, f1=f1, tp=tp, fp=fp, fn=fn)


def run_eval(fixtures_dir: Path, artifacts_dir: Path) -> dict[str, Any]:
    fixtures_dir = fixtures_dir.resolve()
    expected = load_expected(fixtures_dir)

    baseline_result = run_baseline(fixtures_dir)
    agent_result, _report = run_agent(fixtures_dir, artifacts_dir=artifacts_dir)

    baseline_metrics = score(baseline_result.findings, expected)
    agent_metrics = score(agent_result.findings, expected)

    payload: dict[str, Any] = {
        "fixtures_dir": str(fixtures_dir),
        "expected_issue_count": len(expected),
        "baseline": baseline_metrics.__dict__,
        "agent": agent_metrics.__dict__,
        "delta_f1": agent_metrics.f1 - baseline_metrics.f1,
        "baseline_findings": [f.to_dict() for f in baseline_result.sorted_findings()],
        "agent_findings": [f.to_dict() for f in agent_result.sorted_findings()],
    }

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    write_json(artifacts_dir / "eval.json", payload)
    return payload


def print_eval_table(payload: dict[str, Any]) -> None:
    b = payload["baseline"]
    a = payload["agent"]

    def fmt(m: dict[str, float | int]) -> str:
        return f"{m['f1']:.3f}"

    def delta(key: str) -> str:
        change = a[key] - b[key]
        sign = "+" if change >= 0 else ""
        return f"{sign}{change:.3f}"

    rows = [
        ("F1", fmt(b), fmt(a), delta("f1")),
        ("Precision", f"{b['precision']:.3f}", f"{a['precision']:.3f}", delta("precision")),
        ("Recall", f"{b['recall']:.3f}", f"{a['recall']:.3f}", delta("recall")),
        ("True Positives", str(b["tp"]), str(a["tp"]), f"{a['tp'] - b['tp']:+d}"),
        ("False Positives", str(b["fp"]), str(a["fp"]), f"{a['fp'] - b['fp']:+d}"),
        ("False Negatives", str(b["fn"]), str(a["fn"]), f"{a['fn'] - b['fn']:+d}"),
    ]
    headers = ("Metric", "Baseline", "Agent", "Change")
    widths = [max(len(str(row[i])) for row in ([headers] + list(rows))) for i in range(4)]
    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * widths[i] for i in range(4))
    print(line)
    print(sep)
    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(4)))
