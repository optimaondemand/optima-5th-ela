#!/usr/bin/env python3
"""Week 29 plain language, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Wording and folding only; no graded item, answer or key changes. Nov 24 2026."""
import io, re, sys
F = {1: 'lesson-29-1-btghs-ch13.html', 2: 'lesson-29-2-btghs-ch14.html', 3: 'lesson-29-3-btghs-ch15.html', 4: 'lesson-29-4-btghs-voice.html'}
LONG = ('<strong>Long sentences</strong> flow and accumulate — they let Fleischman stack detail on detail until the reader feels the full weight of a moment, the way a day of prospecting in the mountains might feel when every rock turned over is another small disappointment.',
        '<strong>Long sentences</strong> flow. They let a writer stack detail on detail.', 1)
def fold(label, summary):
    rx = re.compile(r'(<div class="key-concept"[^>]*>)<div class="key-concept-label">' + re.escape(label) + r'</div>(.*?)\n</div>', re.S)
    return (rx, lambda m: m.group(1) + '<details><summary>%s</summary>' % summary + m.group(2) + '\n</details></div>', 1)
def before(text):
    return (re.compile(r'<div class="callout callout-info"[^>]*><span class="callout-icon">[^<]*</span><p>Before you start: ' + re.escape(text) + r'</p></div>'), '', 1)
FAM = fold('📌 Word Families — Related Words from One Root', '📌 See the four word families (from Day 1)')
P = {
 1: [LONG, ('As you read, listen for it &mdash; and notice that flea traps and notoriety get exactly the same deadpan treatment as anything else. ', '', 1)],
 2: [fold('📌 Sentence Variety for Style', '📌 See the ways to vary sentences (from Day 1)'), FAM],
 3: [FAM, before('read the first family and work out what changes from word to word. Then read on.'), before('find the base word hiding under the ending.')],
 4: [('Now <strong>put it together</strong>. Describe this book&rsquo;s voice to somebody who has not read it, in three sentences, using evidence. Then ask the harder question: what does this voice let Fleischman do that a different one could not? Pull',
      'Now <strong>put it together</strong>: describe this book&rsquo;s voice in three sentences, with evidence. Pull', 1),
     ('The biggest laughs in the novel come from a gap between two things: what is expected vs. what happens; what a character says vs. what they privately feel; what should be dignified vs. what is ridiculous. Praiseworthy&rsquo;s umbrella as a gold pan = gap between butler dignity and Gold Rush reality.',
      'The biggest laughs come from a gap between what you expect and what happens, like a proper butler&rsquo;s umbrella used as a gold pan.', 1),
     before('look for the pattern before you are told it.'),
     ('I answered the Read Like a Writer box on the Reading tab.', 'I answered the Read Like a Writer box on the Voice &amp; Tone tab.', 1)],
}
for k, reps in P.items():
    f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    for old, new, n in reps:
        if isinstance(old, str):
            if s.count(old) != n: sys.exit('%s: %d x %r' % (f, s.count(old), old[:70]))
            s = s.replace(old, new)
        else:
            s, c = old.subn(new, s)
            if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:50]))
    if s0.count('<div') - s0.count('</div>') != s.count('<div') - s.count('</div>'): sys.exit('div balance ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain2', f, len(s0), '->', len(s))
