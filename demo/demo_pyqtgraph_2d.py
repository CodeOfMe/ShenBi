"""
ShenBi — PyQtGraph 2D Demos Reimagined
========================================
Implements key pyqtgraph 2D examples using ShenBi's matplotlib-compatible API,
including: Plotting, ScatterPlot, BarGraphItem, ErrorBarItem, FillBetweenItem,
Symbols, ColorMaps, LinkedViews, LogAxis, MultiplePlotAxes, Histogram, InfiniteLine,
Isocurve, ImageView, PColorMesh, ScrollingPlots, MultiDataPlot, and more.

PNG + SVG output for each demo.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import numpy as np
import shenbi.pyplot as plt
from shenbi.cm import get_cmap

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

def save(name):
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    plt.savefig(os.path.join(OUT_DIR, name + '.svg'))
    print(f"  {name}.png + .svg")
    plt.close('all')

def save_png(name):
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    print(f"  {name}.png")
    plt.close('all')

N = 10_000

# ═══════════════════════════════════════════════════════════════════
#  1. SimplePlot — basic line plot (pyqtgraph SimplePlot.py)
# ═══════════════════════════════════════════════════════════════════
print("\n1. SimplePlot")
x = np.linspace(0, 4 * np.pi, N)
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'b--', linewidth=2, label='cos(x)')
plt.title('Simple Plot — sin(x) & cos(x)')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15); plt.legend()
save('pg01_simple_plot')

# ═══════════════════════════════════════════════════════════════════
#  2. Plotting — multiple line styles, markers, colors
# ═══════════════════════════════════════════════════════════════════
print("2. Plotting — Styles & Markers")
x = np.linspace(0, 10, 200)
plt.figure(figsize=(12, 6))
styles = [
    ('r-', 'solid'), ('b--', 'dashed'), ('g-.', 'dash-dot'),
    ('k:', 'dotted'), ('mo-', 'circle+line'), ('c^--', 'triangle'),
    ('ys-', 'square'), ('#e377c2D-', 'diamond'),
]
for i, (fmt, name) in enumerate(styles):
    plt.plot(x, np.sin(x - i*0.3) + i*0.5, fmt, linewidth=1.5, markersize=5, label=name)
plt.title('Line Styles, Markers & Colors')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15); plt.legend(fontsize=8)
save('pg02_plotting_styles')

# ═══════════════════════════════════════════════════════════════════
#  3. ScatterPlot — single color + colormap
# ═══════════════════════════════════════════════════════════════════
print("3. ScatterPlot")
np.random.seed(42)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Single color with alpha
n = 5000
sx = np.random.randn(n); sy = np.random.randn(n)
axes[0].scatter(sx, sy, s=6, c='steelblue', alpha=0.3, edgecolors='none')
axes[0].set_title(f'Scatter — Single Color ({n} pts)')
axes[0].grid(alpha=0.15)

# Colormap viridis
t = np.sqrt(sx*sx + sy*sy)
axes[1].scatter(sx, sy, s=8, c=t, cmap='viridis', alpha=0.5, edgecolors='none')
axes[1].set_title('Scatter — Viridis')
axes[1].grid(alpha=0.15)

# Colormap plasma with black edges
axes[2].scatter(sx[:1000], sy[:1000], s=15, c=t[:1000], cmap='plasma',
                 edgecolors='#333', linewidths=0.5, alpha=0.8)
axes[2].set_title('Scatter — Plasma + Edges')
axes[2].grid(alpha=0.15)
plt.tight_layout()
save('pg03_scatter_plots')

# ═══════════════════════════════════════════════════════════════════
#  4. ScatterPlotSpeedTest — 100K pts
# ═══════════════════════════════════════════════════════════════════
print("4. ScatterPlotSpeed — 100K pts")
sx = np.random.randn(100_000); sy = np.random.randn(100_000)
t = np.sqrt(sx*sx + sy*sy)
plt.figure(figsize=(8, 8))
plt.scatter(sx, sy, s=2, c='#1f77b4', alpha=0.15, edgecolors='none')
plt.title('Scatter (100,000 pts) — High Performance')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.10)
save_png('pg04_scatter_100k')

# ═══════════════════════════════════════════════════════════════════
#  5. BarGraphItem — multi-color bar chart
# ═══════════════════════════════════════════════════════════════════
print("5. BarGraphItem")
categories = ['Apples', 'Oranges', 'Bananas', 'Grapes', 'Melons', 'Kiwi', 'Mango', 'Peach']
values = np.random.randint(15, 80, len(categories))
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#17becf']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].bar(range(len(categories)), values, color=bar_colors, edgecolor='#333', linewidth=1)
axes[0].set_xticks(range(len(categories))); axes[0].set_xticklabels(categories, rotation=45)
axes[0].set_title('Bar Chart — Multi Color')
axes[0].set_ylabel('Sales'); axes[0].grid(axis='y', alpha=0.15)

axes[1].barh(range(len(categories)), values, color=bar_colors, edgecolor='#333', linewidth=1)
axes[1].set_yticks(range(len(categories))); axes[1].set_yticklabels(categories)
axes[1].set_title('Horizontal Bar Chart')
axes[1].set_xlabel('Sales'); axes[1].grid(axis='x', alpha=0.15)
plt.tight_layout()
save('pg05_bar_graphs')

# ═══════════════════════════════════════════════════════════════════
#  6. ErrorBarItem
# ═══════════════════════════════════════════════════════════════════
print("6. ErrorBarItem")
x = np.linspace(0, 10, 30)
y = np.sin(x) + np.random.normal(0, 0.1, 30)
yerr = 0.15 + 0.1 * np.random.rand(30)
plt.figure(figsize=(10, 5))
plt.errorbar(x, y, yerr=yerr, fmt='ro-', capsize=4, markersize=6,
             label='Measured', ecolor='gray')
plt.plot(x, np.sin(x), 'b-', alpha=0.4, linewidth=1.5, label='True sin(x)')
plt.title('Error Bar Plot')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15); plt.legend()
save('pg06_errorbar')

# ═══════════════════════════════════════════════════════════════════
#  7. FillBetweenItem
# ═══════════════════════════════════════════════════════════════════
print("7. FillBetweenItem")
x = np.linspace(0, 10, N)
y1 = np.sin(x); y2 = np.sin(x) + 0.6
plt.figure(figsize=(10, 5))
plt.fill_between(x, y1, y2, alpha=0.3, color='#1f77b4', label='Fill Region')
plt.plot(x, y1, '#1f77b4', linewidth=1, label='Lower')
plt.plot(x, y2, '#1f77b4', linewidth=1, label='Upper')
plt.title('Fill Between Curves')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15); plt.legend()
save('pg07_fill_between')

# ═══════════════════════════════════════════════════════════════════
#  8. Symbols — all marker types
# ═══════════════════════════════════════════════════════════════════
print("8. Symbols / Marker Types")
markers = ['o', 's', '^', 'v', 'D', 'p', 'h', '*', '+', 'x']
from shenbi.colors import TAB10_COLORS
x_sub = np.linspace(0, 1, 20)

plt.figure(figsize=(12, 8))
for i, mk in enumerate(markers):
    plt.plot(x_sub, np.sin(x_sub * 2 * np.pi * (i+1)),
             marker=mk, linestyle='-', color=TAB10_COLORS[i % 10],
             markersize=8, linewidth=1.5, label=f"'{mk}'")
plt.title('All Marker Types')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15); plt.legend(loc='lower left', fontsize=8, ncol=2)
save('pg08_symbols')

# ═══════════════════════════════════════════════════════════════════
#  9. ColorMaps — scatter + imshow demos
# ═══════════════════════════════════════════════════════════════════
print("9. ColorMaps")
cmap_names = ['viridis', 'plasma', 'inferno', 'magma', 'jet', 'cool', 'hot', 'coolwarm']
np.random.seed(0)
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes_flat = axes.flatten()
sx, sy = np.random.randn(800), np.random.randn(800)
t_vals = np.sqrt(sx*sx + sy*sy)
for idx, cname in enumerate(cmap_names):
    ax = axes_flat[idx]
    ax.scatter(sx, sy, s=8, c=t_vals, cmap=cname, alpha=0.6, edgecolors='none')
    ax.set_title(cname)
    ax.grid(alpha=0.10)
plt.tight_layout()
save('pg09_colormaps')

# ═══════════════════════════════════════════════════════════════════
#  10. LogAxis — semilogx, semilogy, loglog
# ═══════════════════════════════════════════════════════════════════
print("10. LogAxis / Log Plots")
x = np.logspace(0, 3, N)
y = x**1.5 + np.random.randn(N) * x * 0.3

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].loglog(x, y, 'b.', markersize=1, alpha=0.3)
axes[0].set_title('loglog'); axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
axes[0].grid(alpha=0.15)

axes[1].semilogy(x, y, 'r.', markersize=1, alpha=0.3)
axes[1].set_title('semilogy'); axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
axes[1].grid(alpha=0.15)

axes[2].semilogx(x, y, 'g.', markersize=1, alpha=0.3)
axes[2].set_title('semilogx'); axes[2].set_xlabel('x'); axes[2].set_ylabel('y')
axes[2].grid(alpha=0.15)
plt.tight_layout()
save('pg10_log_axes')

# ═══════════════════════════════════════════════════════════════════
#  11. MultiplePlotAxes — twinx, twiny
# ═══════════════════════════════════════════════════════════════════
print("11. MultiplePlotAxes — twinx")
x = np.linspace(0, 10, N)
plt.figure(figsize=(10, 6))
ax1 = plt.gca()
ax1.plot(x, np.sin(x), 'b-', linewidth=1.5, label='sin(x)')
ax1.set_xlabel('x'); ax1.set_ylabel('sin(x)', color='b')
ax1.grid(alpha=0.15)

ax2 = ax1.twinx()
ax2.plot(x, np.exp(x**0.3) - 1, 'r--', linewidth=1.5, label='exp growth')
ax2.set_ylabel('growth', color='r')
plt.title('Multiple Axes — twinx()')
plt.tight_layout()
save('pg11_twin_axes')

# ═══════════════════════════════════════════════════════════════════
#  12. Histogram
# ═══════════════════════════════════════════════════════════════════
print("12. Histogram")
data1 = np.random.randn(N); data2 = np.random.randn(N) * 0.8 + 2

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].hist(data1, bins=60, color='#2ca02c', alpha=0.7, edgecolor='white', linewidth=0.3)
axes[0].set_title(f'Histogram ({N:,} pts)')

x = data2[data2 > 0]
axes[1].hist(x, bins=50, color='#d62728', alpha=0.6, edgecolor='white', linewidth=0.3)
axes[1].set_title('Histogram (shifted)')
plt.tight_layout()
save('pg12_histogram')

# ═══════════════════════════════════════════════════════════════════
#  13. InfiniteLine — axhline / axvline
# ═══════════════════════════════════════════════════════════════════
print("13. InfiniteLine (axhline / axvline)")
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), 'b-', linewidth=1.5)
for y_val in [-0.75, -0.5, 0, 0.5, 0.75]:
    plt.axhline(y=y_val, color='gray' if y_val != 0 else 'red',
                linestyle='--' if y_val != 0 else '-', alpha=0.4 if y_val != 0 else 0.8)
plt.axvline(x=np.pi, color='green', linestyle=':', linewidth=2)
plt.axvline(x=2*np.pi, color='green', linestyle=':', linewidth=2)
plt.title('Reference Lines (axhline / axvline)')
plt.xlabel('x'); plt.ylabel('sin(x)')
plt.grid(alpha=0.15)
save('pg13_infinite_lines')

# ═══════════════════════════════════════════════════════════════════
#  14. LinkedViews — subplots with shared axes
# ═══════════════════════════════════════════════════════════════════
print("14. LinkedViews / Shared Axes")
x = np.linspace(0, 4 * np.pi, N)
fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
axes[0].plot(x, np.sin(x), 'r-', linewidth=1); axes[0].set_ylabel('sin(x)'); axes[0].grid(alpha=0.15)
axes[1].plot(x, np.cos(x), 'b-', linewidth=1); axes[1].set_ylabel('cos(x)'); axes[1].grid(alpha=0.15)
axes[2].plot(x, np.sin(x) * np.cos(x), 'g-', linewidth=1); axes[2].set_ylabel('sin·cos')
axes[2].set_xlabel('x'); axes[2].grid(alpha=0.15)
plt.tight_layout()
save('pg14_linked_views')

# ═══════════════════════════════════════════════════════════════════
#  15. ImageView — imshow with various styles
# ═══════════════════════════════════════════════════════════════════
print("15. ImageView / imshow")
img = np.random.rand(200, 200)
img_smooth = np.sin(np.linspace(0, 4*np.pi, 200)).reshape(-1, 1) * \
             np.cos(np.linspace(0, 4*np.pi, 200)).reshape(1, -1)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].imshow(img, aspect='auto', vmin=0, vmax=1)
axes[0].set_title('Random Image')
axes[1].imshow(img_smooth, aspect='auto', extent=[0, 4*np.pi, 0, 4*np.pi])
axes[1].set_title('Sinusoidal Pattern')
plt.tight_layout()
save('pg15_image_view')

# ═══════════════════════════════════════════════════════════════════
#  16. Isocurve — contour via filled regions
# ═══════════════════════════════════════════════════════════════════
print("16. Isocurve / Contour Style")
x = np.linspace(0, 4 * np.pi, 500)
y1 = np.sin(x); y2 = np.cos(x)
plt.figure(figsize=(10, 5))
for i in range(5):
    offset = i * 0.8
    plt.fill_between(x, y1 - offset, y2 + offset, alpha=0.08, color='steelblue')
plt.plot(x, y1, 'r-', linewidth=1, label='sin(x)')
plt.plot(x, y2, 'b-', linewidth=1, label='cos(x)')
plt.title('Isocurve-Style Fill')
plt.xlabel('x'); plt.grid(alpha=0.15); plt.legend()
save('pg16_isocurve')

# ═══════════════════════════════════════════════════════════════════
#  17. MultiDataPlot — many lines on one plot
# ═══════════════════════════════════════════════════════════════════
print("17. MultiDataPlot — 20 lines")
x = np.linspace(0, 10, N)
plt.figure(figsize=(12, 6))
for i in range(20):
    plt.plot(x, np.sin(x + i * 0.3) + i * 0.5, linewidth=0.8, alpha=0.7)
plt.title('Multi-Data Plot (20 lines)')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.10)
save('pg17_multi_data')

# ═══════════════════════════════════════════════════════════════════
#  18. Stemplot & Step
# ═══════════════════════════════════════════════════════════════════
print("18. Stem & Step")
x = np.linspace(0, 2*np.pi, 30)
y = np.exp(-0.1*x) * np.sin(x)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].stem(x, y, linefmt='C0-', markerfmt='C0o', basefmt='C3-')
axes[0].set_title('Stem Plot'); axes[0].grid(alpha=0.15)
axes[1].step(x, y, where='mid', label='steps-mid')
axes[1].step(x, y, where='post', linewidth=0.5, alpha=0.5, label='steps-post')
axes[1].set_title('Step Plot'); axes[1].grid(alpha=0.15); axes[1].legend()
plt.tight_layout()
save('pg18_stem_step')

# ═══════════════════════════════════════════════════════════════════
#  19. Boxplot
# ═══════════════════════════════════════════════════════════════════
print("19. Boxplot")
data = [np.random.randn(150) * (i+1) + i*8 for i in range(6)]
plt.figure(figsize=(10, 6))
plt.boxplot(data, tick_labels=['A', 'B', 'C', 'D', 'E', 'F'])
plt.title('Box Plot — 6 Groups')
plt.xlabel('Group'); plt.ylabel('Value')
plt.grid(axis='y', alpha=0.15)
save('pg19_boxplot')

# ═══════════════════════════════════════════════════════════════════
#  20. Pie
# ═══════════════════════════════════════════════════════════════════
print("20. Pie")
sizes = [22, 18, 35, 15, 10]
labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Other']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, startangle=140)
plt.title('Pie Chart — Product Distribution')
save('pg20_pie')

print(f"\n{'='*60}")
print("  PyQtGraph 2D Demos Complete! (20 demos)")
print(f"  Output: {OUT_DIR}/")
print(f"{'='*60}")
