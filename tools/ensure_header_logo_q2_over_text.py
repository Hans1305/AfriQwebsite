from __future__ import annotations

import pathlib
import re


TARGET_TEXT_DIV = (
    '<div style="font-weight:900; letter-spacing:-.01em; color:#fff; margin-top:10px;">'
    "AfriQ ArtisanSkills</div>"
)


LOGO_ANCHOR_RE = re.compile(
    r'(?P<open><a\s+class="afriq-header__logo"[^>]*>)\s*'
    r'(?P<div>'
    r'<div style="font-weight:900; letter-spacing:-\.01em; color:#fff; margin-top:10px;">'
    r'AfriQ ArtisanSkills</div>'
    r')\s*(?P<close></a>)',
    re.IGNORECASE,
)


def rel_prefix(root: pathlib.Path, html_path: pathlib.Path) -> str:
    rel = html_path.relative_to(root)
    depth = len(rel.parts) - 1
    return "../" * depth


def replacement_block(prefix: str) -> str:
    src = f'{prefix}wp-content/uploads/2020/08/Q%20-%202.png'
    return (
        '<div style="display:flex; flex-direction:column; align-items:flex-start;">\n'
        f'            <img src="{src}" alt="AfriQ ArtisanSkills" style="width:min(29px, 8.5vw); height:auto; display:block;" />\n'
        f"            {TARGET_TEXT_DIV}\n"
        "          </div>"
    )


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for html_path in root.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if TARGET_TEXT_DIV not in text:
            continue

        if '<a class="afriq-header__logo"' not in text:
            continue

        prefix = rel_prefix(root, html_path)

        def repl(m: re.Match[str]) -> str:
            return f"{m.group('open')}\n          {replacement_block(prefix)}\n          {m.group('close')}"

        new_text, count = LOGO_ANCHOR_RE.subn(repl, text)
        if count == 0:
            continue

        html_path.write_text(new_text, encoding="utf-8", newline="\n")
        updated.append(str(html_path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Updated header logo (added Q-2 above text) in:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No files updated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

