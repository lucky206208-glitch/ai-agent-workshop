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
