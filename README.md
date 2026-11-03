# A Second Chance: Wildlife Rescue and Rehabilitation in Malaysia

An interactive data visualisation study of how wild animals move through rescue and rehabilitation in Malaysia, from handover to release, based on published records from the Department of Wildlife and National Parks Peninsular Malaysia and the Bornean Sun Bear Conservation Centre for 2021–2025.

**Live site:** https://ninopanini.github.io/fit3179-malaysia-wildlife-rescue/

**Author:** Kenneth Gomes, Monash University (2026)

## Research questions

The study uses separate public records to explain four parts of wildlife care. Each section addresses one question:

1. **Intake.** Which animals are handed over to the wildlife authorities, and in which states?
2. **Recovery.** What happens while animals are in care?
3. **Return.** Where are rehabilitated animals released?
4. **People.** Who gives their time to support this work?

The site presents twelve visualisations built with Vega-Lite. They include a waffle chart, three map idioms (proportional symbols, a choropleth and a flow map), a chart of how each state's handovers changed from 2021 to 2024, a heatmap of when each animal group arrives at the rescue centre, a tree of what happened to the featured sun bears, a Sankey diagram, a treemap of volunteer origins, and monthly volunteer-start columns linked to an isotype of how long each placement lasted. Main counts are visible without hovering. See the [chart inventory](CHART_INVENTORY.md) for the classification and purpose of each view.

## Data sources

| Source | Records used | Period |
|---|---|---|
| Department of Wildlife and National Parks Peninsular Malaysia (Jabatan Perlindungan Hidupan Liar dan Taman Negara Semenanjung Malaysia, PERHILITAN), *Laporan Tahunan / Annual Report* | Animals handed over, by state and animal group. National Wildlife Rescue Centre (NWRC), Sungkai: monthly intake and releases by destination | 2021–2024 |
| Bornean Sun Bear Conservation Centre (BSBCC), Sepilok, Sabah, *Annual Report* | Dated rescue, release and outcome events for nine sun bears. Volunteer and intern numbers. 2025 volunteer placement dates and countries of origin | 2021–2025 |
| Brunton et al. (2025), *Wildlife Biology* | Outcomes of sun bears released in 2021–2023 | 2021–2023 |
| geoBoundaries Global Database of Political Administrative Boundaries, Malaysia ADM1 | State boundaries used as a reference map | 2017 boundaries |

The PERHILITAN and BSBCC reports are used with the permission of each organisation. Two guidelines inform the background text but supply no data: the NWRC sun bear management guideline (Izzat-Husna et al., 2022) and the IUCN guidelines on translocating displaced organisms (Sherman et al., 2025). Every figure on the site is traceable to a table and printed page, listed in [`data/provenance.json`](data/provenance.json) and in [`tools/README.md`](tools/README.md).

## Method

**Extraction.** Figures were transcribed from the published tables and checked against the original pages. Each transcribed table is checked against its printed or derived totals before any output is written.

**Processing.** Three Python scripts in [`tools/`](tools/) turn the extracts into JSON data files and Vega-Lite specifications. The pipeline is deterministic: a fresh clone regenerates the committed data and specifications byte for byte.

**Encoding.** Choropleth values are rates rather than raw counts: animals per 1,000 km² of land (area measured from the boundary file), or one group's share of each state's handovers. Records from different sources are shown side by side and never combined into rates.

**Accessibility.** Categories use the Okabe–Ito palette and amounts use ColorBrewer YlGnBu. Every colour distinction is repeated with labels, shapes or line styles. The main datasets can also be opened as data tables, for keyboard and screen-reader users.

**Validation.** `npm run check` compiles and runs every chart. It confirms report totals, geographic joins, Sankey flows, treemap blocks, the placement figures and the key figures quoted in the text.

## Limitations

- Handovers are records of contact with the authorities. They do not estimate wild populations or measure how well a state protects wildlife.
- PERHILITAN's 2022 report gives only a national total. The state comparison uses the 2021 and 2024 endpoints, and its subtitle gives the national totals, including the 2022 dip. In the 2023 report, the rescue centre's December row repeats the annual totals, so December 2023 is marked unavailable. The heatmap's year-total column and its monthly shares use the published annual totals, not sums of incomplete monthly records, so the 2023 rows add up to slightly less than 100%.
- The Federal Territories are reported as a single unit. The maps treat Kuala Lumpur, Putrajaya and Labuan as one unit drawn at Kuala Lumpur, and its rate per km² uses their combined area.
- The animals-per-1,000 km² rate uses state areas measured from the simplified boundary file, so the areas are approximate.
- Release-area positions are approximate (within about 10–20 km) and show destinations, not routes. The 2024 NWRC report does not follow up on the animals it released.
- The sun bear tree covers cases described in BSBCC's public reports, not every bear in its care. Sabah and Sarawak wildlife agencies publish separately and are outside the scope of this study.
- No animal tracking (GPS) data are used. Volunteer records contain no personal names.

## Repository structure

| Path | Contents |
|---|---|
| `index.html`, `css/`, `js/` | The site: text, layout and chart loading |
| `charts/` | Vega-Lite specifications (12 files) |
| `data/` | Processed data, boundary geometry and the provenance record |
| `tools/` | Data and specification scripts, their inputs and documentation |
| `scripts/` | Local server and validation checks |
| `vendor/`, `assets/fonts/` | Pinned Vega libraries and self-hosted typefaces, with their licences |

## Reproducing the site

The site is static and has no build step. To view it locally, install [Node.js](https://nodejs.org/) and run the following in the repository folder, then open http://127.0.0.1:8000/:

```
npm start
```

To regenerate the data and specifications, run the three steps in [`tools/README.md`](tools/README.md) with Python 3.9 or later, then run `npm run check`. The validation check needs the pinned development packages, which `npm ci --ignore-scripts` installs.

## Licence

© 2026 Kenneth Gomes. The text, visualisations, chart specifications and code in this repository are licensed under the [Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). They may be shared and adapted for non-commercial purposes with credit; commercial use requires the author's permission. See [`LICENSE`](LICENSE).

Third-party material is excluded from this licence and remains with its owners:

- Figures from the PERHILITAN and BSBCC annual reports remain the property of those organisations and are used with their permission.
- Brunton et al. (2025) is published under CC BY 4.0.
- Boundary data are © OpenStreetMap contributors via geoBoundaries; the adapted boundary files are available under the Open Database License 1.0.
- Fraunces and Source Sans 3 are licensed under the SIL Open Font License 1.1; Vega, Vega-Lite and vega-embed are © University of Washington Interactive Data Lab under the BSD 3-Clause License. Licence texts are included beside these files.

## Acknowledgements

The map-layering, lookup-join and linked-view patterns adapt the FIT3179 Vega-Lite teaching examples (Monash University). OpenAI Codex and Anthropic Claude helped extract tables, write code and edit text. The author designed the study, checked every figure against the source reports and reviewed all code and text.

## References

Bornean Sun Bear Conservation Centre. *Annual report* (2021–2025 editions). [2021](https://www.bsbcc.org.my/s/Annual-Report-2021.pdf), [2022](https://www.bsbcc.org.my/s/Annual-Report-2022.pdf), [2023](https://www.bsbcc.org.my/s/Annual-Report-2023_FINAL_compressed-3ebd.pdf), [2024](https://www.bsbcc.org.my/s/Annual-Report-2024_FINAL.pdf), [2025](https://www.bsbcc.org.my/s/Annual-Report-2025.pdf)

Brunton, E. A., Levengood, A. L., Tee, T. L., Chiew, L. M., Seng, Y. W., Yeoh, B. N., Tuuga, A., & Wong, S. T. (2025). A window into the forest: Post-release behaviour of rehabilitated Bornean sun bears *Helarctos malayanus euryspilus* in Sabah, Malaysia. *Wildlife Biology, 2025*(2), e01264. https://doi.org/10.1002/wlb3.01264

Department of Wildlife and National Parks Peninsular Malaysia. *Laporan tahunan / Annual report* (2021–2024 editions). [Library catalogue record](https://koha.wildlife.gov.my/cgi-bin/koha/opac-detail.pl?biblionumber=1449)

Harrower, M., & Brewer, C. A. (2003). ColorBrewer.org: An online tool for selecting colour schemes for maps. *The Cartographic Journal, 40*(1), 27–37. https://doi.org/10.1179/000870403235002042

Izzat-Husna, M., Nabilah, N., Kamaruddin, Z. A., Mansor, M. S., Zubaidah, K., Syarifah, N. A. S. A., Ilangovan, K., Hartini, I., Magintan, D., Pazil, A. P., & Shukor, M. N. (2022). *Sun bear management guideline at National Wildlife Rescue Centre (NWRC), Peninsular Malaysia* (2nd ed.). FGV Holdings Berhad.

Okabe, M., & Ito, K. (2008). *Color Universal Design (CUD): How to make figures and presentations that are friendly to colorblind people*. J\*Fly.

Runfola, D., et al. (2020). geoBoundaries: A global database of political administrative boundaries. *PLoS ONE, 15*(4), e0231866. https://doi.org/10.1371/journal.pone.0231866

Satyanarayan, A., Moritz, D., Wongsuphasawat, K., & Heer, J. (2017). Vega-Lite: A grammar of interactive graphics. *IEEE Transactions on Visualization and Computer Graphics, 23*(1), 341–350. https://doi.org/10.1109/TVCG.2016.2599030

Sherman, J., Menon, V., Kock, R., King, T., Luz, S., Ashraf, N. V. K., Soorae, P., & Moehrenschlager, A. (2025). *Guidelines on responsible translocation of displaced organisms*. IUCN. https://doi.org/10.2305/QKVR4181

## Citation

Gomes, K. (2026). *A second chance: Wildlife rescue and rehabilitation in Malaysia* [Interactive data visualisation]. https://ninopanini.github.io/fit3179-malaysia-wildlife-rescue/
