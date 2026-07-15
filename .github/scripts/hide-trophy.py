#!/usr/bin/env python3
"""Remove one panel from a github-profile-trophy SVG."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
SVG_TAG = f"{{{SVG_NAMESPACE}}}svg"
TEXT_TAG = f"{{{SVG_NAMESPACE}}}text"
PANEL_WIDTH = 115
PANEL_MARGIN = 10


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"Usage: {sys.argv[0]} SVG_PATH PANEL_TITLE")

    path = Path(sys.argv[1])
    panel_title = sys.argv[2]

    ET.register_namespace("", SVG_NAMESPACE)
    tree = ET.parse(path)
    root = tree.getroot()
    panels = [child for child in root if child.tag == SVG_TAG]
    matches = [
        panel
        for panel in panels
        if any((text.text or "").strip() == panel_title for text in panel.iter(TEXT_TAG))
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one {panel_title!r} panel in {path}, found {len(matches)}"
        )

    root.remove(matches[0])
    remaining_panels = [child for child in root if child.tag == SVG_TAG]
    for index, panel in enumerate(remaining_panels):
        panel.set("x", str(index * (PANEL_WIDTH + PANEL_MARGIN)))

    width = PANEL_WIDTH * len(remaining_panels) + PANEL_MARGIN * (
        len(remaining_panels) - 1
    )
    root.set("width", str(width))
    root.set("viewBox", f"0 0 {width} {root.get('height')}")
    tree.write(path, encoding="unicode")


if __name__ == "__main__":
    main()

