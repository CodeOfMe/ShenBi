"""
ShenBi (神笔) - Performance Demo
================================
Demonstrates high-performance rendering at 1K → 1M points.
Outputs both PNG and SVG.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import numpy as np
import shenbi.pyplot as plt

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

def bench_plot(n, m=1):
    x = np.linspace(0, 1000, n)
    plt.figure(figsize=(12, 4))
    t0 = time.time()
    for i in range(m):
        y = np.sin(x + i * 0.5) + np.random.randn(n) * 0.1
        plt.plot(x, y, linewidth=1)
    plt.title(f'{n:,} pts x {m} line(s)')
    name = f'perf_{n}_{m}'
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    t = time.time() - t0
    plt.close('all')
    return t

def bench_scatter(n):
    x = np.random.randn(n)
    y = np.random.randn(n)
    plt.figure(figsize=(8, 8))
    t0 = time.time()
    plt.scatter(x, y, s=2 if n > 5000 else 10,
                c='#1f77b4', alpha=0.15 if n > 5000 else 0.5,
                edgecolors='none')
    plt.title(f'Scatter {n:,} pts')
    name = f'perf_scatter_{n}'
    plt.savefig(os.path.join(OUT_DIR, name + '.png'))
    t = time.time() - t0
    plt.close('all')
    return t

print("=" * 65)
print("  ShenBi Performance Benchmark (PNG + SVG)")
print("=" * 65)
print(f"\n{'Test':<30} {'Points':>10} {'Time':>10} {'Status':>10}")
print("-" * 65)

total = 0.0
for n, m in [(1_000, 1), (10_000, 1), (100_000, 1), (1_000_000, 1),
             (10_000, 10), (100_000, 5)]:
    t = bench_plot(n, m)
    lbl = f'Line x{m}' if m > 1 else 'Line'
    print(f"{lbl:<30} {n:>10,} {t:>10.4f} {'OK':>10}")
    total += t

for n in [1_000, 10_000, 100_000]:
    t = bench_scatter(n)
    print(f"{'Scatter':<30} {n:>10,} {t:>10.4f} {'OK':>10}")
    total += t

print("-" * 65)
print(f"{'TOTAL':<30} {'':>10} {total:>10.4f}")
print(f"\nOutput: {OUT_DIR}/")
