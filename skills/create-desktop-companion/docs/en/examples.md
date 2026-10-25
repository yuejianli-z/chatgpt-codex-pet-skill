# Runnable examples

[中文](../zh-CN/examples.md)

Run commands from the directory containing `SKILL.md`, with the [Python environment](installation.md) active. Example paths below use macOS/Linux `/tmp`; on Windows choose a new writable directory such as `$env:TEMP\companion-demo` and invoke the environment's Python executable.

## 1. Encode and decode a tiny animation

```sh
python scripts/make_test_fixture.py /tmp/companion-demo
```

Outputs:

- `geometry-test.gif`: three original rectangle frames, 64×64 pixels.
- `fixture-check.json`: decoded holds of 100/200/300 ms, 600 ms total, and the GIF's SHA-256.

The generator refuses to overwrite its existing GIF; use a fresh directory to repeat. This is an encoder fixture, not a character-quality example.

## 2. Inspect all atlas states offline

```sh
python tools/state-tester/tests/make_fixture.py /tmp/companion-atlas.png
```

Open `tools/state-tester/standalone.html` in a desktop browser and select `/tmp/companion-atlas.png`. Inspect the numbered colored cells with play/pause, stepping, scrub, gaze selection, seams and hard cuts. Export QA before closing: notes live in the current tab only, and there is no report-import feature. The viewer does not contact a server or control an installed pet.

## 3. Validate a complete record

```sh
python scripts/check_manifest.py examples/geometry-coverage.json
python scripts/check_learning_ledger.py examples/learning-ledger.json
python scripts/check_learning_ledger.py examples/learning-ledger.zh-CN.json
python scripts/check_feature_applicability.py templates/feature-applicability.example.json
python scripts/check_acceptance_scope.py templates/acceptance-scope.example.json
```

These examples check record structure and consistency. They do not authenticate approvals, verify the truth of cited evidence, or match a record to image pixels automatically. The ledger is a historical method-learning example, not a record of your project.

Contrast with the deliberately incomplete template:

```sh
python scripts/check_manifest.py templates/completeness-manifest.example.json
```

Expected result: nonzero exit with unmet requirements. Copy and fill the template for your project rather than changing the checker to make empty evidence pass. Required body views are configurable; gaze samples do not count as action animation.

## 4. Inspect the command interfaces

```sh
python scripts/check_animation.py --help
python scripts/diagnose_visual_geometry.py --help
python scripts/compare_rgba.py --help
python scripts/check_platform_claims.py --help
```

Use the documented schema and real source files for your project. `check_animation.py` analyzes frame geometry/timing according to its arguments; there are no universal visual-comfort thresholds. Preserve sources and choose separate output paths. Geometry diagnostics refuse input aliases and existing report outputs.

### CLI versus Python library

| File | Interface | What it checks |
|---|---|---|
| `preflight.py` | CLI | Local Python/Pillow prerequisites, not cloud access |
| `check_manifest.py` | CLI | Required source-index and role coverage records |
| `check_learning_ledger.py` | CLI | Learning-record evidence and status consistency |
| `check_feature_applicability.py` | CLI | Whether requested cues apply to the subject |
| `check_acceptance_scope.py` | CLI | Scoped acceptance-record consistency |
| `check_platform_claims.py` | CLI | Capability/evidence declarations |
| `check_animation.py` | CLI | Animation geometry/timing diagnostics |
| `diagnose_visual_geometry.py` | CLI | Subject-role and topology diagnostics |
| `compare_rgba.py` | CLI | Decoded RGBA comparison |
| `check_repair_contract.py` | Importable Python functions | Schedule phase, final holds, hashes, changed-cell records, translation and scoped style approval |
| `check_blind_review_pair.py` | Importable Python functions | Binding a review board to its exact answer-key hashes |

The last two files are libraries, not command-line validators: executing them directly does not run a check. Their tests demonstrate usage. None recognizes faces or judges visual direction semantics.

## 5. Rebuild developer tools

```sh
python tools/state-tester/build.py
python tools/line-art-rig/build_specimen.py
python tools/line-art-rig/test_specimen.py
```

The viewer build regenerates `standalone.html` from `index.html` and `tester.js`. The line-art builder has no command-line options and regenerates its teaching assets in its own folder; do not run it against irreplaceable edits. The rig tests cover the generic specimen, not a production character.

To embed your own atlas in a separate local viewer, use an explicitly chosen output:

```sh
python tools/state-tester/build.py --atlas /tmp/companion-atlas.png --output /tmp/companion-viewer.html
```

Embedding copies image data into the HTML. Treat that file as containing the source artwork and do not distribute it without the corresponding rights. The builder prevents embedding into the public `standalone.html` output.

## 6. Optional browser smoke test

Requires Playwright available to Node and a runnable Chromium executable. From the repository root:

```sh
CHROMIUM_PATH=/usr/bin/chromium node tools/state-tester/tests/browser-test.cjs /tmp/companion-atlas.png
```

Use the real executable path on your machine. The default is `/usr/bin/chromium`. See [viewer instructions](../../tools/state-tester/README.md) for the test details. A passing smoke test does not establish download UX, visual quality or host behavior; see [validation evidence](../validation.md).

## From examples to a project

Create a [project specification](../../templates/en/project-spec.md), [state plan](../../templates/en/state-plan.md) and [delivery review](../../templates/en/delivery-review.md). Produce source frames with your authorized art tools, inspect them at target size, then run applicable checks. Character demonstrations in the full repository gallery illustrate presentation outcomes, not an automated generation-to-installation pipeline.
