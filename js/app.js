/* Chart embedding follows FIT3179/Vega-Lite/5_multiple_charts_html.
   Specs, data, fonts and libraries are local, so the page works offline.
   Charts wait for the web fonts so Vega measures labels with the right typeface. */
const views = new Map();
window.vegaViews = views;   // e.g. vegaViews.get('placement-months').signal('selectedMonth')
const specs = new Map();     // original specs, kept so fixed-width charts can be refitted on resize
// Chart 03 headings for each choice in its "Show" menu: [heading, subtitle]
const SHARE_MAP_HEADINGS = {   // kept to similar lengths so the map does not jump when the menu changes
  'All animals': ['Handover density by state', 'Animals per 1,000 km² of land · Peninsular Malaysia, 2024'],
  Reptiles: ['Reptile share of handovers by state', 'Share that were reptiles · Peninsular Malaysia, 2024'],
  Mammals: ['Mammal share of handovers by state', 'Share that were mammals · Peninsular Malaysia, 2024'],
  Birds: ['Bird share of handovers by state', 'Share that were birds · Peninsular Malaysia, 2024'],
};
window.chartStatus = {};

/* Concatenated views (hconcat/vconcat) cannot use width "container" in Vega-Lite, so their specs
   carry usermeta.fitWidth: the natural width they were designed at. Here every fixed sub-view width
   is scaled to the space the page actually has (e.g. narrower at 1024 px), without sideways scrolling. */
function fitToColumn(spec, element, correction = 1) {
  const base = spec.usermeta && spec.usermeta.fitWidth;
  if (!base) return spec;
  if (spec.usermeta.mobileStack && element.clientWidth < 720) {
    const copy = structuredClone(spec);
    copy.vconcat = copy.hconcat;
    delete copy.hconcat;
    copy.spacing = 52;
    copy.vconcat.forEach(panel => { panel.width = Math.max(240, element.clientWidth - 65); });
    return copy;
  }
  const avail = Math.max(element.clientWidth, 620);          // below this, the .chart-scroll box scrolls
  const scale = Math.min(Math.max(avail / base, 0.6), 1.12) * correction;
  const copy = structuredClone(spec);
  (function scaleWidths(node) {
    for (const key of ['hconcat', 'vconcat', 'concat']) (node[key] || []).forEach(scaleWidths);
    if (typeof node.width === 'number') node.width = Math.round(node.width * scale);
    if (typeof node.spacing === 'number') node.spacing = Math.round(node.spacing * scale);   // gaps shrink with the charts
  })(copy);
  return copy;
}

async function renderChart(element) {
  const id = element.id;
  try {
    if (!specs.has(id)) {
      const response = await fetch(element.dataset.spec);
      if (!response.ok) throw new Error(`Chart file unavailable (${response.status})`);
      specs.set(id, await response.json());
    }
    if (views.has(id)) views.get(id).finalize();
    let result = await vegaEmbed(element, fitToColumn(specs.get(id), element), { actions: false, renderer: 'svg' });
    const drawn = element.querySelector('svg') && element.querySelector('svg').getBoundingClientRect().width;
    const avail = Math.max(element.clientWidth, 620);
    if (specs.get(id).usermeta && drawn > avail + 1) {         // labels took more room than estimated: shrink once more
      result.view.finalize();
      result = await vegaEmbed(element, fitToColumn(specs.get(id), element, (avail - 4) / drawn), { actions: false, renderer: 'svg' });
    }
    views.set(id, result.view);
    if (id === 'share-map') {   // chart 03: the heading and subtitle follow the "Show" menu
      const title = document.getElementById('share-map-title'), subtitle = document.getElementById('share-map-subtitle');
      const showHeading = (name, choice) => { [title.textContent, subtitle.textContent] = SHARE_MAP_HEADINGS[choice]; };
      result.view.addSignalListener('groupChoice', showHeading);
      showHeading('groupChoice', result.view.signal('groupChoice'));
    }
    if (id === 'placement-months') {
      result.view.addEventListener('click', (event, item) => {
        const month = item && item.datum && item.datum.month;
        if (month) result.view.signal('selectedMonth', result.view.signal('selectedMonth') === month ? 'All months' : month).runAsync();
      });
    }
    window.chartStatus[id] = 'ready';
    element.setAttribute('aria-busy', 'false');
    return result.view;
  } catch (error) {
    window.chartStatus[id] = 'error';
    element.textContent = 'This chart could not load. Refresh the page to try again; its data table is available below.';
    element.classList.add('chart-error');
    console.error(id, error);
  }
}

/* Charts 07 and 08 show the same 32 released animals. Clicking a release area on the map, or choosing
   it in the Sankey's menu, highlights that area in both charts. */
const ALL = 'All destinations';
function linkReleaseCharts() {
  const map = views.get('release-map'), sankey = views.get('release-sankey');
  if (!map || !sankey) return;
  const focus = site => {
    map.signal('siteFocus', site).runAsync();
    if (sankey.signal('destinationChoice') !== site) sankey.signal('destinationChoice', site).runAsync();
    window.chartStatus.releaseFocus = site;
  };
  map.addEventListener('click', (event, item) => {
    const site = item && item.datum && item.datum.site;
    focus(!site || site === map.signal('siteFocus') ? ALL : site);   // click again or on empty map to reset
  });
  sankey.addSignalListener('destinationChoice', (name, value) => map.signal('siteFocus', value).runAsync());
  sankey.addEventListener('click', (event, item) => {
    const d = item && item.datum;
    const site = d && (d.destination || (d.side === 'destination' && d.label));
    if (site) focus(site === sankey.signal('destinationChoice') ? ALL : site);
  });
}

const fontsReady = document.fonts ? Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 2500))]) : Promise.resolve();
fontsReady.then(async () => {
  await Promise.all([...document.querySelectorAll('[data-spec]')].map(renderChart));
  linkReleaseCharts();
});
let resizeTimer, lastWidth = window.innerWidth;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(async () => {
    if (window.innerWidth === lastWidth) return;
    lastWidth = window.innerWidth;
    for (const [id, view] of views) {
      const element = document.getElementById(id);
      if (specs.get(id).usermeta && specs.get(id).usermeta.fitWidth) await renderChart(element); else view.resize().runAsync();
    }   // charts 07 and 08 are not refitted, so their link listeners stay attached
  }, 200);
});
// The chapter bar is visible before the introduction and stays above the reading surface.
// Track chapter starts rather than intersections: long sections and jumps in either direction
// should keep the same active marker, including after charts resize and change page height.
const chapterNav = document.querySelector('.chapter-nav');
const navLinks = [...chapterNav.querySelectorAll('a')];
const navSections = navLinks.map(link => document.querySelector(link.hash));
let navFrame = 0;
function updateChapterNav() {
  navFrame = 0;
  const readingLine = chapterNav.getBoundingClientRect().height + 32;
  let current = -1;   // nothing is highlighted above chapter 01
  navSections.forEach((section, index) => {
    if (section.getBoundingClientRect().top <= readingLine) current = index;
  });
  navLinks.forEach((link, index) => {
    if (index === current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
function scheduleChapterNav() {
  if (!navFrame) navFrame = requestAnimationFrame(updateChapterNav);
}
window.addEventListener('scroll', scheduleChapterNav, { passive: true });
window.addEventListener('resize', scheduleChapterNav);
window.addEventListener('hashchange', scheduleChapterNav);
new ResizeObserver(scheduleChapterNav).observe(document.querySelector('main'));
scheduleChapterNav();
// Text tables provide a keyboard-readable alternative to chart tooltips.
document.querySelectorAll('details[data-table]').forEach(detail => {
  detail.addEventListener('toggle', async () => {
    if (!detail.open || detail.dataset.loaded) return;
    detail.dataset.loaded = 'true';
    const target = detail.querySelector('.table-wrap');
    try {
      const response = await fetch(detail.dataset.table);
      if (!response.ok) throw new Error('Table unavailable');
      const rows = await response.json();
      const columns = JSON.parse(detail.dataset.columns);
      const table = document.createElement('table');
      const caption = table.createCaption(); caption.textContent = detail.dataset.caption;
      const header = table.createTHead().insertRow();
      for (const [, label] of columns) { const th = document.createElement('th'); th.scope = 'col'; th.textContent = label; header.append(th); }
      const body = table.createTBody();
      for (const row of rows) { const tr = body.insertRow(); for (const [key] of columns) { const cell = tr.insertCell(); cell.textContent = row[key] ?? 'Not reported'; } }
      target.replaceChildren(table);
    } catch { target.textContent = 'The data table could not load. Please refresh.'; delete detail.dataset.loaded; }
  });
});
