#!/usr/bin/env python3
"""Week 26 family guide (parent-guide-week-26.html) in the week 18 guide's look. Every line from the finished
week 26 lessons and Ch. 4-6 of By the Great Horn Spoon! (project doc text). History as on the 26.2 card (Britannica, maritimeheritage.org).
Nov 23 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 26 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 26' in head
B = '''<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 26: Through the Strait</h1>
      <div class="sub"><em>By the Great Horn Spoon!</em> by Sid Fleischman, Chapters 4–6 and a humor day</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Second week of the book</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/btghs/pritchett-beagle-magellan.jpg');background-position:center 45%;" role="img" aria-label="An 1890 engraving of the sailing ship Beagle in the Strait of Magellan, with a snowy mountain behind"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment. A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson. Keep the book nearby.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>The <em>Lady Wilma</em> sails south toward the bottom of South America. Jack hides his pet pig from the cook, and at Rio de Janeiro Praiseworthy offers him a ticket home before the dangerous waters ahead. Jack says no. Then come thirty-seven days of storms and a surprise: Captain Swain has secretly taken the ship through the Strait of Magellan. On the Pacific side the ship sits becalmed, and Jack thinks of a way to save a Frenchman&rsquo;s grape cuttings with a Yankee trader&rsquo;s spoiled potatoes. Day 4 looks back at how Fleischman makes the story funny.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families</div>These chapters are gentle and funny. One small sad moment: Jack&rsquo;s pig is carried off when the thief escapes at Rio (the pig is safe from the cook). The places are real: Rio de Janeiro, Patagonia, the Strait of Magellan and Tierra del Fuego. A short card on Day 2 keeps real history apart from the story.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Humor, tone and characterization.</strong> Your student notices who a joke is on, how calm the telling stays in a storm, and what a funny moment shows about a character.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Self-control.</strong> Praiseworthy calls the scary sea stories &ldquo;Stuff and nonsense,&rdquo; even though he believes every word of them.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">26.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 4 · The Pig Hunt</span><br>The cook comes for Good Luck the pig with a meat cleaver. Jack hides him in the captain&rsquo;s cabin; then the pig gets stuck in a porthole, and Mountain Jim hides him under a barrel. At Rio, Praiseworthy offers Jack a passage home, and Jack chooses to go on. The thief, Cut-Eye Higgins, escapes with Dr. Buckbee&rsquo;s gold map, and the pig goes with him.<br><span class="pill p-extra">A free ticket home?</span><span class="pill p-museum">The bay of Rio de Janeiro, 1837</span></td>
          <td>What does loyalty look like when something ridiculous is at stake?</td>
        </tr>
        <tr>
          <td class="day-n">26.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 5 · Land of Fire</span><br>Snow off Patagonia, then thirty-seven days of storms. Praiseworthy keeps everyone calm. At last the Pacific, with the <em>Sea Raven</em> behind them: Captain Swain secretly took the ship through the Strait of Magellan.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">The Beagle in the Strait, 1890</span></td>
          <td>What does it mean to keep calm when everyone else is terrified?</td>
        </tr>
        <tr>
          <td class="day-n">26.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 6 · Spoiled Potatoes</span><br>A haircut on deck, then no wind and no coal. Mr. Azariah Jones&rsquo;s potatoes are spoiling, and Monsieur Gaunt&rsquo;s grape cuttings are drying up. Jack&rsquo;s idea saves both: poke each cutting into a juicy potato.<br><span class="pill p-museum">A calm sea, 1884</span></td>
          <td>What does it mean to see possibility where everyone else sees failure?</td>
        </tr>
        <tr>
          <td class="day-n">26.4<span>Day 4</span></td>
          <td><span class="ch">Humor and tone · looking back at Chapters 4–6</span><br>Three ways Fleischman makes readers laugh: comic contrast, the straight face, and the ticking clock.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A comic print, about 1850</span></td>
          <td>How does Fleischman make a Gold Rush adventure funny, and why does that matter?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The pig hunt from Chapter 4, ending with Monsieur Gaunt&rsquo;s &ldquo;But rats &mdash; oui!&rdquo; Your student reads it once to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up: dialogue punctuation, the roots rid/ris and lud/lus, dialogue tags and speech spellings, three reading questions, and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>becalmed</b><span>stuck still because there is no wind</span></div>
      <div class="word"><b>strait</b><span>a narrow passage of water joining two larger bodies of water</span></div>
      <div class="word"><b>headwinds</b><span>winds blowing straight against a ship</span></div>
      <div class="word"><b>monotony</b><span>boring sameness, day after day</span></div>
      <div class="word"><b>ludicrous</b><span>so silly it is laughable</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Roots</div><strong>rid / ris</strong> mean laugh and <strong>lud / lus</strong> mean play.<span class="eg">ridiculous · derision · ludicrous · illusion</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Dialogue tags, and speech spellings</strong> where an apostrophe takes the place of a missing letter.<span class="eg">bellowed · muttered · stammered · eatin&rsquo; = eating</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Dialogue punctuation and paragraphing:</strong> commas inside the quotation marks, and a new paragraph for each new speaker.<span class="eg">&ldquo;Pig?&rdquo; said Praiseworthy. &ldquo;What pig?&rdquo;</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">🧭 Through the Strait</div>The week&rsquo;s word game. The ship works west through a map of the Strait of Magellan. At each narrows your student picks the channel with the right word (a real laugh or play root, or a speech spelling with the apostrophe in the right place). Each narrows passed lights a fire on the shore of Tierra del Fuego.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: self-control</div>After reading, your student sorts everyday examples, picks the calmest moment in the storms, rates Jack&rsquo;s self-control when Praiseworthy gives his idea away, and on Day 4 picks the moment of most self-control in the week.</div>
      <div class="box b-sky"><div class="box-label">🗺️ Real history, kept apart</div>A short card on Day 2: the real Strait of Magellan (about 350 miles long, first sailed by Europeans in 1520), how Tierra del Fuego got its name from the fires of the people who lived there, and a real steamship, the SS <em>California</em>, that took the same route in 1848&ndash;49.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer, every day</div>One line from the book a day, chosen to show voice, dialogue and reaction, like &ldquo;You mean to say, sir,&rdquo; said Mr. Azariah Jones, turning white, &ldquo;that we&rsquo;ve been bouncing around in that awful place?&rdquo;</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: Drafting the Adventure Scene</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Last week&rsquo;s plan becomes a scene. <strong>Day 1:</strong> jot who is there, where it happens, what goes wrong and one line the hero says, then start in the middle of the action. <strong>Day 2:</strong> keep drafting, with sentence frames for help. <strong>Day 3:</strong> revise with a checklist (dialogue punctuated correctly, a new paragraph for each speaker, a reaction that shows a feeling, a hero who sounds like themself). <strong>Day 4:</strong> add one comic moment and submit.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: Voice and Diction in a Comic Poem</h2></div>
    <div class="poem-wrap">
      <div class="poem">&rsquo;Twas brillig, and the slithy toves<br>&nbsp;&nbsp;Did gyre and gimble in the wabe;<br>All mimsy were the borogoves,<br>&nbsp;&nbsp;And the mome raths outgrabe.<small>Lewis Carroll, &ldquo;Jabberwocky&rdquo; (1871)</small></div>
      <div><p><strong>Diction</strong> is word choice. In &ldquo;Jabberwocky&rdquo; Carroll invents words from sounds we know, and two of them, <em>chortle</em> and <em>galumph</em>, became real English words. On Day 4, &ldquo;You Are Old, Father William&rdquo; is a comic conversation in verse: each speaker has his own <strong>voice</strong>, and the father says ridiculous things with a perfectly straight face, a bit like Praiseworthy.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Praiseworthy offered Jack a ticket home at Rio. What did Jack say, and why?</span><span class="listen">Listen for: he wouldn&rsquo;t turn back; they were partners; Praiseworthy was checking he really wanted to go on (&ldquo;You&rsquo;ll do, Master Jack&rdquo;).</span></li>
      <li><span class="q">Why didn&rsquo;t Jack see the fires of Tierra del Fuego?</span><span class="listen">Listen for: the ship never went around Cape Horn; Captain Swain secretly took it through the Strait of Magellan.</span></li>
      <li><span class="q">What is the real Strait of Magellan?</span><span class="listen">Listen for: a narrow passage at the tip of South America, about 350 miles long; Magellan&rsquo;s ships sailed it in 1520.</span></li>
      <li><span class="q">How did spoiled potatoes save the grape cuttings?</span><span class="listen">Listen for: each cutting was poked into a juicy potato to keep it alive; Jack knew they were juicy from being a stowaway.</span></li>
      <li><span class="q">What do rid/ris and lud/lus mean? Name a word for each.</span><span class="listen">Listen for: laugh (ridiculous, derision); play (ludicrous, illusion).</span></li>
      <li><span class="q">Read me a line of dialogue from your scene. Where do the commas go?</span><span class="listen">Listen for: inside the closing quotation marks, and a new paragraph for each new speaker.</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 reading questions, that day&rsquo;s Word Study response, the Read Like a Writer box and the Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 4 pig hunt</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers with a detail from the chapter, dialogue punctuated correctly, and a scene where the hero sounds like a real person.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Say it two ways:</strong> one person says &ldquo;What pig?&rdquo; calmly, then in a panic. Which is funnier, and why?</li>
        <li><strong>Laugh or play?</strong> Name a word, and let your student say if it has rid/ris, lud/lus, or neither.</li>
        <li><strong>Find the strait:</strong> trace the Strait of Magellan on a map or globe, between South America and Tierra del Fuego.</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong><em>By the Great Horn Spoon!</em></strong> by Sid Fleischman · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 27</h2></div>
    <p><strong>Chapters 7&ndash;9.</strong> The race to San Francisco comes to its end, and Jack and Praiseworthy set out for the gold fields.</p>
  </section>

  <p class="foot"><a href="parent-guide-btghs-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole By the Great Horn Spoon! unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 26 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-26.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-26.html')
