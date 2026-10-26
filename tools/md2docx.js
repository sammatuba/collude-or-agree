// Markdown subset -> .docx. Needs the npm package docx (install in a scratch folder: npm install docx@9.5.1).
// Usage: NODE_PATH=<scratch>/node_modules node tools/md2docx.js in.md out.docx
// Convert a Markdown subset (headings, paragraphs, lists, tables, code, bold/italic/code spans)
// to .docx with docx-js. Usage: node build.js in.md out.docx
const fs = require("fs");
const d = require("docx");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, LevelFormat, Footer, PageNumber } = d;

const [inp, out] = process.argv.slice(2);
let md = fs.readFileSync(inp, "utf8");
md = md.replace(/^---\n[\s\S]*?\n---\n/, "").replace(/<!--[\s\S]*?-->/g, "");
const lines = md.split("\n");

const FONT = "Calibri", MONO = "Consolas", PAGE_W = 9360;
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*\s][^*]*\*|\[\d{1,2}(?:,\s*\d{1,2})*\])/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, font: FONT, ...base }));
    else if (t.startsWith("`")) out.push(new TextRun({ text: t.slice(1, -1), font: MONO, size: 19, ...base }));
    else if (t.startsWith("[")) out.push(new TextRun({ text: t.slice(1, -1), superScript: true, font: FONT, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), italics: true, font: FONT, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...base }));
  return out;
}
const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(rows) {
  const cells = rows.map(r => r.replace(/^\||\|$/g, "").split("|").map(c => c.trim()));
  const n = Math.max(...cells.map(r => r.length));
  const len = Array(n).fill(4);
  cells.forEach(r => r.forEach((c, i) => { len[i] = Math.max(len[i], Math.min(c.length, 60)); }));
  const tot = len.reduce((a, b) => a + b, 0);
  let widths = len.map(l => Math.max(700, Math.round(PAGE_W * l / tot)));
  const s = widths.reduce((a, b) => a + b, 0);
  widths = widths.map(w => Math.round(w * PAGE_W / s));
  widths[n - 1] += PAGE_W - widths.reduce((a, b) => a + b, 0);
  const small = n >= 8 ? 16 : 19;
  return new Table({
    width: { size: PAGE_W, type: WidthType.DXA }, columnWidths: widths,
    rows: cells.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: Array.from({ length: n }, (_, i) => new TableCell({
        width: { size: widths[i], type: WidthType.DXA }, borders,
        shading: ri === 0 ? { fill: "E7ECF2", type: ShadingType.CLEAR, color: "auto" } : undefined,
        margins: { top: 60, bottom: 60, left: 90, right: 90 },
        children: [new Paragraph({ children: runs(r[i] || "", { size: small, bold: ri === 0 ? true : undefined }) })],
      })),
    })),
  });
}

const children = [];
let para = [], numInstance = 0, inNum = false, i = 0;
const flush = () => { if (para.length) { children.push(new Paragraph({ spacing: { after: 120 }, children: runs(para.join(" ")) })); para = []; } };
while (i < lines.length) {
  const line = lines[i], s = line.trim();
  if (s.startsWith("```")) {
    flush(); i++;
    while (i < lines.length && !lines[i].trim().startsWith("```")) {
      children.push(new Paragraph({ shading: { fill: "F2F2F2", type: ShadingType.CLEAR, color: "auto" },
        children: [new TextRun({ text: lines[i] || " ", font: MONO, size: 18 })] }));
      i++;
    }
    i++; continue;
  }
  if (s.startsWith("|")) {
    flush(); const rows = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) {
      if (!/^\|[\s\-:|]+\|$/.test(lines[i].trim())) rows.push(lines[i].trim());
      i++;
    }
    children.push(table(rows)); children.push(new Paragraph({ children: [] })); continue;
  }
  if (!s) { flush(); inNum = false; i++; continue; }
  if (s === "---") { flush(); children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "AAAAAA", space: 1 } }, children: [] })); i++; continue; }
  let m;
  if ((m = s.match(/^!\[([^\]]*)\]\(([^)]+)\)$/))) {
    // Image line: ![caption](relative/path.png). Scaled to the text width, caption below.
    flush();
    const path = require("path");
    const imgPath = path.resolve(path.dirname(inp), m[2]);
    const data = fs.readFileSync(imgPath);
    const sz = require("image-size");
    const dim = sz.imageSize ? sz.imageSize(data) : sz(data);
    const maxW = 624, w = Math.min(maxW, dim.width), h = Math.round(dim.height * (w / dim.width));
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 },
      children: [new d.ImageRun({ type: m[2].endsWith(".png") ? "png" : "jpg", data, transformation: { width: w, height: h } })] }));
    if (m[1]) children.push(new Paragraph({ spacing: { after: 160 }, children: runs(m[1], { size: 19, italics: true }) }));
    i++; continue;
  }
  if ((m = s.match(/^(#{1,3})\s+(.*)$/))) {
    flush(); const lv = m[1].length;
    const heading = lv === 1 ? HeadingLevel.TITLE : lv === 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2;
    children.push(new Paragraph({ heading, children: runs(m[2]) })); i++; continue;
  }
  const indent = line.match(/^\s*/)[0].length;
  if ((m = s.match(/^[-*]\s+(.*)$/))) {
    flush(); children.push(new Paragraph({ numbering: { reference: "bul", level: indent >= 2 ? 1 : 0 }, spacing: { after: 60 }, children: runs(m[1]) })); i++; continue;
  }
  if ((m = s.match(/^(\d+)\.\s+(.*)$/))) {
    flush(); if (!inNum || m[1] === "1") { numInstance++; inNum = true; }
    children.push(new Paragraph({ numbering: { reference: "num", level: 0, instance: numInstance }, spacing: { after: 60 }, children: runs(m[2]) })); i++; continue;
  }
  inNum = inNum && false;
  para.push(s); i++;
}
flush();

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 34, bold: true, font: FONT, color: "1F3864" }, paragraph: { spacing: { after: 240 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, font: FONT, color: "1F3864" }, paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, font: FONT, color: "2E5395" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } } ] },
    { reference: "num", levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } } ] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("wrote", out, b.length, "bytes"); });
