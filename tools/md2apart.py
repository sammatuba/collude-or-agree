#!/usr/bin/env python3
"""md2apart.py: build the sprint paper as a Word file on the Apart Research template.

Usage (from any directory):
    python3 tools/md2apart.py
    python3 tools/md2apart.py --report path/to/REPORT.md --out path/to/OUT.docx

Standard library only (zipfile, re, struct, xml.etree). No network, no API calls.

What the script does:
1. Opens the template `sources/apart-template/Apart Research hackathon submission
   template.docx` in memory and keeps every part (styles, embedded fonts, numbering,
   footnotes, settings, theme, page setup).
2. Keeps the template's front block (the outer table that holds the Title paragraph,
   the author grid, "With Apart Research", the "Abstract" label, and the abstract box)
   and patches it: the title text, one author line with the paper's placeholder, and
   the abstract paragraph. The footnote reference on the title is kept.
3. Drops every guidance paragraph and the yellow "How to use this template" box.
4. Rebuilds the rest of `word/document.xml` from `REPORT.md` with the template's
   style ids (Heading2 for `##`, Heading3 for `###`, Normal for text, Table1 for
   tables, the template's bullet and decimal numbering definitions).
5. Adds each PNG figure to `word/media/`, with a relationship and a content type.
6. Checks the result: paragraph counts by style, drawings, media files, table
   column counts against the Markdown, and a grep for surviving guidance text.

Markdown subset read: YAML frontmatter and HTML comments (dropped), `# title`,
`##` and `###` headings, paragraphs with **bold** *italic* `code`, `- ` bullets
(two-space indent gives level 2), `1. ` numbered lists (a new list starts at "1."),
pipe tables with an alignment row, fenced code blocks, image lines
`![caption](figures/x.png)`, bare http(s) URLs (made clickable), status tags
[ESTABLISHED] [FINDING] [INTERPRETATION] [HYPOTHESIS] [SPECULATION] (bold small
caps), and `[AUTHOR: ...]` notes (yellow highlight so the owner can find them).
Bracket citations such as [S1] stay literal text.
"""

from __future__ import annotations

import argparse
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape as _xml_escape

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "sources" / "apart-template" / "Apart Research hackathon submission template.docx"
REPORT = REPO / "projects" / "2026-10-apart-collusion-sprint" / "report" / "REPORT.md"
OUT = REPO / "projects" / "2026-10-apart-collusion-sprint" / "report" / "REPORT-APART.docx"

FONT = "Old Standard TT"
MONO = "Courier New"
TEXT_WIDTH = 9360  # twips, 6.5 in
TEXT_WIDTH_EMU = 5943600
STATUS_TAGS = ("ESTABLISHED", "FINDING", "INTERPRETATION", "HYPOTHESIS", "SPECULATION")
GUIDANCE_STRINGS = (
    "Replace the italicized",
    "How to use this template",
    "Author name",
    "Summarize your project",
    "Reference 1",
    "First contribution",
    "Evaluation Rubric",
    "PROJECT TITLE",
)
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def esc(text: str) -> str:
    """Escape text for an XML text node or attribute value."""
    return _xml_escape(text, {'"': "&quot;"})


# ----------------------------------------------------------------------------
# Markdown parsing
# ----------------------------------------------------------------------------


class Block:
    """One block of the Markdown document.

    kind: title | author | h2 | h3 | p | bullets | numbered | table | code | image
    """

    def __init__(self, kind: str, **data):
        self.kind = kind
        self.data = data

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Block({self.kind}, {self.data})"


def parse_markdown(md: str) -> list[Block]:
    md = re.sub(r"\A---\n.*?\n---\n", "", md, count=1, flags=re.S)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.split("\n")
    blocks: list[Block] = []
    para: list[str] = []
    i = 0
    list_kind: str | None = None  # kind of the list block that is open

    def flush() -> None:
        nonlocal para
        if para:
            text = " ".join(s.strip() for s in para)
            if blocks and blocks[-1].kind == "title":
                # The first paragraph after the title is the author line.
                blocks.append(Block("author", text=text))
            else:
                blocks.append(Block("p", text=text))
            para = []

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            list_kind = None
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            blocks.append(Block("code", lines=code))
            continue
        if s.startswith("|"):
            flush()
            list_kind = None
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not re.fullmatch(r"\|[\s\-:|]+\|?", row):
                    cells = row.strip().strip("|").split("|")
                    rows.append([c.strip() for c in cells])
                i += 1
            ncols = len(rows[0]) if rows else 0
            rows = [r + [""] * (ncols - len(r)) if len(r) < ncols else r[:ncols] for r in rows]
            blocks.append(Block("table", rows=rows, ncols=ncols))
            continue
        if not s:
            flush()
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            flush()
            list_kind = None
            i += 1
            continue
        m = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", s)
        if m:
            flush()
            list_kind = None
            blocks.append(Block("image", caption=m.group(1), path=m.group(2)))
            i += 1
            continue
        m = re.fullmatch(r"(#{1,3})\s+(.*)", s)
        if m:
            flush()
            list_kind = None
            level = len(m.group(1))
            text = m.group(2).strip()
            kind = {1: "title", 2: "h2", 3: "h3"}[level]
            blocks.append(Block(kind, text=text))
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        m = re.fullmatch(r"[-*]\s+(.*)", s)
        if m:
            flush()
            level = 1 if indent >= 2 else 0
            if list_kind != "bullets":
                blocks.append(Block("bullets", items=[]))
                list_kind = "bullets"
            blocks[-1].data["items"].append((level, m.group(1)))
            i += 1
            continue
        m = re.fullmatch(r"(\d+)\.\s+(.*)", s)
        if m:
            flush()
            if list_kind != "numbered" or m.group(1) == "1":
                blocks.append(Block("numbered", items=[]))
                list_kind = "numbered"
            blocks[-1].data["items"].append((0, m.group(2)))
            i += 1
            continue
        # Continuation of a paragraph, or a wrapped list item.
        if list_kind and indent >= 2 and blocks and blocks[-1].kind == list_kind and not para:
            lvl, txt = blocks[-1].data["items"][-1]
            blocks[-1].data["items"][-1] = (lvl, txt + " " + s)
            i += 1
            continue
        list_kind = None
        para.append(s)
        i += 1
    flush()
    return blocks


# ----------------------------------------------------------------------------
# WordprocessingML builders
# ----------------------------------------------------------------------------


class Doc:
    """Collects relationships, media, and numbering instances while building XML."""

    def __init__(self, report_dir: Path, next_rid: int):
        self.report_dir = report_dir
        self.next_rid = next_rid
        self.rels: list[str] = []  # Relationship elements to append
        self.media: dict[str, bytes] = {}  # word/media/<name> -> bytes
        self.nums: list[int] = []  # new numId values that restart a decimal list
        self.next_num_id = 6
        self.drawing_id = 0
        self.author_notes: list[str] = []
        self.hyperlinks: dict[str, str] = {}

    def new_rid(self) -> str:
        rid = f"rId{self.next_rid}"
        self.next_rid += 1
        return rid

    def hyperlink_rid(self, url: str) -> str:
        if url not in self.hyperlinks:
            rid = self.new_rid()
            self.rels.append(
                f'<Relationship Id="{rid}" Type="{REL_NS}/hyperlink" Target="{esc(url)}" TargetMode="External"/>'
            )
            self.hyperlinks[url] = rid
        return self.hyperlinks[url]

    def image_rid(self, rel_path: str) -> tuple[str, int, int]:
        src = (self.report_dir / rel_path).resolve()
        data = src.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"not a PNG: {src}")
        width, height = struct.unpack(">II", data[16:24])
        name = f"image{len(self.media) + 1}.png"
        self.media[name] = data
        rid = self.new_rid()
        self.rels.append(f'<Relationship Id="{rid}" Type="{REL_NS}/image" Target="media/{name}"/>')
        return rid, width, height

    def new_numbered_list(self) -> int:
        num_id = self.next_num_id
        self.next_num_id += 1
        self.nums.append(num_id)
        return num_id


def rfonts(font: str = FONT) -> str:
    return f'<w:rFonts w:ascii="{font}" w:cs="{font}" w:eastAsia="{font}" w:hAnsi="{font}"/>'


def rpr(
    *,
    font: str = FONT,
    bold: bool = False,
    italic: bool = False,
    small_caps: bool = False,
    color: str | None = None,
    size: int | None = None,
    highlight: str | None = None,
    underline: bool = False,
    shade: str | None = None,
    superscript: bool = False,
) -> str:
    """Run properties in schema order."""
    parts = [rfonts(font)]
    if bold:
        parts.append("<w:b/><w:bCs/>")
    if italic:
        parts.append("<w:i/><w:iCs/>")
    if small_caps:
        parts.append("<w:smallCaps/>")
    if color:
        parts.append(f'<w:color w:val="{color}"/>')
    if size:
        parts.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if highlight:
        parts.append(f'<w:highlight w:val="{highlight}"/>')
    if underline:
        parts.append('<w:u w:val="single"/>')
    if shade:
        parts.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    if superscript:
        parts.append('<w:vertAlign w:val="superscript"/>')
    return "<w:rPr>" + "".join(parts) + "</w:rPr>"


def run(text: str, **fmt) -> str:
    if text == "":
        return ""
    return f'<w:r>{rpr(**fmt)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


INLINE = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<bold>\*\*(?P<bold_in>.+?)\*\*)"
    r"|(?P<ital>(?<![\w*])\*(?P<ital_in>\S(?:[^*]*?\S)?)\*(?![\w*]))"
    r"|(?P<cite>\[(?P<cite_in>\d{1,2}(?:,\s*\d{1,2})*)\])"
    r"|(?P<author>\[AUTHOR:[^\]]*\])"
    r"|(?P<tag>\[(?:" + "|".join(STATUS_TAGS) + r")\])"
    r"|(?P<url>https?://[^\s<>\]\)\"]+)"
)


def inline_runs(doc: Doc, text: str, *, size: int | None = None, bold: bool = False, italic: bool = False, highlight: str | None = None) -> str:
    """Convert inline Markdown to a sequence of w:r (and w:hyperlink) elements."""
    out: list[str] = []
    pos = 0
    base = dict(size=size, bold=bold, italic=italic, highlight=highlight)
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(run(text[pos : m.start()], **base))
        pos = m.end()
        if m.group("code"):
            code_size = max(16, (size or 22) - 3)
            out.append(run(m.group("code")[1:-1], font=MONO, size=code_size, bold=bold, italic=italic, highlight=highlight))
        elif m.group("bold"):
            out.append(inline_runs(doc, m.group("bold_in"), size=size, bold=True, italic=italic, highlight=highlight))
        elif m.group("ital"):
            out.append(inline_runs(doc, m.group("ital_in"), size=size, bold=bold, italic=True, highlight=highlight))
        elif m.group("cite"):
            out.append(run(m.group("cite_in"), size=size, bold=bold, italic=italic, highlight=highlight, superscript=True))
        elif m.group("author"):
            doc.author_notes.append(m.group("author"))
            inner = m.group("author")[len("[AUTHOR:") : -1]
            out.append(run("[AUTHOR:", size=size, bold=bold, italic=italic, highlight="yellow"))
            out.append(inline_runs(doc, inner, size=size, bold=bold, italic=italic, highlight="yellow"))
            out.append(run("]", size=size, bold=bold, italic=italic, highlight="yellow"))
        elif m.group("tag"):
            tag_size = max(14, (size or 22) - 4)
            out.append(run(m.group("tag"), size=tag_size, bold=True, small_caps=True, italic=italic, highlight=highlight))
        elif m.group("url"):
            url = m.group("url")
            trail = ""
            while url and url[-1] in ".,;:":
                trail = url[-1] + trail
                url = url[:-1]
            rid = doc.hyperlink_rid(url)
            link_run = run(url, size=size, bold=bold, italic=italic, color="1155cc", underline=True, highlight=highlight)
            out.append(f'<w:hyperlink r:id="{rid}">{link_run}</w:hyperlink>')
            if trail:
                out.append(run(trail, **base))
    if pos < len(text):
        out.append(run(text[pos:], **base))
    return "".join(out)


def paragraph(
    content: str,
    *,
    style: str | None = None,
    keep_next: bool = False,
    num: tuple[int, int] | None = None,
    shade: str | None = None,
    spacing: str | None = None,
    ind: str | None = None,
    jc: str | None = None,
    mark_rpr: str | None = None,
) -> str:
    """A w:p with its properties in schema order."""
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        ppr.append("<w:keepNext/>")
    if num:
        ppr.append(f'<w:numPr><w:ilvl w:val="{num[1]}"/><w:numId w:val="{num[0]}"/></w:numPr>')
    if shade:
        ppr.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    if spacing:
        ppr.append(spacing)
    if ind:
        ppr.append(ind)
    if jc:
        ppr.append(f'<w:jc w:val="{jc}"/>')
    ppr.append(mark_rpr or rpr())
    return "<w:p><w:pPr>" + "".join(ppr) + "</w:pPr>" + content + "</w:p>"


H2_RPR = rpr(bold=True, size=28)
H3_RPR = rpr(bold=True, color="000000", size=26)


def heading2(text: str) -> str:
    return paragraph(
        f'<w:r>{H2_RPR}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>',
        style="Heading2",
        spacing='<w:spacing w:after="0" w:before="200" w:line="360" w:lineRule="auto"/>',
        mark_rpr=H2_RPR,
    )


def heading3(text: str) -> str:
    return paragraph(
        f'<w:r>{H3_RPR}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>',
        style="Heading3",
        spacing='<w:spacing w:before="200" w:lineRule="auto"/>',
        mark_rpr=H3_RPR,
    )


def body_paragraph(doc: Doc, text: str, *, keep_next: bool = False) -> str:
    return paragraph(inline_runs(doc, text), keep_next=keep_next, spacing='<w:spacing w:after="120"/>')


def list_paragraph(doc: Doc, text: str, num_id: int, level: int) -> str:
    left = 720 + 720 * level
    return paragraph(
        inline_runs(doc, text),
        num=(num_id, level),
        spacing='<w:spacing w:after="60"/>',
        ind=f'<w:ind w:left="{left}" w:hanging="360"/>',
    )


def code_block(lines: list[str]) -> str:
    out = []
    for k, line in enumerate(lines):
        after = "120" if k == len(lines) - 1 else "0"
        content = run(line, font=MONO, size=16) if line else ""
        out.append(
            paragraph(
                content,
                shade="F2F2F2",
                spacing=f'<w:spacing w:after="{after}" w:line="240" w:lineRule="auto"/>',
                ind='<w:ind w:left="240" w:right="240"/>',
                mark_rpr=rpr(font=MONO, size=16),
            )
        )
    return "".join(out)


def column_widths(rows: list[list[str]], ncols: int) -> list[int]:
    lens = [4] * ncols
    for r in rows:
        for k, c in enumerate(r[:ncols]):
            lens[k] = max(lens[k], min(len(c), 60))
    total = sum(lens)
    widths = [max(700, round(TEXT_WIDTH * l / total)) for l in lens]
    s = sum(widths)
    widths = [round(w * TEXT_WIDTH / s) for w in widths]
    widths[-1] += TEXT_WIDTH - sum(widths)
    return widths


def table(doc: Doc, rows: list[list[str]], ncols: int) -> str:
    widths = column_widths(rows, ncols)
    if ncols >= 9:
        size = 16
    elif ncols > 5:
        size = 18
    else:
        size = 20
    border = '<w:{side} w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
    borders = "".join(border.format(side=s) for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = [
        "<w:tbl><w:tblPr>",
        '<w:tblStyle w:val="Table1"/>',
        f'<w:tblW w:w="{TEXT_WIDTH}" w:type="dxa"/>',
        '<w:jc w:val="center"/>',
        f"<w:tblBorders>{borders}</w:tblBorders>",
        '<w:tblLayout w:type="fixed"/>',
        '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>',
        '<w:tblLook w:val="0420" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>',
        "</w:tblPr><w:tblGrid>",
        "".join(f'<w:gridCol w:w="{w}"/>' for w in widths),
        "</w:tblGrid>",
    ]
    for ri, row in enumerate(rows):
        header = ri == 0
        xml.append("<w:tr>")
        if header:
            xml.append("<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>")
        else:
            xml.append("<w:trPr><w:cantSplit/></w:trPr>")
        for ci in range(ncols):
            cell = row[ci] if ci < len(row) else ""
            tcpr = f'<w:tcW w:w="{widths[ci]}" w:type="dxa"/>'
            if header:
                tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="E7ECF2"/>'
            tcpr += '<w:vAlign w:val="top"/>'
            content = inline_runs(doc, cell, size=size, bold=header)
            para = paragraph(content, spacing='<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>', mark_rpr=rpr(size=size, bold=header))
            xml.append(f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{para}</w:tc>")
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    # An empty paragraph after each table keeps adjacent tables apart.
    xml.append(paragraph("", spacing='<w:spacing w:after="0"/>', mark_rpr=rpr(size=12)))
    return "".join(xml)


def image(doc: Doc, caption: str, rel_path: str) -> str:
    rid, px_w, px_h = doc.image_rid(rel_path)
    cx = TEXT_WIDTH_EMU
    cy = round(cx * px_h / px_w)
    doc.drawing_id += 1
    did = doc.drawing_id
    name = Path(rel_path).name
    drawing = (
        '<w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{did}" name="Figure {did}" descr="{esc(caption)}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{did}" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
    )
    out = paragraph(drawing, keep_next=True, spacing='<w:spacing w:before="120" w:after="60"/>', jc="center")
    if caption:
        cap = re.sub(r"^(Figure \d+\.)", r"**\1**", caption)
        out += paragraph(inline_runs(doc, cap, size=18, italic=True), spacing='<w:spacing w:after="160"/>', mark_rpr=rpr(size=18, italic=True))
    return out


# ----------------------------------------------------------------------------
# Template surgery
# ----------------------------------------------------------------------------


def matching_tbl_end(xml: str, start: int) -> int:
    """Index just past the </w:tbl> that closes the <w:tbl> at `start`."""
    depth = 0
    for m in re.finditer(r"<w:tbl>|</w:tbl>", xml[start:]):
        depth += 1 if m.group(0) == "<w:tbl>" else -1
        if depth == 0:
            return start + m.end()
    raise SystemExit("unbalanced w:tbl in template")


def enclosing_paragraph(xml: str, idx: int) -> tuple[int, int]:
    start = xml.rfind("<w:p ", 0, idx)
    end = xml.find("</w:p>", idx) + len("</w:p>")
    return start, end


def build_front_block(doc: Doc, body: str, title: str, author: str, abstract: str) -> str:
    """Return the template's front block with the paper's title, author, and abstract."""
    first_tbl = body.find("<w:tbl>")
    front = body[: matching_tbl_end(body, first_tbl)]

    # Title text; the footnote reference run that follows stays.
    assert front.count(">PROJECT TITLE<") == 1, "template title not found"
    front = front.replace(">PROJECT TITLE<", ">" + esc(title) + "<")

    # Author grid (Table3) -> one centered paragraph with the placeholder.
    t3 = front.find('<w:tblStyle w:val="Table3"/>')
    assert t3 > 0, "template author table not found"
    t3_start = front.rfind("<w:tbl>", 0, t3)
    t3_end = matching_tbl_end(front, t3_start)
    author_par = paragraph(
        inline_runs(doc, author),
        spacing='<w:spacing w:after="200" w:line="240" w:lineRule="auto"/>',
        jc="center",
    )
    front = front[:t3_start] + author_par + front[t3_end:]

    # Abstract guidance paragraph -> the paper's abstract.
    idx = front.find("Summarize your project")
    assert idx > 0, "template abstract paragraph not found"
    p_start, p_end = enclosing_paragraph(front, idx)
    abstract_par = paragraph(
        inline_runs(doc, abstract),
        spacing='<w:spacing w:after="200" w:line="240" w:lineRule="auto"/>',
        ind='<w:ind w:left="540" w:right="45" w:firstLine="0"/>',
        jc="both",
    )
    front = front[:p_start] + abstract_par + front[p_end:]

    # Google Docs export artifacts: decimal twips and tracked grid changes.
    front = re.sub(r'w:w="(\d+)\.0"', r'w:w="\1"', front)
    front = re.sub(r"<w:tblGridChange w:id=\"\d+\">.*?</w:tblGridChange>", "", front, flags=re.S)
    return front


def build_document(doc: Doc, template_xml: str, blocks: list[Block]) -> str:
    body_start = template_xml.find("<w:body>") + len("<w:body>")
    sect_start = template_xml.rfind("<w:sectPr")
    head = template_xml[:body_start]
    body = template_xml[body_start:sect_start]
    tail = template_xml[sect_start:]  # <w:sectPr>...</w:sectPr></w:body></w:document>
    if "w:gutter=" not in tail:  # required by the schema; the template omits it
        tail = tail.replace("<w:pgMar ", '<w:pgMar w:gutter="0" ', 1)

    title = next((b.data["text"] for b in blocks if b.kind == "title"), "")
    author = next((b.data["text"] for b in blocks if b.kind == "author"), "[AUTHOR: name, affiliation, email]")

    # Split blocks: preamble (before the first ## after Abstract, minus title, author,
    # and the abstract paragraph) and main body.
    abstract = ""
    preamble: list[Block] = []
    main: list[Block] = []
    in_abstract = False
    seen_abstract_par = False
    reached_main = False
    for b in blocks:
        if b.kind in ("title", "author"):
            continue
        if b.kind == "h2" and b.data["text"].strip().lower() == "abstract":
            in_abstract = True
            continue
        if b.kind == "h2" and in_abstract:
            reached_main = True
        if reached_main:
            main.append(b)
        elif in_abstract and b.kind == "p" and not seen_abstract_par:
            abstract = b.data["text"]
            seen_abstract_par = True
        else:
            preamble.append(b)

    front = build_front_block(doc, body, title, author, abstract)
    content = [front]
    content.append(render_blocks(doc, preamble))
    content.append(render_blocks(doc, main))
    return head + "".join(content) + tail


def render_blocks(doc: Doc, blocks: list[Block]) -> str:
    out: list[str] = []
    for k, b in enumerate(blocks):
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        if b.kind == "h2":
            text = re.sub(r"\s*\(required\)\s*$", "", b.data["text"])
            out.append(heading2(text))
        elif b.kind == "h3":
            out.append(heading3(b.data["text"]))
        elif b.kind == "p":
            keep = bool(nxt and nxt.kind in ("table", "code") ) or bool(nxt and nxt.kind == "image" and b.data["text"].startswith("**Figure"))
            out.append(body_paragraph(doc, b.data["text"], keep_next=keep))
        elif b.kind == "bullets":
            for level, item in b.data["items"]:
                out.append(list_paragraph(doc, item, 3, level))
        elif b.kind == "numbered":
            num_id = doc.new_numbered_list()
            for level, item in b.data["items"]:
                out.append(list_paragraph(doc, item, num_id, level))
        elif b.kind == "table":
            out.append(table(doc, b.data["rows"], b.data["ncols"]))
        elif b.kind == "code":
            out.append(code_block(b.data["lines"]))
        elif b.kind == "image":
            out.append(image(doc, b.data["caption"], b.data["path"]))
        else:
            raise SystemExit(f"unhandled block kind {b.kind}")
    return "".join(out)


def patch_rels(rels_xml: str, doc: Doc) -> str:
    # Drop the template's rubric hyperlink; its paragraph (the info box) is gone.
    rels_xml = re.sub(r'<Relationship Id="rId\d+" Type="[^"]+/hyperlink" Target="https://apartresearch\.notion\.site[^"]*" TargetMode="External"/>', "", rels_xml)
    return rels_xml.replace("</Relationships>", "".join(doc.rels) + "</Relationships>")


def patch_content_types(ct_xml: str) -> str:
    if 'Extension="png"' not in ct_xml:
        ct_xml = ct_xml.replace("<Default ", '<Default ContentType="image/png" Extension="png"/><Default ', 1)
    return ct_xml


def patch_numbering(num_xml: str, doc: Doc) -> str:
    # abstractNum 5 is the template's decimal list ("1."). Each new w:num restarts at 1.
    assert '<w:abstractNum w:abstractNumId="5">' in num_xml, "template decimal list not found"
    assert '<w:abstractNum w:abstractNumId="3">' in num_xml, "template bullet list not found"
    new = "".join(
        f'<w:num w:numId="{n}"><w:abstractNumId w:val="5"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
        for n in doc.nums
    )
    return num_xml.replace("</w:numbering>", new + "</w:numbering>")


# ----------------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------------


def check_output(out_path: Path, blocks: list[Block], expected_images: int) -> bool:
    ok = True
    ns = {"w": W_NS}
    with zipfile.ZipFile(out_path) as z:
        names = z.namelist()
        doc_xml = z.read("word/document.xml").decode("utf8")
    root = ET.fromstring(doc_xml)
    body = root.find("w:body", ns)
    styles: dict[str, int] = {}
    for p in root.iter(f"{{{W_NS}}}p"):
        st = p.find("w:pPr/w:pStyle", ns)
        key = st.get(f"{{{W_NS}}}val") if st is not None else "Normal"
        styles[key] = styles.get(key, 0) + 1
    print("paragraphs by style:", ", ".join(f"{k}={v}" for k, v in sorted(styles.items())))
    drawings = len(list(root.iter(f"{{{W_NS}}}drawing")))
    media = [n for n in names if n.startswith("word/media/")]
    print(f"drawings={drawings} media={len(media)} (expected {expected_images})")
    if drawings != expected_images or len(media) != expected_images:
        ok = False
    md_tables = [b.data["ncols"] for b in blocks if b.kind == "table"]
    body_tables = body.findall("w:tbl", ns)
    # The first body table is the template's front block; the rest come from Markdown.
    got = [len(t.findall("w:tblGrid/w:gridCol", ns)) for t in body_tables[1:]]
    print(f"tables from markdown={len(md_tables)} in docx={len(got)}; columns match={got == md_tables}")
    if got != md_tables:
        print("  markdown:", md_tables)
        print("  docx:    ", got)
        ok = False
    for t in body_tables[1:]:
        ncol = len(t.findall("w:tblGrid/w:gridCol", ns))
        for tr in t.findall("w:tr", ns):
            if len(tr.findall("w:tc", ns)) != ncol:
                print("  row/grid mismatch in a table")
                ok = False
    text = "".join(root.itertext())
    for g in GUIDANCE_STRINGS:
        if g in text:
            print(f"guidance text survives: {g!r}")
            ok = False
    print("guidance text check:", "clean" if all(g not in text for g in GUIDANCE_STRINGS) else "FAILED")
    return ok


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--template", type=Path, default=TEMPLATE)
    ap.add_argument("--report", type=Path, default=REPORT)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args(argv)

    md = args.report.read_text(encoding="utf8")
    blocks = parse_markdown(md)

    with zipfile.ZipFile(args.template) as z:
        parts = {info.filename: z.read(info.filename) for info in z.infolist()}
        order = [info.filename for info in z.infolist()]

    rels_xml = parts["word/_rels/document.xml.rels"].decode("utf8")
    max_rid = max(int(m) for m in re.findall(r'Id="rId(\d+)"', rels_xml))
    doc = Doc(args.report.parent, max_rid + 1)

    document_xml = build_document(doc, parts["word/document.xml"].decode("utf8"), blocks)
    parts["word/document.xml"] = document_xml.encode("utf8")
    parts["word/_rels/document.xml.rels"] = patch_rels(rels_xml, doc).encode("utf8")
    parts["[Content_Types].xml"] = patch_content_types(parts["[Content_Types].xml"].decode("utf8")).encode("utf8")
    parts["word/numbering.xml"] = patch_numbering(parts["word/numbering.xml"].decode("utf8"), doc).encode("utf8")
    for name, data in doc.media.items():
        parts["word/media/" + name] = data
        order.append("word/media/" + name)

    # Well-formedness check before writing.
    ET.fromstring(parts["word/document.xml"])
    ET.fromstring(parts["word/numbering.xml"])
    ET.fromstring(parts["word/_rels/document.xml.rels"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        names = ["[Content_Types].xml"] + [n for n in order if n != "[Content_Types].xml"]
        for name in names:
            z.writestr(name, parts[name])
    print(f"wrote {args.out} ({args.out.stat().st_size} bytes)")

    expected_images = sum(1 for b in blocks if b.kind == "image")
    ok = check_output(args.out, blocks, expected_images)
    if doc.author_notes:
        print(f"[AUTHOR] notes kept as highlighted text: {len(doc.author_notes)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
