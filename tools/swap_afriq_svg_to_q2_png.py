from __future__ import annotations

import pathlib
import re


TARGET = "wp-content/uploads/afriq/Q%20-%20AfriQ%20ArtisanSkills%20with%20Centre%20Wording.svg?v=4"
REPLACEMENT = "wp-content/uploads/2020/08/Q%20-%202.png"

SRC_RE = re.compile(r'(?P<prefix>(?:\.\./)*)' + re.escape(TARGET))


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for html_path in root.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if TARGET not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            return f"{m.group('prefix')}{REPLACEMENT}"

        new_text = SRC_RE.sub(repl, text)
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(str(html_path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Replaced AfriQ SVG logo references in:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No files updated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

