# Identity-preserving focused repair

[中文](../zh-CN/focused-repair.md)

Use this method when an approved character has a localized defect: a gaze pose, an accessory, or a silhouette detail. It does not require regenerating the whole character, and it does not change the identity that was already approved.

## 1. Freeze scope before editing

1. Keep the approved source and every rejected candidate. Record the artifact hash, the editable cells, the protected cells, the identity landmarks, and the registration anchors.
2. Freeze the approved pixels of every protected cell, not just a description of its appearance. Check equality again after cleanup and after final assembly.
3. Describe the small accessory by its attachment point, scale, count, and branch structure. A replacement that looks pleasing can still be the wrong identity.
4. Do not enlarge the head, the crown, or an accessory just to make it easier to generate.

## 2. Repair the smallest coherent unit

Common failures:

- A full gaze redraw loses a small identifying detail, or inflates it.
- A focused attempt attaches the detail to the wrong place, such as the wrong body height.
- A pass still fails a mandatory gate, even though the picture looks plausible.

Repair method:

- Anchor the attachment point and the local silhouette first. Verify that correction on one pose before propagating it to the related poses.
- Change only the region, and only the pose constraints, that the defect justifies.
- Keep failed attempts. Stop repeating a root hypothesis that has already failed.
- The exact detail, palette, and pose from one case are not defaults for other characters.

## 3. Decode and register without collateral changes

- Verify the adapter's required source key color for the current host. Do not substitute another key color, and do not generalize one color to every host.
- Register corrected poses to the approved anchors and the documented scale and offsets. Check for accidental cell shifts and clipping. Check body and feet stability and accessory placement separately. Exact cell registration does not prove that newly generated pixels are identical.
- Apply chroma cleanup only to the rows you changed. Re-insert protected rows from the original.
- Do not change alpha, opacity, mandatory checkers, or thresholds to obtain a pass.
- Inspect cleaned edges at native size on white, gray, and black backgrounds, and at enlarged size for diagnosis. A clean mask alone does not prove identity or direction readability.

## 4. Separate acceptance layers

1. Run the current mandatory structural, chroma, and quality gates on the exact final file.
2. Review every changed cell against the approved identity.
3. Use blind direction reviews without the answer key, then compare the observations with the key afterward. A primary reviewer must also check identity and boundary transitions. Blind direction recognition cannot replace identity review.
4. Keep the local gate results, the server preflight, any pet creation or selection, visible user feedback, and full runtime verification as separate records. Selecting a pet is not proof of every host state or dwell duration.

## 5. Record limitations

If a boundary between two poses still shows a visible change, record it as a limitation. Do not describe it as seamless interpolation, long-view comfort, or full runtime acceptance. Keep that limitation in every later handoff until it is retested.

## Repair checklist

- [ ] Approved source and editable/protected cells recorded.
- [ ] Protected pixel equality checked after final assembly.
- [ ] Attachment point, proportions, and identity checked for each changed pose.
- [ ] Source key verified; cleanup limited to changed cells; alpha preserved.
- [ ] Registration, clipping, body and feet, and native-size edges on white, gray, and black checked.
- [ ] Mandatory gates passed on the exact final file; no bypass and no changed checker.
- [ ] Blind direction reviews and the separate identity/boundary review recorded.
- [ ] Creation, selection, and user feedback recorded separately from runtime evidence.
- [ ] Boundary transitions and untested contexts recorded as limitations.

## Related methods

- For faceless or stroke-based characters, see [line-art and faceless guidance](line-art.md).
- For what counts as runtime evidence, see [runtime state evidence](runtime-state-evidence.md).
- For the gate that decides acceptance, see [independent acceptance gates](independent-acceptance-gates.md).

This document describes generalized methods only. It contains no private artwork, no executed prompts, and no identifiers. Code licensing does not grant rights to any character artwork.
