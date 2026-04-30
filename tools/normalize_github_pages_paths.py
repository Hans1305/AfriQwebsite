from __future__ import annotations

import pathlib
import re
import urllib.parse


def compute_prefix(file_path: pathlib.Path, site_root: pathlib.Path) -> str:
    rel = file_path.relative_to(site_root)
    depth = max(0, len(rel.parents) - 1)
    if depth == 0:
        return ""
    return "../" * depth


def safe_write_text(file_path: pathlib.Path, content: str, *, encoding: str = "utf-8") -> None:
    temp_path = file_path.with_name(file_path.name + ".tmp")
    temp_path.write_text(content, encoding=encoding)
    try:
        file_path.unlink()
    except FileNotFoundError:
        pass
    temp_path.replace(file_path)


def normalize_html(content: str, prefix: str, site_root: pathlib.Path) -> str:
    prefix_escaped = prefix.replace("/", r"\/")

    def rewrite_root_absolute_url(value: str) -> str:
        if not value or value[0] != "/":
            return value
        if value.startswith("//"):
            return value
        if value.startswith("/AfriQwebsite/"):
            return value

        base = value
        suffix = ""
        q = base.find("?")
        h = base.find("#")
        cut = min([i for i in (q, h) if i != -1], default=-1)
        if cut != -1:
            base, suffix = base[:cut], base[cut:]

        if base == "/":
            base = "/index_new.html"

        target_rel = base.lstrip("/")
        target_path = site_root / urllib.parse.unquote(target_rel)
        if target_path.is_dir():
            if not base.endswith("/"):
                base = base + "/"
            if (target_path / "index.html").exists():
                return f"{prefix}{base.lstrip('/')}{suffix}"

        if target_path.exists():
            return f"{prefix}{base.lstrip('/')}{suffix}"

        return f"https://www.afriqartisanskills.com{base}{suffix}"

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

    content = re.sub(
        r"""href=(["'])/([^"']*)\1""",
        lambda m: f'href={m.group(1)}{rewrite_root_absolute_url("/" + m.group(2))}{m.group(1)}',
        content,
    )
    content = re.sub(
        r"""src=(["'])/([^"']*)\1""",
        lambda m: f'src={m.group(1)}{rewrite_root_absolute_url("/" + m.group(2))}{m.group(1)}',
        content,
    )
    content = re.sub(
        r"""url\((["']?)/([^"')]+)\1\)""",
        lambda m: f'url({m.group(1)}{rewrite_root_absolute_url("/" + m.group(2))}{m.group(1)})',
        content,
    )

    content = re.sub(
        r"""(^|[\s,(])/(wp-content/)""",
        lambda m: f"{m.group(1)}{prefix}{m.group(2)}",
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"""(^|[\s,(])/(wp-includes/)""",
        lambda m: f"{m.group(1)}{prefix}{m.group(2)}",
        content,
        flags=re.MULTILINE,
    )

    content = re.sub(
        r"""@font-face\s*\{[\s\S]*?assets/fonts/astra[\s\S]*?\}""",
        "",
        content,
        flags=re.IGNORECASE,
    )

    return content


def normalize_css(content: str, prefix: str, css_file: pathlib.Path) -> str:
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

    css_path = str(css_file).replace("\\", "/")

    def strip_src_from_font_face(block: str) -> str:
        return re.sub(r"""src:[^;}]*(?:;|(?=\}))""", "", block)

    def strip_src_font_faces(css: str) -> str:
        return re.sub(r"""@font-face\s*\{[\s\S]*?\}""", lambda m: strip_src_from_font_face(m.group(0)), css)

    if css_path.endswith("/wp-content/astra-local-fonts/astra-local-fonts.css"):
        content = re.sub(r"""(?m)^\s*src:\s*[^;]+;\s*$""", "", content)

    if css_path.endswith("/wp-content/plugins/elementor/assets/lib/eicons/css/elementor-icons.min.css"):
        content = strip_src_font_faces(content)

    if "/wp-content/plugins/elementor/assets/lib/font-awesome/css/" in css_path:
        content = strip_src_font_faces(content)

    if css_path.endswith("/wp-content/plugins/happy-elementor-addons/assets/fonts/style.min.css"):
        content = strip_src_font_faces(content)

    if css_path.endswith("/wp-content/plugins/quadmenu/assets/frontend/icons/fontawesome5/css/all.min.css"):
        content = strip_src_font_faces(content)

    if css_path.endswith("/wp-content/plugins/quadmenu/assets/frontend/owlcarousel/owl.carousel.min.css"):
        content = re.sub(r"""url\((["']?)owl\.video\.play\.png\1\)""", "none", content)

    if css_path.endswith("/wp-content/plugins/webtoffee-gdpr-cookie-consent/public/css/cookie-law-info-public.css"):
        content = re.sub(r"""url\((["']?)\.\./images/cli_placeholder\.svg\1\)""", "none", content)

    if "/wp-content/uploads/elementor/google-fonts/css/" in css_path:
        content = strip_src_font_faces(content)

    return content


def audit_missing_references(site_root: pathlib.Path) -> list[tuple[str, str]]:
    attr_re = re.compile(r"""\b(?:href|src)=(["'])([^"']+)\1""", re.IGNORECASE)
    url_re = re.compile(r"""url\(([^)]+)\)""", re.IGNORECASE)
    skip_prefixes = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")

    def clean(value: str) -> str:
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        return value

    def is_skippable(value: str) -> bool:
        lower = value.lower()
        if "/" not in lower and "." not in lower and not lower.endswith("/"):
            return True
        return lower.startswith(skip_prefixes) or lower.startswith("//") or lower.startswith("#")

    def resolve(file_path: pathlib.Path, value: str) -> pathlib.Path:
        value = value.split("#", 1)[0].split("?", 1)[0]
        if value.startswith("/"):
            return (site_root / urllib.parse.unquote(value.lstrip("/"))).resolve()
        return (file_path.parent / urllib.parse.unquote(value)).resolve()

    missing: set[tuple[str, str]] = set()
    for file_path in list(site_root.rglob("*.html")) + list(site_root.rglob("*.css")):
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for m in attr_re.finditer(text):
            value = clean(m.group(2))
            if is_skippable(value):
                continue
            target = resolve(file_path, value)
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                missing.add((str(file_path.relative_to(site_root)), value))

        for m in url_re.finditer(text):
            value = clean(m.group(1))
            if is_skippable(value):
                continue
            target = resolve(file_path, value)
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                missing.add((str(file_path.relative_to(site_root)), value))

    return sorted(missing)


def main() -> None:
    site_root = pathlib.Path(__file__).resolve().parents[1]

    html_files = sorted(site_root.rglob("*.html"))
    changed_count = 0

    for file_path in html_files:
        prefix = compute_prefix(file_path, site_root)
        original = file_path.read_text(encoding="utf-8", errors="ignore")
        updated = normalize_html(original, prefix, site_root)
        if updated != original:
            safe_write_text(file_path, updated, encoding="utf-8")
            changed_count += 1

    css_files = []
    css_files.extend(sorted((site_root / "wp-content" / "astra-local-fonts").glob("*.css")))
    css_files.extend(
        sorted((site_root / "wp-content" / "uploads" / "elementor" / "google-fonts" / "css").glob("*.css"))
    )
    css_files.extend(sorted((site_root / "wp-content" / "uploads" / "elementor" / "css").glob("*.css")))
    css_files.append(site_root / "wp-content" / "plugins" / "elementor" / "assets" / "lib" / "eicons" / "css" / "elementor-icons.min.css")
    css_files.extend(sorted((site_root / "wp-content" / "plugins" / "elementor" / "assets" / "lib" / "font-awesome" / "css").glob("*.css")))
    css_files.append(site_root / "wp-content" / "plugins" / "happy-elementor-addons" / "assets" / "fonts" / "style.min.css")
    css_files.append(
        site_root
        / "wp-content"
        / "plugins"
        / "quadmenu"
        / "assets"
        / "frontend"
        / "icons"
        / "fontawesome5"
        / "css"
        / "all.min.css"
    )
    css_files.append(
        site_root / "wp-content" / "plugins" / "quadmenu" / "assets" / "frontend" / "owlcarousel" / "owl.carousel.min.css"
    )
    css_files.append(
        site_root
        / "wp-content"
        / "plugins"
        / "webtoffee-gdpr-cookie-consent"
        / "public"
        / "css"
        / "cookie-law-info-public.css"
    )
    css_changed = 0
    for css_file in css_files:
        prefix = compute_prefix(css_file, site_root)
        original = css_file.read_text(encoding="utf-8", errors="ignore")
        updated = normalize_css(original, prefix, css_file)
        if updated != original:
            safe_write_text(css_file, updated, encoding="utf-8")
            css_changed += 1

    missing = audit_missing_references(site_root)
    print(f"Updated {changed_count} HTML files and {css_changed} CSS files")
    print(f"Missing references: {len(missing)}")
    for file_path, value in missing[:50]:
        print(f"{file_path} -> {value}")
    if len(missing) > 50:
        print(f"... and {len(missing) - 50} more")


if __name__ == "__main__":
    main()
