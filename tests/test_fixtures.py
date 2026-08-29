"""Tests for fixture expectations and scanner behavior."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from php_upgrade_agent.agent import run_agent
from php_upgrade_agent.baseline import run_baseline
from php_upgrade_agent.eval_runner import load_expected, run_eval, score


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"


def test_expected_manifest_has_twelve_fixtures() -> None:
    data = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    assert len(data["fixtures"]) >= 12


def test_clean_file_has_no_baseline_hits() -> None:
    result = run_baseline(FIXTURES / "clean_file.php")
    assert result.findings == []


def test_false_positive_file_baseline_noisy_agent_clean() -> None:
    baseline = run_baseline(FIXTURES / "false_positive_comment.php")
    agent, _ = run_agent(FIXTURES / "false_positive_comment.php")
    assert len(baseline.findings) > 0
    assert agent.findings == []


def test_multi_issue_detected_by_agent() -> None:
    expected = [e for e in load_expected(FIXTURES) if e.file == "multi_issue.php"]
    agent, _ = run_agent(FIXTURES / "multi_issue.php")
    found = {(f.file, f.rule_id) for f in agent.findings}
    gold = {(e.file, e.rule_id) for e in expected}
    assert gold.issubset(found)


def test_agent_beats_baseline_f1_on_fixture_pack() -> None:
    payload = run_eval(FIXTURES, ARTIFACTS)
    assert payload["agent"]["f1"] > payload["baseline"]["f1"]
    assert payload["agent"]["fp"] < payload["baseline"]["fp"]
