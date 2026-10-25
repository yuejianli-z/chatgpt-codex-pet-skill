# Design actions before generating them

[中文](../zh-CN/action-design.md)

Use this branch before new action batches or a semantic redesign. Keep approved appearance, proportions, material, costume and existing accepted motion frozen unless the user changes that scope. This is action direction, not a mandate to redraw every saved character.

## What the earlier method missed

The earlier workflow asked for “one intention” and signature behavior but did not turn a character's source material into a concrete state plan before generation. Generic production menus such as “thinking, typing, scanning, busy paws or purposeful bobbing” delegated the central design decision to image generation. A recognizable first pose, good geometry or a complete row could then hide an incoherent cycle. Some manually tailored performances were already useful; inspect each actual version instead of condemning or replacing everything.

## 1. Build the action bank from the correct source tier

1. **Real animal or personal pet:** start with observed individual habits when available, then species-typical behavior from credible ethology, veterinary or zoo sources. Record what the body actually does and its context. A cat's kneading may be characteristic, but is not evidence that it means “thinking.” It is not categorically forbidden as a metaphor; reject or revise a particular proposal if it reads as comfort/idle rather than the chosen work cue. The transfer to an interface state is a design proposal, and must remain anatomically natural. Do not give every animal human hands or make every animal wave.
2. **Known IP or recognizable meme:** identify the exact character/version first. Inspect official character/game footage, animation, creator material or a traceable original clip for distinctive performances. Record source, observed phases and timestamp only if actually viewed. A signature attack, dance or transformation is not automatically appropriate for quiet work or approval. Adapt the portion that fits the state; label the adaptation, not “canonical thinking” when the source only shows combat. A still establishes pose/identity, not the motion between frames. If provenance cannot be verified, say so and use an explicitly proposed fallback rather than inventing canon.
3. **Concept or source-poor avatar:** use a familiar, legible state gesture adapted to its existing anatomy and personality. Thought, request, rest, failure and review must look different for a reason. Source-poor does not mean generic visual redesign, and a personal avatar is not automatically an IP. Use only existing limbs, face, equipment and mechanical functions. Propose a new prop or expressive feature separately if truly necessary; do not smuggle it into a motion prompt.

These are three **action-source routes, not three states**. Choose the route that fits this character; fallback remains available when a natural/canonical action does not fit the interface meaning. This is not a quota of clips or a requirement to shoehorn a famous action into every state. Mix natural/canonical evidence with clearly labeled fallback where a particular state lacks a suitable source. Record `observed behavior`, `canonical performance`, `adapted proposal`, or `conventional fallback` per action, with what remains unknown.

## 2. Make the state mean one thing

Read the actual host state contract. Technical keys, task labels and visible performances are not interchangeable. In the dated Pets example, `running` is active work, while `running-left/right` are locomotion. If the chosen work performance is thinking, its whole loop must stay thinking; do not switch to greeting, shrugging, approval, celebration or generic idle halfway through.

- **Idle/rest:** a calm baseline with quiet natural maintenance such as breathing. It is not repeated attention-seeking, a random gaze tour, or a montage of favorite gestures.
- **Active work/thinking:** sustained engagement with one problem or task. Pick one concrete action and a stable attention target. Anatomy-compatible thought cues are options to choose from, not a menu to paste into generation. Returning to the loop start must retain the thought cue, not repeatedly announce task completion.
- **Waiting for input/approval:** address the user with a patient request, then visibly await the response. Specify the addressee and request cue. Mere inactivity, sleep, self-inspection or an undirected head tilt is insufficient. This is asking for approval, not displaying that approval was already granted.
- **Failed/blocked:** an interrupted or discouraged attempt followed by a readable blocked condition or bounded recovery. Do not confuse it with a jump, ordinary rest, or triumphant completion. Avoid inventing injury/distress for a real pet merely as a status metaphor.
- **Review/ready:** establish the host's exact fact before choosing the performance. In the dated Pets 0.1.6 production contract this is inspection of **completed output**, also called ready/completed-output review; it is not another round of ongoing processing. A bounded look at the result followed by a settled ready posture can be proposed, with the attention target explicit even when off-frame. A thumbs-up or nod is not globally forbidden: judge whether the actual sequence reads as completed-output review/ready, rather than mere greeting, celebration or permission already granted. Keep it distinct from active work and waiting for user input; do not prescribe continuous scanning as a universal review gesture.
- **Greeting, locomotion and jump events:** select species/character-specific mechanics with actual support and recovery. A famous action may fit here better than a sustained work loop. For a car, moving reflections are not rolling wheels; a body bob is not a plausible jump. If a host-required event is incompatible with a realistic design, state the conflict and obtain an explicit stylization decision rather than fake compliance.

**Contract evidence and limit.** The [official Pets product page](https://learn.chatgpt.com/docs/pets#understand-pet-status) defines desktop Ready as a completed chat with unread activity. Design for “the result is ready to view,” not continued processing. The production adapter's completed-output inspection wording can inform a small result-attention cue, but must not override that product meaning. A verified CLI `Review → Ready` mapping does not prove an in-chat/header/overlay binding. Read [surface and trigger evidence](runtime-state-evidence.md) and label each unverified binding unknown.

For a faceless actor use connected arm pose, head/torso orientation and weight, not borrowed eyes or mouth. For a vehicle use existing mechanical/light signals only where supported by the approved design; acknowledge if “thinking” versus “review” cannot be made unambiguous without a new visual convention. Do not infer intent from arbitrary chassis rocking. For compound subjects assign each actor a role, with one clear semantic lead, while preserving their relationship.

## 3. Approve the action map, not a new art style

Before bulk regeneration, inspect existing prompts and final source rows. For each character identify what can be retained, what has a demonstrated semantic defect, and what is still unreviewed. Prompt intent is not proof of the resulting artwork. Keep exact version/evidence privately.

Show a concise [action proposal](../../templates/en/action-proposal.md): character, source tier, proposed action for each host state, why it communicates the state, evidence/adaptation label, and changed/retained/unknown status. Put the few real trade-offs in plain language. This review concerns motion design; do not reopen already approved appearance or run every character through style selection again. Without authorization for the affected production scope, keep the proposal pending. If a later instruction explicitly authorizes an ordered character remake, show the concise character-specific mapping and proceed within that scope without inventing a new mandatory approval wait. Reconfirm only a material scope/identity change or unresolved decision that actually needs the user; retain per-character semantic review.

Choose representative samples that resolve the highest semantic risk, usually the easily confused idle/work/request/review group, before producing the remaining rows. A complete batch is not the cheapest way to learn that a proposed action reads as something else. If the user requests a large design board first, label it with the [board template](../../templates/en/action-board.md); one pose per track is design coverage, not complete animation coverage.

## 4. Compile a concrete performance brief

Use the [generation brief](../../templates/en/generation-brief.md) after selecting the action. Specify one action, intended state, addressee/attention target, moving and fixed parts, and ordered phases. Describe the chosen movement directly; remove conflicting generic action clauses instead of appending an override beneath them. Preserve genuine executed prompts unchanged and label future briefs as unexecuted until used.

A sustained row has entry into the cue → living hold with one small evolution → return to that same semantic cue. Its loop does not need to return to generic idle. An event can have preparation → action → recovery, but recovery must not imply a contradictory task result. Host cross-state transitions remain a separate problem; do not erase meaning to make every endpoint neutral.

The frame budget limits how much performance fits. Simplify the selected action instead of packing thought, pointing, shrugging and smiling into six frames. Do not add stage props, facial anatomy or costume changes to rescue an underdesigned brief.

## 5. Judge meaning over the whole cycle

Review the final encoded row without a state label, at the intended display size, then alongside the confusable states. Ask what the character is doing, whom it addresses, and where that interpretation changes. Record actual observations and ambiguous phases; do not lead reviewers with the intended answer. First-frame recognition alone does not pass a loop. Check the final→first boundary for semantic as well as physical continuity.

Compare observed action with the chosen source and adaptation boundary. The questions are: does this look like this character; does it communicate the intended state throughout; and is it distinct from the neighboring states without text? Natural behavior need not literally carry a human mental state, but the interface metaphor must be readable and honestly labeled. If ambiguity remains, revise the action choice, not the label, validator threshold or reviewer answer.

Record separate verdicts for source fidelity, anatomy/identity, state meaning, cross-state distinction, whole-cycle consistency and actual-client behavior. No JSON schema, motion metric, direction test or passing upload can certify these semantic judgments. Use [state planning](../../templates/en/state-plan.md) and [delivery review](../../templates/en/delivery-review.md) to retain evidence without inventing pass counts.

## Animation principles that inform these choices

[Frank Thomas and Ollie Johnston](https://frankanollie.com/KeysToEmotion.html) emphasize clear, simple character intention; [Dave Burgess](https://www.animationmentor.com/blog/timing-the-12-basic-principles-of-animation/) explains giving main poses time to read, and [Shawn Kelly](https://www.animationmentor.com/blog/why-all-animators-need-to-master-the-moving-hold/) explains a living hold. Applied here: one dominant action, a legible silhouette/attention target, and small supporting motion within that intention. These are design principles, not an authoritative dictionary assigning animal/IP gestures to software states. Do not import film timing or UI transition durations as unverified host playback settings.

## Identity-safe presentation and character rationale
Follow [identity and presentation](identity-and-presentation.md). Layout acceptance does not approve character art. Review anatomy, tail topology, natural occlusion, all attention directions, representative cover indices and the actual encoded final file independently. Each character needs its own concise rationale and signature details. Preserve approved transformations and newer approved actions; never transfer old-asset defects or passes across unverified lineage. This is a visual/production requirement, not an extra machine acceptance claim.

## Current production extension

Use [exposure-aware design](exposure-design.md) for design priority and presentation ordering, and [OpenAI production/delivery](openai-production.md) for the independent v2 export and post-approval installation workflow. These supplement, rather than replace, host-specific evidence and visual acceptance.
