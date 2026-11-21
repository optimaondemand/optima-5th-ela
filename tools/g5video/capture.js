const { chromium } = require('playwright'); const fs = require('fs');
const key = process.argv[2], FPS = +(process.argv[3] || 12), out = '/tmp/vid/frames/' + key;
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const tl = JSON.parse(fs.readFileSync('/tmp/vid/build/timeline.json'))[key];
  const owl = '';
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 1280, height: 720 } });
  await pg.goto('file:///tmp/vid/build/render.html'); await pg.evaluate(([a, b]) => setup(a, b), [tl, owl]);
  await pg.waitForTimeout(400);
  const N = Math.ceil((tl.dur + 0.8) * FPS);
  for (let i = 0; i < N; i++) {
    await pg.evaluate(t => render(t), i / FPS);
    await pg.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 88 });
  }
  await pg.evaluate(t => render(t), Math.min(tl.dur - 1, 3.5)); 
  await br.close(); console.log(key, N, 'frames');
})();
