#!/usr/bin/env python3
"""setdata.py - change one lesson's DATA in BOTH places it lives (data/g5ela-W-D.json and
the page's embedded #oao-data block), so they never drift. Used by the Nov 12 2026 G5 polish pass.

    python tools/g5sparkle/setdata.py lesson-18-2-hbg-ch5.html data/g5ela-18-2.json patch.json [--apply]
patch.json is a dict of top-level keys to replace, plus optional "howDo": {"<match>": [do lines]}.
"""
import io, json, re, sys
lesson, dfile, pfile = sys.argv[1:4]; apply = '--apply' in sys.argv
D = json.load(io.open(dfile, encoding='utf-8')); P = json.load(io.open(pfile, encoding='utf-8'))
for k, v in P.items():
    if k == 'howDo':
        for m, lines in v.items():
            hit = [x for x in D.get('how', []) if x.get('match') == m]
            if not hit: sys.exit('no how block ' + m)
            hit[0]['do'] = lines
    else:
        D[k] = v
html = io.open(lesson, encoding='utf-8', newline='').read()
rx = re.compile(r'(<script type="application/json" id="oao-data">)(.*?)(</script>)', re.S)
m = rx.search(html)
if not m: sys.exit('no oao-data in ' + lesson)
old = json.loads(m.group(2))
if old != json.load(io.open(dfile, encoding='utf-8')): print('WARNING: page DATA and data file already differed; page now follows the data file')
body = json.dumps(D, ensure_ascii=False, indent=1).replace('</', '<\\/')
new = html[:m.start(2)] + body + html[m.end(2):]
if apply:
    io.open(lesson, 'w', encoding='utf-8', newline='').write(new)
    io.open(dfile, 'w', encoding='utf-8').write(json.dumps(D, ensure_ascii=False, indent=1) + '\n')
    print('written', lesson, dfile)
else:
    print('dry run ok', lesson)
