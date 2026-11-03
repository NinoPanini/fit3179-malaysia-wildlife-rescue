"""Step 3 of 3: the Vega-Lite specifications (run from the website folder: python tools/3_chart_specs.py).

Writes every chart as readable JSON in charts/. One shared config (font, palette) keeps all
charts consistent. Patterns for layered maps, lookups, bound selectors, the bump-chart
selection and the brush-linked views are adapted from the FIT3179/Vega-Lite teaching examples.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'charts'                 # ROOT is the website folder
SCHEMA = 'https://vega.github.io/schema/vega-lite/v5.json'

# ---- One palette for the whole page -------------------------------------
# Colour rules (FIT3179 colour notes + Munzner): hue for categories, light-to-dark for amounts,
# colour-vision-safe palettes, and never colour alone - every colour is backed by a label, shape,
# dash, position or number so the charts still read for colour-blind viewers.
INK, MUTED, GRID, PAPER = '#1f2d2a', '#56625d', '#e4e0d2', '#fbf9f2'
GROUP = {'Reptiles': '#0072B2', 'Mammals': '#B26F00', 'Birds': '#A85F8C'}   # Okabe-Ito hues, darkened so every mark reaches 3:1 contrast
SEQ = ['#ffffcc', '#a1dab4', '#41b6c4', '#2171b5', '#253494', '#081d58']   # ColorBrewer YlGnBu, steps spaced so neighbours stay apart for colour-blind readers
MARK = '#3e5260'                                                             # neutral slate for single-series marks
PALE = '#9c947f'   # context lines and dots: faint but still visible (2.9:1)
MY, OTHER = '#2f4858', '#8a8270'                                             # Malaysia highlighted in slate, other countries in neutral grey
FONT = "'Source Sans 3', 'Segoe UI', Arial, sans-serif"  # quoted: the family name contains a digit

CONFIG = {
    'background': None, 'font': FONT,
    'view': {'stroke': None},
    'axis': {'labelFontSize': 13, 'titleFontSize': 13, 'titleFontWeight': 600, 'labelColor': MUTED,
             'titleColor': INK, 'domain': False, 'gridColor': GRID, 'tickColor': GRID,
             'labelPadding': 6, 'titlePadding': 12},
    'legend': {'labelFontSize': 13, 'titleFontSize': 13, 'titleFontWeight': 600, 'labelColor': INK,
               'titleColor': INK, 'symbolStrokeWidth': 0},
    'text': {'font': FONT, 'color': INK},
    'title': {'font': FONT, 'anchor': 'start', 'color': INK},
}
GEO = {'url': 'data/peninsular-states.geojson', 'format': {'type': 'json', 'property': 'features'}}
LAND, BORDER, NODATA = '#e6e0cf', '#a39b86', '#958d78'   # land, coast and state borders, 'no separate figure'
BASEMAP = {
    'data': GEO,
    'mark': {'type': 'geoshape', 'fill': LAND, 'stroke': BORDER, 'strokeWidth': 0.8},
    'encoding': {'tooltip': [{'field': 'properties.state', 'type': 'nominal', 'title': 'State / territory'}]},
}
def group_colour(title=None, legend=None):
    return {'field': 'group', 'type': 'nominal', 'title': title,
            'scale': {'domain': list(GROUP), 'range': list(GROUP.values())}, 'legend': legend}

def save(name, spec):
    if spec.get('width') == 'container' and 'autosize' not in spec:
        spec['autosize'] = {'type': 'fit-x', 'contains': 'padding'}
    spec = {'$schema': SCHEMA, **spec, 'config': CONFIG}
    with open(OUT / name, 'w', encoding='utf8', newline='\n') as f:
        f.write(json.dumps(spec, indent=2, ensure_ascii=False) + '\n')

# ---- 01 Waffle: what was handed over in 2024 ----------------------------
save('01-handover-waffle.json', {
    'description': '100 squares, one per percent of the 16,034 animals handed over to PERHILITAN in 2024, coloured by animal group.',
    'data': {'url': 'data/handovers-waffle-2024.json'},
    'transform': [{'calculate': "datum.group + ' · ' + datum.share + '%'", 'as': 'label'}],
    'width': 300, 'height': 300,
    'mark': {'type': 'rect', 'cornerRadius': 2, 'stroke': PAPER, 'strokeWidth': 3},
    'encoding': {
        'x': {'field': 'col', 'type': 'ordinal', 'axis': None},
        'y': {'field': 'row', 'type': 'ordinal', 'axis': None},
        'color': group_colour(None, {'orient': 'right', 'direction': 'vertical', 'symbolType': 'square',
                                     'symbolSize': 260, 'labelFontSize': 15, 'rowPadding': 10, 'labelLimit': 300,
                                     'labelExpr': "datum.label == 'Reptiles' ? 'Reptiles · 88% (14,146)' : datum.label == 'Mammals' ? 'Mammals · 11% (1,683)' : 'Birds · 1% (205)'"}),
        'tooltip': [{'field': 'group', 'type': 'nominal', 'title': 'Animal group'},
                    {'field': 'group_total', 'type': 'quantitative', 'title': 'Animals handed over, 2024', 'format': ','},
                    {'field': 'share', 'type': 'quantitative', 'title': 'Share of all handovers (%)'}],
    },
})

# ---- State labels shared by maps 02 and 03 ---------------------------------
# Hand-placed so every state is named. Small or crowded states get their label in the sea with a
# thin leader line back to the state's centre (lon/lat = label position; ax/ay = state centre).
def lab(state, lon, lat, align, leader, name=None):
    return {'state': state, 'name': name or state, 'lon': lon, 'lat': lat, 'align': align, 'leader': leader}
CIRCLE_LABELS = [lab('Perlis', 99.85, 6.62, 'right', True), lab('Kedah', 99.85, 6.08, 'right', True),
    lab('Pulau Pinang', 99.85, 5.42, 'right', True), lab('Perak', 101.38, 4.62, 'left', False),
    lab('Kelantan', 102.3, 5.62, 'left', False), lab('Terengganu', 103.42, 5.0, 'left', False),
    lab('Pahang', 102.78, 3.75, 'left', False), lab('Selangor', 100.85, 3.6, 'right', True),
    lab('Wilayah Persekutuan', 100.95, 3.12, 'right', True, 'Federal Territories'),
    lab('Negeri Sembilan', 102.5, 2.98, 'left', False), lab('Melaka', 101.7, 2.08, 'right', True),
    lab('Johor', 103.82, 2.12, 'left', False)]
SHARE_LABELS = [lab('Perlis', 99.85, 6.62, 'right', True), lab('Pulau Pinang', 99.85, 5.42, 'right', True),
    lab('Melaka', 101.7, 2.08, 'right', True), lab('Kedah', 100.66, 5.92, 'center', False),
    lab('Perak', 101.11, 4.77, 'center', False), lab('Kelantan', 102.03, 5.28, 'center', False),
    lab('Terengganu', 102.95, 4.94, 'center', False), lab('Pahang', 102.54, 3.74, 'center', False),
    lab('Selangor', 100.85, 3.6, 'right', True), lab('Negeri Sembilan', 102.21, 2.78, 'center', False),
    lab('Johor', 103.38, 2.05, 'center', False)]
WP_POINT = {'state': 'Wilayah Persekutuan', 'longitude': 101.69, 'latitude': 3.12}   # Kuala Lumpur, where the combined figure is drawn
def leader_lines(labels, anchors_url='data/state-anchors.json'):
    """Thin grey lines from each offshore label back to its state."""
    return {'data': {'values': [d for d in labels if d['leader']]},
            'transform': [{'lookup': 'state', 'from': {'data': {'url': anchors_url}, 'key': 'state', 'fields': ['longitude', 'latitude']}},
                          {'calculate': "isValid(datum.longitude) ? datum.longitude : 101.69", 'as': 'ax'},
                          {'calculate': "isValid(datum.latitude) ? datum.latitude : 3.12", 'as': 'ay'}],
            'mark': {'type': 'rule', 'color': '#8a8270', 'strokeWidth': 0.8},
            'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                         'longitude2': {'field': 'ax'}, 'latitude2': {'field': 'ay'}}}

# ---- 02 Proportional-symbol map ----------------------------------------
save('02-handover-map.json', {
    'description': 'Proportional-symbol map: circle area shows wildlife handed over in each reporting state, 2024.',
    'width': 'container', 'height': 470, 'padding': {'left': 72, 'top': 5, 'right': 5, 'bottom': 5},   # room for the labels in the sea
    'projection': {'type': 'mercator'},
    'layer': [
        BASEMAP,
        {'data': {'values': [WP_POINT]},   # Federal Territories: one combined figure, drawn at Kuala Lumpur
         'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                     'fields': ['total', 'reptiles', 'mammals', 'birds']}},
                       {'calculate': "'Federal Territories (combined)'", 'as': 'state'}],
         'mark': {'type': 'circle', 'color': MARK, 'stroke': PAPER, 'strokeWidth': 1.5, 'opacity': 0.72},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'},
                      'size': {'field': 'total', 'type': 'quantitative'},
                      'tooltip': [{'field': 'state', 'title': 'Reporting unit'}, {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','}]}},
        {'data': {'url': 'data/state-anchors.json'},
         'params': [{'name': 'stateHover', 'select': {'type': 'point', 'fields': ['state'], 'on': 'pointerover', 'clear': 'pointerout'}}],
         'mark': {'type': 'circle', 'color': MARK, 'stroke': PAPER, 'strokeWidth': 1.5, 'cursor': 'pointer'},
         'encoding': {
             'longitude': {'field': 'longitude', 'type': 'quantitative'},
             'latitude': {'field': 'latitude', 'type': 'quantitative'},
             'size': {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over',
                      'scale': {'range': [0, 1900], 'zero': True},
                      'legend': {'values': [300, 1000, 2500], 'orient': 'bottom-left', 'symbolFillColor': MARK,
                                 'symbolOpacity': 0.7, 'labelExpr': "format(datum.value, ',')"}},
             'opacity': {'condition': {'param': 'stateHover', 'empty': False, 'value': 0.95}, 'value': 0.72},
             'tooltip': [{'field': 'state', 'type': 'nominal', 'title': 'Reporting state'},
                         {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','},
                         {'field': 'reptiles', 'type': 'quantitative', 'title': 'Reptiles', 'format': ','},
                         {'field': 'mammals', 'type': 'quantitative', 'title': 'Mammals', 'format': ','},
                         {'field': 'birds', 'type': 'quantitative', 'title': 'Birds', 'format': ','}]}},
        leader_lines(CIRCLE_LABELS),
    ] + [{'data': {'values': [d for d in CIRCLE_LABELS if d['align'] == a]},
          'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state', 'fields': ['total']}},
                        {'calculate': "[datum.name, format(datum.total, ',')]", 'as': 'label'}],
          'mark': {'type': 'text', 'align': a, 'dx': 4 if a == 'left' else -4, 'fontSize': 12, 'fontWeight': 600, 'lineHeight': 14, 'baseline': 'middle'},
          'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                       'text': {'field': 'label'}}} for a in ('left', 'right')],
})

# ---- 03 Choropleth with animal-group selector -------------------------
share = "(groupChoice == 'Mammals' ? datum.mammals : groupChoice == 'Reptiles' ? datum.reptiles : datum.birds) / datum.total"
# Manual class breaks (Week 9 classification) chosen separately for each group, because the groups
# live on very different ranges: birds never exceed 3.4% of a state's handovers, reptiles never fall
# below 38%. One shared scale would paint the bird map a single colour. The page explains this and
# prints every state's exact percentage, so readers never have to decode a colour.
BREAKS = {'Mammals': [0.02, 0.04, 0.07, 0.10, 0.25], 'Reptiles': [0.50, 0.90, 0.93, 0.96, 0.98], 'Birds': [0.005, 0.01, 0.015, 0.02, 0.03]}
def _cls(b):
    return " : ".join([f"datum.share < {v} ? {i}" for i, v in enumerate(b)]) + " : 5"
cls = ("groupChoice == 'Mammals' ? (" + _cls(BREAKS['Mammals']) + ") : groupChoice == 'Reptiles' ? (" +
       _cls(BREAKS['Reptiles']) + ") : (" + _cls(BREAKS['Birds']) + ")")
def _labels(b):
    f = lambda v: (f"{v*100:.1f}".rstrip('0').rstrip('.')) + '%'
    return [f"under {f(b[0])}"] + [f"{f(b[i])}–{f(b[i+1])}" for i in range(len(b) - 1)] + [f"{f(b[-1])} or more", 'No separate figure']
LEGEND_EXPR = ("(groupChoice == 'Mammals' ? " + json.dumps(_labels(BREAKS['Mammals'])) + " : groupChoice == 'Reptiles' ? " +
               json.dumps(_labels(BREAKS['Reptiles'])) + " : " + json.dumps(_labels(BREAKS['Birds'])) + ")[datum.value]")
save('03-group-share-map.json', {
    'description': "Choropleth: the selected animal group's share of each state's 2024 handovers, in fixed classes.",
    'width': 'container', 'height': 470, 'padding': {'left': 72, 'top': 5, 'right': 5, 'bottom': 5},
    'params': [{'name': 'groupChoice', 'value': 'Mammals',
                'bind': {'input': 'select', 'options': ['Mammals', 'Reptiles', 'Birds'], 'name': 'Animal group: ', 'element': '#share-map-control'}}],
    'projection': {'type': 'mercator'},
    'layer': [
        {**BASEMAP, 'transform': [{'calculate': "'Federal Territories: one combined figure, not split by territory'", 'as': 'note'}],
         'mark': {'type': 'geoshape', 'stroke': PAPER, 'strokeWidth': 1.2},
         'encoding': {'color': {'datum': 6, 'type': 'ordinal'},   # class 6 = no separate figure (last legend entry)
                      'tooltip': [{'field': 'properties.state', 'type': 'nominal', 'title': 'Territory'},
                                  {'field': 'note', 'type': 'nominal', 'title': 'Note'}]}},
        {'data': GEO,
         'transform': [{'lookup': 'properties.state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                              'fields': ['reptiles', 'mammals', 'birds', 'total']}},
                       {'filter': 'isValid(datum.total)'},
                       {'calculate': share, 'as': 'share'},
                       {'calculate': "groupChoice == 'Mammals' ? datum.mammals : groupChoice == 'Reptiles' ? datum.reptiles : datum.birds", 'as': 'count'},
                       {'calculate': cls, 'as': 'cls'}],
         'mark': {'type': 'geoshape', 'stroke': BORDER, 'strokeWidth': 0.9},
         'encoding': {
             'color': {'field': 'cls', 'type': 'ordinal', 'title': 'Share of the state’s handovers (classes change with the group)',
                       'scale': {'domain': [0, 1, 2, 3, 4, 5, 6], 'range': SEQ + [NODATA]},
                       'legend': {'labelExpr': LEGEND_EXPR, 'orient': 'bottom', 'direction': 'horizontal', 'columns': 4, 'title': ['Share of each state’s', 'handovers in the chosen group'],
                                  'symbolType': 'square', 'symbolSize': 220, 'symbolStrokeColor': '#9c9686', 'symbolStrokeWidth': 0.5,
                                  'labelLimit': 160, 'titleLimit': 420, 'columnPadding': 14}},
             'tooltip': [{'field': 'properties.state', 'type': 'nominal', 'title': 'State'},
                         {'field': 'share', 'type': 'quantitative', 'title': 'Share of handovers', 'format': '.1%'},
                         {'field': 'count', 'type': 'quantitative', 'title': 'Animals in this group', 'format': ','},
                         {'field': 'total', 'type': 'quantitative', 'title': 'All animals handed over', 'format': ','}]}},
        leader_lines(SHARE_LABELS),
    ] + [{'data': {'values': [d for d in SHARE_LABELS if d['leader'] == offshore]},
          'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                      'fields': ['reptiles', 'mammals', 'birds', 'total']}},
                        {'calculate': share, 'as': 'share'}, {'calculate': cls, 'as': 'cls'},
                        {'calculate': "[datum.name, datum.share < 0.1 ? format(datum.share, '.1%') : format(datum.share, '.0%')]", 'as': 'label'}],
          # offshore labels sit in the sea (dark text); the rest sit on their state (white on dark classes)
          'mark': {'type': 'text', 'fontSize': 11.5, 'fontWeight': 700, 'lineHeight': 13, 'baseline': 'middle',
                   'align': 'right' if offshore else 'center', 'dx': -4 if offshore else 0},
          'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                       'text': {'field': 'label'},
                       'color': {'value': INK} if offshore else {'condition': {'test': 'datum.cls >= 3', 'value': 'white'}, 'value': INK},
                       'tooltip': [{'field': 'name', 'title': 'State'}, {'field': 'share', 'type': 'quantitative', 'title': 'Share', 'format': '.1%'}]}}
         for offshore in (False, True)],
})

# ---- 04 Bump chart of state ranks --------------------------------------
YEARS = [2021, 2022, 2023, 2024]
x_year = {'field': 'year', 'type': 'ordinal', 'scale': {'domain': YEARS, 'padding': 1.6},
          'axis': {'title': None, 'labelAngle': 0, 'labelFontSize': 15, 'labelFontWeight': 600, 'labelColor': INK, 'orient': 'top'}}
y_rank = {'field': 'rank', 'type': 'quantitative', 'scale': {'domain': [0.5, 14.6], 'reverse': True}, 'axis': None}
picked = {'param': 'pickState'}
save('04-state-rank-bump.json', {
    'description': 'Bump chart: each reporting state ranked by animals handed over in 2021, 2023 and 2024. 2022 has no state table.',
    'width': 'container', 'height': 420,
    'data': {'url': 'data/handovers-trend.json'},
    'encoding': {'x': x_year, 'y': y_rank},
    'layer': [
        {'data': {'values': [{'year': 2022, 'rank': 13.6}]},
         'mark': {'type': 'text', 'fontSize': 12.5, 'color': MUTED, 'lineHeight': 17, 'fontStyle': 'italic',
                  'text': ['2022 state rankings unavailable:', 'dashed lines join 2021 to 2023']}},
        {'transform': [{'filter': 'datum.year <= 2023'}],
         'mark': {'type': 'line', 'strokeDash': [4, 4], 'cursor': 'pointer', 'interpolate': 'monotone'},
         'encoding': {'detail': {'field': 'state'},
                      'color': {'condition': {**picked, 'value': INK}, 'value': PALE},
                      'strokeWidth': {'condition': {**picked, 'value': 3}, 'value': 1.6},
                      'order': {'field': 'year'}}},
        {'transform': [{'filter': 'datum.year >= 2023'}],
         'mark': {'type': 'line', 'cursor': 'pointer'},
         'encoding': {'detail': {'field': 'state'},
                      'color': {'condition': {**picked, 'value': INK}, 'value': PALE},
                      'strokeWidth': {'condition': {**picked, 'value': 3.5}, 'value': 2},
                      'order': {'field': 'year'}}},
        {'params': [{'name': 'pickState', 'value': [{'state': 'Terengganu'}],   # the headline's state stands out first
                     'select': {'type': 'point', 'fields': ['state'], 'on': 'click', 'clear': 'dblclick'}}],
         'mark': {'type': 'circle', 'size': 90, 'opacity': 1, 'stroke': PAPER, 'strokeWidth': 1.5, 'cursor': 'pointer'},
         'encoding': {'color': {'condition': {**picked, 'value': INK}, 'value': PALE},
                      'tooltip': [{'field': 'state', 'type': 'nominal', 'title': 'State'},
                                  {'field': 'year', 'type': 'ordinal', 'title': 'Year'},
                                  {'field': 'rank', 'type': 'quantitative', 'title': 'Rank (1 = most)'},
                                  {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','}]}},
        {'transform': [{'filter': 'datum.year == 2021'}, {'calculate': "datum.state + '  ' + datum.rank", 'as': 'label'}],
         'mark': {'type': 'text', 'align': 'right', 'dx': -12, 'fontSize': 13},
         'encoding': {'text': {'field': 'label'},
                      'color': {'condition': {**picked, 'value': INK}, 'value': MUTED}}},
        {'transform': [{'filter': 'datum.year == 2024'}, {'calculate': "datum.rank + '  ' + datum.state + '  ' + format(datum.total, ',')", 'as': 'label'}],
         'mark': {'type': 'text', 'align': 'left', 'dx': 12, 'fontSize': 13},
         'encoding': {'text': {'field': 'label'},
                      'color': {'condition': {**picked, 'value': INK}, 'value': MUTED}}},
        {'transform': [{'filter': picked},
                       {'calculate': "datum.rank == 1 ? '1st' : datum.rank == 2 ? '2nd' : datum.rank == 3 ? '3rd' : datum.rank + 'th'", 'as': 'ord'}],
         'mark': {'type': 'text', 'dy': -14, 'fontSize': 13, 'fontWeight': 700, 'color': INK},
         'encoding': {'text': {'field': 'ord'}}},
    ],
})

# ---- 05 Heatmap + total bars: NWRC monthly intake 2023-2024 -----------
ROWS = [f'{y} · {g}' for y in (2023, 2024) for g in GROUP]
row_y = {'field': 'row', 'type': 'nominal', 'sort': ROWS, 'title': None}
BANDS = ['0', '1–9', '10–99', '100–999', '1,000+', 'Not available']
band = ("!datum.reported ? 'Not available' : datum.animals == 0 ? '0' : datum.animals < 10 ? '1–9' : "
        "datum.animals < 100 ? '10–99' : datum.animals < 1000 ? '100–999' : '1,000+'")
save('05-intake-heatmap.json', {
    'description': 'Heatmap of animals received by NWRC each month in 2023 and 2024 by animal group, with yearly totals as bars.',
    'usermeta': {'fitWidth': 990},   # js/app.js scales the fixed widths below to the page column
    'hconcat': [
        {'width': 590, 'height': 240,
         'data': {'url': 'data/nwrc-intake-2023-2024.json'},
         'transform': [{'calculate': "datum.year + ' · ' + datum.group", 'as': 'row'},
                       {'calculate': band, 'as': 'band'}],
         'encoding': {
             'x': {'field': 'month', 'type': 'ordinal', 'sort': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                   'axis': {'title': None, 'labelAngle': 0, 'orient': 'top', 'labelColor': INK}},
             'y': {**row_y, 'axis': {'labelFontSize': 13, 'labelColor': INK, 'labelPadding': 10}},
             'tooltip': [{'field': 'month', 'type': 'nominal', 'title': 'Month'}, {'field': 'year', 'type': 'ordinal', 'title': 'Year'},
                         {'field': 'group', 'type': 'nominal', 'title': 'Group'},
                         {'field': 'animals', 'type': 'quantitative', 'title': 'Animals received', 'format': ','},
                         {'field': 'band', 'type': 'nominal', 'title': 'Class'}]},
         'layer': [
             # zero months: empty cell with a thin outline; unavailable months: grey with "n/a"
             {'mark': {'type': 'rect', 'cornerRadius': 3},
              'encoding': {'stroke': {'condition': {'test': "datum.band == '0'", 'value': '#c9c3b0'}, 'value': PAPER},
                           'strokeWidth': {'condition': {'test': "datum.band == '0'", 'value': 1}, 'value': 3},
                           'color': {'field': 'band', 'type': 'ordinal', 'title': 'Animals received in the month',
                                     'scale': {'domain': BANDS, 'range': [PAPER, '#ffffcc', '#a1dab4', '#41b6c4', '#225ea8', '#d6d0bf']},
                                     'legend': {'orient': 'bottom', 'direction': 'horizontal', 'symbolType': 'square',
                                                'symbolStrokeColor': '#bdb7a5', 'symbolStrokeWidth': 1}}}},
             {'mark': {'type': 'text', 'fontSize': 12.5},
              'encoding': {'text': {'condition': {'test': '!datum.reported', 'value': 'n/a'}, 'field': 'animals', 'format': ','},
                           'color': {'condition': {'test': 'datum.animals >= 1000', 'value': 'white'}, 'value': INK}}},
             # the two spikes behind "sudden waves": outlined in ink
             {'transform': [{'filter': 'datum.animals >= 1000'}],
              'mark': {'type': 'rect', 'fillOpacity': 0, 'stroke': INK, 'strokeWidth': 2.5, 'cornerRadius': 3}},
         ]},
        {'width': 210, 'height': 240,
         'data': {'url': 'data/nwrc-intake-totals.json'},
         'transform': [{'calculate': "datum.year + ' · ' + datum.group", 'as': 'row'}],
         'encoding': {'y': {**row_y, 'axis': None},
                      'x': {'field': 'animals', 'type': 'quantitative', 'title': 'Year total',
                            'scale': {'domain': [0, 14000]}, 'axis': {'orient': 'top', 'tickCount': 2, 'grid': False, 'labels': False}}},
         'layer': [
             {'mark': {'type': 'bar', 'height': 18, 'cornerRadiusEnd': 2},
              'encoding': {'color': group_colour(), 'tooltip': [{'field': 'row', 'title': 'Year · group'},
                                                               {'field': 'animals', 'type': 'quantitative', 'title': 'Animals received', 'format': ','}]}},
             {'mark': {'type': 'text', 'align': 'left', 'dx': 6, 'fontSize': 13, 'fontWeight': 600},
              'encoding': {'text': {'field': 'animals', 'format': ','}}},
             {'data': {'values': [{}]}, 'mark': {'type': 'rule', 'color': MUTED, 'strokeWidth': 1},   # zero baseline
              'encoding': {'x': {'datum': 0}, 'y': {'value': 0}, 'y2': {'value': 'height'}}},
         ]},
    ],
    'spacing': 18,
    'resolve': {'scale': {'color': 'independent'}},
})

# ---- 06 Bear journeys: connected dot plot on a timeline ----------------
KINDS = ['Into care', 'Rehabilitation step', 'Release', 'Recaptured', 'Other collar signal', 'Collar death signal', 'Remains found']
X_SHAPE = 'M-1,-0.6L-0.6,-1L0,-0.4L0.6,-1L1,-0.6L0.4,0L1,0.6L0.6,1L0,0.4L-0.6,1L-1,0.6L-0.4,0Z'   # an X, drawn as an SVG path
XT = {'type': 'temporal', 'title': None,
      'axis': {'format': '%Y', 'tickCount': {'interval': 'year'}, 'labelFontSize': 14, 'labelColor': INK, 'grid': True}}
SHAPES = {'domain': KINDS, 'range': ['circle', 'square', 'triangle-up', 'diamond', 'triangle-down', X_SHAPE, 'cross']}
KCOLS = {'domain': KINDS, 'range': ['#8a8270', '#1b7837', '#D55E00', '#762a83', '#5e6b8a', '#b2182b', '#000000']}
BEAR_TIP = [{'field': 'bear', 'title': 'Bear'}, {'field': 'event', 'title': 'Event'},
            {'field': 'date_label', 'title': 'Date'}, {'field': 'place', 'title': 'Place'},
            {'field': 'note', 'title': 'Note'}, {'field': 'source', 'title': 'Source'}]
LEG = {'orient': 'top', 'direction': 'horizontal', 'symbolSize': 150, 'columnPadding': 22, 'labelLimit': 200}
picked_bear = {'param': 'bearPick'}
RELEASED, IN_CARE = ['Sunbearo', 'Loki', 'Wawa', 'Sika', 'Itam'], ['Rudy', 'Kwong', 'Tenom', 'Pitang']
GROUP_HEAD = ['Released to the forest · 5 bears', 'Still in care · 4 bears']
save('06-bear-journeys.json', {
    'description': 'Timeline of nine sun bears at BSBCC, 2021-2025, with an enlarged view of the bear you click.',
    'usermeta': {'fitWidth': 960},   # js/app.js scales the fixed widths below to the page column
    'data': {'url': 'data/bear-journeys.json'},
    'vconcat': [
        {'width': 860, 'height': 418,   # 11 rows of 38 px
         'encoding': {'y': {'field': 'bear', 'type': 'nominal', 'title': None,
                            'scale': {'domain': [GROUP_HEAD[0]] + RELEASED + [GROUP_HEAD[1]] + IN_CARE},   # a heading row above each group
                            'axis': {'values': RELEASED + IN_CARE, 'labelFontSize': 15, 'labelFontWeight': 600, 'labelColor': INK, 'labelPadding': 12, 'grid': True, 'gridColor': '#efece2'}}},
         'layer': [
             {'data': {'values': [{'head': h} for h in GROUP_HEAD]},
              'mark': {'type': 'text', 'align': 'left', 'fontSize': 14, 'fontWeight': 700, 'color': MUTED},
              'encoding': {'y': {'field': 'head', 'type': 'nominal', 'title': None}, 'x': {'value': -90}, 'text': {'field': 'head'}}},
             {'data': {'url': 'data/bear-outcomes.json'},
              'mark': {'type': 'rule', 'strokeWidth': 2.5},
              'encoding': {'x': {'field': 'first', **XT}, 'x2': {'field': 'last'},
                           'color': {'condition': {**picked_bear, 'value': INK}, 'value': '#c9c3b0'}}},
             {'params': [{'name': 'bearPick', 'value': [{'bear': 'Itam'}], 'select': {'type': 'point', 'fields': ['bear'], 'on': 'click', 'clear': False}},
                         {'name': 'kindPick', 'select': {'type': 'point', 'fields': ['kind']}, 'bind': 'legend'}],
              'mark': {'type': 'point', 'filled': True, 'size': 140, 'stroke': PAPER, 'strokeWidth': 1, 'cursor': 'pointer'},
              'encoding': {'x': {'field': 'date', **XT, 'scale': {'domain': ['2020-12-01', '2027-03-01']},
                                 'axis': {**XT['axis'], 'values': [{'year': y, 'month': 1, 'date': 1} for y in range(2021, 2026)]}},   # only years with events; the space on the right holds the notes
                           'shape': {'field': 'kind', 'type': 'nominal', 'title': None, 'scale': SHAPES, 'legend': LEG},
                           'color': {'field': 'kind', 'type': 'nominal', 'title': None, 'scale': KCOLS, 'legend': LEG},
                           'yOffset': {'field': 'nudge', 'type': 'quantitative', 'scale': {'domain': [-1, 1], 'range': [8, 30]}},   # offset from the row top (row centre = 19 px); stacks events under five weeks apart
                           'opacity': {'condition': {'param': 'kindPick', 'value': 1}, 'value': 0.12},
                           'tooltip': BEAR_TIP}},
             {'data': {'url': 'data/bear-outcomes.json'},
              'mark': {'type': 'text', 'align': 'left', 'dx': 16, 'fontSize': 13, 'fontStyle': 'italic'},
              'encoding': {'x': {'field': 'last', **XT}, 'text': {'field': 'outcome'},
                           'color': {'condition': {**picked_bear, 'value': INK}, 'value': MUTED}}},
         ]},
        {'width': 860, 'height': 150,
         'transform': [{'filter': picked_bear},
                       {'window': [{'op': 'row_number', 'as': 'n'}], 'sort': [{'field': 'date'}]},
                       {'calculate': 'datum.n % 3', 'as': 'lane'},
                       {'calculate': "[datum.event, datum.date_label]", 'as': 'label'}],
         'encoding': {'x': {'field': 'date', 'type': 'temporal', 'title': None,
                            'scale': {'padding': 70, 'nice': False},
                            'axis': {'format': '%-d %b %Y', 'tickCount': 5, 'labelFontSize': 13, 'labelColor': INK, 'grid': False}},
                      'y': {'datum': 0, 'type': 'quantitative', 'scale': {'domain': [-1, 1]}, 'axis': None}},
         'layer': [
             {'mark': {'type': 'rule', 'color': INK, 'strokeWidth': 2.5},
              'encoding': {'x': {'aggregate': 'min', 'field': 'date', 'type': 'temporal'}, 'x2': {'aggregate': 'max', 'field': 'date'}}},
             {'mark': {'type': 'point', 'filled': True, 'size': 260, 'stroke': PAPER, 'strokeWidth': 1.5},
              'encoding': {'shape': {'field': 'kind', 'type': 'nominal', 'scale': SHAPES, 'legend': None},
                           'color': {'field': 'kind', 'type': 'nominal', 'scale': KCOLS, 'legend': None}, 'tooltip': BEAR_TIP}},
             {'transform': [{'filter': 'datum.lane == 0'}],
              'mark': {'type': 'text', 'dy': -30, 'fontSize': 12.5, 'lineHeight': 15, 'baseline': 'bottom'},
              'encoding': {'text': {'field': 'label'}}},
             {'transform': [{'filter': 'datum.lane == 1'}],
              'mark': {'type': 'text', 'dy': 22, 'fontSize': 12.5, 'lineHeight': 15, 'baseline': 'top'},
              'encoding': {'text': {'field': 'label'}}},
             {'transform': [{'filter': 'datum.lane == 2'}],
              'mark': {'type': 'text', 'dy': -64, 'fontSize': 12.5, 'lineHeight': 15, 'baseline': 'bottom', 'color': MUTED},
              'encoding': {'text': {'field': 'label'}}},
             {'transform': [{'window': [{'op': 'row_number', 'as': 'k'}]}, {'filter': 'datum.k == 1'},
                            {'calculate': "'Enlarged: ' + datum.bear + ' (click another bear above to switch)'", 'as': 't'}],
              'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'fontSize': 15, 'fontWeight': 700, 'color': INK},
              'encoding': {'x': {'value': 0}, 'y': {'value': -38}, 'text': {'field': 't'}}},
         ]},
    ],
    'spacing': 56,
    'resolve': {'legend': {'color': 'independent', 'shape': 'independent'}},
})

# ---- 07 Flow map: NWRC to named release areas --------------------------
SITES = {'url': 'data/release-sites.json'}
def site_labels(names, align, dx):
    return {'data': SITES,
            'transform': [{'filter': {'field': 'site', 'oneOf': names}},
                          {'calculate': "[datum.site, datum.animals + (datum.animals == 1 ? ' animal' : ' animals')]", 'as': 'label'}],
            'mark': {'type': 'text', 'align': align, 'dx': dx, 'fontSize': 12.5, 'fontWeight': 600, 'lineHeight': 15, 'cursor': 'pointer'},
            'encoding': {'opacity': {'condition': {'test': "siteFocus == 'All destinations' || datum.site == siteFocus", 'value': 1}, 'value': 0.3},
                         'longitude': {'field': 'longitude', 'type': 'quantitative'},
                         'latitude': {'field': 'latitude', 'type': 'quantitative'}, 'text': {'field': 'label'}}}
width_scale = {'domain': [0, 13], 'range': [0, 9]}
save('07-release-flow-map.json', {
    'description': 'Flow map: animals released by NWRC in 2024, from the centre at Sungkai to six named protected areas. Line width shows animals.',
    'width': 'container', 'height': 520,
    'padding': {'left': 110, 'top': 5, 'right': 5, 'bottom': 5},
    # siteFocus is shared with chart 08: js/app.js copies a click here into the Sankey's menu and back.
    'params': [{'name': 'siteFocus', 'value': 'All destinations'}],
    'projection': {'type': 'mercator'},
    'layer': [
        BASEMAP,
        {'data': {'url': 'data/release-arcs.json'},
         'mark': {'type': 'line', 'color': MARK, 'opacity': 0.8, 'strokeCap': 'round'},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'},
                      'latitude': {'field': 'latitude', 'type': 'quantitative'},
                      'detail': {'field': 'site'}, 'order': {'field': 'step'},
                      'opacity': {'condition': {'test': "siteFocus == 'All destinations' || datum.site == siteFocus", 'value': 0.85}, 'value': 0.1},
                      'strokeWidth': {'field': 'animals', 'type': 'quantitative', 'scale': width_scale,
                                      'title': 'Animals released', 'legend': {'values': [1, 4, 13], 'orient': 'bottom-left', 'symbolType': 'stroke', 'symbolSize': 1600, 'labelFontSize': 13}}}},
        {'data': SITES, 'transform': [{'filter': 'isValid(datum.arrow_angle)'}, {'calculate': '50 + datum.animals * 16', 'as': 'arrow_size'}],
         'mark': {'type': 'point', 'shape': 'triangle-up', 'filled': True, 'color': MARK},
         'encoding': {'opacity': {'condition': {'test': "siteFocus == 'All destinations' || datum.site == siteFocus", 'value': 0.95}, 'value': 0.1},'longitude': {'field': 'arrow_longitude', 'type': 'quantitative'},
                      'latitude': {'field': 'arrow_latitude', 'type': 'quantitative'},
                      'angle': {'field': 'arrow_angle', 'type': 'quantitative', 'scale': None},
                      'size': {'field': 'arrow_size', 'type': 'quantitative', 'scale': None}}},
        {'data': SITES,
         'mark': {'type': 'circle', 'color': INK, 'stroke': PAPER, 'strokeWidth': 1.5, 'cursor': 'pointer'},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'},
                      'latitude': {'field': 'latitude', 'type': 'quantitative'},
                      'size': {'condition': {'test': "datum.site == siteFocus", 'value': 260}, 'value': 110},
                      'tooltip': [{'field': 'site', 'title': 'Release area'}, {'field': 'state', 'title': 'State'},
                                  {'field': 'animals', 'type': 'quantitative', 'title': 'Animals released'},
                                  {'field': 'species_list', 'title': 'Species (animals)'}]}},
        # NWRC and the one local release: labels sit offshore, joined to the centre by thin leader lines
        {'data': {'values': [{'lon': 100.42, 'lat': 4.0, 'text': 'NWRC, Sungkai', 'bold': True},
                             {'lon': 100.42, 'lat': 3.5, 'text': ['1 animal released locally,', 'in Sungkai Wildlife Reserve'], 'bold': False}]},
         'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'}},
         'layer': [
             {'mark': {'type': 'rule', 'color': INK, 'strokeWidth': 0.8},
              'encoding': {'longitude2': {'datum': 101.31}, 'latitude2': {'datum': 3.97}}},
             {'transform': [{'filter': 'datum.bold'}],
              'mark': {'type': 'text', 'align': 'right', 'dx': -5, 'fontSize': 13, 'fontWeight': 700, 'color': INK},
              'encoding': {'text': {'field': 'text'}}},
             {'transform': [{'filter': '!datum.bold'}],
              'mark': {'type': 'text', 'align': 'right', 'dx': -5, 'fontSize': 12.5, 'lineHeight': 15, 'color': INK},
              'encoding': {'text': {'field': 'text'}}}]},
        {'data': {'values': [{'longitude': 101.33, 'latitude': 3.98}]},
         'mark': {'type': 'circle', 'size': 380, 'color': INK, 'stroke': PAPER, 'strokeWidth': 2},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'}}},
        site_labels(['Penang National Park'], 'right', -10),
        site_labels(['Ulu Muda Forest Reserve', 'Temenggor Forest Reserve', 'Taman Negara Terengganu', 'Taman Negara Pahang'], 'left', 10),
    ],
})

# ---- 08 Sankey: species to destination (same 32 animals) ---------------
BIRDS = ['Brahminy kite', 'White-bellied sea eagle', 'Changeable hawk-eagle', 'Buffy fish owl', 'Spotted wood owl', 'Oriental pied hornbill']
group_of = "indexof(" + json.dumps(BIRDS) + ", datum.{f}) >= 0 ? 'Birds' : 'Mammals'"
DESTS = ['Temenggor Forest Reserve', 'Taman Negara Terengganu', 'Ulu Muda Forest Reserve', 'Penang National Park',
         'Taman Negara Pahang', 'Sungkai Wildlife Reserve']
save('08-release-sankey.json', {
    'description': 'Sankey diagram linking 16 released species to six release areas; ribbon width shows animals. Same 32 animals as the flow map.',
    'width': 'container', 'height': 520,
    'params': [{'name': 'destinationChoice', 'value': 'All destinations',
                'bind': {'input': 'select', 'options': ['All destinations'] + DESTS, 'name': 'Highlight a release area: ', 'element': '#sankey-control'}}],
    'padding': {'left': 4, 'right': 4, 'top': 4, 'bottom': 10},   # 'fit' already leaves room for the labels
    'autosize': {'type': 'fit', 'contains': 'padding'},
    'encoding': {'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 1]}, 'axis': None},
                 'y': {'field': 'y', 'type': 'quantitative', 'scale': {'reverse': True, 'domain': [-2, 45.5]}, 'axis': None}},
    'layer': [
        {'data': {'url': 'data/release-ribbons.json'},
         'transform': [{'calculate': group_of.format(f='species'), 'as': 'group'}],
         'mark': {'type': 'area', 'interpolate': 'monotone'},
         'encoding': {'y2': {'field': 'y2'}, 'detail': {'field': 'species'}, 'color': group_colour(),
                      'opacity': {'condition': {'test': "destinationChoice == 'All destinations' || datum.destination == destinationChoice", 'value': 0.6}, 'value': 0.08},
                      'tooltip': [{'field': 'species', 'title': 'Species'}, {'field': 'destination', 'title': 'Release area'},
                                  {'field': 'animals', 'type': 'quantitative', 'title': 'Animals'}]}},
        {'data': {'url': 'data/release-nodes.json'},
         'transform': [{'calculate': "datum.side == 'destination' ? 'Area' : " + group_of.format(f='label'), 'as': 'group'}],
         'mark': 'rect',
         'encoding': {'x2': {'field': 'x2'}, 'y2': {'field': 'y2'},
                      'color': {'field': 'group', 'type': 'nominal', 'scale': {'domain': ['Mammals', 'Birds', 'Area'], 'range': [GROUP['Mammals'], GROUP['Birds'], INK]}, 'legend': None},
                      'tooltip': [{'field': 'label', 'title': 'Species / area'}, {'field': 'animals', 'type': 'quantitative', 'title': 'Animals'}]}},
        {'data': {'url': 'data/release-nodes.json'},
         'transform': [{'filter': {'field': 'label', 'oneOf': ['Leopard', 'Brahminy kite']}},
                       {'calculate': "datum.label == 'Leopard' ? 'MAMMALS' : 'BIRDS'", 'as': 'heading'}],
         'mark': {'type': 'text', 'align': 'right', 'dx': -8, 'dy': -6, 'fontSize': 12.5, 'fontWeight': 700, 'letterSpacing': 1.5, 'baseline': 'bottom'},
         'encoding': {'y': {'field': 'y', 'type': 'quantitative'}, 'text': {'field': 'heading'},   # just above the first species of each group
                      'color': {'value': MUTED}}},
        {'data': {'url': 'data/release-nodes.json'},
         'transform': [{'filter': "datum.side == 'species'"}, {'calculate': "datum.label + '  ' + datum.animals", 'as': 'label_count'}],
         'mark': {'type': 'text', 'align': 'right', 'dx': -8, 'fontSize': 13},
         'encoding': {'y': {'field': 'mid', 'type': 'quantitative'}, 'text': {'field': 'label_count'}}},
        {'data': {'url': 'data/release-nodes.json'},
         'transform': [{'filter': "datum.side == 'destination'"}, {'calculate': "datum.label + '  ' + datum.animals", 'as': 'label_count'}],
         'mark': {'type': 'text', 'align': 'left', 'dx': 8, 'fontSize': 13, 'fontWeight': 600},
         'encoding': {'x': {'field': 'x2', 'type': 'quantitative'}, 'y': {'field': 'mid', 'type': 'quantitative'}, 'text': {'field': 'label_count'}}},
    ],
    'resolve': {'scale': {'color': 'independent'}},
})

# ---- 09 Volunteers and interns, 2021-2025 (basic multi-line) -----------
PROG = {'domain': ['Volunteers', 'Interns'], 'range': [INK, '#6f5520']}
save('09-volunteer-lines.json', {
    'description': 'Line chart: volunteers and interns reported by BSBCC each year, 2021-2025.',
    'width': 'container', 'height': 300,
    'data': {'url': 'data/bsbcc-participation-2021-2025.json'},
    'padding': {'right': 20},
    'encoding': {'x': {'field': 'year', 'type': 'ordinal', 'title': None, 'axis': {'labelAngle': 0, 'labelFontSize': 14, 'labelColor': INK}},
                 'y': {'field': 'people', 'type': 'quantitative', 'title': 'People', 'scale': {'domain': [0, 65]}, 'axis': {'tickCount': 4}},
                 'color': {'field': 'programme', 'type': 'nominal', 'scale': PROG, 'legend': None},
                 'tooltip': [{'field': 'programme', 'title': 'Programme'}, {'field': 'year', 'title': 'Year'},
                             {'field': 'people', 'type': 'quantitative', 'title': 'People'}, {'field': 'note', 'title': 'Note'}]},
    'layer': [
        {'mark': {'type': 'line', 'strokeWidth': 3},
         'encoding': {'strokeDash': {'field': 'programme', 'type': 'nominal', 'scale': {'domain': ['Volunteers', 'Interns'], 'range': [[1, 0], [6, 4]]}, 'legend': None}}},
        {'mark': {'type': 'point', 'filled': True, 'size': 80, 'opacity': 1},
         'encoding': {'shape': {'field': 'programme', 'type': 'nominal', 'scale': {'domain': ['Volunteers', 'Interns'], 'range': ['circle', 'square']}, 'legend': None}}},
        {'transform': [{'filter': "datum.programme == 'Volunteers'"}],
         'mark': {'type': 'text', 'dy': -14, 'fontSize': 13, 'fontWeight': 600}, 'encoding': {'text': {'field': 'people'}}},
        {'transform': [{'filter': "datum.programme == 'Interns'"}],
         'mark': {'type': 'text', 'dy': 17, 'fontSize': 13, 'fontWeight': 600}, 'encoding': {'text': {'field': 'people'}}},
        {'transform': [{'filter': 'datum.year == 2025'}],
         'mark': {'type': 'text', 'align': 'left', 'dx': 12, 'dy': 4, 'fontSize': 14, 'fontWeight': 600},
         'encoding': {'text': {'field': 'programme'}}},
        {'data': {'values': [{'year': 2021, 'people': 60}]},   # the 2021 caveat, above that year
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'dx': -8, 'fontSize': 12, 'fontStyle': 'italic', 'lineHeight': 15, 'color': MUTED,
                  'text': ['2021 report also mentions', '2 remote volunteers;', 'unclear if among the 7']},
         'encoding': {'color': {'value': MUTED}, 'tooltip': None}},
    ],
})

# ---- 10 Lollipop: where 2025 volunteers came from ----------------------
save('10-volunteer-origins.json', {
    'description': 'Lollipop chart: 2025 BSBCC volunteer placements by listed country of origin.',
    'width': 'container', 'height': 300,
    'data': {'url': 'data/bsbcc-origins-2025.json'},
    'encoding': {'y': {'field': 'origin', 'type': 'nominal', 'sort': '-x', 'title': None, 'axis': {'labelFontSize': 13.5, 'labelColor': INK}},
                 'x': {'field': 'placements', 'type': 'quantitative', 'title': 'Volunteer placements, 2025', 'scale': {'domain': [0, 38]}, 'axis': {'values': [0, 10, 20, 30]}},
                 'color': {'condition': {'test': "datum.origin == 'Malaysia'", 'value': MY}, 'value': OTHER},
                 'tooltip': [{'field': 'origin', 'title': 'Listed origin'}, {'field': 'placements', 'type': 'quantitative', 'title': 'Placements'}]},
    'layer': [
        {'mark': {'type': 'rule', 'strokeWidth': 2.5}, 'encoding': {'x2': {'datum': 0}}},
        {'mark': {'type': 'circle', 'size': 150, 'opacity': 1}},
        {'transform': [{'joinaggregate': [{'op': 'sum', 'field': 'placements', 'as': 'all'}]},
                       {'calculate': "datum.origin == 'Malaysia' ? datum.placements + ' of ' + datum.all + ' · ' + format(datum.placements / datum.all, '.0%') : datum.placements", 'as': 'label'}],
         'mark': {'type': 'text', 'align': 'left', 'dx': 11, 'fontSize': 13, 'fontWeight': 600}, 'encoding': {'text': {'field': 'label'}, 'color': {'value': INK}}},
    ],
})

# ---- 11 Gantt + linked histogram: 57 placements in 2025 ---------------
BINS = ['8–14', '15–21', '22–28', '29–35', '36–42']            # one-week bins, labelled by the days they hold
WEEK_BIN = [{'bin': {'step': 7, 'extent': [8, 43], 'nice': False}, 'field': 'days', 'as': ['bin_start', 'bin_end']},
            {'calculate': "datum.bin_start + '–' + (datum.bin_end - 1)", 'as': 'range'}]
HX = {'field': 'range', 'type': 'ordinal', 'scale': {'domain': BINS}, 'title': 'Length of stay (days on site)', 'axis': {'labelAngle': 0}}
ORIGIN = {'domain': ['Malaysia', 'Other countries'], 'range': [MY, OTHER]}
def half_year(name, title, first, after, domain):
    """One Gantt panel: placements that started in this half of 2025. Both panels use a 197-day x domain, so they share one scale."""
    return {'name': name, 'width': 620, 'height': {'step': 11},
            'title': {'text': title, 'anchor': 'start', 'fontSize': 14, 'color': INK, 'offset': 4},
            'transform': [{'filter': {'field': 'start', 'gte': first}}, {'filter': {'field': 'start', 'lt': after}}],
            'mark': {'type': 'bar', 'height': 8, 'cornerRadius': 1.5},
            'encoding': {
                'y': {'field': 'placement', 'type': 'nominal', 'sort': {'field': 'start'}, 'title': None,
                      'axis': {'labels': False, 'ticks': False, 'domain': False, 'grid': True, 'gridColor': '#efece2'}},
                'x': {'field': 'start', 'type': 'temporal', 'title': None, 'scale': {'domainMin': domain[0], 'domainMax': domain[1]},
                      'axis': {'format': '%b', 'tickCount': {'interval': 'month'}, 'orient': 'top', 'labelColor': INK, 'labelFontSize': 13}},
                'x2': {'field': 'end'},
                'color': {'field': 'origin_group', 'type': 'nominal', 'title': 'Volunteer from', 'scale': ORIGIN,
                          'legend': {'orient': 'top', 'direction': 'horizontal'}},
                'tooltip': [{'field': 'origin', 'title': 'Listed origin'},
                            {'field': 'start', 'type': 'temporal', 'title': 'Start', 'format': '%d %b %Y'},
                            {'field': 'end', 'type': 'temporal', 'title': 'End', 'format': '%d %b %Y'},
                            {'field': 'days', 'type': 'quantitative', 'title': 'Days on site'}]}}
JAN, JUL = {'year': 2025, 'month': 1, 'date': 1}, {'year': 2025, 'month': 7, 'date': 1}
save('11-placement-gantt.json', {
    'description': 'Gantt chart of 57 volunteer placements at BSBCC in 2025 (two half-year panels), linked to a histogram of placement length. Drag across either timeline to select placements that started in that period.',
    'usermeta': {'fitWidth': 1010},  # js/app.js scales the fixed widths below to the page column
    'data': {'url': 'data/bsbcc-placements-2025.json'},
    'params': [{'name': 'brush', 'select': {'type': 'interval', 'encodings': ['x']}, 'views': ['firstHalf', 'secondHalf']}],
    'hconcat': [
        {'vconcat': [half_year('firstHalf', 'Started January–June', JAN, JUL, [JAN, {'year': 2025, 'month': 7, 'date': 17}]),
                     half_year('secondHalf', 'Started July–December', JUL, {'year': 2026, 'month': 1, 'date': 1}, [JUL, {'year': 2026, 'month': 1, 'date': 14}])],
         'spacing': 22, 'resolve': {'scale': {'x': 'independent'}}},   # each half-year has its own dates
        {'width': 290, 'height': 250,
         'layer': [
             {'transform': [{'filter': {'param': 'brush'}},
                            {'aggregate': [{'op': 'count', 'as': 'n'}, {'op': 'sum', 'field': 'days', 'as': 'd'}, {'op': 'median', 'field': 'days', 'as': 'm'}]},
                            {'calculate': "[(length(data('brush_store')) ? 'Selected: ' : 'All: ') + datum.n + (datum.n == 1 ? ' placement' : ' placements'),"
                                          " format(datum.d, ',') + ' total placement-days', 'Median stay: ' + datum.m + ' days']", 'as': 't'}],
              'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'fontSize': 14, 'fontWeight': 700, 'lineHeight': 19, 'color': INK},
              'encoding': {'x': {'value': 0}, 'y': {'value': -78}, 'text': {'field': 't'}}},
             {'transform': WEEK_BIN,
              'mark': {'type': 'bar', 'fill': PAPER, 'stroke': MARK, 'strokeWidth': 1.5, 'strokeDash': [3, 2]},
              'encoding': {'x': HX, 'y': {'aggregate': 'count', 'type': 'quantitative', 'title': 'Placements', 'scale': {'domain': [0, 45]}, 'axis': {'tickCount': 5}}}},
             {'transform': [{'filter': {'param': 'brush'}}] + WEEK_BIN,
              'mark': {'type': 'bar', 'color': MY, 'stroke': PAPER, 'strokeWidth': 2},
              'encoding': {'x': HX, 'y': {'aggregate': 'count', 'type': 'quantitative'},
                           'tooltip': [{'field': 'range', 'title': 'Days on site'},
                                       {'aggregate': 'count', 'type': 'quantitative', 'title': 'Placements'}]}},
             {'data': {'values': [{'range': '8–14', 'n': 38}]},
              'mark': {'type': 'text', 'text': '38 of 57 stayed two weeks or less', 'align': 'left', 'dx': -16, 'dy': -8,
                       'baseline': 'bottom', 'color': INK, 'fontSize': 12.5, 'fontWeight': 600},
              'encoding': {'x': {'field': 'range', 'type': 'ordinal'}, 'y': {'field': 'n', 'type': 'quantitative'}}}]},
    ],
    'spacing': 36,
})

# ---- Context (not counted): national handover totals beside the bump chart --
save('context-national-totals.json', {
    'description': 'Small bar chart of total animals handed over to PERHILITAN each year, 2021-2024.',
    'width': 220, 'height': 70,
    'data': {'url': 'data/handovers-national.json'},
    'encoding': {'x': {'field': 'year', 'type': 'ordinal', 'title': None, 'axis': {'labelAngle': 0, 'labelColor': INK, 'labelFontSize': 13}},
                 'y': {'field': 'total', 'type': 'quantitative', 'axis': None, 'scale': {'domain': [0, 17000]}},
                 'tooltip': [{'field': 'year', 'title': 'Year'}, {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','},
                             {'field': 'source', 'title': 'Source'}]},
    'layer': [
        {'mark': {'type': 'bar', 'width': 24, 'cornerRadiusEnd': 2},
         'encoding': {'color': {'condition': {'test': '!datum.state_table', 'value': '#b9b39f'}, 'value': MARK}}},
        {'mark': {'type': 'text', 'dy': -5, 'baseline': 'bottom', 'fontSize': 12, 'fontWeight': 600},
         'encoding': {'text': {'field': 'total', 'format': ','}}},
    ],
})

# ---- Context inset (not counted): Sabah places named in section 2 ------
save('context-sabah-map.json', {
    'description': 'Locator map of Sabah showing BSBCC at Sepilok and Tabin Wildlife Reserve.',
    'width': 280, 'height': 190,
    'projection': {'type': 'mercator'},
    'layer': [
        {'data': {'url': 'data/borneo-states.geojson', 'format': {'type': 'json', 'property': 'features'}},
         'transform': [{'filter': "datum.properties.state == 'Sabah'"}],
         'mark': {'type': 'geoshape', 'fill': '#e3ddc9', 'stroke': PAPER, 'strokeWidth': 1}},
        {'data': {'values': [{'longitude': 116.55, 'latitude': 5.45, 't': 'SABAH'}]},
         'mark': {'type': 'text', 'fontSize': 12, 'letterSpacing': 2, 'color': MUTED, 'fontWeight': 600},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'}, 'text': {'field': 't'}}},
        {'data': {'url': 'data/sabah-places.json'},
         'mark': {'type': 'circle', 'size': 70, 'color': INK, 'stroke': PAPER, 'strokeWidth': 1.5},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'},
                      'tooltip': [{'field': 'place', 'title': 'Place'}, {'field': 'role', 'title': 'Role'}]}},
        {'data': {'url': 'data/sabah-places.json'}, 'transform': [{'filter': "datum.place == 'BSBCC, Sepilok'"}],
         'mark': {'type': 'text', 'align': 'right', 'dx': -8, 'dy': -8, 'fontSize': 12, 'fontWeight': 600},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'}, 'text': {'field': 'place'}}},
        {'data': {'url': 'data/sabah-places.json'}, 'transform': [{'filter': "datum.place != 'BSBCC, Sepilok'"}],
         'mark': {'type': 'text', 'align': 'right', 'dx': -8, 'dy': 10, 'fontSize': 12, 'fontWeight': 600},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'}, 'text': {'field': 'place'}}},
    ],
})
print('Step 3 done: chart specs written to charts/.')
