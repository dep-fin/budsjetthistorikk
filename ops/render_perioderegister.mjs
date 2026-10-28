import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// Les faktisk lagret bok; openpyxl er forfatter etter repoets kontrakt.
const modules = process.env.BUDSJETT_NODE_MODULES || path.join(path.dirname(path.dirname(process.execPath)), 'node_modules');
const runtimeRequire = createRequire(path.join(modules, 'runtime.cjs'));
const { FileBlob, SpreadsheetFile } = runtimeRequire('@oai/artifact-tool');
const [input, output] = process.argv.slice(2);
if (!input || !output) throw new Error('Bruk: node ops/render_perioderegister.mjs lagret.xlsx ny-katalog');
await fs.mkdir(output, { recursive: false });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const documents = workbook.worksheets.getItem('Dokumenter').getRange('A1:Q3000').values;
const fullmakt = documents.findIndex(row => row[0] === 'Dokument' && String(row[2]).includes('346/40032933')) + 1;
const candidate = documents.findIndex(row => row[0] === 'Indeksinventar') + 1;
const views = [
  ['Forløp', 'A1:K12', 'forlop'],
  ['Forløp', 'N1:R8', 'originalreferanser'],
  ['Dokumenter', 'A1:L6', 'dokumenter'],
  ['Dokumenter', `C${fullmakt}:Q${fullmakt + 5}`, 'fullmakt-inventar'],
  ['Dokumenter', `C${candidate}:Q${candidate + 2}`, 'indeksinventar'],
  ['Omtale', 'B1:I5', 'omtale'],
  ['Sammenligninger', 'A1:J8', 'sammenligninger'],
  ['Dekning og avvik', 'A1:B16', 'dekning'],
  ['Dekning og avvik', 'A17:B23', 'globale-hull'],
  ['Kontroll', 'A1:K8', 'kontroll'],
  ['Offlinegrunnlag', 'A1:B3', 'offline'],
];
if (workbook.worksheets.getItem('Forløp').getRange('A13:A27').values.some(row => Boolean(row[0]))) {
  views.push(['Forløp', 'A13:K27', 'forlop-fortsettelse']);
}
const journal = { input, readOnly: true, nativeExcel: false, views: [],
  sheets: (await workbook.inspect({ kind: 'sheet', include: 'id,name', maxChars: 3000 })).ndjson };
for (const [sheetName, range, label] of views) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: 'png' });
  const file = path.join(output, label + '.png');
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  journal.views.push({ sheetName, range, file });
}
journal.amountInspection = (await workbook.inspect({ kind: 'table', range: 'Forløp!A1:R12',
  include: 'values,formulas', tableMaxRows: 12, tableMaxCols: 18, tableMaxCellChars: 100, maxChars: 14000 })).ndjson;
await fs.writeFile(path.join(output, 'render.json'), JSON.stringify(journal, null, 2) + '\n');
console.log(JSON.stringify({ input, output, views: journal.views.length }));
