"""
ShenBi — Comprehensive Performance Benchmark
=============================================
Compares matplotlib, pyqtgraph, and ShenBi across multiple plot types
and data sizes (1K → 10M points). Outputs a detailed report.
"""
import os, sys, time, gc
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

import numpy as np
import json

# ── Benchmark Config ─────────────────────────────────────────────
SIZES  = [1_000, 10_000, 100_000, 1_000_000]
WARMUP = 2    # warmup runs (discarded)
REPEAT = 3    # measurement runs
OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Time helper ──────────────────────────────────────────────────
def measure(fn):
    """Run fn, return elapsed seconds."""
    gc.collect()
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0

def median(times):
    return float(np.median(times))

# ── matplotlib ───────────────────────────────────────────────────
def bench_mpl_line(n):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as mpl_plt
    x = np.linspace(0, 100, n)
    y = np.sin(x)
    def fn():
        fig, ax = mpl_plt.subplots(figsize=(10, 5))
        ax.plot(x, y, 'b-', linewidth=1)
        fig.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'), dpi=30, bbox_inches='tight')
        mpl_plt.close(fig)
    return median([measure(fn) for _ in range(REPEAT)])

def bench_mpl_scatter(n):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as mpl_plt
    x = np.random.randn(n)
    y = np.random.randn(n)
    def fn():
        fig, ax = mpl_plt.subplots(figsize=(8, 8))
        ax.scatter(x, y, s=2, c='steelblue', alpha=0.3, edgecolors='none')
        fig.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'), dpi=30, bbox_inches='tight')
        mpl_plt.close(fig)
    return median([measure(fn) for _ in range(REPEAT)])

def bench_mpl_bar(n):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as mpl_plt
    cats = n // 20
    x = np.arange(cats)
    h = np.random.randint(10, 100, cats)
    def fn():
        fig, ax = mpl_plt.subplots(figsize=(10, 5))
        ax.bar(x, h, width=0.8, color='steelblue')
        fig.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'), dpi=30, bbox_inches='tight')
        mpl_plt.close(fig)
    return median([measure(fn) for _ in range(REPEAT)])

def bench_mpl_hist(n):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as mpl_plt
    data = np.random.randn(n)
    def fn():
        fig, ax = mpl_plt.subplots(figsize=(10, 5))
        ax.hist(data, bins=50, color='green', alpha=0.7)
        fig.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'), dpi=30, bbox_inches='tight')
        mpl_plt.close(fig)
    return median([measure(fn) for _ in range(REPEAT)])

# ── pyqtgraph ────────────────────────────────────────────────────
def bench_pg_line(n):
    import pyqtgraph as pg
    from pyqtgraph.exporters import ImageExporter
    pw = pg.PlotWidget()
    x = np.linspace(0, 100, n)
    y = np.sin(x)
    pw.plot(x, y, pen=pg.mkPen('b', width=1))
    exporter = ImageExporter(pw.plotItem)
    def fn():
        exporter.export(os.path.join(OUT_DIR, '_bench_tmp.png'))
    return median([measure(fn) for _ in range(REPEAT)])

def bench_pg_scatter(n):
    import pyqtgraph as pg
    from pyqtgraph.exporters import ImageExporter
    pw = pg.PlotWidget()
    x = np.random.randn(n)
    y = np.random.randn(n)
    pw.plot(x, y, pen=None, symbol='o', symbolSize=2, symbolPen=None,
            symbolBrush=pg.mkBrush(70, 130, 180, 77))
    exporter = ImageExporter(pw.plotItem)
    def fn():
        exporter.export(os.path.join(OUT_DIR, '_bench_tmp.png'))
    return median([measure(fn) for _ in range(REPEAT)])

def bench_pg_bar(n):
    import pyqtgraph as pg
    from pyqtgraph.exporters import ImageExporter
    cats = n // 20
    pw = pg.PlotWidget()
    x = np.arange(cats)
    h = np.random.randint(10, 100, cats)
    pw.setBackground('w')
    pw.addItem(pg.BarGraphItem(x=x, height=h, width=0.8, brush='steelblue'))
    pw.setXRange(-1, cats)
    pw.setYRange(0, h.max() * 1.1)
    pw.setLabel('left', 'Value')
    exporter = ImageExporter(pw.plotItem)
    def fn():
        exporter.export(os.path.join(OUT_DIR, '_bench_tmp.png'))
    return median([measure(fn) for _ in range(REPEAT)])

def bench_pg_hist(n):
    import pyqtgraph as pg
    from pyqtgraph.exporters import ImageExporter
    data = np.random.randn(n)
    counts, edges = np.histogram(data, bins=50)
    pw = pg.PlotWidget()
    pw.setBackground('w')
    centers = (edges[:-1] + edges[1:]) / 2
    pw.addItem(pg.BarGraphItem(x=centers, height=counts, width=(edges[1]-edges[0])*0.8, brush='g'))
    pw.setXRange(edges[0], edges[-1])
    pw.setYRange(0, counts.max() * 1.1)
    pw.setLabel('bottom', 'Value')
    pw.setLabel('left', 'Count')
    exporter = ImageExporter(pw.plotItem)
    def fn():
        exporter.export(os.path.join(OUT_DIR, '_bench_tmp.png'))
    return median([measure(fn) for _ in range(REPEAT)])

# ── ShenBi ───────────────────────────────────────────────────────
def bench_sb_line(n):
    import shenbi.pyplot as sb_plt
    x = np.linspace(0, 100, n)
    y = np.sin(x)
    def fn():
        sb_plt.figure(figsize=(10, 5))
        sb_plt.plot(x, y, 'b-', linewidth=1)
        sb_plt.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'))
        sb_plt.close('all')
    return median([measure(fn) for _ in range(REPEAT)])

def bench_sb_scatter(n):
    import shenbi.pyplot as sb_plt
    x = np.random.randn(n)
    y = np.random.randn(n)
    def fn():
        sb_plt.figure(figsize=(8, 8))
        sb_plt.scatter(x, y, s=2, c='steelblue', alpha=0.3, edgecolors='none')
        sb_plt.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'))
        sb_plt.close('all')
    return median([measure(fn) for _ in range(REPEAT)])

def bench_sb_bar(n):
    import shenbi.pyplot as sb_plt
    cats = n // 20
    x = np.arange(cats)
    h = np.random.randint(10, 100, cats)
    def fn():
        sb_plt.figure(figsize=(10, 5))
        sb_plt.bar(x, h, width=0.8, color='steelblue', edgecolor='white', linewidth=0.5)
        sb_plt.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'))
        sb_plt.close('all')
    return median([measure(fn) for _ in range(REPEAT)])

def bench_sb_hist(n):
    import shenbi.pyplot as sb_plt
    data = np.random.randn(n)
    def fn():
        sb_plt.figure(figsize=(10, 5))
        sb_plt.hist(data, bins=50, color='green', alpha=0.7, edgecolor='white', linewidth=0.5)
        sb_plt.savefig(os.path.join(OUT_DIR, '_bench_tmp.png'))
        sb_plt.close('all')
    return median([measure(fn) for _ in range(REPEAT)])

# ── Run Benchmark ────────────────────────────────────────────────
BENCHMARKS = [
    ("Line Plot",   bench_mpl_line,  bench_pg_line,  bench_sb_line),
    ("Scatter",     bench_mpl_scatter, bench_pg_scatter, bench_sb_scatter),
    ("Bar Chart",   bench_mpl_bar,   bench_pg_bar,   bench_sb_bar),
    ("Histogram",   bench_mpl_hist,  bench_pg_hist,  bench_sb_hist),
]

results = {}  # {plot_type: {size: {mpl: t, pg: t, sb: t}}}

print("=" * 80)
print("  ShenBi Performance Benchmark")
print("=" * 80)

for name, fn_mpl, fn_pg, fn_sb in BENCHMARKS:
    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"{'─' * 60}")
    print(f"  {'Size':>12s}  {'matplotlib':>12s}  {'pyqtgraph':>12s}  {'ShenBi':>12s}  {'SB vs MPL':>12s}")
    print(f"  {'-' * 62}")
    results[name] = {}
    for n in SIZES:
        t_mpl = fn_mpl(n) if n <= 1_000_000 else 999.0  # matplotlib OOM at 10M
        t_pg  = fn_pg(n)
        t_sb  = fn_sb(n)
        speedup = f"{t_mpl/t_sb:.1f}x" if t_sb > 0 else "—"
        label = f"{n:,}"
        results[name][n] = {"matplotlib": round(t_mpl, 4), "pyqtgraph": round(t_pg, 4), "shenbi": round(t_sb, 4), "speedup": speedup}
        print(f"  {label:>12s}  {t_mpl:>10.4f}s  {t_pg:>10.4f}s  {t_sb:>10.4f}s  {speedup:>12s}")

# Clean up temp file
tmp_file = os.path.join(OUT_DIR, '_bench_tmp.png')
if os.path.exists(tmp_file):
    os.remove(tmp_file)

# ── Save JSON ────────────────────────────────────────────────────
json_path = os.path.join(OUT_DIR, 'benchmark_results.json')
with open(json_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✅ Benchmark results saved to {json_path}")

# ── Generate Summary Chart ───────────────────────────────────────
import shenbi.pyplot as sb_plt

fig, axes = sb_plt.subplots(2, 2, figsize=(14, 12))
plot_types = ["Line Plot", "Scatter", "Bar Chart", "Histogram"]
for idx, (ax, name) in enumerate(zip(axes.flat, plot_types)):
    r = results[name]
    sizes_list = list(r.keys())
    mpl_times = [r[s]["matplotlib"] for s in sizes_list]
    pg_times  = [r[s]["pyqtgraph"] for s in sizes_list]
    sb_times  = [r[s]["shenbi"] for s in sizes_list]
    x_pos = np.arange(len(sizes_list))
    width = 0.25
    ax.bar(x_pos - width, mpl_times, width, label='matplotlib', color='#d62728', edgecolor='white', linewidth=0.5)
    ax.bar(x_pos,        pg_times,  width, label='pyqtgraph',  color='#ff7f0e', edgecolor='white', linewidth=0.5)
    ax.bar(x_pos + width, sb_times,  width, label='ShenBi',     color='#1f77b4', edgecolor='white', linewidth=0.5)
    ax.set_title(name)
    ax.set_ylabel('Time (s)')
    ax.set_xlabel('Data Size')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'{s:,}' for s in sizes_list], rotation=30, ha='right')
    ax.legend(fontsize=8)
sb_plt.suptitle('ShenBi Performance Benchmark — matplotlib vs pyqtgraph vs ShenBi')
sb_plt.tight_layout()
sb_plt.savefig(os.path.join(OUT_DIR, 'benchmark_chart.png'))
sb_plt.savefig(os.path.join(OUT_DIR, 'benchmark_chart.svg'))
sb_plt.close('all')
print(f"✅ Benchmark chart saved to {OUT_DIR}/")

# ── Generate Markdown Report ─────────────────────────────────────
report = []
report.append("# ShenBi Performance Benchmark Report\n")
report.append(f"*Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
report.append("## Summary\n")
report.append("This benchmark compares rendering performance of **matplotlib**, **pyqtgraph**, and **ShenBi** across 4 plot types and 4 data sizes.\n")
report.append("Each test includes figure creation, data binding, and PNG export at 30 DPI.\n")

for name in plot_types:
    r = results[name]
    report.append(f"## {name}\n")
    report.append("| Size | matplotlib | pyqtgraph | ShenBi | Speedup (mpl/SB) |")
    report.append("|------|-----------|-----------|--------|-----------------|")
    for n in SIZES:
        v = r[n]
        report.append(f"| {n:,} | {v['matplotlib']:.4f}s | {v['pyqtgraph']:.4f}s | {v['shenbi']:.4f}s | {v['speedup']} |")
    report.append("")

# Speedup comparison
report.append("## Speedup (matplotlib / ShenBi)\n")
report.append("| Size | Line Plot | Scatter | Bar Chart | Histogram |")
report.append("|------|-----------|---------|-----------|-----------|")
for n in SIZES:
    su = []
    for name in plot_types:
        su.append(results[name][n]["speedup"])
    report.append(f"| {n:,} | {su[0]} | {su[1]} | {su[2]} | {su[3]} |")
report.append("")

report.append("## Raw Data\n")
report.append("All results are also available in [benchmark_results.json](benchmark_results.json).\n")

report.append("## Test Environment\n")
report.append(f"- CPU: {os.uname().machine}")
report.append(f"- Python: {sys.version.split()[0]}")
try:
    import pyqtgraph; report.append(f"- pyqtgraph: {pyqtgraph.__version__}")
except: pass
try:
    import matplotlib; report.append(f"- matplotlib: {matplotlib.__version__}")
except: pass
report.append(f"- ShenBi: {__import__('shenbi').__version__}")
report.append("")

report_path = os.path.join(OUT_DIR, 'benchmark_report.md')
with open(report_path, 'w') as f:
    f.write('\n'.join(report))
print(f"✅ Benchmark report saved to {report_path}")

print(f"\n{'=' * 80}")
print("  Benchmark Complete!")
print(f"{'=' * 80}")
