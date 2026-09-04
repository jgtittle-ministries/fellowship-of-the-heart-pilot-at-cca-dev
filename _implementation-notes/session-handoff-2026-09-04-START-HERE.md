# Session Handoff — 2026-09-04 · START HERE

**Read this first in a new session. The LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_foth_adult_cpr_sequence.md` carries the adult year; `project_jsfsc_companion_series.md` carries the papers). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-22 (and all its same-day addenda).**

**Everything is mirrored. Both mirror queues are empty.** Heads at close: CCA dev `f981618` / CCA prod `c23b8b8` (tree diff = exactly the five standing divergences; reader files identical) · IJH dev `34257ad` / IJH prod `8c01e50` · adult dev `2921f72` (DEV ONLY, gates 18c/19/20 only) · CPR untouched.

> **Date caveat for the next session:** the machine clock at this close reads **4 September 2026** — after the planned 2 September opening — while the last dated file work was 22–23 August. Reconcile with John first thing: if the date is right, Week 1 did not run and the pilot is un-launched; nothing below assumes otherwise.

---

## 0. The live thread — read this before touching anything

**Zero families have signed up.** John suspects the 5:30 end (every other club stops at 5:00) and is weighing two doors:
- **45-minute sessions** (4:15–5:00). A decision draft exists — *scratchpad only, nothing deployed*: the standard-week 45 template, Week 2 at 45, and Week 3 both ways (as a published long night vs. an honest 45 with one-scene tells). The recommended shape was "45 plus six published long nights" (Weeks 3, 4, 6, 9, 14, 21).
- **An evening home group, back to the original 7:00–8:30 ninety minutes.** Governance moves with it (covering, premises, safeguarding leave CCA; the door out travels); materials roll back cheaply with the sweep tooling; a middle door is a CCA-blessed group meeting in a home.

**Ruled first move: interview three families before any ruling.** The card is built — `FotH Pilot\FotH Getting Started - The Family Interview (how should this year run).docx` — open question first, five-option menu A–E, the parent question (draw / stretch / dealbreaker), logistics, the closer. Other suspects named beside the clock: the both-of-you weekly ask, recruitment mechanics, and the fact that the permission conversations (Sep 3–15) were always the plan's engine.

**Nothing in the plans, deck, site, or printed materials changes until John rules.**

---

## 1. What landed since 08-22 (all on John's word; all mirrored)

- **Printed take-homes, the whole year:** the Practice Check-Off Cards carry how-to text on 17 of 22 cards (Weeks 2–13, 15–20; the deck's Between-Session slides in the room's own words); Week 6/11/16/20 say *answers go on the sheet, not the card*. Standalone return sheets: Q1 Pulse (W6), Midpoint Pulse (W11), Pulse 3 (W16), Post-Series Survey (W20). Week 3 Take-Home Pack (card + H3.2–H3.5). The site's cards match (H2.4 … H20.2), and Week 6 prints the Quarterly Pulse as H6.3 in Q1 framing.
- **Session slides:** the site serves **v1.5** (277 slides; v1.4 hold lifted). The FotH Pilot v1.5 DRAFT is the working master; **re-snapshot on John's word when it moves.** Two text fixes went master + snapshot: slide 8 "seventy-five minutes," title slide "Wednesday afternoons."
- **Seventy-five minutes, said everywhere / afternoons, not evenings:** the session-length and slot residues of the original 90-minute-evening design are swept from the pilot materials (handbook ×7+, Weeks 1/12/14/22, series and site taglines, start-here, consent v3, covenant v2, Clear Agreement, Plain-Words). Real 90s kept: story-writing pre-work, GD/GO pre-meets, the Rhythm Card clearing time, the approved Proposal v2 (stands as submitted).
- **Appendix C v2** (FotH Pilot): CCA example rows filled — Head of School **Andrea Sponsler** (cell still blank), **Pastor Bobby Gore (831) 277-9878** as the club's pastoral care / the door out, Encompass mobile crisis; the school-counselor row struck (Gore is pastoral care for the club, not the school); John's own edit stripped the "verify" scaffolding from the card. The Referral List working card matches.
- **Adoptions from vetting a commercial trauma journal** (dev `74be6ce` → prod `c23b8b8`; IJH dev `34257ad` → prod `8c01e50`): the after-writing dip named in the W3 pre-work, the journal ("When honest writing leaves you low"), and H11.2; the Path Home Card named as the hard-night page in the journal's safety section; handbook §1 "The year itself is the titration"; IJH Register trail 7 (expressive-writing evidence base). The titration paragraph is also **in the curriculum article v1** (John's baton). `FotH Pilot\…The Vetted Shelf (trauma and healing resources).docx` is the one-page team resource.
- **CCA folder reorganized:** `…\Churches and Ministries\CCA\FotH Pilot\` = the current version of every pilot document (25 files, listed in §3); `CCA\Archived Doc\` = 21 superseded/past-event files. Desktop duplicates cleared.

---

## 2. Disciplines — keep them

- **One Word file per deliverable, in `CCA\FotH Pilot\`.** No PDF twin, no Desktop copy. New version in, old version to `Archived Doc\`.
- **Every "CCA folder" path in older notes now means `CCA\FotH Pilot\`** — the debrief pack docx there is still the single source (re-export PDF → copy both into dev → regenerate → mirror; pack page = week + 3).
- **Mirror only on John's explicit word** (both pairs). Handbook, `getting-started/index.md`, `docs/index.md`, `start-here.md`, `going-out/index.md` are the five standing-divergence files — targeted edits, never whole-copy. `week-06-brave.md` is stored with CRLF in both CCA repos: insert with the file's own ending; compare lone-CR/bare-LF counts, not total CRs.
- **Baton:** John hand-edits a Word file and says "closed" → diff against the last known state, keep his deletions exactly, tidy only mechanical residue (dangling separators), report. The curriculum article is his.
- **Sweep tooling lives in the session scratchpad** (`cards/`, `deck90/`): asserted-anchor Python scripts run on either repo root; the pattern is proven — write the script once, run on dev, run on prod, check `docs/` diff = 5.
- **Deck edits:** unzip → edit slide XML → rezip with `[Content_Types].xml` first → open in PowerPoint via COM to verify → deploy master → re-snapshot both repos on John's word.

---

## 3. `CCA\FotH Pilot\` at close (25 files)

Deck v1.5 DRAFT · 4 Connects v13 (summer club, latest) · Practice Check-Off Cards 1–22 · Week 3 Take-Home Pack · Quarterly Pulse Q1 / Midpoint / Pulse 3 · Post-Series Survey · Weekly Companion Debrief Sheets (single source) · Appendix A consent v3 · Appendix B covenant v2 · Appendix C quick-reference v2 · Referral List working card · Appendix J Clear Agreement · Covering Tonight · Measurement Map 2026-27 · Participant Profile Page · Pre-Series Survey · Permission Conversation carry card · Plain-Words Cover Sheet (DRAFT for counsel) · CCA Proposal v2 · The Family Interview · The Vetted Shelf · Thursday Brief · Thursday Prep.

**Goes home with the card (print together):** W3 the pack · W6 the Q1 Pulse · W7 H7.1 + H7.3 · W9 H9.2 + H9.3 · W11 H11.2 + the Midpoint Pulse · W15 H15.3 + their built Rhythm Card · W16 Pulse 3 · W19 the two mercy cards · W20 the Survey.

---

## 4. Still open, all John's

- The three family interviews → the ruling (45 / long nights / home group / as announced).
- Andrea Sponsler's after-hours cell; Pastor Gore's after-hours protocol; phone-verifying every local number on Appendix C.
- The people-work carried since August: founder-absent Wednesdays, permission conversations, covenant and child-protection signatures, the same-week counselor, the chaplain row.
- Adult repo gates 18c/19/20 before any prod. Papers: foundation R2 awaiting Porter; curriculum article v1 with John (titration paragraph now in it); Twenty-Two Wednesdays v2.4 frozen.

JD: fetch before dev pushes, as always. Prod CNAME files are infrastructure; leave them be.
