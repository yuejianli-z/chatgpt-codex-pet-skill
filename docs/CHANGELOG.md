## 3.3.7

- Add exposure-aware action design and separate future display order from immutable atlas row order.
- Add independent OpenAI v2 assembly, structural validation (including 20 MiB), and source previews with regression tests.
- Add visual-review → authorized installation/update/activation workflow, preserving stable IDs and capability boundaries.
- Existing character artwork and approved GIFs are unchanged.

# Changelog

[中文](CHANGELOG.zh-CN.md)

## 3.3.6 — Unreleased

- Separate the self-contained skill under `skills/create-desktop-companion/` from character studies under `examples/characters/`; document sparse installation and explicit asset version status.

- Rebuild bilingual onboarding with verified local-skill paths, runnable examples, compatibility, FAQ, and attributed demonstration media.
- Replace project-specific approval narratives with reusable acceptance guidance and curated character-design examples.
- Prevent geometry reports from overwriting subject metadata, other input aliases, or existing outputs.
- Reject malformed platform-claim records and missing/non-string evidence; report invalid input cleanly.
- Add seven regressions; the Python suite now contains 126 tests, including six package-layout regressions. Browser rendering and native host behavior remain separate, unverified checks.

## Development history

Historical labels describe development checkpoints, not published release tags. The notes below summarize implementation and method changes; they do not retroactively certify artwork or runtime behavior.

### 3.3.4-draft — 2026-10-23

- Restored shared cross-row scale registration guidance.
- Clarified reference provenance, scoped visual acceptance and absent audio support in the documented upload route.

### 3.3.3-candidate — 2026-10-21

- Required shared identity-scale registration using neutral head/torso landmarks, not per-frame bounding-box fitting.
- Replaced a fixed presentation ratio with configurable layout and requested body views.
- Separated concept/layout sources from approved identity sources; added anatomy, attachment, occlusion and final-encoding checks.

### 3.3.0–3.3.2 candidates

- Introduced source-led character action design, whole-cycle semantic contrast and bilingual action/state labels.
- Distinguished business states, animation tracks, gaze samples and host trigger evidence.
- Required genuine within-state animation in requested animated boards rather than pose slideshows.

### 3.2.3–3.2.5 candidates

- Added focused repair records, protected-cell checks, exact decoded-RGBA comparisons and scoped style approval.
- Added line-art feature applicability, compound-subject acceptance and multi-form timing guidance.
- Kept local structural acceptance separate from full coverage, visual review and native playback.

### 3.2.0–3.2.2 candidates

- Added the bilingual offline state viewer, standalone build, synthetic fixtures and controller tests.
- Added independent topology/subject-role diagnostics and learning-record checks.
- Distinguished authored frame rows from host timing, occupancy and interruption behavior.

### 3.1.0-candidate

- Established canonical English instructions with aligned Chinese guidance and templates.
- Added local preflight, manifest coverage, timing/hash/repair contracts and original geometric fixtures.
- Introduced platform-first capability classification and separate display, import and runtime evidence.

### Earlier checkpoints

2.2.0 consolidated the Chinese method and diagnostic code; 2.1.x established unified delivery and alpha-source tracing. These identifiers are historical checkpoints, not a guarantee of public release or complete visual acceptance.

