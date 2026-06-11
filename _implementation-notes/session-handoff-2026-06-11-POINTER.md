# Session handoff pointer (2026-06-11)

The **master START-HERE handoff** for the 2026-06-11 session lives in the IJH dev repo (it covers both projects):

`…\Intentional-Journey-of-the-Heart-dev\_implementation-notes\session-handoff-2026-06-11-START-HERE.md`

**FotH-specific quick state (2026-06-11):**
- FotH **dev `0fd36de` / prod `9dae8d0`**, in sync (only `start-here.md` IJH-URL line + `index.md` DEV banner differ).
- The **full eight-author peer review is implemented through Tier A + Tier B-draftable** (B1/B3/B5/B6 done; **B2/B4 scaffolded with `[fill in]` placeholders**). Diagnostic artifact: `_implementation-notes/peer-review-foth/peer-review-foth-eight-authors.md` (+ `.docx`).
- **Open:** Tier C judgment calls; deferred Tier A micro-polish; and the **John/JD launch-blockers** (the A1 Companion-contact blank; the B2 named-backup/referral-numbers/CCA-policy/VA-reporting-review + signatures; the B4 VA legal review) — all written into the handbooks as checkboxes.
- **Mirror reminder:** copy matching docs dev→prod, apply `start-here.md` in place (keeps prod IJH URL), then `node tools/build-manifest.mjs && node tools/build-search-index.mjs` in prod, commit "Mirror … from dev", push.
