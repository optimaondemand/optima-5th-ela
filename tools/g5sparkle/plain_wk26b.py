#!/usr/bin/env python3
"""Week 26 plain-language pass, round 2 (Bethany, Nov 23 2026: "do the plain language pass yes, always").
Wording and folding only; no graded question, answer or key changes. Targets the long steps found by the
Next-only walk (aim about 110 words a step):
- What Good Readers Do: one think-question per box (the second is cut); 26.3/26.4 intro paragraphs shortened.
- Writer's Workshop: Alex's model draft stays open on 26.1 and folds into "See Alex's draft scene again" on 26.2-26.4
  (the same model was shown four days running); the Notice line shortened.
- Spelling notes on 26.1/26.3 and the 26.4 journal prompt shortened; 26.4 comic techniques shortened, the
  initials "BTGHS" spelled out, "make it around the Horn" corrected (the ship took the Strait)."""
import io, re, sys
F = {1: 'lesson-26-1-btghs-ch4.html', 2: 'lesson-26-2-btghs-ch5.html', 3: 'lesson-26-3-btghs-ch6.html', 4: 'lesson-26-4-btghs-humor.html'}
SECOND_Q = {
 1: '        <p class="socratic-q">What has the humor told you about Jack that a serious description could not?</p>\n',
 2: '        <p class="socratic-q">Pick one dangerous moment. How would the chapter feel if it were told in a panicked voice instead?</p>\n',
 3: '        <p class="socratic-q">How does Fleischman use a character&rsquo;s reaction to make an event funnier than it would be on its own?</p>\n',
 4: '        <p class="socratic-q">Which character has been revealed most through comedy rather than description? Give a specific moment.</p>\n'}
NOTICE_OLD = '<strong>Notice:</strong> dialogue that sounds like real speech, not a summary. A pause that shows tension. Specific detail (seventeen plans). The voice is Maya&rsquo;s &mdash; nervous, over-prepared, suddenly blank.'
NOTICE_NEW = '<strong>Notice:</strong> real speech, a pause that shows tension, one specific detail (seventeen plans), and Maya&rsquo;s own nervous voice.'
ALEX_OLD = '    <div class="key-concept">\n      <div class="key-concept-label">&#x1F440; Watch How &mdash; Alex&rsquo;s Draft Scene</div>\n'
ALEX_NEW = '    <div class="key-concept"><details><summary style="cursor:pointer;">\n      <div class="key-concept-label" style="display:inline;">&#x1F440; See Alex&rsquo;s draft scene again</div></summary>\n'
ALEX_END = re.compile(r'(suddenly blank\.</p>|own nervous voice\.</p>)\n    </div>\n    <div class="textbox-prompt">')
FIX = {
 1: [(SECOND_Q[1], '', 1), (NOTICE_OLD, NOTICE_NEW, 1),
     ('Dialogue tags tell the reader <em>how</em> someone is speaking. Fleischman uses them brilliantly. This week&rsquo;s spelling words are verbs used as dialogue tags:',
      'Dialogue tags tell <em>how</em> someone speaks. This week&rsquo;s spelling words are tags:', 1),
     ('Many of these end in <em>-ed</em> or contain tricky double letters. Learn the spelling by learning the word.</p>', 'Watch the <em>-ed</em> endings and the double letters.</p>', 1)],
 2: [(SECOND_Q[2], '', 1), (NOTICE_OLD, NOTICE_NEW, 1), (ALEX_OLD, ALEX_NEW, 1)],
 3: [(SECOND_Q[3], '', 1), (NOTICE_OLD, NOTICE_NEW, 1), (ALEX_OLD, ALEX_NEW, 1),
     ('Today <strong>reread</strong> a comic passage and take it apart. A joke on the page has a structure: setup, expectation, and a turn that breaks it. Fleischman also uses character to carry humor &mdash; Praiseworthy solving a problem in the most dignified way possible is funny because of who he is.',
      'Today <strong>reread</strong> a funny passage and take it apart. A joke has a setup and a turn. Praiseworthy is funny because he solves silly problems in the most dignified way.', 1),
     ('Each one tells the reader exactly how the character sounds. Good writers choose the precise tag rather than defaulting to &ldquo;said.&rdquo;</p>', 'Each one tells how the character sounds.</p>', 1)],
 4: [(SECOND_Q[4], '', 1), (NOTICE_OLD, NOTICE_NEW, 1), (ALEX_OLD, ALEX_NEW, 1),
     ('Now <strong>put the week together</strong>. Comedy is not the opposite of seriousness. Fleischman is writing about a gold rush that ruined a great many people, and the humor is part of how he tells that story without flinching. Ask what the laughter makes bearable, and what it keeps you reading toward.',
      'Now <strong>put the week together</strong>. Funny and serious can sit side by side. Ask what the laughter does for the story.', 1),
     ('Three Comic Techniques in BTGHS</div>', 'Three Comic Techniques in <em>By the Great Horn Spoon!</em></div>', 1),
     ('Putting things that should never touch right next to each other. A butler shoveling coal. A pig hiding in the captain&rsquo;s cabin. Eighteen barrels of &ldquo;spoiled&rdquo; potatoes saving a vineyard. The comedy comes from the mismatch.',
      'Putting things side by side that don&rsquo;t belong together: a butler shoveling coal, a pig in the captain&rsquo;s cabin, spoiled potatoes saving a vineyard.', 1),
     ('Praiseworthy maintains perfect dignity in every absurd situation. He is funnier because he refuses to acknowledge anything is unusual. &ldquo;As unconcerned as you please.&rdquo;',
      'Praiseworthy stays perfectly calm and polite in every silly situation, as if nothing were unusual.', 1),
     ('Comedy needs stakes. The pig must survive until Rio. The ship must make it around the Horn. The grapes must not die before Callao. The more urgent the situation, the funnier the absurd solution.',
      'Comedy needs something at stake: the pig must escape the cook, the ship must survive the storms, the grape cuttings must live until Callao.', 1),
     ('Compare using &ldquo;said&rdquo; vs. &ldquo;bellowed&rdquo; vs. &ldquo;muttered&rdquo; in dialogue. Why does word choice in the tag matter? Use one example from this week&rsquo;s reading to show the difference.',
      'Why does the tag matter? Compare <em>said</em>, <em>bellowed</em> and <em>muttered</em>, with one example from this week&rsquo;s reading.', 1)],
}
apply = '--apply' in sys.argv; out = {}
for k, f in F.items():
    s0 = io.open(f, encoding='utf-8', newline=''); s0 = s0.read(); s = s0
    for old, new, n in FIX[k]:
        c = s.count(old)
        if c != n: sys.exit('%s: %d x %r' % (f, c, old[:60]))
        s = s.replace(old, new)
    if k > 1:
        s, c = ALEX_END.subn(lambda m: m.group(1) + '</details>\n    </div>\n    <div class="textbox-prompt">', s)
        if c != 1: sys.exit('alex end ' + f)
    if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div ' + f)
    if s.count('<details') != s.count('</details>'): sys.exit('details ' + f)
    w0 = len(re.sub(r'<[^>]+>', ' ', s0).split()); w1 = len(re.sub(r'<[^>]+>', ' ', s).split())
    out[f] = s; print('ok', f, 'page words', w0, '->', w1)
if apply:
    for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
    print('written')
