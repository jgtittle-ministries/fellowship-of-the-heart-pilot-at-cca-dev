# -*- coding: utf-8 -*-
"""Week 2 expansion — the Week-1 pattern applied:
road slide loses the standing card; 8 stop slides (slide80-87, pos 14-21);
Four Soils diagram on the teaching slide; Week 2 Anchor & Practice deleted."""
import re, shutil, os

B = 'build/ppt'
EMU = 914400
FOREST, MOSS, INK, CREAM, DIM = '2C5F2D', '97BC62', '222B22', 'F1F6EC', '5A665A'

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def run(text, sz=1800, color=INK, b=0, i=0, u=None, font='Calibri', link=None):
    rpr = f'<a:rPr sz="{sz}" b="{b}" i="{i}"' + (f' u="{u}"' if u else '') + '>'
    rpr += f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/>'
    if link:
        rpr += f'<a:hlinkClick xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{link}"/>'
    rpr += '</a:rPr>'
    return f'<a:r>{rpr}<a:t>{esc(text)}</a:t></a:r>'

def para(runs, spc=900, marL=0, indent=0):
    attrs = ''
    if marL: attrs += f' marL="{marL}"'
    if indent: attrs += f' indent="{indent}"'
    return (f'<a:p><a:pPr{attrs}>'
            f'<a:spcAft><a:spcPts val="{spc}"/></a:spcAft></a:pPr>{"".join(runs)}</a:p>')

def bullet(text_or_runs, sz=1800, b=0, i=0, spc=900):
    rest = [run(text_or_runs, sz=sz, b=b, i=i)] if isinstance(text_or_runs, str) else text_or_runs
    return para([run('•  ', sz=sz, color=MOSS, b=1)] + rest, spc=spc, marL=274320, indent=-274320)

def sub(runs_or_text, sz=1600, spc=700):
    lead = run('–  ', sz=sz, color=MOSS, b=1)
    rest = [run(runs_or_text, sz=sz)] if isinstance(runs_or_text, str) else runs_or_text
    return para([lead] + rest, spc=spc, marL=685800, indent=-274320)

def numbered(n, text, sz=1700, spc=750, bold_num=1):
    return para([run(f'{n}   ', sz=sz, color=MOSS, b=bold_num), run(text, sz=sz)],
                spc=spc, marL=342900, indent=-342900)

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

def write_slide(fname, shapes, rels_extra=''):
    xml = HEAD + BG + ''.join(shapes) + TAIL
    open(f'{B}/slides/{fname}', 'w', encoding='utf-8').write(xml)
    rels = ('<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            'Target="../slideLayouts/slideLayout7.xml"/>' + rels_extra + '</Relationships>')
    open(f'{B}/slides/_rels/{fname}.rels', 'w', encoding='utf-8').write(rels)

# ---------- N1 (pos 14, slide80) — Opening Container, eight steps ----------
n1 = [
    numbered(1, 'Welcome — five minutes to open the container'),
    numbered(2, 'Phones silenced and put away'),
    numbered(3, 'Stand in a circle'),
    numbered(4, 'One-word check-in — how you actually are, right now'),
    numbered(5, 'Put out / bring in — set something down; bring a blessing in'),
    numbered(6, 'Spoken commitment: “I am here. I am paying attention. I am willing to be moved.”'),
    numbered(7, 'Opening prayer — “Holy Spirit, you are welcome here. Speak. We are listening.”'),
    numbered(8, 'Sit. Begin.'),
]
write_slide('slide80.xml', [title_sp('Opening Container — the Full Eight Steps'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n1)])

# ---------- N2 (pos 15, slide81) — Practice check-in ----------
n2 = [
    bullet('One quick round, one sentence each — a parent starts'),
    sub([run('“One thing I noticed this week when I asked the morning question …”', sz=1600, i=1)]),
    sub([run('Or one thing about the practice itself — “I forgot it three days running” is a real answer', sz=1600)]),
    bullet('No grades, no lectures — honesty over performance'),
    bullet('Missed it? “Thanks for the honesty. Pick it back up tomorrow.”'),
]
write_slide('slide81.xml', [title_sp('Check-In on Week 1 Practice'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n2)])

# ---------- N3 (pos 16, slide82) — Teaching: Mark 4 and the Four Soils ----------
shutil.copy('four-soils.png', f'{B}/media/image22.png')
W, H = 11.5, 11.5 * 990 / 2760
pic = ('<p:pic><p:nvPicPr><p:cNvPr id="5" name="Picture 4" descr="four soils diagram"/>'
       '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
       '<p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
       f'<p:spPr><a:xfrm><a:off x="{int(0.9*EMU)}" y="{int(1.9*EMU)}"/>'
       f'<a:ext cx="{int(W*EMU)}" cy="{int(H*EMU)}"/></a:xfrm>'
       '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
n3 = [para([run('Read Mark 4:1–20 in full, slowly — all twenty verses, no commentary. ', sz=1500),
            run('Then walk the four soils.', sz=1500, b=1)])]
imgrel = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
          'Target="../media/image22.png"/>')
write_slide('slide82.xml', [title_sp('Teaching — Mark 4 and the Four Soils'), pic,
                            textbox(4, 0.9, 6.15, 11.5, 0.7, n3)], imgrel)

# ---------- N4 (pos 17, slide83) — The Heart Soil Diagnostic ----------
n4 = [
    bullet([run('Not ', sz=1600), run('“which soil am I?”', sz=1600, i=1),
            run(' — where does each soil show up in my life right now? Specifically.', sz=1600)], spc=800),
    numbered(1, 'Path — where is the ground hard right now? One specific place, this week', sz=1600, spc=650),
    numbered(2, 'Rocky — where has a season with God not lasted? What sun revealed the missing roots?', sz=1600, spc=650),
    numbered(3, 'Thorny — what is choking me right now: cares, riches, other desires? Which is loudest?', sz=1600, spc=650),
    numbered(4, 'Good — where has something God planted actually grown? Name one real piece of fruit', sz=1600, spc=650),
    bullet('Journal two minutes, then share — a parent answers first, every round', sz=1600, spc=650),
    bullet('“I’d rather not share that one” is a complete answer — a gift, not ammunition', sz=1600, spc=650),
]
write_slide('slide83.xml', [title_sp('Family Clusters — the Heart Soil Diagnostic'),
                            textbox(4, 0.9, 1.65, 11.5, 5.4, n4)])

# ---------- N5 (pos 18, slide84) — Re-merge + Mark 4:20 ----------
n5 = [
    bullet('What surfaced stays in your cluster — here, just one word from each of us', sz=1600, spc=800),
    bullet('Then the verse Jesus ends with, read slowly — listen for the word that lands', sz=1600, spc=800),
    bullet('Noticing rocks and thorns is not the opposite of good soil — it is what good soil does', sz=1600, spc=800),
]
verse = [
    para([run('MARK 4:20', sz=1200, color=MOSS, b=1)], spc=1000),
    para([run('“But those that were sown on the good soil are the ones who hear the word and accept it and bear fruit, thirtyfold and sixtyfold and a hundredfold.”', sz=1700, i=1, font='Cambria')], spc=600),
]
write_slide('slide84.xml', [title_sp('Re-Merge — One Word, Then the Verse'),
                            textbox(4, 0.9, 1.75, 6.2, 4.4, n5),
                            textbox(6, 7.4, 1.9, 5.1, 3.6, verse, fill=CREAM, anchor='ctr')])

# ---------- N6 (pos 19, slide85) — Between-week practice ----------
n6 = [
    bullet('The Soil Journal — three times this week, five minutes each. Not every day; three times.'),
    sub([run('Today, where did the path show up? The rocky? The thorny? The good soil?', sz=1600, i=1)]),
    sub('One sentence per soil. Specific, not general.'),
    bullet('No fixing. We notice; the Spirit fixes.'),
    bullet([run('Keep the morning question going too: ', sz=1800),
            run('“Father, what are you up to today?”', sz=1800, i=1),
            run(' The practices stack.', sz=1800)]),
]
write_slide('slide85.xml', [title_sp('Between-Week Practice'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n6)])

# ---------- N7 (pos 20, slide86) — Leader Feedback Round ----------
n7 = [
    bullet('The evening’s leader goes first — same two questions, every week'),
    sub([run('“What I think went well tonight: ______”', sz=1600, i=1)]),
    sub([run('“What I’d do differently next time: ______”', sz=1600, i=1)]),
    bullet('Then the room — the same two questions about tonight'),
    bullet('The leader receives without defending — “thank you” is the whole response'),
]
write_slide('slide86.xml', [title_sp('The Leader Feedback Round'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n7)])

# ---------- N8 (pos 21, slide87) — Closing + Blessing ----------
n8 = [
    bullet('We close the way we opened — the container, six steps', sz=1600, spc=800),
    bullet('One-word landing · the one thing you are taking · the one practice', sz=1600, spc=800),
    sub('Commit to the week’s practice aloud — or modify it to something you will actually do', sz=1500, spc=800),
    bullet('Blessings — specific, witnessed, short', sz=1600, spc=800),
    bullet('Then the Aaronic blessing — spoken over each other, face to face', sz=1600, spc=800),
]
blessing = [
    para([run('THE AARONIC BLESSING — NUMBERS 6:24–26', sz=1200, color=MOSS, b=1)], spc=1000),
    para([run('“The Lord bless you and keep you;', sz=1800, i=1, font='Cambria')], spc=700),
    para([run('the Lord make his face to shine upon you, and be gracious to you;', sz=1800, i=1, font='Cambria')], spc=700),
    para([run('the Lord lift up his countenance upon you, and give you peace.”', sz=1800, i=1, font='Cambria')], spc=700),
]
write_slide('slide87.xml', [title_sp('Closing the Container + Aaronic Blessing'),
                            textbox(4, 0.9, 1.75, 6.2, 4.6, n8),
                            textbox(6, 7.4, 1.9, 5.1, 4.0, blessing, fill=CREAM, anchor='ctr')])

# ---------- Week 2 road (slide7): drop the standing card ----------
p = f'{B}/slides/slide7.xml'
x = open(p, encoding='utf-8').read()
card = None
for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S):
    if 'You don’t have to remember' in m.group(0):
        card = m.group(0)
assert card, 'standing card not found on slide7'
x = x.replace(card, '')
open(p, 'w', encoding='utf-8').write(x)
print('slide7: standing card removed')

# ---------- Delete Week 2 Anchor & Practice (slide8.xml, pos 22) ----------
pres = f'{B}/presentation.xml'
prels = f'{B}/_rels/presentation.xml.rels'
rx = open(prels, encoding='utf-8').read()
rid = re.search(r'Id="(rId\d+)"[^>]*Target="slides/slide8\.xml"', rx).group(1)
px = open(pres, encoding='utf-8').read()
px2 = re.sub(rf'<p:sldId id="\d+" r:id="{rid}"/>', '', px, count=1)
assert px2 != px
open(pres, 'w', encoding='utf-8').write(px2)
print('slide8 removed from sldIdLst')

# ---------- Slide numbers on the new slides ----------
def slidenum_sp(color):
    return ('<p:sp><p:nvSpPr><p:cNvPr id="90" name="SlideNum"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(12.45*EMU)}" y="{int(7.05*EMU)}"/>'
            f'<a:ext cx="{int(0.7*EMU)}" cy="{int(0.32*EMU)}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="45720" bIns="0" anchor="ctr"/><a:lstStyle/>'
            '<a:p><a:pPr algn="r"/><a:fld id="{B1F00A3C-9A6E-4E85-9D4C-1A56F3D0A001}" type="slidenum">'
            f'<a:rPr sz="1000" b="1"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            '<a:latin typeface="Calibri"/></a:rPr><a:t>1</a:t></a:fld></a:p></p:txBody></p:sp>')
count = 0
for f in os.listdir(f'{B}/slides'):
    if not re.match(r'slide\d+\.xml$', f):
        continue
    fp = f'{B}/slides/{f}'
    x = open(fp, encoding='utf-8').read()
    if 'type="slidenum"' in x:
        continue
    x = x.replace('</p:spTree>', slidenum_sp('7A8A6E') + '</p:spTree>')
    open(fp, 'w', encoding='utf-8').write(x)
    count += 1
print('slide numbers added to', count, 'new slides')
print('WEEK 2 BUILD DONE')
