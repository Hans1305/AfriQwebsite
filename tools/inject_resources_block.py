from __future__ import annotations

import os
import pathlib


DISCIPLINE_ANCHORS: list[tuple[str, str]] = [
    ("hvac", "HVAC"),
    ("commercial-hvac", "Commercial HVAC"),
    ("plumbing", "Plumbing"),
    ("electrical", "Electrical"),
    ("solar", "Solar"),
    ("safety", "Safety"),
    ("multi-family-maintenance", "Multi-Family Maintenance"),
    ("facilities-maintenance", "Facilities Maintenance"),
    ("industrial-maintenance", "Industrial Maintenance"),
    ("crane-and-rigging", "Crane & Rigging"),
    ("automotive", "Automotive (MVAC)"),
    ("diesel-mechanics", "Diesel Mechanics"),
    ("motor-mechanics", "Motor Mechanics"),
    ("auto-electrician", "Auto Electrician"),
    ("welding", "Welding"),
    ("construction", "Construction"),
    ("entrepreneurial", "Entrepreneurial"),
]


def rel_href(from_path: pathlib.Path, target: pathlib.Path) -> str:
    rel = os.path.relpath(target, start=from_path.parent)
    rel = pathlib.PurePosixPath(rel).as_posix()
    if not rel.startswith("."):
        rel = "./" + rel
    return rel


def build_block(from_path: pathlib.Path, root: pathlib.Path) -> str:
    resources_html = root / "resources.html"
    catalogue_dir = root / "training" / "courses" / "catalog"
    resources_href = rel_href(from_path, resources_html) + "#disciplines"
    catalogue_href = rel_href(from_path, catalogue_dir) + "/"

    links = " · ".join(
        f'<a href="{rel_href(from_path, resources_html)}#{anchor}">{label}</a>'
        for anchor, label in DISCIPLINE_ANCHORS
    )

    return (
        '\n      <section class="afriq-section afriq-strip" data-afriq-resources="true">\n'
        '        <div class="afriq-container">\n'
        '          <div class="afriq-cta">\n'
        '            <div>\n'
        '              <h3 class="afriq-cta__title">Resources</h3>\n'
        f'              <p class="afriq-cta__text">{links}</p>\n'
        "            </div>\n"
        '            <div class="afriq-cta__actions">\n'
        f'              <a class="afriq-btn" href="{resources_href}">View Resources</a>\n'
        f'              <a class="afriq-btn afriq-btn--outline" href="{catalogue_href}">Course Catalogue</a>\n'
        "            </div>\n"
        "          </div>\n"
        "        </div>\n"
        "      </section>\n"
    )


def should_process(path: pathlib.Path, root: pathlib.Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if rel == "index_new.html":
        return False
    if rel.endswith(".html") and (
        rel.startswith("industries/")
        or rel.startswith("solutions/")
        or rel.startswith("training/")
        or rel.startswith("about/")
        or rel.startswith("news/")
        or rel.startswith("careers/")
        or rel.startswith("contact/")
    ):
        return True
    if rel in {"resources.html"}:
        return True
    return False


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated: list[str] = []

    for html_path in root.rglob("*.html"):
        if not should_process(html_path, root):
            continue

        text = html_path.read_text(encoding="utf-8", errors="ignore")
        if 'data-afriq-resources="true"' in text:
            continue

        if "</main>" not in text:
            continue

        block = build_block(html_path, root)
        new_text = text.replace("</main>", block + "    </main>", 1)

        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(str(html_path.relative_to(root)).replace("\\", "/"))

    if updated:
        print("Injected resources block into:")
        for p in sorted(updated):
            print(f"- {p}")
    else:
        print("No pages needed updates.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
