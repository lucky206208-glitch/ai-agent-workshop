# Lecture 02 GitHub PR Control Materials Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the 2nd lecture materials for teaching beginners how to control AI agent changes through GitHub PR review, including a Korean instructor guide, two PPTX deck variants, and three sample PRs.

**Architecture:** Keep the workshop repo small: one static demo site, one CI workflow, one instructor Markdown file, and generated decks. The sample PRs live as GitHub branches/PRs so students can inspect real `Files changed`, `Checks`, and review states without learning Git commands first.

**Tech Stack:** Git/GitHub, GitHub Actions, static HTML/CSS, Markdown, artifact-tool presentation JSX, local `pptx-design-styles` guidance, PowerPoint PPTX.

---

## File Structure

- Create `README.md` as the workshop landing page and student-facing repo orientation.
- Create `index.html` and `styles.css` as the tiny static site used by sample PRs.
- Create `.github/workflows/check.yml` as the simple PR check that catches broken HTML markers and demo secret-like strings.
- Create `lectures/02-github-pr-control.md` as the Korean instructor guide.
- Create `decks/02-github-pr-control-bento-swiss.pptx` as the primary teaching deck.
- Create `decks/02-github-pr-control-gradient-mesh.pptx` as the design alternative deck.
- Create `docs/pr-review-checklist.md` as a reusable one-page checklist for students.
- Create `docs/sample-pr-scenarios.md` as a reference index for the three PR exercises and their intended teaching points.
- Create temporary presentation build files only under `outputs/<thread-id>/presentations/lecture-02-github-pr-control/`; do not commit those scratch files.

## Branch And PR Names

- Base material branch: `codex/lecture-02-github-pr-control-materials`
- Good PR branch: `sample/good-pr-checklist-copy`
- Problem PR A branch: `sample/problem-overbroad-agent-change`
- Problem PR B branch: `sample/problem-failing-ci-secret-like-file`

## Commit Strategy

- Commit 1: base static site and CI.
- Commit 2: instructor guide and student checklist.
- Commit 3: sample PR scenario index.
- Commit 4: Bento+Swiss deck.
- Commit 5: Gradient Mesh deck.
- Sample PR branches are committed separately and pushed as PRs against `main`.

---

### Task 1: Repository Preflight And Baseline

**Files:**
- Verify: repository root
- Verify: `.gitignore`

- [ ] **Step 1: Confirm repo and current branch**

Run:

```powershell
git remote -v
git status --short --branch
git branch --show-current
```

Expected:

```text
origin  https://github.com/lucky206208-glitch/ai-agent-workshop.git (fetch)
origin  https://github.com/lucky206208-glitch/ai-agent-workshop.git (push)
## codex/lecture-02-github-pr-control-plan
codex/lecture-02-github-pr-control-plan
```

- [ ] **Step 2: Confirm `.worktrees/` stays ignored**

Run:

```powershell
git check-ignore -v .worktrees/
```

Expected includes:

```text
.gitignore:1:.worktrees/
```

- [ ] **Step 3: Check push path before PR work**

Run:

```powershell
git ls-remote --heads origin main
git push --dry-run origin HEAD:refs/heads/codex/lecture-02-github-pr-control-materials
```

Expected:

```text
Everything up-to-date
```

If the dry run rejects authentication or permissions, stop PR creation work and report that the repo can be read but not written from this environment. Continue creating local files and decks in the worktree.

- [ ] **Step 4: Create implementation branch from the worktree**

Run:

```powershell
git switch -c codex/lecture-02-github-pr-control-materials
```

Expected:

```text
Switched to a new branch 'codex/lecture-02-github-pr-control-materials'
```

- [ ] **Step 5: Commit**

No commit in this task unless `.gitignore` needed changes. If it did, run:

```powershell
git add .gitignore
git commit -m "chore: keep worktrees out of workshop repo"
```

---

### Task 2: Create Static Demo Site And CI

**Files:**
- Create: `README.md`
- Create: `index.html`
- Create: `styles.css`
- Create: `.github/workflows/check.yml`

- [ ] **Step 1: Create `README.md`**

Create `README.md` with this content:

```markdown
# AI Agent Workshop

AI agent가 만든 변경사항을 GitHub PR로 검증하는 실습 repo입니다.

## Lecture 02: GitHub PR Control

수강생은 이 repo에서 세 가지 PR을 비교합니다.

1. 좋은 PR: 요구사항이 작고 변경 범위가 명확합니다.
2. 문제 PR A: 작은 요청인데 agent가 관련 없는 파일까지 크게 바꿉니다.
3. 문제 PR B: CI가 실패하고 secret-like 문자열이 포함됩니다.

## Student Goal

Git 명령어를 외우는 것이 목표가 아닙니다. PR에서 `Files changed`, `Checks`, `Conversation`을 읽고 `merge`, `request changes`, `hold` 중 하나를 근거와 함께 선택하는 것이 목표입니다.

## Design Reference

External decks use: `Design reference: corazzon/pptx-design-styles (MIT)`.
```

- [ ] **Step 2: Create `index.html`**

Create `index.html` with this content:

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI Agent Workshop</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body data-workshop-page="lecture-02">
    <main class="page">
      <section class="hero">
        <p class="eyebrow">Lecture 02</p>
        <h1>GitHub PR로 AI Agent 작업 통제하기</h1>
        <p class="lead">
          Agent가 코드를 바꾸는 속도보다 사람이 변경을 검증하는 기준이 더 중요합니다.
        </p>
      </section>
      <section class="grid" aria-label="PR review checkpoints">
        <article>
          <h2>Files changed</h2>
          <p>어떤 파일이 바뀌었는지 먼저 봅니다.</p>
        </article>
        <article>
          <h2>Diff</h2>
          <p>agent 설명과 실제 변경이 같은지 확인합니다.</p>
        </article>
        <article>
          <h2>Checks</h2>
          <p>CI가 실패하면 merge하지 않습니다.</p>
        </article>
      </section>
    </main>
  </body>
</html>
```

- [ ] **Step 3: Create `styles.css`**

Create `styles.css` with this content:

```css
:root {
  color-scheme: light;
  --ink: #111111;
  --muted: #444444;
  --paper: #f8f8f2;
  --accent: #e8000d;
  --navy: #1a1a2e;
  --yellow: #e8ff3b;
  --teal: #4ecdc4;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: var(--paper);
  color: var(--ink);
}

.page {
  width: min(1040px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 64px 0;
}

.hero {
  border-left: 8px solid var(--accent);
  padding-left: 28px;
  margin-bottom: 36px;
}

.eyebrow {
  margin: 0 0 12px;
  font-family: "Courier New", monospace;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
}

h1 {
  max-width: 760px;
  margin: 0;
  font-size: clamp(36px, 6vw, 68px);
  line-height: 0.98;
}

.lead {
  max-width: 680px;
  margin: 20px 0 0;
  color: var(--muted);
  font-size: 20px;
  line-height: 1.55;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

article {
  min-height: 180px;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #dddddd;
}

article:first-child {
  background: var(--navy);
  color: #ffffff;
}

article:nth-child(2) {
  background: var(--yellow);
}

article:nth-child(3) {
  background: var(--teal);
}

h2 {
  margin: 0 0 48px;
  font-size: 24px;
}

article p {
  margin: 0;
  font-size: 16px;
  line-height: 1.45;
}

@media (max-width: 760px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 4: Create `.github/workflows/check.yml`**

Create `.github/workflows/check.yml` with this content:

```yaml
name: workshop-check

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  static-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check required workshop marker
        run: grep -q 'data-workshop-page="lecture-02"' index.html
      - name: Block demo secret-like strings
        run: |
          if grep -RIn --exclude-dir=.git --exclude='*.md' 'sk-[A-Za-z0-9_-]\{8,\}' .; then
            echo "Secret-like string detected. Remove it before merge."
            exit 1
          fi
      - name: Check page title
        run: grep -q '<title>AI Agent Workshop</title>' index.html
```

- [ ] **Step 5: Verify locally with Git Bash if available**

Run:

```powershell
git status --short
```

Expected:

```text
?? .github/
?? README.md
?? index.html
?? styles.css
```

- [ ] **Step 6: Commit**

Run:

```powershell
git add README.md index.html styles.css .github/workflows/check.yml
git commit -m "feat: add workshop static site and PR checks"
```

Expected includes:

```text
[codex/lecture-02-github-pr-control-materials
```

---

### Task 3: Create Student Checklist And Scenario Index

**Files:**
- Create: `docs/pr-review-checklist.md`
- Create: `docs/sample-pr-scenarios.md`

- [ ] **Step 1: Create `docs/pr-review-checklist.md`**

Create `docs/pr-review-checklist.md` with this content:

```markdown
# PR Review Checklist

## 1. 요청과 PR 설명이 같은가

- Issue가 요구한 작업을 한 문장으로 다시 말한다.
- PR description이 그 요구를 그대로 해결하는지 확인한다.
- 설명에 없는 큰 변경이 있으면 merge하지 않는다.

## 2. Files changed를 먼저 본다

- 변경 파일 수가 요청 규모와 맞는지 본다.
- 관련 없는 파일, 설정 파일, secret 파일, 테스트 삭제가 있는지 본다.
- 이해할 수 없는 파일이 있으면 agent에게 이유를 묻는다.

## 3. Diff를 읽는다

- 새 코드나 문구가 요구사항과 일치하는지 본다.
- 삭제된 내용이 필요한 기능인지 확인한다.
- 큰 diff는 작은 PR로 나누라고 요청한다.

## 4. Checks를 확인한다

- CI가 실패하면 merge하지 않는다.
- 실패 로그에서 원인을 한 줄로 요약한다.
- agent에게 실패 로그를 붙여서 수정 요청한다.

## 5. 결정한다

| 판단 | 기준 | 다음 행동 |
|---|---|---|
| Merge | 요청과 diff가 일치하고 checks가 통과했다 | merge한다 |
| Request changes | 방향은 맞지만 수정할 점이 명확하다 | comment로 수정 요청한다 |
| Hold | 범위가 크거나 위험한 변경이 있다 | merge를 보류하고 PR을 쪼개게 한다 |
```

- [ ] **Step 2: Create `docs/sample-pr-scenarios.md`**

Create `docs/sample-pr-scenarios.md` with this content:

```markdown
# Sample PR Scenarios

## PR 1: Good PR

- Branch: `sample/good-pr-checklist-copy`
- Title: `docs: add PR review checklist link`
- Expected decision: Merge
- Teaching point: 요청, 변경 파일, diff, checks가 모두 일치하면 merge할 수 있다.

## PR 2: Problem A

- Branch: `sample/problem-overbroad-agent-change`
- Title: `style: over-expand small copy request`
- Expected decision: Hold
- Teaching point: 작은 문구 수정 요청인데 unrelated files와 큰 스타일 변경이 섞이면 merge하지 않는다.

## PR 3: Problem B

- Branch: `sample/problem-failing-ci-secret-like-file`
- Title: `chore: add local demo env file`
- Expected decision: Request changes
- Teaching point: CI 실패와 secret-like 문자열은 agent에게 수정 요청해야 한다.

## Instructor Rule

수업 중에는 정답을 먼저 말하지 않는다. 수강생이 `Files changed`, `Diff`, `Checks` 근거를 하나 이상 말한 뒤 판단을 공개한다.
```

- [ ] **Step 3: Commit**

Run:

```powershell
git add docs/pr-review-checklist.md docs/sample-pr-scenarios.md
git commit -m "docs: add PR review student materials"
```

---

### Task 4: Write Korean Instructor Guide

**Files:**
- Create: `lectures/02-github-pr-control.md`

- [ ] **Step 1: Create lecture directory and file**

Create `lectures/02-github-pr-control.md` with this exact structure and content:

```markdown
# 2회차 강사용 수업안: GitHub PR로 AI Agent 작업 통제하기

## 수업 목표

수강생은 Git 명령어를 외우지 않고도 AI agent가 만든 PR을 검토하고 merge 여부를 판단할 수 있어야 한다.

## 2시간 시간표

| 시간 | 구간 | 목표 |
|---:|---|---|
| 0-15분 | Mental model | GitHub는 agent 작업의 검문소라는 관점을 만든다 |
| 15-30분 | 최소 개념 | commit, branch, PR, merge, CI를 한 문장으로 설명한다 |
| 30-50분 | 강사 데모 | issue에서 PR까지 흐름을 보여준다 |
| 50-75분 | 좋은 PR 읽기 | merge 가능한 PR의 조건을 찾는다 |
| 75-100분 | 문제 PR 읽기 | merge하면 안 되는 신호를 찾는다 |
| 100-115분 | 판단표 실습 | merge, request changes, hold를 근거와 함께 선택한다 |
| 115-120분 | 과제 안내 | 다음 수업 전 개인 PR 검토 과제를 낸다 |

## 강의 핵심 문장

Agent가 코드를 바꾸는 속도보다 사람이 변경을 검증하는 기준이 더 중요하다.

## 최소 개념 설명

- `commit`: 저장된 변경 스냅샷이다.
- `branch`: main과 분리된 작업 줄기다.
- `PR`: 이 변경을 main에 합쳐도 되는지 검토하는 제안서다.
- `merge`: 검토가 끝난 변경을 main에 합치는 행동이다.
- `CI`: 사람이 놓칠 수 있는 기계적 검사를 자동으로 돌리는 장치다.

## 강사 데모 스크립트

1. GitHub issue를 연다.
2. issue 요구사항을 한 문장으로 읽는다.
3. agent가 만든 PR을 연다.
4. PR description을 읽는다.
5. `Files changed` 탭으로 이동한다.
6. 변경 파일 수와 파일명을 먼저 확인한다.
7. diff가 issue 요구와 같은지 확인한다.
8. `Checks`가 통과했는지 확인한다.
9. merge, request changes, hold 중 하나를 선택한다.

## 실습 1: 좋은 PR 검토

학생에게 먼저 묻는다.

> 이 PR을 merge해도 된다고 판단하려면 어떤 근거가 필요할까요?

기대 답변:

- 변경 파일이 요청 범위 안에 있다.
- PR 설명과 diff가 일치한다.
- CI가 통과했다.

## 실습 2: 문제 PR A 검토

학생에게 먼저 묻는다.

> issue는 작은 요청인데 변경 파일이 많다면 무엇을 의심해야 할까요?

기대 답변:

- agent가 관련 없는 리팩터링을 섞었을 수 있다.
- 스타일이나 설정 변경이 요청과 무관할 수 있다.
- PR을 나누라고 요청해야 한다.

## 실습 3: 문제 PR B 검토

학생에게 먼저 묻는다.

> CI가 실패하고 secret처럼 보이는 문자열이 있으면 어떤 결정을 해야 할까요?

기대 답변:

- merge하지 않는다.
- 실패 로그를 읽는다.
- agent에게 로그와 함께 수정 요청한다.

## Merge 판단표

| 판단 | 수업 중 사용하는 문장 |
|---|---|
| Merge | 요청과 diff가 일치하고 checks가 통과했으므로 merge합니다 |
| Request changes | 방향은 맞지만 수정할 점이 있어 comment를 남깁니다 |
| Hold | 변경 범위나 위험이 커서 이 PR은 보류합니다 |

## 예상 질문과 답변

### Git을 몰라도 PR을 볼 수 있나요?

볼 수 있다. 이 수업의 목표는 Git 내부 구조가 아니라 PR 검토 화면에서 위험 신호를 찾는 것이다.

### CI가 초록색이면 무조건 merge해도 되나요?

아니다. CI는 자동 검사일 뿐이다. PR 설명과 diff가 맞는지 사람의 검토가 필요하다.

### Agent가 만든 설명을 믿어도 되나요?

설명은 출발점일 뿐이다. 항상 `Files changed`와 diff를 기준으로 확인한다.

## 과제

수강생은 세 개의 sample PR 중 하나를 골라 다음 형식으로 판단을 제출한다.

```text
선택한 PR:
판단: Merge / Request changes / Hold
근거 1:
근거 2:
agent에게 남길 comment:
```

## 강사용 체크리스트

- 수업 전 sample PR 3개가 열리는지 확인한다.
- 좋은 PR의 CI가 통과했는지 확인한다.
- 문제 PR B의 CI가 실패하는지 확인한다.
- 학생에게 정답을 먼저 말하지 않는다.
- 모든 판단에는 `Files changed`, `Diff`, `Checks` 중 하나 이상의 근거를 요구한다.

## Design Reference

Design reference: corazzon/pptx-design-styles (MIT)
```

- [ ] **Step 2: Commit**

Run:

```powershell
git add lectures/02-github-pr-control.md
git commit -m "docs: add lecture 02 instructor guide"
```

---

### Task 5: Create The Three Sample PR Branches

**Files:**
- Modify in branch `sample/good-pr-checklist-copy`: `README.md`, `index.html`
- Modify in branch `sample/problem-overbroad-agent-change`: `index.html`, `styles.css`, `README.md`, `docs/agent-extra-notes.md`
- Modify in branch `sample/problem-failing-ci-secret-like-file`: `.env`, `index.html`

- [ ] **Step 1: Push base material branch**

Run:

```powershell
git push -u origin codex/lecture-02-github-pr-control-materials
```

Expected: branch is pushed. If authentication fails, skip remote PR creation and keep local branches for later push.

- [ ] **Step 2: Create good PR branch**

Run:

```powershell
git switch main
git merge --ff-only codex/lecture-02-github-pr-control-materials
git switch -c sample/good-pr-checklist-copy
```

- [ ] **Step 3: Modify good PR files**

In `README.md`, add this section after `## Student Goal`:

```markdown
## Review Checklist

수업 중에는 [`docs/pr-review-checklist.md`](docs/pr-review-checklist.md)를 열고 PR 판단 근거를 표시합니다.
```

In `index.html`, add this fourth card inside `<section class="grid" aria-label="PR review checkpoints">`:

```html
        <article>
          <h2>Decision</h2>
          <p>merge, request changes, hold 중 하나를 근거와 함께 선택합니다.</p>
        </article>
```

- [ ] **Step 4: Commit and push good PR branch**

Run:

```powershell
git add README.md index.html
git commit -m "docs: add PR checklist entry point"
git push -u origin sample/good-pr-checklist-copy
gh pr create --base main --head sample/good-pr-checklist-copy --title "docs: add PR review checklist link" --body "Good PR sample for Lecture 02. Expected student decision: Merge."
```

- [ ] **Step 5: Create problem PR A branch**

Run:

```powershell
git switch main
git switch -c sample/problem-overbroad-agent-change
```

- [ ] **Step 6: Modify problem PR A files**

Replace the `h1` text in `index.html` with:

```html
        <h1>AI Agent Workshop Portal</h1>
```

Append this unrelated section to `README.md`:

```markdown
## Unrelated Roadmap

이 섹션은 현재 issue 범위를 벗어난 예시입니다. 작은 문구 수정 PR에 이런 큰 방향 변경이 섞이면 hold 판단을 해야 합니다.
```

Replace `styles.css` with a visibly different visual system:

```css
body {
  margin: 0;
  font-family: "Courier New", monospace;
  background: #0a0014;
  color: #ffffff;
}

.page {
  width: min(980px, calc(100vw - 24px));
  margin: 0 auto;
  padding: 48px 0;
}

.hero {
  padding: 32px;
  border: 4px solid #ff0080;
  box-shadow: 12px 12px 0 #00ffff;
}

.eyebrow {
  color: #ffff00;
  text-transform: uppercase;
}

h1 {
  font-size: clamp(40px, 8vw, 88px);
  line-height: 1;
  text-shadow: 3px 3px 0 #ff0080;
}

.lead {
  font-size: 18px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 32px;
}

article {
  padding: 24px;
  border: 3px solid #ffffff;
  background: #1a0533;
}
```

Create `docs/agent-extra-notes.md`:

```markdown
# Agent Extra Notes

이 파일은 문제 PR A를 위한 unrelated file 예시입니다. issue와 무관한 파일이 섞였는지 확인하는 훈련에 사용합니다.
```

- [ ] **Step 7: Commit and push problem PR A**

Run:

```powershell
git add README.md index.html styles.css docs/agent-extra-notes.md
git commit -m "style: over-expand small copy request"
git push -u origin sample/problem-overbroad-agent-change
gh pr create --base main --head sample/problem-overbroad-agent-change --title "style: over-expand small copy request" --body "Problem PR A for Lecture 02. Expected student decision: Hold because the diff is much wider than the request."
```

- [ ] **Step 8: Create problem PR B branch**

Run:

```powershell
git switch main
git switch -c sample/problem-failing-ci-secret-like-file
```

- [ ] **Step 9: Modify problem PR B files**

Create `.env`:

```text
DEMO_API_KEY=sk-demo-not-real-key-123456
```

In `index.html`, remove this attribute from `<body>`:

```html
data-workshop-page="lecture-02"
```

The resulting opening body tag should be:

```html
  <body>
```

- [ ] **Step 10: Commit and push problem PR B**

Run:

```powershell
git add .env index.html
git commit -m "chore: add local demo env file"
git push -u origin sample/problem-failing-ci-secret-like-file
gh pr create --base main --head sample/problem-failing-ci-secret-like-file --title "chore: add local demo env file" --body "Problem PR B for Lecture 02. Expected student decision: Request changes because CI fails and a secret-like string was committed."
```

- [ ] **Step 11: Return to implementation branch**

Run:

```powershell
git switch codex/lecture-02-github-pr-control-materials
```

---

### Task 6: Build Bento+Swiss PPTX

**Files:**
- Create: `decks/02-github-pr-control-bento-swiss.pptx`
- Use scratch: `outputs/<thread-id>/presentations/lecture-02-github-pr-control/`

- [ ] **Step 1: Activate deck skills**

Use these skills before building the deck:

```text
presentations:Presentations
pptx-design-styles
```

- [ ] **Step 2: Lock Bento+Swiss design system**

Use this design system:

```text
Primary style: Bento Grid
Fallback style: Swiss International Style
Background: #F8F8F2
Dark anchor cell: #1A1A2E
Accent yellow: #E8FF3B
Accent coral: #FF6B6B
Accent teal: #4ECDC4
Swiss rule red: #E8000D
Primary text: #111111
Secondary text: #444444
Title font: Arial Bold, 34-44pt
Body font: Arial, 14-18pt
Label font: Courier New, 9-11pt
Signature: asymmetric bento cells plus Swiss red rule for section structure
Avoid: equal card grids, decorative gradients, dense paragraph slides
```

- [ ] **Step 3: Build 12-slide claim spine**

Use these slides:

```text
1. Title — Agent 시대의 안전장치는 PR이다
2. Why — 코드를 빨리 바꾸는 것보다 검증 기준이 중요하다
3. Mental Model — GitHub는 작업대장이자 검문소다
4. Vocabulary — commit, branch, PR, merge, CI를 한 문장으로 이해한다
5. Workflow — issue에서 PR 검토까지의 전체 흐름
6. Read Order — Files changed → Diff → Checks 순서로 본다
7. Good PR — merge 가능한 PR의 증거
8. Problem A — 작은 요청에 큰 변경이 섞인 PR
9. Problem B — CI 실패와 secret-like 문자열
10. Decision Matrix — merge/request changes/hold 판단표
11. Agent Correction Loop — 실패 로그와 diff 근거로 수정 요청한다
12. Assignment — PR 하나를 골라 판단 근거를 제출한다
```

- [ ] **Step 4: Render and export**

Use artifact-tool presentation JSX through the Presentations skill. Save the final PPTX at:

```text
decks/02-github-pr-control-bento-swiss.pptx
```

- [ ] **Step 5: Commit**

Run:

```powershell
git add decks/02-github-pr-control-bento-swiss.pptx
git commit -m "docs: add bento swiss lecture 02 deck"
```

---

### Task 7: Build Gradient Mesh PPTX

**Files:**
- Create: `decks/02-github-pr-control-gradient-mesh.pptx`
- Use scratch: `outputs/<thread-id>/presentations/lecture-02-github-pr-control-gradient/`

- [ ] **Step 1: Reuse the same claim spine**

Use the exact same 12-slide claim spine from Task 6 so design differences are comparable.

- [ ] **Step 2: Lock Gradient Mesh design system**

Use this design system:

```text
Primary style: Gradient Mesh
Background: multi-point radial gradient using #FF6EC7, #7B61FF, #00D4FF, #FFB347
Text: #FFFFFF on darkened mesh zones
Panel: #111111 at 70% opacity for dense checklist content
Title font: Barlow Condensed ExtraBold or Arial Bold, 44-64pt
Body font: Arial, 14-18pt
Label font: Courier New, 9-11pt
Signature: painterly multi-radial gradient, large white claim titles, dark translucent panels for PR evidence
Avoid: low-contrast text, gradient behind dense tables, more than one proof object per slide
```

- [ ] **Step 3: Keep content readability gate**

For slides 4, 6, 10, and 12, place dense text on dark translucent panels. Use direct labels, not legends. If any slide needs more than six bullets, split it or convert it to a table.

- [ ] **Step 4: Render and export**

Use artifact-tool presentation JSX through the Presentations skill. Save the final PPTX at:

```text
decks/02-github-pr-control-gradient-mesh.pptx
```

- [ ] **Step 5: Commit**

Run:

```powershell
git add decks/02-github-pr-control-gradient-mesh.pptx
git commit -m "docs: add gradient mesh lecture 02 deck"
```

---

### Task 8: Final Verification

**Files:**
- Verify: `lectures/02-github-pr-control.md`
- Verify: `decks/02-github-pr-control-bento-swiss.pptx`
- Verify: `decks/02-github-pr-control-gradient-mesh.pptx`
- Verify: GitHub PR links

- [ ] **Step 1: Verify required files exist**

Run:

```powershell
Test-Path lectures/02-github-pr-control.md
Test-Path decks/02-github-pr-control-bento-swiss.pptx
Test-Path decks/02-github-pr-control-gradient-mesh.pptx
Get-Item decks/02-github-pr-control-bento-swiss.pptx, decks/02-github-pr-control-gradient-mesh.pptx | Select-Object Name,Length
```

Expected:

```text
True
True
True
```

Both PPTX lengths should be greater than `10000` bytes.

- [ ] **Step 2: Verify Markdown timing matches slide spine**

Run:

```powershell
Select-String -Path lectures/02-github-pr-control.md -Pattern "0-15분","75-100분","Merge 판단표","Design Reference"
```

Expected: all four patterns are found.

- [ ] **Step 3: Verify sample PR branches exist locally**

Run:

```powershell
git branch --list "sample/*"
```

Expected:

```text
sample/good-pr-checklist-copy
sample/problem-overbroad-agent-change
sample/problem-failing-ci-secret-like-file
```

- [ ] **Step 4: Verify GitHub PRs if push was available**

Run:

```powershell
gh pr list --repo lucky206208-glitch/ai-agent-workshop --state open --json number,title,headRefName,statusCheckRollup
```

Expected:

```text
docs: add PR review checklist link
style: over-expand small copy request
chore: add local demo env file
```

If `gh` is unavailable or unauthenticated, verify in the browser and record the three PR URLs in `docs/sample-pr-scenarios.md`.

- [ ] **Step 5: Run final status**

Run:

```powershell
git status --short --branch
```

Expected:

```text
## codex/lecture-02-github-pr-control-materials
```

No untracked or modified files should remain except intentionally retained generated PPTX files before their commit.

- [ ] **Step 6: Commit final verification notes if PR URLs were added**

Run only if `docs/sample-pr-scenarios.md` changed:

```powershell
git add docs/sample-pr-scenarios.md
git commit -m "docs: record sample PR links"
```

---

## Self-Review

Spec coverage:

- Korean instructor guide is covered by Task 4.
- Static demo site and CI are covered by Task 2.
- Good PR and two problem PRs are covered by Task 5.
- Bento+Swiss PPTX is covered by Task 6.
- Gradient Mesh PPTX is covered by Task 7.
- Verification is covered by Task 8.

Placeholder scan:

- The plan contains exact file paths, branch names, slide claims, command lines, and expected outputs.
- The plan intentionally avoids unresolved placeholder markers.

Type and naming consistency:

- Lecture file path is consistently `lectures/02-github-pr-control.md`.
- Deck paths are consistently under `decks/`.
- Sample branch names match `docs/sample-pr-scenarios.md`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-31-lecture-02-github-pr-control-materials.md`. Two execution options:

1. Subagent-Driven (recommended): dispatch a fresh subagent per task, review between tasks, fast iteration.
2. Inline Execution: execute tasks in this session using `superpowers:executing-plans`, batch execution with checkpoints.

