# ShenBi (神笔)

> matplotlib 的语法 + pyqtgraph 的性能

ShenBi 是一个高性能 Python 可视化库，提供与 matplotlib 完全兼容的 API，底层使用 pyqtgraph 的 GPU 加速渲染引擎。用 matplotlib 的方式写代码，获得 pyqtgraph 的速度。

[English Docs](README.md) | [英文教程](demo/tutorial.md) | [中文教程](demo/tutorial_cn.md)

## 为什么选择 ShenBi？

| | matplotlib | pyqtgraph | **ShenBi** |
|---|---|---|---|
| API 友好度 | 优秀 | 复杂 | **优秀**（兼容 matplotlib） |
| 性能 | 大数据慢 | 非常快 | **非常快**（pyqtgraph 引擎） |
| 交互性 | 有限 | 丰富（平移/缩放） | **丰富**（内置） |
| GPU 加速 | 无 | 有（OpenGL） | **有**（继承） |
| 自动降采样 | 无 | 有 | **有**（自动） |
| 默认网格 | 有 | 有 | **无**（更干净） |
| 背景色 | 白色 | 深色 | **白色**（matplotlib 风格） |

## 快速开始

```python
import numpy as np
import shenbi.pyplot as plt

# 生成 100 万个数据点
x = np.linspace(0, 100, 1_000_000)
y = np.sin(x) + 0.1 * np.random.randn(1_000_000)

# 使用熟悉的 matplotlib 语法
plt.figure(figsize=(12, 4))
plt.plot(x, y, 'b-', linewidth=1, label='信号')
plt.title('100 万数据点 — 瞬间渲染')
plt.xlabel('时间')
plt.ylabel('振幅')
plt.legend()
plt.savefig('signal.png')
```

## 功能特性

### 核心绘图
```python
# 线图（支持格式字符串）
plt.plot(x, y, 'r-', linewidth=2, label='线')
plt.plot(x, y2, 'b--', marker='o', markersize=4)

# 散点图（支持 colormap）
plt.scatter(x, y, s=10, c=values, cmap='viridis', alpha=0.5)

# 柱状图（支持边框色）
plt.bar(categories, values, color='steelblue', edgecolor='white')

# 直方图
plt.hist(data, bins=50, color='green', alpha=0.7, edgecolor='white')

# 等高线 / 填充等高线
plt.contourf(X, Y, Z, levels=20, cmap='plasma')
plt.contour(X, Y, Z, levels=8, colors='white')
```

### 子图与布局
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, np.sin(x), 'r-')
axes[0, 1].scatter(xs, ys, s=5, c=ys, cmap='coolwarm')
axes[1, 0].bar([0, 1, 2, 3], [10, 20, 15, 25])
axes[1, 1].hist(np.random.randn(5000), bins=30)
plt.tight_layout()
```

### 高级功能
- **Colormap**：`viridis`、`plasma`、`inferno`、`magma`、`jet`、`cool`、`hot`、`coolwarm`、`Blues`、`Reds` 等 24 种
- **颜色循环**：自动 tab10 颜色循环（`C0`-`C9`）
- **格式字符串**：`'r-o'`、`'b--'`、`'g.'`、`'k:'`、`'mo-'`、`'c^--'` 等
- **误差棒**：`plt.errorbar(x, y, yerr=errors, capsize=5)`
- **填充区域**：`plt.fill_between(x, y1, y2, alpha=0.3)`
- **箱线图**：`plt.boxplot(data, tick_labels=labels)`
- **饼图**：`plt.pie(sizes, labels=labels, colors=colors)`
- **茎叶图**：`plt.stem(x, y, linefmt='C0-', markerfmt='C0o')`
- **阶梯图**：`plt.step(x, y, where='mid')`
- **参考线**：`plt.axhline(y=0)`、`plt.axvline(x=5)`
- **文本与标注**：`plt.text()`、`plt.annotate()`
- **图像显示**：`plt.imshow(data, cmap='viridis')`
- **对数坐标**：`plt.xscale('log')`、`plt.yscale('log')`、`plt.loglog()`
- **双轴**：`ax2 = ax1.twinx()`
- **Line2D API**：`line.set_color()`、`line.set_linewidth()`、`line.set_marker()` 等
- **多边形填充**：`plt.fill()`、`plt.Polygon()`、`ax.add_patch()`

### 3D 可视化（2D 投影）
在所有平台（包括 Apple Silicon macOS）上均可正常工作：
```python
from demo.demo_pyqtgraph_3d import project_3d

px, py, pz = project_3d(X, Y, Z, azim=-50, elev=25)
plt.scatter(px, py, s=20, c=colors, cmap='viridis')
```

## 安装

```bash
# 必需依赖
pip install pyqtgraph numpy

# Qt 绑定（任选其一）
pip install PySide6   # 推荐
# 或：pip install PyQt6 PyQt5 PySide2
```

```bash
# 安装 ShenBi
git clone https://github.com/CodeOfMe/ShenBi.git
cd ShenBi
pip install -e .
```

## 运行环境

- Python >= 3.9
- pyqtgraph >= 0.13.0
- numpy >= 1.20
- Qt 绑定：PyQt5、PyQt6、PySide2 或 PySide6
- 可选：scikit-learn（数据集演示）、scipy（KDE/插值）

## 性能

ShenBi 继承 pyqtgraph 的多级性能优化：

- **自动降采样**：查看大数据集时，根据屏幕像素密度自动抽稀数据点
- **视口裁剪**：仅处理可见范围内的数据进行渲染
- **GPU 加速**：使用 OpenGL 后端时，顶点数据通过 VBO 上传到 GPU 进行硬件加速渲染
- **分段线渲染**：在合适时使用快速的 QPainter.drawLines()

CPU 渲染 100 万数据点约需 1 秒，GPU 上几乎瞬间完成。

## 架构

```
用户代码（matplotlib 风格 API）
        │
        ▼
   shenbi.pyplot  ──  状态式 API（plt.plot、plt.figure 等）
        │
        ▼
   ShenBiFigure   ──  封装 pyqtgraph GraphicsLayoutWidget
        │
        ▼
   ShenBiAxes     ──  封装 pyqtgraph PlotItem
        │
        ▼
   ShenBiLine2D   ──  封装 pyqtgraph PlotDataItem
        │
        ▼
   pyqtgraph      ──  高性能 Qt 渲染引擎
```

## 项目结构

```
ShenBi/
├── shenbi/
│   ├── __init__.py        # 包入口
│   ├── pyplot.py          # matplotlib 兼容状态 API（40+ 函数）
│   ├── figure.py          # ShenBiFigure 封装
│   ├── axes.py            # ShenBiAxes（30+ 方法）
│   ├── line.py            # ShenBiLine2D、ShenBiScatter 封装
│   ├── colors.py          # 颜色解析（CSS4、hex、RGB、tab10）
│   ├── cm.py              # Colormap 支持（24 种）
│   ├── utils.py           # 格式字符串解析、标记/线型规范化
│   ├── mplot3d.py         # 3D 绘图工具包（Axes3D）
│   └── tests/             # 单元测试
├── demo/
│   ├── demo_pyqtgraph_2d.py   # 20 个数据集可视化演示
│   ├── demo_pyqtgraph_3d.py   # 10 个 3D 投影演示
│   ├── tutorial.md            # 英文教程
│   ├── tutorial_cn.md         # 中文教程
│   └── output/                # 生成的 PNG + SVG 文件
├── README.md              # 英文文档
├── README_CN.md           # 中文文档
├── pyproject.toml         # 包配置
├── upload_pypi.sh         # PyPI 上传脚本（Linux/macOS）
└── upload_pypi.bat        # PyPI 上传脚本（Windows）
```

## 数据集演示

ShenBi 包含 30 个综合演示，使用真实标准数据集：

| 数据集 | 样本数 | 特征数 | 类别数 |
|--------|--------|--------|--------|
| Iris（鸢尾花） | 150 | 4 | 3 |
| Wine（葡萄酒） | 178 | 13 | 3 |
| Breast Cancer（乳腺癌） | 569 | 30 | 2 |
| Digits（手写数字） | 1,797 | 64 | 10 |
| Diabetes（糖尿病） | 442 | 10 | 1（回归） |

运行所有演示：
```bash
cd demo
python demo_pyqtgraph_2d.py   # 20 个 2D 演示
python demo_pyqtgraph_3d.py   # 10 个 3D 演示
```

## 许可证

GPLv3 — 完整文本见 [LICENSE](LICENSE)。
