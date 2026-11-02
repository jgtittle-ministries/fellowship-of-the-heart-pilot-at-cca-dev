# -*- coding: utf-8 -*-
"""Word and PowerPoint downloads for the CCA pilot and Adult series, one stop per page.

Run from the repo root:  python tools/build-series-downloads.py
For each series folder (CCA: getting-started, going-deeper, going-out; Adult:
adult/getting-started, adult/going-deeper, adult/going-out; and shared):

- every lesson plan, handbook and card page gets a Word copy of itself in
  <series>/downloads/, and a "> **Downloads** · ..." line at the top of the page;
- CCA Getting Started weeks also get their own slides, split from the full deck;
- each series index gets a "## Downloads" section: the handbook, the whole
  series in one .zip, and (CCA Getting Started) the full deck.

Idempotent and deterministic (SOURCE_DATE_EPOCH, fixed zip times); only files
whose source changed are rewritten. Rerun after any page edit or a redeploy
from the Word sources, then mirror docs/ to prod. The evening series has its
own tool, tools/build-evening-materials.py.
"""
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys
import zipfile

import pptx
import pypandoc

sys.stdout.reconfigure(encoding="utf-8")
os.environ["SOURCE_DATE_EPOCH"] = "1767225600"

SITE = "https://fellowshipoftheheart.org/reader.html#"
DECK = "docs/getting-started/gs-session-slides-v1.5.pptx"
SERIES = {
    "getting-started": "Getting Started (CCA pilot)", "going-deeper": "Going Deeper (CCA pilot)",
    "going-out": "Going Out (CCA pilot)", "adult/getting-started": "Getting Started (Adult)",
    "adult/going-deeper": "Going Deeper (Adult)", "adult/going-out": "Going Out (Adult)",
    "shared": "Shared materials",
}
SKIP = {"index.md", "CHANGELOG.md", "cca-2026-27-calendar.md"}
# the CCA pilot's measurement instruments (John's word, 2 November 2026: instruments only — not the
# consent, covenant, crisis, referral, profile or interview pages), copied from the Word source of truth
CCA = (r"C:\Users\jgtit\OneDrive\Documents\Intentional Journey of the Heart\Fellowship of the Heart"
       r"\CCA Pilot\FotH Getting Started - ")
INSTRUMENTS = [
    ("Measurement Map 2026-27.docx", "instrument-measurement-map.docx",
     "The Measurement Map", "the year at a glance: what is measured, when, and the guards around it"),
    ("Pre-Series Survey (on each family's yes).docx", "instrument-pre-series-survey.docx",
     "The Pre-Series Survey", "the before, on each family's yes"),
    ("Quarterly Pulse - Quarter 1 (Week 6, H6.3).docx", "instrument-pulse-1.docx",
     "Quarterly Pulse 1", "Week 6, three questions"),
    ("Quarterly Pulse - Midpoint (Week 11, H11.4).docx", "instrument-pulse-2-midpoint.docx",
     "Quarterly Pulse 2, the Midpoint", "Week 11, three questions"),
    ("Quarterly Pulse - Pulse 3 (Week 16, H16.1).docx", "instrument-pulse-3.docx",
     "Quarterly Pulse 3", "Week 16, three questions"),
    ("Post-Series Survey (Week 20, H20.1).docx", "instrument-post-series-survey.docx",
     "The Post-Series Survey", "the after, Week 20"),
    ("Practice Check-Off Cards - Weeks 1-22.docx", "instrument-practice-check-off-cards.docx",
     "The Practice Check-Off Cards", "Weeks 1–22; they go home and are never collected"),
]
STAMP = "> **Downloads** · "
CACHE = "tools/.series-downloads-cache.json"

IMG = re.compile(r"^\s*!\[.*\]\(.*\)\s*$")
HR = re.compile(r"^\s*(-{3,}|\*{3,})\s*$")
ATTR = re.compile(r"\{:[^}]*\}")
LINK = re.compile(r"\]\((?!https?:|mailto:|#)([^)#\s]+\.md)(#[^)\s]*)?\)")


def to_word_md(md, page):
    """The page's markdown, made print-ready: no images or rules, admonitions as quotes, site links absolute."""
    base = os.path.dirname(page)
    out, quote = [], False
    for ln in md.replace("\r\n", "\n").split("\n"):
        if ln.startswith(STAMP) or IMG.match(ln) or HR.match(ln):
            continue
        m = re.match(r'^!!!\s+\w+(?:\s+"([^"]*)")?', ln)
        if m:
            out.append("> **%s**" % (m.group(1) or "Note"))
            out.append(">")
            quote = True
            continue
        if quote:
            if ln.startswith("    "):
                out.append("> " + ln[4:])
                continue
            if ln.strip() == "":
                out.append(">")
                continue
            quote = False
        out.append(ln)
    text = ATTR.sub("", "\n".join(out))

    def absol(m):
        target = os.path.normpath(os.path.join(base, m.group(1))).replace("\\", "/")
        return "](%s%s)" % (SITE, target.replace("/", "%2F"))
    return LINK.sub(absol, text)


def digest(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p if isinstance(p, bytes) else p.encode("utf-8"))
    return h.hexdigest()


def week_ranges():
    """{week number: [slide indexes]} from the WEEK N dividers; a quarter divider goes with the week after it."""
    deck = pptx.Presentation(DECK)
    starts = []
    for i, s in enumerate(deck.slides):
        t = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
        m = re.match(r"\s*WEEK (\d+)\b", t)
        if m:
            starts.append((int(m.group(1)), i))
    n = len(deck.slides)
    out = {}
    for k, (wk, i) in enumerate(starts):
        end = starts[k + 1][1] if k + 1 < len(starts) else n
        first = i
        prev = " ".join(sh.text_frame.text for sh in deck.slides[i - 1].shapes if sh.has_text_frame) if i else ""
        if re.match(r"\s*Quarter \d", prev):
            first = i - 1
        if k + 1 < len(starts):
            nxt = " ".join(sh.text_frame.text for sh in deck.slides[end - 1].shapes if sh.has_text_frame)
            if re.match(r"\s*Quarter \d", nxt):
                end -= 1
        out[wk] = list(range(first, end))
    if starts and starts[0][1] > 0:
        out[starts[0][0]] = list(range(0, starts[0][1])) + out[starts[0][0]]
    return out


def split_deck(keep, dst):
    deck = pptx.Presentation(DECK)
    ids = deck.slides._sldIdLst
    for i, sid in reversed(list(enumerate(list(ids)))):
        if i not in keep:
            deck.part.drop_rel(sid.rId)
            ids.remove(sid)
    deck.save(dst)


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    deck_hash = digest(open(DECK, "rb").read())
    weeks = week_ranges()
    for folder, label in SERIES.items():
        src = "docs/" + folder
        dl = src + "/downloads"
        os.makedirs(dl, exist_ok=True)
        keep, pages = set(), []
        for path in sorted(glob.glob(src + "/*.md")):
            name = os.path.basename(path)
            if name in SKIP:
                continue
            stem = name[:-3]
            page = "docs/%s/%s" % (folder, name)
            md = io.open(path, encoding="utf-8").read()
            body = to_word_md(md, page)
            docx_name = stem + ".docx"
            keep.add(docx_name)
            key = "%s/%s" % (folder, docx_name)
            h = digest(body)
            if cache.get(key) != h or not os.path.exists(os.path.join(dl, docx_name)):
                pypandoc.convert_text(body, "docx", format="markdown-smart",
                                      outputfile=os.path.join(dl, docx_name), extra_args=["--wrap=none"])
                cache[key] = h
                print("word  ", key)
            links = ["[This page (Word)](downloads/%s)" % docx_name]
            m = re.match(r"week-(\d+)-", name)
            if folder == "getting-started" and m and int(m.group(1)) in weeks:
                wk = int(m.group(1))
                pp = "week-%02d-slides.pptx" % wk
                keep.add(pp)
                key = "%s/%s" % (folder, pp)
                if cache.get(key) != deck_hash or not os.path.exists(os.path.join(dl, pp)):
                    split_deck(set(weeks[wk]), os.path.join(dl, pp))
                    cache[key] = deck_hash
                    print("slides", key)
                links.append("[This week's slides (PowerPoint)](downloads/%s)" % pp)
            if folder != "shared":
                links.append("[The whole series (zip)](downloads/%s.zip)" % folder.replace("/", "-"))
            stamp = STAMP + " · ".join(links)
            lines = md.split("\n")
            while lines and (lines[0].startswith(STAMP) or (lines[0] == "" and len(lines) > 1 and lines[1].startswith(STAMP))):
                lines.pop(0)
            if lines and lines[0] == "":
                lines.pop(0)
            new = stamp + "\n\n" + "\n".join(lines)
            if new != md:
                io.open(path, "w", encoding="utf-8", newline="\n").write(new)
            pages.append((name, docx_name))
        if folder == "getting-started":
            for srcname, web, _, _ in INSTRUMENTS:
                keep.add(web)
                s, d = CCA + srcname, os.path.join(dl, web)
                if os.path.exists(s) and (not os.path.exists(d) or open(s, "rb").read() != open(d, "rb").read()):
                    shutil.copyfile(s, d)
                    print("instr ", web)
        if folder != "shared":
            zname = folder.replace("/", "-") + ".zip"
            keep.add(zname)
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                for _, d in pages:
                    zi = zipfile.ZipInfo("%s/%s" % (folder.replace("/", "-"), d), (2026, 1, 1, 0, 0, 0))
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(zi, open(os.path.join(dl, d), "rb").read())
            data = buf.getvalue()
            zp = os.path.join(dl, zname)
            if not os.path.exists(zp) or open(zp, "rb").read() != data:
                open(zp, "wb").write(data)
                print("zip   ", folder)
        index_section(folder, label, pages)
        for f in os.listdir(dl):
            if f not in keep:
                os.remove(os.path.join(dl, f))
                print("removed stale", folder, f)
    json.dump(cache, open(CACHE, "w"), indent=1, sort_keys=True)


def index_section(folder, label, pages):
    path = "docs/%s/index.md" % folder
    md = io.open(path, encoding="utf-8").read()
    s = ["## Downloads", ""]
    if folder == "shared":
        s.append("Every card and page here, as a Word file to print or adapt:")
        s.append("")
        for name, d in pages:
            s.append("- [%s](downloads/%s)" % (title_of("docs/%s/%s" % (folder, name)), d))
    else:
        s.append("Everything for %s, current with these pages. Each lesson plan also carries its own "
                 "download at the top of its page." % label)
        s.append("")
        for name, d in pages:
            if "handbook" in name or "guide" in name:
                s.append("- [%s (Word)](downloads/%s)" % (title_of("docs/%s/%s" % (folder, name)), d))
        s.append("- [Every lesson plan and handbook in one download (zip of Word files)](downloads/%s.zip)"
                 % folder.replace("/", "-"))
        if folder == "getting-started":
            s.append("- [The full slide deck, all twenty-two weeks (PowerPoint)](gs-session-slides-v1.5.pptx); "
                     "each week's page also has just that week's slides.")
            s.append("- [The Weekly Companion Debrief Sheets (Word)](gs-weekly-companion-debrief-sheets.docx)")
            s += ["", "**The measurement instruments.** What the pilot asks of families, and when. Each is "
                  "used only on a family's yes, under the [Measurement Covenant](../shared/measurement-covenant.md); "
                  "the full plan is Section 8 of the [Handbook](handbook.md).", ""]
            for _, web, label_, what in INSTRUMENTS:
                s.append("- [%s (Word)](downloads/%s) — %s." % (label_, web, what))
    sec = "\n".join(s) + "\n"
    md = re.sub(r"\n## Downloads\n.*?(?=\n## )", "", md, flags=re.S)
    i = md.find("\n## ")
    md = md[:i] + "\n" + sec + md[i:] if i >= 0 else md.rstrip("\n") + "\n\n" + sec
    io.open(path, "w", encoding="utf-8", newline="\n").write(md)


def title_of(path):
    """The page's title as the site's navigation shows it (manifest.js)."""
    m = re.search(r'"path": "%s",\s*"title": "([^"]+)"' % re.escape(path), io.open("manifest.js", encoding="utf-8").read())
    return m.group(1) if m else os.path.basename(path)[:-3].replace("-", " ").capitalize()


main()
