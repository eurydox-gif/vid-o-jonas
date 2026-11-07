// Rend jonas.html en vidéo MP4 (1920x1080, 30 i/s) via Playwright + ffmpeg.
// Usage : node render.js [sortie.mp4] [fps]   |   node render.js --stills dossier
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(__dirname, 'jonas.html') + '?capture');
  const canvas = await page.$('#c');
  const grab = async t => { await page.evaluate(t => window.renderFrame(t), t); return canvas.screenshot({ type: 'png' }); };

  if (args[0] === '--stills') {
    const dir = args[1] || 'stills'; fs.mkdirSync(dir, { recursive: true });
    for (let s = 0; s < 8; s++) for (const lt of [1.5, 3.5, 4.4, 6.5])
      fs.writeFileSync(path.join(dir, `s${s + 1}_${lt}.png`), await grab(s * 8 + lt));
    await browser.close(); return;
  }
  const out = args[0] || 'jonas.mp4', fps = Number(args[1] || 30);
  const duration = await page.evaluate(() => window.DURATION);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(duration * fps);
  for (let f = 0; f < n; f++) {
    const buf = await grab(f / fps);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % fps === 0) process.stdout.write(`\r${(f / fps).toFixed(0)} / ${duration} s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`\nVidéo écrite : ${out}`);
})();
