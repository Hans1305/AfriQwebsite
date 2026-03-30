from __future__ import annotations

import pathlib
import re


SVG_SRC_RE = re.compile(
    r'(?P<prefix>(?:\.\./)+)wp-content/uploads/afriq/Q%20-%20AfriQ%20ArtisanSkills%20with%20Centre%20Wording\.svg\?v=4'
)


IMG_TAG_RE = re.compile(
    r'<img\s+[^>]*?src="(?P<src>(?:\.\./)+wp-content/uploads/afriq/Q%20-%20AfriQ%20ArtisanSkills%20with%20Centre%20Wording\.svg\?v=4)"[^>]*?>\s*(?:</img>)?',
    re.IGNORECASE,
)


def replacement_block(prefix: str) -> str:
    q2_src = f'{prefix}wp-content/uploads/2020/08/Q%20-%202.png'
    return (
        '<div style="display:flex; flex-direction:column; align-items:flex-start;">\n'
        f'              <img src="{q2_src}" alt="AfriQ ArtisanSkills" style="width:min(29px, 8.5vw); height:auto; display:block;" />\n'
        '              <div style="font-weight:900; letter-spacing:-.01em; color:#fff; margin-top:10px;">AfriQ ArtisanSkills</div>\n'
        "            </div>"
    )


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for html_path in root.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if "Q%20-%202.png" in text and "AfriQ ArtisanSkills</div>" in text:
            continue

        m = SVG_SRC_RE.search(text)
        if not m:
            continue

        prefix = m.group("prefix")
        new_text, count = IMG_TAG_RE.subn(replacement_block(prefix), text, count=1)
        if count == 0:
            continue

        html_path.write_text(new_text, encoding="utf-8", newline="\n")
        updated.append(str(html_path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Updated header logo in:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No files updated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

