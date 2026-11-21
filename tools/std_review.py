#!/usr/bin/env python3
"""Rebuild standards/gN-q3q4-standards-review.xlsx from the week manifests (standards/gN-week-WW.json)
and standards/crosswalk-gN.json. Keeps the workbook's styles and Notes sheet; rewrites Summary,
All blocks and the crosswalk sheet. Weeks with no manifest are left out (G3 week 17 = break week).
Usage from the repo root:  python3 tools/std_review.py <grade>    (Nov 20 2026)"""
import glob, json, re, sys, openpyxl
from copy import copy
G = int(sys.argv[1]); P = f'standards/g{G}-standards-review.xlsx' if G == 5 else f'standards/g{G}-q3q4-standards-review.xlsx'
CW = json.load(open(f'standards/crosswalk-g{G}.json', encoding='utf8'))['map']
ST = ['TX', 'AR', 'MO', 'AL', 'TN', 'PR']
sh = lambda c: c.replace('ELA.', '')
def fmt(st, v):
    if v == 'pending' or v is None: return 'pending'
    if st == 'TX': v = ['TEKS ' + re.sub(r'^110\.\d+\(b\)', '', x) for x in v]
    return ', '.join(v) or None
DECIDED = {5: [(19, 'Nov 21: EE.1.1 added to the week 19 bar (every Chapter Thinking question asks for book evidence).'),
               (20, 'Nov 21: bar kept as is (every code on it is taught; nothing taught is off it). R.1.1 and C.1.3 added to the crosswalk.')],
           4: [(17, 'Check-in Q5 is context clues (V.1.3); left off the bar (check-in only)'),
               (27, 'Nov 20: V.1.3 and EE.4.1 added to the bar (EE.4.1 only in week 27: the Discussion Prompts block is the only place it is taught)'),
               ('28-31', 'Nov 20: V.1.3 added to the bar'),
               (31, 'Nov 20: C.2.1 removed from the bar (nothing in week 31 has students present orally)'),
               ('14, 19', 'Nov 20: standards bars added to the Anne scrapbook and Number the Stars project pages (tagged whole-page)')],
           3: [(24, 'Nov 20: R.3.1 added to the bar (Poetry Corner)'),
               (32, 'Nov 20: C.2.1, C.5.1, F.1.4 removed from the bar (not taught that week)'),
               (32, 'Nov 20: F.1.3 and R.3.1 added to the bar (spelling/morphology; Poetry Corner days 2 and 4)')]}
wb = openpyxl.load_workbook(P)
def reset(ws, rows):
    style = [copy(ws.cell(2, c)._style) for c in range(1, ws.max_column + 1)]
    ws.delete_rows(2, ws.max_row)
    for i, r in enumerate(rows, 2):
        for j, v in enumerate(r, 1):
            cell = ws.cell(i, j, v)
            if j <= len(style): cell._style = copy(style[j - 1])
summ, allb, total = [], [], 0
for f in sorted(glob.glob(f'standards/g{G}-week-*.json'), key=lambda x: int(re.findall(r'(\d+)\.json', x)[0])):
    m = json.load(open(f, encoding='utf8')); w = m['week']
    bar, tagged, n = set(), set(), 0
    for p in m['pages']:
        bar |= set(p['standards_bar']); tagged |= set(p['lesson_tags']['FL']); n += len(p['blocks'])
        for b in p['blocks']:
            allb.append([w, p['page'], b['id'], b['title'], ', '.join(map(sh, b['FL']))] + [fmt(s, b.get(s)) for s in ST])
    total += n
    j = lambda xs: ', '.join(sorted(map(sh, xs))) or None
    summ.append([w, len(m['pages']), n, j(bar), j(tagged - bar), j(bar - tagged)])
import os
if os.path.exists(f'standards/g{G}-projects.json'):   # unit project pages tagged whole-page (tools/std_tag.py projects)
    for p in json.load(open(f'standards/g{G}-projects.json', encoding='utf8'))['pages']:
        for b in p['blocks']:
            allb.append([p['week'], p['page'], b['id'], b['title'], ', '.join(map(sh, b['FL']))] + [fmt(s, b.get(s)) for s in ST])
        total += len(p['blocks'])
        summ.append([f"Project (wk {p['week']})", 1, len(p['blocks']), ', '.join(sorted(map(sh, p['standards_bar']))), None, None])
summ += [[None] * 6, ['Total', None, total, None, None, None], [None] * 6, ['Bar decisions', None, None, None, None, None]]
summ += [[a, b, None, None, None, None] for a, b in DECIDED[G]]
reset(wb['Summary'], summ); reset(wb['All blocks'], allb)
cws = [ws for ws in wb if 'crosswalk' in ws.title][0]
reset(cws, [[sh(k)] + [fmt(s, v.get(s)) for s in ST] for k, v in CW.items()])
for ws in wb:
    if ws.title in ('Summary', 'All blocks'): ws.auto_filter.ref = None
if G == 5:   # notes + sheet name follow crosswalk-g5.json
    cws.title = 'G5 crosswalk'
    nt = wb['Notes']; style = [copy(nt.cell(1, c)._style) for c in (1, 2)]
    nt.delete_rows(1, nt.max_row)
    notes = json.load(open('standards/crosswalk-g5.json', encoding='utf8'))['notes']
    rows = list(notes.items()) + [('Where tags live', "Each block/question: data-std (FL) + data-std-id. Each page: <script id=\"oao-standards\"> with all 7 states. Each week: standards/g5-week-WW.json. Nothing visible changed.")]
    for i, (k, v) in enumerate(rows, 1):
        nt.cell(i, 1, k)._style = copy(style[0]); nt.cell(i, 2, v)._style = copy(style[1])
wb.save(P); print(P, len(summ), 'summary rows,', len(allb), 'blocks')
