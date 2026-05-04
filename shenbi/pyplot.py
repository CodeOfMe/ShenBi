"""
ShenBi pyplot: matplotlib.pyplot-compatible state-based plotting API.

Provides the same functional interface as matplotlib.pyplot, but powered
by pyqtgraph's high-performance rendering engine. Users can write:

    import shenbi.pyplot as plt
    plt.plot(x, y, 'r-', linewidth=2)
    plt.title('My Plot')
    plt.show()

And get matplotlib-compatible syntax with pyqtgraph-level performance.
"""
from __future__ import annotations

import sys
from typing import Any, List, Optional, Tuple, Union

import numpy as np

from .colors import _reset_color_cycle, resolve_color
from .cm import cm, get_cmap, Colormap
from .figure import ShenBiFigure
from .line import ShenBiLine2D, ShenBiScatter
from .utils import MARKER_MAP, parse_format_string, process_plot_args

# ── Global State ──────────────────────────────────────────────────────

_current_figure: Optional[ShenBiFigure] = None
_current_axes: Optional[ShenBiAxes] = None
_interactive: bool = False
_ION: bool = False


# ── Figure Management ─────────────────────────────────────────────────

def figure(
    num: Optional[Union[int, str]] = None,
    figsize: Optional[Tuple[float, float]] = None,
    dpi: float = 100,
    *,
    facecolor: Optional[str] = None,
    edgecolor: Optional[str] = None,
    frameon: bool = True,
    FigureClass=ShenBiFigure,
    clear: bool = False,
    **kwargs: Any,
) -> ShenBiFigure:
    """
    Create a new figure, or activate an existing figure.

    Parameters
    ----------
    num : int or str, optional
        Figure identifier.
    figsize : (float, float), optional
        Width, height in inches.
    dpi : float, optional
        Dots per inch.
    facecolor : str, optional
        Background color.
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    ShenBiFigure
    """
    global _current_figure, _current_axes

    if num is not None:
        existing = ShenBiFigure.get_figure(num)
        if existing is not None:
            _current_figure = existing
            _current_axes = existing.gca
            return existing

    fig = FigureClass(
        num=num, figsize=figsize, dpi=dpi,
        facecolor=facecolor, edgecolor=edgecolor,
        frameon=frameon, clear=clear, **kwargs,
    )
    _current_figure = fig
    _current_axes = None
    _reset_color_cycle()
    return fig


def subplots(
    nrows: int = 1,
    ncols: int = 1,
    *,
    sharex: bool = False,
    sharey: bool = False,
    squeeze: bool = True,
    width_ratios: Optional[List[float]] = None,
    height_ratios: Optional[List[float]] = None,
    subplot_kw: Optional[dict] = None,
    gridspec_kw: Optional[dict] = None,
    **fig_kw: Any,
) -> Tuple[ShenBiFigure, Any]:
    """
    Create a figure and a set of subplots.

    Returns
    -------
    fig : ShenBiFigure
    ax : ShenBiAxes or array of ShenBiAxes
    """
    global _current_figure, _current_axes

    fig = figure(**fig_kw)
    fig, axes = fig.subplots(
        nrows=nrows, ncols=ncols,
        sharex=sharex, sharey=sharey,
        squeeze=squeeze,
        width_ratios=width_ratios,
        height_ratios=height_ratios,
        subplot_kw=subplot_kw,
        gridspec_kw=gridspec_kw,
    )
    _current_figure = fig

    if isinstance(axes, (list, np.ndarray)):
        flat = np.asarray(axes).flatten()
        _current_axes = flat[0] if len(flat) > 0 else None
    else:
        _current_axes = axes

    return fig, axes


def subplot(*args: Any, **kwargs: Any) -> 'ShenBiAxes':
    """
    Add a subplot to the current figure.

    Parameters
    ----------
    *args : int or tuple
        Either a 3-digit number (e.g., 211) or (nrows, ncols, index).
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    ShenBiAxes
    """
    global _current_figure, _current_axes

    if _current_figure is None:
        _current_figure = figure()

    ax = _current_figure.add_subplot(*args, **kwargs)
    _current_axes = ax
    return ax


def subplots_adjust(
    left: Optional[float] = None,
    bottom: Optional[float] = None,
    right: Optional[float] = None,
    top: Optional[float] = None,
    wspace: Optional[float] = None,
    hspace: Optional[float] = None,
) -> None:
    """Adjust subplot layout parameters (stub for compatibility)."""
    pass


def gcf() -> ShenBiFigure:
    """Get the current figure."""
    global _current_figure
    if _current_figure is None:
        _current_figure = figure()
    return _current_figure


def gca() -> 'ShenBiAxes':
    """Get the current axes."""
    global _current_figure, _current_axes
    if _current_figure is None:
        _current_figure = figure()
    if _current_axes is None:
        _current_axes = _current_figure.add_subplot(1, 1, 1)
    return _current_axes


def scf(fig: ShenBiFigure) -> None:
    """Set the current figure."""
    global _current_figure
    _current_figure = fig


def sca(ax: 'ShenBiAxes') -> None:
    """Set the current axes."""
    global _current_axes
    _current_axes = ax


def clf() -> None:
    """Clear the current figure."""
    fig = gcf()
    fig.clf()


def cla() -> None:
    """Clear the current axes."""
    ax = gca()
    ax.cla()


def close(fig: Optional[Any] = None) -> None:
    """Close a figure window. Pass 'all' to close all figures."""
    global _current_figure, _current_axes

    if fig == 'all' or (isinstance(fig, str) and fig.lower() == 'all'):
        for f in list(ShenBiFigure.get_all_figures()):
            f.close()
        _current_figure = None
        _current_axes = None
        return

    if fig is None:
        fig = _current_figure

    if fig is not None and hasattr(fig, 'close'):
        fig.close()
        if _current_figure is fig:
            remaining = ShenBiFigure.get_all_figures()
            _current_figure = remaining[-1] if remaining else None
            _current_axes = _current_figure.gca if _current_figure else None


# ── Plotting Functions ────────────────────────────────────────────────

def plot(*args: Any, scalex: bool = True, scaley: bool = True,
         data: Optional[Any] = None, **kwargs: Any) -> List[ShenBiLine2D]:
    """
    Plot y versus x as lines and/or markers.

    Call signatures:
        plot(y)               # y values, x auto-index
        plot(x, y)            # x, y values
        plot(x, y, 'r--')     # with format string
        plot(x1, y1, 'g-', x2, y2, 'b:')  # multiple

    Parameters
    ----------
    *args : array-like or str
        x, y values and optional format string
    scalex, scaley : bool
        Whether to auto-scale x/y axes
    data : dict-like, optional
        Indexable data source
    **kwargs : dict
        Line2D properties

    Returns
    -------
    list of ShenBiLine2D
    """
    return gca().plot(*args, scalex=scalex, scaley=scaley,
                      data=data, **kwargs)


def scatter(x: Any, y: Any,
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
    """A scatter plot of y vs x with varying marker size and/or color."""
    return gca().scatter(
        x, y, s=s, c=c, marker=marker,
        cmap=cmap, norm=norm, vmin=vmin, vmax=vmax,
        alpha=alpha, linewidths=linewidths,
        edgecolors=edgecolors, colorizer=colorizer,
        plotnonfinite=plotnonfinite, data=data, **kwargs,
    )


def bar(x: Any, height: Any, width: float = 0.8,
        bottom: Optional[Any] = None, *,
        align: str = 'center', data: Optional[Any] = None,
        **kwargs: Any) -> Any:
    """Make a bar plot."""
    return gca().bar(x, height, width=width, bottom=bottom,
                     align=align, data=data, **kwargs)


def barh(y: Any, width: Any, height: float = 0.8,
         left: Optional[Any] = None, *,
         align: str = 'center', **kwargs: Any) -> Any:
    """Make a horizontal bar plot."""
    return gca().barh(y, width, height=height, left=left,
                      align=align, **kwargs)


def errorbar(x: Any, y: Any,
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
             **kwargs: Any) -> Any:
    """Plot y versus x with error bars."""
    return gca().errorbar(
        x, y, yerr=yerr, xerr=xerr, fmt=fmt,
        ecolor=ecolor, elinewidth=elinewidth,
        capsize=capsize, barsabove=barsabove,
        lolims=lolims, uplims=uplims,
        xlolims=xlolims, xuplims=xuplims,
        errorevery=errorevery, capthick=capthick,
        data=data, **kwargs,
    )


def fill_between(x: Any, y1: Any, y2: Any = 0,
                 where: Optional[Any] = None,
                 interpolate: bool = False,
                 step: Optional[str] = None,
                 *,
                 data: Optional[Any] = None,
                 **kwargs: Any) -> Any:
    """Fill the area between two horizontal curves."""
    return gca().fill_between(
        x, y1, y2, where=where, interpolate=interpolate,
        step=step, data=data, **kwargs,
    )


def hist(x: Any, bins: Optional[Any] = None,
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
         **kwargs: Any) -> Any:
    """Compute and plot a histogram."""
    return gca().hist(
        x, bins=bins, range=range, density=density,
        weights=weights, cumulative=cumulative,
        bottom=bottom, histtype=histtype,
        align=align, orientation=orientation,
        rwidth=rwidth, log=log, color=color,
        label=label, stacked=stacked,
        data=data, **kwargs,
    )


def contour(X: Any, Y: Any, Z: Any,
            levels: Optional[Any] = None,
            colors: Optional[Any] = None,
            linewidths: Optional[float] = None,
            linestyles: Optional[str] = None,
            alpha: Optional[float] = None,
            **kwargs: Any) -> Any:
    """Draw contour lines."""
    return gca().contour(X, Y, Z, levels=levels, colors=colors,
                         linewidths=linewidths, linestyles=linestyles,
                         alpha=alpha, **kwargs)


def contourf(X: Any, Y: Any, Z: Any,
             levels: Optional[Any] = None,
             cmap: Optional[Any] = None,
             alpha: Optional[float] = None,
             **kwargs: Any) -> Any:
    """Draw filled contours."""
    return gca().contourf(X, Y, Z, levels=levels, cmap=cmap,
                          alpha=alpha, **kwargs)


def colorbar(mappable: Optional[Any] = None,
             cax: Optional[Any] = None,
             ax: Optional[Any] = None,
             **kwargs: Any) -> Any:
    """Add a colorbar to the current axes."""
    from pyqtgraph import ColorBarItem
    if mappable is not None and hasattr(mappable, 'levels'):
        cbar = ColorBarItem(values=(mappable.vmin, mappable.vmax),
                           cmap=mappable.cmap if hasattr(mappable, 'cmap') else 'viridis')
        return cbar
    return None


def fill(x: Any, y: Any,
         color: Optional[str] = None,
         alpha: Optional[float] = None,
         edgecolor: Optional[str] = None,
         linewidth: Optional[float] = None,
         **kwargs: Any) -> Any:
    """Fill a polygon."""
    return gca().fill(x, y, color=color, alpha=alpha,
                      edgecolor=edgecolor, linewidth=linewidth, **kwargs)


class Polygon:
    """matplotlib-compatible Polygon patch."""
    def __init__(self, xy, facecolor=None, edgecolor=None,
                 linewidth=None, alpha=None, **kwargs):
        self._xy = np.asarray(xy)
        self._facecolor = facecolor
        self._edgecolor = edgecolor
        self._linewidth = linewidth
        self._alpha = alpha

    def get_xy(self):
        return self._xy

    def get_facecolor(self):
        if self._facecolor is None:
            return (0.0, 0.0, 1.0, 0.8)
        if isinstance(self._facecolor, str):
            from .colors import resolve_color
            c = resolve_color(self._facecolor, self._alpha or 0.8)
            return (c[0]/255, c[1]/255, c[2]/255, c[3]/255)
        return self._facecolor

    def get_edgecolor(self):
        if self._edgecolor is None:
            return None
        if isinstance(self._edgecolor, str):
            from .colors import resolve_color
            c = resolve_color(self._edgecolor, 1.0)
            return (c[0]/255, c[1]/255, c[2]/255, 1.0)
        return self._edgecolor

    def get_linewidth(self):
        return self._linewidth


def imshow(X: Any,
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
           **kwargs: Any) -> Any:
    """Display data as an image."""
    return gca().imshow(
        X, cmap=cmap, norm=norm, aspect=aspect,
        interpolation=interpolation, alpha=alpha,
        vmin=vmin, vmax=vmax, origin=origin,
        extent=extent, **kwargs,
    )


# ── Axes Decoration ───────────────────────────────────────────────────

def title(label: str, fontdict=None, loc=None, pad=None, *,
          y=None, **kwargs) -> None:
    """Set the title of the current axes."""
    gca().set_title(label, fontdict=fontdict, loc=loc,
                    pad=pad, y=y, **kwargs)


def xlabel(xlabel: str, fontdict=None, labelpad=None, *,
           loc=None, **kwargs) -> None:
    """Set the x-axis label of the current axes."""
    gca().set_xlabel(xlabel, fontdict=fontdict, labelpad=labelpad,
                     loc=loc, **kwargs)


def ylabel(ylabel: str, fontdict=None, labelpad=None, *,
           loc=None, **kwargs) -> None:
    """Set the y-axis label of the current axes."""
    gca().set_ylabel(ylabel, fontdict=fontdict, labelpad=labelpad,
                     loc=loc, **kwargs)


def xlim(*args: Any, **kwargs: Any) -> Union[Tuple[float, float], None]:
    """Get or set the x limits of the current axes."""
    ax = gca()
    if not args and not kwargs:
        return ax.get_xlim()
    left = args[0] if len(args) > 0 else None
    right = args[1] if len(args) > 1 else None
    ax.set_xlim(left, right, **kwargs)
    return None


def ylim(*args: Any, **kwargs: Any) -> Union[Tuple[float, float], None]:
    """Get or set the y limits of the current axes."""
    ax = gca()
    if not args and not kwargs:
        return ax.get_ylim()
    bottom = args[0] if len(args) > 0 else None
    top = args[1] if len(args) > 1 else None
    ax.set_ylim(bottom, top, **kwargs)
    return None


def xscale(value: str, **kwargs: Any) -> None:
    """Set the x-axis scale."""
    gca().set_xscale(value, **kwargs)


def yscale(value: str, **kwargs: Any) -> None:
    """Set the y-axis scale."""
    gca().set_yscale(value, **kwargs)


def grid(visible: Optional[bool] = None,
         which: str = 'major',
         axis: str = 'both',
         **kwargs: Any) -> None:
    """Show or hide grid lines on the current axes."""
    gca().grid(visible=visible, which=which, axis=axis, **kwargs)


def legend(*args: Any, **kwargs: Any) -> Any:
    """Add a legend to the current axes."""
    return gca().legend(*args, **kwargs)


def xticks(ticks=None, labels=None, *, minor=False, **kwargs) -> Any:
    """Get or set the x-axis tick locations and labels."""
    ax = gca()
    if ticks is None and labels is None:
        return ([], [])
    ax.set_xticks(ticks, labels, minor=minor, **kwargs)


def yticks(ticks=None, labels=None, *, minor=False, **kwargs) -> Any:
    """Get or set the y-axis tick locations and labels."""
    ax = gca()
    if ticks is None and labels is None:
        return ([], [])
    ax.set_yticks(ticks, labels, minor=minor, **kwargs)


def axhline(y: float = 0, xmin: float = 0, xmax: float = 1,
            **kwargs: Any) -> Any:
    """Add a horizontal line across the axes."""
    return gca().axhline(y, xmin=xmin, xmax=xmax, **kwargs)


def axvline(x: float = 0, ymin: float = 0, ymax: float = 1,
            **kwargs: Any) -> Any:
    """Add a vertical line across the axes."""
    return gca().axvline(x, ymin=ymin, ymax=ymax, **kwargs)


def text(x: float, y: float, s: str,
         fontdict=None, **kwargs: Any) -> Any:
    """Add text to the axes."""
    return gca().text(x, y, s, fontdict=fontdict, **kwargs)


def annotate(text: str, xy: Tuple[float, float],
             xytext: Optional[Tuple[float, float]] = None,
             xycoords: str = 'data',
             textcoords: Optional[str] = None,
             arrowprops: Optional[dict] = None,
             **kwargs: Any) -> Any:
    """Annotate a point with text and optional arrow."""
    return gca().annotate(text, xy, xytext=xytext, xycoords=xycoords,
                          textcoords=textcoords, arrowprops=arrowprops, **kwargs)


def step(x: Any, y: Any, *args: Any, where: str = 'pre',
         data: Optional[Any] = None, **kwargs: Any) -> Any:
    """Make a step plot."""
    return gca().step(x, y, *args, where=where, data=data, **kwargs)


def stem(*args: Any, linefmt: Optional[str] = None,
         markerfmt: Optional[str] = None, basefmt: Optional[str] = None,
         bottom: float = 0, label: Optional[str] = None,
         orientation: str = 'vertical',
         data: Optional[Any] = None) -> Any:
    """Create a stem plot."""
    return gca().stem(*args, linefmt=linefmt, markerfmt=markerfmt,
                      basefmt=basefmt, bottom=bottom, label=label,
                      orientation=orientation, data=data)


def pie(x: Any, *,
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
    """Plot a pie chart."""
    return gca().pie(x, explode=explode, labels=labels, colors=colors,
                     wedge_labels=wedge_labels,
                     wedge_label_distance=wedge_label_distance,
                     autopct=autopct, pctdistance=pctdistance,
                     shadow=shadow, labeldistance=labeldistance,
                     startangle=startangle, radius=radius,
                     counterclock=counterclock, wedgeprops=wedgeprops,
                     textprops=textprops, center=center, frame=frame,
                     rotatelabels=rotatelabels, normalize=normalize,
                     hatch=hatch, data=data)


def twinx(ax: Optional[Any] = None) -> Any:
    """Create a twin Axes sharing the x-axis."""
    if ax is None:
        ax = gca()
    return ax.twinx()


def twiny(ax: Optional[Any] = None) -> Any:
    """Create a twin Axes sharing the y-axis."""
    if ax is None:
        ax = gca()
    return ax.twiny()


def semilogx(*args: Any, base: float = 10, subs: Optional[Any] = None,
             nonpositive: str = 'clip', **kwargs: Any) -> Any:
    """Plot with log scale on x-axis."""
    return gca().semilogx(*args, base=base, subs=subs,
                          nonpositive=nonpositive, **kwargs)


def semilogy(*args: Any, base: float = 10, subs: Optional[Any] = None,
             nonpositive: str = 'clip', **kwargs: Any) -> Any:
    """Plot with log scale on y-axis."""
    return gca().semilogy(*args, base=base, subs=subs,
                          nonpositive=nonpositive, **kwargs)


def loglog(*args: Any, basex: float = 10, basey: float = 10,
           subsx: Optional[Any] = None, subsy: Optional[Any] = None,
           nonposx: str = 'clip', nonposy: str = 'clip',
           **kwargs: Any) -> Any:
    """Plot with log scale on both axes."""
    return gca().loglog(*args, basex=basex, basey=basey,
                        subsx=subsx, subsy=subsy,
                        nonposx=nonposx, nonposy=nonposy, **kwargs)


def boxplot(x: Any,
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
    return gca().boxplot(
        x, notch=notch, sym=sym, vert=vert, orientation=orientation,
        whis=whis, positions=positions, widths=widths,
        patch_artist=patch_artist, bootstrap=bootstrap,
        usermedians=usermedians, conf_intervals=conf_intervals,
        meanline=meanline, showmeans=showmeans, showcaps=showcaps,
        showbox=showbox, showfliers=showfliers, boxprops=boxprops,
        tick_labels=tick_labels, flierprops=flierprops,
        medianprops=medianprops, meanprops=meanprops,
        capprops=capprops, whiskerprops=whiskerprops,
        manage_ticks=manage_ticks, autorange=autorange,
        zorder=zorder, capwidths=capwidths, label=label, data=data)


def colorbar(mappable: Optional[Any] = None,
             cax: Optional[Any] = None,
             ax: Optional[Any] = None,
             **kwargs: Any) -> Any:
    """Add a colorbar to a plot."""
    from pyqtgraph import HistogramLUTItem
    if mappable is not None and hasattr(mappable, 'getLevels'):
        cbar = HistogramLUTItem(image=mappable)
        return cbar
    return None


def margins(*margins: Any, x: Optional[float] = None,
            y: Optional[float] = None,
            tight: Optional[bool] = True) -> None:
    """Set or retrieve autoscaling margins (stub)."""
    pass


def tick_params(axis: str = 'both', **kwargs: Any) -> None:
    """Change the appearance of ticks, tick labels, and gridlines (stub)."""
    pass


# ── Style / rcParams ──────────────────────────────────────────────────

class _RcParams(dict):
    def __getattr__(self, key):
        return self.get(key, None)
    def __setattr__(self, key, value):
        self[key] = value

rcParams = _RcParams({'figure.figsize': (6.4, 4.8),
                       'figure.dpi': 100,
                       'lines.linewidth': 1.5,
                       'lines.color': 'b',
                       'font.size': 10})


def style_use(style_name: str) -> None:
    """Use a matplotlib style (stub)."""
    pass


# ── Display / Output ──────────────────────────────────────────────────

def show(*, block: Optional[bool] = None) -> None:
    """
    Display all open figures.

    Starts the Qt event loop. This must be called to display the figures.

    Parameters
    ----------
    block : bool, optional
        Whether to block the interpreter (default: True).
    """
    from pyqtgraph.Qt import QtWidgets

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    for fig in ShenBiFigure.get_all_figures():
        fig.show()

    if block is not False:
        sys.exit(app.exec())


def savefig(
    fname: str,
    *,
    dpi: Optional[float] = None,
    facecolor: Optional[str] = None,
    edgecolor: Optional[str] = None,
    orientation: str = 'portrait',
    format: Optional[str] = None,
    transparent: bool = False,
    bbox_inches: Optional[str] = None,
    pad_inches: float = 0.1,
    metadata: Optional[dict] = None,
    **kwargs: Any,
) -> None:
    """Save the current figure to a file."""
    gcf().savefig(
        fname, dpi=dpi, facecolor=facecolor,
        edgecolor=edgecolor, orientation=orientation,
        format=format, transparent=transparent,
        bbox_inches=bbox_inches, pad_inches=pad_inches,
        metadata=metadata, **kwargs,
    )


def suptitle(t: str, **kwargs: Any) -> None:
    """Add a centered suptitle to the figure."""
    gcf().suptitle(t, **kwargs)


def tight_layout(*, pad: float = 1.08, h_pad: Optional[float] = None,
                 w_pad: Optional[float] = None,
                 rect: Optional[Tuple[float, float, float, float]] = None
                 ) -> None:
    """Adjust subplot parameters for tight layout (stub for compatibility)."""
    pass


# ── Interactive Mode ──────────────────────────────────────────────────

def ion() -> None:
    """Turn on interactive mode (stub)."""
    global _interactive
    _interactive = True


def ioff() -> None:
    """Turn off interactive mode (stub)."""
    global _interactive
    _interactive = False


def isinteractive() -> bool:
    """Return whether interactive mode is on."""
    return _interactive


# ── Utilities ─────────────────────────────────────────────────────────

def setp(obj: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Set properties on artist objects.

    setp(obj, 'property', value) or setp(obj, prop1=val1, prop2=val2).
    """
    if len(args) == 2 and isinstance(args[0], str):
        prop, val = args
        setattr(obj, f'set_{prop}', lambda v: None)
        if hasattr(obj, f'set_{prop}'):
            getattr(obj, f'set_{prop}')(val)
    else:
        for key, val in kwargs.items():
            method_name = f'set_{key}'
            if hasattr(obj, method_name):
                getattr(obj, method_name)(val)

    if isinstance(obj, (list, tuple)):
        return [None for _ in obj]
    return None
