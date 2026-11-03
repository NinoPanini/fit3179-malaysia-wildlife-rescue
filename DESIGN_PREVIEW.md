# Editorial design preview

Branch: `codex/editorial-design-preview`

Baseline: `main` at `c472026531e97c472a157ae62c0e596dad6cb106`.

This branch changes the page presentation only. It has not been merged or pushed.

## Changes

- Chapter navigation appears above the opening and stays visible while reading. Its active marker follows chapter starts in either scroll direction.
- The opening is more compact, with aligned headline figures and a clearer Begin the story button.
- Desktop chapter headings and introductions share a two-column grid. Narrow screens retain a single reading column.
- Spacing, rules, controls and expandable tables use consistent sizing. Full-width section backgrounds no longer cause sideways page scrolling.
- The existing colours, locally hosted fonts, chart specifications, data, wording and twelve numbered visualisations are retained.

## Course material applied

FIT2179 Course Notes 9, Layout: alignment, sight-lines, consistent grids, whitespace and a clear viewing order.

FIT2179 Course Notes 6, Data-ink Ratio and Chartjunk: keep the visualisations prominent and avoid decorative imagery, textures, animation or extra panels.

Typography principles: a consistent type hierarchy, readable text measures and sufficient spacing. The page also retains keyboard focus indicators and now respects reduced-motion preferences for smooth scrolling.

The Sites plugin's presentation-led design guidance informed the layout. Browser checks used the Computer Use plugin. No new hosting service or runtime dependency was added.

## Validation

- `npm run check`: all 12 specifications render; report totals, state joins and placement checks pass.
- Browser: all 12 chart containers rendered SVGs; no console warnings or errors observed.
- Checked layouts at 1366, 1024 and 390 px viewport widths; fixed the section-background overflow.
- Checked forward/backward chapter navigation, the volunteer month selection and the 57-row expandable table.
- All original HTML text is preserved; only the navigation's position changed.
- `charts`, `data`, `assets`, `vendor` and `tools` are unchanged from the baseline.

This is a presentation preview, not a new rubric or data audit. Large charts retain their existing horizontal-scroll behaviour on small screens.

## Compare locally

The comparison bundle is outside the repository, at:

`../outputs/editorial-design-comparison/`

It contains frozen copies of the baseline and completed draft, screenshots and a local comparison server. Read its README for restart instructions. No submission files or GitHub Pages settings were changed.
