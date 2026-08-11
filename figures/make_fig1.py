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

# 方法：(x=时间[年], y=粒度刻度, 类别)
# 粒度刻度：1 答案级 / 2 结构级 / 3 区域级 / 4 物体级 / 5 步骤+证据级
methods = {
    'CR³':             (2025.20, 1.0, 'verifier'),
    'SpatialThinker':  (2025.40, 2.0, 'verifier'),
    'SVQA-R1':         (2025.80, 1.5, 'verifier'),
    'Ground-R1':       (2025.25, 3.0, 'grounded'),
    'GRIT':            (2025.50, 2.8, 'grounded'),
    'POLIA':           (2025.70, 4.0, 'grounded'),
    'Saliency-R1':     (2026.30, 4.5, 'grounded'),
    'Self-Questioning':(2025.90, 3.5, 'process'),
    'DLR':             (2026.10, 4.8, 'process'),
    'H-GRPO':          (2026.50, 5.0, 'process'),
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

# 时间轴
ax.set_xlim(2025.0, 2026.8)
ax.set_xticks([2025.0, 2025.5, 2026.0, 2026.5])
ax.set_xticklabels(['2025-01', '2025-07', '2026-01', '2026-07'], fontsize=11)
ax.set_xlabel('时间（示意）', fontsize=12)

# 三条水平网格线分隔粒度带
for v in (1.0, 2.0, 3.0, 4.0, 5.0):
    ax.axhline(v, color='#bbbbbb', lw=0.6, alpha=0.5, zorder=0)

legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color[c],
                 markersize=10, label=label[c]) for c in ('verifier', 'grounded', 'process')]
ax.legend(handles=legend, loc='upper left', fontsize=11, frameon=True, framealpha=0.95)

ax.set_title('图 1：奖励信号设计空间演化示意图（草稿）', fontsize=14, pad=12)
ax.text(0.5, -0.13,
        '时间与粒度位置为示意；三类方法作为并行分支持续细化，展示"结果验证→视觉对齐→过程优化"的关注点扩展而非线性继承。',
        transform=ax.transAxes, ha='center', fontsize=9.5, color='#555555')

fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(r'C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\figures\fig1_reward_signal_evolution.png',
            dpi=300, bbox_inches='tight')
print('saved fig1')
