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
       r"\Fellowship of the Heart\Evenings at Home")

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

for path in sorted(glob.glob(SRC + "/handouts/*.docx")):
    base = os.path.basename(path)
    m = re.match(r"FotH Pilot Session (\d+) Homework Handout DRAFT v1\.docx$", base)
    if m:
        dst = os.path.join(EAH, "Take-Home Sheets", "Session %s \u2014 Take-Home.docx" % m.group(1))
    elif "Template" in base:
        dst = os.path.join(EAH, "Take-Home Sheets", "Take-Home Template.docx")
    else:
        continue
    shutil.copy2(path, dst)
    count += 1

print("synced %d artifacts to Evenings at Home" % count)
