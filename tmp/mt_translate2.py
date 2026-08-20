# -*- coding: utf-8 -*-
"""Phase 2: finish remaining segments - MyMemory first (gtx is rate-limited),
single gtx attempt per segment as opportunistic retry. Verbatim MT output, cache-aware."""
import json, time, random, urllib.request, urllib.parse

SEGS = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\segments.json"
OUT = r"C:\Users\Lenovo\Desktop\study\essay\mllm-rl-survey\tmp\translations.json"
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def gtx(text):
    data = urllib.parse.urlencode({'client': 'gtx', 'sl': 'zh-CN', 'tl': 'en', 'dt': 't', 'q': text}).encode('utf-8')
    req = urllib.request.Request('https://translate.googleapis.com/translate_a/single', data=data,
                                 headers={'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode('utf-8'))
    return ''.join(seg[0] for seg in payload[0] if seg[0])

def mm_one(text):
    url = 'https://api.mymemory.translated.net/get?' + urllib.parse.urlencode({'q': text, 'langpair': 'zh-CN|en'})
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    t = data['responseData']['translatedText']
    if data.get('responseStatus') != 200 or (isinstance(t, str) and 'MYMEMORY WARNING' in t.upper()):
        raise RuntimeError('mymemory err: ' + str(t)[:100])
    return t

def mymemory(text):
    if len(text) <= 480:
        return mm_one(text)
    pieces, cur = [], ''
    for ch in text:
        cur += ch
        if ch in '。；？！\n' and len(cur) > 200:
            pieces.append(cur); cur = ''
    if cur: pieces.append(cur)
    return ' '.join(mm_one(p) for p in pieces if p.strip())

def main():
    segs = json.load(open(SEGS, encoding='utf-8'))
    cache = json.load(open(OUT, encoding='utf-8'))
    remaining = [s for s in segs if not cache.get(f"{s['p']}:{s['c']}", {}).get('en')]
    print(f'remaining: {len(remaining)}')
    ok = fail = 0
    for s in remaining:
        key = f"{s['p']}:{s['c']}"
        en = None; engine = None
        # opportunistic single gtx try
        try:
            en = gtx(s['text']); engine = 'gtx'
        except Exception:
            pass
        if en is None:
            for att in range(3):
                try:
                    en = mymemory(s['text']); engine = 'mymemory'
                    break
                except Exception as e:
                    print(f'  mm retry {att+1}: {str(e)[:80]}', flush=True)
                    time.sleep(2 + att * 2)
        if en is None:
            print(f"FAILED {key}: {s['text'][:50]}", flush=True)
            fail += 1
            continue
        cache[key] = {'zh': s['text'], 'en': en, 'engine': engine}
        ok += 1
        time.sleep(0.6)
    json.dump(cache, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    total = sum(1 for s in segs if cache.get(f"{s['p']}:{s['c']}", {}).get('en'))
    print(f'phase2 ok={ok} fail={fail}; total cached {total}/{len(segs)}')

if __name__ == '__main__':
    main()
