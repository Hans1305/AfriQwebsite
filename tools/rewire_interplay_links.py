from __future__ import annotations

import pathlib


REPLACEMENTS: list[tuple[str, str]] = [
    ("https://www.afriqartisanskills.com/training/career-development-platform/", "training/career-development-platform/"),
    ("https://www.afriqartisanskills.com/training/courses/catalog/", "training/courses/catalog/"),
    ("https://www.afriqartisanskills.com/training/courses/", "training/courses/"),
    ("https://www.afriqartisanskills.com/training/certification-accreditation/", "training/certification-accreditation/"),
    ("https://www.afriqartisanskills.com/training/how-it-works/", "training/how-it-works/"),
    ("https://www.afriqartisanskills.com/industries/commercial-hvac/", "industries/commercial-hvac/"),
    ("https://www.afriqartisanskills.com/industries/multi-family-maintenance/", "industries/multi-family-maintenance/"),
    ("https://www.afriqartisanskills.com/industries/facilities-maintenance/", "industries/facilities-maintenance/"),
    ("https://www.afriqartisanskills.com/industries/industrial-maintenance/", "industries/industrial-maintenance/"),
    ("https://www.afriqartisanskills.com/industries/solar/", "industries/solar/"),
    ("https://www.afriqartisanskills.com/industries/safety/", "industries/safety/"),
    ("https://www.afriqartisanskills.com/about/meet-the-experts/", "about/meet-the-experts/"),
    ("https://www.afriqartisanskills.com/about/partners/", "about/partners/"),
    ("https://www.afriqartisanskills.com/about/", "about/"),
    ("https://www.afriqartisanskills.com/news/", "news/"),
    ("https://www.afriqartisanskills.com/careers/", "careers/"),
    ("https://www.afriqartisanskills.com/contact/", "contact/"),
    ("https://www.afriqartisanskills.com/privacy/", "privacy/"),
    ("https://www.afriqartisanskills.com/webinar/", "webinar/"),
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
