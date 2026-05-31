# Sample PR Scenarios

All scenarios use Draft PRs with `[TRAINING - DO NOT MERGE]` in the title. Draft status is a class safety guardrail. Judge the PR content by reading Files changed, Diff, and Checks.

## PR 1: Good PR

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/6
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/8
- Branch: `training/good-pr-small-checklist-entry`
- Student task: decide whether the content is mergeable.
- Expected files to inspect: `README.md`, `index.html`
- Checks state to observe: passing
- Student clues: small request, small file list, matching diff, green checks.

## PR 2: Problem A

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/7
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/9
- Branch: `training/problem-a-overbroad-agent-change`
- Student task: decide whether passing checks are enough.
- Expected normal file: `index.html`
- Actual files to inspect: `index.html`, `styles.css`, `README.md`, `docs/agent-extra-notes.md`
- Checks state to observe: passing
- Student clues: tiny copy request, unrelated docs, visual system change, green checks.

## PR 3: Problem B

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/5
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/10
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

수업 중에는 결론을 먼저 말하지 않는다. 수강생이 `Files changed`, `Diff`, `Checks` 근거를 하나 이상 말한 뒤 판단을 공개한다.
