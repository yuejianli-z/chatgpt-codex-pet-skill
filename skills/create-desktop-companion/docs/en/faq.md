# Frequently asked questions

[中文](../zh-CN/faq.md)

## Is this a desktop pet application?

No. It is a production skill plus local review tools. It helps an assistant plan, produce with available tools, and inspect companion assets. A host application must supply native display, installation, and events.

## Why does the repository have a different name from the skill?

The GitHub repository is `chatgpt-codex-pet-skill`; the skill's declared name is `create-desktop-companion`. Clone or rename the complete folder to the latter when installing. `SKILL.md` must sit directly inside it.

## Do I need an API key?

Not for bundled diagnostics, synthetic examples, or the offline viewer. New artwork requires whichever image service you choose, with that service's own access and terms. This repository does not collect credentials.

## Can I use my own pet photos or an existing character?

Yes, as input to an authorized project. Preserve individual markings and distinguish unseen details from observed ones. Having a reference or approving an image does not grant redistribution rights. Do not upload private references to external services without permission.

## Does it work with Claude, Codex, Cursor, or another agent?

The workflow is Markdown-based. Local installation paths are documented for Codex and Claude Code. Skill loading is separate from image-generation tools and native pet support. Cross-agent runtime adapters are not bundled. See [compatibility](compatibility.md).

## Why is my atlas rejected by the viewer?

Check format, encoded size and exact dimensions: PNG/WebP, up to 20 MiB, 1536×1872 (v1) or 1536×2288 (v2). Do not resize a different atlas blindly: cell meaning and padding matter. Other contracts need an adapter. A viewer pass also does not guarantee host acceptance.

## Can the viewer force my installed pet into a state?

No. It reads a local atlas and simulates playback. Real state triggers, timing and pointer behavior must be observed in the target client. Its 16 gaze poses are not 16 task states.

## Does a passing check mean the character is good?

No. Machine checks test records, geometry, timing or pixels. Likeness, action meaning, direction readability and comfortable playback require visual review. An incomplete template is expected to fail until it is filled with actual evidence.

## Why does rerunning the fixture command fail?

`make_test_fixture.py` refuses to overwrite an existing `geometry-test.gif`. Choose a fresh output directory. Preserve source assets and review each tool's output path before running it.

## Can I make a GIF or video presentation?

The workflow explains how to plan and review one. It does not bundle a complete character-board/video renderer. Use your compositor, keep source timing, and inspect the encoded file. A static pose slideshow does not demonstrate within-action animation.

## Are demonstration images included in the MIT license?

Only assets explicitly covered by their attribution are. See [asset policy](../../ASSET-POLICY.md) and any asset-local notice. MIT for the toolkit does not license third-party characters, photos, or generated project artwork.
