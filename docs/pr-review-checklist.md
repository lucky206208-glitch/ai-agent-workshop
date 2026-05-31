# PR Review Checklist

## 1. 요청과 PR 설명이 같은가

- Issue가 요구한 작업을 한 문장으로 다시 말한다.
- PR description이 그 요구를 그대로 해결하는지 확인한다.
- 설명에 없는 큰 변경이 있으면 merge하지 않는다.

## 2. Files changed를 먼저 본다

- 변경 파일 수가 요청 규모와 맞는지 본다.
- 관련 없는 파일, 설정 파일, secret 파일, 테스트 삭제가 있는지 본다.
- 이해할 수 없는 파일이 있으면 agent에게 이유를 묻는다.
- secret처럼 보이는 문자열이 있으면 값을 복사하지 않고 즉시 merge를 보류한다.

## 3. Diff를 읽는다

- 새 코드나 문구가 요구사항과 일치하는지 본다.
- 삭제된 내용이 필요한 기능인지 확인한다.
- 큰 diff는 작은 PR로 나누라고 요청한다.

## 4. Checks를 확인한다

- CI가 실패하면 merge하지 않는다.
- 실패 로그에서 원인을 한 줄로 요약한다.
- agent에게 실패 로그를 붙여서 수정 요청한다.

## 5. 결정한다

| 운영 판단 | 기준 | GitHub에서 할 행동 |
|---|---|---|
| Merge | 요청과 diff가 일치하고 checks가 통과했다 | merge한다 |
| Request changes | 방향은 맞지만 수정할 점이 명확하다 | review comment로 수정 요청한다 |
| Hold | 범위가 크거나 위험한 변경이 있다 | approve하지 않고 blocking comment를 남긴다 |

## 6. Secret-like 변경 고위험 규칙

- 실제 secret 가능성이 있으면 merge하지 않는다.
- PR comment, Slack, 강의 채팅에 값을 복사하지 않는다.
- 파일 삭제만으로 끝내지 않는다. 이미 Git history에 노출됐는지 확인해야 한다.
- 실제 키라면 키 회전 또는 폐기를 요청한다.
- 수업에서는 secret-like 문자열을 예시로만 쓰고, 실제 키를 만들거나 공유하지 않는다.
