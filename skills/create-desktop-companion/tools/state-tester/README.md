# 宠物状态实验室 / Pet State Lab

## 中文：快速使用

1. 双击 `standalone.html`，用现代桌面浏览器打开。无需安装、服务器或网络。
2. 选择宠物的原始透明 PNG / WebP 图集。v1 为 1536×1872；v2 为 1536×2288；最大 20 MiB。取消选择或加载错误时保留旧图集；错误加载会暂停旧播放。
3. 点击九种动作、v2 的 16 个视线姿态，或「一键遍历全部状态」。默认中文，右上角切换 English。
4. 用播放、暂停、逐帧、进度条、1–60 FPS 和 0.5× / 0.25× 慢放检查。原始格子始终为 192×208，不会改动原图。显示倍率只影响预览。
5. 「循环接缝测试」交替末帧与首帧；「中断切换测试」在每个动作中途硬切；也可以选目标后「立即硬切」。这些是特意暴露问题的假设性测试，不是客户端状态机。
6. 展开「记录与导出」，给当前状态填人工结论和备注。切换状态也会保存当前备注到本次会话内存。导出 JSON 保存文件名、可用时的 SHA-256、图集合同、模拟设置、显示过的格子、各状态审阅记录和最近 2000 个事件。

工具只读取本地文件，不上传、修改图片或静默持久化图片。关闭页面会丢失本次记录，请先导出。没有报告导入/恢复功能。打开全新图片会开始新会话。浏览器下载 JSON 的位置取决于用户设置。

重要边界：这是同一图集的独立模拟器，不能强制已安装 Dot 宠物切状态，不能证明安装/启用、真实 FPS、随机概率、停留、循环、混合或触发行为。覆盖计数仅说明显示过的格子；人工结论默认「未审阅」。不会自动判断美感、动作自然或视线正确。空白格/透明度内容审核仍应使用制作流程的 preflight。

## English: quick start

Open `standalone.html` in a modern desktop browser and select a transparent PNG/WebP atlas. No network or server is needed. Exact v1/v2 geometry and encoded size are checked. Select actions/gaze, play/pause/step/scrub, adjust simulated FPS and slow motion, inspect loop seams and hypothetical hard-cut transitions. The all-state sequence stops visibly after 57 action cells plus 16 v2 gaze poses. Gaze samples are static poses, clockwise from up in 22.5° steps, not animations.

Expand QA to record a human verdict and notes per state; export JSON before closing. Notes are kept only in current memory and reset for a new image. No session import is provided. Cancelling selection preserves the current asset; invalid selection retains it and pauses playback. Source pixels are never modified. Native cell size is 192×208; preview scale does not assert installed on-screen size.

This is an independent same-atlas simulation, not an installed-runtime controller. The tool cannot verify installation, real triggers, host timing, randomness, blending or loop behavior. Display coverage is not visual approval. No automatic aesthetic pass is issued. Use the separate production preflight for blank-cell/alpha checks.

## Build and test

- `python build.py` rebuilds art-free `standalone.html` from `index.html` and `tester.js`.
- `node tests/controller-test.cjs` tests controller logic with minimal DOM/canvas mocks. This is not browser rendering verification.
- `node tests/browser-test.cjs /path/to/valid-v2-atlas.png` runs the supplied Playwright browser regression. Requires Playwright and Chromium; set `CHROMIUM_PATH` if needed. The test uses the supplied private atlas and produces local screenshots, never package those screenshots publicly.
- `python build.py --atlas /path/to/atlas.png --output /private/path/demo.html` explicitly embeds that atlas into a PRIVATE user demo. Never include private demos or character images in the public skill package. PNG/WebP input is validated by the app on opening.

## Verification status

Node controller tests pass. JavaScript syntax is valid. For full verification including browser rendering and file-decoder behavior, run the provided browser regression in an environment that permits local Chromium.

For a public, art-free browser fixture, run `python tests/make_fixture.py /tmp/pet-fixture-v2.png` (Pillow required), then pass that path to `browser-test.cjs`. The fixture is original colored rectangles with row/frame labels. It is a geometry fixture, not a production pet.

- `node tests/independent-review.cjs` runs independent timeout-bounded state-engine regressions; also mocked DOM/canvas, not visual rendering.

Private embedding requires an explicit output path different from the public `standalone.html`; the builder refuses to overwrite that default with private art. 私人嵌图必须指定不同于公开 `standalone.html` 的输出路径。
