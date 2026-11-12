#!/usr/bin/env python3
"""
Unit and integration tests for niri-minimap.
Run with: python3 -m unittest discover -s tests -v
"""

import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "niri-minimap"
loader = importlib.machinery.SourceFileLoader("niri_minimap", str(SCRIPT_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
nm = importlib.util.module_from_spec(spec)
loader.exec_module(nm)


def make_win(
    wid: int,
    col: int,
    row: int = 1,
    width: float = 936.0,
    height: float = 994.0,
    ws_id: int = 1,
    ts_secs: int = 100,
) -> dict:
    return {
        "id": wid,
        "title": f"win-{wid}",
        "app_id": "kitty",
        "workspace_id": ws_id,
        "is_focused": False,
        "is_floating": False,
        "layout": {
            "pos_in_scrolling_layout": [col, row],
            "tile_size": [width, height],
            "window_size": [int(width), int(height)],
        },
        "focus_timestamp": {"secs": ts_secs, "nanos": 0},
    }


class TestNiriMinimap(unittest.TestCase):
    def test_single_column_returns_empty_strip_by_default(self):
        """A workspace with only 1 column should not clutter the screen with a 1-dot minimap."""
        engine = nm.MinimapEngine()
        w1 = make_win(1, col=1, width=1888.0)
        engine.windows = {1: w1}

        cols = engine.compute_strip_state(w1, 1920, 1080)
        self.assertEqual(len(cols), 1)
        self.assertEqual(engine.format_strip_plain(cols, min_columns=2), "")
        self.assertEqual(engine.format_strip_markup(cols, min_columns=2), "")

    def test_five_columns_focus_middle_shows_focused_visible_and_offscreen(self):
        """With 5 half-screen columns (936px on 1920px monitor) focused on col 3,
        two columns are visible and three are offscreen."""
        engine = nm.MinimapEngine()
        for c in range(1, 6):
            engine.windows[c] = make_win(c, col=c, width=936.0, ts_secs=100 + c)

        # Focus column 3
        cols = engine.compute_strip_state(engine.windows[3], 1920, 1080)
        self.assertEqual(len(cols), 5)
        self.assertTrue(cols[2]["is_focused"])

        plain = engine.format_strip_plain(cols)
        self.assertIn("▣", plain)
        self.assertIn("□", plain)
        self.assertTrue(plain.endswith("3/5"))

    def test_connection_with_niri_window_label_custom_names(self):
        """Columns containing windows renamed via niri-window-label must use diamond symbols (◈ / ◇)
        and gold Pango markup (#e0af68)."""
        engine = nm.MinimapEngine()
        for c in range(1, 4):
            engine.windows[c] = make_win(c, col=c, width=1888.0, ts_secs=100 + c)

        custom_names = {"1": "API Server"}
        # Focus column 3 while column 1 (offscreen) has a custom name
        cols = engine.compute_strip_state(engine.windows[3], 1920, 1080, custom_names=custom_names)
        self.assertTrue(cols[0]["has_custom"])
        self.assertFalse(cols[2]["has_custom"])

        plain = engine.format_strip_plain(cols)
        self.assertEqual(plain, "◇  □  ▣   3/3")

        markup = engine.format_strip_markup(cols)
        self.assertIn("#e0af68", markup)
        self.assertIn("3/3", markup)

        # Now focus column 1 (which has the custom name)
        cols_focused_custom = engine.compute_strip_state(
            engine.windows[1], 1920, 1080, custom_names=custom_names
        )
        plain_focused = engine.format_strip_plain(cols_focused_custom)
        self.assertEqual(plain_focused, "◈  □  □   1/3")

    def test_floating_window_returns_empty_strip(self):
        """Floating windows are not part of the scrolling column strip."""
        engine = nm.MinimapEngine()
        fw = make_win(99, col=1)
        fw["is_floating"] = True
        engine.windows = {99: fw}

        cols = engine.compute_strip_state(fw, 1920, 1080)
        self.assertEqual(cols, [])

    def test_i18n_and_custom_css_merging(self):
        """Verify locale detection and custom stylesheet merging."""
        self.assertEqual(nm.detect_language({"LANG": "es_MX.UTF-8"}), "es")
        self.assertEqual(nm.detect_language({"LANG": "en_US.UTF-8"}), "en")

        import tempfile

        base = b".minimap-box { border-radius: 12px; }"
        with tempfile.TemporaryDirectory() as tmp:
            css_path = Path(tmp) / "minimap.css"
            self.assertEqual(nm.build_stylesheet(base, css_path), base)
            css_path.write_text(".minimap-box { border-color: #e0af68; }", encoding="utf-8")
            self.assertIn(b"#e0af68", nm.build_stylesheet(base, css_path))


if __name__ == "__main__":
    unittest.main()
