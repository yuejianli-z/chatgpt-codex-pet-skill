# OpenAI pet production and delivery

This independent adapter produces the OpenAI v2 image format without installing `work-pets:pets`, `work-pets:create-pet`, or `work-pets:update-pet`. Those three workflows inform the lifecycle separation below; their presence is not a dependency. An image generator/editor, Python 3.10+, Pillow, and approved character source frames are still required. Host account access and import tools are separate optional capabilities. This package does not bundle credentials, a remote upload client, or the OpenAI application.

## Four separate contracts

1. **Asset:** fixed cells and row order.
2. **Art:** recognizable identity, meaningful motion, valid transparency and continuity.
3. **Preview:** a chosen timing schedule for inspecting frames.
4. **Host:** actual events, playback repetition, gaze override and interruptions on a named client/version.

A pass in one layer never proves the other three. Nine animation tracks are not nine business statuses; sixteen gaze samples are not sixteen task states. Body views are showcase references, not additional import rows.

## Fixed v2 export

Transparent single-image PNG or WebP; exactly 1536 × 2288 pixels; eight columns and eleven rows; each cell 192 × 208; at most 20 MiB (20,971,520 bytes). Do not resize the final atlas to improve quality. Generate higher-resolution sources if useful, then register and fit approved art to the fixed cells without changing proportions or clipping accessories. Leave unused cells alpha-zero. RGB values under alpha zero do not affect transparency.

| Protocol row | Key | Frames | Preview frame durations (ms) | One preview cycle |
|---|---|---:|---|---:|
| 0 | idle | 6 | 280,110,110,140,140,320 | 1100 ms |
| 1 | running-right | 8 | 120 × 7,220 | 1060 ms |
| 2 | running-left | 8 | 120 × 7,220 | 1060 ms |
| 3 | waving | 4 | 140 × 3,280 | 700 ms |
| 4 | jumping | 5 | 140 × 4,280 | 840 ms |
| 5 | failed | 8 | 140 × 7,240 | 1220 ms |
| 6 | waiting | 6 | 150 × 5,260 | 1010 ms |
| 7 | running | 6 | 120 × 5,220 | 820 ms |
| 8 | review | 6 | 150 × 5,280 | 1030 ms |
| 9–10 | gaze | 16 still samples | no intrinsic duration | pointer/host controlled |

This is 57 action frames + 16 gaze samples = 73 occupied cells and 15 unused cells. Gaze is clockwise from screen-up in 22.5° increments: row 9 contains 0°–157.5°; row 10 contains 180°–337.5°. These are gaze poses, not a whole-body turntable. Existing v1 files need a separate legacy inspection path; this adapter builds v2 only.

The durations above are source-preview timings, not guarantees of installed playback. A reported desktop 26.1021.3705.0 analysis describes idle slowed sixfold and non-idle defaulting to three cycles, with explicit-loop and gaze overrides. This is a version-scoped report, not a verified universal rule or a timing control available inside the image. A task can remain running after its visual animation returns to idle. Never infer screen occupancy from task duration.

## Production without the official skills

1. Identify the host and gather an approved character baseline. For animals, inspect characteristic real behavior; for known IP, inspect same-version primary references; otherwise use readable conventional gestures adapted to the anatomy.
2. Plan actions using [exposure-aware design](exposure-design.md). Confirm identity and action concepts before expensive broad generation.
3. Generate each action strip from the same approved reference; generate coherent gaze families from verified cardinal anchors. Do not generate the whole final atlas in one image job. Keep each row's fixed count, physical scale and distinctive landmarks. Extract connected poses with shared registration, not arbitrary equal crops of uneven strips. Preserve a real vertical jump displacement. Mirror left/right only if markings, props and handedness remain valid.
4. Produce individually registered, transparent 192 × 208 frames. Inspect native-size poses, alpha edges, natural occlusions, actual direction, identity, source loop seams, and idle → event → idle transitions. An image generator is an external capability: missing access is a blocker to new art, not permission to fabricate placeholders.
5. Assemble and structurally validate with the bundled script below. It copies approved pixels, never redraws or resizes them. Check visual gates separately; the structural script cannot infer anatomy, semantic direction, likeness, fatigue or whether pixels wrongly intrude from a neighboring pose.
6. Render the nine source previews and sixteen gaze stills. Review actual decoded output at native size and the approved showcase layout. A presentation can use a different ordering from the protocol, but must never reorder the atlas.
7. Show final artwork and animation to the user. Record approval of this exact revision. Then follow the installation decision below.

A build manifest contains `actions` with exactly the nine keys above, each mapped to the fixed number of relative frame paths, and `gaze` with exactly sixteen relative frame paths in protocol order. Example shape: `{"actions":{"idle":["frames/idle-0.png", "..."]},"gaze":["frames/gaze-00.png", "..."]}`. The ellipses illustrate the shape only: supply every real frame path. Prefer generating the full manifest from your approved source inventory rather than filling a template with nonexistent assets.

```sh
python -m pip install -r requirements.txt
python scripts/openai_pet_atlas.py build run/frames.json run/final/spritesheet.png
python scripts/openai_pet_atlas.py validate run/final/spritesheet.png
python scripts/openai_pet_atlas.py preview run/final/spritesheet.png run/source-preview
```

The adapter enforces file size independently instead of relying on an upstream validator to enforce every documented restriction. It rejects missing occupied cells, nontransparent unused cells, wrong dimensions, animated atlas files and unsupported formats. It never overwrites an existing export. A complete delivery includes the atlas, source inventory, structural report, visual review, previews and a host compatibility note; original private references are not included in public packages by default.

## Review, then offer installation

Ask once after visual approval: “Would you like me to install this pet? Which available location should use it: the dot profile, Work pet, desktop app, or more than one?” Only offer surfaces actually supported by the current environment. If the user's existing instruction already explicitly authorizes installation/activation at named destinations, proceed without asking the same question again. Visual approval alone is not installation consent. Approval to install one surface does not authorize changing another or renaming the assistant.

- **New pet:** use the supported import/create route once, after local visual gates and the available server preflight pass. Verify returned identity/name before activation.
- **Existing pet repair:** resolve one stable ID; update that record rather than creating a duplicate. Names are not unique; page through the inventory or ask when ambiguous. Preserve prior metadata and active choices unless requested otherwise.
- **Metadata only:** change only requested fields; do not upload or regenerate an atlas.
- **Activation:** select the intended stable ID separately for each authorized surface. A shared catalog does not imply synchronized selection or runtime events. Verify each result; do not rename the dot unless asked.
- **Upload session:** follow the actual tool's documented preparation and one supported byte-transfer path. Treat returned upload destinations as transport only, not identity. Validate the exact final bytes; never reuse an expired session, assume an upload succeeded, or create duplicate records after an uncertain outcome. Inspect the outcome first.
- **No supported write route:** deliver the locally validated PNG/WebP and previews. If current server eligibility cannot be checked, label the export “candidate; import eligibility unverified”, not “ready to import”. Give only verified instructions for that client (for example, the current web Pets upload flow when available). Use “ready to import” only after applicable production and eligibility checks pass; never call a file delivery “installed”. Installing this skill does not install those missing API tools.
- **After import:** verify the selected pet and, with separate computer access where needed, check appearance and actual event behavior. Distinguish imported, selected, visually approved and runtime-tested. Do not require unsafe permission prompts just to manufacture a waiting/failed animation.

`check_design_delivery.py --installation` evaluates an advisory decision record without performing external writes. It cannot grant authorization; the actual host/tool policy remains authoritative.

## Source and verification scope

Reference workflows: the three Work Pets plugin skills (list/select; create/validate; preserve-ID update). Public product reference: [Pets](https://learn.chatgpt.com/docs/pets). Public production reference: [OpenAI hatch-pet](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet). These sources can change; recheck the target version before claiming new native support. This document and adapter are independent implementations, not copies of an application or private runtime instructions.

## Final-artifact acceptance boundary

The included build/validate/preview commands implement structural assembly and source previews, not a replacement for an applicable official production workflow's mandatory gates. Before a create or artwork update, also establish final-byte quality evidence for chroma/edges, connected anatomy, scale/registration, motion, semantic directions and adjacent-direction continuity, then complete the supported server eligibility check. A local pass alone cannot authorize mutation or certify those visual properties. The preview command's nine action GIFs and sixteen stills are inspection inputs, not a claim that every required presentation or runtime test has been generated.

Update only a resolved custom pet. Verify the returned stable ID remains unchanged; inspect the inventory after create/update and preserve the previous active selection unless activation was requested. No-change requests leave the record and selection unchanged.

The advisory installation record can provide final_artifact_sha256 and production_evidence / eligibility_evidence records, each with passed: true, artifact_sha256 matching the final file, and a nonempty source. These declarations are not authenticated by the checker; missing or mismatched evidence means complete_final_preflight_before_authorized_operation, not permission to proceed.
