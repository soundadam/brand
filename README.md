# soundadam brand

Generator and checked-in SVGs for the soundadam mark. Products copy files
from `dist/`; they do not generate marks.

This repo is small on purpose. Cluster hosts already take copies from
[platform-gitops](https://github.com/soundadam/platform-gitops). When that
tree grows a `brand/` (or `brand-favicon/`) directory that includes
`src/` plus `dist/`, archive this repository — do not keep a second
source of truth.

Four files, three jobs. Do not put the blue hat or grid on a black canvas.
Do not pad the nine-cell cutout onto white — the hole must stay transparent
so the page (or browser chrome) shows through.

| Job | File | Pair with type? |
| --- | --- | --- |
| Large / browser mark (nine-cell, hat **cutout**, alpha hole) | [`dist/mark.svg`](dist/mark.svg), [`dist/mark.png`](dist/mark.png) (512), [`dist/icon-192.png`](dist/icon-192.png) | No |
| Compact hat on light / transparent | [`dist/compact.svg`](dist/compact.svg) | Yes — this is the glyph in the lockup |
| Compact hat as a **tile** (blue field, white hat) | [`dist/compact-on-blue.svg`](dist/compact-on-blue.svg) | **No** — icon only |
| Lockup (compact hat + wordmark) | [`dist/lockup.svg`](dist/lockup.svg) | — |
| **Default site icon (SVG)** | [`dist/favicon.svg`](dist/favicon.svg) — same drawing as `compact.svg` | — |
| Legacy ICO fallback | [`dist/favicon.ico`](dist/favicon.ico) — 16/32/48/256, compact on white | — |
| iOS / opaque home-screen | [`dist/apple-touch-icon.png`](dist/apple-touch-icon.png) (180) — compact-on-blue | — |

`dist/mark-compact.svg` is a copy of `compact.svg` so existing product paths
do not break.

A page’s default icon is the **SVG**, not the ICO. Example:

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

Do not point `<link rel="icon">` at the 16×32 ICO alone. Tabs and the
address bar on a retina display will pick the SVG (or `mark.svg` if you
want the nine-cell cutout at large chrome sizes). Keep the ICO only so
old Windows / crawlers still get a bitmap.

Blue gradient: `#006fe8` → `#0f93ff` (mid highlight) → `#1386ff`. Wordmark:
`#050505`. Canvas: 1324×280 (lockup), 224×224 (marks). Grid cells: 68px, 8px
gutter, 10px corner radius.

The nine-cell mark punches the hat through the grid. Use it where the cutout
can pick up a **non-white** surface (dark UI, tinted page, browser tab). On
white the hole becomes a hard white slab and reads as a mistake. At small
sizes next to letters, drop the grid and use the compact hat.

`compact-on-blue` is a self-contained tile (touch icon, avatar, app glyph).
Do not sit it beside the wordmark — the blue square fights the type.

## Archive

The unused stroked Mexican-hat lives in [`dist/archive/`](dist/archive/)
([`stroke.svg`](dist/archive/stroke.svg) for light, [`stroke-on-blue.svg`](dist/archive/stroke-on-blue.svg)
for inverse). Do not copy these into products.

## Already copied

| Product | Path in that repo |
| --- | --- |
| [soundadam.com](https://github.com/soundadam/soundadam.com) header and footer | `wp-content/themes/soundadam/assets/logo/soundadam-waveform.svg` ← `lockup.svg` |
| soundadam.com mark | `wp-content/themes/soundadam/assets/logo/soundadam-mark.svg` ← `dist/mark.svg` (keep the cutout transparent; do not flatten onto white) |
| soundadam.com favicon | SVG: `favicon.svg` / `compact.svg`; ICO: `favicon.ico`; `apple-touch-icon.png` from compact-on-blue |
| [docs](https://github.com/soundadam/docs) (`docs.llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` ← `lockup.svg`; `soundadam-mark.svg` ← `mark.svg`; do not use `compact-on-blue` next to the wordmark |
| cluster product hosts | [platform-gitops](https://github.com/soundadam/platform-gitops) — copy `dist/` here when that tree is ready to own brand |

Copy again when the mark changes. Do not submodule this repo into WordPress
or Mintlify unless a product actually needs the whole tree.

Teaway’s Mintlify `docs/logo/{light,dark}.svg` is a product mark, not this
lockup.

## Rebuild SVG

`dist/*.svg` are the checked-in deliverable. `src/build_vector_logos.py`
recomposes them from `src/wordmark-trace.svg` (letterforms) plus the
Mexican-hat / Ricker wavelet sampled onto the 224×224 square
(`waveform_points`). Negative lobes are stretched so the brim cuts the
bottom row of the large mark; numpy is optional at build time.

```sh
python3 src/build_vector_logos.py
```

PNG rasters are not rebuilt by that script. After a geometry change
(needs `rsvg-convert` and `magick`; ICO needs Pillow so the 256px
frame stays PNG-compressed instead of a 280KB BMP). Never composite
`mark.svg` onto `#ffffff`.

```sh
rsvg-convert -w 512 -h 512 dist/mark.svg -o dist/mark.png
rsvg-convert -w 192 -h 192 dist/mark.svg -o dist/icon-192.png
TMP=$(mktemp -d)
for s in 16 32 48 256; do
  rsvg-convert -w "$s" -h "$s" dist/compact.svg -o "$TMP/c-$s.png"
  magick -size "${s}x${s}" xc:'#ffffff' "$TMP/c-$s.png" -composite PNG32:"$TMP/w-$s.png"
done
python3 - <<PY
from pathlib import Path
from PIL import Image
tmp = Path("$TMP")
Image.open(tmp / "w-256.png").convert("RGBA").save(
    "dist/favicon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (256, 256)],
    bitmap_format="png",
)
PY
rsvg-convert -w 180 -h 180 dist/compact-on-blue.svg -o dist/apple-touch-icon.png
```
