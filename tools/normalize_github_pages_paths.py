from __future__ import annotations

import pathlib
import re


def compute_prefix(file_path: pathlib.Path, site_root: pathlib.Path) -> str:
    rel = file_path.relative_to(site_root)
    depth = max(0, len(rel.parents) - 1)
    if depth == 0:
        return ""
    return "../" * depth


def normalize_html(content: str, prefix: str) -> str:
    prefix_escaped = prefix.replace("/", r"\/")

    def repl_attr(match: re.Match[str]) -> str:
        quote = match.group(1)
        kind = match.group(2)
        path = match.group(3)
        return f"{kind}={quote}{prefix}{path}"

    def repl_css_url(match: re.Match[str]) -> str:
        quote = match.group(1) or ""
        path = match.group(2)
        return f"url({quote}{prefix}{path}{quote})"

    content = re.sub(
        r"""(=)(["'])/(wp-content/[^"']+)""",
        lambda m: f'{m.group(1)}{m.group(2)}{prefix}{m.group(3)}',
        content,
    )
    content = re.sub(
        r"""(=)(["'])/(wp-includes/[^"']+)""",
        lambda m: f'{m.group(1)}{m.group(2)}{prefix}{m.group(3)}',
        content,
    )
    content = re.sub(
        r"""url\((["']?)/(wp-content/[^"')]+)\1\)""",
        lambda m: f'url({m.group(1)}{prefix}{m.group(2)}{m.group(1)})',
        content,
    )
    content = re.sub(
        r"""url\((["']?)/(wp-includes/[^"')]+)\1\)""",
        lambda m: f'url({m.group(1)}{prefix}{m.group(2)}{m.group(1)})',
        content,
    )

    content = re.sub(
        r"""\\/(wp-content\\/)""",
        lambda m: f"{prefix_escaped}{m.group(1)}",
        content,
    )
    content = re.sub(
        r"""\\/(wp-includes\\/)""",
        lambda m: f"{prefix_escaped}{m.group(1)}",
        content,
    )

    return content


def main() -> None:
    site_root = pathlib.Path(__file__).resolve().parents[1]

    html_files = sorted(site_root.rglob("*.html"))
    changed_count = 0

    for file_path in html_files:
        prefix = compute_prefix(file_path, site_root)
        original = file_path.read_text(encoding="utf-8", errors="ignore")
        updated = normalize_html(original, prefix)
        if updated != original:
            file_path.write_text(updated, encoding="utf-8", newline="\n")
            changed_count += 1

    css_files = sorted((site_root / "wp-content" / "uploads" / "elementor" / "css").glob("*.css"))
    css_changed = 0
    for css_file in css_files:
        original = css_file.read_text(encoding="utf-8", errors="ignore")
        updated = original
        updated = updated.replace('url("/wp-content/uploads/', 'url("../../')
        updated = updated.replace("url('/wp-content/uploads/", "url('../../")
        updated = updated.replace("url(/wp-content/uploads/", "url(../../")
        if updated != original:
            css_file.write_text(updated, encoding="utf-8", newline="\n")
            css_changed += 1

    print(f"Updated {changed_count} HTML files and {css_changed} Elementor CSS files")


if __name__ == "__main__":
    main()
