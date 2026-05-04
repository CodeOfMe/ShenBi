"""
ShenBiAxes: matplotlib Axes-compatible wrapper around pyqtgraph PlotItem.

Provides the familiar matplotlib Axes interface (plot, scatter, bar,
set_title, set_xlabel, etc.) backed by pyqtgraph's high-performance PlotItem.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pyqtgraph as pg

from .colors import resolve_color
from .line import ShenBiLine2D, ShenBiScatter
from .utils import process_plot_args, normalize_linestyle, normalize_marker


def _apply_matplotlib_style(plot_item: 'pg.PlotItem') -> None:
    """Apply matplotlib-like styling to a pyqtgraph PlotItem."""
    for axis_name in ('bottom', 'left'):
        axis = plot_item.getAxis(axis_name)
        axis.setPen(pg.mkPen(color='#333333', width=1))
        axis.setTextPen(pg.mkPen(color='#333333'))
        axis.setStyle(showValues=True)
    for axis_name in ('top', 'right'):
        axis = plot_item.getAxis(axis_name)
        axis.setPen(pg.mkPen(color='#cccccc', width=0))
        axis.setStyle(showValues=False)


class ShenBiAxes:
    """
    A matplotlib Axes-compatible object wrapping pyqtgraph's PlotItem.

    Each ShenBiAxes corresponds to a single subplot with its own x/y axes,
    view box, and collection of plot items.

    Parameters
    ----------
    plot_item : pg.PlotItem
        The underlying pyqtgraph PlotItem to wrap
    """
    _shenbi_lines: List[ShenBiLine2D]
    _shenbi_scatters: List[ShenBiScatter]

    def __init__(self, plot_item: pg.PlotItem):
        self._plot_item = plot_item
        self._shenbi_lines = []
        self._shenbi_scatters = []
        self._legend = None
        _apply_matplotlib_style(plot_item)

    # ── Plotting Methods ──────────────────────────────────────────────

    def plot(self, *args: Any, scalex: bool = True, scaley: bool = True,
             data: Optional[Any] = None, **kwargs: Any) -> List[ShenBiLine2D]:
        """
        Plot y versus x as lines and/or markers.

        Call signatures:
            plot(y)                 # y only, x auto-index
            plot(x, y)              # x, y
            plot(x, y, 'r--')       # with format string
            plot(x1, y1, 'g-', x2, y2, 'b:')  # multiple datasets

        Parameters
        ----------
        *args : array-like or str
            x, y, and optional format string
        scalex, scaley : bool
            Whether to auto-scale axes
        data : dict-like, optional
            Indexable data source
        **kwargs : dict
            Line2D properties (color, linewidth, linestyle, marker, etc.)

        Returns
        -------
        list of ShenBiLine2D
        """
        datasets = process_plot_args(*args, data=data, **kwargs)
        lines = []

        for x, y, fmt, props in datasets:
            line = ShenBiLine2D(x, y, **props)
            self._plot_item.addItem(line.plot_data_item)
            self._shenbi_lines.append(line)
            lines.append(line)

        if scalex and datasets:
            self._plot_item.enableAutoRange(axis='x')
            self._plot_item.autoRange()
        if scaley and datasets:
            self._plot_item.enableAutoRange(axis='y')
            self._plot_item.autoRange()

        self._update_legend()
        return lines

    def scatter(self, x: Any, y: Any,
                s: Optional[Any] = None,
                c: Optional[Any] = None,
                marker: str = 'o',
                cmap: Optional[Any] = None,
                norm: Optional[Any] = None,
                vmin: Optional[float] = None,
                vmax: Optional[float] = None,
                alpha: Optional[float] = None,
                linewidths: Optional[float] = None,
                *,
                edgecolors: Optional[str] = None,
                colorizer: Optional[Any] = None,
                plotnonfinite: bool = False,
                data: Optional[Any] = None,
                **kwargs: Any) -> ShenBiScatter:
        """
        A scatter plot of y vs x with varying marker size and/or color.

        Parameters
        ----------
        x, y : array-like
            Data positions
        s : float or array-like, optional
            Marker size
        c : str, array-like, optional
            Marker color — scalar array for colormap mapping
        marker : str, optional
            Marker style
        cmap : str or Colormap, optional
            Colormap for mapping c values to colors
        alpha : float, optional
            Opacity
        edgecolors : str, optional
            Edge color of markers
        linewidths : float, optional
            Width of marker edges
        label : str, optional
            Legend label

        Returns
        -------
        ShenBiScatter
        """
        from .cm import get_cmap as _get_cmap

        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if c is not None and not isinstance(c, str):
            c_arr = np.asarray(c, dtype=float)
            if c_arr.ndim >= 1 and c_arr.shape[0] == len(x):
                cmap_obj = _get_cmap(cmap) if cmap is not None else _get_cmap('viridis')
                lo = vmin if vmin is not None else float(np.nanmin(c_arr))
                hi = vmax if vmax is not None else float(np.nanmax(c_arr))
                rng = hi - lo if hi != lo else 1.0
                c_norm = (c_arr - lo) / rng
                colors = cmap_obj(np.clip(c_norm, 0, 1), bytes=True)

                scatter = ShenBiScatter(
                    x, y, s=s, c=colors, marker=marker,
                    alpha=alpha, edgecolors=edgecolors,
                    linewidths=linewidths, label=kwargs.get('label', None),
                )
                self._plot_item.addItem(scatter.scatter_item)
                self._shenbi_scatters.append(scatter)
                if len(x) > 0:
                    x_pad = (x.max() - x.min()) * 0.05 or 1.0
                    y_pad = (y.max() - y.min()) * 0.05 or 1.0
                    self._plot_item.setXRange(x.min() - x_pad, x.max() + x_pad, padding=0)
                    self._plot_item.setYRange(y.min() - y_pad, y.max() + y_pad, padding=0)
                self._update_legend()
                return scatter

        scatter = ShenBiScatter(
            x, y,
            s=s, c=c, marker=marker,
            alpha=alpha,
            edgecolors=edgecolors,
            linewidths=linewidths,
            label=kwargs.get('label', None),
        )
        self._plot_item.addItem(scatter.scatter_item)
        self._shenbi_scatters.append(scatter)
        if len(x) > 0:
            x_pad = (x.max() - x.min()) * 0.05 or 1.0
            y_pad = (y.max() - y.min()) * 0.05 or 1.0
            self._plot_item.setXRange(x.min() - x_pad, x.max() + x_pad, padding=0)
            self._plot_item.setYRange(y.min() - y_pad, y.max() + y_pad, padding=0)
        self._update_legend()
        return scatter

    def bar(self, x: Any, height: Any,
            width: float = 0.8,
            bottom: Optional[Any] = None,
            *,
            align: str = 'center',
            data: Optional[Any] = None,
            **kwargs: Any) -> pg.BarGraphItem:
        """Make a bar plot."""
        x = np.asarray(x, dtype=float)
        height = np.asarray(height, dtype=float)

        if align == 'edge':
            x = x + width / 2.0

        x0 = x - width / 2.0
        x1 = x + width / 2.0
        y0 = np.asarray(bottom, dtype=float) if bottom is not None else np.zeros_like(height)
        y1 = y0 + height

        color = kwargs.get('color', None)
        if isinstance(color, (list, tuple, np.ndarray)) and len(color) > 0:
            color = color[0]
        rgba = resolve_color(color)

        edge_color = kwargs.get('edgecolor', kwargs.get('edgecolors', None))
        if edge_color is not None:
            edge_rgba = resolve_color(edge_color)
        else:
            edge_rgba = rgba

        pen = pg.mkPen(color=edge_rgba, width=kwargs.get('linewidth', 1.0))

        bar_item = pg.BarGraphItem(
            x0=x0, x1=x1, y0=y0, y1=y1,
            brush=pg.mkBrush(color=rgba),
            pen=pen,
        )
        self._plot_item.addItem(bar_item)
        if len(x0) > 0:
            x_pad = (x1.max() - x0.min()) * 0.05 or 0.5
            y_min = min(y0.min(), 0)
            y_pad = (y1.max() - y_min) * 0.05 or 1.0
            self._plot_item.setXRange(x0.min() - x_pad, x1.max() + x_pad, padding=0)
            self._plot_item.setYRange(y_min - y_pad, y1.max() + y_pad, padding=0)
        return bar_item

    def barh(self, y: Any, width: Any,
             height: float = 0.8,
             left: Optional[Any] = None,
             *,
             align: str = 'center',
             **kwargs: Any) -> pg.BarGraphItem:
        """Make a horizontal bar plot."""
        y_pos = np.asarray(y, dtype=float)
        w = np.asarray(width, dtype=float)

        if align == 'edge':
            y_pos = y_pos + height / 2.0

        y0 = y_pos - height / 2.0
        y1 = y_pos + height / 2.0
        x0 = np.asarray(left, dtype=float) if left is not None else np.zeros_like(w)
        x1 = x0 + w

        color = kwargs.get('color', None)
        if isinstance(color, (list, tuple, np.ndarray)) and len(color) > 0:
            color = color[0]
        rgba = resolve_color(color)

        edge_color = kwargs.get('edgecolor', kwargs.get('edgecolors', None))
        edge_rgba = resolve_color(edge_color) if edge_color is not None else rgba

        bar_item = pg.BarGraphItem(
            x0=x0, x1=x1, y0=y0, y1=y1,
            brush=pg.mkBrush(color=rgba),
            pen=pg.mkPen(color=edge_rgba, width=kwargs.get('linewidth', 1.0)),
        )
        self._plot_item.addItem(bar_item)
        if len(y0) > 0:
            y_pad = (y1.max() - y0.min()) * 0.05 or 0.5
            x_min = min(x0.min(), 0)
            x_pad = (x1.max() - x_min) * 0.05 or 1.0
            self._plot_item.setXRange(x_min - x_pad, x1.max() + x_pad, padding=0)
            self._plot_item.setYRange(y0.min() - y_pad, y1.max() + y_pad, padding=0)
        return bar_item

    def errorbar(self, x: Any, y: Any,
                 yerr: Optional[Any] = None,
                 xerr: Optional[Any] = None,
                 fmt: str = '',
                 ecolor: Optional[str] = None,
                 elinewidth: Optional[float] = None,
                 capsize: Optional[float] = None,
                 barsabove: bool = False,
                 lolims: bool = False, uplims: bool = False,
                 xlolims: bool = False, xuplims: bool = False,
                 errorevery: int = 1,
                 capthick: Optional[float] = None,
                 *,
                 data: Optional[Any] = None,
                 **kwargs: Any) -> Tuple[ShenBiLine2D, pg.ErrorBarItem]:
        """
        Plot y versus x with error bars.

        Returns
        -------
        tuple of (ShenBiLine2D, pg.ErrorBarItem)
        """
        line = self.plot(x, y, fmt, **kwargs)[0]

        if yerr is not None:
            err_item = pg.ErrorBarItem(
                x=np.asarray(x, dtype=float),
                y=np.asarray(y, dtype=float),
                height=np.asarray(yerr, dtype=float),
                beam=capsize or 0.0,
                pen=pg.mkPen(
                    color=resolve_color(ecolor or kwargs.get('color', None)),
                    width=elinewidth or 1.0,
                ),
            )
            self._plot_item.addItem(err_item)
            return line, err_item

        return line, _DummyErrorBar()

    def fill_between(self, x: Any, y1: Any, y2: Any = 0,
                     where: Optional[Any] = None,
                     interpolate: bool = False,
                     step: Optional[str] = None,
                     *,
                     data: Optional[Any] = None,
                     **kwargs: Any) -> pg.FillBetweenItem:
        """
        Fill the area between two horizontal curves.

        Returns
        -------
        pyqtgraph.FillBetweenItem
        """
        from .colors import resolve_color

        color = kwargs.get('color', kwargs.get('facecolor', None))
        rgba = resolve_color(color, kwargs.get('alpha', 0.3))
        brush = pg.mkBrush(color=rgba)

        curve1 = pg.PlotDataItem(np.asarray(x, dtype=float),
                                 np.asarray(y1, dtype=float))
        y2_arr = np.asarray(y2, dtype=float)
        if y2_arr.ndim == 0:
            y2_arr = np.full(len(x), float(y2_arr))
        curve2 = pg.PlotDataItem(np.asarray(x, dtype=float), y2_arr)

        fill = pg.FillBetweenItem(curve1, curve2, brush=brush)
        self._plot_item.addItem(fill)
        return fill

    def hist(self, x: Any, bins: Optional[Any] = None,
             range: Optional[Any] = None,
             density: bool = False,
             weights: Optional[Any] = None,
             cumulative: bool = False,
             bottom: Optional[Any] = None,
             histtype: str = 'bar',
             align: str = 'mid',
             orientation: str = 'vertical',
             rwidth: Optional[float] = None,
             log: bool = False,
             color: Optional[str] = None,
             label: Optional[str] = None,
             stacked: bool = False,
             *,
             data: Optional[Any] = None,
             **kwargs: Any) -> Tuple[Any, Any, Any]:
        """Compute and plot a histogram."""
        x = np.asarray(x, dtype=float)

        if bins is None:
            bins = 10

        counts, edges = np.histogram(x, bins=bins, range=range,
                                     weights=weights, density=density)

        if cumulative:
            counts = np.cumsum(counts)

        width = edges[1] - edges[0]
        if rwidth is not None:
            width *= rwidth

        centers = (edges[:-1] + edges[1:]) / 2.0

        color = color or 'b'
        rgba = resolve_color(color, kwargs.get('alpha', None))

        edge_color = kwargs.get('edgecolor', kwargs.get('edgecolors', '#ffffff'))
        edge_rgba = resolve_color(edge_color)

        if orientation == 'horizontal':
            bar_item = pg.BarGraphItem(
                x0=np.zeros_like(counts),
                x1=counts,
                y=centers,
                height=width * 0.8,
                brush=pg.mkBrush(color=rgba),
                pen=pg.mkPen(color=edge_rgba, width=kwargs.get('linewidth', 0.5)),
            )
        else:
            bar_item = pg.BarGraphItem(
                x=centers,
                height=counts,
                width=width * 0.8,
                brush=pg.mkBrush(color=rgba),
                pen=pg.mkPen(color=edge_rgba, width=kwargs.get('linewidth', 0.5)),
            )

        self._plot_item.addItem(bar_item)
        if len(centers) > 0:
            x_pad = (edges[-1] - edges[0]) * 0.05
            y_max = counts.max() if len(counts) > 0 else 1
            y_pad = y_max * 0.05 or 0.5
            self._plot_item.setXRange(edges[0] - x_pad, edges[-1] + x_pad, padding=0)
            self._plot_item.setYRange(0 - y_pad, y_max + y_pad, padding=0)
        return counts, edges, bar_item

    def axhline(self, y: float = 0,
                xmin: float = 0, xmax: float = 1,
                **kwargs: Any) -> pg.InfiniteLine:
        """Add a horizontal line across the axes."""
        from pyqtgraph.Qt import QtCore
        color = kwargs.get('color', 'k')
        rgba = resolve_color(color)
        line = pg.InfiniteLine(
            pos=y,
            angle=0,
            pen=pg.mkPen(color=rgba,
                         width=kwargs.get('linewidth', 1.0),
                         style=normalize_linestyle(kwargs.get('linestyle', '-')))
        )
        self._plot_item.addItem(line)
        return line

    def axvline(self, x: float = 0,
                ymin: float = 0, ymax: float = 1,
                **kwargs: Any) -> pg.InfiniteLine:
        """Add a vertical line across the axes."""
        from pyqtgraph.Qt import QtCore
        color = kwargs.get('color', 'k')
        rgba = resolve_color(color)
        line = pg.InfiniteLine(
            pos=x,
            angle=90,
            pen=pg.mkPen(color=rgba,
                         width=kwargs.get('linewidth', 1.0),
                         style=normalize_linestyle(kwargs.get('linestyle', '-')))
        )
        self._plot_item.addItem(line)
        return line

    # ── Image ─────────────────────────────────────────────────────────

    def imshow(self, X: Any,
               cmap: Optional[Any] = None,
               norm: Optional[Any] = None,
               *,
               aspect: Optional[Any] = None,
               interpolation: Optional[str] = None,
               alpha: Optional[float] = None,
               vmin: Optional[float] = None,
               vmax: Optional[float] = None,
               origin: Optional[str] = None,
               extent: Optional[Any] = None,
               **kwargs: Any) -> pg.ImageItem:
        """Display data as an image."""
        X = np.asarray(X)
        img = pg.ImageItem(image=X.T if X.ndim == 2 else X)

        if vmin is not None and vmax is not None:
            img.setLevels([vmin, vmax])

        self._plot_item.addItem(img)

        if extent is not None:
            left, right, bottom, top = extent
            img.setRect(pg.QtCore.QRectF(left, bottom,
                                         right - left, top - bottom))
            self._plot_item.setXRange(left, right)
            self._plot_item.setYRange(bottom, top)
        else:
            self._plot_item.autoRange()

        return img

    # ── Text / Annotations ────────────────────────────────────────────

    def set_title(self, label: str,
                  fontdict: Optional[Dict[str, Any]] = None,
                  loc: Optional[str] = None,
                  pad: Optional[float] = None,
                  *,
                  y: Optional[float] = None,
                  **kwargs: Any) -> None:
        """Set the title of the axes."""
        self._plot_item.setTitle(label, **kwargs)

    def set_xlabel(self, xlabel: str,
                   fontdict: Optional[Dict[str, Any]] = None,
                   labelpad: Optional[float] = None,
                   *,
                   loc: Optional[str] = None,
                   **kwargs: Any) -> None:
        """Set the x-axis label."""
        self._plot_item.setLabel('bottom', xlabel, **kwargs)

    def set_ylabel(self, ylabel: str,
                   fontdict: Optional[Dict[str, Any]] = None,
                   labelpad: Optional[float] = None,
                   *,
                   loc: Optional[str] = None,
                   **kwargs: Any) -> None:
        """Set the y-axis label."""
        self._plot_item.setLabel('left', ylabel, **kwargs)

    def text(self, x: float, y: float, s: str,
             fontdict: Optional[Dict[str, Any]] = None,
             **kwargs: Any) -> pg.TextItem:
        """Add text to the axes."""
        color = kwargs.get('color', 'k')
        rgba = resolve_color(color)

        text_item = pg.TextItem(text=s, color=rgba)
        text_item.setPos(x, y)
        self._plot_item.addItem(text_item)
        return text_item

    def annotate(self, text: str, xy: Tuple[float, float],
                 xytext: Optional[Tuple[float, float]] = None,
                 xycoords: str = 'data',
                 textcoords: Optional[str] = None,
                 arrowprops: Optional[Dict[str, Any]] = None,
                 **kwargs: Any) -> pg.TextItem:
        """Annotate a point with text and optional arrow."""
        color = kwargs.get('color', 'k')
        rgba = resolve_color(color)

        if xytext is None:
            xytext = (xy[0] + 0.5, xy[1] + 0.5)

        text_item = pg.TextItem(text=text, color=rgba, anchor=(0, 0))
        text_item.setPos(*xytext)
        self._plot_item.addItem(text_item)

        if arrowprops is not None:
            arrow_color = arrowprops.get('color', 'k')
            arrow_rgba = resolve_color(arrow_color)

            arrow = pg.ArrowItem(
                pos=xytext,
                angle=self._compute_angle(xy, xytext),
                pen=pg.mkPen(color=arrow_rgba),
                brush=pg.mkBrush(color=arrow_rgba),
            )
            self._plot_item.addItem(arrow)

        return text_item

    @staticmethod
    def _compute_angle(p1: Tuple[float, float],
                       p2: Tuple[float, float]) -> float:
        """Compute angle from p1 to p2 in degrees."""
        import math
        return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

    # ── Scale / Limits ────────────────────────────────────────────────

    def set_xlim(self, left: Optional[float] = None,
                 right: Optional[float] = None,
                 *, emit: bool = True,
                 auto: Optional[bool] = None,
                 xmin: Optional[float] = None,
                 xmax: Optional[float] = None) -> None:
        """Set the x-axis view limits."""
        left = left if left is not None else xmin
        right = right if right is not None else xmax
        if left is not None and right is not None:
            self._plot_item.setXRange(left, right)
        elif left is not None:
            self._plot_item.setXRange(left, self._plot_item.viewRange()[0][1])
        elif right is not None:
            self._plot_item.setXRange(self._plot_item.viewRange()[0][0], right)

    def set_ylim(self, bottom: Optional[float] = None,
                 top: Optional[float] = None,
                 *, emit: bool = True,
                 auto: Optional[bool] = None,
                 ymin: Optional[float] = None,
                 ymax: Optional[float] = None) -> None:
        """Set the y-axis view limits."""
        bottom = bottom if bottom is not None else ymin
        top = top if top is not None else ymax
        if bottom is not None and top is not None:
            self._plot_item.setYRange(bottom, top)
        elif bottom is not None:
            self._plot_item.setYRange(bottom, self._plot_item.viewRange()[1][1])
        elif top is not None:
            self._plot_item.setYRange(self._plot_item.viewRange()[1][0], top)

    def get_xlim(self) -> Tuple[float, float]:
        """Get the x-axis view limits."""
        r = self._plot_item.viewRange()
        return (r[0][0], r[0][1])

    def get_ylim(self) -> Tuple[float, float]:
        """Get the y-axis view limits."""
        r = self._plot_item.viewRange()
        return (r[1][0], r[1][1])

    def set_xscale(self, value: str, **kwargs: Any) -> None:
        """Set the x-axis scale ('linear' or 'log')."""
        self._plot_item.setLogMode(x=(value == 'log'), y=None)

    def set_yscale(self, value: str, **kwargs: Any) -> None:
        """Set the y-axis scale ('linear' or 'log')."""
        self._plot_item.setLogMode(x=None, y=(value == 'log'))

    # ── Grid / Legend ─────────────────────────────────────────────────

    def grid(self, visible: Optional[bool] = None,
             which: str = 'major',
             axis: str = 'both',
             **kwargs: Any) -> None:
        """Show or hide grid lines."""
        if visible is None:
            visible = True

        show_x = axis in ('both', 'x')
        show_y = axis in ('both', 'y')

        alpha = kwargs.get('alpha', 0.15)
        self._plot_item.showGrid(x=show_x and visible,
                                 y=show_y and visible,
                                 alpha=alpha)

    def legend(self, *args: Any, **kwargs: Any) -> Optional[pg.LegendItem]:
        """Add a legend to the axes."""
        if self._legend is not None:
            self._plot_item.removeItem(self._legend)
            self._legend = None

        if not any(line._label for line in self._shenbi_lines if line._label):
            return None

        self._legend = self._plot_item.addLegend(**kwargs)
        self._update_legend()
        return self._legend

    def _update_legend(self) -> None:
        """Update legend items from current lines."""
        if self._legend is None:
            return
        self._legend.clear()
        for line in self._shenbi_lines:
            if line._label:
                self._legend.addItem(line.plot_data_item, line._label)
        for scatter in self._shenbi_scatters:
            if hasattr(scatter, '_label') and scatter._label:
                self._legend.addItem(scatter.scatter_item, scatter._label)

    # ── Ticks ─────────────────────────────────────────────────────────

    def set_xticks(self, ticks: Any = None,
                   labels: Optional[List[str]] = None, *,
                   minor: bool = False,
                   **kwargs: Any) -> None:
        """Set the x-axis ticks."""
        if ticks is not None and labels is not None:
            ticks = np.asarray(ticks, dtype=float)
            tick_vals = [(float(t), str(l)) for t, l in zip(ticks, labels)]
            axis = self._plot_item.getAxis('bottom')
            axis.setTicks([tick_vals])

    def set_yticks(self, ticks: Any = None,
                   labels: Optional[List[str]] = None, *,
                   minor: bool = False,
                   **kwargs: Any) -> None:
        """Set the y-axis ticks."""
        if ticks is not None and labels is not None:
            ticks = np.asarray(ticks, dtype=float)
            tick_vals = [(float(t), str(l)) for t, l in zip(ticks, labels)]
            axis = self._plot_item.getAxis('left')
            axis.setTicks([tick_vals])

    def set_xticklabels(self, labels: List[str], **kwargs) -> None:
        """Set the x-axis tick labels, keeping current tick positions."""
        try:
            axis = self._plot_item.getAxis('bottom')
            curr_ticks = axis.tickValues()
            if curr_ticks and len(curr_ticks) > 0:
                lengths = curr_ticks[0][1] if isinstance(curr_ticks[0], tuple) else []
                positions = [float(t) for t in lengths] if lengths else list(range(len(labels)))
            else:
                positions = list(range(len(labels)))
            tick_vals = [(float(p), str(l)) for p, l in zip(positions[:len(labels)], labels)]
            axis = self._plot_item.getAxis('bottom')
            axis.setTicks([tick_vals])
        except Exception:
            axis.setTicks([[(float(i), str(l)) for i, l in enumerate(labels)]])

    def set_yticklabels(self, labels: List[str], **kwargs) -> None:
        """Set the y-axis tick labels."""
        try:
            axis = self._plot_item.getAxis('left')
            curr_ticks = axis.tickValues()
            if curr_ticks and len(curr_ticks) > 0:
                lengths = curr_ticks[0][1] if isinstance(curr_ticks[0], tuple) else []
                positions = [float(t) for t in lengths] if lengths else list(range(len(labels)))
            else:
                positions = list(range(len(labels)))
            tick_vals = [(float(p), str(l)) for p, l in zip(positions[:len(labels)], labels)]
            axis.setTicks([tick_vals])
        except Exception:
            axis.setTicks([[(float(i), str(l)) for i, l in enumerate(labels)]])

    # ── Other Methods ─────────────────────────────────────────────────

    def step(self, x: Any, y: Any, *args: Any,
             where: str = 'pre',
             data: Optional[Any] = None,
             **kwargs: Any) -> List[ShenBiLine2D]:
        """Make a step plot. Delegates to plot with drawstyle='steps-{where}'."""
        kwargs['drawstyle'] = f'steps-{where}'
        return self.plot(x, y, *args, data=data, **kwargs)

    def stem(self, *args: Any,
             linefmt: Optional[str] = None,
             markerfmt: Optional[str] = None,
             basefmt: Optional[str] = None,
             bottom: float = 0,
             label: Optional[str] = None,
             orientation: str = 'vertical',
             data: Optional[Any] = None) -> Any:
        """Create a stem plot."""
        from .colors import resolve_color
        from .utils import parse_format_string

        if len(args) == 1:
            locs = np.arange(len(np.asarray(args[0])))
            heads = np.asarray(args[0], dtype=float)
        elif len(args) >= 2:
            locs = np.asarray(args[0], dtype=float)
            heads = np.asarray(args[1], dtype=float)

        markerline = self.plot(locs, heads, markerfmt or 'o', label=label,
                               linestyle='')[0]

        baseline = np.full_like(locs, bottom)
        base_color, _, base_ls = parse_format_string(basefmt or 'C3-')
        if not base_ls:
            base_ls = '-'

        baseline = self.plot([locs[0], locs[-1]], [bottom, bottom],
                             linestyle=base_ls,
                             color=base_color or 'C3')[0]

        stem_color, _, stem_ls = parse_format_string(linefmt or 'C0-')
        if not stem_ls:
            stem_ls = '-'
        stem_lines = []
        for lx, hy in zip(locs, heads):
            line = self.plot([lx, lx], [bottom, hy],
                             linestyle=stem_ls,
                             color=stem_color or 'C0')[0]
            stem_lines.append(line)

        return markerline, stem_lines, baseline

    def pie(self, x: Any, *,
            explode: Optional[Any] = None,
            labels: Optional[Any] = None,
            colors: Optional[Any] = None,
            wedge_labels: Optional[Any] = None,
            wedge_label_distance: float = 0.6,
            autopct: Optional[Any] = None,
            pctdistance: float = 0.6,
            shadow: bool = False,
            labeldistance: Optional[float] = None,
            startangle: float = 0,
            radius: float = 1,
            counterclock: bool = True,
            wedgeprops: Optional[dict] = None,
            textprops: Optional[dict] = None,
            center: Tuple[float, float] = (0, 0),
            frame: bool = False,
            rotatelabels: bool = False,
            normalize: bool = True,
            hatch: Optional[Any] = None,
            data: Optional[Any] = None) -> Any:
        """Plot a pie chart using filled wedge curves."""
        x = np.asarray(x, dtype=float)
        total = x.sum()
        if total == 0:
            return []
        if normalize:
            fracs = x / total
        else:
            fracs = x

        cx, cy = center
        colors = colors or [None] * len(x)
        if isinstance(colors, str):
            colors = [colors] * len(x)

        start_angle = startangle
        wedges = []

        for i, frac in enumerate(fracs):
            sweep = frac * 360.0
            c = resolve_color(colors[i % len(colors)] if isinstance(colors, list) else colors)

            n_arc = max(int(sweep), 30)
            angles_rad = np.deg2rad(np.linspace(start_angle, start_angle + sweep, n_arc))
            xp = np.concatenate([[cx], cx + radius * np.cos(angles_rad), [cx]])
            yp = np.concatenate([[cy], cy + radius * np.sin(angles_rad), [cy]])

            curve = pg.PlotCurveItem(
                xp, yp,
                fillLevel=0,
                brush=pg.mkBrush(color=c),
                pen=pg.mkPen(color=(255, 255, 255, 255), width=1.5),
            )
            self._plot_item.addItem(curve)
            wedges.append(curve)

            if labels is not None and i < len(labels):
                label_angle = np.deg2rad(start_angle + sweep / 2)
                label_r = radius * 1.3
                lx = cx + label_r * np.cos(label_angle)
                ly = cy + label_r * np.sin(label_angle)
                text = pg.TextItem(text=str(labels[i]), color='#333333', anchor=(0.5, 0.5))
                text.setPos(lx, ly)
                self._plot_item.addItem(text)

            start_angle += sweep

        self._plot_item.setXRange(cx - radius * 1.5, cx + radius * 1.5, padding=0)
        self._plot_item.setYRange(cy - radius * 1.5, cy + radius * 1.5, padding=0)
        self._plot_item.setAspectLocked(lock=True, ratio=1.0)
        self._plot_item.hideButtons()

        return wedges

    def twinx(self) -> 'ShenBiAxes':
        """Create a twin Axes sharing the x-axis."""
        plot_item = pg.PlotItem()
        plot_item.setXLink(self._plot_item)
        ax = ShenBiAxes(plot_item)
        self._plot_item.scene().addItem(plot_item)
        return ax

    def twiny(self) -> 'ShenBiAxes':
        """Create a twin Axes sharing the y-axis."""
        plot_item = pg.PlotItem()
        plot_item.setYLink(self._plot_item)
        ax = ShenBiAxes(plot_item)
        self._plot_item.scene().addItem(plot_item)
        return ax

    def semilogx(self, *args: Any, base: float = 10,
                 subs: Optional[Any] = None,
                 nonpositive: str = 'clip',
                 **kwargs: Any) -> List[ShenBiLine2D]:
        """Plot with log scale on x-axis."""
        self.set_xscale('log')
        return self.plot(*args, **kwargs)

    def semilogy(self, *args: Any, base: float = 10,
                 subs: Optional[Any] = None,
                 nonpositive: str = 'clip',
                 **kwargs: Any) -> List[ShenBiLine2D]:
        """Plot with log scale on y-axis."""
        self.set_yscale('log')
        return self.plot(*args, **kwargs)

    def loglog(self, *args: Any, basex: float = 10, basey: float = 10,
               subsx: Optional[Any] = None, subsy: Optional[Any] = None,
               nonposx: str = 'clip', nonposy: str = 'clip',
               **kwargs: Any) -> List[ShenBiLine2D]:
        """Plot with log scale on both axes."""
        self.set_xscale('log')
        self.set_yscale('log')
        return self.plot(*args, **kwargs)

    def boxplot(self, x: Any,
                notch: Optional[bool] = None,
                sym: Optional[str] = None,
                vert: Optional[bool] = None,
                orientation: str = 'vertical',
                whis: float = 1.5,
                positions: Optional[Any] = None,
                widths: Optional[Any] = None,
                patch_artist: Optional[bool] = None,
                bootstrap: Optional[int] = None,
                usermedians: Optional[Any] = None,
                conf_intervals: Optional[Any] = None,
                meanline: Optional[bool] = None,
                showmeans: Optional[bool] = None,
                showcaps: Optional[bool] = None,
                showbox: Optional[bool] = None,
                showfliers: Optional[bool] = None,
                boxprops: Optional[dict] = None,
                tick_labels: Optional[Any] = None,
                flierprops: Optional[dict] = None,
                medianprops: Optional[dict] = None,
                meanprops: Optional[dict] = None,
                capprops: Optional[dict] = None,
                whiskerprops: Optional[dict] = None,
                manage_ticks: bool = True,
                autorange: bool = False,
                zorder: Optional[float] = None,
                capwidths: Optional[Any] = None,
                label: Optional[Any] = None,
                *,
                data: Optional[Any] = None) -> dict:
        """Draw a box and whisker plot."""
        datasets = []
        x_arr = np.asarray(x)
        if x_arr.ndim == 1:
            datasets = [x_arr]
        elif x_arr.ndim == 2:
            datasets = [x_arr[:, i] for i in range(x_arr.shape[1])]
        else:
            datasets = [np.asarray(d) for d in x]

        if positions is None:
            positions = list(range(1, len(datasets) + 1))
        if widths is None:
            widths = 0.5

        box_color = boxprops.get('color', '#1f77b4') if boxprops else '#1f77b4'
        box_rgba = resolve_color(box_color)
        median_color = medianprops.get('color', '#d62728') if medianprops else '#d62728'

        result: dict = {'boxes': [], 'medians': [], 'whiskers': [],
                        'caps': [], 'fliers': [], 'means': []}

        from pyqtgraph.Qt import QtGui

        y_min_all = float('inf')
        y_max_all = float('-inf')

        for i, d in enumerate(datasets):
            d = d[~np.isnan(d)]
            if len(d) == 0:
                continue
            q1, med, q3 = np.percentile(d, [25, 50, 75])
            iqr = q3 - q1
            wlo = q1 - whis * iqr
            whi = q3 + whis * iqr
            flo = d[d < wlo]
            fhi = d[d > whi]
            wlo = max(d.min(), wlo)
            whi = min(d.max(), whi)

            pos = float(positions[i] if i < len(positions) else i + 1)
            w = float(widths if isinstance(widths, (int, float)) else widths[i] if i < len(widths) else 0.5)
            hw = w / 2.0

            y_min_all = min(y_min_all, d.min())
            y_max_all = max(y_max_all, d.max())

            box_item = pg.QtWidgets.QGraphicsRectItem(pos - hw, q1, w, q3 - q1)
            box_item.setPen(pg.mkPen(color='#333333', width=1))
            box_item.setBrush(pg.mkBrush(color=box_rgba))
            self._plot_item.addItem(box_item)
            result['boxes'].append(box_item)

            med_line = self.plot([pos - hw, pos + hw], [med, med],
                                color=median_color, linewidth=2)[0]
            result['medians'].append(med_line)

            whisk_lo = self.plot([pos, pos], [wlo, q1],
                                color='#333333', linewidth=1, linestyle='-')[0]
            whisk_hi = self.plot([pos, pos], [q3, whi],
                                color='#333333', linewidth=1, linestyle='-')[0]
            result['whiskers'].extend([whisk_lo, whisk_hi])

            cap_w = hw * 0.5
            cap_lo = self.plot([pos - cap_w, pos + cap_w], [wlo, wlo],
                               color='#333333', linewidth=1)[0]
            cap_hi = self.plot([pos - cap_w, pos + cap_w], [whi, whi],
                               color='#333333', linewidth=1)[0]
            result['caps'].extend([cap_lo, cap_hi])

            fliers = np.concatenate([flo, fhi])
            if len(fliers) > 0:
                scatter = ShenBiScatter(
                    np.full(len(fliers), pos), fliers,
                    marker='+', s=15, c='#333333',
                )
                self._plot_item.addItem(scatter.scatter_item)
                self._shenbi_scatters.append(scatter)
                result['fliers'].append(scatter)

        if tick_labels is not None:
            self.set_xticks(list(positions[:len(datasets)]), list(tick_labels[:len(datasets)]))

        pad = (y_max_all - y_min_all) * 0.05 or 1.0
        self._plot_item.setXRange(positions[0] - 0.8, positions[-1] + 0.8, padding=0)
        self._plot_item.setYRange(y_min_all - pad, y_max_all + pad, padding=0)

        return result

    # ── Clear / Other ─────────────────────────────────────────────────

    def cla(self) -> None:
        """Clear the axes."""
        self._plot_item.clear()
        self._shenbi_lines.clear()
        self._shenbi_scatters.clear()
        self._legend = None

    def autoscale(self, enable: bool = True, axis: str = 'both',
                  tight: Optional[bool] = None) -> None:
        """Auto-scale the axis."""
        if axis in ('both', 'x'):
            self._plot_item.enableAutoRange(axis='x' if enable else None)
        if axis in ('both', 'y'):
            self._plot_item.enableAutoRange(axis='y' if enable else None)

    def set_aspect(self, aspect: Any = None,
                   adjustable: Optional[Any] = None,
                   anchor: Optional[Any] = None,
                   share: bool = False) -> None:
        """Set the aspect ratio of the axes scaling."""
        if aspect == 'equal':
            self._plot_item.setAspectLocked(lock=True, ratio=1.0)
        elif aspect == 'auto' or aspect is None:
            self._plot_item.setAspectLocked(lock=False)
        elif isinstance(aspect, (int, float)):
            self._plot_item.setAspectLocked(lock=True, ratio=float(aspect))
        else:
            self._plot_item.setAspectLocked(lock=False)

    @property
    def plot_item(self) -> pg.PlotItem:
        """Get the underlying pyqtgraph PlotItem."""
        return self._plot_item


class _DummyErrorBar:
    """Dummy error bar item when none is provided."""
    visible = False

    def setData(self, *args, **kwargs):
        pass


def title(label: str, fontdict=None, loc=None, pad=None, *, y=None,
          **kwargs):
    """Set the title of the current axes."""
    from .pyplot import gca
    gca().set_title(label, fontdict=fontdict, loc=loc, pad=pad, y=y, **kwargs)


def xlabel(xlabel: str, fontdict=None, labelpad=None, *, loc=None,
           **kwargs):
    """Set the x-axis label of the current axes."""
    from .pyplot import gca
    gca().set_xlabel(xlabel, fontdict=fontdict, labelpad=labelpad,
                     loc=loc, **kwargs)


def ylabel(ylabel: str, fontdict=None, labelpad=None, *, loc=None,
           **kwargs):
    """Set the y-axis label of the current axes."""
    from .pyplot import gca
    gca().set_ylabel(ylabel, fontdict=fontdict, labelpad=labelpad,
                     loc=loc, **kwargs)


def xlim(*args, **kwargs):
    """Get or set the x limits of the current axes."""
    from .pyplot import gca
    ax = gca()
    if not args and not kwargs:
        return ax.get_xlim()
    left = args[0] if len(args) > 0 else None
    right = args[1] if len(args) > 1 else None
    ax.set_xlim(left, right, **kwargs)


def ylim(*args, **kwargs):
    """Get or set the y limits of the current axes."""
    from .pyplot import gca
    ax = gca()
    if not args and not kwargs:
        return ax.get_ylim()
    bottom = args[0] if len(args) > 0 else None
    top = args[1] if len(args) > 1 else None
    ax.set_ylim(bottom, top, **kwargs)


def grid(visible=None, which='major', axis='both', **kwargs):
    """Show or hide grid lines on the current axes."""
    from .pyplot import gca
    gca().grid(visible=visible, which=which, axis=axis, **kwargs)


def legend(*args, **kwargs):
    """Add a legend to the current axes."""
    from .pyplot import gca
    return gca().legend(*args, **kwargs)
