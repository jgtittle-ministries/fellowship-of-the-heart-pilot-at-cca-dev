# Evening 13 (Serving Together) deck, from the Evening 11 deck (file key 12a). Corner pages S1, S2, ...
# usage: python build-evening-13-deck.py <take-home page 1 png> <take-home page 2 png> <scratch dir>
# The pngs are 150-dpi renders of "FotH Pilot Session 13a Homework Handout DRAFT v1.docx".
# Only the opening and the circle use the screen; on site there is none. The divider picture (two hands reaching)
# comes from the spare Session 14 deck, which is not in the walk.
import copy, io, re, sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
SRC = B + r"\FotH Evening Session 12a Slides DRAFT v1.pptx"
PIC = B + r"\FotH Evening Session 14 Slides DRAFT v1.pptx"
OUT = B + r"\FotH Evening Session 13a Slides DRAFT v1.pptx"
IMG1, IMG2, TMP = sys.argv[1], sys.argv[2], sys.argv[3]

prs = Presentation(SRC)
PFX = re.compile(r"^(•\s+|–\s+|\d+\s+)")


def drop(prs, idx):
    sld = prs.slides._sldIdLst
    ids = list(sld)
    rid = ids[idx].get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    prs.part.drop_rel(rid)
    sld.remove(ids[idx])


def kind(text):
    t = text.lstrip()
    if t.startswith("•"): return "bullet"
    if t.startswith("–"): return "sub"
    if re.match(r"\d+\s", t): return "num"
    return "plain"


def set_lines(shape, lines):
    tf = shape.text_frame
    paras = list(tf.paragraphs)
    tpl = {}
    for p in paras:
        tpl.setdefault(kind(p.text), []).append(p._p)
    fallback = paras[0]._p
    parent = fallback.getparent()
    anchor = paras[-1]._p
    new, seen = [], {}
    for line in lines:
        k = kind(line)
        i = seen.get(k, 0); seen[k] = i + 1
        group = tpl.get(k) or [fallback]
        el = copy.deepcopy(group[min(i, len(group) - 1)] if k == "plain" else group[0])
        new.append(el)
    for el in new:
        anchor.addnext(el); anchor = el
    for p in paras:
        parent.remove(p._p)
    from pptx.text.text import _Paragraph
    for el, line in zip(new, lines):
        p = _Paragraph(el, tf)
        runs = p.runs
        m = PFX.match(line)
        if m and len(runs) >= 2:
            runs[0].text, runs[1].text = m.group(1), line[m.end():]
            for r in runs[2:]: r.text = ""
        elif runs:
            runs[0].text = line
            for r in runs[1:]: r.text = ""


def shape(s, name):
    return next(sh for sh in s.shapes if sh.name == name)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


AREA_T, AREA_H, AREA_W = 1463040, 4892040, 10332720


def place_crop(s, img, box, name):
    old = next(sh for sh in s.shapes if sh.shape_type == 13 and sh.name == "Picture 3")
    old._element.getparent().remove(old._element)
    path = "%s\\%s.png" % (TMP, name)
    Image.open(img).convert("RGB").crop(box).save(path)
    im = Image.open(path)
    r = min(AREA_W / im.width, AREA_H / im.height)
    w, h = int(im.width * r), int(im.height * r)
    new = s.shapes.add_picture(path, Emu((prs.slide_width - w) // 2), Emu(AREA_T), Emu(w), Emu(h))
    new.name = "Picture 3"
    print(name, im.size, "->", round(w / 914400, 2), "x", round(h / 914400, 2), "in")


def swap_divider_picture(s, src_deck, name):
    old = next(sh for sh in s.shapes if sh.shape_type == 13)
    l, t, w, h, nm = old.left, old.top, old.width, old.height, old.name
    blob = next(sh for sh in Presentation(src_deck).slides[1].shapes if sh.shape_type == 13).image.blob
    path = "%s\\%s.jpg" % (TMP, name)
    open(path, "wb").write(blob)
    im = Image.open(io.BytesIO(blob))
    r = min(w / im.width, h / im.height)
    nw, nh = int(im.width * r), int(im.height * r)
    new = s.shapes.add_picture(path, Emu(l + (w - nw) // 2), Emu(t + (h - nh) // 2), Emu(nw), Emu(nh))
    # keep the old picture's frame and shadow: take its spPr effects, then remove it
    eff = old._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    ln = old._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ln")
    for el in (ln, eff):
        if el is not None:
            new._element.spPr.append(copy.deepcopy(el))
    old._element.addprevious(new._element)
    old._element.getparent().remove(old._element)
    new.name = nm


# the Evening 11 deck, 0-based: 0 title, 1 divider, 2 map, 3 road, 4 container, 5 check-in, 6 teaching, 7 read-back,
# 8 choose, 9 test, 10 pairs, 11 merge, 12 take-home 1, 13 take-home 2, 14 feedback, 15 closing.
for i in (10, 9, 8):
    drop(prs, i)
S = list(prs.slides)   # 0 title, 1 div, 2 map, 3 road, 4 container, 5 check-in, 6 teaching, 7 read-back, 8 merge,
                       # 9 th1, 10 th2, 11 feedback, 12 closing

# 1 divider
set_lines(shape(S[1], "TextBox 3"), [
    "EVENING 13", "Serving Together",
    "The room obeys together: an hour of serving someone, side by side, with the teens having planned it"])
set_lines(shape(S[1], "TextBox 4"), ["Quarter 3: Mission & Rhythm"])
swap_divider_picture(S[1], PIC, "e13-divider")
notes(S[1], "E13 · pre-session · DIVIDER\nOn screen through the quick dinner. The planning teens confirm jobs and rides at the table, from the Serving Plan.")

# 2 the map
set_lines(shape(S[2], "TextBox 4"), [
    "Evening 13 stands in the fourth box — Connect with Mission: tonight the room does, together, one of the works He prepared (Eph. 2:10). Each connection makes the next one real (Matt. 22:37–40)."])
notes(S[2], "E13 · 6:25 · LEAD: CONTAINER HOLDER · GROUNDING — every session opens on this map\nBEATS:\n1. One sentence: at Evening 11 each of us took one small step of obedience. Tonight the room takes one together.\n2. At Evening 12 we looked for the works God prepared for us. Tonight we do one of them.\nCUES: Thirty seconds tonight; the clock is short.")

# 3 tonight's road
set_lines(shape(S[3], "TextBox 2"), ["Evening 13 — Tonight’s Road"])
set_lines(shape(S[3], "TextBox 3"), [
    "1   Welcome, blessing and John 13", "2   The guards, and the plan",
    "3   Travel — leave at 6:35", "4   Serving — about an hour, together",
    "5   Travel back — home by 8:00", "6   The circle — where did you see God?",
    "7   Homework, feedback and the Aaronic blessing"])
notes(S[3], "E13 · 6:25–6:35 · LEAD: BOTH LEADERS\nBEATS:\n1. Walk the road in one breath: a short opening here, the work there, the circle back here.\n2. Name who leads on site: the planning teens, with an adult alongside each job.\n3. Two named adults hold safety tonight, here and on site.\nCUES: Ten minutes for the whole opening, slides 2 to 8.")

# 4 opening container: short form tonight
set_lines(shape(S[4], "TextBox 2"), ["Opening Container — Short Form Tonight"])
set_lines(shape(S[4], "TextBox 4"), [
    "1   Phones silenced and put away",
    "2   Stand in a circle",
    "3   Spoken commitment: “I am here. I am paying attention. I am willing to be moved.”",
    "4   Opening prayer — “Holy Spirit, you are welcome here. Speak. We are listening.”",
    "5   The full eight steps return at the next evening"])
notes(S[4], "E13 · 6:25 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Aaronic blessing first.\n2. Short form tonight: stand, the spoken commitment, the opening prayer. The full eight steps return at the next evening.\nCUES: Two minutes; the people we serve are expecting us.")

# 6 teaching (John 13) comes before the guards
set_lines(shape(S[6], "TextBox 2"), ["If You Do Them — John 13"])
set_lines(shape(S[6], "TextBox 4"), [
    "•  On His last night, Jesus took a towel and washed His disciples’ feet (John 13:4–5)",
    "•  “I have given you an example, that you also should do just as I have done to you” (John 13:15)",
    "•  What we do for the hungry, the stranger and the sick, we do for Him (Matt 25:35–40)",
    "•  At Evening 11, each of us obeyed. Tonight the room obeys together",
    "•  Say verse 17 together"])
set_lines(shape(S[6], "TextBox 6"), [
    "JOHN 13:17",
    "“If you know these things, blessed are you if you do them.”"])
notes(S[6], "E13 · 6:27–6:31 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Read John 13:1–17 aloud from the physical Bible; slowly, but without comment.\n2. Then the whole room says verse 17 together, once.\n3. One sentence from Matthew 25: tonight we serve Him.\nCUES: Four minutes. The reading is the teaching tonight.")

# 5 the guards
set_lines(shape(S[5], "TextBox 2"), ["Before We Go — the Guards"])
set_lines(shape(S[5], "TextBox 4"), [
    "•  We serve with people, not at them: what they asked for, the way they want it done",
    "•  No photos for show (Matt 6:1); a photo for the family who asked for one is fine",
    "•  If they ask why we came, say so simply. Tonight the kindness is the witness",
    "•  Parents present; no one works alone or out of sight",
    "–  No ladders, roofs or power tools for teens",
    "•  We go under the same pastoral covering as every evening"])
notes(S[5], "E13 · 6:31–6:33 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Read the guards aloud, plainly. They protect the people we serve, and us.\n2. Name the pastoral covering aloud, by name, before anyone leaves.\nGUARD: The people we serve keep their dignity. We do what they asked for, the way they want it done.")

# 7 the plan
set_lines(shape(S[7], "TextBox 2"), ["Tonight’s Work"])
set_lines(shape(S[7], "TextBox 4"), [
    "1   Who we are serving: ________________",
    "2   Where: ________________",
    "3   What they asked for: ________________",
    "4   The jobs and who does them — on the Serving Plan",
    "5   Drivers and riders — leave at 6:35, on site 6:45",
    "•  The planning teens lead on site; an adult alongside each job"])
notes(S[7], "E13 · 6:33–6:35 · LEAD: CONTENT PRESENTER · A PLANNING TEEN WALKS THE PLAN\nBEATS:\n1. Before the evening, the planning teens fill the blanks on this slide from the Serving Plan.\n2. A planning teen walks it aloud: who, where, what they asked for, the jobs, the rides.\n3. Then a short prayer for the people we serve, by name, and we go.\nCUES: Two minutes. If the work moved to a Saturday, this slide still opens the morning.")

# 8 the circle
set_lines(shape(S[8], "TextBox 2"), ["The Circle — Where Did You See God?"])
set_lines(shape(S[8], "TextBox 4"), [
    "•  One sentence each: what I saw, what I felt, where I saw God",
    "•  A parent starts; pass is a full answer",
    "•  Received as witness: “We hear that.” No commentary",
    "•  Tired is fine. The work is not finished until the room has said where it saw God",
    "•  “Truly, I say to you, as you did it to one of the least of these my brothers, you did it to me” (Matt 25:40)"])
notes(S[8], "E13 · 8:00–8:20 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Back in the circle, coats off, sitting. One sentence each, the arranged parent first.\n2. 'We hear that' is the whole response.\n3. Thank the planning teens by name, specifically: what they did, and what it made possible.\nCUES: Twenty minutes, even if everyone is tired.\nGUARD: Talk about the people we served with honor; nothing said about them here that we would not say in front of them.")

# 9, 10 take-home: one part of the sheet per slide, full size
set_lines(shape(S[9], "TextBox 2"), ["The Take-Home Sheet — Week One"])
place_crop(S[9], IMG1, (100, 745, 1175, 1245), "e13-takehome-week-one")
notes(S[9], "E13 · 8:20–8:25 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n2. Week one: daily PROAPT, as always, and eyes open for one more chance to serve, unplanned. The morning question with it: 'Lord, who could I serve today?'\n3. Check-in partners named aloud: at the end of week one, 'Did a chance come? Did you take it?'")
set_lines(shape(S[10], "TextBox 2"), ["The Take-Home Sheet — Week Two"])
place_crop(S[10], IMG2, (100, 120, 1175, 515), "e13-takehome-week-two")
notes(S[10], "E13 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. Week two: two lines in the journal, what I did and where I saw God in it.\n2. No chance came, or you let one pass? Write that too. Honest data, not failure.\n3. Bring one sentence back to The Rhythm: where I saw God when we served.")

# 11 leader feedback round, folded into the circle tonight
notes(S[11], "E13 · 8:25–8:28 · LEAD: BOTH LEADERS\nBEATS:\n1. Folded into the circle tonight, and short: each leader, one thing that went well and one to do differently.\n2. The planning teens are leaders tonight too: invite one of them to answer the same two.\nCUES: 'Thank you' is the whole response.")

# 12 closing
notes(S[12], "E13 · 8:28–8:30 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Short close: stand; one-word landing; the Aaronic blessing.\n2. Name the road: at the next evening, The Rhythm and the Four Questions, each person builds the rhythm they will carry, and serving can be part of it.\nBLESSINGS: eyes on the person, not the screen; say what is on your heart for them, specific and short.")

# order: teaching (6) before the guards (5)
sld = prs.slides._sldIdLst
ids = list(sld)
sld.remove(ids[6]); sld.insert(5, ids[6])

# corner pages S1, S2, ...
for i, s in enumerate(prs.slides, 1):
    sn = next(sh for sh in s.shapes if sh.name == "SlideNum")
    runs = sn.text_frame.paragraphs[0].runs
    runs[0].text = "S%d" % i
    for r in runs[1:]: r.text = ""
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
