# Evening 9 deck: enlarge the take-home pictures (H13, H14) to match earlier decks.
# H13 = the standing practice only; H14 = the rest of the sheet (week one, check-in, week two, preparation).
# Usage: python fix-evening-09-takehome.py <scratch dir>
import io, sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\jgtit\claude\_work\fellowship-of-the-heart-pilot-at-cca-dev\_implementation-notes\evening-series"
DECK = B + r"\FotH Evening Session 11a Slides DRAFT v1.pptx"
TMP = sys.argv[1]

prs = Presentation(DECK)
S = list(prs.slides)


def pic(s):
    return next(sh for sh in s.shapes if sh.shape_type == 13 and sh.name == "Picture 3")


p1 = Image.open(io.BytesIO(pic(S[12]).image.blob)).convert("RGB")
p2 = Image.open(io.BytesIO(pic(S[13]).image.blob)).convert("RGB")
W = max(p1.width, p2.width)

top = p1.crop((0, 0, p1.width, 592))                      # title through "invitation to return"
wk1 = p1.crop((0, 600, p1.width, 858))                    # 1. the homework practice, week one
wk2 = p2.crop((0, 0, p2.width, 296))                      # 3. the homework practice, week two
gap = 24
rest = Image.new("RGB", (W, wk1.height + gap + wk2.height), "white")
rest.paste(wk1, (0, 0)); rest.paste(wk2, (0, wk1.height + gap))

# picture area used by earlier decks: top 1463040, max height 4892040, max width 10332720, centered
AREA_T, AREA_H, AREA_W = 1463040, 4892040, 10332720


def place(s, img, name):
    old = pic(s)
    old._element.getparent().remove(old._element)
    path = "%s\\%s.png" % (TMP, name)
    img.save(path)
    r = min(AREA_W / img.width, AREA_H / img.height)
    w, h = int(img.width * r), int(img.height * r)
    new = s.shapes.add_picture(path, Emu((prs.slide_width - w) // 2), Emu(AREA_T), Emu(w), Emu(h))
    new.name = "Picture 3"
    print(name, img.size, "->", round(w / 914400, 2), "x", round(h / 914400, 2), "in")


place(S[12], top, "e9-takehome-rhythm")
place(S[13], rest, "e9-takehome-weeks")

S[13].shapes  # retitle H14 and move the week-one beat there
from pptx.text.text import _Paragraph
t = next(sh for sh in S[13].shapes if sh.name == "TextBox 2")
r = t.text_frame.paragraphs[0].runs
r[0].text = "The Take-Home Sheet — the Two Weeks"
for x in r[1:]: x.text = ""
S[12].notes_slide.notes_text_frame.text = (
    "E9 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n"
    "1. The sheet on the screen is the sheet in their hands: walk it, don't read it.\n"
    "2. The standing rhythm: the morning question and the evening line, one box per day, both weeks.")
S[13].notes_slide.notes_text_frame.text = (
    "E9 · COMMISSIONING · LEAD: CONTENT PRESENTER\nBEATS:\n"
    "1. Week one: daily PROAPT, with tonight's Tell sentence in view; name a time of day aloud.\n"
    "2. Week two: one Heart Bible Study at your own table, a teen leading, on 1 Samuel 3:11–21 or a passage you choose. The second page has the steps.\n"
    "3. Check-in partners named aloud before leaving this slide.\n"
    "4. Two sentences of preparation for The Return: what you kept over the break, and what you most want to keep.")
prs.save(DECK)
print("saved")
