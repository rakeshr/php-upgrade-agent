"""CLI entrypoint for php_upgrade_agent."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from php_upgrade_agent import __version__
from php_upgrade_agent.agent import run_agent
from php_upgrade_agent.baseline import run_baseline
from php_upgrade_agent.eval_runner import print_eval_table, run_eval
from php_upgrade_agent.models import write_json


def _default_fixtures() -> Path:
    return Path(__file__).resolve().parents[2] / "fixtures"


def _default_artifacts() -> Path:
    return Path(__file__).resolve().parents[2] / "artifacts"


def cmd_baseline(args: argparse.Namespace) -> int:
    target = Path(args.path)
    if not target.exists():
        print(f"error: path not found: {target}", file=sys.stderr)
        return 1
    result = run_baseline(target)
    out = result.to_dict()
    if args.json:
        print_json = __import__("json").dumps(out, indent=2)
        print(print_json)
    else:
        for f in result.sorted_findings():
            print(f"{f.file}:{f.line} [{f.severity}] {f.rule_id} — {f.message}")
        print(f"\n{len(result.findings)} finding(s)")
    if args.output:
        write_json(Path(args.output), out)
    return 0


def cmd_agent(args: argparse.Namespace) -> int:
    target = Path(args.path)
    if not target.exists():
        print(f"error: path not found: {target}", file=sys.stderr)
        return 1
    artifacts = Path(args.artifacts) if args.artifacts else _default_artifacts()
    result, report = run_agent(target, artifacts_dir=artifacts)
    report_path = artifacts / "report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report.to_markdown(), encoding="utf-8")

    if args.json:
        print(__import__("json").dumps(result.to_dict(), indent=2))
    else:
        print(report.to_markdown())
        print(f"\nReport written to {report_path}")
        print(f"Trajectory logged under {artifacts / 'trajectories'}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    fixtures = Path(args.fixtures) if args.fixtures else _default_fixtures()
    artifacts = Path(args.artifacts) if args.artifacts else _default_artifacts()
    if not fixtures.exists():
        print(f"error: fixtures not found: {fixtures}", file=sys.stderr)
        return 1
    payload = run_eval(fixtures, artifacts)
    print_eval_table(payload)
    print(f"\nWrote {artifacts / 'eval.json'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="php_upgrade_agent",
        description="PHP 8.3+ upgrade readiness scanner for WordPress agencies",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_base = sub.add_parser("baseline", help="Fast regex scan (no verification)")
    p_base.add_argument("path", nargs="?", default=str(_default_fixtures()), help="File or directory")
    p_base.add_argument("--json", action="store_true", help="Emit JSON")
    p_base.add_argument("-o", "--output", help="Write JSON results to path")
    p_base.set_defaults(func=cmd_baseline)

    p_agent = sub.add_parser("agent", help="Token-aware agent with verify pass")
    p_agent.add_argument("path", nargs="?", default=str(_default_fixtures()), help="File or directory")
    p_agent.add_argument("--artifacts", help="Artifacts directory")
    p_agent.add_argument("--json", action="store_true", help="Emit JSON")
    p_agent.set_defaults(func=cmd_agent)

    p_eval = sub.add_parser("eval", help="Score baseline vs agent on fixtures")
    p_eval.add_argument("--fixtures", help="Fixtures directory")
    p_eval.add_argument("--artifacts", help="Artifacts directory")
    p_eval.set_defaults(func=cmd_eval)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
