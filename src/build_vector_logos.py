#!/usr/bin/env python3
"""Compose soundadam-family lockups and marks from the traced wordmark.

The nine-cell grid + blue gradient is the shared "chassis" for every
sound-* product. Each product gets its own glyph cut into the grid via
ICONS; only soundadam has a traced wordmark today, so other family
members currently render as icon-only marks (see FAMILY below).
"""

import math
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


def polyline_path(points: list[tuple[float, float]]) -> str:
    """Dense sample polyline — faithful to the numpy Ricker, no spline fattening."""
    parts = [f"M{points[0][0]:.2f} {points[0][1]:.2f}"]
    parts.extend(f"L{x:.2f} {y:.2f}" for x, y in points[1:])
    return " ".join(parts)


def ricker(t: float) -> float:
    """Mexican-hat / Ricker wavelet: (1 - t²) exp(-t² / 2). Peak 1 at t=0.

    Zeros at t=±1, negative lobes at t=±√3 (value ≈ −0.446), returns to
    ~0 by |t|≈4. Same formula as numpy; scipy.signal.ricker is this
    shape at a discrete width.
    """
    return (1.0 - t * t) * math.exp(-0.5 * t * t)


# t ∈ [−4, 4]: edges ≈ 0 (flat brim). Previous [−2.4, 2.4] cut the
# return-to-zero and stretched the peak across the side columns.
RICKER_T_MAX = 4.0
RICKER_SAMPLES = 241
WAVEFORM_X0, WAVEFORM_X1 = 8.0, 216.0
WAVEFORM_Y_ZERO = 112.0
# Peak into the top row. True-ratio troughs only reach ~y=157 (gutter),
# so the grid overlay optionally stretches negatives to the bottom row.
WAVEFORM_AMP_POS = 96.0
WAVEFORM_AMP_NEG = 184.0  # −0.446 * 184 ≈ 82px below zero → y≈194
WAVEFORM_STROKE = 10
RICKER_TROUGH = -2.0 * math.exp(-1.5)  # exact min, t=±√3


def ricker_series(n: int = RICKER_SAMPLES, t_max: float = RICKER_T_MAX):
    """(t, ψ(t)) samples. numpy when present, identical math otherwise."""
    try:
        import numpy as np

        t = np.linspace(-t_max, t_max, n)
        psi = (1.0 - t * t) * np.exp(-0.5 * t * t)
        return list(zip(t.tolist(), psi.tolist()))
    except ImportError:
        return [
            (
                -t_max + 2 * t_max * i / (n - 1),
                ricker(-t_max + 2 * t_max * i / (n - 1)),
            )
            for i in range(n)
        ]


def waveform_points(*, brim_boost: bool = True) -> list[tuple[float, float]]:
    """Map a real Ricker onto the 224×224 nine-cell.

    Linear t→x. Positive lobe uses AMP_POS. If brim_boost, negative lobes
    use AMP_NEG so the hat brim cuts the bottom row; otherwise true 0.446
    ratio (brim sits in the mid/bottom gutter and vanishes at favicon size).
    """
    span = WAVEFORM_X1 - WAVEFORM_X0
    pts = []
    for t, psi in ricker_series():
        x = WAVEFORM_X0 + span * (t + RICKER_T_MAX) / (2 * RICKER_T_MAX)
        amp = WAVEFORM_AMP_POS if (psi >= 0 or not brim_boost) else WAVEFORM_AMP_NEG
        y = WAVEFORM_Y_ZERO - amp * psi
        pts.append((x, y))
    return pts


def waveform_overlay(
    cutout: str, filled: bool = True, *, brim_boost: bool = True
) -> str:
    pts = waveform_points(brim_boost=brim_boost)
    curve = polyline_path(pts)
    if filled:
        y0 = WAVEFORM_Y_ZERO
        return (
            f'<path d="{curve} L{pts[-1][0]:.2f} {y0:.2f} '
            f'L{pts[0][0]:.2f} {y0:.2f} Z" fill="{cutout}"/>'
        )
    return (
        f'<path d="{curve}" fill="none" stroke="{cutout}" '
        f'stroke-width="{WAVEFORM_STROKE}" stroke-linecap="round" '
        f'stroke-linejoin="round"/>'
    )


def waveform_stroke_overlay(cutout: str) -> str:
    """Same Ricker, stroke instead of fill — unused alternate in dist/waveform-stroke."""
    return waveform_overlay(cutout, filled=False)


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
    "waveform-stroke": waveform_stroke_overlay,
    "equalizer": equalizer_overlay,
    "relay": relay_overlay,
}

ICON_LABELS = {
    "waveform": "filled Mexican-hat waveform",
    "waveform-stroke": "stroked Mexican-hat waveform",
    "equalizer": "mixer faders",
    "relay": "signal relay",
}


def mark_svg(kind: str = "waveform", overlay: str | None = None) -> str:
    if overlay is None:
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
    for kind in ("waveform", "waveform-stroke", "equalizer"):
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
    (DIST / "waveform-stroke" / "mark.svg").write_text(
        mark_svg("waveform-stroke"), encoding="utf-8"
    )

    for slug, kind in FAMILY_ICON_ONLY.items():
        out = DIST / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "mark.svg").write_text(mark_svg(kind), encoding="utf-8")


if __name__ == "__main__":
    main()
