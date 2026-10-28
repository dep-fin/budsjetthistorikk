import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// Rendering leser bare den lagrede XLSX-filen; forfatteren er repoets openpyxl-skriver.
const modules = process.env.BUDSJETT_NODE_MODULES || path.join(path.dirname(path.dirname(process.execPath)), 'node_modules');
const runtimeRequire = createRequire(path.join(modules, 'runtime.cjs'));
const { FileBlob, SpreadsheetFile } = runtimeRequire('@oai/artifact-tool');
const [input, output, mode = 'both'] = process.argv.slice(2);
if (!input || !output) throw new Error('Bruk: node ops/render_fleraarspilot.mjs lagret.xlsx ny-katalog [both|201|empty]');
await fs.mkdir(output, { recursive: false });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const views = [
  ['Forløp', mode === 'empty' ? 'A1:K3' : mode === '201' ? 'A1:K3' : 'A1:K12', 'forlop'],
  ['Dokumenter', 'A1:L6', 'dokumenter'],
  ['Dokumenter', 'C1645:Q1646', 'dokument201-dekning'],
  ['Dokumenter', 'C1745:Q1749', 'dokument201-nivaaer'],
  ['Omtale', 'B1:I5', 'omtale'],
  ['Sammenligninger', mode === 'both' ? 'A1:J15' : 'A1:J3', 'sammenligninger'],
  ['Dekning og avvik', 'A1:B20', 'dekning'],
  ['Dekning og avvik', 'A26:B38', 'aarsbrudd-og-hull'],
  ['Kontroll', 'A1:K12', 'kontroll'],
  ['Offlinegrunnlag', 'A1:B3', 'offline'],
];
const journal = { input, mode, readOnly: true, views: [],
  inspection: (await workbook.inspect({ kind: 'sheet', include: 'id,name', maxChars: 3000 })).ndjson };
for (const [sheetName, range, label] of views) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: 'png' });
  const file = path.join(output, label + '.png');
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  journal.views.push({ sheetName, range, file });
}
journal.amountInspection = (await workbook.inspect({ kind: 'table', range: 'Forløp!A1:K12',
  include: 'values,formulas', tableMaxRows: 12, tableMaxCols: 11, tableMaxCellChars: 100,
  maxChars: 12000 })).ndjson;
await fs.writeFile(path.join(output, 'render.json'), JSON.stringify(journal, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ input, output, renderedViews: journal.views.length }));
