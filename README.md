# Wildlife care in Malaysia

A data visualisation story about wildlife rescue in Malaysia: animals handed over to PERHILITAN, the National Wildlife Rescue Centre's intake and releases, nine sun bears at BSBCC, and the volunteers who help. Built with [Vega-Lite](https://vega.github.io/vega-lite/) for FIT3179 Data Visualisation 2 (Monash University, 2026) by Kenneth Gomes.

## Open it

The page is published with GitHub Pages from the root of this repository. To run it locally, use `npm start` in this folder and open **http://127.0.0.1:8000/** (Ctrl+C stops the server). Opening `index.html` directly does not work, because browsers block chart data from loading over `file://`.

The site is static: no build step, database or API key. The Vega libraries and fonts are stored in the repository, so charts do not depend on a CDN.

## Folders

| Location | Purpose |
|---|---|
| index.html | Story, captions and sources |
| css/styles.css | Layout, colours and typography (Fraunces and Source Sans 3) |
| js/app.js | Loads each chart with vega-embed (after the fonts), fits wide charts to the column, links charts 07 and 08, and builds the accessible tables |
| charts/ | 13 Vega-Lite specs: files 01–11 (file 11 holds the linked Gantt chart and histogram, charts 11–12) and two context charts |
| data/ | Small JSON extracts from the reports, map geometry, and `provenance.json` (sources, pages and caveats) |
| tools/ | The Python scripts that write `data/` and `charts/`, with their inputs. See [tools/README.md](tools/README.md) |
| scripts/ | Local server (`npm start`), chart checks (`npm run check`) and the library copier (`npm run vendor`) |
| vendor/ | Pinned Vega 5.33, Vega-Lite 5.23 and vega-embed 6.29, with their licences |
| assets/fonts/ | Self-hosted font subsets with their OFL licences |

## Charts

01 waffle · 02 proportional-symbol map · 03 choropleth with a group selector · 04 bump chart · 05 heatmap with total bars · 06 bear timeline (connected dot plot) · 07 flow map · 08 Sankey (linked to 07) · 09 line chart · 10 lollipop · 11 Gantt chart brushing 12 histogram.

## Checks

`npm run check` compiles and runs every chart in Node, then checks report totals, the map joins, the Sankey ribbons, the histogram counts and the figures quoted in the page text. Run it after changing a script or spec.

## Sources and credit

Data come from PERHILITAN's and BSBCC's annual reports, used with their permission. The page and `data/provenance.json` give the table and page for every figure, and [tools/README.md](tools/README.md) links each report. No animal GPS data is used.

Embedding, layered maps, lookup joins and bound controls follow the [FIT3179 Vega-Lite examples](https://github.com/FIT3179/Vega-Lite). State boundaries: [geoBoundaries](https://www.geoboundaries.org/), © OpenStreetMap contributors; the adapted files in `data/` are available under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/). Report content remains the copyright of its publishers.
