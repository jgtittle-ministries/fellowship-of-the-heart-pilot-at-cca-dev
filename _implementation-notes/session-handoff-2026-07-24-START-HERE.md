# Session Handoff — 2026-07-24 · START HERE

**Read this first in a new session — but the LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; also `project_ijh_household_of_faith_profile.md`). This file is the repo-side snapshot for John and JD.**

## 1. What is live right now

- **The summer "4 Connects" club is RUNNING at CCA** (six sessions, Tuesdays, started 2026-07-21; 3 families + 3 teens, more joining later; John presenting). Deck = `…\Churches and Ministries\CCA\4 Connects for CCA Club July 2026 v10.pptx` (six session dividers; all scripture verified ESV; interest cards at the LAST session only; pass gate agreed as **4–6 families** for the fall launch). Interest Card docx in the same folder + John's Desktop.
- **The fall club** = FotH Getting Started, **fifteen weeks from mid-September** (Wks 14–15 in January). The consolidated handbook + all fifteen full lesson plans + the fifteen-section journal are DONE on this dev repo.
- **John's covering:** standing Thursday meetings, confirmed listening. His accountability partner (+ wife, decades CRU staff) reviewed CPR 7/24, gave rich feedback, and were **invited to serve as Formation Companions — praying about it**.

## 2. Repo state

| Repo | State |
|---|---|
| **FotH dev** | HEAD `9388a72`. **UNMIRRORED since prod `9ac9a65`:** the 15-week consolidation (`e1da2dd`), CCA proposal archive (`de42c2f`), curriculum batch (`c4f92c8` — renames + 5 new full plans + journal), Keeping the Flame (`562fb6b`), and four review-fix commits (`b7240da`…`9388a72`) from John's ongoing read. Mirror ONLY on John's word. **Mirror-time gotchas:** GS handbook + manifest carry env divergences (targeted-patch, never whole-copy); manifest + search are GENERATED — run `node tools/build-manifest.mjs` + `build-search-index.mjs` IN PROD after mirroring (reader loads `search-index.json`; legacy `search-index.js` was deleted). |
| **CPR dev** | HEAD `1870d23`. Dev-only feedback capture `_implementation-notes/reader-feedback-2026-07-24-first-outside-reader.md` + **five drafted revisions awaiting John's review** (Jesus Movement + Fullam/Darien in the Record; Brooklyn Tabernacle + Korean dawn prayer calendar examples; facilitator profile; Wesley-vs-Finney contrast; humility/submission/love bullet in Deciding Together). All facts web-verified; the Darien vestry-unanimity claim was NOT verifiable and was not made. |
| **IJH dev/prod** | Fully mirrored (prod `35ba728` = Household of Faith Profile Register entry complete). WR wing (Walk-In Reading, 6 portraits) dev-only, awaiting John's read → persona keying. |

## 3. Pickup options, in order

1. **John's continued review of the fifteen-week batch** — his screenshot review is finding stragglers (the Wk-1 map table was one); fix on report. Four sweep-classes already cleared: ten-week phrases, half-mapped ranges, week-count arithmetic, container-age counters.
2. **Summer club support** — session debriefs (the Three Vital Signs practice on a real room), tweaks to the v10 deck between sessions, dead-video-link check still on John.
3. **CPR revisions review** → mirror on John's word (CPR conventions: `_implementation-notes/` + `_on-request/` never mirror; in-content cross-links are relative .md paths).
4. **CCA proposal** — John fills placeholders + submits; the CCA/legal gate must clear before fall Week 4 (~mid-Oct); adult-led fallback exists.
5. **FC recruitment follow-up** — the CRU couple's answer; also the partner's eyewitness repentance-revival (identify + permission to capture) and his vestry as a candidate CPR first mover.
6. **Wk 13 + Wk 15 images** (the only two lesson pages without one) — John sources per the image workflow.
7. **WR wing persona keying** on John's word; the Household of Faith Profile brainstorm is officially still open.
8. Standing: Porter/JSFSC decision pending; nothing moves without John's word; JD pushes to dev — **fetch first**.
