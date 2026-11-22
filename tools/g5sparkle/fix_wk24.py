#!/usr/bin/env python3
"""Week 24 accuracy fixes (approved by Bethany Nov 22 2026; audit claude/g5-ela-wk24-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 28-29). History checked against the Treaty of
Dancing Rabbit Creek (7 Stat. 333, Kappler II:310; signed Sept 27 1830, Article 3: falls of 1831, 1832, 1833)
and George W. Harkins, "To the American People" (Natchez Weekly Courier, Dec 2 1831, as shared by the
Choctaw Nation of Oklahoma). Every replacement asserts its count; div balance must not change; nothing is
written unless every file passes. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-24-1-hbg-ch28.html', 2: 'lesson-24-2-hbg-ch29.html', 3: 'lesson-24-3-hbg-ch28-29.html', 4: 'lesson-24-4-hbg-ch28-29.html'}
WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>', '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.', 'I wrote my Read Like a Writer answers on the Reading tab.', 1)
OLDHINT = 'Rewrite in active voice with strong verbs. Fix capitalization and punctuation.'
HINT = 'Rewrite it in formal style. Fix capitalization and punctuation.'
DOL = {
 1: dict(label='Formal style + source transition', words=[('According ', 'A source transition: it tells where the idea comes from.'), ('to ', None), ('Tingle, ', 'Comma after the source.'), ('Isaac&rsquo;s ', None), ('family ', None), ('was ', None), ('displaced ', 'A precise word: forced out of their home.'), ('during ', None), ('the ', None), ('forced ', 'Precise: the families did not choose to go.'), ('removal ', None), ('of ', None), ('the ', None), ('Choctaw ', 'Always capitalized.'), ('people. ', None)],
         fix='tingle&rsquo;s story shows that the choctaw people were treated really bad and the removal wasn&rsquo;t fair to them',
         ans='According to Tingle&rsquo;s novel, the Choctaw people were treated unjustly during the forced removal.',
         why='Formal style: a source transition (&ldquo;According to&rdquo;), one exact word (&ldquo;unjustly&rdquo;) in place of &ldquo;really bad&rdquo; and &ldquo;wasn&rsquo;t fair,&rdquo; and no contraction. Capitalize <em>Tingle</em> and <em>Choctaw</em>.'),
 2: dict(label='Comparison transition', words=[('Similarly, ', 'A comparison transition, followed by a comma.'), ('both ', None), ('the ', None), ('novel ', 'One source.'), ('and ', None), ('the ', None), ('historical ', None), ('record ', 'The other source.'), ('describe ', 'A formal verb for what a source does.'), ('a ', None), ('hard ', None), ('winter ', None), ('journey. ', None)],
         fix='the novel and the history both talk about how lots of people died during the trail of tears',
         ans='Both the novel and the historical record show that many Choctaw people died on the Trail of Tears.',
         why='Formal style: &ldquo;the historical record&rdquo; not &ldquo;the history,&rdquo; &ldquo;show&rdquo; not &ldquo;talk about,&rdquo; &ldquo;many&rdquo; not &ldquo;lots of.&rdquo; Capitalize <em>Choctaw</em> and <em>Trail of Tears</em>.'),
}
def dol_block(d):
    D = DOL[d]
    spans = ''.join(('          <span class="dol-highlight-word" onclick="dolHighlight(this,&quot;%s&quot;)">%s</span>\n' % (n, w)) if n else ('          <span>%s</span>\n' % w) for w, n in D['words'])
    return ('<div class="dol-model-label">&#9989; Correct &mdash; %s</div>\n        <div class="dol-sentence-wrap" id="dolModel">\n%s        </div>' % (D['label'], spans),
            '<div class="dol-sentence-wrap" style="border-left:4px solid #8B3A20;">%s</div>\n        <div class="dol-hint">%s</div>' % (D['fix'], HINT),
            '<p style="margin-bottom:6px;"><strong>Corrected:</strong> %s</p>\n          <p style="font-size:13px;color:#7A88A8;font-style:italic;">%s</p>' % (D['ans'], D['why']))
def dol(d, s):
    if d not in DOL:
        if s.count(OLDHINT) != 1: sys.exit('DOL hint %d' % d)
        return s.replace(OLDHINT, HINT)
    m1, m2, m3 = dol_block(d)
    for pat, new in [(r'<div class="dol-model-label">.*?\n        </div>(?=\n        <div id="dolExplain")', m1),
                     (r'<div class="dol-sentence-wrap" style="border-left:4px solid #8B3A20;">[^<]*</div>\n        <div class="dol-hint">[^<]*</div>', m2),
                     (r'<p style="margin-bottom:6px;"><strong>Corrected:</strong>.*?</p>\n          <p style="font-size:13px;color:#7A88A8;font-style:italic;">.*?</p>', m3)]:
        s, n = re.subn(pat, lambda _m: new, s, count=1, flags=re.S)
        if n != 1: sys.exit('DOL %d: %s' % (d, pat[:40]))
    return s

MEAN = '<strong>Match each word to its meaning.</strong> Tap a word, then tap its meaning.'
ROOTDIR = '<strong>Match each word to its root family.</strong> Tap a word, then tap the root it belongs to.'
SHARED = ('<p>Before you start: find the shared part and what it does.</p>', '<p>Before you start: read the six words in the box.</p>', 1)
SEP = 'amilies were separated at the river'
FIX = {
 1: [('The panther has appeared before. Now the wolf appears.', 'The panther has appeared before, and so has the wolf. Now they meet.', 1),
     # grammar notice: the promised second version
     ('<div class="task-sentence" style="border-left-color:#8B3A20;"><strong>According to</strong> the Treaty of Dancing Rabbit Creek, the Choctaw agreed to leave their homeland.</div>',
      '<div class="task-sentence" style="border-left-color:#8B3A20;">So basically the Choctaw had to leave.</div>\n        <div class="task-sentence" style="border-left-color:#8B3A20;margin-top:8px;"><strong>According to</strong> the Treaty of Dancing Rabbit Creek, the Choctaw agreed to leave their homeland.</div>', 1),
     ('Contemporary accounts describe severe shortages of food and shelter.', 'Harkins&rsquo;s letter of 1831 describes the removal as a wrong done to his people.', 1),
     ('>treaty</span>', '>liberty</span>', 1),
     ('In your reading journal: write your claim', 'In the box below, write your claim', 1),
     WW],
 2: [('The Choctaw Four carry the memory of their people into the future. They are young. They have survived. And they choose to carry the weight of witness. To remember what happened is a form of courage.',
      'At the end of Chapter 28, Pushmataha tells the four young Choctaws, &ldquo;You are brave and you are honest.&rdquo; He praises Isaac and Joseph for rescuing Naomi, and Naomi for saving a man&rsquo;s life. Doing the right thing when it is hard is courage.', 1),
     ('(1) Families were separated at the river.', '(1) The Choctaw were to leave in the falls of 1831, 1832 and 1833.', 1),
     ('Contemporary accounts record that families were separated at the river. This source is...', 'According to the treaty of 1830, the Choctaw were to leave in the falls of 1831, 1832 and 1833. This source is...', 1),
     (ROOTDIR, MEAN, 1), SHARED, RWMCHK, WW],
 3: [('<strong>The historical record indicates</strong> that families were separated at the river.', '<strong>The treaty of 1830 states</strong> that the Choctaw were to leave in the falls of 1831, 1832 and 1833.', 1),
     ('>Families were separated at the river.<', '>The Choctaw did not leave by choice.<', 1),
     ('>Contemporary accounts record that families were separated at the river.<', '>In his letter of 1831, George W. Harkins writes that the Choctaw did not leave by choice.<', 1),
     ('What do the informational or primary sources tell you about the Trail of Tears that the novel cannot?', 'What do the two primary sources (the treaty and Harkins&rsquo;s letter) tell you about the Trail of Tears that the novel cannot?', 1),
     ('<p>Today you read a source next to the novel. Work with both in front of you and ask what each one is for. A primary source records what somebody wrote down at the time; a novel gives you a ten-year-old boy&rsquo;s voice, which no document preserved. Ask what each makes possible, and what each leaves out.</p>',
      '<p>Today you read two real sources next to the novel. A primary source is something written at the time; a novel can give you a ten-year-old boy&rsquo;s voice, which no document kept. Ask what each one can tell you, and what each one leaves out.</p>', 1),
     ('>sovereign</span>', '>national</span>', 1),
     ('<strong>Sort by ending.</strong> These are the words you will need in your own essay.', '<strong>Sort by ending.</strong> Two bins hold nouns. The third holds describing words that end in <em>-al</em>.', 1),
     (ROOTDIR, MEAN, 1), SHARED, RWMCHK, WW],
 4: [('Historical fiction and a primary source disagree about nothing factual here, and still tell you different things. Say what each one is for, and what a reader would miss having only one of them.',
      'The novel and the sources do not match on every detail. The novel&rsquo;s first page says 1830; the treaty sets the removal for 1831 to 1833. They also tell you different things. Say what each one is for, and what a reader would miss with only one of them.', 1),
     ('Isaac saw the ghosts and families were separated at the river.', 'Isaac saw the ghosts and the Choctaw left in 1831.', None),
     ('In Tingle&rsquo;s novel, Isaac sees ghosts; contemporary accounts record that families were separated at the river.', 'In Tingle&rsquo;s novel, Isaac sees ghosts; the treaty of 1830 sets the removal for the falls of 1831, 1832 and 1833.', None),
     ('The first sentence puts a novelist&rsquo;s invention and a documented fact on the same footing.', 'The first sentence mixes something a novelist made up with a fact from the record, as if they were the same kind of thing.', 1),
     ('The novel and the historical accounts both describe the winter as unusually severe.', 'The novel and Harkins&rsquo;s letter both describe a painful parting from home.', 1),
     ('Everyone agrees the winter was unusually severe.', 'Everyone agrees that leaving home was painful.', 1),
     ('the historical record documents the deaths of thousands.', 'the historical record shows that many Choctaw people died on the journey.', 1),
     ('A boy became a ghost and thousands of people died.', 'A boy became a ghost and many people died.', 1),
     ('<strong>Sort by ending.</strong> Last one of the unit &mdash; name the rule before you place the word.', '<strong>Sort by the job each word does:</strong> noun, verb or adjective. The ending is your clue.', 1),
     (ROOTDIR, MEAN, 1), SHARED, WW],
}
# vocabulary: "Pushmataha" (a name) -> "honor" (Ch. 28), then book order
OLDDEF = 'A famous Choctaw chief and general, honored for leading and protecting his people.'
NEWDEF = 'To show great respect for someone.'
OLDSENT = 'We knew we would see General <strong style="color:#8B3A20;">Pushmataha</strong> for many days and years to come.'
NEWSENT = 'I come today to <strong style="color:#8B3A20;">honor</strong> four young Choctaw heroes.'
SWAP = {
 1: [(OLDSENT, NEWSENT, 1), ('<div class="fc-emoji">\U0001F54A️</div>', '<div class="fc-emoji">\U0001F396️</div>', 1),
     ('<div class="fc-word">Pushmataha</div>', '<div class="fc-word">honor</div>', 1), ('<div class="fc-word-back">Pushmataha</div>', '<div class="fc-word-back">honor</div>', 1),
     ('onclick="matchClick(this)">Pushmataha</div>', 'onclick="matchClick(this)">honor</div>', 1)],
 2: [(OLDSENT, NEWSENT, 1), ('<strong>Pushmataha</strong> &mdash;', '<strong>honor</strong> &mdash;', 1), ('onclick="matchClick(this)">Pushmataha</div>', 'onclick="matchClick(this)">honor</div>', 1)],
 3: [('<strong>Pushmataha</strong> &mdash;', '<strong>honor</strong> &mdash;', 1),
     ('We knew we would see General <input class="fillin-input" data-answer="pushmataha" maxlength="12" placeholder="______"> for many days and years to come.',
      'I come today to <input class="fillin-input" data-answer="honor" maxlength="12" placeholder="______"> four young Choctaw heroes.', 1)],
 4: [('<strong>Pushmataha</strong> &mdash;', '<strong>honor</strong> &mdash;', 1),
     ('margin-bottom:4px;">Pushmataha <span', 'margin-bottom:4px;">honor <span', 1),
     ('vocab-pushmataha', 'vocab-honor', None), ('data-label="Vocabulary: Pushmataha" placeholder="Write a sentence using Pushmataha..."', 'data-label="Vocabulary: honor" placeholder="Write a sentence using honor..."', 1),
     ("['journal-vocab-honor','journal-vocab-protector','journal-vocab-reunited','journal-vocab-survived','journal-vocab-lifeless']",
      "['journal-vocab-lifeless','journal-vocab-survived','journal-vocab-honor','journal-vocab-reunited','journal-vocab-protector']", None)],
}
ORDER = ["lifeless", "survived", "honor", "reunited", "protector"]
CH = {"lifeless": 28, "survived": 28, "honor": 28, "reunited": 29, "protector": 29}
SHORT = {"lifeless": "Without life; not moving or breathing.", "survived": "Stayed alive through something dangerous.", "honor": NEWDEF,
         "reunited": "Brought back together after being apart.", "protector": "Someone who keeps another person safe from harm."}
PERM = [3, 2, 4, 0, 1]
EVERY = [('from Chapters 28–29', 'from this week&rsquo;s chapters'), ('honour', 'honor'), ('signalling', 'signaling'), ('memorise', 'memorize'), ('centre', 'center'),
         ('what happened to the Choctaw in 1831.', 'what happened to the Choctaw from 1831 to 1833.'), (OLDDEF, NEWDEF),
         ('executed without regard for', 'carried out without regard for'), ('>executed </span>', '>carried out </span>')]

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
    if not m: sys.exit('no match grid')
    ind = "\n          "; rows = []
    for i, w in enumerate(ORDER):
        rows.append('<div class="match-item is-word" data-match="%s" onclick="matchClick(this)">%s</div>' % ("ABCDE"[i], w))
        rows.append('<div class="match-item" data-match="%s" onclick="matchClick(this)">%s</div>' % ("ABCDE"[PERM[i]], SHORT[ORDER[PERM[i]]]))
    return s[:m.start()] + m.group(1) + ind + ind.join(rows) + m.group(3) + s[m.end():]
def vocab(d, s):
    if 'Word Bank' in s:
        s = reorder(s, r'<p style="margin:4px 0;"><strong>(?:%s)</strong> &mdash; [^\n]*</p>' % "|".join(ORDER), "word bank")
    if d == 1:
        s = reorder(s, r'<div class="vocab-decode-item">\s*<div class="decode-sentence">.*?</div>\s*<div class="flip-card.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', "day1 cards")
        for w in ORDER:
            s, n = re.subn(r'(<div class="decode-sentence">(?:(?!</div>).)*<strong style="color:#8B3A20;">%s</strong>(?:(?!</div>).)*?)(</div>)' % w,
                           r'\1 <span class="vocab-ch" style="font-style:normal;font-size:12px;font-weight:700;color:#7A88A8;white-space:nowrap;">Ch. %d</span>\2' % CH[w], s, count=1, flags=re.S | re.I)
            if n != 1: sys.exit('no chapter tag for ' + w)
        s = match_grid(s)
    if d == 2:
        s = reorder(s, r'<p style="font-size:15px;color:#3A4A6B;line-height:1\.8;margin-bottom:\d+(?:px)?;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">(?:%s)</strong>[^\n]*?</p>' % "|".join(ORDER), "day2 sentences")
        s = re.sub(r'margin-bottom:0;">&ldquo;', 'margin-bottom:10px;">&ldquo;', s)
        ms = list(re.finditer(r'margin-bottom:10px;">&ldquo;', s))
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
    for old, new, n in FIX[d] + SWAP[d]:
        c = s.count(old)
        if (n is None and c < 1) or (n is not None and c != n): sys.exit('%s: expected %s of %r, found %d' % (f, n, old[:70], c))
        s = s.replace(old, new)
    for old, new in EVERY: s = s.replace(old, new)
    s = dol(d, s)
    s = vocab(d, s)
    for bad in (SEP, 'removal of 1830', 'honour', 'vocab-pushmataha', OLDDEF, 'root family', 'disagree about nothing'):
        if bad in s: sys.exit('%s: leftover %r' % (f, bad))
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    OUT[f] = s

f = 'lesson-24-fluency.html'
s = io.open(f, encoding='utf-8', newline='').read(); orig = s
a = s.index('<div class="fluency-passage"><p>Pushmataha appeared before us')
end = 'Chapter 1</div>\n  </div>\n      </div>\n'; b = s.index(end, a) + len(end)
s = s[:a] + '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      By day&rsquo;s end, the bonepickers had a new wagon and the burned blankets were replaced, as ordered by Leader. The soldiers delivered bags filled with ears of corn to every wagon of walkers. Naomi was reunited with her mother and father, and that very evening she insisted on helping with the cooking.<br><br>
      &ldquo;Please,&rdquo; she said. &ldquo;I can&rsquo;t sit still and be waited on.&rdquo;<br><br>
      &ldquo;But this is your first day with your family,&rdquo; her mother said. &ldquo;We are celebrating your return.&rdquo;
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 29</div>
  </div>
  </div>
      </div>
''' + s[b:]
FL = [
 ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
  'Chapter 29 is the last chapter of <em>How I Became a Ghost</em>. It opens at the end of a long, frightening day, and for once the news is good. Today you&rsquo;ll practice reading it with accuracy, smoothness, and expression.'),
 ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
  'Read it once to yourself first. Then read it again and keep your voice flowing. The first paragraph is three sentences of good news; let each one arrive without rushing.'),
 ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
  'Now bring the two speakers to life. Naomi is eager and cannot sit still. Her mother is gentle and glad. Let a listener hear which one is talking.'),
 ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;bonepickers,&rdquo; &ldquo;reunited&rdquo; and &ldquo;celebrating&rdquo;?'),
 ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
  'Did Naomi and her mother sound like two different people?'),
 ('You&rsquo;ve read Isaac&rsquo;s voice all week &mdash; now let your voice carry his.', 'You have read Isaac&rsquo;s voice for seven weeks. Now let your voice carry the last chapter.')]
for old, new in FL:
    if s.count(old) != 1: sys.exit('fluency %r x%d' % (old[:50], s.count(old)))
    s = s.replace(old, new)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('fluency: div balance')
OUT[f] = s
for f, s in OUT.items():
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
