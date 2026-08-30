# SoundAdam brand

Source of truth for the SoundAdam lockup. Products copy files from `dist/`;
they do not generate marks.

The live wordmark is the **waveform** lockup. The equalizer set is an unused
alternate kept here so it does not live only in scratch.

## Use this

| Surface | File |
| --- | --- |
| Light UI, transparent canvas | [`dist/waveform/transparent-on-light.svg`](dist/waveform/transparent-on-light.svg) |
| Dark UI, transparent canvas | [`dist/waveform/transparent-on-dark.svg`](dist/waveform/transparent-on-dark.svg) |
| App icon / favicon | [`dist/mark.svg`](dist/mark.svg) |

Opaque `on-light` / `on-dark` SVG and PNG sit next to those for slides or
places that cannot composite a transparent SVG. Prefer SVG.

Blue gradient: `#006fe8` → `#1386ff`. Wordmark on light: `#050505`. Wordmark
on dark: `#f7f9fb`. Canvas: 1280×280 (wordmark), 224×224 (mark).

## Already copied

| Product | Path in that repo |
| --- | --- |
| [soundadam.com](https://github.com/soundadam/soundadam.com) header and footer | `wp-content/themes/soundadam/assets/logo/soundadam-waveform.svg` ← `transparent-on-light.svg` |
| soundadam.com mark | `wp-content/themes/soundadam/assets/logo/soundadam-mark.svg` ← `dist/mark.svg` |
| [docs](https://github.com/soundadam/docs) (`llm.soundadam.com`) | `llm/logo/soundadam-waveform.svg` ← same wordmark |

Copy again when the mark changes. Do not submodule this repo into WordPress
or Mintlify unless a product actually needs the whole tree.

Teaway’s Mintlify `docs/logo/{light,dark}.svg` is a product mark, not this
lockup.

## Rebuild SVG

`dist/*.svg` are the checked-in deliverable. `src/build_vector_logos.py`
recomposes them from `src/wordmark-trace.svg` (letterforms) plus the
nine-cell geometry. PNG rasters are not rebuilt by that script.

```sh
python3 src/build_vector_logos.py
```
