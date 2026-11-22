#!/usr/bin/env python3
"""Week 23 pages brought in line with the scope (v2_poetry scope week 22 = v4 week 23), approved by
Bethany Nov 21 2026 (claude/g5-ela-wk23-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk23.py rwm|poetry|grammar|writing
Book lines checked against planning docs/hbg_ocr.txt. Poems: Lazarus "The New Colossus" (1883), whole
sonnet, Wikisource transcription of The Poems of Emma Lazarus (1889); Stevenson "Requiem", Underwoods
(1887), Wikisource transcription. Hughes "Let America Be America Again" (1936) was under copyright."""
import io, sys
F = {1: 'lesson-23-1-hbg-ch24.html', 2: 'lesson-23-2-hbg-ch25.html', 3: 'lesson-23-3-hbg-ch26.html', 4: 'lesson-23-4-hbg-ch27.html'}
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
 1: rwm('The soldiers had tried to put the fire out with buckets of snow, but the wagon was destroyed.', 24,
        'This sentence sums up a whole night of work in a few words. Tingle does not tell you how many buckets, who carried them, or how long they tried. He gives you the effort and the result, joined by <em>but</em>. That is <strong>summarizing</strong>: keep what matters and leave out the rest.',
        'Write one sentence that sums up something that happened in Chapter 24. Tell what someone tried and how it turned out, joined by <em>but</em>.', None),
 4: rwm('The soldiers continued their search, burning blankets and questioning Choctaws at every camp.', 27,
        'One sentence covers a whole morning: the search, the burning, the questions, every camp. You already watched this happen in Chapter 25, so Tingle only needs a summary to move the story on to the wagon.',
        'On your own: write one sentence that sums up a stretch of Chapter 27 without retelling every event. Then write one more sentence: what did you leave out, and why?', None),
}
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my Read Like a Writer answers on the Reading tab.</div></div>\n        '
COLOSSUS = ('Not like the brazen giant of Greek fame,<br>With conquering limbs astride from land to land;<br>Here at our sea-washed, sunset gates shall stand<br>A mighty woman with a torch, whose flame<br>'
            'Is the imprisoned lightning, and her name<br>Mother of Exiles. From her beacon-hand<br>Glows world-wide welcome; her mild eyes command<br>The air-bridged harbor that twin cities frame.<br>'
            '&ldquo;Keep, ancient lands, your storied pomp!&rdquo; cries she<br>With silent lips. &ldquo;Give me your tired, your poor,<br>Your huddled masses yearning to breathe free,<br>'
            'The wretched refuse of your teeming shore.<br>Send these, the homeless, tempest-tost to me,<br>I lift my lamp beside the golden door!&rdquo;')
REQUIEM = ('Under the wide and starry sky,<br>Dig the grave and let me lie.<br>Glad did I live and gladly die,<br>And I laid me down with a will.<br><br>'
           'This be the verse you grave for me:<br>Here he lies where he longed to be;<br>Home is the sailor; home from sea,<br>And the hunter home from the hill.')
POEMS = {
 2: ('The New Colossus', 'Emma Lazarus (1883)', COLOSSUS,
     'This poem is a <strong>sonnet</strong>: fourteen lines with a tight rhyme pattern, a shape poets use for serious, formal speech. Lazarus wrote it to help pay for the base of the Statue of Liberty, and in the last lines the statue herself speaks, &ldquo;with silent lips.&rdquo; <strong>Why might a poet choose a strict, formal shape for words spoken by a monument? Find the line where the poem turns from describing the statue to letting her speak.</strong>'),
 4: ('Requiem', 'Robert Louis Stevenson (1887)', REQUIEM,
     'Stevenson shaped this poem like a gravestone: two short stanzas, steady rhymes, and in the second stanza the very words he wants carved on the stone. <strong>Why would a poem about the end of a life be so short and so calm? What do the sailor and the hunter have in common? In Chapter 27, watch how the bonepickers treat the dead.</strong>'),
}
def poem(s, title, author, text, prompt):
    a = s.index('<div class="poem-title">'); b = s.index('</div>', s.index('<div class="poem-text">', a)) + len('</div>')
    q = s.index('<p class="socratic-q">', b); qe = s.index('</p>', q) + 4
    new = ('<div class="poem-title">%s</div>\n        <div class="poem-author">%s</div>\n        <div class="poem-text">%s</div>' % (title, author, text))
    return s[:a] + new + s[b:q] + '<p class="socratic-q">%s</p>' % prompt + s[qe:]
P = {
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)]},
 'grammar': {3: [
   ('<p style="margin-top:10px;color:#3A4A6B;">Two ideas that belong together are joined; the third stays short, so it lands.</p>',
    '<p style="margin-top:10px;color:#3A4A6B;">Two ideas that belong together are joined; the third stays short, so it lands.</p>\n'
    '      <div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;"><div class="key-concept-label" style="color:#3D5285;">&#x1F517; Transitions</div>'
    '<p>Transition words show how one idea connects to the next. <em>But</em> shows a contrast. <em>Because</em> shows a reason. <em>When</em> and <em>then</em> show time. <em>Instead</em> shows a change of plan.</p></div>', 1),
   ('Combine at least two sentences and split at least one. Then explain what each change did for the reader.',
    'Combine at least two sentences and split at least one. Use at least one transition word (<em>but</em>, <em>because</em>, <em>when</em>, <em>then</em> or <em>instead</em>). Then explain what each change did for the reader.', 1)]},
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 23 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 23 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Read your draft from Day 2. Make one pass for each: (1) strong verbs, (2) sentence variety, (3) clear pronouns. Mark your three best sentences with a star. Mark one sentence you want to completely rewrite.',
  'Today is the <strong>Revise</strong> stage. Read your draft from Day 2 and check it against this list, one pass for each: (1) strong verbs, (2) sentence variety, with at least one combined sentence, (3) clear pronouns, (4) at least one transition word. Mark your three best sentences with a star. Rewrite one sentence that needs it.', 1),
 ("data-label=\"Writer's Workshop: Publish Piece — Apply (Polish)\"", "data-label=\"Writer's Workshop: Publish Piece — Revise\"", 1),
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
