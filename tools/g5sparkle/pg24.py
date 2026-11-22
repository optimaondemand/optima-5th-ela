#!/usr/bin/env python3
"""Week 24 family guide (parent-guide-week-24.html) from the week 18 guide's look. Every line from the
finished week 24 lessons, Ch. 28-29 of the book (planning docs/hbg_ocr.txt) and the two sources on the pages (the 1830 treaty; Harkins's 1831 letter). Nov 22 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head, body = s[:s.index('<body>')], s[s.index('<body>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 24 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 24' in head
B = '''<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 24: The Story and the Record</h1>
      <div class="sub"><em>How I Became a Ghost</em> by Tim Tingle, Chapters 28–29 and two real sources</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Ch. 28–29 · end of the novel</span>
        <span class="chip">Check-In at week’s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/hbg/boisseau-louisiana-indians-bayou.jpg');background-position:center 50%;" role="img" aria-label="An 1847 painting of a family walking beside a bayou under tall trees"></div>
  </header>

  <!-- HOW THE LESSON PAGES WORK -->
  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment. A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There’s a box for each one, including the Daily Oral Language sentence.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn’t turned in until it’s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn’t work inside a lesson. Keep the book nearby.</li>
    </ul>
  </section>

  <!-- AT A GLANCE -->
  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>The novel ends this week. In Chapter 28 the wolf returns, and Naomi and Joseph save the life of Leader, the man who vowed Naomi would die. Leader lets her go home. The ghost of a famous Choctaw chief honors the four young people. In Chapter 29 the families share a meal of corn, with a hard winter and the rest of the Trail still ahead. Then your student reads two real sources from the same years, part of a treaty and part of a letter by a Choctaw chief, and writes a paragraph comparing the novel with the record.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A heads-up for families</div>Chapter 28 has one short, fierce fight: a panther kills a wolf, and there is blood. No person is hurt, and the book ends gently. The harder part this week is the real history. The Choctaw people were forced to leave their homeland in Mississippi, and many died on the journey. The lessons say this plainly and calmly, keep the made-up story separate from the real record, and close on the fact that the Choctaw Nation is still here today, in Oklahoma.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Comparing historical fiction with real sources.</strong> A novel can show what something felt like. A primary source, written at the time, shows what was agreed, decided or said. Your student learns to say which is which.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Doing right, even by an enemy.</strong> When Leader asks Naomi why she saved him, she answers that it was the right thing to do.</div>
    </div>
    <p class="quote">&ldquo;It was the right thing to do. It is the Choctaw way.&rdquo;<small>Naomi, Chapter 28</small></p>
  </section>

  <!-- DAY BY DAY -->
  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">24.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 28 · Panther and the Wolf</span><br>The wolf leaps for Leader. Joseph, as the panther, stops it, and Naomi says, &ldquo;We cannot let this happen.&rdquo; Leader sends her home to her parents. The ghost of Chief Pushmataha honors the four young Choctaws.<br><span class="pill p-museum">Audubon&rsquo;s wolf</span><span class="pill p-extra">Would you help your enemy?</span></td>
          <td>What can a story tell you that a record cannot?</td>
        </tr>
        <tr>
          <td class="day-n">24.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 29 · Pushmataha and the Choctaw Four</span><br>The soldiers bring corn to every wagon. Naomi is back with her mother and father and insists on cooking. The winter is fierce, but the families are together.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A portrait of the real Pushmataha</span></td>
          <td>Which moments would you want to check against a real record?</td>
        </tr>
        <tr>
          <td class="day-n">24.3<span>Day 3</span></td>
          <td><span class="ch">Source study · Two real sources</span><br>Part of the Treaty of Dancing Rabbit Creek (1830), which set the removal for the falls of 1831, 1832 and 1833. Part of a letter Choctaw chief George W. Harkins wrote in 1831 as he left Mississippi with his people.<br><span class="pill p-museum">Boisseau&rsquo;s family by a bayou</span></td>
          <td>Who wrote this, when, and why?</td>
        </tr>
        <tr>
          <td class="day-n">24.4<span>Day 4</span></td>
          <td><span class="ch">Source comparison · End of the unit</span><br>Your student rereads the two sources, looks back at Chapters 28 and 29, and writes the final comparison paragraph.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Catlin&rsquo;s portrait of a Choctaw chief</span></td>
          <td>What do the novel and the sources show together?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The opening of Chapter 29: a new wagon, corn for everyone, and Naomi home with her family. Your student reads it once to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up on the week: formal style and source transitions, history words, taking long words apart, two reading questions (one on the novel and the sources), and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- WORDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>lifeless</b><span>without life; not moving or breathing</span></div>
      <div class="word"><b>survived</b><span>stayed alive through something dangerous</span></div>
      <div class="word"><b>honor</b><span>to show great respect for someone</span></div>
      <div class="word"><b>reunited</b><span>brought back together after being apart</span></div>
      <div class="word"><b>protector</b><span>someone who keeps another person safe from harm</span></div>
    </div>
    <div class="skills">
      <div class="box b-sky"><div class="box-label">The vocabulary of history</div>Six words a historian uses with care: a <strong>claim</strong> is a statement put forward as true, <strong>evidence</strong> supports it, and <strong>reasoning</strong> explains how. A <strong>treaty</strong> is a formal agreement between nations.<span class="eg">claim · evidence · reasoning · treaty · removal · nation</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Long words are short words with parts added.</strong> Students sort history words by their endings and roots.<span class="eg">settlement · declaration · sovereignty · national · testimony</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Formal style and source transitions.</strong> An essay uses exact words, no slang and no contractions, and says where each fact came from.<span class="eg">According to the treaty of 1830, … In Tingle&rsquo;s novel, …</span></div>
    </div>
  </section>

  <!-- EXTRAS -->
  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="extras">
      <div class="box b-plum"><div class="box-label">🌽 Ears of Corn</div>The week&rsquo;s word game. Each long word is an ear of corn. Your student taps the parts added to the front or the end (the husks) to find the base word inside: <em>mis | treat | ment</em>. Three words a day.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: courage</div>After reading, your student sorts moments, keeps a log, rates a moment on a meter, and on Day 4 picks the strongest moment of courage in the week. One moment comes from real history: Harkins choosing to go with his people.</div>
      <div class="box b-sky"><div class="box-label">🖼️ Art from the time</div>Each lesson opens with a print or painting from the 1820s to 1840s, including a portrait of the real Pushmataha, painted in 1824. He was a real Choctaw chief and a general. He died six years before the novel begins, which is why he arrives in the story as a ghost.</div>
      <div class="box b-green"><div class="box-label">📜 Two real sources</div>Day 3 puts real words from 1830 and 1831 on the page, with a plain-words version under each. The treaty gives the dates. The letter gives a Choctaw leader&rsquo;s own voice: &ldquo;We go forth sorrowful, knowing that wrong has been done.&rdquo;</div>
    </div>
  </section>

  <!-- WRITING -->
  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: A Source Comparison</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Your student writes one paragraph that sets the novel beside a real source. <strong>Day 1:</strong> plan a claim, one detail from the novel, one line from a source, and the reasoning. <strong>Day 2:</strong> write a full draft in formal style. <strong>Day 3:</strong> revise with a checklist: formal style, two source transitions, a claim with evidence and reasoning, and every fact tied to its source. <strong>Day 4:</strong> write the final paragraph, and tell what a story told by a ghost taught them about real history.</p>
    <p>Every day also has a <strong>Read Like a Writer</strong> box with one of the book&rsquo;s sentences, like &ldquo;The Trail still lay before us.&rdquo; This week the boxes model claim, evidence and reasoning.</p>
  </section>

  <!-- POETRY -->
  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: A Poem as a Primary Source</h2></div>
    <div class="poem-wrap">
      <div class="poem">Ye say they all have passed away,<br>That noble race and brave,<br>That their light canoes have vanished<br>From off the crested wave;<small>Lydia Huntley Sigourney, &ldquo;Indian Names&rdquo; (1834), opening lines, Day 2. On Day 4: William Cullen Bryant, &ldquo;An Indian at the Burial-Place of His Fathers&rdquo; (1824).</small></div>
      <div><p>Both poems were written in the years of removal, so each is a piece of history. Sigourney answers Americans who said Native people had &ldquo;passed away.&rdquo; Bryant, a white poet, imagines a Native speaker. On Day 4 your student sets his poem beside Harkins&rsquo;s own letter and asks which one to trust for how Choctaw people felt. Both poets use the word of their time, &ldquo;Indian.&rdquo; The lessons explain that today we name each nation.</p><p><strong>How to help:</strong> Read the Sigourney lines aloud together. Ask what she says is still here, even after people were forced away.</p></div>
    </div>
  </section>

  <!-- ASK AT HOME -->
  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Why did Naomi help save Leader?</span><span class="listen">Listen for: &ldquo;It was the right thing to do. It is the Choctaw way.&rdquo; And afterward Leader let her go home.</span></li>
      <li><span class="q">Was Pushmataha a real person?</span><span class="listen">Listen for: yes. A real Choctaw chief and general who died in 1824. In the novel he comes as a ghost.</span></li>
      <li><span class="q">What is a primary source? Name the two you read.</span><span class="listen">Listen for: something written at the time. Part of a treaty from 1830 and part of a letter by a Choctaw chief from 1831.</span></li>
      <li><span class="q">What is one thing the novel and the real record do not agree on?</span><span class="listen">Listen for: the novel&rsquo;s first page says 1830. The treaty set the real removal for 1831 to 1833.</span></li>
      <li><span class="q">What can the novel show you that the treaty cannot?</span><span class="listen">Listen for: what it felt like for one family; a ten-year-old&rsquo;s voice; Choctaw beliefs about the people who have died.</span></li>
      <li><span class="q">Read me your comparison paragraph. Where is your reasoning?</span><span class="listen">Listen for: a claim, a detail from the novel, a line from a source, and a sentence that explains how they fit together.</span></li>
    </ol>
  </section>

  <!-- TURN IN + TRY AT HOME -->
  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 questions answered with evidence, the grammar response, the Read Like a Writer box and that day&rsquo;s Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 29 passage</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
        <li><strong>End-of-novel project:</strong> &ldquo;A Ghost&rsquo;s-Eye View,&rdquo; a four-page booklet turned in as one PDF. It has its own page in Canvas</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers that say where each fact comes from, formal sentences with no slang, and a paragraph with a claim, evidence from both texts, and reasoning.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Says who?</strong> When someone states a fact at dinner, ask, &ldquo;According to what?&rdquo; Let your student name the source.</li>
        <li><strong>Casual to formal:</strong> say a slangy sentence and let your student say it the way an essay would.</li>
        <li><strong>Peel a word:</strong> find a long word on a cereal box or in the news and take off its front and end parts to find the base.</li>
      </ul>
    </section>
  </div>

  <!-- NEED -->
  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong><em>How I Became a Ghost</em></strong> by Tim Tingle · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <!-- NEXT WEEK -->
  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 25</h2></div>
    <p><strong>A new book and a new quarter: <em>By the Great Horn Spoon!</em> by Sid Fleischman.</strong> Week 25 begins with the Gold Rush of 1849 and the long sea voyage from Boston to San Francisco.</p>
  </section>

  <p class="foot"><a href="parent-guide-hbg-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole How I Became a Ghost unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 24 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-24.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-24.html')
