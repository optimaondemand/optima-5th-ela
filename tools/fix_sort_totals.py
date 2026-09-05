#!/usr/bin/env python3
"""Set each lesson's sortTotal to the number of chips actually in #sortBank.

Pages can carry more than one word-sort game (a vocabulary sort and a
spelling sort), each with its own bank id. sortTotal governs the game whose
bank is id="sortBank", so the count has to come from that div specifically,
walking nested <div>s to find where it ends.
"""
import re, sys, glob, os

def div_body(s, start_re):
    m = re.search(start_re, s)
    if not m: return None
    i = m.end(); depth = 1
    for t in re.finditer(r'<div\b|</div>', s[i:]):
        depth += 1 if t.group(0).startswith('<div') else -1
        if depth == 0: return s[i:i+t.start()]
    return s[i:]

def main(paths, apply=False):
    rows=[]
    for p in sorted(paths):
        s=open(p,encoding='utf-8',errors='replace').read()
        body=div_body(s, r'<div class="sort-bank" id="sortBank"[^>]*>')
        if body is None: continue
        actual=len(re.findall(r'class="sort-chip"', body))
        m=re.search(r'(\bvar\s+sortTotal\s*=\s*)(\d+)', s)
        if not m or not actual: continue
        declared=int(m.group(2))
        if declared==actual: continue
        rows.append((os.path.basename(p),declared,actual))
        if apply:
            open(p,'w',encoding='utf-8').write(s[:m.start(2)]+str(actual)+s[m.end(2):])
    for n,d,a in rows:
        print('%-38s %d -> %-2d  (%s)'%(n,d,a,'UNWINNABLE' if d>a else 'fires early'))
    print('\n%d file(s) %s'%(len(rows),'corrected' if apply else 'would change'))

if __name__=='__main__':
    apply='--apply' in sys.argv
    main([a for a in sys.argv[1:] if not a.startswith('--')] or glob.glob('lesson-*.html'), apply)
