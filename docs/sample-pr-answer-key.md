# Sample PR Instructor Answer Key

이 문서는 강사용이다. 수업 전에 학생에게 먼저 공유하지 않는다.

## PR 1: Good PR

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/6
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/8
- Branch: `training/good-pr-small-checklist-entry`
- Operational decision: Merge in content judgment.
- GitHub action: No real merge in class because this is a Draft training PR.
- Why: 변경 파일이 `README.md`, `index.html`로 제한되고 checklist entry point 추가라는 issue 요구와 diff가 일치하며 checks가 통과한다.
- Common wrong answer: Draft PR이므로 무조건 판단 보류라고 말한다.
- Instructor prompt: "이 PR에서 merge 가능하다는 근거를 Files changed, Diff, Checks 중 어디서 찾을 수 있나요?"
- Correction sentence: "Draft는 수업 안전장치이고, 판단 근거는 파일 범위, diff 일치, checks 결과에서 찾아야 합니다."
- Example comment: "README.md와 index.html만 변경되었고 checklist entry point 요구와 diff가 일치하며 checks가 통과했습니다. 내용상 merge 가능한 PR로 판단합니다."

## PR 2: Problem A

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/7
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/9
- Branch: `training/problem-a-overbroad-agent-change`
- Operational decision: Hold
- GitHub action: Do not approve. Leave a blocking comment asking the agent to split or reduce the PR.
- Why: 작은 copy 변경 요청에 전체 CSS 교체, README roadmap 추가, unrelated notes file 생성이 섞여 있다.
- Common wrong answer: CI가 초록색이므로 merge해도 된다고 판단한다.
- Instructor prompt: "이 PR이 CI를 통과해도 merge하면 안 되는 이유는 무엇인가요?"
- Correction sentence: "CI는 자동 검사일 뿐이고, Files changed와 diff가 Issue 범위를 벗어나면 hold해야 합니다."
- Example comment: "Files changed에서 styles.css, README roadmap, unrelated notes file 변경을 확인했습니다. 이번 Issue는 작은 copy 변경이므로 요청 밖 변경을 제외하거나 별도 PR로 나눠 주세요."

## PR 3: Problem B

- Issue: https://github.com/lucky206208-glitch/ai-agent-workshop/issues/5
- PR: https://github.com/lucky206208-glitch/ai-agent-workshop/pull/10
- Branch: `training/problem-b-ci-secret-fixture`
- Operational decision: Hold
- GitHub action: Request changes. Do not copy the marker value into comments.
- Why: `.env`와 secret-like 문자열이 포함되고, required marker 삭제로 CI가 실패한다.
- Common wrong answer: `.env` 파일 삭제만 요청하면 충분하다고 판단한다.
- Instructor prompt: "이 경우 단순히 파일 삭제 요청만 하면 충분할까요? history 노출과 키 회전은 어떻게 판단해야 할까요?"
- Correction sentence: "CI를 복구하고, marker 제거와 history 노출 확인을 요청하되, 값 자체를 comment에 다시 쓰지 않습니다."
- Example comment: "Files changed에서 .env 변경을 확인했고 Checks가 실패했습니다. secret-like 값은 comment에 복사하지 않고, 파일 제거, history 노출 확인, CI 복구를 요청합니다."

## High-Risk Rule

Secret-like 변경은 일반 품질 문제가 아니라 보안 사고 가능성으로 취급한다. 실제 키일 수 있으면 merge 금지, 값 재공유 금지, 키 회전 또는 폐기, history 노출 확인을 요구한다.

Hold는 GitHub 버튼이 아니다. Hold는 approve하지 않고 위험 근거를 남기는 운영 판단이다.
