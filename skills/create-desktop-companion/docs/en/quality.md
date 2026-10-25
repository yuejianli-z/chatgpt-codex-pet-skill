# Quality, repair, and timing gates

## R04 — Review every changed cell against the approved identity

Before repair freeze the latest task-relevant approved source, cell map, hashes, allowed changes, and comparison protocol. Enumerate every changed cell; for each show the approved reference beside the same/nearest view of the result, enlarged and at native size. Record stable ratio landmarks, silhouette, eye/mouth or core-component geometry, outfit/accessories, reviewer, evidence, and verdict. A machine can require these fields and exact changed-cell coverage; it cannot verify likeness. Sixty-seven unchanged cells do not approve six changed faces.

Check protected cells separately with decoded-pixel hashes; distinguish encoded-file hash from decoded-pixel hash because metadata/re-encoding may change bytes. For pure integer translation record dx/dy, identical visible RGBA after translation, and no clipping. This is not unchanged whole-cell coordinates or equal whole-cell hashes, and proves no new animation. Re-extract the final deliverable for regression rather than inspecting only a good source file.

## R05 — Require character-specific action and truthful measurement

Before generation, complete the source-led [action design](action-design.md). A sustained state needs a concrete performance whose meaning survives every phase. Thinking must remain thinking, asking must address the user, idle must stay calm, and failure/review must remain distinguishable. Review unlabeled full cycles and compare the confusing states at target size; record the observed action, addressee and ambiguous phases, not merely a planned intention or a recognized first frame.

A sustained performance uses entry → living hold → return to the same semantic cue, not automatically generic neutral. Event recovery and cross-state transition anchors are separate design decisions. Low amplitude alone does not establish calmness or meaning. Do not swap gestures every second or label a translated still, crossfade, higher FPS, or reflection flicker as breathing, articulation, or wheel rotation. Distinguish unique source poses, pose hold durations, and encoding/refresh rate. A whole-actor jump can contain translation, but requires actor-specific takeoff/airborne/landing evidence; it does not establish internal articulation.

Maintain shared camera, scale, and contact/hover anchors across a sequence. Never fit, center, scale, or ground every frame independently: this produces size pumping and erases jumps. For a rider/mount, measure the jumping actor separately from the grounded mount; composite bounding-box minima cannot disprove the actor's jump. Connected pixel components are not anatomical limb counts. Faceless attention/pointing is not eye gaze; retain approved anatomy and ownership of limbs.

For variable-spacing strips extract complete components using verified masks before mirroring, not equal-width slots or expanded rectangles containing adjacent limbs. Asymmetric accessories and anatomical-side eye colors prohibit naive mirroring. Use one scale/anchor across all direction rows. Directional attention is not whole-body yaw. Source pixels distinguish intended negative space, background sealed by mixed edges, extraction damage, and truly missing anatomy. Preserve original diagnostic failures even after a local alpha repair; a local improvement cannot silently turn the overall verdict into pass.

## R08 — Inspect pose AND velocity continuity

At actual timing view several complete loops, then inspect the final two and first two frames together. Check pose, support/contact, direction and magnitude of velocity, accessory lag, and intended pauses. Equal first/last pictures are neither necessary nor sufficient. A schedule repair cannot repair a source-pose or velocity seam. Check entry/hold/exit interruptions separately where the host actually permits them; record source phase, destination, trigger, and observed runtime behavior. Offline hard cuts demonstrate possible risk, not actual host switching behavior. If triggers cannot be controlled, mark runtime interruption untested.

## R09 — Define the scheduler and encoded tail exactly

Use positive integer source-frame holds in milliseconds. For each row, period P is the sum of its holds. At time t, select the unique frame whose half-open cumulative interval contains t modulo P. Rows keep independent phase; do not reset one whenever another row changes. For an exactly repeating board choose master M divisible by every row period, or explicitly redesign timing with approval where required. Do not truncate a source loop merely to fit a short board.

Worked offline schedule: M=12,000 ms; gait holds [160,140] repeated four times give P=1,200 ms; work [500] repeated six times gives P=3,000 ms; an event timeline [1,000,2,000,9,000] gives P=12,000 ms with neutral holds around the event. These are diagnostic/example values, not measured host defaults. An imported 1,060 ms gait does not divide either an 8,000 ms or 12,000 ms board; 1,200 ms is a new timing proposal, not its original period. If original timing must remain, use an appropriate common multiple or a non-looping clearly labeled excerpt.

Verify decoded PTS and each displayed frame's hold: first PTS=0; all holds positive; PTS[i]+hold[i]=PTS[i+1]; last PTS+last hold=requested duration. Encoder duration flags alone are insufficient, especially for variable frame rate. At 50 fps, a 12 s constant-frame-rate file has 600 frames, last PTS 11.98 s and last hold 0.02 s. The 30 s and 60 s diagnostics have 1,500 and 3,000 frames, respectively. Repeated encoded frames are not new source poses. Compare GIF/source timing with MP4 first/last frames and holds; report quantization or tail differences.

## R10 — Actually watch 30 and 60 seconds

For each high-frequency state, conduct actual timed 30-second and 60-second viewing at the host's display size. Record reviewer, exact asset hash, size, actual watched duration, anomaly timestamps, repetitive beat, closed-eye share, gesture density, and reading distraction. Unknown size uses labeled 64/96/128 calibration, not claimed host validation. Generated, decoded, sampled, or partially watched diagnostics do not satisfy a complete timed viewing. Historical diagnostics passed encoding checks but lacked complete timed-viewing records; long-duration comfort remains unverified.

## R11 — Keep separate verdicts and honest evidence

Report coverage, structure, visual/identity, timing/playback, runtime, and rights separately as pass, warning, fail, unchecked, or blocked. Cancellation is a task state: stop work and do not count it complete. A complete asset candidate is not all-gates-pass, final user approval, installation, or public permission. Preserve original failed reports, counterexamples, and unresolved warnings.

Freeze reference, view, normalization, success criteria, and blind-review board/key hashes before testing. A newly randomized board needs its own key and review; old answers remain bound to the old pair. Never edit reviewer answers, remove failing states, or widen thresholds after seeing results merely to obtain pass. New evidence may justify revised criteria only with the old conclusion retained and the same input re-evaluated. Hashes, bounding boxes, optical flow, frame differences, alpha topology, and schemas locate issues; they cannot certify identity, comfort, meaning, or user preference.

## Identity-safe presentation and character rationale
Follow [identity and presentation](identity-and-presentation.md). Layout acceptance does not approve character art. Review anatomy, tail topology, natural occlusion, all attention directions, representative cover indices and the actual encoded final file independently. Each character needs its own concise rationale and signature details. Preserve approved transformations and newer approved actions; never transfer old-asset defects or passes across unverified lineage. This is a visual/production requirement, not an extra machine acceptance claim.


## Cross-row scale registration before mixing sources

A newly extracted strip passing its own row checks does not mean it can be mixed with an older atlas at the same nominal multiplier. Extraction may have used a different scale or anchor. Review state changes between the approved idle/reference row and every new row before accepting the combined atlas or showcase.

Use an approved neutral or comparable pose as the identity anchor. Compare stable head and torso feature dimensions, body proportions and the intended foot/contact or hover anchor at a shared physical scale. A frame's overall bounding-box height may grow because a paw, wing or tail extends or a jump leaves the ground; it is not a reliable standalone measure of identity scale. If no comparable pose exists, record that uncertainty and use multiple stable landmarks rather than forcing equal height.

Preserve the original extracted frames and their extraction scale/translation. When a source group is consistently oversized or undersized, apply one documented shared scale and registration transform to that complete group, aligned to the reference contact anchor. Keep the same transform across its frames and any rows that share that source registration. Do not fit each frame to its own bounding box, normalize all poses to identical height, or erase airborne displacement. If the mismatch is inconsistent within a group, correct the extraction or source artwork rather than concealing it with per-frame fitting.

Record source version/hash, original extraction transform, reference neutral frame and landmarks, measured feature sizes with units, selected group scale/translation, anchor, affected frames, and final registered source hashes. Recheck idle → each changed row → idle, identity at normal display size, contact/airborne motion, and loop seams. Separately inspect the actual encoded output after composition. A numeric scale correction is evidence of registration, not an automatic verdict on anatomy, likeness or semantic quality.
