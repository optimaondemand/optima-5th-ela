#!/usr/bin/env python3
"""Week 18 clarity pass (Nov 10 2026, ahead of the pilot review): a What to do
on the two activities that had none (Virtue Watch, Reading), and a named button
on each picture's reveal. Writes data/g5ela-18-N.json and the page's oao-data."""
import io, json, re, glob, subprocess
VIRTUE = {"match": "Virtue Watch", "do": ["Read what courage means.", "Read how courage shows up in this week's chapters.", "Watch for courage while you read. Nothing to write here."]}
RWM = "Do the RWM box: read the sentence, then answer as a reader and as a writer."
READ = {
 1: ["Tap Listen, or read the chapter introduction.", "Open your book and read Chapters 1–2.", "Answer the Quick Check."],
 2: ["Tap Listen, or read the chapter introduction.", "Open your book and read Chapters 3–4.", "Answer the Quick Check.", RWM],
 3: ["Read the chapter introduction and today's reading skill.", "Open your book and read Chapters 5–6.", RWM],
 4: ["Read the chapter introduction and today's reading skill.", "Open your book and read Chapter 7.", "Answer the Quick Check."],
}
BTN = {1: "Tap to learn about this map", 2: "Tap to learn about this cypress photo", 3: "Tap to learn about this swamp photo", 4: "Tap to learn about this stickball painting"}
for d in (1, 2, 3, 4):
    p = 'data/g5ela-18-%d.json' % d
    orig = io.open(p, encoding='utf-8').read()
    ind = len(orig.split('\n')[1]) - len(orig.split('\n')[1].lstrip(' '))
    j = json.loads(orig)
    j['how'] = [x for x in j['how'] if x.get('match') not in ('Virtue Watch', 'Chapter Introduction')]
    j['how'] += [VIRTUE, {"match": "Chapter Introduction", "do": READ[d]}]
    j['art']['lookBtn'] = BTN[d]
    io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=ind) + ('\n' if orig.endswith('\n') else ''))
    f = [x for x in glob.glob('lesson-18-%d-hbg-*.html' % d) if x.endswith('.html')][0]
    h = io.open(f, encoding='utf-8', newline='').read()
    m = re.search(r'(id="oao-data">\s*)(\{.*?\})(\s*</script>)', h, re.S)
    raw = m.group(2); ind2 = 1 if '\n "' in raw else (2 if '\n  "' in raw else None)
    k = json.loads(raw); k['how'] = j['how']; k['art'] = j['art']
    h = h[:m.start(2)] + json.dumps(k, ensure_ascii=False, indent=ind2) + h[m.end(2):]
    io.open(f, 'w', encoding='utf-8', newline='').write(h); print(f, 'ok')
