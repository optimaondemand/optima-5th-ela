#!/usr/bin/env python3
"""Add or remove Florida codes on the visible standards bar (standards panel FL row + footer FL list)
of every lesson and fluency page in the given weeks (Nov 20 2026 bar decisions).
Usage from the repo root:  python3 tools/bar_edit.py 27-31 +ELA.4.V.1.3 -ELA.4.C.2.1
New codes go in standard order (R, C, F, V, then K12 EE). Re-runnable. In G4, run tools/fix_tx_footers.py
afterwards so the Texas row follows; then tools/std_tag.py for the same weeks."""
import glob, re, sys
ORDER = {'R': 0, 'C': 1, 'F': 2, 'V': 3, 'EE': 4}
def key(c):
    p = c.split('.')  # ELA.4.R.1.4 / ELA.K12.EE.4.1
    return (ORDER[p[2]], int(p[3]), int(p[4]))
def edit(codes, add, rem):
    codes = [c for c in codes if c not in rem]
    for a in add:
        if a in codes: continue
        i = next((k for k, c in enumerate(codes) if key(c) > key(a)), len(codes))
        codes.insert(i, a)
    return codes
a, b = (int(x) for x in (sys.argv[1].split('-') * 2)[:2])
add = [x[1:] for x in sys.argv[2:] if x[0] == '+']; rem = [x[1:] for x in sys.argv[2:] if x[0] == '-']
for w in range(a, b + 1):
    for f in sorted(glob.glob(f'lesson-{w}-*.html')):   # lessons, fluency and check-in
        s = open(f, encoding='utf8', newline='').read()
        def panel(m):   # keeps the page's own separator (" · " or " &middot; ")
            sep = ' &middot; ' if '&middot;' in m.group(2) else ' · '
            return m.group(1) + sep.join(f'<span class="fl-code">{c}</span>' for c in
                edit(re.findall(r'fl-code">([^<]*)<', m.group(2)), add, rem)) + m.group(3)
        s2 = re.sub(r'(<div class="standards-codes">)((?:<span class="fl-code">[^<]*</span>(?: · | &middot; )?)+)(</div>)', panel, s, count=1)
        s2 = re.sub(r'(<div class="footer-standards">FL: )([^<·]*?)( · TX: | &middot; TX: |</div>)',
            lambda m: m.group(1) + ', '.join(edit([c.strip() for c in m.group(2).split(',')], add, rem)) + m.group(3), s2, count=1)
        if s2 != s:
            open(f, 'w', encoding='utf8', newline='').write(s2); print('bar edited:', f)
        else: print('no change:', f)
