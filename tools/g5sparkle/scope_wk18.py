#!/usr/bin/env python3
"""Week 18 pages brought in line with ELA OAO/5th_grade_ela_scope_sequence_v2_poetry.xlsx (scope week 17),
approved by Bethany Nov 9 2026. One concern per run, so each can be its own commit:
    python tools/g5sparkle/scope_wk18.py rwm|poetry|grammar|standards|spelling
Every replacement asserts its count; div balance must not change. Book lines checked against planning docs/hbg_ocr.txt."""
import io, sys

F = {1: 'lesson-18-1-hbg-ch4.html', 2: 'lesson-18-2-hbg-ch5.html', 3: 'lesson-18-3-hbg-ch6.html', 4: 'lesson-18-4-hbg-ch7.html'}

def chip(g, w):
    return 'data-group="%s" onclick="pickSortChip(this)">%s<' % (g, w)

def swaps(old, new):
    # two passes through placeholders, so a word that moves to another slot is never replaced twice
    first = [(chip(g, a), '@@CHIP%d@@' % i, 1) for i, (g, a) in enumerate(old)]
    second = [('@@CHIP%d@@' % i, chip(g, b), 1) for i, (g, b) in enumerate(new)]
    return first + second

P = {
 # scope RWM: first-person narration that reveals memory, emotion, and perspective (D2 frames, D3 apply)
 'rwm': {
  2: [
   ('<div class="rwm-sentence">&ldquo;The torches made slow circles, turning over and over, followed by a trail of sparks.&rdquo;</div>',
    '<div class="rwm-sentence">&ldquo;When I was only six, I went fishing by myself with my new cane fishing pole.&rdquo; <span style="font-size:13px;color:#5A6B8C;">(Chapter 3)</span></div>', 1),
   ('Tingle uses <strong>participial phrases</strong> &mdash; &ldquo;turning over and over&rdquo; and &ldquo;followed by a trail of sparks&rdquo; &mdash; to build the image in motion.',
    'Isaac stops the story to step back into a <strong>memory</strong> from when he was six. A first-person narrator can do that: tell you something from earlier so you feel what he feels now. This memory is why the sharp stones at the pier scare him. What feeling does the memory carry?', 1),
   ('Write a sentence about something moving. Use a participial phrase (&ldquo;___ing&rdquo; or &ldquo;followed by ___&rdquo;) to add visual detail.',
    'Think of a place you know well. Write one or two sentences with <strong>I</strong> that step back into a memory from when you were younger. Let the memory show how you feel about the place.', 1),
   ('<div class="rwm-frame">The ___ made slow ___, turning ___, followed by ___.</div>',
    '<div class="rwm-frame">When I was only ___, I ___.</div>', 1),
  ],
  3: [
   ('<div class="rwm-sentence">&ldquo;With blowguns we caught our food. With lean-tos we had a place to sleep.&rdquo;</div>',
    '<div class="rwm-sentence">&ldquo;I almost became a ghost that day. If my mother hadn&rsquo;t pulled me back, I would have become a ghost.&rdquo; <span style="font-size:13px;color:#5A6B8C;">(Chapter 6)</span></div>', 1),
   ('Tingle uses <strong>parallel structure</strong> &mdash; &ldquo;With X we did Y&rdquo; repeated. Same sentence shape, different content. This creates rhythm and dignity.',
    'Isaac tells this from <strong>later</strong>, after he knows how things turned out. Looking back lets a first-person narrator show his <strong>perspective</strong>: a moment that seemed small then (his mother pulling him back) turns out to be huge. What does Isaac understand now that he did not understand then?', 1),
   ('Write two parallel sentences using &ldquo;With ___ we ___&rdquo; to describe something in your own life.',
    'Write two sentences about a small moment that mattered more than you knew at the time. Tell it with <strong>I</strong>, looking back from now.', 1),
   ('<div class="rwm-frame">With ___ we ___. With ___ we ___.</div>\n', '', 1),
  ],
 },
 # scope poetry, Days 2 and 4: the poet and the speaker (the voice in the poem is not the writer)
 'poetry': {
  2: [
   ('<p class="socratic-q">Isaac&rsquo;s family literally moves in the dark the night their town burns. Dickinson says we can adapt to darkness and &ldquo;meet the Road erect.&rdquo; <strong>How does this poem describe what you see Isaac and his family doing in Chapter 4?</strong></p>',
    '<p class="socratic-q">The &ldquo;We&rdquo; in this poem is the <em>speaker</em>, the voice talking in the poem. The speaker is not the same person as Emily Dickinson, the poet who wrote it, just as Isaac, the narrator, is not Tim Tingle, the author. <strong>What is the speaker learning to do in the dark? Where do you see Isaac and his family doing the same thing in Chapter 4?</strong></p>', 1),
  ],
  4: [
   ('<p class="socratic-q">Frost says the most precious things are hardest to keep. <strong>What was the &ldquo;gold&rdquo; that couldn&rsquo;t stay for Isaac&rsquo;s family? And what do they keep, even after everything is taken?</strong>',
    '<p class="socratic-q">The <em>speaker</em> of this poem is the voice watching the first spring leaves change and saying &ldquo;Nothing gold can stay.&rdquo; The speaker is not exactly Robert Frost, the poet, the same way Isaac tells this book but Tim Tingle wrote it. <strong>How does the speaker feel about the gold that cannot stay? What was the &ldquo;gold&rdquo; Isaac&rsquo;s family lost, and what do they keep?</strong>', 1),
  ],
 },
 # scope grammar: precise nouns AND appositives
 'grammar': {
  1: [
   ('Grammar:</strong> I will <em>identify</em> appositives in sentences from Chapters 1&ndash;2.',
    'Grammar:</strong> I will <em>identify</em> appositives and precise nouns in sentences from Chapters 1&ndash;2.', 1),
   ('      <div class="swyk">',
    '      <div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#127919;</span><p><strong>Precise nouns.</strong> A precise noun names exactly who or what. <em>A man came home with his weapon</em> tells you less than <em>My father came home with his shotgun</em>. Appositives are a good home for precise nouns: <em>Jumper, my dog,</em> tells you exactly who Jumper is.</p></div>\n      <div class="swyk">', 1),
  ],
  2: [
   ('Grammar:</strong> I will <em>identify</em> appositives in sentences from Chapters 3&ndash;4.',
    'Grammar:</strong> I will <em>identify</em> appositives and precise nouns in sentences from Chapters 3&ndash;4.', 1),
   ('      <div class="swyk">',
    '      <div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#127919;</span><div><p><strong>Precise nouns.</strong> Which names exactly what Isaac sees: <em>a tree</em> or <em>a weeping willow</em>? <em>some women</em> or <em>the old Choctaw women</em>?</p><details><summary style="cursor:pointer;font-weight:700;">Check</summary><p><em>A weeping willow</em> and <em>the old Choctaw women</em>. Both are precise: they name exactly what Isaac sees at the river in Chapter 3.</p></details></div></div>\n      <div class="swyk">', 1),
  ],
  3: [
   ('Grammar:</strong> I will <em>identify</em> appositives in sentences from Chapters 5&ndash;6.',
    'Grammar:</strong> I will <em>build</em> appositives with precise nouns in sentences from Chapters 5&ndash;6.', 1),
   ('Write it as one sentence with an appositive.</strong></p></div>',
    'Write it as one sentence with an appositive. Make the appositive a precise noun phrase (not just <em>a man</em>).</strong></p></div>', 1),
  ],
  4: [
   ('Grammar:</strong> I will <em>identify</em> appositives in sentences from Chapter 7.',
    'Grammar:</strong> I will <em>explain</em> how commas set off an appositive and use precise nouns in my own sentence.', 1),
   ('then say what the sentence would lose if you took the appositive out.</strong></p></div>',
    'then say what the sentence would lose if you took the appositive out. Use at least one precise noun (a name, or an exact word like <em>lean-to</em> instead of <em>house</em>).</strong></p></div>', 1),
  ],
 },
 # scope standards + the Day 3 workshop stage is Revise
 'standards': {},
 # scope spelling: syllable division in historical and cultural vocabulary (skill kept: open/closed)
 'spelling': {
  1: swaps([('open', 'silent'), ('closed', 'winter'), ('open', 'rifle'), ('closed', 'panther'), ('open', 'native'), ('closed', 'blanket')],
           [('open', 'native'), ('closed', 'Choctaw'), ('open', 'nation'), ('closed', 'blanket'), ('open', 'tribal'), ('closed', 'hunting')]),
  2: swaps([('open', 'fever'), ('closed', 'hunger'), ('open', 'paper'), ('closed', 'sister'), ('open', 'moment'), ('closed', 'wagon'), ('open', 'frozen'), ('closed', 'bundle')],
           [('open', 'cedar'), ('closed', 'willow'), ('open', 'Bible'), ('closed', 'stickball'), ('open', 'cypress'), ('closed', 'chicken'), ('closed', 'comet'), ('closed', 'hollow')]),
  3: swaps([('open', 'human'), ('closed', 'basket'), ('open', 'pilot'), ('closed', 'rattle'), ('open', 'later'), ('closed', 'hollow'), ('open', 'removal'), ('closed', 'sudden')],
           [('open', 'uniform'), ('closed', 'government'), ('open', 'station'), ('closed', 'territory'), ('open', 'frozen'), ('closed', 'Mississippi'), ('closed', 'missionary'), ('closed', 'wagon')]),
  4: swaps([('open', 'begin'), ('closed', 'cabin'), ('open', 'prevent'), ('closed', 'river'), ('open', 'equal'), ('closed', 'robin'), ('open', 'notice'), ('closed', 'never')],
           [('open', 'even'), ('closed', 'river'), ('open', 'moment'), ('closed', 'shiver'), ('open', 'silent'), ('closed', 'visit'), ('open', 'final'), ('closed', 'never')]),
 },
}
OLD_FL = ['ELA.5.R.3.3', 'ELA.5.C.1.3', 'ELA.5.C.4.1', 'ELA.5.V.1.3', 'ELA.K12.EE.1.1']
for d in (1, 2, 3, 4):
    new = ['ELA.5.R.1.3', 'ELA.5.C.1.2', 'ELA.5.V.1.2'] + (['ELA.5.R.1.4'] if d in (2, 4) else [])
    reps = [(' &middot; '.join('<span class="fl-code">%s</span>' % c for c in OLD_FL),
             ' &middot; '.join('<span class="fl-code">%s</span>' % c for c in new), 1),
            ('FL: ' + ', '.join(OLD_FL) + ' &middot;', 'FL: ' + ', '.join(new) + ' &middot;', 1),
            ('Apply</span>', 'Revise</span>', 1)]
    if d == 3:
        reps += [('Today is the <strong>Apply</strong> stage', 'Today is the <strong>Revise</strong> stage', 1),
                 ('Week 18 &middot; APPLY', 'Week 18 &middot; REVISE', 1)]
    P['standards'][d] = reps

which = sys.argv[1]
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in reps:
        c = s.count(old)
        if c != n:
            sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'):
        sys.exit('%s: div balance changed' % f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print(which, 'ok', f)
