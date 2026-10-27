import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

// Bundlet Node fra load_workspace_dependencies; ingen repoavhengigheter installeres.
const modules = process.env.BUDSJETT_NODE_MODULES || path.join(path.dirname(path.dirname(process.execPath)), 'node_modules');
const runtimeRequire = createRequire(path.join(modules, 'runtime.cjs'));
const { FileBlob, SpreadsheetFile } = runtimeRequire('@oai/artifact-tool');
const [input, output] = process.argv.slice(2);
if (!input || !output) throw new Error('Bruk: node ops/render_komitepilot.mjs lagret.xlsx ny-katalog');
await fs.mkdir(output, { recursive: false });
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const journal = { input, views: [], inspection: (await workbook.inspect({ kind: 'sheet', include: 'id,name', maxChars: 3000 })).ndjson };
const views = [
  ['Forløp', 'A1:J7'], ['Dokumenter', 'A1:L10'], ['Omtale', 'B1:I8'],
  ['Sammenligninger', 'A1:I7'], ['Dekning og avvik', 'A1:B20'],
  ['Kontroll', 'A1:J8'], ['Offlinegrunnlag', 'A1:B3'],
];
for (const [sheetName, range] of views) {
  const preview = await workbook.render({ sheetName, range, scale: 1.3, format: 'png' });
  const file = path.join(output, sheetName + '.png');
  await fs.writeFile(file, new Uint8Array(await preview.arrayBuffer()));
  journal.views.push({ sheetName, range, file });
}
journal.amountInspection = (await workbook.inspect({ kind: 'table', range: 'Forløp!A1:J7', include: 'values,formulas', tableMaxRows: 7, tableMaxCols: 10, tableMaxCellChars: 80, maxChars: 5000 })).ndjson;
await fs.writeFile(path.join(output, 'render.json'), JSON.stringify(journal, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ input, output, renderedSheets: journal.views.length }));
