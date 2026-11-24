#!/usr/bin/env python3
"""Update parent-guide-btghs-unit.html for the unit's close (Bethany, Nov 24 2026): week rows 26-30 rewritten
from the finished weekly guides, links to every weekly guide, the writing card matched to what was built
(week 28 is a literary response), an End-of-unit box naming the project, a "How the Unit Ends" card. Run once."""
import io, sys
p = 'parent-guide-btghs-unit.html'
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
R = [
 # week rows, from the "This Week at a Glance" of each finished weekly guide
 ('<p class="wk-sum">A pig hunt on board, a stop in Rio de Janeiro, and storms near the tip of South America.</p>',
  '<p class="wk-sum">Jack hides his pet pig from the cook, says no to a ticket home at Rio de Janeiro, and rides out thirty-seven days of storms on the way around South America.</p>'),
 ('<p class="wk-sum">The race between two ships ends, and the partners land in a city full of gold-seekers, with no money for the riverboat.</p>',
  '<p class="wk-sum">The race to the Golden Gate ends. In San Francisco everything costs a fortune, and a haircut for a shaggy miner gives the partners their start. Day 4: the real words of reporter Bayard Taylor.</p>'),
 ('<p class="wk-sum">A stagecoach ride into the mountains, a holdup, and a new name in a mining town.</p>',
  '<p class="wk-sum">A stagecoach holdup, then Hangtown, where Jack learns to pan for gold and earns the name Jamoka Jack. Day 4: your student names a theme of the novel and argues for it.</p>'),
 ('<p class="wk-sum">Hard work in the gold fields, a burro with opinions, and a run-in with a grizzly.</p>',
  '<p class="wk-sum">Life in the diggings, a misheard word at an auction that Jack pays for rather than break his word, and a burro named Stubb for a prospecting trip into the mountains.</p>'),
 ('<p class="wk-sum">The partners find out what a fortune is really made of. The book ends back at the Long Wharf in San Francisco.</p>',
  '<p class="wk-sum">Praiseworthy speaks up to keep a promise, the fight with the Mountain Ox, and a fast boat back to the Long Wharf in San Francisco. Day 1 has a real-history card on Sutter&rsquo;s Mill. Day 4 looks back at the whole book.</p>'),
 # writing card, matched to the weeks as built
 ('Week 25 is the plan: a hero, a problem, a setting, and what is at stake. Then a draft, scenes with dialogue and voice, a middle that raises the stakes, a revision for voice and tone, and a finished, edited story.',
  'Week 25 is the plan: a hero, a problem, a setting, and what is at stake. Week 26 drafts a scene with dialogue, and Week 27 builds a middle that raises the stakes. In Week 28 the story rests while your student writes about the novel: a claim about its theme, proved with what the characters choose. Week 29 revises one paragraph for voice, and Week 30 adds a strong ending and publishes the finished, edited story.'),
 ('<div class="box b-green"><div class="box-label">End of unit</div>The finished adventure story, plus an end-of-novel project that your student&rsquo;s teacher will share in Week 30.</div>',
  '<div class="box b-green"><div class="box-label">End of unit</div>The finished adventure story (Week 30, Day 4), then the end-of-novel project, <strong>From Boston to the Long Wharf</strong>, turned in as one PDF.</div>'),
 ('<p class="foot"><a href="parent-guide-week-25.html" style="color:#1F6FA8;font-weight:700;">Open the Week 25 guide →</a>',
  '<p class="foot"><a href="parent-guide-week-25.html" style="color:#1F6FA8;font-weight:700;">Open the Week 25 guide →</a> &nbsp;·&nbsp; <a href="parent-guide-week-30.html" style="color:#1F6FA8;font-weight:700;">Open the Week 30 guide →</a>'),
 ('  <section class="card">\n    <div class="card-head"><span class="ico">✍️</span>', '''  <!-- HOW THE UNIT ENDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🏁</span><h2>How the Unit Ends</h2></div>
    <div class="grid2">
      <div class="box b-gold"><div class="box-label">⛏️ Real history, kept apart (Week 30)</div>The novel&rsquo;s last chapters pass through Coloma, where gold was found. A Day 1 card tells the real story: James Marshall&rsquo;s discovery at Sutter&rsquo;s Mill on January 24, 1848, a worker&rsquo;s diary from that day, and the Nisenan valley of Cullumah. The story and the record stay in separate boxes, the way they have all unit.</div>
      <div class="box b-sky"><div class="box-label">🧭 Words from 1963</div>Two short passages in the last week use unkind words from the time the book was written: one about Chinese miners in Chapter 17 and one about Hawaiian sailors in Chapter 18. A folded note on that day&rsquo;s Reading tab names each one plainly and gives the true history. The Week 30 guide has the details.</div>
    </div>
    <div class="box b-green" style="margin-top:12px;"><div class="box-label">📘 End-of-novel project: From Boston to the Long Wharf</div>After Lesson 30.4, your student makes a four-page booklet about the whole book: the adventure&rsquo;s shape from problem to ending, six turning points told fast or slow, one funny moment and one figure of speech, and the big idea. The last page holds 5 to 10 sentences from the adventure story your student published this unit. Every moment needs a chapter number. Your student taps <strong>Make my booklet</strong>, saves it as a PDF, and uploads it in Canvas. It is graded out of 20 points with a rubric on the page.</div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span>'''),
]
for old, new in R:
    if s.count(old) != 1: sys.exit('expected 1 of %r, found %d' % (old[:70], s.count(old)))
    s = s.replace(old, new)
for w in (26, 27, 28, 29, 30):
    tag = '<div class="wk-n"><b>%d</b>' % w
    i = s.index(tag); j = s.index('</div></div>', i)
    blk = s[i:j]
    if 'wk-link' in blk: sys.exit('link already in %d' % w)
    s = s[:j] + '  <a class="wk-link" href="parent-guide-week-%d.html">Open the Week %d guide →</a>\n      ' % (w, w) + s[j:]
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('div balance')
if s.count('<section') - s.count('</section') != 0: sys.exit('section balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s); print('updated', p)
