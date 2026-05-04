# ShenBi (神笔)

> matplotlib syntax + pyqtgraph performance

ShenBi is a high-performance Python plotting library that provides the familiar
matplotlib API while leveraging pyqtgraph's GPU-accelerated rendering engine.
Write code like you do with matplotlib, get the speed of pyqtgraph.

[中文文档](README_CN.md) | [Tutorial](demo/tutorial.md) | [中文教程](demo/tutorial_cn.md)

## Why ShenBi?

| | matplotlib | pyqtgraph | **ShenBi** |
|---|---|---|---|
| API friendliness | Excellent | Complex | **Excellent** (matplotlib-compatible) |
| Performance | Slow on large data | Very fast | **Very fast** (pyqtgraph engine) |
| Interactivity | Limited | Rich (pan/zoom) | **Rich** (built-in) |
| GPU acceleration | No | Yes (OpenGL) | **Yes** (inherited) |
| Auto-downsampling | No | Yes | **Yes** (automatic) |
| Grid by default | Yes | Yes | **No** (cleaner look) |
| Background | White | Dark | **White** (matplotlib-style) |

## Quick Start

```python
import numpy as np
import shenbi.pyplot as plt

# Generate 1 million data points
x = np.linspace(0, 100, 1_000_000)
y = np.sin(x) + 0.1 * np.random.randn(1_000_000)

# Use familiar matplotlib syntax
plt.figure(figsize=(12, 4))
plt.plot(x, y, 'b-', linewidth=1, label='Signal')
plt.title('1 Million Points — Rendered Instantly')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.savefig('signal.png')
```

## Features

### Core Plotting
```python
# Line plots with format strings
plt.plot(x, y, 'r-', linewidth=2, label='Line')
plt.plot(x, y2, 'b--', marker='o', markersize=4)

# Scatter with colormap
plt.scatter(x, y, s=10, c=values, cmap='viridis', alpha=0.5)

# Bar charts with edge colors
plt.bar(categories, values, color='steelblue', edgecolor='white')

# Histograms
plt.hist(data, bins=50, color='green', alpha=0.7, edgecolor='white')

# Contour / filled contour
plt.contourf(X, Y, Z, levels=20, cmap='plasma')
plt.contour(X, Y, Z, levels=8, colors='white')
```

### Subplots & Layout
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, np.sin(x), 'r-')
axes[0, 1].scatter(xs, ys, s=5, c=ys, cmap='coolwarm')
axes[1, 0].bar([0, 1, 2, 3], [10, 20, 15, 25])
axes[1, 1].hist(np.random.randn(5000), bins=30)
plt.tight_layout()
```

### Advanced Features
- **Colormaps**: `viridis`, `plasma`, `inferno`, `magma`, `jet`, `cool`, `hot`, `coolwarm`, `Blues`, `Reds`, etc.
- **Color cycle**: Automatic tab10 color cycling (`C0`-`C9`)
- **Format strings**: `'r-o'`, `'b--'`, `'g.'`, `'k:'`, `'mo-'`, `'c^--'`, etc.
- **Error bars**: `plt.errorbar(x, y, yerr=errors, capsize=5)`
- **Fill between**: `plt.fill_between(x, y1, y2, alpha=0.3)`
- **Box plots**: `plt.boxplot(data, tick_labels=labels)`
- **Pie charts**: `plt.pie(sizes, labels=labels, colors=colors)`
- **Stem plots**: `plt.stem(x, y, linefmt='C0-', markerfmt='C0o')`
- **Step plots**: `plt.step(x, y, where='mid')`
- **Reference lines**: `plt.axhline(y=0)`, `plt.axvline(x=5)`
- **Text & annotations**: `plt.text()`, `plt.annotate()`
- **Image display**: `plt.imshow(data, cmap='viridis')`
- **Log scales**: `plt.xscale('log')`, `plt.yscale('log')`, `plt.loglog()`
- **Twin axes**: `ax2 = ax1.twinx()`
- **Line2D API**: `line.set_color()`, `line.set_linewidth()`, `line.set_marker()`, etc.
- **Polygon patches**: `plt.fill()`, `plt.Polygon()`, `ax.add_patch()`

### 3D Visualization (2D Projection)
Works on all platforms including Apple Silicon macOS:
```python
from demo.demo_pyqtgraph_3d import project_3d

px, py, pz = project_3d(X, Y, Z, azim=-50, elev=25)
plt.scatter(px, py, s=20, c=colors, cmap='viridis')
```

## Installation

```bash
# Required dependencies
pip install pyqtgraph numpy

# Qt bindings (choose one)
pip install PySide6   # recommended
# or: pip install PyQt6 PyQt5 PySide2
```

```bash
# Install ShenBi
git clone https://github.com/CodeOfMe/ShenBi.git
cd ShenBi
pip install -e .
```

## Requirements

- Python >= 3.9
- pyqtgraph >= 0.13.0
- numpy >= 1.20
- Qt bindings: PyQt5, PyQt6, PySide2, or PySide6
- Optional: scikit-learn (for dataset demos), scipy (for KDE/interpolation)

## Performance

ShenBi inherits pyqtgraph's multi-level performance optimizations:

- **Automatic downsampling**: When viewing large datasets, points are automatically
  decimated based on screen pixel density
- **Clip-to-view**: Only data within the visible view range is processed for rendering
- **GPU acceleration**: When using OpenGL-backed widgets, vertex data is uploaded
  to GPU via VBOs for hardware-accelerated rendering
- **Segmented line rendering**: Fast QPainter.drawLines() used when beneficial

Rendering 1 million data points takes ~1 second on CPU, virtually instant on GPU.

## Architecture

```
User Code (matplotlib-style API)
        │
        ▼
   shenbi.pyplot  ──  State-based API (plt.plot, plt.figure, etc.)
        │
        ▼
   ShenBiFigure   ──  Wraps pyqtgraph GraphicsLayoutWidget
        │
        ▼
   ShenBiAxes     ──  Wraps pyqtgraph PlotItem
        │
        ▼
   ShenBiLine2D   ──  Wraps pyqtgraph PlotDataItem
        │
        ▼
   pyqtgraph      ──  High-performance Qt-based rendering engine
```

## Project Structure

```
ShenBi/
├── shenbi/
│   ├── __init__.py        # Package entry point
│   ├── pyplot.py          # matplotlib-compatible state API (40+ functions)
│   ├── figure.py          # ShenBiFigure wrapper
│   ├── axes.py            # ShenBiAxes with 30+ methods
│   ├── line.py            # ShenBiLine2D, ShenBiScatter wrappers
│   ├── colors.py          # Color resolution (CSS4, hex, RGB, tab10)
│   ├── cm.py              # Colormap support (24 colormaps)
│   ├── utils.py           # Format string parser, marker/linestyle normalization
│   ├── mplot3d.py         # 3D plotting toolkit (Axes3D)
│   └── tests/             # Unit tests
├── demo/
│   ├── demo_pyqtgraph_2d.py   # 20 dataset visualization demos
│   ├── demo_pyqtgraph_3d.py   # 10 3D projection demos
│   ├── tutorial.md            # English tutorial
│   ├── tutorial_cn.md         # Chinese tutorial
│   └── output/                # Generated PNG + SVG files
├── README.md              # English documentation
├── README_CN.md           # Chinese documentation
├── pyproject.toml         # Package configuration
├── upload_pypi.sh         # PyPI upload script (Linux/macOS)
└── upload_pypi.bat        # PyPI upload script (Windows)
```

## Dataset Demos

ShenBi includes 30 comprehensive demos using real standard datasets:

| Dataset | Samples | Features | Classes |
|---------|---------|----------|---------|
| Iris | 150 | 4 | 3 |
| Wine | 178 | 13 | 3 |
| Breast Cancer | 569 | 30 | 2 |
| Digits | 1,797 | 64 | 10 |
| Diabetes | 442 | 10 | 1 (regression) |

Run all demos:
```bash
cd demo
python demo_pyqtgraph_2d.py   # 20 2D demos
python demo_pyqtgraph_3d.py   # 10 3D demos
```

## License

GPLv3 — See [LICENSE](LICENSE) for the full text.
