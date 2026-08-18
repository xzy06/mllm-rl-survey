# -*- coding: utf-8 -*-
"""图 1 草稿：奖励信号设计空间演化示意图（时间 × 粒度，三类并行分支）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.lines import Line2D

# 注册中文字体（Windows 微软雅黑）
try:
    fm.fontManager.addfont(r'C:\Windows\Fonts\msyh.ttc')
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
except Exception:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 方法：(x=首次公开时间[年小数], y=粒度刻度, 类别)
# 时间口径：arXiv 论文取 v1 提交日期；CR³/POLIA 未公开于 arXiv，分别取 AAAI 2026（2026-01-20）与 ICML 2026（2026-07-06）会议时间
# 粒度刻度：1 答案级 / 2 结构级 / 3 区域级 / 4 物体级 / 5 步骤+证据级
methods = {
    'CR³':             (2026.055, 1.0, 'verifier'),   # AAAI 2026 会议（无 arXiv）
    'SpatialThinker':  (2025.860, 2.0, 'verifier'),   # arXiv v1 2025-11-10
    'SVQA-R1':         (2025.419, 1.5, 'verifier'),   # arXiv v1 2025-06-02
    'Ground-R1':       (2025.400, 3.0, 'grounded'),   # arXiv v1 2025-05-26
    'GRIT':            (2025.386, 2.8, 'grounded'),   # arXiv v1 2025-05-21
    'POLIA':           (2026.511, 4.0, 'grounded'),   # ICML 2026 会议（无 arXiv）
    'Self-Questioning':(2026.451, 3.5, 'process'),    # arXiv v1 2026-06-14
    'H-GRPO':          (2026.492, 5.0, 'process'),    # arXiv v1 2026-06-29
}

color = {'verifier': '#1f6fb2', 'grounded': '#e08a2e', 'process': '#3d9a5f'}
label = {'verifier': '验证器奖励（结果验证）', 'grounded': '视觉对齐奖励', 'process': '推理过程优化'}

fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=300)

# 按类别连接成并行分支（浅色虚线，体现"并行而非线性继承"）
for cat in ('verifier', 'grounded', 'process'):
    pts = [(x, y) for (x, y, c) in methods.values() if c == cat]
    pts.sort()
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color[cat], alpha=0.35, lw=1.2, ls=(0, (4, 3)), zorder=1)

# 散点 + 标注
for name, (x, y, cat) in methods.items():
    ax.scatter(x, y, s=95, color=color[cat], edgecolor='white', linewidth=1.0, zorder=3)
    dy = 0.16 if y < 4.5 else -0.30
    ax.annotate(name, (x, y), textcoords='offset points',
                xytext=(0, 8 if dy > 0 else -14), ha='center', va='bottom',
                fontsize=10.5, zorder=4)

# 粒度刻度轴
gran = {1.0: '答案级', 2.0: '结构级', 3.0: '区域级', 4.0: '物体级', 5.0: '步骤+证据级'}
ax.set_yticks(list(gran.keys()))
ax.set_yticklabels(list(gran.values()), fontsize=11)
ax.set_ylim(0.4, 5.7)
ax.set_ylabel('奖励信号粒度', fontsize=12)

# 时间轴（真实首次公开时间）
ax.set_xlim(2025.30, 2026.62)
ax.set_xticks([2025.38, 2025.62, 2025.87, 2026.12, 2026.37, 2026.62])
ax.set_xticklabels(['2025-05', '2025-08', '2025-11', '2026-02', '2026-05', '2026-08'], fontsize=11)
ax.set_xlabel('首次公开时间（arXiv v1 / 会议）', fontsize=12)

# 三条水平网格线分隔粒度带
for v in (1.0, 2.0, 3.0, 4.0, 5.0):
    ax.axhline(v, color='#bbbbbb', lw=0.6, alpha=0.5, zorder=0)

legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color[c],
                 markersize=10, label=label[c]) for c in ('verifier', 'grounded', 'process')]
ax.legend(handles=legend, loc='upper left', fontsize=11, frameon=True, framealpha=0.95)

ax.set_title('图 1：奖励信号设计空间演化示意图', fontsize=14, pad=12)
ax.text(0.5, -0.13,
        '横轴为论文首次公开时间：arXiv 论文取 v1 提交日期；CR³（AAAI 2026）、POLIA（ICML 2026）未公开于 arXiv，取会议时间。\n三类方法作为并行分支持续细化，展示“结果验证→视觉对齐→过程优化”的关注点扩展而非线性继承。',
        transform=ax.transAxes, ha='center', fontsize=9.5, color='#555555')

fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(r'C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\figures\fig1_reward_signal_evolution.png',
            dpi=300, bbox_inches='tight')
print('saved fig1')
