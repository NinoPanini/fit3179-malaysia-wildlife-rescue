# tools: how the data and charts were made

These three Python scripts rebuild every file in `data/` (except `provenance.json`, which is written by hand) and every chart in `charts/`. The website itself does not need them: it only reads the JSON they produce.

## Run

Python 3.9 or newer, standard library only. Run from the website folder, in this order:

```
python tools/1_base_data.py
python tools/2_chart_data.py
python tools/3_chart_specs.py
npm run check
```

On Windows, use `py` in place of `python` if `python` is not found. Running the scripts again gives byte-identical files, so `git diff` after a run shows only what you changed.

| Step | Writes | What it does |
|---|---|---|
| `1_base_data.py` | 7 files in `data/` | PERHILITAN 2024 tables typed from the report (handovers by state, NWRC monthly intake, NWRC releases), the Peninsular state outlines and centre points, and the Sankey layout |
| `2_chart_data.py` | 14 files in `data/` | Adds PERHILITAN 2021–2023, the BSBCC bear events and volunteer figures, release-area positions, flow-map curves and the Sabah inset |
| `3_chart_specs.py` | 13 files in `charts/` | Writes each Vega-Lite spec as readable JSON with one shared font and palette |

Figures typed from a report sit in the scripts with their table and page number. Each typed table is checked with `assert` against its expected totals before anything is written, so a typing slip stops the script instead of reaching the page. Edit the scripts rather than the JSON, then run `npm run check`.

## Inputs (`tools/inputs/`)

| File | Contents | Source |
|---|---|---|
| `perhilitan_handovers_2021.csv` | Handovers by state and animal group, 2021 | PERHILITAN Laporan Tahunan 2021, Table 20, printed p80 |
| `bsbcc_selected_case_timeline.csv` | 23 dated events for nine bears | BSBCC Annual Reports 2021–2025 (page in each row) |
| `bsbcc_volunteers_interns_2021_2025.csv` | Volunteers and interns per year | BSBCC Annual Reports 2021–2025 |
| `bsbcc_volunteer_placements_2025.csv` | Start and end date of 57 placements, with country of origin | BSBCC Annual Report 2025, Appendix I, pp30–32 |
| `bsbcc_volunteer_origins_2025.csv` | Placements by country of origin | Same appendix, counted |
| `geoboundaries-MYS-ADM1-simplified.geojson` | Malaysian state boundaries | [geoBoundaries](https://www.geoboundaries.org/) MYS ADM1 (simplified), © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |

The placement files list no names, only dates and countries. Bear names are the animals' names as printed by BSBCC.

## The reports

The PDFs are large and stay with their publishers, so they are linked rather than copied here. Page numbers in the data refer to the printed page; where a PDF page is also given, it is the page in the copy linked below.

- PERHILITAN, Laporan Tahunan (Annual Report), all years: [library catalogue record](https://koha.wildlife.gov.my/cgi-bin/koha/opac-detail.pl?biblionumber=1449). Direct files: [2024](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=17de2df114c33ae95d20726b59c8bea6), [2023](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=7197e1fada4267a10d41dc857176c569), [2022](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=92d8a4367169dc9c2c52fc7189214b1a), [2021](https://koha.wildlife.gov.my/cgi-bin/koha/opac-retrieve-file.pl?id=72808791d6dcfdbf3102f842ddc26d53). The 2021 extract was made from the copy on PERHILITAN's website (link in the CSV).
- BSBCC Annual Reports: [2021](https://www.bsbcc.org.my/s/Annual-Report-2021.pdf), [2022](https://www.bsbcc.org.my/s/Annual-Report-2022.pdf), [2023](https://www.bsbcc.org.my/s/Annual-Report-2023_FINAL_compressed-3ebd.pdf), [2024](https://www.bsbcc.org.my/s/Annual-Report-2024_FINAL.pdf), [2025](https://www.bsbcc.org.my/s/Annual-Report-2025.pdf).

Release-area positions in `2_chart_data.py` were placed by hand from public maps and are approximate (within about 10–20 km). Report content remains the copyright of its publishers and is used with their permission.
