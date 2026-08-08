# -*- coding: utf-8 -*-
"""Weeks 3-22: apply the established pattern deck-wide.
Per week: road keeps its list but loses the standing card; after the road,
one slide per stop — standard slides for opening/feedback/closing, generated
slides (from weeks/weekNN.json) for everything else; anchor slide deleted."""
import re, os, json, glob

B = 'build/ppt'
EMU = 914400
FOREST, MOSS, INK, CREAM, DIM = '2C5F2D', '97BC62', '222B22', 'F1F6EC', '5A665A'

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def run(text, sz=1800, color=INK, b=0, i=0, font='Calibri'):
    return (f'<a:r><a:rPr sz="{sz}" b="{b}" i="{i}">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/></a:rPr>'
            f'<a:t>{esc(text)}</a:t></a:r>')

def para(runs, spc=800, marL=0, indent=0):
    attrs = (f' marL="{marL}"' if marL else '') + (f' indent="{indent}"' if indent else '')
    return f'<a:p><a:pPr{attrs}><a:spcAft><a:spcPts val="{spc}"/></a:spcAft></a:pPr>{"".join(runs)}</a:p>'

def textbox(cid, x, y, w, h, paras, fill=None, anchor=None):
    sp = f'<p:sp><p:nvSpPr><p:cNvPr id="{cid}" name="TextBox {cid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
    sp += f'<p:spPr><a:xfrm><a:off x="{int(x*EMU)}" y="{int(y*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm>'
    sp += '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    sp += (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>')
    sp += '</p:spPr><p:txBody><a:bodyPr wrap="square" lIns="91440" tIns="91440" rIns="91440" bIns="91440"'
    if anchor: sp += f' anchor="{anchor}"'
    sp += '/><a:lstStyle/>' + ''.join(paras) + '</p:txBody></p:sp>'
    return sp

BG = ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="Rectangle 1"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>'
      '<a:xfrm><a:off x="0" y="0"/><a:ext cx="12191695" cy="6858000"/></a:xfrm>'
      '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
      '<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')

def title_sp(text):
    return ('<p:sp><p:nvSpPr><p:cNvPr id="3" name="TextBox 2"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="822960" y="502920"/><a:ext cx="10515600" cy="822960"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="square"><a:spAutoFit/></a:bodyPr><a:lstStyle/>'
            '<a:p><a:pPr algn="l"><a:spcAft><a:spcPts val="600"/></a:spcAft></a:pPr>'
            f'<a:r><a:rPr sz="2800" b="1" i="0"><a:solidFill><a:srgbClr val="{FOREST}"/></a:solidFill>'
            f'<a:latin typeface="Cambria"/></a:rPr><a:t>{esc(text)}</a:t></a:r></a:p></p:txBody></p:sp>')

HEAD = ('<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>')
TAIL = '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'

def slidenum_sp():
    return ('<p:sp><p:nvSpPr><p:cNvPr id="90" name="SlideNum"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(12.45*EMU)}" y="{int(7.05*EMU)}"/>'
            f'<a:ext cx="{int(0.7*EMU)}" cy="{int(0.32*EMU)}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="45720" bIns="0" anchor="ctr"/><a:lstStyle/>'
            '<a:p><a:pPr algn="r"/><a:fld id="{B1F00A3C-9A6E-4E85-9D4C-1A56F3D0A001}" type="slidenum">'
            '<a:rPr sz="1000" b="1"><a:solidFill><a:srgbClr val="7A8A6E"/></a:solidFill>'
            '<a:latin typeface="Calibri"/></a:rPr><a:t>1</a:t></a:fld></a:p></p:txBody></p:sp>')

# ---------- bulk registrar ----------
ct_path = 'build/[Content_Types].xml'
pres_path = f'{B}/presentation.xml'
prels_path = f'{B}/_rels/presentation.xml.rels'
ct = open(ct_path, encoding='utf-8').read()
pres = open(pres_path, encoding='utf-8').read()
prels = open(prels_path, encoding='utf-8').read()
next_slide = max(int(m) for m in re.findall(r'slides/slide(\d+)\.xml', prels)) + 1
next_rid = max(int(m) for m in re.findall(r'Id="rId(\d+)"', prels)) + 1
next_sid = max(int(m) for m in re.findall(r'<p:sldId id="(\d+)"', pres)) + 1

SLIDE_CT = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
REL_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'

def register(fname, after_rid):
    """Register slide part + rel + sldIdLst entry right after after_rid. Returns its rId."""
    global ct, pres, prels, next_rid, next_sid
    rid = f'rId{next_rid}'; next_rid += 1
    sid = next_sid; next_sid += 1
    ct = ct.replace('</Types>', f'<Override PartName="/ppt/slides/{fname}" ContentType="{SLIDE_CT}"/></Types>')
    prels = prels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="{REL_T}" Target="slides/{fname}"/></Relationships>')
    anchor = re.search(rf'<p:sldId id="\d+" r:id="{after_rid}"/>', pres).group(0)
    pres = pres.replace(anchor, anchor + f'<p:sldId id="{sid}" r:id="{rid}"/>', 1)
    return rid

def write_slide(fname, shapes):
    xml = HEAD + BG + ''.join(shapes) + slidenum_sp() + TAIL
    open(f'{B}/slides/{fname}', 'w', encoding='utf-8').write(xml)
    rels = ('<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            'Target="../slideLayouts/slideLayout7.xml"/></Relationships>')
    open(f'{B}/slides/_rels/{fname}.rels', 'w', encoding='utf-8').write(rels)

# ---------- item renderers ----------
def render_items(items, big, mid, spc):
    paras = []
    for it in items:
        k = it.get('kind', 'bullet')
        i = 1 if it.get('italic') else 0
        t = it['text']
        if k == 'bullet':
            paras.append(para([run('•  ', sz=big, color=MOSS, b=1), run(t, sz=big, i=i)],
                              spc=spc, marL=274320, indent=-274320))
        elif k == 'sub':
            paras.append(para([run('–  ', sz=mid, color=MOSS, b=1), run(t, sz=mid, i=i)],
                              spc=max(500, spc-200), marL=685800, indent=-274320))
        elif k == 'numbered':
            n = it.get('num', '')
            paras.append(para([run(f'{n}   ', sz=big, color=MOSS, b=1), run(t, sz=big, i=i)],
                              spc=spc, marL=342900, indent=-342900))
    return paras

def gen_slide(fname, title, items, panel=None):
    n = len(items)
    if panel:
        big, mid = (1500, 1400) if n >= 6 else (1600, 1500)
        spc = 650 if n >= 6 else 800
        shapes = [title_sp(title), textbox(4, 0.9, 1.75, 6.2, 5.0, render_items(items, big, mid, spc))]
        lines = [para([run(panel['label'], sz=1200, color=MOSS, b=1)], spc=900)]
        for ln in panel['lines']:
            lines.append(para([run(ln, sz=1600, i=1, font='Cambria')], spc=600))
        est = sum(max(1, len(ln)//48 + 1) for ln in panel['lines'])
        h = min(4.6, max(2.4, 1.1 + 0.42*est))
        shapes.append(textbox(6, 7.4, 1.9, 5.1, h, lines, fill=CREAM, anchor='ctr'))
    else:
        big, mid = (1500, 1400) if n >= 8 else ((1600, 1500) if n >= 6 else (1800, 1600))
        spc = 650 if n >= 8 else (750 if n >= 6 else 900)
        shapes = [title_sp(title), textbox(4, 0.9, 1.7, 11.5, 5.35, render_items(items, big, mid, spc))]
    write_slide(fname, shapes)

def std_open(fname):
    steps = ['Welcome — five minutes to open the container', 'Phones silenced and put away',
             'Stand in a circle', 'One-word check-in — how you actually are, right now',
             'Put out / bring in — set something down; bring a blessing in',
             'Spoken commitment: “I am here. I am paying attention. I am willing to be moved.”',
             'Opening prayer — “Holy Spirit, you are welcome here. Speak. We are listening.”',
             'Sit. Begin.']
    items = [{'kind': 'numbered', 'num': i, 'text': s} for i, s in enumerate(steps, 1)]
    gen_slide(fname, 'Opening Container — the Eight Steps', items)

def std_feedback(fname):
    items = [{'kind': 'bullet', 'text': 'The evening’s leader goes first — same two questions, every week'},
             {'kind': 'sub', 'text': '“What I think went well tonight: ______”', 'italic': True},
             {'kind': 'sub', 'text': '“What I’d do differently next time: ______”', 'italic': True},
             {'kind': 'bullet', 'text': 'Then the room — the same two questions about tonight'},
             {'kind': 'bullet', 'text': 'The leader receives without defending — “thank you” is the whole response'}]
    gen_slide(fname, 'The Leader Feedback Round', items)

def std_close(fname):
    items = [{'kind': 'bullet', 'text': 'We close the way we opened — the container, six steps'},
             {'kind': 'bullet', 'text': 'One-word landing · the one thing you are taking · the one practice'},
             {'kind': 'sub', 'text': 'Commit to the week’s practice aloud — or modify it to something you will actually do'},
             {'kind': 'bullet', 'text': 'Blessings — specific, witnessed, short'},
             {'kind': 'bullet', 'text': 'Then the Aaronic blessing — spoken over each other, face to face'}]
    panel = {'label': 'THE AARONIC BLESSING — NUMBERS 6:24–26',
             'lines': ['“The Lord bless you and keep you;',
                       'the Lord make his face to shine upon you, and be gracious to you;',
                       'the Lord lift up his countenance upon you, and give you peace.”']}
    gen_slide(fname, 'Closing the Container + Aaronic Blessing', items, panel)

# ---------- classification ----------
def classify(stop):
    s = stop.lower()
    if 'leader feedback' in s: return 'FB'
    if 'closing container' in s or ('closing' in s and 'blessing' in s): return 'CLOSE'
    if s.startswith(('welcome and centering', 'welcome and opening container', 'opening container')):
        return 'OPEN'
    return 'GEN'

# ---------- main ----------
roads = json.load(open('weeks/roads.json', encoding='utf-8'))
anchors = {3:'slide11',4:'slide14',5:'slide17',6:'slide20',7:'slide25',8:'slide28',9:'slide31',10:'slide34',
           11:'slide37',12:'slide41',13:'slide44',14:'slide47',15:'slide50',16:'slide53',17:'slide56',
           18:'slide60',19:'slide63',20:'slide66',21:'slide69',22:'slide72'}
warns = []
made = 0
for wk in range(3, 23):
    info = roads[str(wk)]
    road_file = info['road_file']
    wdata = json.load(open(f'weeks/week{wk:02d}.json', encoding='utf-8'))
    by_stop = {s['stop']: s for s in wdata['slides']}
    # remove standing card from road
    rp = f'{B}/slides/{road_file}'
    rx = open(rp, encoding='utf-8').read()
    for m in re.finditer(r'<p:sp>.*?</p:sp>', rx, re.S):
        if 'You don’t have to remember' in m.group(0):
            rx = rx.replace(m.group(0), '')
            break
    open(rp, 'w', encoding='utf-8').write(rx)
    # road slide rId
    road_rid = re.search(rf'Id="(rId\d+)"[^>]*Target="slides/{road_file}"', prels).group(1)
    prev = road_rid
    for idx, stop in enumerate(info['stops'], 1):
        cat = classify(stop)
        fname = f'slide{next_slide}.xml'
        sl = by_stop.get(idx)
        if sl and cat in ('GEN', 'OPEN'):
            # honor an agent-provided slide even on an "opening" stop (e.g. Week 12's slow open)
            gen_slide(fname, sl['title'], sl['items'], sl.get('panel'))
        elif cat == 'OPEN':
            std_open(fname)
        elif cat == 'FB':
            std_feedback(fname)
        elif cat == 'CLOSE':
            std_close(fname)
        else:
            warns.append(f'wk{wk} stop {idx} "{stop[:40]}" missing from JSON — skipped')
            continue
        prev = register(fname, prev)
        made += 1
        next_slide += 1
    # check for generated slides whose stop wasn't consumed
    for s in wdata['slides']:
        if classify(info['stops'][s['stop']-1]) != 'GEN':
            warns.append(f'wk{wk}: JSON slide for stop {s["stop"]} maps to a standard stop — ignored')
    # delete anchor
    a = anchors[wk]
    arid = re.search(rf'Id="(rId\d+)"[^>]*Target="slides/{a}\.xml"', prels).group(1)
    pres_new = re.sub(rf'<p:sldId id="\d+" r:id="{arid}"/>', '', pres, count=1)
    assert pres_new != pres, f'anchor {a} not found in sldIdLst'
    pres = pres_new

open(ct_path, 'w', encoding='utf-8').write(ct)
open(pres_path, 'w', encoding='utf-8').write(pres)
open(prels_path, 'w', encoding='utf-8').write(prels)
print(f'slides made: {made}')
for w in warns: print('WARN:', w)
print('BUILD WEEKS 3-22 DONE')
