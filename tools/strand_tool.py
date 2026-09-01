# -*- coding: utf-8 -*-
"""Locate and rewrite strand sections in OAO 5th grade ELA lesson HTML."""
import io, re

DIV_RE = re.compile(r'<div\b[^>]*>|</div>', re.I)

def block_span(s, open_idx):
    """Given index of a '<div' opening tag, return (start, end) of the balanced block."""
    depth = 0
    for m in DIV_RE.finditer(s, open_idx):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (open_idx, m.end())
        else:
            depth += 1
    raise ValueError("unbalanced div from %d" % open_idx)

def find_activity(s, key):
    """Return (start,end) of the <div class="activity ..."> block whose
    activity-title contains `key`."""
    for m in re.finditer(r'<div class="activity-title">(.*?)</div>', s, re.S):
        if key.lower() in m.group(1).lower():
            # walk backwards to the enclosing <div class="activity
            j = s.rfind('<div class="activity ', 0, m.start())
            if j == -1:
                j = s.rfind('<div class="activity"', 0, m.start())
            if j == -1:
                continue
            return block_span(s, j)
    raise KeyError("no activity titled ~%r" % key)

def get_activity(s, key):
    a, b = find_activity(s, key)
    return s[a:b]

def body_span(block):
    j = block.find('<div class="activity-body">')
    if j == -1:
        raise KeyError("no activity-body")
    a, b = block_span(block, j)
    inner_start = a + len('<div class="activity-body">')
    inner_end = b - len('</div>')
    return inner_start, inner_end

def rewrite(s, key, title=None, sub=None, body=None):
    a, b = find_activity(s, key)
    blk = s[a:b]
    if title is not None:
        blk = re.sub(r'(<div class="activity-title">).*?(</div>)',
                     lambda m: m.group(1) + title + m.group(2), blk, count=1, flags=re.S)
    if sub is not None:
        blk = re.sub(r'(<div class="activity-sub">).*?(</div>)',
                     lambda m: m.group(1) + sub + m.group(2), blk, count=1, flags=re.S)
    if body is not None:
        i, j = body_span(blk)
        blk = blk[:i] + body + blk[j:]
    return s[:a] + blk + s[b:]

def swyk_of(block):
    """Return the existing <div class="swyk"> ... </div> markup, or None."""
    m = re.search(r'<div class="swyk(?:-section)?"[^>]*>', block)
    if not m:
        return None
    j = m.start()
    a, b = block_span(block, j)
    return block[a:b]

def make_swyk(label, prompt, textbox_prompt, tid, data_label, placeholder):
    return ('<div class="swyk">\n'
            '        <div class="swyk-label">&#x1FAB6; Show What You Know &middot; %s</div>\n'
            '        <div class="swyk-prompt">%s</div>\n'
            '        <div class="textbox-prompt">%s</div>\n'
            '        <textarea class="journal-box" id="%s" data-label="%s"\n'
            '          placeholder="%s"\n'
            '          oninput="autoSave(this,\'dot-%s\');gatherAnswers();"></textarea>\n'
            '        <div class="journal-label">&#x1F4D3; <span class="saved-dot" id="dot-%s"></span></div>\n'
            '      </div>') % (label, prompt, textbox_prompt, tid, data_label, placeholder,
                              tid.replace('journal-',''), tid.replace('journal-',''))

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8').write(s)

def check(s, path=''):
    """Structural sanity checks. Returns list of problems."""
    probs = []
    o = len(re.findall(r'<div\b', s)); c = len(re.findall(r'</div>', s))
    if o != c:
        probs.append('div imbalance %d open / %d close' % (o, c))
    for m in re.finditer(r'<div class="spotter-sentence" id="([^"]+)">', s):
        a, b = block_span(s, m.start())
        seg = s[a:b]
        t = seg.count('data-correct="true"')
        if seg.count('data-correct=') and t != 1:
            probs.append('%s has %d correct answers' % (m.group(1), t))
    for m in re.finditer(r'data-answer="([^"]+)"[^>]*maxlength="(\d+)"', s):
        if len(m.group(1)) > int(m.group(2)):
            probs.append('answer %r longer than maxlength %s' % (m.group(1), m.group(2)))
    for m in re.finditer(r'maxlength="(\d+)"[^>]*data-answer="([^"]+)"', s):
        if len(m.group(2)) > int(m.group(1)):
            probs.append('answer %r longer than maxlength %s' % (m.group(2), m.group(1)))
    for gm in re.finditer(r'<div class="root-match-grid"', s):
        a, b = block_span(s, gm.start())
        pairs = {}
        for m in re.finditer(r'class="root-match-item( is-word)?" data-match="([A-Z])"', s[a:b]):
            pairs.setdefault(m.group(2), []).append(bool(m.group(1)))
        for k, v in pairs.items():
            if not any(v) or all(v):
                probs.append('root-match group %s malformed: %r' % (k, v))
    for gm in re.finditer(r'<div class="sort-game"', s):
        a, b = block_span(s, gm.start())
        seg = s[a:b]
        groups = set(re.findall(r'data-group="([^"]+)"', seg))
        cols = set(re.findall(r'data-col="([^"]+)"', seg))
        if groups - cols:
            probs.append('sort chips with no column: %r' % sorted(groups - cols))
    return probs


# ── in-place content setters (keep scaffolding + JS hooks, swap the content) ──

def _sub_first(block, pattern, repl, flags=re.S):
    new, n = re.subn(pattern, repl, block, count=1, flags=flags)
    if n == 0:
        raise KeyError("pattern not found: %.60r" % pattern)
    return new

def set_lead_para(block, html):
    """Replace the first <p>...</p> inside activity-body."""
    i, j = body_span(block)
    inner = block[i:j]
    inner = _sub_first(inner, r'<p(?:\s[^>]*)?>.*?</p>', lambda m: '<p>%s</p>' % html)
    return block[:i] + inner + block[j:]

def set_key_concept(block, label, lines):
    """lines: list of html strings, each wrapped in <p>."""
    j = block.find('<div class="key-concept"')
    if j == -1:
        raise KeyError('no key-concept')
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    body = ('\n        <div class="key-concept-label">%s</div>\n' % label +
            ''.join('        <p>%s</p>\n' % l for l in lines) + '      ')
    return block[:a] + open_tag + body + '</div>' + block[b:]

def set_rule_callout(block, html):
    """Replace the <p> inside the first callout-gold 'The Rule' box."""
    j = block.find('callout callout-gold')
    if j == -1:
        raise KeyError('no rule callout')
    j = block.rfind('<div', 0, j)
    a, b = block_span(block, j)
    seg = _sub_first(block[a:b], r'(<p[^>]*>).*?(</p>)',
                     lambda m: m.group(1) + html + m.group(2))
    return block[:a] + seg + block[b:]

def _grid(block, cls, inner):
    j = block.find('<div class="%s"' % cls)
    if j == -1:
        raise KeyError('no %s' % cls)
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    return block[:a] + open_tag + '\n' + inner + '        </div>' + block[b:]

def set_rootmatch(block, pairs):
    """pairs: [(word, meaning)] -> interleaved A,B,C,D items."""
    letters = 'ABCDEFGH'
    items = []
    for n, (w, mean) in enumerate(pairs):
        L = letters[n]
        items.append('          <div class="root-match-item is-word" data-match="%s" onclick="rootMatchClick(this)">%s</div>\n' % (L, w))
    metas = []
    for n, (w, mean) in enumerate(pairs):
        L = letters[n]
        metas.append('          <div class="root-match-item" data-match="%s" onclick="rootMatchClick(this)">%s</div>\n' % (L, mean))
    out = []
    for n in range(len(pairs)):
        out.append(items[n]); out.append(metas[(n + 1) % len(pairs)])
    return _grid(block, 'root-match-grid', ''.join(out))

def set_fillin(block, items, feedback=None):
    """items: [(before_html, answer, after_html)]"""
    j = block.find('<div class="fillin-game"')
    if j == -1:
        raise KeyError('no fillin-game')
    a, b = block_span(block, j)
    seg = block[a:b]
    btn = re.search(r'<button class="fillin-check-btn".*?</button>', seg, re.S).group(0)
    fb = re.search(r'<div class="fillin-feedback".*?</div>', seg, re.S).group(0)
    if feedback:
        fb = re.sub(r'(<div class="fillin-feedback"[^>]*>).*?(</div>)',
                    lambda m: m.group(1) + feedback + m.group(2), fb, flags=re.S)
    open_tag = seg[:seg.index('>') + 1]
    rows = ''.join(
        '        <div class="fillin-item">%s <input class="fillin-input" data-answer="%s" maxlength="%d" placeholder="______"> %s</div>\n'
        % (bef, ans, len(ans) + 2, aft) for bef, ans, aft in items)
    return block[:a] + open_tag + '\n' + rows + '        ' + btn + '\n        ' + fb + '\n      </div>' + block[b:]

def set_spotter(block, sentences):
    """sentences: [ {'lead': html or None, 'choices': [(text, is_correct, explain)]} ]"""
    j = block.find('<div class="spotter-game"')
    if j == -1:
        raise KeyError('no spotter-game')
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    out = []
    for n, sent in enumerate(sentences, 1):
        sid = 'spot%d' % n
        out.append('        <div class="spotter-sentence" id="%s">\n' % sid)
        if sent.get('lead'):
            out.append('          <span style="font-family:Georgia,serif;display:block;margin-bottom:8px;">%s</span>\n' % sent['lead'])
        for k, (txt, ok, expl) in enumerate(sent['choices']):
            if k:
                out.append('          <span style="display:block;height:6px;"></span>\n')
            out.append('          <span class="spotter-word" onclick="spotterPick(this,\'%s\')" data-correct="%s" data-explain="%s">%s</span>\n'
                       % (sid, 'true' if ok else 'false', expl.replace('"', '&quot;'), txt))
        out.append('          <div class="spotter-result" id="%s-result"></div>\n' % sid)
        out.append('        </div>\n')
    return block[:a] + open_tag + '\n' + ''.join(out) + '      </div>' + block[b:]

def set_sort(block, columns, hint=None):
    """columns: [(header_label, group_key, [words])]. Works with or without a
    .sort-game wrapper — falls back to rewriting .sort-bank and .sort-columns."""
    j = block.find('<div class="sort-game"')
    if j == -1:
        return _set_sort_loose(block, columns)
    a, b = block_span(block, j)
    seg = block[a:b]
    open_tag = seg[:seg.index('>') + 1]
    hdr_styles = re.findall(r'<div class="sort-col-header" style="([^"]*)">', seg)
    while len(hdr_styles) < len(columns):
        hdr_styles.append(hdr_styles[-1] if hdr_styles else 'background:#0E1C42;')
    chips = []
    for label, key, words in columns:
        for w in words:
            chips.append((key, w))
    chips.sort(key=lambda t: t[1].lower())
    bank = ''.join('          <span class="sort-chip" data-group="%s" onclick="pickSortChip(this)">%s</span>\n' % (k, w)
                   for k, w in chips)
    cols = ''.join(
        '          <div class="sort-col"><div class="sort-col-header" style="%s">%s</div>'
        '<div class="sort-col-drop" data-col="%s" onclick="dropSortChip(this,\'%s\')"></div></div>\n'
        % (hdr_styles[n], label, key, key) for n, (label, key, words) in enumerate(columns))
    score_id = (re.search(r'<div class="sort-score" id="([^"]+)">', seg) or [None, 'sortScore'])[1]
    inner = ('        <div class="sort-bank" id="sortBank">\n%s        </div>\n'
             '        <div class="sort-columns">\n%s        </div>\n'
             '        <div class="sort-score" id="%s"></div>\n' % (bank, cols, score_id))
    return block[:a] + open_tag + '\n' + inner + '      </div>' + block[b:]

def set_swyk(block, prompt=None, textbox_prompt=None, data_label=None, placeholder=None):
    m = re.search(r'<div class="swyk(?:-section)?"[^>]*>', block)
    if not m:
        raise KeyError('no swyk')
    j = m.start()
    a, b = block_span(block, j)
    seg = block[a:b]
    if prompt is not None:
        seg = _sub_first(seg, r'(<div class="swyk-prompt">).*?(</div>)', lambda m: m.group(1) + prompt + m.group(2))
    if textbox_prompt is not None:
        seg = _sub_first(seg, r'(<div class="textbox-prompt">).*?(</div>)', lambda m: m.group(1) + textbox_prompt + m.group(2))
    if data_label is not None:
        seg = _sub_first(seg, r'data-label="[^"]*"', 'data-label="%s"' % data_label, flags=0)
    if placeholder is not None:
        seg = _sub_first(seg, r'placeholder="[^"]*"', 'placeholder="%s"' % placeholder, flags=0)
    return block[:a] + seg + block[b:]

def set_callout(block, marker, html):
    """Replace the <p> of the callout whose current text contains `marker`."""
    for m in re.finditer(r'<div class="callout[^"]*"', block):
        a, b = block_span(block, m.start())
        if marker.lower() in re.sub(r'<[^>]+>', '', block[a:b]).lower():
            seg = _sub_first(block[a:b], r'(<p[^>]*>).*?(</p>)', lambda mm: mm.group(1) + html + mm.group(2))
            return block[:a] + seg + block[b:]
    raise KeyError('no callout containing %r' % marker)

def set_challenges(block, items):
    """items: [(word_display, hint, answer_html)] — challenge-item boxes."""
    spans = [block_span(block, m.start()) for m in re.finditer(r'<div class="challenge-item">', block)]
    if not spans:
        raise KeyError('no challenge-item')
    out = []
    for n, (word, hint, ans) in enumerate(items, 1):
        out.append('      <div class="challenge-item">\n'
                   '        <div class="challenge-word">%s</div>\n'
                   '        <div class="challenge-hint">%s</div>\n'
                   '        <button class="challenge-reveal-btn" onclick="document.getElementById(\'ch%d\').classList.toggle(\'show\')">&#x1F50D; Reveal</button>\n'
                   '        <div class="challenge-answer" id="ch%d">%s</div>\n'
                   '      </div>' % (word, hint, n, n, ans))
    return block[:spans[0][0]] + '\n'.join(out) + block[spans[-1][1]:]


def set_matchgrid(block, pairs):
    """Works with either the root-match-* or match-* class family."""
    if '<div class="root-match-grid"' in block:
        grid, item = 'root-match-grid', 'root-match-item'
    elif '<div class="match-grid"' in block:
        grid, item = 'match-grid', 'match-item'
    else:
        raise KeyError('no match grid')
    j = block.find('<div class="%s"' % grid)
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    letters = 'ABCDEFGH'
    words, metas = [], []
    for n, (w, mean) in enumerate(pairs):
        L = letters[n]
        words.append('          <div class="%s is-word" data-match="%s" onclick="rootMatchClick(this)">%s</div>\n' % (item, L, w))
        metas.append('          <div class="%s" data-match="%s" onclick="rootMatchClick(this)">%s</div>\n' % (item, L, mean))
    out = []
    for n in range(len(pairs)):
        out.append(words[n]); out.append(metas[(n + 1) % len(pairs)])
    return block[:a] + open_tag + '\n' + ''.join(out) + '        </div>' + block[b:]

def paras(block):
    """Spans of <p>...</p> that sit directly in activity-body — not inside a
    key-concept, callout, reveal, swyk or game container."""
    i, j = body_span(block)
    skip = []
    for cls in ('key-concept', 'callout', 'reveal-content', 'swyk', 'task-box',
                'fillin-game', 'spotter-game', 'sort-game', 'match-game',
                'root-match-game', 'challenge-item', 'video-wrap', 'vp-notes'):
        for m in re.finditer(r'<div class="[^"]*\b%s\b[^"]*"' % re.escape(cls), block):
            try:
                skip.append(block_span(block, m.start()))
            except ValueError:
                pass
    out = []
    for m in re.finditer(r'<p(?:\s[^>]*)?>.*?</p>', block[i:j], re.S):
        a, b = i + m.start(), i + m.end()
        if any(sa <= a < sb for sa, sb in skip):
            continue
        out.append((a, b))
    return out

def set_para(block, n, html):
    sp = paras(block)
    a, b = sp[n]
    keep = re.match(r'<p(\s[^>]*)?>', block[a:b]).group(0)
    return block[:a] + keep + html + '</p>' + block[b:]

def drop_para(block, n):
    sp = paras(block)
    a, b = sp[n]
    return block[:a] + block[b:]

def set_reveal(block, lines):
    j = block.find('<div class="reveal-content"')
    if j == -1:
        raise KeyError('no reveal-content')
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    return block[:a] + open_tag + '\n' + ''.join('        <p>%s</p>\n' % l for l in lines) + '      </div>' + block[b:]

def set_discovery(block, cards):
    """cards: [(label, [lines])] for the 3-column key-concept discovery grid."""
    m = re.search(r'<div style="display:grid;grid-template-columns:(?:1fr ?)+[^"]*"', block)
    if not m:
        raise KeyError('no discovery grid')
    j = m.start()
    a, b = block_span(block, j)
    open_tag = block[a:block.index('>', a) + 1]
    styles = [('', ''), ('background:#E0F2F1;border-color:#B2DFDB;', 'color:#00695C;'),
              ('background:#F3E5F5;border-color:#E1BEE7;', 'color:#7B5EA7;')]
    out = []
    for n, (label, lines) in enumerate(cards):
        bg, fg = styles[n % 3]
        out.append('        <div class="key-concept" style="margin-bottom:0;%s">\n' % bg)
        out.append('          <div class="key-concept-label"%s>%s</div>\n' % ((' style="%s"' % fg) if fg else '', label))
        out.extend('          <p>%s</p>\n' % l for l in lines)
        out.append('        </div>\n')
    return block[:a] + open_tag + '\n' + ''.join(out) + '      </div>' + block[b:]


def set_feedback(block, text):
    """Rewrite the completion message of whichever game this block contains."""
    n = 0
    for cls in ('root-match-feedback', 'match-feedback', 'fillin-feedback', 'sort-score'):
        pat = r'(<div class="%s"[^>]*>)(.*?)(</div>)' % cls
        def rep(m):
            inner = m.group(2)
            lead = re.match(r'(\s*(?:&#x[0-9A-Fa-f]+;|[\U0001F300-\U0001FAFF☀-➿])\s*)', inner)
            return m.group(1) + ((lead.group(1) if lead else '') + text) + m.group(3)
        block, k = re.subn(pat, rep, block, flags=re.S)
        n += k
    if not n:
        raise KeyError('no game feedback')
    return block


GAME_CLASSES = ('fillin-game', 'spotter-game', 'root-match-grid', 'match-grid',
                'sort-game', 'challenge-item', 'checkFillBlanks', 'reveal-content')

def has_game(block):
    return any(c in block for c in GAME_CLASSES)

def set_body(block, html):
    """Replace the entire activity-body. ONLY safe when the block has no game
    (no JS handlers or element ids to preserve)."""
    i, j = body_span(block)
    return block[:i] + '\n' + html + '\n    ' + block[j:]

def notebook_callouts(block):
    """Text of every callout in the block, for locating one to rewrite."""
    out = []
    for m in re.finditer(r'<div class="callout[^"]*"', block):
        a, b = block_span(block, m.start())
        out.append(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', block[a:b])).strip())
    return out


def _chips_and_cols(columns, hdr_styles):
    chips = sorted([(k, w) for label, k, words in columns for w in words], key=lambda t: t[1].lower())
    bank = ''.join('          <span class="sort-chip" data-group="%s" onclick="pickSortChip(this)">%s</span>\n' % (k, w)
                   for k, w in chips)
    cols = ''.join(
        '          <div class="sort-col"><div class="sort-col-header" style="%s">%s</div>'
        '<div class="sort-col-drop" data-col="%s" onclick="dropSortChip(this,\'%s\')"></div></div>\n'
        % (hdr_styles[n], label, key, key) for n, (label, key, words) in enumerate(columns))
    return bank, cols

def _set_sort_loose(block, columns):
    jb = block.find('<div class="sort-bank"')
    jc = block.find('<div class="sort-columns"')
    if jb == -1 or jc == -1:
        raise KeyError('no sort bank/columns')
    styles = re.findall(r'<div class="sort-col-header" style="([^"]*)">', block)
    while len(styles) < len(columns):
        styles.append(styles[-1] if styles else 'background:#0E1C42;')
    bank, cols = _chips_and_cols(columns, styles)
    ab, bb = block_span(block, jb)
    block = block[:ab] + block[ab:block.index('>', ab) + 1] + '\n' + bank + '        </div>' + block[bb:]
    jc = block.find('<div class="sort-columns"')
    ac, bc = block_span(block, jc)
    return block[:ac] + block[ac:block.index('>', ac) + 1] + '\n' + cols + '        </div>' + block[bc:]

def set_choice(block, items):
    """items: [(prompt_html, question_html, [(button_text, is_correct)])].
    Regenerates a .choice-game, preserving its id and per-item id prefix."""
    j = block.find('<div class="choice-game"')
    if j == -1:
        raise KeyError('no choice-game')
    a, b = block_span(block, j)
    seg = block[a:b]
    open_tag = seg[:seg.index('>') + 1]
    handler = re.search(r'onclick="(\w+)\(', seg)
    handler = handler.group(1) if handler else 'choiceBtn'
    ids = re.findall(r'<div class="choice-item" id="([A-Za-z]+)\d+"', seg)
    pre = ids[0] if ids else 'ci'
    out = []
    for n, (prompt, q, choices) in enumerate(items, 1):
        iid = '%s%d' % (pre, n)
        out.append('        <div class="choice-item" id="%s">\n' % iid)
        if prompt:
            out.append('          <div class="choice-prompt" style="font-style:italic;color:#7A88A8;">%s</div>\n' % prompt)
        if q:
            out.append('          <p style="font-size:14px;color:#3A4A6B;margin:6px 0 10px;">%s</p>\n' % q)
        out.append('          <div class="choice-row">\n')
        for txt, ok in choices:
            out.append('            <button class="choice-btn" onclick="%s(this,\'%s\',%s)">%s</button>\n'
                       % (handler, iid, 'true' if ok else 'false', txt))
        out.append('          </div>\n          <div class="choice-score" id="%s-msg"></div>\n        </div>\n' % iid)
    return block[:a] + open_tag + '\n' + ''.join(out) + '      </div>' + block[b:]

def set_js_message(page, func, text):
    """Rewrite the hardcoded success string inside a per-file game handler."""
    m = re.search(r'function %s\b.*?\n\}' % re.escape(func), page, re.S)
    if not m:
        raise KeyError('no function %s' % func)
    body = m.group(0)
    new, n = re.subn(r"(msg\.textContent=')[^']*(')", lambda mm: mm.group(1) + text + mm.group(2), body, count=1)
    if not n:
        raise KeyError('no message in %s' % func)
    return page[:m.start()] + new + page[m.end():]

def set_js_total(page, var, n):
    new, k = re.subn(r'(var\s+%s\s*=\s*)\d+' % re.escape(var), lambda m: m.group(1) + str(n), page, count=1)
    if not k:
        raise KeyError('no var %s' % var)
    return new


def set_button_game(block, groups):
    """Regenerate an inline button game (odd-one-out, root detective, 'which wins').
    Auto-detects group/row/button/message classes, the id prefix and the JS handler.
    Handles both a wrapped container and bare sibling groups.
    groups: [(label_html, [(button_text, is_correct)], message_html)]"""
    gm = list(re.finditer(r'<div class="([\w-]*(?:group|item))" id="([A-Za-z]+)\d+">', block))
    gm = [m for m in gm if 'onclick=' in block[m.start():m.start() + 1200]]
    if not gm:
        raise KeyError('no inline button game')
    gcls, pre = gm[0].group(1), gm[0].group(2)
    gm = [m for m in gm if m.group(1) == gcls and m.group(2) == pre]
    start = gm[0].start()
    end = block_span(block, gm[-1].start())[1]
    seg = block[start:end]
    base = gcls.rsplit('-', 1)[0]
    lab = (re.search(r'<div class="([\w-]+(?:label|word))"', seg) or [None, base + '-label'])[1]
    row = (re.search(r'<div class="([\w-]*row)"', seg) or [None, base + '-row'])[1]
    btn = (re.search(r'<button class="([\w-]+)"', seg) or [None, base + '-btn'])[1]
    msg = (re.search(r'<div class="([\w-]*msg)"', seg) or [None, base + '-msg'])[1]
    handler = (re.search(r'onclick="(\w+)\(', seg) or [None, 'oddOne'])[1]
    out = []
    for n, (label, choices, message) in enumerate(groups, 1):
        gid = '%s%d' % (pre, n)
        out.append('      <div class="%s" id="%s">\n' % (gcls, gid))
        out.append('        <div class="%s">%s</div>\n' % (lab, label))
        out.append('        <div class="%s">\n' % row)
        for txt, ok in choices:
            out.append('          <button class="%s" onclick="%s(this,\'%s\',%s)">%s</button>\n'
                       % (btn, handler, gid, 'true' if ok else 'false', txt))
        out.append('        </div>\n')
        out.append('        <div class="%s" id="%s-msg">%s</div>\n' % (msg, gid, message))
        out.append('      </div>\n')
    return block[:start] + ''.join(out) + block[end:]


def set_taskbox(block, sentences):
    """Replace the .task-sentence lines inside a .task-box."""
    j = block.find('<div class="task-box"')
    if j == -1:
        raise KeyError('no task-box')
    a, b = block_span(block, j)
    seg = block[a:b]
    open_tag = seg[:seg.index('>') + 1]
    style = (re.search(r'<div class="task-sentence" style="([^"]*)"', seg) or [None, 'border-left-color:#8B3A20;'])[1]
    rows = ''.join('        <div class="task-sentence" style="%s">%s</div>\n' % (style, x) for x in sentences)
    return block[:a] + open_tag + '\n' + rows + '      </div>' + block[b:]
