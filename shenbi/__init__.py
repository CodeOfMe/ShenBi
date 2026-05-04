"""
ShenBi (神笔) - matplotlib syntax with pyqtgraph performance.

Usage:
    import shenbi.pyplot as plt
    import numpy as np

    x = np.linspace(0, 10, 1000000)
    y = np.sin(x)

    plt.plot(x, y, 'r-', linewidth=2, label='sin(x)')
    plt.title('Sine Wave')
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.grid(True)
    plt.legend()
    plt.show()
"""
from . import pyplot
from .figure import ShenBiFigure
from .axes import ShenBiAxes
from .line import ShenBiLine2D, ShenBiScatter
from .colors import resolve_color
from .utils import parse_format_string
from .cm import cm, get_cmap, Colormap
from . import mplot3d

__version__ = "0.1.1"
__all__ = [
    "pyplot",
    "mplot3d",
    "ShenBiFigure",
    "ShenBiAxes",
    "ShenBiLine2D",
    "ShenBiScatter",
    "resolve_color",
    "parse_format_string",
    "cm",
    "get_cmap",
    "Colormap",
]
