# -*- coding: utf-8 -*-
"""Publish each evening's current materials on the site, one stop per evening.

Run from the repo root:  python tools/build-evening-materials.py
Copies the decks, run sheets, leader notes, take-home sheets and cards for
every evening that has a page into docs/evening/materials/ under short web
names (evening-07-slides.pptx ...), and writes a "## Materials" section into
each evening page, just before "## The evening". Idempotent: rerun after any
material changes, then mirror docs/evening to prod.

The evening-to-file tables match tools/sync-evening-to-onedrive.py. Add an
evening to PAGES (and its keys to WALK / HANDOUT) when its page goes up.
"""
import glob
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = "_implementation-notes/evening-series"
DOCS = "docs/evening"
OUT = DOCS + "/materials"

PAGES = {1: "session-01-welcome-to-the-journey.md", 2: "session-02-the-soil-of-your-heart.md",
         3: "session-03-04-telling-your-story.md", 4: "session-05-knowing-and-being-known.md",
         5: "session-06-safe-and-brave-together.md", 6: "session-07-08-hearing-god-in-scripture.md",
         7: "session-09-10-the-garden-of-your-heart.md", 8: "session-11-any-doubts.md",
         9: "session-11a-heart-bible-study.md"}
WALK = {"1": 1, "2": 2, "3-4 Combined": 3, "5": 4, "6": 5, "7-8 Combined": 6, "9-10 Combined": 7, "11": 8, "11a": 9}
HANDOUT = {"1": 1, "2": 2, "3": 3, "5": 4, "6": 5, "7": 6, "7-8": 6, "9": 7, "9-10": 7, "11": 8, "11a": 9}

# kind: (label, what it is for, "room" = goes home with everyone, "leads" = for the two leads)
KINDS = {
    "take-home": ("Take-home sheet", "handed out at the close; the practice until the next evening", "room"),
    "practices-so-far-card": ("The Practices So Far", "every practice walked so far, to choose from", "room"),
    "how-did-you-know-card": ("How Did You Know? card", "the checks for testing what you heard", "room"),
    "road-so-far-handout": ("The Road So Far", "the first movement on one page", "room"),
    "proapt-handout": ("PROAPT — what each step is for", "the scripture practice, step by step", "room"),
    "heart-bible-study-handout": ("Heart Bible Study — what each step is for", "the group practice, step by step, for the family table", "room"),
    "slides": ("Slides", "the room screen, with the leader's notes under each slide", "leads"),
    "run-sheet": ("Run sheet", "the clock: each block, its time, and who leads it", "leads"),
    "leader-notes": ("Leader notes", "what to say and watch for, slide by slide", "leads"),
    "reading-card": ("Reading card", "the senior reader's script, with the pauses", "leads"),
    "pair-card": ("Pair card", "the steps the pairs follow", "leads"),
    "breakout-card": ("Breakout card", "the small-group steps", "leads"),
}
ORDER = list(KINDS)


def collect():
    """Return {evening: [(kind, source path)]} for every evening with a page."""
    found = {}
    for p in glob.glob(SRC + "/*.pptx") + glob.glob(SRC + "/*.docx"):
        b = os.path.basename(p)
        for pat, kind in [(r"FotH Evening Session (.+?) Slides DRAFT v1\.pptx$", "slides"),
                          (r"FotH Pilot Session (.+?) Evening Run Sheet DRAFT v1\.docx$", "run-sheet"),
                          (r"FotH Evening Session (.+?) Leader Notes DRAFT v1\.docx$", "leader-notes")]:
            m = re.match(pat, b)
            if m and m.group(1) in WALK:
                found.setdefault(WALK[m.group(1)], []).append((kind, p))
    for p in glob.glob(SRC + "/handouts/*.docx"):
        m = re.match(r"FotH Pilot Session ([\da-z-]+) (.+?) DRAFT v1\.docx$", os.path.basename(p))
        if m and m.group(1) in HANDOUT:
            kind = "take-home" if m.group(2) == "Homework Handout" else m.group(2).lower().replace(" ", "-")
            if kind in KINDS:
                found.setdefault(HANDOUT[m.group(1)], []).append((kind, p))
    return found


def section(n, items):
    """The Materials section for one evening's page."""
    def lines(group):
        out = []
        for kind, name in items:
            label, what, g = KINDS[kind]
            if g == group:
                fmt = "PowerPoint" if name.endswith(".pptx") else "Word"
                out.append("- [%s (%s)](materials/%s) — %s." % (label, fmt, name, what))
        return out
    s = ["## Materials", "",
         "Everything for this evening, current as of the last update. Download, open, print.", ""]
    room, leads = lines("room"), lines("leads")
    if room:
        s += ["**For everyone**", ""] + room + [""]
    s += ["**For the two leads**", ""] + leads + [""]
    return "\n".join(s) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    found = collect()
    keep = set()
    for n, page in sorted(PAGES.items()):
        items = []
        for kind, src in sorted(found.get(n, []), key=lambda x: ORDER.index(x[0])):
            name = "evening-%02d-%s%s" % (n, kind, os.path.splitext(src)[1])
            shutil.copy2(src, os.path.join(OUT, name))
            keep.add(name)
            items.append((kind, name))
        path = os.path.join(DOCS, page)
        text = open(path, encoding="utf-8").read()
        text = re.sub(r"## Materials\n.*?(?=\n## )\n?", "", text, flags=re.S)
        text = text.replace("\n## The evening\n", "\n" + section(n, items) + "\n## The evening\n", 1)
        open(path, "w", encoding="utf-8", newline="\n").write(text)
        print("Evening %d: %d files" % (n, len(items)))
    for f in os.listdir(OUT):
        if f not in keep:
            os.remove(os.path.join(OUT, f))
            print("removed stale", f)


main()
