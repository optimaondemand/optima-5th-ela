#!/usr/bin/env python3
"""Week 21 pages brought in line with the scope (v2_poetry scope week 20 = v4 week 21), approved by
Bethany Nov 21 2026 (claude/g5-ela-wk21-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk21.py spelling|rwm|poetry|writing
Every replacement asserts its count; div balance may only change by the boxes a strand adds on purpose.
Book lines checked against planning docs/hbg_ocr.txt. Poems: Hughes "Dreams" as first printed in The World
Tomorrow (May 1923, Lehigh African American Poetry anthology); Rossetti from Sing-Song (Gutenberg #76703)."""
import io, sys

F = {1: 'lesson-21-1-hbg-ch16.html', 2: 'lesson-21-2-hbg-ch17.html', 3: 'lesson-21-3-hbg-ch18.html', 4: 'lesson-21-4-hbg-ch19.html'}
def chip(g, w): return 'data-group="%s" onclick="pickSortChip(this)">%s<' % (g, w)

def rwm(sentence, ch, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">&ldquo;%s&rdquo; <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">What does this sentence make you see or feel?</div>\n'
      '      <textarea class="journal-box" id="journal-rwm-reader" placeholder="This sentence makes me..." oninput="autoSave(this,\'dot-rwm-reader\');gatherAnswers();"></textarea></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n'
      '      <textarea class="journal-box" id="journal-rwm-writer" placeholder="This connects to..." oninput="autoSave(this,\'dot-rwm-writer\');gatherAnswers();"></textarea></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s'
      '      <textarea class="journal-box" id="journal-rwm-mimic" placeholder="My sentence..." oninput="autoSave(this,\'dot-rwm-mimic\');gatherAnswers();"></textarea></div>\n'
      '  </div>\n') % (sentence, ch, writer, tryit, fr)

R = {
 1: rwm('Rescuing Naomi gave us all a purpose.', 16,
        'This short sentence names a big idea plainly: helping someone gives people a reason to keep going. To explain a theme, you join details from <strong>more than one part</strong> of a book. This line connects back to Chapter 12, when Nita&rsquo;s ghost asks Isaac to find her sister.',
        'Write two sentences about an idea that keeps coming back in this book. In the first, give a detail from Chapter 16. In the second, connect it to an earlier chapter. Start it with <strong>Back in Chapter ___</strong>.', None),
 4: rwm('Maybe being a ghost wasn&rsquo;t so bad after all.', 19,
        'Put this line beside Mister Jonah&rsquo;s words in Chapter 9: &ldquo;Our lives are over, but we can still help the living.&rdquo; Two details from two parts of the book point at the <strong>same idea</strong>. That is how a writer explains a theme: one claim, two places that prove it.',
        'On your own: write two sentences. State a theme of this book in the first. Support it with details from two different chapters in the second.', None),
}
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my Read Like a Writer answers on the Reading tab.</div></div>\n        '
COLC = '<div class="sort-col"><div class="sort-col-header" style="background:linear-gradient(135deg,#8B6914,#a87f1f);">A result, or to influence</div><div class="sort-col-drop" data-col="c" onclick="dropSortChip(this,\'c\')"></div></div>'
COLS = ('<div class="sort-col"><div class="sort-col-header" style="background:linear-gradient(135deg,#8B6914,#a87f1f);">To influence (a verb)</div><div class="sort-col-drop" data-col="c" onclick="dropSortChip(this,\'c\')"></div></div>\n'
        '          <div class="sort-col"><div class="sort-col-header" style="background:linear-gradient(135deg,#2B5BA8,#3A6FC0);">A result (a noun)</div><div class="sort-col-drop" data-col="d" onclick="dropSortChip(this,\'d\')"></div></div>')
DREAMS = ('Hold fast to dreams, my son,<br>For if dreams die<br>Life is a broken-winged bird<br>That cannot fly.<br><br>'
          'Hold fast to dreams, O boy,<br>For when dreams go<br>Life is a barren field<br>Frozen with snow.')
WIND = ('Who has seen the wind?<br>Neither I nor you:<br>But when the leaves hang trembling<br>The wind is passing thro&rsquo;.<br><br>'
        'Who has seen the wind?<br>Neither you nor I:<br>But when the trees bow down their heads<br>The wind is passing by.')
P = {
 'spelling': {
  3: [(chip('verb', 'counsel'), chip('verb', 'accept'), 1)],   # counsel is a noun too; accept is only a verb
  4: [(chip('c', 'effect'), chip('d', 'effect'), 1), (COLC, COLS, 1)],
 },
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)]},
 'poetry': {
  2: [('<div class="poem-title">Fog</div>\n        <div class="poem-author">Carl Sandburg (1916)</div>\n        <div class="poem-text">The fog comes<br>on little cat feet.<br><br>It sits looking<br>over harbor and city<br>on silent haunches<br>and then moves on.</div>',
       '<div class="poem-title">Dreams</div>\n        <div class="poem-author">Langston Hughes (1923)</div>\n        <div class="poem-text">' + DREAMS + '</div>', 1),
      ('<p class="socratic-q">Isaac moves through the soldiers&rsquo; camp unseen &mdash; like fog. Like a cat. <strong>How does Sandburg&rsquo;s poem describe the way Isaac moves as a ghost? What does comparing fog to a cat add to the image?</strong></p>',
       '<p class="socratic-q">Look at what comes back. &ldquo;Hold fast to dreams&rdquo; opens both stanzas, and each time a new picture follows: a bird that cannot fly, then a field frozen with snow. <strong>What do the two pictures say together that one alone would not? What idea keeps coming back in Isaac&rsquo;s story the same way?</strong></p>', 1)],
  4: None,
 },
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 21 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 21 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Revise Moment 2 from your plan.', 'Today is the <strong>Revise</strong> stage. Check Moment 1: Did you add a sensory detail? Did you add a comparison? Does it fit the feeling? Then revise Moment 2 from your plan.', 1),
 ("data-label=\"Writer's Workshop: Narrative Revision — Apply\"", "data-label=\"Writer's Workshop: Narrative Revision — Revise\"", 1),
]
which = sys.argv[1]
if which == 'poetry':
    s4 = io.open(F[4], encoding='utf-8', newline='').read()
    a = s4.index('<div class="poem-title">Ode to My Socks</div>'); b = s4.index('</div>', s4.index('<div class="poem-text">', a)) + len('</div>')
    q = s4.index('<p class="socratic-q">Neruda writes an ode'); qe = s4.index('</p>', q) + 4
    P['poetry'][4] = [(s4[a:b], '<div class="poem-title">Who Has Seen the Wind?</div>\n        <div class="poem-author">Christina Rossetti (1872)</div>\n        <div class="poem-text">' + WIND + '</div>', 1),
      (s4[q:qe], '<p class="socratic-q">The question comes back, and so does the answer: nobody has seen the wind. But each time, something shows it is there: trembling leaves, then trees bowing their heads. <strong>How can you know something is there when you cannot see it? In Chapter 18, Isaac tells Joseph, &ldquo;I know you&rsquo;re there, even though I can&rsquo;t always see you.&rdquo; What idea do the poem and the novel share?</strong></p>', 1)]
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new, 1)
    ok = {'rwm': 5, 'spelling': 3 if d == 4 else 0}.get(which, 0)
    if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print(which, 'ok', f)
