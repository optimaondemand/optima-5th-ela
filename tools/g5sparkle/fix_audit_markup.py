#!/usr/bin/env python3
"""Q3-Q4 audit (Nov 25 2026): markup fixes found by the tag-nesting scan. Week 31's round-2 folds (plain_wk31b.py) closed their
<details> at a later block, so the browser closed them at the key-concept's </div> and later met a stray </details>; two root lines
lost their opening <p>. Rendering did not change; the markup is now valid."""
import io, re, sys
def fix(f, reps):
    s = io.open(f, encoding='utf-8', newline='').read()
    for a, b in reps:
        if s.count(a) != 1: sys.exit('%s: x%d %r' % (f, s.count(a), a[:60]))
        s = s.replace(a, b)
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
ROOT_P = ('\n  <em>fort + val/valid</em> (strong / worth)', '\n  <p><em>fort + val/valid</em> (strong / worth)')
fix('lesson-31-1-comparison-plan.html', [ROOT_P])
s2 = io.open('lesson-31-2-comparison-sources.html', encoding='utf-8').read()
m = re.search(r'(Cumulative Spelling — All Units</div><details>.*?)(\n</div>\n<div class="callout callout-think">)', s2, re.S)
fix('lesson-31-2-comparison-sources.html', [ROOT_P, (m.group(0), m.group(1) + '</details>' + m.group(2)), ('  </div>\n</details></div>', '  </div>\n</div>')])
s4 = io.open('lesson-31-4-comparison-submit.html', encoding='utf-8').read()
m = re.search(r'(Grammar Spiral Review — All Year</div><details>.*?)(\n</div>\n<div class="callout callout-think">)', s4, re.S)
fix('lesson-31-4-comparison-submit.html', [(m.group(0), m.group(1) + '</details>' + m.group(2)), ('fix that.&rdquo;</p></details></div>', 'fix that.&rdquo;</p></div>')])
