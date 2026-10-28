# -*- coding: utf-8 -*-
"""Sync evening-series artifacts to John's OneDrive per the 2026-09-16 filing
convention (see _implementation-notes/evening-series/onedrive-sync-map.md).

Run from the repo root:  python tools/sync-evening-to-onedrive.py
Copies every deck, run sheet, take-home sheet, and leader-notes doc to the
new homes with the short names. Idempotent; overwrites destinations.

Since 13 October 2026 (John's word) the walk is numbered Evening 1-17: the
evening-form artifacts sync as "Evening N — ...", and the spare two-session
forms (the separate Sessions 3, 4, 7, 8, 9, 10, 14, 19 decks, run sheets and
take-homes) sync as "Session N — ..." under a "Spares — two-session forms"
subfolder. Repo filenames keep their session numbers.
"""
import glob
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"_implementation-notes/evening-series"
EAH = (r"C:\Users\jgtit\OneDrive\Documents\Intentional Journey of the Heart"
       r"\Fellowship of the Heart\Evening, two weeks, pilot")

RULES = [
    (r"FotH Evening Session (.+?) Slides DRAFT v1\.pptx$",
     "Slides", "{} \u2014 Slides.pptx"),
    (r"FotH Pilot Session (.+?) (?:Combined )?Evening Run Sheet DRAFT v1\.docx$",
     "Run Sheets", "{} \u2014 Run Sheet.docx"),
    (r"FotH Evening Session (.+?) Leader Notes DRAFT v1\.docx$",
     "Leader Notes", "{} \u2014 Leader Notes.docx"),
]

# the walk, Evening 1-17 (deck/run-sheet keys; combined forms carry "Combined")
WALK = {"1": 1, "2": 2, "3-4 Combined": 3, "5": 4, "6": 5, "7-8 Combined": 6, "9-10 Combined": 7,
        "11": 8, "12": 9, "13": 10, "15": 11, "16": 12, "17": 13, "18": 14, "20": 15, "21": 16, "22": 17}
# handouts and cards, by the session number in their filename
HANDOUT = {"1": 1, "2": 2, "3": 3, "5": 4, "6": 5, "7": 6, "7-8": 6, "9": 7, "9-10": 7, "11": 8, "12": 9,
           "13": 10, "15": 11, "16": 12, "17": 13, "18": 14, "20": 15, "21": 16, "22": 17}
SPARES = "Spares \u2014 two-session forms"


def place(folder, key, table, name):
    """Return the destination for an artifact: Evening N in the folder, or a spare."""
    if key in table:
        return os.path.join(EAH, folder, name.format("Evening %d" % table[key]))
    return os.path.join(EAH, folder, SPARES, name.format("Session %s" % key))

count = 0
skipped = []


def copy(path, dst):
    """Copy, but skip a destination that is open in Word or PowerPoint (reported at the end)."""
    global count
    try:
        shutil.copy2(path, dst)
        count += 1
    except PermissionError:
        skipped.append(dst)

for path in sorted(glob.glob(SRC + "/*")):
    base = os.path.basename(path)
    for pat, sub, fmt in RULES:
        m = re.match(pat, base)
        if m:
            key = m.group(1)
            if "Combined" in base and "Combined" not in key:
                key += " Combined"
            dst = place(sub, key, WALK, fmt)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            copy(path, dst)
            break

for path in sorted(glob.glob(SRC + "/handouts/*.docx") + glob.glob(SRC + "/*Homework Handout Template*.docx")):
    base = os.path.basename(path)
    m = re.match(r"FotH Pilot Session (\d+) Homework Handout DRAFT v1\.docx$", base)
    m2 = re.match(r"FotH Pilot Session (\d+) Road So Far Handout DRAFT v1\.docx$", base)
    m3 = re.match(r"FotH Pilot Session (\d+) PROAPT Handout DRAFT v1\.docx$", base)
    m4 = re.match(r"FotH Pilot Session ([\d-]+) (Breakout Card|Pair Card|Reading Card) DRAFT v1\.docx$", base)
    m5 = re.match(r"FotH Pilot Session (\d+) How Did You Know Card DRAFT v1\.docx$", base)
    m6 = re.match(r"FotH Pilot Session (\d+) Practices So Far Card DRAFT v1\.docx$", base)
    if m6:
        dst = place("Take-Home Sheets", m6.group(1), HANDOUT, "{} \u2014 The Practices So Far.docx")
    elif m5:
        dst = place("Take-Home Sheets", m5.group(1), HANDOUT, "{} \u2014 How Did You Know.docx")
    elif m4:
        dst = place("Leader Notes", m4.group(1), HANDOUT, "{} \u2014 %s.docx" % m4.group(2))
    elif m:
        dst = place("Take-Home Sheets", m.group(1), HANDOUT, "{} \u2014 Take-Home.docx")
    elif m2:
        dst = place("Take-Home Sheets", m2.group(1), HANDOUT, "{} \u2014 The Road So Far.docx")
    elif m3:
        dst = place("Take-Home Sheets", m3.group(1), HANDOUT, "{} \u2014 PROAPT, What Each Step Is For.docx")
    elif "Template" in base:
        dst = os.path.join(EAH, "Take-Home Sheets", "Take-Home Template.docx")
    else:
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    copy(path, dst)

print("synced %d artifacts to Evening, two weeks, pilot" % count)
for dst in skipped:
    print("SKIPPED (open in another program; close it and rerun):", dst)
