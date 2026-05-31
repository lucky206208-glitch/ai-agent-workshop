# Sample PR Instructor Answer Key

이 문서는 강사용이다. 수업 전에 학생에게 먼저 공유하지 않는다.

## PR 1: Good PR

- Branch: `sample/good-pr-checklist-copy`
- Title: `docs: add PR review checklist link`
- Operational decision: Merge
- GitHub action: Merge
- Why: 변경 파일이 `README.md`, `index.html`로 제한되고 checklist entry point 추가라는 issue 요구와 diff가 일치한다.
- Instructor prompt: "이 PR에서 merge 가능하다는 근거를 Files changed, Diff, Checks 중 어디서 찾을 수 있나요?"

## PR 2: Problem A

- Branch: `sample/problem-overbroad-agent-change`
- Title: `style: over-expand small copy request`
- Operational decision: Hold
- GitHub action: Do not approve. Leave a blocking comment asking the agent to split or reduce the PR.
- Why: 작은 copy 변경 요청에 전체 CSS 교체, README roadmap 추가, unrelated notes file 생성이 섞여 있다.
- Instructor prompt: "이 PR이 CI를 통과해도 merge하면 안 되는 이유는 무엇인가요?"

## PR 3: Problem B

- Branch: `sample/problem-failing-ci-secret-like-file`
- Title: `chore: add local demo env file`
- Operational decision: Hold
- GitHub action: Request changes. Do not copy the secret-like value into comments.
- Why: `.env`와 secret-like 문자열이 포함되고, required marker 삭제로 CI가 실패한다.
- Instructor prompt: "이 경우 단순히 파일 삭제 요청만 하면 충분할까요? history 노출과 키 회전은 어떻게 판단해야 할까요?"

## High-Risk Rule

Secret-like 변경은 일반 품질 문제가 아니라 보안 사고 가능성으로 취급한다. 실제 키일 수 있으면 merge 금지, 값 재공유 금지, 키 회전 또는 폐기, history 노출 확인을 요구한다.
