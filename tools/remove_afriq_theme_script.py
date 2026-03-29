from __future__ import annotations

import pathlib


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated = 0

    for html_path in root.rglob("*.html"):
        try:
            text = html_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        if "afriq-theme.js" not in text:
            continue

        lines = text.splitlines(True)
        new_lines: list[str] = []
        changed = False
        for line in lines:
            if "afriq-theme.js" in line:
                changed = True
                continue
            new_lines.append(line)

        if not changed:
            continue

        try:
            html_path.write_text("".join(new_lines), encoding="utf-8")
        except OSError:
            continue

        updated += 1

    print(f"Updated {updated} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
