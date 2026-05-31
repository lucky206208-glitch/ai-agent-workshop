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
