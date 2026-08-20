# -*- coding: utf-8 -*-
"""Extract all paragraphs (incl. table cells) from 二稿.docx with structure info."""
import zipfile, json, sys
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = NS['w']

def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' or '\u3000' <= c <= '\u303f' or c in '，。；：？！（）“”‘’、—…《》' for c in s)

src = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\二稿.docx"
with zipfile.ZipFile(src) as z:
    xml = z.read('word/document.xml').decode('utf-8')

root = ET.fromstring(xml)
body = root.find(f'{{{W}}}body')

paras = []
def walk(container, in_table=False):
    for child in container:
        tag = child.tag.split('}')[1]
        if tag == 'p':
            texts = [t.text or '' for t in child.iter(f'{{{W}}}t')]
            full = ''.join(texts)
            # paragraph style
            style = ''
            pPr = child.find(f'{{{W}}}pPr')
            if pPr is not None:
                pStyle = pPr.find(f'{{{W}}}pStyle')
                if pStyle is not None:
                    style = pStyle.get(f'{{{W}}}val', '')
            # collect run info
            runs = []
            for r in child.findall(f'{{{W}}}r'):
                rt = ''.join(t.text or '' for t in r.findall(f'{{{W}}}t'))
                if rt:
                    runs.append(rt)
            # has drawing/image
            has_pic = child.find(f'.//{{{W}}}drawing') is not None or len(child.findall(f'.//{{{W}}}pict')) > 0
            paras.append({
                'idx': len(paras),
                'style': style,
                'in_table': in_table,
                'has_pic': has_pic,
                'n_runs': len(runs),
                'text': full,
                'cjk': has_cjk(full),
            })
        elif tag == 'tbl':
            walk(child, in_table=True)
        elif tag in ('sdt',):
            content = child.find(f'{{{W}}}sdtContent')
            if content is not None:
                walk(content, in_table=in_table)

walk(body)

out = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\paras.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(paras, f, ensure_ascii=False, indent=1)

n_all = len(paras)
n_text = sum(1 for p in paras if p['text'].strip())
n_cjk = sum(1 for p in paras if p['cjk'] and p['text'].strip())
n_tbl = sum(1 for p in paras if p['in_table'])
chars_cjk_text = sum(len(p['text']) for p in paras if p['cjk'])
print(f"total paragraphs: {n_all}")
print(f"non-empty: {n_text}")
print(f"with CJK (need translation): {n_cjk}")
print(f"in tables: {n_tbl}")
print(f"total chars in CJK paras: {chars_cjk_text}")
# styles distribution
from collections import Counter
c = Counter(p['style'] or '(none)' for p in paras)
print("styles:", dict(c))
