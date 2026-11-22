#!/usr/bin/env python3
"""Week 23 accuracy fixes (approved by Bethany Nov 21 2026; audit claude/g5-ela-wk23-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 24-27). Every replacement asserts its count;
div balance must not change; nothing is written unless every file passes. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-23-1-hbg-ch24.html', 2: 'lesson-23-2-hbg-ch25.html', 3: 'lesson-23-3-hbg-ch26.html', 4: 'lesson-23-4-hbg-ch27.html'}
WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>', '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.', 'I wrote my Read Like a Writer answers on the Reading tab.', 1)
HINT = 'Combine into one clear sentence. Fix capitalization and punctuation.'
DOL = {
 1: dict(label='Sentence combining', words=[('Roundman ', 'One subject does both actions.'), ('leapt ', 'First action.'), ('to ', None), ('his ', None), ('friend ', None), ('and ', 'And joins two actions by the same person, so no comma.'), ('wrapped ', 'Second action, same subject.'), ('a ', None), ('cloth ', None), ('around ', None), ('his ', None), ('head. ', None)],
         fix='joseph fell asleep in minutes. his blanket was soon covered in snow',
         ans='Joseph fell asleep in minutes, and his blanket was soon covered in snow.',
         why='Two complete sentences, joined with a comma and <em>and</em>. Capitalize the first word and the name.'),
 2: dict(label='Combining with who', words=[('Mister ', None), ('Tibbi, ', 'Comma opens the who part.'), ('who ', 'Who tells more about Mister Tibbi.'), ('stood ', None), ('his ', None), ('ground, ', 'Comma closes the who part.'), ('spoke ', 'The main verb.'), ('in ', None), ('a ', None), ('quiet ', None), ('but ', None), ('strong ', None), ('voice. ', None)],
         fix='stella lay under the heavy branch. she was elderly',
         ans='Stella, who was elderly, lay under the heavy branch.',
         why='Turn the second sentence into a <em>who</em> part and set it off with commas. Capitalize the name.'),
 3: dict(label='Combining with an -ing opener', words=[('Thinking ', 'An -ing phrase holds the first idea.'), ('of ', None), ('their ', None), ('children, ', 'Comma after the opening phrase.'), ('the ', None), ('soldiers ', 'The phrase tells about the soldiers, so they come right after the comma.'), ('hung ', None), ('their ', None), ('heads. ', None)],
         fix='pointy nose reached for the blanket. he saw the snake. he stopped',
         ans='When Pointy Nose reached for the blanket, he saw the snake and stopped.',
         why='<em>When</em> joins the first idea to the rest, and <em>and</em> joins the last two actions. Put a comma after the opening part. Capitalize the name.'),
 4: dict(label='Combining with but', words=[('The ', None), ('bonepickers ', None), ('were ', None), ('frail, ', 'Comma before but: two complete sentences are joined.'), ('but ', 'But shows a contrast.'), ('they ', 'They = the bonepickers.'), ('were ', None), ('brave. ', None)],
         fix='the soldier lifted the lid. he stepped back in horror',
         ans='The soldier lifted the lid and stepped back in horror.',
         why='One person does both actions, so join them with <em>and</em> and drop <em>he</em>. Capitalize the first word.'),
}

def dol_block(d):
    D = DOL[d]
    spans = ''.join(('          <span class="dol-highlight-word" onclick="dolHighlight(this,&quot;%s&quot;)">%s</span>\n' % (n, w)) if n else ('          <span>%s</span>\n' % w) for w, n in D['words'])
    return ('<div class="dol-model-label">&#9989; Correct &mdash; %s</div>\n        <div class="dol-sentence-wrap" id="dolModel">\n%s        </div>' % (D['label'], spans),
            '<div class="dol-sentence-wrap" style="border-left:4px solid #8B3A20;">%s</div>\n        <div class="dol-hint">%s</div>' % (D['fix'], HINT),
            '<p style="margin-bottom:6px;"><strong>Corrected:</strong> %s</p>\n          <p style="font-size:13px;color:#7A88A8;font-style:italic;">%s</p>' % (D['ans'], D['why']))
def dol(d, s):
    m1, m2, m3 = dol_block(d)
    for pat, new in [(r'<div class="dol-model-label">.*?\n        </div>(?=\n        <div id="dolExplain")', m1),
                     (r'<div class="dol-sentence-wrap" style="border-left:4px solid #8B3A20;">[^<]*</div>\n        <div class="dol-hint">[^<]*</div>', m2),
                     (r'<p style="margin-bottom:6px;"><strong>Corrected:</strong>.*?</p>\n          <p style="font-size:13px;color:#7A88A8;font-style:italic;">.*?</p>', m3)]:
        s, n = re.subn(pat, lambda _m: new, s, count=1, flags=re.S)
        if n != 1: sys.exit('DOL %d: %s' % (d, pat[:40]))
    return s
INTRO = ('<div class="activity-title">&#128212; Reading &middot; Chapter Introduction</div><div class="activity-sub">Watch, then read.</div></div></div>\n    <div class="activity-body">\n        <div class="activity bl-purple" style="margin-bottom:18px;">')
def intro(text):
    return (INTRO, INTRO.replace('<div class="activity-body">\n', '<div class="activity-body">\n        <p>%s</p>\n' % text), 1)

MEAN = '<strong>Match each word to its meaning.</strong> Tap a word, then tap its meaning.'
ROOTDIR = '<strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.'
FIX = {
 1: [('Isaac was cold. Isaac was tired. Isaac kept walking.', 'It was freezing. Joseph was worn out. He fell asleep in minutes.', 3),
     ('Isaac was cold and tired, but he kept walking.', 'It was freezing, but Joseph was so worn out that he fell asleep in minutes.', 3),
     ('Two women, one &lsquo;she.&rsquo; The reader cannot tell who stopped.', 'Two men, one &lsquo;he.&rsquo; The reader cannot tell who fell.', 1),
     ('>Naomi walked with Nita until she stopped.<', '>Roundman helped Pointy Nose after he fell.<', 1),
     ('>Naomi walked with Nita until Nita stopped.<', '>Roundman helped Pointy Nose after Pointy Nose fell.<', 1),
     (ROOTDIR, MEAN, 1),
     ('Isaac is now summarizing his journey from life to death to purpose. <strong>What has he learned about himself? And what has he understood about what it means to live &mdash; in any form?</strong>',
      'Isaac has been a ghost for several chapters now. <strong>What has he learned about himself so far? What has he come to understand about what it means to live, in any form?</strong>', 1),
     WW],
 2: [('>The treaty was broken and it was signed only years before and nobody was held responsible.<', '>The soldiers rode into camp and they tore the blankets away and they threw them into the fire.<', 1),
     ('>The treaty had been signed only years before. It was broken, and nobody was held responsible.<', '>The soldiers rode into camp. They tore the blankets away and threw them into the fire.<', 1),
     ('Correct! Both pronouns have no antecedent. The reader has to guess at everything.">It never protected them.<', 'Correct! No pronoun points at anything. The reader has to guess who did what.">He told them to burn them.<', 1),
     ('Both nouns are named, so nothing has to be inferred.">The treaty never protected the Choctaw people.<', 'Every noun is named, so nothing has to be guessed.">Leader told the soldiers to burn the blankets.<', 1),
     ('the treaty was broken and it was signed only years before and nobody was held responsible.</em>', 'the soldiers rode into camp and they tore the blankets away and they threw them into the fire.</em>', 1),
     (ROOTDIR, MEAN, 1),
     ('The ghost walkers grow in number. <strong>What does this growing number mean for the story&rsquo;s argument about history?',
      'At the end of Chapter 25, Old Man appears in a cloud with every Choctaw from Isaac&rsquo;s town, the living and the dead. <strong>What does it mean that the dead stand with the living?', 1),
     ('Q2: Ch. 25 — the ghost walkers grow', 'Q2: Ch. 25 — the living and the dead', 1),
     ('The growing number of ghost walkers means...', 'The dead standing with the living means...', 1),
     RWMCHK, WW],
 3: [('The ghosts appeared. Only Isaac could see them. He said nothing.', 'The snake rose over Nita. Pointy Nose stopped. He begged Leader.', 1),
     ('The ghosts appeared, and only Isaac could see them. He said nothing.', 'The snake rose over Nita, and Pointy Nose stopped. He begged Leader.', 2),
     ('>The ghosts appeared and only Isaac could see them and he said nothing.<', '>The snake rose over Nita and Pointy Nose stopped and he begged Leader.<', 1),
     ('The contrast between his age and what he did disappears.">Isaac was ten years old, and he carried his brother all day.<', 'The contrast between her tiny voice and her strong words disappears.">Nita&rsquo;s voice was tiny, and her words were strong.<', 1),
     ('>Isaac was only ten, but he carried his brother all day.<', '>Nita&rsquo;s voice was tiny, but her words were strong.<', 1),
     ('Now <strong>use</strong> them. Chapters 24 to 27 are full of people finding a voice, and of orders being declared from far away. Choose the word that fits.',
      'Now <strong>use</strong> them. These chapters are full of voices: orders shouted, promises made, and people who will not stay silent. Match each word to its meaning.', 1),
     (ROOTDIR, MEAN, 1),
     ('<span class="q-num">3</span>&#127775; <strong>Week Closer.</strong> In Chapters 24, 25, and 26: Leader vows that someone will die, Isaac witnesses mass death, and the rattlesnake turns fear back on the soldiers. <strong>What argument does Tingle make across these three chapters about how justice works?',
      '<span class="q-num">3</span>In Chapters 24, 25, and 26, Leader vows that someone will die, his soldiers shoot into the Choctaw Council&rsquo;s camp and burn blankets, and a rattlesnake stops Pointy Nose from taking Nita&rsquo;s body. <strong>What do these three chapters show about how justice works?', 1),
     ('data-label="Q3 (week closer): three chapters, one argument about justice"', 'data-label="Q3: three chapters, one idea about justice"', 1),
     intro('In Chapter 26, Leader and his soldiers reach Isaac&rsquo;s family, still hunting for Naomi. <strong>As you read, watch: what does Ruth do when Leader demands her little girl, and what stops Pointy Nose?</strong>'),
     RWMCHK, WW],
 4: [('character, conflict, perspective and theme across the whole novel.', 'character, conflict, perspective and theme across the novel so far.', 1),
     ('Across the whole book, say who Isaac has become', 'Across the book so far, say who Isaac has become', 1),
     ('Across the whole novel, Tingle has honored the dead:', 'Across the novel so far, Tingle has honored the dead:', 1),
     ('This is your big synthesis question for the unit. Use the whole novel.', 'This is your big thinking question for the week. Use the chapters you have read so far.', 1),
     intro('In Chapter 27, the soldiers reach the bonepickers&rsquo; wagon, where Naomi is still hiding in the trunk. <strong>As you read, watch: what does Leader do to the old women, how do his own soldiers react, and how does Joseph help Naomi?</strong>'),
     WW],
}
# D2 morphology tiles: four distinct meanings (was two "Root: dict (say)" tiles, and voc / voke split)
TILES2 = {'A': ('Root: <em>voc</em> (voice)', 'using the voice'), 'B': ('Root: <em>voke</em> (call)', 'to call up anger in someone'),
          'C': ('Root: <em>dict</em> (say)', 'to say the opposite'), 'D': ('Root: <em>dict</em> (say)', 'an order a ruler declares')}
def tiles2(s):
    for k, (old, new) in TILES2.items():
        s, n = re.subn(r'(<div class="root-match-item" data-match="%s" onclick="rootMatchClick\(this\)">)%s(</div>)' % (k, re.escape(old)), lambda m: m.group(1) + new + m.group(2), s)
        if n != 1: sys.exit('tile %s x%d' % (k, n))
    return s
ORDER = ["exhausted", "revenge", "unconscious", "gratitude", "prophecy"]
CH = {"exhausted": 24, "revenge": 24, "unconscious": 25, "gratitude": 26, "prophecy": 27}
SHORT = {"exhausted": "Completely worn out.", "revenge": "Hurting someone back for something they did to you.",
         "unconscious": "Not awake and not able to feel anything, usually after being hurt.",
         "gratitude": "Thankfulness, and the showing of it.", "prophecy": "A prediction of what will happen in the future."}
PERM = [2, 3, 4, 0, 1]
EVERY = [(' &mdash; which is what happened to the treaty</p>', ', like taking back a promise</p>'),
         ('from Chapters 24–27', 'from this week&rsquo;s chapters'), ('Five words from Chapters 24–27.', 'Five words from this week&rsquo;s chapters.')]

def word_of(b):
    c = {w: len(re.findall(r'\b%s\b' % w, b, re.I)) for w in ORDER}
    return max(c, key=c.get)
def reorder(s, pat, name):
    ms = list(re.finditer(pat, s, re.S))
    if len(ms) != 5: sys.exit("%s: expected 5 blocks, found %d" % (name, len(ms)))
    blocks = {word_of(m.group(0)): m.group(0) for m in ms}
    if set(blocks) != set(ORDER): sys.exit("%s: words %s" % (name, list(blocks)))
    out, last = [], 0
    for i, m in enumerate(ms):
        out.append(s[last:m.start()]); out.append(blocks[ORDER[i]]); last = m.end()
    return ''.join(out) + s[last:]
def match_grid(s):
    m = re.search(r'(<div class="match-grid" id="matchGrid">)(.*?)(\n\s*</div>\s*<div class="match-feedback")', s, re.S)
    if not m: return s
    ind = "\n          "; rows = []
    for i, w in enumerate(ORDER):
        rows.append('<div class="match-item is-word" data-match="%s" onclick="matchClick(this)">%s</div>' % ("ABCDE"[i], w))
        rows.append('<div class="match-item" data-match="%s" onclick="matchClick(this)">%s</div>' % ("ABCDE"[PERM[i]], SHORT[ORDER[PERM[i]]]))
    return s[:m.start()] + m.group(1) + ind + ind.join(rows) + m.group(3) + s[m.end():]
def vocab(d, s):
    if 'class="vocab-bank"' in s:
        s = reorder(s, r'<p style="margin:4px 0;"><strong>(?:%s)</strong> &mdash; [^\n]*</p>' % "|".join(ORDER), "word bank")
    if d == 1:
        s = reorder(s, r'<div class="vocab-decode-item">\s*<div class="decode-sentence">.*?</div>\s*<div class="flip-card.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', "day1 cards")
        for w in ORDER:
            s, n = re.subn(r'(<div class="decode-sentence">(?:(?!</div>).)*<strong style="color:#8B3A20;">%s</strong>(?:(?!</div>).)*?)(</div>)' % w,
                           r'\1 <span class="vocab-ch" style="font-style:normal;font-size:12px;font-weight:700;color:#7A88A8;white-space:nowrap;">Ch. %d</span>\2' % CH[w], s, count=1, flags=re.S | re.I)
            if n != 1: sys.exit('no chapter tag for ' + w)
        s = match_grid(s)
    if d == 2:
        s = reorder(s, r'<p style="font-size:15px;color:#3A4A6B;line-height:1\.8;margin-bottom:\d+(?:px)?;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">(?:%s)</strong>[^\n]*?</p>' % "|".join(w.capitalize() + '|' + w for w in ORDER), "day2 sentences")
        s = re.sub(r'margin-bottom:0;">&ldquo;', 'margin-bottom:10px;">&ldquo;', s)
        ms = list(re.finditer(r'margin-bottom:10px;">&ldquo;', s))
        # the last of the five context sentences keeps margin 0
        five = [m for m in ms if re.match(r'margin-bottom:10px;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">', s[m.start():m.start() + 400])]
        last = five[-1]; s = s[:last.start()] + 'margin-bottom:0;">&ldquo;' + s[last.end():]
        s = match_grid(s)
    if d == 3:
        s = reorder(s, r'<div class="fillin-item">[^\n]*?</div>', "day3 fill-in")
    if d == 4:
        s = reorder(s, r'<div class="vocab-use-item".*?</textarea>\s*</div>', "day4 use-it")
    return s


OUT = {}
for d, f in F.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in FIX[d]:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], s.count(old)))
        s = s.replace(old, new)
    for old, new in EVERY: s = s.replace(old, new)
    if 'Chapters 24–27' in s or 'treaty' in s: sys.exit(f + ': leftover Chapters 24–27 / treaty')
    if d == 2: s = tiles2(s)
    s = dol(d, s)
    s = vocab(d, s)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    OUT[f] = s

f = 'lesson-23-fluency.html'
s = io.open(f, encoding='utf-8', newline='').read(); orig = s
a = s.index('<div class="fluency-passage"><p>Life is very different as a ghost')
end = 'Chapter 1</div>\n  </div>\n      </div>\n'; b = s.index(end, a) + len(end)
s = s[:a] + '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      In spite of the freezing cold, Joseph fell asleep in minutes. His blanket was soon covered in snow. I knew he was exhausted from the long day of rescuing Naomi, setting fire to the soldiers&rsquo; camp, rushing Naomi to the bonepickers&rsquo; wagon, and catching a raccoon with his bare teeth!<br><br>
      I sat watching him sleep. I was neither tired nor cold. Life is very different as a ghost, I told myself. I learned something else that night: Without sleep, life as a ghost can be boring! That must be why ghosts know everything, I thought. While everybody else is sleeping, they float around and see what&rsquo;s happening.
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 24</div>
  </div>
  </div>
      </div>
''' + s[b:]
FL = [
 ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
  'Chapter 24 opens on a snowy night after a very long day. Joseph sleeps, and Isaac, who no longer gets tired or cold, has the whole night to think. Today you&rsquo;ll practice reading it with accuracy, smoothness, and expression.'),
 ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
  'Read it once to yourself first. Then read it again and keep your voice flowing. The long list in the third sentence should roll along without stopping, like the long day it describes.'),
 ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
  'Now bring Isaac to life. Let your voice sound surprised at the raccoon, quiet as he watches Joseph sleep, and a little amused when he says that being a ghost can be boring.'),
 ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;exhausted&rdquo; and &ldquo;bonepickers&rsquo;&rdquo;?'),
 ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
  'Did I read the long list smoothly, and pause at the exclamation points so they could land?')]
for old, new in FL:
    if s.count(old) != 1: sys.exit('fluency %r x%d' % (old[:50], s.count(old)))
    s = s.replace(old, new)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('fluency: div balance')
OUT[f] = s
for f, s in OUT.items():
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
