# Session Handoff — 2026-08-22 · START HERE

**Read this first in a new session. The LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_foth_adult_cpr_sequence.md` carries the adult year; `project_jsfsc_companion_series.md` carries the papers). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-21 (both versions).**

**Everything is mirrored and live. No mirror queue on the CCA pair. Adult repo is DEV ONLY as always.** Current heads: CCA dev `a29cfd3` / CCA prod `f77c16a` (tree diff = exactly the five standing divergences, reader files identical) · adult dev `34075d0` · IJH and CPR untouched.

---

## 1. What happened since the last handoff (evening of 08-21 through 08-22)

**The adult year (foth-for-a-cpr-dev, DEV ONLY).**
- Going Out re-authored — all twelve sessions + index — so **backlog item 18b is COMPLETE across all three series** (`71c1cb9`). Wk 12's continuation is now **the family year**, at the host church's discernment and decision; "the discernment is a covering, not a draft." Record in the adult repo's `_implementation-notes/RETROFIT-BACKLOG.md`; scripts `reauthor_go01–go12.py` beside the GS/GD sets.
- Reader: the top nav was clipping with eight entries — short root-page labels (Leadership Year, Register Key), the strip now wraps, and the sticky sidebars/anchor scrolls follow the header's real height (`--topnav-h`) (`9fb258c`).
- Reader: the two rail features below were ported (`d051057`); the cross-page handout content links were added across all three series — 39 edits on 13 pages, including Going Out → Going Deeper's H11.3 across series — with three stale seed codes corrected (W3 H3.5→H3.3, W4 H3.4→H3.2, W5 H5.5→H5.3) (`34075d0`).
- **Remaining adult-repo work = the gates only:** 18c adult safeguarding section (John + counsel, at a real church's entry gate), 19 final label, 20 image licences before any prod. Observation-pack printable deferred until a first church is real. **Later on 08-22 (adult dev `2921f72`, DEV ONLY):** the residue turned out wider than Wk 9 and was swept — 10 GS files / 33 edits: 'three cohort versions' (H6.1, H9.1), 'all cohorts' (H6.2, H7.1, H9.1 + H11.3 headings), 'three age-tiered sheets' (H7.3 = three tracks on one sheet), 'three versions on this page — use the one for your cohort' (H11.1, H12.1), 'across all three cohorts' / 'each cohort' in the W5 + W12 merge scripts (now 'across the circles' / 'each circle', matching GD/GO), 'Three private spaces for cohort circles' in ten materials lists (now 'a private space per cohort circle'), and three W4 'the senior' leftovers (now 'the rotation leader' / 'the leader'). GD/GO already clean; handbooks stay family-edition seed by design; recorded under 18b in the adult RETROFIT-BACKLOG.

**The CCA pilot (dev → prod, all on John's word).**
- **GS Week 6 image** replaced with the clasped-hands photo now in deck v1.5 (licence for web use confirmed by John): `wk06-brave.jpg` per current-week naming, old single-tree `wk05-brave.jpg` removed. Deck-vs-site audit across all 22 weeks: Wk 6 was the only divergence (Wks 9/10 share the tiny deck divider by design; **Wk 20 is live at the thin 379×463 — full-res original still wanted someday**). dev `aa19620` → prod `8922fdc`.
- **Reader: section numbers in the right-rail index.** Pages with several H1s (the handbooks: Section 1–11, Appendices A–J; week pages: Quick Reference Card … Handouts) now show them as group labels in "In this chapter." (`f8efa81`)
- **Reader: handouts are link targets.** Every `**Handout HN.M — …**` block gets id `handout-hN-M` and a rail entry under Handouts; check-off cards link their handout codes to the printed form — **Wk 6's Quarterly Pulse (H6.3) → Wk 11's H11.4 where the page actually prints; Wk 4's Joint Footprints → Wk 3's H3.5; Wks 3/5/9/11/16/20 → their own blocks.** (`a0ef08b`) Mirrored prod `27f4ce0`.
- **Reader: cross-chapter anchors re-land as layout settles** (fonts.ready / load / 1.5s / 3.5s; backs off once the reader scrolls) — long pages had been landing thousands of pixels off. (`32e86a7`, mirrored with the pack below.)
- **The Weekly Companion Debrief Sheets pack has a front door (John's option 2).** `docs/getting-started/gs-weekly-companion-debrief-sheets.pdf` (exported from the Word original via Word COM) + `.docx` (hash-identical to the CCA-folder/Desktop copy); Shared Materials hub entry (team-facing) + how-they-fit bullet; every GS week's debrief section opens with *"Print this week's sheet — page N of the pack (PDF) · Word original"* — **pack page = week + 3** (p1 cover rules, p2–3 Ladder of Signs calibration), opening in the reader's PDF viewer at that page. dev `a29cfd3` → prod `f77c16a`. **The blank pack is public by John's decision; filled named sheets never go anywhere.**
- **Printed Practice Check-Off Cards docx** (Desktop + CCA folder, hash-identical, 22 pp): Week 6 line now says "(H6.3 — printed form at Week 11, H11.4)" and Week 4's says "(H3.5 — printed on the Week 3 page)" — same wording as the site. Backups in the session scratchpad.

---

## 2. Disciplines created today — keep them

- **Debrief pack refresh:** the CCA-folder Word file stays the single source. Whenever it is hand-patched, re-export the PDF (Word COM `ExportAsFixedFormat(path, 17)`), copy BOTH files into dev under the same names, regenerate, mirror. Page = week + 3 unless the front matter changes.
- **Handout link convention:** in-page `[H9.2](#handout-h9-2)`; cross-page `[H6.3 — …](week-11-doubts.md#handout-h11-4)`; cross-series `../going-deeper/week-11-….md#handout-h11-3`. The reader's PDF popup (`a.pdf-popup`) honors `#page=N`.
- **Four-place change rule still stands** for anything touching the signs (block heading, script, deck slide, run-sheet table, pre-printed pack) — and now the printed check-off cards are a sixth place for handout pointers.

---

## 3. Eleven days to September 2 — people-work unchanged

Carried forward verbatim: the two founder-absent ordinary Wednesdays (John's pick); phone-verify Pastor Gore's number with the crisis card; Andrea's name and date on the launch-blocking checklist; permission conversations one family at a time in the gap week Sep 3–15 (carry card printed, CCA folder); covenant and child-protection signatures at the pre-launch team call; same-week-call counselor designated; chaplain row confirmed; second-door question (not urgent).

---

## 4. The papers — both in waiting states

- **"Measuring Spiritual Maturity in Hearing God" (JSF-26-0039):** R2 submitted 08-15; awaiting Porter. Nothing to do.
- **"If a Teenager Can Use It" (curriculum article):** v1 canonical; awaiting John's next blue round ("Word closed, over to you" restarts the baton). Citations still to web-verify before any submission.
- **Twenty-Two Wednesdays v2.4:** frozen; gated on the foundation paper's acceptance; Porter gets a short description first.

---

## 5. Gotchas paid for today (so nobody pays twice)

- A Python heredoc turned `\\b` into a literal BACKSPACE byte inside a JS regex (`cat -A` shows `^H`) — write regexes to files via raw strings or avoid `\b`.
- Both CCA repos have `core.autocrlf=true`: committed content is LF, working copies may be CRLF after python writes — use `\r?`-tolerant regexes or `newline=''`.
- The Browser pane preview does not composite when hidden: screenshots time out, ResizeObserver callbacks and smooth scrolls never fire — verify with JS measurements and `fonts.ready`/timers, and use a fresh port for every reader.js change (sticky cache).
- `diff -rq` exits 1 when the five standing divergences exist — never chain a commit after it with `&&`.
- Deck images licensed for the deck are not automatically licensed for the web — ask every time (asked and confirmed for Wk 6).

JD: fetch before dev pushes, as always. Prod CNAME files are infrastructure; leave them be. Mirror only on John's explicit word; the adult repo has no prod at all until items 19 and 20 clear.
