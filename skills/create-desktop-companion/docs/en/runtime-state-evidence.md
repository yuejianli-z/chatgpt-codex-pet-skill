# Runtime state evidence

[中文](../zh-CN/runtime-state-evidence.md)

## Name the interface before assigning triggers

“ChatGPT pet” is not an exact runtime target. Record the product, client/version, **surface**, date and evidence. Treat these separately:

| Target surface | Evidence boundary |
|---|---|
| Desktop floating pet/overlay | Public product documentation describes its activity statuses and controls. An observed drag moving the pet does not establish which sprite row plays. |
| Desktop in-chat or header avatar | Do not inherit floating-overlay triggers, gaze behavior or priorities just because the same character appears. Record evidence for this surface or unknown. |
| Web Work in-chat pet | The public Pets page distinguishes it from the desktop overlay/activity tray. Recheck the accepted format and interactions on this surface. |
| Codex CLI | Official source can establish CLI mappings only. It is not the implementation of the desktop header or Dot. |
| Interactive sample on a documentation page | Its handlers demonstrate that embedded sample. They cannot establish behavior of an installed client. |

For each proposed action record **trigger known/unknown**, evidence type (product documentation, exact-surface observation or matching implementation), scope/version, and what remains unknown. A source may verify the operation but not the animation: “drag changes position” does not prove `running-left/right`; a click that opens controls does not prove `jumping`; the presence of sixteen gaze cells does not prove pointer tracking or gaze priority. Do not invent hover/click/double-click/drag bindings from asset names.

## Three distinct counts, not one state machine

Evidence from the official pages:

1. **Four desktop business statuses.** The [official Pets product page](https://learn.chatgpt.com/docs/pets#understand-pet-status) defines Running as active chat work, Needs input as requiring approval/answer/decision, Ready as completed with unread activity, and Blocked as failure/system error. Its multi-chat priority is input, blocked, ready, running. This does not prove every interface's sprite-row binding.
2. **Nine authored animation tracks / 57 active frames.** The inspected production adapter uses the track catalog below. Frame counts are asset budgets, not durations, probabilities or mouse-event counts.
3. **Sixteen gaze poses in v2.** These are clockwise directional samples at 22.5° increments, not sixteen business states or sixteen complete action clips. Full v2 has 73 active cells. Verify the actual saved file before attributing this coverage to a character; occupied/different pixels alone do not prove correct gaze meaning.

| Track | Frames | Authored purpose, not a verified trigger | Exact-target trigger/binding |
|---|---:|---|---|
| idle | 6 | calm rest | unknown until separately evidenced |
| running-right | 8 | rightward locomotion | unknown until separately evidenced |
| running-left | 8 | leftward locomotion | unknown until separately evidenced |
| waving | 4 | greeting/attention gesture | unknown until separately evidenced |
| jumping | 5 | preparation, lift and landing | unknown until separately evidenced |
| failed | 8 | failure/blocked reaction | unknown until separately evidenced |
| waiting | 6 | request for user input/approval | unknown until separately evidenced |
| running | 6 | active processing, not foot-running | unknown until separately evidenced |
| review | 6 | completed-output review/ready-compatible performance | unknown until separately evidenced |

This is an authoring catalog, **not a proven universal nine-state runtime machine**. Keep the product fact, proposed performance and runtime binding in separate fields. For Ready-compatible performance, show work finished and the result available to view; continuous proofreading can misleadingly imply processing is still underway. Older production wording about inspection of completed output does not override the public product meaning. CLI `Review → Ready` evidence remains CLI-scoped.

The public page's web-upload paragraph lists a different/older layout from the inspected v2 production route. Do not silently collapse them into a universal format or reject a verified stored v2 merely because another entry point documents v1. Recheck the destination and identify the mismatch.

## Authored pixels, playback and labels are separate

An atlas row defines authored pixels. The host chooses triggers, playback length, repetition, fallback and gaze priority. A tooltip/activity label describes task status and is not a reliable readback of the current sprite row. Do not assign the “frequent” form to `running` merely because work is frequent. For the documented Pets state semantics, `waiting` means waiting for user approval, help or input, not generic loading or every long task; recheck the target adapter rather than expanding that meaning.

A single screenshot establishes only the visible appearance and label at that instant. Without exact source matching or playback telemetry it cannot uniquely identify idle versus gaze or another visually matching cell, reconstruct a transition, measure dwell, or prove a bug cause. Record the apparent mismatch without turning the hypothesis into a confirmed client defect.

Treat “main form most of the time,” “common,” and percentages such as 95% as design targets until measured in the actual target client. Record asset hash, client/version, observation window, representative task/interaction conditions, per-form visible durations and ambiguous/unclassified intervals. State the denominator and measurement method; a finite sample is not a guaranteed probability. Offline frame counts, simulator loops and source-row names do not establish occupancy.

When no supported live state-trigger API is verified, leave forced trigger coverage unknown. Do not claim that the bundled offline controller tests installed behavior. Preserve approved art while investigating; do not automatically redraw or reshuffle forms as a workaround. If actual host limits require an artistic compromise, explain the trade-off and obtain the scoped approval before changing it. Respect declined previews and avoid sending new preview attachments unless requested.

### Related reports, not a confirmed diagnosis

Checked 2026-10-19: first-hand Codex Desktop reports [#28995](https://github.com/openai/codex/issues/28995) and [#29196](https://github.com/openai/codex/issues/29196) describe brief work animation followed by idle despite ongoing work. [#48536](https://github.com/openai/codex/issues/48536) is an enhancement request that also reports finite `running` playback in an inspected Windows build. These are version-scoped community reports, not official confirmation of the cause in Dot or another client. They motivate checking host playback; they do not authorize patching the application or prove that a particular private screenshot has the same cause.

## Later source audit and a separate workaround

The later uploaded v3 atlas audit confirmed the intended event rows and alternate-form pixels from each row's first frame. This establishes asset mapping, not that the desktop client selected or painted those rows. There is still no observed live playback proving the originally reported missing-form symptom is fixed.

An experimental idle-row form montage introduced hard cuts and was rejected separately. Its visible jumps belong to that new workaround, not to the earlier unchanged event-row asset. Keep the two symptoms and versions distinct; do not use a rejected workaround to diagnose the original report or silently install it.

## Current production extension

Use [exposure-aware design](exposure-design.md) for design priority and presentation ordering, and [OpenAI production/delivery](openai-production.md) for the independent v2 export and post-approval installation workflow. These supplement, rather than replace, host-specific evidence and visual acceptance.
