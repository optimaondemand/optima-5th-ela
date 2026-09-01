# -*- coding: utf-8 -*-
"""Repair unbalanced <div> nesting *inside .activity blocks only*."""
import sys, os, re
sys.path.insert(0, os.path.expanduser('~/ela'))
import strand_tool as st

def mask(s):
    return re.sub(r'<script\b.*?</script>', lambda m: ' ' * len(m.group(0)), s, flags=re.S | re.I)

BOUND = r'<div class="activity[ "]|<div class="tab-next-wrap"|<div class="rwm-box"|<div class="gathered-card"|<div class="tab-panel"|<!--\s*/tab-\w+\s*-->'

def act_regions(s):
    m = mask(s)
    marks = [(x.start(), x.group(0)) for x in re.finditer(BOUND, m)]
    out = []
    for i, (a, g) in enumerate(marks):
        if not g.startswith('<div class="activity'):
            continue
        b = marks[i + 1][0] if i + 1 < len(marks) else len(s)
        out.append((a, b))
    return out

def net(s, a, b):
    seg = mask(s)[a:b]
    return len(re.findall(r'<div\b', seg)) - len(re.findall(r'</div>', seg))

def title(s, a):
    t = re.search(r'<div class="activity-title">(.*?)</div>', s[a:a + 900], re.S)
    return re.sub(r'&#x[0-9A-Fa-f]+;|<[^>]+>', '', t.group(1)).strip()[:38] if t else '?'

def repair(path):
    s = st.load(path); edits = []
    for _ in range(20):
        hit = None
        for a, b in act_regions(s):
            n = net(s, a, b)
            if n:
                hit = (a, b, n); break
        if not hit:
            break
        a, b, n = hit; t = title(s, a)
        if n > 0:
            ins = b
            while ins > a and s[ins - 1] in ' \n\t':
                ins -= 1
            s = s[:ins] + '\n  </div>' + s[ins:]
            edits.append('+1 </div> in "%s"' % t)
        else:
            seg = mask(s)[a:b]
            last = None
            for m in re.finditer(r'</div>', seg):
                last = m
            s = s[:a + last.start()] + s[a + last.end():]
            edits.append('-1 </div> in "%s"' % t)
    m = mask(s)
    bal = len(re.findall(r'<div\b', m)) - len(re.findall(r'</div>', m))
    return s, edits, bal

if __name__ == '__main__':
    B = os.path.expanduser('~/mnt/optima-5th-ela/')
    apply = '--apply' in sys.argv
    for n in [x for x in sys.argv[1:] if not x.startswith('--')]:
        s, e, bal = repair(B + n)
        print('%-34s final=%+d  %s' % (n, bal, '; '.join(e) or 'no change'))
        if apply and bal == 0 and e:
            st.save(B + n, s); print('     APPLIED')
