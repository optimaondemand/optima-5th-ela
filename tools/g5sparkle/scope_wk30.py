#!/usr/bin/env python3
"""Week 30 pages brought in line with the scope (v2_poetry scope week 30), approved by Bethany Nov 24 2026
(claude/g5-ela-wk30-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk30.py rwm|poetry|wgrd|writing [--apply]
Read Like a Writer lines are real chapter endings already read (Ch. 7, 16, 17, 18), checked against the book.
Poem: Poe, "Eldorado" (1849), checked word for word on Wikisource (The Works of the Late Edgar Allan Poe, 1859, vol. 2, p. 46).
Morphology, spelling, grammar and standards already match."""
import io, re, sys
F = {1: 'lesson-30-1-btghs-ch16.html', 2: 'lesson-30-2-btghs-ch17.html', 3: 'lesson-30-3-btghs-ch18.html', 4: 'lesson-30-4-btghs-synthesis.html',
     'flu': 'lesson-30-fluency.html', 'chk': 'lesson-30-checkin.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-28) */
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
def rwm(sentence, ch, reader, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, reader, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'I notice...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'The writer...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))

R = {
 1: rwm('After a 15,000-mile voyage and five months at sea, the gold-seekers had arrived.', 7,
        'This is the last sentence of Chapter 7. How does it make you feel about the whole voyage?',
        'This is a <strong>conclusion</strong>. In one sentence Fleischman looks back at the whole adventure (<em>15,000 miles</em>, <em>five months</em>) and then lands on one plain word: <em>arrived</em>. A good ending looks back at how far the characters came, then stops at the right word.',
        'Write one sentence that could end your own adventure. Look back at how far your hero came, then land on one strong word.', None),
 2: rwm('When they got the hole four feet deep they couldn&rsquo;t go any farther. They hit bedrock. And struck gold.', 16,
        'Read the three sentences out loud. Which one hits hardest, and why?',
        'This conclusion ties together <strong>adventure</strong> (digging a grave), <strong>character</strong> (the partners keep working when things look hopeless) and <strong>theme</strong> (doing right pays off in a way nobody expects). The sentences get shorter and shorter, so the last three words land with a thump.',
        'Use the frame to write a three-sentence ending for your adventure. Make each sentence shorter than the one before.', 'They ___. They ___. And ___.'),
 3: rwm('&ldquo;It wasn&rsquo;t a fair match, no sir,&rdquo; Jack grinned. &ldquo;The Mountain Ox can hardly read or write. Why, he doesn&rsquo;t know B from a bull&rsquo;s foot.&rdquo;', 17,
        'Where have you heard &ldquo;B from a bull&rsquo;s foot&rdquo; before? Why does Jack say it now?',
        'This conclusion connects all three. The <strong>adventure</strong> (the fight) is over. The <strong>character</strong> line shows Jack talking like a real miner now, and teasing like Praiseworthy. The <strong>theme</strong> (brains beat brawn) comes back as a joke, using a phrase the miners said in Chapter 13.',
        'Find the last lines of your adventure. Add one line that brings back a phrase, an object or a joke from earlier in your story. Write the new ending.', None),
 4: rwm('They looked very much like a family. They felt like a family. They were a family.', 18,
        'This is the last line of the whole novel. What has the story been building toward?',
        'On your own this time. How does this ending connect the adventure, the characters and the theme? Think about the three sentences, and the one word that changes from the first to the last.',
        'Write 2&ndash;3 sentences: explain how this ending connects adventure, character and theme, then write one ending sentence for your own story that uses the same move.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box on the Reading tab.</div></div>'
CHKL = '<div class="turn-in-checklist">'

# ---- poetry: Poe, "Eldorado" (1849), text from The Works of the Late Edgar Allan Poe (1859), vol. 2, p. 46, on Wikisource
POEM = '''<div class="poetry-title">&ldquo;Eldorado&rdquo;</div>
        <div class="poetry-author">Edgar Allan Poe, 1849 (from <em>The Works of the Late Edgar Allan Poe</em>, 1859) &mdash; public domain</div>
        <div class="poetry-lines">
          Gaily bedight,<br>
          A gallant knight,<br>
          In sunshine and in shadow,<br>
          Had journeyed long,<br>
          Singing a song,<br>
          In search of Eldorado.<br>
          <br>
          But he grew old&mdash;<br>
          This knight so bold&mdash;<br>
          And o&rsquo;er his heart a shadow<br>
          Fell as he found<br>
          No spot of ground<br>
          That looked like Eldorado.<br>
          <br>
          And, as his strength<br>
          Failed him at length,<br>
          He met a pilgrim shadow&mdash;<br>
          &ldquo;Shadow,&rdquo; said he,<br>
          &ldquo;Where can it be&mdash;<br>
          This land of Eldorado?&rdquo;<br>
          <br>
          &ldquo;Over the Mountains<br>
          Of the Moon,<br>
          Down the Valley of the Shadow,<br>
          Ride, boldly ride,&rdquo;<br>
          The shade replied,&mdash;<br>
          &ldquo;If you seek for Eldorado!&rdquo;<br>
        </div>'''
OLD_POEM = re.compile(r'<div class="poetry-title">&ldquo;In a Station of the Metro&rdquo;</div>.*?</div>\s*(?=</div>\s*<div class="callout callout-tip">)', re.S)
def poetry(sub, intro, tip, q):
    return [(OLD_POEM, POEM + '\n      ', 1),
            (re.compile(r'(<div class="activity-title">Poetry Corner</div>\s*<div class="activity-sub">)[^<]*'), lambda m: m.group(1) + sub, 1),
            (re.compile(r'(<div class="activity-body">\s*<p>)[^<]*(</p>\s*<div class="poetry-block">)'), lambda m: m.group(1) + intro + m.group(2), 1),
            (re.compile(r'(<div class="callout callout-tip"><span class="callout-icon">💡</span><p>).*?(</p></div>\s*<div class="socratic-box"><div class="socratic-label">🤔 Think)', re.S), lambda m: m.group(1) + tip + m.group(2), 1),
            (re.compile(r'(🤔 Think — Write in Your Journal</div>\s*<p class="socratic-q">).*?(</p>)', re.S), lambda m: m.group(1) + q + m.group(2), 1)]
POETRY = {
 2: poetry('Every element, working together',
           'Poe wrote this poem in 1849, the year the Gold Rush began. It is short, but all five elements are at work, and they work together.',
           '<strong>Form:</strong> four stanzas of six lines, and every stanza ends with <em>Eldorado</em>. <strong>Rhyme:</strong> the short lines rhyme in pairs (<em>bedight/knight</em>, <em>long/song</em>). <strong>Meter:</strong> short, bouncing lines, like a horse at a walk. <strong>Line breaks:</strong> each stanza&rsquo;s third line ends on <em>shadow</em>. <strong>Figurative language:</strong> the <em>shadow</em> means something different in each stanza.',
           'Pick two elements, for example rhyme and the word <em>shadow</em>. <strong>How do they work together</strong> to change how the knight&rsquo;s search feels from the first stanza to the last?'),
 4: poetry('How the elements combine to make meaning',
           'On Day 2 you saw two elements work together. Today put all of them together and say what they add up to.',
           'The choices reinforce each other. The bouncing beat sounds cheerful at first, and it keeps bouncing while the knight grows old. The word <em>shadow</em> comes back in the same spot every stanza, and each time it grows darker: shade beside sunshine, then sadness, then a ghostly pilgrim, then the Valley of the Shadow. Every stanza ends on <em>Eldorado</em>, so the search never ends.',
           'Write a full paragraph: <strong>name the elements, then explain how they work together</strong> to say something about searching for gold. Connect it to Jack and Praiseworthy if you can. Use evidence for every claim.'),
}

# ---- WGRD: the four elements as lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*)+(</ol>)', re.S)
INTRO_RE = re.compile(r'(What Good Readers Do</div><div class="activity-sub">)[^<]*(</div></div></div>\s*<div class="activity-body">\s*<p>).*?(</p>)', re.S)
Q_RE = re.compile(r'(ask yourself</div>\s*)(?:<p class="socratic-q">.*?</p>\s*)+', re.S)
W = {
 1: ('Set your reading lens &mdash; everything at once',
     'This is the last week of the novel, so read with everything you have. Plot, character, humor and theme are not four separate things; they are one story seen from four sides. As you read Chapter 16, watch one scene do all four jobs at once.',
     [('Plot', 'What happens, and what changes because of it.'), ('Character', 'What a choice shows about the person who makes it.'),
      ('Humor', 'Where Fleischman makes you smile, even in a tight spot.'), ('Theme', 'What the chapter seems to say about doing the right thing.')],
     'Pick one scene in Chapter 16. What does it do for the plot, and what does it show about Praiseworthy?'),
 2: ('Read closely &mdash; the payoff of the setup',
     'A good ending pays off things planted long before. Today read closely and gather evidence for all four elements. As you read Chapter 17, watch for something that pays off a moment from an early chapter.',
     [('Plot', 'Find a payoff, then find where it was set up.'), ('Character', 'Notice what a name, a habit or a promise shows about someone.'),
      ('Humor', 'Find a joke that was set up chapters ago.'), ('Theme', 'Ask what the payoff says about keeping your word.')],
     'Find one thing in Chapter 17 that pays off something from an early chapter. Where was it planted, and which of the four elements does it serve?'),
 3: ('Reread &mdash; the last turns',
     'Today you reread a key passage from the last chapter and look at the author&rsquo;s choices. Look at all four elements together: what happens, who it happens to, how it is told, and what it means. After you read Chapter 18, pick the passage that surprised you most and read it again.',
     [('Plot', 'What the passage changes.'), ('Character', 'Who changes, and how you can tell.'),
      ('Humor', 'Whether the passage makes you smile, and how.'), ('Theme', 'What the passage says about what is worth having.')],
     'Reread the passage that surprised you most. Which of the four elements carries the most weight in it? Use words from the passage.'),
 4: ('Synthesize the novel &mdash; what it was about',
     'Now put the whole novel together. It was a comedy, an adventure, and an argument about what is worth having. State what you think the book is finally saying, and support it from the beginning, the middle and the end.',
     [('Plot', 'One event from the beginning, one from the middle, one from the end.'), ('Character', 'How Jack and Praiseworthy changed, and why.'),
      ('Humor', 'Whether the jokes support the big idea or push against it.'), ('Theme', 'One sentence on what the book says about gold and what is truly valuable.')],
     'What is <em>By the Great Horn Spoon!</em> finally saying about gold and what is truly valuable? Point to the beginning, the middle and the end.'),
}
def wgrd(d):
    sub, intro, lenses, q = W[d]
    return [(INTRO_RE, lambda m: m.group(1) + sub + m.group(2) + intro + m.group(3), 1),
            (OL_RE, lambda m: m.group(1) + ol(lenses) + m.group(2), 1),
            (Q_RE, lambda m: m.group(1) + '<p class="socratic-q">%s</p>\n      ' % q, 1)]

# ---- writing: Publish adventure/literary response, D1 plan, D2 draft with support, D3 revise, D4 submit
TITLE = 'Writer&rsquo;s Workshop &middot; Week 30 &middot; PUBLISH</div>'
TIP = re.compile(r'<div class="callout callout-think"><span class="callout-icon">🏆</span>\s*<p><strong>This is it — the final week\.</strong>.*?</p>\s*</div>', re.S)
BOX = 'textbox-prompt">Write the final published version of your adventure story. Give it a title.'
LABEL = 'data-label="Writer&#x27;s Workshop: Week 30 PUBLISHED ADVENTURE — final version with title"'
SUB = re.compile(r'(Week 30 &middot; PUBLISH[^<]*</div>\s*<div class="activity-sub">)[^<]*')
def stage(t): return '<div class="callout callout-info"><span class="callout-icon">&#128204;</span><p>%s</p></div>' % t
def wr(step, sub, text, box, label, ph=None):
    L = [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 30 &middot; PUBLISH &middot; %s</div>' % step, 1), (SUB, lambda m: m.group(1) + sub, 1),
         (TIP, stage(text), 1), (BOX, 'textbox-prompt">' + box, 1), (LABEL, 'data-label="Writer&#x27;s Workshop: Week 30 %s"' % label, 1)]
    if ph: L.append(('placeholder="Title: ___&#10;&#10;[Your final published adventure story]"', 'placeholder="%s"' % ph, 1))
    return L
WR = {
 1: wr('Plan', 'Plan the conclusion your adventure needs',
       '<strong>Today&rsquo;s step: Plan.</strong> Your adventure is drafted and revised. This week you give it a strong conclusion and publish it. Don&rsquo;t write the ending yet. In the box, collect three notes: (1) what happens at the very end, (2) who your hero has become since the beginning, (3) what your story means, in one sentence.',
       'Plan: your three notes for the conclusion.', 'PLAN — three notes for the conclusion',
       'WHAT HAPPENS AT THE END:&#10;&#10;WHO MY HERO BECAME:&#10;&#10;WHAT MY STORY MEANS:'),
 2: wr('Draft with support', 'Draft your conclusion with frames',
       '<strong>Today&rsquo;s step: Draft with support.</strong> Write your conclusion paragraph from your three notes. If you get stuck, use these frames: <em>At last, ___.</em> &middot; <em>___ was not the same ___ who ___.</em> &middot; <em>Now ___ knew that ___.</em>',
       'Draft: your conclusion paragraph, at least 5 sentences.', 'DRAFT — conclusion paragraph',
       'At last, ...'),
 3: wr('Revise', 'Revise your whole story with the checklist',
       '<strong>Today&rsquo;s step: Revise using the checklist.</strong> Put your new conclusion at the end of your story. Check the conclusion: (1) it ends the main problem; (2) it shows how your hero changed; (3) it hints at what the story means without preaching; (4) the last sentence lands. Then check the whole story with the Final Publishing Checklist below.',
       'Revise: your whole story with its new conclusion, checked and given a title.', 'REVISED ADVENTURE — whole story with conclusion and title'),
}
WR[4] = [(re.compile(r'(<span class="wp-step done">✓ Publish</span>\s*</div>)'), lambda m: m.group(1) + '\n    ' + stage('<strong>Today&rsquo;s step: Submit.</strong> Read your whole story out loud one last time, ending and all. Then put the final version in the box below with its title.'), 1)]

ST = {}   # standards: every scope code is already on all six bars; V.1.3 is kept and taught by a check-in context-clue item (status doc)

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'poetry': P = POETRY
    elif which == 'wgrd':
        for d in (1, 2, 3, 4): P[d] = wgrd(d)
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
            if n == 'oneq': s = one_question(s); continue
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
