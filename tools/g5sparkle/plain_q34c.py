#!/usr/bin/env python3
"""Q3-Q4 audit, plain-language round 3 (Nov 25 2026, Bethany: "do your recommended fixes for long steps").
Wording and folds only; no graded item, answer or key changes; poems and primary-source steps stay long on purpose.
1. What Good Readers Do intros over 55 words (weeks 18-30) keep their first and last sentences (the last names what to watch for).
2. Day 4 Grammar "Last day..." explanations (weeks 19-23; week 24's history nuance kept whole) keep their first three sentences (the prompt and the first line of the explanation).
3. 25.1: the Gold Rush background passage is split into its own sections (one step each, nothing cut); Alex's example plan is folded.
    python tools/g5sparkle/plain_q34c.py [--apply]"""
import io, re, sys, glob, html
def words(t): return len(re.findall(r"[A-Za-z’'&;]+", re.sub(r'<[^>]+>', '', t)))
def sents(t):
    parts = re.split(r'(?<=[.!?])(?:&rdquo;|”)?\s+(?=[A-Z&<“])', t)
    out = []
    for p in parts:
        if out and re.search(r'\b(Ch|Mr|Mrs|Dr|St)\.$', out[-1]): out[-1] += ' ' + p
        else: out.append(p)
    return out
WG = re.compile(r'(What Good Readers Do</div>\s*<div class="activity-sub">[^<]*</div>(?:\s*</div>){2}\s*<div class="activity-body">\s*<p>)(.*?)(</p>)', re.S)
LAST = re.compile(r'(<p>)(Last day(?: of the unit)?\. Now <strong>explain</strong>.*?)(</p>)', re.S)
report = []
def trim_wg(m, f):
    body = m.group(2)
    if words(body) <= 55: return m.group(0)
    ss = sents(body)
    if len(ss) < 3: return m.group(0)
    new = ss[0] + ' ' + ss[-1]
    report.append((f, 'WGRD', words(body), words(new), html.unescape(re.sub('<[^>]+>', '', new))))
    return m.group(1) + new + m.group(3)
def trim_last(m, f):
    ss = sents(m.group(2))
    if len(ss) <= 3: return m.group(0)
    new = ' '.join(ss[:3])
    report.append((f, 'LASTDAY', words(m.group(2)), words(new), html.unescape(new)))
    return m.group(1) + new + m.group(3)
out = {}
for f in sorted(glob.glob('lesson-*.html')):
    m = re.match(r'lesson-(\d+)-(\d)-', f)
    if not m or not 18 <= int(m.group(1)) <= 30: continue
    s = io.open(f, encoding='utf-8', newline='').read(); o = s
    s = WG.sub(lambda mm: trim_wg(mm, f), s, count=1)
    if int(m.group(1)) <= 23: s = LAST.sub(lambda mm: trim_last(mm, f), s)
    if s != o: out[f] = (o, s)
# 25.1
f = 'lesson-25-1-btghs.html'
o, s = out.get(f, (None, io.open(f, encoding='utf-8', newline='').read()))
o = o or s
def dwalk(t, i):
    d = 0
    for mm in re.finditer(r'<div\b|</div>', t[i:]):
        d += 1 if mm.group(0) == '<div' else -1
        if d == 0: return i + mm.end()
i = s.find('<div class="passage-text">', s.find('Background Knowledge Passage')); e = dwalk(s, i)
seg = s[i:e]; heads = re.findall(r'<p><strong>[^<]*</strong></p>', seg)
assert len(heads) == 5
for h in heads[1:]:
    seg = seg.replace(h, '</div>\n        </div>\n        <div class="passage-block">\n        <div class="passage-text">\n          ' + h, 1)
s = s[:i] + seg + s[e:]
report.append((f, 'PASSAGE', 594, 0, 'Gold Rush background split into 5 sections, nothing cut'))
k = s.find('<div class="key-concept">\n        <div class="key-concept-label" style="color:#8B5E0A;">👀 Watch How &mdash; Meet Alex, our example writer</div>')
assert k > 0
e = dwalk(s, k); body = s[k:e]
body = body.replace('<div class="key-concept-label" style="color:#8B5E0A;">👀 Watch How &mdash; Meet Alex, our example writer</div>',
    '<details><summary class="key-concept-label" style="color:#8B5E0A;cursor:pointer;">👀 Watch How &mdash; Meet Alex, our example writer (tap to open)</summary>', 1)
body = body[:-len('</div>')] + '</details></div>'
s = s[:k] + body + s[e:]
report.append((f, 'ALEX', 0, 0, "Alex's example plan folded"))
out[f] = (o, s)
for f, (o, s) in out.items():
    if o.count('<div') - o.count('</div') != s.count('<div') - s.count('</div'): sys.exit('div ' + f)
for r in report: print('%-34s %-8s %3d->%3d | %s' % (r[0][:34], r[1], r[2], r[3], r[4][:200]))
if '--apply' in sys.argv:
    for f, (o, s) in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('written', len(out))
