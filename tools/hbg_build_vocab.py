# -*- coding: utf-8 -*-
"""Rebuild the How I Became a Ghost vocabulary sections (weeks 18-24, all four days).

Follows the OAO day progression:
  D1 Decode & Discover  - context sentence + flip card per word, then the match game
  D2 Context Detective  - a second book sentence per word with the word bolded, then the match game
  D3 Fill in the Blank  - cloze sentences from the book, checked by checkVocabFillIn()
  D4 Use the Word!      - a textarea per word, collected by gatherAnswers()

Word list: tools/hbg_vocab.py   Quotes: tools/hbg_sentences.py (verified by tools/hbg_verify_quotes.py)
"""
import re, glob, sys, io
sys.path.insert(0, 'tools')
from hbg_vocab import VOCAB
from hbg_sentences import S

GOLD, BROWN = '#C8A850', '#8B3A20'

CSS = """.vocab-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0;}
.vocab-decode-item{display:flex;flex-direction:column;}
.flip-card{perspective:800px;height:175px;cursor:pointer;}
.flip-card-inner{position:relative;width:100%;height:100%;transition:transform .5s ease;transform-style:preserve-3d;}
.flip-card.flipped .flip-card-inner{transform:rotateY(180deg);}
.flip-card-front,.flip-card-back{position:absolute;top:0;left:0;width:100%;height:100%;border-radius:16px;backface-visibility:hidden;-webkit-backface-visibility:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:14px 16px;text-align:center;border:2px solid #E2E8F4;box-shadow:0 2px 10px rgba(14,28,66,.06);}
.flip-card-front{background:#fff;border-top:5px solid #C8A850;}
.flip-card-front .fc-emoji{font-size:28px;margin-bottom:6px;}
.flip-card-front .fc-word{font-family:Georgia,serif;font-size:17px;font-weight:700;color:#0E1C42;margin-bottom:4px;}
.flip-card-front .fc-tap{font-size:11px;color:#7A88A8;font-weight:600;letter-spacing:.3px;}
.flip-card-back{background:linear-gradient(145deg,#0E1C42,#1A2D5A);border-color:#0E1C42;transform:rotateY(180deg);}
.flip-card-back .fc-def{font-size:13.5px;color:#fff;line-height:1.5;font-weight:600;}
.flip-card-back .fc-word-back{font-size:10px;color:#C8A850;text-transform:uppercase;letter-spacing:1px;font-weight:800;margin-bottom:6px;}
.fc-color-1 .flip-card-front{border-top-color:#C8A850;}
.fc-color-2 .flip-card-front{border-top-color:#8B3A20;}
.fc-color-3 .flip-card-front{border-top-color:#5A7A6A;}
.fc-color-4 .flip-card-front{border-top-color:#7B5EA7;}
.fc-color-5 .flip-card-front{border-top-color:#0E1C42;}
@media (max-width:700px){.vocab-grid{grid-template-columns:1fr;}.flip-card{height:165px;}}
"""

CHECK_JS = """
/* ───── VOCAB FILL-IN (Day 3) ───── */
window._vocabFillinDone=false;
function checkVocabFillIn(){
  var items=document.querySelectorAll('#vocabFillinGame .fillin-input');var correct=0;
  items.forEach(function(inp){
    var ans=inp.getAttribute('data-answer').toLowerCase().trim();
    var val=inp.value.toLowerCase().trim();
    if(val===ans){inp.classList.remove('wrong');inp.classList.add('correct');inp.disabled=true;correct++;}
    else{inp.classList.remove('correct');inp.classList.add('wrong');setTimeout(function(){inp.classList.remove('wrong');},600);}
  });
  var fb=document.getElementById('vocabFillinFeedback');
  if(correct===items.length&&fb){fb.classList.add('show');window._vocabFillinDone=true;}
}
"""

def esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def word_bank(words):
    rows = '\n'.join(
        '<p style="margin:4px 0;"><strong>%s</strong> &mdash; %s</p>' % (w, esc(d))
        for w, e, d in words)
    return ("""<details class="vocab-bank" style="margin-bottom:16px;background:#FFFCF0;border:2px solid #F5E6C8;border-radius:10px;padding:0;">
<summary style="padding:12px 16px;cursor:pointer;font-weight:700;font-size:15px;color:%s;list-style:none;display:flex;align-items:center;gap:8px;">
<span style="transition:transform .2s;">&#x25B6;</span> &#x1F4D6; Word Bank &mdash; tap to see this week&rsquo;s definitions
</summary>
<div style="padding:4px 16px 14px;font-size:14px;color:#3A4A6B;line-height:1.7;">
%s
</div>
</details>
""" % (BROWN, rows))

DEF_ORDER = [2, 4, 0, 1, 3]

def match_game(words):
    letters = 'ABCDE'
    rows = []
    for i, (w, e, d) in enumerate(words):
        j = DEF_ORDER[i]
        rows.append('          <div class="match-item is-word" data-match="%s" onclick="matchClick(this)">%s</div>' % (letters[i], w))
        rows.append('          <div class="match-item" data-match="%s" onclick="matchClick(this)">%s</div>' % (letters[j], esc(words[j][2])))
    return ('      <div class="match-game" id="vocabMatch">\n'
            '        <div class="match-grid" id="matchGrid">\n' + '\n'.join(rows) +
            '\n        </div>\n'
            '        <div class="match-feedback" id="matchFeedback">&#x2728; All matched!</div>\n'
            '      </div>')

def bold_word(sentence, word):
    return re.sub(r'\b(' + re.escape(word) + r')\b',
                  r'<strong style="color:%s;">\1</strong>' % BROWN, esc(sentence), count=1, flags=re.I)

def day1(words, chs):
    cards = []
    for i, (w, e, d) in enumerate(words, 1):
        q1 = S[w][0]
        cards.append(
'''        <div class="vocab-decode-item">
          <div class="decode-sentence">&ldquo;%s&rdquo;</div>
          <div class="flip-card fc-color-%d" onclick="this.classList.toggle('flipped')">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <div class="fc-emoji">%s</div>
                <div class="fc-word">%s</div>
                <div class="fc-tap">think first, then tap</div>
              </div>
              <div class="flip-card-back">
                <div class="fc-word-back">%s</div>
                <div class="fc-def">%s</div>
              </div>
            </div>
          </div>
        </div>''' % (bold_word(q1, w), i, e, w, w, esc(d)))
    return ('Decode &amp; Discover &mdash; words from Chapters ' + chs,
            '      <p>Five words from Chapters %s. Read the sentence from the book first and make your best guess at the word, then tap the card to check.</p>\n'
            '      <div class="vocab-grid">\n%s\n      </div>\n'
            '      <div class="callout callout-info" style="margin-top:14px;"><span class="callout-icon">&#127919;</span><p><strong>Now check yourself.</strong> Match each word to its meaning.</p></div>\n%s'
            % (chs, '\n'.join(cards), match_game(words)))

def day2(words, chs):
    lines = []
    for n, (w, e, d) in enumerate(words):
        q = S[w][1] or S[w][0]
        last = ';margin-bottom:0' if n == len(words) - 1 else ';margin-bottom:10px'
        lines.append('        <p style="font-size:15px;color:#3A4A6B;line-height:1.8%s;">&ldquo;%s&rdquo;</p>'
                     % (last, bold_word(q, w)))
    return ('Context Detective',
            word_bank(words) +
            '\n      <p>You met these words yesterday. Today, work out how they behave in a sentence &mdash; then match each one to its meaning.</p>\n'
            '      <div class="callout callout-vocab" style="margin-top:14px;"><span class="callout-icon">&#x1F50D;</span>'
            '<p><strong>Context Detective:</strong> Read each sentence from Chapters %s. What clues around the bolded word tell you what it means?</p></div>\n'
            '      <div style="background:#FAFBFF;border:2px solid #E2E8F4;border-radius:12px;padding:16px 18px;margin-bottom:16px;">\n%s\n      </div>\n%s'
            % (chs, '\n'.join(lines), match_game(words)))

def day3(words, chs):
    items = []
    for w, e, d in words:
        cloze = S[w][2]
        before, after = cloze.split('{}')
        items.append('        <div class="fillin-item">%s<input class="fillin-input" data-answer="%s" maxlength="%d" placeholder="______">%s</div>'
                     % (esc(before), w.lower(), max(len(w) + 2, 12), esc(after)))
    return ('Fill in the Blank',
            word_bank(words) +
            '\n      <p>You have read these words and worked out their meanings. Now put them back where they belong.</p>\n'
            '      <div class="callout callout-info"><span class="callout-icon">&#x1F3AF;</span><p><strong>Practice:</strong> Type the word that fits each sentence from Chapters %s, then check your answers.</p></div>\n'
            '      <div class="fillin-game" id="vocabFillinGame">\n%s\n'
            '        <button class="fillin-check-btn" onclick="checkVocabFillIn()">Check My Words</button>\n'
            '        <div class="fillin-feedback" id="vocabFillinFeedback">&#x1F331; All correct &mdash; you know this week&rsquo;s words.</div>\n'
            '      </div>'
            % (chs, '\n'.join(items)))

def day4(words, chs):
    items = []
    for w, e, d in words:
        items.append(
'''      <div class="vocab-use-item" style="margin-bottom:14px;">
        <div style="font-size:18px;font-weight:700;color:%s;margin-bottom:4px;">%s <span style="font-size:13px;font-weight:400;color:#7A88A8;">&mdash; %s</span></div>
        <div class="journal-label">&#x1F4D3; Your sentence <span class="saved-dot" id="dot-vocab-%s"></span></div>
        <textarea class="journal-box" id="journal-vocab-%s" data-label="Vocabulary: %s" placeholder="Write a sentence using %s..." oninput="autoSave(this,'dot-vocab-%s');gatherAnswers();" style="min-height:50px;"></textarea>
      </div>''' % (BROWN, w, esc(d), w.lower(), w.lower(), w, w, w.lower()))
    return ('Use the Word!',
            word_bank(words) +
            '\n      <p>You have worked with these words all week. Show what you know: write your own sentence for each one. Make the sentence prove you understand the word &mdash; not just that you can spell it.</p>\n'
            + '\n'.join(items))

BUILDERS = {1: day1, 2: day2, 3: day3, 4: day4}
TITLES = {1: '&#x1F524; Vocabulary', 2: '&#x1F524; Vocabulary',
          3: '&#x1F524; Vocabulary: Use It', 4: '&#x1F524; Vocabulary'}

STATUS = re.compile(r"\(matchCount >= 4 \? '\u2705' : '\u2b1c'\) \+ ' Vocabulary Match")
BLOCK = re.compile(r'( *<!-- VOCABULARY -->\n).*?(\n\n *<!-- GRAMMAR -->)', re.S)

def build(path, week, day):
    rng, words = VOCAB[week]
    chs = rng.replace('-', '–')
    sub, body = BUILDERS[day](words, chs)
    s = io.open(path, encoding='utf-8').read()
    orig = s

    block = ('  <div class="activity bl-cyan">\n'
             '    <div class="activity-head"><div class="activity-num" style="background:%s;">2</div><div style="flex:1;">'
             '<div class="activity-title">%s</div><div class="activity-sub">%s</div></div></div>\n'
             '    <div class="activity-body">\n%s\n    </div>\n  </div>' % (GOLD, TITLES[day], sub, body))
    s = BLOCK.sub(lambda m: m.group(1) + block + m.group(2), s, count=1)

    if day == 1 and '.flip-card{' not in s:
        line = s.rindex('\n', 0, s.index('.match-game')) + 1
        s = s[:line] + CSS + s[line:]
    if day == 1 and '.vocab-decode-item{' not in s:
        s = s.replace('.flip-card{perspective', '.vocab-decode-item{display:flex;flex-direction:column;}\n.flip-card{perspective', 1)

    if day == 3:
        if 'function checkVocabFillIn' not in s:
            s = s.replace('\nfunction matchClick(', CHECK_JS + '\nfunction matchClick(', 1)
        s = STATUS.sub("(window._vocabFillinDone ? '\u2705' : '\u2b1c') + ' Vocabulary Fill-In", s)
    if day == 4:
        ids = ','.join("'journal-vocab-%s'" % w.lower() for w, e, d in words)
        sec = "    { title: '\U0001F524 USE THE WORD', ids: [%s] },\n" % ids
        if sec not in s:                                   # idempotent: only insert once
            s = s.replace('  var sections = [\n', '  var sections = [\n' + sec, 1)
        first = words[0][0].lower()
        s = STATUS.sub("(document.getElementById('journal-vocab-%s') && document.getElementById('journal-vocab-%s')"
                       ".value.trim() ? '\u2705' : '\u2b1c') + ' Use the Word" % (first, first), s)

    if s != orig:
        io.open(path, 'w', encoding='utf-8', newline='').write(s)
        return True
    return False

if __name__ == '__main__':
    n = 0
    for week in sorted(VOCAB):
        for day in (1, 2, 3, 4):
            for f in sorted(glob.glob('lesson-%d-%d-*.html' % (week, day))):
                if '.bak' in f:
                    continue
                if build(f, week, day):
                    n += 1
                    print('  built', f)
    print('files updated:', n)
