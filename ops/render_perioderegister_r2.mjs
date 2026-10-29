import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// Read-only rendering av faktisk lukket/gjenlest bok. Repoet bruker openpyxl som forfatter.
const modules = process.env.BUDSJETT_NODE_MODULES || path.join(path.dirname(path.dirname(process.execPath)), 'node_modules');
const runtimeRequire = createRequire(path.join(modules, 'runtime.cjs'));
const { FileBlob, SpreadsheetFile } = runtimeRequire('@oai/artifact-tool');
const [input, output] = process.argv.slice(2);
if (!input || !output) throw new Error('Bruk: node ops/render_perioderegister_r2.mjs lagret.xlsx ny-katalog');
await fs.mkdir(output, { recursive: false });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const flow = workbook.worksheets.getItem('Forløp').getRange('S1:S200').values;
const estimate = flow.findIndex(row => row[0] === 'FIN-1429-1') + 1;
const authorization = flow.findIndex(row => row[0] === 'FULLMAKT429') + 1;
const coverage = workbook.worksheets.getItem('Dekning og avvik').getRange('A1:B300').values;
const update = coverage.findIndex(row => String(row[0]).includes('/ separat status for sak 101000')) + 1;
const views = [
  ['Forløp', 'A1:K12', 'forlop'],
  ['Forløp', 'S1:W4', 'forskningskolonner'],
  ['Dekning og avvik', 'A1:B16', 'dekning'],
  ['Dekning og avvik', 'A17:B23', 'globale-hull'],
  ['Dokumenter', 'A1:L6', 'dokumentinventar'],
  ['Omtale', 'B1:I5', 'omtale'],
];
if (estimate) views.push(['Forløp', `S${estimate}:Z${estimate}`, 'foreslatt-anslag']);
if (authorization) views.push(['Forløp', `S${authorization}:Z${authorization}`, 'fullmakt429']);
if (update) views.push(['Dekning og avvik', `A${update}:B${update + 2}`, 'separat-status-og-rest']);
const journal = { input, readOnly: true, nativeExcel: false, views: [],
  sheets: (await workbook.inspect({ kind: 'sheet', include: 'id,name', maxChars: 3000 })).ndjson };
for (const [sheetName, range, label] of views) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: 'png' });
  const file = path.join(output, label + '.png');
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  journal.views.push({ sheetName, range, file });
}
journal.researchInspection = (await workbook.inspect({ kind: 'table', range: 'Forløp!S1:Z30',
  include: 'values,formulas', tableMaxRows: 30, tableMaxCols: 8, tableMaxCellChars: 500, maxChars: 20000 })).ndjson;
await fs.writeFile(path.join(output, 'render.json'), JSON.stringify(journal, null, 2) + '\n');
console.log(JSON.stringify({ input, output, views: journal.views.length }));
