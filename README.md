# soundadam brand

Source of truth for the soundadam lockup. Products copy files from `dist/`;
they do not generate marks.

Two marks, two colorways. Do not put the blue hat or grid on a black canvas.

| Surface | File |
| --- | --- |
| Large mark (nine-cell, hat cutout) | [`dist/mark.svg`](dist/mark.svg) — light backgrounds only |
| Compact hat, light UI | [`dist/compact.svg`](dist/compact.svg) |
| Compact hat, brand-blue field | [`dist/compact-on-blue.svg`](dist/compact-on-blue.svg) |
| Lockup (hat + wordmark), light | [`dist/lockup.svg`](dist/lockup.svg) |
| Lockup on brand blue | [`dist/lockup-on-blue.svg`](dist/lockup-on-blue.svg) |
| Favicon (vector) | [`dist/compact.svg`](dist/compact.svg) (`mark-compact.svg` is the same file, kept as an alias) |
| Favicon (ICO) | [`dist/favicon.ico`](dist/favicon.ico) — compact on white |
| Touch / PWA raster | [`dist/apple-touch-icon.png`](dist/apple-touch-icon.png) (180), [`dist/icon-192.png`](dist/icon-192.png) — compact-on-blue |

Blue gradient: `#006fe8` → `#0f93ff` (mid highlight) → `#1386ff`. Wordmark on
light: `#050505`. Wordmark and hat on blue: `#ffffff`. Canvas: 1324×280
(lockup), 224×224 (marks). Grid cells: 68px, 8px gutter, 10px corner radius.

The nine-cell mark punches the hat through the grid so a **light** surface
shows in the cutout. Do not place it on blue (cells vanish) or on black
(too heavy). Next to type, use the compact hat — the grid reads cramped at
that scale.

## Archive

The unused stroked Mexican-hat lives in [`dist/archive/`](dist/archive/)
([`stroke.svg`](dist/archive/stroke.svg) for light, [`stroke-on-blue.svg`](dist/archive/stroke-on-blue.svg)
for inverse). Do not copy these into products.

## Already copied

| Product | Path in that repo |
| --- | --- |
| [soundadam.com](https://github.com/soundadam/soundadam.com) header and footer | `wp-content/themes/soundadam/assets/logo/soundadam-waveform.svg` ← `lockup.svg` |
| soundadam.com mark | `wp-content/themes/soundadam/assets/logo/soundadam-mark.svg` ← `dist/mark.svg` |
| soundadam.com favicon | `assets/logo/soundadam-mark-compact.svg` ← `dist/compact.svg` / `mark-compact.svg`; `assets/favicon.ico` / `icon-192.png` / `apple-touch-icon.png` from compact / compact-on-blue |
| [docs](https://github.com/soundadam/docs) (`docs.llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` ← `lockup.svg`; dark header should use `lockup-on-blue.svg` or `compact-on-blue.svg`, not a black canvas with a blue hat; `soundadam-mark.svg` ← `mark.svg`; favicon `soundadam-mark-compact.svg` |
| cluster product hosts | [platform-gitops](https://github.com/soundadam/platform-gitops) `clusters/production/networking/brand-favicon/` ← compact ICO / PNG / SVG |

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
(needs `rsvg-convert` and `magick`):

```sh
rsvg-convert -w 32 -h 32 dist/compact.svg -o /tmp/mark-32.png
rsvg-convert -w 48 -h 48 dist/compact.svg -o /tmp/mark-48.png
magick -size 32x32 xc:'#ffffff' /tmp/mark-32.png -composite /tmp/mark-32-white.png
magick -size 48x48 xc:'#ffffff' /tmp/mark-48.png -composite /tmp/mark-48-white.png
magick /tmp/mark-32-white.png /tmp/mark-48-white.png dist/favicon.ico
rsvg-convert -w 180 -h 180 dist/compact-on-blue.svg -o dist/apple-touch-icon.png
rsvg-convert -w 192 -h 192 dist/compact-on-blue.svg -o dist/icon-192.png
```
