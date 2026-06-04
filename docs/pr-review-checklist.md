# PR Review Checklist

## Beginner Glossary

| GitHub UI term | 한국어 의미 | 수업에서 보는 위치 | 판단 질문과 예시 |
|---|---|---|---|
| Issue | 요청서 또는 문제 설명 | PR 본문에 연결된 링크 | "요구가 무엇인가?"를 한 문장으로 줄인다. 예: README에 checklist 링크 추가 |
| Branch | main과 분리된 작업 줄기 | PR 상단의 compare 정보 | agent가 main을 바로 바꾸지 않고 따로 작업했는지 확인한다 |
| Pull Request / PR | main에 합쳐도 되는지 검토하는 제안 | PR 화면 전체 | PR description은 주장이다. 실제 증거는 Files changed, Diff, Checks에서 확인한다 |
| Files changed | 변경된 파일 목록 | PR의 Files changed 탭 | 파일 수와 종류가 Issue 범위와 맞는가? 작은 요청인데 CSS와 설정이 같이 바뀌면 위험 신호다 |
| Diff | 추가/삭제된 줄 | Files changed 안의 코드 영역 | 초록 줄과 빨간 줄이 요구사항을 해결하는가? 불필요한 삭제가 있는가? |
| Checks | 자동 검사 결과 | PR 하단 또는 Checks 영역 | 실패하면 merge하지 않는다. 성공해도 scope 판단은 사람이 따로 한다 |
| CI | merge 전 자동 검사 | Checks의 workflow 결과 | required marker, secret-like 문자열, page title 같은 규칙을 기계가 확인한다 |
| CD | merge 후 자동 배포 | 이번 수업에서는 용어만 짧게 설명 | CI와 구분만 한다. 이번 실습에서는 배포 설정이나 실행을 다루지 않는다 |
| Merge | PR을 main에 합침 | 수업에서는 실제로 누르지 않음 | 내용상 merge 가능해도 Draft training PR은 실제 merge하지 않는다 |
| Request changes | 수정 요청 리뷰 | 수업에서는 exit ticket 문장으로 작성 | 방향은 맞지만 고칠 점이 명확할 때 파일명과 요청을 함께 쓴다 |
| Hold | merge 보류 운영 판단 | GitHub 버튼이 아님 | 범위가 크거나 보안 위험이 있으면 approve하지 않고 blocking comment를 남긴다 |
| Worktree | branch별 분리 작업 폴더 | AI agent 운영 사례에서 설명 | Codex, Claude Code, Antigravity 모두 agent별 폴더와 branch를 분리하면 PR별로 Files changed, Diff, Checks를 따로 판단하기 쉽다 |

CI는 깊게, CD는 짧게 다룬다. 이번 수업의 핵심은 merge 전 자동 검사인 CI 결과를 PR 판단 근거로 읽는 것이고, CD는 merge 뒤 배포 자동화라는 개념만 짚는다.

## 1. 요청과 PR 설명이 같은가

- Issue가 요구한 작업을 한 문장으로 다시 말한다.
- 예: "README에 checklist 링크를 추가한다"처럼 파일과 결과가 보이면 좋은 요청이다.
- PR description이 그 요구를 그대로 해결하는지 확인한다.
- 설명에 없는 큰 변경이 있으면 merge하지 않는다.

## 2. Files changed를 먼저 본다

- 변경 파일 수가 요청 규모와 맞는지 본다.
- 예: 제목 한 줄 수정 요청인데 `styles.css`, 설정 파일, 새 문서가 함께 바뀌면 scope creep을 의심한다.
- 관련 없는 파일, 설정 파일, secret 파일, 테스트 삭제가 있는지 본다.
- 이해할 수 없는 파일이 있으면 agent에게 이유를 묻는다.
- secret처럼 보이는 문자열이 있으면 값을 복사하지 않고 즉시 merge를 보류한다.

## 3. Diff를 읽는다

- 새 코드나 문구가 요구사항과 일치하는지 본다.
- 삭제된 내용이 필요한 기능인지 확인한다.
- agent 설명이 "작은 copy 변경"이라고 해도 diff에서 레이아웃, 정책, 보안 파일 변경이 보이면 설명을 그대로 믿지 않는다.
- 큰 diff는 작은 PR로 나누라고 요청한다.

## 4. Checks를 확인한다

- CI가 실패하면 merge하지 않는다.
- 실패 로그에서 원인을 한 줄로 요약한다.
- 예: required marker 삭제, secret-like 문자열 감지, page title 검사 실패처럼 자동 검사 이름과 원인을 함께 적는다.
- agent에게 실패 로그를 붙여서 수정 요청한다.

## Training PR Safety Note

Draft는 수업 안전장치입니다. 이 수업에서는 Draft 배너 자체가 아니라 Files changed, Diff, Checks를 보고 내용상 판단을 연습합니다.

Hold는 GitHub 버튼이 아니다. Hold는 approve하지 않고, 위험 근거를 남기며, 필요한 경우 request changes 또는 blocking comment를 남기는 운영 판단입니다.

## 5. 결정한다

| 운영 판단 | 기준 | GitHub에서 할 행동 |
|---|---|---|
| Merge | 요청과 diff가 일치하고 checks가 통과했다 | 실제 PR이라면 merge한다. 수업 Draft PR은 누르지 않는다 |
| Request changes | 방향은 맞지만 수정할 점이 명확하다 | review comment로 파일명, 근거, 요청을 남긴다 |
| Hold | 범위가 크거나 위험한 변경이 있다 | approve하지 않고 blocking comment를 남긴다 |

Comment 문장 틀:

```text
[위치]에서 [근거]를 확인했습니다. [요청]해 주세요.
```

예:

```text
Files changed에서 styles.css 변경을 확인했습니다. 이번 Issue는 heading copy 변경이므로 styles.css 변경은 제외하거나 별도 PR로 나눠 주세요.
```

## 6. Secret-like 변경 고위험 규칙

- 실제 secret 가능성이 있으면 merge하지 않는다.
- PR comment, Slack, 강의 채팅에 값을 복사하지 않는다.
- 파일 삭제만으로 끝내지 않는다. 이미 Git history에 노출됐는지 확인해야 한다.
- 실제 키라면 키 회전 또는 폐기를 요청한다.
- 수업에서는 secret-like 문자열을 예시로만 쓰고, 실제 키를 만들거나 공유하지 않는다.

## 7. Agent별 worktree 생성 패턴

Worktree는 학생이 외울 Git 명령어가 아니라, agent 결과를 PR 단위로 분리하기 위한 운영 패턴이다. Codex, Claude Code, Antigravity 모두 같은 흐름을 쓸 수 있다.

```powershell
git fetch origin
git switch main
git pull --ff-only
git worktree add .worktrees/<tool>-<task> -b <tool>/<task> main
cd .worktrees/<tool>-<task>
```

예:

- Codex: `.worktrees/codex-pr-checklist`, branch `codex/pr-checklist`
- Claude Code: `.worktrees/claude-copy-fix`, branch `claude/copy-fix`
- Antigravity: `.worktrees/antigravity-ci-fix`, branch `antigravity/ci-fix`
