# -*- coding: utf-8 -*-
"""Rebuild the How I Became a Ghost vocabulary blocks (weeks 18-24).

Day 1 gets flip cards (introduce the words) plus the match game; Days 2-4 keep
their match game but use that week's words instead of the copy-pasted set.
"""
import re, glob, sys, io
sys.path.insert(0, 'tools')
from hbg_vocab import VOCAB

CSS = """.vocab-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0;}
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

def cards_html(words):
    out = ['      <div class="vocab-grid">']
    for i, (w, e, d) in enumerate(words, 1):
        out.append('        <div class="flip-card fc-color-%d" onclick="this.classList.toggle(\'flipped\')">' % i)
        out.append('          <div class="flip-card-inner">')
        out.append('            <div class="flip-card-front">')
        out.append('              <div class="fc-emoji">%s</div>' % e)
        out.append('              <div class="fc-word">%s</div>' % w)
        out.append('              <div class="fc-tap">think first, then tap</div>')
        out.append('            </div>')
        out.append('            <div class="flip-card-back">')
        out.append('              <div class="fc-word-back">%s</div>' % w)
        out.append('              <div class="fc-def">%s</div>' % d)
        out.append('            </div>')
        out.append('          </div>')
        out.append('        </div>')
    out.append('      </div>')
    return '\n'.join(out)

DEF_ORDER = [2, 4, 0, 1, 3]   # definitions offset from their word, same shape the old block used

def match_items(words):
    letters = 'ABCDE'
    rows = []
    for i, (w, e, d) in enumerate(words):
        j = DEF_ORDER[i]
        dw, de, dd = words[j]
        rows.append('          <div class="match-item is-word" data-match="%s" onclick="matchClick(this)">%s</div>' % (letters[i], w))
        rows.append('          <div class="match-item" data-match="%s" onclick="matchClick(this)">%s</div>' % (letters[j], dd))
    return '\n'.join(rows)

GRID = re.compile(r'(<div class="match-grid" id="matchGrid">\s*\n).*?(\n\s*</div>\s*\n\s*<div class="match-feedback")', re.S)
OLDCOPY = re.compile(r'<p>Yesterday you learned these five words\. Today, match each word to its meaning\. Think before you tap!</p>')
SUB = re.compile(r'(<div class="activity-title">\s*\U0001F524 Vocabulary</div><div class="activity-sub">)[^<]*(</div>)')

def build(path, week, day):
    rng, words = VOCAB[week]
    s = io.open(path, encoding='utf-8').read()
    orig = s
    s = GRID.sub(lambda m: m.group(1) + match_items(words) + m.group(2), s, count=1)
    if day == 1:
        chs = rng.replace('-', '–')
        intro = ('<p>Five words from Chapters %s. Read each card, say the word out loud, '
                 'and make your best guess at the meaning before you tap it over.</p>' % chs)
        s = OLDCOPY.sub(intro + '\n' + cards_html(words) +
                        '\n      <div class="callout callout-info" style="margin-top:14px;">'
                        '<span class="callout-icon">&#127919;</span><p><strong>Now check yourself.</strong> '
                        'Match each word to its meaning below.</p></div>', s, count=1)
        s = SUB.sub(lambda m: m.group(1) + 'Decode &amp; Discover — words from Chapters ' + chs + m.group(2), s, count=1)
        if '.flip-card{' not in s:
            anchor = s.index('.match-game')
            line = s.rindex('\n', 0, anchor) + 1
            s = s[:line] + CSS + s[line:]
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
                    print('  updated', f)
    print('files updated:', n)
