"""
ShenBi (神笔) - Comprehensive Feature Demo
==========================================
Tests ALL visual elements: markers, labels, alpha, colors, colormaps,
grid, legend, format strings, Line2D API, etc.

Compatible with both matplotlib and shenbi — just switch the import.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import numpy as np

# === SWITCH IMPORT HERE TO COMPARE ===
# import matplotlib.pyplot as plt
import shenbi.pyplot as plt

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

N = 10_000

def save(name):
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    plt.savefig(os.path.join(OUT_DIR, name + '.svg'))
    print(f"  {name}.png + .svg")
    plt.close('all')

def save_png_only(name):
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    print(f"  {name}.png")
    plt.close('all')

def header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════════
#  1. LINE PLOTS — colors, linewidths, linestyles
# ═══════════════════════════════════════════════════════════════
header("1. Line Plots")
x = np.linspace(0, 4 * np.pi, N)
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'b--', linewidth=1.5, label='cos(x)')
plt.plot(x, np.sin(x)*np.exp(-x/10), 'g-.', linewidth=1, label='damped')
plt.title('Line Plots — Colors, Linestyles, Linewidths')
plt.xlabel('x'); plt.ylabel('y')
plt.legend(loc='upper right')
save('01_line')

# Multi-dataset in one call
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'r-', x, np.cos(x), 'b--')
plt.title('Multiple Datasets in One plot()')
save('01b_multi')

# ═══════════════════════════════════════════════════════════════
#  2. MARKERS — all marker types
# ═══════════════════════════════════════════════════════════════
header("2. Markers")
x_sub = x[::200]
plt.figure(figsize=(10, 5))
markers = ['o', 's', '^', 'v', 'D', '+', 'x', '*', 'p', 'h']
colors_mk = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
             '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
for i, mk in enumerate(markers):
    offset = i * 0.3
    plt.plot(x_sub, np.sin(x_sub) + offset, marker=mk, linestyle='none',
             markersize=8, color=colors_mk[i], label=mk)
plt.title('All Marker Types')
plt.xlabel('x'); plt.ylabel('y')
plt.legend(loc='upper right', fontsize=7)
save('02_markers')

# ═══════════════════════════════════════════════════════════════
#  3. SCATTER — single color, alpha, colormap
# ═══════════════════════════════════════════════════════════════
header("3. Scatter")

# Basic scatter with alpha
np.random.seed(42)
sx, sy = np.random.randn(N), np.random.randn(N)
plt.figure(figsize=(8, 8))
plt.scatter(sx, sy, s=10, c='steelblue', alpha=0.3, edgecolors='none')
plt.title(f'Scatter — Single Color, alpha=0.3 ({N:,} pts)')
plt.xlabel('x'); plt.ylabel('y')
save('03a_scatter_basic')

# Scatter with colormap
plt.figure(figsize=(8, 8))
t = np.sqrt(sx**2 + sy**2)
plt.scatter(sx, sy, s=8, c=t, cmap='plasma', alpha=0.7, edgecolors='none')
plt.title('Scatter — Plasma Colormap')
plt.xlabel('x'); plt.ylabel('y')
save('03b_scatter_cmap_plasma')

# Scatter with viridis colormap
plt.figure(figsize=(8, 8))
idx = np.arange(N) / N
plt.scatter(sx, sy, s=6, c=idx, cmap='viridis', alpha=0.5, edgecolors='none')
plt.title('Scatter — Viridis Colormap')
plt.xlabel('x'); plt.ylabel('y')
save('03c_scatter_cmap_viridis')

# Scatter with jet colormap + edge color
plt.figure(figsize=(8, 8))
plt.scatter(sx[:3000], sy[:3000], s=20, c=idx[:3000], cmap='cool',
            edgecolors='black', linewidths=0.5, alpha=0.8)
plt.title('Scatter — Cool Colormap + Black Edges')
plt.xlabel('x'); plt.ylabel('y')
save('03d_scatter_cmap_cool')

# Large scatter (100K) — PNG only
sx2, sy2 = np.random.randn(100_000), np.random.randn(100_000)
plt.figure(figsize=(8, 8))
plt.scatter(sx2, sy2, s=2, c='#1f77b4', alpha=0.15, edgecolors='none')
plt.title('Scatter (100K pts)')
plt.xlabel('x'); plt.ylabel('y')
save_png_only('03e_scatter_100k')

# ═══════════════════════════════════════════════════════════════
#  4. BAR — colors, edgecolor, labels
# ═══════════════════════════════════════════════════════════════
header("4. Bar")
cats = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
vals = np.random.randint(10, 100, len(cats))
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#17becf']

plt.figure(figsize=(10, 5))
plt.bar(range(len(cats)), vals, color=bar_colors, edgecolor='#333333', linewidth=1)
plt.xticks(range(len(cats)), cats)
plt.title('Bar Chart — Multiple Colors + Edge Color')
plt.xlabel('Category'); plt.ylabel('Value')
plt.grid(axis='y', alpha=0.15)
save('04_bar')

plt.figure(figsize=(10, 5))
plt.barh(range(len(cats)), vals, color=bar_colors, edgecolor='#333333', linewidth=1)
plt.yticks(range(len(cats)), cats)
plt.title('Horizontal Bar Chart')
plt.xlabel('Value')
plt.grid(axis='x', alpha=0.15)
save('04b_barh')

# ═══════════════════════════════════════════════════════════════
#  5. HISTOGRAM — color, alpha, density, edge color
# ═══════════════════════════════════════════════════════════════
header("5. Histogram")
data = np.random.randn(N)
plt.figure(figsize=(10, 5))
plt.hist(data, bins=50, color='#2ca02c', alpha=0.7, edgecolor='white', linewidth=0.5)
plt.title(f'Histogram ({N:,} pts) — Color, Alpha, Edge')
plt.xlabel('Value'); plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.15)
save('05_hist')

plt.figure(figsize=(10, 5))
plt.hist(data, bins=50, density=True, color='#9467bd', alpha=0.5, edgecolor='white', linewidth=0.5)
plt.title('Histogram — Density')
plt.xlabel('Value'); plt.ylabel('Density')
plt.grid(axis='y', alpha=0.15)
save('05b_hist_density')

# ═══════════════════════════════════════════════════════════════
#  6. ERRORBAR — color, marker, capsize
# ═══════════════════════════════════════════════════════════════
header("6. Errorbar")
xe = np.linspace(0, 10, 25)
ye = np.sin(xe)
yerr = 0.1 + 0.2 * np.random.rand(25)
plt.figure(figsize=(10, 5))
plt.errorbar(xe, ye, yerr=yerr, fmt='ro-', capsize=5, markersize=6, label='measured')
plt.plot(xe, np.sin(xe), 'b-', alpha=0.3, linewidth=1, label='true')
plt.title('Error Bar Plot')
plt.xlabel('x'); plt.ylabel('y')
plt.legend()
plt.grid(alpha=0.15)
save('06_errorbar')

# ═══════════════════════════════════════════════════════════════
#  7. FILL_BETWEEN — alpha, color
# ═══════════════════════════════════════════════════════════════
header("7. Fill Between")
x = np.linspace(0, 10, N)
y1 = np.sin(x)
y2 = np.sin(x) + 0.5
plt.figure(figsize=(10, 5))
plt.fill_between(x, y1, y2, alpha=0.3, color='#1f77b4', label='fill')
plt.plot(x, y1, '#1f77b4', linewidth=1)
plt.plot(x, y2, '#1f77b4', linewidth=1)
plt.title('Fill Between — Alpha, Color')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15)
plt.legend()
save('07_fill_between')

# ═══════════════════════════════════════════════════════════════
#  8. IMSHOW — with colormaps
# ═══════════════════════════════════════════════════════════════
header("8. Image (imshow)")
img_data = np.random.rand(100, 100)
plt.figure(figsize=(7, 6))
plt.imshow(img_data, aspect='auto', vmin=0, vmax=1, extent=[0, 10, 0, 10])
plt.title('Image (imshow) — Default')
plt.xlabel('x'); plt.ylabel('y')
save('08_imshow')

# ═══════════════════════════════════════════════════════════════
#  9. TEXT & ANNOTATE
# ═══════════════════════════════════════════════════════════════
header("9. Text & Annotate")
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'b-', linewidth=1.5)
plt.text(2.5, 0.8, 'Peak', fontsize=12, color='red')
plt.annotate('Zero cross', xy=(np.pi, 0), xytext=(5, 0.4),
             arrowprops=dict(arrowstyle='->', color='green'))
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(x=np.pi, color='gray', linestyle='--', alpha=0.5)
plt.title('Text & Annotations')
plt.xlabel('x'); plt.ylabel('sin(x)')
plt.grid(alpha=0.15)
save('09_text_annotate')

# ═══════════════════════════════════════════════════════════════
#  10. SUBPLOTS
# ═══════════════════════════════════════════════════════════════
header("10. Subplots")
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
x = np.linspace(0, 2 * np.pi, N)
axes[0,0].plot(x, np.sin(x), 'r-'); axes[0,0].set_title('sin(x)'); axes[0,0].grid(alpha=0.15)
axes[0,1].plot(x, np.cos(x), 'b-'); axes[0,1].set_title('cos(x)'); axes[0,1].grid(alpha=0.15)
axes[0,2].scatter(np.random.randn(200), np.random.randn(200), s=5, alpha=0.5)
axes[0,2].set_title('Scatter'); axes[0,2].grid(alpha=0.15)
axes[1,0].bar([0,1,2,3,4], [10,20,15,30,25], color='steelblue')
axes[1,0].set_title('Bar'); axes[1,0].grid(axis='y', alpha=0.15)
axes[1,1].hist(np.random.randn(5000), bins=30, color='green', alpha=0.7)
axes[1,1].set_title('Histogram'); axes[1,1].grid(alpha=0.15)
axes[1,2].fill_between(x, np.sin(x), alpha=0.3, color='blue')
axes[1,2].plot(x, np.sin(x), 'b-'); axes[1,2].set_title('Fill Between')
axes[1,2].grid(alpha=0.15)
plt.tight_layout()
save('10_subplots')

# ═══════════════════════════════════════════════════════════════
#  11. LOG SCALES
# ═══════════════════════════════════════════════════════════════
header("11. Log Scales")
x = np.logspace(0, 3, N)
y = x**2 + np.random.randn(N) * x * 0.5
plt.figure(figsize=(10, 5))
plt.loglog(x, y, 'b.', markersize=1, alpha=0.3)
plt.title('Log-Log Plot')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(True, which='both', alpha=0.15)
save('11_loglog')

plt.figure(figsize=(10, 5))
plt.semilogy(x, y, 'r.', markersize=1, alpha=0.3)
plt.title('Semi-Log Y')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(True, alpha=0.15)
save('11b_semilogy')

# ═══════════════════════════════════════════════════════════════
#  12. STEM
# ═══════════════════════════════════════════════════════════════
header("12. Stem")
x = np.linspace(0.1, 2*np.pi, 40)
y = np.exp(-0.1*x) * np.sin(x)
plt.figure(figsize=(10, 5))
plt.stem(x, y, linefmt='C0-', markerfmt='C0o', basefmt='C3-')
plt.title('Stem Plot')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15)
save('12_stem')

# ═══════════════════════════════════════════════════════════════
#  13. AXVLINE / AXHLINE — different colors, styles
# ═══════════════════════════════════════════════════════════════
header("13. Axhline / Axvline")
plt.figure(figsize=(10, 5))
plt.plot(np.linspace(0,10,100), np.sin(np.linspace(0,10,100)), 'b-')
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0.5, color='red', linestyle=':', linewidth=2)
plt.axvline(x=5, color='green', linestyle='-.', linewidth=2)
plt.title('axhline / axvline — Colors, Styles, Widths')
plt.grid(alpha=0.15)
save('13_axline')

# ═══════════════════════════════════════════════════════════════
#  14. BOXPLOT — colors, labels
# ═══════════════════════════════════════════════════════════════
header("14. Boxplot")
data = [np.random.randn(100)*(i+1)+i*5 for i in range(5)]
plt.figure(figsize=(10, 5))
plt.boxplot(data, tick_labels=['G1','G2','G3','G4','G5'])
plt.title('Boxplot — Labels')
plt.xlabel('Group'); plt.ylabel('Value')
plt.grid(axis='y', alpha=0.15)
save('14_boxplot')

# ═══════════════════════════════════════════════════════════════
#  15. FORMAT STRINGS — all matplotlib fmt combos
# ═══════════════════════════════════════════════════════════════
header("15. Format Strings")
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'r-', label="'r-' (red solid)")
plt.plot(x, np.cos(x), 'b--', label="'b--' (blue dashed)")
plt.plot(x, np.sin(x+1), 'g.', label="'g.' (green dots)")
plt.plot(x, np.sin(x+2), 'k:', label="'k:' (black dotted)")
plt.plot(x, np.sin(x+3), 'mo-', label="'mo-' (magenta circle+line)")
plt.plot(x, np.sin(x+4), 'c^--', label="'c^--' (cyan triangle+dash)")
plt.title('Format String Combinations')
plt.grid(alpha=0.15)
plt.legend(fontsize=8)
save('15_format_strings')

# ═══════════════════════════════════════════════════════════════
#  16. LINE2D API — set_color, set_linewidth, set_alpha, set_marker
# ═══════════════════════════════════════════════════════════════
header("16. Line2D API")
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 5))
lines = plt.plot(x, np.sin(x), 'b-', label='original')
line = lines[0]
line.set_linewidth(3.0); line.set_linestyle('--')
line.set_color('r'); line.set_label('modified')
line.set_alpha(0.7)
line.set_marker('s'); line.set_markersize(5)
plt.title('Line2D — set_color, set_linewidth, set_marker, set_alpha')
plt.grid(alpha=0.15); plt.legend()
save('16_line2d_api')

# ═══════════════════════════════════════════════════════════════
#  17. PIE — colors, labels
# ═══════════════════════════════════════════════════════════════
header("17. Pie")
sizes = [15, 30, 45, 10]
labels = ['A', 'B', 'C', 'D']
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, colors=colors, startangle=90)
plt.title('Pie Chart — Colors, Labels')
save('17_pie')

# ═══════════════════════════════════════════════════════════════
#  18. COLORMAPS — scatter with all major cmaps
# ═══════════════════════════════════════════════════════════════
header("18. Colormaps")
cmap_names = ['viridis', 'plasma', 'inferno', 'magma', 'jet', 'cool', 'hot']
np.random.seed(42)
sx, sy = np.random.randn(500), np.random.randn(500)
t = np.sqrt(sx**2 + sy**2)

from shenbi.cm import get_cmap

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
cmap_list = ['viridis', 'plasma', 'inferno', 'magma', 'jet', 'cool', 'hot', 'coolwarm']
for idx, cname in enumerate(cmap_list):
    row, col = idx // 4, idx % 4
    ax = axes[row][col] if hasattr(axes, '__getitem__') else axes
    if hasattr(axes, '__len__'):
        ax = axes[row][col] if isinstance(axes[0], list) or hasattr(axes[0], '__getitem__') else axes[idx]
    else:
        ax = axes
    ax.scatter(sx, sy, s=15, c=t, cmap=cname, alpha=0.7, edgecolors='none')
    ax.set_title(cname)
save('18_cmaps')

# ═══════════════════════════════════════════════════════════════
#  19. ALPHA — transparency demonstration
# ═══════════════════════════════════════════════════════════════
header("19. Alpha / Transparency")
x = np.linspace(0, 10, 200)
plt.figure(figsize=(10, 5))
for i in range(5):
    alpha = 0.15 + i * 0.18
    plt.fill_between(x, np.sin(x + i * 0.5), alpha=alpha,
                     color='#1f77b4', label=f'alpha={alpha:.2f}')
plt.title('Alpha / Transparency Demo')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(alpha=0.15)
plt.legend(fontsize=8)
save('19_alpha')

# ═══════════════════════════════════════════════════════════════
#  20. NAMED COLORS + HEX COLORS
# ═══════════════════════════════════════════════════════════════
header("20. Named & Hex Colors")
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 5))
colors_demo = [
    ('steelblue', '-'), ('darkorange', '--'), ('crimson', '-.'),
    ('#2ca02c', ':'), ('#9467bd', 'o-'), ('forestgreen', 's--')
]
for color_name, ls in colors_demo:
    plt.plot(x, np.sin(x + len(ls)), ls, color=color_name, label=color_name, linewidth=1.5)
plt.title('Named & Hex Colors')
plt.grid(alpha=0.15)
plt.legend(fontsize=8)
save('20_colors')

print(f"\n{'='*60}")
print(f"  Done! {N:,} points per test. PNG + SVG for each.")
print(f"  Output: {OUT_DIR}/")
print(f"{'='*60}")