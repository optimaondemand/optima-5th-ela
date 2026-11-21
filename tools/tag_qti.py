#!/usr/bin/env python3
"""tag_qti.py: put each check-in question's standards into a Canvas check-in package.

    python3 tools/tag_qti.py PACKAGE.zip|PACKAGE.imscc [...]      (run from the repo root)

For every quiz item it
  * renames the question "Week W Question N · <FL codes>" (Canvas shows question names to
    teachers in the editor and Quiz Statistics, never to students), and
  * adds qtimetadata fields standards_fl / _tx / _ar / _mo / _al / _tn / _pr.
The standards come from the tags already on lesson-W-checkin.html (the <script id="oao-standards">
block written by tools/std_tag.py), question N = the page's Nth question, so a page and its
package always agree. The package is rewritten in place; nothing else in it changes.
Re-running is safe. Builders call tag() on what they write."""
import io, json, re, sys, zipfile
from xml.sax.saxutils import escape

STATES = ['FL', 'TX', 'AR', 'MO', 'AL', 'TN', 'PR']
_cache = {}

def page_tags(week):
    if week not in _cache:
        s = io.open('lesson-%d-checkin.html' % week, encoding='utf8').read()
        m = re.search(r'<script type="application/json" id="oao-standards">(.*?)</script>', s, re.S)
        if not m: raise SystemExit('lesson-%d-checkin.html has no standards tags; run tools/std_tag.py %d first' % (week, week))
        _cache[week] = json.loads(m.group(1).replace('<\\/', '</'))['blocks']
    return _cache[week]

def meta(l, v):
    return '<qtimetadatafield><fieldlabel>%s</fieldlabel><fieldentry>%s</fieldentry></qtimetadatafield>' % (l, escape(v))

def tag_xml(x):
    a = re.search(r'<assessment [^>]*title="([^"]*)"', x)
    if not a: return x, 0
    week = int(re.search(r'Week (\d+)', a.group(1)).group(1))
    blocks = page_tags(week)
    n_items = len(re.findall(r'<item ', x))
    if n_items != len(blocks):
        raise SystemExit('week %d: package has %d questions, page has %d tagged; rebuild the package from the page first'
                         % (week, n_items, len(blocks)))
    count = [0]
    def one(m):
        count[0] += 1
        n = count[0]
        b = blocks[n - 1]
        assert b['title'].startswith('Q%d ' % n), (week, n, b['title'])
        head, rest = m.group(1), m.group(2)
        head = re.sub(r'title="[^"]*"', 'title="Week %d Question %d · %s"' % (week, n, ' + '.join(b['FL'])), head)
        rest = re.sub(r'<qtimetadatafield><fieldlabel>standards_\w+</fieldlabel><fieldentry>[^<]*</fieldentry></qtimetadatafield>', '', rest)
        add = ''.join(meta('standards_' + st.lower(), b[st] if isinstance(b[st], str) else ' '.join(b[st])) for st in STATES)
        rest = rest.replace('</qtimetadata>', add + '</qtimetadata>', 1)
        return head + rest
    x = re.sub(r'(<item [^>]*>)(<itemmetadata>.*?</itemmetadata>)', one, x, flags=re.S)
    return x, count[0]

def tag(path):
    src = zipfile.ZipFile(path)
    files = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    out, total = io.BytesIO(), 0
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for info, data in files:
            if info.filename.endswith(('.xml', '.qti')) and b'<questestinterop' in data:
                x, n = tag_xml(data.decode('utf8'))
                total += n
                data = x.encode('utf8')
            z.writestr(info, data)
    open(path, 'wb').write(out.getvalue())
    print('%s: %d questions tagged' % (path, total))
    return total

if __name__ == '__main__':
    for p in sys.argv[1:]: tag(p)
