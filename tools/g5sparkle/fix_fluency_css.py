#!/usr/bin/env python3
"""Fluency pages 27-29: the standards-bar CSS sat after <body> as plain text, so it showed at the top of the page
(and pushed it sideways on a phone). Move it, unchanged, to the end of the page's <style>. Usage: fix_fluency_css.py <file>..."""
import io, sys
for f in sys.argv[1:]:
    s = io.open(f, encoding='utf-8', newline='').read()
    a = s.find('/* ======= STANDARDS TOGGLE BAR ======= */'); b = s.find('<div class="page-wrap">', a); body = s.find('<body')
    if a < body or b < 0: sys.exit('%s: not the bad shape' % f)
    css = s[a:b].rstrip() + '\n'
    st = s.rfind('</style>', 0, body)
    s2 = s[:a] + s[b:]
    s2 = s2[:st] + '\n' + css + s2[st:]
    if s2.count('<div') != s.count('<div'): sys.exit('div ' + f)
    io.open(f, 'w', encoding='utf-8', newline='').write(s2); print('fixed', f, len(css), 'chars of CSS moved')
