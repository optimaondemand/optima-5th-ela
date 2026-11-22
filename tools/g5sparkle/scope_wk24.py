#!/usr/bin/env python3
"""Week 24 pages brought in line with the scope (v2_poetry scope week 24 = v4 week 24), approved by
Bethany Nov 22 2026 (claude/g5-ela-wk24-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk24.py sources|rwm|poetry|writing
Sources (both public domain, copied from the originals Nov 22 2026):
  A. Treaty of Dancing Rabbit Creek, Article III, signed Sept 27 1830 (7 Stat. 333; Kappler II:310).
  B. George W. Harkins, "To the American People", Natchez Weekly Courier, Dec 2 1831, p. 6, as reproduced by
     the Choctaw Nation of Oklahoma (Iti Fabvssa, Oct 2 2023).
Poems: Sigourney "Indian Names", Poems (Philadelphia: Key and Biddle, 1834), Wikisource transcription, stanzas
1 and 3; Bryant "An Indian at the Burial-Place of His Fathers" (1824), text as in Poetical Works (Appleton,
1903), stanzas 1 and 3. Book lines checked against planning docs/hbg_ocr.txt."""
import io, re, sys
F = {1: 'lesson-24-1-hbg-ch28.html', 2: 'lesson-24-2-hbg-ch29.html', 3: 'lesson-24-3-hbg-ch28-29.html', 4: 'lesson-24-4-hbg-ch28-29.html'}
QA = ('&hellip;the Choctaw nation of Indians consent and hereby cede to the United States, the entire country they own and possess, east of the Mississippi River; '
      'and they agree to move beyond the Mississippi River, early as practicable, and will so arrange their removal, that as many as possible of their people '
      'not exceeding one half of the whole number, shall depart during the falls of 1831 and 1832; the residue to follow during the succeeding fall of 1833&hellip;')
QB = ('Yet it is said that our present movements are our own voluntary acts &mdash; such is not the case. &hellip; We go forth sorrowful, knowing that wrong has been done. &hellip; '
      'Here is the land of our progenitors, and here are their bones &hellip; it is dear to us, yet we cannot stay, my people are dear to me, with them I must go. &hellip; '
      'my destiny is cast among the Choctaw people. If they suffer, so will I; if they prosper, then I will rejoice.')
QS = 'style="background:#FFFCF0;border-left:4px solid #8B3A20;border-radius:8px;padding:12px 16px;margin:10px 0;font-family:\'Lora\',Georgia,serif;font-size:15px;line-height:1.75;color:#3A2A1A;"'
CS = 'style="font-size:12px;color:#7A88A8;margin-top:6px;"'
def src_box(label, who, quote, plain, cite):
    return ('      <div class="task-box" style="margin-top:14px;">\n'
            '        <div class="dol-model-label">%s</div>\n'
            '%s'
            '        <div class="source-quote" %s>&ldquo;%s&rdquo;</div>\n'
            '%s'
            '        <p %s>%s</p>\n'
            '      </div>\n') % (label, ('        <p>%s</p>\n' % who) if who else '', QS, quote, ('        <p><strong>In plain words:</strong> %s</p>\n' % plain) if plain else '', CS, cite)
CITE_A = 'Treaty of Dancing Rabbit Creek, Article 3. United States Statutes at Large, volume 7, page 333.'
CITE_B = 'George W. Harkins, &ldquo;To the American People,&rdquo; <em>The Natchez Weekly Courier</em>, December 2, 1831, as shared by the Choctaw Nation of Oklahoma.'
STUDY = ('  <!-- Source Study -->\n'
  '  <div class="activity bl-navy" id="source-study">\n'
  '    <div class="activity-head"><div class="activity-num" style="background:#2C5F2E;">&#128220;</div><div><div class="activity-title">&#128220; Reading &middot; Two Real Sources</div><div class="activity-sub">Read each one slowly. They are short.</div></div></div>\n'
  '    <div class="activity-body">\n'
  '      <p>The novel is a made-up story set inside real history. These two sources come from the real history. Both were written at the time, so both are <strong>primary sources</strong>.</p>\n'
  + src_box('&#128220; Source A &middot; A government document &middot; 1830',
            'On September 27, 1830, leaders of the Choctaw Nation and men sent by the United States government signed the Treaty of Dancing Rabbit Creek in Mississippi. This is part of Article 3.',
            QA, 'The Choctaw Nation gives up all of its land east of the Mississippi River. The people are to leave in groups, in the fall of 1831, 1832 and 1833. (<em>Cede</em> means give up. <em>The residue</em> means the rest.)', CITE_A)
  + src_box('&#9993;&#65039; Source B &middot; A letter from a Choctaw chief &middot; 1831',
            'George W. Harkins was a young Choctaw chief. In 1831 he led about 600 Choctaw people out of Mississippi by steamboat. On the boat he wrote a letter &ldquo;To the American People.&rdquo; A Mississippi newspaper printed it on December 2, 1831. These lines are from that letter.',
            QB, 'People say we are leaving because we want to. That is not true. We leave sad, knowing a wrong has been done. This land holds the bones of our ancestors, but I will go where my people go. (<em>Voluntary</em> means by choice. <em>Progenitors</em> means ancestors.)', CITE_B)
  + '      <div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#128269;</span><p><strong>Keep the story and the record apart.</strong> The first page of the novel says 1830. The treaty shows that the real removal began in the fall of 1831 and went on until 1833. A novelist may change a detail like that. A historian checks it.</p></div>\n'
  '    </div>\n'
  '  </div>\n\n')
AGAIN = ('  <!-- Source Study -->\n'
  '  <div class="activity bl-navy" id="source-study">\n'
  '    <div class="activity-head"><div class="activity-num" style="background:#2C5F2E;">&#128220;</div><div><div class="activity-title">&#128220; Reading &middot; The Two Sources Again</div><div class="activity-sub">Reread them before you write.</div></div></div>\n'
  '    <div class="activity-body">\n'
  '      <p>Here are your two primary sources from Day 3. Choose the line you will quote in your paragraph.</p>\n'
  + src_box('&#128220; Source A &middot; Treaty of Dancing Rabbit Creek &middot; 1830', None, QA, None, CITE_A)
  + src_box('&#9993;&#65039; Source B &middot; George W. Harkins&rsquo;s letter &middot; 1831', None, QB, None, CITE_B)
  + '    </div>\n'
  '  </div>\n\n')
MINI = ('      <div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;"><div class="key-concept-label" style="color:#3D5285;">&#128220; Your two real sources</div>'
        '<p>You will study these closely on Day 3. For now, choose one line to use.</p>'
        '<p><strong>Source A, the Treaty of Dancing Rabbit Creek (1830):</strong> &ldquo;&hellip;they agree to move beyond the Mississippi River &hellip; shall depart during the falls of 1831 and 1832; the residue to follow during the succeeding fall of 1833&hellip;&rdquo;</p>'
        '<p><strong>Source B, a letter by Choctaw chief George W. Harkins (1831):</strong> &ldquo;We go forth sorrowful, knowing that wrong has been done.&rdquo; &ldquo;&hellip;my people are dear to me, with them I must go.&rdquo;</p></div>\n')
INTRO = ('<div class="activity-title">&#128212; Reading &middot; Chapter Introduction</div><div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n        <div class="activity bl-purple" style="margin-bottom:18px;">')
def intro(text):
    return (INTRO, INTRO.replace('<div class="activity-body">\n', '<div class="activity-body">\n        <p>%s</p>\n' % text), 1)
RWM_AT = '  <!-- RWM -->\n  <div class="rwm-box">'
NEXT_A = '  <div class="tab-next-wrap">\n    <button class="tab-next-btn" onclick="switchTab(\'assignment\')">'
P1 = '      <div class="textbox-prompt">Today is the <strong>Plan</strong> stage'
P2 = '      <div class="textbox-prompt">Today is the <strong>Draft with support</strong> stage'

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
 1: rwm('I was a general in the United States Army.', 28,
        'This is a line you can check, and here is a model of a source comparison. <strong>Claim:</strong> The novel&rsquo;s Pushmataha is based on a real man. <strong>Evidence:</strong> In the novel, he says this sentence. The National Park Service&rsquo;s history of the real Pushmataha says he was given the rank of brigadier general. <strong>Reasoning:</strong> The story and the record agree, so this part of the scene is true to history. The meeting itself is made up: the real Pushmataha died in 1824, before this story begins, so in the novel he comes as a ghost.',
        'Find one more thing in Chapter 28 that a historian could check against a real source. Write it as a question that starts with <em>Did</em> or <em>Was</em>.', None),
 3: rwm('The Trail still lay before us.', 29,
        'Use this line as evidence. <strong>Claim:</strong> The Choctaw removal did not end quickly. <strong>Evidence from the novel:</strong> this sentence, from the last chapter. <strong>Evidence from Source A:</strong> the treaty spreads the removal over the falls of 1831, 1832 and 1833. One part is missing: the <strong>reasoning</strong>, a sentence that tells how the evidence supports the claim.',
        'Write the reasoning sentence. Tell how the novel&rsquo;s line and the treaty&rsquo;s dates both support the claim.', 'Both ___ and ___ show that ___, because ___.'),
 4: rwm('Naomi was reunited with her mother and father, and that very evening she insisted on helping with the cooking.', 29,
        'On your own this time. Find one line in Source B, Harkins&rsquo;s letter, that goes with this sentence. Think about what both say about staying with your people.',
        'Write three sentences: a claim, the evidence from each text, and your reasoning. Start each piece of evidence with a source transition, such as <em>In Tingle&rsquo;s novel</em> or <em>In his letter of 1831, Harkins writes</em>.', None),
}
CHK_WW = '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>'
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I wrote my Read Like a Writer answers on the Reading tab.</div></div>\n        '
SIG = ('Ye say they all have passed away,<br>That noble race and brave,<br>That their light canoes have vanished<br>From off the crested wave;<br>'
       'That &rsquo;mid the forests where they roamed<br>There rings no hunter shout,<br>But their name is on your waters,<br>Ye may not wash it out.<br><br>'
       'Ye say their cone-like cabins,<br>That clustered o&rsquo;er the vale,<br>Have fled away like withered leaves<br>Before the autumn gale,<br>'
       'But their memory liveth on your hills,<br>Their baptism on your shore,<br>Your everlasting rivers speak<br>Their dialect of yore.')
BRY = ('It is the spot I came to seek&mdash;<br>My fathers&rsquo; ancient burial-place,<br>Ere from these vales, ashamed and weak,<br>Withdrew our wasted race.<br>'
       'It is the spot&mdash;I know it well&mdash;<br>Of which our old traditions tell.<br><br>'
       'A white man, gazing on the scene,<br>Would say a lovely spot was here,<br>And praise the lawns, so fresh and green,<br>Between the hills so sheer.<br>'
       'I like it not&mdash;I would the plain<br>Lay in its tall old groves again.')
POEMS = {
 2: ('Indian Names (stanzas 1 and 3)', 'Lydia Huntley Sigourney (1834)', SIG,
     'Lydia Sigourney published this poem in 1834, in the same years the Choctaw and other nations were being forced west. That makes it a <strong>primary source</strong>: it shows what one American writer thought at the time. <em>Ye</em> means <em>you</em>. She is speaking to Americans who said Native people had &ldquo;passed away,&rdquo; and she uses the word of her time, &ldquo;Indian.&rdquo; Today we name each nation, such as the Choctaw Nation. <strong>What is her answer to those Americans? A treaty states dates and land. What can this poem show you about 1834 that a treaty cannot?</strong>'),
 4: ('An Indian at the Burial-Place of His Fathers (stanzas 1 and 3)', 'William Cullen Bryant (1824)', BRY,
     'Bryant was not Native. He imagined a Native man coming back to the place where his ancestors are buried. In 1829 a Cherokee newspaper, the <em>Cherokee Phoenix</em>, printed this poem. It is a primary source for what one white poet of the 1820s imagined. It is not a primary source for what a Native person felt. Bryant&rsquo;s speaker calls his people &ldquo;ashamed and weak.&rdquo; <strong>Now reread Source B, the letter a Choctaw chief wrote for himself. Does Harkins sound ashamed? Which source would you trust to tell you how Choctaw people felt, and why?</strong>'),
}
def poem(s, title, author, text, prompt):
    a = s.index('<div class="poem-title">'); b = s.index('</div>', s.index('<div class="poem-text">', a)) + len('</div>')
    q = s.index('<p class="socratic-q">', b); qe = s.index('</p>', q) + 4
    new = ('<div class="poem-title">%s</div>\n        <div class="poem-author">%s</div>\n        <div class="poem-text">%s</div>' % (title, author, text))
    return s[:a] + new + s[b:q] + '<p class="socratic-q">%s</p>' % prompt + s[qe:]
P = {
 'sources': {
   1: [(P1, MINI + P1, 1), ('with what an informational or primary source says.', 'with what a real source from the time says.', 1)],
   2: [(P2, MINI + P2, 1), ('how the novel and one informational source together give', 'how the novel and one of the two real sources together give', 1)],
   3: [intro('Today&rsquo;s reading is short and real. After this introduction you will find two sources from the years of the Choctaw removal: part of a treaty and part of a letter. <strong>As you read each one, ask: who wrote this, when, and why? Then look back at Chapters 28 and 29 for one moment that goes with each source.</strong>'),
       (RWM_AT, STUDY + RWM_AT, 1)],
   4: [intro('Today you finish the unit. Reread the two sources, then look back through Chapters 28 and 29. <strong>Choose the one moment from the novel and the one line from a source that you will set side by side in your paragraph.</strong>'),
       (NEXT_A, AGAIN + NEXT_A, 1)]},
 'rwm': {1: [(NEXT_A, R[1] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)],
         4: [(NEXT_A, R[4] + NEXT_A, 1), (CHK_WW, CHK_RWM + CHK_WW, 1)]},
 'writing': {d: [('&#9675; Apply</span>', '&#9675; Revise</span>', 1)] for d in (1, 2, 4)},
}
P['writing'][3] = [
 ('&#9733; Apply</span>', '&#9733; Revise</span>', 1),
 ('Writer&rsquo;s Workshop: Week 24 &middot; APPLY', 'Writer&rsquo;s Workshop: Week 24 &middot; REVISE', 1),
 ('Today is the <strong>Apply</strong> stage. Read your source comparison draft. Edit for: (1) formal style (no contractions, no &ldquo;I think&rdquo;), (2) at least two source-based transitions, (3) claim + evidence + reasoning structure. Show your strongest sentence and one you rewrote.',
  'Today is the <strong>Revise</strong> stage. Read your draft from Day 2 and check it against this list: (1) formal style, with no contractions and no &ldquo;I think&rdquo;; (2) at least two source transitions; (3) a claim, evidence from the novel, evidence from a source, and reasoning; (4) every fact is tied to its source. Then show your strongest sentence and one you rewrote.', 1),
 ("data-label=\"Writer's Workshop: Source Comparison — Apply (Edit)\"", "data-label=\"Writer's Workshop: Source Comparison — Revise\"", 1),
]
P['writing'][4] += [
 ('Complete your source comparison paragraph (if not already done) and paste it here. Then write one sentence: what is your claim?',
  'Your final paragraph goes in the Writer&rsquo;s Workshop box. Here, write your claim in one sentence. Then name the one detail from the novel and the one line from a source that you will use as evidence.', 1),
]
which = sys.argv[1]
if which == 'poetry':
    for d, (t, au, tx, pr) in POEMS.items():
        f = F[d]; s = io.open(f, encoding='utf-8', newline='').read(); orig = s
        s = poem(s, t, au, tx, pr)
        if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('%s: div balance changed' % f)
        io.open(f, 'w', encoding='utf-8', newline='').write(s); print('poetry ok', f)
    sys.exit()
OUT = {}
for d, reps in P[which].items():
    f = F[d]
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    if which == 'rwm' and d == 4 and 'id="source-study"' not in s: sys.exit('run sources first')
    for old, new, n in reps:
        c = s.count(old)
        if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:80], c))
        s = s.replace(old, new, 1)
    if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('%s: div balance changed' % f)
    OUT[f] = s
if which == 'rwm':
    f = F[3]; s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    s, n = re.subn(r'  <!-- RWM -->\n  <div class="rwm-box">.*?\n  </div>\n(?=  <div class="tab-next-wrap">)', lambda m: R[3], s, count=1, flags=re.S)
    if n != 1: sys.exit('24.3 rwm box not found')
    if (s.count('<div') - s.count('</div')) != (orig.count('<div') - orig.count('</div')): sys.exit('24.3: div balance changed')
    OUT[f] = s
for f, s in OUT.items():
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print(which, 'ok', f)
