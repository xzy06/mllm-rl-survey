# -*- coding: utf-8 -*-
"""Batch machine translation of segments.json via web MT engines (no AI polishing).
Primary: Google Translate web endpoint (client=gtx) - classic neural MT engine.
Fallback: MyMemory web MT API.
Output is stored verbatim - no post-editing."""
import json, time, sys, re, urllib.request, urllib.parse, random

SEGS = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\segments.json"
OUT = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\translations.json"
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def gtx(text, sl='zh-CN', tl='en'):
    """Google Translate gtx endpoint - the classic MT engine used by the website."""
    data = urllib.parse.urlencode({'client': 'gtx', 'sl': sl, 'tl': tl, 'dt': 't', 'q': text}).encode('utf-8')
    req = urllib.request.Request('https://translate.googleapis.com/translate_a/single', data=data,
                                 headers={'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode('utf-8'))
    parts = [seg[0] for seg in payload[0] if seg[0]]
    return ''.join(parts)

def mymemory(text):
    """MyMemory MT API fallback (<=500 chars per call)."""
    if len(text) <= 480:
        url = 'https://api.mymemory.translated.net/get?' + urllib.parse.urlencode({'q': text, 'langpair': 'zh-CN|en'})
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
        t = data['responseData']['translatedText']
        if data.get('responseStatus') != 200 or (isinstance(t, str) and 'MYMEMORY WARNING' in t.upper()):
            raise RuntimeError('mymemory quota/err')
        return t
    # split long text at sentence enders
    pieces, cur = [], ''
    for ch in text:
        cur += ch
        if ch in '。；？！\n' and len(cur) > 200:
            pieces.append(cur); cur = ''
    if cur: pieces.append(cur)
    return ' '.join(mymemory(p) for p in pieces if p.strip())

def translate(text):
    for attempt in range(4):
        try:
            return ('gtx', gtx(text))
        except Exception as e:
            wait = 1.5 * (attempt + 1) + random.random()
            print(f'  gtx retry {attempt+1} after err: {e}', flush=True)
            time.sleep(wait)
    for attempt in range(2):
        try:
            return ('mymemory', mymemory(text))
        except Exception as e:
            print(f'  mymemory retry {attempt+1}: {e}', flush=True)
            time.sleep(2)
    return (None, None)

def main():
    segs = json.load(open(SEGS, encoding='utf-8'))
    try:
        cache = json.load(open(OUT, encoding='utf-8'))
    except FileNotFoundError:
        cache = {}
    ok = fail = 0
    engines = {'gtx': 0, 'mymemory': 0}
    for i, s in enumerate(segs):
        key = f"{s['p']}:{s['c']}"
        if key in cache and cache[key].get('en'):
            continue
        engine, en = translate(s['text'])
        if en is None:
            print(f"FAILED p{s['p']}c{s['c']}", flush=True)
            fail += 1
            continue
        cache[key] = {'zh': s['text'], 'en': en, 'engine': engine}
        engines[engine] = engines.get(engine, 0) + 1
        ok += 1
        if ok % 20 == 0:
            json.dump(cache, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'... {ok} translated ({engines})', flush=True)
        time.sleep(0.35)
    json.dump(cache, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'DONE ok={ok} fail={fail} engines={engines} cached={len(cache)}')

if __name__ == '__main__':
    main()
