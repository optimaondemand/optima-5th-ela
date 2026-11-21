#!/usr/bin/env python3
"""Week 22 pages brought in line with the scope (v2_poetry scope week 21 = v4 week 22), approved by
Bethany Nov 21 2026 (claude/g5-ela-wk22-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk22.py rwm|poetry|writing
Book lines checked against planning docs/hbg_ocr.txt. Poems: Blake "The Tyger", stanzas 1-2, from the
1826 copy of Songs of Innocence and of Experience (Wikisource transcription; "seize" as in later printed
editions, Blake's plate has "sieze"); Frost from New Hampshire (Holt, 1923), Wikisource transcription."""
import io, sys
F = {1: 'lesson-22-1-hbg-ch20.html', 2: 'lesson-22-2-hbg-ch21.html', 3: 'lesson-22-3-hbg-ch22.html', 4: 'lesson-22-4-hbg-ch23.html'}
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
 1: rwm('Fat balls of tears rolled down her cheeks.', 20,
        'Tingle could have written &ldquo;Naomi cried hard.&rdquo; Instead he gives you a picture: tears so big they are &ldquo;fat balls.&rdquo; That is <strong>imagery</strong>, words that let you see it. A picture makes you feel the sadness instead of just being told about it.',
        'Write one sentence about Chapter 20 that shows a feeling with a picture. Do not use the feeling word itself (sad, scared, angry).', None),
 4: rwm('In the dark of the woods the air trembled with light.', 23,
        'Air cannot really tremble. Tingle gives it a feeling, so the moment the ghosts appear seems alive. Notice the two opposites in one short sentence: <em>dark</em> and <em>light</em>.',
        'On your own: write one sentence about a moment in Chapters 20 to 23 that uses a comparison, or gives a feeling to something that is not alive. Then write one more sentence: what does your picture help a reader feel?', None),
}
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my Read Like a Writer answers on the Reading tab.</div></div>\n        '
TYGER = ('Tyger Tyger, burning bright,<br>In the forests of the night:<br>What immortal hand or eye,<br>Could frame thy fearful symmetry?<br><br>'
         'In what distant deeps or skies<br>Burnt the fire of thine eyes?<br>On what wings dare he aspire?<br>What the hand dare seize the fire?')
WOODS = ('Whose woods these are I think I know.<br>His house is in the village though;<br>He will not see me stopping here<br>To watch his woods fill up with snow.<br><br>'
         'My little horse must think it queer<br>To stop without a farmhouse near<br>Between the woods and frozen lake<br>The darkest evening of the year.<br><br>'
         'He gives his harness bells a shake<br>To ask if there is some mistake.<br>The only other sound&rsquo;s the sweep<br>Of easy wind and downy flake.<br><br>'
         'The woods are lovely, dark and deep.<br>But I have promises to keep,<br>And miles to go before I sleep,<br>And miles to go before I sleep.')
def poem(s, title, author, text, prompt):
    a = s.index('<div class="poem-title">'); b = s.index('</div>', s.index('<div class="poem-text">', a)) + len('</div>')
    q = s.index('<p class="socratic-q">', b); qe = s.index('</p>', q) + 4
    new = ('<div class="poem-title">%s</div>\n        <div class="poem-author">%s</div>\n        <div class="poem-text">%s</div>' % (title, author, text))
    return s[:a] + new + s[b:q] + '<p class="socratic-q">%s</p>' % prompt + s[qe:]
POEMS = {
 2: ('The Tyger', 'William Blake (1794)', TYGER,
     'Blake never says the tiger is dangerous. He gives you pictures instead: an animal <em>burning bright</em> in a dark forest, eyes made of fire. <strong>Which picture do you see most clearly? What does it make you feel about the tiger? Watch for fire and a big cat in Chapter 21, too.</strong>'),
 4: ('Stopping by Woods on a Snowy Evening', 'Robert Frost (1923)', WOODS,
     'Frost never says how the evening feels. He lets you see and hear it: woods filling up with snow, the darkest evening of the year, the soft sweep of wind. <strong>Which picture makes the woods feel quiet? Why do you think he repeats the last line? In Chapter 23, Isaac and Joseph wait in snowy woods at night, too.</strong>'),
}
P = {
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)]},
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 22 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 22 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Read your draft from Day 2. Edit it:', 'Today is the <strong>Revise</strong> stage. Read your draft from Day 2 and check it:', 1),
 ("data-label=\"Writer's Workshop: Draft Literary Analysis — Apply (Edit)\"", "data-label=\"Writer's Workshop: Draft Literary Analysis — Revise\"", 1),
]
which = sys.argv[1]
if which == 'poetry':
    for d, (t, au, tx, pr) in POEMS.items():
        f = F[d]; s = io.open(f, encoding='utf-8', newline='').read(); orig = s
        s = poem(s, t, au, tx, pr)
        if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('%s: div balance changed' % f)
        io.open(f, 'w', encoding='utf-8', newline='').write(s); print('poetry ok', f)
    sys.exit()
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new, 1)
    if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print(which, 'ok', f)
