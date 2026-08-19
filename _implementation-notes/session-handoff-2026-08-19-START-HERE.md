# Session Handoff — 2026-08-19 · START HERE

**Read this first in a new session. The LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_jsfsc_companion_series.md` carries the paper). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-18.**

---

## 1. The one thing that must happen before September 2

**The door out needs a name.** Handbook Section 6 now carries a subsection called *The door out* — one adult outside the Companion team, reachable by any participant without going through a Companion or a parent, announced aloud in Week 1 and printed on the take-home page. The name and contact are blank, and they are now a **launch-blocking checklist item: if the name is blank, the program does not open.**

The natural fit is the counseling-referral contact CCA was asked to designate in proposal request #3. This is John's to supply.

Everything else below can wait. This cannot.

---

## 2. Where the paper stands

**Canonical file: `Twenty-Two Wednesdays - JSFSC Protocol Paper v2.4.docx`** in OneDrive `…\Current Documents\Articles for Publication\JSFSC Articles and Revisions\`. **20 pp / 8,586 words / 15 footnotes / 0 open comments.** v2.3 and below are frozen snapshots; do not edit them.

**Word budget is the live constraint: 8,586 of a 9,000 cap.** About 414 words of headroom. From here, every addition needs a subtraction. The second principle (174 words against 37–45 for its siblings) is the most obvious place to find room.

**Two peer-review stages are complete and applied.** Artifacts are dev-only in IJH under `_implementation-notes/`:
- `peer-review-twenty-two-wednesdays-sources/` — Stage A, source fidelity (IJH dev `e58c2dd`)
- `peer-review-twenty-two-wednesdays-methodology/` — Stage B, methodology (IJH dev `ed6f2bd`)

Each carries a synthesis + punch-list docx, the full reviews, the refuter verdicts, and the briefs. **Read the synthesis, not the reviews** — the refuters killed or narrowed several of the reviews' most striking claims, and the synthesis records which.

**Still open from Stage B**, in the synthesis's own order:
- The four free fixes (raw weekly series reported beside the ratcheted rung; independent marking before the Thursday Call; sheets unread until June; quarterly re-marking of the calibration vignettes).
- The falsifiability repair (Tier 2): no decision criteria, nothing tests adherence, no attendance record, no decisions log, and the frozen-observation / adaptive-content split.
- Tier 3 inference work, including the two cheap rival tests: **two founder-absent ordinary Wednesdays** (the teen-led nights do not serve, since they run with a full team present) and **one unsigned card eight weeks after the year ends**. If the summer card is adopted, the permission language must change before the gap-week conversations.
- Two design questions John deferred: safety items on the quarterly pulse read as a teen-versus-parent gap, and whether attrition is read as safety data.

**Stage C** (the Biola desk: Coe, Porter, M. Elizabeth Lewis Hall) is designed and not yet run. Run it on a corrected paper.

---

## 3. Mirror queue — two commits waiting

**FotH dev is two commits ahead of prod.** Mirror only on John's explicit word.

| dev commit | what |
|---|---|
| `ab7a338` | The reader from outside (quarterly outsider, two hours, no notes or transcripts) + the weekly surprise line in the Companion observation notes |
| `a468f39` | The safeguarding set: the door out, the stopping rule on being sought, a pass is data, when a family stops coming, and the retention endpoint in the Measurement Covenant |

Files touched beyond the five standing divergences: `getting-started/CHANGELOG.md`, `getting-started/week-01-welcome.md`, `shared/measurement-covenant.md`. The handbook has unmirrored content **on top of** its standing IJH-URL divergence, so it stays a targeted-patch file at mirror time.

Everything else is in sync: IJH dev/prod, CPR dev/prod, and FotH prod is current through `00da339`.

---

## 4. Printables changed today (CCA folder + Desktop)

- **The Permission Conversation (carry card)** — new, one page. The gap-week ask in John's own words, what one yes covers, what a no costs, six likely questions, and two guards. Privacy promise revised to what can actually be kept.
- **Weekly Companion Debrief Sheets (Weeks 1–22)** — gained the surprise line, the pass-read, and the sought-and-declined tick. **Still exactly 25 pages; one page per week is intact.** Week 22 deliberately has none of these: the rite is not measured.
- **Watching Trust Grow card** — corrected and mirrored to prod. Six markers re-attributed (three psychological safety, one group-development conflict, one reciprocity, one our own) and the KNOWN listening cue un-inverted to *"I know how they'll take it."*

---

## 5. How John and the assistant now work on the docx

Written up in the assistant's memory as `feedback_docx_baton_workflow.md`. In short:

- **The baton.** One of us holds the file at a time. John edits, closes Word fully, says it is back. The assistant verifies no lock file and no WINWORD process before writing, then hands it back explicitly.
- **John does not summarize his edits.** The assistant snapshots a baseline before handing over and diffs on return, reporting every change for confirmation. A change missing from that report means a save did not take.
- **Questions go in Word Comments**, not in the prose. The assistant reads them with the exact words each is anchored to.
- **Version numbers move at John's milestones, not per exchange.**

Four gotchas learned the hard way today, all recorded: rebuilding a paragraph from its text destroys footnote references inside it; hand-moving runs between paragraphs corrupts the file; deleting comments by editing `comments.xml` corrupts the file because three companion parts go stale (use Word COM); and `python-docx` does not walk tables unless told to. **Always back up before a structural edit and open the result in Word to check page, word, and footnote counts before handing the baton back.** Both of today's corruptions were caught by that check and nothing else.

---

## 6. Standing rules that held up today

- The rite at Week 22 is not measured.
- One page per debrief week is sacred. Fight the spill, never the sheet count. Three attempts were needed today to add two lines without losing that.
- Rooms, never people. Mirrors, never levers.
- Permission is for pages, never for care.
- Mirror only on John's explicit word; the handbook is always a targeted patch.
- De-AI watchlist for the paper: no em dashes, "load-bearing" banned.

JD: fetch before dev pushes, as always. Prod CNAME files are infrastructure; leave them be.
