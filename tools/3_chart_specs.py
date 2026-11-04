"""Step 3 of 3: the Vega-Lite specifications (run from the website folder: python tools/3_chart_specs.py).

Writes every chart as readable JSON in charts/. One shared config (font, palette) keeps all
charts consistent. Patterns for layered maps, lookups, bound selectors
and the linked views are adapted from the FIT3179/Vega-Lite teaching examples.
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
GROUP = {'Reptiles': '#0072B2', 'Mammals': '#B26F00', 'Birds': '#8F3F72'}   # Okabe-Ito hues, darkened so every mark reaches 3:1 contrast
SEQ = ['#f7ed9e', '#a1dab4', '#41b6c4', '#2171b5', '#253494', '#020c33']   # ColorBrewer YlGnBu; lightest step deepened so it shows against the page, darkest step deepened so the top two classes stay apart for colour-blind readers
MARK = '#3e5260'                                                             # neutral slate for single-series marks
MY, OTHER = '#00525a', '#8a8270'   # Malaysia in deep teal (checked against grey for all three colour-blind types), other countries in neutral grey; no other chart uses these
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
LAND, BORDER = '#e6e0cf', '#a39b86'   # land, and coast and state borders
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
    'width': 240, 'height': 240,   # fits a half-width column at 1024 px, so the side text shares the page's column line
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
# Map 02: every circle is joined to its label by a leader line.
CIRCLE_LABELS = [lab('Perlis', 99.85, 6.62, 'right', True), lab('Kedah', 99.85, 6.08, 'right', True),
    lab('Pulau Pinang', 99.85, 5.42, 'right', True), lab('Perak', 100.2, 4.5, 'right', True),
    lab('Kelantan', 102.6, 6.4, 'left', True), lab('Terengganu', 103.55, 5.2, 'left', True),
    lab('Pahang', 103.75, 3.75, 'left', True), lab('Selangor', 100.85, 3.62, 'right', True),
    lab('Wilayah Persekutuan', 100.95, 3.08, 'right', True, 'Federal Territories'),
    lab('Negeri Sembilan', 101.15, 2.6, 'right', True), lab('Melaka', 101.7, 2.08, 'right', True),
    lab('Johor', 104.15, 2.1, 'left', True)]   # all labels sit in the sea, outside the coastline
# Selangor's centre is so close to Kuala Lumpur that its circle covered the Federal Territories circle,
# so map 02 draws it a little north-west, still inside Selangor.
MOVED = {'Selangor': (101.3, 3.45)}
SHARE_LABELS = [lab('Perlis', 99.85, 6.62, 'right', True), lab('Pulau Pinang', 99.85, 5.42, 'right', True),
    lab('Melaka', 101.7, 2.08, 'right', True), lab('Kedah', 100.66, 5.92, 'center', False),
    lab('Perak', 101.11, 4.77, 'center', False), lab('Kelantan', 102.03, 5.28, 'center', False),
    lab('Terengganu', 102.95, 4.94, 'center', False), lab('Pahang', 102.54, 3.74, 'center', False),
    lab('Selangor', 100.85, 3.6, 'right', True), lab('Negeri Sembilan', 102.21, 2.78, 'center', False),
    lab('Wilayah Persekutuan', 100.95, 3.08, 'right', True, 'Federal Territories'),
    lab('Johor', 103.38, 2.05, 'center', False)]
WP_POINT = {'state': 'Wilayah Persekutuan', 'longitude': 101.69, 'latitude': 3.12}   # Kuala Lumpur, where the combined figure is drawn
def moved(axis, field):
    """Expression for a state's drawing position: the state centre, unless MOVED gives another point."""
    i = 0 if axis == 'lon' else 1
    return ''.join(f"datum.state == '{st}' ? {pos[i]} : " for st, pos in MOVED.items()) + field
def leader_lines(labels, anchors_url='data/state-anchors.json', use_moved=False):
    """Thin grey lines from each label back to its state (or its moved circle)."""
    lon = moved('lon', 'datum.longitude') if use_moved else 'datum.longitude'
    lat = moved('lat', 'datum.latitude') if use_moved else 'datum.latitude'
    return {'data': {'values': [d for d in labels if d['leader']]},
            'transform': [{'lookup': 'state', 'from': {'data': {'url': anchors_url}, 'key': 'state', 'fields': ['longitude', 'latitude']}},
                          {'calculate': f"isValid(datum.longitude) ? {lon} : 101.69", 'as': 'ax'},
                          {'calculate': f"isValid(datum.latitude) ? {lat} : 3.12", 'as': 'ay'}],
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
        leader_lines(CIRCLE_LABELS, use_moved=True),   # drawn before the circles, so each line ends under its circle
        {'data': {'values': [WP_POINT]},   # Federal Territories: one combined figure, drawn at Kuala Lumpur
         'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                     'fields': ['total', 'reptiles', 'mammals', 'birds']}},
                       {'calculate': "'Federal Territories (combined)'", 'as': 'state'}],
         'mark': {'type': 'circle', 'color': MARK, 'stroke': PAPER, 'strokeWidth': 1.5, 'opacity': 1},
         'encoding': {'longitude': {'field': 'longitude', 'type': 'quantitative'}, 'latitude': {'field': 'latitude', 'type': 'quantitative'},
                      'size': {'field': 'total', 'type': 'quantitative'},
                      'tooltip': [{'field': 'state', 'title': 'Reporting unit'}, {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','}]}},
        {'data': {'url': 'data/state-anchors.json'},
         'transform': [{'calculate': moved('lon', 'datum.longitude'), 'as': 'x_lon'}, {'calculate': moved('lat', 'datum.latitude'), 'as': 'x_lat'}],
         'mark': {'type': 'circle', 'color': MARK, 'stroke': PAPER, 'strokeWidth': 1.5, 'opacity': 1, 'cursor': 'pointer'},   # solid, so leader lines stop at the circle edge
         'encoding': {
             'longitude': {'field': 'x_lon', 'type': 'quantitative'},
             'latitude': {'field': 'x_lat', 'type': 'quantitative'},
             'size': {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over',
                      'scale': {'range': [0, 1900], 'zero': True},
                      'legend': None},   # every circle is labelled with its count, so no size key is needed
             'tooltip': [{'field': 'state', 'type': 'nominal', 'title': 'Reporting state'},
                         {'field': 'total', 'type': 'quantitative', 'title': 'Animals handed over', 'format': ','},
                         {'field': 'reptiles', 'type': 'quantitative', 'title': 'Reptiles', 'format': ','},
                         {'field': 'mammals', 'type': 'quantitative', 'title': 'Mammals', 'format': ','},
                         {'field': 'birds', 'type': 'quantitative', 'title': 'Birds', 'format': ','}]}},
    ] + [{'data': {'values': [d for d in CIRCLE_LABELS if d['align'] == a]},
          'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state', 'fields': ['total']}},
                        {'calculate': "[datum.name, format(datum.total, ',')]", 'as': 'label'}],
          'mark': {'type': 'text', 'align': a, 'dx': 4 if a == 'left' else -4, 'fontSize': 12, 'fontWeight': 600, 'lineHeight': 14, 'baseline': 'middle'},
          'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                       'text': {'field': 'label'}}} for a in ('left', 'right')],
})

# ---- 03 Choropleth: animals per 1,000 km2, or one group's share ------
# "All animals" (the default) is normalised by land area: animals handed over per 1,000 km2, with the
# area measured from the boundary file in step 1. Choosing a group shows that group's share of each
# state's handovers instead. Either way the measure is a rate, never a raw count (map 02 shows counts).
share = ("(groupChoice == 'All animals' ? datum.per_1000_km2 : groupChoice == 'Mammals' ? datum.mammals / datum.total : "
         "groupChoice == 'Reptiles' ? datum.reptiles / datum.total : datum.birds / datum.total)")
# Manual class breaks (Week 9 classification) chosen separately for each view, because they live on very
# different ranges: birds never exceed 3.4% of a state's handovers, reptiles never fall below 38%, and
# the density runs from 16 (Pahang) to 2,442 (Pulau Pinang) animals per 1,000 km2.
BREAKS = {'All animals': [25, 50, 100, 200, 500],
          'Mammals': [0.02, 0.04, 0.07, 0.10, 0.25], 'Reptiles': [0.50, 0.90, 0.93, 0.96, 0.98], 'Birds': [0.005, 0.01, 0.015, 0.02, 0.03]}
GROUPS_03 = ['All animals', 'Reptiles', 'Mammals', 'Birds']
def _cls(b):
    return " : ".join([f"datum.share < {v} ? {i}" for i, v in enumerate(b)]) + " : 5"
cls = " : ".join(f"groupChoice == '{g}' ? ({_cls(BREAKS[g])})" for g in GROUPS_03[:-1]) + f" : ({_cls(BREAKS['Birds'])})"
def _labels(b, density=False):
    f = (lambda v: f"{v:,}") if density else (lambda v: (f"{v*100:.1f}".rstrip('0').rstrip('.')) + '%')
    return [f"< {f(b[0])}"] + [f"{f(b[i])}–{f(b[i+1])}" for i in range(len(b) - 1)] + [f"≥ {f(b[-1])}"]   # same symbols as the heatmap legend
LEGEND_EXPR = ("(" + " : ".join(f"groupChoice == '{g}' ? " + json.dumps(_labels(BREAKS[g], g == 'All animals')) for g in GROUPS_03[:-1]) +
               " : " + json.dumps(_labels(BREAKS['Birds'])) + ")[datum.value]")
LABEL_03 = ("groupChoice == 'All animals' ? format(datum.share, ',.0f') : datum.share < 0.1 ? format(datum.share, '.1%') : format(datum.share, '.0%')")
COUNT_03 = ("groupChoice == 'Mammals' ? datum.mammals : groupChoice == 'Reptiles' ? datum.reptiles : "
            "groupChoice == 'Birds' ? datum.birds : datum.total")
# Tooltip, legend heading and (in js/app.js) the chart heading all follow the "Show" menu, so only the chosen
# measure and its units are shown. A Vega tooltip can be an object, so its rows change with the view.
def _tip(g):
    if g == 'All animals':
        return ("{'State': datum.name, 'Animals per 1,000 km²': format(datum.per_1000_km2, ',.0f'), "
                "'Animals handed over': format(datum.total, ','), 'Land area (km²)': format(datum.area_km2, ',')}")
    return (f"{{'State': datum.name, 'Share that were {g.lower()}': format(datum.share, '.1%'), "
            f"'{g} handed over': format(datum.count, ','), 'All animals handed over': format(datum.total, ',')}}")
TIP_03 = " : ".join(f"groupChoice == '{g}' ? {_tip(g)}" for g in GROUPS_03[:-1]) + " : " + _tip(GROUPS_03[-1])
LEGEND_TITLE_03 = ("groupChoice == 'All animals' ? 'Animals handed over per 1,000 km² of land' : "
                   "'Share of each state’s handovers that were ' + lower(groupChoice)")
save('03-group-share-map.json', {
    'description': "Choropleth: animals handed over per 1,000 km2 in each state (default), or the chosen animal group's share of each state's 2024 handovers, in fixed classes.",
    'width': 'container', 'height': 470, 'padding': {'left': 72, 'top': 5, 'right': 5, 'bottom': 5},
    'params': [{'name': 'groupChoice', 'value': 'All animals',
                'bind': {'input': 'select', 'options': GROUPS_03, 'name': 'Show: ', 'element': '#share-map-control'}}],
    'projection': {'type': 'mercator'},
    'layer': [
        {'data': GEO,
         # Kuala Lumpur and Putrajaya both take the one combined Federal Territories figure (which also covers Labuan)
         'transform': [{'calculate': "indexof(['Kuala Lumpur', 'Putrajaya'], datum.properties.state) >= 0 ? 'Wilayah Persekutuan' : datum.properties.state", 'as': 'unit'},
                       {'calculate': "datum.unit == 'Wilayah Persekutuan' ? 'Federal Territories (combined)' : datum.unit", 'as': 'name'},
                       {'lookup': 'unit', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                              'fields': ['reptiles', 'mammals', 'birds', 'total', 'area_km2', 'per_1000_km2']}},
                       {'filter': 'isValid(datum.total)'},
                       {'calculate': share, 'as': 'share'},
                       {'calculate': COUNT_03, 'as': 'count'},
                       {'calculate': cls, 'as': 'cls'}],
         'mark': {'type': 'geoshape', 'stroke': BORDER, 'strokeWidth': 0.9, 'tooltip': {'expr': TIP_03}},
         'encoding': {
             'color': {'field': 'cls', 'type': 'ordinal', 'title': 'Colour class (classes change with the view)',
                       'scale': {'domain': [0, 1, 2, 3, 4, 5], 'range': SEQ},
                       'legend': {'labelExpr': LEGEND_EXPR, 'orient': 'bottom', 'direction': 'horizontal', 'columns': 4, 'title': None, 'offset': 34,
                                  'symbolType': 'square', 'symbolSize': 220, 'symbolStrokeColor': '#9c9686', 'symbolStrokeWidth': 0.5,
                                  'labelLimit': 160, 'columnPadding': 14}}}},
        # the legend heading is a text mark, because a legend title cannot change with the menu
        {'data': {'values': [{}]},
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'fontSize': 13, 'fontWeight': 600, 'color': INK},
         'encoding': {'x': {'value': 0}, 'y': {'value': {'expr': 'height + 10'}}, 'text': {'value': {'expr': LEGEND_TITLE_03}}}},
        leader_lines(SHARE_LABELS),
    ] + [{'data': {'values': [d for d in SHARE_LABELS if d['leader'] == offshore]},
          'transform': [{'lookup': 'state', 'from': {'data': {'url': 'data/handovers-2024.json'}, 'key': 'state',
                                                      'fields': ['reptiles', 'mammals', 'birds', 'total', 'area_km2', 'per_1000_km2']}},
                        {'calculate': share, 'as': 'share'}, {'calculate': cls, 'as': 'cls'}, {'calculate': COUNT_03, 'as': 'count'},
                        {'calculate': "[datum.name, " + LABEL_03 + "]", 'as': 'label'}],
          # offshore labels sit in the sea (dark text); the rest sit on their state (white on dark classes)
          'mark': {'type': 'text', 'fontSize': 12, 'fontWeight': 700, 'lineHeight': 13, 'baseline': 'middle',
                   'align': 'right' if offshore else 'center', 'dx': -4 if offshore else 0, 'tooltip': {'expr': TIP_03}},
          'encoding': {'longitude': {'field': 'lon', 'type': 'quantitative'}, 'latitude': {'field': 'lat', 'type': 'quantitative'},
                       'text': {'field': 'label'},
                       'color': {'value': INK} if offshore else {'condition': {'test': 'datum.cls >= 3', 'value': 'white'}, 'value': INK}}}
         for offshore in (False, True)],
})

# ---- 04 Change bars: how each state's handovers changed, 2021 to 2024 ----
# One bar per state, sorted from the biggest rise to the biggest fall. Rises go right of zero and falls go
# left, and every bar is labelled with the change and both counts, so one neutral colour is enough: the same
# slate as the animal counts in maps 02 and 07, and not a colour that means a group or an origin elsewhere. (Map 02 already shows the 2024 totals; this chart shows the change.)
RISE = FALL = MARK
trend = json.loads((ROOT / 'data/handovers-trend.json').read_text(encoding='utf8'))
by = {(r['state'], r['year']): r['total'] for r in trend}
CHANGE_ORDER = sorted({r['state'] for r in trend}, key=lambda st: -(by[(st, 2024)] - by[(st, 2021)]))   # biggest rise first
change_label = ("(datum.change >= 0 ? '+' : '−') + format(abs(datum.change), ',') + '   (' + "
                "format(datum.y2021, ',') + ' → ' + format(datum.y2024, ',') + ')'")
save('04-state-comparison.json', {
    'description': 'Bar chart of the change in animals handed over in each state from 2021 to 2024, sorted; each bar is labelled with the change and both counts.',
    'width': 'container', 'height': 480, 'padding': 10,
    'data': {'url': 'data/handovers-trend.json'},
    'transform': [{'filter': 'datum.year == 2021 || datum.year == 2024'},
                  {'pivot': 'year', 'value': 'total', 'groupby': ['state']},
                  {'calculate': "datum['2021']", 'as': 'y2021'}, {'calculate': "datum['2024']", 'as': 'y2024'},
                  {'calculate': 'datum.y2024 - datum.y2021', 'as': 'change'}],
    'encoding': {'y': {'field': 'state', 'type': 'nominal', 'sort': CHANGE_ORDER, 'title': None,
                       'axis': {'labelColor': INK, 'labelFontSize': 13, 'ticks': False, 'labelPadding': 10,
                                'labelExpr': "datum.label == 'Wilayah Persekutuan' ? 'Federal Territories' : datum.label"}}},
    'layer': [
        {'mark': {'type': 'bar', 'height': 22, 'cornerRadiusEnd': 2},
         'encoding': {'x': {'field': 'change', 'type': 'quantitative', 'scale': {'domain': [-600, 2900]},
                            'axis': {'title': 'Change in animals handed over, 2021 to 2024', 'values': [-500, 0, 500, 1000, 1500, 2000, 2500], 'format': '+,d', 'grid': True}},
                      'color': {'condition': {'test': 'datum.change < 0', 'value': FALL}, 'value': RISE},
                      'tooltip': [{'field': 'state', 'title': 'Reporting unit'}, {'field': 'y2021', 'type': 'quantitative', 'title': '2021', 'format': ','},
                                  {'field': 'y2024', 'type': 'quantitative', 'title': '2024', 'format': ','},
                                  {'field': 'change', 'type': 'quantitative', 'title': 'Change', 'format': '+,'}]}},
        {'mark': {'type': 'rule', 'color': INK, 'strokeWidth': 1.5}, 'encoding': {'x': {'datum': 0}, 'y': None}},   # the zero line
        *[{'transform': [{'filter': test}, {'calculate': change_label, 'as': 'label'}],
           'mark': {'type': 'text', 'align': align, 'dx': dx, 'fontSize': 13, 'fontWeight': 600, 'color': colour},
           'encoding': {'x': {'field': 'change', 'type': 'quantitative'}, 'text': {'field': 'label'}}}
          for test, align, dx, colour in [('datum.change >= 0', 'left', 8, INK), ('datum.change < 0', 'right', -8, INK)]],
        *[{'data': {'values': [{'x': x, 't': t}]},   # direction cues above the zero line
           'mark': {'type': 'text', 'align': align, 'baseline': 'bottom', 'dy': -6, 'fontSize': 12, 'fontStyle': 'italic', 'color': MUTED},
           'encoding': {'x': {'field': 'x', 'type': 'quantitative'}, 'y': {'value': 0}, 'text': {'field': 't'}}}
          for x, t, align in [(30, 'More animals than in 2021 →', 'left'), (-30, '← Fewer', 'right')]],
    ],
})

# ---- 05 Heatmap: each month's share of its row's year, with year totals --
# Use the published annual totals, NOT the sum of incomplete 2023 monthly rows.
ROWS = [f'{g} · {y}' for g in GROUP for y in (2023, 2024)]
# Original vector pictograms: lizard, paw and bird. These supplement the text labels;
# they carry category identity only, never magnitude, and require no external assets.
ANIMAL_SHAPES = [
    'M-.15,-.75 Q.4,-1 .45,-.55 L.25,-.25 .8,-.45 .95,-.2 .7,-.15 .2,.05 .75,.5 .6,.7 .1,.3 Q.1,.8 -.35,1 L-.1,.45 -.25,.1 -.75,.55 -.95,.35 -.65,.25 -.25,-.15 -.75,-.4 -.7,-.65 -.2,-.45 Z',
    'M-.5,.85 Q-1,.6 -.6,.15 Q0,-.65 .6,.15 Q1,.6 .5,.85 Q0,.55 -.5,.85 Z M-.9,-.45 A.23,.3 0 1,0 -.44,-.45 A.23,.3 0 1,0 -.9,-.45 M-.35,-.8 A.23,.3 0 1,0 .11,-.8 A.23,.3 0 1,0 -.35,-.8 M.25,-.7 A.23,.3 0 1,0 .71,-.7 A.23,.3 0 1,0 .25,-.7 M.65,-.2 A.21,.28 0 1,0 1.07,-.2 A.21,.28 0 1,0 .65,-.2',
    'M-1,.6 L-.6,.15 Q-.7,-.5 -.15,-.3 Q.1,-1 .65,-.65 L1,-.35 .7,-.3 Q.8,.35 .3,.6 Q-.15,.9 -.6,.6 Z',
]
row_y = {'field': 'row', 'type': 'nominal', 'sort': ROWS, 'title': None}
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# Colour = the month's share of that row's published year total, so every row shows WHEN its group
# arrived, whatever the group's size (75 mammals or 10,968 reptiles). The year-total column shows HOW MANY.
# An even spread over the year would be about 8% a month.
BANDS = ['0', '< 5%', '5–14%', '15–29%', '≥ 30%', 'Not available']   # 0 has its own class, so '< 5%' means above 0
band = ("!datum.reported ? 'Not available' : datum.animals == 0 ? '0' : datum.share < 0.05 ? '< 5%' : "
        "datum.share < 0.15 ? '5–14%' : datum.share < 0.30 ? '15–29%' : '≥ 30%'")
save('05-intake-heatmap.json', {
    'description': 'Monthly intake with 2023 and 2024 paired for each animal group. Each cell shows the month as a share of that row\'s published year total; the year totals are printed at right.',
    'usermeta': {'fitWidth': 1050},
    'hconcat': [
        {'width': 28, 'height': 330,
         'data': {'url': 'data/nwrc-intake-totals.json'},
         'transform': [{'calculate': "datum.group + ' · ' + datum.year", 'as': 'row'}],
         'mark': {'type': 'point', 'filled': True, 'size': 220, 'color': MUTED, 'opacity': 1},
         'encoding': {'y': {**row_y, 'axis': None},
                      'shape': {'field': 'group', 'type': 'nominal', 'scale': {'domain': list(GROUP), 'range': ANIMAL_SHAPES}, 'legend': None}}},
        {'width': 720, 'height': 330,
         'data': {'url': 'data/nwrc-intake-2023-2024.json'},
         'transform': [{'calculate': "datum.group + ' · ' + datum.year", 'as': 'row'},
                       {'calculate': 'datum.animals / datum.year_total', 'as': 'share'},
                       {'calculate': band, 'as': 'band'},
                       {'calculate': "!datum.reported ? '' : datum.animals == 0 ? '0' : datum.share < 0.01 ? '<1%' : format(datum.share, '.0%')", 'as': 'label'}],
         'encoding': {
             'x': {'field': 'month', 'type': 'ordinal', 'sort': MONTHS,
                   'axis': {'title': None, 'labelAngle': 0, 'orient': 'top', 'labelColor': INK}},
             'y': {**row_y, 'axis': {'labelFontSize': 13, 'labelColor': INK, 'labelPadding': 10, 'ticks': False}},
             'tooltip': [{'field': 'month', 'title': 'Month'}, {'field': 'year', 'title': 'Year'},
                         {'field': 'group', 'title': 'Group'}, {'field': 'animals', 'type': 'quantitative', 'title': 'Animals received', 'format': ','},
                         {'field': 'share', 'type': 'quantitative', 'title': 'Share of the year', 'format': '.1%'}]},
         'layer': [
             {'mark': {'type': 'rect', 'cornerRadius': 3},
              # every cell has a thin outline, so the palest cells and the empty (0) months stay visible on the page
              'encoding': {'stroke': {'value': '#9c9686'}, 'strokeWidth': {'value': 1},
                           'color': {'field': 'band', 'type': 'ordinal', 'title': 'Share of the row’s year total that arrived in the month',
                                     'scale': {'domain': BANDS, 'range': [PAPER, SEQ[0], '#a1dab4', '#41b6c4', '#225ea8', '#d6d0bf']},
                                     'legend': {'orient': 'bottom', 'direction': 'horizontal', 'symbolType': 'square', 'titleLimit': 600,
                                                'symbolStrokeColor': '#bdb7a5', 'symbolStrokeWidth': 1}}}},
             {'mark': {'type': 'text', 'fontSize': 14, 'fontWeight': 500},
              'encoding': {'text': {'field': 'label'},
                           'color': {'condition': {'test': "datum.band == '≥ 30%'", 'value': 'white'}, 'value': INK}}},
         ]},
        {'width': 95, 'height': 330, 'title': {'text': 'Year total', 'subtitle': '= 100% of the row', 'anchor': 'middle', 'fontSize': 14, 'subtitleFontSize': 12, 'offset': 8},
         'data': {'url': 'data/nwrc-intake-totals.json'},
         'transform': [{'calculate': "datum.group + ' · ' + datum.year", 'as': 'row'}],
         'mark': {'type': 'text', 'fontSize': 17, 'fontWeight': 700},
         'encoding': {'y': {**row_y, 'axis': None}, 'text': {'field': 'animals', 'type': 'quantitative', 'format': ','},
                      'tooltip': [{'field': 'row', 'title': 'Group · year'}, {'field': 'animals', 'type': 'quantitative', 'title': 'Published annual total', 'format': ','}]}},
    ],
    'spacing': 16,
})

# ---- 06 Outcome tree: what happened to the nine BSBCC bears ------------
# A node-link tree read left to right: 9 bears -> released / still in care -> outcome -> each bear.
# The layout (positions and elbow links) is computed in tools/2_chart_data.py, like the Sankey's.
# The branches leading to the three deaths are dark; every other branch is grey.
TREE_DATA = {'url': 'data/bear-outcome-tree.json'}
TX = {'type': 'quantitative', 'scale': {'domain': [-10, 960], 'nice': False}, 'axis': None}
TY6 = {'type': 'quantitative', 'scale': {'domain': [-25, 430], 'reverse': True, 'nice': False}, 'axis': None}
died = "datum.outcome == 'Died'"
nodes = lambda test: [{'filter': "datum.type == 'node'"}, {'filter': test}]
save('06-bear-outcomes.json', {
    'description': 'Node-link tree of the nine BSBCC sun bears: released or still in care, then each outcome, ending at each bear with its key dates.',
    'usermeta': {'fitWidth': 980},   # js/app.js scales the fixed width below to the page column
    'width': 960, 'height': 450, 'padding': 10,
    'data': TREE_DATA,
    'encoding': {'x': {'field': 'x', **TX}, 'y': {'field': 'y', **TY6}},
    'layer': [
        {'transform': [{'filter': "datum.type == 'link'"}],
         'mark': {'type': 'line', 'strokeWidth': 2},
         'encoding': {'detail': {'field': 'id'}, 'order': {'field': 'step'},
                      'color': {'condition': {'test': died, 'value': INK}, 'value': '#b9b3a3'}}},
        {'transform': nodes('datum.level < 3'),
         'mark': {'type': 'circle', 'size': 110, 'opacity': 1, 'stroke': PAPER, 'strokeWidth': 2},
         'encoding': {'color': {'condition': {'test': died, 'value': INK}, 'value': '#8a8270'}}},
        {'transform': nodes('datum.level < 3'),   # group names sit just above each branch point
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'bottom', 'dx': 4, 'dy': -8, 'fontSize': 14, 'fontWeight': 700, 'color': INK},
         'encoding': {'text': {'field': 'label'}}},
        {'transform': nodes('datum.level == 3'),
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'bottom', 'dx': 10, 'dy': 1, 'fontSize': 15, 'fontWeight': 700, 'color': INK},
         'encoding': {'text': {'field': 'label'}}},
        {'transform': nodes('datum.level == 3'),   # each bear's key dates, under its name
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'dx': 10, 'dy': 3, 'fontSize': 13, 'color': MUTED},
         'encoding': {'text': {'field': 'detail'}}},
    ],
})

# ---- 07 Flow map: NWRC to named release areas --------------------------
SITES = {'url': 'data/release-sites.json'}
def site_labels(names, align, dx):
    return {'data': SITES,
            'transform': [{'filter': {'field': 'site', 'oneOf': names}},
                          {'calculate': "[datum.site, datum.animals + (datum.animals == 1 ? ' animal' : ' animals')]", 'as': 'label'}],
            'mark': {'type': 'text', 'align': align, 'dx': dx, 'fontSize': 12, 'fontWeight': 600, 'lineHeight': 15, 'cursor': 'pointer'},
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
                                      'title': 'Animals released', 'legend': {'values': [1, 4, 6, 13], 'orient': 'bottom-left', 'symbolType': 'stroke', 'symbolSize': 1600, 'labelFontSize': 13}}}},
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
              'mark': {'type': 'text', 'align': 'right', 'dx': -5, 'fontSize': 12, 'lineHeight': 15, 'color': INK},
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
         'mark': {'type': 'text', 'align': 'right', 'dx': -8, 'dy': -6, 'fontSize': 12, 'fontWeight': 700, 'letterSpacing': 1.5, 'baseline': 'bottom'},
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
PROG = {'domain': ['Volunteers', 'Interns'], 'range': [INK, '#7a766b']}   # near-black and mid grey: they differ in lightness, not hue
PROG_LEGEND = {'orient': 'top', 'direction': 'horizontal', 'title': None, 'symbolType': 'stroke', 'symbolStrokeWidth': 3, 'symbolSize': 700, 'labelFontSize': 13, 'columnPadding': 24}
save('09-volunteer-lines.json', {
    'description': 'Line chart: volunteers and interns reported by BSBCC each year, 2021-2025.',
    'width': 'container', 'height': 300,
    'data': {'url': 'data/bsbcc-participation-2021-2025.json'},
    'padding': {'right': 20},
    'encoding': {'x': {'field': 'year', 'type': 'ordinal', 'title': None, 'axis': {'labelAngle': 0, 'labelFontSize': 13, 'labelColor': INK}},
                 'y': {'field': 'people', 'type': 'quantitative', 'title': 'People', 'scale': {'domain': [0, 65]}, 'axis': {'tickCount': 4}},
                 # one legend: colour, dash and marker all describe the same programme field, so Vega-Lite merges them
                 'color': {'field': 'programme', 'type': 'nominal', 'scale': PROG, 'legend': PROG_LEGEND},
                 'tooltip': [{'field': 'programme', 'title': 'Programme'}, {'field': 'year', 'title': 'Year'},
                             {'field': 'people', 'type': 'quantitative', 'title': 'People'}, {'field': 'note', 'title': 'Note'}]},
    'layer': [
        {'mark': {'type': 'line', 'strokeWidth': 3},
         'encoding': {'strokeDash': {'field': 'programme', 'type': 'nominal', 'scale': {'domain': ['Volunteers', 'Interns'], 'range': [[1, 0], [6, 4]]}, 'legend': PROG_LEGEND}}},
        {'mark': {'type': 'point', 'filled': True, 'size': 80, 'opacity': 1},
         'encoding': {'shape': {'condition': {'test': "datum.programme == 'Interns'", 'value': 'square'}, 'value': 'circle'}}},   # a fixed value, so the legend shows only the line style
        {'transform': [{'filter': "datum.programme == 'Volunteers'"}],
         'mark': {'type': 'text', 'dy': -14, 'fontSize': 13, 'fontWeight': 600}, 'encoding': {'text': {'field': 'people'}, 'color': {'value': INK}}},
        {'transform': [{'filter': "datum.programme == 'Interns'"}],
         'mark': {'type': 'text', 'dy': 17, 'fontSize': 13, 'fontWeight': 600}, 'encoding': {'text': {'field': 'people'}, 'color': {'value': INK}}},
        {'transform': [{'filter': 'datum.year == 2025'}],
         'mark': {'type': 'text', 'align': 'left', 'dx': 12, 'dy': 4, 'fontSize': 14, 'fontWeight': 600},
         'encoding': {'text': {'field': 'programme'}, 'color': {'value': INK}}},
        {'data': {'values': [{'year': 2021, 'people': 60}]},   # the 2021 caveat, above that year
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'dx': -8, 'fontSize': 12, 'fontStyle': 'italic', 'lineHeight': 15, 'color': MUTED,
                  'text': ['2021 report also mentions', '2 remote volunteers;', 'unclear if among the 7']},
         'encoding': {'color': {'value': MUTED}, 'tooltip': None}},
    ],
})

# ---- 10 Treemap: where 2025 volunteers came from -------------------------
# Block positions come from tools/2_chart_data.py (squarified layout); area = placements.
TREE = {'url': 'data/volunteer-origins-treemap.json'}
TX = {'type': 'quantitative', 'scale': {'domain': [0, 500]}, 'axis': None}
TY = {'type': 'quantitative', 'scale': {'domain': [0, 300], 'reverse': True}, 'axis': None}
save('10-volunteer-origins.json', {
    'description': 'Treemap: 2025 BSBCC volunteer placements by listed country of origin; block area shows placements.',
    'width': 'container', 'height': 300,
    'padding': {'top': 26, 'left': 2, 'right': 2, 'bottom': 2},
    'data': TREE,
    'layer': [
        {'transform': [{'filter': "datum.level == 'country'"}],
         'mark': {'type': 'rect', 'stroke': PAPER, 'strokeWidth': 2},
         'encoding': {'x': {'field': 'x', **TX}, 'x2': {'field': 'x2'}, 'y': {'field': 'y', **TY}, 'y2': {'field': 'y2'},
                      'color': {'field': 'group', 'type': 'nominal', 'legend': None,
                                'scale': {'domain': ['Malaysia', 'Other countries'], 'range': [MY, OTHER]}},
                      'tooltip': [{'field': 'origin', 'title': 'Listed origin'}, {'field': 'placements', 'type': 'quantitative', 'title': 'Placements'}]}},
        {'transform': [{'filter': "datum.level == 'group'"}],   # a wider gap between Malaysia and the other countries
         'mark': {'type': 'rect', 'fillOpacity': 0, 'stroke': PAPER, 'strokeWidth': 6},
         'encoding': {'x': {'field': 'x', **TX}, 'x2': {'field': 'x2'}, 'y': {'field': 'y', **TY}, 'y2': {'field': 'y2'}}},
        {'transform': [{'filter': "datum.level == 'country'"}],
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'top', 'dx': 8, 'dy': 7, 'fontSize': 13, 'fontWeight': 700, 'lineHeight': 16},
         'encoding': {'x': {'field': 'x', **TX}, 'y': {'field': 'y', **TY}, 'text': {'field': 'label'},
                      'color': {'condition': {'test': "datum.group == 'Malaysia'", 'value': 'white'}, 'value': '#141c19'}}},
        {'transform': [{'filter': "datum.level == 'group'"},
                       {'calculate': "datum.group == 'Malaysia' ? 'From Malaysia · ' + datum.placements : 'From eight other countries · ' + datum.placements", 'as': 'head'}],
         'mark': {'type': 'text', 'align': 'left', 'baseline': 'bottom', 'dx': 2, 'dy': -8, 'fontSize': 13, 'fontWeight': 700, 'color': INK},
         'encoding': {'x': {'field': 'x', **TX}, 'y': {'value': 0}, 'text': {'field': 'head'}}},
    ],
})

# ---- 11 Monthly placement starts + 12 linked lengths of stay -----------
# Counts come from the same 57 anonymised placements; starts are not occupancy.
# Chart 12 is an isotype: one person figure per placement, in a row for each length of stay.
# Within a row, volunteers from Malaysia come first, then a gap, then other countries.
STAYS = ['Under 2 weeks', 'Exactly 2 weeks', '2 to 4 weeks', 'Over 4 weeks']
STAY_DAYS = {'Under 2 weeks': '11–13 days', 'Exactly 2 weeks': '14 days', '2 to 4 weeks': '15–28 days', 'Over 4 weeks': '29–39 days'}
stay_of = "datum.days <= 13 ? 'Under 2 weeks' : datum.days == 14 ? 'Exactly 2 weeks' : datum.days <= 28 ? '2 to 4 weeks' : 'Over 4 weeks'"
PERSON = 'M0,-1A.3,.3 0 1,1 0,-.4A.3,.3 0 1,1 0,-1ZM-.55,1L-.55,.05Q-.55,-.3 -.25,-.3L.25,-.3Q.55,-.3 .55,.05L.55,1Z'   # head and body, drawn here
figures = [
    {'calculate': stay_of, 'as': 'stay'},
    {'window': [{'op': 'row_number', 'as': 'k'}], 'groupby': ['stay'], 'sort': [{'field': 'origin_group'}, {'field': 'start'}]},
    {'calculate': "datum.k - 1 + (datum.origin_group == 'Malaysia' ? 0 : 1)", 'as': 'slot'}]   # +1 leaves the gap
SY = {'field': 'stay', 'type': 'ordinal', 'scale': {'domain': STAYS}, 'title': None,
      'axis': {'labelFontSize': 13, 'labelColor': INK, 'labelPadding': 10, 'ticks': False, 'domain': False,
               'labelExpr': '[datum.value, ' + json.dumps(STAY_DAYS) + '[datum.value]]'}}   # second line: the days in each row
SX = {'field': 'slot', 'type': 'quantitative', 'scale': {'domain': [-0.6, 21.8], 'nice': False}, 'axis': None}
monthly_counts = [
    {'aggregate': [{'op': 'count', 'as': 'placements'}], 'groupby': ['month', 'origin_group']},
    {'calculate': "datum.origin_group == 'Malaysia' ? 0 : 1", 'as': 'group_order'},
    {'stack': 'placements', 'groupby': ['month'], 'sort': [{'field': 'group_order'}], 'as': ['bottom', 'top']},
    {'calculate': '(datum.bottom + datum.top) / 2', 'as': 'middle'}]
save('11-placement-months.json', {
    'description': 'Monthly volunteer placement starts, split by origin, linked to an isotype of stay lengths (one person figure per placement). All counts are labelled. Select a month by click or menu; All months resets.',
    'usermeta': {'fitWidth': 1100, 'mobileStack': True},
    'data': {'url': 'data/bsbcc-placements-2025.json'},
    'transform': [{'calculate': "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][toNumber(substring(datum.start, 5, 7)) - 1]", 'as': 'month'}],
    'params': [{'name': 'selectedMonth', 'value': 'All months',
                'bind': {'input': 'select', 'options': ['All months'] + MONTHS, 'name': 'Month: ', 'element': '#placement-control'}}],
    'hconcat': [
        {'width': 440, 'height': 300,
         'title': {'text': '11 · Placements by start month', 'subtitle': '2025 · new arrivals each month', 'fontSize': 17, 'subtitleFontSize': 13, 'offset': 18},
         'encoding': {'x': {'field': 'month', 'type': 'ordinal', 'sort': MONTHS,
                            'axis': {'title': 'Start month · 2025', 'labelAngle': 0, 'labelFontSize': 13}},
                      'y': {'field': 'top', 'type': 'quantitative', 'title': 'Placements starting',
                            'scale': {'domain': [0, 14]}, 'axis': {'values': [0, 3, 6, 9, 12]}}},
         'layer': [
             {'transform': monthly_counts,
              'mark': {'type': 'bar', 'stroke': PAPER, 'strokeWidth': 1, 'cursor': 'pointer'},
              'encoding': {'y2': {'field': 'bottom'},
                           'color': {'field': 'origin_group', 'type': 'nominal', 'title': None,
                                     'scale': {'domain': ['Malaysia', 'Other countries'], 'range': [MY, OTHER]},
                                     'legend': {'orient': 'top', 'symbolType': 'square', 'labelFontSize': 13}},
                           'tooltip': [{'field': 'month', 'title': 'Start month'}, {'field': 'origin_group', 'title': 'Origin'},
                                       {'field': 'placements', 'title': 'Placements in this group', 'type': 'quantitative'}]}},
             {'transform': monthly_counts,
              'mark': {'type': 'text', 'fontSize': 13, 'fontWeight': 700, 'cursor': 'pointer'},
              'encoding': {'y': {'field': 'middle', 'type': 'quantitative'}, 'text': {'field': 'placements'},
                           'color': {'condition': {'test': "datum.origin_group == 'Malaysia'", 'value': 'white'}, 'value': '#141c19'}}},
             {'transform': [{'aggregate': [{'op': 'count', 'as': 'total'}], 'groupby': ['month']}],
              'mark': {'type': 'text', 'dy': -9, 'fontSize': 15, 'fontWeight': 700, 'cursor': 'pointer'},
              'encoding': {'y': {'field': 'total', 'type': 'quantitative'}, 'text': {'field': 'total'}}},
             # the chosen month gets a dark outline; no fading, so the page keeps two colours only
             {'transform': [{'aggregate': [{'op': 'count', 'as': 'total'}], 'groupby': ['month']}, {'filter': 'datum.month == selectedMonth'}],
              'mark': {'type': 'bar', 'fillOpacity': 0, 'stroke': INK, 'strokeWidth': 3},
              'encoding': {'y': {'field': 'total', 'type': 'quantitative'}, 'y2': {'datum': 0}}},
         ]},
        {'width': 400, 'height': 280,
         'title': {'text': '12 · Placements by length of stay', 'subtitle': {'expr': "selectedMonth == 'All months' ? 'Each figure is one placement · 38 of 57 stayed two weeks or less' : 'Solid: placements starting in ' + selectedMonth + ' · outline: other months'"},
                   'fontSize': 17, 'subtitleFontSize': 13, 'offset': 18},
         'layer': [
             # figures from the chosen month (or all) are solid; the rest become outlines in the same colour
             *[{'transform': figures + [{'filter': ('' if solid else '!') + "(selectedMonth == 'All months' || datum.month == selectedMonth)"}],
                'mark': {'type': 'point', 'shape': PERSON, 'filled': solid, 'opacity': 1, 'size': 330, 'strokeWidth': 0 if solid else 1.2, 'cursor': 'pointer'},
                'encoding': {'x': SX, 'y': SY,
                             'color': {'field': 'origin_group', 'type': 'nominal', 'title': None, 'scale': {'domain': ['Malaysia', 'Other countries'], 'range': [MY, OTHER]},
                                       'legend': {'orient': 'top', 'symbolType': 'square', 'labelFontSize': 13}},   # shared with chart 11: one legend
                             'tooltip': [{'field': 'origin', 'title': 'Listed origin'}, {'field': 'start', 'title': 'Start date'},
                                         {'field': 'days', 'type': 'quantitative', 'title': 'Days on site'}]}}
               for solid in (True, False)],
             {'transform': [{'calculate': stay_of, 'as': 'stay'}, {'aggregate': [{'op': 'count', 'as': 'n'}], 'groupby': ['stay']},
                            {'calculate': 'datum.n + 0.6', 'as': 'end'}],   # count printed at the end of each row
              'mark': {'type': 'text', 'align': 'left', 'fontSize': 16, 'fontWeight': 700, 'color': INK},
              'encoding': {'x': {'field': 'end', 'type': 'quantitative'}, 'y': SY, 'text': {'field': 'n'}}},
         ]},
    ],
    'spacing': 76,   # chart 12 starts on the page's second-column line, as in the chart pairs above
    'resolve': {'scale': {'x': 'independent', 'y': 'independent'}},
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
