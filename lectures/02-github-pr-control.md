# 2회차 강사용 수업안: GitHub PR로 AI Agent 작업 통제하기

## 수업 목표

수강생은 Git 명령어를 외우지 않고도 AI agent가 만든 PR을 검토하고 merge 여부를 판단할 수 있어야 한다.

## 2시간 시간표

| 시간 | 구간 | 목표 |
|---:|---|---|
| 0-15분 | Mental model | GitHub는 agent 작업의 검문소라는 관점을 만든다 |
| 15-30분 | 최소 개념 | commit, branch, PR, merge, CI를 한 문장으로 설명한다 |
| 30-50분 | 강사 데모 | 사전 생성된 PR로 issue에서 PR 검토까지 흐름을 보여준다 |
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
3. 수업 전에 만들어 둔 sample PR을 연다.
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
- 학생용 `docs/sample-pr-scenarios.md`에는 정답이 없고, 강사용 `docs/sample-pr-answer-key.md`에만 정답이 있는지 확인한다.
- 학생에게 정답을 먼저 말하지 않는다.
- 모든 판단에는 `Files changed`, `Diff`, `Checks` 중 하나 이상의 근거를 요구한다.

## Design Reference

Design reference: corazzon/pptx-design-styles (MIT)
