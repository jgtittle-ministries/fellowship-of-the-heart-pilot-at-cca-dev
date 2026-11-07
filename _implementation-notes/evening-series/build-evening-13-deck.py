# Evening 13 (Serving Together) deck, from the Evening 11 deck (file key 12a). Corner pages S1, S2, ...
# usage: python build-evening-13-deck.py <take-home page 1 png> <take-home page 2 png> <scratch dir>
# The pngs are 150-dpi renders of "FotH Pilot Session 13a Homework Handout DRAFT v1.docx".
# Reshaped 7 November 2026 (John's word): the room hears, plans and agrees together in the evening; the serving happens
# in the two weeks; the report comes back at Evening 14. The divider picture (two hands reaching) comes from the spare
# Session 14 deck, which is not in the walk.
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


def stack(img, boxes, name):
    """Crop several regions of one page and stack them, top to bottom, into one picture."""
    src = Image.open(img).convert("RGB")
    parts = [src.crop(b) for b in boxes]
    w = max(p.width for p in parts)
    out = Image.new("RGB", (w, sum(p.height for p in parts) + 20 * (len(parts) - 1)), "white")
    y = 0
    for p in parts:
        out.paste(p, (0, y)); y += p.height + 20
    path = "%s\\%s-stacked.png" % (TMP, name)
    out.save(path)
    return path, (0, 0, out.width, out.height)


# the Evening 11 deck, 0-based: 0 title, 1 divider, 2 map, 3 road, 4 container, 5 check-in, 6 teaching, 7 read-back,
# 8 choose, 9 test, 10 pairs, 11 merge, 12 take-home 1, 13 take-home 2, 14 feedback, 15 closing. All sixteen are used:
# 7 hear, 8 plan, 9 agree, 10 the serving day (moved after the circle), 11 the circle.
S = list(prs.slides)

# 1 divider
set_lines(shape(S[1], "TextBox 3"), [
    "EVENING 13", "Serving Together",
    "The room hears, plans and agrees together, serves someone in the two weeks, and reports back at Evening 14"])
set_lines(shape(S[1], "TextBox 4"), ["Quarter 3: Mission & Rhythm"])
swap_divider_picture(S[1], PIC, "e13-divider")
notes(S[1], "E13 · pre-session · DIVIDER\nOn screen through dinner. Ideas for whom to serve can be talked over at the table; nothing is decided yet. Set up the flip chart where everyone can see it.")

# 2 the map
set_lines(shape(S[2], "TextBox 4"), [
    "Evening 13 stands in the fourth box — Connect with Mission: tonight the room chooses, together, one of the works He prepared (Eph. 2:10), and does it before we meet again. Each connection makes the next one real (Matt. 22:37–40)."])
notes(S[2], "E13 · 7:00 · LEAD: CONTAINER HOLDER · GROUNDING — every session opens on this map\nBEATS:\n1. At Evening 11 each of us took one small step of obedience. At Evening 12 we looked for the works God prepared for us.\n2. Tonight the room chooses one to do together. The serving happens in the next two weeks; at Evening 14 we report back.\n3. Name the three skills: hearing together, planning together, agreeing together.")

# 3 tonight's road
set_lines(shape(S[3], "TextBox 2"), ["Evening 13 — Tonight’s Road"])
set_lines(shape(S[3], "TextBox 3"), [
    "1   Welcome and centering",
    "2   The check-in circle — and the ideas you brought",
    "3   The room obeys together — John 13, Acts 13 and 15",
    "4   Hear together",
    "5   Plan together",
    "6   Agree together",
    "7   The circle, homework, feedback and the Aaronic blessing"])
notes(S[3], "E13 · 7:00–7:07 · LEAD: BOTH LEADERS\nBEATS:\n1. Walk the road briefly: tonight we do not serve yet. We hear, we plan and we agree, and we leave with a date.\n2. Name the handoffs: the content presenter leads the teaching and the hearing; the teens run the chart in the planning; the container holder leads the check-in, the agreement round and the circle.\n3. Two named adults hold safety tonight.")

# 4 opening container (full eight steps)
notes(S[4], "E13 · 7:00–7:07 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Aaronic blessing first.\n2. Full eight steps, normal pace. Safe, present, clear, intentional, said aloud.\nCUES: The one-word check-in gets one unhurried breath after each word; no commentary.")

# 5 check-in, and the ideas brought
set_lines(shape(S[5], "TextBox 4"), [
    "•  Two weeks since What Was Prepared for You: what did you notice?",
    "•  The week-one check-ins: did your partner reach you? Did you reach them?",
    "–  A thin week is an honest answer; pass is a complete answer",
    "•  Then the idea you brought: someone near us the room could serve",
    "–  Each goes on the chart; no discussion yet",
    "•  A parent starts; received with “We hear that”"])
notes(S[5], "E13 · 7:07–7:17 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One sentence each on the two weeks, the arranged parent first; then the week-one check-ins.\n2. Second round: the idea each person brought. A teen writes each on the chart as it is said.\n3. No discussion, no 'that's a good one.' The ideas wait for the hearing.\nCUES: Ten minutes. Never cold-call a teen. No idea brought is fine; say so and pass.\nGUARD: Ideas name people. Speak of them with honor; nothing said here we would not say in front of them.")

# 6 teaching
set_lines(shape(S[6], "TextBox 2"), ["The Room Obeys Together"])
set_lines(shape(S[6], "TextBox 4"), [
    "•  Jesus washed His disciples’ feet: “I have given you an example” (John 13:15)",
    "•  At Antioch, worshiping and fasting, the Spirit spoke to the whole group, and the group acted together (Acts 13:1–3)",
    "•  At Jerusalem, they heard each other out, weighed it by Scripture, and agreed (Acts 15)",
    "•  Tonight, three skills: hear together, plan together, agree together",
    "•  Say John 13:17 together"])
set_lines(shape(S[6], "TextBox 6"), [
    "ACTS 15:28",
    "“It has seemed good to the Holy Spirit and to us.”"])
notes(S[6], "E13 · 7:17–7:24 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Read John 13:12–17 aloud from the physical Bible; the room says verse 17 together, once.\n2. Read Acts 13:1–3: they were worshiping when the Spirit spoke, and the whole group acted on it.\n3. Acts 15 in one breath: a hard question, stories heard, Scripture weighed, then 'it has seemed good to the Holy Spirit and to us.' That is tonight's shape: hear, plan, agree.\nCUES: Seven minutes. The readings are the teaching.")

# 7 hear together
set_lines(shape(S[7], "TextBox 2"), ["Hear Together"])
set_lines(shape(S[7], "TextBox 4"), [
    "1   The question: “Lord, whom would you have us serve together, and how?”",
    "2   Three minutes of quiet; write down what comes",
    "3   Each says what came: a name, a need, a picture, a verse, or nothing",
    "4   It goes on the chart, beside the ideas you brought",
    "5   Received with “We hear that”",
    "•  Say what you heard, not why it is right"])
notes(S[7], "E13 · 7:24–7:36 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Pray the question aloud, then keep three full minutes of quiet. Watch the clock, not the room.\n2. Around the circle, a parent first: what came. A teen adds each to the chart; a star beside an idea already there.\n3. 'Nothing came' is a full answer.\nCUES: Twelve minutes.\nGUARD: Nobody argues for an idea yet, and nobody says 'God told me' to end a discussion. What someone heard is weighed, like everything else (1 John 4:1).")

# 8 plan together
set_lines(shape(S[8], "TextBox 2"), ["Plan Together"])
set_lines(shape(S[8], "TextBox 4"), [
    "•  The teens at the chart: one holds the marker, one keeps the Serving Plan",
    "•  The four checks: local and concrete; a job for every age; an hour or two of real work; arranged with the people served",
    "•  Narrow to a first choice and a second",
    "•  Then the plan: the jobs and who, what each family brings, the date, the drivers",
    "•  Who calls them, and by when: a teen, with a parent alongside"])
notes(S[8], "E13 · 7:36–7:58 · LEAD: CONTENT PRESENTER · THE TEENS AT THE CHART · CONTAINER HOLDER WATCHING THE ROOM\nBEATS:\n1. Hand the marker to a teen. Parents give ideas and concerns like everyone else; the teens run it.\n2. Read the four checks against the chart; strike what fails, star what passes. Look first at what was heard more than once.\n3. Choose a first and a second. Then fill the Serving Plan: jobs (one for every age), what each family brings, a date in the next two weeks (usually a Saturday morning), drivers, and who makes the call by when.\nCUES: Call the five-minute mark at 7:53. A plan that is mostly done is enough; the teens finish the details by text.\nGUARD: Nothing is promised to anyone tonight. The call asks what they would like.")

# 9 agree together
set_lines(shape(S[9], "TextBox 2"), ["Agree Together"])
set_lines(shape(S[9], "TextBox 4"), [
    "•  Not a vote. Each in turn: “I’m in,” or “I’m in, with a concern,” or “Not yet: here is what would make it a yes”",
    "•  Concerns are heard; the plan changes until every voice is in",
    "•  After the call: if they ask for something different, the teens and a parent change the plan to fit; if they say no thank you, the second choice",
    "•  The prayer of agreement, over the plan and the people, by name (Matt 18:19)"])
notes(S[9], "E13 · 7:58–8:08 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Go around the whole circle, parents and teens alike. Every voice, not the loudest.\n2. A concern: thank them, ask what would answer it, and change the plan if it should change. A 'not yet': ask what would make it a yes.\n3. When every voice is in, the room agrees how the plan may change after the call. Then a parent and a teen pray over the plan and the people, by name.\nCUES: Ten minutes. If it will not settle, keep the first choice as heard, name the concern on the Serving Plan, and let the teens and John finish it this week.\nGUARD: A quiet 'not yet' is worth more than a fast yes. Nobody is pressed to agree.")

# 11 the circle
set_lines(shape(S[11], "TextBox 2"), ["The Circle — Which Was Hardest?"])
set_lines(shape(S[11], "TextBox 4"), [
    "•  One sentence each: which was hardest tonight, hearing, planning or agreeing?",
    "•  And where did you see God in it?",
    "•  A parent starts; pass is a full answer",
    "•  Received as witness: “We hear that.” No commentary",
    "•  “If you know these things, blessed are you if you do them” (John 13:17)"])
notes(S[11], "E13 · 8:08–8:14 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One sentence each, the arranged parent first.\n2. 'We hear that' is the whole response.\n3. Thank the teens at the chart by name, specifically: what they did, and what it made possible.\nCUES: Six minutes. Listen for which skill the room found hardest; it goes to the debrief.")

# 10 the serving day (shown at the commissioning)
set_lines(shape(S[10], "TextBox 2"), ["On Our Date — the Serving Day"])
set_lines(shape(S[10], "TextBox 4"), [
    "1   Meet, pray for the people by name, and drive over together",
    "2   An hour or two of work; the teens lead, an adult alongside each job",
    "3   Before we leave: a blessing for the people we served",
    "•  Parents present; no one alone or out of sight; no ladders, roofs or power tools for teens",
    "•  We serve with people, not at them; no photos for show (Matt 6:1)",
    "•  The pastoral covering named aloud before we go"])
notes(S[10], "E13 · 8:14 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. Walk the day in one breath: gather and pray, the work, a blessing before we leave.\n2. Read the guards aloud, plainly. They protect the people we serve, and us.\n3. If they ask why we came, say so simply. The kindness is the witness.")

# 12, 13 take-home: the plan at the top with week one; then on our date and the report
set_lines(shape(S[12], "TextBox 2"), ["The Take-Home Sheet — Our Plan, and Week One"])
img, box = stack(IMG1, [(100, 268, 1175, 472), (100, 950, 1175, 1445)], "e13-takehome-plan-week-one")
place_crop(S[12], img, box, "e13-takehome-plan-week-one")
notes(S[12], "E13 · 8:14–8:20 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n2. At the top: write in our plan now, whom we serve, our date and your part. What they asked for comes after the call.\n3. Week one: daily PROAPT with 'Lord, how should we serve them?' The call is made by the day agreed; the teens tell the room what they asked for. Get your part ready.\n4. Check-in partners named aloud: at the end of week one, 'Is your part ready? What do you need?'")
set_lines(shape(S[13], "TextBox 2"), ["The Take-Home Sheet — On Our Date, and Bring It Back"])
place_crop(S[13], IMG2, (100, 118, 1175, 585), "e13-takehome-date-report")
notes(S[13], "E13 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. On our date: we serve together. Afterwards, two journal lines: what I did, and where I saw God in it.\n2. If the day did not go as planned, write that too. Honest data, not failure.\n3. At Evening 14 the teens who planned it give the room's report: what we planned, what happened, what changed, where we saw God. Then one sentence each.")

# 14 leader feedback round
notes(S[14], "E13 · 8:20–8:24 · LEAD: BOTH LEADERS\nBEATS:\n1. Same round every week, leader first: what went well tonight, what I'd do differently.\n2. The teens who ran the chart are leaders tonight too: invite one of them to answer the same two.\n3. Then the room, the same two questions about the leaders.\nCUES: 'Thank you' is the whole response.")

# 15 closing
notes(S[15], "E13 · 8:24–8:30 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Closing protocol, unhurried: stand; one-word landing; the one thing taken from tonight; the one practice: tonight, your part in the plan.\n2. Name the road: we serve on our date; at Evening 14, The Rhythm and the Four Questions, the room tells what God did, and each person builds the rhythm they will carry.\n3. Aaronic blessing.\nBLESSINGS: eyes on the person, not the screen; say what is on your heart for them, specific and short.")

# order: the circle (11) before the serving day (10)
sld = prs.slides._sldIdLst
ids = list(sld)
sld.remove(ids[11]); sld.insert(10, ids[11])

# corner pages S1, S2, ...
for i, s in enumerate(prs.slides, 1):
    sn = next(sh for sh in s.shapes if sh.name == "SlideNum")
    runs = sn.text_frame.paragraphs[0].runs
    runs[0].text = "S%d" % i
    for r in runs[1:]: r.text = ""
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
