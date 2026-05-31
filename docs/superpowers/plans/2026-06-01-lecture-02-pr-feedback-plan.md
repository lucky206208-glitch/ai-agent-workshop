# Lecture 02 PR Feedback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Revise the Lecture 02 GitHub PR Control materials so beginner students learn how to judge whether AI agent changes should be merged.

**Architecture:** Keep PR judgment as the main learning path, with Issue, CI/CD, and worktree concepts supporting that path. Create live training Draft PRs and Issues, update the lecture documents, regenerate the PPTX from a script, and verify the deck and docs through repeatable checks.

**Tech Stack:** GitHub CLI (`gh`), Git worktrees, GitHub Actions, Markdown, Python 3, `python-pptx`, Pillow, PowerPoint manual visual check.

---

## Current Facts

- Existing lecture materials live in `lectures/02-github-pr-control.md`, `docs/pr-review-checklist.md`, `docs/sample-pr-scenarios.md`, and `docs/sample-pr-answer-key.md`.
- Existing deck is `decks/02-github-pr-control-bento-swiss.pptx`.
- Current deck has 12 slides, and slides 2-12 use overlapping top-left red square and label coordinates.
- Existing sample PR links in `docs/sample-pr-scenarios.md` point to closed PRs #1-#3.
- Current CI only blocks secret-like `sk-...` patterns in non-Markdown files.
- The revised approach is Option A: PR judgment centered expansion.

## File Structure

- Create `CONTEXT.md`: canonical domain language and scope boundaries for future agents.
- Modify `.github/workflows/check.yml`: use explicit training secret marker detection instead of relying only on `sk-...`.
- Create `docs/training-pr-links.json`: current Issue and Draft PR numbers, URLs, branch names, and check expectations.
- Modify `docs/sample-pr-scenarios.md`: student-facing scenarios with new Draft PR links and no answer leakage.
- Modify `docs/sample-pr-answer-key.md`: instructor-only decisions and discussion prompts.
- Modify `docs/pr-review-checklist.md`: beginner glossary and PR judgment checklist.
- Modify `lectures/02-github-pr-control.md`: revised 2-hour flow and slide outline.
- Create `tools/build_github_pr_deck.py`: deterministic PPTX generator.
- Create `tools/verify_training_materials.py`: docs/link/CI content verification.
- Create `tools/verify_pptx_layout.py`: PPTX structure and top-left overlap verification.
- Create `decks/assets/lecture-02/`: GitHub screenshots for the deck.
- Regenerate `decks/02-github-pr-control-bento-swiss.pptx`.

---

### Task 1: Capture Canonical Scope And Vocabulary

**Files:**
- Create: `CONTEXT.md`
- Modify: `README.md`

- [ ] **Step 1: Create the domain context document**

Create `CONTEXT.md` with this exact content:

```markdown
# AI Agent Workshop Context

## Course Domain

This repository supports a beginner workshop about reviewing AI agent code changes through GitHub Pull Requests.

## Lecture 02 Principle

Lecture 02 is not a general Git or GitHub course. Its goal is to teach students how to decide whether an AI agent's Pull Request should be merged.

## Target Student

The target student has little or no prior knowledge of GitHub terms such as Issue, Branch, Pull Request, Diff, Files changed, Checks, CI, CD, Merge, Request changes, Hold, Stash, or Worktree.

## Canonical Terms

- Issue: the request or problem statement that starts the work.
- Branch: the isolated line of work where changes are made before review.
- Pull Request or PR: the review proposal asking whether branch changes should enter main.
- Files changed: the GitHub tab that shows which files changed.
- Diff: the added and removed lines inside a changed file.
- Checks: the GitHub area that shows automated CI results.
- CI: automated checks that run before merge.
- CD: automated deployment after merge. Lecture 02 explains this briefly but does not teach deployment.
- Merge: accepting the PR into main after review.
- Request changes: a GitHub review action asking for specific fixes.
- Hold: an operational decision to not approve or merge because the risk is too high. Hold is not a GitHub button.
- Worktree: a separate local working directory for a branch. In this lecture it is an AI agent operations concept, not a command-line exercise.

## Teaching Boundaries

- Teach PR judgment through Files changed, Diff, Checks, and Decision.
- Keep Issue, Branch, CI/CD, and Worktree explanations in service of PR judgment.
- Do not turn Lecture 02 into Git command memorization.
- Do not ask students to merge training PRs.
- Do not ask students to leave real GitHub PR comments during class.
- Students read PRs and submit an exit ticket.

## Training PR Policy

- Training PRs must be Draft PRs.
- Training PR and Issue titles must start with `[TRAINING - DO NOT MERGE]`.
- Draft status is a safety guardrail. Students should ignore Draft status when practicing content judgment.
- Real secrets must never be used. Secret examples must use explicit training markers such as `TRAINING_SECRET_DO_NOT_USE`.
```

- [ ] **Step 2: Add the context pointer to README**

In `README.md`, after the opening description paragraph, add:

```markdown
Project teaching language and scope boundaries are documented in `CONTEXT.md`.
```

- [ ] **Step 3: Verify the context terms are searchable**

Run:

```powershell
rg -n "Lecture 02 is not a general Git|Hold is not a GitHub button|TRAINING - DO NOT MERGE" CONTEXT.md README.md
```

Expected: three matches, all from the new context or README pointer.

- [ ] **Step 4: Commit Task 1**

Run:

```powershell
git add CONTEXT.md README.md
git commit -m "docs: capture lecture 02 teaching context"
```

---

### Task 2: Make The CI Training Secret Fixture Explicit

**Files:**
- Modify: `.github/workflows/check.yml`
- Create: `tools/verify_training_materials.py`

- [ ] **Step 1: Update CI to block explicit training secret markers**

In `.github/workflows/check.yml`, replace the current secret-like block with:

```yaml
      - name: Block training secret markers
        run: |
          if grep -RIn --exclude-dir=.git --exclude='*.md' 'TRAINING_SECRET_DO_NOT_USE' .; then
            echo "Training secret marker detected. Remove it before merge."
            exit 1
          fi
          if grep -RIn --exclude-dir=.git --exclude='*.md' 'sk-[A-Za-z0-9_-]\{8,\}' .; then
            echo "Secret-like string detected. Remove it before merge."
            exit 1
          fi
```

- [ ] **Step 2: Add material verification script**

Create `tools/verify_training_materials.py` with this content:

```python
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_context() -> None:
    context = read("CONTEXT.md")
    require("Lecture 02 is not a general Git or GitHub course" in context, "CONTEXT.md must lock PR judgment scope")
    require("Hold is not a GitHub button" in context, "CONTEXT.md must define Hold as an operational decision")
    require("TRAINING_SECRET_DO_NOT_USE" in context, "CONTEXT.md must define the training secret marker policy")


def verify_ci() -> None:
    workflow = read(".github/workflows/check.yml")
    require("TRAINING_SECRET_DO_NOT_USE" in workflow, "CI must block explicit training secret markers")
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
    scenario_pr_numbers = set(re.findall(r"https://github\.com/lucky206208-glitch/ai-agent-workshop/pull/(\d+)\b", scenarios))
    require(not (scenario_pr_numbers & {"1", "2", "3"}), "student scenarios must not point to old closed PRs")
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
```

- [ ] **Step 3: Run verifier and confirm expected failure**

Run:

```powershell
python tools\verify_training_materials.py
```

Expected: FAIL because `docs/training-pr-links.json` and revised docs are not created yet.

- [ ] **Step 4: Commit Task 2**

Run:

```powershell
git add .github/workflows/check.yml tools/verify_training_materials.py
git commit -m "ci: add explicit training secret marker check"
```

---

### Task 3: Create The Training Issues And Draft PRs

**Files:**
- Create: `docs/training-pr-links.json`
- Temporary branch changes for three GitHub Draft PRs

- [ ] **Step 1: Confirm GitHub CLI authentication**

Run:

```powershell
gh auth status
```

Expected: authenticated to `github.com` with permission to create Issues, branches, and PRs in `lucky206208-glitch/ai-agent-workshop`.

- [ ] **Step 2: Create three training Issues**

Run these commands in one PowerShell session so the returned URLs stay in variables:

```powershell
$GOOD_ISSUE_URL = gh issue create --repo lucky206208-glitch/ai-agent-workshop --title "[TRAINING - DO NOT MERGE] Good PR request: checklist entry point" --body "Student scenario: add a small entry point so students can find the PR review checklist from README and the workshop page. Expected normal files: README.md and index.html. Teaching point: small request, small diff, passing checks."
$PROBLEM_A_ISSUE_URL = gh issue create --repo lucky206208-glitch/ai-agent-workshop --title "[TRAINING - DO NOT MERGE] Problem A request: shorten one heading" --body "Student scenario: make one title shorter. Expected normal file: index.html. Teaching point: if an agent changes unrelated docs or the visual system for a tiny copy request, hold the PR even when CI passes."
$PROBLEM_B_ISSUE_URL = gh issue create --repo lucky206208-glitch/ai-agent-workshop --title "[TRAINING - DO NOT MERGE] Problem B request: local demo notes" --body "Student scenario: add local demo instructions. Expected normal file: README.md or one docs file. Teaching point: CI failure plus a training secret marker means hold the PR and do not copy sensitive-looking values into comments."
$GOOD_ISSUE_URL
$PROBLEM_A_ISSUE_URL
$PROBLEM_B_ISSUE_URL
```

- [ ] **Step 3: Create the Good PR branch**

Run:

```powershell
git fetch origin
git switch -c training/good-pr-small-checklist-entry origin/main
```

Modify `README.md` by adding this section after `## Student Goal`:

```markdown
## Quick Student Links

- PR review checklist: `docs/pr-review-checklist.md`
- Sample PR scenarios: `docs/sample-pr-scenarios.md`
```

Modify `index.html` by adding a fourth article in the `.grid` section:

```html
        <article>
          <h2>Checklist</h2>
          <p>수업 중 판단 근거를 기록할 때 사용합니다.</p>
        </article>
```

- [ ] **Step 4: Push and open the Good Draft PR**

Run:

```powershell
git add README.md index.html
git commit -m "docs: add training checklist entry point"
git push -u origin training/good-pr-small-checklist-entry
$GOOD_PR_URL = gh pr create --repo lucky206208-glitch/ai-agent-workshop --draft --base main --head training/good-pr-small-checklist-entry --title "[TRAINING - DO NOT MERGE] Good PR: checklist entry point" --body "Linked training issue: $GOOD_ISSUE_URL`n`nStudent task: decide whether this PR can be merged by checking Files changed, Diff, and Checks.`n`nExpected teaching signal: small request, small diff, passing checks."
$GOOD_PR_URL
```

- [ ] **Step 5: Create the Problem A branch**

Run:

```powershell
git switch codex/lecture-02-pr-feedback-plan
git fetch origin
git switch -c training/problem-a-overbroad-agent-change origin/main
```

Modify `index.html` by changing the hero heading to:

```html
        <h1>AI Agent PR 검토하기</h1>
```

Modify `styles.css` by changing these existing variables:

```css
  --paper: #ffffff;
  --accent: #6a3df4;
  --navy: #242447;
```

Add `docs/agent-extra-notes.md`:

```markdown
# Agent Extra Notes

This file is intentionally unrelated to the tiny heading request.
Students should notice that it expands the PR scope.
```

Modify `README.md` by adding this section at the end:

```markdown
## Future Roadmap

This roadmap is intentionally unrelated to the tiny heading request.
Students should treat this as scope creep.
```

- [ ] **Step 6: Push and open the Problem A Draft PR**

Run:

```powershell
git add index.html styles.css README.md docs/agent-extra-notes.md
git commit -m "style: over-expand training heading request"
git push -u origin training/problem-a-overbroad-agent-change
$PROBLEM_A_PR_URL = gh pr create --repo lucky206208-glitch/ai-agent-workshop --draft --base main --head training/problem-a-overbroad-agent-change --title "[TRAINING - DO NOT MERGE] Problem A: overbroad agent change" --body "Linked training issue: $PROBLEM_A_ISSUE_URL`n`nStudent task: decide whether passing checks are enough when Files changed shows unrelated work.`n`nExpected teaching signal: small request, unrelated files, passing checks, Hold decision."
$PROBLEM_A_PR_URL
```

- [ ] **Step 7: Create the Problem B branch**

Run:

```powershell
git switch codex/lecture-02-pr-feedback-plan
git fetch origin
git switch -c training/problem-b-ci-secret-fixture origin/main
```

Create `.env`:

```text
DEMO_TOKEN=TRAINING_SECRET_DO_NOT_USE
```

Modify `index.html` by changing the body tag to remove the required marker:

```html
  <body>
```

- [ ] **Step 8: Push and open the Problem B Draft PR**

Run:

```powershell
git add .env index.html
git commit -m "chore: add failing training demo env"
git push -u origin training/problem-b-ci-secret-fixture
$PROBLEM_B_PR_URL = gh pr create --repo lucky206208-glitch/ai-agent-workshop --draft --base main --head training/problem-b-ci-secret-fixture --title "[TRAINING - DO NOT MERGE] Problem B: CI and training secret marker" --body "Linked training issue: $PROBLEM_B_ISSUE_URL`n`nStudent task: decide what to do when Checks fail and Files changed includes a secret-like training file.`n`nExpected teaching signal: CI failure, .env file, training secret marker, Hold decision."
$PROBLEM_B_PR_URL
```

- [ ] **Step 9: Capture PR and Issue metadata**

Return to the implementation branch and create `docs/training-pr-links.json` from the variables created in this task:

```powershell
git switch codex/lecture-02-pr-feedback-plan
@"
{
  "repository": "https://github.com/lucky206208-glitch/ai-agent-workshop",
  "policy": "All training PRs are Draft PRs and must not be merged.",
  "scenarios": [
    {
      "id": "good-pr",
      "title": "[TRAINING - DO NOT MERGE] Good PR: checklist entry point",
      "branch": "training/good-pr-small-checklist-entry",
      "issue_url": "$GOOD_ISSUE_URL",
      "pr_url": "$GOOD_PR_URL",
      "expected_checks": "passing",
      "expected_decision": "Merge in content judgment; do not actually merge because this is training"
    },
    {
      "id": "problem-a",
      "title": "[TRAINING - DO NOT MERGE] Problem A: overbroad agent change",
      "branch": "training/problem-a-overbroad-agent-change",
      "issue_url": "$PROBLEM_A_ISSUE_URL",
      "pr_url": "$PROBLEM_A_PR_URL",
      "expected_checks": "passing",
      "expected_decision": "Hold"
    },
    {
      "id": "problem-b",
      "title": "[TRAINING - DO NOT MERGE] Problem B: CI and training secret marker",
      "branch": "training/problem-b-ci-secret-fixture",
      "issue_url": "$PROBLEM_B_ISSUE_URL",
      "pr_url": "$PROBLEM_B_PR_URL",
      "expected_checks": "failing",
      "expected_decision": "Hold"
    }
  ]
}
"@ | Set-Content -Path docs\training-pr-links.json -Encoding utf8
```

- [ ] **Step 10: Verify PR state**

Run:

```powershell
gh pr view training/good-pr-small-checklist-entry --repo lucky206208-glitch/ai-agent-workshop --json isDraft,state,baseRefName,headRefName,statusCheckRollup
gh pr view training/problem-a-overbroad-agent-change --repo lucky206208-glitch/ai-agent-workshop --json isDraft,state,baseRefName,headRefName,statusCheckRollup
gh pr view training/problem-b-ci-secret-fixture --repo lucky206208-glitch/ai-agent-workshop --json isDraft,state,baseRefName,headRefName,statusCheckRollup
```

Expected:

- Good PR: `isDraft: true`, `state: OPEN`, `baseRefName: main`, checks pass.
- Problem A: `isDraft: true`, `state: OPEN`, `baseRefName: main`, checks pass.
- Problem B: `isDraft: true`, `state: OPEN`, `baseRefName: main`, checks fail.

- [ ] **Step 11: Commit training link metadata on the implementation branch**

Commit the metadata:

```powershell
git add docs/training-pr-links.json
git commit -m "docs: record current training PR links"
```

---

### Task 4: Rewrite Student And Instructor Documents Around PR Judgment

**Files:**
- Modify: `docs/pr-review-checklist.md`
- Modify: `docs/sample-pr-scenarios.md`
- Modify: `docs/sample-pr-answer-key.md`
- Modify: `lectures/02-github-pr-control.md`

- [ ] **Step 1: Update the checklist with beginner glossary**

In `docs/pr-review-checklist.md`, add this section after the title:

```markdown
## Beginner Glossary

| GitHub UI term | 한국어 의미 | 수업에서 보는 위치 |
|---|---|---|
| Issue | 요청서 또는 문제 설명 | PR 본문에 연결된 링크 |
| Branch | main과 분리된 작업 줄기 | PR 상단의 compare 정보 |
| Pull Request / PR | main에 합쳐도 되는지 검토하는 제안 | PR 화면 전체 |
| Files changed | 변경된 파일 목록 | PR의 Files changed 탭 |
| Diff | 추가/삭제된 줄 | Files changed 안의 코드 영역 |
| Checks | 자동 검사 결과 | PR 하단 또는 Checks 영역 |
| CI | merge 전 자동 검사 | Checks의 workflow 결과 |
| CD | merge 후 자동 배포 | 이번 수업에서는 용어만 짧게 설명 |
| Merge | PR을 main에 합침 | 수업에서는 실제로 누르지 않음 |
| Request changes | 수정 요청 리뷰 | 수업에서는 exit ticket 문장으로 작성 |
| Hold | merge 보류 운영 판단 | GitHub 버튼이 아님 |
| Worktree | branch별 분리 작업 폴더 | AI agent 운영 사례에서만 설명 |
```

Also add this warning box before the decision table:

```markdown
## Training PR Safety Note

Draft는 수업 안전장치입니다. 이 수업에서는 Draft 배너 자체가 아니라 Files changed, Diff, Checks를 보고 내용상 판단을 연습합니다.

Hold는 GitHub 버튼이 아니다. Hold는 approve하지 않고, 위험 근거를 남기며, 필요한 경우 request changes 또는 blocking comment를 남기는 운영 판단입니다.
```

- [ ] **Step 2: Rewrite student scenarios**

Replace `docs/sample-pr-scenarios.md` by generating it from `docs/training-pr-links.json`:

```powershell
$links = Get-Content docs\training-pr-links.json | ConvertFrom-Json
$good = $links.scenarios | Where-Object { $_.id -eq "good-pr" }
$problemA = $links.scenarios | Where-Object { $_.id -eq "problem-a" }
$problemB = $links.scenarios | Where-Object { $_.id -eq "problem-b" }
$content = @'
# Sample PR Scenarios

All scenarios use Draft PRs with `[TRAINING - DO NOT MERGE]` in the title. Draft status is a class safety guardrail. Judge the PR content by reading Files changed, Diff, and Checks.

## PR 1: Good PR

- Issue: {{GOOD_ISSUE_URL}}
- PR: {{GOOD_PR_URL}}
- Branch: `training/good-pr-small-checklist-entry`
- Student task: decide whether the content is mergeable.
- Expected files to inspect: `README.md`, `index.html`
- Checks state to observe: passing
- Student clues: small request, small file list, matching diff, green checks.

## PR 2: Problem A

- Issue: {{PROBLEM_A_ISSUE_URL}}
- PR: {{PROBLEM_A_PR_URL}}
- Branch: `training/problem-a-overbroad-agent-change`
- Student task: decide whether passing checks are enough.
- Expected normal file: `index.html`
- Actual files to inspect: `index.html`, `styles.css`, `README.md`, `docs/agent-extra-notes.md`
- Checks state to observe: passing
- Student clues: tiny copy request, unrelated docs, visual system change, green checks.

## PR 3: Problem B

- Issue: {{PROBLEM_B_ISSUE_URL}}
- PR: {{PROBLEM_B_PR_URL}}
- Branch: `training/problem-b-ci-secret-fixture`
- Student task: decide what to do when Checks fail and a training secret marker appears.
- Expected normal file: `README.md` or one docs file
- Actual files to inspect: `.env`, `index.html`
- Checks state to observe: failing
- Student clues: `.env`, `TRAINING_SECRET_DO_NOT_USE`, removed workshop marker, failing checks.

## Exit Ticket

```text
선택한 PR:
판단: Merge / Request changes / Hold
근거 1:
근거 2:
agent에게 남길 comment:
```

## Instructor Rule

수업 중에는 정답을 먼저 말하지 않는다. 수강생이 `Files changed`, `Diff`, `Checks` 근거를 하나 이상 말한 뒤 판단을 공개한다.
'@
$content = $content.Replace('{{GOOD_ISSUE_URL}}', $good.issue_url)
$content = $content.Replace('{{GOOD_PR_URL}}', $good.pr_url)
$content = $content.Replace('{{PROBLEM_A_ISSUE_URL}}', $problemA.issue_url)
$content = $content.Replace('{{PROBLEM_A_PR_URL}}', $problemA.pr_url)
$content = $content.Replace('{{PROBLEM_B_ISSUE_URL}}', $problemB.issue_url)
$content = $content.Replace('{{PROBLEM_B_PR_URL}}', $problemB.pr_url)
Set-Content -Path docs\sample-pr-scenarios.md -Value $content -Encoding utf8
```

- [ ] **Step 3: Rewrite instructor answer key**

Update `docs/sample-pr-answer-key.md` so each scenario includes:

```markdown
- Operational decision:
- GitHub action:
- Why:
- Common wrong answer:
- Instructor prompt:
- Correction sentence:
```

Use these decisions:

- Good PR: content judgment is Merge; GitHub action in class is no real merge because it is a Draft training PR.
- Problem A: Hold; do not approve; ask the agent to split the PR or reduce scope.
- Problem B: Hold; request changes; do not copy marker value into comments; ask for removal, history review, and CI restoration.

- [ ] **Step 4: Rewrite lecture outline**

In `lectures/02-github-pr-control.md`, update the 2-hour timetable to:

```markdown
| 시간 | 구간 | 목표 |
|---:|---|---|
| 0-10분 | Problem framing | AI agent의 속도보다 merge 판단 기준이 중요하다는 문제의식을 만든다 |
| 10-22분 | GitHub vocabulary for PR judgment | Issue, Branch, PR, Files changed, Diff, Checks, CI/CD를 판단 흐름 안에서 설명한다 |
| 22-35분 | Review protocol | Files changed -> Diff -> Checks -> Decision 순서로 PR을 읽는 법을 익힌다 |
| 35-50분 | 강사 데모 | Training Draft PR 하나로 Issue에서 PR 판단까지 실제 클릭 순서를 보여준다 |
| 50-70분 | Good PR 개인 실습 | merge 가능한 PR의 증거를 찾는다 |
| 70-92분 | Problem A 페어 실습 | CI가 통과해도 scope creep이면 hold한다는 점을 판단한다 |
| 92-106분 | Problem B 페어 실습 | CI 실패와 training secret marker를 merge 중단 신호로 판단한다 |
| 106-114분 | Worktree 운영 사례 | AI agent별 독립 작업공간이 PR 검토를 깔끔하게 만드는 이유를 설명한다 |
| 114-120분 | Exit ticket | 각자 PR 판단 결과와 agent comment를 제출한다 |
```

Add this worktree section:

```markdown
## Worktree 운영 사례

기존 방식에서는 한 폴더에서 여러 agent 작업을 번갈아 보며 `git diff`, `git stash`, branch 전환으로 상태를 관리했다. 이 방식은 변경이 섞였는지 판단하기 어렵고, agent가 만든 diff를 사람이 검토하기 전부터 작업공간이 지저분해질 수 있다.

`git worktree` 방식은 agent마다 별도 폴더와 branch를 준다. 각 agent의 결과가 독립된 PR로 올라오므로, 사람은 로컬 명령어를 외우기보다 PR에서 Files changed, Diff, Checks를 읽고 판단하면 된다.

이 수업에서는 worktree 명령어를 실습하지 않는다. worktree는 AI agent 운영 개념으로만 다룬다.
```

- [ ] **Step 5: Run material verification**

Run:

```powershell
python tools\verify_training_materials.py
```

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

Run:

```powershell
git add docs/pr-review-checklist.md docs/sample-pr-scenarios.md docs/sample-pr-answer-key.md lectures/02-github-pr-control.md
git commit -m "docs: revise lecture 02 around PR judgment"
```

---

### Task 5: Generate The Revised PPTX Deck

**Files:**
- Create: `tools/build_github_pr_deck.py`
- Create: `tools/verify_pptx_layout.py`
- Create: `decks/assets/lecture-02/`
- Modify: `decks/02-github-pr-control-bento-swiss.pptx`

- [ ] **Step 1: Capture GitHub visuals**

Open each Draft PR URL from `docs/training-pr-links.json` in the browser and capture these PNGs:

```text
decks/assets/lecture-02/good-pr-overview.png
decks/assets/lecture-02/good-pr-files-changed.png
decks/assets/lecture-02/problem-a-files-changed.png
decks/assets/lecture-02/problem-a-checks.png
decks/assets/lecture-02/problem-b-files-changed.png
decks/assets/lecture-02/problem-b-checks-failed.png
```

Crop only enough to remove browser chrome. Keep GitHub UI labels visible.

- [ ] **Step 2: Create PPTX generator**

Create `tools/build_github_pr_deck.py` with these implementation rules:

```python
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "decks" / "02-github-pr-control-bento-swiss.pptx"
LINKS = ROOT / "docs" / "training-pr-links.json"
ASSETS = ROOT / "decks" / "assets" / "lecture-02"

FONT_KO = "Malgun Gothic"
FONT_MONO = "Consolas"
INK = RGBColor(17, 17, 17)
MUTED = RGBColor(68, 68, 68)
PAPER = RGBColor(248, 248, 242)
ACCENT = RGBColor(232, 0, 13)
NAVY = RGBColor(26, 26, 46)
TEAL = RGBColor(78, 205, 196)
YELLOW = RGBColor(232, 255, 59)
WHITE = RGBColor(255, 255, 255)


def add_text(slide, text, x, y, w, h, size=24, bold=False, color=INK, font=FONT_KO):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_section_label(slide, label):
    square = slide.shapes.add_shape(1, Inches(0.48), Inches(0.38), Inches(0.13), Inches(0.13))
    square.fill.solid()
    square.fill.fore_color.rgb = ACCENT
    square.line.color.rgb = ACCENT
    add_text(slide, label, 0.72, 0.31, 2.9, 0.25, size=11, bold=True, color=ACCENT, font=FONT_MONO)
    line = slide.shapes.add_shape(1, Inches(0.48), Inches(0.86), Inches(2.9), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.color.rgb = ACCENT


def add_title(slide, label, title, subtitle):
    add_section_label(slide, label)
    add_text(slide, title, 0.72, 1.15, 8.8, 0.75, size=30, bold=True)
    add_text(slide, subtitle, 0.72, 2.0, 8.4, 0.45, size=16, color=MUTED)


def add_card(slide, x, y, w, h, title, body, fill=WHITE):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = RGBColor(221, 221, 221)
    add_text(slide, title, x + 0.16, y + 0.14, w - 0.32, 0.32, size=15, bold=True)
    add_text(slide, body, x + 0.16, y + 0.62, w - 0.32, h - 0.78, size=11, color=MUTED)


def add_asset(slide, filename, x=6.9, y=2.55, w=5.75, h=3.55):
    path = ASSETS / filename
    if path.exists():
        slide.shapes.add_picture(str(path), Inches(x), Inches(y), width=Inches(w), height=Inches(h))
    else:
        add_card(slide, x, y, w, h, "Screenshot needed", filename, WHITE)


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    links = json.loads(LINKS.read_text(encoding="utf-8"))
    scenarios = {item["id"]: item for item in links["scenarios"]}

    slide = prs.slides.add_slide(blank)
    add_title(slide, "LECTURE 02 / GITHUB PR CONTROL", "AI agent PR을 merge해도 되는지 판단하기", "Git 명령어 암기가 아니라 PR 화면에서 근거를 찾는 수업입니다.")
    add_card(slide, 0.72, 3.0, 3.1, 1.2, "핵심 질문", "이 변경을 main에 합쳐도 되는가?", YELLOW)
    add_card(slide, 4.05, 3.0, 3.1, 1.2, "읽는 순서", "Files changed -> Diff -> Checks", TEAL)
    add_card(slide, 7.38, 3.0, 3.1, 1.2, "결정", "Merge / Request changes / Hold", WHITE)

    slide_specs = [
        ("PROBLEM", "속도보다 merge 판단 기준이 중요하다", "Agent는 빠르게 바꿉니다. 사람은 근거로 멈추거나 합쳐야 합니다.", None),
        ("MAP", "오늘은 세 개 Draft PR을 판정한다", "Draft는 수업 안전장치입니다. 판단 연습은 PR 내용과 Checks를 기준으로 합니다.", None),
        ("GLOSSARY", "GitHub 용어는 PR 판단에 필요한 만큼만 배운다", "Issue, Branch, PR, Files changed, Diff, Checks, CI/CD를 화면 위치와 함께 익힙니다.", None),
        ("FLOW", "Issue -> Branch -> PR -> Checks -> Decision", "Issue는 요청, PR은 검문소, Checks는 자동 검사, Decision은 사람의 판단입니다.", None),
        ("PROTOCOL", "PR은 네 단계로 읽는다", "Files changed에서 범위를 보고, Diff에서 내용을 보고, Checks에서 자동 검사를 본 뒤 결정합니다.", None),
        ("DEMO", "강사 데모는 Good PR 하나로 진행한다", scenarios["good-pr"]["pr_url"], "good-pr-overview.png"),
        ("GOOD PR", "작은 요청, 작은 diff, 통과한 checks", "내용상 Merge 판단입니다. 실제 수업 PR은 Draft라서 merge하지 않습니다.", "good-pr-files-changed.png"),
        ("PROBLEM A", "CI가 통과해도 scope creep이면 Hold", "작은 copy 요청에 styles.css, README, unrelated docs가 섞이면 위험 신호입니다.", "problem-a-files-changed.png"),
        ("PROBLEM A", "Problem A의 Checks는 초록색이어도 충분하지 않다", "CI는 자동 검사일 뿐이고 변경 범위 판단은 사람이 합니다.", "problem-a-checks.png"),
        ("PROBLEM B", "CI 실패와 training secret marker는 Hold", ".env와 TRAINING_SECRET_DO_NOT_USE를 보고 값을 복사하지 않습니다.", "problem-b-files-changed.png"),
        ("PROBLEM B", "Problem B의 Checks 실패는 merge 중단 신호다", "실패 로그와 위험 파일을 근거로 request changes 문장을 작성합니다.", "problem-b-checks-failed.png"),
        ("CI/CD", "CI는 깊게, CD는 짧게", "CI는 merge 전 자동 검사입니다. CD는 merge 이후 자동 배포이며 이번 수업에서는 용어만 설명합니다.", None),
        ("DECISION", "Hold는 GitHub 버튼이 아니다", "Hold는 approve하지 않는 운영 판단입니다. 근거를 남기고 수정 요청 또는 blocking comment를 씁니다.", None),
        ("COMMENT", "좋은 agent comment는 위치, 근거, 요청을 담는다", "Checks 실패 로그와 Diff 위치를 말하고, 무엇을 되돌릴지 명확히 요청합니다.", None),
        ("WORKTREE", "AI agent별 작업공간을 분리하면 PR 검토가 쉬워진다", "기존 diff/stash 중심 방식보다 worktree + branch + PR 방식이 변경 범위를 분리합니다.", None),
        ("WORKTREE", "이 수업은 worktree 명령어 실습이 아니다", "Worktree는 운영 개념입니다. 학생은 PR 화면에서 판단 근거를 찾는 데 집중합니다.", None),
        ("PRACTICE", "개인 실습: Good PR", scenarios["good-pr"]["pr_url"], None),
        ("PRACTICE", "페어 실습: Problem A와 Problem B", scenarios["problem-a"]["pr_url"] + "\n" + scenarios["problem-b"]["pr_url"], None),
        ("EXIT", "Exit ticket", "선택한 PR, 판단, 근거 2개, agent에게 남길 comment를 제출합니다.", None),
    ]

    for label, title, subtitle, asset in slide_specs:
        slide = prs.slides.add_slide(blank)
        add_title(slide, label, title, subtitle)
        if asset:
            add_asset(slide, asset)

    prs.save(OUT)


if __name__ == "__main__":
    create_deck()
```

- [ ] **Step 3: Create PPTX layout verifier**

Create `tools/verify_pptx_layout.py` with this content:

```python
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "decks" / "02-github-pr-control-bento-swiss.pptx"
EMU_PER_INCH = 914400
MIN_LABEL_X = int(0.70 * EMU_PER_INCH)
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def slide_number(name: str) -> int:
    return int(re.search(r"slide(\d+)\.xml", name).group(1))


def main() -> int:
    failures: list[str] = []
    with zipfile.ZipFile(PPTX) as zf:
        slides = sorted(
            [name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")],
            key=slide_number,
        )
        if len(slides) < 18:
            failures.append(f"Expected at least 18 slides, found {len(slides)}")
        for name in slides:
            root = ET.fromstring(zf.read(name))
            number = slide_number(name)
            for shape in root.findall(".//p:sp", NS):
                text = "".join(node.text or "" for node in shape.findall(".//a:t", NS)).strip()
                if not text:
                    continue
                xfrm = shape.find(".//a:xfrm", NS)
                if xfrm is None:
                    continue
                off = xfrm.find("a:off", NS)
                if off is None:
                    continue
                x = int(off.get("x"))
                y = int(off.get("y"))
                if y < int(0.75 * EMU_PER_INCH) and text.isupper() and x < MIN_LABEL_X:
                    failures.append(f"Slide {number}: top label '{text}' starts too far left at {x}")
        all_text = []
        for name in slides:
            root = ET.fromstring(zf.read(name))
            all_text.extend(node.text or "" for node in root.findall(".//a:t", NS))
        joined = "\n".join(all_text)
        for required in ["Files changed", "Diff", "Checks", "Draft", "Hold", "Worktree", "CI", "CD"]:
            if required not in joined:
                failures.append(f"Deck missing required term: {required}")
    if failures:
        print("PPTX verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("PPTX verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Build the deck**

Run:

```powershell
python tools\build_github_pr_deck.py
```

Expected: `decks/02-github-pr-control-bento-swiss.pptx` is rewritten with 18 or more slides.

- [ ] **Step 5: Verify the deck structure**

Run:

```powershell
python tools\verify_pptx_layout.py
```

Expected: PASS.

- [ ] **Step 6: Manually inspect in PowerPoint**

Open `decks/02-github-pr-control-bento-swiss.pptx` and verify:

- Korean text renders in Malgun Gothic.
- No slide has top-left red square/text overlap.
- GitHub screenshots are readable.
- PR links are visible on scenario slides.
- Slide text is not crowded.

- [ ] **Step 7: Commit Task 5**

Run:

```powershell
git add tools/build_github_pr_deck.py tools/verify_pptx_layout.py decks/assets/lecture-02 decks/02-github-pr-control-bento-swiss.pptx
git commit -m "docs: regenerate lecture 02 github pr deck"
```

---

### Task 6: Final Verification And Cleanup

**Files:**
- Verify all changed files

- [ ] **Step 1: Run all local checks**

Run:

```powershell
python tools\verify_training_materials.py
python tools\verify_pptx_layout.py
Select-String -Path index.html -Pattern 'data-workshop-page="lecture-02"' -Quiet
Select-String -Path index.html -Pattern '<title>AI Agent Workshop</title>' -Quiet
Get-ChildItem -Recurse -File -Exclude *.md | Select-String -Pattern 'sk-[A-Za-z0-9_-]{8,}'
```

Expected:

- First two commands print `passed`.
- The two `Select-String -Quiet` commands print `True`.
- The final secret-like search prints no matches on the implementation branch.

- [ ] **Step 2: Confirm student materials do not leak answers**

Run:

```powershell
rg -n "Operational decision|expected_decision|answer key|정답" docs\sample-pr-scenarios.md
```

Expected: no matches.

- [ ] **Step 3: Confirm instructor answer key has decisions**

Run:

```powershell
rg -n "Operational decision|GitHub action|Common wrong answer|Correction sentence" docs\sample-pr-answer-key.md
```

Expected: matches for all three PR scenarios.

- [ ] **Step 4: Confirm old closed PR links are absent from student path**

Run:

```powershell
rg -n "/pull/(1|2|3)\b|sample/good-pr-checklist-copy|sample/problem-overbroad-agent-change|sample/problem-failing-ci-secret-like-file" README.md lectures docs/pr-review-checklist.md docs/sample-pr-scenarios.md docs/sample-pr-answer-key.md
```

Expected: no matches in student-facing materials. If history notes are needed, keep them outside `README.md`, `lectures/`, and `docs/sample-pr-scenarios.md`.

- [ ] **Step 5: Review the diff**

Run:

```powershell
git diff --stat main...HEAD
git diff -- README.md CONTEXT.md .github/workflows/check.yml lectures/02-github-pr-control.md docs/pr-review-checklist.md docs/sample-pr-scenarios.md docs/sample-pr-answer-key.md
```

Expected: diff reflects PR judgment-centered expansion, training safety language, explicit CI marker, and updated Draft PR links.

- [ ] **Step 6: Final commit if verification changed files**

If verification caused tracked file updates, run:

```powershell
git add README.md CONTEXT.md .github/workflows/check.yml lectures/02-github-pr-control.md docs/pr-review-checklist.md docs/sample-pr-scenarios.md docs/sample-pr-answer-key.md docs/training-pr-links.json tools/build_github_pr_deck.py tools/verify_training_materials.py tools/verify_pptx_layout.py decks/assets/lecture-02 decks/02-github-pr-control-bento-swiss.pptx
git commit -m "docs: finalize lecture 02 pr judgment materials"
```

- [ ] **Step 7: Push implementation branch**

Run:

```powershell
git push -u origin codex/lecture-02-pr-feedback-plan
```

Expected: branch is pushed and ready for PR creation.

---

## Not In Scope

- Teaching students to execute `git worktree`, `git stash`, or `git diff` commands.
- Teaching deployment or CD implementation.
- Asking students to merge PRs.
- Asking students to leave real GitHub review comments during class.
- Using real secrets or realistic API key values.
- Preserving old closed PR #1-#3 as the main student path.

## Self-Review Checklist

- [ ] Every requested autoplan feedback item is mapped to a task.
- [ ] The plan keeps PR judgment as the central student workflow.
- [ ] Worktree stays as an AI agent operations concept, not student command practice.
- [ ] Secret fixture uses `TRAINING_SECRET_DO_NOT_USE`, not `sk-...`.
- [ ] New Draft PRs and Issues use `[TRAINING - DO NOT MERGE]`.
- [ ] Student docs hide instructor decisions.
- [ ] PPTX layout verification checks top-left label overlap.
- [ ] Manual PowerPoint visual check is required before completion.
