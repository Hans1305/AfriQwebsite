from __future__ import annotations

import pathlib
import re


LOGO_ANCHOR_RE = re.compile(
    r'(?P<open><a\s+class="afriq-header__logo"[^>]*>)'
    r"(?P<body>[\s\S]*?)"
    r"(?P<close></a>)",
    re.IGNORECASE,
)


def rel_prefix(root: pathlib.Path, html_path: pathlib.Path) -> str:
    rel = html_path.relative_to(root)
    depth = len(rel.parts) - 1
    return "../" * depth


def replacement_body(prefix: str) -> str:
    return (
        '\n            <div style="display:flex; flex-direction:column; align-items:flex-start;">\n'
        f'              <img src="{prefix}wp-content/uploads/2020/08/Q%20-%202.png" alt="AfriQ ArtisanSkills" style="width:min(29px, 8.5vw); height:auto; display:block;" />\n'
        '              <div style="font-weight:900; letter-spacing:-.01em; color:#fff; margin-top:10px;">AfriQ ArtisanSkills</div>\n'
        "            </div>\n          "
    )


def should_process(root: pathlib.Path, path: pathlib.Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if rel == "index_new.html":
        return False
    if rel == "resources.html":
        return False
    if rel.startswith("wp-content/"):
        return False
    return True


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for html_path in root.rglob("*.html"):
        if not should_process(root, html_path):
            continue

        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if 'class="afriq-header__logo"' not in text:
            continue

        prefix = rel_prefix(root, html_path)

        def repl(m: re.Match[str]) -> str:
            return f"{m.group('open')}{replacement_body(prefix)}{m.group('close')}"

        new_text, count = LOGO_ANCHOR_RE.subn(repl, text, count=1)
        if count == 0 or new_text == text:
            continue

        html_path.write_text(new_text, encoding="utf-8", newline="\n")
        updated.append(str(html_path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Standardized header logo in:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No files updated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

