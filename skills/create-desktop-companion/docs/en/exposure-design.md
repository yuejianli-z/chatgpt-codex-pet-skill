# Exposure-aware action design

Design the pet for repeated everyday use, not nine equally dramatic showcase cells. Use two separate records: **design attention priority** and **observed on-screen exposure**. The default priority below is an art-direction choice, not measured usage statistics or a promise that any host keeps an animation playing for a task's entire lifetime.

| Design priority | Meaning | Design intent | Avoid |
|---|---|---|---|
| 1 idle | default/rest and frequent return destination | approved core form; stable silhouette; quiet breathing/blinking or species-appropriate micro-motion | repeated whole-body transformation, large swings, flashes, distracting props |
| 2 running | thinking/processing, not locomotion | recognizable core identity and restrained, purposeful work cue | frantic loops; changing to an unrelated character; assuming task duration equals animation duration |
| 3 review | output ready to be viewed | calm completion/readiness, distinct from an input request | frantic celebration or treating every unread result as waiting for an answer |
| 4 waiting | approval, missing input or a decision needed | clear user-directed request without pressure | indefinite waving, aggressive insistence, confusing it with idle |
| 5 failed | exceptional failure/error | brief, readable disappointment or recovery cue | flashing alarms, destructive motion, unreadable exaggeration |

Waving, jumping and left/right motion form a separate **interaction group**. Their frequency depends on user behavior: a hovered pet may jump often. “Interaction” does not grant a fatigue exemption. Keep amplitudes proportionate and recover cleanly to the core rest pose.

## Future showcase order is not atlas order

New nine-action boards use this reading order:

1. idle
2. running
3. review
4. waiting
5. failed
6. waving
7. jumping
8. running-left
9. running-right

The first five follow design priority; the last four are the interaction group, not a measured frequency ranking. Use `DISPLAY_ORDER` for presentation and the immutable `ROWS` protocol for atlas assembly in `openai_pet_atlas.py`. Never move atlas rows to match the board. Keep the sixteen gaze frames in clockwise direction order, not frequency order. Existing approved GIFs do not need remaking just because this future default changes. Preserve their approved layout and background unless the user requests a revision.

## Character-specific planning

For each action record: source behavior, state meaning, exact pose/action, core/alternate identity role, intended amplitude, repetition/fatigue risk, native-size readability, return-to-idle seam, and known host binding. See the [state plan](../../templates/en/state-plan.md).

- Real animals: use characteristic or individual observed gestures while preserving anatomy; a dog may attend with ears and posture rather than human chin-rubbing.
- Known IP: use verified same-version signature behavior only when it communicates the intended state. A famous motion is not automatically a good waiting cue.
- Concepts: use conventional gestures adapted to existing anatomy. Thinking, greeting and requesting input must be distinguishable without a caption.
- Multi-form characters: keep the approved core form in idle and gaze unless the user approves an alternative. Assign rare transformations intentionally, explain their likely visibility under known host playback, and do not pretend row counts set screen-time proportions. Existing approved multi-form assets are not automatically wrong and are not silently redesigned.
- Repeated gestures: one characteristic rest pose can anchor idle, but copying it into every action destroys semantic contrast. A belly-holding idle does not justify nine belly-holding animations.

Review idle → each action → idle, including interrupted entry/hold/exit where the host supports it. Watch high-exposure designs for 30 and 60 seconds; record actual viewing, not merely a generated GIF or automated score. Do not inject large transformations into idle/gaze merely to force a low-visibility form to appear more often. Request specific visual approval for that change.

## Evidence of actual triggers

A user-observed desktop example associates pointer entry with jumping, dragging left/right with directional motion, and initial appearance with waving. A user-observed header dot example switches among sixteen gaze poses as the pointer moves around it. These are useful starting hypotheses scoped to that observed client; they are not a universal specification, and do not prove all nine rows are invoked by both interfaces.

For every destination record `surface`, `client_version`, `event`, `animation`, `evidence_kind` (unknown/user_observed/source_verified/actual_client_test), source and limitations. Unknown version should be written explicitly as “not recorded”, not silently generalized. Record task status, requested animation, currently painted frame and screen occupancy independently where observable. Read [runtime-state evidence](runtime-state-evidence.md) and [production/installation](openai-production.md).
