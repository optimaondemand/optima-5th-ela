#!/usr/bin/env python3
"""Week 20 accuracy fixes (approved by Bethany Nov 21 2026; audit claude/g5-ela-wk20-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 12-15). Every replacement asserts its count;
div balance must not change. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-20-1-hbg-ch12.html', 2: 'lesson-20-2-hbg-ch13.html', 3: 'lesson-20-3-hbg-ch14.html', 4: 'lesson-20-4-hbg-ch15.html'}
WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>', '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.', 'I wrote my three Read Like a Writer answers on the Reading tab.', 1)
FIX = {
 1: [  # DOL fix-it named Naomi on the Ch. 12 day (she is revealed in Ch. 13); now a Ch. 12 sentence
  ('border-left:4px solid #8B3A20;">naomi was taken and all the camp was afraid to speak or to help her</div>',
   'border-left:4px solid #8B3A20;">the snow swirled in circles and we were blinded by it</div>', 1),
  ('<strong>Corrected:</strong> Naomi was taken, and all the camp was afraid to speak.</p>',
   '<strong>Corrected:</strong> The snow swirled in circles, and we were blinded by it.</p>', 1),
  ('Compound sentence: comma before &ldquo;and.&rdquo; Trim &ldquo;or to help her&rdquo; &mdash; it repeats the idea. Capitalize Naomi.',
   'Compound sentence: two complete sentences joined by &ldquo;and,&rdquo; so a comma goes before &ldquo;and.&rdquo; Capitalize the first word.', 1),
  ('In your reading journal: identify', 'In the box below, identify', 1), WW],
 2: [  # the grammar sentence said Naomi walked beside him; she is held by the soldiers
  ('>Naomi walked beside him, and she did not complain once.</span>', '>Joseph walked ahead, and Isaac followed him into the woods.</span>', 1),
  ('>Naomi walked beside him and, she did not complain once.</span>', '>Joseph walked ahead and, Isaac followed him into the woods.</span>', 1),
  RWMCHK, WW],
 3: [  # Joseph cut his ropes and ran; he became the panther when the soldiers reached the cave
  ('He escaped by becoming the panther.', 'He cut his ropes with a sharp stone and ran, and when the soldiers found his cave, he became the panther.', 1),
  ('<span class="q-num">3</span>&#127775; <strong>Week Closer.</strong> In Chapters 12, 13, and 14,', '<span class="q-num">3</span>In Chapters 12, 13, and 14,', 1),
  RWMCHK, WW],
 4: [  # Isaac has not met Naomi by Ch. 15; DOL fix-it now a Ch. 15 sentence
  ('border-left:4px solid #8B3A20;">when isaac looked at naomi he knew she needed his help</div>',
   'border-left:4px solid #8B3A20;">when the warm shiver came all isaac could see was a cloudy mist</div>', 1),
  ('<strong>Corrected:</strong> When Isaac looked at Naomi, he knew she needed his help.</p>',
   '<strong>Corrected:</strong> When the warm shiver came, all Isaac could see was a cloudy mist.</p>', 1),
  ('&#128205; Chapter 15 &mdash; The Bending Branch</div>', '&#128205; Chapter 15 &mdash; The Bending Branch of Treaty Talk</div>', 1),
  WW],
}
for d in F: FIX[d].append(("he joked.&rdquo;", "he joked.", 1 if d in (1, 2) else 0))
for d in (1, 2): FIX[d].append(("I said.&rdquo;", "I said.", 1))

# ── vocabulary: book order (determined Ch. 12; then treaty, council, invisible, permission in Ch. 15) ──
ORDER = ["determined", "treaty", "council", "invisible", "permission"]
CH = {"determined": 12, "treaty": 15, "council": 15, "invisible": 15, "permission": 15}
SHORT = {"determined": "Having your mind firmly made up, no matter how hard the thing is.",
         "treaty": "A formal agreement between governments.", "council": "A group chosen to make decisions for their people.",
         "invisible": "Impossible to see.", "permission": "Being allowed to do something by someone in charge."}
PERM = [2, 3, 4, 0, 1]   # meaning shown beside word i (never its own)
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
        # the treaty card's sentence bolded "Treaty" inside "Treaty Talk"; use Joseph's line that has the word itself
        o = '&ldquo;That was what they agreed, at the <strong style="color:#8B3A20;">Treaty</strong> Talk.&rdquo;'
        if s.count(o) != 1: sys.exit('treaty card x%d' % s.count(o))
        s = s.replace(o, '&ldquo;That is what the <strong style="color:#8B3A20;">treaty</strong> says,&rdquo; Joseph said.')
        s = reorder(s, r'<div class="vocab-decode-item">\s*<div class="decode-sentence">.*?</div>\s*<div class="flip-card.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', "day1 cards")
        for w in ORDER:
            s, n = re.subn(r'(<div class="decode-sentence">(?:(?!</div>).)*<strong style="color:#8B3A20;">%s</strong>(?:(?!</div>).)*?)(</div>)' % w,
                           r'\1 <span class="vocab-ch" style="font-style:normal;font-size:12px;font-weight:700;color:#7A88A8;white-space:nowrap;">Ch. %d</span>\2' % CH[w], s, count=1, flags=re.S | re.I)
            if n != 1: sys.exit('no chapter tag for ' + w)
        s = s.replace('Five words from Chapters 12–15.', 'Five words from Chapters 12 and 15.', 1)
        s = s.replace('Decode &amp; Discover &mdash; words from Chapters 12–15', 'Decode &amp; Discover &mdash; words from Chapters 12 and 15', 1)
        s = match_grid(s)
    if d == 2:
        s = s.replace('&ldquo;That is what the <strong style="color:#8B3A20;">treaty</strong> says,” Joseph said.&rdquo;', '&ldquo;That is what the <strong style="color:#8B3A20;">treaty</strong> says,” Joseph said.')
        s = reorder(s, r'<p style="font-size:15px;color:#3A4A6B;line-height:1\.8;margin-bottom:\d+(?:px)?;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">(?:%s)</strong>[^\n]*?</p>' % "|".join(w.capitalize() + '|' + w for w in ORDER), "day2 sentences")
        s = re.sub(r'margin-bottom:0;">&ldquo;', 'margin-bottom:10px;">&ldquo;', s)
        ms = list(re.finditer(r'margin-bottom:10px;">&ldquo;', s))
        # the last of the five context sentences keeps margin 0
        five = [m for m in ms if re.match(r'margin-bottom:10px;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">', s[m.start():m.start() + 400])]
        last = five[-1]; s = s[:last.start()] + 'margin-bottom:0;">&ldquo;' + s[last.end():]
        s = s.replace('Read each sentence from Chapters 12–15.', 'Read each sentence from Chapters 12 and 15.')
        s = match_grid(s)
    if d == 3:
        s = reorder(s, r'<div class="fillin-item">[^\n]*?</div>', "day3 fill-in")
        s = s.replace('each sentence from Chapters 12–15,', 'each sentence from Chapters 12 and 15,')
    if d == 4:
        s = reorder(s, r'<div class="vocab-use-item".*?</textarea>\s*</div>', "day4 use-it")
    return s

for d, f in F.items():
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    for old, new, n in FIX[d]:
        if s.count(old) != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], s.count(old)))
        if n: s = s.replace(old, new)
    s = vocab(d, s)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit(f + ': div balance')
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)

f = 'lesson-20-fluency.html'   # one continuous Ch. 12 stretch (the icicle dream), credited right
s = io.open(f, encoding='utf-8', newline='').read(); orig = s
a = s.index('<div class="fluency-passage"><p>When we stopped')
end = 'Chapter 1</div>\n  </div>\n      </div>\n'; b = s.index(end, a) + len(end)
s = s[:a] + '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      When you cannot see, your mind tells strange stories. Maybe that&rsquo;s how it happens, I thought. That is how I become a ghost. I bump into a tree and icicles fall all around me. I slip and fall. Then one long dagger icicle waits for its turn to fall.<br><br>
      Everybody in the world stares at that one giant icicle. They hold their breath. I look at the icicle, too. I realize I am lying right under it.<br><br>
      &ldquo;No,&rdquo; I whisper.<br><br>
      The icicle responds. It shakes, but it keeps everybody waiting. It is a very cruel icicle; anybody can see that. Then, as if it has nothing better to do, the icicle falls. I close my eyes. The icicle stabs me in the heart!<br><br>
      &ldquo;No!&rdquo; I shouted. I was in the real world.
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 12</div>
  </div>
  </div>
      </div>
''' + s[b:]
for old, new in [
 ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
  'In Chapter 12, Isaac walks blind through a snowstorm, and his mind tells him a strange story. Today you&rsquo;ll practice reading it with accuracy, smoothness, and the tension it builds.'),
 ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
  'Read it once to yourself first. Then read it again and keep your voice flowing. Let the short sentences slow down as the icicle waits to fall.'),
 ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
  'Now bring the tension to life. Read the whispered &ldquo;No&rdquo; quietly and the shouted &ldquo;No!&rdquo; with force. Then let the last line, &ldquo;I was in the real world,&rdquo; sound like waking up.'),
 ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;dagger&rdquo; and &ldquo;realize&rdquo;?'),
 ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
  'Did my voice build the tension as the icicle waited? Did the two &ldquo;No&rdquo;s sound different?')]:
    if s.count(old) != 1: sys.exit('fluency %r x%d' % (old[:50], s.count(old)))
    s = s.replace(old, new)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('fluency: div balance')
io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
