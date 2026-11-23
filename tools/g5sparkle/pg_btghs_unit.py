#!/usr/bin/env python3
"""By the Great Horn Spoon! unit family guide (parent-guide-btghs-unit.html), in the HBG unit guide's look.
Week skills from the v2_poetry scope (weeks 25-30); book facts from the book text (all 18 chapters); history
as on lesson 25.1 (LOC, NPS, PBS, Calisphere, NLM). Hard parts named calmly, as Bethany asked (Nov 22 2026)."""
import io, re
s = io.open('parent-guide-hbg-unit.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>By the Great Horn Spoon! Unit Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert 'Horn Spoon! Unit' in head
def wk(n, ch, theme, summ, skills, link=False):
    sk = ''.join('<span class="sk"><i>%s</i>%s</span>' % x for x in skills)
    a = '\n        <a class="wk-link" href="parent-guide-week-%d.html">Open the Week %d guide →</a>' % (n, n) if link else ''
    return ('      <div class="wk"><div class="wk-n"><b>%d</b><span>Week</span></div><div class="wk-body">\n        <div class="wk-top"><span class="wk-ch">%s</span><span class="theme">%s</span></div>\n'
            '        <p class="wk-sum">%s</p>\n        <div class="skills">%s</div>%s\n      </div></div>\n') % (n, ch, theme, summ, sk, a)
WEEKS = ''.join([
 wk(25, 'Background + Chapters 1–3', 'The rush is on', 'The real Gold Rush first, then the novel: Jack and Praiseworthy stow away in potato barrels, shovel coal to pay their way, and catch a thief with a pig and some coal dust.',
    [('Reading', 'background and adventure structure'), ('Grammar', 'prepositional phrases for setting'), ('Spelling', 'place names and Gold Rush words'), ('Roots', 'aud, or')], True),
 wk(26, 'Chapters 4–6', 'Around the bottom of the world', 'A pig hunt on board, a stop in Rio de Janeiro, and storms near the tip of South America.',
    [('Reading', 'humor, tone and character'), ('Grammar', 'dialogue punctuation'), ('Spelling', 'words in quoted speech'), ('Roots', 'rid/ris, lud/lus')]),
 wk(27, 'Chapters 7–9', 'The race to San Francisco', 'The race between two ships ends, and the partners land in a city full of gold-seekers, with no money for the riverboat.',
    [('Reading', 'problem-solving, cause and effect'), ('Grammar', 'compound and complex sentences'), ('Spelling', '-tion and -sion'), ('Roots', 'curr/curs, tract')]),
 wk(28, 'Chapters 10–12', 'To the diggings', 'A stagecoach ride into the mountains, a holdup, and a new name in a mining town.',
    [('Reading', 'how events build a theme'), ('Grammar', 'transitions and opening phrases'), ('Spelling', '-ity, -ment, -ness'), ('Roots', 'fort, val/valid')]),
 wk(29, 'Chapters 13–15', 'Prospecting', 'Hard work in the gold fields, a burro with opinions, and a run-in with a grizzly.',
    [('Reading', 'voice and tone'), ('Grammar', 'sentence variety'), ('Spelling', 'word families'), ('Roots', '-ous, -ive, -ity')]),
 wk(30, 'Chapters 16–18', 'Gold, and what it is worth', 'The partners find out what a fortune is really made of. The book ends back at the Long Wharf in San Francisco.',
    [('Reading', 'plot, character, humor and theme together'), ('Grammar', 'editing'), ('Spelling', 'editing for spelling'), ('Roots', 'review')]),
])
B = '''<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Unit: By the Great Horn Spoon!</h1>
      <div class="sub">Weeks 25–30 · 18 chapters · Sid Fleischman</div>
      <div class="chips">
        <span class="chip">6 weeks</span>
        <span class="chip">24 lessons</span>
        <span class="chip">A weekly Check-In</span>
        <span class="chip">Your student writes an adventure story</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/btghs/currier-way-they-go.jpg');background-position:center 45%;" role="img" aria-label="An 1849 comic print of gold-seekers rushing to board a ship for California"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment. A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn’t turned in until it’s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn’t work inside a lesson. Keep the novel nearby.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📕</span><h2>About the Book</h2></div>
    <p><em>By the Great Horn Spoon!</em> by Sid Fleischman was first published in 1963. It is a comic adventure. In January 1849, twelve-year-old Jack Flagg and Praiseworthy, his family&rsquo;s English butler, stow away on a ship from Boston bound around Cape Horn for California. They want to strike gold and save Jack&rsquo;s Aunt Arabella from losing the family home. On the way, the calm, clever butler and the eager boy become true partners.</p>
    <p>We read it because it is funny, fast and full of real Gold Rush detail: the long sea voyage, crowded San Francisco, the mining camps, and the prices miners paid. Each week your student also learns the skills good adventure writers use, and writes an adventure of their own.</p>
    <p class="quote">&ldquo;It was not once upon a time — it was precisely the twenty-seventh day of January in the year 1849.&rdquo;<small>Chapter 1</small></p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>Story and History: What&rsquo;s What</h2></div>
    <div class="grid2">
      <div class="box b-sky"><div class="box-label">Made up</div>Jack, Praiseworthy, the ships <em>Lady Wilma</em> and <em>Sea Raven</em>, and the race between them are invented. So are the tall tales the miners tell about each other.</div>
      <div class="box b-gold"><div class="box-label">Real</div>The Gold Rush, the routes around Cape Horn and across Panama, San Francisco&rsquo;s Long Wharf, Hangtown (now Placerville) and Sutter&rsquo;s Mill are real. Day 1 of the unit teaches the history first, with real numbers from the Library of Congress, the National Park Service and others.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🗓️</span><h2>How a Week Works</h2></div>
    <p>Every week has four lessons, one fluency reading, and a Check-In. Each lesson follows the same path, so your student always knows what comes next. Across the four days, the grammar and word skills build:</p>
    <div class="rhythm">
      <div><b>Day 1</b>Notice: work out the rule</div>
      <div><b>Day 2</b>Identify: find and sort</div>
      <div><b>Day 3</b>Use: build it yourself</div>
      <div><b>Day 4</b>Explain: say why it works</div>
    </div>
    <ul class="routines">
      <li><span>📚</span><strong>What Good Readers Do:</strong> one reading habit to try in the chapters</li>
      <li><span>✏️</span><strong>Daily Oral Language:</strong> fix a sentence, often from the book</li>
      <li><span>🌱</span><strong>Word study:</strong> a Latin root, a spelling pattern, and vocabulary from the chapters</li>
      <li><span>🧩</span><strong>Grammar:</strong> one sentence skill each week, practiced with sentences from the book</li>
      <li><span>🪶</span><strong>Poetry Corner:</strong> a short classic poem on Days 2 and 4</li>
      <li><span>✅</span><strong>Virtue Watch:</strong> a virtue found in the chapter (loyalty in Week 25)</li>
      <li><span>📖</span><strong>Read Like a Writer:</strong> one sentence from the book to notice and try</li>
      <li><span>🎲</span><strong>A word game:</strong> a new one each week, tied to the chapters</li>
      <li><span>🖼️</span><strong>Real pictures:</strong> old maps, prints and paintings from the Gold Rush years</li>
      <li><span>🎙️</span><strong>Fluency:</strong> a short passage read three times, then recorded</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🗺️</span><h2>The Unit, Week by Week</h2></div>
    <div class="weeks">
''' + WEEKS + '''    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Plan</span><span class="now">Draft</span><span class="now">Add Craft</span><span class="now">Revise &amp; Edit</span><span class="now">Publish</span></div>
    <p>Across the six weeks, your student writes an adventure story of their own, inspired by Jack and Praiseworthy but completely their own. Week 25 is the plan: a hero, a problem, a setting, and what is at stake. Then a draft, scenes with dialogue and voice, a middle that raises the stakes, a revision for voice and tone, and a finished, edited story. Each day also has a <strong>Read Like a Writer</strong> box with one of Fleischman&rsquo;s sentences to study and imitate.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner</h2></div>
    <p>On Days 2 and 4, your student reads a short classic poem. This unit starts with humor and tone (Edward Lear&rsquo;s &ldquo;The Jumblies&rdquo; and Lewis Carroll&rsquo;s &ldquo;The Walrus and the Carpenter&rdquo; in Week 25), then moves through voice, rhythm and theme. Read the poems aloud together; they are meant to be heard.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📋</span><h2>How Learning Is Checked</h2></div>
    <div class="grid3">
      <div class="box b-sky"><div class="box-label">Every lesson</div>Chapter questions answered with evidence from the book, plus word-study and writing responses, submitted in Canvas.</div>
      <div class="box b-gold"><div class="box-label">Every week</div>A fluency recording, plus a <strong>Check-In</strong> in Canvas covering grammar, word parts, spelling, reading, and short writing.</div>
      <div class="box b-green"><div class="box-label">End of unit</div>The finished adventure story, plus an end-of-novel project that your student&rsquo;s teacher will share in Week 30.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💛</span><h2>Good to Know Ahead of Time</h2></div>
    <p class="small">This is a funny book, and most of it is gentle. It was also written in 1963 about 1849, and a few parts show the attitudes of those times. The lessons don&rsquo;t hide them. They name them plainly and calmly, and Day 1 of the unit tells the real history the book leaves out. It&rsquo;s fine to pause and say, &ldquo;That&rsquo;s how people talked then, and here&rsquo;s why it&rsquo;s hurtful.&rdquo;</p>
    <div class="grid2">
      <div class="box b-rose"><div class="box-label">Native Californians</div>The book uses words for Native people that were common then and hurtful now. In Chapter 1, Jack imagines &ldquo;wild Indians&rdquo; to fight off. In Chapters 9 and 15, the characters call California&rsquo;s Native people &ldquo;Digger Indians,&rdquo; a name miners used as an insult, and treat them as curiosities. The book doesn&rsquo;t mention what the Gold Rush cost them: about 150,000 Native Californians lived there in 1848, and twelve years later only about 30,000 were left. Their nations are still in California today.</div>
      <div class="box b-rose"><div class="box-label">Chinese and Mexican miners</div>In Chapter 8, a Chinese laundryman is drawn as a type, with a pigtail and broken English, and in another place a character says &ldquo;mighty white of you&rdquo; to mean kind. Chinese, Mexican and Chilean miners were a large part of the real Gold Rush, and many faced unfair taxes and violence.</div>
      <div class="box b-plum"><div class="box-label">Rough-and-tumble action</div>A holdup by masked robbers, a near-hanging played for comedy in a mining camp, a grizzly bear, a bare-knuckle boxing match, and a steamboat explosion. No one the reader cares about is badly hurt.</div>
      <div class="box b-plum"><div class="box-label">Talk about money</div>The partners are trying to save a family home. The book is honest that most miners found little gold and that prices in the gold fields were sky-high.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🤝</span><h2>How to Help (Without Doing It for Them)</h2></div>
    <div class="grid2">
      <div>
        <h3 style="font-size:19px;margin-bottom:6px;">Try this</h3>
        <ul class="check">
          <li>Ask &ldquo;Where in the book does it say that?&rdquo; when your student answers a question.</li>
          <li>Ask &ldquo;Is that the story or the history?&rdquo; when the novel mentions something real.</li>
          <li>Read a funny scene aloud together and let your student do the voices.</li>
          <li>Be the audience for the fluency reading and the finished adventure story.</li>
        </ul>
      </div>
      <div>
        <h3 style="font-size:19px;margin-bottom:6px;">Try to avoid</h3>
        <ul class="check dont">
          <li>Typing or wording answers for them. Teachers need to see your student&rsquo;s own thinking.</li>
          <li>Fixing their story drafts. Revising is a lesson of its own.</li>
          <li>Telling them how the book ends.</li>
        </ul>
      </div>
    </div>
  </section>

  <p class="foot"><a href="parent-guide-week-25.html" style="color:#1F6FA8;font-weight:700;">Open the Week 25 guide →</a><br><br>Optima Academy Online · 5th Grade ELA · By the Great Horn Spoon! Unit Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-btghs-unit.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-btghs-unit.html')
