#!/usr/bin/env python3
"""Week 19 plain-language pass + lines that pointed at things that weren't there (approved Nov 21 2026).
Wording only; no graded question or answer changes. Every replacement asserts its count."""
import io, sys
SMALL = ("The soldiers' blankets carried it.", "In the story, blankets carried it.")
SICK = ("Illness. On the road, Choctaws died from sickness and from hunger.", "Being ill; disease.")   # a meaning never names its word
DOL = 'Rewrite in active voice with strong verbs. Fix capitalization and punctuation.'
ALL4 = [("'🪶 WRITING CONNECTION'", "'✍️ WRITER\\'S WORKSHOP'", 2)]
FIX = {
 'lesson-19-1-hbg-ch8.html': ALL4 + [
  (SMALL[0], SMALL[1], 2), (SICK[0], SICK[1], 2),
  (DOL, 'Fix the capital letters and add the missing comma.', 1),
  ('Chapters 8–11</div>', 'this week&rsquo;s chapters</div>', 1),
  ('In your reading journal: jot down', 'In the box below, jot down', 1),
  ("'MORPHOLOGY SWYK'", "'GRAMMAR SWYK'", 1),
 ],
 'lesson-19-2-hbg-ch9.html': ALL4 + [
  (SMALL[0], SMALL[1], 2), (SICK[0], SICK[1], 2),
  (DOL, 'Fix the capital letter and add the missing comma.', 1),
  ('Read each sentence from Chapters 8–11.', 'Read each sentence from this week&rsquo;s chapters.', 1),
 ],
 'lesson-19-3-hbg-ch10.html': ALL4 + [
  (SMALL[0], SMALL[1], 1), (SICK[0], SICK[1], 1),
  (DOL, 'Fix the capitals and the comma, and join the two actions into one.', 1),
  ('each sentence from Chapters 8–11, then check', 'each sentence from this week&rsquo;s chapters, then check', 1),
  # empty Chapter Introduction (WGRD moves to Warm-Up at load, leaving nothing)
  ('<div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n        <div class="activity bl-purple"',
   '<div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n    <p>Chapter 10 is the coldest day of the walk. Isaac stands too long in the icy rain, and Mister Jonah&rsquo;s warning comes true. Watch what finally pulls him back.</p>\n        <div class="activity bl-purple"', 1),
 ],
 'lesson-19-4-hbg-ch11.html': ALL4 + [
  (SMALL[0], SMALL[1], 2), (SICK[0], SICK[1], 2),
  (DOL, 'Fix the capitals and the comma, and cut the words that repeat.', 1),
  ('<div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n        <div class="activity bl-purple"',
   '<div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n    <p>In Chapter 11, Nita gives Isaac a gift, and Isaac sees something about her that he does not want to see. This chapter holds a hard loss. Read it slowly, and notice how Isaac&rsquo;s family and friends care for each other.</p>\n        <div class="activity bl-purple"', 1),
 ],
}
for f, reps in FIX.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], c))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain', f)
