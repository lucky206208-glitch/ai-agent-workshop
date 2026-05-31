from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "decks" / "02-github-pr-control-bento-swiss.pptx"
LINKS = ROOT / "docs" / "training-pr-links.json"
ASSETS = ROOT / "decks" / "assets" / "lecture-02"

FONT_KO = "Malgun Gothic"
FONT_MONO = "Consolas"

INK = RGBColor(17, 17, 17)
MUTED = RGBColor(68, 68, 68)
PAPER = RGBColor(248, 248, 242)
ACCENT = RGBColor(232, 0, 13)
NAVY = RGBColor(26, 26, 46)
TEAL = RGBColor(78, 205, 196)
YELLOW = RGBColor(232, 255, 59)
CORAL = RGBColor(255, 107, 107)
WHITE = RGBColor(255, 255, 255)
LINE = RGBColor(221, 221, 221)
GREEN = RGBColor(31, 136, 61)
RED = RGBColor(207, 34, 46)


def inches(value: float):
    return Inches(value)


def set_fill(slide, color=PAPER) -> None:
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = color


def add_text(
    slide,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    size: int = 24,
    bold: bool = False,
    color=INK,
    font: str = FONT_KO,
    align=None,
    valign=None,
    name: str | None = None,
):
    box = slide.shapes.add_textbox(inches(x), inches(y), inches(w), inches(h))
    if name:
        box.name = name
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = inches(0.03)
    frame.margin_right = inches(0.03)
    frame.margin_top = inches(0.02)
    frame.margin_bottom = inches(0.02)
    if valign:
        frame.vertical_anchor = valign
    p = frame.paragraphs[0]
    if align:
        p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_link_text(slide, text: str, url: str, x: float, y: float, w: float, h: float):
    box = slide.shapes.add_textbox(inches(x), inches(y), inches(w), inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    p = frame.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.name = FONT_MONO
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(9, 105, 218)
    run.hyperlink.address = url
    return box


def add_rule(slide, x: float, y: float, w: float, h: float = 0.025, color=ACCENT):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, inches(x), inches(y), inches(w), inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = color
    return shape


def add_section_label(slide, label: str) -> None:
    marker = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, inches(0.48), inches(0.38), inches(0.14), inches(0.14))
    marker.name = "kicker-marker"
    marker.fill.solid()
    marker.fill.fore_color.rgb = ACCENT
    marker.line.color.rgb = ACCENT
    add_text(
        slide,
        label,
        0.74,
        0.31,
        4.6,
        0.28,
        size=10,
        bold=True,
        color=ACCENT,
        font=FONT_MONO,
        valign=MSO_ANCHOR.MIDDLE,
        name="kicker-label",
    )
    add_rule(slide, 0.48, 0.9, 2.85)


def add_footer(slide, number: int) -> None:
    add_text(
        slide,
        f"{number:02d} / Design reference: corazzon/pptx-design-styles (MIT)",
        9.45,
        7.1,
        3.25,
        0.18,
        size=7,
        color=RGBColor(115, 115, 115),
        font=FONT_MONO,
        align=PP_ALIGN.RIGHT,
    )


def add_title(slide, label: str, title: str, subtitle: str, number: int) -> None:
    add_section_label(slide, label)
    add_text(slide, title, 0.72, 1.1, 9.85, 1.16, size=29, bold=True)
    add_text(slide, subtitle, 0.72, 2.38, 8.95, 0.58, size=15, color=MUTED)
    add_footer(slide, number)


def add_card(slide, x: float, y: float, w: float, h: float, title: str, body: str, *, fill=WHITE, dark=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, inches(x), inches(y), inches(w), inches(h))
    shape.adjustments[0] = 0.08
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = LINE if not dark else fill
    title_color = WHITE if dark else INK
    body_color = RGBColor(230, 230, 230) if dark else MUTED
    add_text(slide, title, x + 0.18, y + 0.16, w - 0.36, 0.34, size=14, bold=True, color=title_color)
    add_text(slide, body, x + 0.18, y + 0.62, w - 0.36, h - 0.76, size=10, color=body_color)
    return shape


def add_status_chip(slide, x: float, y: float, label: str, color, text_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, inches(x), inches(y), inches(1.2), inches(0.33))
    shape.adjustments[0] = 0.5
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = color
    add_text(slide, label, x + 0.04, y + 0.06, 1.1, 0.16, size=9, bold=True, color=text_color, align=PP_ALIGN.CENTER)


def add_asset(slide, filename: str, x: float = 5.55, y: float = 2.76, w: float = 7.15, h: float = 4.02) -> None:
    path = ASSETS / filename
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, inches(x), inches(y), inches(w), inches(h))
    frame.fill.solid()
    frame.fill.fore_color.rgb = WHITE
    frame.line.color.rgb = LINE
    if not path.exists():
        add_card(slide, x + 0.2, y + 0.2, w - 0.4, h - 0.4, "Screenshot needed", filename)
        return
    with Image.open(path) as img:
        img_w, img_h = img.size
    ratio = min(w / img_w, h / img_h)
    pic_w = img_w * ratio
    pic_h = img_h * ratio
    pic_x = x + (w - pic_w) / 2
    pic_y = y + (h - pic_h) / 2
    slide.shapes.add_picture(str(path), inches(pic_x), inches(pic_y), width=inches(pic_w), height=inches(pic_h))


def add_three_step_flow(slide, y: float, items: list[tuple[str, str, object]]) -> None:
    x = 0.72
    for idx, (title, body, fill) in enumerate(items):
        add_card(slide, x + idx * 4.1, y, 3.55, 1.28, title, body, fill=fill, dark=fill == NAVY)
        if idx < len(items) - 1:
            add_text(slide, "->", x + idx * 4.1 + 3.68, y + 0.42, 0.32, 0.24, size=16, bold=True, color=ACCENT, font=FONT_MONO)


def add_bullet_stack(slide, x: float, y: float, bullets: list[str], color=INK):
    for idx, bullet in enumerate(bullets):
        add_rule(slide, x, y + idx * 0.47 + 0.09, 0.12, 0.12, ACCENT)
        add_text(slide, bullet, x + 0.24, y + idx * 0.47, 5.4, 0.32, size=12, color=color)


def create_deck() -> None:
    prs = Presentation()
    prs.slide_width = inches(13.333)
    prs.slide_height = inches(7.5)
    blank = prs.slide_layouts[6]
    links = json.loads(LINKS.read_text(encoding="utf-8"))
    scenarios = {item["id"]: item for item in links["scenarios"]}

    slide_no = 1

    slide = prs.slides.add_slide(blank)
    set_fill(slide)
    add_section_label(slide, "LECTURE 02 / GITHUB PR CONTROL")
    add_text(slide, "AI agent PR을\nmerge해도 되는지 판단하기", 0.72, 1.25, 7.2, 1.55, size=36, bold=True)
    add_text(slide, "Git 명령어 암기가 아니라 PR 화면에서 근거를 찾는 수업입니다.", 0.76, 2.95, 7.4, 0.42, size=16, color=MUTED)
    add_card(slide, 0.72, 4.08, 3.4, 1.35, "핵심 질문", "이 변경을 main에 합쳐도 되는가?", fill=YELLOW)
    add_card(slide, 4.38, 3.72, 3.0, 1.72, "읽는 순서", "Files changed -> Diff -> Checks", fill=TEAL)
    add_card(slide, 7.68, 4.08, 3.35, 1.35, "결정", "Merge / Request changes / Hold", fill=NAVY, dark=True)
    add_rule(slide, 11.55, 1.15, 0.25, 4.6)
    add_footer(slide, slide_no)
    slide_no += 1

    specs = [
        {
            "label": "PROBLEM",
            "title": "속도보다 merge 판단 기준이 중요하다",
            "subtitle": "Agent는 빠르게 바꿉니다. 사람은 근거로 멈추거나 합쳐야 합니다.",
            "cards": [
                ("빠른 생성", "AI agent는 한 번에 여러 파일을 바꿀 수 있다.", YELLOW, False),
                ("느린 판단", "사람은 PR에서 위험 신호를 확인해야 한다.", TEAL, False),
                ("실패 비용", "잘못 merge하면 main과 배포 흐름이 오염된다.", NAVY, True),
            ],
        },
        {
            "label": "MAP",
            "title": "오늘은 세 개 Draft PR을 판정한다",
            "subtitle": "Draft는 수업 안전장치입니다. 판단 연습은 PR 내용과 Checks를 기준으로 합니다.",
            "cards": [
                ("Good PR", "작은 요청, 작은 diff, checks 통과", YELLOW, False),
                ("Problem A", "checks는 통과하지만 scope creep", TEAL, False),
                ("Problem B", "checks 실패와 training secret marker", CORAL, False),
            ],
        },
        {
            "label": "GLOSSARY",
            "title": "GitHub 용어는 PR 판단에 필요한 만큼만 배운다",
            "subtitle": "Issue, Branch, PR, Files changed, Diff, Checks, CI/CD를 화면 위치와 함께 익힙니다.",
            "bullets": [
                "Issue: 작업 요청서",
                "Branch: main과 분리된 작업 줄기",
                "PR: main에 합쳐도 되는지 검토하는 제안",
                "Files changed / Diff: 변경 파일과 줄 단위 변경",
                "Checks / CI: merge 전 자동 검사",
                "CD: merge 뒤 자동 배포, 이번 수업에서는 짧게",
            ],
        },
        {
            "label": "FLOW",
            "title": "Issue -> Branch -> PR -> Checks -> Decision",
            "subtitle": "Issue는 요청, PR은 검문소, Checks는 자동 검사, Decision은 사람의 판단입니다.",
            "flow": [
                ("Issue", "요구사항을 한 문장으로 줄인다.", YELLOW),
                ("PR", "Files changed와 Diff로 실제 변경을 본다.", TEAL),
                ("Decision", "Checks까지 보고 merge 여부를 결정한다.", NAVY),
            ],
        },
        {
            "label": "PROTOCOL",
            "title": "PR은 네 단계로 읽는다",
            "subtitle": "Files changed에서 범위를 보고, Diff에서 내용을 보고, Checks에서 자동 검사를 본 뒤 결정합니다.",
            "flow": [
                ("1 Files changed", "요청 범위와 파일 목록이 맞는가?", YELLOW),
                ("2 Diff", "agent 설명과 실제 변경이 같은가?", WHITE),
                ("3 Checks", "CI가 통과했는가?", TEAL),
            ],
        },
        {
            "label": "DEMO",
            "title": "강사 데모는 Good PR 하나로 진행한다",
            "subtitle": scenarios["good-pr"]["pr_url"],
            "asset": "good-pr-overview.png",
            "bullets": ["Issue 링크 확인", "Draft는 안전장치", "탭 순서: Conversation -> Files changed -> Checks"],
        },
        {
            "label": "GOOD PR",
            "title": "작은 요청, 작은 diff, 통과한 checks",
            "subtitle": "내용상 Merge 판단입니다. 실제 수업 PR은 Draft라서 merge하지 않습니다.",
            "asset": "good-pr-files-changed.png",
            "chips": [("2 files", GREEN), ("Checks pass", GREEN)],
        },
        {
            "label": "PROBLEM A",
            "title": "CI가 통과해도 scope creep이면 Hold",
            "subtitle": "작은 copy 요청에 styles.css, README, unrelated docs가 섞이면 위험 신호입니다.",
            "asset": "problem-a-files-changed.png",
            "chips": [("4 files", RED), ("Scope creep", RED)],
        },
        {
            "label": "PROBLEM A",
            "title": "Problem A의 Checks는 초록색이어도 충분하지 않다",
            "subtitle": "CI는 자동 검사일 뿐이고 변경 범위 판단은 사람이 합니다.",
            "asset": "problem-a-checks.png",
            "chips": [("Checks pass", GREEN), ("Still Hold", RED)],
        },
        {
            "label": "PROBLEM B",
            "title": "CI 실패와 training secret marker는 Hold",
            "subtitle": ".env와 TRAINING_SECRET_DO_NOT_USE를 보고 값을 복사하지 않습니다.",
            "asset": "problem-b-files-changed.png",
            "chips": [(".env", RED), ("Do not copy value", RED)],
        },
        {
            "label": "PROBLEM B",
            "title": "Problem B의 Checks 실패는 merge 중단 신호다",
            "subtitle": "실패 로그와 위험 파일을 근거로 request changes 문장을 작성합니다.",
            "asset": "problem-b-checks-failed.png",
            "chips": [("Checks fail", RED), ("Request changes", RED)],
        },
        {
            "label": "CI/CD",
            "title": "CI는 깊게, CD는 짧게",
            "subtitle": "CI는 merge 전 자동 검사입니다. CD는 merge 이후 자동 배포이며 이번 수업에서는 용어만 설명합니다.",
            "cards": [
                ("CI", "PR마다 자동 검사: marker, secret-like 문자열, page title", YELLOW, False),
                ("Checks", "GitHub PR 화면에서 성공/실패를 확인한다.", TEAL, False),
                ("CD", "merge 뒤 배포 자동화. 이번 수업의 실습 범위 밖.", WHITE, False),
            ],
        },
        {
            "label": "DECISION",
            "title": "Hold는 GitHub 버튼이 아니다",
            "subtitle": "Hold는 approve하지 않는 운영 판단입니다. 근거를 남기고 수정 요청 또는 blocking comment를 씁니다.",
            "cards": [
                ("Merge", "요청과 diff가 일치하고 checks가 통과한다.", TEAL, False),
                ("Request changes", "방향은 맞지만 수정 지점이 명확하다.", YELLOW, False),
                ("Hold", "범위 또는 보안 위험이 커서 approve하지 않는다.", NAVY, True),
            ],
        },
        {
            "label": "COMMENT",
            "title": "좋은 agent comment는 위치, 근거, 요청을 담는다",
            "subtitle": "Checks 실패 로그와 Diff 위치를 말하고, 무엇을 되돌릴지 명확히 요청합니다.",
            "bullets": [
                "위치: Files changed의 파일명 또는 Checks 단계",
                "근거: Issue 범위, diff, 실패 로그 중 하나",
                "요청: 삭제, 분리, CI 복구처럼 행동으로 끝나는 문장",
                "주의: secret-like 값은 comment에 복사하지 않는다",
            ],
        },
        {
            "label": "WORKTREE",
            "title": "AI agent별 작업공간을 분리하면 PR 검토가 쉬워진다",
            "subtitle": "기존 diff/stash 중심 방식보다 worktree + branch + PR 방식이 변경 범위를 분리합니다.",
            "cards": [
                ("기존 방식", "한 폴더에서 diff/stash/branch 전환으로 agent 결과를 관리", WHITE, False),
                ("문제", "변경이 섞였는지 판단하기 어렵고 workspace가 지저분해짐", CORAL, False),
                ("worktree 방식", "agent마다 별도 폴더와 branch를 주고 PR 단위로 검토", TEAL, False),
            ],
        },
        {
            "label": "WORKTREE",
            "title": "이 수업은 worktree 명령어 실습이 아니다",
            "subtitle": "Worktree는 운영 개념입니다. 학생은 PR 화면에서 판단 근거를 찾는 데 집중합니다.",
            "flow": [
                ("Agent A", "worktree A -> branch A -> PR A", YELLOW),
                ("Agent B", "worktree B -> branch B -> PR B", TEAL),
                ("Human", "PR별 Files changed / Diff / Checks 판정", NAVY),
            ],
        },
        {
            "label": "PRACTICE",
            "title": "개인 실습: Good PR",
            "subtitle": scenarios["good-pr"]["pr_url"],
            "bullets": ["변경 파일 수를 말한다", "diff가 Issue와 일치하는지 말한다", "Checks 상태를 말한다", "내용상 Merge인지 판단한다"],
        },
        {
            "label": "PRACTICE",
            "title": "페어 실습: Problem A와 Problem B",
            "subtitle": "통과한 checks와 실패한 checks가 각각 어떤 판단 근거가 되는지 비교합니다.",
            "links": [scenarios["problem-a"]["pr_url"], scenarios["problem-b"]["pr_url"]],
            "bullets": ["Problem A: CI 통과와 scope creep을 분리해 판단", "Problem B: CI 실패와 training marker를 근거로 판단"],
        },
        {
            "label": "EXIT",
            "title": "Exit ticket",
            "subtitle": "선택한 PR, 판단, 근거 2개, agent에게 남길 comment를 제출합니다.",
            "cards": [
                ("판단", "Merge / Request changes / Hold 중 하나", YELLOW, False),
                ("근거", "Files changed, Diff, Checks 중 2개 이상", TEAL, False),
                ("comment", "위치 + 근거 + 요청이 모두 보이게 작성", WHITE, False),
            ],
        },
    ]

    for spec in specs:
        slide = prs.slides.add_slide(blank)
        set_fill(slide)
        add_title(slide, spec["label"], spec["title"], spec["subtitle"], slide_no)
        if "cards" in spec:
            for idx, (title, body, fill, dark) in enumerate(spec["cards"]):
                add_card(slide, 0.72 + idx * 4.1, 3.25, 3.55, 1.55, title, body, fill=fill, dark=dark)
        if "flow" in spec:
            add_three_step_flow(slide, 3.35, spec["flow"])
        if "bullets" in spec:
            add_bullet_stack(slide, 0.82, 3.15, spec["bullets"])
        if "links" in spec:
            for idx, url in enumerate(spec["links"]):
                add_link_text(slide, url, url, 0.82, 5.32 + idx * 0.38, 6.4, 0.28)
        if "chips" in spec:
            for idx, (label, color) in enumerate(spec["chips"]):
                add_status_chip(slide, 0.82 + idx * 1.42, 3.05, label, color)
        if "asset" in spec:
            add_asset(slide, spec["asset"])
        slide_no += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)


if __name__ == "__main__":
    create_deck()
