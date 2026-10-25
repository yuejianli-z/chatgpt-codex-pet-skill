# Offline state tester

Open `tools/state-tester/standalone.html` in a modern desktop browser, then select your local PNG or WebP atlas. No server, installation, credentials, upload or network service is needed. Chinese is the default; use English to switch language. The default viewer contains no embedded character art; separate demonstration media has its own rights notice.

Accepted layouts are the dated eight-column Pets atlas contract: 192×208 cells, v1 1536×1872 or v2 1536×2288, at most 20 MiB. Nine actions have 6, 8, 8, 4, 5, 8, 6, 6, 6 frames (57 total). v2 adds 16 static gaze poses (73 cells total), clockwise from up in 22.5° increments. These are not 25 animations. Other host formats require a separate adapter.

1. Select the same approved source atlas you intend to inspect. Confirm its displayed file name and version.
2. Select an action or v2 gaze pose. Pause and step or scrub source frames; adjust display size/background. FPS and speed are your simulation settings.
3. Test all states for one pass, inspect last↔first loop seams, and run mid-action interruptions or a manual hard cut. No interpolation or host blending is implemented.
4. Record a human verdict and notes for each inspected state. Export QA JSON before closing or loading another atlas; records live only in this tab. Do not publish reports containing private filenames or notes without authorization.

Coverage means displayed source cells only. It does not prove human inspection, visual quality, rights clearance, installation, actual host timing, random scheduling, or runtime acceptance. This tool cannot control a live installed Dot pet. Genuine runtime observations and uninterrupted long-view records remain separate gates.

Run the supplied tester tests using the commands in `tools/state-tester/README.md`. Python diagnostics and their tests remain independent of the browser tool. The standalone file is generated from the reviewed HTML and JavaScript; do not edit it separately.

## Release verification boundary

The supplied controller and independent review tests use mocked DOM/canvas behavior. They verify state math, not browser rendering or image decoding. Browser smoke tests were attempted but Chromium could not launch in the validation environment. Layout, decoding and visual playback remain unverified; the smoke script does not test download UX. See [validation evidence](../validation.md).

Read [runtime state evidence](runtime-state-evidence.md) before interpreting activity labels, assigning frequent forms or claiming measured occupancy.
