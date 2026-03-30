from __future__ import annotations

import pathlib


REPLACEMENTS = {
    "â€œ": "“",
    "â€�": "”",
    "â€˜": "‘",
    "â€™": "’",
    "â€“": "–",
    "â€”": "—",
    "â€¢": "•",
    "â€¦": "…",
    "Â ": " ",
    "Â": "",
}


def fix_text(text: str) -> str:
    for bad, good in REPLACEMENTS.items():
        text = text.replace(bad, good)
    return text


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix.lower() not in {".html", ".css"}:
            continue
        original = path.read_text(encoding="utf-8", errors="ignore")
        fixed = fix_text(original)
        if fixed != original:
            path.write_text(fixed, encoding="utf-8", newline="\n")
            updated.append(str(path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Fixed mojibake in:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No mojibake found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

