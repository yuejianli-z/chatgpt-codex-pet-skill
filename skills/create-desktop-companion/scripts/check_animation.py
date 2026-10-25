#!/usr/bin/env python3
"""Measure exported RGBA frames; never redraw, align, mirror, or interpolate them.

This diagnostic manifest is independent of a desktop host's packaging schema:
{"states": {"pulse": {"loop": true, "frames": [
    {"path": "pulse-0.png", "duration_ms": 120,
     "anchors": {"core": [20, 20]}},
    {"path": "pulse-1.png", "duration_ms": 240, "hold": true,
     "anchors": {"core": [20, 20]}}
], "checks": {}}}}

Paths resolve relative to the manifest. Coordinates use canvas pixels, origin at
top left. A frame's hold=true declares that its identical preceding transition
(including the loop seam for frame 0) is an intentional pause. Named anchors are
provided by the author, not inferred anatomical landmarks.

Optional per-state checks: edge_margin_px (default 0), max_centroid_step_px,
max_bbox_size_step_px, max_anchor_step_px (name -> limit), max_frame_difference,
max_loop_difference. Differences are normalized premultiplied RGBA mean absolute
differences in [0, 1]. There are NO default motion or seam thresholds. Calibrate
limits for each state's intended action; jumps normally move across the canvas.

Exit 0: analysis completed without input errors (warnings may remain).
Exit 1: manifest/frame data errors. Exit 2: invocation or file I/O failure.
No exit code or geometric metric certifies identity, style, natural motion,
direction, host compatibility, or visual quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageStat


CHECK_KEYS = {
    "edge_margin_px", "max_centroid_step_px", "max_bbox_size_step_px",
    "max_anchor_step_px", "max_frame_difference", "max_loop_difference",
}


def finite_number(value: Any) -> bool:
    try:
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value))
    except OverflowError:
        return False


def number(value: Any, *, positive: bool = False) -> bool:
    return finite_number(value) and (value > 0 if positive else value >= 0)


def issue(report: dict, code: str, message: str, *, severity: str = "warning",
          **context: Any) -> None:
    report["issues"].append(dict(code=code, severity=severity, message=message, **context))


def distance(a: list | None, b: list | None) -> float | None:
    if a is None or b is None:
        return None
    return round(math.hypot(a[0] - b[0], a[1] - b[1]), 6)


def premultiplied(image: Image.Image) -> Image.Image:
    r, g, b, alpha = image.split()
    return Image.merge("RGBA", tuple(ImageChops.multiply(c, alpha) for c in (r, g, b)) + (alpha,))


def fingerprint(image: Image.Image) -> str:
    """Exact visible-pixel identity, ignoring RGB only where alpha is zero.

    Do not hash 8-bit premultiplied RGB: rounding would merge distinct faint pixels.
    """
    raw = bytearray(image.tobytes())
    for i in range(0, len(raw), 4):
        if raw[i + 3] == 0:
            raw[i:i + 3] = b"\0\0\0"
    return hashlib.sha256(str(image.size).encode("ascii") + raw).hexdigest()


def geometry(image: Image.Image) -> dict:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return dict(alpha_bbox=None, bbox_size=None, alpha_centroid=None,
                    nontransparent_pixels=0, alpha_mass=0, margins_px=None)
    width, height = image.size
    total = sx = sy = occupied = 0
    for i, value in enumerate(alpha.tobytes()):
        if value:
            occupied += 1
            total += value
            sx += (i % width) * value
            sy += (i // width) * value
    left, top, right, bottom = bbox  # right and bottom are exclusive.
    return dict(alpha_bbox=list(bbox), bbox_size=[right-left, bottom-top],
                alpha_centroid=[round(sx/total, 6), round(sy/total, 6)],
                nontransparent_pixels=occupied, alpha_mass=round(total/255, 6),
                margins_px=dict(left=left, top=top, right=width-right, bottom=height-bottom))


def validate_checks(value: Any, report: dict) -> dict:
    if not isinstance(value, dict):
        issue(report, "invalid_checks", "checks must be an object.", severity="error")
        return {}
    clean = {}
    for key, limit in value.items():
        valid = key in CHECK_KEYS
        if key == "max_anchor_step_px":
            valid = (isinstance(limit, dict) and all(
                isinstance(name, str) and bool(name) and number(v) for name, v in limit.items()))
        elif valid:
            valid = number(limit) and ("difference" not in key or limit <= 1)
        if not valid:
            issue(report, "invalid_check", f"Unknown or invalid check: {key}.", severity="error")
        else:
            clean[key] = limit
    return clean


def compare(a: dict, b: dict, image_a: Image.Image, image_b: Image.Image) -> dict:
    result = {"from": a["index"], "to": b["index"]}
    if image_a.size != image_b.size:
        return dict(result, comparable=False, reason="canvas_size_mismatch")
    means = ImageStat.Stat(ImageChops.difference(
        premultiplied(image_a), premultiplied(image_b))).mean
    dims_a, dims_b = a["bbox_size"], b["bbox_size"]
    return dict(result, comparable=True,
                identical_visible_pixels=a["fingerprint"] == b["fingerprint"],
                difference=round(sum(means)/(4*255), 8),
                centroid_step_px=distance(a["alpha_centroid"], b["alpha_centroid"]),
                bbox_size_step_px=(max(abs(x-y) for x, y in zip(dims_a, dims_b))
                                   if dims_a and dims_b else None),
                anchor_steps_px={name: distance(point, b["anchors"][name])
                                 for name, point in a["anchors"].items() if name in b["anchors"]},
                intentional_hold=(a["fingerprint"] == b["fingerprint"] and b["hold"]))


def check_transition(t: dict, checks: dict, report: dict, *, seam: bool = False) -> None:
    if not t["comparable"]:
        return
    context = dict(from_frame=t["from"], to_frame=t["to"], loop_seam=seam)
    if t["identical_visible_pixels"] and not t["intentional_hold"]:
        issue(report, "unmarked_repeat", "Identical adjacent visible pixels; review whether this is an intended hold.", **context)
    pairs = [("centroid_step_px", "max_centroid_step_px"),
             ("bbox_size_step_px", "max_bbox_size_step_px"),
             ("difference", "max_loop_difference" if seam else "max_frame_difference")]
    for metric, key in pairs:
        if key in checks and t[metric] is not None and t[metric] > checks[key]:
            issue(report, "configured_limit_exceeded", f"{metric} exceeds the author's configured limit; review intent.",
                  metric=metric, value=t[metric], limit=checks[key], **context)
    for name, limit in checks.get("max_anchor_step_px", {}).items():
        value = t["anchor_steps_px"].get(name)
        if value is None:
            issue(report, "missing_anchor", f"Configured anchor '{name}' is missing on one or both frames.", **context)
        elif value > limit:
            issue(report, "configured_limit_exceeded", f"Anchor '{name}' moves beyond the author's configured limit; review intent.",
                  metric="anchor_step_px", anchor=name, value=value, limit=limit, **context)


def analyze_state(name: str, state: Any, base_dir: Path) -> tuple[dict, list]:
    report = dict(name=name, issues=[], frames=[], transitions=[], loop_seam=None)
    loaded = []
    if not isinstance(state, dict) or not isinstance(state.get("frames"), list) or not state["frames"]:
        issue(report, "invalid_state", "Each state needs a nonempty frames list.", severity="error")
        return report, loaded
    loop = state.get("loop")
    if not isinstance(loop, bool):
        issue(report, "invalid_loop", "loop must explicitly be true or false.", severity="error")
    report["loop"] = loop if isinstance(loop, bool) else None
    checks = validate_checks(state.get("checks", {}), report)
    report["checks"] = checks
    first_size = None
    for index, frame in enumerate(state["frames"]):
        if not isinstance(frame, dict):
            issue(report, "invalid_frame", "Frame must be an object.", severity="error", frame=index)
            loaded.append(None)
            continue
        duration = frame.get("duration_ms")
        if not number(duration, positive=True):
            issue(report, "invalid_duration", "duration_ms must be a finite positive number.", severity="error", frame=index)
            duration = None
        hold = frame.get("hold", False)
        if not isinstance(hold, bool):
            issue(report, "invalid_hold", "hold must be a boolean.", severity="error", frame=index)
            hold = False
        anchors = frame.get("anchors", {})
        if not (isinstance(anchors, dict) and all(
            isinstance(k, str) and k and isinstance(v, list) and len(v) == 2
            and all(finite_number(n) for n in v)
            for k, v in anchors.items())):
            issue(report, "invalid_anchors", "anchors must map names to finite [x, y] pixel coordinates.", severity="error", frame=index)
            anchors = {}
        path = frame.get("path")
        if not isinstance(path, str) or not path:
            issue(report, "invalid_path", "Frame path must be a nonempty string.", severity="error", frame=index)
            loaded.append(None)
            continue
        try:
            with Image.open(base_dir / path) as source:
                if source.format != "PNG" or source.mode != "RGBA" or getattr(source, "n_frames", 1) != 1:
                    issue(report, "invalid_image_format", "Expected a single-frame RGBA PNG; export the individual frames first.", severity="error", frame=index)
                    loaded.append(None)
                    continue
                source.load()
                image = source.copy()
        except (OSError, ValueError, Image.DecompressionBombError) as exc:
            issue(report, "unreadable_frame", f"Cannot read frame ({type(exc).__name__}).", severity="error", frame=index)
            loaded.append(None)
            continue
        if first_size is None:
            first_size = image.size
        elif image.size != first_size:
            issue(report, "canvas_size_mismatch", "Frame dimensions differ from the first readable frame.", severity="error", frame=index)
        for anchor, point in list(anchors.items()):
            if not (0 <= point[0] < image.width and 0 <= point[1] < image.height):
                issue(report, "anchor_outside_canvas", f"Anchor '{anchor}' must lie inside the frame's canvas.", severity="error", frame=index)
                anchors = {k: v for k, v in anchors.items() if k != anchor}
        record = dict(index=index, path=path, duration_ms=duration, hold=hold,
                      anchors=anchors, size=list(image.size), fingerprint=fingerprint(image), **geometry(image))
        if record["alpha_bbox"] is None:
            issue(report, "empty_frame", "Frame has no nonzero alpha pixels; verify whether invisibility is intentional.", frame=index)
        else:
            margin = checks.get("edge_margin_px", 0)
            edges = [edge for edge, gap in record["margins_px"].items() if gap <= margin]
            if edges:
                issue(report, "edge_contact_risk", "Nonzero alpha is at or within the requested edge margin; clipping is possible, not proven.",
                      frame=index, edges=edges, margin_px=margin)
        report["frames"].append(record)
        loaded.append((record, image))
    for a, b in zip(loaded, loaded[1:]):
        if a is not None and b is not None:
            t = compare(a[0], b[0], a[1], b[1])
            report["transitions"].append(t)
            check_transition(t, checks, report)
    if loop is True and len(loaded) > 1 and loaded[0] is not None and loaded[-1] is not None:
        seam = compare(loaded[-1][0], loaded[0][0], loaded[-1][1], loaded[0][1])
        report["loop_seam"] = seam
        check_transition(seam, checks, report, seam=True)
    valid = [x for x in loaded if x is not None]
    durations = [r["duration_ms"] for r, _ in valid]
    all_durations_valid = len(valid) == len(loaded) and all(v is not None for v in durations)
    total_duration = sum(durations) if all_durations_valid else None
    if total_duration is not None and not finite_number(total_duration):
        issue(report, "invalid_total_duration", "Total duration exceeds a finite representable number.", severity="error")
        total_duration = None
    duplicates = sum(t.get("identical_visible_pixels", False) for t in report["transitions"])
    holds = sum(t.get("intentional_hold", False) for t in report["transitions"])
    report["summary"] = dict(requested_frames=len(loaded), readable_frames=len(valid),
                             unique_visible_frames=len({r["fingerprint"] for r, _ in valid}),
                             repeated_visible_frames=len(valid)-len({r["fingerprint"] for r, _ in valid}),
                             adjacent_repeat_transitions=duplicates, intentional_hold_transitions=holds,
                             unmarked_repeat_transitions=duplicates-holds,
                             repeat_transition_counts_exclude_loop_seam=True,
                             total_duration_ms=total_duration)
    return report, loaded


def analyze_manifest(manifest: Any, base_dir: Path) -> tuple[dict, dict]:
    report = dict(report_version=1, issues=[], states={},
                  interpretation="Measurements and review warnings only. No identity, style, motion-quality, or host-compatibility verdict.")
    loaded = {}
    if not isinstance(manifest, dict) or not isinstance(manifest.get("states"), dict) or not manifest["states"]:
        issue(report, "invalid_manifest", "Manifest needs a nonempty states object.", severity="error")
    else:
        for name, state in manifest["states"].items():
            report["states"][name], loaded[name] = analyze_state(name, state, base_dir)
    report["error_count"] = sum(i["severity"] == "error" for i in all_issues(report))
    report["warning_count"] = sum(i["severity"] == "warning" for i in all_issues(report))
    return report, loaded


def all_issues(report: dict) -> list:
    return report["issues"] + [i for state in report["states"].values() for i in state["issues"]]


def output_path(path: Path, sources: set[Path]) -> Path:
    if path.resolve() in sources:
        raise ValueError("An output path would overwrite the manifest or a source frame.")
    if path.exists():
        raise ValueError(f"Output already exists: {path}. Choose a new output path.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def contact_sheet(loaded: dict, path: Path) -> None:
    """Native-size tiles on a checkerboard; no rescaling or character edits."""
    tiles = [(name, r, im) for name, items in loaded.items() for item in items
             if item is not None for r, im in [item]]
    if not tiles:
        raise ValueError("No readable frames for contact sheet.")
    cell_w = max(im.width for _, _, im in tiles) + 16
    cell_h = max(im.height for _, _, im in tiles) + 40
    columns = min(4, len(tiles))
    size = (cell_w*columns, cell_h*math.ceil(len(tiles)/columns))
    if size[0]*size[1] > 40_000_000:
        raise ValueError("Contact sheet exceeds 40 million pixels; use a smaller manifest.")
    sheet = Image.new("RGB", size, "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for i, (name, record, im) in enumerate(tiles):
        x, y = (i % columns)*cell_w+8, (i//columns)*cell_h+8
        for by in range(0, im.height, 8):
            for bx in range(0, im.width, 8):
                color = "#bbbbbb" if (bx//8+by//8) % 2 else "#eeeeee"
                draw.rectangle((x+bx, y+by, x+min(bx+7, im.width-1), y+min(by+7, im.height-1)), fill=color)
        sheet.paste(im, (x, y), im)
        label = f"{name} #{record['index']} {record['duration_ms']} ms"
        draw.text((x, y+im.height+4), label.encode("ascii", "replace").decode("ascii")[:max(1, cell_w//6)], fill="black")
    sheet.save(path, format="PNG")


def preview_filename(index: int, name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-")[:40] or "state"
    return f"{index:03d}-{slug}.png"


def previews(loaded: dict, report: dict, directory: Path, sources: set[Path]) -> list[str]:
    outputs = []
    for i, (name, items) in enumerate(loaded.items(), 1):
        state = report["states"][name]
        if not items or any(item is None for item in items) or any(x["severity"] == "error" for x in state["issues"]):
            issue(report, "preview_skipped", f"Preview skipped for state '{name}': input errors.")
            continue
        records, images = zip(*items)
        durations = [r["duration_ms"] for r in records]
        # Pillow's APNG encoder uses integer milliseconds in a 16-bit numerator.
        if any(v != int(v) or not 1 <= v <= 65535 for v in durations):
            issue(report, "preview_skipped", f"Preview skipped for state '{name}': this writer requires whole-millisecond durations from 1 to 65535.")
            continue
        longest_hold = current_hold = 0
        previous = None
        for r in records:
            current_hold = current_hold+r["duration_ms"] if r["fingerprint"] == previous else r["duration_ms"]
            longest_hold = max(longest_hold, current_hold)
            previous = r["fingerprint"]
        if longest_hold > 65535:
            issue(report, "preview_skipped", f"Preview skipped for state '{name}': coalesced identical hold exceeds this writer's 65535 ms limit.")
            continue
        path = output_path(directory / preview_filename(i, name), sources)
        images[0].save(path, format="PNG", save_all=True, append_images=list(images[1:]),
                       duration=durations, loop=0 if state["loop"] else 1,
                       disposal=0, blend=0)
        outputs.append(str(path))
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path, help="JSON report; stdout if omitted. Existing outputs are not overwritten.")
    parser.add_argument("--contact-sheet", type=Path, help="Optional native-size PNG layout on checkerboard.")
    parser.add_argument("--preview-dir", type=Path, help="Optional APNG previews of the existing frames; no interpolation.")
    args = parser.parse_args(argv)
    try:
        def bad_constant(value: str) -> None:
            raise ValueError(f"Non-JSON numeric constant: {value}")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"), parse_constant=bad_constant)
        report, loaded = analyze_manifest(manifest, args.manifest.parent)
        sources = {args.manifest.resolve()}
        sources.update((args.manifest.parent / r["path"]).resolve() for items in loaded.values()
                       for item in items if item is not None for r, _ in [item])
        # Protect every named source, even an unreadable or invalid image.
        if isinstance(manifest, dict) and isinstance(manifest.get("states"), dict):
            for state in manifest["states"].values():
                if isinstance(state, dict) and isinstance(state.get("frames"), list):
                    sources.update((args.manifest.parent / f["path"]).resolve() for f in state["frames"]
                                   if isinstance(f, dict) and isinstance(f.get("path"), str))
        report["artifacts"] = {}
        planned = [p for p in (args.report, args.contact_sheet) if p is not None]
        if args.preview_dir:
            planned.extend(args.preview_dir / preview_filename(i, name)
                           for i, name in enumerate(loaded, 1))
        resolved = [p.resolve() for p in planned]
        if len(set(resolved)) != len(resolved):
            raise ValueError("Output paths must be distinct from one another.")
        if any(p in q.parents for p in resolved for q in resolved if p != q):
            raise ValueError("An output file cannot also be another output's directory.")
        for path in planned:
            output_path(path, sources)
        if args.contact_sheet:
            contact_sheet(loaded, output_path(args.contact_sheet, sources))
            report["artifacts"]["contact_sheet"] = str(args.contact_sheet)
        if args.preview_dir:
            report["artifacts"]["previews"] = previews(loaded, report, args.preview_dir, sources)
        report["warning_count"] = sum(i["severity"] == "warning" for i in all_issues(report))
        text = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.report:
            args.report.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 1 if report["error_count"] else 0
    except (OSError, ValueError) as exc:
        print(f"check_animation: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
