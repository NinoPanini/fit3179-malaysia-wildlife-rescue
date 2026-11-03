"""Step 2 of 3: data for the remaining charts (run from the website folder: python tools/2_chart_data.py).

Reads step 1's output and the small extracts in tools/inputs/, adds the PERHILITAN 2021-2023
and BSBCC 2021-2025 figures, and writes JSON into data/. Numbers typed from the reports are
written out below with their page references; each table's totals are checked (assert)
before anything is written.
"""
import csv, datetime as _dt, json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'data'                   # ROOT is the website folder
PROC = ROOT / 'tools' / 'inputs'
def rd(p): return json.loads((WEB / p).read_text(encoding='utf8'))
def wr(name, value):
    with open(WEB / name, 'w', encoding='utf8', newline='\n') as f:
        f.write(json.dumps(value, indent=1, ensure_ascii=False))
def rows(p): return list(csv.DictReader(open(PROC / p, encoding='utf-8-sig')))
GROUPS = ['Reptiles', 'Mammals', 'Birds']

# ---- 1. Handovers by state: 2021 (Table 20), 2023 (Table 46), 2024 (Table 34)
h21 = {}
for r in rows('perhilitan_handovers_2021.csv'):
    h21[r['state']] = int(r['state_total'])
assert sum(h21.values()) == 11408 and len(h21) == 12
# PERHILITAN Laporan Tahunan 2023, Table 46 (Jadual 46), state x group, printed total 12,691
t46 = {'Kelantan': (2344, 28, 18), 'Pulau Pinang': (1934, 97, 23), 'Johor': (1828, 29, 16),
       'Selangor': (426, 951, 38), 'Terengganu': (1249, 41, 10), 'Wilayah Persekutuan': (957, 142, 15),
       'Kedah': (866, 34, 9), 'Perak': (554, 33, 6), 'Pahang': (293, 44, 9), 'Perlis': (262, 4, 1),
       'Negeri Sembilan': (220, 1, 0), 'Melaka': (166, 35, 8)}
assert [sum(v[i] for v in t46.values()) for i in range(3)] == [11099, 1439, 153]
h23 = {s: sum(v) for s, v in t46.items()}
assert sum(h23.values()) == 12691
h24 = {r['state']: r['total'] for r in rd('handovers-2024.json')}
assert sum(h24.values()) == 16034
trend = []
for year, src, loc in [(2021, h21, 'PERHILITAN 2021, Table 20, printed p80'),
                       (2023, h23, 'PERHILITAN 2023, Table 46, printed p119'),
                       (2024, h24, 'PERHILITAN 2024, Table 34, p121')]:
    ordered = sorted(src.items(), key=lambda kv: -kv[1])
    for rank, (state, total) in enumerate(ordered, 1):
        trend.append({'state': state, 'year': year, 'total': total, 'rank': rank, 'source': loc})
wr('handovers-trend.json', trend)
# National totals incl. 2022, which publishes only a national figure (PDF p106, printed p105):
# 11,170 total; reptiles 9,190, mammals 1,820, birds 161 (these parts sum to 11,171 in the source).
wr('handovers-national.json', [
    {'year': 2021, 'total': 11408, 'reptiles': 9048, 'mammals': 2095, 'birds': 265, 'state_table': True, 'source': 'PERHILITAN 2021, Table 20'},
    {'year': 2022, 'total': 11170, 'reptiles': 9190, 'mammals': 1820, 'birds': 161, 'state_table': False, 'source': 'PERHILITAN 2022, printed p105 text (no state table published)'},
    {'year': 2023, 'total': 12691, 'reptiles': 11099, 'mammals': 1439, 'birds': 153, 'state_table': True, 'source': 'PERHILITAN 2023, Table 46, printed p119'},
    {'year': 2024, 'total': 16034, 'reptiles': 14146, 'mammals': 1683, 'birds': 205, 'state_table': True, 'source': 'PERHILITAN 2024, Table 34'}])

# ---- 2. Waffle: 2024 handovers as 100 squares (1 square = 1%), largest-remainder rounding
tot = {'Reptiles': 14146, 'Mammals': 1683, 'Birds': 205}
raw = {g: v / 16034 * 100 for g, v in tot.items()}
cells = {g: int(v) for g, v in raw.items()}
for g in sorted(raw, key=lambda g: -(raw[g] - int(raw[g])))[:100 - sum(cells.values())]:
    cells[g] += 1
assert cells == {'Reptiles': 88, 'Mammals': 11, 'Birds': 1}
waffle, i = [], 0
for g in GROUPS:
    for _ in range(cells[g]):
        waffle.append({'cell': i, 'col': i % 10, 'row': i // 10, 'group': g,
                       'group_total': tot[g], 'share': round(raw[g], 1)}); i += 1
wr('handovers-waffle-2024.json', waffle)

# ---- 3. NWRC monthly intake 2023 + 2024
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# PERHILITAN 2023, Table 31 (received: mammals, reptiles, birds). The printed "Disember" row
# (77, 417, 73) equals the annual totals stated in the text (567 animals), and the release
# columns Jan-Nov sum exactly to that row; December's own intake is therefore not printed.
t31 = [(7,2,13),(8,1,0),(7,10,4),(4,10,1),(11,35,9),(10,91,19),(0,0,0),(2,243,3),(1,0,0),(9,6,13),(14,3,7)]
intake = []
for m, (mam, rep, bird) in zip(MONTHS, t31):
    for g, v in (('Mammals', mam), ('Reptiles', rep), ('Birds', bird)):
        intake.append({'year': 2023, 'month': m, 'group': g, 'animals': v, 'reported': True})
for g in GROUPS:
    intake.append({'year': 2023, 'month': 'Dec', 'group': g, 'animals': None, 'reported': False})
for r in rd('nwrc-intake-2024.json'):
    intake.append({'year': 2024, 'month': r['month'], 'group': r['group'], 'animals': r['animals'], 'reported': True})
assert len(intake) == 72
wr('nwrc-intake-2023-2024.json', intake)
wr('nwrc-intake-totals.json', [
    {'year': 2023, 'group': 'Reptiles', 'animals': 417}, {'year': 2023, 'group': 'Mammals', 'animals': 77},
    {'year': 2023, 'group': 'Birds', 'animals': 73},
    {'year': 2024, 'group': 'Reptiles', 'animals': 10968}, {'year': 2024, 'group': 'Mammals', 'animals': 75},
    {'year': 2024, 'group': 'Birds', 'animals': 183}])

# ---- 4. Bear journeys 2021-2025 (BSBCC reports; GPS fixes never used)
KIND = {'Confiscation': 'Into care', 'Handover': 'Into care', 'Admission / transfer': 'Into care',
        'Transfer for soft-release rehabilitation': 'Rehabilitation step', 'Forest walks started': 'Rehabilitation step',
        'Hard release': 'Release', 'First hard release': 'Release', 'Second hard release': 'Release',
        'Recapture': 'Recaptured', 'Last reported signal': 'Other collar signal', 'Mortality signal': 'Collar death signal',
        'Location alert': 'Other collar signal', 'Remains recovered': 'Remains found'}
# Plain wording for collar and release terms shown on the chart (the report's own term stays in brackets).
PLAIN = {'Hard release': 'Released to the forest (hard release)',
         'First hard release': 'First release to the forest', 'Second hard release': 'Second release to the forest',
         'Mortality signal': 'Collar signalled death', 'Last reported signal': 'Last collar signal',
         'Location alert': 'Collar location alert', 'Transfer for soft-release rehabilitation': 'Moved to soft-release training',
         'Admission / transfer': 'Admitted or transferred'}
ev = []
for r in rows('bsbcc_selected_case_timeline.csv'):
    # Month-only events are drawn at the start of the month; the label says the day is not reported.
    d = r['event_date'] if r['date_precision'] == 'day' else r['event_date'] + '-01'
    ev.append({'bear': r['bear_name'], 'date': d, 'precision': r['date_precision'], 'event': PLAIN.get(r['event_type'], r['event_type']),
               'kind': KIND[r['event_type']], 'place': r['location_as_reported'], 'note': r['note'],
               'source': f"BSBCC {r['source_id'][-4:]}, {r['source_locator']}"})
# Sika: BSBCC 2023 PDF p7 - mortality signal first received 5 March 2023; skeleton found 15-25 May.
ev.append({'bear': 'Sika', 'date': '2023-03-05', 'precision': 'day', 'event': PLAIN['Mortality signal'],
           'kind': 'Collar death signal', 'place': 'Tabin Wildlife Reserve', 'note': 'First mortality signal; remains found 15-25 May',
           'source': 'BSBCC 2023, PDF p7'})
assert len(ev) == 23 and all(e['date'] >= '2021' for e in ev)
for e in ev:
    t = _dt.date.fromisoformat(e['date'])
    if e['precision'] == 'day':
        e['date_label'] = f"{t.day} {t:%b %Y}"
    else:
        early = 'early ' if 'early' in e['note'].lower() else ''
        e['date_label'] = f"{early.capitalize()}{t:%B %Y}".strip() + ' (day not reported)'
outcome = {'Sunbearo': 'Later confirmed dead (collar retrieved)', 'Loki': 'Fate unknown: collar failed',
           'Wawa': 'No news after May 2022', 'Sika': 'Died about three weeks after release',
           'Itam': 'Died weeks after release', 'Tenom': 'Still in supervised rehabilitation (2025 report)',
           'Pitang': 'Still in supervised rehabilitation (2025 report)', 'Rudy': 'At BSBCC (2024 report)', 'Kwong': 'At BSBCC (2025 report)'}
released, in_care = ['Sunbearo', 'Loki', 'Wawa', 'Sika', 'Itam'], ['Rudy', 'Kwong', 'Tenom', 'Pitang']
order = released + in_care
for e in ev:
    e['order'] = order.index(e['bear']); e['outcome'] = outcome[e['bear']]
# Events less than five weeks apart overlap on the overview, so they are stacked (earliest on top).
# 'nudge' only moves the symbol up or down inside the bear's row; the date is unchanged.
ev.sort(key=lambda e: (e['order'], e['date']))
clusters = []
for e in ev:
    near = clusters and clusters[-1][-1]['bear'] == e['bear'] and \
        (_dt.date.fromisoformat(e['date']) - _dt.date.fromisoformat(clusters[-1][-1]['date'])).days < 35
    clusters[-1].append(e) if near else clusters.append([e])
for c in clusters:
    for i, e in enumerate(c):
        e['nudge'] = i - (len(c) - 1) / 2
wr('bear-journeys.json', ev)
wr('bear-outcomes.json', [{'bear': b, 'order': i, 'outcome': outcome[b], 'group': 'Released' if b in released else 'In care',
    'first': min(e['date'] for e in ev if e['bear'] == b),
    'last': max(e['date'] for e in ev if e['bear'] == b)} for i, b in enumerate(order)])

# ---- 5. Release flows to named protected areas (approximate area positions, approved 24 Oct)
SITES = {  # lon, lat - approximate positions of each protected area, for orientation only
    'Penang National Park': (100.19, 5.45, 'Pulau Pinang'), 'Ulu Muda Forest Reserve': (100.97, 6.00, 'Kedah'),
    'Temenggor Forest Reserve': (101.40, 5.40, 'Perak'), 'Taman Negara Terengganu': (102.65, 4.90, 'Terengganu'),
    'Taman Negara Pahang': (102.40, 4.38, 'Pahang'), 'Sungkai Wildlife Reserve': (101.33, 3.98, 'Perak')}
ORIGIN = (101.33, 3.98)  # NWRC, Sungkai, Perak (centre sits beside Sungkai Wildlife Reserve)
rel = rd('nwrc-releases-2024.json')
flows = []
for site, (lon, lat, state) in SITES.items():
    sp = [r for r in rel if r['destination'] == site]
    flows.append({'site': site, 'state': state, 'longitude': lon, 'latitude': lat,
                  'origin_longitude': ORIGIN[0], 'origin_latitude': ORIGIN[1],
                  'animals': sum(r['animals'] for r in sp), 'species': len(sp),
                  'species_list': ', '.join(f"{r['species']} ({r['animals']})" for r in sp)})
assert sum(f['animals'] for f in flows) == 32
wr('release-sites.json', flows)

# ---- 6. BSBCC volunteers and interns 2021-2025
wr('bsbcc-participation-2021-2025.json', [{'year': int(r['year']), 'programme': r['programme'],
    'people': int(r['people']), 'note': r['note']} for r in rows('bsbcc_volunteers_interns_2021_2025.csv')])

# ---- 7. 2025 placements for the Gantt chart (no names; origin as listed)
pl = []
for r in rows('bsbcc_volunteer_placements_2025.csv'):
    pl.append({'placement': r['placement_id'], 'start': r['start_date'], 'end': r['end_date'],
               'days': int(r['calendar_days_inclusive']), 'origin': r['country_of_origin'],
               'origin_group': 'Malaysia' if r['country_of_origin'] == 'Malaysia' else 'Other countries'})
assert len(pl) == 57 and sum(p['days'] for p in pl) == 978
wr('bsbcc-placements-2025.json', pl)
wr('bsbcc-origins-2025.json', [{'origin': r['country_of_origin'], 'placements': int(r['placements'])}
                               for r in rows('bsbcc_volunteer_origins_2025.csv')])
print('Step 2: chart data written.')

# ---- 8. Curved flow arcs (quadratic curves between NWRC and each site; drawing aid only)
arcs = []
for f in flows:
    if f['site'] == 'Sungkai Wildlife Reserve':
        continue  # released beside the centre itself; shown as a ring at the origin
    x0, y0, x1, y1 = f['origin_longitude'], f['origin_latitude'], f['longitude'], f['latitude']
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * 0.22, my + dx * 0.22  # bend each arc to its left
    n = 24
    for k in range(n + 1):
        t = k / n * 0.94  # stop short so the arrowhead sits on the end
        arcs.append({'site': f['site'], 'animals': f['animals'], 'step': k,
                     'longitude': (1-t)**2*x0 + 2*(1-t)*t*cx + t*t*x1,
                     'latitude': (1-t)**2*y0 + 2*(1-t)*t*cy + t*t*y1})
    t = 0.94
    tx, ty = 2*(1-t)*(cx-x0) + 2*t*(x1-cx), 2*(1-t)*(cy-y0) + 2*t*(y1-cy)
    f['arrow_angle'] = (90 - math.degrees(math.atan2(ty, tx))) % 360  # screen angle for a triangle mark
    f['arrow_longitude'], f['arrow_latitude'] = arcs[-1]['longitude'], arcs[-1]['latitude']
wr('release-sites.json', flows)
wr('release-arcs.json', arcs)

# ---- 9. Borneo context inset: Sabah and Sarawak outlines (simplified) + two labelled places
def dp(pts, tol):  # Douglas-Peucker line simplification (pure Python)
    if len(pts) < 3: return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    L = math.hypot(x1 - x0, y1 - y0) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs((x1 - x0) * (y0 - pts[i][1]) - (x0 - pts[i][0]) * (y1 - y0)) / L
        if d > dmax: dmax, idx = d, i
    if dmax <= tol: return [pts[0], pts[-1]]
    return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)
def ring_area(r): return sum(r[i][0]*r[i+1][1] - r[i+1][0]*r[i][1] for i in range(len(r) - 1)) / 2
raw = json.loads((PROC / 'geoboundaries-MYS-ADM1-simplified.geojson').read_text(encoding='utf8'))
feats = []
for x in raw['features']:
    name = x['properties']['shapeName']
    if name not in ('Sabah', 'Sarawak'): continue
    g = x['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    out = []
    for poly in polys:
        r = poly[0]; h = len(r) // 2  # split the closed ring so the simplifier has two distinct end points
        ext = [[round(a, 3), round(b, 3)] for a, b in dp(r[:h + 1], 0.01)[:-1] + dp(r[h:], 0.01)]
        if len(ext) < 4 or abs(ring_area(ext)) < 0.0005: continue
        if ring_area(ext) > 0: ext = ext[::-1]  # clockwise exterior rings, as in the Peninsular file
        out.append([ext])
    feats.append({'type': 'Feature', 'properties': {'state': name}, 'geometry': {'type': 'MultiPolygon', 'coordinates': out}})
wr('borneo-states.geojson', {'type': 'FeatureCollection', 'features': feats})
wr('sabah-places.json', [
    {'place': 'BSBCC, Sepilok', 'role': 'Care centre', 'longitude': 117.95, 'latitude': 5.86},
    {'place': 'Tabin Wildlife Reserve', 'role': 'Rehabilitation and release forest', 'longitude': 118.50, 'latitude': 5.20}])
print('Step 2 done: release arcs and Sabah inset written.')
