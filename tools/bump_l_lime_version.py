from __future__ import annotations

import pathlib
import re


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    pattern = re.compile(r"wp-content/uploads/2024/07/L_lime\.svg\?v=\d+")
    replacement = "wp-content/uploads/2024/07/L_lime.svg?v=4"

    updated = 0

    for html_path in root.rglob("*.html"):
        try:
            text = html_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        new_text, count = pattern.subn(replacement, text)
        if count == 0:
            continue

        try:
            html_path.write_text(new_text, encoding="utf-8")
        except OSError:
            continue

        updated += 1

    print(f"Updated {updated} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
