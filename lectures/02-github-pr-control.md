# 2회차 강사용 수업안: GitHub PR로 AI Agent 작업 통제하기

## 수업 목표

수강생은 Git 명령어를 외우지 않고도 AI agent가 만든 PR을 검토하고 merge 여부를 판단할 수 있어야 한다.

## 2시간 시간표

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

## 강의 핵심 문장

Agent가 코드를 바꾸는 속도보다 사람이 변경을 검증하는 기준이 더 중요하다.

## 추천 슬라이드 구조

이번 덱은 용어를 먼저 길게 설명하지 않고, 학생이 실제 GitHub 화면에서 따라 할 순서대로 구성한다.

| 슬라이드 | 역할 | 핵심 메시지 |
|---:|---|---|
| 1 | 표지 | PR은 agent 작업의 안전장치다 |
| 2 | 문제 제기 | 속도보다 검증 기준이 중요하다 |
| 3 | 수업 지도 | 2시간 안에 세 개 PR을 직접 판정한다 |
| 4 | Mental model | issue는 요청, PR은 검문소, main은 결과선이다 |
| 5 | Review protocol | PR은 Files changed -> Diff -> Checks -> Decision 네 단계로 읽는다 |
| 6 | 강사 데모 | issue에서 PR 판단까지 실제 클릭 순서를 보여준다 |
| 7 | 좋은 PR | 작은 요청, 작은 diff, CI 통과가 merge 근거다 |
| 8 | 문제 PR A | 작은 요청에 큰 변경이 섞이면 PR을 나누게 한다 |
| 9 | 문제 PR B | CI 실패와 secret-like 변경은 merge 중단 신호다 |
| 10 | 판단표 | Merge, Request changes, Hold를 기준으로 구분한다 |
| 11 | Comment 작성 | 실패 로그와 diff 위치를 넣어 수정 요청한다 |
| 12 | Exit ticket | 판단, 근거 2개, agent comment를 제출한다 |

## 최소 개념 설명

- `Issue`: 작업 요청서다. 수업에서는 PR 본문에 연결된 Issue를 먼저 열고 요구사항을 한 문장으로 줄인다.
- `commit`: 저장된 변경 스냅샷이다.
- `branch`: main과 분리된 작업 줄기다.
- `PR`: 이 변경을 main에 합쳐도 되는지 검토하는 제안서다.
- `Files changed`: PR에서 어떤 파일이 바뀌었는지 보는 탭이다.
- `Diff`: 파일 안에서 추가된 줄과 삭제된 줄이다.
- `Checks`: 자동 검사의 결과다.
- `merge`: 검토가 끝난 변경을 main에 합치는 행동이다.
- `CI`: 사람이 놓칠 수 있는 기계적 검사를 자동으로 돌리는 장치다.
- `CD`: merge 뒤 배포를 자동화하는 장치다. CI는 깊게, CD는 짧게 설명한다.

## 강사 데모 스크립트

1. GitHub issue를 열고 요구사항을 한 문장으로 줄인다.
2. 수업 전에 만들어 둔 Training Draft PR을 연다.
3. PR description을 읽되 결론을 바로 믿지 않는다.
4. `Files changed` 탭에서 변경 파일 수와 파일명을 먼저 확인한다.
5. diff가 issue 요구와 같은지 확인한다.
6. `Checks`에서 CI 상태와 실패 로그를 확인한다.
7. merge, request changes, hold 중 하나를 선택하고 근거를 말한다.
8. request changes 또는 hold라면 agent에게 남길 comment를 작성한다.

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
- 값을 comment나 채팅에 복사하지 않는다.
- 실제 키일 수 있으면 키 회전 또는 폐기와 history 노출 확인을 요청한다.
- GitHub에서는 request changes comment를 남기되, 운영 판단은 hold로 둔다.

## Merge 판단표

| 운영 판단 | GitHub에서 할 행동 | 수업 중 사용하는 문장 |
|---|---|---|
| Merge | Merge | 요청과 diff가 일치하고 checks가 통과했으므로 merge합니다 |
| Request changes | Review comment | 방향은 맞지만 수정할 점이 있어 comment를 남깁니다 |
| Hold | Approve하지 않음 | 변경 범위나 위험이 커서 이 PR은 보류합니다 |

## Secret-like 변경 대응 규칙

- 실제 secret 가능성이 있으면 merge하지 않는다.
- PR comment, Slack, 강의 채팅에 값을 복사하지 않는다.
- 파일 삭제만으로 끝내지 않는다. 이미 Git history에 노출됐는지 확인해야 한다.
- 실제 키라면 키 회전 또는 폐기를 요청한다.
- 수업에서는 secret-like 문자열을 예시로만 쓰고, 실제 키를 만들거나 공유하지 않는다.

## Worktree 운영 사례

기존 방식에서는 한 폴더에서 여러 agent 작업을 번갈아 보며 `git diff`, `git stash`, branch 전환으로 상태를 관리했다. 이 방식은 변경이 섞였는지 판단하기 어렵고, agent가 만든 diff를 사람이 검토하기 전부터 작업공간이 지저분해질 수 있다.

`git worktree` 방식은 agent마다 별도 폴더와 branch를 준다. 각 agent의 결과가 독립된 PR로 올라오므로, 사람은 로컬 명령어를 외우기보다 PR에서 Files changed, Diff, Checks를 읽고 판단하면 된다.

이 수업에서는 worktree 명령어를 실습하지 않는다. worktree는 AI agent 운영 개념으로만 다룬다.

## 예상 질문과 답변

### Git을 몰라도 PR을 볼 수 있나요?

볼 수 있다. 이 수업의 목표는 Git 내부 구조가 아니라 PR 검토 화면에서 위험 신호를 찾는 것이다.

### CI가 초록색이면 무조건 merge해도 되나요?

아니다. CI는 자동 검사일 뿐이다. PR 설명과 diff가 맞는지 사람의 검토가 필요하다.

### Agent가 만든 설명을 믿어도 되나요?

설명은 출발점일 뿐이다. 항상 `Files changed`와 diff를 기준으로 확인한다.

## 과제

수강생은 세 개의 Training Draft PR 중 하나를 골라 exit ticket 형식으로 판단을 제출한다.

```text
선택한 PR:
판단: Merge / Request changes / Hold
근거 1:
근거 2:
agent에게 남길 comment:
```

## 강사용 체크리스트

- 수업 전 Training Draft PR 3개가 열리는지 확인한다.
- 좋은 PR의 CI가 통과했는지 확인한다.
- 문제 PR B의 CI가 실패하는지 확인한다.
- 학생용 `docs/sample-pr-scenarios.md`에는 정답이 없고, 강사용 `docs/sample-pr-answer-key.md`에만 정답이 있는지 확인한다.
- 학생에게 정답을 먼저 말하지 않는다.
- 모든 판단에는 `Files changed`, `Diff`, `Checks` 중 하나 이상의 근거를 요구한다.

## Design Reference

Design reference: corazzon/pptx-design-styles (MIT)
