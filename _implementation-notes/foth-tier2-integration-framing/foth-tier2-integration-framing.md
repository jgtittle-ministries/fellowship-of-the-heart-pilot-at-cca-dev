# FotH Tier 2 — Integration framing additions

**Status:** brainstorm; not yet committed. Lives in `_implementation-notes/` so it stays out of `docs/` and doesn't break the strict build. Establishes the same `_implementation-notes/` convention FotH inherits from IJH (see [[reference-ijh-implementation-notes-convention]] in the parallel IJH repo).

**Date:** 2026-05-25 (draft 1)

**Context:** the IJH AT integration reframe landed across Vols 1–5 markdown earlier today (see IJH `task_ijh_affective_taxonomy_reframe.md`). The Vol 4 Pilot Ready restructure followed and is now end-to-end on dev and prod (see IJH `task_ijh_vol4_pilot_ready_restructure.md`). The FotH Tier 1 sweep (committed in `f0198db` dev / `0cfcce1` prod) closed the mechanical citation fixes triggered by Vol 4's restructure.

What remains is **Tier 2** — pastorally consequential places in FotH where the integration framing the IJH AT reframe established should be applied to the user's own pastoral extrapolations. None of these are *broken*; each is operationally important if FotH is going to read coherently with the post-reframe IJH state, especially for facilitators who will work in both projects.

---

## Why this work

The integration reading (Vol 4 §2 canonical home; V2.Exp7 pastoral home) is the claim that *mature formation is the held integration of all five AT stages, not the replacement of earlier stages by later ones*. The canonical Pharisee-as-stage-N-collapse diagnostic spells this out at every stage: Pharisee-Receiving = sectarianism, Pharisee-Responding = debate culture, etc.

FotH already uses the AT pervasively — for cohort goals (GS), for Companion development (GD), for a five-stage Leadership Taxonomy extrapolation (GO inviting-others-handbook Section 4). These were all written before the integration reframe was established and present the AT in the classical progression frame. Three things are at stake if FotH is updated to read in the integration frame:

1. **Facilitator-level pastoral risk.** The integrated-vs-closed Stage 4 facilitator caveat from Vol 4 §4e is directly relevant to the FotH Companion role. A Companion II or III who has closed earlier-stage openness isn't actually at that level — they're rigid, and the closure pattern reproduces in the cohorts they companion. Without the integration framing in the GD handbook, the team has no operational vocabulary for the failure mode.

2. **Coherent reading across IJH and FotH.** Companions who work in both projects will read the AT in the integration frame in IJH and the progression-only frame in FotH. The discontinuity will be noticeable, and the integration reading is operationally more truthful.

3. **Leadership Taxonomy extrapolation is new theological work.** The GO inviting-others-handbook Section 4 explicitly says: "This is new theological work for the IJH project. The five Leader Levels are extrapolated from the Affective Taxonomy as it is established in Vol 2 and Vol 5." If the IJH AT is now read in the integration frame, the Leadership Taxonomy extrapolation needs to extend in the same frame to stay theologically consistent.

---

## Three surfaces — proposed scope per surface

### Surface 1: GD handbook Companion I/II/III levels — **HIGH leverage**

**Where:** `docs/going-deeper/handbook.md`, lines ~296–328 (the "three levels of Companion development" section through "Hearing and obeying — the developmental spine" section).

**Current state:** The three Companion levels are presented with AT floors (Stage 3, 4, 4+). The section already has integration-friendly framing at the "developmental spine" paragraph ("scriptural engagement and hearing-and-obeying God are NOT prerequisites...they are the developmental spine...continue to develop across all three levels"). What's missing is the **explicit closure-pattern naming** — that a Companion at any level whose earlier-stage capacities have died is not actually at that level.

**Proposed addition:** a new paragraph (or short sub-section) under "The three levels" or as a closing note to the section. Probably 4–6 sentences. Names the closed-Companion failure mode at each level, points to the "Every Companion has a Companion" supervision relationship at line 330+ as the operational detection point, and cross-references the IJH Vol 4 §4e treatment for facilitators wanting the construct-level frame.

Draft language sketch:

> **Integrated vs. closed at each level.** The Companion levels above name what each level *adds* — they do not name what would happen if a Companion lost what an earlier level required. The IJH integration reading (Vol 4 §2 and §4e) makes this explicit: a Companion II or III whose Stage 1 Receiving has died — who is no longer genuinely open to a new word, to a peer challenging them, to a pilgrim's hard question they did not see coming — is not actually at Level II or III. They have collapsed into a rigid version of the role. The pattern reproduces in the cohorts they companion (a closed Companion III forms a closed cohort). The Companion's own Companion (the supervision relationship described in the next section) is the primary place where this is detected and addressed; it is the practical operational meaning of "every Companion has a Companion" and one of the strongest arguments for why that relationship is non-negotiable.

### Surface 2: GO inviting-others-handbook Section 4 Leadership Taxonomy — **MEDIUM leverage**

**Where:** `docs/going-out/inviting-others-handbook.md`, Section 4 (lines ~195–298).

**Current state:** Fully-developed five-Leader-Level extrapolation, with State / Sower parallel / What they need framings for each level. Currently reads as classical progression. Already has one integration-friendly principle at line 295: "Progress is spiral, not linear. A leader at Level 3 in their primary group may be at Level 1–2 when they encounter a different kind of room." This is congenial but framed as "returning to earlier levels under new conditions" rather than "earlier levels remain alive."

**Proposed addition:** a brief opening framing note before "The five Leader Levels" header AND an "Integration check across the levels" sub-section before "What Inviting Others is realistically aiming at." The opening note frames the levels as integration not replacement; the closing sub-section gives the Leader-Pharisee-as-Level-N-collapse diagnostic in leadership vocabulary.

The Leader-Pharisee-collapse pattern is worth working out in the leadership register specifically:

- Leader Pharisee-Receiving collapse: dismisses what a cohort member or peer leader brings — "I don't need to hear that"; the leader has stopped being genuinely open to surprise.
- Leader Pharisee-Responding collapse: every engagement returns to defending the leader's framework rather than working the substance of what was raised.
- Leader Pharisee-Valuing collapse: leadership-as-status — visible leader-discipline that establishes status with the formation community rather than serving it.
- Leader Pharisee-Organization collapse: leadership-as-system — rule-following / curriculum-running replacing leadership-from-formation. (The Section already names "curriculum-runner" as the failure mode at Level 3 in its current language; this connects to the existing prose.)
- Leader Pharisee-Characterization collapse: settled rigidity in leadership identity — the leader has stopped surprising anyone, including themselves; their groups become closed because the leader has.

This is also where the user's own theological work could either incorporate or reject the integration extension. The Section's own caveat — "presented here as a working frame; the Council and the broader IJH community should test the frame across the next several Inviting Others cycles" — leaves room for the integration extension to be presented as a *next move* in the working frame rather than a definitive resolution.

### Surface 3: GS handbook AT goals by cohort — **LOW leverage**

**Where:** `docs/getting-started/handbook.md`, lines ~85–93 (the "Affective Taxonomy goals by cohort" section).

**Current state:** Per-cohort targets (Junior to stable Level 2; Senior toward threshold of Level 3; Parents move at least one full level). Already framed honestly — "we are not trying to push every participant to Level 3 in ten weeks." Doesn't presume stage replacement; reads as realistic targets within the program.

**Proposed addition:** a single sentence or short note at the end of the section, framing the targets as "stable integration at that level" rather than "passing through that level." Light touch — the GS register is introductory and the audience (parents and youth pastors orienting kids to the program) doesn't need the integration framing exposed in detail. Probably 1–2 sentences.

Draft language sketch:

> The goal at every cohort is *integration* at the target level, not just touching it — a participant who reaches Level 2 (Responding) with genuine Level 1 Receiving still alive is sturdier than a participant who has skipped past Level 1's openness in order to perform Level 2's engagement.

---

## Sequencing recommendation

Three surfaces with very different leverage. Options:

- **(a) Single Tier 2 pass covering all three.** One dev push, one mirror cycle. Cleanest result; biggest single diff.
- **(b) Two passes: GD-handbook Companion levels first (highest pastoral leverage), then GO Leadership Taxonomy + GS AT cohort goals together.** Lets the user see the highest-impact change land and read it before the more substantive Leadership Taxonomy extension.
- **(c) Three separate passes, one per surface.** Maximum review granularity; most cycles.

My lean: **(b)**. The GD handbook addition is the single most operationally consequential change in this Tier — the closure-pattern naming for the Companion role is what gives the team operational vocabulary for the failure mode the IJH §4e caveat names. Worth landing on its own so the user can read it on dev before the Leadership Taxonomy extension (which is more substantive theologically and where the user's own extrapolation may want to be adjusted in light of how the integration reading looks in the leadership register).

Estimated scope per pass:
- Pass 1 (GD handbook): ~6 line addition (one paragraph). Surgical.
- Pass 2 (GO Section 4 + GS handbook): ~25 line addition in GO inviting-others-handbook + ~2 line addition in GS handbook. Medium.

---

## Open design questions

1. **Should the GD handbook addition use the V2.Exp7 "Reading these Levels as Integration" header style** or fit into the existing sub-section structure? The IJH precedent (V2.Exp7 + Vol 4 §2) is the explicit "Reading these Levels as Integration, Not Replacement" header. FotH's GD handbook is more pastoral and a discrete header may be heavier than the section needs. My lean: keep it as a `**Integrated vs. closed at each level.**` bold-lead paragraph under "The three levels," not a standalone header.

2. **For the GO Leadership Taxonomy, should the integration framing be in an opening note + closing sub-section, or distributed as one-line notes at each Level?** Distributed reads more naturally for a reader working through the levels in order; opening+closing keeps the existing Level descriptions clean. My lean: opening framing note + closing "Integration check" sub-section. Matches V2.Exp7's structure.

3. **Should the Leader-Pharisee-collapse diagnostic be presented with the same Pharisee vocabulary used in IJH**, or in pure leadership vocabulary (closed-leader, rigid-leader)? Pharisee vocabulary is theologically precise but may carry charge in some FotH-adjacent church contexts (CCA is Reformed-evangelical; some readers may find "Pharisee" framing pointed). Pure leadership vocabulary is lower-charge but loses the theological precision. My lean: use "Leader Pharisee-Receiving collapse" etc. in the Section 4 addition since the Section already does extensive theological framing and the Pharisee language is what makes the diagnostic precise. Note in the draft that this can be softened.

4. **Should the GD addition cross-reference Vol 4 §4e by name and link**, or stay self-contained? Cross-referencing IJH directly is the IJH precedent (V2.Exp7 links to Vol 4 §2 and back). For FotH, cross-referencing into IJH is consistent with the DP-4 audit pattern. My lean: include a brief "(see IJH Vol 4 §4e for the construct-level frame)" parenthetical.

5. **Should this work also update the GD handbook Appendix C "Three Taxonomies" disambiguation note** (referenced in the CHANGELOG at line 62) to mention integration framing? The Three Taxonomies note disambiguates Affective / Group Level / Leader Level when a session reference says "Level 3." Adding a brief integration framing across all three taxonomies might be a natural fit. Likely a small addition (~3 lines). Could fit in Pass 1 or Pass 2.

---

## Next steps (your call)

1. Read this draft.
2. Settle the open design questions (especially #3 Pharisee vocabulary and #5 Three Taxonomies note).
3. If you approve the direction and sequencing, Pass 1 (GD handbook Companion levels) is the smallest viable first move.

Nothing committed beyond this brainstorm. The actual FotH Tier 2 changes are substantive enough that the brainstorm-doc-first pattern from the SIP / Vol 4 restructure work feels right here too.
