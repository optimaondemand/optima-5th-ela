#!/usr/bin/env python3
"""Week 27 pages brought in line with the scope (v2_poetry scope week 27), approved by Bethany Nov 23 2026
(claude/g5-ela-wk27-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk27.py spelling|rwm|poetry|wgrd|writing|standards [--apply]
Book lines checked against the By the Great Horn Spoon! text (Ch. 7-9).
Poems (public domain, copied from Wikisource Nov 23 2026):
  Robert Browning, "How They Brought the Good News from Ghent to Aix" (Dramatic Romances and Lyrics, 1845), stanza 1, text as in
  Poems That Every Child Should Know (1904), ed. Mary E. Burt (the 1897 Bells and Pomegranates printing has a comma after "watch"
  and capitals on He/Three; words the same).
  Robert Louis Stevenson, "From a Railway Carriage", A Child's Garden of Verses (1885), XXXVII, both stanzas ("for ever" as printed)."""
import io, re, sys
F = {1: 'lesson-27-1-btghs-ch7.html', 2: 'lesson-27-2-btghs-ch8.html', 3: 'lesson-27-3-btghs-ch9.html', 4: 'lesson-27-4-btghs-info.html',
     'flu': 'lesson-27-fluency.html', 'chk': 'lesson-27-checkin.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-26) */
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
    return ('      <textarea class="journal-box" id="%s" data-label="%s" placeholder="%s" oninput="autoSave(this,\'dot-%s\');"></textarea>\n'
            '      <div class="journal-label">&#128211; <span class="saved-dot" id="dot-%s"></span></div>\n') % (id_, label, ph, id_, id_)
def rwm(sentence, ch, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">What happens first, next and last? Does it feel fast or slow to read?</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'First... then... It feels...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'I notice...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('A deep throb ran through the ship &mdash; and then another. Then a splash of the sidewheels could be heard. Then another. And another.', 7,
        'This is <strong>pacing</strong>. Fleischman puts the sounds in order (a throb, then a splash) and then makes each sentence shorter: &ldquo;Then another. And another.&rdquo; Short pieces make you read faster, the way the sidewheels speed up. Which words tell you the order?',
        'Write three sentences for the middle of your adventure where something speeds up. Put the steps in order, and make the last two very short.', None),
 2: rwm('The water turned brown from the dirt and mud that had gathered in Quartz Jackson&rsquo;s whiskers and hair. Finally he poured off everything &mdash; everything but a thin residue at the bottom of the pan. Jack&rsquo;s eyes opened like blossoms. Gold dust!', 8,
        'The order word <em>Finally</em> keeps the steps of panning in <strong>sequence</strong>. Then the pace changes: two long sentences of slow work, a short one, and then just two words. The short ending lands like a surprise. Where does the pace change?',
        'Use the frame to write a short sequence for your own middle that ends with a surprise.', 'First, ___. Then ___. Finally, ___. (one very short sentence: the surprise)'),
 3: rwm('It was almost an hour before he awoke. His hand rested on the pistol and he tipped the hat back off his face. He looked straight into Jack&rsquo;s eyes with the faintest of smiles, as if he hadn&rsquo;t been asleep at all. Jack very nearly jumped. It was Mr. Cut-Eye Higgins.', 9,
        'Here Fleischman <strong>slows the moment down</strong>. Each sentence adds one small step in order (he wakes, his hand rests on the pistol, he tips back the hat, he looks at Jack), so you have to wait. Then the last line is short and plain. Slow steps build the suspense; the short line lets it go.',
        'Find the most tense moment in your middle. Slow it down with three small steps in order, then end with one short sentence.', None),
 4: rwm('Beat by beat of her sidewheels, the Lady Wilma pulled slowly ahead. Wood sparks showered from her funnel. She entered the sparkling narrows of the Golden Gate and finally came out into San Francisco Bay.', 7,
        'On your own this time. Name the order words, tell whether the pace feels fast or slow, and say why &ldquo;Beat by beat&rdquo; fits a race this close.',
        'Revise two or three sentences of your middle so the order is clear and the pace matches the action.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box on the Reading tab.</div></div>'
CHKL = '<div class="turn-in-checklist">'

# ---- poetry
GHENT = ('I sprang to the stirrup, and Joris, and he;<br>I galloped, Dirck galloped, we galloped all three;<br>'
         '&ldquo;Good speed!&rdquo; cried the watch as the gate-bolts undrew;<br>&ldquo;Speed!&rdquo; echoed the wall to us galloping through;<br>'
         'Behind shut the postern, the lights sank to rest,<br>And into the midnight we galloped abreast.')
RAIL = ('Faster than fairies, faster than witches,<br>Bridges and houses, hedges and ditches;<br>And charging along like troops in a battle,<br>'
        'All through the meadows the horses and cattle:<br>All of the sights of the hill and the plain<br>Fly as thick as driving rain;<br>'
        'And ever again, in the wink of an eye,<br>Painted stations whistle by.<br><br>'
        'Here is a child who clambers and scrambles,<br>All by himself and gathering brambles;<br>Here is a tramp who stands and gazes;<br>'
        'And there is the green for stringing the daisies!<br>Here is a cart run away in the road<br>Lumping along with man and load;<br>'
        'And here is a mill and there is a river:<br>Each a glimpse and gone for ever!')
def poem_block(sub, intro, label, title, author, lines, note, prompt):
    return ('<!-- poetry-corner:auto -->\n  <div class="activity bl-navy">\n'
      '    <div class="activity-head"><div class="activity-num" style="background:#0E3A5C;">📜</div>\n      <div style="flex:1;"><div class="activity-title">Poetry Corner</div>\n'
      '      <div class="activity-sub">%s</div></div>\n    </div>\n    <div class="activity-body">\n      <p>%s</p>\n'
      '      <div class="poetry-block">\n        <div class="poetry-label">📜 %s</div>\n        <div class="poetry-title">%s</div>\n        <div class="poetry-author">%s</div>\n'
      '        <div class="poetry-lines">\n          %s\n        </div>\n      </div>\n'
      '      <div class="callout callout-tip"><span class="callout-icon">💡</span><p>%s</p></div>\n'
      '      <div class="socratic-box"><div class="socratic-label">🤔 Think — Write in Your Journal</div>\n        <p class="socratic-q">%s</p>\n      </div>\n'
      '      <p style="font-size:13px;color:#7A88A8;font-style:italic;margin-top:10px;">Write your response in your reading journal.</p>\n    </div>\n  </div>\n<!-- /poetry-corner:auto -->') % (sub, intro, label, title, author, lines, note, prompt)
POEM = {
 2: poem_block('Pacing: meter and line length driving the action',
      'Robert Browning published this poem in 1845. Three riders gallop through the night to carry important news. Read it aloud and listen for the hoofbeats.',
      'Week 27 Poem', '&ldquo;How They Brought the Good News from Ghent to Aix&rdquo; (stanza 1)', 'Robert Browning, 1845 &mdash; public domain', GHENT,
      '<strong>Meter</strong> is the beat under the words. Here the beat sounds like hooves: da-da-DUM, da-da-DUM. Say line 2 and hear it: &ldquo;I GALloped, Dirck GALloped, we GALloped all THREE.&rdquo; Every line has four strong beats and is about the same length, so the poem never slows down, just like the riders. Browning never even tells us what the news is. The poem is all speed.',
      'Tap the four strong beats in lines 1 and 2. Then write 2&ndash;3 sentences: how does the beat make the ride feel fast? Compare it to the last night of the race in Chapter 7.'),
 4: poem_block('Pacing: meter and line length driving the action',
      'Robert Louis Stevenson wrote this poem for children in <em>A Child&rsquo;s Garden of Verses</em> (1885). A child looks out of a train window. Read it aloud as fast as the train.',
      'Week 27 Poem', '&ldquo;From a Railway Carriage&rdquo;', 'Robert Louis Stevenson, 1885 &mdash; public domain', RAIL,
      'Look at the <strong>line length</strong>. Most lines are long and packed with quick little words. A few lines are short: &ldquo;Fly as thick as driving rain&rdquo; and &ldquo;Painted stations whistle by.&rdquo; Short lines flash past, like a station seen from the window. The last line is a glimpse too: &ldquo;Each a glimpse and gone for ever!&rdquo; Line length controls how fast you read.',
      'Find the two shortest lines in the first stanza. Explain what they do to your reading speed. Then name one moment in Chapters 7&ndash;9 where Fleischman uses a short sentence the same way.'),
}
POEM_RE = re.compile(r'<!-- poetry-corner:auto -->.*?<!-- /poetry-corner:auto -->', re.S)

# ---- WGRD lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
LENS = {
 1: [('Name the problem', 'When trouble starts, note exactly what is in the way.'),
     ('Track the fix', 'Note the solution a character chooses, and what it costs.'),
     ('Watch what it causes', 'Every solution sets up the next problem. Look for the chain.')],
 2: [('Ask what caused it', 'For each event, ask what made it happen.'),
     ('Ask what it opened up', 'For each decision, ask what it made possible and what it ruled out.'),
     ('Spot the small choice', 'Notice where a small choice has a big result.')],
 3: [('Mark the problem', 'Mark the moment a problem appears.'),
     ('Mark every try', 'Mark every attempt to solve it, including the ones that fail.'),
     ('Mark the result', 'Mark what happens, and ask whether the character could have seen it coming.')],
}
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*){3}(</ol>)', re.S)
WATCH = {
 1: ('not just what happens, but what each solution sets in motion.</p>', 'not just what happens, but what each solution sets in motion. As you read Chapter 7, watch the coal: who has it, who loses it, and what that causes.</p>'),
 2: ('while they are in it. Watch the links.</p>', 'while they are in it. Watch the links. As you read, watch the prices, and watch for one small choice that changes everything.</p>'),
 3: ('and notice how Fleischman constructs it.</p>', 'and notice how Fleischman constructs it. As you reread, watch how Praiseworthy plans for trouble before it arrives.</p>'),
 4: ('the novel makes history human.</p>', 'the novel makes history human. Then pull the week together: one problem, its solution, and what that solution caused, from Chapter 7, 8 or 9.</p>'),
}

# ---- spelling (-tion/-sion + related word families)
FAM1 = ('''<div class="key-concept"><div class="key-concept-label">📌 Word Families</div>
  <p>A <strong>word family</strong> is a group of words built on the same base. Adding <em>–tion</em> or <em>–sion</em> makes one member; other endings make more:</p>
  <p>invade → <strong>invasion</strong>, <strong>invader</strong> &middot; decide → <strong>decision</strong>, <strong>decisive</strong> &middot; attract → <strong>attraction</strong>, <strong>attractive</strong> &middot; direct → <strong>direction</strong>, <strong>director</strong></p>
  <p>From Chapter 7: the crew is too busy to bother with &ldquo;the invasion of Peruvian cats.&rdquo; <em>Invasion</em> belongs to the family of <em>invade</em>.</p>
</div>
''')
SP = {
 1: [('<div class="callout callout-info"><span class="callout-icon">✏️</span>\n  <p>In your journal: Write all eight words, break each into base + suffix',
      FAM1 + '<div class="callout callout-info"><span class="callout-icon">✏️</span>\n  <p>In your journal: Write all eight words, break each into base + suffix', 1)],
 2: [('Notice: the stressed syllable is almost always the one <em>before</em> the suffix.</p>',
      'Notice: the stressed syllable is almost always the one <em>before</em> the suffix.</p>\n  <p style="font-size:13px;color:#7A88A8;margin-top:6px;"><strong>Word families in Chapter 8:</strong> Quartz Jackson keeps groaning &ldquo;Ruination!&rdquo; (<em>ruin</em> → <em>ruination</em>). &ldquo;We&rsquo;ll wait,&rdquo; says Praiseworthy &ldquo;with decision&rdquo; (<em>decide</em> → <em>decision</em>). The miner didn&rsquo;t want to break in on their &ldquo;conversation&rdquo; (<em>converse</em> → <em>conversation</em>).</p>', 1)],
 3: [('Underline the –tion or –sion in each word.</div>',
      'Underline the –tion or –sion in each word. Then pick one word and write two more words from its family (like <em>decide</em>, <em>decision</em>, <em>decisive</em>).</div>', 1)],
 4: [('Why do these suffixes appear so often in nonfiction and informational writing?</p>',
      'Then show one word family: a base word and two words built from it. Why do these suffixes appear so often in nonfiction and informational writing?</p>', 1)],
}

# ---- writing
PUB = '      <span class="wp-step">Publish</span>\n    </div>\n'
def stage(text):
    return PUB + '    <div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">&#128204;</span><p>%s</p></div>\n' % text
TITLE = 'Writer&#x2019;s Workshop &middot; Week 27 &middot; BUILD THE MIDDLE</div>'
WR = {
 1: [(TITLE, 'Writer&#x2019;s Workshop &middot; Week 27 &middot; BUILD THE MIDDLE &middot; Plan</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Plan the middle.</strong> Answer the three questions below in a few words each, at the top of your box. That is your plan. Then start writing.'), 1)],
 2: [(TITLE, 'Writer&#x2019;s Workshop &middot; Week 27 &middot; BUILD THE MIDDLE &middot; Draft with support</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Draft with support.</strong> Keep writing your middle. If you get stuck, use these frames: <em>Just when ___ seemed safe, ___.</em> &middot; <em>My hero tried ___, but ___.</em> &middot; <em>First ___. Then ___. Finally ___.</em>'), 1)],
 3: [(TITLE, 'Writer&#x2019;s Workshop &middot; Week 27 &middot; BUILD THE MIDDLE &middot; Revise</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Revise using a checklist.</strong> Check your middle: (1) something goes wrong that your hero did not expect; (2) their first try makes things worse; (3) the steps are in a clear order; (4) one tense moment is slowed down, with a short sentence at the end; (5) it ends on a question, not an answer. Fix anything missing.'), 1)],
 4: [(TITLE, 'Writer&#x2019;s Workshop &middot; Week 27 &middot; BUILD THE MIDDLE &middot; Submit</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Submit.</strong> Read your middle once more, then put the whole middle section in the box below. It goes to your teacher with the rest of your work when you copy it into Canvas.'), 1)],
}
V13 = '<span class="fl-code">ELA.5.V.1.3</span>'
ST = {k: [(V13, V13 + ' &middot; <span class="fl-code">ELA.5.R.3.2</span> &middot; <span class="fl-code">ELA.K12.EE.1.1</span>', 1)] for k in F}

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'poetry':
        for d in (2, 4): P[d] = [(POEM_RE, POEM[d], 1), ('Frost', None, 0)]
    elif which == 'wgrd':
        for d in (1, 2, 3): P[d] = [(OL_RE, lambda m, d=d: m.group(1) + ol(LENS[d]) + m.group(2), 1), (WATCH[d][0], WATCH[d][1], 1)]
        P[4] = [(WATCH[4][0], WATCH[4][1], 1)]
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
            if new is None:
                if s.count(old) != n: sys.exit('%s: %d x %r after' % (f, s.count(old), old))
                continue
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
