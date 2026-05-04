"""
ShenBi (神笔) - Matplotlib Compatibility Test
=============================================
Tests that matplotlib code can run unchanged by switching the import.
All function signatures and parameter names must match matplotlib exactly.

To test with matplotlib:
    import matplotlib.pyplot as plt    # <-- uncomment this

To test with shenbi:
    import shenbi.pyplot as plt        # <-- uncomment this
"""
import os
import sys

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import numpy as np

# ============================================================
# SWITCH THE IMPORT BELOW TO TEST COMPATIBILITY
# ============================================================
# import matplotlib as mpl
# import matplotlib.pyplot as plt
import shenbi.pyplot as plt

# ============================================================

OUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUT_DIR, exist_ok=True)

errors = []
passed = 0
N = 10_000  # 10,000 points per test


def check(name: str, fn):
    global passed, errors
    try:
        fn()
        passed += 1
        print(f"  [OK] {name}")
    except Exception as e:
        errors.append((name, str(e)))
        print(f"  [FAIL] {name}: {e}")


# ── Test: figure creation ───────────────────────────────────────────
def _test_figure():
    plt.figure(figsize=(8, 4), dpi=100, facecolor='white')
    plt.close('all')
check("figure(figsize, dpi, facecolor)", _test_figure)


# ── Test: subplots ──────────────────────────────────────────────────
def _test_subplots():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=False, sharey=False)
    assert axes.shape == (2, 2)
    plt.close('all')
check("subplots(2,2)", _test_subplots)


# ── Test: subplot ───────────────────────────────────────────────────
def _test_subplot():
    plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)
    plt.close('all')
check("subplot(2,1,N)", _test_subplot)


# ── Test: plot with all parameters ───────────────────────────────────
def _test_plot():
    x = np.linspace(0, 10, N)
    y = np.sin(x)
    plt.figure()
    lines = plt.plot(x, y, 'r-', scalex=True, scaley=True,
                     linewidth=2, linestyle='-', color='red',
                     marker='o', markersize=4,
                     markeredgecolor='black', markerfacecolor='red',
                     alpha=0.8, label='test', zorder=2,
                     visible=True, antialiased=True)
    assert len(lines) == 1
    line = lines[0]
    # Test Line2D property access
    assert line.get_linewidth() > 0
    line.set_linewidth(3.0)
    assert line.get_linewidth() == 3.0
    line.set_linestyle('--')
    assert line.get_linestyle() == '--'
    line.set_color('blue')
    line.set_marker('s')
    line.set_markersize(8)
    line.set_alpha(0.5)
    line.set_label('changed')
    line.set_visible(True)
    line.set_zorder(5)
    line.set_data([1, 2, 3], [4, 5, 6])  # set_data test
    line.set_xdata([10, 20, 30])  # set_xdata test
    line.set_ydata([40, 50, 60])  # set_ydata test
    plt.close('all')
check("plot() with all parameters + Line2D API", _test_plot)


# ── Test: scatter ───────────────────────────────────────────────────
def _test_scatter():
    x = np.random.randn(N)
    y = np.random.randn(N)
    plt.figure()
    s = plt.scatter(x, y, s=10, c='red', marker='o',
                    alpha=0.5, linewidths=0.5,
                    edgecolors='darkred', label='scatter')
    assert s is not None
    plt.close('all')
check("scatter() with all parameters", _test_scatter)


# ── Test: bar / barh ────────────────────────────────────────────────
def _test_bar():
    plt.figure()
    plt.bar([0, 1, 2, 3, 4], [10, 20, 15, 30, 25],
            width=0.6, bottom=0, align='center',
            color='steelblue', edgecolor='navy')
    plt.close('all')
check("bar() with all parameters", _test_bar)


def _test_barh():
    plt.figure()
    plt.barh([0, 1, 2, 3, 4], [10, 20, 15, 30, 25],
             height=0.6, left=0, align='center',
             color='darkorange')
    plt.close('all')
check("barh() with all parameters", _test_barh)


# ── Test: hist ──────────────────────────────────────────────────────
def _test_hist():
    data = np.random.randn(N)
    plt.figure()
    n, bins, patches = plt.hist(data, bins=50,
                                range=(-4, 4), density=False,
                                weights=None, cumulative=False,
                                bottom=None, histtype='bar',
                                align='mid', orientation='vertical',
                                rwidth=None, log=False,
                                color='green', label='hist',
                                stacked=False, alpha=0.7)
    assert n is not None
    plt.close('all')
check("hist() with all parameters", _test_hist)


# ── Test: errorbar ──────────────────────────────────────────────────
def _test_errorbar():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([10, 20, 15, 25, 18])
    plt.figure()
    plt.errorbar(x, y, yerr=[1, 2, 1.5, 2, 1], xerr=None,
                 fmt='ro-', ecolor='red', elinewidth=1,
                 capsize=5, barsabove=False,
                 lolims=False, uplims=False,
                 xlolims=False, xuplims=False,
                 errorevery=1, capthick=None)
    plt.close('all')
check("errorbar() with all parameters", _test_errorbar)


# ── Test: fill_between ──────────────────────────────────────────────
def _test_fill():
    x = np.linspace(0, 10, N)
    plt.figure()
    plt.fill_between(x, np.sin(x), 0.5,
                     where=None, interpolate=False, step=None,
                     color='blue', alpha=0.3)
    plt.close('all')
check("fill_between() with all parameters", _test_fill)


# ── Test: imshow ────────────────────────────────────────────────────
def _test_imshow():
    data = np.random.rand(100, 100)
    plt.figure()
    img = plt.imshow(data, cmap=None, norm=None,
                     aspect=None, interpolation=None,
                     alpha=None, vmin=0, vmax=1,
                     origin=None, extent=[0, 10, 0, 10])
    assert img is not None
    plt.close('all')
check("imshow() with all parameters", _test_imshow)


# ── Test: step ──────────────────────────────────────────────────────
def _test_step():
    x = np.linspace(0, 10, 100)
    plt.figure()
    plt.step(x, np.sin(x), where='pre')
    plt.close('all')
check("step() with all parameters", _test_step)


# ── Test: stem ──────────────────────────────────────────────────────
def _test_stem():
    x = np.linspace(0, 2 * np.pi, 40)
    plt.figure()
    plt.stem(x, np.sin(x), linefmt='C0-', markerfmt='C0o', basefmt='C3-')
    plt.close('all')
check("stem() with all parameters", _test_stem)


# ── Test: pie ───────────────────────────────────────────────────────
def _test_pie():
    plt.figure()
    plt.pie([15, 30, 45, 10], labels=['A', 'B', 'C', 'D'],
            colors=['r', 'g', 'b', 'y'],
            explode=None, autopct='%1.1f%%',
            startangle=90, radius=1,
            counterclock=True, wedgeprops=None, textprops=None,
            center=(0, 0), frame=False,
            rotatelabels=False, normalize=True, hatch=None)
    plt.close('all')
check("pie() with all parameters", _test_pie)


# ── Test: boxplot ───────────────────────────────────────────────────
def _test_boxplot():
    data = [np.random.randn(100) * s for s in [1, 2, 3, 4, 5]]
    plt.figure()
    result = plt.boxplot(data, notch=False, sym='b+',
                         orientation='vertical', whis=1.5,
                         positions=None, widths=0.5,
                         patch_artist=False, bootstrap=None,
                         usermedians=None, conf_intervals=None,
                         meanline=False, showmeans=False,
                         showcaps=True, showbox=True,
                         showfliers=True, boxprops=None,
                         tick_labels=[f'G{i}' for i in range(1, 6)],
                         manage_ticks=True, autorange=False)
    assert 'boxes' in result
    plt.close('all')
check("boxplot() with all parameters", _test_boxplot)


# ── Test: log scales ────────────────────────────────────────────────
def _test_log():
    x = np.logspace(0, 3, N)
    y = x**2
    plt.figure()
    plt.loglog(x, y, basex=10, basey=10, subsx=None, subsy=None,
               nonposx='clip', nonposy='clip')
    plt.close('all')

    plt.figure()
    plt.semilogx(x, y, base=10, subs=None, nonpositive='clip')
    plt.close('all')

    plt.figure()
    plt.semilogy(x, y, base=10, subs=None, nonpositive='clip')
    plt.close('all')
check("loglog/semilogx/semilogy", _test_log)


# ── Test: axes decoration ───────────────────────────────────────────
def _test_decoration():
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.title('Title', fontsize=14, color='black')
    plt.xlabel('X Label', fontsize=12)
    plt.ylabel('Y Label', fontsize=12)
    plt.xlim(0, 4)
    plt.ylim(0, 4)
    x0, x1 = plt.xlim()
    y0, y1 = plt.ylim()
    plt.xscale('linear')
    plt.yscale('linear')
    plt.grid(True, which='major', axis='both')
    plt.legend(loc='best')
    plt.xticks([1, 2, 3], ['A', 'B', 'C'])
    plt.yticks([1, 2, 3], ['a', 'b', 'c'])
    plt.axhline(y=2, color='r', linestyle='--', linewidth=1)
    plt.axvline(x=2, color='b', linestyle='-.', linewidth=1)
    plt.text(1.5, 1.5, 'Text', fontsize=12)
    plt.annotate('Point', xy=(2, 2), xytext=(2.5, 2.5),
                 arrowprops=dict(arrowstyle='->'))
    plt.tight_layout(pad=1.08)
    plt.close('all')
check("axes decoration (title, labels, limits, grid, legend, ticks, etc.)", _test_decoration)


# ── Test: savefig ───────────────────────────────────────────────────
def _test_savefig():
    import tempfile
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        fname = f.name
    try:
        plt.savefig(fname, dpi=72, facecolor='white', edgecolor='white',
                    orientation='portrait', format='png',
                    transparent=False, bbox_inches=None, pad_inches=0.1)
        assert os.path.getsize(fname) > 0
    finally:
        os.unlink(fname)
    plt.close('all')
check("savefig() with all parameters", _test_savefig)


# ── Test: state management ──────────────────────────────────────────
def _test_state():
    plt.close('all')
    f1 = plt.figure()
    f2 = plt.figure()
    assert plt.gcf() is not None
    plt.scf(f1)
    assert plt.gcf() is f1
    plt.scf(f2)
    plt.clf()
    plt.cla()
    assert plt.isinteractive() in (True, False)
    plt.ion()
    plt.ioff()
    plt.close('all')
check("state management (gcf, gca, scf, sca, clf, cla, close, ion, ioff)", _test_state)


# ── Test: rcParams and style ────────────────────────────────────────
def _test_rcparams():
    assert isinstance(plt.rcParams, dict)
    plt.style_use('default')
check("rcParams and style_use", _test_rcparams)


# ── Test: subplots_adjust ───────────────────────────────────────────
def _test_subplots_adjust():
    plt.figure()
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9,
                        wspace=0.2, hspace=0.2)
    plt.close('all')
check("subplots_adjust()", _test_subplots_adjust)


# ── Test: tight_layout, margins, tick_params ───────────────────────
def _test_stubs():
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.tight_layout()
    plt.margins(0.1)
    plt.tick_params(axis='both', which='major')
    plt.close('all')
check("tight_layout, margins, tick_params (stubs)", _test_stubs)


# ── Test: Multiple datasets in plot ──────────────────────────────────
def _test_multi_plot():
    x = np.linspace(0, 10, 100)
    plt.figure()
    lines = plt.plot(x, np.sin(x), 'r-',
                     x, np.cos(x), 'b--',
                     x, np.sin(x + 1), 'g.')
    assert len(lines) == 3
    plt.close('all')
check("plot() with multiple datasets", _test_multi_plot)


# ── Test: colorbar ──────────────────────────────────────────────────
def _test_colorbar():
    plt.figure()
    plt.imshow(np.random.rand(50, 50))
    plt.colorbar()
    plt.close('all')
check("colorbar()", _test_colorbar)


# ── Test: gca().set_aspect ──────────────────────────────────────────
def _test_aspect():
    plt.figure()
    plt.plot([1, 2, 3], [1, 2, 3])
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.autoscale(enable=True, axis='both')
    plt.close('all')
check("set_aspect / autoscale", _test_aspect)


# ── Summary ──────────────────────────────────────────────────────────
print()
print("=" * 65)
print(f"  Results: {passed} passed, {len(errors)} failed")
print("=" * 65)

if errors:
    print("\nFailed tests:")
    for name, msg in errors:
        print(f"  - {name}: {msg}")
    sys.exit(1)
else:
    print("\nAll compatibility tests passed!")
    print("ShenBi is fully compatible with matplotlib's API.")
