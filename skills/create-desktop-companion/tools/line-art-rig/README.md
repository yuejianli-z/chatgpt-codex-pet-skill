# Original line-art rig teaching specimen / 原创线条骨架教学样例

This is an original, generic teal line figure, with no private reference art, named character or pig. It demonstrates a controllable drawing method, not native image generation, a finished pet, an installation artifact, an official validation exemption or a repair of another asset. The open head is a graphic outline; no physical 3D anatomy is asserted.

这是原创的青色通用线条人，不含私人参考图、特定角色或小猪。它只演示可控绘制方法，不是原生图像生成结果、成品宠物、安装包、官方验收豁免或对其他素材的修复。头部只是留白轮廓，不代表对三维实体结构的判断。

## Run / 运行
Python 3 standard library only; no installation required.

    python build_specimen.py
    python test_specimen.py

Open rest.svg or microgesture.svg in an SVG-capable browser for visual inspection. The second file uses SVG SMIL animation; environments without that support may show only its initial pose. Animated playback, 96/128 px views and native-host behavior are not verified. Geometry tests do not certify visual quality.

用支持 SVG 的浏览器打开 rest.svg 或 microgesture.svg。后者使用 SVG SMIL 动画，不支持它的环境可能只显示首帧。动画实播、96/128 像素视图和原生宿主行为均未验证。几何测试通过不等于视觉效果验收通过。

## Files / 文件
- build_specimen.py: source generator; angles drive connected two-segment limbs.
- test_specimen.py: standard-library geometry checks.
- rest.svg: static pose, transparent background, unfilled head outline.
- microgesture.svg: original 2-second subtle greeting loop.
- poses.json: 25 sampled poses with fixed lengths and line width.
- diagnostics.json: minimum selected edge-clearance measurements.

## What the tests establish / 测试范围
The tests check fixed segment lengths, joint connections/stable feet, loop closure and bounded hand displacement, selected negative-space clearances, and SVG fill/stroke/join properties. The tests use full-precision pose data; SVG coordinates are serialized to six decimals. The stroke width is 4 viewBox units, the head radius 17 units, and the canvas 160×176. These are parameters for this example, not universal design rules.

五项测试检查固定骨段长度、关节连接与脚部锚定、首尾闭合与受限手部位移、部分留白距离，以及 SVG 无填充和圆端圆角属性。测试使用完整精度坐标，SVG 输出保留六位小数。线宽 4、头半径 17、画布 160×176 仅是本例参数，不是通用规范。

The 25 poses include the repeated endpoint. Discrete SVG pose switching intentionally avoids linear endpoint interpolation, which would shorten rotating segments between samples. This creates an approximately 12 fps educational loop with a repeated seam pose; it is not claimed to be production-smooth. For smoother animation, recompute coordinates from interpolated angles at render time or export sufficiently sampled constrained poses, then inspect playback.

25 个姿势含重复终点。离散切换避免了端点线性插值使旋转骨段在中间变短的问题。这是约 12 帧/秒、含重复首尾姿势的教学循环，不声称已达到生产级顺滑。更细腻的动画需要逐时刻由角度重新求坐标，或导出足够密的约束姿势，再实播检查。

Clearance tests cover raised forearm/head, raised hand/torso and foot endpoints only. They do not test every collision, whole silhouette, semantic expression, browser rendering, raster antialiasing, small-size readability or any platform gate. Intentional transparent space is preserved; no hidden fills or inspection avoidance is used.

留白检测仅覆盖举起前臂与头、举起手与躯干、两脚端点。它不涵盖所有碰撞、完整轮廓、语义表情、浏览器效果、抗锯齿、小尺寸可读性或任何平台验收。保留正常透明留白，没有隐藏填充或规避检测。

## Manual next check / 后续人工检查
At verified runtime size and at 96/128 px height, compare rest and the whole loop on light, dark and mixed backgrounds at 100% zoom. Check limb separation, readable open center, rounded joints, line flicker, hand gesture, grounding and seam pause. Enlargement helps diagnosis only. Record untested items honestly; passing these geometry tests cannot substitute for official requirements.

在真实运行尺寸以及高度 96/128 px 下，以 100% 缩放检查浅色、深色和复杂背景上的静态图及完整循环。检查肢体分离、头部留白、关节圆角、线条闪烁、手势、脚部落地感及循环接缝停顿。放大只辅助诊断；如实记录未检查项，不能用几何测试替代官方要求。

## Primary source / 一手来源
W3C SVG painting defines fill, stroke, caps and joins: https://www.w3.org/TR/SVG/painting . The example's artistic parameters and geometry tests are our own teaching choices.
