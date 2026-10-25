---
name: create-desktop-companion
description: Design and review consistent desktop companions from pet photos, existing characters, memes, original concepts, or approved sprites. Confirm identity and style, preserve approved artwork during motion repairs, map behavior to verified host capabilities, and deliver evidence-backed previews without claiming untested runtime support.
---

# Create Desktop Companion

Version: 3.3.7. English is the canonical operational specification; the bundled `docs/zh-CN/` files carry the same per-topic rules in Chinese. This is an assistant workflow and diagnostic toolkit, not an image model or platform API. It includes an independent OpenAI v2 atlas assembler/validator/preview adapter, but not a universal compositor or credentialed pet installer.

## Core principles

1. **Verify the target first.** Confirm the exact product, client version, and display surface before making art. An unconfirmed capability is unknown, not supported.
2. **Lock identity once, then protect it.** Approve style and identity, then keep them fixed. A motion fix never redesigns the face or body.
3. **Keep four facts apart.** Structurally valid, visually approved, installed, and running on a real client are four different facts. State only the one you actually have.
4. **Take actions from the character's own source**, not from a generic gesture list.
5. **Say what you did not test.** If you did not watch it, install it, or confirm the trigger, say so.

The workflow runs in this order: verify the destination → establish identity and style → design actions → review motion and exports → deliver with honest evidence. Read only the branches relevant to the request. Do not make users complete a large questionnaire. When information is thin, ask rather than guess (see R3).

Local atlas validation is structural only. Without current eligibility evidence, deliver a candidate, not an installation-ready claim. Read [OpenAI production](docs/en/openai-production.md) before any native import.

## Workflow rules

### R1 — Verify the platform foundation

- Identify the target product, client version, and accepted asset type before committing to a style or animation budget.
- Name the exact surface: desktop floating pet, in-chat or header avatar, web Work pet, or another verified target. Do not stop at the application name.
- Record the current authoritative format and state requirements. Keep these separate: host hard constraints, mandatory production gates, heuristic diagnostics, preview settings, and observed runtime.
- A missing capability is unknown. Concept-only work may continue with an explicit integration gap, but stop any dependent import or activation claim.
- Track displayable, format and production-ready, installed, and runtime-accepted status separately, each tied to the exact artifact and client version.
- A local quality error is not evidence of a server rejection or a content prohibition. Preserve the approved artwork and the original failed report, and classify the cause before editing.
- Never change a bundled gate, remove a report field, or fill intentional negative space just to pass.
- A later explicit approval of visible fill changes only that visual constraint. Keep the earlier rejected result, and review the new design against the new scope.
- Required failing gates stay blocking until they are resolved through a supported route.
- A diagnostic false-positive reproduction does not certify the actual character.
- Read [platform foundation](docs/en/platform-foundation.md) and complete its checklist before integration.

### R2 — Native-first portability

- Detect the actual target product, version, and display surface before producing art.
- Prefer an existing, verified native pet import route.
- Treat skill readability, asset export, and native runtime acceptance as three independent capabilities.
- Preserve approved identity in target-neutral clips: transparent source frames, frame durations, anchors and baselines, loop semantics, and separate action and gaze meanings. This is authoring guidance, not an interoperable schema.
- Compile an exact host export only against a verified contract. Do not impose one host's track count, gaze sample count, or atlas dimensions on another host. Disclose resampling, missing directions, and other conversion losses.
- This toolkit does not include a universal exporter or a new platform adapter.
- Test the intended renderer and host version before promising identical artwork or animation. One host's drawing surface, element tree, or capability set does not transfer to another.

### R3 — Inputs and questions

- Accept a name, an original description, an ordinary photograph, a low-resolution meme, a video, multiple references, or an existing approved atlas.
- Preserve the original input. Additional references are supplements, not replacements, and cannot make a failed original-input test look successful.
- Ask only for information that changes the outcome.
- For an established public character, default to at least three useful references from the same version, each showing distinct identity, structure, or action evidence. If fewer exist, disclose the gap and limit your claims. Do not invent evidence or silently substitute versions.
- Private photos, original concepts, and genuinely unavailable public characters do not need a reference quota.
- **When the input is thin, or the character is named but not shown:** search for candidate reference images yourself and show them to the user before generating anything. Ask "is this the one you mean?" Do not guess silently, and do not stall waiting for the user to supply more. If several versions exist (a game skin, a redesign, a regional variant), show the distinct candidates side by side and ask which one. Once the user confirms, lock that reference and stop re-asking.

### R4 — Identity and names

- Resolve ambiguous names, versions, tools, and references before production.
- Separate official names, community aliases, user-chosen names, and transliterations. Do not invent an official English name.
- Record observed features, inferences, and proposals separately. An unseen rear marking is not verified anatomy.
- See [workflow](docs/en/workflow.md).

### R5 — Capability preflight

- Verify readable inputs, public research, image-generation or editing access, local execution, actual playback, and optional host import as separate capabilities.
- Run `python scripts/preflight.py` for local prerequisites. It does not verify cloud providers.
- Use available lawful tools. No provider, credentials, official Pets implementation, or complete board renderer is bundled.
- If a capability is missing, stop only the dependent stage, and name the deliverable you can still produce. See [installation](docs/en/installation.md).

### R6 — Style gate

- For a new or materially changed visual style, show three distinct candidates. Hold identity, pose, expression, camera, and outfit meaning constant; vary only the style.
- Include enlarged views and actual desktop-size views. If the host size is unknown, use 64/96/128-pixel-height calibration previews and label them as calibration, not host measurement.
- Obtain the specific style choice before locking the canonical reference and before batch production.
- An exception needs an explicit waiver for this character and this style choice, or an exact reuse of an unchanged approved baseline.
- A broad "finish everything" delegation is not a waiver.
- A high-resolution master does not need high detail density.
- Adapt the style to the character: realistic animal, soft 3D, flat sticker, ink, or source-faithful proportions.

### R7 — Scope approval and frozen identity

- Record style, identity, outfit, pose, and final approval separately, each with its source, version, and hash.
- Prefer the latest relevant approved motion source over an older installed atlas.
- A timing repair cannot redesign the chin, body ratio, eyes, mouth, or clothing.
- Preserve the source files and the actual executed prompts.
- After a rejection, withdraw the recommendation and recover the approved source pixels before any newly authorized redraw.
- For every changed cell, review identity against the approved reference at the same view and physical scale, both native and enlarged. Check physical ratios, silhouette, eye and mouth landmarks, hem position, and asymmetric accessories.
- Unchanged cells prove scope only. They cannot approve changed cells.
- An exact integer translation needs an offset record, visible-RGBA equality, and a no-clipping proof. It is not whole-cell pixel identity.
- Machine hashes never certify likeness. See [quality](docs/en/quality.md).

### R8 — Exposure and fatigue

- Read [exposure-aware design](docs/en/exposure-design.md).
- Default design attention runs idle > running > review > waiting > failed. This is a design priority, not measured screen occupancy.
- Keep the approved core form stable in idle and gaze. Keep frequent work cues restrained. Save more salient variation for intentional, lower-exposure moments.
- Interaction frequency depends on the user.
- Review the return to idle and the interruptions, not only isolated loops.
- For future boards, use this display order: `idle, running, review, waiting, failed, waving, jumping, running-left, running-right`.
- Never change the protocol atlas row order or the clockwise gaze order.
- Do not remake an approved board only to adopt the new display order.

### R9 — Source-led action design

- Choose each action before image generation, from one of three action-source routes:
  1. Real animals and pets use observed individual or species-characteristic behavior.
  2. Known IP or memes use verified same-version canonical performances from actually inspected primary media.
  3. Original concepts or source-poor avatars use legible conventional gestures adapted to their existing anatomy.
- These are three action-source routes, not three states. Business statuses, animation tracks, and gaze samples are separate catalogs with separate counts and meanings.
- A natural motion still needs a reason to express this interface state. Distinguish observation, adaptation, and fallback. Read [action design](docs/en/action-design.md) before planning or regenerating states.
- For every proposed track, record the trigger or binding for the exact surface, backed by evidence, or mark it unknown. Never infer it from a filename, a row key, a shared avatar, or an interactive documentation demo. See [runtime evidence](docs/en/runtime-state-evidence.md).
- Inspect existing prompts and final rows. Keep the good actions, and mark unreviewed ones rather than condemning everything.
- Before broad edits, give the user a concise per-character [action proposal](templates/en/action-proposal.md). Approved visual designs stay frozen while this happens.
- For a requested visual board, use the [labeled board template](templates/en/action-board.md): a compact combined animation, short Chinese and English action labels, one-character gaze, and evidence in the companion manifest. Include the requested body views on the same board, and keep the layout configurable.
- Layout approval never approves rejected character art.
- Distinguish representative key poses from complete animations, and gaze poses from task states.
- If sequential multi-character work is authorized, follow the agreed roster one character at a time, each with a fresh source and semantic check. Do not reuse stale performances. Do not add an approval wait the user has already superseded.
- Compile each accepted state into one [concrete generation brief](templates/en/generation-brief.md), not a menu of possible gestures.
- Thought stays thought across the whole cycle. Input or approval requests address the user. Idle stays calm. Failed and review need distinct meanings.
- Review unlabeled whole loops against their confusable neighbors, not only the first frames.
- If a vehicle or faceless design cannot express a distinction with its existing anatomy, say so. Do not invent parts or assign meaning to arbitrary movement.

### R10 — Host contract and multi-form characters

- Read the actual host contract. Names, frame budgets, and direction order are specific to each adapter.
- Keep these quantities separate: cycle length, preview event recurrence, observed host dwell, and random scheduling.
- Unknown support stays unknown.
- For one character with several forms, use a verified single-identity mapping and a feasible frame budget. Three separate pets or parallel demo boards do not satisfy a one-pet transformation.
- Matching start and end anchors on the main form do not guarantee a seamless interruption.
- Never infer occupancy percentages from asset counts or description text. See [multi-form](docs/en/multiform.md).

### R11 — Production iteration

- Generate a representative identity and gait sample before scaling production.
- Bound each iteration with a specific hypothesis, the changes allowed, and an observable success condition.
- After repeated failure, change the strategy. Do not keep resampling.
- Use connected pose groups instead of equal-width crops when spacing varies. Preserve jump displacement and shared registration.
- Asymmetric accessories may prohibit mirroring.
- Compare source pixels before treating alpha negative space as missing anatomy.

### R12 — Coverage and presentation

- Derive the expected requirements from the host contract. The current Pets v2 contract has nine tracks, 57 action frames, and 16 gaze samples, separate from the four business statuses.
- A requested combined showcase includes genuine track animations, one character demonstrating gaze, and the requested body views. Body views are presentation requirements, not extra host states.
- Record each view as observed, inferred, or proposed.
- Configure the layout from the latest verified reference. Do not hardcode a ratio, and do not drop body views to make the layout fit.
- A representative static overview accompanies the animation. It never replaces it.
- Extras cannot satisfy a missing host item.
- See [examples](docs/en/examples.md) and [identity and presentation](docs/en/identity-and-presentation.md).

### R13 — Loop seams and transitions

- Inspect the last two and first two source frames for pose, velocity, contact, scale, accessories, and texture.
- Matching endpoints alone are not enough. Duplicate extreme frames can introduce a pause.
- Check source seams independently of the board timing.
- Do not stretch blinks or airborne contacts without reason.
- Choose a master period that fits each sustained or event schedule, or explicitly export a non-reset sequence.
- Verify every transition phase, including `t` versus `t+T` and the intended final-to-first successor.- An event hold must cite exact approved neutral source frames, and stays labeled preview-only.
- Decode the actual GIF or MP4 timestamps and the final hold. An encoder command or total duration alone cannot prove late-phase correctness.

### R14 — Long viewing and runtime

- Watch high-frequency states for an actual uninterrupted 30- and 60-second window at the target size.
- Record the reviewer, the file hash, the size, the viewing time, and timestamped notes on any repetition, fatigue, flicker, or readability problem.
- Keep these as separate facts: generated, decoded, and watched.
- Test interruptions in the entry, hold, and exit phases only within what the actual host supports. Offline hard cuts expose risk but do not implement blending.
- Numerical proxies do not certify comfort.
- Unwatched diagnostics stay unwatched.

### R15 — OpenAI export and installation

- Read [independent production and delivery](docs/en/openai-production.md) for the exact v2 contract, the bundled `openai_pet_atlas.py` commands, and the lifecycle.
- The three official Work Pets skills are not prerequisites.
- Keep these gates separate: local structure, visual approval, server preflight, and host runtime.
- After showing the final animation and receiving visual approval, offer installation to supported destinations. If explicit installation or activation authorization already exists, carry it out without a redundant question.
- Preserve stable IDs on updates. Omit unchanged metadata. Never upload for a metadata-only change.
- Verify each authorized surface separately.
- Without a supported write route, deliver import-ready files and accurate instructions, not an installation claim.

### R16 — Deliverables

- Match the requested format, including an animation established by the user's reference or an earlier request.
- An animated board needs genuine within-state motion from the generated source frames. A slideshow of one pose per state, a camera zoom, or a whole-image translation is not a substitute.
- A static key-pose board may be a labeled interim preview. It never fulfills an animation request by itself.
- Preserve full-quality masters and source atlases. Provide lighter chat renditions only with verified source coverage and timing.
- Upscaling adds no original detail.
- Include animation or video where supported, plus source and provenance, coverage, and layered review states. A static poster is optional unless requested.
- Keep these separate: complete candidate, visual acceptance, runtime validation, and user approval.
- A showcase is not an import atlas.

### R17 — Privacy and rights

- Private creation and public redistribution have separate gates.
- Do not default-upload private inputs for reverse search, or put package photos, character art, private identifiers, or executed prompts into an open-source candidate.
- User risk acceptance is not a rights-holder license. The code license does not license referenced characters. Do not guarantee copyright clearance.
- Installation, activation, remote repository creation, and publication are separate authorized actions.
- See [asset policy](ASSET-POLICY.md).

### R18 — Learning and failures

- For each stage, retain: evidence, failure, hypothesis, bounded change, verification, generalization, and a regression reference.
- Mark untested transfers and uncatalogued stages as untested. Do not invent a pass or a failure.
- Never rewrite a historical executed prompt.
- Preserve original failed reports, even when a later interpretation explains an apparent false positive.
- Run the applicable diagnostics and tests, and state clearly what they cannot assess.
- Templates: [project spec](templates/en/project-spec.md), [state plan](templates/en/state-plan.md), [repair record](templates/en/repair-record.md), [delivery review](templates/en/delivery-review.md), [learning ledger](templates/en/learning-ledger.md).

## Acceptance evidence

- Never convert four-direction feasibility into full sixteen-direction coverage.
- Geometry, identity, direction semantics, full coverage, and actual runtime are independent evidence categories. None replaces another, and none replaces the whole-cycle action-meaning review.
- Keep installation-format readiness and successful installation narrower than runtime acceptance.
- Natural occlusion can reduce gap diagnostics while still failing identity or attention direction.
- Preserve the approved baseline while you verify real host event routing.
- Read [generalized lessons from executed tests](docs/en/independent-acceptance-gates.md). The acceptance-scope checker validates records only and does not replace the official gates.
- After final compositing and cleanup, re-run the applicable gates on the exact delivery file, not on a precursor.
- For server readback, compare encoded hashes and decoded RGBA separately. Re-encoding can change the hash without changing any pixel. See [final-artifact verification](docs/en/independent-acceptance-gates.md#final-artifact-and-readback).
- Read [identity-safe presentation](docs/en/identity-and-presentation.md) before changing a layout, reusing a concept, or repairing gaze. Keep installed art, newer source frames, and concept layouts in separate evidence chains. A visual verdict never transfers just because names match.

## Optional tools

- **Offline state tester** ([docs](docs/en/state-tester.md)): inspect all source states in a v1 or v2 atlas without regenerating artwork. It is an independent simulator, not installed-pet control. Keep its coverage, user verdicts, and simulation timing separate from visual approval and client runtime evidence.
- **Authored row, host trigger, and task label are three different things.** Never infer common-form occupancy from a row name or one screenshot. Offline control is not live verification. See [runtime state evidence](docs/en/runtime-state-evidence.md).
- **Localized repair** ([focused repair](docs/en/focused-repair.md)): for a gaze, accessory, or silhouette defect on an approved baseline, freeze the protected pixels, repair only the smallest coherent unit, and keep the acceptance layers separate.
- **Feature applicability**: before adapting a motion template, declare per-actor feature applicability in the [state plan](templates/en/state-plan.md) and run `scripts/check_feature_applicability.py`. A faceless actor cannot require pupil or nose-tip cues. Structured checks do not replace reviewing the actual generation instructions.
- **Line-art and faceless designs** ([guidance](docs/en/line-art.md)): keep researched drawing mechanics, synthetic geometry, the observed authorized-fill case, and unverified runtime transfer as separate items.

## Capability and acceptance boundaries

Read [compatibility](docs/en/compatibility.md) when planning a deliverable. Sound is not implemented by this toolkit, so do not invent audio fields or native sound triggers. Reference approval, layout approval, and final-art acceptance remain three separate gates.
