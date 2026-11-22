#!/usr/bin/env python3
"""Update parent-guide-hbg-unit.html for the unit's close (Bethany, Nov 22 2026): history figures tied to their
sources (Choctaw Nation of Oklahoma; National Park Service), week 24 row from the finished lessons, links to
every weekly guide, a "How the Unit Ends" card (two real sources + the end-of-novel project). Run once."""
import io, sys
p = 'parent-guide-hbg-unit.html'
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
R = [
 ('in three groups from 1831 to 1833. Nearly 15,000 Choctaws made the move, and historians estimate about 2,500 died along the way, many in bitter winter weather and a cholera epidemic in 1832. About 5,000–6,000 Choctaws stayed in Mississippi; the Mississippi Band of Choctaw Indians lives there today.',
  'in groups from 1831 to 1833. The treaty itself set those dates: the falls of 1831, 1832 and 1833. About 15,000 Choctaws made the move in those years. No one knows exactly how many died, from disease, hunger, cold and violence. Historians often give about 2,500, and the Choctaw Nation of Oklahoma says one-quarter to one-third of those who were removed. About 6,000 Choctaws stayed in Mississippi, according to the National Park Service; the Mississippi Band of Choctaw Indians lives there today, and the Choctaw Nation of Oklahoma is one of the largest Native nations in the United States.'),
 ('<p class="wk-sum">The panther and the wolf, and Naomi home with her family. Then your student compares the novel with a historical source.</p>',
  '<p class="wk-sum">The panther and the wolf, and Naomi home with her family. Then your student reads two real sources, part of the 1830 treaty and part of a letter by Choctaw chief George W. Harkins, and compares the novel with the record.</p>'),
 ('<li><span>🪨</span><strong>Stones in the River:</strong> the unit’s word game</li>', '<li><span>🎲</span><strong>A word game:</strong> a new one each week, tied to the chapters</li>'),
 ('<div class="box b-green"><div class="box-label">End of unit</div>In Week 24, your student compares the novel with a historical source, using a claim, evidence and reasoning.</div>',
  '<div class="box b-green"><div class="box-label">End of unit</div>In Week 24, your student compares the novel with a real source, using a claim, evidence and reasoning. Then comes the end-of-novel project, <strong>A Ghost’s-Eye View</strong>, turned in as one PDF.</div>'),
 ('  <!-- WRITING -->\n', '''  <!-- HOW THE UNIT ENDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🏁</span><h2>How the Unit Ends</h2></div>
    <div class="grid2">
      <div class="box b-gold"><div class="box-label">📜 Two real sources (Week 24)</div>On Day 3 your student reads real words from the time. <strong>Article 3 of the Treaty of Dancing Rabbit Creek</strong>, signed September 27, 1830, gives up the Choctaw land east of the Mississippi River and sets the removal for the falls of 1831, 1832 and 1833. <strong>George W. Harkins</strong>, a young Choctaw chief, wrote a letter “To the American People” as he left Mississippi with his people in 1831: “We go forth sorrowful, knowing that wrong has been done.” Each source has a plain-words version under it.</div>
      <div class="box b-sky"><div class="box-label">🧭 The story and the record, kept apart</div>The novel’s first page says 1830; the real removal began in the fall of 1831. Pushmataha, who appears at the end of the novel, was a real Choctaw chief and general who died in 1824, so in the story he comes as a ghost. The lessons point these out, so your student learns to ask, “Is that the story or the history?”</div>
    </div>
    <div class="box b-green" style="margin-top:12px;"><div class="box-label">📘 End-of-novel project: A Ghost’s-Eye View</div>After Lesson 24.4, your student makes a four-page booklet about the whole book: how a ghost narrator changes what the reader sees, one theme tracked through a moment from the beginning, the middle and the end, one character with evidence, one figure of speech explained, and a reflection. The project page saves as they type and turns the work into <strong>one PDF</strong> to upload in Canvas. It is graded on a 20-point rubric shown on the page. Plan on one or two sittings, with the book open.</div>
  </section>

  <!-- WRITING -->
'''),
]
for w in (19, 20, 21, 22, 23, 24):
    pass
for old, new in R:
    if s.count(old) != 1: sys.exit('expected 1 of %r, found %d' % (old[:60], s.count(old)))
    s = s.replace(old, new)
soon = '<span class="wk-soon">Weekly guide comes with the week</span>'
if s.count(soon) != 6: sys.exit('wk-soon x%d' % s.count(soon))
for w in (19, 20, 21, 22, 23, 24):
    s = s.replace(soon, '<a class="wk-link" href="parent-guide-week-%d.html">Open the Week %d guide →</a>' % (w, w), 1)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s); print('updated', p)
