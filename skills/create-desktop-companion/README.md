# Create Desktop Companion: installable skill

[简体中文](README.zh-CN.md) · [Instructions](SKILL.md) · [Installation](docs/en/installation.md)

Version 3.3.6. This folder is a self-contained, copy-installable skill. Keep all its contents together. The full repository separately contains project governance and a character gallery; neither is required by this kit. Character art is not bundled here.

Start with [SKILL.md](SKILL.md), [workflow](docs/en/workflow.md), [examples](docs/en/examples.md), and [quality gates](docs/en/quality.md). See [asset policy](ASSET-POLICY.md) and [source credits](SOURCE-CREDITS.md).

## Local checks

Run from this folder with Python 3.10+, Pillow, and Node.js:

```sh
python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
python scripts/preflight.py
node tools/state-tester/tests/controller-test.cjs
node tools/state-tester/tests/independent-review.cjs
python tools/line-art-rig/test_specimen.py
python scripts/check_package.py
```

The package check verifies relative Markdown links and the distributable file boundary. Optional browser tests are documented in [the state tester](tools/state-tester/README.md). Passing local checks does not establish actual-client discovery, pet installation, native rendering, or runtime behavior.


## Independent OpenAI export and thoughtful motion

No installation of the three official Work Pets skills is required. This package includes a fixed-v2 atlas assembler, structural validator and source-animation preview exporter; artwork generation still uses your chosen image provider. Design attention favors quiet idle and restrained work motion, with explicit fatigue review. After visual approval, the workflow offers installation or performs already-authorized activation through available host tools. Without a supported write route it delivers import-ready files, not a false installation claim.

- [Exposure-aware design](docs/en/exposure-design.md)
- [Production, exact format and installation](docs/en/openai-production.md)
