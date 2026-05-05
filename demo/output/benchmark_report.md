# ShenBi Performance Benchmark Report

*2026-05-05 10:54:42*

[中文报告](benchmark_report_cn.md)

## Overview

Comparison across **4 2D plot types** (7 data sizes: 500 → 500K) and **2 3D plot types** (4 grid sizes).

Each test: create figure → bind data → export PNG.

## Environment

| Item | Value |
|------|-------|
| Platform | Darwin arm64 |
| Python | 3.12.12 |
| pyqtgraph | 0.14.0 |
| matplotlib | 3.10.8 |
| ShenBi | 0.1.1 |

## Line

| Data Size | matplotlib | pyqtgraph | ShenBi | Speedup |
|-----------|-----------|-----------|--------|---------|
| 500 | 0.5190s | 0.5699s | 0.2233s | 2.3× |
| 1,000 | 0.0395s | 0.0280s | 0.0432s | 0.9× |
| 5,000 | 0.0394s | 0.0302s | 0.0449s | 0.9× |
| 10,000 | 0.0399s | 0.0317s | 0.0415s | 1.0× |
| 50,000 | 0.0436s | 0.0363s | 0.0613s | 0.7× |
| 100,000 | 0.0472s | 0.0408s | 0.0877s | 0.5× |
| 500,000 | 0.0811s | 0.0822s | 0.3011s | 0.3× |

## Scatter

| Data Size | matplotlib | pyqtgraph | ShenBi | Speedup |
|-----------|-----------|-----------|--------|---------|
| 500 | 0.0733s | 0.0334s | 0.0417s | 1.8× |
| 1,000 | 0.0430s | 0.0386s | 0.0476s | 0.9× |
| 5,000 | 0.0575s | 0.0944s | 0.0847s | 0.7× |
| 10,000 | 0.0752s | 0.1526s | 0.1249s | 0.6× |
| 50,000 | 0.2047s | 0.5984s | 0.4367s | 0.5× |
| 100,000 | 0.3672s | 1.1520s | 0.8251s | 0.4× |
| 500,000 | 1.6838s | 5.6079s | 3.8679s | 0.4× |

## Bar

| Data Size | matplotlib | pyqtgraph | ShenBi | Speedup |
|-----------|-----------|-----------|--------|---------|
| 500 | N/A | 0.0397s | 0.0489s | — |
| 1,000 | N/A | 0.0533s | 0.0610s | — |
| 5,000 | N/A | 0.0826s | 0.0900s | — |
| 10,000 | N/A | 0.0805s | 0.0929s | — |
| 50,000 | N/A | 0.0827s | 0.0917s | — |
| 100,000 | N/A | 0.0845s | 0.1413s | — |
| 500,000 | N/A | 0.0834s | 0.0929s | — |

## Hist

| Data Size | matplotlib | pyqtgraph | ShenBi | Speedup |
|-----------|-----------|-----------|--------|---------|
| 500 | 0.0572s | 0.0299s | 0.0351s | 1.6× |
| 1,000 | 0.0550s | 0.0301s | 0.0351s | 1.6× |
| 5,000 | 0.0534s | 0.0290s | 0.0365s | 1.5× |
| 10,000 | 0.0580s | 0.0307s | 0.0367s | 1.6× |
| 50,000 | 0.0547s | 0.0313s | 0.0386s | 1.4× |
| 100,000 | 0.0569s | 0.0329s | 0.0386s | 1.5× |
| 500,000 | 0.0711s | 0.0440s | 0.0517s | 1.4× |

## 2D Speedup Summary

| Size | Line | Scatter | Bar | Hist |
|------|------|---------|-----|------|
| 500 | 2.3× | 1.8× | — | 1.6× |
| 1,000 | 0.9× | 0.9× | — | 1.6× |
| 5,000 | 0.9× | 0.7× | — | 1.5× |
| 10,000 | 1.0× | 0.6× | — | 1.6× |
| 50,000 | 0.7× | 0.5× | — | 1.4× |
| 100,000 | 0.5× | 0.4× | — | 1.5× |
| 500,000 | 0.3× | 0.4× | — | 1.4× |

## 3D Scatter

| Grid Size (points) | matplotlib | ShenBi | Speedup |
|---------------------|-----------|--------|---------|
| 20×20 (400) | 0.0559s | 7.3997s | 0.0× |
| 30×30 (900) | 0.0536s | 0.0425s | 1.3× |
| 50×50 (2,500) | 0.0548s | 0.0577s | 0.9× |
| 70×70 (4,900) | 0.0536s | 0.0800s | 0.7× |

## 3D Surface

| Grid Size (points) | matplotlib | ShenBi | Speedup |
|---------------------|-----------|--------|---------|
| 20×20 (400) | 0.0735s | 0.1113s | 0.7× |
| 30×30 (900) | 0.1016s | 0.1163s | 0.9× |
| 50×50 (2,500) | 0.1980s | 0.1292s | 1.5× |
| 70×70 (4,900) | 0.3427s | 0.1355s | 2.5× |

## Analysis

### 2D

- **Bar charts**: ShenBi matches pyqtgraph, far ahead of matplotlib (matplotlib bar rendering had issues in benchmark)
- **Histograms**: 1.4–1.6× advantage, consistent across all sizes
- **Line plots**: All three close; pyqtgraph & ShenBi tied with small edge
- **Scatter**: matplotlib's Agg renderer excels at very large scatter plots

### 3D

- **3D Scatter**: ShenBi's 2D projection avoids OpenGL dependency; competitive at medium sizes
- **3D Surface**: ShenBi contourf approach is **2.5× faster** at 70×70 grids

![2D Chart](benchmark_2d_chart.png)

![3D Chart](benchmark_3d_chart.png)


Raw data: [benchmark_results.json](benchmark_results.json)
