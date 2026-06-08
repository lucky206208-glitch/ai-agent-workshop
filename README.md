# AI Agent Workshop

AI agent가 만든 변경사항을 GitHub PR로 검증하는 실습 repo입니다.

Project teaching language and scope boundaries are documented in `CONTEXT.md`.

## Lecture 02: GitHub PR Control

수강생은 이 repo에서 세 가지 PR을 비교합니다.

1. 좋은 PR: 요구사항이 작고 변경 범위가 명확합니다.
2. 문제 PR A: 작은 요청인데 agent가 관련 없는 파일까지 크게 바꿉니다.
3. 문제 PR B: CI가 실패하고 secret-like 문자열이 포함됩니다.

## Student Goal

Git 명령어를 외우는 것이 목표가 아닙니다. PR에서 `Files changed`, `Checks`, `Conversation`을 읽고 `merge`, `request changes`, `hold` 중 하나를 근거와 함께 선택하는 것이 목표입니다.

## Design Reference

External decks use: `Design reference: corazzon/pptx-design-styles (MIT)`.

## Future Roadmap

This roadmap is intentionally unrelated to the tiny heading request.
Students should treat this as scope creep.
