# ShenBi Performance Benchmark Report

*Generated: Tue  5 May 2026 10:32:57 CST*

[中文报告](benchmark_report_cn.md)

## Overview

Comprehensive performance comparison of **matplotlib**, **pyqtgraph**, and **ShenBi** across 4 plot types and 3 data sizes.

Each test includes: figure creation → data binding → PNG export at 30 DPI.


## Test Environment

| Item | Value |
|------|-------|
| Platform | Darwin arm64 |
| Python | 3.12.12 |
| pyqtgraph | 0.14.0 |
| matplotlib | 3.10.8 |
| ShenBi | 0.1.1 |

## Line Plot

| Data Size | matplotlib | pyqtgraph | ShenBi | Faster than mpl |
|-----------|-----------|-----------|--------|-----------------|
| 1,000 | 0.0413s | 0.0292s | 0.0337s | 1.2× |
| 10,000 | 0.0412s | 0.0312s | 0.0361s | 1.1× |
| 100,000 | 0.0567s | 0.0424s | 0.0479s | 1.2× |

## Scatter

| Data Size | matplotlib | pyqtgraph | ShenBi | Faster than mpl |
|-----------|-----------|-----------|--------|-----------------|
| 1,000 | 0.0398s | 0.0373s | 0.0447s | 0.9× |
| 10,000 | 0.0749s | 0.1445s | 0.1205s | 0.6× |
| 100,000 | 0.3764s | 1.1281s | 0.8295s | 0.5× |

## Bar Chart

| Data Size | matplotlib | pyqtgraph | ShenBi | Faster than mpl |
|-----------|-----------|-----------|--------|-----------------|
| 1,000 | 0.1094s | 0.0550s | 0.0635s | 1.7× |
| 10,000 | 0.2112s | 0.0845s | 0.0943s | 2.2× |
| 100,000 | 0.2210s | 0.0874s | 0.1175s | 1.9× |

## Histogram

| Data Size | matplotlib | pyqtgraph | ShenBi | Faster than mpl |
|-----------|-----------|-----------|--------|-----------------|
| 1,000 | 0.0739s | 0.0358s | 0.0456s | 1.6× |
| 10,000 | 0.0751s | 0.0313s | 0.0487s | 1.5× |
| 100,000 | 0.0734s | 0.0417s | 0.0518s | 1.4× |

## Speedup Summary (matplotlib ÷ ShenBi)

| Data Size | Line Plot | Scatter | Bar Chart | Histogram |
|-----------|-----------|---------|-----------|-----------|
| 1,000 | 1.2× | 0.9× | 1.7× | 1.6× |
| 10,000 | 1.1× | 0.6× | 2.2× | 1.5× |
| 100,000 | 1.2× | 0.5× | 1.9× | 1.4× |

## Analysis

### Where ShenBi Wins

- **Bar charts**: 1.7–2.2× faster — largest margin across all chart types
- **Histograms**: 1.4–1.6× faster — consistent advantage from pyqtgraph's fast BarGraphItem
- **Line plots**: 1.1–1.2× faster — benefiting from auto-downsampling

### Where matplotlib Wins

- **Scatter plots**: matplotlib's Agg renderer is highly optimised for scatter; ShenBi's pyqtgraph backend creates per-spot items that add overhead at large sizes

### Verdict

ShenBi provides matplotlib-compatible syntax with pyqtgraph-level performance.  
For bar charts, histograms, and line plots, ShenBi is faster.  
For scatter plots, matplotlib's native rendering is more efficient at >10K points.

![Benchmark Chart](benchmark_chart.png)


Raw data: [benchmark_results.json](benchmark_results.json)
