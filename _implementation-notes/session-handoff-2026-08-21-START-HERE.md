# Session Handoff — 2026-08-21 · START HERE

**Read this first in a new session. The LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_foth_adult_cpr_sequence.md` carries the adult year; `project_jsfsc_companion_series.md` carries the papers). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-20. EVENING UPDATE the same day: Going Out is done — item 18b is complete.**

**Today's work was entirely in the adult repo (`foth-for-a-cpr-dev`, DEV ONLY, no prod). This CCA repo did not change. All sites current; nothing in any mirror queue.**

---

## 1. The adult year — ALL THREE SERIES ARE NOW FULLY RE-AUTHORED (18b COMPLETE)

- **Getting Started (2026-08-20):** all fifteen sessions + index + both hold pages.
- **Going Deeper (2026-08-21, morning):** all twelve sessions + index.
- **Going Out (2026-08-21, evening):** all twelve sessions + index, pushed as adult dev `71c1cb9` and live-verified on the dev Pages site. The whole leadership year now speaks the adult register end to end. Weave audit still clean (only GS15's designed 8:00 rite end).

**What Going Out's re-authoring settled, beyond the proven pattern:** the split weeks (3, 5, 11) run in circles of four to eight; cross-cohort teen/parent dynamics became cross-spouse and cross-circle protocols; Week 9's parental-consent contingency became household capacity with the spouse's own yes named in the pastoral conversation; workplace/school became workplace/ministry; and **Week 12's "Going Deeper round 2" continuation became THE FAMILY YEAR — the work the leadership year exists to prepare, at the host church's discernment and decision (the seriousness gate's exit), with "the discernment is a covering, not a draft" protecting honest non-continuation.** New ordained watches worth knowing when reading the series: a sermon is not a Tell (Wk 2); the job description as sent-context (Wk 3); the no-third-place-at-all hazard — every room turns into church (Wk 7); the org-chart pull in corporate discernment — an offering lands as an announcement (Wk 8); tonight-they-receive at the laying-on-of-hands (Wk 9); the pre-polished integration — the pulpit knows how to make a year preach (Wk 10); the credentialed reading of the body (Wk 11); the office is not a draft notice (Wk 12).

**The method that carried all three series:** read the file whole; hand-build exact-pair patches with count==1 asserts that refuse to write on any failure; splice the Differentiation section between anchors; residual-grep with word boundaries; classify room-roles (convert) vs life-roles (keep — family-of-origin, spouses, children, caregiving stay, and the household week keeps its family language whole). Grep the file for its actual apostrophes before writing any pair. Scripts: `reauthor_gs*.py` / `reauthor_gd*.py` / `reauthor_go*.py` in the adult repo's `_implementation-notes/`, record in `RETROFIT-BACKLOG.md` item 18b.

**Seed repairs made in passing today (GO):** "WWks/WWk" typos (6×); "Going Out's Going Out" and "Going Out Going Out" artifacts; "The Going Out series" redundancy in the Wk 1 script; "the interlude have/were" grammar (3×); stray registration apparatus. The series handbooks (including Inviting Others) stay family-edition seed under their notices — the Leadership Year Handbook governs.

**Now queued in the adult repo (the gates before any prod):** 18c adult safeguarding section (John + counsel, at a real church's entry gate); item 19 final label; item 20 image licences. The observation-pack printable stays deferred until a first church is real. **There is no keyboard task left in 18b.**

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
