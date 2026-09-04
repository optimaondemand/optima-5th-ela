# -*- coding: utf-8 -*-
"""Pass 5: revive the Story Journey Tracker in How I Became a Ghost (weeks 18-24).
renderTracker() in all 28 files bails at `if (!scene) return;` because the markup for
the scene and the character token was never added. Everything else already exists in
each file's own CSS (.scene-wrap, .node/.done/.active/.upcoming, .title-plaque, .cloud,
.hills-far, .path-svg, @keyframes hop) — only `.char-token` was missing.
Ports the working Witch pattern using HBG's own styles. Adds nothing invented."""
import re, os, shutil, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHAR_TOKEN_CSS = (
".char-token {\n"
"  position: absolute;\n"
"  font-size: 26px;\n"
"  z-index: 20;\n"
"  pointer-events: none;\n"
"  filter: drop-shadow(0 3px 5px rgba(0, 0, 0, 0.3));\n"
"  animation: hop 2s ease-in-out infinite;\n"
"}\n")

PATH = ("M -20,168 C 70,162 90,132 160,128 C 230,124 250,158 330,150 "
        "C 410,143 430,108 520,111 C 610,115 630,152 720,144 "
        "C 810,136 840,102 930,107 C 1020,112 1040,150 1120,142 "
        "C 1200,134 1230,112 1310,117 C 1350,119 1400,132 1430,137")

def scene(indent='    '):
    i = indent
    s  = i + '<div class="scene-wrap" id="scene">\n'
    s += i + '  <div class="title-plaque"><h1>&#128123; <em>How I Became a Ghost</em></h1></div>\n'
    for w, h, top, left in ((80,24,16,'8%'), (52,16,26,'24%'), (90,26,12,'58%'), (56,18,30,'80%')):
        s += i + '  <div class="cloud" style="width:%dpx;height:%dpx;top:%dpx;left:%s"></div>\n' % (w,h,top,left)
    s += i + '  <div class="hills-far"></div>\n'
    s += i + '  <svg class="path-svg" viewBox="0 0 1400 210" preserveAspectRatio="none">\n'
    s += i + '    <path d="%s" fill="none" stroke="#8B6914" stroke-width="14" stroke-linecap="round" opacity="0.45"/>\n' % PATH
    s += i + '    <path d="%s" fill="none" stroke="#e8dcc8" stroke-width="7" stroke-linecap="round" stroke-dasharray="4 8" opacity="0.55"/>\n' % PATH
    s += i + '  </svg>\n'
    s += i + '  <div class="char-token" id="characterToken">&#128123;</div>\n'
    s += i + '</div>\n'
    return s

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    notes = []

    if 'id="scene"' in s:
        print('%-30s already has a scene - skipped' % fn); return

    # 1. add the one missing CSS rule, right after .node.upcoming
    if '.char-token' not in s:
        m = re.search(r'\.node\.upcoming\s*\{[^}]*\}\n?', s)
        if not m:
            m = re.search(r'\.path-svg\s*\{[^}]*\}\n?', s)
        if not m:
            print('%-30s !! no CSS anchor' % fn); return
        s = s[:m.end()] + CHAR_TOKEN_CSS + s[m.end():]
        notes.append('css')

    # 2. insert the scene inside tracker-card, after the tracker-header div
    tc = s.find('<div class="tracker-card"')
    if tc < 0:
        print('%-30s !! no tracker-card' % fn); return
    hd = s.find('<div class="tracker-header"', tc)
    if hd < 0:
        print('%-30s !! no tracker-header' % fn); return
    # end of the tracker-header element: walk its divs
    k, depth = hd, 0
    for m in re.finditer(r'<div\b|</div>', s[hd:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            k = hd + m.end(); break
    else:
        print('%-30s !! unbalanced tracker-header' % fn); return
    s = s[:k] + '\n' + scene() + '  ' + s[k:].lstrip('\n')
    notes.append('scene')

    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        o, c = len(re.findall(r'<div\b', s)), len(re.findall(r'</div>', s))
        print('%-30s %s  divs %d/%d %s' % (fn, ', '.join(notes), o, c, 'OK' if o == c else '!! UNBALANCED'))

only = sys.argv[1:]
import glob
files = sorted(glob.glob(os.path.join(D, 'lesson-1[89]-[1-4]-*.html'))) + \
        sorted(glob.glob(os.path.join(D, 'lesson-2[0-4]-[1-4]-*.html')))
files = [os.path.basename(f) for f in files]
files.sort(key=lambda f: (int(re.match(r'lesson-(\d+)', f).group(1)), int(re.match(r'lesson-\d+-(\d)', f).group(1))))
for fn in files:
    if only and not any(o in fn for o in only):
        continue
    patch(fn)
