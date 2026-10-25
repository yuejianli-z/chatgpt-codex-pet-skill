"""Temporary geometric fixtures test algorithms, never represent pet artwork."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_animation.py"
spec = importlib.util.spec_from_file_location("check_animation", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class AnimationChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def frame(self, name, *, box=(8, 8, 15, 15), size=(32, 32),
              fill=(90, 140, 220, 255), duration=100, **extra):
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        if box is not None:
            ImageDraw.Draw(image).rectangle(box, fill=fill)
        image.save(self.root / name)
        return dict(path=name, duration_ms=duration, **extra)

    def analyze(self, frames, *, loop=False, checks=None):
        manifest = {"states": {"synthetic": {"frames": frames, "loop": loop}}}
        if checks is not None:
            manifest["states"]["synthetic"]["checks"] = checks
        report, loaded = checker.analyze_manifest(manifest, self.root)
        return report, report["states"]["synthetic"], loaded

    def codes(self, state):
        return [issue["code"] for issue in state["issues"]]

    def test_normal_geometry_and_duration(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(9, 8, 16, 15), duration=150)]
        report, state, _ = self.analyze(frames)
        self.assertEqual(report["error_count"], 0)
        self.assertEqual(state["issues"], [])
        self.assertEqual(state["frames"][0]["alpha_bbox"], [8, 8, 16, 16])
        self.assertEqual(state["frames"][0]["alpha_centroid"], [11.5, 11.5])
        self.assertEqual(state["transitions"][0]["centroid_step_px"], 1)
        self.assertEqual(state["summary"]["total_duration_ms"], 250)
        self.assertIsNone(state["loop_seam"])

    def test_empty_and_edge_contact_are_observations(self):
        frames = [self.frame("empty.png", box=None), self.frame("edge.png", box=(0, 8, 4, 12))]
        report, state, _ = self.analyze(frames)
        self.assertEqual(report["error_count"], 0)
        self.assertIn("empty_frame", self.codes(state))
        self.assertIn("edge_contact_risk", self.codes(state))
        self.assertIsNone(state["frames"][0]["alpha_centroid"])
        self.assertIsNone(state["transitions"][0]["centroid_step_px"])

    def test_configurable_margin(self):
        frame = self.frame("close.png", box=(1, 8, 4, 12))
        _, default, _ = self.analyze([frame])
        _, configured, _ = self.analyze([frame], checks={"edge_margin_px": 1})
        self.assertNotIn("edge_contact_risk", self.codes(default))
        self.assertIn("edge_contact_risk", self.codes(configured))

    def test_size_mismatch_skips_pair_comparison(self):
        frames = [self.frame("a.png"), self.frame("wide.png", size=(40, 32))]
        report, state, _ = self.analyze(frames)
        self.assertEqual(report["error_count"], 1)
        self.assertIn("canvas_size_mismatch", self.codes(state))
        self.assertFalse(state["transitions"][0]["comparable"])

    def test_jump_is_not_automatically_failed(self):
        frames = [self.frame("ground.png", box=(10, 24, 15, 29)),
                  self.frame("air.png", box=(10, 2, 15, 7))]
        report, state, _ = self.analyze(frames)
        self.assertEqual(state["transitions"][0]["centroid_step_px"], 22)
        self.assertEqual(report["warning_count"], 0)
        self.assertEqual(report["error_count"], 0)

    def test_configured_motion_limit_is_review_warning(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(15, 8, 22, 15))]
        report, state, _ = self.analyze(frames, checks={"max_centroid_step_px": 2})
        self.assertEqual(report["error_count"], 0)
        self.assertIn("configured_limit_exceeded", self.codes(state))

    def test_state_thresholds_are_independent(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(15, 8, 22, 15))]
        manifest = {"states": {
            "idle": {"frames": frames, "loop": False, "checks": {"max_centroid_step_px": 2}},
            "jump": {"frames": frames, "loop": False},
        }}
        report, _ = checker.analyze_manifest(manifest, self.root)
        self.assertIn("configured_limit_exceeded", self.codes(report["states"]["idle"]))
        self.assertEqual(report["states"]["jump"]["issues"], [])

    def test_loop_seam_only_for_loop_intent(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(16, 8, 23, 15))]
        _, state, _ = self.analyze(frames, loop=True, checks={"max_loop_difference": 0})
        self.assertGreater(state["loop_seam"]["difference"], 0)
        seam_warnings = [i for i in state["issues"] if i.get("loop_seam")]
        self.assertEqual(len(seam_warnings), 1)
        self.assertEqual(seam_warnings[0]["code"], "configured_limit_exceeded")
        _, nonloop, _ = self.analyze(frames, checks={"max_loop_difference": 0})
        self.assertIsNone(nonloop["loop_seam"])
        self.assertEqual(nonloop["issues"], [])

    def test_loop_seam_has_no_default_failure_threshold(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(16, 8, 23, 15))]
        report, state, _ = self.analyze(frames, loop=True)
        self.assertGreater(state["loop_seam"]["difference"], 0)
        self.assertEqual(report["warning_count"], 0)

    def test_repeats_distinguish_declared_holds(self):
        frames = [self.frame("a.png"), self.frame("hold.png", hold=True, duration=500),
                  self.frame("repeat.png")]
        _, state, _ = self.analyze(frames)
        self.assertEqual(state["summary"]["repeated_visible_frames"], 2)
        self.assertEqual(state["summary"]["intentional_hold_transitions"], 1)
        self.assertEqual(state["summary"]["unmarked_repeat_transitions"], 1)
        self.assertEqual(self.codes(state), ["unmarked_repeat"])

    def test_hidden_rgb_is_not_visible_motion(self):
        a = self.frame("a.png")
        image = Image.open(self.root / "a.png").convert("RGBA")
        image.putpixel((0, 0), (255, 20, 90, 0))
        image.save(self.root / "b.png")
        b = dict(path="b.png", duration_ms=100, hold=True)
        _, state, _ = self.analyze([a, b])
        self.assertEqual(state["transitions"][0]["difference"], 0)
        self.assertTrue(state["transitions"][0]["identical_visible_pixels"])

    def test_faint_pixels_not_falsely_exact_duplicates(self):
        a = self.frame("a.png", fill=(1, 0, 0, 1))
        b = self.frame("b.png", fill=(2, 0, 0, 1))
        _, state, _ = self.analyze([a, b])
        self.assertFalse(state["transitions"][0]["identical_visible_pixels"])

    def test_author_anchors_and_missing_anchor(self):
        a = self.frame("a.png", anchors={"feet": [10, 15]})
        b = self.frame("b.png", box=(9, 8, 16, 15), anchors={"feet": [13, 15]})
        _, state, _ = self.analyze([a, b], checks={"max_anchor_step_px": {"feet": 1, "head": 1}})
        self.assertEqual(state["transitions"][0]["anchor_steps_px"]["feet"], 3)
        self.assertIn("configured_limit_exceeded", self.codes(state))
        self.assertIn("missing_anchor", self.codes(state))

    def test_bbox_size_limit(self):
        a = self.frame("a.png")
        b = self.frame("b.png", box=(8, 8, 20, 15))
        _, state, _ = self.analyze([a, b], checks={"max_bbox_size_step_px": 2})
        self.assertEqual(state["transitions"][0]["bbox_size_step_px"], 5)
        self.assertIn("configured_limit_exceeded", self.codes(state))

    def test_invalid_durations(self):
        frame = self.frame("a.png")
        for duration in (None, 0, -1, True, "100", float("nan"), float("inf"), 10**400):
            with self.subTest(duration=duration):
                report, state, _ = self.analyze([dict(frame, duration_ms=duration)])
                self.assertIn("invalid_duration", self.codes(state))
                self.assertIsNone(state["summary"]["total_duration_ms"])
                self.assertGreater(report["error_count"], 0)

    def test_invalid_manifest_and_loop(self):
        for manifest in ({}, [], {"states": {}}, {"states": {"x": {"frames": []}}}):
            report, _ = checker.analyze_manifest(manifest, self.root)
            self.assertGreater(report["error_count"], 0)
        report, state, _ = self.analyze([self.frame("a.png")], loop="true")
        self.assertIn("invalid_loop", self.codes(state))
        self.assertGreater(report["error_count"], 0)

    def test_invalid_settings_and_anchors(self):
        frame = self.frame("a.png", anchors={"feet": [1]})
        _, state, _ = self.analyze([frame], checks={"made_up": 1, "max_frame_difference": 3})
        self.assertIn("invalid_anchors", self.codes(state))
        self.assertEqual(self.codes(state).count("invalid_check"), 2)

    def test_missing_frame_does_not_join_nonadjacent_frames(self):
        frames = [self.frame("a.png"), {"path": "missing.png", "duration_ms": 100}, self.frame("b.png")]
        report, state, _ = self.analyze(frames)
        self.assertIn("unreadable_frame", self.codes(state))
        self.assertEqual(state["transitions"], [])
        self.assertEqual(state["summary"]["requested_frames"], 3)
        self.assertEqual(state["summary"]["readable_frames"], 2)
        self.assertEqual(report["error_count"], 1)

    def test_rgb_and_animation_are_rejected(self):
        Image.new("RGB", (20, 20), "red").save(self.root / "rgb.png")
        _, state, _ = self.analyze([{"path": "rgb.png", "duration_ms": 100}])
        self.assertIn("invalid_image_format", self.codes(state))
        images = [Image.new("RGBA", (20, 20), color) for color in ("red", "blue")]
        images[0].save(self.root / "animated.png", save_all=True, append_images=images[1:], duration=100)
        _, state, _ = self.analyze([{"path": "animated.png", "duration_ms": 100}])
        self.assertIn("invalid_image_format", self.codes(state))

    def test_contact_sheet_and_apng_are_readable_and_preserve_pixels(self):
        frames = [self.frame("a.png"), self.frame("b.png", box=(16, 8, 23, 15), duration=150)]
        report, _, loaded = self.analyze(frames, loop=False)
        checker.contact_sheet(loaded, self.root / "board.png")
        outputs = checker.previews(loaded, report, self.root / "previews", set())
        with Image.open(self.root / "board.png") as board:
            self.assertEqual(board.size, (96, 72))
        with Image.open(outputs[0]) as animation:
            self.assertEqual(animation.n_frames, 2)
            self.assertEqual(animation.info["loop"], 1)
            for i, frame in enumerate(frames):
                animation.seek(i)
                self.assertEqual(animation.info["duration"], frame["duration_ms"])
                with Image.open(self.root / frame["path"]) as source:
                    self.assertEqual(animation.convert("RGBA").tobytes(), source.tobytes())

    def test_apng_hold_may_coalesce_but_preserves_playback_duration(self):
        frames = [self.frame("a.png", duration=100), self.frame("hold.png", hold=True, duration=200),
                  self.frame("b.png", box=(16, 8, 23, 15), duration=150)]
        report, _, loaded = self.analyze(frames, loop=True)
        paths = checker.previews(loaded, report, self.root / "previews", set())
        with Image.open(paths[0]) as animation:
            self.assertEqual(animation.info["loop"], 0)
            total = 0
            for i in range(animation.n_frames):
                animation.seek(i)
                total += animation.info["duration"]
            self.assertEqual(total, 450)

    def test_preview_skips_unrepresentable_duration_without_changing_it(self):
        frames = [self.frame("a.png", duration=0.25)]
        report, _, loaded = self.analyze(frames)
        self.assertEqual(checker.previews(loaded, report, self.root / "previews", set()), [])
        self.assertEqual(report["issues"][0]["code"], "preview_skipped")
        self.assertEqual(report["states"]["synthetic"]["frames"][0]["duration_ms"], 0.25)

    def test_cli_report_exit_code_and_no_clobber(self):
        manifest = {"states": {"demo": {"frames": [self.frame("a.png")], "loop": False}}}
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        output = self.root / "report.json"
        self.assertEqual(checker.main([str(path), "--report", str(output)]), 0)
        self.assertEqual(json.loads(output.read_text())["error_count"], 0)
        before = path.read_bytes()
        with redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main([str(path), "--report", str(path)]), 2)
            self.assertEqual(checker.main([str(path), "--report", str(output)]), 2)
        self.assertEqual(path.read_bytes(), before)
        manifest["states"]["demo"]["frames"][0]["duration_ms"] = 0
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main([str(path)]), 1)

    def test_cli_rejects_non_json_nan(self):
        path = self.root / "bad.json"
        path.write_text('{"states": NaN}', encoding="utf-8")
        with redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main([str(path)]), 2)

    def test_extreme_numeric_inputs_are_structured_errors(self):
        a = self.frame("a.png", anchors={"marker": [10**400, 1]})
        report, state, _ = self.analyze([a], checks={"max_centroid_step_px": 10**400})
        self.assertIn("invalid_anchors", self.codes(state))
        self.assertIn("invalid_check", self.codes(state))
        self.assertEqual(report["error_count"], 2)
        frames = [self.frame("b.png", duration=1e308), self.frame("c.png", duration=1e308)]
        _, state, _ = self.analyze(frames)
        self.assertIn("invalid_total_duration", self.codes(state))
        self.assertIsNone(state["summary"]["total_duration_ms"])

    def test_outside_anchor_cannot_create_nonfinite_metrics(self):
        a = self.frame("a.png", anchors={"marker": [1e308, 1]})
        _, state, _ = self.analyze([a])
        self.assertIn("anchor_outside_canvas", self.codes(state))
        self.assertEqual(state["frames"][0]["anchors"], {})

    def test_preview_skips_excessive_coalesced_hold_duration(self):
        frames = [self.frame("a.png", duration=40000), self.frame("b.png", duration=40000, hold=True)]
        report, _, loaded = self.analyze(frames)
        self.assertEqual(checker.previews(loaded, report, self.root / "previews", set()), [])
        self.assertEqual(report["issues"][0]["code"], "preview_skipped")
        self.assertEqual(report["states"]["synthetic"]["summary"]["total_duration_ms"], 80000)

    def test_cli_output_collisions_are_rejected_before_writing(self):
        manifest = {"states": {"demo": {"frames": [self.frame("a.png")], "loop": False}}}
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        collision = self.root / "collision.png"
        with redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main([str(path), "--report", str(collision), "--contact-sheet", str(collision)]), 2)
        self.assertFalse(collision.exists())
        preview_dir = self.root / "previews"
        preview_path = preview_dir / "001-demo.png"
        with redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main([str(path), "--report", str(preview_path), "--preview-dir", str(preview_dir)]), 2)
        self.assertFalse(preview_path.exists())
        with redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main([str(path), "--report", str(preview_dir), "--preview-dir", str(preview_dir)]), 2)
        self.assertFalse(preview_dir.exists())


if __name__ == "__main__":
    unittest.main()
