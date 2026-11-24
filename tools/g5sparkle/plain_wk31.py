#!/usr/bin/env python3
"""Week 31 plain-language pass, round 1 (standing approval Nov 23 2026: every week). Wording only; no graded question or answer changes.
Strand initials out of student text (skill 8f.5): SWYK -> Show What You Know; book initials in the vocabulary list -> short titles;
'Tomorrow' -> 'Next lesson' (students are self-paced); a direction that pointed 'above' at another step names the box instead.
HTML comments and data-label keys are left as they are, so saved work still matches."""
import io, re, sys
FILES = ['lesson-31-1-comparison-plan.html', 'lesson-31-2-comparison-sources.html', 'lesson-31-3-comparison-draft.html', 'lesson-31-4-comparison-submit.html']
VIS = re.compile(r'(?<=>)([^<>]*?)\bSWYK\b')
REP = {
 'lesson-31-1-comparison-plan.html': [('Plan complete. Tomorrow: gather your sources.', 'Plan complete. Next lesson: real sources and your first paragraphs.', 1)],
 'lesson-31-3-comparison-draft.html': [('following the four-step structure above.', 'following the four steps in the How to Write box.', 1)],
 'lesson-31-4-comparison-submit.html': [
   ('<p><strong>Historical fiction (WOBP, JT):</strong>', '<p><strong>Historical fiction (<em>Witch</em>, <em>Johnny Tremain</em>):</strong>', 1),
   ('<p><strong>Navigation/science (CMB):</strong>', '<p><strong>Navigation/science (<em>Bowditch</em>):</strong>', 1),
   ('Yesterday you named the elements.', 'On Day 2 you named the elements.', 1)],
}
for f in FILES:
    s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    parts = re.split(r'(<!--.*?-->)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        p = parts[i]
        while True:
            p2 = VIS.sub(lambda m: m.group(1) + 'Show What You Know', p)
            if p2 == p: break
            p = p2
        parts[i] = p
    s = ''.join(parts)
    for a, b, n in REP.get(f, []):
        c = s.count(a)
        if c != n: sys.exit('count %s %d %r' % (f, c, a))
        s = s.replace(a, b)
    if s.count('<div') != s0.count('<div') or s.count('</div>') != s0.count('</div>'): sys.exit('div ' + f)
    if len(re.findall(r'data-label="[^"]*SWYK', s0)) != len(re.findall(r'data-label="[^"]*SWYK', s)): sys.exit('label ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f, s0.count('SWYK') - s.count('SWYK'), 'SWYK replaced')
