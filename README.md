# Wildlife care in Malaysia website

Local scaffold prepared 16 October 2026. No finished webpage or chart has been implemented yet.

This folder is the root of the DV2 Git repository. The parent assignment workspace contains research and original sources and is not part of this repository.

## Intended structure

- `index.html`: single scrolling visual story; to be created.
- `css/`: page layout and typography.
- `js/`: chart loading and page interactions.
- `charts/`: readable Vega/Vega-Lite JSON specifications.
- `data/`: selected validated publication data and map geometry.
- `assets/`: selected credited presentation assets.

The empty folders are placeholders, not completed implementation.

## Local preview after implementation

From this folder, use a local HTTP server, for example `python -m http.server 8000 --bind 127.0.0.1`, then open `http://127.0.0.1:8000/`. Use an installed Python interpreter. There is no homepage to preview yet.

Use relative paths within the website. References to Downloads, local drive letters or parent research folders will not work on the published site.

## GitHub setup still to do

Create the user's DV2 repository, connect it as `origin`, push `main`, then enable GitHub Pages from `main` and `/(root)`. No remote URL or deployment is configured yet.

[GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## Before publishing

Select only the data and assets used by the visual story, with source and permission notes. Add the author, date and AI acknowledgement. Verify the three distinct map idioms, rubric coverage, small-laptop layout, readable chart JSON and interactions. Check both the local preview and public URL.
