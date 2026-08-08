# Session Handoff — 2026-08-07 · START HERE

**Read this first in a new session — the LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_jsfsc_measuring_maturity_rnr.md` for the journal article). This file is the repo-side snapshot for John and JD. Supersedes the 2026-08-04 handoff.**

## 1. The big new thing — the 22-week session slide deck (v1.3 DRAFT)

`CCA\FotH Getting Started Club 2026-27 Slides v1.3 DRAFT.pptx` — **240 slides, all 22 sessions**, built from John's dictated pattern (Weeks 1–2 dictated line by line; Weeks 3–22 extracted from the lesson plans by five parallel agents and spot-corrected in John's walk-through). v1.2 kept as fallback; the confusing "v2 DRAFT" file was an interim save and was **deleted** on John's instruction.

**The pattern per week:** divider → Tonight's Road (standing card removed) → one slide per road stop — the standard eight-step opening, week-specific content slides in big read-aloud type, the Leader Feedback Round, the closing with the full Aaronic blessing on a cream card → (Anchor & Practice slides all deleted; content absorbed). Auto-updating slide numbers deck-wide.

**Five standing liturgical images** (same size/position everywhere, so they read as liturgy): the **open walnut bowl** on every road W2+ (the container built first) · the **trail cairn** on all 13 check-ins incl. both "What Held?" re-entries (each adds a stone) · the **compass in hand** on all 22 Leader Feedback Rounds (the bearing-check) · the **luminous seedling** on the Between-Session Practice slides (what grows between Wednesdays; W1 keeps the journal image, W3 keeps joint-footprints) · the **cream blessing card** at every close. Week 1's road carries the "Hearing and obeying God" purpose panel instead of the bowl (the very-first-time exception).

**Quarter 1 teaching images placed** (all free Pexels, no faces): stepping stones (W3 stories), parent+child footprints (W3 practice), threefold cord (W5, Eccl 4), sunlit water over stones (W6 confession). W4 deliberately text-only. W6 **divider** re-imaged: clasped hands ("together") replaces the lone tree. W22's welcome slide repeats the W1 open-door divider image — the gate bookend.

**Walk-through fixes already applied:** deck is 100% self-contained — zero H-handout-codes (Any Doubts scriptures + four steps inline; Gifts/Downhill questions + share frames inline; 7 more slides de-coded); the W15 road slide had **16,000 characters of leaked lesson-plan text** in stop 9 (v1.2 build artifact) — cleaned to a proper road line; W16 rails corrected (see §3).

**Build system preserved at `_implementation-notes/slide-deck-build/`** (dev-only): the four build scripts, `weeks/roads.json` + `week03..22.json` (per-slide content JSON), `deck_map.txt` (position → title map, pre-fix snapshot), and **`four-soils.svg`** — a new diagram in the site's wk01-four-connects style, on the W2 teaching slide, and a candidate for the site's week-02 page on John's word. Editing workflow gotcha: **John must close PowerPoint before each edit round** (file lock); QA renders via PowerPoint COM export.

**OPEN on the deck:** John's continuing walk-through of Weeks 3–22 (read out slide numbers — they auto-update) · Quarter 2–4 teaching images, quarter at a time (Q2 = W7–11 next: PROAPT/Garden/Doubts) · six divider VISUAL-TO-COME placeholders (W12/14/16/17/19 + W15 re-choice) awaiting John's sourced photos · four weeks (12/14/19/21) list a post-feedback "blessing and sending" stop that the standing closing slide covers — flagged, John may want dedicated final-blessing slides there.

## 2. JSFSC article — STILL UPLOAD-READY (clock running since 08-01)

**Em-dash / AI-tell pass DONE 2026-08-07** on all four upload files (John's call: "impress sensitive academic readers"): v23 blue text 37→0 em dashes (black text untouched), Response 32→0, Cover 4→0, TitlePage 2→0 — per-sentence rewrites, reviewer-verbatim sentences untouched, two Proposition en-dash typos fixed, three broken appositive sentences repaired (repairs colored blue per the marking convention). **Abstract is now 298 words** (TitlePage updated). Cover letter re-dated Aug 5 — **re-date again on upload day**. Backups: `_backup … (pre em-dash pass).docx` ×4 in IJH edits. **John's remaining steps unchanged:** final blue read → Table 1 glance → paste the 298-word abstract into ScholarOne metadata → upload all four via the link in `JSFSC Article R1 Comments.docx`.

## 3. Site work shipped this session (ALL MIRRORED — mirror queue EMPTY)

- **Reader: in-chapter outline** (dev `d57a456` → prod `1195e06`): right rail shows Reading % + a jump list of the page's sections on every content-rich page; repeated headings ("Script") excluded; heading ids collision-safe.
- **Standalone handout printing** (dev `dc1d445` → prod `f187694`): `@media print` stylesheet (chrome drops away, black-on-white, paper type scale) + a **Print button** in the top bar + "Printing a handout" section on the shared-materials hub (which also gained the missing Weekly Run Card + Interrogating Reality Card listings). Any card = one click to a clean printout.
- **PROAPT Observe = two layers** (dev `1c7519d` → prod `464d17d`): John's teaching — first the **data** (who/what/when/where, answerable from the text by anyone; John 4: Jesus and a Samaritan woman, noon, a well, Samaria), then the **interpretation** of the data (her surprise — the door into the Jew/Samaritan, man/woman dynamics). In 6 files: PROAPT card (canonical, full John 4 example), GS Wk7 (QRC + Mark-1 walk + cardstock appendix), GS Wk8 (Mark-2 walk + facilitation card), GS Wk14, GD Wk6 (structural observe keeps the order), journal template ×7.
- **W16 three rails** (dev `1654a77` → prod `3423e78`): the first church ran on **three** rails — the teaching, the table, and the prayers (Acts 2:42) — fixed in both the framing paragraph and the table-grace script; deck slide matches.

## 4. Housekeeping this session

- `FotH Getting Started Club 2026-27 Slides v2 DRAFT.pptx` **deleted** (it was an older interim save masquerading as newer — internally labeled v1 DRAFT).
- JSFSC TitlePage v2 copied into IJH edits so both folders hold the full four-file upload set.

## 5. Standing threads (unchanged from 08-04 unless noted)

- **TONIGHT (Thursday 2026-08-07) was slated as the summer 4Cs club's FINAL session — interest cards at the close (pass gate 4–6 families).** Debrief next session.
- Sep 2 launch; legal review in motion; student-leadership written yes/no needed before Week 4 (Sep 23); consent form current on prod for counsel.
- August FC1 ramp: call conversations + consent addendum; Lab 1 alongside Weeks 1–2.
- Bill + wife's FC answer pending; WR wing persona keying on John's word; JD pushes to dev — **fetch first**.

## 6. Pickup order

1. **JSFSC upload** (longest-running clock): blue read → abstract paste (298 words) → ScholarOne; re-date the cover letter.
2. **Summer club debrief** + interest-card count.
3. **Deck:** continue the walk-through; Q2 images on John's word; divider photos when John sources them.
4. **FC1 ramp calls** + standing items above.
