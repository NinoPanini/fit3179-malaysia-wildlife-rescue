/* Chart embedding follows FIT3179/Vega-Lite/5_multiple_charts_html.
   Specs, data, fonts and libraries are local, so the page works offline.
   Charts wait for the web fonts so Vega measures labels with the right typeface. */
const views = new Map();
window.chartStatus = {};
async function renderChart(element) {
  const id = element.id;
  try {
    const response = await fetch(element.dataset.spec);
    if (!response.ok) throw new Error(`Chart file unavailable (${response.status})`);
    const spec = await response.json();
    const result = await vegaEmbed(element, spec, { actions: false, renderer: 'svg' });
    views.set(id, result.view);
    window.chartStatus[id] = 'ready';
    element.setAttribute('aria-busy', 'false');
  } catch (error) {
    window.chartStatus[id] = 'error';
    element.textContent = 'This chart could not load. Refresh the page to try again; its data table is available below.';
    element.classList.add('chart-error');
    console.error(id, error);
  }
}
const fontsReady = document.fonts ? Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 2500))]) : Promise.resolve();
fontsReady.then(() => document.querySelectorAll('[data-spec]').forEach(renderChart));
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => views.forEach(view => view.resize().runAsync()), 180);
});
const navLinks = [...document.querySelectorAll('nav a')];
const sectionObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    navLinks.forEach(link => {
      const active = link.hash === `#${entry.target.id}`;
      if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
  });
}, { rootMargin: '-15% 0px -65% 0px' });
document.querySelectorAll('main > section[id]').forEach(section => sectionObserver.observe(section));
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
