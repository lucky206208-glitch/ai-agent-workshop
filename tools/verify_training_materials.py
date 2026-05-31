from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAINING_MARKER = "_".join(["TRAINING", "SECRET", "DO", "NOT", "USE"])
TRAINING_MARKER_REGEX = "TRAINING_SECRET[_]DO_NOT_USE"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_context() -> None:
    context = read("CONTEXT.md")
    require("Lecture 02 is not a general Git or GitHub course" in context, "CONTEXT.md must lock PR judgment scope")
    require("Hold is not a GitHub button" in context, "CONTEXT.md must define Hold as an operational decision")
    require(TRAINING_MARKER in context, "CONTEXT.md must define the training secret marker policy")


def verify_ci() -> None:
    workflow = read(".github/workflows/check.yml")
    require(TRAINING_MARKER_REGEX in workflow, "CI must use a self-nonmatching training marker regex")
    require(TRAINING_MARKER not in workflow, "CI control file must not contain the marker contiguously")
    require("sk-[A-Za-z0-9_-]" in workflow, "CI must still block sk-style secret-like strings")


def verify_training_links() -> None:
    path = ROOT / "docs" / "training-pr-links.json"
    require(path.exists(), "docs/training-pr-links.json must exist")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(len(data["scenarios"]) == 3, "training-pr-links.json must contain exactly three scenarios")
    for scenario in data["scenarios"]:
        require(scenario["title"].startswith("[TRAINING - DO NOT MERGE]"), f"{scenario['id']} title must use training prefix")
        require(scenario["pr_url"].startswith("https://github.com/"), f"{scenario['id']} must include a GitHub PR URL")
        require(scenario["issue_url"].startswith("https://github.com/"), f"{scenario['id']} must include a GitHub Issue URL")


def verify_docs() -> None:
    lecture = read("lectures/02-github-pr-control.md")
    checklist = read("docs/pr-review-checklist.md")
    scenarios = read("docs/sample-pr-scenarios.md")
    answer_key = read("docs/sample-pr-answer-key.md")
    combined = "\n".join([lecture, checklist, scenarios, answer_key])
    for required in [
        "Files changed",
        "Diff",
        "Checks",
        "Draft는 수업 안전장치",
        "Hold는 GitHub 버튼이 아니다",
        "CI는 깊게, CD는 짧게",
        "Worktree",
    ]:
        require(required in combined, f"Missing required teaching phrase: {required}")
    require("/pull/1" not in scenarios and "/pull/2" not in scenarios and "/pull/3" not in scenarios, "student scenarios must not point to old closed PRs")
    require("Operational decision" in answer_key, "answer key must keep instructor-only decisions")


def main() -> int:
    checks = [verify_context, verify_ci, verify_training_links, verify_docs]
    failures: list[str] = []
    for check in checks:
        try:
            check()
        except Exception as exc:
            failures.append(f"{check.__name__}: {exc}")
    if failures:
        print("Training material verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("Training material verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
