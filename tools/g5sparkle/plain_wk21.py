#!/usr/bin/env python3
"""Week 21 plain-language pass (approved Nov 21 2026). Wording only; no graded question or answer changes.
Morphology directions now say what the tiles are (meanings); two duplicate/overlapping tiles reworded."""
import io, sys
ALL4 = [("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2)]
RWMH = ('&#128214; RWM &mdash; Read &bull; Notice &bull; Try', '&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try', 1)
ROOTDIR = ('<p><strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.</p>',
           '<p><strong>Match each word to its meaning.</strong> Tap a word, then tap its meaning.</p>', 1)
FIX = {
 'lesson-21-1-hbg-ch16.html': ALL4 + [ROOTDIR, ("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1),
   ('onclick="rootMatchClick(this)">something seen</div>', 'onclick="rootMatchClick(this)">the power of seeing</div>', 1)],
 'lesson-21-2-hbg-ch17.html': ALL4 + [RWMH,
   ('<p><strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.</p>',
    '<p><strong>Match each word to its root and meaning.</strong> Tap a word, then tap the one that fits.</p>', 1),
   ('data-match="B" onclick="rootMatchClick(this)">Root: <em>vid</em> (see)</div>', 'data-match="B" onclick="rootMatchClick(this)"><em>vid</em> (see): what is seen that proves something</div>', 1),
   ('data-match="C" onclick="rootMatchClick(this)">Root: <em>spect</em> (look)</div>', 'data-match="C" onclick="rootMatchClick(this)"><em>spect</em> (look): to look at closely</div>', 1),
   ('data-match="D" onclick="rootMatchClick(this)">Root: <em>spect</em> (look)</div>', 'data-match="D" onclick="rootMatchClick(this)"><em>spect</em> (look): something amazing to look at</div>', 1),
   ('data-match="A" onclick="rootMatchClick(this)">Root: <em>vis</em> (see)</div>', 'data-match="A" onclick="rootMatchClick(this)"><em>vis</em> (see): able to be seen</div>', 1)],
 'lesson-21-3-hbg-ch18.html': ALL4 + [RWMH, ROOTDIR, ("'SPELLING SWYK'", "'GRAMMAR SWYK'", 1)],
 'lesson-21-4-hbg-ch19.html': ALL4 + [ROOTDIR],
}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:60], s.count(old)))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f)
