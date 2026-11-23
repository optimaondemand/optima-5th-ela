#!/usr/bin/env python3
"""Week 27 plain language, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Wording and folding only; no graded item, answer or key changes. Nov 23 2026."""
import io, re, sys
F = {1: 'lesson-27-1-btghs-ch7.html', 2: 'lesson-27-2-btghs-ch8.html', 3: 'lesson-27-3-btghs-ch9.html', 4: 'lesson-27-4-btghs-info.html'}
SECOND_Q = re.compile(r'(ask yourself</div>\n\s*<p class="socratic-q">[^<]*</p>)\n\s*<p class="socratic-q">[^<]*</p>')
STAKES = ' Now make things harder. The middle of every great adventure is where things go wrong, unexpected, or impossible. Fleischman'
BEFORE = re.compile(r'<div class="callout callout-info"[^>]*><span class="callout-icon">[^<]*</span><p>Before you start: [^<]*</p></div>')
SKED = ('Fled or left in a hurry. Informal American English. Captain Swain says it when he learns the Sea Raven has already left Callao.',
        'Left in a hurry. Captain Swain says it when he learns the Sea Raven has already left Callao.')
GRUB = ('Money or supplies given to a miner in return for a share of the gold found; their survival fund for mining.', 'Money or supplies a miner lives on while looking for gold.')
FAN = ('Two independent clauses joined by a coordinating conjunction (for, and, nor, but, or, yet, so — FANBOYS) or a semicolon. Equal ideas, forward momentum.',
       'Two complete sentences joined by a comma and <em>and</em>, <em>but</em>, <em>or</em> or <em>so</em> (or by a semicolon). Two equal ideas, moving forward.')
CPX = ('An independent clause + a dependent clause (because, when, although, unless, while, since, until, if). Shows cause, condition, or time relationship.',
       'A complete sentence + a part that cannot stand alone, starting with <em>because</em>, <em>when</em>, <em>although</em>, <em>if</em> or <em>until</em>. It shows cause, condition or time.')
P = {
 1: [(SECOND_Q, None, 1), (STAKES, ' Now make things harder. Fleischman', 1),
     (' Words with this root involve movement, flow, or the passage of time.</p>', '</p>', 1),
     (' Words with this root involve drawing something toward, or pulling it along.</p>', '</p>', 1),
     ('The whole voyage is a <em>current</em> of events rushing forward. Losing the coal could <em>distract</em> any captain. When Praiseworthy reminds Captain Swain about the lumber, the captain finds a way to <em>extract</em> one more burst of speed. And the race has a prize: if Swain wins, he gets command of a new clipper ship.',
      'Events rush along like a <em>current</em>. Losing the coal could <em>distract</em> any captain, but the lumber lets Captain Swain <em>extract</em> one more burst of speed.', 1),
     SKED + (1,), GRUB + (1,), FAN + (1,), CPX + (1,)],
 2: [(SECOND_Q, None, 1), (STAKES, ' Now make things harder. Fleischman', 1), (BEFORE, '', 2), SKED + (1,), GRUB + (1,), FAN + (1,), CPX + (1,)],
 3: [(SECOND_Q, None, 1), (STAKES, ' Now make things harder. Fleischman', 1), (BEFORE, '', 2),
     ('Today <strong>reread</strong> a single problem from start to finish. A river journey, a stagecoach, a plan that does not survive contact with reality &mdash; follow one of them through the whole chain and notice how Fleischman constructs it.',
      'Today <strong>reread</strong> one problem from start to finish and notice how Fleischman builds it.', 1),
     ('Each sentence adds one small step in order (he wakes, his hand rests on the pistol, he tips back the hat, he looks at Jack), so you have to wait. Then the last line is short and plain. Slow steps build the suspense; the short line lets it go.',
      'Each sentence adds one small step, so you have to wait. Then the last line is short and plain. Slow steps build suspense; the short line lets it go.', 1)],
 4: [(STAKES, ' Now make things harder. Fleischman', 1), (BEFORE, '', 2),
     ('<p>A real eyewitness turns Chapter 8 into more than a story. Taylor paid two dollars just to have his trunks carried; Jack and Praiseworthy hear that water costs a dollar a bucket. History makes the novel vivid; the novel makes history human.',
      '<p>A real eyewitness turns Chapter 8 into more than a story. History makes the novel vivid; the novel makes history human.', 1)],
}
for k, reps in P.items():
    f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    for old, new, n in reps:
        if isinstance(old, str):
            if s.count(old) != n: sys.exit('%s: %d x %r' % (f, s.count(old), old[:70]))
            s = s.replace(old, new)
        else:
            s, c = old.subn((lambda m: m.group(1)) if new is None else new, s)
            if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:50]))
    if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('plain2', f, len(s0), '->', len(s))
# round 2b: 27.2 grammar examples (shown on Day 1) folded, as week 26 folded Alex's draft
K2_OLD = ('''Two equal ideas, moving forward.<br>
  <em>Example:</em> &ldquo;The paddlewheels twirled, faster and faster, <strong>and</strong> the bowsprit came around on course like a compass needle.&rdquo; (Chapter 7)</p>
  <p style="margin-top:8px;"><strong>Complex sentence:</strong> A complete sentence + a part that cannot stand alone, starting with <em>because</em>, <em>when</em>, <em>although</em>, <em>if</em> or <em>until</em>. It shows cause, condition or time.<br>
  <em>Example:</em> &ldquo;<strong>When</strong> the Lady Wilma entered the blue Bay of Callao, Jack counted thirty-one sailing ships at anchor.&rdquo; (Chapter 7)</p>
  <p style="margin-top:8px;"><strong>In action writing:</strong> Compound = simultaneous events happening together. Complex = cause and effect, the engine of adventure.</p>''')
K2_NEW = ('''Two equal ideas, moving forward.</p>
  <p style="margin-top:8px;"><strong>Complex sentence:</strong> A complete sentence + a part that cannot stand alone, starting with <em>because</em>, <em>when</em>, <em>although</em>, <em>if</em> or <em>until</em>. It shows cause, condition or time.</p>
  <p style="margin-top:8px;"><strong>In action writing:</strong> compound = two things happening together; complex = cause and effect.</p>
  <details style="margin-top:8px;"><summary>See the two examples from Chapter 7 again</summary><p>&ldquo;The paddlewheels twirled, faster and faster, <strong>and</strong> the bowsprit came around on course like a compass needle.&rdquo; (compound)</p><p>&ldquo;<strong>When</strong> the Lady Wilma entered the blue Bay of Callao, Jack counted thirty-one sailing ships at anchor.&rdquo; (complex)</p></details>''')
import io as _io
_f = 'lesson-27-2-btghs-ch8.html'; _s = _io.open(_f, encoding='utf-8', newline='').read()
if _s.count(K2_OLD) == 1:
    _io.open(_f, 'w', encoding='utf-8', newline='').write(_s.replace(K2_OLD, K2_NEW)); print('plain2b folded 27.2 grammar examples')
