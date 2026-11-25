#!/usr/bin/env python3
"""32.2 page structure (found Nov 25 2026 in the week 32 test): the Warm-Up panel closed early after the video placeholder and never closed after its own activities, and three Word Study
activities (Grammar, Morphology, Spelling) closed early, and the page wrapper never closed after the footer after an auto-inserted block, so their checklists, journal tasks
and the word game sat outside every tab. Moves the closing tags to where they belong; no text changes."""
import io, re, sys
p = 'lesson-32-2-fluency-draft.html'
s = io.open(p, encoding='utf-8', newline='').read(); o = s
def one(old, new):
    global s
    if s.count(old) != 1: sys.exit('x%d %r' % (s.count(old), old[:70]))
    s = s.replace(old, new)
one('<p>Before you start: read as a hunter, not as a reader.</p></div>\n</div>\n</div>\n<div class="key-concept">', '<p>Before you start: read as a hunter, not as a reader.</p></div>\n<div class="key-concept">')
one('Keep the reading journal and the two chosen novels close by.</div>\n</div>\n</div>\n\n</div>\n</div><div class="activity bl-sage">', 'Keep the reading journal and the two chosen novels close by.</div>\n</div>\n</div>\n<div class="activity bl-sage">')
one('<span class="saved-dot" id="dot-grammar"></span></div></div></div><div class="activity bl-plum">', '<span class="saved-dot" id="dot-grammar"></span></div></div></div></div><div class="activity bl-plum">')
one('Continue to 🔤 Word Study →</button></div><div class="tab-panel" id="tab-words">', 'Continue to 🔤 Word Study →</button></div></div><div class="tab-panel" id="tab-words">')
one('Four roots, four units, one year. You will keep these.</div></div>\n</div>\n</div>\n<div class="callout callout-think">', 'Four roots, four units, one year. You will keep these.</div></div>\n<div class="callout callout-think">')
one('style="display:none;"></div></div></div>\n</div>\n</div>\n<div class="key-concept"><div class="key-concept-label">📌 Final Spelling Review', 'style="display:none;"></div></div></div>\n<div class="key-concept"><div class="key-concept-label">📌 Final Spelling Review')
# morphology ends where spelling starts
m = re.search(r'(correctly spelled\.</p></div>|how the root gives you the word&rsquo;s meaning\.</p></div>|</p></div>)(<div class="activity bl-[a-z]+"><div class="activity-head"><div class="activity-num"[^>]*>3</div><div style="flex:1;"><div class="activity-title">🔠 Spelling)', s)
if not m: sys.exit('no morph end')
s = s[:m.end(1)] + '</div></div>' + s[m.end(1):]
one('</p></div><div class="tab-next-wrap"><p class="tab-transition-voice">Edited and polished.', '</p></div></div></div><div class="tab-next-wrap"><p class="tab-transition-voice">Edited and polished.')
one('Continue to 🎙️ Fluency →</button></div><div class="tab-panel" id="tab-reading">', 'Continue to 🎙️ Fluency →</button></div></div><div class="tab-panel" id="tab-reading">')
one('Portfolio Draft</div>\n</div>\n\n<script>', 'Portfolio Draft</div>\n</div>\n</div>\n<script>')
b = s.count('<div') - s.count('</div')
print('balance', o.count('<div') - o.count('</div'), '->', b)
if b != 0: sys.exit('unbalanced')
if '--apply' in sys.argv: io.open(p, 'w', encoding='utf-8', newline='').write(s); print('written')
