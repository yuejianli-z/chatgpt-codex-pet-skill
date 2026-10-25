# Validation evidence

Date: 2026-10-24. Current toolkit version: 3.3.7. This report separates current and historical evidence; no check certifies native-host behavior.

## Follow-up compatibility checks / 后续兼容性检查

2026-10-24: 148 Python tests, 12 controller tests and 5 rig tests passed after adding artifact-bound production/eligibility decision regressions. The standalone package check covers 147 files. The checks remain advisory and cannot authenticate reports or perform native installation. The final repository commit must pass its own CI; the earlier CI below is historical evidence only.

## Earlier 3.3.7 evidence / 较早版本验证

- Tested commit: not recorded here; the earlier development history is not part of this repository.
- 144 Python regressions passed, including v2 assembly/validation, display-order separation, design evidence and installation/activation consent boundaries.
- 12 controller tests, independent controller review, and 5 generic line-art rig tests passed.
- Clean self-contained package: 147 files; relative file links and binary allowlist passed. The separately delivered ZIP contains only this skill directory, not the character gallery.
- A remote CI run for that earlier development commit passed on Python 3.10/3.12 with isolated-copy smoke checks; the run belonged to the previous repository history and is not linked here.
- Follow-up review verified that activate_existing cannot bypass activation consent or target-surface requirements when activate is omitted or false.
- These are structure/code/directory checks, not likeness, actual browser rendering, native installation, runtime trigger, rights, or fatigue approval. Later commits must be checked independently.

中文摘要：3.3.7 对应提交完成 144 项 Python 回归、12 项控制器测试、独立控制器审阅、5 项线稿测试及 147 文件独立包检查。上述远端 CI 同提交成功。安装和激活授权边界有专门回归；这些结果不等于角色视觉、浏览器真实渲染、原生安装、触发规则或分发权利验收。后续提交必须分别核验。

## Historical 3.3.6 evidence / 历史记录

The following results describe earlier revisions and are retained for traceability, not the current test count.

## Executed checks

| Check | Result | Environment / scope |
|---|---|---|
| Python regression suite | 120 passed | Python 3.12.14; Pillow 12.3.0 and a fresh isolated install of Pillow 13.0.0 |
| Viewer controller | 12 passed | Node.js 24.22.1; mocked DOM/canvas |
| Independent controller review | Passed | Timeout-bounded mocked state-engine checks |
| Generic line-art specimen | 5 passed | Geometry/pose regression, not character artwork |
| Preflight and GIF fixture | Passed | Three decoded holds: 100/200/300 ms |
| Complete manifest, bilingual ledgers, feature and acceptance examples | Passed | Record consistency only |
| Incomplete completeness template | Failed as expected | Missing requirements are not silently accepted |
| Viewer build and separate fixture embedding | Passed | Deterministic build and output protection |
| Animation diagnostic fixture and RGBA self-comparison | Passed | Synthetic files, not production visual acceptance |
| Browser smoke test | Blocked before execution | Chromium launch denied by environment socket permissions |

A clean virtual environment installed dependencies from `requirements.txt` and reran all 120 Python tests and five rig tests. Local shell/Python commands do not establish an installation test in Codex or Claude Code; installation locations were checked against current official documentation.

## Fixes covered by new regressions

- Geometry report output cannot overwrite the atlas, official report, subject metadata, aliases (including symlinks/hardlinks), or an existing output.
- Platform capability records reject malformed containers and invalid status/evidence types. Missing/non-string evidence cannot support an asserted capability. Invalid JSON and missing files produce a clear failure.

## Not established

- Browser rendering, file-decoder behavior and actual visual playback were not validated in this environment.
- The supplied browser smoke test does not click the download/export UI; download UX needs a separate manual or browser test even when smoke execution succeeds.
- Native installation, state triggers, real timing, pointer tracking, random scheduling, audio and host content acceptance are not covered by local tests.
- Likeness, anatomical correctness, action meaning, gaze readability, rights clearance and long-duration comfort require separate evidence for each actual asset.

## Reproduce

Follow the [English examples](en/examples.md) or [中文示例](zh-CN/examples.md), then run the README's developer checks. Record the exact checkout, runtime versions, commands and outputs for a release. GitHub Actions results, if available, must be tied to the remote commit; local results do not imply a CI pass.

## Repository-layout validation (2026-10-24)

After separating the project gallery from the installable skill, the full local suite passed: 126 Python tests (the existing 120 plus six package-integrity regressions), 12 controller tests, the independent controller review, and five line-art geometry tests. Preflight found Python 3.12.14, Pillow and ffmpeg; image-generation access, native-size visual playback and host import remain unverified.

An isolated copy of only `skills/create-desktop-companion` under a temporary `.agents/skills/create-desktop-companion` directory passed the same 126 + 12 + 5 tests, independent review, preflight, fixture generation, record validators and viewer/rig builds. Its package check passed with no missing or external relative Markdown file links, no character media, and no caches. This verifies directory self-containment, not real Codex or Claude Code discovery, native integration, or a remote CI run. No user computer was involved.

Run `python scripts/check_package.py` on a clean distributable copy. Local virtual environments and interpreter caches are deliberately rejected by this release-boundary check; keep them outside the folder being packaged and use `PYTHONDONTWRITEBYTECODE=1` while testing the release copy.
