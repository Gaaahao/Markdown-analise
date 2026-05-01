from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MarkdownStats:
    """Aggregate statistics for a markdown document."""

    headings: int
    links: int
    images: int
    code_blocks: int
    words: int


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+", re.MULTILINE)
_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_FENCE_START_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_HTML_TAG_RE = re.compile(r"<[^>]+>")


def analyze_markdown(content: str) -> MarkdownStats:
    """Analyze markdown content and return common text statistics."""

    text_without_code, code_blocks = _strip_fenced_code_and_count(content)

    images = len(_IMAGE_RE.findall(text_without_code))
    links = len(_LINK_RE.findall(text_without_code))
    headings = len(_HEADING_RE.findall(text_without_code))

    text_without_markdown = _strip_markdown_markup(text_without_code)
    words = len([w for w in re.split(r"\s+", text_without_markdown.strip()) if w])

    return MarkdownStats(
        headings=headings,
        links=links,
        images=images,
        code_blocks=code_blocks,
        words=words,
    )


def _strip_fenced_code_and_count(content: str) -> tuple[str, int]:
    lines: list[str] = []
    in_block = False
    open_fence_char = ""
    open_fence_len = 0
    code_blocks = 0

    for line in content.splitlines():
        fence = _FENCE_START_RE.match(line)
        if fence:
            marker = fence.group(1)
            marker_char = marker[0]
            marker_len = len(marker)

            if not in_block:
                in_block = True
                open_fence_char = marker_char
                open_fence_len = marker_len
                continue

            if marker_char == open_fence_char and marker_len >= open_fence_len:
                in_block = False
                code_blocks += 1
                open_fence_char = ""
                open_fence_len = 0
                continue

        if not in_block:
            lines.append(line)

    return "\n".join(lines), code_blocks


def _strip_markdown_markup(content: str) -> str:
    content = _IMAGE_RE.sub(" ", content)
    content = _LINK_RE.sub(lambda m: m.group(0).split("](")[0].lstrip("["), content)
    content = re.sub(r"`[^`]*`", " ", content)
    content = re.sub(r"[*_~>#-]", " ", content)
    content = _HTML_TAG_RE.sub(" ", content)
    content = re.sub(r"\s+", " ", content)
    return content
