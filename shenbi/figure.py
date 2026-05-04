"""
ShenBiFigure: matplotlib Figure-compatible wrapper around pyqtgraph widgets.

Manages a window containing a GraphicsLayoutWidget that hosts
multiple subplots (PlotItems).
"""
from __future__ import annotations

import os
from typing import Any, List, Optional, Tuple, Union

import pyqtgraph as pg

from .axes import ShenBiAxes
from .colors import _reset_color_cycle


class ShenBiFigure:
    """
    A matplotlib Figure-compatible object wrapping pyqtgraph windows.

    Each Figure contains one window (QMainWindow or dialog) with a
    GraphicsLayoutWidget that holds the subplot grid.

    Parameters
    ----------
    num : int or str, optional
        Figure identifier
    figsize : tuple of (width, height), optional
        Figure size in inches (converted to pixels at 100 DPI)
    dpi : float, optional
        Dots per inch (default 100)
    facecolor : str, optional
        Background color
    **kwargs : dict
        Additional Figure properties
    """

    _figures: List[ShenBiFigure] = []

    def __init__(
        self,
        num: Optional[Union[int, str]] = None,
        figsize: Optional[Tuple[float, float]] = None,
        dpi: float = 100,
        *,
        facecolor: Optional[str] = None,
        edgecolor: Optional[str] = None,
        frameon: bool = True,
        clear: bool = False,
        **kwargs: Any,
    ):
        self._num = num
        self._dpi = dpi
        self._facecolor = facecolor

        figsize = figsize or (6.4, 4.8)
        width_px = int(figsize[0] * dpi)
        height_px = int(figsize[1] * dpi)

        self._window = pg.GraphicsLayoutWidget(
            title=f"Figure {num}" if num else "ShenBi Figure"
        )
        self._window.resize(width_px, height_px)
        self._window.setBackground('w')

        self._layout: pg.GraphicsLayout = self._window.ci
        self._axes_list: List[ShenBiAxes] = []

        self._grid_rows = 0
        self._grid_cols = 0
        self._sharex: Optional[ShenBiAxes] = None
        self._sharey: Optional[ShenBiAxes] = None

        ShenBiFigure._figures.append(self)

    # ── Subplot Management ────────────────────────────────────────────

    def add_subplot(self, *args: Any, **kwargs: Any) -> ShenBiAxes:
        """
        Add a subplot to the figure.

        Parameters
        ----------
        nrows, ncols, index : int
            Grid specification (3-digit or 3 args)
        projection : str, optional
            Projection type (not supported)
        sharex, sharey : ShenBiAxes, optional
            Share x/y axes with another subplot
        **kwargs
            Additional subplot properties

        Returns
        -------
        ShenBiAxes
        """
        if len(args) == 1 and isinstance(args[0], int) and args[0] >= 100:
            # 3-digit notation: 221 = 2 rows, 2 cols, index 1
            num = args[0]
            nrows = num // 100
            ncols = (num // 10) % 10
            index = num % 10
        elif len(args) >= 3:
            nrows, ncols, index = int(args[0]), int(args[1]), int(args[2])
        else:
            nrows, ncols, index = 1, 1, 1

        self._grid_rows = max(self._grid_rows, nrows)
        self._grid_cols = max(self._grid_cols, ncols)

        row = (index - 1) // ncols
        col = (index - 1) % ncols

        plot_item = self._layout.addPlot(
            row=row, col=col,
            rowspan=kwargs.get('rowspan', 1),
            colspan=kwargs.get('colspan', 1),
            title=kwargs.get('title', None),
        )

        if 'sharex' in kwargs and kwargs['sharex'] is not None:
            plot_item.setXLink(kwargs['sharex'].plot_item)
        if 'sharey' in kwargs and kwargs['sharey'] is not None:
            plot_item.setYLink(kwargs['sharey'].plot_item)

        ax = ShenBiAxes(plot_item)
        self._axes_list.append(ax)
        return ax

    def subplots(self, nrows: int = 1, ncols: int = 1, *,
                 sharex: bool = False, sharey: bool = False,
                 squeeze: bool = True,
                 width_ratios: Optional[List[float]] = None,
                 height_ratios: Optional[List[float]] = None,
                 subplot_kw: Optional[dict] = None,
                 gridspec_kw: Optional[dict] = None,
                 **fig_kw: Any) -> Tuple[ShenBiFigure, Any]:
        """
        Create a figure and a set of subplots.

        Returns
        -------
        fig : ShenBiFigure
        ax : ShenBiAxes or array of ShenBiAxes
        """
        subplot_kw = subplot_kw or {}
        axes = []

        prev_ax = None
        for i in range(nrows * ncols):
            row = i // ncols
            col = i % ncols

            kw = dict(subplot_kw)
            if sharex and prev_ax is not None and col > 0:
                kw['sharex'] = prev_ax
            if sharey and prev_ax is not None and row > 0:
                kw['sharey'] = prev_ax

            ax = self.add_subplot(nrows, ncols, i + 1, **kw)
            axes.append(ax)
            prev_ax = axes[0] if sharex else None

        if squeeze:
            if nrows == 1 and ncols == 1:
                axes_arr: Any = axes[0]
            elif nrows == 1 or ncols == 1:
                axes_arr = axes
            else:
                import numpy as np
                axes_arr = np.array(axes).reshape(nrows, ncols)
        else:
            import numpy as np
            axes_arr = np.array(axes).reshape(nrows, ncols)

        return self, axes_arr

    # ── Display / Export ──────────────────────────────────────────────

    def show(self) -> None:
        """Display the figure window."""
        self._window.show()

    def savefig(
        self,
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
        """Save the figure to a file. Supports PNG and SVG formats."""
        ext = os.path.splitext(fname)[1].lower()
        if ext in ('.svg',):
            from pyqtgraph.exporters import SVGExporter
            exporter = SVGExporter(self._window.scene())
        else:
            from pyqtgraph.exporters import ImageExporter
            exporter = ImageExporter(self._window.scene())
            exporter.parameters()['width'] = max(
                int(self._window.size().width() * (dpi or self._dpi) / 100),
                100
            )

        if transparent:
            self._window.setBackground(None)
        else:
            self._window.setBackground('w')

        exporter.export(fname)

    def suptitle(self, t: str, **kwargs: Any) -> None:
        """Add a centered suptitle to the figure.

        Note: Simplified implementation using window title.
        For full suptitle support, use the LayoutWidget.
        """
        self._window.setWindowTitle(t)

    # ── Figure Management ─────────────────────────────────────────────

    def set_size_inches(self, w: float, h: float,
                        forward: bool = True) -> None:
        """Set the figure size in inches."""
        self._window.resize(int(w * self._dpi), int(h * self._dpi))

    def get_size_inches(self) -> Tuple[float, float]:
        """Get the figure size in inches."""
        size = self._window.size()
        return (size.width() / self._dpi, size.height() / self._dpi)

    def set_dpi(self, dpi: float) -> None:
        """Set the DPI."""
        self._dpi = dpi

    def get_dpi(self) -> float:
        """Get the DPI."""
        return self._dpi

    def clf(self) -> None:
        """Clear the figure."""
        self._layout.clear()
        self._axes_list.clear()
        _reset_color_cycle()

    def close(self) -> None:
        """Close the figure window."""
        self._window.close()
        if self in ShenBiFigure._figures:
            ShenBiFigure._figures.remove(self)

    @property
    def axes(self) -> List[ShenBiAxes]:
        """Return the list of axes in this figure."""
        return self._axes_list

    @property
    def gca(self) -> Optional[ShenBiAxes]:
        """Get the current axes (last created)."""
        return self._axes_list[-1] if self._axes_list else None

    @property
    def window(self):
        """Get the underlying Qt window/widget."""
        return self._window

    @classmethod
    def get_all_figures(cls) -> List[ShenBiFigure]:
        """Return all existing figures."""
        return cls._figures

    @classmethod
    def get_figure(cls, num: Union[int, str]) -> Optional[ShenBiFigure]:
        """Get a figure by its num identifier."""
        for fig in cls._figures:
            if fig._num == num:
                return fig
        return None
