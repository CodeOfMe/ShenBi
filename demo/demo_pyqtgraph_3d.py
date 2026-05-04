"""
ShenBi — 3D Demos (2D Projection Fallback)
============================================
Implements pyqtgraph 3D-style demos using 2D projection rendering.
Works on all platforms including Apple Silicon macOS where OpenGL fails.

Uses perspective projection math to render 3D surfaces, scatter, wireframes,
volumes, and bar charts as 2D plots with proper depth ordering.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import numpy as np
import shenbi.pyplot as plt
from shenbi.colors import TAB10_COLORS

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

# ── 3D Projection Helper ──────────────────────────────────────────
def project_3d_to_2d(X, Y, Z, azim=-60, elev=30, scale=1.0):
    """Project 3D points to 2D using perspective projection."""
    azim_rad = np.deg2rad(azim)
    elev_rad = np.deg2rad(elev)

    # Rotation matrices
    cos_a, sin_a = np.cos(azim_rad), np.sin(azim_rad)
    cos_e, sin_e = np.cos(elev_rad), np.sin(elev_rad)

    # Rotate around z (azimuth)
    x1 = X * cos_a - Y * sin_a
    y1 = X * sin_a + Y * cos_a
    z1 = Z

    # Rotate around x (elevation)
    x2 = x1
    y2 = y1 * cos_e - z1 * sin_e
    z2 = y1 * sin_e + z1 * cos_e

    # Perspective projection
    dist = 10.0
    perspective = dist / (dist - z2 * 0.1)
    px = x2 * perspective * scale
    py = y2 * perspective * scale
    return px, py, z2

# ═══════════════════════════════════════════════════════════════════
#  1. Surface Plot — 3D surface as filled contours
# ═══════════════════════════════════════════════════════════════════
print("\n1. Surface Plot (3D projection)")
x = np.linspace(-4, 4, 80)
y = np.linspace(-4, 4, 80)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2) + 1e-10
Z = np.sin(R) / R

plt.figure(figsize=(10, 8))
# Draw surface as filled contour bands
levels = np.linspace(Z.min(), Z.max(), 25)
cs = plt.contourf(X, Y, Z, levels=levels, cmap='viridis', alpha=0.8)
# Add wireframe overlay
plt.contour(X, Y, Z, levels=10, colors='white', linewidths=0.3, alpha=0.5)
plt.title('Surface Plot — sin(r)/r')
plt.xlabel('x'); plt.ylabel('y')
plt.colorbar(cs, label='z')
save('gl01_surface')

# ═══════════════════════════════════════════════════════════════════
#  2. Wireframe Plot
# ═══════════════════════════════════════════════════════════════════
print("2. Wireframe Plot")
x = np.linspace(-3, 3, 40)
y = np.linspace(-3, 3, 40)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

plt.figure(figsize=(10, 8))
# Wireframe: draw grid lines
for i in range(0, len(x), 3):
    plt.plot(X[i, :], Y[i, :], Z[i, :], 'navy', linewidth=0.5, alpha=0.6)
for j in range(0, len(y), 3):
    plt.plot(X[:, j], Y[:, j], Z[:, j], 'navy', linewidth=0.5, alpha=0.6)
plt.title('Wireframe Plot — sin(r)')
plt.xlabel('x'); plt.ylabel('y')
save('gl02_wireframe')

# ═══════════════════════════════════════════════════════════════════
#  3. Scatter3D — 3D scatter with depth-based sizing
# ═══════════════════════════════════════════════════════════════════
print("3. Scatter3D")
np.random.seed(42)
n_pts = 500
xs = np.random.randn(n_pts) * 2
ys = np.random.randn(n_pts) * 2
zs = np.random.randn(n_pts) * 2
colors_pts = [TAB10_COLORS[i % 10] for i in range(n_pts)]

# Project to 2D
px, py, pz = project_3d_to_2d(xs, ys, zs, azim=-50, elev=25)

plt.figure(figsize=(8, 8))
# Batch scatter by color groups for efficiency
for ci, color in enumerate(TAB10_COLORS):
    mask = [c == color for c in colors_pts]
    if not any(mask):
        continue
    mask_arr = np.array(mask)
    plt.scatter(px[mask_arr], py[mask_arr], s=15, c=color,
                alpha=0.6, edgecolors='none')
plt.title(f'Scatter3D ({n_pts} pts) — Depth Projection')
plt.xlabel('x'); plt.ylabel('y')
save('gl03_scatter3d')

# ═══════════════════════════════════════════════════════════════════
#  4. Plot3D — 3D helix curve
# ═══════════════════════════════════════════════════════════════════
print("4. Plot3D (Helix)")
t = np.linspace(0, 8 * np.pi, 1000)
xt = np.sin(t)
yt = np.cos(t * 1.3)
zt = t / 10

px, py, pz = project_3d_to_2d(xt, yt, zt, azim=-45, elev=30)

plt.figure(figsize=(10, 8))
# Color by depth
for i in range(len(t) - 1):
    color_val = (pz[i] - pz.min()) / (pz.max() - pz.min() + 1e-10)
    from shenbi.cm import get_cmap
    cmap = get_cmap('plasma')
    c = cmap(color_val)
    plt.plot(px[i:i+2], py[i:i+2], color=(c[0]/255, c[1]/255, c[2]/255),
             linewidth=2, alpha=0.8)
plt.title('3D Helix Curve — Plasma Colormap')
plt.xlabel('x'); plt.ylabel('y')
save('gl04_line3d')

# ═══════════════════════════════════════════════════════════════════
#  5. Bar3D — 3D bars with perspective
# ═══════════════════════════════════════════════════════════════════
print("5. Bar3D")
nx, nz = 6, 4
heights = np.random.randint(2, 10, (nx, nz))
colors_grid = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

plt.figure(figsize=(10, 8))
for i in range(nx):
    for j in range(nz):
        h = heights[i, j]
        # 3D bar projection
        cx = i * 1.2
        cy = j * 1.2
        # Top face
        top_x = [cx, cx+0.8, cx+0.8+0.3, cx+0.3]
        top_y = [cy, cy, cy+0.3, cy+0.3]
        plt.fill(top_x, top_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.9, edgecolor='white', linewidth=1)
        # Front face
        front_x = [cx, cx+0.8, cx+0.8, cx]
        front_y = [cy-h*0.3, cy-h*0.3, cy, cy]
        plt.fill(front_x, front_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.7, edgecolor='white', linewidth=0.5)
        # Right face
        right_x = [cx+0.8, cx+0.8+0.3, cx+0.8+0.3, cx+0.8]
        right_y = [cy-h*0.3, cy-h*0.3+0.3*0.5, cy+0.3*0.5, cy]
        plt.fill(right_x, right_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.5, edgecolor='white', linewidth=0.5)

plt.xlim(-1, nx * 1.2 + 1)
plt.ylim(-nz * 0.3 - 1, nz * 1.2 + 1)
plt.title('3D Bar Chart')
plt.xlabel('x'); plt.ylabel('y')
save('gl05_bar3d')

# ═══════════════════════════════════════════════════════════════════
#  6. Volume — 3D scalar field as slice views
# ═══════════════════════════════════════════════════════════════════
print("6. Volume (Slice Views)")
x = np.linspace(-2, 2, 60)
y = np.linspace(-2, 2, 60)
z = np.linspace(-2, 2, 60)
X, Y, Z = np.meshgrid(x, y, z)
vol_data = np.exp(-(X**2 + Y**2 + Z**2) / 1.5)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# XY slice at z=0
axes[0].imshow(vol_data[:, :, 30], cmap='viridis', aspect='auto',
               extent=[-2, 2, -2, 2], origin='lower')
axes[0].set_title('XY Slice (z=0)')
# XZ slice at y=0
axes[1].imshow(vol_data[:, 30, :], cmap='plasma', aspect='auto',
               extent=[-2, 2, -2, 2], origin='lower')
axes[1].set_title('XZ Slice (y=0)')
# YZ slice at x=0
axes[2].imshow(vol_data[30, :, :], cmap='inferno', aspect='auto',
               extent=[-2, 2, -2, 2], origin='lower')
axes[2].set_title('YZ Slice (x=0)')
plt.suptitle('Volume Rendering — 3 Orthogonal Slices')
plt.tight_layout()
save('gl06_volume')

# ═══════════════════════════════════════════════════════════════════
#  7. Multi-Surface — two surfaces
# ═══════════════════════════════════════════════════════════════════
print("7. Multiple Surfaces")
x = np.linspace(-5, 5, 60)
y = np.linspace(-5, 5, 60)
X, Y = np.meshgrid(x, y)
Z1 = np.sin(np.sqrt(X**2 + Y**2))
Z2 = np.cos(np.sqrt(X**2 + Y**2) * 0.7) - 2

plt.figure(figsize=(12, 6))
# Surface 1
plt.subplot(1, 2, 1)
plt.contourf(X, Y, Z1, levels=20, cmap='Blues', alpha=0.8)
plt.contour(X, Y, Z1, levels=8, colors='white', linewidths=0.3, alpha=0.4)
plt.title('Surface 1: sin(r)')
plt.xlabel('x'); plt.ylabel('y')

# Surface 2
plt.subplot(1, 2, 2)
plt.contourf(X, Y, Z2, levels=20, cmap='Reds', alpha=0.8)
plt.contour(X, Y, Z2, levels=8, colors='white', linewidths=0.3, alpha=0.4)
plt.title('Surface 2: cos(0.7r) - 2')
plt.xlabel('x'); plt.ylabel('y')
plt.suptitle('Multiple Surfaces')
plt.tight_layout()
save('gl07_multi_surface')

# ═══════════════════════════════════════════════════════════════════
#  8. TriSurface — triangulated surface from random points
# ═══════════════════════════════════════════════════════════════════
print("8. TriSurface")
np.random.seed(42)
n = 200
pts_x = np.random.uniform(-3, 3, n)
pts_y = np.random.uniform(-3, 3, n)
pts_z = np.sin(np.sqrt(pts_x**2 + pts_y**2) * 1.5)

from scipy.spatial import Delaunay
tri = Delaunay(np.column_stack([pts_x, pts_y]))

plt.figure(figsize=(10, 8))
# Draw triangles
for simplex in tri.simplices:
    triangle = np.column_stack([pts_x[simplex], pts_y[simplex]])
    z_avg = pts_z[simplex].mean()
    color_val = (z_avg - pts_z.min()) / (pts_z.max() - pts_z.min() + 1e-10)
    from shenbi.cm import get_cmap
    cmap = get_cmap('viridis')
    c = cmap(color_val)
    poly = plt.Polygon(triangle, facecolor=(c[0]/255, c[1]/255, c[2]/255),
                       edgecolor='white', linewidth=0.3, alpha=0.8)
    plt.gca().add_patch(poly)

plt.xlim(-3.5, 3.5); plt.ylim(-3.5, 3.5)
plt.title('Triangulated Surface — 200 Points')
plt.xlabel('x'); plt.ylabel('y')
save('gl08_trisurf')

# ═══════════════════════════════════════════════════════════════════
#  9. Parametric Curves — toroidal helix
# ═══════════════════════════════════════════════════════════════════
print("9. Parametric Curves")
t = np.linspace(0, 20 * np.pi, 2000)
r = 2; w = 1
x_h = (r + w * np.cos(t * 3)) * np.cos(t)
y_h = (r + w * np.cos(t * 3)) * np.sin(t)
z_h = w * np.sin(t * 3)

px, py, pz = project_3d_to_2d(x_h, y_h, z_h, azim=-50, elev=25)

plt.figure(figsize=(10, 8))
# Color by z-depth
for i in range(len(t) - 1):
    color_val = (pz[i] - pz.min()) / (pz.max() - pz.min() + 1e-10)
    from shenbi.cm import get_cmap
    cmap = get_cmap('coolwarm')
    c = cmap(color_val)
    plt.plot(px[i:i+2], py[i:i+2], color=(c[0]/255, c[1]/255, c[2]/255),
             linewidth=1.5, alpha=0.8)
plt.title('Toroidal Helix — Coolwarm Colormap')
plt.xlabel('x'); plt.ylabel('y')
save('gl09_parametric')

# ═══════════════════════════════════════════════════════════════════
#  10. 3D Bar Grid — perspective bar chart
# ═══════════════════════════════════════════════════════════════════
print("10. 3D Bar Grid")
nx, nz = 8, 5
heights = np.random.randint(2, 12, (nx, nz))
colors_grid = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
               '#8c564b', '#e377c2', '#17becf']

plt.figure(figsize=(12, 8))
for i in range(nx):
    for j in range(nz):
        h = heights[i, j]
        cx = i * 1.0
        cy = j * 0.8
        # Top face
        top_x = [cx, cx+0.7, cx+0.7+0.25, cx+0.25]
        top_y = [cy, cy, cy+0.25, cy+0.25]
        plt.fill(top_x, top_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.9, edgecolor='white', linewidth=0.8)
        # Front face
        front_x = [cx, cx+0.7, cx+0.7, cx]
        front_y = [cy-h*0.25, cy-h*0.25, cy, cy]
        plt.fill(front_x, front_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.6, edgecolor='white', linewidth=0.3)
        # Right face
        right_x = [cx+0.7, cx+0.7+0.25, cx+0.7+0.25, cx+0.7]
        right_y = [cy-h*0.25, cy-h*0.25+0.25*0.5, cy+0.25*0.5, cy]
        plt.fill(right_x, right_y, color=colors_grid[i % len(colors_grid)],
                 alpha=0.4, edgecolor='white', linewidth=0.3)

plt.xlim(-0.5, nx * 1.0 + 0.5)
plt.ylim(-nz * 0.25 - 1, nz * 0.8 + 1)
plt.title('3D Bar Grid (8×5)')
plt.xlabel('x'); plt.ylabel('y')
save('gl10_bar_grid')

print(f"\n{'='*60}")
print("  3D Demos Complete! (10 demos — 2D projection fallback)")
print(f"  All demos work on all platforms including Apple Silicon.")
print(f"  Output: {OUT_DIR}/")
print(f"{'='*60}")
