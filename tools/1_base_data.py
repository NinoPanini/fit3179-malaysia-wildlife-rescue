"""Step 1 of 3: base data for the website (run from the website folder: python tools/1_base_data.py).

Writes into data/:
  handovers-2024.json        PERHILITAN 2024 Table 34 (typed from the report)
  peninsular-states.geojson  state outlines for the maps (geoBoundaries, see tools/README.md)
  state-anchors.json         a centre point per state, for the proportional circles
  nwrc-intake-2024.json      NWRC monthly intake, numeric table under Figure 26
  nwrc-releases-2024.json    NWRC releases, Table 31
  release-nodes.json, release-ribbons.json   the Sankey layout for the same 32 releases
The report PDFs are not stored here (they are large); tools/README.md links each one.
Page numbers are given beside each table.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # the website folder
OUT = ROOT / 'data'
INPUTS = ROOT / 'tools' / 'inputs'
OUT.mkdir(exist_ok=True)

def save(name, rows):
    with open(OUT / name, 'w', encoding='utf-8', newline='\n') as f:   # same line endings on every OS
        f.write(json.dumps(rows, ensure_ascii=False, indent=2))

# PERHILITAN 2024: Table 34, printed p121 / PDF p123.
# Order: reptiles, mammals, birds. W. Persekutuan is a combined reporting unit.
raw = [('Kelantan',2845,36,8),('Pulau Pinang',2359,192,37),('Johor',2091,39,23),
       ('Terengganu',1979,24,14),('Selangor',773,1169,45),('Wilayah Persekutuan',1017,19,2),
       ('Kedah',805,61,18),('Perak',693,25,10),('Melaka',572,58,20),('Pahang',530,43,20),
       ('Negeri Sembilan',346,13,6),('Perlis',136,4,2)]
states = [dict(state=n, reptiles=r, mammals=m, birds=b, total=r+m+b,
               mammal_share=m/(r+m+b),year=2024,source='PERHILITAN 2024, Table 34, p121') for n,r,m,b in raw]
assert sum(r['total'] for r in states)==16034
assert [sum(r[k] for r in states) for k in ['reptiles','mammals','birds']]==[14146,1683,205]
save('handovers-2024.json',states)
lookup={r['state']:r for r in states}

# Geographic anchors are derived from administrative geometry, never animal GPS.
# Reverse exterior ring winding for Vega's spherical geoshape rendering.
geo=json.loads((INPUTS/'geoboundaries-MYS-ADM1-simplified.geojson').read_text(encoding='utf-8'))
anchors={}
features=[]
for f in geo['features']:
    name=f['properties']['shapeName']
    if name in ['Sabah','Sarawak','Labuan']: continue
    name={'Penang':'Pulau Pinang','Malacca':'Melaka'}.get(name,name)
    polygons=f['geometry']['coordinates'] if f['geometry']['type']=='MultiPolygon' else [f['geometry']['coordinates']]
    def area(ring): return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]))/2
    ring=max((p[0] for p in polygons),key=lambda r:abs(area(r)))
    signed=area(ring)
    lon=sum((a[0]+b[0])*(a[0]*b[1]-b[0]*a[1]) for a,b in zip(ring,ring[1:]))/(6*signed)
    lat=sum((a[1]+b[1])*(a[0]*b[1]-b[0]*a[1]) for a,b in zip(ring,ring[1:]))/(6*signed)
    # round to 6 decimals (about 0.1 m): float sums differ in the last digits between Python versions
    anchors[name]={'longitude':round(lon,6),'latitude':round(lat,6)}
    for polygon in polygons:
        for i,r in enumerate(polygon):
            if (i==0 and area(r)>0) or (i>0 and area(r)<0): r.reverse()
    f['properties']={'state':name,'coverage':'Separate state count not available' if name not in lookup else 'Reported'}
    features.append(f)
save('peninsular-states.geojson',{'type':'FeatureCollection','features':features})
save('state-anchors.json',[dict(lookup[n],**a) for n,a in anchors.items() if n in lookup])

# NWRC: use the numeric table below Figure 26, p107 / PDF p109.
# Several labels in the plotted bars disagree with this table. Keep this caveat visible.
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly={'Mammals':[10,10,3,4,2,6,7,4,5,9,9,6],
         'Reptiles':[32,45,0,9,16,0,4,469,5009,95,77,5212],
         'Birds':[37,3,0,55,30,3,10,6,17,10,11,1]}
assert [sum(v) for v in monthly.values()]==[75,10968,183]   # 11,226 in all; the report prints no grand total, so this guards against typing errors
save('nwrc-intake-2024.json',[dict(month=m,month_number=i+1,group=g,animals=v[i],year=2024,
  source='PERHILITAN 2024, numeric table beneath Figure 26, p107') for g,v in monthly.items() for i,m in enumerate(months)])

# NWRC releases: Table 31, p108 / PDF p110. All 16 rows, public destinations only.
release_rows=[('Leopard','Panthera pardus',4,'Temenggor Forest Reserve','Perak'),
('Clouded leopard','Neofelis nebulosa',2,'Taman Negara Terengganu','Terengganu'),
('Sun bear','Helarctos malayanus',3,'Taman Negara Terengganu','Terengganu'),
('Dhole','Cuon alpinus',1,'Taman Negara Pahang','Pahang'),
('Sambar deer','Rusa unicolor',1,'Taman Negara Terengganu','Terengganu'),
('Agile gibbon','Hylobates agilis',3,'Ulu Muda Forest Reserve','Kedah'),
('Leopard cat','Prionailurus bengalensis',1,'Penang National Park','Pulau Pinang'),
('Dusky leaf monkey','Trachypithecus obscurus',1,'Ulu Muda Forest Reserve','Kedah'),
('Common palm civet','Paradoxurus hermaphroditus',3,'Penang National Park','Pulau Pinang'),
('Asian small-clawed otter','Aonyx cinereus',2,'Penang National Park','Pulau Pinang'),
('Brahminy kite','Haliastur indus',1,'Penang National Park','Pulau Pinang'),
('White-bellied sea eagle','Haliaeetus leucogaster',4,'Penang National Park','Pulau Pinang'),
('Changeable hawk-eagle','Nisaetus cirrhatus',3,'Taman Negara Pahang','Pahang'),
('Buffy fish owl','Ketupa ketupu',1,'Penang National Park','Pulau Pinang'),
('Spotted wood owl','Strix seloputo',1,'Penang National Park','Pulau Pinang'),
('Oriental pied hornbill','Anthracoceros albirostris',1,'Sungkai Wildlife Reserve','Perak')]
releases=[dict(species=s,scientific_name=sn,animals=n,destination=d,state=st,year=2024,
               source='PERHILITAN 2024, Table 31, p108') for s,sn,n,d,st in release_rows]
assert sum(r['animals'] for r in releases)==32
save('nwrc-releases-2024.json',releases)
# A reproducible Sankey layout, with ribbon thickness proportional to animal count.
# All destinations remain distinct; strips are not movement tracks.
dests=list(dict.fromkeys(r['destination'] for r in releases))
gap=0.65
left_total=32+gap*(len(releases)-1)
right_total=32+gap*(len(dests)-1)
right_pos={}; cursor=(left_total-right_total)/2
nodes=[]
for d in dests:
    n=sum(r['animals'] for r in releases if r['destination']==d)
    right_pos[d]=cursor
    nodes.append(dict(side='destination',label=d,animals=n,x=0.98,x2=1,y=cursor,y2=cursor+n,mid=cursor+n/2,destination=d))
    cursor+=n+gap
ribbons=[]; cursor=0
for r in releases:
    d=r['destination']; n=r['animals']; y1=right_pos[d]
    nodes.append(dict(side='species',label=r['species'],animals=n,x=0,x2=0.02,y=cursor,y2=cursor+n,mid=cursor+n/2,destination=d))
    for step in range(31):
        t=step/30; easing=t*t*(3-2*t); bottom=cursor+(y1-cursor)*easing
        ribbons.append(dict(species=r['species'],destination=d,animals=n,x=0.02+t*0.96,y=bottom,y2=bottom+n,order=step))
    right_pos[d]+=n; cursor+=n+gap
save('release-ribbons.json',ribbons); save('release-nodes.json',nodes)

print('Step 1 done: 2024 handovers, map geometry, NWRC intake and releases, Sankey layout.')
