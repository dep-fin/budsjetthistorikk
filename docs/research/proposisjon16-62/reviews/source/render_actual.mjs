import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => {
  if (i % 2 === 0) a.push([v.replace(/^--/, ''), all[i + 1]]);
  return a;
}, []));
for (const key of ['root', 'candidate', 'base', 'runtime']) {
  if (!args[key]) throw new Error('Missing --' + key);
}
const root = path.resolve(args.root);
const tree = execFileSync('git', ['rev-parse', args.candidate + '^{tree}'], { cwd: root, encoding: 'utf8' }).trim();
const base = execFileSync('git', ['rev-parse', args.base + '^{commit}'], { cwd: root, encoding: 'utf8' }).trim();
if (tree !== 'df0eed6d6e8a0b2a07962e641ae05d1194a3304d') throw new Error('Wrong candidate tree');
const loader = createRequire(path.join(path.resolve(args.runtime), 'loader.mjs'));
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(loader.resolve('@oai/artifact-tool')).href);
const directory = path.join(root, args.input || '.local/source-check/run4');
const output = path.join(root, 'docs/research/proposisjon16-62/reviews/source/visual');
await fs.mkdir(output, { recursive: true });
const jobs = [
  ['inntekt-null', 'Forløp', 'B1:K5'],
  ['inntekt-null', 'Fullmakter', 'A1:F10'],
  ['inntekt-null', 'Fullmakter', 'L1:L10'],
  ['inntekt-null', 'Grenbevis', 'A1:G9'],
  ['inntekt-null', 'Kontoer', 'A1:H6'],
  ['inntekt-null', 'Inventar', 'L1:N6'],
  ['inntekt-null', 'T5-dekning', 'B1:G2'],
  ['utgift', 'Forløp', 'B1:K5'],
  ['tekst', 'Utvalg', 'A1:B12'],
  ['tekst', 'Fullmakter', 'A1:F10'],
  ['tekst', 'Fullmakter', 'L1:L10'],
  ['tomt', 'Utvalg', 'A1:B12'],
  ['1533', 'Forløp', 'B1:K5'],
];
const records = [];
let lastName = null, wb;
for (const [name, sheetName, range] of jobs) {
  const input = path.join(directory, name + '.xlsx');
  if (lastName !== name) {
    wb = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
    lastName = name;
  }
  const result = await wb.render({ sheetName, range, scale: 1.5, format: 'png' });
  const target = path.join(output, name + '-' + sheetName + '-' + range.replace(':', '-') + '.png');
  await fs.writeFile(target, new Uint8Array(await result.arrayBuffer()));
  records.push({ input: path.relative(root, input), input_sha256: createHash('sha256').update(await fs.readFile(input)).digest('hex'), sheetName, range, image: path.relative(root, target), image_sha256: createHash('sha256').update(await fs.readFile(target)).digest('hex') });
}
await fs.writeFile(path.join(root, 'docs/research/proposisjon16-62/reviews/source/render-control.json'), JSON.stringify({ tree, base, records }, null, 2));
console.log(JSON.stringify({ rendered: records.length, output }));
