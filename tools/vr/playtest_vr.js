// Play a built G5 ELA VR page end to end in Chromium.
// usage: node tools/vr/playtest_vr.js 7 [port]   (run from the repo root; serves the repo itself)
// Both paths at 1150 and 420 px: the 6 required VR steps -> chapter token; help drawer images load;
// Field Notes Day: a wrong pick first, then all cards right -> field notes stamp; 2 sentence chips; timer; no PDF.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const W = process.argv[2] || '18', PORT = +(process.argv[3] || 8765), ROOT = process.cwd();
const TYPES = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.mp3': 'audio/mpeg', '.js': 'text/javascript', '.css': 'text/css' };
const srv = http.createServer((q, r) => {
  const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'content-type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
}).listen(PORT);

(async () => {
  const browser = await chromium.launch(); let fails = 0;
  const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails++; };
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/vr/week' + W + '.json'), 'utf8'));
  for (const width of [1150, 420]) {
    console.log('— ' + width + ' px');
    const page = await browser.newPage({ viewport: { width, height: 900 } }), errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error' && !/404|Failed to load|ERR_|net::/.test(m.text())) errs.push(m.text()); });
    await page.goto(`http://localhost:${PORT}/vr-${W}.html`); await page.evaluate(() => localStorage.clear()); await page.reload();
    ok(await page.$eval('#pb-vr', b => b.getAttribute('aria-pressed')) === 'true', 'Story Expedition is the default path');
    const scrollW = () => page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    ok(await scrollW() <= 0, 'no horizontal scroll (VR)');
    const chks = await page.$$('#vr-steps .chk');
    for (const i of [0, 1, 2, 3, 5]) await chks[i].click();
    await chks[6].click();
    ok(!(await page.$eval('#vr-done', d => d.classList.contains('show'))), 'chapter token waits for step 5');
    await chks[4].click();
    ok(await page.$eval('#vr-done', d => d.classList.contains('show')), 'chapter token shows after all 7 steps');
    await page.click('#vr-help summary');
    await page.$$eval('#vr-help img', a => a.forEach(i => { i.loading = 'eager'; }));
    await page.waitForTimeout(800);
    const imgs = await page.$$eval('#vr-help img', a => a.map(i => i.complete && i.naturalWidth > 0));
    ok(imgs.length === 14 && imgs.every(Boolean), 'help drawer: 14 images load');
    ok(await page.$('#vr-help iframe') !== null, 'help video loads on open');
    if (width === 1150) await page.screenshot({ path: `/tmp/vr${W}-vr-${width}.png`, fullPage: true });

    await page.click('#pb-alt');
    ok(await page.$eval('#vr', s => getComputedStyle(s).display) === 'none', 'Field Notes Day hides the VR card');
    const C = data.alt.cards;
    ok(await page.$$eval('.vcard', a => a.length) === C.length, C.length + ' cards to sort');
    const wrong = C[0].ans === 'vision' ? 'real' : 'vision';
    await page.click(`.vbtn[data-i="0"][data-a="${wrong}"]`);
    ok(!(await page.$eval('#g-msg', m => m.classList.contains('ok'))) && !(await page.$eval('#bmark', b => b.classList.contains('show'))), 'a wrong pick gets the clue, no stamp');
    for (let i = 0; i < C.length; i++) await page.click(`.vbtn[data-i="${i}"][data-a="${C[i].ans}"]`);
    ok(/6 of 6/.test(await page.textContent('#vr-tally')), 'tally reaches 6 of 6');
    ok(await page.$eval('#bmark', b => b.classList.contains('show')), 'field notes stamp shows when the game is done');
    ok(await scrollW() <= 0, 'no horizontal scroll (Field Notes Day)');
    const para = 'Isaac’s mother says the river is their home because the land matters more than a building. In Chapter 3, the old women dance on the stones to say good-bye.';
    await page.fill('#para', para);
    ok(await page.$$eval('.chip', c => c.every(x => x.classList.contains('on'))), '2 good sentences light every chip');
    ok(/2 of 2 sentences ✓/.test(await page.textContent('#para-count')), 'sentence counter reaches 2');
    ok(await page.$('#pdf-btn') === null && await page.$('#g-name') === null, 'no PDF and no name box: the video is the only thing turned in');
    ok((await page.$$('.turn-steps li')).length === 4, 'Turn it in shows the 4 Canvas recording steps');
    await page.click('#timer-btn'); await page.waitForTimeout(1200);
    ok(/^0:2\d$/.test(await page.textContent('#timer')), 'the 30 second timer counts down');
    await page.click('#timer-btn');
    if (width === 1150) await page.screenshot({ path: `/tmp/vr${W}-alt-${width}.png`, fullPage: true });
    else await page.screenshot({ path: `/tmp/vr${W}-alt-${width}.png`, fullPage: false });
    await page.reload();
    ok(await page.$eval('#bmark', b => b.classList.contains('show')) && (await page.inputValue('#para')).length > 50, 'progress survives a reload');
    ok(errs.length === 0, 'no page errors' + (errs.length ? ': ' + errs.join(' | ') : ''));
    await page.close();
  }
  await browser.close(); srv.close();
  console.log(fails ? `✗ ${fails} check(s) failed` : '✓ playtest passed');
  process.exit(fails ? 1 : 0);
})();
