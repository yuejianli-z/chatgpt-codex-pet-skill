[中文](README.md) · [English](README.en.md)

# ChatGPT / Codex Pets

![Version](https://img.shields.io/badge/version-3.3.7-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Language](https://img.shields.io/badge/lang-中文%20%7C%20English-lightgrey)

Author on Bilibili: [百香里_](https://space.bilibili.com/147521399)

Create your own ChatGPT / Codex pet with this skill, or download a ready-made pet pack and follow its import instructions.
Preview the characters below, then choose a download.

> This project is for entertainment and learning/exchange purposes only. Character designs belong to their respective rights holders; if you believe something infringes your rights, please contact us and it will be removed. See the [Disclaimer](#disclaimer) at the bottom.

## What you can start from

- **A real pet's photo**: your own cat, dog, hamster, and so on. A few clear photos are enough.
- **A concept reference**: a hand-drawn design sheet, a meme, an avatar, an illustration.
- **Any object**: not limited to animals or existing characters. If you have a reference image, it can become a pet.

The clearer the reference, the better the result.

## Downloads

| I want | Download |
|---|---|
| Just the Skill (make my own pet) | [Download ZIP](https://github.com/yuejianli-z/chatgpt-codex-pet-skill/raw/refs/heads/main/downloads/pet-skill-3.3.7.zip) |
| Just a ready-made pet (11 import packs) | [See individual download links](downloads/README.md) |
| Both | [Download the repository ZIP](https://github.com/yuejianli-z/chatgpt-codex-pet-skill/archive/refs/heads/main.zip) (skill, current packs and previews) |

## Character previews

Each animation below shows that character's nine action states and 16-direction gaze after import (a showcase GIF, not the import file). The transparent atlas used for installation is in the download section below.

### 01 · 短短（作者的猫） / Duanduan (the author's cat)

<p align="center">
  <img src="examples/characters/duanduan/preview-warm.gif" alt="短短（作者的猫） / Duanduan (the author's cat)" width="1000">
</p>

### 02 · 斯莫德（英雄联盟英雄，蕊雪盈春：聚珍皮肤） / Smolder (League of Legends, Petals of Spring skin)

<p align="center">
  <img src="examples/characters/smolder/preview-warm.gif" alt="斯莫德（英雄联盟英雄，蕊雪盈春：聚珍皮肤） / Smolder (League of Legends, Petals of Spring skin)" width="1000">
</p>

### 03 · 奶蛙 / Naiwa

<p align="center">
  <img src="examples/characters/naiwa/preview-warm.gif" alt="奶蛙 / Naiwa" width="1000">
</p>

### 04 · DeepSeek鲸鱼娘 / DeepSeek Whale Girl

<p align="center">
  <img src="examples/characters/deepseek/preview-warm.gif" alt="DeepSeek鲸鱼娘 / DeepSeek Whale Girl" width="1000">
</p>

### 05 · 小熊猫 / Red Panda

<p align="center">
  <img src="examples/characters/red-panda/preview-warm.gif" alt="小熊猫 / Red Panda" width="1000">
</p>

### 06 · 比格犬 / Beagle

<p align="center">
  <img src="examples/characters/beagle/preview-warm.gif" alt="比格犬 / Beagle" width="1000">
</p>

### 07 · 卡皮巴拉 / Capybara

<p align="center">
  <img src="examples/characters/capybara/preview-warm.gif" alt="卡皮巴拉 / Capybara" width="1000">
</p>

### 08 · 银月（《凡人修仙传》角色） / Yinyue (character from Mortal Cultivation Chronicles)

<p align="center">
  <img src="examples/characters/yinyue/preview-warm.gif" alt="银月（《凡人修仙传》角色） / Yinyue (character from Mortal Cultivation Chronicles)" width="1000">
</p>

### 09 · 木棍人 / Tung Tung

<p align="center">
  <img src="examples/characters/tungtung/preview-warm.gif" alt="木棍人 / Tung Tung" width="1000">
</p>

### 10 · 笨笨的韭菜 / Benjiu

<p align="center">
  <img src="examples/characters/benjiu/preview-warm.gif" alt="笨笨的韭菜 / Benjiu" width="1000">
</p>

### 11 · 做多中国的好人豆子 / Douzi

<p align="center">
  <img src="examples/characters/douzi/preview-warm.gif" alt="做多中国的好人豆子 / Douzi" width="1000">
</p>

<details>
<summary><strong>Pet actions: when each of the 9 actions triggers</strong></summary>

| Action | Trigger / purpose | Frames |
|---|---|---:|
| Idle | Default/resting display; return after other actions | 6 |
| Working | Processing a task; not walking across the screen | 6 |
| Review | Result is ready to be viewed | 6 |
| Waiting | Input or approval is needed | 6 |
| Failed | Task error or failure | 8 |
| Wave | Initial desktop appearance | 4 |
| Jump | Pointer enters the desktop pet | 5 |
| Move left | Dragging the desktop pet left | 8 |
| Move right | Dragging the desktop pet right | 8 |
| Gaze | Pointer position around the page-top pet | 16 single poses |

Triggers describe the tested client surfaces, not a guarantee for every version. Task state and currently playing animation are different: a task can remain active after its animation returns to idle. The list is the design/display order; atlas row order is fixed separately.

</details>

<details>
<summary><strong>Deliverables: exact format for the import atlas, pet pack and skill</strong></summary>

| Deliverable | Format / purpose |
|---|---|
| Import atlas | One transparent PNG or WebP, exactly 1536 × 2288 px; 8 × 11 cells of 192 × 208 px; 57 action frames + 16 gaze poses; 15 empty cells; at most 20 MiB |
| Showcase | Animated GIF with actions, four reference views and 16-direction gaze; not the import file |
| Pet pack | Atlas, character metadata, import instructions and validation reports |
| Skill | Self-contained workflow, references, templates and diagnostic scripts |

</details>

## Disclaimer

- This project is for entertainment and learning/exchange purposes only. Do not use it for any commercial purpose. You use it at your own risk.
- The names, settings and copyrights of the characters shown here (including but not limited to Smolder from League of Legends, Yinyue from Mortal Cultivation Chronicles, DeepSeek-related designs, creator avatars and internet characters) belong to their respective rights holders. The pet atlases in this repository are fan-made re-creations of those designs. They are not affiliated with, authorized by or endorsed by the original rights holders or related companies.
- The MIT license applies only to the code, documentation and templates in this repository that the contributors own. It does not cover the character designs, reference images or pet artwork above.
- If you are a rights holder and believe this project infringes your rights, please contact us through this repository's Issues. Once verified, the material will be removed or replaced promptly. See [License and asset sources](docs/ASSET-POLICY.md).

[Installation](downloads/README.md) · [Skill guide](skills/create-desktop-companion/SKILL.md) · [Compatibility](skills/create-desktop-companion/docs/en/compatibility.md) · [License and asset sources](docs/ASSET-POLICY.md)
