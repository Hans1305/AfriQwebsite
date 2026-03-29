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

        if "afriq-theme.js" in text:
            continue

        if "afriq-site.css" not in text and "afriq-subpages.css" not in text:
            continue

        lower = text.lower()
        head_close = lower.rfind("</head>")
        if head_close == -1:
            continue

        rel = html_path.relative_to(root)
        depth = max(len(rel.parts) - 1, 0)
        prefix = "../" * depth
        tag = f'    <script src="{prefix}afriq-theme.js?v=1" defer></script>\n'

        text = text[:head_close] + tag + text[head_close:]
        try:
            html_path.write_text(text, encoding="utf-8")
        except OSError:
            continue

        updated += 1

    print(f"Updated {updated} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
