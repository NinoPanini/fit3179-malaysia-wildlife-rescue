# Data and specification pipeline

These three Python scripts produce every file in `data/` (except `provenance.json`, which is maintained by hand) and every specification in `charts/`. The site itself does not run them; it reads only the JSON they produce.

## Usage

Python 3.9 or newer, standard library only. Run from the website folder, in this order:

```
python tools/1_base_data.py
python tools/2_chart_data.py
python tools/3_chart_specs.py
npm run check
```

On Windows, use `py` in place of `python` if `python` is not found. The output is deterministic: rerunning the scripts produces byte-identical files, so `git diff` shows only intended changes.

| Step | Writes | What it does |
|---|---|---|
| `1_base_data.py` | 7 files in `data/` | PERHILITAN 2024 tables transcribed from the report (handovers by state, National Wildlife Rescue Centre monthly intake and releases), Peninsular state outlines, centre points and land areas (for the choropleth's animals per 1,000 km²), and the Sankey layout |
| `2_chart_data.py` | 15 files in `data/` | PERHILITAN 2021–2023 figures, BSBCC sun bear events and volunteer figures, the volunteer-origin treemap layout, release-area positions, flow-map curves and the Sabah inset |
| `3_chart_specs.py` | 12 files in `charts/` | Each Vega-Lite specification as readable JSON, sharing one configuration for typography and colour |

Figures transcribed from a report appear in the scripts with their table and page number. Each transcribed table is checked with `assert` against its expected totals before anything is written, so a transcription error stops the script before it reaches the site. Make changes in the scripts rather than the JSON, then run `npm run check`.

## Inputs (`tools/inputs/`)

| File | Contents | Source |
|---|---|---|
| `perhilitan_handovers_2021.csv` | Handovers by state and animal group, 2021 | Department of Wildlife and National Parks Peninsular Malaysia (PERHILITAN), *Laporan Tahunan / Annual Report 2021*, Table 20, printed p. 80 |
| `bsbcc_selected_case_timeline.csv` | 23 dated events for nine sun bears | Bornean Sun Bear Conservation Centre (BSBCC), *Annual Report* 2021–2025 (page given in each row) |
| `bsbcc_volunteers_interns_2021_2025.csv` | Volunteers and interns per year | Bornean Sun Bear Conservation Centre (BSBCC), *Annual Report* 2021–2025 |
| `bsbcc_volunteer_placements_2025.csv` | Start and end dates of 57 placements, with country of origin | Bornean Sun Bear Conservation Centre (BSBCC), *Annual Report 2025*, Appendix I, pp. 30–32 |
| `bsbcc_volunteer_origins_2025.csv` | Placements by country of origin | Counted from the same appendix |
| `geoboundaries-MYS-ADM1-simplified.geojson` | Malaysian state boundaries | [geoBoundaries Global Database of Political Administrative Boundaries](https://www.geoboundaries.org/), Malaysia ADM1 (simplified), © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |

The placement files contain no personal names, only dates and countries. Bear names are those given to the animals by BSBCC.

## Source reports

The reports are linked rather than copied into the repository. Page numbers in the data refer to the printed page; where a PDF page is also given, it refers to the copy linked below.

- Department of Wildlife and National Parks Peninsular Malaysia (PERHILITAN), *Laporan Tahunan / Annual Report*, all editions: [library catalogue record](https://koha.wildlife.gov.my/cgi-bin/koha/opac-detail.pl?biblionumber=1449). Direct files: [2024](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=17de2df114c33ae95d20726b59c8bea6), [2023](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=7197e1fada4267a10d41dc857176c569), [2022](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=92d8a4367169dc9c2c52fc7189214b1a), [2021](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=72808791d6dcfdbf3102f842ddc26d53). The 2021 extract was made from the copy published on PERHILITAN's website (linked in the CSV).
- Bornean Sun Bear Conservation Centre (BSBCC), *Annual Report*: [2021](https://www.bsbcc.org.my/s/Annual-Report-2021.pdf), [2022](https://www.bsbcc.org.my/s/Annual-Report-2022.pdf), [2023](https://www.bsbcc.org.my/s/Annual-Report-2023_FINAL_compressed-3ebd.pdf), [2024](https://www.bsbcc.org.my/s/Annual-Report-2024_FINAL.pdf), [2025](https://www.bsbcc.org.my/s/Annual-Report-2025.pdf).

Release-area positions in `2_chart_data.py` were placed manually from public maps and are approximate (within about 10–20 km). Report content remains the copyright of its publishers and is used with their permission.
