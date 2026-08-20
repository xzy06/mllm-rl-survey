# -*- coding: utf-8 -*-
"""Round-2 corrections: sentence-level rewrites of broken MT segments (now approved),
remaining word/phrase swaps, and table-header / scale-unit / 无-case normalization.
All on translations.json; rebuild via build_en_v2 afterwards."""
import json, re

P = r'C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\translations.json'
cache = json.load(open(P, encoding='utf-8'))

# ---- 1. full rewrites of broken paragraphs (plain, faithful English; unified terms) ----
REWRITES = {
 '9:0': "A review of the representative work from 2024 to 2026 that uses RL to enhance MLLM compositional reasoning shows that its development is essentially a gradual expansion of reward signals from 'result verification' to 'visual semantic structure alignment' and 'reasoning process alignment', that is, an expansion of what the reward acts upon (answer -> visual structure -> reasoning process). Three directions have developed in parallel: one takes structured result verification of the final answer as the reward source (CR3, SpatialThinker, SVQA-R1); one takes the degree of alignment between the answer and the visual semantic structure as the reward source (Ground-R1, GRIT, POLIA); and one applies the optimization signal to the reasoning process itself (Self-Questioning VLM, H-GRPO). The deep driving force behind this evolution is the constraint that 'correctness must be definable' in compositional reasoning.",
 '15:0': "Focusing on the above abilities, the academic community has constructed a series of evaluation benchmarks. VALSE tests the model's judgment on language phenomena such as existence, counting, and spatial relations by constructing foiled examples [5]; CREPE expands the evaluation scale to 370,000 image-text pairs and systematically examines compositionality along the two dimensions of systematicity and productivity [1]; ARO covers three types of compositional structures, attributes, relations, and word order, with 50,000 cases, and reveals that existing retrieval benchmarks do not require compositional understanding, allowing models to score via shortcuts [2]; SugarCrepe addresses the problem that programmatic benchmarks are easily hacked by using an LLM to generate semantically reasonable hard negative samples, converging the evaluation into three atomic operations: Replace, Swap, and Add [3].",
 '205:0': "The three-way classification in Section 3.4 is convenient for description, but the granularity scale in Table 3 reveals a more essential fact: the three types of methods are not discrete categories but a continuous spectrum within the same reward design space. This judgment is supported mathematically: as stated in Section 2.2, under the token-level policy gradient with a single update, the standard GRPO objective is equivalent to the PRM-aware objective [11], so the result reward is already performing process-level credit assignment implicitly. A continuous hybrid form also appears at the method level: H-GRPO simultaneously contains both result verification and process matching signals, POLIA's external and internal advantages share a single loss function, and SVQA-R1's consistency penalty lies between a verifier and self-supervised alignment. The so-called 'evolution' is not a temporal succession with elimination, but a dimensional expansion of the reward design space: along the inference-expansion dimension it extends from the answer level (CR3) through the structure level (SpatialThinker) to the step level (H-GRPO), and along the visual-anchoring dimension it is refined from the region level (Ground-R1) to the object level (POLIA); the two dimensions are independent and not directly comparable, and each scale is still developing in parallel.",
 '200:0': "Note: all values in the table are reported by the original papers; 'improvement' and 'exceeds' both refer to absolute percentage points (including SVQA-R1's +30 points); GIoU is the grounded IoU. Because the base models, training data, and evaluation protocols differ across methods, the values cannot be directly compared horizontally (see Section 4.3).",
}
for k, en in REWRITES.items():
    cache[k]['en'] = en

# ---- 2. remaining word/phrase swaps ----
SWAPS = [
    ('frameless supervision', 'box-free supervision'),
    ('Choose one search', 'two-choice retrieval'),
    ('strengthening MLLM compositional reasoning', 'enhancing MLLM compositional reasoning'),
    ('cover combinations', 'cover compositional cases'),
    ('Strong existence', 'Strong on existence'),
    ('2.2 Main line of RL foundation and reward signal evolution',
     '2.2 RL background and the reward signal evolution thread'),
]
for k, v in cache.items():
    en = v['en']
    for a, b in SWAPS:
        if a in en:
            en = en.replace(a, b)
    # [35:0] 检索 -> Retrieval (table cell, was 'Search')
    if k == '35:0' and en.strip() == 'Search':
        en = 'Retrieval'
    v['en'] = en

# ---- 3. table header capitalization (first-letter) ----
CAPS = {
    '18:0': 'Benchmark', '21:0': 'Scale',
    '86:0': 'Visual alignment reward',
    '109:0': 'Method', '111:0': 'Signaling mechanism', '113:0': 'Incremental contribution layer',
}
for k, val in CAPS.items():
    cache[k]['en'] = val

# ---- 4. 万级 scale-unit unification ----
SCALE = {'31:0': '370K-level', '36:0': '50K-level', '41:0': '7.5K-level'}
for k, val in SCALE.items():
    cache[k]['en'] = val

# ---- 5. 无 case unification -> None ----
for k, v in cache.items():
    if v['en'].strip() == 'none':
        v['en'] = 'None'

json.dump(cache, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# scan for we/our/us (paper convention: avoid first person)
print('--- first-person scan ---')
for k, v in cache.items():
    for m in re.finditer(r'\b(we|our|us)\b', v['en'], re.I):
        ctx = v['en'][max(0,m.start()-25):m.end()+25]
        print(f'{k}: ...{ctx}...')
print('done; rewrites applied:', list(REWRITES))
