#!/usr/bin/env python3
"""Week 21 accuracy fixes (approved by Bethany Nov 21 2026; audit claude/g5-ela-wk21-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 16-19). Every replacement asserts its count;
div balance must not change. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-21-1-hbg-ch16.html', 2: 'lesson-21-2-hbg-ch17.html', 3: 'lesson-21-3-hbg-ch18.html', 4: 'lesson-21-4-hbg-ch19.html'}
WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>', '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.', 'I wrote my Read Like a Writer answers on the Reading tab.', 1)
HINT = 'Fix the unclear pronoun. Fix capitalization and punctuation.'
# DOL: model + fix-it from the day's chapter (two different sentences); the skill is pronoun reference
DOL = {
 1: dict(label='Clear pronoun reference', words=[('When ', 'Opens a dependent clause, so a comma comes after it.'), ('Nani ', None), ('Humma ', 'One person: he.'), ('caught ', None), ('the ', None), ('boys, ', 'The boys = them. The comma ends the opening clause.'), ('he ', 'He = Nani Humma, the only one person named.'), ('made ', None), ('them ', 'Them = the boys.'), ('tell ', None), ('the ', None), ('whole ', None), ('story. ', None)],
         fix='the women waved to the soldiers and they promised them a berry pudding',
         ans='The women waved to the soldiers and promised them a berry pudding.',
         why='&ldquo;They&rdquo; could mean the women or the soldiers. Drop it, so the women do both things; &ldquo;them&rdquo; = the soldiers. Capitalize the first word.'),
 2: dict(label='Clear pronoun reference', words=[('Luke ', 'One person, named first.'), ('gave ', None), ('his ', 'His = Luke&rsquo;s. Only Luke has been named yet.'), ('blowgun ', None), ('to ', None), ('Joseph, ', 'Comma before and: two complete sentences are joined.'), ('and ', None), ('Joseph ', 'The name again, so nobody wonders who &ldquo;he&rdquo; is.'), ('made ', None), ('darts. ', None)],
         fix='isaac hugged luke and he said he was glad isaac was safe',
         ans='Isaac hugged Luke, and Luke said he was glad Isaac was safe.',
         why='The first &ldquo;he&rdquo; could be Isaac or Luke, so name Luke. Put a comma before &ldquo;and.&rdquo; Capitalize the names.'),
 3: dict(label='Clear pronoun reference', words=[('Joseph ', 'One person, named first.'), ('told ', None), ('Isaac&rsquo;s ', None), ('parents ', 'Parents = they.'), ('what ', None), ('happened, ', 'Comma before and: two complete sentences are joined.'), ('and ', None), ('they ', 'They = Isaac&rsquo;s parents.'), ('cried ', None), ('together. ', None)],
         fix='joseph saw a deer across the river and he told isaac that he was going hunting',
         ans='Joseph saw a deer across the river and told Isaac, &ldquo;I&rsquo;m going hunting.&rdquo;',
         why='&ldquo;He was going hunting&rdquo; could mean Joseph or Isaac. Joseph&rsquo;s own words make it clear. Capitalize the names.'),
 4: dict(label='Clear pronoun reference', words=[('Naomi ', 'One person, named first.'), ('took ', None), ('the ', None), ('soldier&rsquo;s ', None), ('bowl ', 'Bowl = it.'), ('and ', None), ('filled ', None), ('it ', 'It = the bowl.'), ('again. ', None)],
         fix='joseph told nani humma that isaac was dead and that he would stay with them',
         ans='Joseph told Nani Humma, &ldquo;Isaac is dead, but he will stay with us.&rdquo;',
         why='&ldquo;He&rdquo; could be Joseph or Isaac, and &ldquo;them&rdquo; is unclear. Joseph&rsquo;s own words make both clear. Capitalize the names.'),
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
FIX = {
 1: [('Isaac could have stayed safe with his family. Instead he slips out at night',
      'Isaac could have stayed in his blanket by the council fire. Instead he slips out at night', 1), WW],
 2: [('The first clause gives you what you expected of a chief;', 'The first clause gives you what you expected of a leader;', 1), RWMCHK, WW],
 3: [  # nothing in the book has Isaac carrying his brother
  ('data-explain="Correct! The contrast between his age and what he did is the point &mdash; and <em>but</em> carries it.">Isaac was ten years old, but he carried his brother all day.</span>',
   'data-explain="Correct! The contrast between the fear and what he did is the point, and <em>but</em> carries it.">Isaac was afraid, but he stepped into the soldiers&rsquo; camp.</span>', 1),
  ('data-explain="<em>And</em> flattens it into a list. The contrast disappears.">Isaac was ten years old, and he carried his brother all day.</span>',
   'data-explain="<em>And</em> flattens it into a list. The contrast disappears.">Isaac was afraid, and he stepped into the soldiers&rsquo; camp.</span>', 1),
  ('(2) Isaac was ten. He carried his brother all day.</em>', '(2) Joseph saw a deer. He went hunting.</em>', 1),
  ('Isaac is watching his own father lift his body onto his shoulder. Back in Chapter 13',
   'Isaac is watching his family set out to carry his body. Back in Chapter 13', 1),
  ('<span class="q-num">3</span>&#127775; <strong>Week Closer.</strong> In Chapters 16, 17, and 18,', '<span class="q-num">3</span>In Chapters 16, 17, and 18,', 1),
  ('Tingle compares movement to fog, to smoke, to snow. Your comparison should fit the emotion of the moment.',
   'Tingle does this in Chapter 18: the panther&rsquo;s black coat goes away &ldquo;like dark grass fading into the ground.&rdquo; Your comparison should fit the feeling of the moment.', 1),
  intro('Chapter 18 is the hardest chapter in the book. Isaac says good-bye to his mother, and on the way back to the council wagon a wolf attacks him. <strong>As you read, watch: what does Isaac see once he becomes a ghost, and what does he decide when he wants to go back?</strong>'),
  RWMCHK, WW],
 4: [('<div class="textbox-prompt">Read the first page of Chapter 20 to check your idea.</div>',
      '<div class="textbox-prompt">Think about how long she has been alone, and what she hoped for.</div>', 1),
  intro('In Chapter 19, Isaac&rsquo;s family learns Joseph&rsquo;s secret, and Isaac and Joseph go to the soldiers&rsquo; camp to find Naomi. <strong>As you read, watch: what can Isaac do now that he is a ghost, and what can&rsquo;t he do? What does Naomi say when he whispers her name?</strong>'),
  WW],
}
# vocabulary: book order (terrified Ch. 16; stickball, mourning Ch. 18; suffering, courage Ch. 19)
ORDER = ["terrified", "stickball", "mourning", "suffering", "courage"]
CH = {"terrified": 16, "stickball": 18, "mourning": 18, "suffering": 19, "courage": 19}
SHORT = {"terrified": "Extremely frightened.", "stickball": "A traditional Choctaw game played with sticks and a ball.",
         "mourning": "Deep sadness after someone dies, and the quiet way people show it.",
         "suffering": "Pain or hardship a person is living through.", "courage": "Facing something frightening anyway."}
PERM = [2, 3, 4, 0, 1]
EVERY = [("Facing something frightening anyway. Isaac walks to the soldiers' campfire with newfound courage.", SHORT['courage']),
         ("A traditional Choctaw game played with sticks — one of the things carried from home.", SHORT['stickball']),
         ('young girl,” said another woman.&rdquo;', 'young girl,&rdquo; said another woman.'),
         ('<div class="fillin-item">A <input class="fillin-input" data-answer="terrified" maxlength="12" placeholder="______"> young girl,” said another woman.</div>',
          '<div class="fillin-item">&ldquo;A <input class="fillin-input" data-answer="terrified" maxlength="12" placeholder="______"> young girl,&rdquo; said another woman.</div>')]
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


for d, f in F.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in FIX[d]:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], s.count(old)))
        if n: s = s.replace(old, new)
    for old, new in EVERY: s = s.replace(old, new)
    s = dol(d, s)
    s = vocab(d, s)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)

f = 'lesson-21-fluency.html'   # one continuous Ch. 19 stretch, credited right (was invented lines + the Ch. 1 opening)
s = io.open(f, encoding='utf-8', newline='').read(); orig = s
a = s.index('<div class="fluency-passage"><p>I was a ghost')
end = 'Chapter 1</div>\n  </div>\n      </div>\n'; b = s.index(end, a) + len(end)
s = s[:a] + '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      He was right. What did I have to worry about? That&rsquo;s when I realized, for the first time, that the soldiers couldn&rsquo;t hurt me. I was already dead! Maybe being a ghost wasn&rsquo;t so bad after all.<br><br>
      With my newfound courage, I walked to the soldiers&rsquo; campfire. I sat down next to the man who had passed out the smallpox blankets. He could not see me, of course.<br><br>
      A young man was scooping beef stew from a large kettle and filling their bowls. He was Luke&rsquo;s age, more or less, but his arms were long and thin. His black hair was cut short, and I could see he was Choctaw. Where is Naomi? I asked myself. I thought she was their helper.<br><br>
      Dumb me! Of course, this was Naomi, dressed like a teenage boy, with short-cut hair. I have to be smarter than this, I told myself.
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 19</div>
  </div>
  </div>
      </div>
''' + s[b:]
for old, new in [
 ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
  'In Chapter 19, Isaac walks into the soldiers&rsquo; camp, and nobody can see him. Today you&rsquo;ll practice reading it with accuracy, smoothness, and the surprise of his discovery.'),
 ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
  'Read it once to yourself first. Then read it again and keep your voice flowing. Let the long sentences about the young man move smoothly.'),
 ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
  'Now bring Isaac to life. Let &ldquo;I was already dead!&rdquo; sound like a surprise, and &ldquo;Dumb me!&rdquo; sound like Isaac laughing at himself.'),
 ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;Choctaw&rdquo; and &ldquo;smallpox&rdquo;?'),
 ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
  'Did my voice change when Isaac figured out who the young man was?')]:
    if s.count(old) != 1: sys.exit('fluency %r x%d' % (old[:50], s.count(old)))
    s = s.replace(old, new)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('fluency: div balance')
io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
