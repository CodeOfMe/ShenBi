"""
ShenBi — Comprehensive Dataset Visualization Demos
====================================================
Uses real standard datasets (iris, wine, breast_cancer, digits, diabetes)
to demonstrate all plotting capabilities with meaningful data.

No grid by default. White background. All matplotlib-compatible syntax.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import numpy as np
import shenbi.pyplot as plt
from shenbi.colors import TAB10_COLORS
from shenbi.cm import get_cmap

# ── Load Standard Datasets ─────────────────────────────────────────
try:
    from sklearn.datasets import (
        load_iris, load_wine, load_breast_cancer,
        load_digits, load_diabetes, fetch_california_housing
    )
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("sklearn not installed, using synthetic data")

def get_iris():
    if HAS_SKLEARN:
        return load_iris()
    # Fallback synthetic iris-like data
    np.random.seed(42)
    n = 50
    d = {'data': np.vstack([
        np.random.randn(n, 4) * 0.3 + [5, 3.5, 1.5, 0.3],
        np.random.randn(n, 4) * 0.4 + [5.9, 2.8, 4.3, 1.3],
        np.random.randn(n, 4) * 0.5 + [6.6, 3.0, 5.5, 2.0],
    ]), 'target': np.array([0]*n + [1]*n + [2]*n),
       'target_names': ['setosa', 'versicolor', 'virginica'],
       'feature_names': ['sepal length', 'sepal width', 'petal length', 'petal width']}
    return type('Dataset', (), d)()

def get_wine():
    if HAS_SKLEARN:
        return load_wine()
    np.random.seed(42)
    n = 60
    d = {'data': np.vstack([
        np.random.randn(n, 13) * 0.5 + 13,
        np.random.randn(n, 13) * 0.5 + 12,
        np.random.randn(n, 13) * 0.5 + 13.5,
    ]), 'target': np.array([0]*n + [1]*n + [2]*n),
       'target_names': ['Class 0', 'Class 1', 'Class 2'],
       'feature_names': [f'feat_{i}' for i in range(13)]}
    return type('Dataset', (), d)()

def get_breast_cancer():
    if HAS_SKLEARN:
        return load_breast_cancer()
    np.random.seed(42)
    n = 285
    d = {'data': np.vstack([
        np.random.randn(n, 30) * 0.3,
        np.random.randn(n, 30) * 0.3 + 1,
    ]), 'target': np.array([0]*n + [1]*n),
       'target_names': ['malignant', 'benign'],
       'feature_names': [f'f{i}' for i in range(30)]}
    return type('Dataset', (), d)()

def get_digits():
    if HAS_SKLEARN:
        return load_digits()
    np.random.seed(42)
    n = 180
    d = {'data': np.random.rand(n, 64) * 16,
         'target': np.tile(np.arange(10), n//10),
         'images': np.random.rand(n, 8, 8) * 16}
    return type('Dataset', (), d)()

def get_diabetes():
    if HAS_SKLEARN:
        return load_diabetes()
    np.random.seed(42)
    n = 442
    d = {'data': np.random.randn(n, 10),
         'target': np.random.randn(n) * 100 + 150,
         'feature_names': ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']}
    return type('Dataset', (), d)()

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

# Load all datasets
iris = get_iris()
wine = get_wine()
cancer = get_breast_cancer()
digits = get_digits()
diabetes = get_diabetes()

# ═══════════════════════════════════════════════════════════════════
#  1. IRIS — Scatter matrix (sepal length vs width)
# ═══════════════════════════════════════════════════════════════════
print("\n1. Iris — Sepal Length vs Width (colored by species)")
X = iris.data
y = iris.target
names = iris.target_names
feat = iris.feature_names

plt.figure(figsize=(8, 6))
for i, name in enumerate(names):
    mask = y == i
    plt.scatter(X[mask, 0], X[mask, 1], s=40, c=TAB10_COLORS[i],
                alpha=0.7, edgecolors='white', linewidths=0.5, label=name)
plt.title('Iris Dataset — Sepal Length vs Sepal Width')
plt.xlabel(f'{feat[0]} (cm)')
plt.ylabel(f'{feat[1]} (cm)')
plt.legend()
save('ds01_iris_sepal')

# ═══════════════════════════════════════════════════════════════════
#  2. IRIS — Petal scatter with colormap
# ═══════════════════════════════════════════════════════════════════
print("2. Iris — Petal Length vs Width (colormap)")
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X[:, 2], X[:, 3], s=50, c=y, cmap='viridis',
                       alpha=0.8, edgecolors='white', linewidths=0.5)
plt.title('Iris — Petal Length vs Petal Width')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel(f'{feat[3]} (cm)')
plt.colorbar(scatter, label='Species')
save('ds02_iris_petal_cmap')

# ═══════════════════════════════════════════════════════════════════
#  3. IRIS — Boxplot by species
# ═══════════════════════════════════════════════════════════════════
print("3. Iris — Boxplot (all features by species)")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax_idx, ax in enumerate(axes.flat):
    data_by_class = [X[y == i, ax_idx] for i in range(3)]
    ax.boxplot(data_by_class, tick_labels=names)
    ax.set_title(f'{feat[ax_idx]}')
    ax.set_ylabel('cm')
plt.suptitle('Iris Dataset — Feature Distribution by Species')
plt.tight_layout()
save('ds03_iris_boxplot')

# ═══════════════════════════════════════════════════════════════════
#  4. IRIS — Histogram overlay
# ═══════════════════════════════════════════════════════════════════
print("4. Iris — Histogram overlay (petal length)")
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    plt.hist(X[mask, 2], bins=20, alpha=0.5, color=TAB10_COLORS[i],
             edgecolor='white', linewidth=0.5, label=name)
plt.title('Iris — Petal Length Distribution by Species')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel('Count')
plt.legend()
save('ds04_iris_hist')

# ═══════════════════════════════════════════════════════════════════
#  5. IRIS — Bar chart (mean values)
# ═══════════════════════════════════════════════════════════════════
print("5. Iris — Mean feature values by species")
means = np.array([X[y == i].mean(axis=0) for i in range(3)])
x_pos = np.arange(len(feat))
width = 0.25

plt.figure(figsize=(12, 6))
for i, name in enumerate(names):
    plt.bar(x_pos + i * width, means[i], width, label=name,
            color=TAB10_COLORS[i], edgecolor='white', linewidth=0.5)
plt.xticks(x_pos + width, feat, rotation=45, ha='right')
plt.title('Iris — Mean Feature Values by Species')
plt.ylabel('Mean Value (cm)')
plt.legend()
save('ds05_iris_bar')

# ═══════════════════════════════════════════════════════════════════
#  6. WINE — Radar/parallel coordinates style
# ═══════════════════════════════════════════════════════════════════
print("6. Wine — Feature means by class")
wine_data = wine.data
wine_y = wine.target
wine_names = wine.target_names
wine_feat = wine.feature_names[:6]  # First 6 features for readability

wine_means = np.array([wine_data[wine_y == i, :6].mean(axis=0) for i in range(3)])
x_pos = np.arange(6)
width = 0.25

plt.figure(figsize=(12, 6))
for i, name in enumerate(wine_names):
    plt.bar(x_pos + i * width, wine_means[i], width, label=name,
            color=TAB10_COLORS[i], edgecolor='white', linewidth=0.5)
plt.xticks(x_pos + width, wine_feat, rotation=45, ha='right')
plt.title('Wine Dataset — Mean Feature Values by Class (first 6)')
plt.ylabel('Mean Value')
plt.legend()
save('ds06_wine_bar')

# ═══════════════════════════════════════════════════════════════════
#  7. WINE — Scatter with error bars
# ═══════════════════════════════════════════════════════════════════
print("7. Wine — Scatter with error bars")
plt.figure(figsize=(8, 6))
for i, name in enumerate(wine_names):
    mask = wine_y == i
    x_mean = wine_data[mask, 0].mean()
    y_mean = wine_data[mask, 1].mean()
    x_std = wine_data[mask, 0].std()
    y_std = wine_data[mask, 1].std()
    plt.errorbar(x_mean, y_mean, xerr=x_std, yerr=y_std, fmt='o',
                 color=TAB10_COLORS[i], markersize=10, capsize=5,
                 label=f'{name} (mean±std)')
plt.title('Wine Dataset — Feature 0 vs Feature 1 (mean ± std)')
plt.xlabel(wine_feat[0])
plt.ylabel(wine_feat[1])
plt.legend()
save('ds07_wine_errorbar')

# ═══════════════════════════════════════════════════════════════════
#  8. BREAST CANCER — Feature importance bar
# ═══════════════════════════════════════════════════════════════════
print("8. Breast Cancer — Feature means (malignant vs benign)")
cancer_data = cancer.data
cancer_y = cancer.target
cancer_names = cancer.target_names
cancer_feat = cancer.feature_names[:10]  # Top 10

cancer_means = np.array([cancer_data[cancer_y == i, :10].mean(axis=0) for i in range(2)])
x_pos = np.arange(10)
width = 0.35

plt.figure(figsize=(14, 6))
plt.bar(x_pos - width/2, cancer_means[0], width, label=cancer_names[0],
        color='#d62728', edgecolor='white', linewidth=0.5)
plt.bar(x_pos + width/2, cancer_means[1], width, label=cancer_names[1],
        color='#2ca02c', edgecolor='white', linewidth=0.5)
plt.xticks(x_pos, cancer_feat, rotation=45, ha='right')
plt.title('Breast Cancer — Mean Feature Values (Malignant vs Benign)')
plt.ylabel('Mean Value')
plt.legend()
save('ds08_cancer_bar')

# ═══════════════════════════════════════════════════════════════════
#  9. BREAST CANCER — Violin-style boxplot
# ═══════════════════════════════════════════════════════════════════
print("9. Breast Cancer — Boxplot (top 5 features)")
fig, axes = plt.subplots(1, 5, figsize=(16, 5))
top_feats = [0, 1, 2, 3, 22]  # mean radius, mean texture, mean perimeter, mean area, worst texture
for idx, ax in enumerate(axes):
    feat_idx = top_feats[idx]
    data_by_class = [cancer_data[cancer_y == i, feat_idx] for i in range(2)]
    ax.boxplot(data_by_class, tick_labels=cancer_names)
    ax.set_title(cancer_feat[feat_idx])
plt.suptitle('Breast Cancer — Feature Distribution by Diagnosis')
plt.tight_layout()
save('ds09_cancer_boxplot')

# ═══════════════════════════════════════════════════════════════════
#  10. DIGITS — Image display
# ═══════════════════════════════════════════════════════════════════
print("10. Digits — Sample images")
digits_data = digits.data
digits_images = digits.images if hasattr(digits, 'images') else digits_data.reshape(-1, 8, 8)
digits_y = digits.target

fig, axes = plt.subplots(3, 5, figsize=(12, 8))
axes = axes.flatten()
for i, ax in enumerate(axes):
    ax.imshow(digits_images[i], cmap='Greys', vmin=0, vmax=16)
    ax.set_title(f'Digit: {digits_y[i]}')
    ax.axis('off')
plt.suptitle('Digits Dataset — Sample Images (8×8 pixels)')
plt.tight_layout()
save('ds10_digits_images')

# ═══════════════════════════════════════════════════════════════════
#  11. DIGITS — PCA-like scatter (first 2 features as proxy)
# ═══════════════════════════════════════════════════════════════════
print("11. Digits — Feature scatter (colored by digit)")
plt.figure(figsize=(8, 6))
for digit in range(10):
    mask = digits_y == digit
    plt.scatter(digits_data[mask, 0], digits_data[mask, 1],
                s=20, c=get_cmap('tab10')(digit/9, bytes=True),
                alpha=0.6, edgecolors='none', label=str(digit))
plt.title('Digits — Feature 0 vs Feature 1')
plt.xlabel('Feature 0')
plt.ylabel('Feature 1')
plt.legend(title='Digit', fontsize=8)
save('ds11_digits_scatter')

# ═══════════════════════════════════════════════════════════════════
#  12. DIGITS — Histogram of pixel intensities
# ═══════════════════════════════════════════════════════════════════
print("12. Digits — Pixel intensity histogram")
plt.figure(figsize=(10, 6))
for digit in range(0, 10, 2):
    mask = digits_y == digit
    pixels = digits_data[mask].flatten()
    plt.hist(pixels, bins=32, alpha=0.4, color=get_cmap('tab10')(digit/9, bytes=True),
             edgecolor='white', linewidth=0.3, label=f'Digit {digit}')
plt.title('Digits — Pixel Intensity Distribution (every other digit)')
plt.xlabel('Pixel Value (0-16)')
plt.ylabel('Count')
plt.legend(fontsize=8)
save('ds12_digits_hist')

# ═══════════════════════════════════════════════════════════════════
#  13. DIABETES — Scatter with regression line
# ═══════════════════════════════════════════════════════════════════
print("13. Diabetes — BMI vs Target with fit line")
dia_data = diabetes.data
dia_target = diabetes.target
dia_feat = diabetes.feature_names

bmi_idx = 2  # BMI is 3rd feature
x_bmi = dia_data[:, bmi_idx]
y_target = dia_target

# Simple linear fit
coeffs = np.polyfit(x_bmi, y_target, 1)
x_fit = np.linspace(x_bmi.min(), x_bmi.max(), 100)
y_fit = np.polyval(coeffs, x_fit)

plt.figure(figsize=(10, 6))
plt.scatter(x_bmi, y_target, s=15, c='#1f77b4', alpha=0.4, edgecolors='none')
plt.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'y = {coeffs[0]:.1f}x + {coeffs[1]:.0f}')
plt.title(f'Diabetes — BMI vs Disease Progression')
plt.xlabel(dia_feat[bmi_idx])
plt.ylabel('Disease Progression')
plt.legend()
save('ds13_diabetes_scatter')

# ═══════════════════════════════════════════════════════════════════
#  14. DIABETES — Bar chart of feature correlations
# ═══════════════════════════════════════════════════════════════════
print("14. Diabetes — Feature correlations with target")
correlations = np.array([np.corrcoef(dia_data[:, i], dia_target)[0, 1]
                         for i in range(dia_data.shape[1])])
colors_corr = ['#d62728' if c < 0 else '#2ca02c' for c in correlations]

plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(dia_feat)), correlations, color=colors_corr,
               edgecolor='white', linewidth=0.5)
plt.xticks(range(len(dia_feat)), dia_feat, rotation=45, ha='right')
plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
plt.title('Diabetes — Feature Correlation with Disease Progression')
plt.ylabel('Correlation Coefficient')
save('ds14_diabetes_corr')

# ═══════════════════════════════════════════════════════════════════
#  15. IRIS — Pairwise scatter (subset)
# ═══════════════════════════════════════════════════════════════════
print("15. Iris — Pairwise feature scatter matrix")
fig, axes = plt.subplots(4, 4, figsize=(14, 14))
for i in range(4):
    for j in range(4):
        ax = axes[i, j]
        if i == j:
            # Histogram on diagonal
            for k, name in enumerate(names):
                mask = y == k
                ax.hist(X[mask, i], bins=15, alpha=0.5, color=TAB10_COLORS[k],
                        edgecolor='white', linewidth=0.3)
            ax.set_title(feat[i])
        else:
            # Scatter off-diagonal
            for k, name in enumerate(names):
                mask = y == k
                ax.scatter(X[mask, j], X[mask, i], s=15, c=TAB10_COLORS[k],
                           alpha=0.5, edgecolors='none')
        if i == 3:
            ax.set_xlabel(feat[j])
        if j == 0:
            ax.set_ylabel(feat[i])
plt.suptitle('Iris — Pairwise Feature Scatter Matrix', y=1.02)
plt.tight_layout()
save('ds15_iris_pairwise')

# ═══════════════════════════════════════════════════════════════════
#  16. IRIS — Cumulative distribution
# ═══════════════════════════════════════════════════════════════════
print("16. Iris — Cumulative distribution (petal length)")
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    vals = np.sort(X[mask, 2])
    cumsum = np.arange(1, len(vals) + 1) / len(vals)
    plt.plot(vals, cumsum, color=TAB10_COLORS[i], linewidth=2, label=name)
plt.title('Iris — Cumulative Distribution of Petal Length')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel('Cumulative Proportion')
plt.legend()
save('ds16_iris_cdf')

# ═══════════════════════════════════════════════════════════════════
#  17. WINE — Stacked bar chart
# ═══════════════════════════════════════════════════════════════════
print("17. Wine — Stacked bar (feature contributions)")
# Normalize features to [0,1] for stacking
wine_norm = (wine_data[:, :5] - wine_data[:, :5].min(axis=0)) / \
            (wine_data[:, :5].max(axis=0) - wine_data[:, :5].min(axis=0) + 1e-10)
wine_class_means = np.array([wine_norm[wine_y == i, :5].mean(axis=0) for i in range(3)])

plt.figure(figsize=(10, 6))
bottom = np.zeros(3)
for j in range(5):
    plt.bar(range(3), wine_class_means[:, j], bottom=bottom,
            label=wine_feat[j], color=TAB10_COLORS[j], edgecolor='white', linewidth=0.5)
    bottom += wine_class_means[:, j]
plt.xticks(range(3), wine_names)
plt.title('Wine — Stacked Feature Contributions by Class')
plt.ylabel('Normalized Mean')
plt.legend(fontsize=8)
save('ds17_wine_stacked')

# ═══════════════════════════════════════════════════════════════════
#  18. Multi-dataset comparison
# ═══════════════════════════════════════════════════════════════════
print("18. Multi-dataset — Sample size comparison")
datasets = ['Iris', 'Wine', 'Breast\nCancer', 'Digits', 'Diabetes']
sizes = [len(iris.data), len(wine.data), len(cancer.data),
         len(digits.data), len(diabetes.data)]
features = [iris.data.shape[1], wine.data.shape[1], cancer.data.shape[1],
            digits.data.shape[1], diabetes.data.shape[1]]
classes = [len(iris.target_names), len(wine.target_names),
           len(cancer.target_names), 10, 1]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
axes[0].bar(datasets, sizes, color='#1f77b4', edgecolor='white', linewidth=0.5)
axes[0].set_title('Sample Size')
axes[0].set_ylabel('Number of Samples')
axes[1].bar(datasets, features, color='#2ca02c', edgecolor='white', linewidth=0.5)
axes[1].set_title('Number of Features')
axes[1].set_ylabel('Features')
axes[2].bar(datasets, classes, color='#d62728', edgecolor='white', linewidth=0.5)
axes[2].set_title('Number of Classes')
axes[2].set_ylabel('Classes')
plt.suptitle('Dataset Overview Comparison')
plt.tight_layout()
save('ds18_dataset_overview')

# ═══════════════════════════════════════════════════════════════════
#  19. IRIS — Line plot (mean profiles)
# ═══════════════════════════════════════════════════════════════════
print("19. Iris — Mean feature profiles")
plt.figure(figsize=(10, 6))
x_feat = np.arange(4)
for i, name in enumerate(names):
    plt.plot(x_feat, means[i], 'o-', color=TAB10_COLORS[i], linewidth=2,
             markersize=8, label=name)
plt.xticks(x_feat, feat, rotation=45, ha='right')
plt.title('Iris — Mean Feature Profiles by Species')
plt.ylabel('Mean Value (cm)')
plt.legend()
save('ds19_iris_profiles')

# ═══════════════════════════════════════════════════════════════════
#  20. IRIS — Fill between (confidence bands)
# ═══════════════════════════════════════════════════════════════════
print("20. Iris — Confidence bands (petal measurements)")
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    petal_l = X[mask, 2]
    petal_w = X[mask, 3]
    # Sort by petal length for fill_between
    sort_idx = np.argsort(petal_l)
    pl = petal_l[sort_idx]
    pw = petal_w[sort_idx]
    # Simple confidence band (±1 std)
    std_w = np.std(pw)
    plt.plot(pl, pw, color=TAB10_COLORS[i], linewidth=1.5, label=name)
    plt.fill_between(pl, pw - std_w, pw + std_w, alpha=0.15, color=TAB10_COLORS[i])
plt.title('Iris — Petal Length vs Width with Confidence Bands')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel(f'{feat[3]} (cm)')
plt.legend()
save('ds20_iris_confidence')

print(f"\n{'='*60}")
print("  Dataset Visualization Demos Complete! (20 demos)")
print(f"  Datasets: Iris, Wine, Breast Cancer, Digits, Diabetes")
print(f"  Output: {OUT_DIR}/")
print(f"{'='*60}")
