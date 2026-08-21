# Session Handoff — 2026-08-21 · START HERE

**Read this first in a new session. The LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_foth_adult_cpr_sequence.md` carries the adult year; `project_jsfsc_companion_series.md` carries the papers). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-20.**

**Today's work was entirely in the adult repo (`foth-for-a-cpr-dev`, DEV ONLY, no prod). This CCA repo did not change. All sites current; nothing in any mirror queue.**

---

## 1. The adult year — Getting Started AND Going Deeper are now fully re-authored

The per-file adult re-authoring is two series done, one to go:

- **Getting Started (2026-08-20):** all fifteen sessions + index + both hold pages.
- **Going Deeper (2026-08-21):** all twelve sessions + index. Live-verified on the dev Pages site.
- **REMAINING — the pickup task: Going Out.** Twelve sessions + index; the practice hold sits after Week 8 with the what-held re-entry at Week 9. The pattern is fully proven; the detailed record and conversion vocabulary live in the adult repo's `_implementation-notes/RETROFIT-BACKLOG.md` (item 18b) and the `reauthor_gs*.py` / `reauthor_gd*.py` scripts beside it.

**The method that worked (unchanged for Going Out):** read the file whole; hand-build exact-pair patches with count==1 asserts that refuse to write on any failure; splice the Differentiation section between anchors; residual-grep with word boundaries; classify room-roles (convert) vs life-roles (keep — family-of-origin, a parent's death, children, grandmothers stay). Grep the file for its actual apostrophes before writing any pair — the seeds mix straight and curly per file.

**The conversions that now define the adult register, carried through both series:** three-cohort splits → circles of four to eight; the family-across-cohorts protocols → the spouse protocols; Section 6 / Virginia / two-adult → the safeguarding frame (Leadership Year Handbook §7 + the host church's policy) with the about-minors reporting note; generational projection → positional projection (pastor ⇄ congregation); junior/senior/parent handouts → the single adult card (the parent version was the adult version all along); differentiation → first-timers / veterans / the-ordained-and-the-staff; and the leader tells first, now structural (GD Week 4's demonstrations run Companion-first). GD Week 12's continuation-registration became the entry-gate year commitment — attrition read, never scored.

**Seed repairs made in passing, for the record:** the "Going Deeperback" corruption → Tell Buddies fallback; Asker→Discerner in GD Weeks 11–12 (48×); the Anthony/CCA reporting line → the covering; "The Question Carried into Spring" → Going Out; the 6–10-week interlude durations → the year's two-week break; four stale 10-week-shape lines in the GS index. The series handbooks stay family-edition seed under their notices — the Leadership Year Handbook governs.

**Also still queued in the adult repo:** 18c adult safeguarding section (John + counsel, at a real church's entry gate); item 19 final label; item 20 image licences before any prod. The observation-pack printable stays deferred until a first church is real.

---

## 2. Twelve days to September 2 — the people-work is unchanged

Nothing here moved today; carried forward verbatim from 08-20:

- **Two founder-absent ordinary Wednesdays need picking** and putting on the calendar — John's pick, not a keyboard task.
- Phone-verify Pastor Gore's number with the rest of the crisis card; Andrea's name and date onto the launch-blocking checklist.
- Permission conversations, one family at a time, gap week September 3–15 (carry card printed, in the CCA folder).
- Covenant signatures at the pre-launch team call; child-protection signatures; same-week-call counselor designated; chaplain row confirmed.
- Decide whether to name a second door with no CCA connection. Not urgent, worth a think.

---

## 3. The papers — both in waiting states

- **"Measuring Spiritual Maturity in Hearing God" (JSF-26-0039):** R2 submitted 2026-08-15. Awaiting Porter. Nothing to do.
- **"If a Teenager Can Use It" (curriculum article):** v1 canonical in OneDrive `…\JSFSC Articles and Revisions\` + Desktop — 14 pp / 9 footnotes / 2 tables after blue round 2. **Awaiting John's next blue round** ("Word closed, over to you" restarts the baton). Standalone by design — no TTW reference. Citations still to web-verify before any submission: Tuckman, Bion, Krathwohl, Lencioni, Smith.
- **Twenty-Two Wednesdays v2.4:** frozen. Submission gate unchanged — nothing moves until the foundation paper is fully accepted with a preprint link, and Porter gets a short description first.

---

## 4. Sites, deck, and images — unchanged

FotH prod `7335eb6`, IJH prod `5af7910`, CPR unchanged, all as live-verified 2026-08-19; the adult dev Pages rebuilt and verified today (2026-08-21). Deck = 277 slides, v1.5 DRAFT in the CCA folder. IJH still wants FL.XLVIII and the *Properties of Spiritual Law* image; John wants an IJH/CPR image pass later.

---

## 5. Standing rules that held up today

- Life roles are kept; room roles are converted. An adult still has a mother, a childhood, a family — the register change never erases them.
- Patch scripts refuse to write on any failed match. The one time a cleanup script wrote unconditionally (GS W13b), it cost a spliced word; the gate stays.
- Grep the file's own apostrophes before writing a pair. Every file mixes straight and curly differently.
- The rites are not measured; commissionings lay the feedback round down.
- Mirror only on John's explicit word — and the adult repo has no prod at all until items 19 and 20 clear.
- Every commit in the adult repo ends "DEV ONLY."

JD: fetch before dev pushes, as always. Prod CNAME files are infrastructure; leave them be.
