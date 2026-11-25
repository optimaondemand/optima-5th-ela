#!/usr/bin/env python3
"""Q3-Q4 audit (Nov 25 2026): wording fixes, weeks 17-30 (31-32 were already done in their runs).
- strand initials spelled out in visible text and My Work labels (skill 8f.5): DOL -> Daily Oral Language, RWM -> Read Like a Writer,
  SWYK -> Show What You Know (text between tags and data-label only; scripts, ids and classes untouched)
- the generic teacher recording note ("pay close attention to the characters' actions...") replaced with one plain line
- check-ins 18-24: "or download as a PDF and upload the file" dropped (turning in is copy and paste)
    python tools/g5sparkle/fix_audit_wording.py [--apply]"""
import io, re, sys, glob
MAP = [(r'\bDOL\b', 'Daily Oral Language'), (r'\bRWM\b', 'Read Like a Writer'), (r'\bSWYK\b', 'Show What You Know')]
NOTE = 'As you read, pay close attention to the characters&#x27; actions and motivations. Think about how events connect to the bigger ideas in the story. Use your journal to capture your thoughts and any questions that come up.'
UP = (' — or <strong>download as a PDF</strong> and upload the file to the Canvas assignment.', '.')
def textfix(seg):
    for rx, rep in MAP: seg = re.sub(rx, rep, seg)
    return seg
def fix(s):
    parts = re.split(r'(?is)(<script\b.*?</script>|<style\b.*?</style>)', s)
    for i in range(0, len(parts), 2):
        p = parts[i]
        p = re.sub(r'>([^<]+)<', lambda m: '>' + textfix(m.group(1)) + '<', p)
        p = re.sub(r'(data-label=")([^"]*)(")', lambda m: m.group(1) + textfix(m.group(2)) + m.group(3), p)
        parts[i] = p
    s = ''.join(parts)
    s = s.replace(NOTE, 'Keep the novel and the reading journal close by.')
    s = s.replace(*UP)
    return s
tot = 0
for f in sorted(glob.glob('lesson-*.html')):
    m = re.match(r'lesson-(\d+)-', f)
    if not m or not 17 <= int(m.group(1)) <= 30 or 'project' in f: continue
    o = io.open(f, encoding='utf-8', newline='').read(); t = fix(o)
    if t != o:
        if o.count('<div') - o.count('</div') != t.count('<div') - t.count('</div'): sys.exit('div ' + f)
        n = sum(len(re.findall(rx, re.sub(r'(?is)<script\b.*?</script>|<style\b.*?</style>', '', o))) for rx, _ in MAP)
        tot += 1; print(f, 'changed', len(o), '->', len(t))
        if '--apply' in sys.argv: io.open(f, 'w', encoding='utf-8', newline='').write(t)
print(tot, 'files')
