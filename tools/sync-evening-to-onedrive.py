# -*- coding: utf-8 -*-
"""Sync evening-series artifacts to John's OneDrive per the 2026-09-16 filing
convention (see _implementation-notes/evening-series/onedrive-sync-map.md).

Run from the repo root:  python tools/sync-evening-to-onedrive.py
Copies every deck, run sheet, take-home sheet, and leader-notes doc to the
new homes with the short names. Idempotent; overwrites destinations.
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
     "Slides", "Session {} \u2014 Slides.pptx"),
    (r"FotH Pilot Session (.+?) (?:Combined )?Evening Run Sheet DRAFT v1\.docx$",
     "Run Sheets", "Session {} \u2014 Run Sheet.docx"),
    (r"FotH Evening Session (.+?) Leader Notes DRAFT v1\.docx$",
     "Leader Notes", "Session {} \u2014 Leader Notes.docx"),
]

count = 0
for path in sorted(glob.glob(SRC + "/*")):
    base = os.path.basename(path)
    for pat, sub, fmt in RULES:
        m = re.match(pat, base)
        if m:
            key = m.group(1)
            if "Combined" in base and "Combined" not in key:
                key += " Combined"
            dst = os.path.join(EAH, sub, fmt.format(key))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(path, dst)
            count += 1
            break

for path in sorted(glob.glob(SRC + "/handouts/*.docx") + glob.glob(SRC + "/*Homework Handout Template*.docx")):
    base = os.path.basename(path)
    m = re.match(r"FotH Pilot Session (\d+) Homework Handout DRAFT v1\.docx$", base)
    m2 = re.match(r"FotH Pilot Session (\d+) Road So Far Handout DRAFT v1\.docx$", base)
    m3 = re.match(r"FotH Pilot Session (\d+) PROAPT Handout DRAFT v1\.docx$", base)
    m4 = re.match(r"FotH Pilot Session (\d+) Breakout Card DRAFT v1\.docx$", base)
    if m4:
        dst = os.path.join(EAH, "Leader Notes", "Session %s — Breakout Card.docx" % m4.group(1))
    elif m:
        dst = os.path.join(EAH, "Take-Home Sheets", "Session %s \u2014 Take-Home.docx" % m.group(1))
    elif m2:
        dst = os.path.join(EAH, "Take-Home Sheets", "Session %s \u2014 The Road So Far.docx" % m2.group(1))
    elif m3:
        dst = os.path.join(EAH, "Take-Home Sheets", "Session %s \u2014 PROAPT, What Each Step Is For.docx" % m3.group(1))
    elif "Template" in base:
        dst = os.path.join(EAH, "Take-Home Sheets", "Take-Home Template.docx")
    else:
        continue
    shutil.copy2(path, dst)
    count += 1

print("synced %d artifacts to Evening, two weeks, pilot" % count)
