"""
ShenBi — PyQtGraph 3D GL Demos Reimagined
===========================================
Implements key pyqtgraph OpenGL demos using ShenBi's mplot3d API:
- GLSurfacePlot → plot_surface
- GLScatterPlot → scatter3D
- GLLinePlot → plot3D
- GLMeshItem → plot_wireframe / plot_trisurf
- GLVolumeItem → volume
- GLBarGraphItem → bar3d
- GLIsosurface → contour3D
- GLGridItem / GLAxisItem → built-in

Output: PNG screenshots only (3D SVGs not supported by GL).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from PySide6 import QtWidgets

app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)

from shenbi import mplot3d
from shenbi.colors import TAB10_COLORS

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

def save_3d(ax, name):
    """Save a 3D view to PNG."""
    ax.gl_view.setGeometry(0, 0, 800, 600)
    ax.gl_view.show()
    app.processEvents()
    import time
    time.sleep(0.3)
    app.processEvents()
    fname = os.path.join(OUT_DIR, name + '.png')
    pixmap = ax.gl_view.grab()
    pixmap.save(fname)
    print(f"  {name}.png")
    ax.gl_view.hide()

# ═══════════════════════════════════════════════════════════════════
#  1. GLSurfacePlot — surface plot
# ═══════════════════════════════════════════════════════════════════
print("\n1. Surface Plot (GLSurfacePlot)")
x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2) + 1e-10
Z = np.sin(R) / R

ax1 = mplot3d.Axes3D(azim=-50, elev=30)
ax1.plot_surface(X, Y, Z, color='steelblue', alpha=0.8, shade=True)
ax1.view_init(elev=30, azim=-50)
save_3d(ax1, 'gl01_surface')

# ═══════════════════════════════════════════════════════════════════
#  2. Wireframe plot
# ═══════════════════════════════════════════════════════════════════
print("2. Wireframe Plot")
ax2 = mplot3d.Axes3D(azim=-45, elev=35)
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
ax2.plot_wireframe(X, Y, Z, color='navy', rstride=1, cstride=1, alpha=0.6)
ax2.view_init(elev=35, azim=-45)
save_3d(ax2, 'gl02_wireframe')

# ═══════════════════════════════════════════════════════════════════
#  3. Scatter3D — colored 3D scatter
# ═══════════════════════════════════════════════════════════════════
print("3. Scatter3D (GLScatterPlot)")
np.random.seed(42)
n_pts = 2000
xs = np.random.randn(n_pts) * 2
ys = np.random.randn(n_pts) * 2
zs = np.random.randn(n_pts) * 2
colors_pts = [TAB10_COLORS[i % 10] for i in range(n_pts)]

ax3 = mplot3d.Axes3D(azim=-60, elev=25)
ax3.scatter3D(xs, ys, zs, s=8, c='#1f77b4', alpha=0.6)
ax3.view_init(elev=25, azim=-60)
save_3d(ax3, 'gl03_scatter3d')

# ═══════════════════════════════════════════════════════════════════
#  4. Plot3D — 3D line / curve
# ═══════════════════════════════════════════════════════════════════
print("4. Plot3D (GLLinePlot)")
t = np.linspace(0, 8 * np.pi, 2000)
x_line = np.sin(t)
y_line = np.cos(t * 1.3)
z_line = t / 10

ax4 = mplot3d.Axes3D(azim=-55, elev=30)
ax4.plot3D(x_line, y_line, z_line, color='#d62728', linewidth=3)
ax4.view_init(elev=30, azim=-55)
save_3d(ax4, 'gl04_line3d')

# ═══════════════════════════════════════════════════════════════════
#  5. Bar3D — 3D bars
# ═══════════════════════════════════════════════════════════════════
print("5. Bar3D (GLBarGraph)")
x_bar = np.array([0, 1, 2, 3, 4, 5, 6, 7])
y_bar = np.array([0, 0, 0, 0, 0, 0, 0, 0])
z_bar = np.random.randint(1, 10, len(x_bar))

ax5 = mplot3d.Axes3D(azim=-45, elev=35)
ax5.bar3d(x_bar, y_bar, z_bar, dx=0.7, dy=0.7, dz=z_bar, color=z_bar)
ax5.view_init(elev=35, azim=-45)
save_3d(ax5, 'gl05_bar3d')

# ═══════════════════════════════════════════════════════════════════
#  6. Volume — 3D volume rendering
# ═══════════════════════════════════════════════════════════════════
print("6. Volume (GLVolume)")
try:
    # Create 3D scalar field (density blob)
    x = np.linspace(-2, 2, 60)
    y = np.linspace(-2, 2, 60)
    z = np.linspace(-2, 2, 60)
    X, Y, Z = np.meshgrid(x, y, z)
    vol_data = np.exp(-(X**2 + Y**2 + Z**2) / 1.5)
    # Add some noise structure
    vol_data += 0.1 * np.sin(X * 3) * np.sin(Y * 3) * np.sin(Z * 3)
    vol_data = np.clip(vol_data, 0, 1)

    ax6 = mplot3d.Axes3D(azim=-50, elev=25)
    ax6.volume(vol_data, sliceDensity=256, smooth=True)
    ax6.view_init(elev=25, azim=-50)
    save_3d(ax6, 'gl06_volume')
except Exception as e:
    print(f"  Volume rendering skipped: {e}")

# ═══════════════════════════════════════════════════════════════════
#  7. Multi-surface — multiple surfaces
# ═══════════════════════════════════════════════════════════════════
print("7. Multiple Surfaces")
x = np.linspace(-5, 5, 80)
y = np.linspace(-5, 5, 80)
X, Y = np.meshgrid(x, y)
Z1 = np.sin(np.sqrt(X**2 + Y**2))
Z2 = np.cos(np.sqrt(X**2 + Y**2) * 0.7) - 2

ax7 = mplot3d.Axes3D(azim=-40, elev=20)
ax7.plot_surface(X, Y, Z1, color='steelblue', alpha=0.7, shade=True)
ax7.plot_surface(X, Y, Z2, color='coral', alpha=0.7, shade=True)
ax7.view_init(elev=20, azim=-40)
save_3d(ax7, 'gl07_multi_surface')

# ═══════════════════════════════════════════════════════════════════
#  8. Tricontour / Mesh from random points
# ═══════════════════════════════════════════════════════════════════
print("8. Tri Surface (trisurf)")
np.random.seed(42)
n = 300
pts_x = np.random.uniform(-3, 3, n)
pts_y = np.random.uniform(-3, 3, n)
pts_z = np.sin(np.sqrt(pts_x**2 + pts_y**2) * 1.5)

ax8 = mplot3d.Axes3D(azim=-50, elev=30)
try:
    ax8.plot_trisurf(pts_x, pts_y, pts_z, color='forestgreen', alpha=0.8, shade=True)
except Exception as e:
    print(f"  Trisurf skipped (scipy needed): {e}")
    ax8.scatter3D(pts_x[::3], pts_y[::3], pts_z[::3], s=15, c='forestgreen', alpha=0.7)
ax8.view_init(elev=30, azim=-50)
save_3d(ax8, 'gl08_trisurf')

# ═══════════════════════════════════════════════════════════════════
#  9. Parametric curve
# ═══════════════════════════════════════════════════════════════════
print("9. Parametric Curves")
t = np.linspace(0, 20 * np.pi, 3000)
ax9 = mplot3d.Axes3D(azim=-60, elev=25)
# Toroidal helix
r = 2
w = 1
x_h = (r + w * np.cos(t * 3)) * np.cos(t)
y_h = (r + w * np.cos(t * 3)) * np.sin(t)
z_h = w * np.sin(t * 3)
ax9.plot3D(x_h, y_h, z_h, color='coral', linewidth=2)
# Add a second thinner curve
x_h2 = (r + 0.5 * w * np.cos(t * 5)) * np.cos(t * 0.7)
y_h2 = (r + 0.5 * w * np.cos(t * 5)) * np.sin(t * 0.7)
z_h2 = w * np.sin(t * 5) + 0.5
ax9.plot3D(x_h2, y_h2, z_h2, color='steelblue', linewidth=1, alpha=0.5)
ax9.view_init(elev=25, azim=-60)
save_3d(ax9, 'gl09_parametric')

# ═══════════════════════════════════════════════════════════════════
#  10. 3D Bar Chart — grid of bars
# ═══════════════════════════════════════════════════════════════════
print("10. 3D Bar Grid")
nx, nz = 8, 5
heights = np.random.randint(2, 12, (nx, nz))

ax10 = mplot3d.Axes3D(azim=-45, elev=40)
x_positions = np.arange(nx)
z_positions = np.arange(nz)
colors_grid = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
               '#8c564b', '#e377c2', '#17becf']

for i in range(nx):
    for j in range(nz):
        ax10.bar3d(x_positions[i], j, 0, dx=0.6, dy=0.6, dz=heights[i, j],
                    color=colors_grid[i % len(colors_grid)], shade=True)
ax10.view_init(elev=40, azim=-45)
save_3d(ax10, 'gl10_bar_grid')

print(f"\n{'='*60}")
print("  PyQtGraph 3D GL Demos Complete! (10 demos)")
print(f"  Output: {OUT_DIR}/")
print(f"{'='*60}")
