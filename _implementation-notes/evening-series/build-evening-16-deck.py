# Evening 16 (Carrying the Word) deck, from the Evening 11 deck (file key 12a). Corner pages W1, W2, ...
# usage: python build-evening-16-deck.py <take-home page 1 png> <take-home page 2 png> <scratch dir>
# The pngs are 150-dpi renders of "FotH Pilot Session 16a Homework Handout DRAFT v1.docx".
# The divider picture (two candles, one flame passing to the other) comes from the spare Session 19 deck,
# which is not in the walk.
import copy, io, re, sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
SRC = B + r"\FotH Evening Session 12a Slides DRAFT v1.pptx"
PIC = B + r"\FotH Evening Session 19 Slides DRAFT v1.pptx"
OUT = B + r"\FotH Evening Session 16a Slides DRAFT v1.pptx"
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
for i in (10, 9):
    drop(prs, i)
S = list(prs.slides)   # 0 title, 1 div, 2 map, 3 road, 4 container, 5 check-in, 6 teaching, 7 five ways (read-back),
                       # 8 family tables (choose), 9 say it to the room (merge), 10 th1, 11 th2, 12 feedback, 13 closing

# 1 divider
set_lines(shape(S[1], "TextBox 3"), [
    "EVENING 16", "Carrying the Word",
    "Each family chooses a short passage, learns it by heart together, and takes it home to be said every day"])
set_lines(shape(S[1], "TextBox 4"), ["Quarter 3: Mission & Rhythm"])
swap_divider_picture(S[1], PIC, "e16-divider")
notes(S[1], "E16 · pre-session · DIVIDER\nOn screen through dinner. Families talk over their passage at the table; a family still choosing can start from the PROAPT weeks, Heart Bible Study or Doing the Word.")

# 2 the map
set_lines(shape(S[2], "TextBox 4"), [
    "Evening 16 closes the third movement, Mission and Rhythm: the rhythm is built, and tonight each family takes the most portable thing there is to carry, the Word by heart. Each connection makes the next one real (Matt. 22:37–40)."])
notes(S[2], "E16 · 7:00 · LEAD: CONTAINER HOLDER · GROUNDING — every session opens on this map\nBEATS:\n1. Locate tonight: the end of Mission and Rhythm. At The Rhythm and the Four Questions each of us built the rhythm we will carry.\n2. Next time, at The Float, everyone chooses one practice to carry through the break. A passage learned tonight is the easiest thing to carry.\n3. One sentence: a verse carried by heart is there when no Bible is open, long after the evenings stop.")

# 3 tonight's road
set_lines(shape(S[3], "TextBox 2"), ["Evening 16 — Tonight’s Road"])
set_lines(shape(S[3], "TextBox 3"), [
    "1   Welcome and centering",
    "2   The check-in circle — two weeks of the Rhythm Card",
    "3   On your heart — Deuteronomy 6 and Psalm 119",
    "4   Five ways to carry it — taught by the teens",
    "5   Family tables — choose, write, learn",
    "6   Say it to the room",
    "7   Homework, feedback and the Aaronic blessing"])
notes(S[3], "E16 · 7:00–8:30 · LEAD: BOTH LEADERS\nBEATS:\n1. Walk the road briefly: a check-in, a short teaching, the teens teach five ways to carry a passage, then the family tables, then each family says its passage to the room.\n2. Name the handoffs: the content presenter leads the teaching, the five ways (with the other teens) and the tables; the container holder keeps the clock, watches the room, and leads the check-in and the circle.\n3. Two named adults hold safety tonight.")

# 4 opening container (full eight steps)
notes(S[4], "E16 · 7:00–7:08 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Aaronic blessing first.\n2. Full eight steps, normal pace. Safe, present, clear, intentional, said aloud.\nCUES: The one-word check-in gets one unhurried breath after each word; no commentary.")

# 5 check-in
set_lines(shape(S[5], "TextBox 4"), [
    "•  Two weeks of the Rhythm Card: what held, what slipped?",
    "•  The week-one check-ins: did your partner reach you? Did you reach them?",
    "–  A thin week is an honest answer; pass is a complete answer",
    "•  A parent starts the round — pass-anytime holds",
    "•  Received with “We hear that.” No advice, no fixing"])
notes(S[5], "E16 · 7:08–7:22 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One or two sentences each, the arranged parent first: two weeks of the Rhythm Card, what held and what slipped.\n2. Then the week-one check-ins: did the partners connect? Thank the pairs who did, by name.\n3. Receive each with 'We hear that'; no advice.\nCUES: Never cold-call a teen. Fourteen minutes, not more.\nGUARD: Anything heavy goes to a safety adult after the close, not into the circle.")

# 6 teaching
set_lines(shape(S[6], "TextBox 2"), ["On Your Heart — Deuteronomy 6"])
set_lines(shape(S[6], "TextBox 4"), [
    "•  “These words that I command you today shall be on your heart” (Deut 6:6)",
    "•  Taught to your children, talked of when you sit at home, when you walk by the way, when you lie down and when you rise (Deut 6:7)",
    "•  The Word passed from parent to child, at home, in ordinary moments: this whole design in one sentence",
    "•  “Let the word of Christ dwell in you richly … teaching and admonishing one another” (Col 3:16)",
    "•  A verse carried by heart is there when no Bible is open"])
set_lines(shape(S[6], "TextBox 6"), [
    "PSALM 119:11",
    "“I have stored up your word in my heart, that I might not sin against you.”"])
notes(S[6], "E16 · 7:22–7:30 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Read Deuteronomy 6:6–9 aloud, slowly, from the physical Bible. Then Psalm 119:11.\n2. The one idea: God told parents to carry His words at home, in the sitting, walking, lying down and rising. That is what this whole walk has been for.\n3. Name the four moments in Deuteronomy 6: a meal, the drive, bedtime, waking. Tonight each family will choose one.\nCUES: Eight minutes. Psalm 119:11 is the room's verse for the next block; say it once together now.")

# 7 five ways to carry it (taught by the teens)
set_lines(shape(S[7], "TextBox 2"), ["Five Ways to Carry It"])
set_lines(shape(S[7], "TextBox 4"), [
    "1   Write it out by hand — slowly, once, in your journal",
    "2   First letters only — “I h s u y w i m h”",
    "3   A phrase at a time, building — say it, add the next, say both",
    "4   Aloud, with a gesture — a simple movement for each line",
    "5   Tie it to a moment — a meal, the drive, bedtime, waking",
    "•  The room tries each one on Psalm 119:11, together"])
notes(S[7], "E16 · 7:30–7:42 · LEAD: CONTENT PRESENTER, WITH THE OTHER TEENS\nBEATS:\n1. The teens teach: each takes one of the five ways and leads the room through it on Psalm 119:11.\n2. Write it by hand: everyone writes the verse once. First letters: say it from the letters on the screen. A phrase at a time: build it together. Aloud with a gesture: the teen shows one; the room copies. Tie it to a moment: which moment will you use?\n3. By the end the whole room can say Psalm 119:11. Say it once together.\nCUES: Two minutes per way; keep it light. The Carrying Card has all five for the tables.")

# 8 family tables
set_lines(shape(S[8], "TextBox 2"), ["Family Tables — Choose, Write, Learn"])
set_lines(shape(S[8], "TextBox 4"), [
    "•  Choose or confirm your passage: two to four verses, one translation, from your own journey if it can be",
    "•  Write it out on the Carrying Card; decide who carries which part",
    "•  Every age carries what it can: one verse, or one line of it, counts as fully as four",
    "•  Start learning it, a parent and a teen taking turns; a parent goes first",
    "•  Name your moment each day",
    "•  Back in the circle at 8:05"])
notes(S[8], "E16 · 7:42–8:05 · LEAD: CONTENT PRESENTER · CONTAINER HOLDER WATCHING THE ROOM\nBEATS:\n1. Send the families to their tables with the Carrying Card. Twenty-three minutes.\n2. Walk the room: help a family still choosing; shorten a portion quietly for the youngest or anyone finding it hard.\n3. A family without a passage yet can take Psalm 119:11, the room's verse; they may choose another during the week.\nCUES: Call the five-minute mark at 8:00.\nGUARD: No contests, no grading, no shame. A family that gets one line is doing the practice.")

# 9 say it to the room
set_lines(shape(S[9], "TextBox 2"), ["Say It to the Room"])
set_lines(shape(S[9], "TextBox 4"), [
    "•  Each family says its passage, as far as it has it; haltingly is fine",
    "•  A parent begins; stumbles included",
    "•  Received with “We hear that”; the room may say it back once",
    "•  It is the Word, not a performance: slowly, meaning it",
    "•  Forgetting is part of learning"])
notes(S[9], "E16 · 8:05–8:15 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Family by family, the arranged family first. A parent begins.\n2. After each, 'We hear that.' If the family wants, the room says it back once.\n3. Close the round: 'At The Float we will say these again.'\nCUES: Ten minutes; about a minute a family. Never cold-call a teen to say a part alone.\nGUARD: Nobody is scored and nobody is compared. Teens learn to carry the Word by watching their parents carry it.")

# 10, 11 take-home: one part of the sheet per slide, full size
set_lines(shape(S[10], "TextBox 2"), ["The Take-Home Sheet — Your Passage, and Week One"])
place_crop(S[10], IMG1, (100, 740, 1175, 1212), "e16-takehome-week-one")
notes(S[10], "E16 · 8:15–8:21 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n2. At the top: your passage, the part you carry, and your moment. Fill it in now.\n3. Week one: say it together every day, at your moment. Once a day is enough; more is a gift.\n4. Check-in partners named aloud: at the end of week one, say your part of the passage to each other.")
set_lines(shape(S[11], "TextBox 2"), ["The Take-Home Sheet — Week Two, and Bring It Back"])
place_crop(S[11], IMG2, (100, 120, 1175, 610), "e16-takehome-week-two")
notes(S[11], "E16 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. Week two: keep saying it together, and one journal line, where this passage met me this week.\n2. At The Float, each family says its passage again; it is the first thing offered to carry through the break.\n3. At The Return II, after the break, we say it once more and see what carried.")

# 12 leader feedback round
notes(S[12], "E16 · 8:21–8:25 · LEAD: BOTH LEADERS\nBEATS:\n1. Same round every week, leader first: what went well tonight, what I'd do differently.\n2. Invite one of the teens who taught a way to answer the same two.\n3. Then the room, the same two questions about the leaders.\nCUES: 'Thank you' is the whole response.")

# 13 closing
notes(S[13], "E16 · 8:25–8:30 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Closing protocol, unhurried: stand; one-word landing; the one thing taken from tonight; the one practice: tonight, the passage.\n2. Name the road: at the next evening, The Float, everyone chooses one practice to carry through the break, and the passage comes first.\n3. Aaronic blessing.\nBLESSINGS: eyes on the person, not the screen; say what is on your heart for them, specific and short.")

# corner pages W1, W2, ...
for i, s in enumerate(prs.slides, 1):
    sn = next(sh for sh in s.shapes if sh.name == "SlideNum")
    runs = sn.text_frame.paragraphs[0].runs
    runs[0].text = "W%d" % i
    for r in runs[1:]: r.text = ""
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))

