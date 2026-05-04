"""
ShenBiLine2D: matplotlib Line2D compatible wrapper around pyqtgraph PlotDataItem.

Provides the familiar matplotlib Line2D interface (get_xdata, set_xdata,
get_color, set_color, etc.) backed by pyqtgraph's high-performance PlotDataItem.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np
import pyqtgraph as pg

from .colors import resolve_color
from .utils import normalize_linestyle, normalize_marker


class ShenBiLine2D:
    """
    A matplotlib Line2D-compatible object wrapping pyqtgraph's PlotDataItem.

    This provides the get/set property pattern that matplotlib users expect,
    while leveraging pyqtgraph's efficient internal representation and rendering.

    Parameters
    ----------
    x : array-like
        x data
    y : array-like
        y data
    color : str or tuple, optional
        matplotlib color specification
    linewidth : float, optional
        Line width in points
    linestyle : str, optional
        '-', '--', '-.', ':', 'None', 'none', ''
    marker : str, optional
        matplotlib marker character
    markersize : float, optional
        Marker size
    markeredgecolor : str, optional
        Marker edge color
    markerfacecolor : str, optional
        Marker fill color
    alpha : float, optional
        Opacity (0-1)
    label : str, optional
        Legend label
    zorder : float, optional
        Drawing order
    visible : bool, optional
        Whether the artist is visible
    **kwargs : dict
        Additional properties
    """
    _zorder: float

    def __init__(
        self,
        x: Any = None,
        y: Any = None,
        *,
        color: Optional[str] = None,
        linewidth: Optional[float] = None,
        linestyle: Optional[str] = None,
        marker: Optional[str] = None,
        markersize: Optional[float] = None,
        markeredgecolor: Optional[str] = None,
        markerfacecolor: Optional[str] = None,
        alpha: Optional[float] = None,
        label: Optional[str] = None,
        zorder: Optional[float] = None,
        visible: bool = True,
        **kwargs: Any,
    ):
        self._x = np.asarray(x) if x is not None else np.array([])
        self._y = np.asarray(y) if y is not None else np.array([])

        # Store property values
        self._label = label
        self._zorder = zorder if zorder is not None else 2
        self._visible = visible
        self._alpha = alpha if alpha is not None else 1.0

        # Color
        self._color = color
        rgba = resolve_color(color, self._alpha)

        # Line properties
        self._linewidth = linewidth if linewidth is not None else 1.5
        self._linestyle = linestyle if linestyle is not None else '-'
        pen_style = normalize_linestyle(self._linestyle)
        pen = pg.mkPen(color=rgba, width=self._linewidth, style=pen_style)

        # Marker properties
        self._marker = marker
        self._markersize = markersize if markersize is not None else 6
        self._markeredgecolor = markeredgecolor
        self._markerfacecolor = markerfacecolor

        if marker and marker.lower() not in ('none', '', ' '):
            symbol = normalize_marker(marker)
            symbol_pen = pg.mkPen(color=rgba, width=1.0)
            symbol_brush = pg.mkBrush(color=rgba)
            symbol_size = self._markersize
        else:
            symbol = None
            symbol_pen = None
            symbol_brush = None
            symbol_size = 0

        from pyqtgraph.Qt import QtCore

        self._plot_data_item = pg.PlotDataItem(
            self._x, self._y,
            pen=pen if self._linewidth > 0 and pen_style != QtCore.Qt.PenStyle.NoPen else None,
            symbol=symbol,
            symbolPen=symbol_pen,
            symbolBrush=symbol_brush,
            symbolSize=symbol_size if symbol_size > 0 else None,
            name=label,
        )

    # ── Property Accessors (matplotlib Line2D compatible) ──────────────

    def get_xdata(self, orig: bool = True) -> np.ndarray:
        """Return the x data."""
        return self._x.copy() if orig else self._x

    def get_ydata(self, orig: bool = True) -> np.ndarray:
        """Return the y data."""
        return self._y.copy() if orig else self._y

    def set_xdata(self, x: Any) -> None:
        """Set the x data."""
        self._x = np.asarray(x, dtype=float)
        self._plot_data_item.setData(self._x, self._y)

    def set_ydata(self, y: Any) -> None:
        """Set the y data."""
        self._y = np.asarray(y, dtype=float)
        self._plot_data_item.setData(self._x, self._y)

    def set_data(self, *args: Any) -> None:
        """Set x and y data.

        Accepts: set_data(x, y) or set_data([x, y])
        """
        if len(args) == 1:
            xy = args[0]
            if isinstance(xy, dict):
                self._x = np.asarray(xy.get('x', self._x))
                self._y = np.asarray(xy.get('y', self._y))
            else:
                xy = np.asarray(xy)
                self._x = xy[0] if len(xy) == 2 else np.arange(len(xy[0]))
                self._y = xy[1] if len(xy) == 2 else xy[0]
        elif len(args) == 2:
            self._x = np.asarray(args[0], dtype=float)
            self._y = np.asarray(args[1], dtype=float)
        self._plot_data_item.setData(self._x, self._y)

    def get_color(self) -> Optional[str]:
        """Return the line color."""
        return self._color

    def set_color(self, color: Any) -> None:
        """Set the line color."""
        self._color = color
        rgba = resolve_color(color, self._alpha)
        pen = pg.mkPen(color=rgba, width=self._linewidth,
                       style=normalize_linestyle(self._linestyle))
        self._plot_data_item.setPen(pen)

    def get_linewidth(self) -> float:
        """Return the line width."""
        return self._linewidth

    def set_linewidth(self, lw: float) -> None:
        """Set the line width."""
        self._linewidth = float(lw)
        rgba = resolve_color(self._color, self._alpha)
        pen = pg.mkPen(color=rgba, width=self._linewidth,
                       style=normalize_linestyle(self._linestyle))
        self._plot_data_item.setPen(pen)

    def get_linestyle(self) -> str:
        """Return the line style string."""
        return self._linestyle

    def set_linestyle(self, ls: str) -> None:
        """Set the line style."""
        self._linestyle = ls
        rgba = resolve_color(self._color, self._alpha)
        pen = pg.mkPen(color=rgba, width=self._linewidth,
                       style=normalize_linestyle(ls))
        self._plot_data_item.setPen(pen)

    def get_marker(self) -> Optional[str]:
        """Return the marker style."""
        return self._marker

    def set_marker(self, marker: Any) -> None:
        """Set the marker style."""
        self._marker = str(marker) if marker else None
        if marker and str(marker).lower() not in ('none', '', ' '):
            self._markersize = self._markersize if self._markersize and self._markersize > 0 else 6
            symbol = normalize_marker(str(marker))
            rgba = resolve_color(self._color, self._alpha)
            pen_style = normalize_linestyle(self._linestyle)
            pen = pg.mkPen(color=rgba, width=self._linewidth, style=pen_style)
            sym_pen = pg.mkPen(color=rgba, width=1.0)
            sym_brush = pg.mkBrush(color=rgba)
            from pyqtgraph.Qt import QtCore
            self._plot_data_item.setData(
                self._x, self._y,
                pen=pen if self._linewidth > 0 and pen_style != QtCore.Qt.PenStyle.NoPen else None,
                symbol=symbol,
                symbolSize=self._markersize,
                symbolPen=sym_pen,
                symbolBrush=sym_brush,
                name=self._label,
            )
        else:
            self._plot_data_item.setSymbol(None)

    def get_markersize(self) -> float:
        """Return the marker size."""
        return self._markersize

    def set_markersize(self, ms: float) -> None:
        """Set the marker size."""
        self._markersize = float(ms)
        self._plot_data_item.setSymbolSize(self._markersize)

    def get_markeredgecolor(self) -> Optional[str]:
        """Return the marker edge color."""
        return self._markeredgecolor

    def set_markeredgecolor(self, color: Any) -> None:
        """Set the marker edge color."""
        self._markeredgecolor = color
        rgba = resolve_color(color)
        self._plot_data_item.setSymbolPen(pg.mkPen(color=rgba))

    def get_markerfacecolor(self) -> Optional[str]:
        """Return the marker face color."""
        return self._markerfacecolor

    def set_markerfacecolor(self, color: Any) -> None:
        """Set the marker face color."""
        self._markerfacecolor = color
        rgba = resolve_color(color)
        self._plot_data_item.setSymbolBrush(pg.mkBrush(color=rgba))

    def get_alpha(self) -> float:
        """Return the alpha (opacity)."""
        return self._alpha

    def set_alpha(self, alpha: float) -> None:
        """Set the alpha (opacity)."""
        self._alpha = float(alpha)
        self._plot_data_item.setOpacity(self._alpha)

    def get_label(self) -> Optional[str]:
        """Return the legend label."""
        return self._label

    def set_label(self, label: str) -> None:
        """Set the legend label."""
        self._label = label
        self._plot_data_item.setData(self._x, self._y, name=label)

    def get_zorder(self) -> float:
        """Return the z-order."""
        return self._zorder

    def set_zorder(self, zorder: float) -> None:
        """Set the z-order."""
        self._zorder = float(zorder)
        self._plot_data_item.setZValue(self._zorder)

    def get_visible(self) -> bool:
        """Return visibility."""
        return self._visible

    def set_visible(self, visible: bool) -> None:
        """Set visibility."""
        self._visible = bool(visible)
        self._plot_data_item.setVisible(self._visible)

    def remove(self) -> None:
        """Remove this artist from its parent."""
        scene = self._plot_data_item.scene()
        if scene is not None:
            scene.removeItem(self._plot_data_item)

    @property
    def plot_data_item(self) -> pg.PlotDataItem:
        """Get the underlying pyqtgraph PlotDataItem."""
        return self._plot_data_item


class ShenBiScatter:
    """
    A matplotlib PathCollection-compatible scatter wrapper.
    """

    def __init__(
        self,
        x: Any,
        y: Any,
        *,
        s: Optional[Any] = None,
        c: Optional[Any] = None,
        marker: str = 'o',
        alpha: Optional[float] = None,
        edgecolors: Optional[str] = None,
        linewidths: Optional[float] = None,
        label: Optional[str] = None,
        **kwargs: Any,
    ):
        self._x = np.asarray(x, dtype=float)
        self._y = np.asarray(y, dtype=float)
        self._label = label

        symbol = normalize_marker(marker)
        size = float(np.asarray(s).flat[0]) if s is not None else 10.0

        c_arr = np.asarray(c) if c is not None else None
        per_point_color = False
        if c_arr is not None and c_arr.ndim == 2 and c_arr.shape[1] >= 3:
            per_point_color = True
            brushes = []
            for row in c_arr:
                r, g, b = int(row[0]), int(row[1]), int(row[2])
                a = int(row[3]) if c_arr.shape[1] > 3 else 255
                brushes.append(pg.mkBrush(color=(r, g, b, a)))
        elif c_arr is not None and c_arr.ndim == 2 and c_arr.shape[0] == len(self._x):
            per_point_color = True
            brushes = []
            for row in c_arr:
                brushes.append(pg.mkBrush(color=tuple(int(v) for v in row)))

        if per_point_color:
            from pyqtgraph.Qt import QtGui
            edge_pen = pg.mkPen(color=(0, 0, 0, 0), width=0)
            if edgecolors is not None:
                edge_rgba = resolve_color(edgecolors)
                edge_pen = pg.mkPen(color=edge_rgba, width=linewidths or 1.0)
            spots = []
            for i in range(len(self._x)):
                spots.append({
                    'x': float(self._x[i]),
                    'y': float(self._y[i]),
                    'size': size,
                    'symbol': symbol,
                    'brush': brushes[i],
                    'pen': edge_pen,
                })
            self._scatter_item = pg.ScatterPlotItem(spots=spots, name=label)
        else:
            color_val = c if c is not None else None
            rgba = resolve_color(color_val, alpha)
            edge_pen = None
            if edgecolors is not None:
                edge_rgba = resolve_color(edgecolors)
                edge_pen = pg.mkPen(color=edge_rgba, width=linewidths or 1.0)
            else:
                edge_pen = pg.mkPen(color=rgba, width=0)

            self._scatter_item = pg.ScatterPlotItem(
                x=self._x, y=self._y,
                symbol=symbol,
                size=size,
                pen=edge_pen,
                brush=pg.mkBrush(color=rgba),
                name=label,
            )

    @property
    def scatter_item(self) -> pg.ScatterPlotItem:
        """Get the underlying pyqtgraph ScatterPlotItem."""
        return self._scatter_item

    def get_offsets(self) -> np.ndarray:
        """Return the (x, y) offsets."""
        return np.column_stack([self._x, self._y])

    def set_offsets(self, offsets: Any) -> None:
        """Set the (x, y) offsets."""
        offsets = np.asarray(offsets)
        self._x = offsets[:, 0]
        self._y = offsets[:, 1]
        self._scatter_item.setData(x=self._x, y=self._y)

    def get_facecolor(self) -> Any:
        """Return the face color."""
        return self._scatter_item.opts.get('brush', None)

    def set_facecolor(self, color: Any) -> None:
        """Set the face color."""
        rgba = resolve_color(color)
        self._scatter_item.setBrush(pg.mkBrush(color=rgba))

    def get_edgecolor(self) -> Any:
        """Return the edge color."""
        return self._scatter_item.opts.get('pen', None)

    def set_edgecolor(self, color: Any) -> None:
        """Set the edge color."""
        rgba = resolve_color(color)
        self._scatter_item.setPen(pg.mkPen(color=rgba))

    def get_sizes(self) -> Any:
        """Return the marker sizes."""
        return self._scatter_item.opts.get('size', 10)

    def set_sizes(self, sizes: Any) -> None:
        """Set the marker sizes."""
        self._scatter_item.setSize(sizes)

    def remove(self) -> None:
        """Remove this artist from its parent."""
        scene = self._scatter_item.scene()
        if scene is not None:
            scene.removeItem(self._scatter_item)
