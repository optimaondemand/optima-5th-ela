#!/usr/bin/env python3
"""Week 19 pages brought in line with the scope (v2_poetry scope week 18 = v4 week 19), approved by
Bethany Nov 21 2026 (claude/g5-ela-wk19-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk19.py spelling|rwm|poetry|writing
Every replacement asserts its count; div balance may only change by the boxes a strand adds on purpose.
Book lines checked against planning docs/hbg_ocr.txt; the Hughes poem against a public-domain edition."""
import io, sys

F = {1: 'lesson-19-1-hbg-ch8.html', 2: 'lesson-19-2-hbg-ch9.html', 3: 'lesson-19-3-hbg-ch10.html', 4: 'lesson-19-4-hbg-ch11.html'}
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
      '      <textarea class="journal-box" id="journal-rwm-writer" placeholder="Isaac\'s voice shows..." oninput="autoSave(this,\'dot-rwm-writer\');gatherAnswers();"></textarea></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s'
      '      <textarea class="journal-box" id="journal-rwm-mimic" placeholder="My sentence..." oninput="autoSave(this,\'dot-rwm-mimic\');gatherAnswers();"></textarea></div>\n'
      '  </div>\n') % (sentence, ch, writer, tryit, fr)

R = {
 1: rwm('I was so hungry that I would have eaten the corn uncooked. But with wild onions, roasted over a log fire, it was delicious!', 8,
        'A first-person narrator lets you inside his head. Isaac gives a <strong>thought</strong> (he would have eaten the corn raw), a <strong>detail</strong> (wild onions, a log fire) and a <strong>reaction</strong> (delicious!). That mix makes his voice sound like a real boy talking. Name the thought, the detail and the reaction.',
        'Write two sentences with <strong>I</strong> about a meal or a moment you remember. Put in one thought, one detail and one reaction.', None),
 2: rwm('I hung my head and hoped nobody would make fun of me. I thought this big-brother-thing would be a secret.', 9,
        'Isaac shows what he <strong>does</strong> (hangs his head) and what he <strong>thinks</strong> (he hopes nobody laughs; he thought it would be a secret). The action and the thought together let you feel his embarrassment without him naming it.',
        'Write about a time you felt shy or embarrassed. Show one action and one thought, with <strong>I</strong>.', 'I ___ and hoped ___. I thought ___.'),
 3: rwm('My feet were freezing cold and burning hot at the same time. I never knew pain could hurt this bad.', 10,
        'First a <strong>detail</strong> only Isaac can feel (cold and hot at once), then his <strong>reaction</strong> in plain words a boy would say. The plain second sentence is what makes it sound true.',
        'Look at your Writer&rsquo;s Workshop draft. Write one sentence with <strong>I</strong> that gives a detail only your narrator could feel, then one plain reaction.', 'My ___ was ___. I never knew ___.'),
 4: rwm('I had learned long ago never to refuse a gift.', 11,
        'One short <strong>thought</strong> tells you a rule Isaac lives by, and it explains why he takes Nita&rsquo;s shoes. A first-person narrator can show who he is by telling you what he already knows.',
        'On your own: write one sentence with <strong>I</strong> that tells something you learned long ago. Then write a second sentence that shows it in action.', None),
}
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my three Read Like a Writer answers on the Reading tab.</div></div>\n        '

def old_box(d):
    s = io.open(F[d], encoding='utf-8', newline='').read()
    a = s.index('  <!-- RWM -->\n  <div class="rwm-box">'); b = s.index('  </div>\n', s.index('journal-rwm-mimic', a)) + len('  </div>\n')
    return s[a:b]

RIVERS = ('I&rsquo;ve known rivers:<br>I&rsquo;ve known rivers ancient as the world and older than the flow of human blood in human veins.<br><br>'
          'My soul has grown deep like the rivers.<br><br>'
          'I bathed in the Euphrates when dawns were young.<br>I built my hut near the Congo and it lulled me to sleep.<br>'
          'I looked upon the Nile and raised the pyramids above it.<br>'
          'I heard the singing of the Mississippi when Abe Lincoln went down to New Orleans, and I&rsquo;ve seen its muddy bosom turn all golden in the sunset.<br><br>'
          'I&rsquo;ve known rivers:<br>Ancient, dusky rivers.<br><br>My soul has grown deep like the rivers.')
P = {
 # -ive/-al/-ic: 19.4's middle column had no right answers; 19.3 repeated every word from 19.1-19.2
 'spelling': {
  3: swaps([('al', 'brutal'), ('ive', 'creative'), ('ic', 'historic'), ('al', 'personal'), ('ive', 'protective'), ('ive', 'supportive'), ('al', 'survival'), ('ic', 'symbolic'), ('ic', 'tragic')],
           [('ive', 'active'), ('ic', 'angelic'), ('ic', 'athletic'), ('al', 'cultural'), ('ive', 'inventive'), ('ive', 'massive'), ('al', 'musical'), ('ic', 'rhythmic'), ('al', 'tribal')]),
  4: [(chip('yi', 'historic'), chip('base', 'historic'), 1), (chip('yi', 'tragic'), chip('base', 'tragic'), 1),
      (chip('drop', 'descriptive'), chip('base', 'descriptive'), 1),
      ('background:linear-gradient(135deg,#8B3A20,#A84A2A);">y becomes i</div><div class="sort-col-drop" data-col="yi" onclick="dropSortChip(this,\'yi\')">',
       'background:linear-gradient(135deg,#8B3A20,#A84A2A);">Base changes spelling</div><div class="sort-col-drop" data-col="base" onclick="dropSortChip(this,\'base\')">', 1),
      ('did a silent <em>e</em> drop, did a <em>y</em> become <em>i</em>, or did nothing change at all?',
       'did a silent <em>e</em> drop, did the base change its spelling some other way (<em>describe &rarr; descriptive</em>), or did nothing change at all?', 1)],
 },
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1)]},
 'poetry': {
  2: [('<div class="poem-title">Dreams</div>\n        <div class="poem-author">Langston Hughes (1922)</div>',
       '<div class="poem-title">The Negro Speaks of Rivers</div>\n        <div class="poem-author">Langston Hughes (1921)</div>', 1),
      ('<div class="poem-text">Hold fast to dreams<br>For if dreams die<br>Life is a broken-winged bird<br>That cannot fly.<br><br>Hold fast to dreams<br>For when dreams go<br>Life is a barren field<br>Frozen with snow.</div>',
       '<div class="poem-text">' + RIVERS + '</div>', 1),
      ('<p class="socratic-q">Isaac&rsquo;s feet freeze to the ground and nearly kill him. But something inside refuses to die. <strong>What &ldquo;dream&rdquo; does Isaac hold fast to? What keeps him walking when his feet are bloody?</strong></p>',
       '<p class="socratic-q">The &ldquo;I&rdquo; in this poem is the <em>speaker</em>, the voice talking. The speaker says he bathed in the Euphrates and raised the pyramids, thousands of years before Langston Hughes was born, so the speaker is not the poet. He speaks for a whole people across time. Isaac, the narrator, is not Tim Tingle either. <strong>What has the speaker carried with him from all those rivers? What does Isaac&rsquo;s family carry with them onto the road?</strong></p>', 1)],
  4: [('<p class="socratic-q">Isaac&rsquo;s father says: &ldquo;You cannot keep your eyes on the bloody footprints you have left behind you. You must keep your eyes on where you are going.&rdquo; <strong>How does this poem sound like Isaac&rsquo;s father speaking? What has the mother in this poem endured, and what is she telling her son to do?</strong></p>',
       '<p class="socratic-q">The <em>speaker</em> of this poem is a mother talking to her son. Langston Hughes was not a mother: he gave her the voice, the way Tim Tingle gives Isaac his. <strong>What has the speaker lived through, and what does she tell her son to do? In Chapter 10, Isaac&rsquo;s father tells him to keep his eyes on where he is going. How are these two speakers alike?</strong></p>', 1)],
 },
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['rwm'][2] = [(old_box(2), R[2], 1)]
P['rwm'][3] = [(old_box(3), R[3], 1)]
P['rwm'][4].append((CHK_WW, CHK_RWM + CHK_WW, 1))
P['rwm'][1][1] = (CHK_WW, CHK_RWM + CHK_WW, 1)
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 19 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 19 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Add ONE rising-tension sentence to your draft &mdash; a moment where everything is about to break.',
  'Today is the <strong>Revise</strong> stage. Reread your draft with this checklist: Is the conflict clear? Does the tension build? Is it still unresolved? Then add ONE rising-tension sentence &mdash; a moment where everything is about to break.', 1),
 ('data-label="Writer\'s Workshop: Conflict and Rising Action — Apply"', 'data-label="Writer\'s Workshop: Conflict and Rising Action — Revise"', 1),
]
ADD = {'rwm': {1: 5, 4: 5}}   # a new box: rwm-box + 3 steps + header/sentence/labels... counted below

which = sys.argv[1]
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new, 1) if n == 1 else s.replace(old, new)
    bal = lambda t: t.count('<div') - t.count('</div')
    if bal(s) != bal(orig): sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print(which, 'ok', f)
