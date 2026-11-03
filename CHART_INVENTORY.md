# Chart inventory

Updated 3 November 2026 after a first-view readability review: each chart must be understandable from what it shows before the caption is read or a tooltip is opened.

The site has **12 numbered charts** and **8 advanced idioms**, including three different map idioms. Basic idioms are classified using the unit's own definitions: the brief lists bar, stacked bar, grouped bar, dot plots, line, area, pie, scatter and bubble charts as basic, and Course Notes 4 (section 2.2.2) treats dumbbell and connected dot plots as dot plots.

| Chart | Question | Idiom | Classification |
|---|---|---|---|
| 01 | Which animal groups were handed over? | Waffle (100 squares, 1 square ≈ 1%) | Advanced 1 |
| 02 | Where were most animals handed over? | Proportional-symbol map | Advanced 2 (map) |
| 03 | How does the animal mix vary by state? | Choropleth with classed shares and a group selector | Advanced 3 (map) |
| 04 | How did each state's handovers change from 2021 to 2024? | Connected dot plot (two labelled endpoints per state) | Basic (dot plot) |
| 05 | When did animals arrive at NWRC? | Heatmap with published annual totals | Advanced 4 |
| 06 | What happened to the featured bears? | Event timeline: one row per bear, event types by shape and colour, outcome at the end of each row, enlarged view of a chosen bear | Advanced 5 |
| 07 | Where did NWRC release animals? | Flow map | Advanced 6 (map) |
| 08 | Which species went to each release area? | Sankey diagram | Advanced 7 |
| 09 | How did volunteers and interns change over time? | Multi-line chart | Basic |
| 10 | Where did volunteers come from? | Treemap (block area = placements) | Advanced 8 |
| 11 | When did placements start? | Stacked columns by month and origin | Basic (stacked bar) |
| 12 | How long did placements last? | Histogram, one column per day of stay | Basic |

The national-total bars beside chart 04 and the Sabah locator map are supporting context and are not counted. Selections, tooltips, pictograms and repeated panels do not create extra idioms.

## First-view design decisions

- **04** replaced a bump chart of ranks, which readers could not decode without the caption. Each row now shows the same state's 2021 and 2024 counts, with year shown by both colour and shape; Terengganu is highlighted.
- **06** groups the bears into "Released to the forest" and "Still in care". Each row ends with its outcome, and the three deaths are in bold so they can be counted at a glance. A collar death signal (×) is kept separate from remains recovered (cross). Events less than five weeks apart are stacked so their symbols do not overlap.
- **10** replaced a lollipop chart. The Malaysia block fills almost half the area, which is the chart's message; every block carries its country and count. The layout is calculated in `tools/2_chart_data.py` with the squarified treemap algorithm (Bruls et al., 2000), in the same way as the Sankey layout.
- **11** replaced a Gantt chart of individual placements, which readers did not recognise. Monthly starts are split by origin and every segment is labelled. These are starts, not the number of volunteers present in a month.
- **12** shows one column for each length of stay (11–39 days) rather than week-wide bins, so the fixed programme lengths are visible: 14 days (19 placements), 11 days (12) and 32 days (7). A shaded band marks stays of two weeks or less and states how many of the shown placements fall in it. A month menu or a click on a chart 11 column filters the histogram; All months restores the full year.
- **03** uses a deeper top class so the two darkest colours stay distinct for colour-blind readers; every state also prints its percentage.

## Verification

`npm run check` compiles all 13 specifications, validates the source totals, verifies the 24 state-comparison endpoints, the missing heatmap values, the nine treemap blocks (57 placements), the histogram peaks and every month's histogram against the original placement records. Browser review covers visible labels, menu and column selection, reset, and the 1280 and 1024 px laptop layouts with no sideways scrolling.
