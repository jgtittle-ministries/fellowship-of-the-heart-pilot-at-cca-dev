# Build an evening run sheet .docx from its markdown, using the Evening 6 run sheet as the formatting template.
# usage: python tools/build-evening-run-sheet.py <run-sheet.md> <out.docx>
import copy, re, sys
import docx

sys.stdout.reconfigure(encoding="utf-8")
SRC, OUT = sys.argv[1], sys.argv[2]
TPL = (r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
       r"\FotH Pilot Session 7-8 Combined Evening Run Sheet DRAFT v1.docx")
d = docx.Document(TPL)
P = d.paragraphs
T_TITLE, T_PLAIN, T_HEAD, T_LEAD, T_CLOSE = (P[0]._p, P[1]._p, P[4]._p, P[6]._p, P[-1]._p)
T_TABLE = d.tables[0]._tbl
tpl = {k: copy.deepcopy(v) for k, v in dict(title=T_TITLE, plain=T_PLAIN, head=T_HEAD, lead=T_LEAD,
                                              close=T_CLOSE, table=T_TABLE).items()}
body = d.element.body
for el in list(body):
    if not el.tag.endswith("sectPr"):
        body.remove(el)
sect = body[-1]


def strip_md(s):
    return s.replace("**", "").replace("*", "")


def add(kind, *texts):
    el = copy.deepcopy(tpl[kind])
    sect.addprevious(el)
    p = docx.text.paragraph.Paragraph(el, d._body)
    runs = p.runs
    if kind == "lead":
        runs[0].text, runs[1].text = texts[0], texts[1]
        for r in runs[2:]:
            r.text = ""
    else:
        runs[0].text = texts[0]
        for r in runs[1:]:
            r.text = ""


def add_table(rows):
    el = copy.deepcopy(tpl["table"])
    sect.addprevious(el)
    t = docx.table.Table(el, d._body)
    head, proto = t.rows[0]._tr, copy.deepcopy(t.rows[1]._tr)
    for r in list(t.rows)[1:]:
        el.remove(r._tr)
    for cells in rows:
        tr = copy.deepcopy(proto)
        el.append(tr)
        row = docx.table._Row(tr, t)
        for c, txt in zip(row.cells, cells):
            ps = c.paragraphs
            rs = ps[0].runs
            rs[0].text = txt
            for r in rs[1:]:
                r.text = ""
            for extra in ps[1:]:
                extra._p.getparent().remove(extra._p)


md = open(SRC, encoding="utf-8").read().strip().split("\n\n")
first_plain = True
for block in md:
    b = block.strip()
    if b.startswith("# "):
        title = b[2:].strip()
        m = re.match(r"(Evening \d+) — (.+)", title)
        add("title", "%s — %s" % (m.group(1), m.group(2).title()) if m else title)
    elif b.startswith("## "):
        add("head", b[3:].strip())
    elif b.startswith("|"):
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in b.splitlines()]
        add_table([r for r in rows[2:]])
    elif b.startswith("*Further up"):
        add("close", strip_md(b))
    else:
        text = " ".join(b.split())
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", text)
        if m and not text.startswith("**Aim.") and not text.startswith("**Anchor."):
            add("lead", m.group(1).strip() + " ", strip_md(m.group(2)))
        else:
            add("plain", strip_md(text))
d.save(OUT)
print("saved", OUT)
