# Line-art and faceless companions

[中文](../zh-CN/line-art.md)

## Scope and evidence

Use this branch for approved stroke-based, faceless or compound characters. These combine source-informed drawing recommendations with one separately observed, explicitly authorized visible-fill production case. That case is not proof of native playback, a substitute native-generation workflow, or a waiver for mandatory gates. The optional original path-rig teaching fixture demonstrates geometry only. Keep artwork quality, readable behavior and platform eligibility separate.

## Freeze the graphic language

Record source silhouette, line weight, head/body proportions, component ownership and contact points at native size. A visually empty head is not automatically a physical hollow tube; distinguish source pixels from a later approved transparent interpretation. Preserve intentional negative space unless the user explicitly changes that constraint. Keep the scope of any later change, such as visible interior fill, separate from permission to redraw the outline or move a companion.

Explore flat strokes or restrained shallow highlights as candidates when glossy tubing produces small-scale clutter or flicker. This is an artistic hypothesis to compare against the approved baseline, not a universal winner. Use nearby line weights with the same proportions and display height; avoid inventing a generic pixel-width target.

For an authorized unfilled path workflow, explicitly use no interior paint, stable-width centerlines, rounded caps/joins and connected shoulder–elbow–wrist or hip–knee–ankle chains. Check bends for doubled thickness and accidental tangencies. Keep limb lengths and registration stable; pose changes should not globally rescale the subject. Rasterize once through a suitable antialiased path and inspect encoded output. Repeated resizing and crisp-edge rendering can damage curved strokes. Rendering hints do not guarantee identical output across engines.

If the current native-pet workflow requires image generation, express these as reference/production constraints and inspect the generated output. Do not silently replace a required renderer or image-generation workflow with the educational rig.

## Feature applicability and expression

Before generation, fill the [state plan](../../templates/en/state-plan.md) and [structured example](../../templates/feature-applicability.example.json). Explicitly set `has_face: false` for faceless actors; do not require pupils, nose tips, mouths, eyes or eyebrows. Record features per actor so a companion's anatomy does not leak into the main actor. Unknown features are unavailable for required cues.

Run `python scripts/check_feature_applicability.py templates/feature-applicability.example.json`. Also inspect the actual generation instructions: remove incompatible template clauses rather than appending contradictory exclusions. This diagnostic checks declared structure, not arbitrary prompt text or artwork.

Use approved body construction to communicate: small head displacement relative to shoulders, connected-arm pointing, torso inclination, shoulder settling, weight shift and clear holds. Rotation of a perfectly circular featureless outline alone is not visible directional evidence. Emotional poses are proposals; verify native-size readability rather than adding facial anatomy.

For compound subjects, assign the moving and resting limbs, contact points, ground anchors and jump roles for each actor. A union bounding box cannot prove every actor is grounded or airborne. Preserve approved coordinated motion unless a change is authorized.

## Directions and motion

Author eight readable major screen-space attention poses first when compatible with the host plan. If sixteen are required, author or review the intermediate 22.5° poses; interpolation alone cannot certify distinguishability. Use connected arm, head offset and restrained torso lean together. These are attention poses, not a 3D turnaround or pupil tracking.

Keep required feet and companion anchors fixed. Review joint connections, limb lengths, silhouette openings, interior transitions and the final→first boundary. Shuffle unlabeled final frames for independent native-size direction review; record expected/observed direction and uncertainty. Watch temporal playback separately. If the required distinctions are not readable at the display size, report the limitation rather than adding anatomy or claiming a pass.

## Native-size acceptance

Verify actual runtime display size; atlas-cell dimensions are not display dimensions. While unknown, 96/128 px height can be labeled calibration views, not runtime proof. Compare against the approved character at equal height and 100% viewer zoom on white, near-black and representative mixed backgrounds. Inspect stroke continuity, open centers, separate limbs and secondary-actor readability; watch final encoded timing for shimmer, line-width pumping and pose pops. Enlarged views diagnose defects but cannot substitute for native-size review.

Maintain three independent verdicts: identity/drawing craft; action/direction/continuity; unchanged mandatory platform gates. Do not fill intentional openings without approval, conceal pixels, change alpha to game a detector, shrink features to thresholds or modify the checker. Visible user-authorized fill is a substantive art choice, not an invisible detector workaround. A line-art case that looks sound but still fails a required gate remains blocked for installation. An alternative platform requires separate authorization and verified availability.

## Checklist

- [ ] Source versus inferred anatomy, line weight, proportions and ownership recorded.
- [ ] Applicable features declared per actor; structured check and actual instruction review passed.
- [ ] No facial cues injected into faceless construction.
- [ ] Connected joints, stable lengths, clear negative space and registration reviewed.
- [ ] Actual-size stills, timing and independent unlabeled directions inspected.
- [ ] Per-actor contact and compound motion checked independently of the union box.
- [ ] Official gate results retained unchanged; visual success not used as a waiver.
- [ ] Unimplemented transfer and actual-client gaps explicitly reported.

## Sources and limits

- [W3C SVG 2 painting](https://www.w3.org/TR/SVG/painting): fill/stroke semantics, caps, joins and rendering hints; not an artistic ranking.
- [NFB animation principles](https://blog.nfb.ca/blog/2015/03/20/12-principles-animation/): staging, anticipation, timing and follow-through; character-specific poses remain proposals.
- [Blender Grease Pencil](https://www.blender.org/features/grease-pencil/): an official example of editable-stroke animation, not a required tool or verified environment capability.

No referenced character artwork, source photographs or private executed prompts are included. Code licensing does not grant character-art rights.

## Original teaching fixture

See [the bilingual path-rig specimen](../../tools/line-art-rig/README.md). Run `python tools/line-art-rig/build_specimen.py` and `python tools/line-art-rig/test_specimen.py`.  It does not cover animated playback or native-host behavior. It is original MIT-licensed educational material, not a native pet or a repaired private asset.

## Authorized background-like fill

When the user accepts opaque interior color, record the changed constraint and preserve the remaining identity: line silhouette and weight, proportions, connected limbs, companion relationship and action meaning. “Background-like” does not mean transparent or theme-adaptive. A neutral dark fill can blend into a dark background and still read as a solid shape on a light background. Show and inspect both.

A workable route keeps the outline and the compound composition, and uses generated fill pixels for the interior. One repair extracts the generated backing layer and composites the unmodified approved foreground over it, instead of accepting a redraw that changes the outline. Keep that derivation on record. Do not describe generated fill as original pixels, and do not promise exact whole-cell equality once the interior has changed.

Filling only the head is often not enough. Wide gaps between the chest, arms and a companion may also need the explicitly authorized visible backing. Keep the same aiming arm, and keep the other arm in a consistent resting position, so that arm roles do not switch with direction. Register the complete compound frame with a shared scale rather than resizing the companion on its own.

Review the fully assembled output: head fill, separations between arm, torso and companion, doubled lines, hand endpoints, every direction and each actor's jump. Run the unmodified full quality gate after compositing and chroma cleanup. A clean gap metric alone cannot approve identity or attention semantics. See the limitations in [independent gates](independent-acceptance-gates.md#authorized-visible-fill). Other designs still require their own trial.
