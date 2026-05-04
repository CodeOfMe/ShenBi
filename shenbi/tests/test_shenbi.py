"""
Tests for the ShenBi library.
"""
import os
import sys
import tempfile

import numpy as np
import pytest

# Ensure offscreen mode for headless testing
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')


class TestFormatStringParser:
    def test_single_color(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('b') == ('b', '', '-')
        assert parse_format_string('r') == ('r', '', '-')
        assert parse_format_string('k') == ('k', '', '-')

    def test_single_marker(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('o') == (None, 'o', '')
        assert parse_format_string('s') == (None, 's', '')
        assert parse_format_string('^') == (None, '^', '')

    def test_color_marker(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('ro') == ('r', 'o', '')
        assert parse_format_string('g.') == ('g', '.', '')
        assert parse_format_string('or') == ('r', 'o', '')

    def test_color_linestyle(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('r-') == ('r', '', '-')
        assert parse_format_string('b--') == ('b', '', '--')
        assert parse_format_string('k:') == ('k', '', ':')
        assert parse_format_string('g-.') == ('g', '', '-.')

    def test_color_marker_linestyle(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('r-o') == ('r', 'o', '-')
        assert parse_format_string('b:o') == ('b', 'o', ':')

    def test_linestyle_only(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('--') == (None, '', '--')
        assert parse_format_string('-') == (None, '', '-')

    def test_empty_and_none(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('') == (None, '', '-')
        assert parse_format_string('None') == (None, '', '-')

    def test_marker_linestyle(self):
        from shenbi.utils import parse_format_string
        assert parse_format_string('o--') == (None, 'o', '--')


class TestColorResolution:
    def test_base_colors(self):
        from shenbi.colors import resolve_color
        assert resolve_color('b') == (31, 119, 180, 255)
        assert resolve_color('r') == (214, 39, 40, 255)
        assert resolve_color('g') == (44, 160, 44, 255)
        assert resolve_color('k') == (0, 0, 0, 255)
        assert resolve_color('w') == (255, 255, 255, 255)

    def test_css4_colors(self):
        from shenbi.colors import resolve_color
        assert resolve_color('red') == (255, 0, 0, 255)
        assert resolve_color('blue') == (0, 0, 255, 255)
        assert resolve_color('darkorange') == (255, 140, 0, 255)

    def test_hex_colors(self):
        from shenbi.colors import resolve_color
        assert resolve_color('#FF0000') == (255, 0, 0, 255)
        assert resolve_color('#F00') == (255, 0, 0, 255)
        assert resolve_color('#0f0') == (0, 255, 0, 255)

    def test_rgb_tuple(self):
        from shenbi.colors import resolve_color
        assert resolve_color((1.0, 0.0, 0.0)) == (255, 0, 0, 255)
        assert resolve_color((0.5, 0.5, 0.5)) == (127, 127, 127, 255)

    def test_alpha(self):
        from shenbi.colors import resolve_color
        assert resolve_color('r', alpha=0.5) == (214, 39, 40, 127)

    def test_none_returns_cycle_color(self):
        from shenbi.colors import resolve_color, _reset_color_cycle
        _reset_color_cycle()
        c1 = resolve_color(None)
        c2 = resolve_color(None)
        assert c1 != c2  # Should cycle through tab10 colors


class TestLine2D:
    def test_create_line(self):
        from shenbi.line import ShenBiLine2D
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        line = ShenBiLine2D(x, y, color='r')
        assert np.array_equal(line.get_xdata(), x)
        assert np.array_equal(line.get_ydata(), y)
        assert line.get_label() is None

    def test_label(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2, 3], [1, 2, 3], label='test')
        assert line.get_label() == 'test'

    def test_linewidth(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2], [1, 2], linewidth=3.0)
        assert line.get_linewidth() == 3.0
        line.set_linewidth(5.0)
        assert line.get_linewidth() == 5.0

    def test_linestyle(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2], [1, 2], linestyle='--')
        assert line.get_linestyle() == '--'

    def test_marker(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2], [1, 2], marker='o', linestyle='')
        assert line.get_marker() == 'o'

    def test_set_data(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2, 3], [4, 5, 6])
        line.set_data([10, 20, 30], [40, 50, 60])
        assert np.array_equal(line.get_xdata(), [10, 20, 30])
        assert np.array_equal(line.get_ydata(), [40, 50, 60])

    def test_zorder(self):
        from shenbi.line import ShenBiLine2D
        line = ShenBiLine2D([1, 2], [1, 2], zorder=10)
        assert line.get_zorder() == 10


class TestPyplot:
    def test_figure_creation(self):
        from shenbi.figure import ShenBiFigure
        fig = ShenBiFigure(num=1, figsize=(6, 4))
        assert fig.get_dpi() == 100
        w, h = fig.get_size_inches()
        assert w == pytest.approx(6.0, abs=0.5)
        assert h == pytest.approx(4.0, abs=0.5)

    def test_subplots_single(self):
        from shenbi.figure import ShenBiFigure
        fig = ShenBiFigure(figsize=(8, 4))
        fig, axes = fig.subplots(1, 1)
        assert axes is not None

    def test_subplots_grid(self):
        from shenbi.figure import ShenBiFigure
        fig = ShenBiFigure(figsize=(8, 8))
        fig, axes = fig.subplots(2, 3)
        assert axes.shape == (2, 3)

    def test_plot_basic(self):
        from shenbi import pyplot as plt
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.figure(figsize=(6, 4))
        lines = plt.plot(x, y, 'b-', label='sine')
        assert len(lines) == 1
        line = lines[0]
        assert np.array_equal(line.get_xdata(), x)
        assert np.array_equal(line.get_ydata(), y)
        assert line.get_label() == 'sine'

    def test_scatter(self):
        from shenbi import pyplot as plt
        x = np.random.randn(100)
        y = np.random.randn(100)
        plt.figure(figsize=(6, 4))
        scatter = plt.scatter(x, y, s=10, c='red', marker='o')
        assert scatter is not None

    def test_bar(self):
        from shenbi import pyplot as plt
        plt.figure(figsize=(6, 4))
        bar = plt.bar([0, 1, 2], [10, 20, 15], color='blue')
        assert bar is not None

    def test_hist(self):
        from shenbi import pyplot as plt
        data = np.random.randn(1000)
        plt.figure(figsize=(6, 4))
        n, bins, patches = plt.hist(data, bins=20)
        assert n is not None
        assert bins is not None

    def test_savefig(self):
        from shenbi import pyplot as plt
        x = np.linspace(0, 10, 100)
        plt.figure(figsize=(6, 4))
        plt.plot(x, np.sin(x))
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            fname = f.name
        try:
            plt.savefig(fname)
            assert os.path.getsize(fname) > 0
        finally:
            os.unlink(fname)

    def test_title_and_labels(self):
        from shenbi import pyplot as plt
        plt.figure()
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.title('Test Plot')
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')

    def test_grid_and_legend(self):
        from shenbi import pyplot as plt
        plt.figure()
        plt.plot([1, 2, 3], [1, 2, 3], label='Line 1')
        plt.grid(True)
        plt.legend()

    def test_axhline_axvline(self):
        from shenbi import pyplot as plt
        plt.figure()
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.axhline(y=2.0, color='r')
        plt.axvline(x=2.0, color='b')

    def test_multiple_datasets(self):
        from shenbi import pyplot as plt
        x = np.linspace(0, 10, 100)
        plt.figure()
        lines = plt.plot(x, np.sin(x), 'r-', x, np.cos(x), 'b--')
        assert len(lines) == 2

    def test_format_string_props(self):
        """Test that format strings properly set color and linestyle."""
        from shenbi import pyplot as plt
        x = np.linspace(0, 10, 100)
        plt.figure()
        lines = plt.plot(x, np.sin(x), 'r--')
        line = lines[0]
        assert line.get_linestyle() == '--'


class TestPerformance:
    """Performance tests to verify pyqtgraph-level speed."""

    def test_large_dataset_rendering(self):
        """1 million points should render quickly (< 3 seconds)."""
        import time
        from shenbi import pyplot as plt

        N = 100_000  # Reduced for CI; 1M tested separately
        x = np.linspace(0, 1000, N)
        y = np.sin(x) + 0.1 * np.random.randn(N)

        plt.figure(figsize=(12, 4))
        t0 = time.time()
        plt.plot(x, y, 'b-', linewidth=1)
        t1 = time.time()

        render_time = t1 - t0
        assert render_time < 3.0, f"Rendering {N} points took {render_time:.1f}s"

    def test_multiple_lines(self):
        """Multiple line plots should be fast."""
        import time
        from shenbi import pyplot as plt

        N = 10000
        x = np.linspace(0, 100, N)

        plt.figure(figsize=(8, 4))
        t0 = time.time()
        for i in range(10):
            plt.plot(x, np.sin(x + i * 0.5))
        t1 = time.time()

        assert (t1 - t0) < 2.0, f"Plotting 10 lines took {t1-t0:.1f}s"
