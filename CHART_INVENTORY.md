# Chart inventory

Updated 3 November 2026 after a first-view readability review: each chart must be understandable from what it shows before the caption is read or a tooltip is opened.

The site has **12 numbered charts** and **9 advanced idioms**, including three different map idioms (brief v1.2 confirms that all map idioms count as advanced). Basic idioms are classified using the unit's own definitions: the brief lists bar, stacked bar, grouped bar, dot plots, line, area, pie, scatter and bubble charts as basic, and Course Notes 4 (section 2.2.2) treats dumbbell and connected dot plots as dot plots.

| Chart | Question | Idiom | Classification |
|---|---|---|---|
| 01 | Which animal groups were handed over? | Waffle (100 squares, 1 square ≈ 1%) | Advanced 1 |
| 02 | Where were most animals handed over? | Proportional-symbol map | Advanced 2 (map) |
| 03 | Where are handovers concentrated for the land area, and how does the mix vary? | Choropleth: animals per 1,000 km² by default; a menu switches to one group's share of each state's handovers | Advanced 3 (map) |
| 04 | How did each state's handovers change from 2021 to 2024? | Bar chart of the change, sorted, rises right and falls left | Basic (bar) |
| 05 | When in the year does each animal group arrive at NWRC? | Heatmap: each cell is the month's share of that row's year total, with the published totals beside it | Advanced 4 |
| 06 | What happened to the featured bears? | Event timeline: one row per bear, event types by shape and colour, outcome at the end of each row, enlarged view of a chosen bear | Advanced 5 |
| 07 | Where did NWRC release animals? | Flow map | Advanced 6 (map) |
| 08 | Which species went to each release area? | Sankey diagram | Advanced 7 |
| 09 | How did volunteers and interns change over time? | Multi-line chart | Basic |
| 10 | Where did volunteers come from? | Treemap (block area = placements) | Advanced 8 |
| 11 | When did placements start? | Stacked columns by month and origin | Basic (stacked bar) |
| 12 | How long did placements last, and who stayed how long? | Isotype: one person figure per placement, one row per length of stay, Malaysia first | Advanced 9 |

The Sabah locator map is supporting context and is not counted. Selections, tooltips, pictograms and repeated panels do not create extra idioms.

## First-view design decisions

- **04** replaced a bump chart of ranks, then a connected dot plot; both needed the legend to tell which end was which year. It now shows the change itself: one bar per state, sorted from the biggest rise to the biggest fall, with rises to the right of zero and falls to the left, each labelled with the change and both counts (for example +1,753, from 264 to 2,017). This gives the chart its own story, since map 02 already shows the 2024 totals. The national totals for 2021–2024 moved from a separate mini chart into the subtitle.
- **06** groups the bears into "Released to the forest" and "Still in care". Each row ends with its outcome, and the three deaths are in bold so they can be counted at a glance. A collar death signal (×) is kept separate from remains recovered (cross). Events less than five weeks apart are stacked so their symbols do not overlap.
- **10** replaced a lollipop chart. The Malaysia block fills almost half the area, which is the chart's message; every block carries its country and count. The layout is calculated in `tools/2_chart_data.py` with the squarified treemap algorithm (Bruls et al., 2000), in the same way as the Sankey layout.
- **11** replaced a Gantt chart of individual placements, which readers did not recognise. Monthly starts are split by origin and every segment is labelled. These are starts, not the number of volunteers present in a month.
- **05** previously coloured raw counts on one scale. The rows differ in size by about 150 times (75 mammals against 10,968 reptiles in 2024), so the colours mainly repeated chart 01's message that reptiles dominate, and two months hid everything else. Each row is now normalised to its own published year total, and the cell prints the same percentage that sets its colour. The rows now show timing: reptiles arrive in one or two waves (58% in August 2023; 46% in September and 48% in December 2024), while no month brings in 20% of a year's mammals. A ridgeline of the same shares was considered; it shows the wave shapes, but it reads as an area chart, smooths between months, and makes zero and the missing December 2023 harder to see.
- **12** went through week-wide histogram bins, a one-column-per-day histogram, a four-column bar chart and a stacked-dot unit chart; each either hid the pattern or needed the caption to decode. It is now an isotype: every placement is one person figure, in a row for each plain-language length of stay (under 2 weeks, exactly 2 weeks, 2 to 4 weeks, over 4 weeks, with the days under each label) and the count at the end of the row. Within each row, volunteers from Malaysia come first, then a gap, then other countries, so origin is shown by position as well as colour. At a glance: 38 of 57 stayed two weeks or less, most Malaysians came for exactly two weeks, and most volunteers from other countries stayed under two weeks or over four. Choosing a month keeps the other figures as outlines in the same colour, and outlines the chosen column in chart 11; nothing fades, so the charts only ever use the two origin colours. The isotype is used only here, so chart 09 stays a line chart.
- **03** opens on all animals, normalised by land area (animals per 1,000 km², with each state's area measured from the boundary file in `tools/1_base_data.py`), so the first view needs no choice and does not repeat map 02's counts: the Federal Territories and Pulau Pinang hand over roughly 150 times as many animals per km² as Pahang. The menu (All animals, Reptiles, Mammals, Birds) switches to one group's share of each state's handovers, matching the "All …" defaults of charts 08 and 11–12. The Federal Territories are reported as one figure, so Kuala Lumpur, Putrajaya and Labuan are treated as one unit, coloured on Kuala Lumpur and Putrajaya, with their combined area as the denominator. A deeper top class keeps the two darkest colours distinct for colour-blind readers, and every state prints its value.
- **02** joins every circle to its label with a leader line, and draws Selangor's circle slightly north-west of the state centre so it no longer covers the Federal Territories circle.

## Verification

`npm run check` compiles all 12 specifications, validates the source totals, verifies the 12 change bars in chart 04, the missing heatmap values, the reptile shares in chart 05, the nine treemap blocks (57 placements), the 57 figures and four row counts in chart 12, and every month's highlighted placements against the original placement records. Browser review covers visible labels, menu and column selection, reset, and the 1280 and 1024 px laptop layouts with no sideways scrolling.
