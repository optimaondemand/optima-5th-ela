#!/usr/bin/env python3
"""Week 31 family guide (parent-guide-week-31.html) in the week 18 guide's look. Every line from the finished week 31 lessons
(cross-text comparison; three real primary sources: Bigler 1848, Taylor 1850, Harkins 1831). Nov 24 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 31 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 31' in head
B = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 31: Two Books, One Idea</h1>
      <div class="sub">The year in review: comparing two of this year&rsquo;s five novels</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">No new chapters</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/year/fragonard-young-girl-reading.jpg');background-position:center 30%;" role="img" aria-label="A painting of a girl in a yellow dress reading a small book"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → the day&rsquo;s main work (Plan, Sources, Draft or Reviewer&rsquo;s Eyes) → Assignment. A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>There is no new chapter this week. Your student has read five novels this year: <em>The Witch of Blackbird Pond</em>, <em>Johnny Tremain</em>, <em>Carry On, Mr. Bowditch</em>, <em>How I Became a Ghost</em> and <em>By the Great Horn Spoon!</em> Now they choose one theme (courage, independence or survival) and two of those novels, and write a five-paragraph essay comparing how the two books treat it. The essay is organized by <strong>categories</strong>, so both books sit side by side in each paragraph, and one paragraph uses a real voice from the time.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families: three real primary sources</div>On Day 2 your student reads three short real sources and picks one for the essay. <strong>Henry Bigler&rsquo;s diary</strong> line from Sutter&rsquo;s Mill on January 24, 1848, in his own spelling. <strong>Bayard Taylor</strong>, a reporter who landed in San Francisco in August 1849. And <strong>George W. Harkins</strong>, a Choctaw leader, writing in 1831 as the Choctaw people were forced to leave Mississippi, the real history behind <em>How I Became a Ghost</em>: &ldquo;We go forth sorrowful, knowing that wrong has been done.&rdquo; Students met all three earlier in the year. A short background card, clearly marked as written by Optima, gives the real time and place of each novel. Nothing on the page is a made-up &ldquo;historical&rdquo; source.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Comparing across texts.</strong> Your student sets a lens, reads real sources closely, rereads to test a claim, and finally reads their own essay the way a reviewer would.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Wisdom.</strong> Knowing what matters and making good choices with what you know, like Nat Bowditch checking every figure because sailors&rsquo; lives depend on it.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>The work</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">31.1<span>Day 1</span></td>
          <td><span class="ch">Plan</span><br>Choose a theme and two novels, write a comparison claim, and plan two categories with evidence from each book.<br><span class="pill p-museum">Plan of the Colony of Connecticut, 1766</span></td>
          <td>What do two of the year&rsquo;s novels say, together, about one big idea?</td>
        </tr>
        <tr>
          <td class="day-n">31.2<span>Day 2</span></td>
          <td><span class="ch">Real sources and the first paragraphs</span><br>Read three real primary sources, choose one, and draft the opening and the first category paragraph.<br><span class="pill p-extra">Real history: who was real?</span><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Paul Revere&rsquo;s view of Boston, 1768</span></td>
          <td>What does a real voice from the time add that a novel cannot?</td>
        </tr>
        <tr>
          <td class="day-n">31.3<span>Day 3</span></td>
          <td><span class="ch">Finish and revise</span><br>Write the second category, the real-voice paragraph and the closing, then revise all five paragraphs with a checklist.<br><span class="pill p-museum">The Salem ship Mount Vernon, 1799</span></td>
          <td>Does the claim still hold when you go back to the books?</td>
        </tr>
        <tr>
          <td class="day-n">31.4<span>Day 4</span></td>
          <td><span class="ch">Reviewer&rsquo;s eyes and submit</span><br>Read the essay as if someone else wrote it, argue the other side, make two careful revisions and submit.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Fragonard, Young Girl Reading</span></td>
          <td>Where does the essay need a reason more than another example?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">Your student picks one of five passages, one from each novel (all copied straight from the books), practices it three times, and <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point check: comparison sentences, the year&rsquo;s roots and spelling, a word in context from a real 1850 source, telling a primary source from other kinds, a claim that names a similarity and a difference, the poem, and two short writing items.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>theme</b><span>the big idea a story is about</span></div>
      <div class="word"><b>category</b><span>a group you sort ideas into</span></div>
      <div class="word"><b>primary source</b><span>something made at the time by someone who was there</span></div>
      <div class="word"><b>transition</b><span>a word that joins ideas, like however</span></div>
      <div class="word"><b>reasoning</b><span>the sentences that explain why your evidence proves your point</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Roots, all year</div>A look back at the year&rsquo;s root families: <strong>aud</strong> (hear), <strong>scrib, script</strong> (write), <strong>dict</strong> (say), <strong>spect</strong> (look), <strong>curr, tract</strong> (run, pull), <strong>fort, val</strong> (strong, worth), <strong>nav</strong> (ship), <strong>port</strong> (carry).<span class="eg">verdict · navigator · manuscript · spectators</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>The year&rsquo;s tricky words,</strong> checked in your student&rsquo;s own essay.<span class="eg">separate · definitely · occurred · embarrass</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Comparison sentences</strong> that hold two books at once.<span class="eg">While Kit Tyler stands trial in Wethersfield, Johnny Tremain carries messages in Boston.</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">📚 Two Books, One Root</div>The week&rsquo;s word game is a memory game. Your student turns over word cards to find two words with the same root, like <em>verdict</em> and <em>dictionary</em>. Each pair ties two books on a little bookshelf together with a gold thread.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: wisdom</div>Your student sorts everyday examples of wisdom, picks the wisest moment from the year&rsquo;s books, rates a clever plan of Praiseworthy&rsquo;s, and names the wisest character of the year.</div>
      <div class="box b-sky"><div class="box-label">🗺️ Who was real?</div>A Day 2 card sorts made-up characters from real people: Nathaniel Bowditch, Paul Revere and the Boston patriots, the Choctaw leader Pushmataha, and James Marshall and John Sutter.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer: categories</div>Each day a short model shows how to sort a comparison into categories, so the two books stand side by side instead of one after the other.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: The Comparison Essay</h2><span class="tag">Part 1 of the year-end portfolio</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Five paragraphs: <strong>1.</strong> an opening with both novels and the claim; <strong>2&ndash;3.</strong> two category paragraphs, each with evidence from both books; <strong>4.</strong> a real voice from the chosen primary source; <strong>5.</strong> a closing that says what the two books say together. This essay is the first part of the year-end portfolio your student finishes next week.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: The Benchmark Poem</h2></div>
    <div class="poem-wrap">
      <div class="poem">The buffaloes are gone.<br>And those who saw the buffaloes are gone.<small>Carl Sandburg, &ldquo;Buffalo Dusk&rdquo; (1920), first two lines</small></div>
      <div><p>This is the poem your student has been building toward all year. On Day 2 they name every element at work in it: its shape, its repetition, the missing rhyme and the one enormous middle line. On Day 4 they explain how those choices work together to make a poem about loss.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Which two books did you choose, and what idea do they share?</span><span class="listen">Listen for: a theme (courage, independence or survival) and two novels.</span></li>
      <li><span class="q">How do the two books treat that idea differently?</span><span class="listen">Listen for: a real difference, with a moment from each book.</span></li>
      <li><span class="q">What is a primary source? Which one did you pick?</span><span class="listen">Listen for: made by someone who was there; Bigler, Taylor or Harkins.</span></li>
      <li><span class="q">What would someone who disagrees with you say?</span><span class="listen">Listen for: a fair other side, and an answer with evidence.</span></li>
      <li><span class="q">Which characters this year were real people?</span><span class="listen">Listen for: Nathaniel Bowditch, Paul Revere, Pushmataha, James Marshall.</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> the day&rsquo;s questions, the Word Study response, the Read Like a Writer box and that day&rsquo;s part of the essay, copied and pasted into Canvas</li>
        <li><strong>Day 4:</strong> the final five-paragraph comparison essay</li>
        <li><strong>Fluency:</strong> a recording of one of the five passages</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> a claim that names a similarity and a difference, both books in every category, real moments or exact words as evidence, and a reason for why the difference matters.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Compare two movies</strong> you both know in one category, like how the hero gets help.</li>
        <li><strong>Find a primary source</strong> at home: an old letter, a photo with a date, a family recipe card.</li>
        <li><strong>Root hunt:</strong> find a word with <em>port</em> or <em>spect</em> on a sign or a box.</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong>The two novels your student chooses</strong> (and their notes from the year) · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 32</h2></div>
    <p><strong>Letter to a Future 5th Grader.</strong> The last week of the year: your student writes a real letter recommending one of the year&rsquo;s books to next year&rsquo;s fifth graders, with postcards, a word gift and a recorded read-aloud.</p>
  </section>

  <p class="foot">Optima Academy Online · 5th Grade ELA · Week 31 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
"""
io.open('parent-guide-week-31.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-31.html')
