"""
ShenBi mplot3d — matplotlib.mplot3d-compatible 3D plotting toolkit.

Powered by pyqtgraph.opengl (hardware-accelerated OpenGL rendering).

Usage:
    from shenbi import mplot3d
    fig = mplot3d.figure()
    ax = mplot3d.Axes3D(fig)
    
    # OR
    import shenbi.pyplot as plt
    ax = plt.subplot(projection='3d')

Supported methods:
    - plot3D / plot — 3D line plot
    - scatter3D / scatter — 3D scatter
    - plot_surface — surface plot
    - plot_wireframe — wireframe mesh
    - bar3d — 3D bar chart
    - contour3D — isosurface / volume rendering
    - quiver — vector field (arrow)
    - plot_trisurf — triangular surface
    - set_xlabel / set_ylabel / set_zlabel
    - set_title
    - view_init — set camera azimuth/elevation
    - savefig — export to PNG/SVG
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from .colors import resolve_color, TAB10_COLORS


class Axes3D:
    """matplotlib.mplot3d.Axes3D-compatible 3D axes."""

    def __init__(self, fig: Any = None, *,
                 auto_add_to_figure: bool = True,
                 azim: float = -60, elev: float = 30,
                 shareview: Optional[Any] = None,
                 proj_type: str = 'persp',
                 focal_length: Optional[float] = None,
                 computed_zorder: bool = True,
                 **kwargs: Any):
        self._gl_view = gl.GLViewWidget()
        self._items: list = []
        self._azim = azim
        self._elev = elev
        self._auto_scale = True

        self._gl_view.setCameraPosition(distance=10)
        self._gl_view.opts['azimuth'] = self._azim
        self._gl_view.opts['elevation'] = self._elev

        self._grid = gl.GLGridItem()
        self._grid.setSize(10, 10)
        self._grid.setSpacing(1, 1)
        self._gl_view.addItem(self._grid)

        self._axis = gl.GLAxisItem()
        self._gl_view.addItem(self._axis)

        self._xlabel: Optional[str] = None
        self._ylabel: Optional[str] = None
        self._zlabel: Optional[str] = None

    @property
    def gl_view(self):
        return self._gl_view

    # ── Core 3D Plot Methods ─────────────────────────────────────

    def plot(self, xs: Any, ys: Any, zs: Any = None,
             *args: Any, **kwargs: Any) -> gl.GLLinePlotItem:
        """Plot 3D lines. Alias for plot3D."""
        return self.plot3D(xs, ys, zs, *args, **kwargs)

    def plot3D(self, xs: Any, ys: Any, zs: Any = None,
               *args: Any, **kwargs: Any) -> gl.GLLinePlotItem:
        """Plot 3D line/curve."""
        xs = np.asarray(xs, dtype=float)
        ys = np.asarray(ys, dtype=float)
        zs = np.asarray(zs, dtype=float) if zs is not None else np.zeros_like(xs)

        color = kwargs.pop('color', None)
        rgba = resolve_color(color)
        width = kwargs.pop('linewidth', kwargs.pop('lw', 1.0))

        pts = np.column_stack([xs, ys, zs])
        gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)
        if width == 0:
            item = gl.GLLinePlotItem(pos=pts, color=gl_color, width=1, antialias=True, mode='line_strip')
        else:
            item = gl.GLLinePlotItem(pos=pts, color=gl_color, width=width, antialias=True, mode='line_strip')

        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def scatter(self, xs: Any, ys: Any, zs: Any = None,
                s: Optional[Any] = None,
                c: Optional[Any] = None,
                *args: Any, **kwargs: Any) -> gl.GLScatterPlotItem:
        """3D scatter plot."""
        return self.scatter3D(xs, ys, zs, s=s, c=c, *args, **kwargs)

    def scatter3D(self, xs: Any, ys: Any, zs: Any = None,
                  s: Optional[Any] = None,
                  c: Optional[Any] = None,
                  *args: Any, **kwargs: Any) -> gl.GLScatterPlotItem:
        """3D scatter plot."""
        xs = np.asarray(xs, dtype=float)
        ys = np.asarray(ys, dtype=float)
        zs = np.asarray(zs, dtype=float) if zs is not None else np.zeros_like(xs)

        alpha = kwargs.pop('alpha', 1.0)

        color = c if c is not None else kwargs.pop('color', TAB10_COLORS[0])
        if isinstance(color, (list, np.ndarray)) and not isinstance(color, str):
            gl_colors = []
            for cc in color:
                rgba = resolve_color(cc, alpha)
                gl_colors.append((rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255))
        else:
            rgba = resolve_color(color, alpha)
            gl_colors = [(rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)]

        size = float(np.asarray(s).flat[0]) if s is not None else 10.0

        pts = np.column_stack([xs, ys, zs])
        item = gl.GLScatterPlotItem(pos=pts, size=size, color=gl_colors, pxMode=False)
        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def plot_surface(self, X: Any, Y: Any, Z: Any,
                     *args: Any,
                     color: Optional[str] = None,
                     cmap: Optional[Any] = None,
                     alpha: float = 1.0,
                     rstride: int = 1, cstride: int = 1,
                     facecolors: Optional[Any] = None,
                     shade: bool = True,
                     **kwargs: Any) -> gl.GLSurfacePlotItem:
        """Plot a 3D surface. X, Y should be 1D, Z should be 2D."""
        X = np.asarray(X, dtype=float)
        Y = np.asarray(Y, dtype=float)
        Z = np.asarray(Z, dtype=float)
        if X.ndim == 2:
            X = X[0, :]
        if Y.ndim == 2:
            Y = Y[:, 0]

        color = color or kwargs.pop('color', 'b')
        rgba = resolve_color(color, alpha)
        gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)

        item = gl.GLSurfacePlotItem(
            x=X, y=Y, z=Z,
            color=gl_color,
            shader='shaded' if shade else 'normalColor',
            computeNormals=shade,
        )
        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def plot_wireframe(self, X: Any, Y: Any, Z: Any,
                       *args: Any,
                       color: Optional[str] = None,
                       rstride: int = 1, cstride: int = 1,
                       alpha: float = 1.0,
                       **kwargs: Any) -> gl.GLMeshItem:
        """Plot a 3D wireframe mesh."""
        X_arr = np.asarray(X, dtype=float)
        Y_arr = np.asarray(Y, dtype=float)
        Z_arr = np.asarray(Z, dtype=float)

        color = color or 'k'
        rgba = resolve_color(color, alpha)
        gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)

        mesh_data = self._make_mesh_data(X_arr, Y_arr, Z_arr, rstride, cstride)
        item = gl.GLMeshItem(
            vertexes=mesh_data['vertexes'],
            faces=mesh_data['faces'],
            faceColors=None,
            edgeColor=gl_color,
            drawEdges=True,
            drawFaces=False,
            smooth=False,
        )
        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def plot_trisurf(self, X: Any, Y: Any, Z: Any,
                     triangles: Optional[Any] = None,
                     color: Optional[str] = None,
                     cmap: Optional[Any] = None,
                     alpha: float = 1.0,
                     shade: bool = True,
                     **kwargs: Any) -> gl.GLMeshItem:
        """Plot a triangulated surface."""
        X = np.asarray(X, dtype=float)
        Y = np.asarray(Y, dtype=float)
        Z = np.asarray(Z, dtype=float)

        if triangles is None:
            from scipy.spatial import Delaunay
            tri = Delaunay(np.column_stack([X, Y]))
            faces = tri.simplices
        else:
            faces = np.asarray(triangles, dtype=int)

        vertexes = np.column_stack([X, Y, Z])
        color = color or 'steelblue'
        rgba = resolve_color(color, alpha)
        gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)

        item = gl.GLMeshItem(
            vertexes=vertexes,
            faces=faces,
            color=gl_color,
            shader='shaded' if shade else 'normalColor',
            computeNormals=shade,
            smooth=False,
        )
        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def bar3d(self, x: Any, y: Any, z: Any,
              dx: Any = 1, dy: Any = 1, dz: Any = 1,
              color: Optional[Any] = None,
              alpha: float = 1.0,
              shade: bool = True,
              **kwargs: Any) -> list:
        """Plot 3D bars."""
        x = np.atleast_1d(np.asarray(x, dtype=float))
        y = np.atleast_1d(np.asarray(y, dtype=float))
        z_arr = np.atleast_1d(np.asarray(z, dtype=float))
        n = len(z_arr)

        dx = np.atleast_1d(np.asarray(dx, dtype=float))
        dy = np.atleast_1d(np.asarray(dy, dtype=float))
        dz = np.atleast_1d(np.asarray(dz, dtype=float))

        if dx.shape[0] == 1: dx = np.full(n, dx[0])
        if dy.shape[0] == 1: dy = np.full(n, dy[0])
        if dz.shape[0] == 1: dz = np.full(n, dz[0])

        if color is None:
            colors = TAB10_COLORS[:n]
        elif isinstance(color, str):
            colors = [color] * n
        elif isinstance(color, (list, np.ndarray)):
            if isinstance(color, np.ndarray) and color.ndim == 1 and color.dtype.kind in 'if':
                # Numeric array — map through colormap-like colors
                lo, hi = color.min(), color.max()
                rng = hi - lo if hi != lo else 1.0
                normalized = (color - lo) / rng
                from .cm import get_cmap
                cmap_obj = get_cmap('viridis')
                colors = cmap_obj(normalized)
                # Convert to hex strings
                result_colors = []
                for c in colors:
                    result_colors.append(f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}')
                colors = result_colors
            else:
                colors = list(color)
        else:
            colors = [str(color)] * n

        items = []
        for i in range(n):
            c = resolve_color(colors[i % len(colors)], alpha)
            gl_color = (c[0]/255, c[1]/255, c[2]/255, c[3]/255)

            vx = x[i] - dx[i] / 2.0 if i < len(x) else i
            vy = y[i] - dy[i] / 2.0 if i < len(y) else 0

            vertices = np.array([
                [vx, vy, 0.0],
                [vx + dx[i], vy, 0.0],
                [vx + dx[i], vy + dy[i], 0.0],
                [vx, vy + dy[i], 0.0],
                [vx, vy, dz[i]],
                [vx + dx[i], vy, dz[i]],
                [vx + dx[i], vy + dy[i], dz[i]],
                [vx, vy + dy[i], dz[i]],
            ])

            faces = np.array([
                [0, 1, 2], [0, 2, 3],
                [4, 7, 6], [4, 6, 5],
                [0, 4, 5], [0, 5, 1],
                [1, 5, 6], [1, 6, 2],
                [2, 6, 7], [2, 7, 3],
                [3, 7, 4], [3, 4, 0],
            ])

            mesh = gl.GLMeshItem(
                vertexes=vertices, faces=faces,
                color=gl_color,
                shader='shaded' if shade else 'normalColor',
                drawEdges=True, edgeColor=(0, 0, 0, 0.3),
                drawFaces=True,
                computeNormals=True,
                smooth=False,
            )
            self._gl_view.addItem(mesh)
            items.append(mesh)
            self._items.append(mesh)

        return items

    def contour3D(self, data: np.ndarray,
                  level: float = 0.5,
                  color: Optional[str] = None,
                  alpha: float = 0.7,
                  **kwargs: Any) -> gl.GLIsosurface:
        """Plot a 3D isosurface / contour at the given level."""
        from pyqtgraph.opengl.GLIsosurface import Isosurface
        color = color or 'steelblue'
        rgba = resolve_color(color, alpha)
        gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)

        iso = Isosurface(data=data, level=level, color=gl_color)
        self._gl_view.addItem(iso)
        self._items.append(iso)
        return iso

    def volume(self, data: np.ndarray,
               alpha: float = 1.0,
               sliceDensity: int = 512,
               smooth: bool = True,
               **kwargs: Any) -> gl.GLVolumeItem:
        """Render a 3D volume."""
        data = np.asarray(data, dtype=np.float32)
        data = (data - data.min()) / (data.max() - data.min() + 1e-10)

        item = gl.GLVolumeItem(data, sliceDensity=sliceDensity, smooth=smooth)
        self._gl_view.addItem(item)
        self._items.append(item)
        return item

    def quiver(self, X: Any, Y: Any, Z: Any,
               U: Any, V: Any, W: Any,
               length: float = 1.0,
               color: Optional[Any] = None,
               normalize: bool = False,
               alpha: float = 1.0,
               **kwargs: Any) -> list:
        """3D quiver (vector) plot using line arrows."""
        X = np.asarray(X).flatten()
        Y = np.asarray(Y).flatten()
        Z = np.asarray(Z).flatten()
        U = np.asarray(U).flatten()
        V = np.asarray(V).flatten()
        W = np.asarray(W).flatten()

        if normalize:
            mag = np.sqrt(U**2 + V**2 + W**2) + 1e-10
            U = U / mag * length
            V = V / mag * length
            W = W / mag * length
        else:
            U, V, W = U * length, V * length, W * length

        color = color or 'r'
        items = []
        for i in range(len(X)):
            start = np.array([[X[i], Y[i], Z[i]]])
            end = np.array([[X[i] + U[i], Y[i] + V[i], Z[i] + W[i]]])
            pts = np.vstack([start, end])
            rgba = resolve_color(color, alpha)
            gl_color = (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3]/255)
            line = gl.GLLinePlotItem(pos=pts, color=gl_color, width=2, antialias=True)
            self._gl_view.addItem(line)
            items.append(line)
            self._items.append(line)

        return items

    # ── Decoration ───────────────────────────────────────────────

    def set_xlabel(self, label: str, **kwargs) -> None:
        self._xlabel = label

    def set_ylabel(self, label: str, **kwargs) -> None:
        self._ylabel = label

    def set_zlabel(self, label: str, **kwargs) -> None:
        self._zlabel = label

    def set_title(self, title: str, **kwargs) -> None:
        pass

    def view_init(self, elev: Optional[float] = None,
                  azim: Optional[float] = None,
                  roll: Optional[float] = None,
                  vertical_axis: str = 'z',
                  share: bool = False) -> None:
        """Set camera elevation and azimuth."""
        if elev is not None:
            self._elev = elev
            self._gl_view.opts['elevation'] = elev
        if azim is not None:
            self._azim = azim
            self._gl_view.opts['azimuth'] = azim
        self._gl_view.update()

    def set_aspect(self, aspect: str = 'auto', **kwargs) -> None:
        """Set aspect ratio (stub)."""
        pass

    def autoscale(self, enable: bool = True, **kwargs) -> None:
        self._auto_scale = enable

    def grid(self, visible: bool = True, **kwargs) -> None:
        self._grid.setVisible(visible)

    # ── Save ─────────────────────────────────────────────────────

    def savefig(self, fname: str, **kwargs) -> None:
        """Save the 3D view to a PNG image file."""
        self._gl_view.repaint()
        from PySide6 import QtWidgets, QtCore
        QtCore.QCoreApplication.processEvents()
        pixmap = self._gl_view.grab()
        pixmap.save(fname)

    # ── Helper ───────────────────────────────────────────────────

    @staticmethod
    def _make_mesh_data(X, Y, Z, rstride=1, cstride=1):
        """Build vertex and face arrays for wireframe/surface."""
        vertexes = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
        ny, nx = X.shape
        faces = []
        for i in range(0, ny - cstride, max(1, cstride)):
            for j in range(0, nx - rstride, max(1, rstride)):
                a = i * nx + j
                b = a + rstride
                c = a + cstride * nx
                d = a + rstride + cstride * nx
                if b < vertexes.shape[0] and c < vertexes.shape[0] and d < vertexes.shape[0]:
                    faces.append([a, b, d])
                    faces.append([a, d, c])

        # Edge faces for wireframe
        edge_faces = []
        for i in range(0, ny, max(1, cstride)):
            for j in range(0, nx - 1, max(1, rstride)):
                a = i * nx + j
                b = a + 1
                if b < vertexes.shape[0]:
                    edge_faces.append([a, b, a])

        for j in range(0, nx, max(1, rstride)):
            for i in range(0, ny - 1, max(1, cstride)):
                a = i * nx + j
                b = (i + 1) * nx + j
                if b < vertexes.shape[0]:
                    edge_faces.append([a, b, a])

        return {'vertexes': vertexes, 'faces': np.array(faces or edge_faces)}


# ── Convenience Functions ───────────────────────────────────────

def figure(*, figsize: Tuple[float, float] = (8, 6),
           **kwargs: Any) -> Axes3D:
    """Create a new 3D figure and return Axes3D."""
    ax = Axes3D(**kwargs)
    return ax


def subplots(nrows: int = 1, ncols: int = 1,
             *, subplot_kw: Optional[dict] = None,
             **kwargs: Any):
    """Create a 3D figure with subplots."""
    ax = Axes3D(**kwargs)
    return None, ax  # (fig, ax) tuple for compatibility
