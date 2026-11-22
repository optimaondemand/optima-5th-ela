#!/usr/bin/env python3
"""Week 23 plain-language pass (approved Nov 21 2026). Wording only; no graded question or answer changes.
SWYK labels in My Work name the right strand; RWM header spelled out; Writer's Workshop points at its own box;
Use the Word answers collected in book order."""
import io, sys
ALL4 = [("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2)]
RWMH = ('&#128214; RWM &mdash; Read &bull; Notice &bull; Try', '&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try', 1)
FIX = {
 'lesson-23-1-hbg-ch24.html': ALL4 + [("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1),
   ('In your reading journal: write a plan', 'In the box below, write a plan', 1)],
 'lesson-23-2-hbg-ch25.html': ALL4 + [RWMH],
 'lesson-23-3-hbg-ch26.html': ALL4 + [RWMH, ("'SPELLING SWYK'", "'GRAMMAR SWYK'", 1)],
 'lesson-23-4-hbg-ch27.html': ALL4 + [
   ("['journal-vocab-gratitude','journal-vocab-prophecy','journal-vocab-exhausted','journal-vocab-unconscious','journal-vocab-revenge']",
    "['journal-vocab-exhausted','journal-vocab-revenge','journal-vocab-unconscious','journal-vocab-gratitude','journal-vocab-prophecy']", 1)],
}
OUT = {}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:60], s.count(old)))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    OUT[f] = s
for f, s in OUT.items():
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f)
