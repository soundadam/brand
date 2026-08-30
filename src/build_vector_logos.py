#!/usr/bin/env python3
"""Compose waveform / equalizer lockups from the traced wordmark."""

from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent
DIST = ROOT / "dist"
TRACE = SRC / "wordmark-trace.svg"

CANVAS_W = 1280
CANVAS_H = 280


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


def icon_cells() -> str:
    cells = []
    for y in (2, 78, 154):
        for x in (2, 78, 154):
            cells.append(f'<rect x="{x}" y="{y}" width="68" height="68" rx="6"/>')
    return "\n        ".join(cells)


def icon_overlay(kind: str, cutout: str) -> str:
    if kind == "waveform":
        return (
            '<path d="M2 142 C20 141 29 126 44 124 '
            'C59 122 66 141 78 142 C92 143 93 82 111 69 '
            'C129 56 134 140 150 140 C164 140 170 124 184 124 '
            f'C198 124 205 141 222 143" fill="none" stroke="{cutout}" '
            'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if kind == "equalizer":
        return "\n        ".join(
            [
                f'<path d="M61 58 V164" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
                f'<path d="M110 49 V182" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
                f'<path d="M162 59 V166" fill="none" stroke="{cutout}" stroke-width="10" stroke-linecap="round"/>',
                f'<rect x="10" y="96" width="11" height="34" rx="5.5" fill="{cutout}"/>',
                f'<rect x="207" y="96" width="11" height="34" rx="5.5" fill="{cutout}"/>',
            ]
        )
    raise ValueError(kind)


def mark_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="224" height="224" viewBox="0 0 224 224">
  <defs>
    <linearGradient id="soundadam-blue" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0" stop-color="#006fe8"/>
      <stop offset="1" stop-color="#1386ff"/>
    </linearGradient>
    <mask id="mark-cutout" maskUnits="userSpaceOnUse" x="0" y="0" width="224" height="224">
      <g fill="#ffffff">
        {icon_cells()}
      </g>
      {icon_overlay("waveform", "#000000")}
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

    label = "mixer faders" if kind == "equalizer" else "acoustic waveform"
    background_rect = "" if transparent else f'<rect width="1280" height="280" fill="{background}"/>'
    if transparent:
        symbol_markup = f'''<mask id="symbol-cutout" maskUnits="userSpaceOnUse" x="40" y="28" width="224" height="224">
      <g transform="translate(40 28)" fill="#ffffff">
        {icon_cells()}
        <g>{icon_overlay(kind, "#000000")}</g>
      </g>
    </mask>
    <rect x="40" y="28" width="224" height="224" fill="url(#soundadam-blue)" mask="url(#symbol-cutout)"/>'''
    else:
        symbol_markup = f'''<g transform="translate(40 28)">
    <g fill="url(#soundadam-blue)">
        {icon_cells()}
    </g>
    {icon_overlay(kind, background)}
  </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" aria-labelledby="title desc">
  <title id="title">SoundAdam O&amp;M + acoustics logo</title>
  <desc id="desc">SoundAdam wordmark with a blue nine-cell {label} symbol on a {theme} background.</desc>
  <defs>
    <linearGradient id="soundadam-blue" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0" stop-color="#006fe8"/>
      <stop offset="1" stop-color="#1386ff"/>
    </linearGradient>
  </defs>
  {background_rect}
  {symbol_markup}
  <g transform="translate(318 28)" fill="{foreground}" fill-rule="evenodd">
      {wordmark}
  </g>
</svg>
'''


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
    (DIST / "mark.svg").write_text(mark_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
