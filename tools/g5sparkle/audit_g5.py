#!/usr/bin/env python3
"""G5 ELA static audit (Nov 25 2026, Bethany: "audit all lessons ... bugs, confusing sequences, template drift, scope drift, standards
on every activity"). Weeks 17-32 by default. Reads pages only; writes planning docs/_pv/audit/static.json and prints a summary.
    python tools/g5sparkle/audit_g5.py [first_week last_week]
Checks per page: structure (div balance, every activity inside a tab panel, one Next per tab), onclick functions defined, duplicate ids,
layer + DATA present, standards (data-std on every activity / check-in question, oao-standards JSON, manifest file and count),
visible-text lint (strand initials, partner language, download/upload, British spellings, the broken feather, Quick check, stale
week numbers), scope (bar codes vs v4 scope, Poetry Corner only on scope poetry days, WGRD / Read Like a Writer / Workshop present),
check-in totals. Titles must be unique across the course."""
import io, re, os, sys, json, glob, html
from html.parser import HTMLParser
W0, W1 = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (17, 32)
SCOPE = os.path.expanduser('~/mnt/ELA OAO/5th_grade_ela_scope_sequence_v4_2026-11-10.xlsx')
VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr', 'area', 'col', 'embed', 'param', 'track'}
BRIT = r'\b(colour\w*|favourite\w*|behaviour\w*|organis\w+|realis(?:e|ed|es|ing|ation)\b|recognis\w+|memoris\w+|synthesis(?:e|ed|ing)\b|summaris\w+|analys(?:e|ed|ing)\b|centre\w*|theatre\w*|travell\w+|practise[ds]?|grey|honour\w*|labour\w*|neighbour\w*|humour\w*|valour|apologis\w+|criticis\w+|emphasis(?:e|ed|ing)\b|programme)'
LINT = [('strand initials', r'\b(RWM|SWYK|WGRD|DOL)\b'), ('partner/class talk', r'(?i)\b(talk with a partner|with a partner|your partner|classmate|peer review|turn and talk|with your group|share with the class|your class)\b'),
        ('download/upload', r'(?i)\b(upload|download)'), ('british', BRIT), ('quick check', r'(?i)quick check'),
        ('generic teacher note', r'pay close attention to the characters'), ('placeholder', r'(?i)\b(lorem|TODO|TBD|\[insert|xxx)\b')]
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack = []; s.acts = []; s.ids = {}; s.text = []; s.skip = 0; s.cur = None
    def handle_starttag(s, t, a):
        d = dict(a)
        if t in ('script', 'style'): s.skip += 1
        if d.get('id'): s.ids[d['id']] = s.ids.get(d['id'], 0) + 1
        if t in VOID: return
        cls = (d.get('class') or '').split()
        if t == 'div' and 'activity' in cls:
            tabs = [x[1] for x in s.stack if x[1] and x[1].startswith('tab-')]
            s.acts.append({'tab': tabs[-1] if tabs else None, 'std': 'data-std' in d, 'title': '', 'nested': any('activity' in (x[2] or '').split() for x in s.stack)})
            s.cur = s.acts[-1]
        if t == 'div' and 'activity-title' in cls: s.grab = True
        s.stack.append((t, d.get('id'), d.get('class')))
    def handle_endtag(s, t):
        if t in ('script', 'style'): s.skip = max(0, s.skip - 1)
        if t in VOID: return
        while s.stack:
            x = s.stack.pop()
            if x[0] == t: break
    def handle_data(s, d):
        if s.skip: return
        s.text.append(d)
        if getattr(s, 'grab', False) and d.strip():
            if s.cur is not None and not s.cur['title']: s.cur['title'] = d.strip()[:60]
            s.grab = False
def scope_rows():
    try:
        import openpyxl
        ws = openpyxl.load_workbook(SCOPE, read_only=True, data_only=True).worksheets[0]
        out = {}
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r[0] and r[2] and str(r[2]).startswith('Day'):
                out[(int(r[0]), int(str(r[2])[-1]))] = {'codes': set(re.findall(r'ELA\.[\w]+\.[A-Z]+\.\d\.\d', r[11] or '')), 'poetry': r[10] or '', 'skill': r[4] or '', 'morph': r[6] or ''}
        return out
    except Exception as e:
        print('scope not read:', e); return {}
SC = scope_rows()
LAYER_FN = {'g5Pick', 'g5Spot', 'g5Fill', 'g5Match', 'g5Sort', 'switchTab', 'markDone', 'autoSave', 'toggleCheck', 'copyToClipboard', 'downloadPDF', 'sel', 'ga', 'dropSortChip'}
def page_audit(f, week, kind, titles):
    raw = io.open(f, encoding='utf-8', newline='').read()
    R = {'file': f, 'week': week, 'kind': kind, 'issues': []}
    def add(cat, msg): R['issues'].append([cat, msg])
    t = re.search(r'<title>(.*?)</title>', raw, re.S); title = t.group(1).strip() if t else ''
    titles.setdefault(title, []).append(f)
    bal = raw.count('<div') - raw.count('</div')
    if bal: add('bug', 'div balance %+d' % bal)
    p = P(); p.feed(raw)
    for k, n in p.ids.items():
        if n > 1 and not k.startswith('dot-'): add('bug', 'duplicate id #%s x%d' % (k, n))
    body = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', raw)
    defined = set(re.findall(r'function\s+(\w+)\s*\(', raw)) | set(re.findall(r'(?:window\.)?(\w+)\s*=\s*function', raw)) | LAYER_FN
    for fn in sorted(set(re.findall(r'on(?:click|input|change)="\s*(?:return\s+)?(\w+)\(', raw))):
        if fn not in defined and fn not in ('this', 'event', 'document', 'window', 'if', 'alert'): add('bug', 'onclick calls %s(), not defined on the page' % fn)
    text = re.sub(r'\s+', ' ', html.unescape(' '.join(p.text)))
    text = re.sub(r'(?i)download as pdf|download all my work|copy, or download|(?:📄|📥) download', ' ', text)
    text = re.sub(r'(?i)\bpartners?\b|\bpartnership\b', ' ', text)   # the novels' own word (Jack and Praiseworthy)
    if '\U0001FAD6' in raw or '&#129814;' in raw: add('bug', 'broken feather character &#129814;')
    if re.search(r'<body[^>]*>\s*(?:<[^>]+>\s*)*[^<{]*\.[\w-]+\{[^}]*\}', raw[:raw.find('<body') + 4000] if '<body' in raw else ''): add('bug', 'CSS printed as text after <body>')
    for cat, rx in LINT:
        hits = sorted(set(m.group(0) for m in re.finditer(rx, text)))
        if hits: add('wording', '%s: %s' % (cat, ', '.join(hits[:6])))
    if kind == 'lesson':
        tabs = re.findall(r'<div class="tab-panel[^"]*" id="(tab-\w+)"', raw)
        if len(tabs) != 4: add('bug', 'tab panels: %s' % tabs)
        out = [a['title'] for a in p.acts if not a['tab'] and not a['nested']]
        if out: add('bug', 'activities outside every tab: %s' % out)
        nexts = len(re.findall(r'class="tab-next-btn"', raw))
        if nexts < 3: add('bug', 'only %d tab Next buttons' % nexts)
        if 'g5-sparkle.js' not in raw: add('drift', 'no sparkle layer')
        if 'id="oao-data"' not in raw: add('drift', 'no DATA block')
        miss = [a['title'] for a in p.acts if not a['std'] and not a['nested']]
        if 'id="oao-standards"' not in raw: add('standards', 'no oao-standards block')
        elif miss: add('standards', 'activities without data-std: %s' % miss)
        tl = ' | '.join(a['title'] for a in p.acts).lower()
        d = int(re.search(r'lesson-\d+-(\d)', f).group(1))
        sc = SC.get((week, d))
        if 'what good readers do' not in raw.lower(): add('drift', 'no What Good Readers Do')
        if 'rwm-box' not in raw and week >= 19: add('drift', 'no Read Like a Writer box')
        if not re.search(r"writer.s workshop|comparison project|letter packet|year-end portfolio|writing workshop|writing connection", tl + raw.lower()[:0]): add('drift', 'no Writer\'s Workshop activity')
        if sc:
            bm = re.search(r'class="standards-codes">(.*?)</div>', raw, re.S)
            bar = set(re.findall(r'ELA\.[\w]+\.[A-Z]+\.\d\.\d', bm.group(1))) if bm else set()
            if sc['codes'] and bar and not sc['codes'] <= bar: add('scope', 'bar lacks scope codes %s' % sorted(sc['codes'] - bar))
            poem_day = not re.match(r'\s*[—-]', sc['poetry'] or '-') and bool((sc['poetry'] or '').strip())
            has_poem = 'poetry corner' in tl
            if poem_day and not has_poem: add('scope', 'scope has Poetry Corner today, page does not')
            if has_poem and not poem_day: add('scope', 'page has Poetry Corner on a non-poetry day')
            roots = [r for r in re.findall(r'\b([a-z]{2,6}(?:/[a-z]{2,6})?)\b', sc['morph'].split('—')[0]) if r not in ('roots', 'root', 'and', 'the', 'swyk', 'define', 'suffixes', 'word', 'review', 'unit', 'year', 'long', 'final', 'reflection', 'application', 'parts', 'launch', 'families')]
            if roots and sc['morph'].lower().startswith('root'):
                lowr = raw.lower()
                gone = [r for r in roots if not any(x in lowr for x in r.split('/'))]
                if gone: add('scope', 'scope roots not on page: %s' % gone)
    elif kind == 'checkin':
        qs = len(re.findall(r'<div class="question"', raw)); qstd = len(re.findall(r'<div class="question" data-std=', raw))
        pts = sum(int(x) for x in re.findall(r'<span class="pts">(\d+) pt', raw))
        if qs != 14 or pts != 14: add('bug', 'check-in has %d questions, %d points' % (qs, pts))
        if 'id="oao-standards"' not in raw: add('standards', 'no oao-standards block')
        elif qstd != qs: add('standards', '%d of %d questions tagged' % (qstd, qs))
        if 'function ga(' not in raw: add('bug', 'no ga() gather function')
        three = sum(1 for ul in re.findall(r'<ul class="options"[^>]*>(.*?)</ul>', raw, re.S) if len(re.findall(r'<li\b', ul)) < 4)
        if three: add('drift', '%d multiple-choice items with only 3 options' % three)
        qz = glob.glob('planning docs/Week%d_CheckIn*QTI.zip' % week)
        if not qz: add('drift', 'no Week%d QTI zip' % week)
    elif kind == 'fluency':
        if 'g5-sparkle.js' not in raw: add('drift', 'no sparkle layer')
        if not re.search(r'class="(fluency-)?passage', raw): add('bug', 'no passage block')
        if 'id="oao-standards"' not in raw: add('standards', 'no oao-standards block')
    if kind in ('lesson', 'checkin', 'fluency') and not os.path.exists('standards/g5-week-%d.json' % week): add('standards', 'no standards/g5-week-%d.json manifest' % week)
    return R
res, titles = [], {}
for w in range(W0, W1 + 1):
    for f in sorted(glob.glob('lesson-%d-*.html' % w)):
        kind = 'checkin' if f.endswith('-checkin.html') else 'fluency' if re.search(r'-fluency\.html$', f) else 'project' if 'project' in f or 'portfolio.html' in f else 'lesson'
        if kind == 'project': continue
        res.append(page_audit(f, w, kind, titles))
for t, fs in titles.items():
    if len(fs) > 1:
        for r in res:
            if r['file'] in fs: r['issues'].append(['bug', 'duplicate <title> with %s' % [x for x in fs if x != r['file']]])
os.makedirs('planning docs/_pv/audit', exist_ok=True)
json.dump(res, open('planning docs/_pv/audit/static.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(cat for r in res for cat, _ in r['issues'])
print('pages', len(res), dict(c))
for r in res:
    for cat, m in r['issues']: print('%2d %-38s %-9s %s' % (r['week'], r['file'][:38], cat, m[:150]))
