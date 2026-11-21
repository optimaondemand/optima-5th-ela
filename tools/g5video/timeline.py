import json, re, subprocess, sys
sys.path.insert(0, '.')
import os; V = __import__(os.environ.get("SPECS", "specs_wk19")).V  # SPECS=specs_wk20 python timeline.py ...
scripts = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/vid/scripts.json'))
def silences(f):
    o = subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','silencedetect=noise=-35dB:d=0.28','-f','null','-'],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', o)]; en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', o)]
    dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    return list(zip(st, en)), dur
out = {}
for key, spec in V.items():
    f = '/tmp/vid/%s.mp3' % key
    sil, dur = silences(f)
    text = re.sub(r'\[[^\]]*\]\s*', '', scripts[key])
    # speech intervals
    sp, cur = [], 0.0
    for a, b in sil:
        if a > cur: sp.append((cur, a))
        cur = b
    if cur < dur: sp.append((cur, dur))
    if sp and sp[-1][1]-sp[-1][0] < 0.05: sp.pop()
    S = sum(b-a for a,b in sp)
    ends = [b for a,b in sil] + [sp[0][0]]
    # boundaries after punctuation; DP-align each silence to a boundary
    B = [m.end() for m in re.finditer(r'[,.?!:;]\s+', text)]
    L = len(text)
    def lin(off):
        s = off / L * S
        for a, b in sp:
            if s <= b - a: return a + s
            s -= b - a
        return sp[-1][1]
    inner = [(a, b) for a, b in sil if a > sp[0][0] + 0.05 and b < dur - 0.05]
    n, m = len(B), len(inner)
    INF = 1e9; SKIP = 4.0
    # dp[i][j]: best cost using first i boundaries and first j silences
    dp = [[INF]*(m+1) for _ in range(n+1)]; bt = [[None]*(m+1) for _ in range(n+1)]
    dp[0][0] = 0
    for i in range(n+1):
        for j in range(m+1):
            c = dp[i][j]
            if c >= INF: continue
            if i < n and c < dp[i+1][j]: dp[i+1][j] = c; bt[i+1][j] = (i, j, None)            # boundary w/o pause
            if j < m and c + SKIP < dp[i][j+1]: dp[i][j+1] = c + SKIP; bt[i][j+1] = (i, j, None) # pause w/o boundary
            if i < n and j < m:
                cc = c + abs(lin(B[i]) - inner[j][0])
                if cc < dp[i+1][j+1]: dp[i+1][j+1] = cc; bt[i+1][j+1] = (i, j, 'm')
    i, j = n, m; pairs = []
    while (i, j) != (0, 0):
        pi, pj, k = bt[i][j]
        if k: pairs.append((B[pi], inner[pj]))
        i, j = pi, pj
    pairs.reverse()
    if key.endswith("rwm"): print([(text[b:b+12], round(a,2)) for b,(a,e) in pairs])
    # knots: (offset, time) ; a boundary at offset b: text before ends at sil start, after starts at sil end
    knots = [(0, sp[0][0])]
    for b, (a, e) in pairs: knots += [(b - 0.001, a), (b, e)]
    knots.append((L, sp[-1][1]))
    OV = {'g3ela-19-1-teach-vocab': {'Scheme has no prefix': 10.63, 'Guess the meaning': 27.81},
          'g3ela-19-1-teach-gram': {'Next, sort the word groups': 24.68},
          'g3ela-19-3-teach-morph': {'Then tap Check My Answers': 18.5},
          'g3ela-19-4-teach-spell': {'Bottle': 1.9, 'Count back three letters': 2.9, 't, l, e': 5.6, 'Bot, tle': 7.6, "That's the split": 9.2,
                                     'Tap Roll the dice': 10.5, 'Say the word out loud': 11.4, 'Then tap Check my answer': 16.4, 'Roll all six words': 17.5}}.get(key, {})
    WT = None
    try:
        from trim import align, words as _w
        al = align(f, text); ws = list(re.finditer(r"[A-Za-z0-9']+", text.replace('-', ' ')))
        if [a[0] for a in al] == [_w(m.group(0))[0] for m in ws]:
            WT = [(m.start(), a[1]) for m, a in zip(ws, al)]
    except SystemExit as e: print('  (no forced alignment:', e, ')')
    except Exception as e: print('  (no forced alignment:', type(e).__name__, ')')
    def t_of(anchor, off=None):
        if anchor is None: return None
        if WT and not OV:
            o = text.lower().find(anchor.lower()) if off is None else off
            assert o >= 0, (key, anchor)
            st = [t for p, t in WT if p >= o]
            return round(max(0, (st[0] if st else dur) - 0.1), 2)
        for k, v in OV.items():
            if anchor.lower().startswith(k.lower()) or k.lower().startswith(anchor.lower()): return v
        if off is None: off = text.lower().find(anchor.lower())
        assert off >= 0, (key, anchor)
        for (o1, t1), (o2, t2) in zip(knots, knots[1:]):
            if o1 <= off <= o2:
                t = t1 + (t2 - t1) * ((off - o1) / (o2 - o1) if o2 > o1 else 0); break
        return round(max(0, t - 0.1), 2)
    scenes = []
    for sc in spec['scenes']:
        t0 = t_of(sc['at']) if sc['at'] else 0.0
        items = [{'t': (t_of(a) if a else t0), 'html': h} for a, h in sc['items']]
        hl = [{'t': t_of(a), 'sel': s} for a, s in sc.get('hl', [])]
        scenes.append({'t': t0, 'items': items, 'hl': hl, 'layout': sc.get('layout', ''), 'dots': t_of(sc['dots']) if sc.get('dots') else None})
    caps = []
    for m in re.finditer(r'[^.?!:]+[.?!:]?', text):
        s = m.group(0).strip()
        if s: caps.append({'t': t_of(s[:25], m.start() + (len(m.group(0)) - len(m.group(0).lstrip()))) if m.start() else 0.0, 'text': s})
    # MERGE_SHORT: a caption of 3 letters or fewer (the S. of P.S.) joins the one before it
    for i in range(len(caps)-1, 0, -1):
        if len(caps[i]['text']) <= 3: caps[i-1]['text'] += caps[i]['text']; caps.pop(i)
    out[key] = {'title': spec['title'], 'sub': spec['sub'], 'dur': round(dur, 2), 'scenes': scenes, 'caps': caps, 'sil': sil}
    print(key, round(dur,1), 'aligned' if WT and not OV else 'pauses', [s['t'] for s in scenes])
json.dump(out, open('timeline.json', 'w'), ensure_ascii=False)
