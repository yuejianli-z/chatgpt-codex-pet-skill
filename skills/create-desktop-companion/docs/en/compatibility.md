# Compatibility and capabilities

[中文](../zh-CN/compatibility.md)

There are three separate layers: reading the skill, producing assets, and running a pet. Support for one does not establish the other two.

## Included

- Markdown workflow and bilingual templates, with Python 3.10+/Pillow diagnostics.
- A fixed-v2 atlas assembler, structural validator and source-animation preview exporter; see [independent production](openai-production.md). These require supplied, registered source frames and do not generate artwork or install a pet.
- An offline browser viewer for the fixed Pets-style v1/v2 atlas layouts.
- Node controller tests, an optional Playwright browser smoke test, and original synthetic fixtures.
- A generic SVG line-art teaching specimen, not a renderer for arbitrary characters.

## Supplied externally

Image generation/editing, complete character-board or video composition, native host importing/selection, and host lifecycle events. No universal exporter, event bridge, cross-agent player, audio engine, or new native adapter is implemented here.

## Viewer contract

PNG/WebP, at most 20 MiB, 8 columns of 192×208 cells. v1 is 1536×1872; v2 is 1536×2288. Nine action tracks contain 6/8/8/4/5/8/6/6/6 frames (57). v2 adds 16 clockwise gaze samples from up; 73 active cells and 15 unused cells total. The viewer validates layout and file size, not full production content acceptance.

Simulation controls include FPS, slow motion, seam inspection and hard cuts. They neither change native timing nor establish real triggers, randomness, dwell, blending, pointer tracking, or installed display size. Runtime verification must identify the exact product, version, and surface.

## Integration guidance

Prefer a verified native import route. When a host lacks one, a Mod or external player is a separate engineering project, not an automatic consequence of skill installation. Keep target-neutral source frames, timings, anchors and meanings; export only to a checked host contract.

The dated [platform contract notes](platform-foundation.md) and [runtime evidence](runtime-state-evidence.md) distinguish schema observations from runtime measurements.

## Audio

The recorded 2026-10-23 custom Pets upload/create/update interface accepted sprite sheets and metadata, with no audio upload or action-to-sound mapping fields. This toolkit therefore provides no installed-pet sound through that route. This is not a statement about all future interfaces. MP4 audio is separate demonstration media; GIF has no audio.
