#!/usr/bin/env python3
"""Week 20 pages brought in line with the scope (v2_poetry scope week 19 = v4 week 20), approved by
Bethany Nov 21 2026 (claude/g5-ela-wk20-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk20.py spelling|rwm|poetry|writing
Every replacement asserts its count; div balance may only change by the boxes a strand adds on purpose.
Book lines checked against planning docs/hbg_ocr.txt; the Hughes poem against a public-domain edition."""
import io, sys

F = {1: 'lesson-20-1-hbg-ch12.html', 2: 'lesson-20-2-hbg-ch13.html', 3: 'lesson-20-3-hbg-ch14.html', 4: 'lesson-20-4-hbg-ch15.html'}
def chip(g, w): return 'data-group="%s" onclick="pickSortChip(this)">%s<' % (g, w)
def swaps(old, new):
    first = [(chip(g, a), '@@CHIP%d@@' % i, 1) for i, (g, a) in enumerate(old)]
    return first + [('@@CHIP%d@@' % i, chip(g, b), 1) for i, (g, b) in enumerate(new)]

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
      '      <textarea class="journal-box" id="journal-rwm-writer" placeholder="The order of events..." oninput="autoSave(this,\'dot-rwm-writer\');gatherAnswers();"></textarea></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s'
      '      <textarea class="journal-box" id="journal-rwm-mimic" placeholder="My sentence..." oninput="autoSave(this,\'dot-rwm-mimic\');gatherAnswers();"></textarea></div>\n'
      '  </div>\n') % (sentence, ch, writer, tryit, fr)

R = {
 1: rwm('The icicle responds. It shakes, but it keeps everybody waiting.', 12,
        'Tingle makes you wait. First the icicle <strong>shakes</strong>, then it <strong>keeps everybody waiting</strong>, and only after that does it fall. Putting the delay before the event is how a writer builds tension: the reader holds their breath with everyone in the story.',
        'Write two sentences about something that is about to happen. Make the reader wait: put one small delay before the big moment.', None),
 4: rwm('I gripped the limb and was about to climb, when the warm shiver came.', 15,
        'Isaac starts an action (<strong>about to climb</strong>), and then <strong>when</strong> something interrupts it. The interruption comes last, so it lands hard. The order of the events is doing the work.',
        'On your own: write one sentence where someone starts to do something and is interrupted. Use <strong>when</strong> to bring in the interruption.', None),
}
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my three Read Like a Writer answers on the Reading tab.</div></div>\n        '
SNAKE = ('A narrow fellow in the grass<br>Occasionally rides;<br>You may have met him, &mdash; did you not,<br>His notice sudden is.<br><br>'
         'The grass divides as with a comb,<br>A spotted shaft is seen;<br>And then it closes at your feet<br>And opens further on.<br><br>'
         'He likes a boggy acre,<br>A floor too cool for corn.<br>Yet when a child, and barefoot,<br>I more than once, at morn,<br><br>'
         'Have passed, I thought, a whip-lash<br>Unbraiding in the sun, &mdash;<br>When, stooping to secure it,<br>It wrinkled, and was gone.<br><br>'
         'Several of nature&rsquo;s people<br>I know, and they know me;<br>I feel for them a transport<br>Of cordiality;<br><br>'
         'But never met this fellow,<br>Attended or alone,<br>Without a tighter breathing,<br>And zero at the bone.')
def poem4(s):
    a = s.index('<div class="poem-title">I Shall Not Pass This Way Again</div>')
    b = s.index('</div>', s.index('<div class="poem-text">', a)) + len('</div>')
    return s[a:b]
P = {
 'spelling': {
  2: [(chip('one', 'compete'), chip('two', 'compete'), 1)],
  3: swaps([('one', 'nation'), ('two', 'national'), ('two', 'signatory'), ('one', 'signature')],
           [('one', 'atom'), ('two', 'atomic'), ('two', 'metallic'), ('one', 'metal')]),
  4: swaps([('one', 'sentiment'), ('two', 'sentimental')], [('one', 'major'), ('two', 'majority')]),
 },
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)]},
 'poetry': {
  2: [('<p class="socratic-q">Isaac has a choice: become a ghost now, or stay alive and keep his promises. He chooses to keep walking. <strong>How does Frost&rsquo;s poem apply to Isaac&rsquo;s decision in Chapter 10? What &ldquo;road&rdquo; does Isaac take, and why does it matter?</strong></p>',
       '<p class="socratic-q">Look at the last stanza. The line breaks after &ldquo;and I&mdash;&rdquo; and then repeats &ldquo;I&rdquo; on the next line. That break makes you wait, the same way Tingle makes you wait in a tense moment. <strong>Read the stanza aloud and pause at each line break. Where do you feel the most tension, and why does Frost put the break there?</strong></p>', 1)],
  4: None,
 },
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 20 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 20 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Add a second piece of evidence', 'Today is the <strong>Revise</strong> stage. Check your draft: Does the topic sentence name the theme? Does each piece of evidence prove it? Then add a second piece of evidence', 1),
 ('data-label="Writer\'s Workshop: Theme Paragraph — Apply"', 'data-label="Writer\'s Workshop: Theme Paragraph — Revise"', 1),
]
which = sys.argv[1]
if which == 'poetry':
    s4 = io.open(F[4], encoding='utf-8', newline='').read()
    P['poetry'][4] = [(poem4(s4), '<div class="poem-title">A narrow fellow in the grass</div>\n        <div class="poem-author">Emily Dickinson (published 1866)</div>\n        <div class="poem-text">' + SNAKE + '</div>', 1),
      ('<p class="socratic-q">The Choctaw people on the Trail of Tears pass through impossible suffering. People die every day. <strong>How does this poem apply to Isaac&rsquo;s decision to help Naomi, even though the risk is enormous? What does &ldquo;I shall not pass this way again&rdquo; mean for someone on the Trail of Tears?</strong></p>',
       '<p class="socratic-q">Dickinson never says the word <em>snake</em>. She lets each line break hide the next clue, so you see the fellow a little at a time, and the poem ends with a line break into &ldquo;And zero at the bone.&rdquo; <strong>Which line break makes you feel the most tension? How does Isaac feel this week, waiting for a sign, the way the speaker feels in the grass?</strong></p>', 1)]
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new, 1)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print(which, 'ok', f)
