# Animation Craft

Reusable craft knowledge for ManimGL educational videos: algebra-solving style, layout and animation gotchas, table construction, and highlighting rules.

> Treat these as preferred patterns, not universal APIs. Before reusing indexed `Tex` slices, inspect the actual token structure in the current scene.

## Algebra-solving style

- Show each operation explicitly. For example, write `+24` under both sides before combining. Use `ReplacementTransform` and `FadeOut` for combination or cancellation instead of jumping directly to the simplified result.
- Reserve fresh equals signs for genuinely new conclusions. For tidying or simplification, visually transform the existing expression, such as shrinking a fraction bar or morphing digits.
- When substituting known values into a symbolic formula, copy indexed pieces from existing `Tex` or `Text` mobjects into their destinations with `TransformFromCopy` or `ReplacementTransform`. This preserves visual traceability.
- Build a final substituted equation as one combined `Tex` object and choreograph its pieces by index. Do not construct it as a `VGroup` of independently created colored fragments unless the scene specifically requires that.
- For controlled equation-state changes, prefer explicit element-wise `ReplacementTransform` calls between inspected pieces of the old and new `Tex`. `TransformMatchingTex` may not produce the intended visual correspondence.
- Split `Tex` input into fine-grained arguments—for example, `"b", "^2"` and `"\\cos", "A"`—when bases, exponents, operators, or angle labels must animate independently.
- When substituting a diagram value, animate a copy of the actual diagram label into the equation. Reuse separate copies of the source label if the value appears in multiple destinations.
- When old pieces retire as new structural pieces appear, consider fading old pieces downward and new pieces upward to communicate replacement rather than a flat cross-fade.
- After a multi-piece transformation assembles a new `Tex` object, explicitly add the complete new object to the scene before later treating it as one coherent mobject.
- When `tex_to_color_map` cannot distinguish repeated strings with different meanings, apply colors by inspected index or slice after construction.

## Layout and animation

- `.animate.become()` does not reflow sibling mobjects in an arranged row. When short content becomes wider, manually correct its position.
- Revert temporary expanded labels to their original concise form once they have served their explanatory purpose.
- After long transformation sequences, explicitly identify survivors and objects to fade. Do not depend on an old tracking `VGroup` whose membership may no longer reflect the live scene.
- Read live mobject coordinates after transforms instead of reusing stale Python coordinate values.
- For a positional and structural line swap, an effective handoff is to move/replace the old line while making it transparent as the new line fades in. Remove the invisible leftover explicitly afterward.
- To return a final numeric answer to the diagram, move a copy of the value from the final equation beside the relevant diagram label instead of writing a disconnected answer sentence.

## Table style

- Use compact spacing: border buffer around 0.2 and tight header/column buffers.
- Center the header over the rows using vertical arrangement when that matches the scene; avoid unnecessary left-edge alignment.
- Prefer concise headers such as “No. of Pets”.
- If header text is wider than the data, calculate a column divider's x-position from the header cells.
- When extending a table, retain dividers and lines that do not need to move. Rebuild only the border and row lines whose extent changes.

## Highlighting

- In interleaved grids, show non-contiguous selections with separate per-row `SurroundingRectangle` objects. One bounding box across separated rows can enclose unrelated content.
- If an element already has an identity color, use a contrasting highlight-box color. Maintain separate identity and cross-highlight palettes when helpful.

## Scene layout conventions

- In median and cumulative-frequency GCSE scenes, place the primary frequency table on the right and the expanded list or working area on the left.
