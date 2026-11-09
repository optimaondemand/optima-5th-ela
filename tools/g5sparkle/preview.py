#!/usr/bin/env python3
"""preview.py — one self-contained preview of a sparkled G5 ELA lesson for Bethany (never committed).
    python tools/g5sparkle/preview.py lesson-18-1-hbg-ch4.html out.html
Inlines g5-sparkle.css/js, every assets/ image and mp3 the page or its DATA points at."""
import base64, io, os, re, sys, mimetypes
src, out = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.abspath(src))
html = io.open(src, encoding='utf-8', newline='').read()
css = io.open(os.path.join(root, 'g5-sparkle.css'), encoding='utf-8').read()
js = io.open(os.path.join(root, 'g5-sparkle.js'), encoding='utf-8').read()
html = html.replace('<link rel="stylesheet" href="g5-sparkle.css">', '<style>' + css + '</style>')
html = html.replace('<script src="g5-sparkle.js" defer></script>', '<script>' + js.replace('</script>', '<\\/script>') + '</script>')
def uri(path):
    p = os.path.join(root, path)
    if not os.path.isfile(p):
        return None
    mt = mimetypes.guess_type(p)[0] or 'application/octet-stream'
    return 'data:%s;base64,%s' % (mt, base64.b64encode(open(p, 'rb').read()).decode())
n = 0
def rep(m):
    global n
    u = uri(m.group(1))
    if u: n += 1; return u
    return m.group(0)
html = re.sub(r'(assets/(?:art|audio)/[A-Za-z0-9_./-]+\.(?:jpg|png|mp3))', rep, html)
# the layer probes audio by URL; in the preview, map known clip names to inlined data
clips = {}
import json as _j
_d = re.search(r'id="oao-lesson">(.*?)</script>', html)
_d = _j.loads(_d.group(1)) if _d else {}
want = ('g5ela-%s-%s-' % (_d['week'], _d['day'])) if _d else ''
ad = os.path.join(root, 'assets/audio')
if os.path.isdir(ad):
    for dp, _, fs in os.walk(ad):
        for f in fs:
            if f.endswith('.mp3') and (not want or f.startswith(want)):
                rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
                clips[rel] = uri(rel)
if clips:
    import json
    shim = '<script>window.__G5_CLIPS=%s;</script>' % json.dumps(clips)
    html = html.replace('<!-- ═════════ OAO G5 SPARKLE LAYER (additive) ═════════ -->', shim + '<!-- ═════════ OAO G5 SPARKLE LAYER (additive) ═════════ -->')
html = html.replace('<title>', '<title>PREVIEW · ', 1)
io.open(out, 'w', encoding='utf-8', newline='').write(html)
print('wrote', out, len(html) // 1024, 'KB;', n, 'assets inlined;', len(clips), 'clips')
