#!/usr/bin/env python3
"""Week 30 plain language, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Wording and folding only; no graded item, answer or key changes. Nov 24 2026."""
import io, re, sys
F = {1: 'lesson-30-1-btghs-ch16.html', 2: 'lesson-30-2-btghs-ch17.html', 3: 'lesson-30-3-btghs-ch18.html', 4: 'lesson-30-4-btghs-synthesis.html'}
def fold(label, summary, end=r'\n</div>'):
    rx = re.compile(r'(<div class="key-concept"[^>]*>)<div class="key-concept-label">' + re.escape(label) + r'</div>(.*?)(' + end + ')', re.S)
    return (rx, lambda m: m.group(1) + '<details><summary>%s</summary>' % summary + m.group(2) + '\n</details>' + m.group(3), 1)
def before(text):
    return (re.compile(r'<div class="callout callout-info"[^>]*><span class="callout-icon">[^<]*</span><p>Before you start: ' + re.escape(text) + r'</p></div>\n?'), '', 1)
CHECK = fold('📌 Editing Checklist: Punctuation, Capitalization &amp; Clarity', '📌 See the editing checklist (from Day 1)')
WORDS = fold('📌 Grade-Level Editing: High-Frequency Error Words', '📌 See the list of tricky words (from Day 1)')
PUB = fold('📋 Final Publishing Checklist', '📋 See the Final Publishing Checklist (you will use it on Day 3)', r'\n    </div>')
HUNT, ROOT, PATT = before('read as a hunter, not as a reader.'), before('predict what the shared root has to do with, then check.'), before('name the pattern before you spell the word.')
P = {
 1: [('This is the last week of the novel, so read with everything you have. Plot, character, humor and theme are not four separate things; they are one story seen from four sides.',
      'Plot, character, humor and theme are one story seen from four sides.', 1), PUB],
 2: [('A good ending pays off things planted long before. Today read closely and gather evidence for all four elements. As you read',
      'A good ending pays off things planted long before. As you read', 1), CHECK, WORDS, HUNT, ROOT, PATT, PUB],
 3: [('Today you reread a key passage from the last chapter and look at the author&rsquo;s choices. Look at all four elements together: what happens, who it happens to, how it is told, and what it means. After you read Chapter 18, pick the passage that surprised you most and read it again.',
      'After you read Chapter 18, pick the passage that surprised you most and reread it. Look at all four elements: what happens, who it happens to, how it is told, and what it means.', 1),
     WORDS, HUNT, ROOT, PATT],
 4: [('Now put the whole novel together. It was a comedy, an adventure, and an argument about what is worth having. State what you think',
      'Now put the whole novel together. State what you think', 1),
     fold('🗺️ The Six-Week Journey', '🗺️ See the six-week journey', r'\n      </div>'), HUNT, ROOT, before('compare each base word with its longer form.')],
}
for k, reps in P.items():
    f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    for old, new, n in reps:
        if isinstance(old, str):
            if s.count(old) != n: sys.exit('%s: %d x %r' % (f, s.count(old), old[:70]))
            s = s.replace(old, new)
        else:
            s, c = old.subn(new, s, count=1)
            if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:60]))
    if s0.count('<div') - s0.count('</div>') != s.count('<div') - s.count('</div>'): sys.exit('div balance ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain2', f, len(s0), '->', len(s))
