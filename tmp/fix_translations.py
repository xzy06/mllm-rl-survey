# -*- coding: utf-8 -*-
"""Word/term-level corrections to the MT cache (translations.json).
Strictly lexical swaps - no sentence rewriting. Then rebuild via build_en_v2."""
import json, re

P = r'C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\translations.json'
cache = json.load(open(P, encoding='utf-8'))

# ---- global term unification (ordered; longer phrases first) ----
SUBS = [
    # 组合 -> compositional (field standard; matches source's own parenthetical gloss)
    ('combinatorial inference', 'compositional reasoning'),
    ('Combinatorial inference', 'Compositional reasoning'),
    ('combinatoriality', 'compositionality'),
    ('combined ability', 'compositional ability'),
    ('combined reference value', 'compositional reference value'),
    ('combined reasoning', 'compositional reasoning'),
    ('combinatorial hints', 'compositional prompts'),
    ('combination reasoning', 'compositional reasoning'),
    ('combination binding', 'compositional binding'),
    ('combination benchmarks', 'compositional benchmarks'),
    ('combination benchmark', 'compositional benchmark'),
    ('combination capabilities', 'compositional capabilities'),
    ('combination defects', 'compositional defects'),
    ('combination structure', 'compositional structure'),
    ('combination understanding', 'compositional understanding'),
    ('combination correctness', 'compositional correctness'),
    ('combinatorial reasoning', 'compositional reasoning'),
    ('combinatorial structure', 'compositional structure'),
    ('combinatorial complexity', 'compositional complexity'),
    ('combinatorial conditions', 'compositional conditions'),
    ('combinatorial binding', 'compositional binding'),
    ('combinatorial understanding', 'compositional understanding'),
    ('combinatorial reach', 'compositional reach'),
    ('combination reach', 'compositional reach'),
    ('combination task', 'compositional task'),
    ('combinatorial benchmark', 'compositional benchmark'),
    ('combinatorial', 'compositional'),          # residual adjective
    ('Combination correctness', 'Compositional correctness'),
    # 验证器/验证 -> verifier/verification
    ('Validator', 'Verifier'), ('validator', 'verifier'),
    ('Validation', 'Verification'), ('validation', 'verification'),
    # 基座模型 -> base model
    ('Pedestal model', 'Base model'), ('pedestal model', 'base model'),
    # 思维链 -> chain-of-thought
    ('thought chain', 'chain-of-thought'), ('thinking chain', 'chain-of-thought'),
    # 策略(梯度) -> policy
    ('strategy gradient', 'policy gradient'), ('with the strategy', 'with the policy'),
    ('strategy optimization', 'policy optimization'),
    # 场景图 -> scene graph
    ('artificial scene graph annotation', 'manual scene-graph annotation'),
    ('artificial scene-graph', 'manual scene-graph'),
    ('scene map annotation', 'scene-graph annotation'),
    ('scene map', 'scene graph'), ('scene icons', 'scene-graph'),
    ('scene labeling', 'scene-graph labeling'),
    # 显著性 -> saliency
    ('significance level', 'saliency level'),
    # 通用 LVLM -> general
    ('Universal LVLM', 'general LVLM'),
    # 接地 -> grounding/grounded (targeted)
    ('Resolution + Ground', 'Resolution + grounding'),
    ('Ground IoU', 'grounded IoU'),
    # 论文 -> paper
    ('of the thesis', 'of the paper'),
    # 章节标题 探讨 -> Discussion
    ('4. Explore', '4. Discussion'),
    # 分解式 -> Decomposed
    ('Split verifiable rewards', 'Decomposed verifiable rewards'),
    # 梳理 -> reviews
    ('this paper combines the representative work', 'this paper reviews the representative work'),
    # 领域外 -> out-of-domain
    ('out-of-field degradation', 'out-of-domain degradation'),
    # 共指 -> coreference
    ('core-reference', 'coreference'),
    # 存在性 -> existence
    ('Strong presence', 'Strong existence'),
    # 去重 "area area"
    ('dividing bins by area area', 'dividing bins by area'),
    # 提升 -> improvement
    ('"promotion"', '"improvement"'), ('promotion', 'improvement'),
    # 蒙对
    ('mislead the compositional task', 'guess correctly on compositional tasks'),
    ('mislead the combination task', 'guess correctly on compositional tasks'),
    # 脑补 -> hallucinate
    ('make up for it', 'hallucinate'),
    # 节内小结 unify
    ('Summary of the section:', 'Section summary:'),
    # 对比预训练 -> contrastive
    ('comparative pre-training', 'contrastive pre-training'),
    # RL post-training 语序
    ('Post-reinforcement learning training', 'Reinforcement learning post-training'),
    ('post-training after reinforcement learning (RL)', 'reinforcement learning (RL) post-training'),
    # 沿用 -> Following
    ('Inherit GRPO', 'Following GRPO'),
    # 连续谱 -> continuous spectrum
    ('sequential spectra', 'continuous spectrum'),
    # 表头 奖励 bonus -> reward
    ('visual alignment bonus', 'visual alignment reward'),
    ('answer bonus', 'answer reward'),
    ('Count Bonus', 'count reward'),
    ('Intrinsic Benefits', 'Intrinsic advantage'),
    # 评测 -> Evaluation (table cell)
    ('Review does not explicitly cover', 'Evaluation does not explicitly cover'),
    # 镜像翻转问答对
    ('Mirror Flip Q&A Correct', 'Mirror-flip Q&A pairs'),
    # 较标准 GRPO
    ('More standard GRPO', 'vs. standard GRPO'),
    # VSR 等
    ('VSR et al. 7 benchmarks', '7 benchmarks incl. VSR'),
    # 三元组序列 phrase restore (garbled category list in [10:0])
    ('visual pairs Optimize the reward and inference process',
     'visual alignment reward and reasoning process optimization'),
]

# ---- per-key targeted (after global) ----
PERKEY = {
    '68:0': [('in', 'where')],         # 其中 ⟨M⟩ -> where ⟨M⟩ (standalone chunk)
    '77:0': [('in', 'where')],
    # restore the three-level distinction 是否正确/是否看对/是否合理推理
    '51:0': [('"whether it is correct", "whether it is correct"',
              '"whether it is correct", "whether it looks at the right evidence"')],
    '71:0': [('"whether it is correct", "whether it is correct"',
              '"whether it is correct", "whether it looks at the right evidence"')],
    '82:0': [('"whether it is correct", "whether it is correct"',
              '"whether it is correct", "whether it looks at the right evidence"')],
    '69:0': [('whether you see it right', 'whether it looks at the right evidence')],
    '211:0': [('just blinded', 'just guessed correctly'),
              ('looked at the graph', 'looked at the image'),
              ('artificial scene labeling', 'manual scene-graph labeling')],
    '188:0': [('Two-Layer Advantage', 'Two-level advantage')],
}

changed = 0
for k, v in cache.items():
    en = v['en']
    orig = en
    for a, b in SUBS:
        if a in en:
            en = en.replace(a, b)
    for a, b in PERKEY.get(k, []):
        if a in en:
            en = en.replace(a, b)
    if en != orig:
        v['en'] = en
        changed += 1
json.dump(cache, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'updated {changed} segments')

# report residuals
import re
res = []
for k, v in cache.items():
    en = v['en']
    for pat in [r'combinatorial', r'\bcombination\b', r'\bcombinations\b', r'pedestal', r'validator',
                r'\bstrategy\b', r'significance level', r'\bthesis\b', r'\bInherit\b']:
        if re.search(pat, en, re.I):
            res.append((k, pat, en[:80]))
print('--- residuals ---')
for k, pat, e in res:
    print(k, pat, '::', e)
