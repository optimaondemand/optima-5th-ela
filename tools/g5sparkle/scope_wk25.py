#!/usr/bin/env python3
"""Week 25 pages brought in line with the scope (v2_poetry scope week 25), approved by Bethany Nov 22 2026
(claude/g5-ela-wk25-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk25.py spelling|rwm|poetry|wgrd|writing|standards
Book lines checked against the By the Great Horn Spoon! text (Ch. 1-3).
Poems (public domain, copied from Wikisource Nov 22 2026):
  Edward Lear, "The Jumblies", Nonsense Songs, Stories, Botany, and Alphabets (1871), stanzas I and III.
  Lewis Carroll, "The Walrus and the Carpenter", Through the Looking-Glass, ch. IV (1871), stanzas 1, 2, 7, 8."""
import io, re, sys
F = {1: 'lesson-25-1-btghs.html', 2: 'lesson-25-2-btghs-ch1.html', 3: 'lesson-25-3-btghs-ch2.html', 4: 'lesson-25-4-btghs-ch3.html',
     'flu': 'lesson-25-fluency.html', 'chk': 'lesson-25-checkin.html'}
READ_NEXT = re.compile(r'(  <div class="tab-next-wrap">\n    <p class="tab-transition-voice">[^<]*</p>\n    <button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-24) */
.rwm-box{background:#FFFFFF;border:2px solid #E2E8F4;border-radius:14px;overflow:hidden;margin:18px 0 14px;}
.rwm-header{background:linear-gradient(135deg,#2C5F2E,#1A2D5A);color:#fff;padding:12px 18px;font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;}
.rwm-sentence{background:linear-gradient(135deg,#FFFCF0 0%,#FBF5E6 100%);border-bottom:2px solid #F5E6C8;padding:16px 20px;font-family:'Lora',Georgia,serif;font-size:17px;color:#2C5F2E;line-height:1.7;font-style:italic;}
.rwm-step{padding:14px 20px;border-bottom:1.5px solid #E2E8F4;}
.rwm-step:last-child{border-bottom:none;}
.rwm-step-label{display:flex;align-items:center;gap:8px;font-size:14px;color:#C8A850;font-weight:800;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;}
.rwm-step-text{font-size:15px;color:#3A4A6B;line-height:1.6;}
.rwm-frame{background:#FAFBFF;border:1.5px dashed #8B3A20;border-radius:8px;padding:10px 14px;margin-top:8px;font-family:'Lora',Georgia,serif;font-size:15px;color:#8B3A20;font-style:italic;}
'''
def ta(id_, label, ph):
    return ('      <textarea class="journal-box" id="%s" data-label="%s" placeholder="%s" oninput="autoSave(this,\'dot-%s\');gatherAnswers();"></textarea>\n'
            '      <div class="journal-label">&#128211; <span class="saved-dot" id="dot-%s"></span></div>\n') % (id_, label, ph, id_, id_)
def rwm(sentence, ch, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">&ldquo;%s&rdquo; <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">What does this sentence make you see or feel?</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'This sentence makes me...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'I notice...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentence...'))
R = {
 1: rwm('Gold had been discovered in California some twelve months before and now, in a rush, the Gold Rush was on.', 1,
        'Here is how an adventure starts. In one sentence Fleischman gives the <strong>setting</strong> (California, a year after gold was found) and the <strong>pull</strong> that starts everyone moving (the rush for gold). What word in the sentence shows that people are hurrying?',
        'Write one sentence for your own adventure that gives the setting and the thing that pulls your hero into action.', None),
 2: rwm('And then Jack had overheard Banker Stites tell Aunt Arabella that her inheritance was almost gone.', 1,
        'This is Jack&rsquo;s <strong>problem</strong>, the reason the whole adventure begins. The family money is almost gone, and even the old house may have to be sold. Fleischman tells it in one plain sentence. Why does a problem like this make Jack want to act?',
        'Use the frame to write your hero&rsquo;s problem in one sentence.', 'My hero ___ has to ___, because ___.'),
 3: rwm('The boiler room was becoming distinctly overheated.', 2,
        'The setting is becoming a problem too. The hotter the boiler room gets, the more Jack and Praiseworthy need to catch the thief and win back their money. In an adventure, the setting can push the hero to act. How does this sentence add pressure?',
        'Look at your plan. Write one sentence where your setting makes your hero&rsquo;s problem harder.', None),
 4: rwm('To come to the aid of the square-rigger could very well mean that the Lady Wilma might be put out of the race.', 3,
        'On your own this time. Name the problem in this moment and what is at stake. How does the setting, a ship stuck near the equator with no wind, make the choice harder?',
        'Write two sentences for your own story: a moment when your hero must choose, and what is at stake.', None),
}
CHK_RWM = '    <div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div>I answered the Read Like a Writer box on the Reading tab.</div></div>\n'
TURN_T = re.compile(r'(<div class="turn-in-title">[^<]*</div>\n)')
GATHER1_OLD = "  out+='\\n✍️ WRITER\\'S WORKSHOP — WEEK 25 PLAN\\n';"
GATHER1_NEW = ("  out+='\\n📖 READ LIKE A WRITER\\n';\n"
               "  ['journal-rwm-reader','journal-rwm-writer','journal-rwm-mimic'].forEach(function(id,i){var e=document.getElementById(id);if(e){out+=['As a Reader','As a Writer','Try It'][i]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';}});\n\n"
               + GATHER1_OLD)

# ---- poetry
JUMB = ('They went to sea in a Sieve, they did,<br>In a Sieve they went to sea:<br>In spite of all their friends could say,<br>'
        'On a winter&rsquo;s morn, on a stormy day,<br>In a Sieve they went to sea!<br>And when the Sieve turned round and round,<br>'
        'And every one cried, &ldquo;You&rsquo;ll all be drowned!&rdquo;<br>They called aloud, &ldquo;Our Sieve ain&rsquo;t big,<br>'
        'But we don&rsquo;t care a button! we don&rsquo;t care a fig!<br>In a Sieve we&rsquo;ll go to sea!&rdquo;<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;Far and few, far and few,<br>&nbsp;&nbsp;&nbsp;&nbsp;Are the lands where the Jumblies live;<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;Their heads are green, and their hands are blue,<br>&nbsp;&nbsp;&nbsp;&nbsp;And they went to sea in a Sieve.<br><br>'
        'The water it soon came in, it did,<br>The water it soon came in;<br>So to keep them dry, they wrapped their feet<br>'
        'In a pinky paper all folded neat,<br>And they fastened it down with a pin.<br>And they passed the night in a crockery-jar,<br>'
        'And each of them said, &ldquo;How wise we are!<br>Though the sky be dark, and the voyage be long,<br>'
        'Yet we never can think we were rash or wrong,<br>While round in our Sieve we spin!&rdquo;<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;Far and few, far and few,<br>&nbsp;&nbsp;&nbsp;&nbsp;Are the lands where the Jumblies live;<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;Their heads are green, and their hands are blue,<br>&nbsp;&nbsp;&nbsp;&nbsp;And they went to sea in a Sieve.')
WALR = ('&ldquo;The sun was shining on the sea,<br>Shining with all his might:<br>He did his very best to make<br>The billows smooth and bright&mdash;<br>'
        'And this was odd, because it was<br>The middle of the night.<br><br>'
        'The moon was shining sulkily,<br>Because she thought the sun<br>Had got no business to be there<br>After the day was done&mdash;<br>'
        '&lsquo;It&rsquo;s very rude of him,&rsquo; she said,<br>&lsquo;To come and spoil the fun!&rsquo;<br><br>'
        '&hellip;<br><br>'
        '&lsquo;O Oysters, come and walk with us!&rsquo;<br>The Walrus did beseech.<br>&lsquo;A pleasant walk, a pleasant talk,<br>'
        'Along the briny beach:<br>We cannot do with more than four,<br>To give a hand to each.&rsquo;<br><br>'
        'The eldest Oyster looked at him,<br>But never a word he said:<br>The eldest Oyster winked his eye,<br>And shook his heavy head&mdash;<br>'
        'Meaning to say he did not choose<br>To leave the oyster-bed.')
def poem_block(comment, sub, intro, label, title, author, lines, note, prompt):
    return ('<!-- Poetry: %s -->\n  <div class="activity bl-navy">\n'
      '    <div class="activity-head"><div class="activity-num" style="background:#0E1C42;">📜</div><div style="flex:1;"><div class="activity-title">Poetry Corner</div><div class="activity-sub">%s</div></div></div>\n'
      '    <div class="activity-body">\n      <p>%s</p>\n      <div class="poetry-block">\n        <div class="poetry-label">📜 %s</div>\n'
      '        <div class="poetry-title">%s</div>\n        <div class="poetry-author">%s</div>\n        <div class="poetry-lines">\n%s\n        </div>\n      </div>\n'
      '      <div class="callout callout-tip"><span class="callout-icon">💡</span>\n        <p>%s</p>\n      </div>\n'
      '      <div class="socratic-box">\n        <div class="socratic-label">🤔 Think &mdash; Write in Your Journal</div>\n        <p class="socratic-q">%s</p>\n      </div>\n'
      '      <p style="font-size:13px;color:#9A8060;font-style:italic;margin-top:8px;">Write in your reading journal.</p>\n    </div>\n  </div>') % (comment, sub, intro, label, title, author, lines, note, prompt)
POEM = {
 2: poem_block('The Jumblies', 'Humor and tone in verse',
      'Edward Lear published this nonsense poem in 1871. The Jumblies go to sea in a <em>sieve</em>, a kitchen strainer full of holes. Read it aloud and listen to how the Jumblies sound about their own plan.',
      'Week 25 Poem', '&ldquo;The Jumblies&rdquo; (stanzas 1 and 3)', 'Edward Lear, 1871 &mdash; public domain', JUMB,
      '<strong>Tone</strong> is the attitude a writer takes toward the subject. Lear&rsquo;s tone is cheerful and bouncy: quick rhymes, a jolly chorus, &ldquo;we don&rsquo;t care a button!&rdquo; But the plan is silly and dangerous. The humor comes from the gap between how sure the Jumblies sound and what the reader can plainly see.',
      'Copy one line where the Jumblies sound sure of themselves, and tell what makes it funny. In Chapter 1, Jack and Praiseworthy also set out on a risky voyage. Is Fleischman&rsquo;s tone more like Lear&rsquo;s, or more serious? Write 2&ndash;3 sentences.'),
 4: poem_block('The Walrus and the Carpenter', 'Humor and tone in verse',
      'Lewis Carroll wrote this poem for <em>Through the Looking-Glass</em> (1871), where Tweedledee recites it to Alice. Here are four of its stanzas. Read them aloud and listen for the tone.',
      'Week 25 Poem', '&ldquo;The Walrus and the Carpenter&rdquo; (stanzas 1, 2, 7 and 8)', 'Lewis Carroll, 1871 &mdash; public domain', WALR,
      'Carroll&rsquo;s tone is playful from the first line: the sun shines in the middle of the night, and the moon sulks. Then the Walrus speaks very sweetly to the Oysters. Notice how the eldest Oyster answers: he winks, shakes his head and says nothing. A friendly tone can hide a trick.',
      'Which words make the Walrus sound friendly? What clue tells you the eldest Oyster does not trust him? In Chapter 2, Praiseworthy also puts on a show to catch someone. Write 2&ndash;3 sentences comparing the two tricks.'),
}
POEM_OLD = {2: re.compile(r'<!-- Poetry Corner: O Captain! My Captain! -->\n  <div class="activity bl-navy">.*?Write in your reading journal\.</p>\n    </div>\n  </div>', re.S),
            4: re.compile(r'<!-- Poetry: The Road Not Taken -->\n  <div class="activity bl-navy">.*?Write in your reading journal\.</p>\n    </div>\n  </div>', re.S)}

# ---- WGRD lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n        ' % it for it in items)
LENS = {
 1: [('Collect the background facts', 'What real dangers did gold-seekers face on the way to California?'),
     ('Spot the pull', 'What made people leave home anyway? An adventure needs a reason to go.'),
     ('Carry it into the reading', 'Keep two facts in mind and watch how Chapter 1 turns them into Jack&rsquo;s problem.')],
 2: [('Find the problem', 'What has gone wrong at home, and what does Jack want to do about it?'),
     ('Find the two worlds', 'The comedy comes from things that do not belong together, like a butler in a coal bunker.'),
     ('Mark your evidence', 'Find one line that shows Jack&rsquo;s goal and one line that makes you laugh.')],
 3: [('Name the obstacle', 'What stands in the way of Jack and Praiseworthy in Chapter 2?'),
     ('Reread the trick', 'Reread the scene in the dark saloon. When does the author let you in on the plan?'),
     ('Watch the tone', 'Is the moment played for laughs, for tension, or both at once?')],
 4: [('Trace the journey', 'Problem (Chapter 1), obstacle (Chapter 2), hard choice (Chapter 3). What is at stake now?'),
     ('Notice what repeats', 'A theme announces itself by coming back.'),
     ('Say the theme as a sentence', 'Make it true about people, not only about this plot.')],
}
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*){3}(</ol>)', re.S)
WATCH = {
 1: ('completely real &mdash; and completely impossible.</p>', 'completely real &mdash; and completely impossible. As you read, watch for the problem that sends Jack to sea.</p>'),
 2: ('That&rsquo;s character.</p>', 'That&rsquo;s character. As you read, watch for Jack&rsquo;s problem, his goal, and the moment he chooses his partner.</p>'),
 3: ('the delight of the absurdity.</p>', 'the delight of the absurdity. As you reread, watch for the obstacle and the exact moment you understand the trick.</p>'),
 4: ('what your title says you are.</p>', 'what your title says you are. As you read, trace the journey: the problem, the obstacle, and the hard choice in Chapter 3.</p>'),
}

# ---- spelling
SORT_OLD = re.compile(r'<p>Place names carry their own spelling problems\. Sort them by the one that will trip you\.</p></div><div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#127919;</span><p><strong>Sort each place name by what makes it hard to spell\.</strong></p></div><div class="sort-game g5-sort" id="g25d1s">.*?<div class="sort-score" id="g25d1s-score" style="display:none;">[^<]*</div></div>', re.S)
CHIP = '<span class="sort-chip" data-group="%s" onclick="g5Pick(this)">%s</span>'
COL = '<div class="sort-col"><div class="sort-col-header" style="background:linear-gradient(135deg,%s);">%s</div><div class="sort-col-drop" data-col="%s" onclick="g5Drop(this)"></div></div>'
SORT_NEW = ('<p>Place names and Gold Rush words carry their own spelling problems. Sort them by the one that will trip you.</p></div>'
  '<div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#127919;</span><p><strong>Sort each word by what makes it hard to spell.</strong></p></div>'
  '<div class="sort-game g5-sort" id="g25d1s"><div class="sort-bank">'
  + ''.join(CHIP % c for c in [('dbl', 'Massachusetts'), ('vow', 'Argonaut'), ('dbl', 'passengers'), ('vow', 'California'), ('dbl', 'Mississippi'), ('vow', 'Sacramento')])
  + '</div><div class="sort-columns">' + COL % ('#8B3A20,#A84A2A', 'Doubled letters', 'dbl') + COL % ('#2C5F2E,#3A7A3C', 'No doubled letters, but an unstressed vowel', 'vow')
  + '</div><div class="sort-score" id="g25d1s-score" style="display:none;">Sorted. Every one of these is a word you will meet or spell this unit.</div></div>')
SP = {
 1: [('<p><strong>e &middot; qua &middot; tor</strong></p>\n', '<p><strong>e &middot; qua &middot; tor</strong></p>\n        <p style="margin-top:8px;"><strong>Gold Rush words:</strong></p>\n        <p><strong>Ar &middot; go &middot; naut</strong></p>\n        <p><strong>pas &middot; sen &middot; ger</strong></p>\n', 1),
     ('<p>3 syllables &mdash; the imaginary line around the middle of the Earth</p>', '<p>3 syllables &mdash; the imaginary line around the middle of the Earth</p>\n  <p>3 syllables &mdash; a gold-seeker who came by sea (Chapter 1)</p>\n  <p>3 syllables &mdash; a traveler on a ship (the <em>Lady Wilma</em> carries 183 of them)</p>', 1),
     (SORT_OLD, SORT_NEW, 1)],
 2: [('&mdash; <strong>e&bull;qua&bull;tor</strong></p>', '&mdash; <strong>e&bull;qua&bull;tor</strong></p>\n        <p style="margin-top:6px;"><strong>Gold Rush words:</strong> <strong>AR&bull;go&bull;naut</strong> (the first syllable is loudest) &mdash; <strong>PAS&bull;sen&bull;ger</strong> (the first syllable is loudest)</p>', 1)],
 3: [('<p><strong>California</strong> &bull; <strong>Sacramento</strong> &bull; <strong>Patagonia</strong> &bull; <strong>equator</strong></p>',
      '<p><strong>California</strong> &bull; <strong>Sacramento</strong> &bull; <strong>Patagonia</strong> &bull; <strong>equator</strong></p>\n        <p>Gold Rush words: <strong>Argonaut</strong> &bull; <strong>passenger</strong></p>', 1),
     ('Then use one of the four words in a sentence about the Gold Rush.', 'Then write one sentence about the Gold Rush that uses one of the four place names and one Gold Rush word (<em>Argonaut</em> or <em>passenger</em>).', 1)],
 4: [('<div class="spotter-result" id="g25d4ss3-result" style="display:none;"></div></div></div>',
      '<div class="spotter-result" id="g25d4ss3-result" style="display:none;"></div></div>'
      '<div class="spotter-sentence" id="g25d4ss4"><span style="font-family:Georgia,serif;display:block;margin-bottom:8px;">Which is right?</span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g25d4ss4\')" data-correct="false" data-explain="The middle vowel is <em>e</em>: pas-<em>sen</em>-gers.">passangers</span><span style="display:block;height:6px;"></span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g25d4ss4\')" data-correct="true" data-explain="&#9989; Double <em>s</em>, then <em>sen</em>.">passengers</span><span style="display:block;height:6px;"></span>'
      '<div class="spotter-result" id="g25d4ss4-result" style="display:none;"></div></div></div>', 1)],
}

# ---- writing
def stage(text):
    return '      </div>\n      <div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">&#128204;</span><p>%s</p></div>' % text
WPUB = '<span class="wp-step">Publish</span>\n      </div>'
WPUB1 = '<span class="wp-step">Publish</span></div>'
WR = {
 2: [('PLAN (Day 2)</div>', 'PLAN &middot; Draft</div>', 1),
     (WPUB, '<span class="wp-step">Publish</span>\n' + stage('<strong>Today&rsquo;s step: Draft with support.</strong> Turn your plan notes into full sentences. If you get stuck, use these frames: <em>My hero is ___, who ___. The trouble starts when ___. If my hero fails, ___.</em>'), 1),
     ("data-label=\"Writer's Workshop: Week 25 PLAN (Day 2 revision)\"", "data-label=\"Writer's Workshop: Week 25 PLAN — Draft (Day 2)\"", 1)],
 3: [('PLAN (Day 3)</div>', 'PLAN &middot; Revise</div>', 1),
     (WPUB, '<span class="wp-step">Publish</span>\n' + stage('<strong>Today&rsquo;s step: Revise using a checklist.</strong> Check your plan: (1) the hero wants one clear thing; (2) something stands in the way; (3) the setting makes it harder; (4) the stakes are clear. Fix anything missing, then add the surprise below.'), 1),
     ("data-label=\"Writer's Workshop: Week 25 PLAN (Day 3 — add surprise element)\"", "data-label=\"Writer's Workshop: Week 25 PLAN — Revise (Day 3)\"", 1)],
 4: [('PLAN (Final)</div>', 'PLAN &middot; Submit</div>', 1),
     (WPUB, '<span class="wp-step">Publish</span>\n' + stage('<strong>Today&rsquo;s step: Submit.</strong> Put your whole plan in the box below. It goes to your teacher with the rest of your work when you copy it into Canvas.'), 1),
     ("data-label=\"Writer's Workshop: Week 25 PLAN (Final — complete plan for drafting next week)\"", "data-label=\"Writer's Workshop: Week 25 PLAN — Submit (Day 4)\"", 1)],
}
V2 = '<span class="fl-code">ELA.5.V.1.2</span>'
R14 = '<span class="fl-code">ELA.5.R.1.4</span>'
ST = {k: [(V2, '<span class="fl-code">ELA.5.V.1.1</span> &middot; ' + V2, 1)] for k in F}
for k in (2, 4): ST[k].append((R14, R14 + ' &middot; <span class="fl-code">ELA.5.R.3.1</span>', 1))
ST[3].append(('info-value">Chapter 2: Catch a Thief</div>', 'info-value">Chapter 2: How to Catch a Thief</div>', 1))
ST[4].append(('info-value">Chapter 3: Sea Raven</div>', 'info-value">Chapter 3: News of the Sea Raven</div>', 1))

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (TURN_T, lambda m: m.group(1) + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
        P[1].append((GATHER1_OLD, GATHER1_NEW, 1))
    elif which == 'poetry':
        for d in (2, 4): P[d] = [(POEM_OLD[d], POEM[d], 1)]
        P[2].append(('info-value">O Captain! My Captain!</div>', 'info-value">The Jumblies</div>', 1))
        P[4].append(('info-value">The Road Not Taken</div>', 'info-value">The Walrus and the Carpenter</div>', 1))
    elif which == 'wgrd':
        for d in (1, 2, 3, 4): P[d] = [(OL_RE, lambda m, d=d: m.group(1) + ol(LENS[d]) + m.group(2), 1), (WATCH[d][0], WATCH[d][1], 1)]
    elif which == 'spelling': P = SP
    elif which == 'writing': P = WR
    elif which == 'standards': P = ST
    else: sys.exit('strand?')
    return P
def main():
    which = sys.argv[1]; apply = '--apply' in sys.argv
    out = {}
    for k, reps in plan(which).items():
        f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in reps:
            if n == 'first':
                if old not in s: sys.exit('%s: no %r' % (f, old))
                s = s.replace(old, new, 1); continue
            if isinstance(old, str):
                c = s.count(old)
                if c != n: sys.exit('%s: %d x %r' % (f, c, old[:70]))
                s = s.replace(old, new)
            else:
                s, c = old.subn(new, s)
                if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:60]))
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print(which, 'ok', f)
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
main()
