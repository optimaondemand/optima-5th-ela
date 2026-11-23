#!/usr/bin/env python3
"""Week 28 plain language, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Wording and folding only; no graded item, answer or key changes. Nov 23 2026."""
import io, re, sys
F = {1: 'lesson-28-1-btghs-ch10.html', 2: 'lesson-28-2-btghs-ch11.html', 3: 'lesson-28-3-btghs-ch12.html', 4: 'lesson-28-4-btghs-theme.html'}
SECOND_Q = re.compile(r'(ask yourself</div>\n\s*<p class="socratic-q">[^<]*</p>)\n\s*<p class="socratic-q">[^\n]*</p>')
BEFORE = re.compile(r'<div class="callout callout-info"[^>]*><span class="callout-icon">[^<]*</span><p>Before you start: [^<]*</p></div>')
TIP = re.compile(r'<p><strong>This week: shift to literary response\.</strong>.*?</p>', re.S)
TIP_N = ('<p><strong>Your literary response</strong> makes a <strong>claim about theme</strong> and proves it with <strong>specific evidence</strong> from the text. '
         'The strongest evidence is a <strong>character&rsquo;s choice</strong>: what someone decides to do, and what that shows he values.</p>')
STRUCT = re.compile(r'<div class="key-concept"><div class="key-concept-label">📋 Literary Response Structure</div>(.*?)\n</div>', re.S)
STRUCT_N = lambda m: '<div class="key-concept"><details><summary>📋 Literary Response Structure (from Day 1)</summary>' + m.group(1) + '\n</details></div>'
SP2 = re.compile(r'(<p style="margin-top:8px;"><strong>–ity</strong>.*?<strong><em>ness</em></strong></p>)', re.S)
GR3 = re.compile(r'(<p style="margin-top:8px;"><strong>However</strong> &mdash; contrast.*?show what followed from an action</p>)', re.S)
EX1 = re.compile(r'(<div class="key-concept-label" style="color:#7B5EA7;">📌 Examples</div>)(.*?)(\n</div>)', re.S)
P = {
 1: [(SECOND_Q, None, 1), (EX1, lambda m: m.group(1) + '\n  <details><summary>See all the example words</summary>' + m.group(2) + '\n  </details>' + m.group(3), 1)],
 2: [(SECOND_Q, None, 1), (BEFORE, '', 2), (TIP, TIP_N, 1), (STRUCT, STRUCT_N, 1),
     (SP2, lambda m: '<details style="margin-top:8px;"><summary>See the examples from Day 1 again</summary>' + m.group(1) + '</details>', 1)],
 3: [(SECOND_Q, None, 1), (BEFORE, '', 2), (TIP, TIP_N, 1), (STRUCT, STRUCT_N, 1),
     (GR3, lambda m: '<details style="margin-top:8px;"><summary>See all eight transitions and what they do</summary>' + m.group(1) + '</details>', 1),
     ('Today <strong>reread</strong> a passage where an event and an idea meet. Around a campfire, in a conversation about Aunt Arabella, in a choice about the truth &mdash; find the moment where what happens and what it means are the same thing.',
      'Today find and <strong>reread</strong> the moment where what happens and what it means are the same thing.', 1)],
 4: [(SECOND_Q, None, 1), (BEFORE, '', 2), (TIP, TIP_N, 1), (STRUCT, STRUCT_N, 1),
     ('Now <strong>put it together</strong> and name it. You have a week of events. State the theme they are building in one sentence, then test it: does every major event support your wording, or do you need to change it? Then pull',
      'Now <strong>put it together</strong>: state the theme the week&rsquo;s events are building in one sentence, then test it against those events. Then pull', 1),
     ('I answered the Read Like a Writer box on the Reading tab.', 'I answered the Read Like a Writer box on the Theme tab.', 1)],
}
ONLY = [int(a) for a in sys.argv[1:]]
for k, reps in P.items():
    if ONLY and k not in ONLY: continue
    f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    for old, new, n in reps:
        if isinstance(old, str):
            if s.count(old) != n: sys.exit('%s: %d x %r' % (f, s.count(old), old[:70]))
            s = s.replace(old, new)
        else:
            s, c = old.subn((lambda m: m.group(1)) if new is None else new, s)
            if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:50]))
    d0 = s0.count('<div') - s0.count('</div>'); d1 = s.count('<div') - s.count('</div>')
    if d0 != d1: sys.exit('div balance ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain2', f, len(s0), '->', len(s))
