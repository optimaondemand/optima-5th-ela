#!/usr/bin/env python3
"""Week 20 plain-language pass (approved Nov 21 2026). Wording only; no graded question or answer changes."""
import io, sys
DOL = 'Rewrite in active voice with strong verbs. Fix capitalization and punctuation.'
ALL4 = [("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2)]
RWMH = ('&#128214; RWM &mdash; Read &bull; Notice &bull; Try', '&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try', 1)
INTRO = '<div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n        <div class="activity bl-purple"'
def intro(p): return INTRO.replace('<div class="activity-body">\n', '<div class="activity-body">\n    <p>%s</p>\n' % p)
FIX = {
 'lesson-20-1-hbg-ch12.html': ALL4 + [(DOL, 'Add the missing comma and the capital letter.', 1), ("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1)],
 'lesson-20-2-hbg-ch13.html': ALL4 + [(DOL, 'Add the missing comma and the capital letter.', 1), RWMH],
 'lesson-20-3-hbg-ch14.html': ALL4 + [(DOL, 'Add the missing comma and the capital letter, and cut the words that repeat.', 1), RWMH,
   (INTRO, intro('In Chapter 14, Joseph tells Isaac how he was caught by the soldiers and how he got away. Listen for the order of the events. Each one makes the next one possible.'), 1)],
 'lesson-20-4-hbg-ch15.html': ALL4 + [(DOL, 'Add the missing comma and the capital letters.', 1),
   (INTRO, intro('In Chapter 15, Joseph learns that Choctaw leaders ride in a council wagon, and a ghost gives Isaac a plan. Watch how the danger changes from the road to the soldiers themselves.'), 1)],
}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:60], s.count(old)))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f)
