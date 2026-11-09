#!/usr/bin/env python3
"""Check a built G5 ELA VR page against its week JSON.
usage: python3 tools/vr/check_vr.py tools/vr/week18.json
Fails on: a model/map not in Planning docs/vr-assets.csv, wrong day or step count, a missing help image,
a duplicate <title> anywhere in the repo, an inlined data:image, a dash or a banned word in student text,
a VR mention in any lesson, an empty transcript, or too many words."""
import csv, glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
D = json.load(open(sys.argv[1], encoding='utf-8'))
W = D['week']
path = os.path.join(ROOT, 'vr-%d.html' % W)
page = open(path, encoding='utf-8').read()
errs, notes = [], []

# 1. models + map exist in the asset list
rows = list(csv.reader(open(os.path.join(ROOT, 'Planning docs', 'vr-assets.csv'), encoding='utf-8-sig')))
names = {r[0].strip() for r in rows if r}
models = [m['name'] for m in D['models']]
if D.get('groups'):
    for m in D['models']:
        if m.get('group') not in {g['k'] for g in D['groups']}: errs.append('model has no group: ' + m['name'])
for m in models + D['steps']['extraModels']:
    if m not in names: errs.append('model not in vr-assets.csv: ' + m)
if D['map'] not in names: errs.append('map not in vr-assets.csv: ' + D['map'])
if not 5 <= len(models) <= 7: errs.append('need 5-7 models, have %d' % len(models))

# 2. Day 2, 7 steps, Canvas name
if D['day'] != 2: errs.append('VR must be Day 2')
nsteps = len(re.findall(r'<li class="step">', page))
if nsteps != 7: errs.append('need 7 steps, have %d' % nsteps)
canvas = '%d.2 VR · %s' % (W, D['title'])
if html.escape(canvas) not in page: errs.append('Canvas name missing: ' + canvas)

# 3. title unique across the repo (it is the localStorage key with PRE)
title = re.search(r'<title>(.*?)</title>', page).group(1)
for f in glob.glob(os.path.join(ROOT, '*.html')):
    if os.path.abspath(f) != os.path.abspath(path):
        m = re.search(r'<title>(.*?)</title>', open(f, encoding='utf-8', errors='ignore').read())
        if m and m.group(1) == title: errs.append('duplicate <title> in ' + os.path.basename(f))

# 4. nothing inlined, retired help, images exist
if 'data:image' in page: errs.append('data:image inlined')
if 'xVzX24ENnqk' in page or 'vr-help-0' in page: errs.append('retired help video/images')
for img in set(re.findall(r'assets/vr/([\w.-]+)', page)):
    if not os.path.exists(os.path.join(ROOT, 'assets', 'vr', img)): errs.append('missing image assets/vr/' + img)

# 5. transcripts
tr = json.loads(re.search(r'(?s)<script type="application/json" id="vr-data">(.*?)</script>', page).group(1))['transcripts']
for k in ('brief', 'alt', 'saved'):
    t = tr.get(k, '').strip()
    if not t: errs.append('empty transcript: ' + k)
    nw = len(t.split())
    if k == 'brief' and not 40 <= nw <= 75: errs.append('brief is %d words (40-70)' % nw)
    if re.search(r'\b(good morning|good night|tonight|this morning|this afternoon|this evening)\b', t, re.I): errs.append('time of day in ' + k)

# 5b. guide is Mason; scripts never speak as Isaac or a Choctaw character (Bethany, Nov 2026)
if D['guide']['folder'] != 'mason': errs.append('G5 ELA VR guide must be Mason')
if re.search(r"\b(I am|I'm|I’m) (Isaac|Luke|Nita|Joseph)\b", ' '.join(D['scripts'].values())): errs.append('a script speaks as a book character')

# 6. student-facing text: words, dashes, banned words
body = re.sub(r'(?s)<script.*?</script>|<style.*?</style>|<details class="helpdrawer".*?</details>|<svg.*?</svg>|<!--.*?-->', ' ', page)
body = re.sub(r'(?s)<head>.*?</head>|<footer>.*?</footer>|<div class="vslot-ph".*?</div>', ' ', body)
text = html.unescape(re.sub(r'<[^>]+>', ' ', body))
count = lambda t: len(re.findall(r"[A-Za-z0-9’']+", html.unescape(re.sub(r'<[^>]+>', ' ', t))))
cut = body.find('<section class="alt">')
top = body[:body.find('<section class="card vr-only" id="vr">')]
vr_words = count(body[:cut])
game = json.loads(re.search(r'(?s)id="vr-data">(.*?)</script>', page).group(1))['game']
gtxt = ' '.join(str(v) for v in re.findall(r'"(?:plain|hint|t|s|why)":\s*"([^"]*)"', json.dumps(game, ensure_ascii=False)))
alt_words = count(top) + count(body[cut:]) + count(gtxt) + sum(len(o) for r in game.get('rename', []) for o in r['opts']) // 6 + len(re.findall(r'\w+', json.dumps(game.get('cards', []))) ) // 3
for nm, nw in (('Story Expedition path', vr_words), ('Field Notes Day path', alt_words)):
    (errs if nw > 850 else notes).append('%s: about %d visible words (fail over 850 for G5; aim near 600; the help drawer is not counted)' % (nm, nw))
if re.search(r'\s[-–—]\s|—|–', text): errs.append('dash in student text: ' + re.search(r'.{0,30}(\s[-–—]\s|—|–).{0,30}', text).group(0))
for bad in ['bonus', 'backup', 'imagination trip', 'window seat', 'keepsake', 'bookmark']:
    if re.search(r'\b%s\b' % bad, text + ' ' + json.dumps(game, ensure_ascii=False), re.I): errs.append('banned word: ' + bad)
spoken = ' '.join(tr.values())
if re.search(r'\s[-–—]\s|—|–', spoken): errs.append('dash in a transcript')

# 7. the lessons stay VR-free (Bethany, 29 Oct 2026)
for f in glob.glob(os.path.join(ROOT, 'lesson-*.html')):
    s = open(f, encoding='utf-8', errors='ignore').read()
    if re.search(r'vr-\d+\.html', s): errs.append('a lesson links a VR page: ' + os.path.basename(f))

for n in notes: print('  ·', n)
if errs:
    for x in errs: print('  ✗', x)
    sys.exit(1)
print('✓ vr-%d.html passes (%d KB)' % (W, len(page.encode()) // 1024))
