# Workflow and Tools

Working procedure, validation expectations, and reference sources for these ManimGL repositories.

## Working pattern

- Development is iterative: Uzair reviews an output, may edit the code directly, uploads the current version, and work continues from that version.
- Respect the stated task boundary. Do not add scenes, narration beats, or broad rewrites that were not requested.
- Prefer concise, targeted edits over full-file rewrites.
- Treat the latest repository version as authoritative before making changes.

## Source authority

Use this order when researching or generating code:

1. The repository's root `MANIMGL_CONTEXT.md`.
2. Current project-specific status or overview notes.
3. Relevant craft notes.
4. The nearest working Python example in these repositories.
5. ManimGL **1.7.2** source for uncertain APIs.
6. Version-compatible examples from `3b1b/videos`.
7. General model knowledge only as a last resort.

Do not assume that an API from the newest upstream ManimGL source exists in the installed ManimGL 1.7.2 environment. Never introduce Manim Community Edition syntax unless explicitly requested.

## Validation levels

Report validation accurately and distinguish among:

- **Source-verified:** unfamiliar APIs checked against version-compatible ManimGL source.
- **Syntax-checked:** code passed `py_compile`.
- **Lint-reviewed:** `pyflakes` was run and its warnings were interpreted. Wildcard imports may produce misleading warnings.
- **Numerically verified:** standalone calculations checked relevant geometry or physics.
- **Render-tested:** the actual scene rendered successfully in a compatible ManimGL 1.7.2 environment.

Passing `py_compile` proves Python syntax only. It does not prove that ManimGL APIs, LaTeX token indices, assets, geometry, or rendering are correct.

Before producing geometry- or physics-heavy animation code, verify identities, numerical values, and frame-bound clearance with focused calculations where practical.

## Tools and references

- ManimGL 1.7.2 (`3b1b/manim`) as the framework target.
- `3b1b/videos` as a version-compatible production-pattern reference.
- `scipy.integrate.solve_ivp` where differential-equation-based physics animations require numerical integration.
- `xvfb-run` for headless rendering when available.
- `py_compile` for syntax checking.
- `pyflakes` for advisory static analysis.

Common repository conventions include `InteractiveScene`, `Tex`, `FadeIn`, `FadeOut`, `Write`, `ShowCreation`, and `LaggedStart`, but each use must remain compatible with ManimGL 1.7.2 and the existing scene.
