// Compile and execute every chart against the actual local files, then verify
// source totals and geographic coverage before opening or publishing the site.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vega = require('vega');
const vl = require('vega-lite');
const root = path.resolve(__dirname, '..');
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
(async () => {
  const state = read('data/handovers-2024.json');
  assert.equal(state.reduce((n,r)=>n+r.total,0),16034);
  state.forEach(r=>assert.equal(r.reptiles+r.mammals+r.birds,r.total));
  const anchors=read('data/state-anchors.json');
  assert.equal(anchors.length,11);
  assert(!anchors.some(r=>r.state==='Wilayah Persekutuan'));
  const geo=read('data/peninsular-states.geojson');
  assert.equal(geo.features.length,13);
  assert(anchors.every(r=>geo.features.some(f=>f.properties.state===r.state)));
  assert.equal(read('data/nwrc-releases-2024.json').reduce((n,r)=>n+r.animals,0),32);
  assert.equal(read('data/release-state-flows.json').reduce((n,r)=>n+r.animals,0),32);
  const nodes=read('data/release-nodes.json');
  for(const side of ['species','destination']) assert.equal(nodes.filter(r=>r.side===side).reduce((n,r)=>n+r.animals,0),32);
  const placements=read('data/bsbcc-placements.json');
  assert.equal(placements.length,57);
  assert.equal(placements.reduce((n,r)=>n+r.days,0),978);
  assert.equal(placements.map(r=>r.days).sort((a,b)=>a-b)[28],14);
  const files=fs.readdirSync(path.join(root,'charts')).filter(f=>f.endsWith('.json'));
  for (const file of files) {
    const spec = read(`charts/${file}`);
    spec.width=900;
    const warnings=[];
    const logger={level:()=>vega.Warn,warn:(...args)=>warnings.push(args.join(' ')),error:(...args)=>{throw new Error(args.join(' '));},info:()=>{},debug:()=>{}};
    const compiled=vl.compile(spec,{logger}).spec;
    const loader=vega.loader();
    loader.load=uri=>fs.promises.readFile(path.resolve(root,uri),'utf8');
    const view=new vega.View(vega.parse(compiled), {renderer:'none',loader,logger});
    await view.runAsync();
    const svg=await view.toSVG();
    assert(svg.length>1000,`${file}: empty chart`);
    assert(!/(?:NaN|Infinity)/.test(svg),`${file}: invalid geometry`);
    assert.equal(warnings.length,0,`${file}: ${warnings.join('; ')}`);
    const marks=[];
    function walk(node) { if(node.marktype) marks.push(node); for(const item of node.items||[]) walk(item); }
    walk(view.scenegraph().root);
    if(file.startsWith('07-')) assert.equal(marks.filter(m=>m.marktype==='area').length,16,'Each released species must have one continuous ribbon');
    if(file.startsWith('05-')) assert.equal(marks.filter(m=>m.marktype==='line').length,2,'Each bear must have one connected timeline');
    if(file.startsWith('09-')) {
      const bars=marks.filter(m=>m.marktype==='rect' && m.role==='mark').flatMap(m=>m.items);
      assert.equal(bars.length,5,'Histogram must have five seven-day bins');
      assert.equal(bars.reduce((n,b)=>n+b.datum.placements,0),57,'Histogram must count every placement exactly once');
      assert(bars.every(b=>b.width>0 && b.height>0),'Every nonempty histogram bin must have visible area');
    }
    view.finalize();
    console.log(`PASS ${file}`);
  }
  console.log(`Verified ${files.length} charts, report totals, placement durations and state joins.`);
})().catch(error=>{ console.error(error);process.exit(1); });
