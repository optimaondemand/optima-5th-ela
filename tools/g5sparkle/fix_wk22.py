#!/usr/bin/env python3
"""Week 22 accuracy fixes (approved by Bethany Nov 21 2026; audit claude/g5-ela-wk22-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 20-23). Every replacement asserts its count;
div balance must not change. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-22-1-hbg-ch20.html', 2: 'lesson-22-2-hbg-ch21.html', 3: 'lesson-22-3-hbg-ch22.html', 4: 'lesson-22-4-hbg-ch23.html'}
WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>', '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.', 'I wrote my Read Like a Writer answers on the Reading tab.', 1)
HINT = 'Fix the unclear pronoun. Fix capitalization and punctuation.'
DOL = {
 1: dict(label='Clear pronoun reference', words=[('Naomi ', 'One person, named first.'), ('told ', None), ('Isaac ', None), ('that ', None), ('she ', 'She = Naomi, the only girl named.'), ('had ', None), ('dreamed ', None), ('about ', None), ('him ', 'Him = Isaac.'), ('for ', None), ('a ', None), ('week. ', None)],
         fix='isaac told joseph about naomi and he said that she comes with us tonight',
         ans='Isaac told Joseph about Naomi, and Joseph said, &ldquo;Naomi comes with us tonight.&rdquo;',
         why='&ldquo;He&rdquo; could be Isaac or Joseph, so name Joseph and use his own words. Put a comma before &ldquo;and.&rdquo; Capitalize the names.'),
 2: dict(label='Clear pronoun reference', words=[('Roundman ', 'One person, named first.'), ('leaned ', None), ('against ', None), ('the ', None), ('tree ', None), ('and ', None), ('held ', None), ('his ', 'His = Roundman&rsquo;s. Only one person is named.'), ('shotgun ', None), ('ready. ', None)],
         fix='the councilwoman helped naomi and she cut the rope with a sharp knife',
         ans='The councilwoman helped Naomi and cut the rope with a sharp knife.',
         why='&ldquo;She&rdquo; could be the councilwoman or Naomi. Drop it, so the councilwoman does both things. Capitalize the first word and the name.'),
 3: dict(label='Clear pronoun reference', words=[('Naomi ', 'One person, named first.'), ('slipped ', None), ('off ', None), ('her ', 'Her = Naomi&rsquo;s.'), ('boots, ', 'Boots = them. Comma before and: two complete sentences are joined.'), ('and ', None), ('the ', None), ('woman ', None), ('hid ', None), ('them. ', 'Them = the boots.')],
         fix='the woman handed naomi a blanket and she said it will keep you warm',
         ans='The woman handed Naomi a blanket and said, &ldquo;This will keep you warm.&rdquo;',
         why='&ldquo;She&rdquo; could be the woman or Naomi, and &ldquo;it&rdquo; is far from the blanket. The woman&rsquo;s own words make both clear. Capitalize the first word and the name.'),
 4: dict(label='Clear pronoun reference', words=[('Joseph ', 'One person, named first.'), ('caught ', None), ('a ', None), ('raccoon ', 'Raccoon = it.'), ('and ', None), ('dropped ', None), ('it ', 'It = the raccoon.'), ('in ', None), ('the ', None), ('wagon. ', None)],
         fix='luke told joseph and isaac that he needed to get back to the family',
         ans='Luke told Joseph and Isaac, &ldquo;I need to get back to the family.&rdquo;',
         why='&ldquo;He&rdquo; could be Luke, Joseph or Isaac. Luke&rsquo;s own words make it clear. Capitalize the names.'),
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
 1: [('a new word to memorise.', 'a new word to memorize.', 1), ('Find the part at the centre of each word', 'Find the part at the center of each word', 1),
     ('data-group="c" onclick="pickSortChip(this)">chronology<', 'data-group="c" onclick="pickSortChip(this)">anachronism<', 1),
     WW],
 2: [('literary words by the root at their centre.', 'literary words by the root at their center.', 1), ('by the root at its centre.', 'by the root at its center.', 1),
     ('Joseph has become the panther, and this is the distraction that lets Naomi escape.',
      'Joseph has become the panther. After Jumper&rsquo;s splash, this is the second distraction, the one that lets Naomi get away.', 1),
     RWMCHK, WW],
 3: [('Chapter 21 is full of light doing symbolic work &mdash; illuminating, revealing, and refusing to go out. Choose the word that fits.',
      'These chapters are full of light: moonlight, firelight, and a ghost who glows. Choose the meaning that fits.', 1),
     ('<span class="q-num">3</span>&#127775; <strong>Week Closer.</strong> In Chapters 20, 21, and 22,', '<span class="q-num">3</span>In Chapters 20, 21, and 22,', 1),
     intro('In Chapter 22, Luke leads Naomi to a wagon where four old women welcome her in. Part of the chapter explains, calmly, how they cared for the dead in the old Choctaw way. <strong>As you read, watch: who are these women, and why is their wagon the safest place for Naomi?</strong>'),
     RWMCHK, WW],
 4: [('Choose the figurative image that has done the most work across the whole novel.', 'Choose the figurative image that has done the most work in the novel so far.', 1),
     intro('In Chapter 23, the women carry out their plan to keep the soldiers away from the trunk, and Isaac, Joseph and Luke get a visit they will never forget. <strong>As you read, watch: how does the plan work, and how do the ghosts honor the three boys?</strong>'),
     WW],
}
ORDER = ["distraction", "bonepickers", "speechless", "ancestors", "honored"]
CH = {"distraction": 21, "bonepickers": 22, "speechless": 23, "ancestors": 23, "honored": 23}
SHORT = {"distraction": "Something that pulls attention away, so that something else can happen unnoticed.",
         "bonepickers": "Choctaws whose sacred job was to prepare the dead for burial.",
         "speechless": "So surprised or moved that you cannot say a word.",
         "ancestors": "The family members who lived long before you.", "honored": "Treated with great respect."}
PERM = [2, 3, 4, 0, 1]
EVERY = [("The family members who lived long before you. The highest honor is to make the ancestors proud.", SHORT['ancestors']),
         ("Choctaws with the honored duty of preparing the dead for burial.", SHORT['bonepickers']),
         ("rumour", "rumor")]
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


f = 'lesson-22-fluency.html'
s = io.open(f, encoding='utf-8', newline='').read(); orig = s
a = s.index('<div class="fluency-passage"><p>Naomi was not a victim')
end = 'Chapter 1</div>\n  </div>\n      </div>\n'; b = s.index(end, a) + len(end)
s = s[:a] + '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      Sometime after midnight the wind grew angry and sleet replaced the friendly snow. Watching the ice fall, I was glad to be a ghost. I couldn&rsquo;t feel a thing. Joseph wrapped himself tight in my blanket, but I knew he was freezing. We couldn&rsquo;t risk a fire.<br><br>
      &ldquo;The snow has covered our footprints,&rdquo; I said, &ldquo;and the ice will slow them down in the morning.&rdquo;<br><br>
      &ldquo;Yes, I&rsquo;m glad for that,&rdquo; Joseph said, through chattering teeth. &ldquo;Let&rsquo;s hope for more ice!&rdquo;<br><br>
      As if in reply, a branch heavy with ice cracked and landed at our feet.<br><br>
      &ldquo;Careful what you wish for,&rdquo; I reminded him.
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 23</div>
  </div>
  </div>
      </div>
''' + s[b:]
FL = [
 ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
  'Chapter 23 ends on a cold, quiet night. Isaac and Joseph wait in the woods while the sleet falls, and Isaac says something you heard on the very first page of the book. Today you&rsquo;ll practice reading it with accuracy, smoothness, and expression.'),
 ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
  'Read it once to yourself first. Then read it again and keep your voice flowing. Let the first long sentence move smoothly, like the wind.'),
 ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
  'Now bring both boys to life. Let Joseph&rsquo;s words shiver through his teeth. Pause after the branch cracks, then let &ldquo;Careful what you wish for&rdquo; sound like a friend teasing a friend.'),
 ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;sleet&rdquo; and &ldquo;chattering&rdquo;?'),
 ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
  'Did I pause before the last line, so &ldquo;Careful what you wish for&rdquo; could land?')]
for old, new in FL:
    if s.count(old) != 1: sys.exit('fluency %r x%d' % (old[:50], s.count(old)))
    s = s.replace(old, new)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('fluency: div balance')
io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
