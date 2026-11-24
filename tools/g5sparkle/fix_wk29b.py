#!/usr/bin/env python3
"""Week 29 accuracy fixes, part 2 (same approval): banner subtitles and one objective that gave away a chapter before reading."""
import io, sys
F = {1: 'lesson-29-1-btghs-ch13.html', 2: 'lesson-29-2-btghs-ch14.html', 3: 'lesson-29-3-btghs-ch15.html'}
FIX = {1: [('Jack bids on one word, buys another, and Praiseworthy calls it brilliant', 'Flea traps, prices, and one word misheard at an auction')],
       2: [('Stubb the burro, a squirrel gun, and the long search for pay dirt', 'Stubb the burro, the goodbyes, and a book about boxing')],
       3: [('A grizzly, a coyote hole, a white coat — and no map', 'Prospecting, a hunting trip, and a narrator who stays calm'),
           ('I will analyze the coyote hole rescue, the empty coat, and what Praiseworthy&rsquo;s response reveals.', 'I will analyze how the narrator&rsquo;s voice handles danger and disappointment in Chapter 15.')]}
out = {}
for k, reps in FIX.items():
    s = io.open(F[k], encoding='utf-8', newline='').read()
    for o, n in reps:
        if s.count(o) != 1: sys.exit('%s %d %r' % (F[k], s.count(o), o))
        s = s.replace(o, n)
    out[F[k]] = s
for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
print('written')
