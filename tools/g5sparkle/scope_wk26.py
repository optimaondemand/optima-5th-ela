#!/usr/bin/env python3
"""Week 26 pages brought in line with the scope (v2_poetry scope week 26), approved by Bethany Nov 23 2026
(claude/g5-ela-wk26-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk26.py spelling|rwm|poetry|wgrd|writing|standards [--apply]
Book lines checked against the By the Great Horn Spoon! text (Ch. 4-6).
Poems (public domain, copied from Wikisource Nov 23 2026):
  Lewis Carroll, "Jabberwocky", Through the Looking-Glass, ch. I (1871), stanzas 1, 2, 4 and 6 (the second printing
  of stanza 1 on Wikisource reads "wade", a transcription slip; the first and last read "wabe", as in the 1871 text).
  Lewis Carroll, "You Are Old, Father William", Alice's Adventures in Wonderland, ch. V (1866 text), stanzas 1-4."""
import io, re, sys
F = {1: 'lesson-26-1-btghs-ch4.html', 2: 'lesson-26-2-btghs-ch5.html', 3: 'lesson-26-3-btghs-ch6.html', 4: 'lesson-26-4-btghs-humor.html',
     'flu': 'lesson-26-fluency.html', 'chk': 'lesson-26-checkin.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p><button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-25) */
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
      '      <div class="rwm-step-text">What do you hear in this character&rsquo;s voice? What does it make you see or feel?</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'I hear...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'I notice...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('&ldquo;Pig?&rdquo; said Praiseworthy. &ldquo;What pig?&rdquo;', 4,
        'This is <strong>voice</strong>: the way a character sounds. The cook is shouting and waving a meat cleaver, and the pig is stuck in the porthole right behind Praiseworthy&rsquo;s umbrella. Praiseworthy answers with four calm words. The joke is the gap between what he says and what we know. Which word shows he is pretending?',
        'Write two lines of dialogue for your own adventure scene: one character asks a hard question, and your hero answers in a calm voice while hiding something.', None),
 2: rwm('&ldquo;You mean to say, sir,&rdquo; said Mr. Azariah Jones, turning white, &ldquo;that we&rsquo;ve been bouncing around in that awful place?&rdquo;', 5,
        'This sentence has all three parts of a lively scene: <strong>dialogue</strong> (what he says), <strong>reaction</strong> (he turns white) and <strong>voice</strong> (&ldquo;bouncing around in that awful place&rdquo; sounds like him, not like the narrator). The reaction sits in the middle of his words, set off by commas. What does &ldquo;turning white&rdquo; tell you that his words do not?',
        'Use the frame to write one line for your own scene: a character speaks, and a reaction shows how they feel.', '&ldquo;___,&rdquo; said ___, (a reaction: what their face or body does), &ldquo;___.&rdquo;'),
 3: rwm('The Frenchman and the Yankee trader stood facing each other in the sun, and broad smiles crept over their slack, gloomy faces.', 6,
        'No one speaks in this sentence, but it still shows feeling. This is a <strong>reaction</strong>: Fleischman shows the change in the two men (gloomy faces, then broad smiles) instead of saying &ldquo;they were happy.&rdquo; Right after it, the dialogue bursts out. Why does the reaction come before the words?',
        'Find a line of dialogue in your own scene. Add one reaction sentence before or after it that shows how someone feels without naming the feeling.', None),
 4: rwm('&ldquo;Captain,&rdquo; Praiseworthy said with a gleam in his eye. &ldquo;Master Jack appears to be onto your secret.&rdquo;', 5,
        'On your own this time. Name the voice (how does Praiseworthy sound?), the dialogue (what is he really telling the captain?) and the reaction (what does &ldquo;a gleam in his eye&rdquo; show?).',
        'Write two or three sentences for your own scene that use all three: voice, dialogue and a reaction.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box on the Reading tab.</div></div>'
CHKL = '<div class="turn-in-checklist">'

# ---- poetry
JAB = ('&rsquo;Twas brillig, and the slithy toves<br>&nbsp;&nbsp;Did gyre and gimble in the wabe;<br>All mimsy were the borogoves,<br>&nbsp;&nbsp;And the mome raths outgrabe.<br><br>'
       '&ldquo;Beware the Jabberwock, my son!<br>&nbsp;&nbsp;The jaws that bite, the claws that catch!<br>Beware the Jubjub bird, and shun<br>&nbsp;&nbsp;The frumious Bandersnatch!&rdquo;<br><br>'
       '&hellip;<br><br>'
       'And as in uffish thought he stood,<br>&nbsp;&nbsp;The Jabberwock, with eyes of flame,<br>Came whiffling through the tulgey wood,<br>&nbsp;&nbsp;And burbled as it came!<br><br>'
       '&hellip;<br><br>'
       '&ldquo;And hast thou slain the Jabberwock?<br>&nbsp;&nbsp;Come to my arms, my beamish boy!<br>O frabjous day! Callooh! Callay!&rdquo;<br>&nbsp;&nbsp;He chortled in his joy.')
FW = ('&ldquo;You are old, Father William,&rdquo; the young man said,<br>&nbsp;&nbsp;&ldquo;And your hair has become very white;<br>And yet you incessantly stand on your head&mdash;<br>&nbsp;&nbsp;Do you think, at your age, it is right?&rdquo;<br><br>'
      '&ldquo;In my youth,&rdquo; Father William replied to his son,<br>&nbsp;&nbsp;&ldquo;I feared it might injure the brain;<br>But now that I&rsquo;m perfectly sure I have none,<br>&nbsp;&nbsp;Why, I do it again and again.&rdquo;<br><br>'
      '&ldquo;You are old,&rdquo; said the youth, &ldquo;as I mentioned before,<br>&nbsp;&nbsp;And have grown most uncommonly fat;<br>Yet you turned a back-somersault in at the door&mdash;<br>&nbsp;&nbsp;Pray, what is the reason of that?&rdquo;<br><br>'
      '&ldquo;In my youth,&rdquo; said the sage, as he shook his grey locks,<br>&nbsp;&nbsp;&ldquo;I kept all my limbs very supple<br>By the use of this ointment&mdash;one shilling the box&mdash;<br>&nbsp;&nbsp;Allow me to sell you a couple?&rdquo;')
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
 2: poem_block('Voice and diction in a comic poem',
      'Lewis Carroll put this poem in <em>Through the Looking-Glass</em> (1871). Alice finds it in a book and says it is &ldquo;rather hard to understand.&rdquo; Many of the words are made up. Read it aloud anyway and listen to how the words sound.',
      'Week 26 Poem', '&ldquo;Jabberwocky&rdquo; (stanzas 1, 2, 4 and 6)', 'Lewis Carroll, 1871 &mdash; public domain', JAB,
      '<strong>Diction</strong> is word choice. Carroll invents words, but he builds them from sounds you know: <em>slithy</em> sounds like slimy and lithe; <em>burbled</em> sounds like bubbling and gurgling. Two of his made-up words are now real English words: <em>galumph</em> and <em>chortle</em>. Look at the last line: <em>chortled</em> is a dialogue tag, just like this week&rsquo;s spelling words.',
      'Pick two made-up words from the poem. For each one, write what you think it means and which real words its sounds remind you of. Then write one sentence: why is a poem made of nonsense words funny instead of just confusing?'),
 4: poem_block('Voice and diction in a comic poem',
      'Lewis Carroll wrote this poem for <em>Alice&rsquo;s Adventures in Wonderland</em> (1865). Alice tries to recite a serious old poem and these lines come out instead. Here are the first four stanzas. It is a conversation, so watch the quotation marks.',
      'Week 26 Poem', '&ldquo;You Are Old, Father William&rdquo; (stanzas 1&ndash;4)', 'Lewis Carroll, 1865 &mdash; public domain', FW,
      'Every stanza is one speaker. The young man asks polite, worried questions. Father William answers with a straight face, as if standing on your head and selling ointment were perfectly sensible. That is <strong>voice</strong>: each speaker sounds like himself. The comedy comes from how calmly Father William says ridiculous things, a little like Praiseworthy and his umbrella.',
      'Copy one line that shows the young man&rsquo;s voice and one that shows Father William&rsquo;s. Tell how the two voices are different. Then name one place this week where Praiseworthy keeps a straight face the same way.'),
}
POEM_RE = re.compile(r'<!-- poetry-corner:auto -->.*?<!-- /poetry-corner:auto -->', re.S)

# ---- WGRD lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
LENS = {
 1: [('Find the funny moment', 'Mark what made you smile: a surprise, something stretched too far, or someone&rsquo;s reaction.'),
     ('Ask who the joke is on', 'The joke tells you what the author thinks of that character.'),
     ('Watch for the turn', 'Notice where the comedy stops and the chapter turns serious, and how Jack sounds then.')],
 2: [('Find the danger', 'Pick one frightening moment in the storms.'),
     ('Name the tone', 'Is the narrator alarmed, amused or matter-of-fact as he tells it?'),
     ('Read the characters', 'Who stays calm and who panics? What each one says shows who they are.')],
 3: [('Find the setup', 'What does the passage lead you to expect?'),
     ('Find the turn', 'What happens instead?'),
     ('Read the character', 'What does the joke show about the person at the center of it?')],
 4: [('Gather three moments', 'One funny moment from each chapter, and what each one showed about a character.'),
     ('Find the serious line', 'One moment the book does not make funny. Why not?'),
     ('Say what the humor is for', 'In one sentence, tell what the laughter does for the story.')],
}
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*){3}(</ol>)', re.S)
WATCH = {
 1: ('what it never laughs at.</p>', 'what it never laughs at. As you read, watch who the joke is on, and how Jack sounds at Rio when the jokes stop.</p>'),
 2: ('what that steadiness does to you as a reader.</p>', 'what that steadiness does to you as a reader. As you read, watch what Praiseworthy says out loud and what the narrator tells you he really believes.</p>'),
 3: ('is funny because of who he is.</p>', 'is funny because of who he is. As you reread, watch for the setup, the turn, and who gets the credit for the idea.</p>'),
 4: ('and what it keeps you reading toward.</p>', 'and what it keeps you reading toward. Watch for one funny moment from each chapter and the one moment that is not funny at all.</p>'),
}

# ---- spelling (dialogue tags + spelling in quoted speech)
QS1 = ('''      <div class="key-concept"><div class="key-concept-label">📌 Spelling in Quoted Speech</div>
        <p>Inside quotation marks, writers sometimes spell words the way a character <em>says</em> them. When letters are left out, an <strong>apostrophe</strong> takes their place:</p>
        <p><strong>eatin&rsquo;</strong> = eating &middot; <strong>sittin&rsquo;</strong> = sitting &middot; <strong>singin&rsquo;</strong> = singing</p>
        <p>From Chapter 4: &ldquo;Pigs is for eatin&rsquo;, not for pets.&rdquo; &middot; &ldquo;Why, boy &mdash; I&rsquo;m sittin&rsquo; on him.&rdquo;</p>
        <p style="font-size:13px;color:#7A88A8;margin-top:8px;">The apostrophe goes exactly where the missing letter would be. Outside of dialogue, spell the whole word.</p>
      </div>
''')
SP = {
 1: [('Learn the spelling by learning the word.</p>\n      </div>\n', 'Learn the spelling by learning the word.</p>\n      </div>\n' + QS1, 1)],
 2: [('Say each word aloud and listen for the loud beat.</p>',
      'Say each word aloud and listen for the loud beat.</p>\n        <p style="font-size:13px;color:#7A88A8;margin-top:6px;"><strong>Spelling in quoted speech:</strong> in Chapter 5 Mountain Jim says the Strait is worse than grizzly bears that were &ldquo;a mite friendlier.&rdquo; In Chapter 6 he shouts, &ldquo;She&rsquo;s gainin&rsquo; on us!&rdquo; The apostrophe in <em>gainin&rsquo;</em> stands for the missing <em>g</em>.</p>', 1),
     ('id="g26d2ss1-result" style="display:none;"></div></div></div>',
      'id="g26d2ss1-result" style="display:none;"></div></div>'
      '<div class="spotter-sentence" id="g26d2ss2"><span style="font-family:Georgia,serif;display:block;margin-bottom:8px;">Spelling in quoted speech: which is right?</span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g26d2ss2\')" data-correct="false" data-explain="The apostrophe goes where the letter is missing: the g at the end.">&ldquo;She&rsquo;s gain&rsquo;in on us!&rdquo;</span><span style="display:block;height:6px;"></span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g26d2ss2\')" data-correct="true" data-explain="&#9989; Right. gainin&rsquo; = gaining, and the apostrophe sits where the g was.">&ldquo;She&rsquo;s gainin&rsquo; on us!&rdquo;</span><span style="display:block;height:6px;"></span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g26d2ss2\')" data-correct="false" data-explain="A letter is missing, so it needs an apostrophe.">&ldquo;She&rsquo;s gainin on us!&rdquo;</span>'
      '<div class="spotter-result" id="g26d2ss2-result" style="display:none;"></div></div></div>', 1)],
 3: [('Use at least <strong>five</strong> of the eight dialogue tags, each spelled correctly. Underline each tag you use.</div>',
      'Use at least <strong>five</strong> of the eight dialogue tags, each spelled correctly. Underline each tag you use. Give one character a word with a missing letter, and put the apostrophe where the letter was (like <em>eatin&rsquo;</em>).</div>', 1)],
 4: [('Use one example from this week&rsquo;s reading to show the difference. Write 3&ndash;4 sentences.</p>',
      'Use one example from this week&rsquo;s reading to show the difference. Then tell what the apostrophe in <em>eatin&rsquo;</em> stands for. Write 3&ndash;4 sentences.</p>', 1),
     ('id="g26d4ss3-result" style="display:none;"></div></div></div>',
      'id="g26d4ss3-result" style="display:none;"></div></div>'
      '<div class="spotter-sentence" id="g26d4ss4"><span style="font-family:Georgia,serif;display:block;margin-bottom:8px;">Mountain Jim says the barrel is where he is sitting. Which spelling shows how he talks?</span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g26d4ss4\')" data-correct="true" data-explain="&#9989; Right. The apostrophe stands for the missing g, and the reader hears his voice.">&ldquo;I&rsquo;m sittin&rsquo; on him.&rdquo;</span><span style="display:block;height:6px;"></span>'
      '<span class="spotter-word" onclick="g5Spot(this,\'g26d4ss4\')" data-correct="false" data-explain="The g is missing, so an apostrophe goes in its place.">&ldquo;I&rsquo;m sittin on him.&rdquo;</span>'
      '<div class="spotter-result" id="g26d4ss4-result" style="display:none;"></div></div></div>', 1)],
}

# ---- writing
PUB = '      <span class="wp-step">Publish</span>\n    </div>\n'
def stage(text):
    return PUB + '    <div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">&#128204;</span><p>%s</p></div>\n' % text
TITLE = 'Writer&rsquo;s Workshop &middot; Week 26 &middot; DRAFT</div>'
WR = {
 1: [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 26 &middot; DRAFT &middot; Plan</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Plan the scene.</strong> Before you write, jot four things at the top of your box: who is in the scene, where it happens, what goes wrong, and one line your hero says. Then start the scene in the middle of the action.'), 1)],
 2: [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 26 &middot; DRAFT &middot; Draft with support</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Draft with support.</strong> Keep writing your scene. If you get stuck, use these frames: <em>&ldquo;___,&rdquo; ___ said, ___ (a reaction).</em> &middot; <em>Just then, ___.</em> &middot; <em>My hero could not ___, so ___.</em>'), 1)],
 3: [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 26 &middot; DRAFT &middot; Revise</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Revise using a checklist.</strong> Check your scene: (1) it starts in the middle of the action; (2) at least one exchange of dialogue, punctuated correctly; (3) a new paragraph for each new speaker; (4) at least one reaction that shows a feeling; (5) your hero sounds like themself. Fix anything missing.'), 1)],
 4: [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 26 &middot; DRAFT &middot; Submit</div>', 1),
     (PUB, stage('<strong>Today&rsquo;s step: Submit.</strong> Add one comic moment, then put your whole scene in the box below. It goes to your teacher with the rest of your work when you copy it into Canvas.'), 1)],
}
EE6 = '<span class="fl-code">ELA.K12.EE.6.1</span>'
R14 = '<span class="fl-code">ELA.5.R.1.4</span>'
ST = {k: [(EE6, EE6 + ' &middot; <span class="fl-code">ELA.K12.EE.1.1</span>', 1)] for k in F}
for k in (2, 4): ST[k].append((R14, R14 + ' &middot; <span class="fl-code">ELA.5.R.3.1</span>', 1))

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'poetry':
        for d in (2, 4): P[d] = [(POEM_RE, POEM[d], 1), ('Hopkins', None, 0)]
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
