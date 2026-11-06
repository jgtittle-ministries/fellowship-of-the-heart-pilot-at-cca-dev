# Evening 11 (Doing the Word) deck, from the Evening 9 deck (file key 11a). Corner pages D1, D2, ...
# usage: python build-evening-11-deck.py <take-home page 1 png> <take-home page 2 png> <scratch dir>
# The pngs are 150-dpi renders of "FotH Pilot Session 12a Homework Handout DRAFT v1.docx".
# Take-home slides: crop one part of the sheet per slide and fill the picture area (lesson from Evening 9, 6 Nov 2026).
import copy, re, sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
SRC = B + r"\FotH Evening Session 11a Slides DRAFT v1.pptx"
OUT = B + r"\FotH Evening Session 12a Slides DRAFT v1.pptx"
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


AREA_T, AREA_H, AREA_W = 1463040, 4892040, 10332720   # the picture area of the earlier take-home slides


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


# the Evening 9 deck, 0-based: 0 title, 1 divider, 2 map, 3 road, 4 container, 5 welcome home, 6 teaching, 7 steps,
# 8 readings, 9 images, 10 observe/apply, 11 tell, 12 take-home 1, 13 take-home 2, 14 feedback, 15 closing,
# 16 movement divider. Evening 11 sits inside the third movement, so the movement divider goes.
drop(prs, 16)
S = list(prs.slides)

# 1 divider
set_lines(shape(S[1], "TextBox 3"), [
    "EVENING 11", "Doing the Word",
    "The obey step: going back to what we heard, and doing one small thing — between hearing and being sent"])
set_lines(shape(S[1], "TextBox 4"), ["Quarter 3: Mission & Rhythm"])
notes(S[1], "E11 · pre-session · DIVIDER\nOn screen through dinner and as the circle forms. Journals out: everyone needs their Tell sentences from Evenings 6 to 9 tonight.")

# 2 the map
set_lines(shape(S[2], "TextBox 4"), [
    "Evening 11 stands between hearing and being sent — we have heard (Evenings 6–9), we have come back (Evening 10); now we do one thing. Each connection makes the next one real (Matt. 22:37–40)."])
notes(S[2], "E11 · WELCOME · LEAD: CONTAINER HOLDER · GROUNDING — every session opens on this map\nBEATS:\n1. Locate tonight on the map: between Connect with God, behind us, and Connect with Mission, at the next evening.\n2. Hearing has had four evenings. Obeying has had a step, Pray again, but no evening of its own. Tonight gives it one.\n3. Tonight's obedience is small and personal. Mission is the larger one, and at Evening 13 the whole room obeys together.\nCUES: Two minutes at most; then tonight's road.")

# 3 tonight's road
set_lines(shape(S[3], "TextBox 2"), ["Evening 11 — Tonight’s Road"])
set_lines(shape(S[3], "TextBox 3"), [
    "1   Welcome and centering", "2   The check-in circle — two weeks since The Return",
    "3   The rock and the sand, the mirror", "4   The read-back — your Tell sentences, Evenings 6 to 9",
    "5   Choose one, and make it small", "6   Pairs — two questions, and prayer",
    "7   The merge — to the circle", "8   Homework and the Leader Feedback Round",
    "9   Closing container"])
notes(S[3], "E11 · 7:00–8:30 · LEAD: BOTH LEADERS\nBEATS:\n1. Walk the road briefly: a check-in, one short teaching, then quiet with your own journal, and one sentence each.\n2. Name the leading pair and the handoffs: the content presenter leads the teaching, the read-back and the pairs; the container holder keeps the clock, watches the room and leads the check-in and the merge.\n3. Two named adults hold safety tonight, whoever is leading.\nCUES: Thirty seconds; the road, not a preview of the content.")

# 4 opening container: text unchanged
notes(S[4], "E11 · 7:00–7:08 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Aaronic blessing first.\n2. Full eight steps, normal pace. Safe, present, clear, intentional, said aloud.\nCUES: The one-word check-in gets one unhurried breath after each word; no commentary.")

# 5 check-in circle
set_lines(shape(S[5], "TextBox 2"), ["The Check-In Circle"])
set_lines(shape(S[5], "TextBox 4"), [
    "•  Two weeks since The Return: the one practice you restarted — how did it go?",
    "•  The week-one check-ins: did your partner reach you? Did you reach them?",
    "–  A thin week is an honest answer; pass is a complete answer",
    "•  A parent starts the round — pass-anytime holds",
    "•  Received with “We hear that” — no fixing, no follow-up"])
notes(S[5], "E11 · 7:08–7:22 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One or two sentences each, the arranged parent first: the one practice restarted at The Return, and how it went.\n2. Then the week-one check-ins: did the partners connect? Thank the pairs who did, by name.\n3. Receive each with 'We hear that'; no advice.\nCUES: Never cold-call a teen. Fourteen minutes, not more.\nGUARD: Anything heavy goes to a safety adult after the close, not into the circle.")

# 6 teaching
set_lines(shape(S[6], "TextBox 2"), ["The Rock and the Sand, the Mirror"])
set_lines(shape(S[6], "TextBox 4"), [
    "•  Two builders, two houses, one storm. The difference was not the hearing; both heard. One did what he heard (Luke 6:46–49)",
    "•  Hearing without doing is a glance in the mirror: you walk away and forget your own face (James 1:23–24)",
    "•  The one who does it “will be blessed in his doing” (James 1:25)",
    "•  Since Evening 6 we have learned to hear. Tonight we ask the question the whole journey is about: did I do it?",
    "•  Hearing that is not done does not hold"])
set_lines(shape(S[6], "TextBox 6"), [
    "JAMES 1:22",
    "“But be doers of the word, and not hearers only, deceiving yourselves.”"])
notes(S[6], "E11 · 7:22–7:32 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Read Luke 6:46–49 aloud, slowly, from the physical Bible. Then James 1:22–25.\n2. The one idea: both builders heard. Only one did. The storm showed the difference.\n3. Name the mirror honestly: every one of us has heard something and walked away from it. Leaders first: say one of yours, briefly.\n4. Turn to the journals: 'Tonight we go back to what we heard.'\nCUES: Ten minutes; the leader's own example does more than any explanation.")

# 7 the read-back
set_lines(shape(S[7], "TextBox 2"), ["The Read-Back"])
set_lines(shape(S[7], "TextBox 4"), [
    "1   Open your journal to your Tell sentences — Evenings 6, 7, 8 and 9",
    "2   Read them slowly, alone, in silence",
    "3   Mark the ones you have already done — give thanks for them",
    "4   Mark the ones you heard and have not yet done",
    "5   Ask: “Lord, which one is for now?”",
    "•  No journal tonight? Write what you remember hearing; that counts"])
notes(S[7], "E11 · 7:32–7:40 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Eight minutes of real quiet. Do not fill it.\n2. Spare paper ready for anyone without a journal.\n3. At the end, one sentence: 'If more than one stands out, choose the smallest.'\nCUES: The container holder watches the room; a teen who finds nothing gets a quiet word later, not a spotlight now.")

# 8 the sentence
set_lines(shape(S[8], "TextBox 2"), ["Choose One, and Make It Small"])
set_lines(shape(S[8], "TextBox 4"), [
    "•  “I heard ________ (at Evening ___). By ________ I will ________.”",
    "•  Small is the point. Not “be more patient with my brother” but “on Thursday, when he takes my charger, I will ask instead of yelling”",
    "•  Not “pray more” but “five minutes before school on Monday, Wednesday and Friday”",
    "•  A step you can picture yourself doing is a step you can do"])
notes(S[8], "E11 · 7:40–7:48 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Walk the sentence once, slowly; everyone writes theirs on the take-home, at the top.\n2. Give both examples; the room will laugh at the charger one, and remember it.\n3. Then the test (next slide) before anyone takes it to their pair.\nCUES: If someone can't find one, 'I'm still listening' is an honest sentence.")

# 9 pairs
set_lines(shape(S[9], "TextBox 2"), ["Pairs — Two Questions, and Prayer"])
set_lines(shape(S[9], "TextBox 4"), [
    "1   A parent with their own teen, by default; the parent goes first",
    "2   Say your sentence. Your partner asks: Is it small enough to do in two weeks?",
    "3   And: Does it involve another person? Then talk it over with a parent or another adult first",
    "4   Switch at 7:54",
    "5   Pray for each other, by name, from 8:00",
    "•  The Pair Card has the steps; the container holder keeps the clock"])
notes(S[9], "E11 · 7:48–8:06 · LEAD: CONTENT PRESENTER · CONTAINER HOLDER WATCHING THE ROOM\nBEATS:\n1. Pair Cards out; pairs spread through the room.\n2. The container holder calls the switch at 7:54 and the prayer at 8:00, and the return at 8:06.\n3. Walk the room; listen for steps that are too big, and help shrink them.\nGUARD: A step involving another person (an apology, making something right) is talked over with an adult before it is taken. A step can be private from the room; it is never hidden from a teen's parents.")

# 10 the test
set_lines(shape(S[10], "TextBox 2"), ["The Test, Before the Doing"])
set_lines(shape(S[10], "TextBox 4"), [
    "•  Scripture first — does it line up with what God has already said?",
    "•  Peace — is there peace, even if the step is hard? Does it sound like the Lord’s conviction, or like accusation?",
    "•  Company — what does your partner, who knows you and knows God, see?",
    "•  Nothing that fails the checks gets done (1 John 4:1). Choose again, or say “I’m still listening”"])
notes(S[10], "E11 · 7:44–7:48 · LEAD: CONTENT PRESENTER\nBEATS:\n1. Three of the How Did You Know? checks from Evening 7, said aloud before the pairs.\n2. Name accusation plainly: a step that sounds like self-punishment ('I have to stop being so stupid') fails the Peace check.\n3. Then send the room to pairs.\nCUES: This slide comes up inside the 'choose one' block, before the pairs.")

# 11 the merge
set_lines(shape(S[11], "TextBox 2"), ["The Merge — to the Circle"])
set_lines(shape(S[11], "TextBox 4"), [
    "•  One sentence each: “By ___ I will ___.” Or simply: “I have one.”",
    "•  A parent begins; pass anytime",
    "•  Received as witness: “We hear that.” No commentary",
    "•  Some obediences are between a person and God, and that is fine",
    "•  A small step done is worth more than a big one announced"])
notes(S[11], "E11 · 8:06–8:14 · LEAD: CONTAINER HOLDER\nBEATS:\n1. One sentence each, the arranged parent first.\n2. 'I have one' is a full answer; do not ask what it is.\n3. Close the round: 'At the next evening, we hear what happened.'\nCUES: Never cold-call a teen; no comparing, no performing.")

# 12, 13 take-home: one part of the sheet per slide, full size
set_lines(shape(S[12], "TextBox 2"), ["The Take-Home Sheet — Your Sentence, and Week One"])
place_crop(S[12], IMG1, (100, 745, 1175, 1172), "e11-takehome-sentence")
notes(S[12], "E11 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n2. Your sentence at the top, in your own words. The standing rhythm carries on at the head of the sheet, as always.\n3. Week one: do it, on the day you named. Daily PROAPT carries on underneath.\n4. Check-in partners named aloud: at the end of week one, two questions, 'Did you do it yet? What's in the way?'")
set_lines(shape(S[13], "TextBox 2"), ["The Take-Home Sheet — Week Two"])
place_crop(S[13], IMG2, (100, 120, 1175, 520), "e11-takehome-week-two")
notes(S[13], "E11 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n1. Week two: two lines in the journal, what I did and what happened.\n2. Didn't do it yet? Do it this week, or write what got in the way. Honest data, not failure.\n3. Bring one sentence back to the next evening's check-in: what I did, and what happened.")

# 14 leader feedback round
notes(S[14], "E11 · 8:20–8:24 · LEAD: BOTH LEADERS\nBEATS:\n1. Same round every week, leader first: what went well tonight, what I'd do differently.\n2. Then the room, the same two questions about the leaders.\nCUES: 'Thank you' is the whole response.")

# 15 closing
notes(S[15], "E11 · 8:24–8:30 · LEAD: CONTAINER HOLDER\nBEATS:\n1. Closing protocol, unhurried: stand; one-word landing; the one thing taken from tonight; the one practice.\n2. Name the road: at the next evening, What Was Prepared for You, the check-in hears what happened.\n3. Aaronic blessing.\nBLESSINGS: eyes on the person, not the screen; say what is on your heart for them, specific and short.")

# order: the test (10) belongs before the pairs (9)
sld = prs.slides._sldIdLst
ids = list(sld)
sld.remove(ids[10]); sld.insert(9, ids[10])

# corner pages D1, D2, ...
for i, s in enumerate(prs.slides, 1):
    sn = next(sh for sh in s.shapes if sh.name == "SlideNum")
    runs = sn.text_frame.paragraphs[0].runs
    runs[0].text = "D%d" % i
    for r in runs[1:]: r.text = ""
prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
