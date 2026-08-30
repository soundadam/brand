#!/usr/bin/env python3
"""Compose soundadam-family lockups and marks from the traced wordmark.

The nine-cell grid + blue gradient is the shared "chassis" for every
sound-* product. Each product gets its own glyph cut into the grid via
ICONS; only soundadam has a traced wordmark today, so other family
members currently render as icon-only marks (see FAMILY below).
"""

from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent
DIST = ROOT / "dist"
TRACE = SRC / "wordmark-trace.svg"

CANVAS_W = 1324
CANVAS_H = 280
GRID_MARGIN = 48
WORDMARK_GAP = 64

GRADIENT_STOPS = [
    (0, "#006fe8"),
    (0.5, "#0f93ff"),
    (1, "#1386ff"),
]


def wordmark_paths() -> str:
    root = ET.parse(TRACE).getroot()
    chunks = []
    for element in root.iter():
        if element.tag.endswith("path") and element.get("d"):
            transform = element.get("transform")
            transform_attr = f' transform="{transform}"' if transform else ""
            chunks.append(f'<path d="{element.get("d")}"{transform_attr}/>')
    if not chunks:
        raise RuntimeError(f"No wordmark paths in {TRACE}")
    return "\n      ".join(chunks)


def gradient_def() -> str:
    stops = "\n      ".join(
        f'<stop offset="{offset}" stop-color="{color}"/>' for offset, color in GRADIENT_STOPS
    )
    return f'''<linearGradient id="soundadam-blue" x1="0%" y1="100%" x2="100%" y2="0%">
      {stops}
    </linearGradient>'''


def icon_cells(rx: int = 10) -> str:
    cells = []
    for y in (2, 78, 154):
        for x in (2, 78, 154):
            cells.append(f'<rect x="{x}" y="{y}" width="68" height="68" rx="{rx}"/>')
    return "\n        ".join(cells)


# Original Aug 21 lockup: a centred peak with matching side humps.
# Do not off-centre the transient — that reads as a broken sine, not a mark.
WAVEFORM_PATH = (
    "M2 142 C20 141 29 126 44 124 "
    "C59 122 66 141 78 142 C92 143 93 82 111 69 "
    "C129 56 134 140 150 140 C164 140 170 124 184 124 "
    "C198 124 205 141 222 143"
)


def waveform_overlay(cutout: str) -> str:
    return (
        f'<path d="{WAVEFORM_PATH}" fill="none" stroke="{cutout}" '
        'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def equalizer_overlay(cutout: str) -> str:
    return "\n        ".join(
        [
            f'<path d="M61 58 V164" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
            f'<path d="M110 49 V182" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
            f'<path d="M162 59 V166" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
            f'<rect x="10" y="96" width="11" height="34" rx="5.5" fill="{cutout}"/>',
            f'<rect x="207" y="96" width="11" height="34" rx="5.5" fill="{cutout}"/>',
        ]
    )


def relay_overlay(cutout: str) -> str:
    """Arrow – node – arrow: a signal passing through a relay station."""
    return "\n        ".join(
        [
            f'<path d="M30 112 H194" fill="none" stroke="{cutout}" stroke-width="9" stroke-linecap="round"/>',
            f'<path d="M54 88 L30 112 L54 136" fill="none" stroke="{cutout}" stroke-width="9" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="M170 88 L194 112 L170 136" fill="none" stroke="{cutout}" stroke-width="9" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
            f'<circle cx="112" cy="112" r="19" fill="{cutout}"/>',
        ]
    )


ICONS = {
    "waveform": waveform_overlay,
    "equalizer": equalizer_overlay,
    "relay": relay_overlay,
}

ICON_LABELS = {
    "waveform": "acoustic waveform",
    "equalizer": "mixer faders",
    "relay": "signal relay",
}


def mark_svg(kind: str = "waveform") -> str:
    overlay = ICONS[kind]("#000000")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="224" height="224" viewBox="0 0 224 224">
  <defs>
    {gradient_def()}
    <mask id="mark-cutout" maskUnits="userSpaceOnUse" x="0" y="0" width="224" height="224">
      <g fill="#ffffff">
        {icon_cells()}
      </g>
      {overlay}
    </mask>
  </defs>
  <rect width="224" height="224" fill="url(#soundadam-blue)" mask="url(#mark-cutout)"/>
</svg>
'''


def svg_document(kind: str, theme: str, wordmark: str, transparent: bool = False) -> str:
    if theme == "light":
        background = "#ffffff"
        foreground = "#050505"
    elif theme == "dark":
        background = "#07111c"
        foreground = "#f7f9fb"
    else:
        raise ValueError(theme)

    label = ICON_LABELS[kind]
    overlay = ICONS[kind]
    background_rect = "" if transparent else f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="{background}"/>'
    if transparent:
        symbol_markup = f'''<mask id="symbol-cutout" maskUnits="userSpaceOnUse" x="{GRID_MARGIN}" y="28" width="224" height="224">
      <g transform="translate({GRID_MARGIN} 28)" fill="#ffffff">
        {icon_cells()}
        <g>{overlay("#000000")}</g>
      </g>
    </mask>
    <rect x="{GRID_MARGIN}" y="28" width="224" height="224" fill="url(#soundadam-blue)" mask="url(#symbol-cutout)"/>'''
    else:
        symbol_markup = f'''<g transform="translate({GRID_MARGIN} 28)">
    <g fill="url(#soundadam-blue)">
        {icon_cells()}
    </g>
    {overlay(background)}
  </g>'''
    wordmark_x = GRID_MARGIN + 224 + WORDMARK_GAP
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" aria-labelledby="title desc">
  <title id="title">soundadam O&amp;M + acoustics logo</title>
  <desc id="desc">soundadam wordmark with a blue nine-cell {label} symbol on a {theme} background.</desc>
  <defs>
    {gradient_def()}
  </defs>
  {background_rect}
  {symbol_markup}
  <g transform="translate({wordmark_x} 28)" fill="{foreground}" fill-rule="evenodd">
      {wordmark}
  </g>
</svg>
'''


# Family members that only need the shared grid + a glyph today (no traced
# wordmark yet). Add an entry here and a matching ICONS function to spin up
# a new sound-* product mark; give it a wordmark trace later to promote it
# to a full lockup like soundadam's.
FAMILY_ICON_ONLY = {
    "soundapi": "relay",
}


def main() -> None:
    wordmark = wordmark_paths()
    for kind in ("waveform", "equalizer"):
        out = DIST / kind
        out.mkdir(parents=True, exist_ok=True)
        for theme in ("light", "dark"):
            (out / f"on-{theme}.svg").write_text(
                svg_document(kind, theme, wordmark), encoding="utf-8"
            )
            (out / f"transparent-on-{theme}.svg").write_text(
                svg_document(kind, theme, wordmark, transparent=True),
                encoding="utf-8",
            )
    mark = mark_svg("waveform")
    (DIST / "mark.svg").write_text(mark, encoding="utf-8")
    (DIST / "waveform" / "mark.svg").write_text(mark, encoding="utf-8")

    for slug, kind in FAMILY_ICON_ONLY.items():
        out = DIST / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "mark.svg").write_text(mark_svg(kind), encoding="utf-8")


if __name__ == "__main__":
    main()
