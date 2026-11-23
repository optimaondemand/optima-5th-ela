#!/usr/bin/env python3
"""Week 28 plain-language pass (approved Nov 23 2026). Wording only; no graded question or answer changes.
Strand initials out of student text (skill 8f.5): SWYK -> Show What You Know, DOL -> Daily Oral Language
(HTML comments and data-label keys left as they are, so saved work still matches)."""
import io, re, sys
FILES = ['lesson-28-1-btghs-ch10.html', 'lesson-28-2-btghs-ch11.html', 'lesson-28-3-btghs-ch12.html', 'lesson-28-4-btghs-theme.html']
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
        parts[i] = p
    s = ''.join(parts)
    n = s0.count('SWYK') - s.count('SWYK')
    if s.count('<div') != s0.count('<div'): sys.exit('div ' + f)
    if 'data-label="' in s0 and len(re.findall(r'data-label="[^"]*SWYK', s0)) != len(re.findall(r'data-label="[^"]*SWYK', s)): sys.exit('label ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f, n, 'SWYK replaced')
