#!/usr/bin/env python3
"""Week 32 plain-language pass, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Round 1 (strand initials, lines pointing at nothing, portfolio/present wording) went in with the scope packet commit.
Wording and folds only; no graded item, answer or key changes.
- the final grammar checklist folded on Days 2 and 4, the year's spelling list folded on Days 2 and 3 ("from Day 1"), the year in review folded on Day 4
- the Speaking card (32.1), the three revision moves (32.3) and the Day 4 'You did it' line shortened"""
import io, re, sys
F = {1: 'lesson-32-1-portfolio-plan.html', 2: 'lesson-32-2-fluency-draft.html', 3: 'lesson-32-3-final-prep.html', 4: 'lesson-32-4-final-present.html'}
def fold(label, summary):
    return (re.compile(r'(<div class="key-concept[^>]*><div class="key-concept-label">' + re.escape(label) + r'</div>)(.*?)(</div>\s*<div class="(?:swyk|callout))', re.S),
            lambda m: m.group(1) + '<details><summary style="cursor:pointer;font-weight:700;color:#3D5285;">' + summary + '</summary>' + m.group(2) + '</details>' + m.group(3), 1)
GRAM = fold('📌 Final Grammar Checklist — For Your Letter', 'The final grammar checklist. Open it and use it on your letter.')
SPELL = fold('📌 Final Spelling Review — Every Unit Word', 'The year&rsquo;s spelling list, from Day 1. Open it if you need it.')
REVIEW = fold('📚 The Year in Review: Five Novels', 'Open to read the year in review: five novels in five sentences.')
SPEAK = (re.compile(r'(<div class="key-concept-label">📌 What Makes a Letter Sound Like You</div>).*?(</div>)', re.S), lambda m: m.group(1) + '''
  <p><strong>Voice:</strong> sound like you talking about something you care about, not a report.</p>
  <p style="margin-top:8px;"><strong>Tone:</strong> let a funny moment sound funny and a sad one sound sad.</p>
  <p style="margin-top:8px;"><strong>Pacing:</strong> slow down at important moments, pause before a quote, and don&rsquo;t rush the ending.</p>
  <p style="margin-top:8px;"><strong>When you record:</strong> look up from the page now and then.</p>
''' + m.group(2), 1)
REP = {
 1: [SPEAK],
 2: [GRAM, SPELL],
 3: [SPELL, (re.compile(r'Your last sentence should be the one that only YOU could have written[^<]*'), lambda m: 'Your last sentence should be one only you could write.', 1),
     ('That&rsquo;s more interesting than "I really enjoyed this book."', '', 'opt')],
 4: [GRAM, REVIEW,
     ('You did it. Five novels and thirty-two weeks. You read about a girl accused of witchcraft in colonial Connecticut, an apprentice silversmith in Boston, a self-taught navigator, a Choctaw boy on his people&rsquo;s forced journey west, and a butler and a boy in the Gold Rush. You wrote an adventure, a literary response, a comparison, and now a letter.',
      'You did it: five novels, thirty-two weeks, and an adventure, a literary response, a comparison and a letter of your own.', 1)],
}
ok = True; out = {}
for k, reps in REP.items():
    fn = F[k]; t = io.open(fn, encoding='utf-8', newline='').read(); o = t
    for i, (pat, new, n) in enumerate(reps):
        if isinstance(pat, str):
            c = t.count(pat)
            if n != 'opt' and c != n: print('FAIL', fn, i, c, repr(pat[:60])); ok = False; continue
            t = t.replace(pat, new)
        else:
            t, c = pat.subn(new, t)
            if c != n: print('FAIL', fn, i, 'regex', c); ok = False
    if o.count('<div') - o.count('</div>') != t.count('<div') - t.count('</div>'): print('FAIL div', fn); ok = False
    out[fn] = t; print(fn, len(o), '->', len(t))
if not ok: sys.exit(1)
if '--apply' in sys.argv:
    for fn, t in out.items(): io.open(fn, 'w', encoding='utf-8', newline='').write(t)
    print('written')
