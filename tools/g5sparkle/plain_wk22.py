#!/usr/bin/env python3
"""Week 22 plain-language pass (approved Nov 21 2026). Wording only; no graded question or answer changes.
Morphology directions now say what the tiles are (meanings); the D2 duplicate photo tiles reworded;
SWYK labels in My Work name the right strand; vocab chapter ranges say "this week's chapters"."""
import io, sys
ALL4 = [("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2)]
RWMH = ('&#128214; RWM &mdash; Read &bull; Notice &bull; Try', '&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try', 1)
ROOTDIR = ('<p><strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.</p>',
           '<p><strong>Match each word to its meaning.</strong> Tap a word, then tap its meaning.</p>', 1)
FIX = {
 'lesson-22-1-hbg-ch20.html': ALL4 + [ROOTDIR, ("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1),
   ('Five words from Chapters 20–23.', 'Five words from this week&rsquo;s chapters.', 1)],
 'lesson-22-2-hbg-ch21.html': ALL4 + [RWMH,
   ('<p><strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.</p>',
    '<p><strong>Match each word to its root and meaning.</strong> Tap a word, then tap the one that fits.</p>', 1),
   ('Read each sentence from Chapters 20–23.', 'Read each sentence from this week&rsquo;s chapters.', 1),
   ('data-match="A" onclick="rootMatchClick(this)">Root: <em>luc</em> (light)</div>', 'data-match="A" onclick="rootMatchClick(this)"><em>luc</em> (light): clear and easy to understand</div>', 1),
   ('data-match="B" onclick="rootMatchClick(this)">Root: <em>lum</em> (light)</div>', 'data-match="B" onclick="rootMatchClick(this)"><em>lum</em> (light): to shine light on</div>', 1),
   ('data-match="C" onclick="rootMatchClick(this)">Root: <em>photo</em> (light)</div>', 'data-match="C" onclick="rootMatchClick(this)"><em>photo</em> (light): how plants make food from sunlight</div>', 1),
   ('data-match="D" onclick="rootMatchClick(this)">Root: <em>photo</em> (light)</div>', 'data-match="D" onclick="rootMatchClick(this)"><em>photo</em> (light): a camera lens for faraway pictures</div>', 1)],
 'lesson-22-3-hbg-ch22.html': ALL4 + [RWMH, ROOTDIR, ("'SPELLING SWYK'", "'GRAMMAR SWYK'", 1),
   ('each sentence from Chapters 20–23,', 'each sentence from this week&rsquo;s chapters,', 1)],
 'lesson-22-4-hbg-ch23.html': ALL4 + [ROOTDIR],
}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:60], s.count(old)))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f)
