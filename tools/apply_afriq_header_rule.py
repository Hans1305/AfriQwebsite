from __future__ import annotations

import pathlib
import re


SCRIPT_TAG_RE = re.compile(r'<script[^>]+afriq-header-fix\.js', re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r'</head>', re.IGNORECASE)


def rel_prefix(root: pathlib.Path, html_path: pathlib.Path) -> str:
    rel = html_path.relative_to(root)
    parts = rel.parts
    # remove filename
    depth = len(parts) - 1
    return "../" * depth


def insert_script(html: str, script_tag: str) -> str:
    if SCRIPT_TAG_RE.search(html):
        return html
    # insert before </head>
    return HEAD_CLOSE_RE.sub(script_tag + "\n</head>", html, count=1)


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []
    for html_path in root.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if SCRIPT_TAG_RE.search(text):
            continue
        prefix = rel_prefix(root, html_path)
        script_tag = f'<script src="{prefix}afriq-header-fix.js?v=1" defer></script>'
        new_text = insert_script(text, script_tag)
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(str(html_path.relative_to(root)).replace("\\", "/"))
    if updated:
        print("Applied AfriQ header rule to:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("All pages already include afriq-header-fix.js")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

