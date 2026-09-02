# soundadam brand

Source of truth for the soundadam lockup. Products copy files from `dist/`;
they do not generate marks.

Four files, three jobs. Do not put the blue hat or grid on a black canvas.
Do not pad the nine-cell cutout onto white — the hole must stay transparent
so the page (or browser chrome) shows through.

| Job | File | Pair with type? |
| --- | --- | --- |
| Large / browser mark (nine-cell, hat **cutout**, alpha hole) | [`dist/mark.svg`](dist/mark.svg), [`dist/mark.png`](dist/mark.png) (512), [`dist/icon-192.png`](dist/icon-192.png) | No |
| Compact hat on light / transparent | [`dist/compact.svg`](dist/compact.svg) | Yes — this is the glyph in the lockup |
| Compact hat as a **tile** (blue field, white hat) | [`dist/compact-on-blue.svg`](dist/compact-on-blue.svg) | **No** — icon only |
| Lockup (compact hat + wordmark) | [`dist/lockup.svg`](dist/lockup.svg) | — |
| Favicon ICO (legacy, 16/32) | [`dist/favicon.ico`](dist/favicon.ico) — compact on white | — |
| iOS / opaque home-screen | [`dist/apple-touch-icon.png`](dist/apple-touch-icon.png) (180) — compact-on-blue | — |

`dist/mark-compact.svg` is a copy of `compact.svg` so existing product paths
do not break.

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
| soundadam.com favicon | SVG: `mark.svg` in modern browsers, or `compact.svg` / `mark-compact.svg` at 16px; `assets/favicon.ico` from compact; `apple-touch-icon.png` from compact-on-blue |
| [docs](https://github.com/soundadam/docs) (`docs.llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` ← `lockup.svg`; `soundadam-mark.svg` ← `mark.svg`; do not use `compact-on-blue` next to the wordmark |
| cluster product hosts | [platform-gitops](https://github.com/soundadam/platform-gitops) `clusters/production/networking/brand-favicon/` ← compact ICO; SVG mark if the host can serve alpha |

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
(needs `rsvg-convert` and `magick`). Never composite `mark.svg` onto
`#ffffff`.

```sh
rsvg-convert -w 512 -h 512 dist/mark.svg -o dist/mark.png
rsvg-convert -w 192 -h 192 dist/mark.svg -o dist/icon-192.png
rsvg-convert -w 32 -h 32 dist/compact.svg -o /tmp/mark-32.png
rsvg-convert -w 48 -h 48 dist/compact.svg -o /tmp/mark-48.png
magick -size 32x32 xc:'#ffffff' /tmp/mark-32.png -composite /tmp/mark-32-white.png
magick -size 48x48 xc:'#ffffff' /tmp/mark-48.png -composite /tmp/mark-48-white.png
magick /tmp/mark-32-white.png /tmp/mark-48-white.png dist/favicon.ico
rsvg-convert -w 180 -h 180 dist/compact-on-blue.svg -o dist/apple-touch-icon.png
```
