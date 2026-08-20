# -*- coding: utf-8 -*-
"""Shared doc-walk logic: split each paragraph into text chunks at math/drawing boundaries."""
from docx import Document
from docx.oxml.ns import qn

M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

def has_han(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

def para_chunks(p_el):
    """Return list of chunks. Each chunk = list of w:t elements (lxml), in document order.
    Chunks are split at math objects (m:oMath / m:oMathPara). Runs that carry no text
    (e.g. image runs) are neutral and belong to the current chunk but contribute no w:t."""
    chunks = []
    cur = []
    for child in p_el:
        tag = child.tag
        if tag == qn('w:pPr'):
            continue
        if tag == '{%s}oMath' % M_NS or tag == '{%s}oMathPara' % M_NS:
            if cur:
                chunks.append(cur)
                cur = []
            continue
        if tag == qn('w:r'):
            # inline math nested inside a run? check descendants
            has_math_desc = child.find('.//{%s}oMath' % M_NS) is not None
            if has_math_desc:
                if cur:
                    chunks.append(cur)
                    cur = []
                # text runs around math inside this run are unusual; collect non-math w:t
                for t in child.findall(qn('w:t')):
                    cur.append(t)
                if cur:
                    chunks.append(cur)
                    cur = []
                continue
            for t in child.findall(qn('w:t')):
                cur.append(t)
            # br/tab handling: treat as plain, ignore
        # other elements (bookmarks, proofErr, sdt run-level) ignored
    if cur:
        chunks.append(cur)
    return chunks

def chunk_text(ts):
    return ''.join(t.text or '' for t in ts)

def collect_segments(src_path):
    """Walk the document in order; return list of segments.
    Segment = {'p': p_index, 'c': chunk_index, 'text': str, 'ts': [w:t elements]}.
    Only chunks containing at least one Han character are segments."""
    doc = Document(src_path)
    body = doc.element.body
    segments = []
    p_idx = 0
    for p_el in body.iter(qn('w:p')):
        # skip paragraphs nested in math (rare) — w:p can't nest inside w:p except textboxes; fine
        chunks = para_chunks(p_el)
        for ci, ts in enumerate(chunks):
            txt = chunk_text(ts)
            if has_han(txt):
                segments.append({'p': p_idx, 'c': ci, 'text': txt, 'ts': ts})
        p_idx += 1
    return doc, segments
