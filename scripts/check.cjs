// Compile and run every chart against the local files, then verify report totals,
// geographic joins and key chart structure before opening or publishing the site.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vega = require('vega');
const vl = require('vega-lite');
const root = path.resolve(__dirname, '..');
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const sum = (rows, key) => rows.reduce((n, r) => n + (r[key] || 0), 0);

(async () => {
  // PERHILITAN handovers
  const h24 = read('data/handovers-2024.json');
  assert.equal(sum(h24, 'total'), 16034);
  h24.forEach(r => assert.equal(r.reptiles + r.mammals + r.birds, r.total));
  const trend = read('data/handovers-trend.json');
  for (const [year, total] of [[2021, 11408], [2023, 12691], [2024, 16034]]) {
    const rows = trend.filter(r => r.year === year);
    assert.equal(rows.length, 12, `${year}: 12 reporting units`);
    assert.equal(sum(rows, 'total'), total, `${year}: printed total`);
    assert.deepEqual(rows.map(r => r.rank).sort((a, b) => a - b), [...Array(12).keys()].map(i => i + 1));
  }
  const waffle = read('data/handovers-waffle-2024.json');
  assert.equal(waffle.length, 100);
  // Map geometry and anchors
  const anchors = read('data/state-anchors.json');
  assert.equal(anchors.length, 11);
  const geo = read('data/peninsular-states.geojson');
  assert.equal(geo.features.length, 13);
  assert(anchors.every(r => geo.features.some(f => f.properties.state === r.state)));
  assert(h24.filter(r => r.state !== 'Wilayah Persekutuan').every(r => geo.features.some(f => f.properties.state === r.state)), 'Every state row must join to a polygon');
  // NWRC intake and releases
  const intake = read('data/nwrc-intake-2023-2024.json');
  assert.equal(intake.length, 72);
  assert.equal(sum(intake.filter(r => r.year === 2024), 'animals'), 11226);
  assert.equal(intake.filter(r => !r.reported).length, 3, 'Only December 2023 is unprinted');
  assert.equal(sum(read('data/nwrc-releases-2024.json'), 'animals'), 32);
  assert.equal(sum(read('data/release-sites.json'), 'animals'), 32);
  const nodes = read('data/release-nodes.json');
  for (const side of ['species', 'destination']) assert.equal(sum(nodes.filter(r => r.side === side), 'animals'), 32);
  // BSBCC
  const bears = read('data/bear-journeys.json');
  assert.equal(bears.length, 23);
  assert(bears.every(e => e.date_label && (e.precision === 'day' || /day not reported/.test(e.date_label))), 'Month-only dates must say the day is not reported');
  assert(bears.every(e => e.date >= '2021-01-01'), 'No pre-2021 bear events');
  const placements = read('data/bsbcc-placements-2025.json');
  assert.equal(placements.length, 57);
  assert.equal(sum(placements, 'days'), 978);
  assert.equal(placements.map(r => r.days).sort((a, b) => a - b)[28], 14);
  assert.equal(sum(read('data/bsbcc-origins-2025.json'), 'placements'), 57);

  // Claims made in the page text (index.html) - if the data changes, these fail first
  const rank = (st, y) => trend.find(r => r.state === st && r.year === y).rank;
  assert.equal(rank('Terengganu', 2021), 11); assert.equal(rank('Terengganu', 2024), 4);
  assert.equal(rank('Kelantan', 2021), 4); assert.equal(rank('Kelantan', 2024), 1);
  assert.equal(rank('Pulau Pinang', 2021), 1); assert.equal(rank('Pulau Pinang', 2024), 2);
  const national = read('data/handovers-national.json');
  assert(national[1].total < national[0].total, '2022 total dips below 2021');
  assert.equal(Math.round(16034 / 11408 * 100 - 100), 41, 'about 40% rise 2021-2024');
  const share = (st, g) => { const r = h24.find(x => x.state === st); return r[g] / r.total; };
  assert.equal(Math.round(share('Selangor', 'mammals') * 100), 59);
  assert(h24.every(r => r.birds / r.total < 0.034), 'birds never exceed 3.4%');
  assert(h24.every(r => r.reptiles / r.total > 0.38), 'reptiles never below 38%');
  ['Kelantan', 'Johor', 'Terengganu'].forEach(st => assert(share(st, 'mammals') <= 0.02));
  const nwrcTotals = read('data/nwrc-intake-totals.json');
  assert.equal(sum(nwrcTotals.filter(r => r.year === 2023), 'animals'), 567);
  const rep24 = m => intake.find(r => r.year === 2024 && r.month === m && r.group === 'Reptiles').animals;
  assert(rep24('Sep') + rep24('Dec') > 10000, 'two months brought >10,000 reptiles');
  assert.equal(read('data/release-sites.json').find(r => r.site === 'Penang National Park').animals, 13);
  const people = read('data/bsbcc-participation-2021-2025.json').filter(r => r.programme === 'Volunteers').map(r => r.people);
  assert.deepEqual([people[0], people[people.length - 1]], [7, 57]);
  assert(people.every((v, i) => i === 0 || v > people[i - 1]), 'volunteers rose every year');
  assert.equal(read('data/bsbcc-origins-2025.json').find(r => r.origin === 'Malaysia').placements, 27);
  assert(placements.every(p => p.end <= '2025-12-31'), 'all placement days fall in 2025');

  const files = fs.readdirSync(path.join(root, 'charts')).filter(f => f.endsWith('.json'));
  assert.equal(files.length, 13, 'Eleven numbered chart files plus two small context charts');
  for (const file of files) {
    const spec = read(`charts/${file}`);
    if (spec.width === 'container') spec.width = 900;
    const warnings = [];
    const logger = { level: () => vega.Warn, warn: (...a) => { const m = a.join(' '); if (!/event source: window/.test(m)) warnings.push(m); } /* drag-select needs a browser window; harmless in Node */, error: (...a) => { throw new Error(a.join(' ')); }, info: () => {}, debug: () => {} };
    const compiled = vl.compile(spec, { logger }).spec;
    const loader = vega.loader();
    loader.load = uri => fs.promises.readFile(path.resolve(root, uri), 'utf8');
    const view = new vega.View(vega.parse(compiled), { renderer: 'none', loader, logger });
    await view.runAsync();
    const svg = await view.toSVG();
    assert(svg.length > 1000, `${file}: empty chart`);
    assert(!/(?:NaN|Infinity)/.test(svg), `${file}: invalid geometry`);
    assert.equal(warnings.length, 0, `${file}: ${warnings.join('; ')}`);
    const marks = [];
    (function walk(node) { if (node.marktype) marks.push(node); for (const item of node.items || []) walk(item); })(view.scenegraph().root);
    const items = type => marks.filter(m => m.marktype === type && m.role === 'mark').flatMap(m => m.items);
    if (file.startsWith('01-')) assert.equal(items('rect').length, 100, 'Waffle must have 100 squares');
    if (file.startsWith('08-')) assert.equal(marks.filter(m => m.marktype === 'area').length, 16, 'Each released species must have one ribbon');
    if (file.startsWith('06-')) assert(items('symbol').length >= 23, 'Every bear event must be drawn in the overview');
    if (file.startsWith('11-')) assert.equal(items('rect').filter(b => b.datum && b.datum.placement).length, 57, 'Gantt must draw every placement');
    view.finalize();
    console.log(`PASS ${file}`);
  }
  console.log(`Verified ${files.length} charts, report totals, ranks, placements and state joins.`);
})().catch(error => { console.error(error); process.exit(1); });
