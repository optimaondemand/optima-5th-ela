#!/usr/bin/env python3
"""Extract slide data from OAO 5th grade ELA lesson HTML (Bowditch dialect).
usage: python3 extract_g5.py <html_dir> <out.json> file1.html file2.html ...
Every string comes from the HTML. Nothing is invented here.
"""
import re, sys, json, html as H
from bs4 import BeautifulSoup, NavigableString

def T(el):
    if el is None: return ''
    if isinstance(el, str): s = el
    else: s = el.get_text(' ', strip=False)
    s = H.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.;:!?’”)])', r'\1', s)
    s = re.sub(r'([“(‘])\s+', r'\1', s)
    return s

def js_arg(onclick):
    """first single-quoted JS string argument of an onclick handler"""
    if not onclick: return ''
    m = re.search(r"\(\s*this\s*,\s*'((?:\\.|[^'\\])*)'", onclick)
    if not m: return ''
    s = m.group(1).replace("\\'", "'").replace('\\"', '"')
    return T(BeautifulSoup(s, 'html.parser'))

def strip_svg(soup):
    for s in soup.find_all(['svg', 'script', 'style', 'textarea', 'button']): s.decompose()

def tab(soup, name):
    return soup.find(id='tab-' + name)

def activities(root):
    return root.find_all('div', class_='activity', recursive=True) if root else []

def act_title(a):
    t = a.find(class_='activity-title'); return T(t)

def act_sub(a):
    t = a.find(class_='activity-sub'); return T(t)

def body_texts(el):
    """paragraph-level text blocks inside el, skipping interactive widgets"""
    out = []
    if el is None: return out
    skip = {'match-game', 'sort-bank', 'sort-columns', 'spotter-game', 'swyk', 'fillin-item', 'flip-card',
            'fc-grid', 'rwm-block', 'journal-label', 'textbox-prompt', 'match-feedback', 'sort-score', 'dol-answer',
            'choice-game', 'root-match-game', 'fillin-game', 'odd-group', 'root-det-group', 'wins-group',
            'vocab-choice-grid', 'swyk-section', 'choice-item', 'g5-fb', 'fillin-feedback', 'dol-fix-sentence', 'spotter-result',
            'odd-msg', 'root-det-msg', 'wins-msg', 'choice-score'}
    for node in el.find_all(['p', 'li', 'div'], recursive=True):
        cls = set(node.get('class') or [])
        if cls & skip: continue
        if any(set(p.get('class') or []) & skip for p in node.parents if p is not el and hasattr(p, 'get')):
            continue
        if node.name == 'div':
            # only leaf-ish divs with direct text
            direct = ''.join(t for t in node.find_all(string=True, recursive=False)).strip()
            if not direct or node.find(['p', 'li', 'div']): continue
        if node.name == 'p' and node.find_parent('li'): continue
        t = T(node)
        if t and len(t) > 2: out.append(t)
    # de-dup consecutive
    res = []
    for t in out:
        if not res or res[-1] != t: res.append(t)
    return res

def match_pairs(game):
    words, defs = {}, {}
    for it in game.find_all(class_=['match-item', 'root-match-item']):
        k = it.get('data-match');
        if 'is-word' in it.get('class', []): words[k] = T(it)
        else: defs[k] = T(it)
    return [[words[k], defs.get(k, '')] for k in words]

def sort_data(act):
    chips = act.find_all(class_='sort-chip')
    heads = [T(h) for h in act.find_all(class_='sort-col-header')]
    cols = []
    for c in act.find_all(class_='sort-col'):
        k = c.get('data-col')
        dd = c.find(class_='sort-col-drop')
        if not k and dd is not None: k = dd.get('data-col')
        if not k:
            d = c.find(onclick=re.compile(r"dropChip"))
            mm = re.search(r"dropChip\(this,\s*'([^']+)'", d['onclick']) if d else None
            k = mm.group(1) if mm else None
        cols.append(k)
    groups = []
    for c in chips:
        g = c.get('data-group')
        if g not in groups: groups.append(g)
    def header_for(g, idx):
        if cols and g in cols and cols.index(g) < len(heads): return heads[cols.index(g)]
        raise ValueError('sort column key not found for group %r (cols=%r)' % (g, cols))
    out = []
    for i, g in enumerate(groups):
        out.append({'header': header_for(g, i), 'words': [T(c) for c in chips if c.get('data-group') == g]})
    return {'columns': out, 'bank': [T(c) for c in chips]}

def spotters(game):
    qs = []
    for s in game.find_all(class_='spotter-sentence'):
        prompt = ' '.join(T(x) for x in s.find_all('span', recursive=False) if 'spotter-word' not in (x.get('class') or []) and T(x))
        opts = []
        for w in s.find_all(class_='spotter-word'):
            opts.append({'text': T(w), 'correct': w.get('data-correct') == 'true', 'why': js_arg(w.get('onclick'))})
        # if no explicit prompt and the options are words in a sentence, keep sentence order
        qs.append({'prompt': prompt, 'options': opts,
                   'inline': len(opts) > 2 and not prompt})
    return qs

def fillins(act):
    out = []
    items = act.find_all(class_='fillin-item')
    if not items:
        items = [i.parent for i in act.find_all('input', class_='fillin-input')]
    for f in items:
        inp = f.find('input')
        ans = inp.get('data-answer', '') if inp else ''
        parts = []
        for ch in f.children:
            if getattr(ch, 'name', None) == 'input': parts.append('⟦' + ans + '⟧')
            else: parts.append(T(ch) if not isinstance(ch, NavigableString) else H.unescape(str(ch)))
        txt = re.sub(r'\s+', ' ', ''.join(parts)).strip()
        # morphology style: stem + answer directly attached
        out.append({'text': txt, 'answer': ans})
    return out

def cards(act):
    out = []
    for c in act.find_all(class_=re.compile(r'^(flip-card|fc-card)$')) or []:
        w = c.find(class_=re.compile('fc-word'))
        d = c.find(class_=re.compile('fc-def'))
        ex = c.find(class_=re.compile('fc-(ex|sentence|example|context)'))
        if w: out.append({'word': T(w), 'def': T(d), 'ex': T(ex)})
    if not out:
        ws = act.find_all(class_='fc-word'); ds = act.find_all(class_='fc-def')
        for i, w in enumerate(ws):
            out.append({'word': T(w), 'def': T(ds[i]) if i < len(ds) else '', 'ex': ''})
    # de-dup by word (front/back both carry fc-word)
    seen, res = set(), []
    for c in out:
        if c['word'] in seen: continue
        seen.add(c['word']); res.append(c)
    return res

def choices(body):
    groups = []
    seen = set()
    for b in body.find_all('button', onclick=re.compile(r',\s*(true|false)\s*\)')):
        row = b.parent
        grp = row.parent if row is not None else None
        if grp is None or id(grp) in seen: continue
        seen.add(id(grp))
        opts = []
        for bb in grp.find_all('button', onclick=re.compile(r',\s*(true|false)\s*\)')):
            opts.append({'text': T(bb), 'correct': bool(re.search(r',\s*true\s*\)', bb['onclick']))})
        # prompt = group text minus buttons and messages
        import copy
        g2 = copy.copy(grp)
        g2 = BeautifulSoup(str(grp), 'html.parser')
        for x in g2.find_all('button'): x.decompose()
        for x in g2.find_all(class_=re.compile(r'(msg|score|feedback|g5-fb)$')): x.decompose()
        prompt = T(g2)
        groups.append({'prompt': prompt, 'options': opts})
    return groups

def swyk(act):
    s = act.find(class_=['swyk', 'swyk-section'])
    if not s: return None
    return {'label': T(s.find(class_='swyk-label')), 'prompt': T(s.find(class_='swyk-prompt')),
            'task': T(s.find(class_='textbox-prompt'))}

def word_activity(a):
    d = {'title': act_title(a), 'sub': act_sub(a)}
    body = a.find(class_='activity-body') or a
    d['text'] = body_texts(body)
    mg = body.find(class_=['match-game', 'root-match-game'])
    if mg: d['match'] = match_pairs(mg)
    if body.find(class_='sort-chip'): d['sort'] = sort_data(body)
    sg = body.find_all(class_='spotter-game')
    if sg: d['spot'] = [q for g in sg for q in spotters(g)]
    if body.find('input', class_='fillin-input'): d['fill'] = fillins(body)
    wb = body.find(string=re.compile('Word bank'))
    if wb: d['bank'] = T(wb.find_parent('p'))
    ch = choices(body)
    if ch: d['choice'] = ch
    vc = body.find_all(class_='vocab-choice-card')
    if vc: d['menu'] = [[T(c.find(class_='vocab-choice-title')), T(c.find(class_='vocab-choice-desc'))] for c in vc]
    tk = body.find_all(class_='g5-task')
    if tk: d['tasks'] = [T(t) for t in tk]
    cs = cards(body)
    if cs: d['cards'] = cs
    sw = swyk(body)
    if sw: d['swyk'] = sw
    return d

def extract(path):
    raw = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(raw, 'html.parser')
    # keep onclick strings before stripping buttons
    L = {'file': path.split('/')[-1]}
    m = re.search(r'lesson-(\d+)-(\d+)-cmb-ch(\d+)', L['file'])
    L['week'], L['day'], L['chapter'] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    # DOL (before strip, uses onclick on spans)
    dm = soup.find(class_=['dol-model-sentence', 'dol-sentence'])
    L['dol'] = {}
    if dm:
        L['dol']['model'] = T(dm)
        L['dol']['notes'] = [[T(w), js_arg(w.get('onclick'))] for w in dm.find_all(class_='dol-highlight-word')]
    wt_ = soup.find(id='tab-warmup') or soup
    df = wt_.find(class_=['dol-fix-sentence', 'dol-fixbox-sentence'])
    if df: L['dol']['fix'] = T(df)
    da = wt_.find(class_=['dol-answer', 'dol-reveal'])
    if da and 'dol-reveal' in da.get('class', []):
        t = T(da); t = re.sub(r'^Corrected sentence:\s*', '', t)
        m2 = re.match(r'“([^”]+)”\s*(.*)$', t)
        L['dol']['answer'] = m2.group(1) if m2 else t
        L['dol']['fixes'] = m2.group(2) if m2 else ''
        if not m2:
            cm = re.search(r'((?:What needed fixing|This is a different sentence|Compare with the model).*)$', t)
            if cm: L['dol']['answer'] = t[:cm.start()].strip(); L['dol']['fixes'] = cm.group(1)
        da = None
    if da:
        ps = [T(p) for p in da.find_all('p')] or [T(da)]
        ans = ' '.join(p for p in ps if p and p != 'Corrected:')
        ans = re.sub(r'^Corrected:\s*', '', ans)
        fx = re.search(r'((?:[A-Z][a-z]+ )?[Ff]ixes?:.*)$', ans)
        L['dol']['fixes'] = fx.group(1) if fx else ''
        L['dol']['answer'] = ans[:fx.start()].strip() if fx else ans
        # "Compare with the model" style notes
        cm = re.search(r'((?:Compare with the model|What needed fixing|This is a different sentence).*)$', L['dol']['answer'])
        if cm:
            L['dol']['fixes'] = cm.group(1); L['dol']['answer'] = L['dol']['answer'][:cm.start()].strip()
    # spotter "why" also lives in onclick — collect spotter data before strip
    wtab = tab(soup, 'words')
    word_acts = []
    if wtab:
        for a in wtab.find_all('div', class_='activity'):
            if a.find_parent('div', class_='activity'): continue
            word_acts.append(word_activity(a))
        rb = wtab.find(class_='rwm-block')
        if rb:
            L['rwm'] = {'sentence': T(rb.find(class_='rwm-sentence')),
                        'steps': [[T(st.find(class_='rwm-step-label')), T(st.find(class_='rwm-step-text')),
                                   T(st.find(class_='textbox-prompt'))] for st in rb.find_all(class_='rwm-step')],
                        'frame': T(rb.find(class_='rwm-frame'))}
    L['words'] = word_acts
    strip_svg(soup)
    hdr = soup.find(class_='header-title')
    L['header_title'] = T(hdr)
    qs = soup.find(class_='quote-strip')
    if qs: L['quote'] = {'text': T(qs.find(class_='quote-strip-text')), 'attr': T(qs.find(class_='quote-strip-attr'))}
    cards_ = soup.find_all(class_='intro-card')
    L['intro'] = []
    for c in cards_:
        L['intro'].append({'label': T(c.find(class_='intro-card-head-label')), 'title': T(c.find(class_='intro-card-head-title')),
                           'body': [T(p) for p in (c.find(class_='intro-card-body') or c).find_all('p')],
                           'objectives': [T(o) for o in c.find_all(class_='obj-line')]})
    # chapter title
    ct = ''
    for c in L['intro']:
        mm = re.match(r'Chapter \d+[:\s—–-]+(.+)', c['title'])
        if mm: ct = mm.group(1).strip()
    tl = soup.find(class_='tracker-chapter-label')
    L['tracker'] = T(tl)
    if not ct:
        mm = re.search(r'Chapter \d+\s*[—–-]\s*(.+)$', L['tracker'])
        if mm: ct = mm.group(1).strip()
    L['chapter_title'] = ct.strip('“”"')
    # WGRD — activity titled What Good Readers Do OR wgrd-block, anywhere
    w = None
    for a in soup.find_all('div', class_='activity'):
        if 'What Good Readers Do' in act_title(a): w = a; break
    if w:
        body = w.find(class_='activity-body') or w
        kc = body.find(class_='key-concept')
        steps = [T(li) for li in kc.find_all('li')] if kc else []
        paras = [T(p) for p in body.find_all('p', recursive=True) if not p.find_parent(class_='key-concept') and not p.find_parent(class_='socratic-box')]
        soc = [T(x) for x in body.find_all(class_='socratic-q')] + [T(li) for sb in body.find_all(class_='socratic-box') for li in sb.find_all('li')]
        L['wgrd'] = {'strategy': act_sub(w), 'body': paras, 'steps': steps, 'watch': soc}
    else:
        wb = soup.find(class_='wgrd-block')
        if wb:
            kc = wb.find(class_='key-concept')
            L['wgrd'] = {'strategy': T(wb.find(class_='wgrd-strategy')), 'body': [T(wb.find(class_='wgrd-body'))],
                         'steps': [T(li) for li in kc.find_all('li')] if kc else [], 'watch': []}
    # Poetry
    pb = soup.find(class_='poetry-block')
    if pb:
        lines = pb.find(class_='poetry-lines')
        ltxt = H.unescape(re.sub(r'<br\s*/?>', '\n', str(lines))) if lines else ''
        ltxt = re.sub(r'<[^>]+>', '', ltxt)
        lines_ = [re.sub(r'\s+', ' ', l).strip() for l in ltxt.split('\n')]
        # keep stanza breaks as ''
        out = []
        for l in lines_:
            if l or (out and out[-1] != ''): out.append(l)
        while out and out[-1] == '': out.pop()
        q = []
        par = pb.find_parent('div', class_='activity') or pb.parent
        for x in par.find_all(class_=['socratic-q', 'callout']):
            t = T(x)
            if t and t not in q: q.append(t)
        intro = []
        body = par.find(class_='activity-body') or par
        for p in body.find_all('p', recursive=False): intro.append(T(p))
        L['poem'] = {'heading': act_title(par) if par.find(class_='activity-title') else 'Poetry Corner',
                     'title': T(pb.find(class_='poetry-title')), 'author': T(pb.find(class_='poetry-author')),
                     'lines': out, 'questions': q, 'intro': intro}
    # Reading
    rt = tab(soup, 'reading')
    R = {'pauses': [], 'summary': '', 'title': ''}
    if rt:
        for a in rt.find_all('div', class_='activity'):
            if act_title(a).startswith('Read'):
                R['title'] = act_title(a); R['sub'] = act_sub(a)
                R['intro'] = [T(p) for p in a.find_all('p') if not p.find_parent(class_='socratic-box') and not p.find_parent(class_='pause-columns')][:3]
        bp = rt.find_all(class_='book-page-body')
        if bp: R['summary'] = T(bp[0])
        bt = rt.find(class_='book-page-title')
        if bt and not R['title']: R['title'] = 'Read: Chapter %d — %s' % (L['chapter'], T(bt))
        for sb in rt.find_all(class_='socratic-box'):
            lab = T(sb.find(class_='socratic-label')); q = ' '.join(T(x) for x in sb.find_all(class_='socratic-q'))
            if 'Pause' in lab or sb.find_parent(class_='pause-columns'):
                R['pauses'].append([lab, q])
        for pt in rt.find_all(class_='pause-card'):
            R['pauses'].append([T(pt.find(class_='pause-label')), T(pt.find(class_='pause-q'))])
        for pt in rt.find_all(class_='pause-think'):
            R['pauses'].append([T(pt.find(class_='pause-think-label')), T(pt.find(class_='pause-think-q'))])
    L['reading'] = R
    # Assignment
    at = tab(soup, 'assignment')
    A = {'partA': [], 'workshop': None}
    if at:
        for a in at.find_all('div', class_='activity'):
            if a.find_parent('div', class_='activity'): continue
            t = act_title(a)
            if t.startswith('Part A'):
                qs_ = [T(q) for q in a.find_all(class_='q-text')]
                if not qs_:
                    qs_ = [T(q) for q in a.find_all(class_='textbox-prompt') if re.match(r'\s*Q\d', T(q))]
                A['partA'] = [re.sub(r'^(Q?\d+\.?)\s*', '', q) for q in qs_]
                A['partA_title'] = t
            elif 'Workshop' in t or 'Writing Connection' in t:
                body = a.find(class_='activity-body') or a
                secs = []
                for c in body.find_all(['div'], class_=['callout', 'key-concept']):
                    if c.find_parent(class_='key-concept') and 'key-concept' not in c.get('class', []): pass
                    lab = c.find(class_='key-concept-label')
                    label = T(lab) if lab else ''
                    if lab: lab.extract()
                    txt = T(c)
                    secs.append([label, txt])
                stage = ''
                for sp in body.find_all('span'):
                    if '★' in T(sp): stage = T(sp).replace('★', '').strip(); break
                A['workshop'] = {'title': t, 'sub': act_sub(a), 'stage': stage, 'sections': secs}
    L['assign'] = A
    return L

if __name__ == '__main__':
    d, out = sys.argv[1], sys.argv[2]
    data = [extract(d.rstrip('/') + '/' + f) for f in sys.argv[3:]]
    data.sort(key=lambda x: (x['week'], x['day']))
    json.dump(data, open(out, 'w'), indent=1, ensure_ascii=False)
    print('lessons', len(data))
