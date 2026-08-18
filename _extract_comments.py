# -*- coding: utf-8 -*-
"""提取 docx 批注"""
import zipfile, re, sys

out = []
for f in ['初稿带批注.docx', '综述报告feedback.docx']:
    out.append('=' * 25 + ' ' + f + ' ' + '=' * 25)
    with zipfile.ZipFile(f) as z:
        xml = z.read('word/comments.xml').decode('utf-8', errors='replace')
    for m in re.finditer(r'<w:comment\b[^>]*w:author="([^"]*)"[^>]*>(.*?)</w:comment>', xml, re.S):
        author, body = m.group(1), m.group(2)
        texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', body)
        out.append('--- {}: {}'.format(author, ''.join(texts)))

with open('_comments.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(out))
print('done, lines:', len(out))
