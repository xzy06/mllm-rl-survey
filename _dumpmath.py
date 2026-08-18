# -*- coding: utf-8 -*-
"""提取二稿.docx 第 3 章段落完整文本（含 m:oMath 公式内的文本）"""
import sys, io
from docx import Document
from docx.oxml.ns import qn

out = []

doc = Document('二稿.docx')
M = qn('m:t')  # math text

def para_text_full(p):
    """提取段落全部文本：w:t 普通文本 + m:t 公式文本（用 ⟦ ⟧ 标记公式边界）"""
    parts = []
    for child in p._p.iter():
        if child.tag == qn('w:t'):
            parts.append(child.text or '')
        elif child.tag == M:
            parts.append('⟦' + (child.text or '') + '⟧')
    return ''.join(parts)

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if 28 <= i <= 36:
        out.append(f'[{i}] {para_text_full(p)}')
        out.append('---')

with open('_math.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written')
