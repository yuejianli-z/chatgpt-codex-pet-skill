# Independent acceptance gates

[English](../en/independent-acceptance-gates.md) | [简体中文](../zh-CN/independent-acceptance-gates.md)

Generalized lessons from executed tests. Private artwork, source photographs, execution prompts, account identifiers and artifact hashes are omitted. Earlier rejected experiments and later approved results are kept distinct. Neither establishes exhaustive native runtime behavior or every possible future technique.

## Five gates, five kinds of evidence

Keep geometry, identity, direction semantics, full coverage and actual runtime separate. These five evidence categories are necessary, not sufficient for action-design acceptance. Also perform the whole-cycle state-meaning and cross-state contrast review in [action design](action-design.md) on the exact deliverable. Passing one cannot override another. An installable-format claim and installation success are narrower than full runtime acceptance; record their status separately under the target platform contract.

- **Geometry:** unchanged official structure, transparency, registration and quality checks. A supplemental diagnostic is not a substitute for the official gate.
- **Identity:** approved silhouette, proportions, intentional negative space and multi-actor relationship remain recognizable at native size and on contrasting backgrounds.
- **Direction semantics:** each requested attention direction is readable. A relaxed downward arm is not automatically a downward attention cue. Reversing the whole torso is not head-only gaze.
- **Full coverage:** every required direction and state is actually produced and reviewed. Seams, transition consistency and preserved cells must also be checked. Four cardinal anchors are not sixteen directions. Repeating anchors does not add coverage.
- **Actual runtime:** observe the intended asset, client, state entry, dwell, interruption and visible output. A local preview, a successful upload or a byte-identical stored asset does not prove host event routing.

The legacy five-field `scripts/check_acceptance_scope.py` checks declared record consistency, not complete semantic acceptance. It does not check the truth of evidence, the correctness of the supplied platform direction set, artwork, or host behavior. It never authorizes installation. The required direction set must come from the verified target contract; do not shrink it to make a record pass. See [example record](../../templates/acceptance-scope.example.json).

## Partial-direction feasibility tests

A test that replaces only some direction slots can show that a change is possible at those slots. It cannot be read as a complete new sequence. The untouched slots remain controls, and whole-set failures or discontinuities between new and old slots are not measurements of a finished set. Preserve all standard action pixels.

Two lessons follow:

- Judge changed-cell diagnostic success, identity, semantics, complete coverage and full acceptance separately.
- Filling an intentionally hollow shape, or relocating a companion, can change the design even when the gap signal disappears. A filled shape with no eyes or mouth does not keep a hollow-head identity. Stop before expanding a rejected anchor into production. Later permission for a different change does not retroactively approve a rejected pose.

## Natural occlusion and gap diagnostics

A natural pose can fold a long feature behind the body. The official extraction may pass while an unchanged gap diagnostic still reports failing rows. Occluding the feature can reduce the signal while hiding a characteristic silhouette. Separated limbs and footwear can also produce real gaps.

A feasibility test is not a complete atlas gate. Do not add hidden filler, weaken the checker, or call a reduced error count a pass.

## Alternate forms and state onset

Offline inspection can show distinct alternate-form pixels in event rows, including frame zero. Semantic form identity comes from visual review, not from hashes. Stored readback that matches the source does not show what the live client paints.

If the host paints a correct event-row frame, a later loop is not needed to reveal the alternate form. A finite-loop limit alone therefore cannot explain never seeing that form at state onset. This is a conditional inference, not a diagnosis of a host bug.

Fixtures that ignore events, or give gaze absolute priority, can produce main-form-only output from the same file, and appearance alone cannot tell the routes apart. Cycle limits and frame delays in a simulator are test assumptions, not verified host policy. Editing preview timing cannot repair an unverified event selection.

**Evidence still needed:** actual-client observation or supported telemetry that shows which row is selected, when it is painted, and what interrupts it. Until then, runtime stays unknown and approved source art stays unchanged.

## Authorized visible fill

When the user explicitly permits opaque interior colour, treat it as a new scoped visual constraint, not a change to a validator. Generate the backing with the image tool, then composite the unmodified approved foreground over it, so the outline and the companion composition are preserved rather than replaced by a generic filled figure.

Run the unchanged full quality gate on the final file, and obtain server preflight. Blind axis reviews give observations about the horizontal and vertical axes. They are not proof that every adjacent angle is equally distinct. Keep any remaining warnings rather than removing them.

Creation and storage readback can be verified. That does not prove the item is selected, that it plays on a live client, that long viewing is comfortable, or that runtime acceptance is complete.

## Final artifact and readback

Finish compositing, cleanup and encoding before the final gate. Bind every gate and review to that exact artifact. A passing precursor does not cover later paint or compositing. Inspect final pixels as well as geometry. If the source art changes afterward, rerun the affected checks and invalidate stale verdicts.

For readback, keep the encoded SHA-256 and the decoded RGBA result separate. Run `python scripts/compare_rgba.py final.png downloaded.png`. The comparator accepts single-frame 8-bit RGB or RGBA PNGs only. It rejects unsupported precision or animation rather than silently comparing a converted first frame. It checks dimensions and every R, G, B and A value, including RGB beneath zero alpha.

Equal decoded pixels support storage fidelity despite different PNG compression or metadata. Unequal file hashes alone are not an upload defect. Pixel equivalence is not runtime evidence. Keep private asset hashes and downloads outside this method package.

## Meaning can drift over time

A whole row can change meaning in a later review, even when an earlier review passed. Re-review the whole row, not only the frames already judged. A correction limited to the affected frames is a bounded action-meaning fix, not a new runtime claim. Other states still need their own semantic judgment, and a new action map remains a proposal until it is inspected and approved.
