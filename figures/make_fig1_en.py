# -*- coding: utf-8 -*-
"""Figure 1 (English): Reward-signal design-space evolution, dual-panel.
v2: fixes overlapping dots (Ground-R1/GRIT) and label/dot collisions via
per-point label offsets + light white label background."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# (name, x, y, category, label_dx, label_dy)  -- offsets in points
methods_a = [
    ('SVQA-R1',          2025.419, 1.0, 'verifier',   2,  -18),
    ('CR3',              2026.055, 1.0, 'verifier',   0,   10),
    ('SpatialThinker',   2025.860, 2.0, 'verifier',   0,   10),
    ('Self-Questioning', 2026.451, 2.0, 'process',    0,  -18),
    ('VisualPRM',        2025.200, 3.0, 'process',    10,   8),
    ('H-GRPO',           2026.492, 3.0, 'process',    0,   10),
]
methods_b = [
    ('GRIT',      2025.386, 0.75, 'grounded',   -2,  -18),   # lowered to avoid Ground-R1 overlap
    ('Ground-R1', 2025.400, 1.0,  'grounded',    2,   10),
    ('POLIA',     2026.511, 2.0,  'grounded',    0,   10),
    ('SAYO',      2026.100, 3.0,  'grounded',    0,   10),
]

color = {'verifier': '#1f6fb2', 'grounded': '#e08a2e', 'process': '#3d9a5f'}
label = {'verifier': '3.1 Result Verification', 'grounded': '3.2 Visual Alignment', 'process': '3.3 Process Optimization'}
ytickA = {1.0: 'Answer-level', 2.0: 'Structure-level', 3.0: 'Step-level'}
ytickB = {1.0: 'Region-level', 2.0: 'Object-level', 3.0: 'Attention'}
BBOX = dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.85)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(11.6, 6.1), dpi=240)
fig.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.16, wspace=0.34)

def panel(ax, methods, yticks, title):
    # faint parallel-branch guides
    cats_present = {c for *_, c, _, _ in methods}
    for cat in cats_present:
        pts = sorted([(x, y) for (_, x, y, c, _, _) in methods if c == cat])
        if len(pts) > 1:
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color=color[cat], alpha=0.35, lw=1.1, ls=(0, (4, 3)), zorder=1)
    # scatter
    for name, x, y, cat, _, _ in methods:
        ax.scatter(x, y, s=100, color=color[cat], edgecolor='white', linewidth=1.1, zorder=3)
    # labels with explicit offsets + white background to avoid dot overlap
    for name, x, y, cat, dx, dy in methods:
        ax.annotate(name, (x, y), textcoords='offset points', xytext=(dx, dy),
                    ha='center', va='center', fontsize=10.5, zorder=5, bbox=BBOX)
        if name == 'SVQA-R1':
            ax.annotate('(consistency)', (x, y), textcoords='offset points', xytext=(2, -34),
                        ha='center', va='center', fontsize=8.5, color='#666', zorder=5, bbox=BBOX)
    ax.set_yticks(list(yticks.keys()))
    ax.set_yticklabels(list(yticks.values()), fontsize=11)
    ax.set_ylim(0.2, 3.7)
    ax.set_xlim(2025.05, 2026.70)
    ax.set_xticks([2025.0, 2026.0])
    ax.set_xticklabels(['2025', '2026'], fontsize=11)
    ax.set_xlabel('Time', fontsize=12)
    for v in yticks.keys():
        ax.axhline(v, color='#cccccc', lw=0.6, alpha=0.5, zorder=0)
    ax.set_title(title, fontsize=10.5, loc='left', pad=8)

panel(axA, methods_a, ytickA, '(a) Inference Expansion: Answer-level  ->  Structure-level  ->  Step-level')
panel(axB, methods_b, ytickB, '(b) Visual Anchoring: Region-level  ->  Object-level  ->  Attention')

for ax, cats in ((axA, ('verifier', 'process')), (axB, ('grounded',))):
    handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color[c],
                      markersize=10, label=label[c]) for c in cats]
    ax.legend(handles=handles, loc='upper left', fontsize=10.5, frameon=True, framealpha=0.95)

fig.suptitle('Figure 1: Evolution of the reward-signal design space',
             fontsize=14, y=0.97, fontweight='bold')
fig.text(0.5, 0.045,
         'X-axis: first-public time (arXiv v1 or venue date); the three directions develop in parallel, '
         'representing an expansion of the design space rather than a linear succession.',
         ha='center', fontsize=9.5, color='#555', style='italic')

out = r'C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\figures\fig1_reward_signal_evolution_en.png'
fig.savefig(out, dpi=240, bbox_inches='tight')
print('saved', out)
