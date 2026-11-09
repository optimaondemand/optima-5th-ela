#!/usr/bin/env python3
"""Week 18 plain-language trims and lines that pointed at things that weren't there
(approved by Bethany Nov 9 2026; audit items B, K, L, N, S + the two missing grammar boxes).
Wording only; no graded question or answer changes. Every replacement asserts its count."""
import io, sys

def box(n, label, ph):
    return ('<div class="journal-label">Your sentence <span class="saved-dot" id="dot-grammar"></span></div>'
            '<textarea class="journal-box" id="journal-grammar" data-label="%s" placeholder="%s" '
            'oninput="autoSave(this,\'dot-grammar\');gatherAnswers();"></textarea>' % (label, ph))

ALL4 = [
 ('I wrote my Writing Connection sentence.', 'I wrote my Writer&rsquo;s Workshop response.', 1),
 ("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2),
]
FIX = {
 'lesson-18-1-hbg-ch4.html': ALL4 + [
  # B. the cards' book sentences come from later chapters this week
  ('Chapters 1–7</div></div></div>', 'this week&rsquo;s chapters</div></div></div>', 1),
  ('Chapters 1–7. Read the sentence from the book first',
   'this week&rsquo;s chapters (some you will read on Days 2 and 3). Read the sentence from the book first', 1),
  # S. the box is right below
  ('In your reading journal: brainstorm', 'In the box below, brainstorm', 1),
  ("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1),
 ],
 'lesson-18-2-hbg-ch5.html': ALL4,
 'lesson-18-3-hbg-ch6.html': ALL4 + [
  # K. the chapter introduction said only "Watch, then read."
  ('Watch, then read.</div></div></div>\n    <div class="activity-body">\n',
   'Watch, then read.</div></div></div>\n    <div class="activity-body">\n'
   '    <p>A hundred Choctaws reach an island in the swamp and start over: lean-tos, blowguns, and cooking fires hidden from the Nahullos. Then winter freezes the swamp, and soldiers ride in with wagons.</p>\n', 1),
  # the write-it prompt had no box
  ('Write it as one sentence with an appositive.</strong></p></div>',
   'Write it as one sentence with an appositive.</strong></p></div>' +
   box(3, 'Grammar: my appositive sentence', 'Old Man, ..., spoke first in the swamp.'), 1),
  ("'SPELLING SWYK'", "'GRAMMAR SWYK'", 1),
  ('To honour a memory', 'To honor a memory', 1),
 ],
 'lesson-18-4-hbg-ch7.html': ALL4 + [
  ('Watch, then read.</div></div></div>\n    <div class="activity-body">\n',
   'Watch, then read.</div></div></div>\n    <div class="activity-body">\n'
   '    <p>The swamp is frozen and everything is &ldquo;rotten sad.&rdquo; Then Isaac&rsquo;s father takes the boys and Jumper on a walk across the ice, away from camp.</p>\n', 1),
  ('then say what the sentence would lose if you took the appositive out.</strong></p></div>',
   'then say what the sentence would lose if you took the appositive out.</strong></p></div>' +
   box(4, 'Grammar: my appositive sentence and what it adds', 'My sentence: ... Without the appositive, the reader would lose...'), 1),
  ('out loud or to a partner', 'out loud or in your head', 1),
 ],
}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n:
            sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], c))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'):
        sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('trimmed', f)
