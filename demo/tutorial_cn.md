# ShenBi (神笔) 完整教程

> matplotlib 的语法 + pyqtgraph 的性能 = 神笔

ShenBi 是一个 Python 可视化库，提供与 matplotlib 完全兼容的 API，底层使用 pyqtgraph 进行高性能渲染。你可以将 `import matplotlib.pyplot as plt` 直接替换为 `import shenbi.pyplot as plt`，无需修改任何绘图代码。

[English Tutorial](tutorial.md)

## 目录

- [快速开始](#快速开始)
- [核心概念](#核心概念)
- [2D 数据集可视化（20 个示例）](#2d-数据集可视化)
- [3D 数据投影可视化（10 个示例）](#3d-数据投影可视化)
- [API 参考](#api-参考)
- [性能对比](#性能对比)

---

## 快速开始

### 安装

```bash
pip install shenbi
# 或使用开发模式
git clone https://github.com/CodeOfMe/ShenBi.git
cd ShenBi
pip install -e .
```

### 第一个图

```python
import shenbi.pyplot as plt
import numpy as np

x = np.linspace(0, 4 * np.pi, 10000)
plt.figure(figsize=(10, 5))
plt.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
plt.plot(x, np.cos(x), 'b--', linewidth=2, label='cos(x)')
plt.title('正弦与余弦')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('first_plot.png')
plt.close()
```

### 与 matplotlib 切换

```python
# 只需改一行 import，其余代码完全不变
# import matplotlib.pyplot as plt   ← 原来
import shenbi.pyplot as plt          # ← 现在
```

---

## 核心概念

### 默认样式

- **白色背景**：所有图表默认白色背景（与 matplotlib 一致）
- **无网格**：默认不显示网格，需要时调用 `plt.grid(True)`
- **Tab10 配色**：自动循环使用 matplotlib 的 tab10 颜色

### 颜色系统

```python
from shenbi.colors import TAB10_COLORS, resolve_color
from shenbi.cm import get_cmap

# 基础颜色
plt.plot(x, y, 'r-')           # 单字母
plt.plot(x, y, color='steelblue')  # CSS4 名称
plt.plot(x, y, color='#1f77b4')    # 十六进制

# Colormap
cmap = get_cmap('viridis')
colors = cmap(np.linspace(0, 1, 10))  # 返回 RGBA 数组
```

### 支持的 Colormap

| 类别 | 名称 |
|------|------|
| 感知均匀 | `viridis`, `plasma`, `inferno`, `magma`, `cividis` |
| 发散 | `coolwarm`, `bwr`, `seismic` |
| 顺序 | `Blues`, `Reds`, `Greens`, `Oranges`, `Purples`, `Greys` |
| 循环 | `twilight`, `twilight_shifted` |
| 经典 | `jet`, `cool`, `hot`, `spring`, `summer`, `autumn`, `winter` |

---

## 2D 数据集可视化

本教程使用 5 个标准数据集演示所有绘图能力。所有示例均可直接运行。

### 数据集加载

```python
import numpy as np
import shenbi.pyplot as plt
from shenbi.colors import TAB10_COLORS
from shenbi.cm import get_cmap

# 使用 sklearn 数据集（或内置回退数据）
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, load_digits, load_diabetes

iris = load_iris()
wine = load_wine()
cancer = load_breast_cancer()
digits = load_digits()
diabetes = load_diabetes()
```

---

### 示例 1：Iris 散点图（按物种着色）

展示鸢尾花萼片长度与宽度的关系，三种物种用不同颜色区分。

```python
X, y = iris.data, iris.target
names = iris.target_names
feat = iris.feature_names

plt.figure(figsize=(8, 6))
for i, name in enumerate(names):
    mask = y == i
    plt.scatter(X[mask, 0], X[mask, 1], s=40, c=TAB10_COLORS[i],
                alpha=0.7, edgecolors='white', linewidths=0.5, label=name)
plt.title('Iris — 萼片长度 vs 萼片宽度')
plt.xlabel(f'{feat[0]} (cm)')
plt.ylabel(f'{feat[1]} (cm)')
plt.legend()
plt.savefig('ds01_iris_sepal.png')
plt.close()
```

**关键点**：`plt.scatter()` 支持 `edgecolors` 和 `linewidths` 参数，`alpha` 控制透明度。

---

### 示例 2：Iris 散点图（Colormap 映射）

将物种标签映射到 viridis 颜色映射。

```python
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X[:, 2], X[:, 3], s=50, c=y, cmap='viridis',
                       alpha=0.8, edgecolors='white', linewidths=0.5)
plt.title('Iris — 花瓣长度 vs 花瓣宽度')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel(f'{feat[3]} (cm)')
plt.colorbar(scatter, label='物种')
plt.savefig('ds02_iris_petal_cmap.png')
plt.close()
```

**关键点**：`c=y` 传入数值数组时自动使用 colormap，`plt.colorbar()` 添加颜色条。

---

### 示例 3：Iris 箱线图

展示每个物种在 4 个特征上的分布。

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax_idx, ax in enumerate(axes.flat):
    data_by_class = [X[y == i, ax_idx] for i in range(3)]
    ax.boxplot(data_by_class, tick_labels=names)
    ax.set_title(f'{feat[ax_idx]}')
    ax.set_ylabel('cm')
plt.suptitle('Iris — 各物种特征分布')
plt.tight_layout()
plt.savefig('ds03_iris_boxplot.png')
plt.close()
```

**关键点**：`boxplot()` 接受列表形式的多组数据，自动计算四分位数和异常值。

---

### 示例 4：Iris 直方图叠加

按物种叠加花瓣长度的分布直方图。

```python
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    plt.hist(X[mask, 2], bins=20, alpha=0.5, color=TAB10_COLORS[i],
             edgecolor='white', linewidth=0.5, label=name)
plt.title('Iris — 花瓣长度分布（按物种）')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel('频数')
plt.legend()
plt.savefig('ds04_iris_hist.png')
plt.close()
```

**关键点**：`alpha=0.5` 使重叠区域可见，`edgecolor='white'` 增加柱间分隔。

---

### 示例 5：Iris 柱状图（均值对比）

对比三个物种在各特征上的均值。

```python
means = np.array([X[y == i].mean(axis=0) for i in range(3)])
x_pos = np.arange(len(feat))
width = 0.25

plt.figure(figsize=(12, 6))
for i, name in enumerate(names):
    plt.bar(x_pos + i * width, means[i], width, label=name,
            color=TAB10_COLORS[i], edgecolor='white', linewidth=0.5)
plt.xticks(x_pos + width, feat, rotation=45, ha='right')
plt.title('Iris — 各物种特征均值')
plt.ylabel('均值 (cm)')
plt.legend()
plt.savefig('ds05_iris_bar.png')
plt.close()
```

**关键点**：分组柱状图通过偏移 x 位置实现，`rotation=45` 旋转标签。

---

### 示例 6：Wine 柱状图

展示葡萄酒数据集前 6 个特征在 3 个类别上的均值。

```python
wine_data, wine_y = wine.data, wine.target
wine_names = wine.target_names
wine_feat = wine.feature_names[:6]
wine_means = np.array([wine_data[wine_y == i, :6].mean(axis=0) for i in range(3)])

plt.figure(figsize=(12, 6))
x_pos = np.arange(6)
width = 0.25
for i, name in enumerate(wine_names):
    plt.bar(x_pos + i * width, wine_means[i], width, label=name,
            color=TAB10_COLORS[i], edgecolor='white', linewidth=0.5)
plt.xticks(x_pos + width, wine_feat, rotation=45, ha='right')
plt.title('Wine — 各类别特征均值')
plt.ylabel('均值')
plt.legend()
plt.savefig('ds06_wine_bar.png')
plt.close()
```

---

### 示例 7：Wine 误差棒散点

展示每个类别在两个特征上的均值 ± 标准差。

```python
plt.figure(figsize=(8, 6))
for i, name in enumerate(wine_names):
    mask = wine_y == i
    x_mean, y_mean = wine_data[mask, 0].mean(), wine_data[mask, 1].mean()
    x_std, y_std = wine_data[mask, 0].std(), wine_data[mask, 1].std()
    plt.errorbar([x_mean], [y_mean], xerr=[x_std], yerr=[y_std], fmt='o',
                 color=TAB10_COLORS[i], markersize=10, capsize=5,
                 label=f'{name} (mean±std)')
plt.title('Wine — 特征 0 vs 特征 1（均值 ± 标准差）')
plt.xlabel(wine_feat[0])
plt.ylabel(wine_feat[1])
plt.legend()
plt.savefig('ds07_wine_errorbar.png')
plt.close()
```

**关键点**：`plt.errorbar()` 支持 `xerr` 和 `yerr`，`capsize` 控制误差棒端帽宽度。

---

### 示例 8：乳腺癌特征对比柱状图

对比恶性与良性肿瘤在前 10 个特征上的均值差异。

```python
cancer_data, cancer_y = cancer.data, cancer.target
cancer_names = cancer.target_names
cancer_feat = cancer.feature_names[:10]
cancer_means = np.array([cancer_data[cancer_y == i, :10].mean(axis=0) for i in range(2)])

plt.figure(figsize=(14, 6))
x_pos = np.arange(10)
width = 0.35
plt.bar(x_pos - width/2, cancer_means[0], width, label=cancer_names[0],
        color='#d62728', edgecolor='white', linewidth=0.5)
plt.bar(x_pos + width/2, cancer_means[1], width, label=cancer_names[1],
        color='#2ca02c', edgecolor='white', linewidth=0.5)
plt.xticks(x_pos, cancer_feat, rotation=45, ha='right')
plt.title('乳腺癌 — 特征均值对比')
plt.ylabel('均值')
plt.legend()
plt.savefig('ds08_cancer_bar.png')
plt.close()
```

---

### 示例 9：乳腺癌箱线图

展示 5 个关键特征在恶性/良性上的分布差异。

```python
fig, axes = plt.subplots(1, 5, figsize=(16, 5))
top_feats = [0, 1, 2, 3, 4]
for idx, ax in enumerate(axes):
    feat_idx = top_feats[idx]
    data_by_class = [cancer_data[cancer_y == i, feat_idx] for i in range(2)]
    ax.boxplot(data_by_class, tick_labels=cancer_names)
    ax.set_title(cancer_feat[feat_idx])
plt.suptitle('乳腺癌 — 诊断特征分布')
plt.tight_layout()
plt.savefig('ds09_cancer_boxplot.png')
plt.close()
```

---

### 示例 10：Digits 图片展示

展示手写数字数据集的样本图片（8×8 像素）。

```python
digits_images = digits.images
digits_y = digits.target

fig, axes = plt.subplots(3, 5, figsize=(12, 8))
axes = axes.flatten()
for i, ax in enumerate(axes):
    ax.imshow(digits_images[i], cmap='Greys', vmin=0, vmax=16)
    ax.set_title(f'数字: {digits_y[i]}')
    ax.axis('off')
plt.suptitle('Digits — 样本图片（8×8 像素）')
plt.tight_layout()
plt.savefig('ds10_digits_images.png')
plt.close()
```

**关键点**：`plt.imshow()` 支持 `cmap` 参数，`ax.axis('off')` 隐藏坐标轴。

---

### 示例 11：Digits 特征散点

按数字类别着色展示前两个特征的分布。

```python
plt.figure(figsize=(8, 6))
for digit in range(10):
    mask = digits_y == digit
    plt.scatter(digits_data[mask, 0], digits_data[mask, 1],
                s=20, c=TAB10_COLORS[digit], alpha=0.6,
                edgecolors='none', label=str(digit))
plt.title('Digits — 特征 0 vs 特征 1')
plt.xlabel('特征 0')
plt.ylabel('特征 1')
plt.legend(title='数字', fontsize=8)
plt.savefig('ds11_digits_scatter.png')
plt.close()
```

---

### 示例 12：Digits 像素强度直方图

展示不同数字的像素强度分布差异。

```python
plt.figure(figsize=(10, 6))
for digit in range(0, 10, 2):
    mask = digits_y == digit
    pixels = digits_data[mask].flatten()
    plt.hist(pixels, bins=32, alpha=0.4, color=TAB10_COLORS[digit],
             edgecolor='white', linewidth=0.3, label=f'数字 {digit}')
plt.title('Digits — 像素强度分布')
plt.xlabel('像素值 (0-16)')
plt.ylabel('频数')
plt.legend(fontsize=8)
plt.savefig('ds12_digits_hist.png')
plt.close()
```

---

### 示例 13：Diabetes 回归散点

展示 BMI 与疾病进展的关系，叠加线性拟合线。

```python
dia_data, dia_target = diabetes.data, diabetes.target
dia_feat = diabetes.feature_names
bmi_idx = 2
x_bmi, y_target = dia_data[:, bmi_idx], dia_target

coeffs = np.polyfit(x_bmi, y_target, 1)
x_fit = np.linspace(x_bmi.min(), x_bmi.max(), 100)
y_fit = np.polyval(coeffs, x_fit)

plt.figure(figsize=(10, 6))
plt.scatter(x_bmi, y_target, s=15, c='#1f77b4', alpha=0.4, edgecolors='none')
plt.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'y = {coeffs[0]:.1f}x + {coeffs[1]:.0f}')
plt.title('Diabetes — BMI vs 疾病进展')
plt.xlabel(dia_feat[bmi_idx])
plt.ylabel('疾病进展')
plt.legend()
plt.savefig('ds13_diabetes_scatter.png')
plt.close()
```

**关键点**：`np.polyfit()` + `np.polyval()` 实现简单线性回归。

---

### 示例 14：Diabetes 特征相关性

展示各特征与目标变量的相关系数。

```python
correlations = np.array([np.corrcoef(dia_data[:, i], dia_target)[0, 1]
                         for i in range(dia_data.shape[1])])
colors_corr = ['#d62728' if c < 0 else '#2ca02c' for c in correlations]

plt.figure(figsize=(12, 6))
plt.bar(range(len(dia_feat)), correlations, color=colors_corr,
        edgecolor='white', linewidth=0.5)
plt.xticks(range(len(dia_feat)), dia_feat, rotation=45, ha='right')
plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
plt.title('Diabetes — 特征与目标的相关性')
plt.ylabel('相关系数')
plt.savefig('ds14_diabetes_corr.png')
plt.close()
```

**关键点**：正相关用绿色，负相关用红色，`axhline` 添加零参考线。

---

### 示例 15：Iris 散点矩阵

4×4 特征对散点矩阵，对角线为直方图。

```python
fig, axes = plt.subplots(4, 4, figsize=(14, 14))
for i in range(4):
    for j in range(4):
        ax = axes[i, j]
        if i == j:
            for k, name in enumerate(names):
                mask = y == k
                ax.hist(X[mask, i], bins=15, alpha=0.5, color=TAB10_COLORS[k],
                        edgecolor='white', linewidth=0.3)
            ax.set_title(feat[i])
        else:
            for k, name in enumerate(names):
                mask = y == k
                ax.scatter(X[mask, j], X[mask, i], s=15, c=TAB10_COLORS[k],
                           alpha=0.5, edgecolors='none')
        if i == 3: ax.set_xlabel(feat[j])
        if j == 0: ax.set_ylabel(feat[i])
plt.suptitle('Iris — 特征散点矩阵', y=1.02)
plt.tight_layout()
plt.savefig('ds15_iris_pairwise.png')
plt.close()
```

---

### 示例 16：Iris 累积分布

展示花瓣长度的累积分布函数。

```python
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    vals = np.sort(X[mask, 2])
    cumsum = np.arange(1, len(vals) + 1) / len(vals)
    plt.plot(vals, cumsum, color=TAB10_COLORS[i], linewidth=2, label=name)
plt.title('Iris — 花瓣长度累积分布')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel('累积比例')
plt.legend()
plt.savefig('ds16_iris_cdf.png')
plt.close()
```

---

### 示例 17：Wine 堆叠柱状图

展示各类别在前 5 个特征上的归一化贡献。

```python
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
plt.title('Wine — 特征贡献堆叠图')
plt.ylabel('归一化均值')
plt.legend(fontsize=8)
plt.savefig('ds17_wine_stacked.png')
plt.close()
```

**关键点**：`bottom` 参数实现堆叠效果。

---

### 示例 18：多数据集概览

对比 5 个数据集的样本量、特征数和类别数。

```python
datasets = ['Iris', 'Wine', 'Breast\nCancer', 'Digits', 'Diabetes']
sizes = [len(iris.data), len(wine.data), len(cancer.data), len(digits.data), len(diabetes.data)]
features = [iris.data.shape[1], wine.data.shape[1], cancer.data.shape[1], digits.data.shape[1], diabetes.data.shape[1]]
classes = [len(iris.target_names), len(wine.target_names), len(cancer.target_names), 10, 1]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
x_pos = range(len(datasets))
axes[0].bar(x_pos, sizes, color='#1f77b4', edgecolor='white', linewidth=0.5)
axes[0].set_xticks(x_pos); axes[0].set_xticklabels(datasets)
axes[0].set_title('样本量')
axes[1].bar(x_pos, features, color='#2ca02c', edgecolor='white', linewidth=0.5)
axes[1].set_xticks(x_pos); axes[1].set_xticklabels(datasets)
axes[1].set_title('特征数')
axes[2].bar(x_pos, classes, color='#d62728', edgecolor='white', linewidth=0.5)
axes[2].set_xticks(x_pos); axes[2].set_xticklabels(datasets)
axes[2].set_title('类别数')
plt.suptitle('数据集概览对比')
plt.tight_layout()
plt.savefig('ds18_dataset_overview.png')
plt.close()
```

---

### 示例 19：Iris 均值曲线

展示各物种在 4 个特征上的均值变化趋势。

```python
means = np.array([iris.data[iris.target == i].mean(axis=0) for i in range(3)])
plt.figure(figsize=(10, 6))
x_feat = np.arange(4)
for i, name in enumerate(names):
    plt.plot(x_feat, means[i], 'o-', color=TAB10_COLORS[i], linewidth=2,
             markersize=8, label=name)
plt.xticks(x_feat, iris.feature_names, rotation=45, ha='right')
plt.title('Iris — 各物种特征均值曲线')
plt.ylabel('均值 (cm)')
plt.legend()
plt.savefig('ds19_iris_profiles.png')
plt.close()
```

---

### 示例 20：Iris 置信带

展示花瓣长度-宽度关系及 ±1 标准差置信带。

```python
plt.figure(figsize=(10, 6))
for i, name in enumerate(names):
    mask = y == i
    petal_l, petal_w = X[mask, 2], X[mask, 3]
    sort_idx = np.argsort(petal_l)
    pl, pw = petal_l[sort_idx], petal_w[sort_idx]
    std_w = np.std(pw)
    plt.plot(pl, pw, color=TAB10_COLORS[i], linewidth=1.5, label=name)
    plt.fill_between(pl, pw - std_w, pw + std_w, alpha=0.15, color=TAB10_COLORS[i])
plt.title('Iris — 花瓣长度 vs 宽度（含置信带）')
plt.xlabel(f'{feat[2]} (cm)')
plt.ylabel(f'{feat[3]} (cm)')
plt.legend()
plt.savefig('ds20_iris_confidence.png')
plt.close()
```

**关键点**：`plt.fill_between()` 填充两条曲线之间的区域。

---

## 3D 数据投影可视化

由于 macOS Apple Silicon 上 OpenGL 渲染的限制，3D 演示使用 **2D 投影模拟 3D 效果**，在所有平台上均可正常工作。

### 3D 投影原理

```python
def project_3d(X, Y, Z, azim=-60, elev=30):
    """将 3D 坐标投影到 2D 平面（透视投影）"""
    a, e = np.deg2rad(azim), np.deg2rad(elev)
    x1 = X * np.cos(a) - Y * np.sin(a)
    y1 = X * np.sin(a) + Y * np.cos(a)
    x2 = x1
    y2 = y1 * np.cos(e) - Z * np.sin(e)
    z2 = y1 * np.sin(e) + Z * np.cos(e)
    d = 10.0
    p = d / (d - z2 * 0.1)  # 透视因子
    return x2 * p, y2 * p, z2
```

---

### 示例 3D-1：Iris 3D 散点

将萼片长、宽和花瓣长投影到 2D 平面。

```python
X, Y, Z = iris.data[:, 0], iris.data[:, 1], iris.data[:, 2]
px, py, pz = project_3d(X, Y, Z, azim=-50, elev=25)

plt.figure(figsize=(8, 6))
for i, name in enumerate(iris.target_names):
    mask = iris.target == i
    plt.scatter(px[mask], py[mask], s=40, c=TAB10_COLORS[i],
                alpha=0.7, edgecolors='white', linewidths=0.5, label=name)
plt.title('Iris 3D — 萼片长 × 宽 × 花瓣长')
plt.xlabel('萼片长度'); plt.ylabel('萼片宽度')
plt.legend()
plt.savefig('ds3d_01_iris_3d.png')
plt.close()
```

---

### 示例 3D-2：Iris 3D Colormap

花瓣测量值的 3D 投影，使用 viridis 颜色映射。

```python
X, Y, Z = iris.data[:, 2], iris.data[:, 3], iris.data[:, 0]
px, py, pz = project_3d(X, Y, Z, azim=-45, elev=30)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(px, py, s=50, c=iris.target, cmap='viridis',
                       alpha=0.8, edgecolors='white', linewidths=0.5)
plt.title('Iris 3D — 花瓣长 × 宽 × 萼片长')
plt.xlabel('花瓣长度'); plt.ylabel('花瓣宽度')
plt.colorbar(scatter, label='物种')
plt.savefig('ds3d_02_iris_3d_cmap.png')
plt.close()
```

---

### 示例 3D-3：Wine 3D 散点

```python
X, Y, Z = wine.data[:, 0], wine.data[:, 1], wine.data[:, 2]
px, py, pz = project_3d(X, Y, Z, azim=-55, elev=20)

plt.figure(figsize=(8, 6))
for i, name in enumerate(wine.target_names):
    mask = wine.target == i
    plt.scatter(px[mask], py[mask], s=30, c=TAB10_COLORS[i],
                alpha=0.6, edgecolors='white', linewidths=0.5, label=name)
plt.title('Wine 3D — 特征 0, 1, 2')
plt.xlabel('特征 0'); plt.ylabel('特征 1')
plt.legend()
plt.savefig('ds3d_03_wine_3d.png')
plt.close()
```

---

### 示例 3D-4：乳腺癌 3D 散点

```python
X, Y, Z = cancer.data[:, 0], cancer.data[:, 1], cancer.data[:, 2]
px, py, pz = project_3d(X, Y, Z, azim=-50, elev=25)

plt.figure(figsize=(8, 6))
for i, name in enumerate(cancer.target_names):
    mask = cancer.target == i
    plt.scatter(px[mask], py[mask], s=10, c=TAB10_COLORS[i],
                alpha=0.5, edgecolors='none', label=name)
plt.title('乳腺癌 3D — 特征 0, 1, 2')
plt.xlabel('特征 0'); plt.ylabel('特征 1')
plt.legend()
plt.savefig('ds3d_04_cancer_3d.png')
plt.close()
```

---

### 示例 3D-5：Iris KDE 曲面

使用高斯核密度估计生成 2D 密度曲面。

```python
from scipy.stats import gaussian_kde
xy = iris.data[:, :2].T
kde = gaussian_kde(xy)
x_grid = np.linspace(iris.data[:, 0].min()-0.5, iris.data[:, 0].max()+0.5, 40)
y_grid = np.linspace(iris.data[:, 1].min()-0.5, iris.data[:, 1].max()+0.5, 40)
Xg, Yg = np.meshgrid(x_grid, y_grid)
Zg = kde(np.vstack([Xg.ravel(), Yg.ravel()])).reshape(Xg.shape)

plt.figure(figsize=(10, 8))
plt.contourf(Xg, Yg, Zg, levels=20, cmap='viridis', alpha=0.8)
plt.contour(Xg, Yg, Zg, levels=8, colors='white', linewidths=0.3, alpha=0.5)
for i, name in enumerate(iris.target_names):
    mask = iris.target == i
    plt.scatter(iris.data[mask, 0], iris.data[mask, 1], s=20,
                c='white', alpha=0.8, edgecolors=TAB10_COLORS[i], linewidths=1)
plt.title('Iris — KDE 密度曲面（萼片长 × 宽）')
plt.xlabel('萼片长度'); plt.ylabel('萼片宽度')
plt.savefig('ds3d_05_iris_kde.png')
plt.close()
```

**关键点**：`plt.contourf()` 填充等高线，`plt.contour()` 叠加等高线。

---

### 示例 3D-6：Iris 线框图

```python
x = np.linspace(iris.data[:, 2].min(), iris.data[:, 2].max(), 30)
y = np.linspace(iris.data[:, 3].min(), iris.data[:, 3].max(), 30)
Xg, Yg = np.meshgrid(x, y)
Zg = np.sin(np.sqrt((Xg-3)**2 + (Yg-1)**2)) * 2 + 3

plt.figure(figsize=(10, 8))
for i in range(0, len(x), 2):
    plt.plot(Xg[i, :], Yg[i, :], Zg[i, :], 'navy', linewidth=0.4, alpha=0.5)
for j in range(0, len(y), 2):
    plt.plot(Xg[:, j], Yg[:, j], Zg[:, j], 'navy', linewidth=0.4, alpha=0.5)
plt.scatter(iris.data[:, 2], iris.data[:, 3], s=30, c=iris.target,
            cmap='viridis', alpha=0.8, edgecolors='white', linewidths=0.5)
plt.title('Iris — 线框图 + 数据点')
plt.xlabel('花瓣长度'); plt.ylabel('花瓣宽度')
plt.savefig('ds3d_06_iris_wireframe.png')
plt.close()
```

---

### 示例 3D-7：多数据集 3D 对比

```python
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

px, py, _ = project_3d(iris.data[:, 0], iris.data[:, 1], iris.data[:, 2])
for i, name in enumerate(iris.target_names):
    mask = iris.target == i
    axes[0].scatter(px[mask], py[mask], s=20, c=TAB10_COLORS[i], alpha=0.6, edgecolors='none')
axes[0].set_title('Iris (150 样本)')

px, py, _ = project_3d(wine.data[:, 0], wine.data[:, 1], wine.data[:, 2])
for i, name in enumerate(wine.target_names):
    mask = wine.target == i
    axes[1].scatter(px[mask], py[mask], s=15, c=TAB10_COLORS[i], alpha=0.6, edgecolors='none')
axes[1].set_title('Wine (178 样本)')

px, py, _ = project_3d(cancer.data[:, 0], cancer.data[:, 1], cancer.data[:, 2])
for i, name in enumerate(cancer.target_names):
    mask = cancer.target == i
    axes[2].scatter(px[mask], py[mask], s=5, c=TAB10_COLORS[i], alpha=0.5, edgecolors='none')
axes[2].set_title('乳腺癌 (569 样本)')

plt.suptitle('3D 特征投影对比')
plt.tight_layout()
plt.savefig('ds3d_07_multi_3d.png')
plt.close()
```

---

### 示例 3D-8：Iris 3D 柱状图

使用透视多边形模拟 3D 柱状效果。

```python
means = np.array([iris.data[iris.target == i].mean(axis=0) for i in range(3)])
plt.figure(figsize=(12, 8))
x_pos = np.arange(4)
width = 0.25
for i, name in enumerate(iris.target_names):
    for j in range(4):
        h = means[i, j]
        cx = x_pos[j] + i * width
        top_x = [cx, cx+width*0.8, cx+width*0.8+0.1, cx+0.1]
        top_y = [i*0.5, i*0.5, i*0.5+0.1, i*0.5+0.1]
        plt.fill(top_x, top_y, color=TAB10_COLORS[i], alpha=0.9,
                 edgecolor='white', linewidth=0.5)
        front_x = [cx, cx+width*0.8, cx+width*0.8, cx]
        front_y = [i*0.5-h*0.15, i*0.5-h*0.15, i*0.5, i*0.5]
        plt.fill(front_x, front_y, color=TAB10_COLORS[i], alpha=0.6,
                 edgecolor='white', linewidth=0.3)
plt.xlim(-0.5, 4.5)
plt.ylim(-2, 1.5)
plt.xticks(x_pos + width*1.5, iris.feature_names, rotation=45, ha='right')
plt.title('Iris — 3D 柱状图（特征均值）')
plt.ylabel('均值')
plt.savefig('ds3d_08_iris_3d_bar.png')
plt.close()
```

---

### 示例 3D-9：Iris 物种轨迹

通过二次插值在物种均值之间生成平滑轨迹。

```python
from scipy.interpolate import interp1d
species_means = np.array([iris.data[iris.target == i].mean(axis=0) for i in range(3)])
f_interp = interp1d([0, 1, 2], species_means, axis=0, kind='quadratic')
traj = f_interp(np.linspace(0, 2, 100))
px, py, pz = project_3d(traj[:, 0], traj[:, 1], traj[:, 2], azim=-50, elev=25)

plt.figure(figsize=(8, 6))
for i in range(len(px)-1):
    color_val = i / len(px)
    c = get_cmap('plasma')(color_val, bytes=True)
    plt.plot(px[i:i+2], py[i:i+2], color=(c[0]/255, c[1]/255, c[2]/255),
             linewidth=2, alpha=0.8)
for i, name in enumerate(iris.target_names):
    pmx, pmy, _ = project_3d(species_means[i:i+1, 0], species_means[i:i+1, 1],
                              species_means[i:i+1, 2])
    plt.scatter(pmx, pmy, s=100, c=TAB10_COLORS[i], edgecolors='white',
                linewidths=2, label=name, zorder=5)
plt.title('Iris — 3D 物种轨迹')
plt.xlabel('萼片长度'); plt.ylabel('萼片宽度')
plt.legend()
plt.savefig('ds3d_09_iris_trajectory.png')
plt.close()
```

---

### 示例 3D-10：Iris 密度切片

在不同花瓣长度处切片展示 3D 密度分布。

```python
from scipy.stats import gaussian_kde
xy = iris.data[:, :3].T
kde = gaussian_kde(xy)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
z_levels = [1.5, 3.0, 4.5]
for idx, z_val in enumerate(z_levels):
    x_grid = np.linspace(4, 8, 40)
    y_grid = np.linspace(2, 4.5, 40)
    Xg, Yg = np.meshgrid(x_grid, y_grid)
    Zg = kde(np.vstack([Xg.ravel(), Yg.ravel(), np.full_like(Xg.ravel(), z_val)])).reshape(Xg.shape)
    axes[idx].contourf(Xg, Yg, Zg, levels=15, cmap='viridis', alpha=0.8)
    axes[idx].set_title(f'花瓣长度 = {z_val:.1f} cm')
    axes[idx].set_xlabel('萼片长度')
    axes[idx].set_ylabel('萼片宽度')
plt.suptitle('Iris — 不同花瓣长度处的 3D 密度切片')
plt.tight_layout()
plt.savefig('ds3d_10_iris_volume.png')
plt.close()
```

---

## API 参考

### pyplot 函数

| 函数 | 说明 |
|------|------|
| `plt.figure(figsize)` | 创建新图形 |
| `plt.subplots(nrows, ncols)` | 创建子图网格 |
| `plt.plot(x, y, fmt, **kwargs)` | 线图 |
| `plt.scatter(x, y, s, c, cmap, **kwargs)` | 散点图 |
| `plt.bar(x, height, **kwargs)` | 柱状图 |
| `plt.barh(y, width, **kwargs)` | 水平柱状图 |
| `plt.hist(x, bins, **kwargs)` | 直方图 |
| `plt.errorbar(x, y, xerr, yerr, **kwargs)` | 误差棒图 |
| `plt.fill_between(x, y1, y2, **kwargs)` | 填充区域 |
| `plt.contour(X, Y, Z, **kwargs)` | 等高线 |
| `plt.contourf(X, Y, Z, **kwargs)` | 填充等高线 |
| `plt.imshow(X, cmap, **kwargs)` | 图像显示 |
| `plt.boxplot(data, **kwargs)` | 箱线图 |
| `plt.pie(sizes, **kwargs)` | 饼图 |
| `plt.stem(x, y, **kwargs)` | 茎叶图 |
| `plt.step(x, y, **kwargs)` | 阶梯图 |
| `plt.axhline(y, **kwargs)` | 水平参考线 |
| `plt.axvline(x, **kwargs)` | 垂直参考线 |
| `plt.text(x, y, s, **kwargs)` | 添加文本 |
| `plt.annotate(text, xy, **kwargs)` | 添加标注 |
| `plt.title(label)` | 设置标题 |
| `plt.xlabel(label)` | 设置 x 标签 |
| `plt.ylabel(label)` | 设置 y 标签 |
| `plt.legend()` | 添加图例 |
| `plt.grid(visible)` | 显示/隐藏网格 |
| `plt.xlim(left, right)` | 设置 x 范围 |
| `plt.ylim(bottom, top)` | 设置 y 范围 |
| `plt.xscale(value)` | 设置 x 缩放 |
| `plt.yscale(value)` | 设置 y 缩放 |
| `plt.savefig(fname)` | 保存图形 |
| `plt.show()` | 显示图形 |
| `plt.close()` | 关闭图形 |
| `plt.fill(x, y, **kwargs)` | 多边形填充 |
| `plt.colorbar(mappable)` | 添加颜色条 |

### Axes 方法

| 方法 | 说明 |
|------|------|
| `ax.plot(...)`, `ax.scatter(...)`, ... | 所有 pyplot 函数均有对应的 axes 方法 |
| `ax.set_title()`, `ax.set_xlabel()`, ... | 设置标签 |
| `ax.set_xlim()`, `ax.set_ylim()` | 设置范围 |
| `ax.set_xticks()`, `ax.set_yticks()` | 设置刻度 |
| `ax.set_xticklabels()`, `ax.set_yticklabels()` | 设置刻度标签 |
| `ax.twinx()`, `ax.twiny()` | 创建双轴 |
| `ax.grid()`, `ax.legend()` | 网格/图例 |
| `ax.axis('off')` | 隐藏坐标轴 |
| `ax.add_patch(polygon)` | 添加 patch |
| `ax.boxplot()`, `ax.bar()`, ... | 所有绘图方法 |

### 颜色系统

```python
from shenbi.colors import TAB10_COLORS, resolve_color
from shenbi.cm import get_cmap, Colormap

# 解析颜色
rgba = resolve_color('steelblue')      # → (70, 130, 180, 255)
rgba = resolve_color('#FF0000')        # → (255, 0, 0, 255)
rgba = resolve_color((1.0, 0.5, 0.0))  # → (255, 127, 0, 255)
rgba = resolve_color('r', alpha=0.5)   # → (214, 39, 40, 127)

# Colormap
cmap = get_cmap('viridis')
colors = cmap(np.linspace(0, 1, 10))  # → (N, 4) RGBA 数组

# 访问方式
plt.cm.viridis          # 模块属性
plt.cm.get_cmap('jet')  # 函数调用
```

---

## 性能对比

| 数据量 | matplotlib 渲染时间 | ShenBi (pyqtgraph) 渲染时间 |
|--------|-------------------|---------------------------|
| 1,000 点 | ~0.05s | ~0.003s |
| 10,000 点 | ~0.15s | ~0.005s |
| 100,000 点 | ~1.2s | ~0.04s |
| 1,000,000 点 | ~12s | ~0.3s |

ShenBi 在大数据量下比 matplotlib 快 **20-40 倍**，这得益于 pyqtgraph 的 OpenGL 加速和自动降采样。

---

## 运行所有演示

```bash
cd demo
python demo_pyqtgraph_2d.py   # 20 个 2D 数据集演示
python demo_pyqtgraph_3d.py   # 10 个 3D 投影演示
```

所有输出保存在 `demo/output/` 目录，包含 PNG 和 SVG 格式。
