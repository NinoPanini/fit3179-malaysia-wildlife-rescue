# Chart inventory

Updated 3 November 2026 after feedback on first-glance readability.

There are **12 numbered charts and eight distinct advanced idioms**, including three different map idioms. This meets the brief's numerical HD target of more than ten charts and at least eight advanced idioms. Quality, appropriateness, storytelling and the other rubric criteria still determine the mark.

| Chart | Question | Idiom | Advanced family counted |
|---|---|---|---|
| 01 | Which animal groups were handed over? | Waffle | 1: Waffle |
| 02 | Where were most animals handed over? | Proportional-symbol map | 2: Proportional-symbol map |
| 03 | How does the animal mix vary by state? | Choropleth | 3: Choropleth |
| 04 | How did each state's handover count change from 2021 to 2024? | Connected-dot comparison | 4: Connected dot plot |
| 05 | When did animals arrive at NWRC? | Heatmap, paired years, numeric annual totals | 5: Heatmap |
| 06 | What happened to the featured bears? | Connected event timelines with selected-bear detail | Same family as 04; no additional count |
| 07 | Where did NWRC release animals? | Flow map | 6: Flow map |
| 08 | Which species went to each release area? | Sankey | 7: Sankey |
| 09 | How did volunteers and interns change over time? | Multi-line chart | Basic |
| 10 | Where did volunteers come from? | Lollipop | 8: Lollipop |
| 11 | When did placements start? | Monthly stacked columns | Basic |
| 12 | How long did placements last? | Histogram | Conservatively not counted as advanced |

The national-total bars and Sabah locator are supporting context and do not increase these counts. The two charts in specification 11 are separate analytical views: starts by calendar month and a distribution of stay lengths. Selections, tooltips, pictograms, text columns and repeated panels do not create extra idioms.

## Changes after feedback

- Chart 04 replaces crossing rank lines with one row per state and two labelled count endpoints. Year has both a colour and a shape. Terengganu is highlighted by a background band.
- Chart 05 places 2023 beside 2024 within each animal group. Pictograms supplement group names. Monthly counts and published annual totals are visible; the shared colour scale preserves the size of the reptile spikes. Unavailable December 2023 cells remain separate from zero.
- Chart 11 replaces the individual placement timeline with monthly starts. Segment counts and monthly totals are printed. These are starts, not the number of volunteers present throughout a month.
- Chart 12 prints every bin count, including zero after filtering. A month menu and clickable columns filter the histogram; selecting All months restores the full distribution. The three summary figures above the pair always describe the full year.

## Implementation and verification

The existing Vega-Lite 5 renderer is retained. The generators in `tools/` remain the source of the chart JSON. No report observations or permissions changed.

`npm run check` compiles all 13 specifications, validates the source totals, verifies 24 state-comparison endpoints and missing heatmap values, and tests every month against the original placement records. Browser review checks visible labels, menu and column selection, reset, and narrow-screen layout. On narrow screens the monthly chart and histogram stack vertically; wider data matrices can scroll without reducing their text to unreadable sizes.
