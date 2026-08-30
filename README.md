# soundadam brand

Source of truth for the soundadam lockup. Products copy files from `dist/`;
they do not generate marks.

The live wordmark is the **waveform** lockup. The equalizer set is an unused
alternate kept here so it does not live only in scratch.

## Use this

| Surface | File |
| --- | --- |
| Light UI, transparent canvas | [`dist/waveform/transparent-on-light.svg`](dist/waveform/transparent-on-light.svg) |
| Dark UI, transparent canvas | [`dist/waveform/transparent-on-dark.svg`](dist/waveform/transparent-on-dark.svg) |
| App icon / favicon (vector) | [`dist/mark.svg`](dist/mark.svg) |
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
into the grid — `soundadam` gets the acoustic waveform, `soundapi` gets a
signal relay (arrow – node – arrow), and so on. Same silhouette at a
glance, distinct icon up close.

`src/build_vector_logos.py` keeps this as an `ICONS` registry (name → glyph
function) plus a `FAMILY_ICON_ONLY` map of `slug -> icon kind`. To add a new
product mark:

1. Write a glyph function (see `relay_overlay` for a minimal example) and
   register it in `ICONS`.
2. Add `"your-slug": "your-icon"` to `FAMILY_ICON_ONLY`.
3. Run the build script — it writes `dist/your-slug/mark.svg`.

That only gets you the icon-only mark (grid + glyph, no text) — enough for
an avatar, favicon, or app icon. A full text lockup like soundadam's needs
its own traced wordmark (see "Rebuild SVG" below), since the wordmark is
hand-traced art, not live type; there's no font file behind it to retype.

| Product | Mark |
| --- | --- |
| soundadam | [`dist/mark.svg`](dist/mark.svg) — waveform |
| soundapi | [`dist/soundapi/mark.svg`](dist/soundapi/mark.svg) — signal relay |

## Already copied

| Product | Path in that repo |
| --- | --- |
| [soundadam.com](https://github.com/soundadam/soundadam.com) header and footer | `wp-content/themes/soundadam/assets/logo/soundadam-waveform.svg` ← `transparent-on-light.svg` |
| soundadam.com mark | `wp-content/themes/soundadam/assets/logo/soundadam-mark.svg` ← `dist/mark.svg` |
| [docs](https://github.com/soundadam/docs) (`llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` / `soundadam-waveform-dark.svg` / `soundadam-mark.svg` |

Copy again when the mark changes. Do not submodule this repo into WordPress
or Mintlify unless a product actually needs the whole tree.

Teaway’s Mintlify `docs/logo/{light,dark}.svg` is a product mark, not this
lockup.

## Rebuild SVG

`dist/*.svg` are the checked-in deliverable. `src/build_vector_logos.py`
recomposes them from `src/wordmark-trace.svg` (letterforms) plus the
nine-cell geometry. The waveform glyph is a unipolar pulse with two side ripples
(`waveform_points`) — a readable cut on the nine-cell, not a
bipolar hairline.

```sh
python3 src/build_vector_logos.py
```

PNG rasters are not rebuilt by that script. After a geometry change
(needs `rsvg-convert` and `magick`):

```sh
for kind in waveform equalizer; do
  for variant in on-light on-dark transparent-on-light transparent-on-dark; do
    rsvg-convert -w 1324 -h 280 "dist/$kind/$variant.svg" -o "dist/$kind/$variant.png"
  done
done
rsvg-convert -w 180 -h 180 dist/mark.svg -o dist/apple-touch-icon.png
rsvg-convert -w 192 -h 192 dist/mark.svg -o dist/icon-192.png
magick dist/mark.svg -background none -define icon:auto-resize=32,48 dist/favicon.ico
```
