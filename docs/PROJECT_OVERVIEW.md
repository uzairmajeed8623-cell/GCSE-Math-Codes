# GCSE Mathematics Project Overview

> Project-specific status note. Update the “Current state” section whenever the active video or file changes.

## Purpose

- GCSE-level educational mathematics videos made with 3Blue1Brown ManimGL.
- Intended for publication on YouTube.
- Visual direction: a 3Blue1Brown-inspired style with a white exam-paper aesthetic.

## Visual conventions

- White exam-paper background with a `NumberPlane` grid.
- `Tex` is preferred over `MathTex`.
- `TransformFromCopy` is used to preserve visual traceability.
- Use `samples=4`; `samples=8` has produced an “invalid number of samples” ModernGL error in the current environment.
- Portrait Shorts configuration: `frame_config=dict(frame_shape=(4.5, 8.0))` and `resolution=(1080, 1920)` on `InteractiveScene`.
- Landscape format is generally used for longer explanations.

## Color palette

| Role | Color |
|---|---|
| Side a / primary geometry | Teal `#00B8A9` |
| Side b / gradient m | Purple `#7B2CBF` |
| Side c / unknown / point D | Orange `#FF6B00` |
| Angles / probability values | Dark red `#750A0A` |
| Correction terms / intercept c | Gold `#FFB800` |
| Boxed answers / OD | Blue `#0074FF` |
| OB | Green `#00C853` |
| Final-answer boxes / route highlights | Magenta `#FF3EA5` |
| Auxiliary lines such as DE | Red `#E63946` |

## Current state: cosine-rule video

Status captured from the supplied Claude project notes. Confirm against the current repository before continuing.

- Active file: `cosine_rule_intro.py`.
- The merged introduction contains five narrative beats: ancient geometric discovery, right triangle, Pythagoras squares, deformation into non-right triangles, and cosine-rule teaser.
- It includes a dynamic angle demonstration with a `ValueTracker` sweeping the triangle from 90° to 130°.
- It includes cosine-rule sign analysis for obtuse and acute angles with a live interior arc for angle C.
- The triangle remains visible between beats.
- For continuation of this specific video, edit only `cosine_rule_intro.py` unless Uzair explicitly expands the scope.

## Established technical notes

- Verify geometry numerically before integrating it into Manim code, including side lengths, angles, cosine-rule identities, and frame clearance.
- Stop `always_redraw` mobjects with `clear_updaters()` before `FadeOut` when updater activity would conflict with opacity animation.
- A previously tested static-to-dynamic triangle handoff used exact-object `self.remove()` and `self.add()` after numerical alignment. Revalidate this in any changed scene rather than assuming pixel identity.
- On white backgrounds, equations using `tex_to_color_map` may need `fill_color=BLACK` as the base so uncolored tokens such as equals and plus signs remain visible.
