# ShenBi (神笔)

> matplotlib syntax + pyqtgraph performance

ShenBi is a high-performance Python plotting library that provides the familiar
matplotlib API while leveraging pyqtgraph's GPU-accelerated rendering engine.
Write code like you do with matplotlib, get the speed of pyqtgraph.

## Why ShenBi?

| | matplotlib | pyqtgraph | **ShenBi** |
|---|---|---|---|
| API friendliness | Excellent | Complex | **Excellent** (matplotlib-compatible) |
| Performance | Slow on large data | Very fast | **Very fast** (pyqtgraph engine) |
| Interactivity | Limited | Rich (pan/zoom) | **Rich** (built-in) |
| GPU acceleration | No | Yes (OpenGL) | **Yes** (inherited) |
| Auto-downsampling | No | Yes | **Yes** (automatic) |

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
plt.grid(True)
plt.legend()
plt.show()
```

## Features

### Line Plots
```python
plt.plot(x, y, 'r-', linewidth=2, label='Line')
plt.plot(x, y2, 'b--', marker='o', markersize=4)
```

### Scatter Plots
```python
plt.scatter(x, y, s=10, c='darkorange', alpha=0.5, marker='o')
```

### Bar Charts
```python
plt.bar(['A', 'B', 'C', 'D'], [23, 45, 12, 67], color='steelblue')
```

### Histograms
```python
plt.hist(data, bins=50, color='green', alpha=0.7)
```

### Subplots
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, np.sin(x), 'r-')
axes[0, 1].plot(x, np.cos(x), 'b-')
axes[1, 0].bar([0, 1, 2, 3], [10, 20, 15, 25])
axes[1, 1].hist(np.random.randn(5000), bins=30)
```

### Format Strings
Supports matplotlib-style format strings: `'r-o'`, `'b--'`, `'g.'`, `'k:'`, etc.

### Other Features
- `plt.title()`, `plt.xlabel()`, `plt.ylabel()`
- `plt.xlim()`, `plt.ylim()`, `plt.xscale('log')`
- `plt.grid()`, `plt.legend()`
- `plt.axhline()`, `plt.axvline()`, `plt.text()`
- `plt.errorbar()`, `plt.fill_between()`, `plt.imshow()`
- `plt.savefig()` for image export

## Installation

```bash
pip install pyqtgraph numpy
# Then either PyQt5, PyQt6, PySide2, or PySide6:
pip install PySide6
```

```bash
git clone https://github.com/CodeOfMe/ShenBi.git
cd ShenBi
pip install -e .
```

## Requirements

- Python >= 3.9
- pyqtgraph >= 0.13.0
- numpy >= 1.20
- Qt bindings: PyQt5, PyQt6, PySide2, or PySide6

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

## License

MIT
