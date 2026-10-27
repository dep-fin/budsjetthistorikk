import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// Les bare den faktisk lagrede boken. Runtime/deps kommer fra load_workspace_dependencies.
const modules = process.env.BUDSJETT_NODE_MODULES || path.join(path.dirname(path.dirname(process.execPath)), 'node_modules');
const runtimeRequire = createRequire(path.join(modules, 'runtime.cjs'));
const { FileBlob, SpreadsheetFile } = runtimeRequire('@oai/artifact-tool');
const [input, output, mode] = process.argv.slice(2);
if (!input || !output) throw new Error('Bruk: node ops/render_forlopspilot.mjs lagret.xlsx ny-katalog [empty]');
await fs.mkdir(output, { recursive: false });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const views = [
  ['Forløp', mode === 'empty' ? 'A1:K3' : 'A1:K10', 'forlop'],
  ['Dokumenter', 'A1:L8', 'dokumenter'],
  ['Omtale', 'B1:I6', 'omtale'],
  ['Sammenligninger', mode === 'empty' ? 'A1:J3' : 'A1:J15', 'sammenligninger'],
  ['Dekning og avvik', 'A1:B30', 'dekning'],
  ['Kontroll', 'A1:K8', 'kontroll'],
  ['Offlinegrunnlag', 'A1:B3', 'offline'],
];
if (mode !== 'empty') views.push(
  ['Dokumenter', 'C974:Q987', 'rnb-1429-hele-blokken'],
  ['Omtale', 'H3:J8', 'lange-felt'],
);
const journal = { input, mode: mode || 'both', readOnly: true, views: [],
  inspection: (await workbook.inspect({ kind: 'sheet', include: 'id,name', maxChars: 3000 })).ndjson };
for (const [sheetName, range, label] of views) {
  const preview = await workbook.render({ sheetName, range, scale: 1, format: 'png' });
  const file = path.join(output, label + '.png');
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  journal.views.push({ sheetName, range, file });
}
journal.amountInspection = (await workbook.inspect({ kind: 'table', range: 'Forløp!A1:K10', include: 'values,formulas',
  tableMaxRows: 10, tableMaxCols: 11, tableMaxCellChars: 90, maxChars: 8000 })).ndjson;
await fs.writeFile(path.join(output, 'render.json'), JSON.stringify(journal, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ input, output, renderedViews: journal.views.length }));
