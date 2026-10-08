# -*- coding: utf-8 -*-
"""Build every evening Leader Notes doc from its deck's speaker notes.

Run from the repo root:  python tools/build-evening-leader-notes.py [session ...]
(no arguments = every deck in _implementation-notes/evening-series).

The deck is the single source: each slide becomes one block in the notes, headed
by the number in the slide's corner (the master sequence, or C/P/G pages in the
combined decks), so the notes and the screen always agree. The series title slide
is labelled "Title" rather than "1" so the numbers don't appear to jump. Each block
is colour-coded by its LEAD tag (from the 7 October debrief, John's word
8 October 2026): container holder blue, content presenter amber, both leaders
purple, on-screen dividers grey. The left-bar styles differ as well, so the roles
still read on a black-and-white printout.

The existing notes doc supplies the document title, subtitle line and footer, and
nothing else; edit the deck's speaker notes, then rebuild.
"""
import glob
import os
import re
import sys

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from pptx import Presentation

sys.stdout.reconfigure(encoding="utf-8")
SRC = "_implementation-notes/evening-series"

ROLES = {  # key: (label, colour, heading shade, left-bar style)
    "CH": ("CONTAINER HOLDER", "1F4E79", "DEEAF6", "single"),
    "CP": ("CONTENT PRESENTER", "B45309", "FCE9D6", "double"),
    "BOTH": ("BOTH LEADERS", "6B3FA0", "ECE3F5", "thickThinSmallGap"),
    "SCREEN": ("ON SCREEN", "8C8C8C", "F0F0F0", "dotted"),
    "OTHER": ("SEE THE TAG LINE", "8C8C8C", "F0F0F0", "dotted"),
}
GREEN, TAG, GREY = "2C5F2D", "6B8E3F", "595959"
AFTER_BDR = ("w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct",
             "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
             "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
             "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId",
             "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
LABEL = re.compile(r"^([A-Z][A-Z0-9 \-/&']{1,30}):\s*(.*)$")


def role_of(tag):
    if "LEAD: CONTAINER HOLDER" in tag:
        return "CH"
    if "LEAD: CONTENT PRESENTER" in tag:
        return "CP"
    if "LEAD: BOTH" in tag or "BOTH LEADERS" in tag:
        return "BOTH"
    if tag and "DIVIDER" not in tag and "pre-session" not in tag:
        return "OTHER"
    return "SCREEN"


def first_line(t):
    return re.split(r"[\n\x0b]", t.strip())[0].strip()


def slide_info(s):
    frames = {sh.name: sh for sh in s.shapes if sh.has_text_frame}
    num = next((sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame
                and re.fullmatch(r"[A-Z]?\d{1,3}", sh.text_frame.text.strip())), "?")
    if "TextBox 2" in frames and frames["TextBox 2"].text_frame.text.strip():
        title = first_line(frames["TextBox 2"].text_frame.text)
    else:
        title = next((first_line(sh.text_frame.text) for sh in s.shapes if sh.has_text_frame
                      and sh.name != "SlideNum" and sh.text_frame.text.strip()
                      and not re.fullmatch(r"[A-Z]?\d{1,3}", sh.text_frame.text.strip())), "(untitled)")
    nt = ""
    if s.has_notes_slide and s.notes_slide.notes_text_frame is not None:
        nt = s.notes_slide.notes_text_frame.text
    return num, title, [l.strip() for l in nt.split("\n") if l.strip()]


def bar(p, key):
    _, colour, _, style = ROLES[key]
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), style)
    left.set(qn("w:sz"), "12" if style == "double" else "24")
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), colour)
    b.append(left)
    pPr.insert_element_before(b, *AFTER_BDR)


def shade_para(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    pPr.insert_element_before(shd, *AFTER_BDR[1:])


def run(p, text, size=None, bold=None, colour=None, italic=None, font=None, fill=None):
    r = p.add_run(text)
    if size:
        r.font.size = Pt(size)
    if bold is not None:
        r.bold = bold
    if italic is not None:
        r.italic = italic
    if colour:
        r.font.color.rgb = RGBColor.from_string(colour)
    if font:
        r.font.name = font
    if fill:
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
        r._element.get_or_add_rPr().append(shd)
    return r


def para(d, before=0, after=3, keep=False):
    p = d.add_paragraph()
    f = p.paragraph_format
    f.space_before, f.space_after = Pt(before), Pt(after)
    if keep:
        f.keep_with_next = True
    return p


def build(deck):
    notes_path = deck.replace(" Slides DRAFT v1.pptx", " Leader Notes DRAFT v1.docx")
    old = docx.Document(notes_path)
    texts = [p.text for p in old.paragraphs if p.text.strip()]
    doc_title, footer = texts[0], texts[-1]
    session = re.search(r"Session (.+?) Slides", deck).group(1)

    d = docx.Document(notes_path)  # keep page setup and styles; clear the body
    body = d.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"):
            body.remove(el)

    run(para(d, after=2), doc_title, 18, True, GREEN, font="Cambria")
    run(para(d, after=4), "FotH Evening · the speaker notes, in hand — so the leading pair reads the room, not the "
        "screen. The big number on each block is the number in the corner of the screen; the colour is whose "
        "block it is. Built from the deck's own notes, so the two always agree.", 9, None, GREY)
    lp = para(d, after=10)
    for key in ("CH", "CP", "BOTH"):
        label, colour, fill, style = ROLES[key]
        mark = {"single": "▌", "double": "‖", "thickThinSmallGap": "▐"}[style]
        run(lp, f" {mark} {label} ", 9, True, colour, fill=fill)
        run(lp, "   ", 9)
    run(lp, "Bar styles differ too, so the roles still read in black and white.", 8, None, "7F7F7F", italic=True)

    slides = list(Presentation(deck).slides)
    untagged = []
    for k, s in enumerate(slides):
        num, title, lines = slide_info(s)
        tag = lines[0] if lines else ""
        key = role_of(tag)
        if key == "OTHER":
            untagged.append(num)
        label, colour, fill, _ = ROLES[key]
        block = []
        hp = para(d, before=8, after=2, keep=True)
        badge = "Title" if k == 0 else num
        run(hp, badge, 15 if k else 12, True, colour, font="Cambria")
        run(hp, "   " + title, 12, True, GREEN, font="Cambria")
        run(hp, f"    {label}", 8.5, True, colour)
        run(hp, f"   · slide {k + 1} of {len(slides)}", 8, False, "7F7F7F")
        shade_para(hp, fill)
        block.append(hp)
        if not lines:
            p = para(d)
            run(p, "No notes on this slide.", 9, None, GREY, italic=True)
            block.append(p)
        for j, line in enumerate(lines):
            if j == 0:
                p = para(d, after=3, keep=True)
                m = re.search(r"(?:LEAD: [A-Z ]+?|BOTH LEADERS)(?= ·|$)", line)
                if m:
                    run(p, line[:m.start()], 9, True, TAG)
                    run(p, m.group(0), 9, True, colour)
                    run(p, line[m.end():], 9, True, TAG)
                else:
                    run(p, line, 9, True, TAG)
            elif line == "BEATS:":
                p = para(d, after=1)
                run(p, "BEATS:", None, True, GREY)
            elif LABEL.match(line) and not re.match(r"^\d", line):
                m = LABEL.match(line)
                p = para(d)
                run(p, m.group(1) + ": ", None, True, GREY)
                run(p, m.group(2))
            else:
                p = para(d)
                run(p, line)
            block.append(p)
        for p in block:
            bar(p, key)
    fp = para(d, before=10, after=0)
    fp.alignment = 1
    run(fp, footer, 9, None, GREY, italic=True)
    d.save(notes_path)
    return session, len(slides), untagged


if __name__ == "__main__":
    want = set(sys.argv[1:])
    for deck in sorted(glob.glob(SRC + "/FotH Evening Session * Slides DRAFT v1.pptx")):
        s = re.search(r"Session (.+?) Slides", deck).group(1)
        if want and s not in want:
            continue
        session, n, untagged = build(deck)
        print("S%-14s %2d blocks%s" % (session, n, ("   untagged leads: " + ", ".join(untagged)) if untagged else ""))
