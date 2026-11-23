"""Back-end multi-state standards tags for G5 ELA (ported from optima-4th-ela Nov 21 2026; G5 weeks are tagged
as each week is sparkled, g5-ela-sparkle-lesson step 8j).

Run from the optima-5th-ela repo root:  python3 tools/std_tag.py 19 [20 ...]
Nothing visible changes on any page. For each lesson, fluency page and check-in
in a week it:
  * adds data-std (FL codes) and data-std-id to every activity block / quiz question
  * embeds <script type="application/json" id="oao-standards"> (before the LAST
    </body>) with every block's tags for FL, TX, AR, MO, AL, TN, PR and a lesson roll-up
  * writes standards/g5-week-WW.json, the week manifest
Block codes come from the block's strand (fixed rules) or, for the reading,
thinking and writing blocks, from the week's row below, which follows the week's
v4 S&S standards bar and the What Good Readers Do skill on the pages.
Re-running replaces earlier tags (idempotent).
"""
import json, re, sys, glob, os, html

CW = json.load(open('standards/crosswalk-g5.json', encoding='utf8'))
STATES = ['TX', 'AR', 'MO', 'AL', 'TN', 'PR']
def F(*c): return ['ELA.K12.' + x if x.startswith('EE') else 'ELA.5.' + x for x in c]

#            WGRD + reading blocks        thinking / response blocks         writing blocks
WEEKS = {
 19: dict(read=F('R.1.3'),          think=F('R.1.3', 'EE.1.1'),          write=F('C.1.2')),
 20: dict(read=F('R.1.1'),          think=F('R.1.1', 'EE.1.1'),          write=F('C.1.3')),
 21: dict(read=F('R.1.2'),          think=F('R.1.2', 'EE.1.1'),          write=F('C.1.2', 'C.1.5')),
 22: dict(read=F('R.3.1'),          think=F('R.3.1', 'EE.1.1'),          write=F('C.1.3')),
 23: dict(read=F('R.3.2'),          think=F('R.3.2', 'R.1.2', 'EE.3.1'), write=F('C.1.5')),
 24: dict(read=F('R.3.3'),          think=F('R.3.3', 'R.2.4', 'EE.1.1'), write=F('C.1.3')),
 25: dict(read=F('R.1.1'),          think=F('R.1.1', 'EE.1.1'),          write=F('C.1.2')),
 26: dict(read=F('R.1.3'),          think=F('R.1.3', 'EE.1.1'),          write=F('C.1.2', 'EE.6.1')),
 27: dict(read=F('R.1.1'),          think=F('R.1.1', 'R.3.2', 'EE.1.1'), write=F('C.1.2')),
}
CHECKIN_Q = {(19, 5): F('V.1.3'), (20, 5): F('V.1.3'), (21, 5): F('V.1.3'), (22, 5): F('V.1.3'), (23, 5): F('V.1.3'), (24, 5): F('V.1.3'), (25, 5): F('V.1.3'), (26, 5): F('V.1.3'), (27, 5): F('V.1.3'), (27, 13): F('R.1.4')}   # Q5 is a context-clue item each week

def rule(t, tab, W, bar):
    t = t.lower()
    on = lambda c: c in bar
    if re.search(r'\bvirtue watch\b', t): return W['read']   # G5 keeps it on the page
    if 'what good readers do' in t: return W.get('wgrd', W['read'])
    if 'read & write' in t: return W['think']   # BTGHS before-reading journal box (week 25 on)
    if 'daily oral language' in t: return F('C.3.1')
    if 'copywork' in t: return F('C.1.1')
    if 'poetry corner' in t or 'by heart' in t: return F('R.1.4', 'R.3.1') if on('ELA.5.R.3.1') else F('R.1.4')
    if 'word study connection' in t:
        if 'morph' in t: return F('V.1.2')
        if 'vocab' in t: return F('V.1.2')
        if 'grammar' in t: return F('C.3.1')
        return F('C.3.1', 'F.1.3')
    if re.sub(r'^\W+', '', t).startswith('morphology'): return F('V.1.2', 'F.1.3')
    if 'spelling' in t: return F('C.3.1', 'F.1.3')
    if 'grammar' in t: return F('C.3.1')
    if 'vocabulary' in t:
        c = F('V.1.2')
        if on('ELA.5.V.1.1') and re.search(r'use it|choice|week|words|put th', t): c += F('V.1.1')
        if on('ELA.5.V.1.3') or re.search(r'context|cloze', t): c += F('V.1.3')
        return c
    if 'rwm' in t: return F('C.3.1')
    if 'digital t' in t: return F('C.5.2')
    if 'read the table' in t: return F('R.2.1')
    if 'talk it over' in t or 'discussion prompts' in t: return F('EE.4.1')
    if 'present your essay' in t: return F('C.2.1', 'C.5.1')
    if 'portfolio' in t or 'getting ready to celebrate' in t: return F('C.2.1', 'EE.6.1')
    if 'back to your own writing' in t: return F('C.3.1')
    if re.search(r'chapters? [\d\s\u2013-]+:? ?review|week at a glance', t): return W.get('review', W['read'])
    if re.search(r'writer.s workshop|writing con|part b|part c|final literary|final sentence|build your comparison', t):
        return W['write']
    if re.search(r'chapter thinking|whole-book|source thinking|cross-novel|theme comparison|part a', t): return W['think']
    if tab == 'fluency': return F('F.1.4')
    if tab in ('reading', 'assignment', 'workshop'): return W['read'] if tab == 'reading' else W['think']
    return None

def expand(fl):
    out = {'FL': fl}
    for st in STATES:
        if st == 'PR': out['PR'] = 'pending'; continue
        seen = []
        for c in fl:
            for x in CW['map'][c][st]:
                if x not in seen: seen.append(x)
        out[st] = seen
    return out

STRIP = [(re.compile(r' data-std="[^"]*" data-std-id="[^"]*"'), ''),
         (re.compile(r'<script type="application/json" id="oao-standards">.*?</script>\n', re.S), '')]

def tag_page(path, lid, week, W):
    s = open(path, encoding='utf8', newline='').read()
    for rx, rep in STRIP: s = rx.sub(rep, s)
    bm = re.search(r'class="standards-codes">(.*?)</div>', s, re.S)
    bar = set(re.findall(r'ELA\.[\w]+\.[A-Z]+\.\d\.\d', bm.group(1))) if bm else set()
    tabs = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="tab-panel[^"]*" id="tab-(\w+)"', s)]
    is_checkin, is_fluency = 'checkin' in path, 'fluency' in path
    pat = (re.compile(r'<div class="section-icon (\w+)">|<div class="question"') if is_checkin else
           re.compile(r'<div class="activity(?: bl-[\w-]+)?"|<div class="(intro-card) theme-question"'))
    blocks, out, pos, n, section, qn, untagged = [], [], 0, 0, None, 0, []
    for m in pat.finditer(s):
        if is_checkin:
            if m.group(1): section = m.group(1); continue
            qn += 1
            fl = CHECKIN_Q.get((week, qn)) or {
                'grammar': F('C.3.1'), 'morph': F('V.1.2'), 'spelling': F('F.1.3', 'C.3.1'),
                'writing': W['write']}.get(section, W['think'])
            title = f'Q{qn} ({section})'
        elif m.group(1):
            fl, title = W.get('wonder', W['read']), "Big Question / Today's Wonder"
        else:
            tm = re.search(r'activity-title">(.*?)</div>', s[m.end():m.end() + 1500], re.S)
            title = html.unescape(re.sub(r'<[^>]+>', ' ', tm.group(1))).strip() if tm else ''
            title = re.sub(r'\s+', ' ', title)
            tab = [nm for p, nm in tabs if p < m.start()]
            fl = rule(title, 'fluency' if is_fluency else (tab[-1] if tab else ''), W, bar)
        if fl == 'SKIP': continue
        if not fl: untagged.append(title); continue
        n += 1
        bid = f'{lid}-{n:02d}'
        out.append(s[pos:m.end()]); out.append(f' data-std="{" ".join(fl)}" data-std-id="{bid}"'); pos = m.end()
        blocks.append(dict(id=bid, title=title, **expand(fl)))
    out.append(s[pos:]); s = ''.join(out)
    if not blocks and bar and not is_checkin:   # the fluency page has no activity blocks: tag its passage
        m = re.search(r'<div class="fluency-passage"', s) or re.search(r'<div class="passage"', s)   # week 27 fluency uses class="passage"
        if m:
            fl = F('F.1.4'); bid = f'{lid}-01'
            s = s[:m.end()] + f' data-std="{" ".join(fl)}" data-std-id="{bid}"' + s[m.end():]
            blocks.append(dict(id=bid, title='Fluency passage (whole page)', **expand(fl)))
    allfl = []
    for b in blocks:
        for c in b['FL']:
            if c not in allfl: allfl.append(c)
    page = dict(page=os.path.basename(path), lesson=lid, week=week, grade=5,
                crosswalk='standards/crosswalk-g5.json', standards_bar=sorted(bar),
                lesson_tags=expand(allfl), blocks=blocks)
    js = json.dumps(page, ensure_ascii=False).replace('</', '<\\/')
    i = s.rfind('</body>')   # the last one: earlier '</body>' strings sit inside print/export JS
    s = s[:i] + f'<script type="application/json" id="oao-standards">{js}</script>\n' + s[i:]
    open(path, 'w', encoding='utf8', newline='').write(s)
    return page, untagged

for week in [int(a) for a in sys.argv[1:]]:
    W = WEEKS[week]
    pages = [p for p in sorted(glob.glob(f'lesson-{week}-[1-4]-*.html')) if p.endswith('.html')] + [f'lesson-{week}-fluency.html', f'lesson-{week}-checkin.html']
    manifest = dict(week=week, grade=5, status='DRAFT - for review', pages=[])
    weekfl = set(); barall = set()
    for p in pages:
        if not os.path.exists(p): continue
        m = re.match(r'lesson-(\d+-\w+)', p)
        lid = m.group(1).replace('-', '.') if m else f'{week}.checkin'
        pg, un = tag_page(p, lid, week, W)
        manifest['pages'].append(pg)
        weekfl |= set(pg['lesson_tags']['FL']); barall |= set(pg['standards_bar'])
        print(f'{p}: {len(pg["blocks"])} blocks' + (f'  UNTAGGED: {un}' if un else ''))
    print(f'  week {week}: bar codes never tagged: {sorted(barall - weekfl)}  tagged but not on bar: {sorted(weekfl - barall)}')
    os.makedirs('standards', exist_ok=True)
    json.dump(manifest, open(f'standards/g5-week-{week}.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
