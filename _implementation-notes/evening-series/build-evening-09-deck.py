# Evening 9 (Heart Bible Study) deck, from the Evening 6 combined deck. Corner pages H1, H2, ...
import copy, re, sys
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
SRC = B + r"\FotH Evening Session 7-8 Combined Slides DRAFT v1.pptx"
DIV = B + r"\FotH Evening Session 6 Slides DRAFT v1.pptx"      # its last slide is a movement divider with no pictures
OUT = B + r"\FotH Evening Session 11a Slides DRAFT v1.pptx"
IMG1, IMG2 = sys.argv[1], sys.argv[2]                          # renders of the take-home's two pages

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


def swap_picture(s, pic_name, img):
    pic = shape(s, pic_name)
    l, t, w, h = pic.left, pic.top, pic.width, pic.height
    pic._element.getparent().remove(pic._element)
    new = s.shapes.add_picture(img, l, t)
    r = min(w / new.width, h / new.height)
    new.width, new.height = int(new.width * r), int(new.height * r)
    new.left = l + (w - new.width) // 2
    new.top = t
    new.name = pic_name


# slides of the source, 0-based: delete the eye-test story (3) and the room's round (7)
drop(prs, 7)
drop(prs, 3)
S = list(prs.slides)   # now 16 slides: 0 title, 1 divider, 2 map, 3 road, 4 container, 5 re-entry, 6 teaching, 7 steps,
                       # 8 bridge->readings, 9 pairs->images, 10 tell->observe/apply, 11 merge->tell, 12 take-home 1,
                       # 13 take-home 2, 14 feedback, 15 closing

# 1 divider
set_lines(shape(S[1], "TextBox 3"), [
    "EVENING 9", "Heart Bible Study — Hearing God Together",
    "PROAPT in its group form: one passage, three readings, the images, same and different — the first evening back"])
notes(S[1], "E9 · pre-session · DIVIDER\nOn screen through dinner and as the circle forms. The first table together since the break: greet every family at the door, and welcome every walker home.")

# 2 the map
set_lines(shape(S[2], "TextBox 4"), [
    "Evening 9 closes the third box — Connect with God — hearing him together, on the first evening back. Each connection makes the next one real (Matt. 22:37–40)."])
notes(S[2], "E9 · WELCOME · LEAD: CONTAINER HOLDER · GROUNDING — every session opens on this map\nBEATS:\n1. Locate tonight on the map, plainly: the last evening of Connect with God, and the first evening back after the break.\n2. Nothing new tonight: PROAPT from Evening 6, the Tell from every evening, put together into one practice we do as a room.\n3. This is also the 'where we are on the map' minute the welcome owes any newcomer.\nCUES: Two minutes at most; then tonight's road.")

# 3 tonight's road
set_lines(shape(S[3], "TextBox 2"), ["Evening 9 — Tonight’s Road"])
set_lines(shape(S[3], "TextBox 3"), [
    "1   Welcome home and centering", "2   The welcome-back round — one thing from the break",
    "3   From my hearing to our hearing", "4   Pray, and three readings of 1 Samuel 3:1–10",
    "5   Images — what came as you listened", "6   Same and different",
    "7   Observe, Apply, Pray again", "8   The Tell — to the whole circle",
    "9   Homework and the Leader Feedback Round", "10   Closing container"])
notes(S[3], "E9 · 7:00–8:30 · LEAD: BOTH LEADERS\nBEATS:\n1. Walk the road briefly: a short welcome home, then one passage heard together.\n2. Name the leading pair and the handoffs: the content presenter leads the study with the Reading Card; the container holder keeps the clock, watches the room and leads the Tell.\n3. Two named adults hold safety tonight, whoever is leading.\nCUES: Thirty seconds; the road, not a preview of the content.")

# 4 opening container: text unchanged
notes(S[4], "E9 · 7:00–7:08 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Aaronic blessing first.\n2. Rebuild the container slowly: it has been weeks. Safe, present, clear, intentional, said aloud.\n3. Full eight steps, normal pace; nothing changes because it is the first night back.\nCUES: The one-word check-in gets one unhurried breath after each word; no commentary.")

# 5 welcome back
set_lines(shape(S[5], "TextBox 2"), ["Welcome Home"])
set_lines(shape(S[5], "TextBox 4"), [
    "•  The first evening back — the container re-held slowly after the break",
    "•  One sentence each: “One thing from the break I want this room to know.”",
    "–  “It was hard” is a complete answer; pass is a complete answer",
    "•  A parent starts the round — pass-anytime holds",
    "•  What held over the break is read at The Return, in two weeks — not tonight"])
notes(S[5], "E9 · 7:08–7:18 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One sentence each, the arranged parent first: one thing from the break I want this room to know.\n2. Receive each with 'We hear that'; no follow-up questions.\n3. If someone starts reading their practices, smile and park it: 'Save that for The Return.'\nCUES: Never cold-call a teen. Ten minutes, not more.\nGUARD: Anything heavy from the break goes to a safety adult after the close, not into the circle.")

# 6 teaching
set_lines(shape(S[6], "TextBox 2"), ["From My Hearing to Our Hearing"])
set_lines(shape(S[6], "TextBox 4"), [
    "•  PROAPT is how I hear. Heart Bible Study is how we hear, together",
    "•  God has often spoken to his people gathered: the Law read clearly, its sense given (Neh 8:8); the church at Antioch, worshiping (Acts 13:2)",
    "•  The question that makes it work: what did you hear that was the same, and what was different?",
    "•  The Spirit often shows a group what no one heard alone",
    "•  From being taught to teaching others (Heb 5:12): a teen leads the room’s hearing tonight"])
set_lines(shape(S[6], "TextBox 6"), [
    "NEHEMIAH 8:8",
    "“They read from the book, from the Law of God, clearly, and they gave the sense, so that the people understood the reading.”"])
notes(S[6], "E9 · 7:18–7:25 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Read Nehemiah 8:8 aloud, slowly, from the physical Bible.\n2. The one idea: PROAPT is how I hear; Heart Bible Study is how we hear, together.\n3. The question that makes it work: same and different. Say it now, so the room is listening for it.\n4. Name the Hebrews 5 step: tonight a teen leads the room's hearing.\nCUES: Seven minutes; teach the shape, not the content of the passage.")

# 7 the steps
set_lines(shape(S[7], "TextBox 2"), ["Heart Bible Study — the Steps"])
set_lines(shape(S[7], "TextBox 4"), [
    "1   Pray — “Holy Spirit, you are welcome here. Speak. We are listening.”",
    "2   Read — three times, slowly; eyes closed except the reader’s",
    "3   Images — what pictures, words or feelings came as you listened?",
    "4   Same and different — what did others hear that you heard too? What did only you hear?",
    "5   Observe — what the passage actually says: who, what, where",
    "6   Apply — what is the Spirit highlighting for me, tonight? One thing",
    "7   Pray again — what I heard, what I’m willing to do, what I’m struggling with",
    "8   Tell — one sentence to the circle"])
notes(S[7], "E9 · 7:25–7:28 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Walk the eight steps in one breath each; the room already knows six of them from PROAPT.\n2. Then pray, briefly (Reading Card): the Spirit invited.\nCUES: Leave this slide up while you pray; it is the room's map for the next forty minutes.")

# 8 three readings
set_lines(shape(S[8], "TextBox 2"), ["1 Samuel 3:1–10 — Three Readings"])
set_lines(shape(S[8], "TextBox 4"), [
    "•  Three readers: a teen, a parent, a teen — the same passage, the same translation",
    "•  Eyes closed except the reader’s; a short silence between readings",
    "•  Don’t analyze yet — receive it",
    "•  “Speak, for your servant hears” (1 Sam 3:10) — Samuel was a boy, and an older man helped him recognize the voice"])
notes(S[8], "E9 · 7:28–7:38 · LEAD: CONTENT PRESENTER · THREE READERS\nBEATS:\n1. Readers arranged at the planning lab; Bibles open at 1 Samuel 3 before the evening starts.\n2. Thirty seconds of silence between readings. Do not fill it.\n3. Name the picture in the passage only after the readings: a boy, an older man, and a voice.\nCUES: Two words per second. The third reader a little slower again.")

# 9 images and same/different
set_lines(shape(S[9], "TextBox 2"), ["Images, and Same and Different"])
set_lines(shape(S[9], "TextBox 4"), [
    "1   What pictures, words or feelings came as you listened? One at a time, briefly",
    "2   Not a picture person? Another door: a sound, a gesture, a shape, one word",
    "3   Each one received with “We hear that” — no commentary",
    "4   Same and different: what did someone else hear that you heard too? What did only you hear?",
    "•  Watch for what none of us heard alone — often the Spirit’s gift to the group"])
notes(S[9], "E9 · 7:38–7:55 · LEAD: CONTENT PRESENTER · CONTAINER HOLDER WATCHING THE ROOM\nBEATS:\n1. Images, 7:38–7:48: a parent starts; one at a time; 'We hear that.'\n2. Same and different, 7:48–7:55: first what was shared, then what was only yours.\n3. If something none of us heard alone appears, name it gently and move on.\nCUES: If the room runs long, this round shortens first.\nGUARD: Interpreting someone else's image is the commonest drift; stop it kindly.")

# 10 observe, apply, pray again
set_lines(shape(S[10], "TextBox 2"), ["Observe, Apply, Pray Again"])
set_lines(shape(S[10], "TextBox 4"), [
    "•  Observe — what the passage actually says: who, what, where, straight off the page",
    "•  Apply — “What is the Spirit highlighting in this passage for me, tonight?” One specific thing, written in your journal",
    "•  Test it: does it agree with Scripture? Does it sound like the Lord, or like accusation?",
    "•  Pray again, in silence — what I heard, what I’m willing to do, what I’m struggling to be willing to do"])
notes(S[10], "E9 · 7:55–8:07 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Observe, short: a few answers, straight off the page.\n2. Apply: one specific thing, written. Then the test, said aloud (the How Did You Know? card).\n3. Pray again in silence, four minutes, with the spoken frame; close with one sentence.\nGUARD: If an Apply goes heavy, honor it in a sentence; it goes to a safety adult after the close. This is a Bible study, not inner work.")

# 11 the tell
set_lines(shape(S[11], "TextBox 2"), ["The Tell — to the Whole Circle"])
set_lines(shape(S[11], "TextBox 4"), [
    "•  One sentence each: “What I heard is ___. What I will do with it is ___.”",
    "•  A parent opens; pass anytime",
    "•  Received as witness: “We hear that.” No commentary",
    "•  Heard something you don’t yet trust? Take Any Doubts? home with it",
    "•  Something heavy? Honor it briefly; it goes to a safety adult after the close",
    "•  Telling is always invited, never required"])
notes(S[11], "E9 · 8:07–8:14 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One sentence each, the arranged parent first.\n2. 'We hear that' is the whole response.\n3. Close the round with a brief word of what the Lord did in the room's hearing tonight; save it for the closing if time is short.\nCUES: Never cold-call a teen; a pass is a full participation.")

# 12, 13 take-home (pictures of the new sheet)
set_lines(shape(S[12], "TextBox 2"), ["The Take-Home Sheet — the Daily Rhythm"])
swap_picture(S[12], "Picture 3", IMG1)
notes(S[12], "E9 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n2. The standing rhythm first: the morning question and the evening line, one box per day.\n3. Week one: daily PROAPT, with tonight's Tell sentence in view; name a time of day aloud.")
set_lines(shape(S[13], "TextBox 2"), ["The Take-Home Sheet — Week Two"])
swap_picture(S[13], "Picture 3", IMG2)
notes(S[13], "E9 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. Week two: one Heart Bible Study at your own table, a teen leading, on 1 Samuel 3:11–21 or a passage you choose. The second page has the steps.\n2. Check-in partners named aloud before leaving this slide.\n3. Two sentences of preparation for The Return: what you kept over the break, and what you most want to keep.")

# 14 leader feedback round
notes(S[14], "E9 · 8:20–8:24 · LEAD: BOTH LEADERS\nBEATS:\n1. Same round every week, leader first: what went well tonight, what I'd do differently.\n2. Then the room, the same two questions about the leaders.\n3. When a teenager leads, the room's answers are kind and brief; anything harder waits for the planning lab.\nCUES: 'Thank you' is the whole response.")

# 15 closing
notes(S[15], "E9 · 8:24–8:30 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Closing protocol, unhurried: stand; one-word landing; the one thing taken from tonight; the one practice.\n2. A brief word of what the Lord did in the room's hearing tonight, if it was not said at the Tell.\n3. Name the road: in two weeks, The Return.\n4. Aaronic blessing.\nBLESSINGS: eyes on the person, not the screen; say what is on your heart for them, specific and short.")

# final: the movement divider, copied from Evening 5's last slide (no pictures)
from pptx.opc.packuri import PackURI
for stage in ("tmp", "final"):
    for i, s in enumerate(prs.slides, 1):
        s.part.partname = PackURI("/ppt/slides/%sslide%d.xml" % ("x" if stage == "tmp" else "", i))
        if s.has_notes_slide:
            s.notes_slide.part.partname = PackURI("/ppt/notesSlides/%snotesSlide%d.xml" % ("x" if stage == "tmp" else "", i))
div = Presentation(DIV).slides[-1]
new = prs.slides.add_slide(prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1])
for sh in list(new.shapes):
    sh._element.getparent().remove(sh._element)
for sh in div.shapes:
    new.shapes._spTree.append(copy.deepcopy(sh._element))
set_lines(shape(new, "TextBox 2"), [
    "The Third Movement", "Mission & Rhythm",
    "Evenings 10 · 11 · 12 · 13 · 14 · 15 · 16 · 17  —  eight evenings, every two weeks · the Return, Doing the Word, Mission, Serving Together, the Rhythm, Family Night, Carrying the Word, the Float"])
ns = new.notes_slide
if ns.notes_text_frame is None:
    body = next(sh for sh in S[15].notes_slide.placeholders if sh.placeholder_format.type == 2)
    ns.shapes._spTree.append(copy.deepcopy(body._element))
ns.notes_text_frame.text = "MOVEMENT 3 · pre-session · DIVIDER\nOn screen as families arrive at The Return. Greet warmly at the door."

# corner pages H1, H2, ...
for i, s in enumerate(prs.slides, 1):
    sn = next(sh for sh in s.shapes if sh.name == "SlideNum")
    runs = sn.text_frame.paragraphs[0].runs
    runs[0].text = "H%d" % i
    for r in runs[1:]: r.text = ""
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
