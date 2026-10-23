// A local-only static preview. Only public website assets are served.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const port = Number(process.env.PORT || 8000);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.geojson': 'application/geo+json', '.csv': 'text/csv', '.svg': 'image/svg+xml' };
const allowed = new Set(['index.html', 'css', 'js', 'charts', 'data', 'assets', 'vendor']);
http.createServer((req, res) => {
  let relative;
  try { relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, '') || 'index.html'; }
  catch { res.writeHead(400).end(); return; }
  const file = path.resolve(root, relative);
  if (!allowed.has(relative.split('/')[0]) || !file.startsWith(root + path.sep) || !['GET', 'HEAD'].includes(req.method)) { res.writeHead(404).end(); return; }
  fs.stat(file, (error, stat) => {
    if (error || !stat.isFile()) { res.writeHead(404).end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'text/plain', 'Cache-Control': 'no-cache' });
    if (req.method === 'HEAD') res.end(); else fs.createReadStream(file).pipe(res);
  });
}).on('error', error => {
  console.error(error.code === 'EADDRINUSE' ? `Port ${port} is in use. Check the existing preview or choose another PORT.` : error.message);
  process.exit(1);
}).listen(port, '127.0.0.1', () => console.log(`Local preview: http://127.0.0.1:${port}/`));
