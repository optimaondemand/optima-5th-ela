#!/usr/bin/env python3
"""Week 30 plain-language pass, round 1 (standing approval Nov 23 2026: every week). Wording only; no graded question or answer changes.
Strand initials out of student text (skill 8f.5): SWYK -> Show What You Know, DOL -> Daily Oral Language
(HTML comments and data-label keys left as they are, so saved work still matches)."""
import io, re, sys
FILES = ['lesson-30-1-btghs-ch16.html', 'lesson-30-2-btghs-ch17.html', 'lesson-30-3-btghs-ch18.html', 'lesson-30-4-btghs-synthesis.html']
VIS = re.compile(r'(?<=>)([^<>]*?)\bSWYK\b')
for f in FILES:
    s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    parts = re.split(r'(<!--.*?-->)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        p = parts[i]
        while True:
            p2 = VIS.sub(lambda m: m.group(1) + 'Show What You Know', p)
            if p2 == p: break
            p = p2
        p = p.replace('I wrote my DOL fix', 'I wrote my Daily Oral Language fix')
        p = p.replace('Submit it here for your teacher to read.', 'Put it in the box below. It goes to your teacher when you copy your work into Canvas.')
        p = p.replace('(Option ___)', '(I wrote which option at the top)')
        parts[i] = p
    s = ''.join(parts)
    n = s0.count('SWYK') - s.count('SWYK')
    if s.count('<div') != s0.count('<div'): sys.exit('div ' + f)
    if 'data-label="' in s0 and len(re.findall(r'data-label="[^"]*SWYK', s0)) != len(re.findall(r'data-label="[^"]*SWYK', s)): sys.exit('label ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f, n, 'SWYK replaced')
