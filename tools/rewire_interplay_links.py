from __future__ import annotations

import pathlib


REPLACEMENTS: list[tuple[str, str]] = [
    ("https://www.interplaylearning.com/training/career-development-platform/", "training/career-development-platform/"),
    ("https://www.interplaylearning.com/training/courses/catalog/", "training/courses/catalog/"),
    ("https://www.interplaylearning.com/training/courses/", "training/courses/"),
    ("https://www.interplaylearning.com/training/certification-accreditation/", "training/certification-accreditation/"),
    ("https://www.interplaylearning.com/training/how-it-works/", "training/how-it-works/"),
    ("https://www.interplaylearning.com/industries/commercial-hvac/", "industries/commercial-hvac/"),
    ("https://www.interplaylearning.com/industries/multi-family-maintenance/", "industries/multi-family-maintenance/"),
    ("https://www.interplaylearning.com/industries/facilities-maintenance/", "industries/facilities-maintenance/"),
    ("https://www.interplaylearning.com/industries/industrial-maintenance/", "industries/industrial-maintenance/"),
    ("https://www.interplaylearning.com/industries/solar/", "industries/solar/"),
    ("https://www.interplaylearning.com/industries/safety/", "industries/safety/"),
    ("https://www.interplaylearning.com/about/meet-the-experts/", "about/meet-the-experts/"),
    ("https://www.interplaylearning.com/about/partners/", "about/partners/"),
    ("https://www.interplaylearning.com/about/", "about/"),
    ("https://www.interplaylearning.com/news/", "news/"),
    ("https://www.interplaylearning.com/careers/", "careers/"),
    ("https://www.interplaylearning.com/contact/", "contact/"),
    ("https://www.interplaylearning.com/privacy/", "privacy/"),
    ("https://www.interplaylearning.com/webinar/", "webinar/"),
    ("https://interplaylearning.tourial.com/pages/interplay-learning-overview-tour", "tourial/overview/"),
    ("https://interplaylearning.tourial.com/pages/interplay-learning-overview-tour/", "tourial/overview/"),
    ("https://www.iti.com/courses/industries", "industries/crane-and-rigging/"),
]


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[1]
    updated_files: list[pathlib.Path] = []

    for html_path in root.rglob("*.html"):
        try:
            text = html_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        new_text = text
        for find, replace in REPLACEMENTS:
            new_text = new_text.replace(find, replace)

        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8", newline="\n")
            updated_files.append(html_path)

    if updated_files:
        rel = [str(p.relative_to(root)).replace("\\", "/") for p in updated_files]
        print("Updated HTML files:")
        for p in sorted(rel):
            print(f"- {p}")
    else:
        print("No changes needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
