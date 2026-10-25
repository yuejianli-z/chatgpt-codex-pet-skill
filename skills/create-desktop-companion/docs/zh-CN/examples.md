# 可运行示例

[English](../en/examples.md)

在包含 `SKILL.md` 的目录执行，并启用[安装指南](installation.md)中的 Python 环境。以下使用 macOS/Linux 的 `/tmp`；Windows 可选择 `$env:TEMP\companion-demo` 等新的可写目录，使用虚拟环境中的 Python。

## 1. 编码并解码一个小动画

```sh
python scripts/make_test_fixture.py /tmp/companion-demo
```

输出 `geometry-test.gif`（64×64、三帧原创矩形）与 `fixture-check.json`（解码停留 100/200/300 毫秒，总计 600 毫秒，附 SHA-256）。已有 GIF 不会被覆盖；重复时使用新目录。这是编码测试，不是角色质量样例。

## 2. 离线检查全部图集状态

```sh
python tools/state-tester/tests/make_fixture.py /tmp/companion-atlas.png
```

用桌面浏览器打开 `tools/state-tester/standalone.html`，选择该 PNG。通过播放、暂停、逐帧、拖动进度、视线选择、接缝与硬切观察彩色编号格。关闭前导出 QA；记录仅在当前标签页内存中，没有报告导入功能。查看器不连接服务器，也不控制已安装桌宠。

## 3. 验证完整记录

```sh
python scripts/check_manifest.py examples/geometry-coverage.json
python scripts/check_learning_ledger.py examples/learning-ledger.json
python scripts/check_learning_ledger.py examples/learning-ledger.zh-CN.json
python scripts/check_feature_applicability.py templates/feature-applicability.example.json
python scripts/check_acceptance_scope.py templates/acceptance-scope.example.json
```

以上检查记录结构和一致性，不验证批准人的身份、证据真实性，也不自动证明记录与图像像素相符。学习记录是历史方法示例，不是当前项目的验收结果。

对照尚未填完的模板：

```sh
python scripts/check_manifest.py templates/completeness-manifest.example.json
```

预期返回非零退出码并列出缺失要求。应复制后填写实际证据，而不是修改检查器让空模板通过。身体视角要求可配置；注视采样不能充当动作动画。

## 4. 查看命令接口

```sh
python scripts/check_animation.py --help
python scripts/diagnose_visual_geometry.py --help
python scripts/compare_rgba.py --help
python scripts/check_platform_claims.py --help
```

按脚本 schema 提供真实源文件。`check_animation.py` 检查几何与时序，没有通用的观看舒适阈值。保留源文件并使用独立输出路径；几何诊断拒绝覆盖输入别名或已有报告。

### 命令行与 Python 库的区别

| 文件 | 接口 | 用途 |
|---|---|---|
| `preflight.py` | CLI | Python/Pillow 前提，不检查云服务权限 |
| `check_manifest.py` | CLI | 源索引与角色覆盖记录 |
| `check_learning_ledger.py` | CLI | 学习记录的证据与状态一致性 |
| `check_feature_applicability.py` | CLI | 特征/提示是否适用于角色 |
| `check_acceptance_scope.py` | CLI | 验收范围记录 |
| `check_platform_claims.py` | CLI | 能力与证据声明 |
| `check_animation.py` | CLI | 动画几何与时序 |
| `diagnose_visual_geometry.py` | CLI | 主体角色与拓扑 |
| `compare_rgba.py` | CLI | 解码 RGBA 对比 |
| `check_repair_contract.py` | 可导入 Python 函数 | 相位、尾帧、哈希、改动格记录、平移及风格批准范围 |
| `check_blind_review_pair.py` | 可导入 Python 函数 | 盲测板与答案键的精确哈希绑定 |

后两项不是命令行校验器，直接执行不会运行检查；对应测试展示了调用方式。它们不会认脸或判断方向语义。

## 5. 重建开发工具

```sh
python tools/state-tester/build.py
python tools/line-art-rig/build_specimen.py
python tools/line-art-rig/test_specimen.py
```

查看器由 `index.html` 与 `tester.js` 重建 `standalone.html`。线稿 builder 没有命令行选项，会在自身目录重建教学素材；不要覆盖不可恢复的本地修改。测试覆盖通用样例，不认证具体角色。

将测试图集嵌入独立本地页面：

```sh
python tools/state-tester/build.py --atlas /tmp/companion-atlas.png --output /tmp/companion-viewer.html
```

嵌入会把图像数据复制到 HTML；分发该文件等同于分发图像，需要相应权利。builder 禁止将嵌图结果写入公开的 `standalone.html`。

## 6. 可选浏览器冒烟测试

需要 Node 能加载 Playwright，且 Chromium 可运行：

```sh
CHROMIUM_PATH=/usr/bin/chromium node tools/state-tester/tests/browser-test.cjs /tmp/companion-atlas.png
```

将路径改为本机真实可执行文件；默认路径为 `/usr/bin/chromium`。测试说明见[查看器文档](../../tools/state-tester/README.md)。即使通过，也不证明下载体验、视觉质量或宿主行为，见[验证记录](../validation.md)。

## 应用于实际项目

建立[项目规格](../../templates/zh-CN/project-spec.md)、[状态计划](../../templates/zh-CN/state-plan.md)与[交付审阅](../../templates/zh-CN/delivery-review.md)。使用获准工具制作源帧，按目标尺寸观看，再运行适用检查。完整仓库作品集（不随本安装包提供）的角色演示展示一种交付效果，不代表自动生成到安装的完整流水线。
