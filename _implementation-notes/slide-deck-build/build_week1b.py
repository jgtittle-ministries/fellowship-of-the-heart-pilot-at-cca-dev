# -*- coding: utf-8 -*-
"""Round 2 of John's Week-1 dictation:
- slide 6: Four Connects diagram (site SVG rasterized) + one-line Sower refs
- slide 7: container in the PLAN order (Safe, Present, Clear, Intentional) w/ John's subs
- all new content slides: larger read-aloud type
- slide 4: standing card deleted; hearing-and-obeying statement added
- old Week-1 Anchor & Practice slide (pos 12) deleted
"""
import re, shutil, os

B = 'build/ppt'
EMU = 914400
FOREST, MOSS, INK, CREAM, DIM = '2C5F2D', '97BC62', '222B22', 'F1F6EC', '5A665A'
SITE = 'https://jgtittle-ministries.github.io/fellowship-of-the-heart-pilot-at-cca/'

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def run(text, sz=1800, color=INK, b=0, i=0, u=None, font='Calibri', link=None):
    rpr = f'<a:rPr sz="{sz}" b="{b}" i="{i}"' + (f' u="{u}"' if u else '') + '>'
    rpr += f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/>'
    if link:
        rpr += f'<a:hlinkClick xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{link}"/>'
    rpr += '</a:rPr>'
    return f'<a:r>{rpr}<a:t>{esc(text)}</a:t></a:r>'

def para(runs, spc=900, marL=0):
    m = f' marL="{marL}"' if marL else ''
    return (f'<a:p><a:pPr{m}>'
            f'<a:spcAft><a:spcPts val="{spc}"/></a:spcAft></a:pPr>{"".join(runs)}</a:p>')

def bullet(text, sz=1800, b=0, i=0, spc=900):
    return para([run('•  ', sz=sz, color=MOSS, b=1), run(text, sz=sz, b=b, i=i)], spc=spc)

def sub(runs_or_text, sz=1600, spc=700):
    lead = run('–  ', sz=sz, color=MOSS, b=1)
    rest = [run(runs_or_text, sz=sz)] if isinstance(runs_or_text, str) else runs_or_text
    return para([lead] + rest, spc=spc, marL=411480)

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

# ---------- N1 (pos 5, slide79) — Welcome, larger type ----------
n1 = [
    para([run('•  ', color=MOSS, b=1),
          run('“I came that they may have life and have it abundantly.”', i=1),
          run('  — John 10:10', sz=1600, color=MOSS, b=1)]),
    bullet('This is a journey of exploration'),
    sub('Your heart'),
    sub([run('This process — the plans, practices, and pages live at ', sz=1600),
         run('the Fellowship of the Heart website', sz=1600, color=FOREST, u='sng', link='rId2')]),
    sub('This group'),
    bullet('This is not a youth group'),
    bullet('It is family formation and growth in Christ'),
    bullet('An offer of leadership opportunity'),
]
hlink = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
         f'Target="{SITE}" TargetMode="External"/>')
write_slide('slide79.xml', [title_sp('Welcome — the Very-First-Time Orientation'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n1)], hlink)

# ---------- N2 (pos 6, slide78) — Four Connects diagram ----------
shutil.copy('four-connects.png', f'{B}/media/image17.png')
ct = f'{B}/../[Content_Types].xml'
ctp = 'build/[Content_Types].xml'
x = open(ctp, encoding='utf-8').read()
if 'Extension="png"' not in x:
    x = x.replace('</Types>', '<Default Extension="png" ContentType="image/png"/></Types>')
    open(ctp, 'w', encoding='utf-8').write(x)
W, H = 11.5, 11.5 * 990 / 2760
pic = ('<p:pic><p:nvPicPr><p:cNvPr id="5" name="Picture 4" descr="four-connects diagram"/>'
       '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
       '<p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
       f'<p:spPr><a:xfrm><a:off x="{int(0.9*EMU)}" y="{int(1.6*EMU)}"/>'
       f'<a:ext cx="{int(W*EMU)}" cy="{int(H*EMU)}"/></a:xfrm>'
       '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
refs = [para([run('THE SOWER — THREE WITNESSES:  ', sz=1400, color=MOSS, b=1),
              run('Mark 4:1–20', sz=1800, color=FOREST, b=1),
              run('   ·   Matthew 13:1–23   ·   Luke 8:4–15', sz=1800)])]
imgrel = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
          'Target="../media/image17.png"/>')
write_slide('slide78.xml', [title_sp('The Four Connects'), pic,
                            textbox(4, 0.9, 1.75 + H, 11.5, 0.7, refs)], imgrel)

# ---------- N3 (pos 7, slide77) — Container, plan order + John's subs ----------
def head(word):
    return para([run(word, sz=2600, color=FOREST, b=1)], spc=100)
n3 = [
    head('Safe'),
    sub('What is shared in this room stays in this room — no judging, no fixing, no interrupting', sz=1800, spc=100),
    sub('No shaming', sz=1800, spc=800),
    head('Present'),
    sub('Focused here — in this room, with these people', sz=1800, spc=100),
    sub('Phones silent and put away', sz=1800, spc=800),
    head('Clear'),
    sub('Releasing any roadblocks to hearing — set them aside intentionally', sz=1800, spc=800),
    head('Intentional'),
    sub([run('“I’m leaning in. I’m looking for what God has for me in the next ninety minutes.”', sz=1800, i=1)], spc=800),
]
write_slide('slide77.xml', [title_sp('Container Introduction'),
                            textbox(4, 0.9, 1.55, 11.5, 5.5, n3)])

# ---------- N4 (pos 8, slide76) — One True Sentence ----------
n4 = [
    bullet('Around the circle: one true sentence about why you are here tonight'),
    bullet('One sentence — not a paragraph, not a story'),
    bullet('The word that matters is “true” — not what you think we want to hear'),
    bullet('“Because Mom said I had to be here” counts. “I don’t know yet” counts.'),
]
write_slide('slide76.xml', [title_sp('One True Sentence — Why Each of Us Is Here'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n4)])

# ---------- N5 (pos 9, slide75) — Between-Week Practice ----------
n5 = [
    bullet('One practice this week — the simplest we will give you in all of Getting Started'),
    bullet('Each morning, before the phone: five quiet minutes'),
    sub([run('Ask one question: ', sz=1600),
         run('“Father, what are you up to today, and what do you want me to notice?”', sz=1600, i=1)]),
    sub('Then sit. Listen. The asking is the practice.'),
    bullet('Each evening, sixty seconds: one specific sentence in the journal — what did I notice today?'),
    bullet('Parents are doing this too — we check in next Wednesday'),
]
write_slide('slide75.xml', [title_sp('Between-Week Practice'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n5)])

# ---------- N6 (pos 10, slide74) — Leader Feedback Round ----------
n6 = [
    bullet('The evening’s leader goes first — same two questions, every week from here on'),
    sub([run('“What I think went well tonight: ______”', sz=1600, i=1)]),
    sub([run('“What I’d do differently next time: ______”', sz=1600, i=1)]),
    bullet('Then the room — the same two questions about tonight'),
    bullet('The leader receives without defending — “thank you” is the whole response'),
]
write_slide('slide74.xml', [title_sp('The Leader Feedback Round'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n6)])

# ---------- N7 (pos 11, slide73) — Closing + Blessing ----------
n7 = [
    bullet('We close the way we opened — the container, six steps', sz=1600, spc=800),
    bullet('One-word landing · the one thing you are taking · the one practice', sz=1600, spc=800),
    sub([run('The practice, said together: ', sz=1500),
         run('“Father, what are you up to today, and what do you want me to notice?”', sz=1500, i=1)], spc=800),
    bullet('Then the blessing — spoken over each other, face to face', sz=1600, spc=800),
]
blessing = [
    para([run('THE AARONIC BLESSING — NUMBERS 6:24–26', sz=1200, color=MOSS, b=1)], spc=1000),
    para([run('“The Lord bless you and keep you;', sz=1800, i=1, font='Cambria')], spc=700),
    para([run('the Lord make his face to shine upon you, and be gracious to you;', sz=1800, i=1, font='Cambria')], spc=700),
    para([run('the Lord lift up his countenance upon you, and give you peace.”', sz=1800, i=1, font='Cambria')], spc=700),
]
write_slide('slide73.xml', [title_sp('Closing the Container + Aaronic Blessing'),
                            textbox(4, 0.9, 1.75, 6.2, 4.6, n7),
                            textbox(6, 7.4, 1.9, 5.1, 4.0, blessing, fill=CREAM, anchor='ctr')])

# ---------- Slide 4: drop the standing card, add the purpose statement ----------
p = f'{B}/slides/slide4.xml'
x = open(p, encoding='utf-8').read()
card = None
for m in re.finditer(r'<p:sp>.*?</p:sp>', x, re.S):
    if 'You don’t have to remember' in m.group(0):
        card = m.group(0)
assert card, 'standing card not found'
x = x.replace(card, '')
purpose = textbox(80, 8.9, 2.5, 3.6, 2.4, [
    para([run('THIS YEAR, IN ONE LINE', sz=1200, color=MOSS, b=1)], spc=800),
    para([run('Hearing and obeying God', sz=2400, color=FOREST, b=1, font='Cambria')], spc=200),
], anchor='t')
x = x.replace('</p:spTree>', purpose + '</p:spTree>')
open(p, 'w', encoding='utf-8').write(x)
print('slide 4: card removed, purpose statement added')

# ---------- Delete pos-12 (slide5.xml, Week 1 Anchor & Practice) ----------
pres = f'{B}/presentation.xml'
prels = f'{B}/_rels/presentation.xml.rels'
rx = open(prels, encoding='utf-8').read()
rid = re.search(r'Id="(rId\d+)"[^>]*Target="slides/slide5\.xml"', rx).group(1)
px = open(pres, encoding='utf-8').read()
px2 = re.sub(rf'<p:sldId id="\d+" r:id="{rid}"/>', '', px, count=1)
assert px2 != px
open(pres, 'w', encoding='utf-8').write(px2)
print('slide5 removed from sldIdLst')

# ---------- Re-add slide numbers to regenerated slides ----------
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
print('slide numbers re-added to', count, 'slides')
print('ROUND 2 DONE')
