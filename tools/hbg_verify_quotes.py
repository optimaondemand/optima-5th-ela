# -*- coding: utf-8 -*-
"""Check every How I Became a Ghost vocabulary quote against the novel OCR.

q1 and q2 must appear verbatim (after whitespace/quote normalisation).
Cloze sentences are shortened for the exercise, so only their longest clause is checked.
"""
import re, sys, io
sys.path.insert(0, 'tools')
from hbg_sentences import S

def norm(x):
    x = x.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    return re.sub(r'\s+', ' ', x).strip().strip('"')

book = norm(io.open('planning docs/hbg_ocr.txt', encoding='utf-8', errors='replace').read().replace('-\n', ''))
bad = 0
for word, (q1, q2, cloze) in S.items():
    for label, q in (('q1', q1), ('q2', q2)):
        if not q:
            continue
        if norm(q) not in book:
            print('  NOT IN BOOK  %-13s %s: %s' % (word, label, q[:90])); bad += 1
    filled = norm(cloze.replace('{}', word))
    clause = max(re.split(r'[,;]', filled), key=len).strip().rstrip('.!?"')
    if len(clause) > 15 and clause not in book:
        print('  CLOZE DRIFT  %-13s %s' % (word, clause[:90])); bad += 1
print('quotes checked: %d   problems: %d' % (len(S) * 2, bad))
sys.exit(1 if bad else 0)
