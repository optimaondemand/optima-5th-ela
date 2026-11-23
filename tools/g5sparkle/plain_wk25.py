#!/usr/bin/env python3
"""Week 25 plain-language pass (approved Nov 22 2026). Wording only; no graded question or answer changes.
25.2: the opening-line pause repeated 25.1's What Good Readers Do question, so it now asks about the setting;
the vocabulary line says where each word turns up."""
import io, sys
FIX = {
 'lesson-25-2-btghs-ch1.html': [
  ('<p class="socratic-q">Fleischman opens with &ldquo;It was not once upon a time.&rdquo; What effect does this have? Why begin a comic adventure novel by insisting on the specific date?</p>',
   '<p class="socratic-q">Stop when Jack and Praiseworthy climb out of the barrels. Name two details that tell you this story is set in 1849, not today.</p>', 1),
  ('Say the word aloud, read the definition, and think of where you met it in yesterday&rsquo;s background reading or Chapter 1.',
   'Say the word aloud and read the meaning. Four of the words are in Chapter 1 today; <em>undaunted</em> comes in Chapter 2.', 1),
  ('placeholder="Fleischman opens this way because..."', 'placeholder="Two details from 1849: ..."', 1)],
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
