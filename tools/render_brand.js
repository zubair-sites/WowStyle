// Render each #id in brand/assets.html to brand/png/<id>.png (transparent where unstyled),
// or with `covers`, each .cover in brand/covers.html to brand/covers/<id>.png.
// Usage: node tools/render_brand.js [covers]
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const dir = path.join(__dirname, '..', 'brand');
  fs.mkdirSync(path.join(dir, 'png'), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 1 });
  if (process.argv[2] === 'covers') {
    fs.mkdirSync(path.join(dir, 'covers'), { recursive: true });
    await p.goto('file://' + path.join(dir, 'covers.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(1000);
    for (const id of await p.$$eval('.cover', els => els.map(e => e.id))) {
      await p.locator('#' + id).screenshot({ path: path.join(dir, 'covers', id + '.png') });
    }
    await b.close();
    return;
  }
  await p.goto('file://' + path.join(dir, 'assets.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1000);
  for (const id of ['logo-dark', 'logo-light', 'logo-stacked', 'site-icon', 'og-default', 'newsletter']) {
    const el = p.locator('#' + id);
    if (id === 'logo-light') await el.evaluate(e => (e.style.background = 'transparent'));
    await el.screenshot({ path: path.join(dir, 'png', id + '.png'), omitBackground: true });
  }
  await b.close();
})();
