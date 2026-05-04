"""
ShenBi colormap module — matplotlib.cm-compatible colormap support.

Provides:
- All major matplotlib colormaps (viridis, plasma, inferno, magma, cividis,
  jet, cool, hot, etc.)
- get_cmap() function compatible with matplotlib.cm.get_cmap()
- Colormap class that can map scalar values to RGBA colors
- Direct access via plt.cm.viridis, plt.cm.jet, etc.
"""
from __future__ import annotations

from typing import List, Optional, Tuple, Union

import numpy as np


def _interpolate(colors: List[Tuple[float, float, float, float]],
                 n: int = 256) -> np.ndarray:
    """Interpolate a list of (r, g, b, a) control points into n RGBA entries."""
    colors = np.asarray(colors, dtype=float)
    x = np.linspace(0, 1, len(colors))
    xnew = np.linspace(0, 1, n)
    result = np.zeros((n, 4), dtype=float)
    for c in range(4):
        result[:, c] = np.interp(xnew, x, colors[:, c])
    return np.clip(result * 255, 0, 255).astype(np.uint8)


def _simple_cmap(name: str, colors: list) -> 'Colormap':
    """Build a Colormap from a list of (r, g, b, a) control points."""
    lut = _interpolate(colors)
    return Colormap(name=name, lut=lut)


class Colormap:
    """matplotlib-compatible colormap that maps [0,1] -> RGBA(0-255)."""

    def __init__(self, name: str, lut: np.ndarray):
        self.name = name
        self._lut = lut

    def __call__(self, X: Union[float, np.ndarray],
                 alpha: Optional[float] = None,
                 bytes: bool = False) -> np.ndarray:
        """Map scalar(s) in [0,1] to RGBA."""
        X = np.asarray(X, dtype=float)
        scalar_input = X.ndim == 0
        X = np.atleast_1d(X)
        X = np.clip(X, 0, 1)
        indices = (X * (len(self._lut) - 1)).astype(int)
        result = self._lut[indices]
        if alpha is not None:
            a = int(alpha * 255) if alpha <= 1.0 else int(min(alpha, 255))
            result = result.copy()
            result[:, 3] = a
        if bytes:
            result = result.astype(np.uint8)
        if scalar_input:
            return result[0]
        return result

    def __repr__(self):
        return f"Colormap(name={self.name!r}, N={len(self._lut)})"

    @property
    def colors(self):
        return self._lut


# ── Colormap Definitions ──────────────────────────────────────────
# Control points in (r, g, b, a) format, values in [0, 1]

_viridis = [
    (0.267, 0.004, 0.329, 1.0),
    (0.282, 0.140, 0.457, 1.0),
    (0.231, 0.322, 0.545, 1.0),
    (0.177, 0.490, 0.558, 1.0),
    (0.129, 0.648, 0.510, 1.0),
    (0.369, 0.789, 0.382, 1.0),
    (0.667, 0.867, 0.226, 1.0),
    (0.993, 0.906, 0.144, 1.0),
]

_plasma = [
    (0.050, 0.030, 0.528, 1.0),
    (0.340, 0.082, 0.612, 1.0),
    (0.581, 0.131, 0.628, 1.0),
    (0.788, 0.202, 0.553, 1.0),
    (0.924, 0.326, 0.402, 1.0),
    (0.976, 0.495, 0.251, 1.0),
    (0.940, 0.675, 0.153, 1.0),
    (0.868, 0.842, 0.143, 1.0),
]

_inferno = [
    (0.001, 0.000, 0.014, 1.0),
    (0.218, 0.024, 0.396, 1.0),
    (0.506, 0.082, 0.469, 1.0),
    (0.741, 0.215, 0.373, 1.0),
    (0.901, 0.394, 0.218, 1.0),
    (0.969, 0.590, 0.133, 1.0),
    (0.988, 0.802, 0.219, 1.0),
    (0.988, 0.998, 0.645, 1.0),
]

_magma = [
    (0.001, 0.000, 0.014, 1.0),
    (0.200, 0.005, 0.360, 1.0),
    (0.443, 0.077, 0.535, 1.0),
    (0.671, 0.213, 0.458, 1.0),
    (0.853, 0.384, 0.339, 1.0),
    (0.949, 0.591, 0.266, 1.0),
    (0.987, 0.801, 0.342, 1.0),
    (0.988, 0.998, 0.645, 1.0),
]

_cividis = [
    (0.000, 0.135, 0.305, 1.0),
    (0.163, 0.332, 0.455, 1.0),
    (0.369, 0.503, 0.518, 1.0),
    (0.581, 0.632, 0.488, 1.0),
    (0.790, 0.744, 0.406, 1.0),
    (0.976, 0.852, 0.302, 1.0),
]

_jet = [
    (0.000, 0.000, 0.500, 1.0),
    (0.000, 0.000, 1.000, 1.0),
    (0.000, 1.000, 1.000, 1.0),
    (0.500, 1.000, 0.000, 1.0),
    (1.000, 1.000, 0.000, 1.0),
    (1.000, 0.000, 0.000, 1.0),
    (0.500, 0.000, 0.000, 1.0),
]

_cool = [
    (0.000, 1.000, 1.000, 1.0),
    (1.000, 0.000, 1.000, 1.0),
]

_hot = [
    (0.0, 0.0, 0.0, 1.0),
    (0.5, 0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0, 1.0),
    (1.0, 0.5, 0.0, 1.0),
    (1.0, 1.0, 0.0, 1.0),
    (1.0, 1.0, 1.0, 1.0),
]

_coolwarm = [
    (0.230, 0.300, 0.750, 1.0),
    (0.350, 0.530, 0.790, 1.0),
    (0.700, 0.700, 0.700, 1.0),
    (0.920, 0.470, 0.370, 1.0),
    (0.700, 0.020, 0.150, 1.0),
]

_bwr = [
    (0.000, 0.000, 1.000, 1.0),
    (1.000, 1.000, 1.000, 1.0),
    (1.000, 0.000, 0.000, 1.0),
]

_seismic = [
    (0.000, 0.000, 0.350, 1.0),
    (0.350, 0.350, 0.900, 1.0),
    (1.000, 1.000, 1.000, 1.0),
    (0.900, 0.350, 0.350, 1.0),
    (0.350, 0.000, 0.000, 1.0),
]

_Reds = [
    (1.000, 0.970, 0.970, 1.0),
    (0.980, 0.500, 0.450, 1.0),
    (0.850, 0.150, 0.150, 1.0),
    (0.650, 0.000, 0.000, 1.0),
]

_Blues = [
    (0.970, 0.970, 1.000, 1.0),
    (0.450, 0.650, 0.930, 1.0),
    (0.150, 0.350, 0.850, 1.0),
    (0.030, 0.150, 0.450, 1.0),
]

_Greens = [
    (0.970, 0.970, 0.970, 1.0),
    (0.500, 0.870, 0.500, 1.0),
    (0.200, 0.700, 0.200, 1.0),
    (0.000, 0.450, 0.000, 1.0),
]

_Oranges = [
    (1.000, 0.970, 0.920, 1.0),
    (0.980, 0.650, 0.350, 1.0),
    (0.930, 0.400, 0.130, 1.0),
    (0.700, 0.150, 0.020, 1.0),
]

_Greys = [
    (1.000, 1.000, 1.000, 1.0),
    (0.750, 0.750, 0.750, 1.0),
    (0.400, 0.400, 0.400, 1.0),
    (0.000, 0.000, 0.000, 1.0),
]

_Purples = [
    (0.970, 0.940, 0.980, 1.0),
    (0.650, 0.400, 0.800, 1.0),
    (0.490, 0.150, 0.680, 1.0),
    (0.280, 0.030, 0.420, 1.0),
]

_spring = [(1.0, 0.0, 1.0, 1.0), (1.0, 1.0, 0.0, 1.0)]
_summer = [(0.0, 0.5, 0.4, 1.0), (1.0, 1.0, 0.4, 1.0)]
_autumn = [(1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0)]
_winter = [(0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.5, 1.0)]

_twilight = [
    (0.876, 0.860, 0.952, 1.0),
    (0.500, 0.500, 0.860, 1.0),
    (0.295, 0.280, 0.540, 1.0),
    (0.500, 0.500, 0.860, 1.0),
    (0.876, 0.860, 0.952, 1.0),
]

_twilight_shifted = [
    (0.295, 0.280, 0.540, 1.0),
    (0.500, 0.500, 0.860, 1.0),
    (0.876, 0.860, 0.952, 1.0),
    (0.500, 0.500, 0.860, 1.0),
    (0.295, 0.280, 0.540, 1.0),
]

# Build all colormaps
_cmap_data = {
    'viridis': _viridis, 'plasma': _plasma, 'inferno': _inferno,
    'magma': _magma, 'cividis': _cividis, 'jet': _jet,
    'cool': _cool, 'hot': _hot, 'coolwarm': _coolwarm,
    'bwr': _bwr, 'seismic': _seismic,
    'Reds': _Reds, 'Blues': _Blues, 'Greens': _Greens,
    'Oranges': _Oranges, 'Greys': _Greys, 'Purples': _Purples,
    'spring': _spring, 'summer': _summer, 'autumn': _autumn,
    'winter': _winter, 'twilight': _twilight,
    'twilight_shifted': _twilight_shifted,
}

_cmaps: dict[str, Colormap] = {}
for _name, _stops in _cmap_data.items():
    _cmaps[_name] = _simple_cmap(_name, _stops)
    _cmaps[_name.lower()] = _cmaps[_name]


def get_cmap(name: Union[str, int] = None,
             lut: Optional[int] = None) -> Colormap:
    """Get a colormap by name (matplotlib.cm.get_cmap compatible)."""
    if name is None:
        name = 'viridis'
    if isinstance(name, int):
        name = list(_cmaps.keys())[name * 2]
    name_lower = name.lower()
    if name_lower in _cmaps:
        return _cmaps[name_lower]
    if name in _cmaps:
        return _cmaps[name]
    raise ValueError(f"Colormap {name!r} not found. "
                     f"Available: {sorted(set(_cmaps.keys()))}")


class _CMModule:
    """Module-like object for plt.cm.viridis / plt.cm.jet style access."""

    def __init__(self):
        self._cmaps = _cmaps

    def __getattr__(self, name: str) -> Colormap:
        if name in self._cmaps:
            return self._cmaps[name]
        name_lower = name.lower()
        if name_lower in self._cmaps:
            return self._cmaps[name_lower]
        raise AttributeError(f"No colormap named {name!r}")

    def get_cmap(self, name: Union[str, int] = None,
                 lut: Optional[int] = None) -> Colormap:
        return get_cmap(name, lut)


cm = _CMModule()