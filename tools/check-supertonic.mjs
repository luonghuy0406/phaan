// So khớp bản chuyển đổi Supertonic (src/lib/supertonic/core.ts) với bản Python, dùng mô hình trong ~/.cache/supertonic3.
// node tools/check-supertonic.mjs <texts.json> <python-output.json> <thư-mục-ghi-wav>
// onnxruntime-node is NOT a project dependency (its installer downloads CUDA builds and breaks `npm install` on Vercel).
// To run this local check:  npm i --no-save onnxruntime-node@1.22.0  &&  node tools/check-supertonic.mjs …
let ort;
try { ort = (await import('onnxruntime-node')).default; } catch {
  console.error('Thiếu onnxruntime-node. Cài tạm (không ghi vào package.json):  npm i --no-save onnxruntime-node@1.22.0');
  process.exit(1);
}
import { readFileSync, writeFileSync } from 'node:fs';
import { preprocess, toIds, makeStyle, synthesizeOne, encodeWav, chunkForModel } from '../src/lib/supertonic/core.ts';
const D = process.env.HOME + '/.cache/supertonic3/';
const [textsPath, pyPath, outDir] = process.argv.slice(2);
const texts = JSON.parse(readFileSync(textsPath, 'utf8')); const py = JSON.parse(readFileSync(pyPath, 'utf8'));
const cfg = JSON.parse(readFileSync(D + 'onnx/tts.json', 'utf8')); const indexer = JSON.parse(readFileSync(D + 'onnx/unicode_indexer.json', 'utf8'));
const load = (f) => ort.InferenceSession.create(D + 'onnx/' + f);
const m = { cfg, indexer, dp: await load('duration_predictor.onnx'), te: await load('text_encoder.onnx'), ve: await load('vector_estimator.onnx'), voc: await load('vocoder.onnx') };
const style = makeStyle(ort, JSON.parse(readFileSync(D + 'voice_styles/M1.json', 'utf8')));
let ok = true;
for (let i = 0; i < texts.length; i++) {
  const pre = preprocess(texts[i], 'vi'); const ids = toIds(pre, indexer);
  const samePre = pre === py[i].pre, sameIds = JSON.stringify(ids) === JSON.stringify(py[i].ids);
  const t0 = performance.now();
  const r = await synthesizeOne(ort, m, style, texts[i], { lang: 'vi', steps: 8, speed: 1 });
  const ms = Math.round(performance.now() - t0);
  const rms = Math.sqrt(r.pcm.reduce((a, x) => a + x * x, 0) / r.pcm.length);
  const durDiff = Math.abs(r.duration - py[i].dur);
  console.log(`#${i} pre=${samePre} ids=${sameIds} dur js=${r.duration.toFixed(3)} py=${py[i].dur.toFixed(3)} | samples=${r.pcm.length} (${(r.pcm.length / r.sampleRate).toFixed(2)}s) rms=${rms.toFixed(3)} | ${ms}ms`);
  if (!samePre) console.log('   js:', pre, '\n   py:', py[i].pre);
  ok = ok && samePre && sameIds && durDiff < 1e-3 && rms > 0.01;
  writeFileSync(`${outDir}/js-${i}.wav`, Buffer.from(encodeWav(r.pcm, r.sampleRate)));
}
console.log('chunks:', chunkForModel('Câu một rất dài. '.repeat(40)).map((c) => c.length).join(','));
console.log(ok ? 'KHỚP VỚI BẢN PYTHON' : 'CÓ SAI KHÁC');
