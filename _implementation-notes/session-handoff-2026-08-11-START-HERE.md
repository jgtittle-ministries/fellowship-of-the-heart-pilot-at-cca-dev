# Session Handoff — 2026-08-11 · START HERE

**Read this first in a new session — the LIVE state is in the assistant's memory files (`project_foth_15week_cca_launch.md` is the hub; `project_foth_gs_peer_review_alpha_litss.md` for the review punch-list). This file is the repo-side snapshot for John and JD. Supersedes 2026-08-08.**

## 1. THE UNSTARTED NEXT TASK — the pilot's clock (Option 2, John-approved)

The CCA pilot meets **Wednesday afternoons, 4:00–5:30 PM** — but all 22 plans still carry 7:00–8:30 evening run sheets. John's ruling (Option 2): **re-time all clock times, keep the "tonight" script language** (churches and other ministries adopting the edition will mostly run evenings — his own history is almost all evening sessions — and leaders adapt wording on the fly).

To do: shift every clock time in the 22 dev plans −3h — run-sheet rows (including 6:30 setup → 3:30, 6:45 doors → 3:45), block headers "(7:15–7:30, 15 min)", and inline script times ("back at 8:00" → 5:00); Week 21's 120-minute session becomes 4:00–6:00. **Scripture-guard hours 6–9** (Numbers 6:24–26 is everywhere; John 6:35, Romans 7/8, Mark 9 — reuse the guarded-converter pattern proven on the deck notes). Then: the 4:00–5:30 fact on the CCA calendar page + a handbook line, CHANGELOG entry, search index, mirror on John's word.

## 2. Where everything else stands (all mirrored and live unless noted)

- **Site pairs synced** through prod `b3eb797` (the prototype family's field corrections). Peer-review Tier 1 + the covering doctrine (both books) + seed-before-soils + skeptic's seat: all live.
- **Deck v1.5 DRAFT = 268 slides**, CCA working copy: presenter notes on every slide (afternoon clock, SUB flags for a covering leader), 22 take-home card slides, scripture cards at John's 24pt standard, six-step closing panels, gallery frames. v1.4 restored as 241-slide fallback. **Re-snapshot into docs/ as v1.5 + update 3 filename refs at walk-through's end.**
- **Printables in the CCA folder**: Appendix J one-pager, the 22-card Check-Off pack, Covering Tonight (the substitute's ten unbreakables).
- **Prototype family**: ran Weeks 1–2, loved it; three teens have led; parents praying about co-FC roles — awaiting their discernment, do not push.
- **Peer review remaining**: the no-living-joints pair (church handoff + invitation act) active; hold basket = come-and-see night, prayer hour (full design preserved in memory), serve-tier rung.
- **Andrea's Monday (08-10) meeting outcome: still unreported** — ask John gently. Consent forms + cover sheet were with her; FC-gap and recruitment were on the agenda.
- **JSFSC upload** clock still running (since 08-01); John's blue read pending.

## 3. Standing rules that bit us this week (so they don't bite twice)

- PowerPoint slide-order surgery: compute maxid BEFORE removing any sldId; always COM-verify (python-pptx forgives duplicate IDs, PowerPoint doesn't).
- `.replace` across PPT run boundaries fails silently — always render-verify text swaps.
- The deck lock dance: John closes PowerPoint before every edit round; fresh-backup HIS copy first (his format edits are in v1.5).
- Clock-vs-scripture: 6:24, 7:15, 8:28, 9:24 are verses; guard every time-shift with the book-name lookbehind.
- The diagram accent (Mission / Good Soil shaded) is deliberate — ratified, never "fix."

JD: fetch before dev pushes, as always. All queues empty at handoff.
