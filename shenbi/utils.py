"""
Format string parser and argument processing utilities.

Parses matplotlib-style format strings like 'r-o', 'b--', 'g.', etc.
Format: [color][marker][linestyle] in any order.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# ── Marker mapping: matplotlib marker → pyqtgraph symbol ──────────────
MARKER_MAP: dict[str, str] = {
    '.': 'o',        # point → small circle (pyqtgraph has no point)
    ',': 'o',        # pixel → small circle
    'o': 'o',        # circle
    'v': 't1',       # triangle_down
    '^': 't',        # triangle_up
    '<': 't3',       # triangle_left → t3 in pyqtgraph
    '>': 't2',       # triangle_right → t2 in pyqtgraph
    '1': 't1',       # tri_down
    '2': 't',        # tri_up
    '3': 't3',       # tri_left
    '4': 't2',       # tri_right
    '8': 'o',        # octagon → circle fallback
    's': 's',        # square
    'p': 's',        # pentagon → square fallback
    '*': 'star',     # star
    'h': 's',        # hexagon1 → square fallback
    'H': 's',        # hexagon2 → square fallback
    '+': '+',        # plus
    'x': 'x',        # x
    'D': 'd',        # diamond
    'd': 'd',        # thin_diamond
    '|': 'x',        # vline → x fallback
    '_': 'x',        # hline → x fallback
    'P': '+',        # plus_filled → plus
    'X': 'x',        # x_filled
    '': '',          # no marker
    'None': '',      # no marker
    'none': '',      # no marker
    ' ': '',         # no marker
}

# ── Line style mapping: matplotlib → pyqtgraph ──────────────────────────
# Use Qt.PenStyle enum for cross-binding compatibility
def _get_pen_style(style_name: str):
    from pyqtgraph.Qt import QtCore
    styles = {
        'solid': QtCore.Qt.PenStyle.SolidLine,
        'dashed': QtCore.Qt.PenStyle.DashLine,
        'dashdot': QtCore.Qt.PenStyle.DashDotLine,
        'dotted': QtCore.Qt.PenStyle.DotLine,
        'none': QtCore.Qt.PenStyle.NoPen,
    }
    return styles.get(style_name, QtCore.Qt.PenStyle.SolidLine)

LINESTYLE_MAP: dict[str, str] = {
    '-': 'solid',
    '--': 'dashed',
    '-.': 'dashdot',
    ':': 'dotted',
    'solid': 'solid',
    'dashed': 'dashed',
    'dashdot': 'dashdot',
    'dotted': 'dotted',
    'None': 'none',
    'none': 'none',
    '': 'none',
    ' ': 'none',
}

# ── Single-letter color codes (used in format strings) ────────────────
FMT_COLORS = {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}

# ── C0-C9 color cycle codes ──────────────────────────────────────────
FMT_C_COLORS = {f'C{i}' for i in range(10)}

# ── Marker characters used in format strings ──────────────────────────
FMT_MARKERS = set(MARKER_MAP.keys())
FMT_MARKERS.discard('')
FMT_MARKERS.discard('None')
FMT_MARKERS.discard('none')
FMT_MARKERS.discard(' ')

# ── Line style characters used in format strings ──────────────────────
FMT_LINESTYLES = {'-', '--', '-.', ':'}


def parse_format_string(fmt: str) -> Tuple[Optional[str], str, str]:
    """
    Parse a matplotlib-style format string.

    Args:
        fmt: Format string like 'ro-', 'b--', 'g.', '-r', etc.

    Returns:
        Tuple of (color, marker, linestyle).
        - color: string color spec or None
        - marker: pyqtgraph symbol string
        - linestyle: string ('-' or '--' or '-.' or ':' or '')
    """
    if not fmt or fmt == 'None':
        return None, '', '-'

    fmt = fmt.strip()

    if fmt in FMT_COLORS:
        return fmt, '', '-'

    if fmt in FMT_MARKERS:
        return None, fmt, ''

    # C0-C9 color cycle codes
    if len(fmt) == 2 and fmt in FMT_C_COLORS:
        return fmt, '', '-'

    # Two-char: pure color+marker combination (no linestyle)
    if len(fmt) == 2:
        c0, c1 = fmt[0], fmt[1]
        if c0 in FMT_COLORS and c1 in FMT_MARKERS:
            return c0, c1, ''
        if c1 in FMT_COLORS and c0 in FMT_MARKERS:
            return c1, c0, ''

    color: Optional[str] = None
    marker: str = ''
    linestyle: str = ''
    linestyle_found: bool = False

    i = 0
    n = len(fmt)

    while i < n:
        if i + 2 <= n and fmt[i:i + 2] in FMT_C_COLORS:
            color = fmt[i:i + 2]
            i += 2
            continue
        if i + 1 < n and fmt[i:i + 2] in FMT_LINESTYLES:
            linestyle = fmt[i:i + 2]
            linestyle_found = True
            i += 2
            continue
        c = fmt[i]
        if c in FMT_COLORS and color is None:
            color = c
        elif c in FMT_MARKERS and not marker:
            marker = c
        elif c in FMT_LINESTYLES and not linestyle_found:
            linestyle = c
            linestyle_found = True
        i += 1

    if not linestyle_found:
        if marker:
            linestyle = ''
        else:
            linestyle = '-'

    return color, marker, linestyle


def process_plot_args(
    *args: Any,
    data: Optional[Any] = None,
    **kwargs: Any,
) -> List[Tuple[np.ndarray, np.ndarray, Optional[str], Dict[str, Any]]]:
    """
    Process matplotlib-style plot arguments into (x, y, fmt, props) tuples.

    Handles all matplotlib calling conventions:
    - plot(y)
    - plot(x, y)
    - plot(x, y, 'fmt')
    - plot(x1, y1, 'fmt1', x2, y2, 'fmt2', ...)
    - plot(x, y, 'fmt', **kwargs)

    Args:
        *args: Variable plot arguments
        data: Optional dict-like for indexed data access (matplotlib compatibility)
        **kwargs: Keyword properties applied to all datasets

    Returns:
        List of (x, y, fmt_string, line_properties) tuples
    """
    datasets: List[Tuple[np.ndarray, np.ndarray, Optional[str], Dict[str, Any]]] = []

    extracted_kwargs = {k: v for k, v in kwargs.items()
                        if k != 'data'}

    if not args:
        return datasets

    all_args = list(args)

    def _grab_next_arg():
        return all_args.pop(0) if all_args else None

    while all_args:
        arg1 = _grab_next_arg()
        if arg1 is None:
            break

        x: Any
        y: Any
        fmt: Optional[str] = None

        arg2 = _grab_next_arg()

        if arg2 is None:
            # plot(y) - single argument
            y = np.asarray(arg1)
            x = np.arange(len(y))
        elif isinstance(arg2, str):
            # plot(x, y, fmt) or plot(y, fmt) or plot(x, 'fmt')
            # Check: is arg1 numeric?
            try:
                np.asarray(arg1, dtype=float)
                is_numeric = True
            except (ValueError, TypeError):
                is_numeric = False

            if is_numeric:
                y = np.asarray(arg1) if not isinstance(arg1, np.ndarray) else arg1
                x = np.arange(len(y))
                fmt = arg2
                # Put arg2 back? No, it's the fmt
            else:
                # arg1 is likely x, arg2 is fmt
                y = np.asarray(_grab_next_arg()) if _grab_next_arg() is not None else np.asarray([])
                x = np.asarray(arg1)
                fmt = arg2
        else:
            # plot(x, y, ...)
            x = np.asarray(arg1)
            y = np.asarray(arg2)

            # Check if next arg is a format string
            if all_args and isinstance(all_args[0], str):
                fmt = _grab_next_arg()

        # Parse kwargs
        line_kwargs = dict(extracted_kwargs)

        if fmt is not None:
            color, marker, linestyle = parse_format_string(fmt)
            if color and 'color' not in line_kwargs:
                line_kwargs['color'] = color
            if marker and 'marker' not in line_kwargs:
                line_kwargs['marker'] = marker
            if linestyle and 'linestyle' not in line_kwargs:
                line_kwargs['linestyle'] = linestyle

        datasets.append((x, y, fmt, line_kwargs))

    return datasets


def normalize_marker(marker_spec: Any) -> str:
    """Convert a matplotlib marker spec to pyqtgraph symbol string."""
    if marker_spec is None:
        return ''
    s = str(marker_spec)
    return MARKER_MAP.get(s, 'o')


def normalize_linestyle(style_spec: Any):
    """Convert a matplotlib linestyle spec to Qt.PenStyle enum."""
    if style_spec is None:
        return _get_pen_style('none')
    s = str(style_spec)
    style_name = LINESTYLE_MAP.get(s, 'solid')
    return _get_pen_style(style_name)
