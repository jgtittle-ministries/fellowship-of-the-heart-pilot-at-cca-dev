# -*- coding: utf-8 -*-
"""Week 1 expansion of the GS club deck (John's dictation 2026-08-07):
- slide-number field on every slide (auto-updating, bottom-right)
- slide 4 road list: bullet 2 deleted, renumbered
- 7 new content slides after slide 4 (positions 5-11)
"""
import re, shutil, os

B = 'build/ppt'
EMU = 914400
FOREST, MOSS, INK, CREAM, DIM = '2C5F2D', '97BC62', '222B22', 'F1F6EC', '5A665A'
SITE = 'https://jgtittle-ministries.github.io/fellowship-of-the-heart-pilot-at-cca/'

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def run(text, sz=1500, color=INK, b=0, i=0, u=None, font='Calibri', link=None):
    rpr = f'<a:rPr sz="{sz}" b="{b}" i="{i}"' + (f' u="{u}"' if u else '') + '>'
    rpr += f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{font}"/>'
    if link:
        rpr += f'<a:hlinkClick xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{link}"/>'
    rpr += '</a:rPr>'
    return f'<a:r>{rpr}<a:t>{esc(text)}</a:t></a:r>'

def para(runs, spc=800, marL=0, spcBef=0):
    ppr = '<a:pPr'
    if marL: ppr += f' marL="{marL}"'
    ppr += '>'
    if spcBef: ppr += f'<a:spcBef><a:spcPts val="{spcBef}"/></a:spcBef>'
    ppr += f'<a:spcAft><a:spcPts val="{spc}"/></a:spcAft></a:pPr>'
    return f'<a:p>{ppr}{"".join(runs)}</a:p>'

def bullet(text, sz=1500, b=0, i=0, spc=800):
    return para([run('•  ', sz=sz, color=MOSS, b=1), run(text, sz=sz, b=b, i=i)], spc=spc)

def sub(runs_or_text, sz=1400, spc=600):
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

# ---------- N1 (pos 5, slide79) — Welcome ----------
n1 = [
    para([run('•  ', color=MOSS, b=1),
          run('“I came that they may have life and have it abundantly.”', i=1),
          run('  — John 10:10', sz=1400, color=MOSS, b=1)]),
    bullet('This is a journey of exploration'),
    sub('Your heart'),
    sub([run('This process — the plans, practices, and pages live at ', sz=1400),
         run('the Fellowship of the Heart website', sz=1400, color=FOREST, u='sng', link='rId2')]),
    sub('This group'),
    bullet('This is not a youth group'),
    bullet('It is family formation and growth in Christ'),
    bullet('An offer of leadership opportunity'),
]
hlink = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
         f'Target="{SITE}" TargetMode="External"/>')
write_slide('slide79.xml', [title_sp('Welcome — the Very-First-Time Orientation'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n1)], hlink)

# ---------- N2 (pos 6, slide78) — The Four Connects ----------
shutil.copy('s8_visual.jpeg', f'{B}/media/image16.jpg')
pic = ('<p:pic><p:nvPicPr><p:cNvPr id="5" name="Picture 4" descr="four-connects.jpg"/>'
       '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
       '<p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
       f'<p:spPr><a:xfrm><a:off x="{int(1.0*EMU)}" y="{int(1.55*EMU)}"/>'
       f'<a:ext cx="{int(3.70*EMU)}" cy="{int(5.36*EMU)}"/></a:xfrm>'
       '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
refs = [
    para([run('THE SOWER — THREE WITNESSES', sz=1200, color=MOSS, b=1)], spc=1000),
    para([run('Mark 4:1–20', sz=2000, color=FOREST, b=1)], spc=800),
    para([run('Matthew 13:1–23', sz=1700)], spc=800),
    para([run('Luke 8:4–15', sz=1700)], spc=800),
]
imgrel = ('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
          'Target="../media/image16.jpg"/>')
write_slide('slide78.xml', [title_sp('The Four Connects'), pic,
                            textbox(4, 5.3, 2.3, 6.6, 3.2, refs)], imgrel)

# ---------- N3 (pos 7, slide77) — Container Introduction ----------
def word_gloss(word, gloss):
    return [para([run(word, sz=2000, color=FOREST, b=1)], spc=100),
            para([run(gloss, sz=1300, color=DIM)], spc=900)]
n3 = (word_gloss('Present', 'Actually here — this room, these people, the whole evening') +
      word_gloss('Intentional', 'Here on purpose — willing to do whatever the Spirit invites') +
      word_gloss('Clear', 'Nothing unaddressed carried in — set it down so you can be present') +
      word_gloss('Safe', 'What is shared in this room stays in this room — no judging, no fixing, no interrupting'))
write_slide('slide77.xml', [title_sp('Container Introduction'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n3)])

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
    sub([run('Ask one question: ', sz=1400),
         run('“Father, what are you up to today, and what do you want me to notice?”', sz=1400, i=1)]),
    sub('Then sit. Listen. The asking is the practice.'),
    bullet('Each evening, sixty seconds: one specific sentence in the journal — what did I notice today?'),
    bullet('Parents are doing this too — we check in next Wednesday'),
]
write_slide('slide75.xml', [title_sp('Between-Week Practice'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n5)])

# ---------- N6 (pos 10, slide74) — The Leader Feedback Round ----------
n6 = [
    bullet('The evening’s leader goes first — same two questions, every week from here on'),
    sub([run('“What I think went well tonight: ______”', sz=1400, i=1)]),
    sub([run('“What I’d do differently next time: ______”', sz=1400, i=1)]),
    bullet('Then the room — the same two questions about tonight'),
    bullet('The leader receives without defending — “thank you” is the whole response'),
]
write_slide('slide74.xml', [title_sp('The Leader Feedback Round'),
                            textbox(4, 0.9, 1.7, 11.5, 5.2, n6)])

# ---------- N7 (pos 11, slide73) — Closing + Aaronic Blessing ----------
n7 = [
    bullet('We close the way we opened — the container, six steps', sz=1400, spc=700),
    bullet('One-word landing · the one thing you are taking · the one practice', sz=1400, spc=700),
    sub([run('The practice, said together: ', sz=1300),
         run('“Father, what are you up to today, and what do you want me to notice?”', sz=1300, i=1)], spc=700),
    bullet('Then the blessing — spoken over each other, face to face', sz=1400, spc=700),
]
blessing = [
    para([run('THE AARONIC BLESSING — NUMBERS 6:24–26', sz=1100, color=MOSS, b=1)], spc=1000),
    para([run('“The Lord bless you and keep you;', sz=1600, i=1, font='Cambria')], spc=600),
    para([run('the Lord make his face to shine upon you, and be gracious to you;', sz=1600, i=1, font='Cambria')], spc=600),
    para([run('the Lord lift up his countenance upon you, and give you peace.”', sz=1600, i=1, font='Cambria')], spc=600),
]
write_slide('slide73.xml', [title_sp('Closing the Container + Aaronic Blessing'),
                            textbox(4, 0.9, 1.75, 6.3, 4.6, n7),
                            textbox(6, 7.5, 1.9, 5.0, 3.6, blessing, fill=CREAM, anchor='ctr')])

# ---------- Slide 4: delete bullet 2, renumber ----------
p = f'{B}/slides/slide4.xml'
x = open(p, encoding='utf-8').read()
body_sps = re.findall(r'<p:sp>.*?</p:sp>', x, re.S)
body = body_sps[2]
paras = re.findall(r'<a:p>.*?</a:p>', body, re.S)
assert len(paras) == 8, len(paras)
keep = [paras[0]] + paras[2:]
renum = []
for idx, pa in enumerate(keep, 1):
    pa2 = re.sub(r'<a:t>\d+\s*</a:t>', f'<a:t>{idx}   </a:t>', pa, count=1)
    renum.append(pa2)
new_body = body.replace(''.join(paras), ''.join(renum))
x = x.replace(body, new_body)
open(p, 'w', encoding='utf-8').write(x)
print('slide 4 renumbered:', len(renum), 'items')

# ---------- Slide numbers on every slide ----------
def slidenum_sp(color):
    return ('<p:sp><p:nvSpPr><p:cNvPr id="90" name="SlideNum"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(12.45*EMU)}" y="{int(7.05*EMU)}"/>'
            f'<a:ext cx="{int(0.7*EMU)}" cy="{int(0.32*EMU)}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            '<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="45720" bIns="0" anchor="ctr"/><a:lstStyle/>'
            '<a:p><a:pPr algn="r"/><a:fld id="{B1F00A3C-9A6E-4E85-9D4C-1A56F3D0A001}" type="slidenum">'
            f'<a:rPr sz="1000" b="1"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            '<a:latin typeface="Calibri"/></a:rPr><a:t>1</a:t></a:fld></a:p></p:txBody></p:sp>')

def is_dark(hexc):
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    return (0.299*r + 0.587*g + 0.114*b) < 110

count = 0
for f in sorted(os.listdir(f'{B}/slides')):
    if not re.match(r'slide\d+\.xml$', f):
        continue
    fp = f'{B}/slides/{f}'
    x = open(fp, encoding='utf-8').read()
    if 'type="slidenum"' in x:
        continue
    m = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-Fa-f]{6})"/></a:solidFill>', x)
    color = CREAM if (m and is_dark(m.group(1))) else '7A8A6E'
    x = x.replace('</p:spTree>', slidenum_sp(color) + '</p:spTree>')
    open(fp, 'w', encoding='utf-8').write(x)
    count += 1
print('slide numbers added to', count, 'slides')
print('BUILD SCRIPT DONE')
