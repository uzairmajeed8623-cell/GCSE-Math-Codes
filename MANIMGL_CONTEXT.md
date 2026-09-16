# ManimGL Coding Context

This file is the shared coding guide for both **GCSE-Math-Codes** and **Space-Explanatory-Codes**. It was derived from the Python files in both repositories on 2026-09-16.

Its purpose is to make future animation code compatible with the user's actual ManimGL environment and to prevent accidental use of Manim Community Edition (ManimCE) APIs.

## Confirmed local environment

- Package: `manimgl`
- Version: **1.7.2**
- Python package location: `C:\Users\Dell\AppData\Roaming\Python\Python312\site-packages`
- Editable source location: `D:\manim-master`
- Installation mode: editable project installation
- Python series indicated by the package path: 3.12

Because this is an editable installation, the source in `D:\manim-master` is the final authority for the APIs actually available on the user's computer. The package version is known, but the exact Git commit is not yet recorded.


## 1. Non-negotiable framework rule

This codebase uses **3Blue1Brown's ManimGL / `manimlib`**.

```python
from manimlib import *
```

Do not change this to:

```python
from manim import *
```

Do not introduce an API merely because it appears in ManimCE documentation or examples. If an API is not already proven in these repositories, verify it against the installed ManimGL source or the matching commit of `3b1b/manim` before using it.

## 2. Source-of-truth order

When generating or repairing code, use this priority:

1. Working code in the relevant repository.
2. The exact installed `manimlib` source/version in the user's environment.
3. The matching version or commit of `3b1b/manim`, plus relevant examples from `3b1b/videos`.
4. General model knowledge only for framework-independent Python, mathematics, and design reasoning.

Do not assume that current upstream ManimGL and the user's installed copy are identical. The installed package version is ManimGL 1.7.2; the exact Git commit is not yet recorded. If upstream source conflicts with the editable source in `D:\manim-master`, the local editable source wins.

## 3. Codebase snapshot

The repositories currently demonstrate:

- 16 scenes based on `InteractiveScene`
- 4 scenes based on `Scene`
- 1 scene based on `ThreeDScene`
- 2D GCSE explanations, tables, geometry, algebra, and portrait layouts
- script-timed cinematic geometry
- CSV-driven astronomical visualization
- textured 3D spheres, lighting, camera movement, and updaters

The normal scene shape is:

```python
from manimlib import *

class ExampleScene(InteractiveScene):
    def construct(self):
        ...
```

Use `InteractiveScene` as the default for new explanatory scenes unless a nearby working example gives a clear reason to use `Scene` or `ThreeDScene`.

## 4. APIs already proven in these repositories

### Core mobjects and grouping

`VGroup`, `Group`, `Text`, `Tex`, `Line`, `DashedLine`, `Dot`, `GlowDot`, `Circle`, `Arc`, `Polygon`, `Rectangle`, `RoundedRectangle`, `Square`, `Brace`, `Arrow`, `NumberPlane`, `SurroundingRectangle`, `VMobject`, `Sphere`, `Square3D`, `TexturedSurface`, and `Intersection`.

### Animations

`Write`, `ShowCreation`, `FadeIn`, `FadeOut`, `Transform`, `ReplacementTransform`, `TransformFromCopy`, `TransformMatchingTex`, `LaggedStart`, `AnimationGroup`, `GrowFromCenter`, `DrawBorderThenFill`, `Rotate`, `Homotopy`, `ApplyMethod`, and the `.animate` syntax.

### Layout and styling

`move_to`, `shift`, `next_to`, `arrange`, `arrange_in_grid`, `align_to`, `to_edge`, `to_corner`, `center`, `scale`, `rotate`, `set_color`, `set_fill`, `set_stroke`, `set_opacity`, `set_z_index`, `set_max_width`, and `set_max_height`.

### Dynamic systems

`ValueTracker`, `always_redraw`, `add_updater`, `remove_updater`, `clear_updaters`, `become`, `save_state`, and `Restore` are present in working project code.

Use updaters deliberately. Keep a reference to every updater-driven object, and clear or remove updaters before later manual transforms when necessary.

### Camera and 3D

The established camera pattern is:

```python
frame = self.frame
frame.reorient(...)
frame.set_field_of_view(...)
frame.set_height(...)
self.play(frame.animate.move_to(...).set_height(...))
```

3D examples also use `self.camera.light_source`, `TexturedSurface(Sphere(...), ...)`, `set_shading`, `fix_in_frame`, and object rotation through updaters.

## 5. Text and mathematics

- Use `Text` for prose, ordinary labels, question text, and numerals that do not need LaTeX.
- Use `Tex` for equations and mathematical notation.
- Prefer raw strings for LaTeX: `Tex(r"c^2=a^2+b^2")`.
- The codebase relies on submobject indexing and slicing for targeted animation. Verify indices visually after changing any text.
- Prefer `TransformMatchingTex` when two equations have genuinely matching LaTeX parts.
- Use `ReplacementTransform` or `TransformFromCopy` when the visual meaning is object continuity or derivation from an earlier object.
- Reuse established fonts and palettes from the nearest project. GCSE exam-style scenes commonly use black ink on white with `Times New Roman`; cinematic and astronomy scenes use dark backgrounds and brighter accents.

Do not substitute unverified ManimCE classes such as `MathTex` for the established `Tex` pattern.

## 6. Layout and object continuity

Use ManimGL geometry methods instead of scattering unrelated numeric coordinates:

- Build related objects as a `VGroup`.
- Use `arrange`, `next_to`, `align_to`, `get_center`, `get_left`, `get_right`, `get_top`, and `get_bottom`.
- Use `FRAME_WIDTH` and `FRAME_HEIGHT` for responsive framing.
- After a group has been scaled or moved, derive later geometry from its current on-screen points rather than stale pre-layout coordinates.
- When question and solution clips must align, put shared construction and layout logic in a helper module, following `Sector/sector_common.py`.
- Return named components from helpers with a dictionary or `SimpleNamespace` when later animations need individual pieces.
- Preserve the user's existing scene and object structure when making a local repair. Do not rewrite an entire working scene for a small change.

For scene-to-scene continuity, reconstruct the final state deterministically from shared constants/helpers. Python variables do not pass automatically between separately rendered scene classes.

## 7. Animation and narration style

The project is script-led. Organize longer scenes into commented narration beats and make visual actions correspond to the spoken sentence.

Common pacing patterns are:

```python
self.play(Write(label))
self.wait()
self.play(ShowCreation(highlight))
self.play(LaggedStart(*animations, lag_ratio=0.2))
```

Prefer a meaningful transform over fading everything out and rebuilding it. Use highlights, color identity, and `TransformFromCopy` to show where a result came from.

For explicit voice-over timing, keep timing comments near the animation block, as in `Cosine Rule/cosine_rule.py`. Treat those timings as scene-specific rather than universal defaults.

## 8. Repository-specific visual profiles

### GCSE-Math-Codes

- Usually a white/exam-paper or faint-grid presentation.
- `NumberPlane` often uses grey lines with low opacity.
- Main content is usually dark, with a small set of semantic accent colors.
- Tables are manually built from `VGroup`, `Line`, `Rectangle`, and `SurroundingRectangle`.
- Many explanations reveal one reasoning step at a time.
- Portrait question/solution pairs should share builders and layout constants.

The cosine-rule introduction is an intentional exception: it begins with a dark cinematic style, uses warm ancient-ink colors, follows voice-over beats, and later transitions to a white background.

### Space-Explanatory-Codes

- Usually a dark background.
- Uses scientific data, NumPy arrays, and sometimes pandas.
- Uses camera framing, lighting, textured spheres, glows, and updaters.
- Keep numerical units explicit and separate physical values from display scaling.
- For data-driven scenes, validate required columns and file paths before building mobjects.

## 9. Assets and data

Existing files contain machine-specific paths such as `D:\manim-master\Media\...` and `/manim-master/Media/...`. Do not copy those paths into new scenes.

For new work:

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSET_DIR = HERE / "assets"
image_path = ASSET_DIR / "example.png"
```

- Keep images, textures, SVGs, and CSVs inside the relevant project folder when possible.
- Check that every asset exists before rendering.
- State any required filenames when delivering code.
- Import external dependencies such as NumPy and pandas explicitly. Do not rely on `from manimlib import *` to expose unrelated names.

## 10. ManimCE contamination guardrail

Treat the following as unverified unless the installed ManimGL source proves otherwise:

| Familiar ManimCE pattern | Established pattern here |
|---|---|
| `from manim import *` | `from manimlib import *` |
| `Create(mobject)` | `ShowCreation(mobject)` |
| `MathTex(...)` | `Tex(...)` |
| global `config.frame_width` | `FRAME_WIDTH` / `FRAME_HEIGHT` |
| ManimCE camera helpers copied from tutorials | `self.frame`, `frame.reorient`, and `frame.animate` |
| guessing a class or keyword from ManimCE docs | verify it in the installed `manimlib` source |

This table does not claim that every left-column name is impossible in every ManimGL version. It means the name is not part of the proven vocabulary of these repositories and must not be guessed.

## 11. Known hazards found during inspection

Do not reproduce these patterns in new code:

1. **Duplicate method definitions:** `PhasesOfTheMoon` currently contains two `construct()` methods. Python keeps only the second one.
2. **Hard-coded absolute paths:** several texture/image paths are tied to one machine.
3. **Wildcard-import side effects:** some files use names such as `np` or `Path` without explicit imports.
4. **Unused imports:** a few files import unrelated names such as `turtle.pos` or `email.header`.
5. **Commit not recorded:** the package is confirmed as ManimGL 1.7.2, but local editable changes or a different source commit may still differ from current upstream ManimGL.
6. **Fragile text indices:** `Tex` and `Text` slices can change when the source string changes.
7. **Updater conflicts:** moving an object manually while an updater still controls it can produce surprising results.

When repairing old code, change only what is necessary unless the user explicitly requests cleanup.

## 12. Required workflow for new code

Before writing a substantial scene:

1. Identify the target repository, aspect ratio, visual profile, narration, and desired final state.
2. Search the relevant repository for the nearest working example.
3. Reuse existing helpers, palettes, fonts, and construction patterns.
4. List every ManimGL API the proposed design needs.
5. Verify any unproven API against the exact installed `manimlib` source or matching upstream commit.
6. Write a complete scene with explicit imports and asset requirements.
7. Run a Python syntax check.
8. Render a short or low-quality test of the exact scene.
9. Inspect the first frame, major transitions, final frame, text clipping, z-order, and updater cleanup.
10. Only call the code “render-ready” after the actual render succeeds.

If the environment cannot be rendered, say so clearly and distinguish “source-verified” from “render-tested.”

## 13. Delivery checklist

Every future code response should state:

- target file and scene class
- whether it modifies or replaces existing code
- required assets/data
- render command
- APIs verified from repository/source
- whether syntax checking and rendering were actually performed
- any remaining uncertainty

Suggested render form:

```bash
manimgl path/to/file.py SceneClass
```

Add the user's normal write/export flags only after checking the installed CLI.

## 14. Request template for future scenes

A useful prompt is:

> Use `MANIMGL_CONTEXT.md`. First inspect the closest working scenes in this repository. Animate the following narration in ManimGL, not ManimCE. Reuse my established visual style and helpers. Verify every unfamiliar API against ManimGL source, preserve continuity between beats, and tell me whether the final scene was syntax-checked and render-tested.

## 15. Maintaining this guide

Update this file when:

- the ManimGL installation is upgraded or pinned to a commit;
- a new helper module becomes a project standard;
- a new API is confirmed by a successful render;
- the preferred aspect ratio, typography, or color system changes; or
- a recurring failure reveals another ManimCE/ManimGL incompatibility.
