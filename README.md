# soundadam brand

Source of truth for the soundadam lockup. Products copy files from `dist/`;
they do not generate marks.

The live wordmark is the **filled** Mexican-hat waveform lockup. Stroke
waveform and equalizer sets are unused alternates kept here so they do
not live only in scratch.

## Use this

| Surface | File |
| --- | --- |
| Light UI, transparent canvas | [`dist/waveform/transparent-on-light.svg`](dist/waveform/transparent-on-light.svg) |
| Dark UI, transparent canvas | [`dist/waveform/transparent-on-dark.svg`](dist/waveform/transparent-on-dark.svg) |
| Favicon / tab icon (vector) | [`dist/mark-compact.svg`](dist/mark-compact.svg) — blue hat, no grid |
| Large mark / lockup companion | [`dist/mark.svg`](dist/mark.svg) — nine-cell grid |
| Favicon (ICO) | [`dist/favicon.ico`](dist/favicon.ico) |
| Touch / PWA raster | [`dist/apple-touch-icon.png`](dist/apple-touch-icon.png) (180), [`dist/icon-192.png`](dist/icon-192.png) |

Opaque `on-light` / `on-dark` SVG and PNG sit next to those for slides or
places that cannot composite a transparent SVG. Prefer SVG. Do not keep a
ladder of tiny mark PNGs — they are unreadable.

Blue gradient: `#006fe8` → `#0f93ff` (mid highlight) → `#1386ff`. Wordmark on
light: `#050505`. Wordmark on dark: `#f7f9fb`. Canvas: 1324×280 (wordmark),
224×224 (mark). Grid cells: 68px, 8px gutter, 10px corner radius.

## Family system

Every `sound-*` product (soundadam, soundapi, ...) shares one chassis: the
nine-cell grid + blue gradient. What changes per product is the glyph cut
into the grid — `soundadam` gets the filled Mexican-hat waveform,
`soundapi` gets a signal relay (arrow – node – arrow), and so on. Same
silhouette at a glance, distinct icon up close.

`src/build_vector_logos.py` keeps this as an `ICONS` registry (name → glyph
function) plus a `FAMILY_ICON_ONLY` map of `slug -> icon kind`. To add a new
product mark:

1. Write a glyph function (see `relay_overlay` for a minimal example) and
   register it in `ICONS`.
2. Add `"your-slug": "your-icon"` to `FAMILY_ICON_ONLY`.
3. Run the build script — it writes `dist/your-slug/mark.svg`.

That only gets you the icon-only mark (grid + glyph, no text) — enough for
a large avatar or the lockup companion. Tab-sized favicons use
`mark-compact.svg` instead: the 8px gutters collapse at 16–32px and the
grid reads as noise, so those files are the filled hat with no cells. A
full text lockup like soundadam's needs its own traced wordmark (see
"Rebuild SVG" below), since the wordmark is hand-traced art, not live
type; there's no font file behind it to retype.

| Product | Mark |
| --- | --- |
| soundadam | [`dist/mark.svg`](dist/mark.svg) — filled Mexican-hat waveform |
| soundadam (stroke, unused) | [`dist/waveform-stroke/`](dist/waveform-stroke/) |
| soundapi | [`dist/soundapi/mark.svg`](dist/soundapi/mark.svg) — signal relay |

## Already copied

| Product | Path in that repo |
| --- | --- |
| [soundadam.com](https://github.com/soundadam/soundadam.com) header and footer | `wp-content/themes/soundadam/assets/logo/soundadam-waveform.svg` ← `transparent-on-light.svg` |
| soundadam.com mark | `wp-content/themes/soundadam/assets/logo/soundadam-mark.svg` ← `dist/mark.svg` |
| soundadam.com favicon | `assets/logo/soundadam-mark-compact.svg` ← `dist/mark-compact.svg`; `assets/favicon.ico` / `icon-192.png` / `apple-touch-icon.png` from compact |
| [docs](https://github.com/soundadam/docs) (`docs.llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` / `soundadam-waveform-dark.svg` / `soundadam-mark.svg`; favicon `soundadam-mark-compact.svg` |
| cluster product hosts | [platform-gitops](https://github.com/soundadam/platform-gitops) `clusters/production/networking/brand-favicon/` ← compact ICO / PNG / SVG |

Copy again when the mark changes. Do not submodule this repo into WordPress
or Mintlify unless a product actually needs the whole tree.

Teaway’s Mintlify `docs/logo/{light,dark}.svg` is a product mark, not this
lockup.

## Rebuild SVG

`dist/*.svg` are the checked-in deliverable. `src/build_vector_logos.py`
recomposes them from `src/wordmark-trace.svg` (letterforms) plus the
nine-cell geometry. The waveform glyph is a Mexican-hat / Ricker wavelet sampled onto
the nine-cell (`waveform_points`), filled against the zero line.
Negative lobes are stretched so the brim cuts the bottom row; numpy is
optional at build time. The stroke cut lives in `dist/waveform-stroke/`.

```sh
python3 src/build_vector_logos.py
```

PNG rasters are not rebuilt by that script. After a geometry change
(needs `rsvg-convert` and `magick`):

```sh
for kind in waveform waveform-stroke equalizer; do
  for variant in on-light on-dark transparent-on-light transparent-on-dark; do
    rsvg-convert -w 1324 -h 280 "dist/$kind/$variant.svg" -o "dist/$kind/$variant.png"
  done
done
rsvg-convert -w 32 -h 32 dist/mark-compact.svg -o /tmp/mark-32.png
rsvg-convert -w 48 -h 48 dist/mark-compact.svg -o /tmp/mark-48.png
magick /tmp/mark-32.png /tmp/mark-48.png dist/favicon.ico
rsvg-convert -w 180 -h 180 dist/mark-compact.svg -o /tmp/mark-180.png
rsvg-convert -w 192 -h 192 dist/mark-compact.svg -o /tmp/mark-192.png
magick -size 180x180 xc:'#000000' /tmp/mark-180.png -composite dist/apple-touch-icon.png
magick -size 192x192 xc:'#000000' /tmp/mark-192.png -composite dist/icon-192.png
```
