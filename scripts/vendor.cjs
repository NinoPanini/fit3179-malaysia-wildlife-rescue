// Keep the published site independent of CDNs and npm at runtime.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
for (const name of ['vega', 'vega-lite', 'vega-embed']) {
  fs.mkdirSync(path.join(root, 'vendor'), { recursive: true });
  fs.copyFileSync(path.join(root, 'node_modules', name, 'build', `${name}.min.js`), path.join(root, 'vendor', `${name}.min.js`));
  fs.copyFileSync(path.join(root, 'node_modules', name, 'LICENSE'), path.join(root, 'vendor', `${name}.LICENSE`));
}
console.log('Copied pinned Vega libraries and licences into vendor/.');
