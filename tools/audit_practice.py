#!/usr/bin/env python3
"""Scan OAO 5th-grade ELA lessons for practice activities that give away
their own answers, or that no longer teach anything on a wrong tap.

Detectors:
  A  giveaway marker  - a blank/arrow marker printed inside a practice item
                        at the very spot the answer belongs
  B  single option    - an item where only one choice is plausible
                        (fewer than 2 wrong options, or the correct option
                        is the only one carrying the marker)
  C  no explanation   - spotter items with no data-explain on their chunks
  D  orphan card      - a "Group A/Group B" card whose partner is missing
  E  bad total        - a hardcoded game total that disagrees with the
                        number of items actually on the page
"""
import re, sys, glob, os, collections

MARKER = re.compile(r'(__|&#x2190;\s*HERE|←\s*HERE|\bHERE\b)')
SENT   = re.compile(r'<div class="spotter-sentence"[^>]*id="([^"]+)"(.*?)(?=<div class="spotter-sentence"|</div>\s*</div>\s*<!--|\Z)', re.S)
WORD   = re.compile(r'<span class="spotter-word"[^>]*>', re.S)

def chunks(block):
    out=[]
    for m in re.finditer(r'<span class="spotter-word"([^>]*)>(.*?)</span>', block, re.S):
        attrs, text = m.group(1), re.sub(r'<[^>]+>','',m.group(2)).strip()
        out.append({'correct': 'data-correct="true"' in attrs,
                    'explain': 'data-explain=' in attrs,
                    'text': text})
    return out

def audit(path):
    s=open(path,encoding='utf-8',errors='replace').read()
    name=os.path.basename(path); hits=[]

    # --- spotter-based detectors (A on the prompt line, B, C)
    for m in SENT.finditer(s):
        sid, block = m.group(1), m.group(2)
        cs = chunks(block)
        if not cs: continue
        prompt = re.sub(r'<[^>]+>',' ', block.split('<span class="spotter-word"')[0])
        correct = [c for c in cs if c['correct']]
        wrong   = [c for c in cs if not c['correct']]

        if MARKER.search(prompt):
            hits.append(('A', sid, 'answer marker printed in the item text: %r'
                         % MARKER.search(prompt).group(0)))
        marked = [c for c in cs if MARKER.search(c['text'])]
        if marked and all(c['correct'] for c in marked) and len(marked) < len(cs):
            hits.append(('B', sid, 'only the correct option carries the marker (%s)'
                         % ', '.join(c['text'] for c in marked)))
        if len(wrong) < 2:
            hits.append(('B', sid, 'only %d wrong option(s) - little to decide' % len(wrong)))
        if correct and not any(c['explain'] for c in cs):
            hits.append(('C', sid, 'no data-explain on any chunk'))

    # --- D: orphaned Group A/B card
    ga, gb = len(re.findall(r'Group A\b', s)), len(re.findall(r'Group B\b', s))
    if gb and not ga:
        hits.append(('D','-','"Group B" card with no "Group A" partner'))

    # --- E: hardcoded totals vs items on the page
    counts = {
      'sortTotal':  len(re.findall(r'class="sort-chip"', s)),
      'fillTotal':  len(re.findall(r'class="fillin-input"', s)) or len(re.findall(r'id="fill\d+"', s)),
      'matchTotal': len(re.findall(r'class="match-item"', s)),
    }
    for var, actual in counts.items():
        for mm in re.finditer(r'\bvar\s+%s\s*=\s*(\d+)\s*;' % var, s):
            declared=int(mm.group(1))
            if actual and declared != actual:
                hits.append(('E','-','%s=%d but %d item(s) on the page' % (var,declared,actual)))
    return name, hits

def main(paths):
    tally=collections.Counter(); files=0
    for p in sorted(paths):
        name,hits = audit(p)
        if not hits: continue
        files+=1
        print('\n%s' % name)
        for code,sid,msg in hits:
            tally[code]+=1
            print('  [%s] %-8s %s' % (code, sid, msg))
    print('\n%s\n%d file(s) flagged | ' % ('-'*60, files) +
          ' '.join('%s=%d' % (k,tally[k]) for k in sorted(tally)))

if __name__=='__main__':
    main(sys.argv[1:] or glob.glob('lesson-*.html'))
