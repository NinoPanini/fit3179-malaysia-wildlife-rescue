# Wildlife care in Malaysia

A working local Vega-Lite website. Updated 17 October 2026.

Resource audit, 24 October 2026: the permitted data window is January 2021–July 2026. Wildlife tables meet it. The existing 2017 boundary geometry and its derived anchors do not: replace those resources before publication. Passing chart execution checks does not establish date or reuse approval. See `../outputs/RESOURCE_REVIEW.txt` and `data/provenance.json`.

## Open it

Run `npm start` in this folder, then open **http://127.0.0.1:8000/**.
Leave the terminal running while viewing. Ctrl+C stops the server.
Node.js is already installed on this computer. On another computer, install Node.js first.

The site is static: no database, account, API key or build step. All chart libraries and selected data are local, so charts do not depend on a CDN. Do not open index.html directly; use the local server.

## Where to edit

| Location | Purpose |
|---|---|
| index.html | Story, captions and source references |
| css/styles.css | Layout, colours and typography |
| js/app.js | Chart loading, resizing and accessible tables |
| charts/ | Nine readable Vega-Lite JSON specifications |
| data/ | Selected 2024–2025 report extracts, map geometry and provenance |
| vendor/ | Pinned Vega libraries with their original licences |
| scripts/ | Local server, checks and library-copy helper |

Original PDFs, workbooks and research stay in the parent assignment folder. The website is the only DV2 Git repository. node_modules is ignored; do not put original reports or private permission correspondence here.

## Development checks

Dependencies are pinned in package.json and package-lock.json. Use `npm ci --ignore-scripts` only when restoring development packages on another machine. Run `npm run check` to compile and execute all charts and verify report totals, geographic joins, ribbons and histogram counts. Run `npm run vendor` only after deliberately updating a library version.

Nine charts are implemented, including three map idioms. This is a first build, not a finished submission: the plan still needs two further suitable charts to reach more than ten. The scatterplot and treemap remain candidates pending final extraction and review. AI image drafts are not the current website or the required hand-drawn sketch.

## Sources and code credit

The page and data/provenance.json record data sources and caveats. Read them before changing denominators or combining records. NWRC table values are used where Figure 26 bar labels disagree. No animal GPS dataset is included.

Chart embedding, layered maps, lookup joins and bound controls follow the [FIT3179 teaching examples](https://github.com/FIT3179/Vega-Lite), especially 2_symbol_map, 3_choropleth_map, 5_multiple_charts_html and 6_advanced_examples. Local teaching copies are in ../research/course_review_oct11/unit_examples. This is an original page implementation using those patterns, not a wholesale copy of the course site.

The adapted boundary database in data/peninsular-states.geojson is offered under ODbL 1.0, with geoBoundaries and OpenStreetMap attribution in the page. Report copyright remains with the respective owners; no blanket licence is claimed for all project data.

## GitHub later

No GitHub repository or remote is configured. Once the final page is ready, connect this folder to the user's DV2 repository and enable GitHub Pages from main / root. No bundling is required. Preserve .nojekyll, vendor licences and data attribution.
