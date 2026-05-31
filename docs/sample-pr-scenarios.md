# Sample PR Scenarios

## PR 1: Good PR

- Branch: `sample/good-pr-checklist-copy`
- Title: `docs: add PR review checklist link`
- Issue request: 수강생이 checklist를 쉽게 찾을 수 있도록 README와 화면에 entry point를 추가한다.
- Normal changed files: `README.md`, `index.html`
- Checks state: passing
- Student clues: 변경 파일이 요청 범위 안에 있고, 새 링크와 새 카드가 같은 목적을 가진다.
- Teaching point: 요청, 변경 파일, diff, checks가 모두 일치하면 merge할 수 있다.

## PR 2: Problem A

- Branch: `sample/problem-overbroad-agent-change`
- Title: `style: over-expand small copy request`
- Issue request: 제목 문구만 더 짧게 바꾼다.
- Normal changed files: `index.html`
- Actual changed files: `index.html`, `styles.css`, `README.md`, `docs/agent-extra-notes.md`
- Checks state: passing
- Student clues: 작은 문구 수정인데 전체 visual system과 unrelated docs가 함께 바뀐다.
- Teaching point: 작은 문구 수정 요청인데 unrelated files와 큰 스타일 변경이 섞이면 merge하지 않는다.

## PR 3: Problem B

- Branch: `sample/problem-failing-ci-secret-like-file`
- Title: `chore: add local demo env file`
- Issue request: 로컬 데모 실행에 필요한 안내를 추가한다.
- Normal changed files: `README.md` 또는 문서 파일 1개
- Actual changed files: `.env`, `index.html`
- Checks state: failing
- Student clues: `.env` 파일과 secret-like 문자열이 있고, 필수 HTML marker가 삭제되어 CI가 실패한다.
- Teaching point: CI 실패와 secret-like 문자열은 운영상 Hold 판단을 내리고, GitHub에서는 request changes comment를 남겨야 한다.

## Instructor Rule

수업 중에는 정답을 먼저 말하지 않는다. 수강생이 `Files changed`, `Diff`, `Checks` 근거를 하나 이상 말한 뒤 판단을 공개한다.

강사용 정답과 해설은 `docs/sample-pr-answer-key.md`에만 둔다.
