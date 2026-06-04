from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "decks" / "02-github-pr-control-bento-swiss.pptx"
ASSETS = ROOT / "decks" / "assets" / "lecture-02"
EMU_PER_INCH = 914400
MIN_LABEL_X = int(0.70 * EMU_PER_INCH)
MAX_TOP_LABEL_Y = int(0.75 * EMU_PER_INCH)
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
}


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml", name)
    if not match:
        raise ValueError(f"Unexpected slide path: {name}")
    return int(match.group(1))


def shape_text(shape: ET.Element) -> str:
    return "".join(node.text or "" for node in shape.findall(".//a:t", NS)).strip()


def shape_offset(shape: ET.Element) -> tuple[int, int] | None:
    xfrm = shape.find(".//a:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", NS)
    if off is None:
        return None
    return int(off.get("x", "0")), int(off.get("y", "0"))


def verify_assets(failures: list[str]) -> None:
    required = [
        "good-pr-overview.png",
        "good-pr-files-changed.png",
        "problem-a-files-changed.png",
        "problem-a-checks.png",
        "problem-b-files-changed.png",
        "problem-b-checks-failed.png",
    ]
    for name in required:
        path = ASSETS / name
        if not path.exists():
            failures.append(f"Missing deck asset: {name}")
        elif path.stat().st_size < 10_000:
            failures.append(f"Deck asset looks too small: {name}")


def main() -> int:
    failures: list[str] = []
    if not PPTX.exists() or PPTX.stat().st_size < 50_000:
        failures.append(f"PPTX missing or too small: {PPTX}")
        print_failures(failures)
        return 1

    verify_assets(failures)
    with zipfile.ZipFile(PPTX) as zf:
        slides = sorted(
            [name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")],
            key=slide_number,
        )
        if len(slides) < 22:
            failures.append(f"Expected at least 22 slides, found {len(slides)}")

        all_text: list[str] = []
        for name in slides:
            root = ET.fromstring(zf.read(name))
            number = slide_number(name)
            for shape in root.findall(".//p:sp", NS):
                text = shape_text(shape)
                if text:
                    all_text.append(text)
                offset = shape_offset(shape)
                if not text or offset is None:
                    continue
                x, y = offset
                is_kicker = y < MAX_TOP_LABEL_Y and text == text.upper() and any(ch.isalpha() for ch in text)
                if is_kicker and x < MIN_LABEL_X:
                    failures.append(f"Slide {number}: top label '{text}' starts too far left at {x}")

        joined = "\n".join(all_text)
        for required in ["Files changed", "Diff", "Checks", "Draft", "Hold", "Worktree", "CI", "CD", "Codex", "Claude Code", "Antigravity", "git worktree add"]:
            if required not in joined:
                failures.append(f"Deck missing required term: {required}")

        media = [name for name in zf.namelist() if name.startswith("ppt/media/")]
        if len(media) < 6:
            failures.append(f"Expected at least 6 embedded media files, found {len(media)}")
        for name in media:
            if len(zf.read(name)) == 0:
                failures.append(f"Empty embedded media file: {name}")

    if failures:
        print_failures(failures)
        return 1
    print("PPTX verification passed.")
    return 0


def print_failures(failures: list[str]) -> None:
    print("PPTX verification failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
