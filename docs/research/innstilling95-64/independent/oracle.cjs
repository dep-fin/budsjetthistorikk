/* Independent T6 original-source oracle. Node.js standard library only.
 * No product imports, generated product data, or T6 builder files are read.
 * Run: node docs/research/innstilling95-64/independent/oracle.cjs [--check]
 * The sole output is this directory's original-fields.json.
 */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '../../../..');
const DIR = 'docs/research/to-visninger-37/originals/forgrening/';
const PROP = 'docs/research/omtale-o1/originals/prop16s-ch4.html';
const PARENT = 'docs/research/to-visninger-37/originals/aar/session-2024-2025.xml.gz';
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const sources = {};
function read(file) {
  const b = fs.readFileSync(path.join(ROOT, file));
  sources[file] = { bytes: b.length, sha256: hash(b) };
  return b;
}
function unescape(s) {
  return s.replace(/&(#x[\da-f]+|#\d+|amp|lt|gt|quot|apos|nbsp);/gi, (_, x) => {
    const entities = { amp:'&', lt:'<', gt:'>', quot:'"', apos:"'", nbsp:'\u00a0' };
    return x[0] === '#' ? String.fromCodePoint(x[1].toLowerCase() === 'x'
      ? parseInt(x.slice(2),16) : parseInt(x.slice(1),10)) : entities[x];
  });
}
function text(s) { return unescape(s.replace(/<[^>]*>/g, ' ')).replace(/\s+/g,' ').trim(); }
function encodeXml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function locate(source, full, raw, locator, encoded = false, anchor = raw) {
  const needle = encoded ? encodeXml(raw) : raw;
  const anchorNeedle = encoded ? encodeXml(anchor) : anchor;
  const anchorStart = full.indexOf(anchorNeedle);
  assert(anchorStart >= 0, `Missing anchor: ${locator}`);
  const start = full.indexOf(needle,anchorStart);
  assert(start >= 0, `Missing original span: ${locator}`);
  assert(start+needle.length<=anchorStart+anchorNeedle.length,`Span outside anchor: ${locator}`);
  return { source, source_sha256:sources[source].sha256, locator,
    byte_start_0:Buffer.byteLength(full.slice(0,start)), byte_end_exclusive:Buffer.byteLength(full.slice(0,start+needle.length)),
    raw_html:raw, raw_text:text(raw), raw_sha256:hash(Buffer.from(raw)) };
}
// Balanced DIV selection is independent of the product's HTML parser.
function balancedDiv(s,start,openingLength) {
  const re=/<\/?div\b[^>]*>/g;re.lastIndex=start+openingLength;
  let depth=1,token;
  while(depth && (token=re.exec(s))) depth+=token[0][1]==='/'?-1:1;
  assert.equal(depth,0);return s.slice(start,re.lastIndex);
}
function romans(s) {
  const result = {};
  for (const m of s.matchAll(/<div\b[^>]*data-strtngt-romertallseksjon-romertall=['"]([^'"]+)['"][^>]*>/g)) {
    const roman=m[1].toUpperCase();
    assert(!result[roman],`Duplicate Roman ${roman}`);
    result[roman]=balancedDiv(s,m.index,m[0].length);
  }
  return result;
}
function tables(s) { return [...s.matchAll(/<table\b[^>]*>[\s\S]*?<\/table>/gi)].map(m=>m[0]); }
function rows(s) { return [...s.matchAll(/<tr\b[^>]*>[\s\S]*?<\/tr>/gi)].map(m=>m[0]); }
function cells(s) { return [...s.matchAll(/<t[dh]\b[^>]*>[\s\S]*?<\/t[dh]>/gi)].map(m=>m[0]); }
function integer(s) { assert(/^[\d\s]+$/.test(s),s); return Number(s.replace(/\s/g,'')); }
function tableFields(source,full,html,prefix,role,encoded=false) {
  const result=[];
  for (const [ti,table] of tables(html).entries()) {
    const rr=rows(table); let chapter=null;
    for (let ri=0;ri<rr.length;ri++) {
      const cc=cells(rr[ri]), tt=cc.map(text);
      if (/^\d{4}$/.test(tt[0])) chapter=Number(tt[0]);
      if (!chapter || !/^\d{1,2}$/.test(tt[1]||'') || !/(økes|reduseres)\s+med/.test(tt[2]||'')) continue;
      const post=Number(tt[1]), next=cells(rr[ri+1]), ntext=next.map(text);
      const beforeAfter=ntext[2].match(/^fra kr ([\d\s]+?) til kr ([\d\s]+)$/);
      assert(beforeAfter, `${chapter}/${post}: ${ntext[2]}`);
      const delta=integer(tt[3])*(tt[2].includes('reduseres')?-1:1);
      const before=integer(beforeAfter[1]),after=integer(beforeAfter[2]);
      assert.equal(before+delta,after,`${chapter}/${post} arithmetic`);
      const rowLocator=`${prefix}/table[${ti+1}]/tr[${ri+1}]`;
      const values={before_kr:before,change_kr:delta,after_kr:after};
      const pointers={};
      for (const field of Object.keys(values)) {
        const change=field==='change_kr';
        const fieldRow=change?ri:ri+1,ci=change?3:2,raw=change?cc[ci]:next[ci];
        pointers[field]={...locate(source,full,raw,`${prefix}/table[${ti+1}]/tr[${fieldRow+1}]/td[${ci+1}]`,encoded,rr[fieldRow]),
          raw_number:field==='before_kr'?beforeAfter[1]:field==='after_kr'?beforeAfter[2]:tt[3],
          sign_evidence:change?tt[2]:null};
      }
      const rowStart=table.indexOf(rr[ri]),nextStart=table.indexOf(rr[ri+1],rowStart+rr[ri].length);
      const rawRows=table.slice(rowStart,nextStart+rr[ri+1].length);
      result.push({account:`${chapter}/${post}`,chapter,post,budget_year:2024,currency:'NOK',multiplier:1,
        role,values,pointers,row:locate(source,full,rawRows,rowLocator+' + following tr',encoded)});
    }
  }
  assert.equal(new Set(result.map(r=>r.account)).size,result.length,'duplicate accounts');
  return result;
}
const innFile=DIR+'inns95s.html', innFull=read(innFile).toString('utf8');
const innRomans=romans(innFull);
assert.deepEqual(Object.keys(innRomans),['I','II','III','IV','V','VI']);
const inn=tableFields(innFile,innFull,innRomans.I,'95/tilraading/I','samlet_komite_tilraading');
assert.equal(inn.length,36);
assert.equal(new Set(inn.map(x=>x.chapter)).size,14);
const parent=zlib.gunzipSync(read(PARENT));
assert.equal(parent.length,7479943);
assert.equal(hash(parent),'c5f3b90046d23a0e4cacb24f681a01d7e5fd4468ab68fc3d646dc832bb9a4b42');
const parentMetaFile=PARENT.replace('.xml.gz','.meta.json');
const parentMeta=JSON.parse(read(parentMetaFile));
assert.equal(parentMeta.sha256,hash(parent));assert.equal(parentMeta.bytes,parent.length);
const parentText=parent.toString('utf8');
const originalObjects=[...parentText.matchAll(/ {4}<stortingsvedtak>[\s\S]*? {4}<\/stortingsvedtak>/g)];
const decisions=[],decRomans={};
for(let n=0;n<6;n++) {
  const id=40034220+n,number=359+n,source=DIR+id+'.xml';
  const sideFile=DIR+id+'.json',side=JSON.parse(read(sideFile));
  assert.equal(side.source_response_sha256,hash(parent));
  assert.equal(side.source_response_bytes,parent.length);
  assert.equal(side.source_response.sha256,hash(parent));
  assert.equal(side.source_response.bytes,parent.length);
  assert.equal(side.object_bytes,side.object_end_byte_exclusive-side.object_start_byte_0);
  assert.equal(side.suffix_bytes,parent.length-side.suffix_start_byte_0);
  assert.equal(side.inserted_separator_bytes,0);
  const originalIndex=originalObjects.findIndex(m=>m[0].includes(`<id>${id}</id>`));
  assert(originalIndex>=0);
  const originalObject=originalObjects[originalIndex];
  assert.equal(originalIndex+1,side.object_ordinal_1);
  assert.equal(Buffer.byteLength(parentText.slice(0,originalObject.index)),side.object_start_byte_0);
  assert.equal(Buffer.byteLength(parentText.slice(0,originalObject.index+originalObject[0].length)),side.object_end_byte_exclusive);
  const rebuilt=Buffer.concat([parent.subarray(0,side.prefix_bytes),
    parent.subarray(side.object_start_byte_0,side.object_end_byte_exclusive),parent.subarray(side.suffix_start_byte_0)]);
  assert.equal(hash(rebuilt),side.sha256);assert.equal(rebuilt.length,side.bytes);
  assert.deepEqual(rebuilt,read(source));
  const xml=rebuilt.toString('utf8');
  const tag=k=>{const m=xml.match(new RegExp(`<${k}>([\\s\\S]*?)<\\/${k}>`));assert(m,k);return unescape(m[1]);};
  const object=xml.match(/<stortingsvedtak>([\s\S]*?)<\/stortingsvedtak>/)[1];
  assert.equal(object.match(/<id>(\d+)<\/id>/)[1],String(id));
  assert.equal(tag('sak_id'),'100889'); assert.equal(tag('stortingsvedtak_nummer'),String(number));
  assert.equal(tag('sesjon_id'),'2024-2025');assert.equal(tag('stortingsvedtak_dato_tid'),'2024-12-18T00:00:00');
  assert(xml.match(/<stortingsvedtak_type>\s*<id>ANNET<\/id>/));
  const html=tag('stortingsvedtak_tekst'),roman=romans(html),romanKey=Object.keys(innRomans)[n];
  assert.deepEqual(Object.keys(roman),[romanKey]);
  decRomans[romanKey]={source,full:xml,html:roman[romanKey],number,api_id:id};
  decisions.push({api_id:id,number,case_id:100889,session:'2024-2025',date:'2024-12-18',type:'ANNET',roman:romanKey,
    source,source_sha256:hash(rebuilt),bytes:rebuilt.length,sidecar:sideFile,sidecar_sha256:sources[sideFile].sha256,
    parent_sha256:hash(parent),object_ordinal_1:side.object_ordinal_1,prefix_bytes:side.prefix_bytes,
    object_start_byte_0:side.object_start_byte_0,object_end_byte_exclusive:side.object_end_byte_exclusive,
    suffix_start_byte_0:side.suffix_start_byte_0,inserted_separator_bytes:0,byte_identical:true});
}
const d359=decRomans.I;
const adopted=tableFields(d359.source,d359.full,d359.html,'359/stortingsvedtak_tekst/I','stortingsvedtak',true);
assert.equal(adopted.length,36);
assert.deepEqual(inn.map(r=>[r.account,r.values]),adopted.map(r=>[r.account,r.values]));
const propFull=read(PROP).toString('utf8');
const prop=tableFields(PROP,propFull,propFull,'Prop16/vedtak/I','regjeringsforslag');
assert.equal(prop.length,37);
const propKeywordParagraphs=[...propFull.matchAll(/<p>Tilføye stikkordet[\s\S]*?<\/p>/g)].map(m=>m[0]);
assert.equal(propKeywordParagraphs.length,3);
const propKeywordPoints=propKeywordParagraphs.map((raw,i)=>{
  const account=['1420/66','1420/87','1429/60'][i];
  const [chapter,post]=account.split('/');assert(text(raw).includes('kap. '+chapter)&&text(raw).includes('post '+post));
  return {roman:'V',point:String(i+1),account,status:i===2?'utenfor_95_og_T6_vedtak':'til_95_V_og_363',
    evidence:locate(PROP,propFull,raw,`Prop16/V/ol/li[${i+1}]/p`)};
});
const byProp=Object.fromEntries(prop.map(r=>[r.account,r]));
const common=[],missing=[];
for(const row of inn) {
  const previous=byProp[row.account];
  if(previous) {
    assert.deepEqual(previous.values,row.values);
    common.push({account:row.account,prop:previous,innstilling:row,
      differences_kr:{before_kr:0,change_kr:0,after_kr:0}});
  } else for(const meaning of Object.keys(row.values)) missing.push({account:row.account,meaning,
    proposal_value:null,difference_kr:null,status:'manglende_Prop16_tabellrad',innstilling_value:row.values[meaning]});
}
assert.equal(common.length,35);assert.equal(missing.length,3);
assert.deepEqual(missing.map(x=>x.account),['1420/32','1420/32','1420/32']);
assert.deepEqual(inn.find(r=>r.account==='1420/32').values,{before_kr:812765000,change_kr:270000000,after_kr:1082765000});
assert.deepEqual(inn.find(r=>r.account==='4400/2').values,{before_kr:518000,change_kr:-518000,after_kr:0});
// Full authorization paragraphs/cells are kept, including all conditions.
function paragraphs(s) { return [...s.matchAll(/<p\b[^>]*>[\s\S]*?<\/p>/g)].map(m=>m[0]); }
function atomicAuth(source,full,section,roman,stage,encoded) {
  const p=paragraphs(section),all=text(section),pointer=raw=>locate(source,full,raw,`${stage}/${roman}/original-span`,encoded);
  const base={stage,roman,role:stage==='95'?'samlet_komite_tilraading':'stortingsvedtak',budget_year:2024,
    period:'2024',is_monetary_event:false};
  if(roman==='II') {
    assert(/fremtidige år/.test(all)&&/8 mill\. kroner/.test(all)&&/1420/.test(all)&&/post 21/.test(all));
    return [{...base,point:'1',kind:'bestillingsfullmakt',accounts:['1420/21'],frame_kr:8000000,
      period:'2024 og fremtidige år',evidence:pointer(p.find(x=>text(x).includes('Stortinget samtykker')))}];
  }
  if(roman==='III') {
    const result=[];
    for(const row of rows(section)) {
      const c=cells(row),t=c.map(text);
      if(!['61','62'].includes(t[1]))continue;
      const frame=t[3].match(/^(\d+),(\d+) mill\. kroner$/);assert(frame);
      const value=Number(frame[1]+'.'+frame[2])*1000000;
      assert.equal(value,t[1]==='61'?601000000:266300000);
      result.push({...base,point:t[1],kind:'tilsagnsfullmakt',accounts:['1420/'+t[1]],frame_kr:value,
        evidence:pointer(row),conditions:pointer(p.find(x=>text(x).includes('Stortinget samtykker')))});
    }
    assert.equal(result.length,2);return result;
  }
  if(roman==='IV') {
    assert(/16,3 mill\. kroner/.test(all)&&/postene 39, 69 og 79/.test(all)&&/fremtidige år/.test(all));
    return [{...base,point:'1',kind:'delt_forpliktelsesramme',accounts:['1420/39','1420/69','1420/79'],
      frame_kr:16300000,period:'2024 og fremtidige år',shared_frame:true,
      evidence:pointer(p.find(x=>text(x).includes('Stortinget samtykker')))}];
  }
  if(roman==='V') {
    const pp=p.filter(x=>/^\d\./.test(text(x))); assert.equal(pp.length,2);
    return pp.map((raw,i)=>{assert(text(raw).includes(`post ${[66,87][i]}`)&&text(raw).includes('kan overføres'));
      return {...base,point:String(i+1),kind:'stikkordsfullmakt',accounts:['1420/'+[66,87][i]],frame_kr:null,evidence:pointer(raw)};});
  }
  assert.equal(roman,'VI');
  const pp=p.filter(x=>/^\d\./.test(text(x)));assert.equal(pp.length,2);
  assert(/25 mill\. kroner/.test(text(pp[0]))&&/betryggende sikkerhet/.test(text(pp[0]))&&/bindende avtale/.test(text(pp[0])));
  assert(/1471/.test(text(pp[0]))&&/post 1 /.test(text(pp[0]))&&/4471/.test(text(pp[0]))&&/post 3 /.test(text(pp[0])));
  assert(/mellomværendet med statskassen/.test(text(pp[1]))&&/rapportert til statsregnskapet/.test(text(pp[1])));
  return pp.map((raw,i)=>({...base,point:String(i+1),kind:i?'regnskapsregel':'forskutteringsfullmakt',
    accounts:i?[]:['1471/1','4471/3'],frame_kr:i?null:25000000,evidence:pointer(raw)}));
}
const authorizations=[];
for(const roman of ['II','III','IV','V','VI']) {
  const d=decRomans[roman];
  const a=atomicAuth(innFile,innFull,innRomans[roman],roman,'95',false);
  const b=atomicAuth(d.source,d.full,d.html,roman,String(d.number),true);
  const semantic=x=>[x.point,x.kind,x.accounts,x.frame_kr];
  assert.deepEqual(a.map(semantic),b.map(semantic));
  authorizations.push(...a,...b);
}
assert.equal(authorizations.filter(x=>x.stage==='95').length,8);
assert.equal(authorizations.filter(x=>x.stage!=='95').length,8);
const pp=paragraphs(innFull);
const statementRules=[
  ['Ap_Sp_SV','komitemerknad','1420/32',/foreslår å øke støtten til skogvern/],
  ['Høyre','komitemerknad',null,/medlemmer fra Høyre/],
  ['Fremskrittspartiet','komitemerknad',null,/medlemmer fra Fremskrittspartiet/],
  ['samlet_komite','tilraading',null,/tilråding fremmes av en samlet komité/]
];
const statements=statementRules.flatMap(([author,role,account,re])=>{
  const matched=pp.filter(raw=>re.test(text(raw)));assert(matched.length,author);
  return matched.map(raw=>({author,role,account,not_parliament_reasoning:true,
    evidence:locate(innFile,innFull,raw,'95/komitemerknader-eller-tilraading/p')}));
});
const plenFile=DIR+'votering-181224.html',plenFull=read(plenFile).toString('utf8');
const plain=text(plenFull.replace(/<script\b[\s\S]*?<\/script>/gi,''));
const case13=plain.slice(plain.indexOf('Votering i sak nr. 13,'),plain.indexOf('Votering i sak nr. 14,'));
assert(case13.includes('Innst. 95 S (2024–2025)'));
assert(case13.includes('unntatt kap. 1429'));
assert(case13.includes('Komiteens innstilling ble enstemmig vedtatt.'));
const plenumEvidence={source:plenFile,source_sha256:sources[plenFile].sha256,
  locator:'Votering i sak nr. 13, debattert 18. desember 2024; før Votering i sak nr. 14',
  outcome:'Komiteens innstilling ble enstemmig vedtatt.',round_evidence:'en dokumentert votering i sak nr. 13; ingen egen rundeopplysning i API-utdraget',
  innstilling:'Innst. 95 S (2024–2025)',scope:'I–VI, unntatt kap. 1429',full_case_text:case13};
const webFile=DIR+'vedtak-100889.html',webFull=read(webFile).toString('utf8'),webRomans=romans(webFull);
assert.deepEqual(Object.keys(webRomans),Object.keys(innRomans));
for(const d of decisions) {
  assert(webFull.includes(`Vedtak ${d.number}`));
  assert.equal(text(webRomans[d.roman]),text(decRomans[d.roman].html));
}
const web359=tableFields(webFile,webFull,webRomans.I,'vedtaksside/359/I','stortingsvedtak');
assert.deepEqual(web359.map(x=>[x.account,x.values]),inn.map(x=>[x.account,x.values]));
const reusedFile=DIR+'inns95s-20261022-reused.html',reusedFull=read(reusedFile).toString('utf8');
const reusedRomans=romans(reusedFull);
for(const roman of Object.keys(innRomans))assert.equal(text(reusedRomans[roman]),text(innRomans[roman]));
assert(text(innFull).includes('BERIKTIGET'));assert(text(reusedFull).includes('BERIKTIGET'));
const mainTextChecks=[];
for(const id of ['m1','m2','m3','m4']) {
  const section=(full)=>{
    const m=full.match(new RegExp(`<div id="${id}" data-bigdoc-section>`));assert(m);
    return balancedDiv(full,m.index,m[0].length);
  };
  const a=section(innFull),b=section(reusedFull);
  assert.equal(text(a),text(b));
  mainTextChecks.push({section_id:id,normalized_text_sha256:hash(text(a)),identical:true});
}
const output={format:'independent-original-fields-innstilling95-1',method:'Node.js standard library; original-only; no product imports or product parser',
  base_commit:'9616fbe6a8ab15eec696f34de76888565a784f8f',
  counts:{accounts:36,chapters:14,innstilling_fields:108,decision_fields:108,common_prop_trios:35,
    zero_prop_innstilling_differences:105,zero_innstilling_decision_differences:108,missing_proposal_fields:3,
    authorization_details_per_stage:8,new_formal_authorization_decisions:5,new_monetary_events:36},
  sources,uncompressed_parent:{bytes:parent.length,sha256:hash(parent)},decisions,
  innstilling_rows:inn,decision_rows:adopted,prop_rows:prop,common_prop_trios:common,missing_proposal_fields:missing,
  authorizations,prop_keyword_points:propKeywordPoints,formal_authorization_relations:decisions.slice(1).map(d=>({from_document:'inns95',roman:d.roman,to_document:'vedtak'+d.number,api_id:d.api_id,
    source_sha256:d.source_sha256,year:2024,is_monetary_event:false})),statements,plenumEvidence,
  source_representation_check:{both_beriktiget:true,all_roman_sections_normalized_text_identical:true,
    main_sections:mainTextChecks,
    uncorrected_version_or_correction_notice_found:false,unknown_correction_history:true},
  limits:['Full omtale er ikke semantisk kontoavklart.','Identisk bevilgningstabell er ikke alene vedtakelsesbevis; plenumsutfall og formelle API-objekter er kontrollert.',
    'Ingen faglig årsdekning, kontokontinuitet eller faktisk fullmaktsbruk følger.']};
const serialized=JSON.stringify(output,null,2)+'\n';
const outfile=path.join(__dirname,'original-fields.json');
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(outfile,'utf8'),serialized,'Stored oracle differs from originals');
else fs.writeFileSync(outfile,serialized);
console.log(JSON.stringify({status:'passed',output:path.relative(ROOT,outfile).replaceAll('\\','/'),sha256:hash(serialized),counts:output.counts}));
