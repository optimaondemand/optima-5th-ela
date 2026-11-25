#!/usr/bin/env python3
"""Week 32 family guide (parent-guide-week-32.html) and the closing year-end family guide (parent-guide-year-end.html), in the
week 18 guide's look. Every line from the finished week 32 lessons and the year's finished guides (Nov 25 2026).
Real source on the pages: Louise Clappe ("Dame Shirley"), The Shirley Letters, Letter the Twenty-third (1852), 1922 Russell edition."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
HEAD = s[:s.index('<body>')]
LOGO = '<img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">'
HOWTO = """  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → the day&rsquo;s main work (Reflect, Fluency, Revise or Synthesize) → Assignment. A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson.</li>
    </ul>
  </section>
"""
WEEK = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand">%s Family Guide · 5th Grade ELA</div>
      <h1>Week 32: Letter to a Future 5th Grader</h1>
      <div class="sub">The last week of the year: a real letter to next year&rsquo;s fifth graders</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 recording</span>
        <span class="chip">Year-end project</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/year/vermeer-woman-reading-letter.jpg');background-position:center 30%%;" role="img" aria-label="A painting of a woman in a blue jacket reading a letter in window light"></div>
  </header>

%s
  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>There is no new chapter this week. Your student finishes the year&rsquo;s <strong>Reader-Writer Portfolio</strong> by writing a real letter to next year&rsquo;s fifth graders: which of this year&rsquo;s five novels should they read first, and why? The letter comes with a Reader&rsquo;s Portrait (who your student was as a reader in September, and who they are now), five Book Postcards, a Word Gift of three roots, a P.S., and an envelope your student designs. On Day 4 they record the letter and one poem from the year.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families: real letters and real books</div>Every book quote on the pages this week was checked against the novels. On Day 2 a short card shows a real letter from the Gold Rush: <strong>Louise Clappe</strong>, who signed her letters &ldquo;Dame Shirley,&rdquo; wrote 23 letters to her sister from California mining camps in 1851 and 1852. The card quotes only her goodbye to the camp. The year in review on Day 4 names <em>How I Became a Ghost</em> plainly: the story of a Choctaw boy on his people&rsquo;s forced journey west. Your student&rsquo;s letter is real too; teachers can pass it on to next year&rsquo;s class.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Pulling the year together.</strong> Your student sets a purpose across five books, gathers evidence from two of them, rereads one passage for the author&rsquo;s choices, and names an idea that runs through the whole year.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Wisdom.</strong> Knowing what matters and making good choices with what you know, like Nat Bowditch, who checks his figures and lets the land prove him right.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>The work</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">32.1<span>Day 1</span></td>
          <td><span class="ch">Look back</span><br>Write the Reader&rsquo;s Portrait and five Book Postcards (a pitch, an exact quote and &ldquo;Read this if you&hellip;&rdquo;), then plan the letter: a claim, two reasons and a fair point.<br><span class="pill p-museum">Winslow Homer, The New Novel, 1877</span></td>
          <td>Which book would you hand a new reader first?</td>
        </tr>
        <tr>
          <td class="day-n">32.2<span>Day 2</span></td>
          <td><span class="ch">Read aloud and draft</span><br>Pick a short passage to quote, mark the pauses, practice it three times, then draft the whole letter.<br><span class="pill p-extra">Letters that crossed time</span><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Gabri&euml;l Metsu, Man Writing a Letter</span></td>
          <td>What proof from both books makes the advice believable?</td>
        </tr>
        <tr>
          <td class="day-n">32.3<span>Day 3</span></td>
          <td><span class="ch">Revise</span><br>Three revisions (vague to specific, the honest sentence, the best last line), then a Word Gift of three roots and a P.S.<br><span class="pill p-museum">Gerard ter Borch, Woman Writing a Letter</span></td>
          <td>Would a ten-year-old understand every sentence?</td>
        </tr>
        <tr>
          <td class="day-n">32.4<span>Day 4</span></td>
          <td><span class="ch">Seal and send</span><br>The year in review, the envelope, and the final letter, then the recording and the portfolio booklet.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Johannes Vermeer, Woman Reading a Letter</span></td>
          <td>What one idea from this year would you pass on?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Recording</span></td>
          <td colspan="2">The last fluency recording of the year: your student <strong>reads the letter aloud (2 to 3 minutes), then one poem from the year,</strong> and submits it in Canvas.</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📘<span>Project</span></td>
          <td colspan="2"><strong>The Reader-Writer Portfolio</strong> (one PDF): the Week 31 comparison essay, then the whole letter packet with the envelope, made into a booklet on the project page and uploaded in Canvas.</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point check: final editing (agreement, titles, run-ons), the year&rsquo;s roots and tricky spellings, pacing and tone in two real lines from the novels, a primary source, the poem, and the claim of your student&rsquo;s letter.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>voice</b><span>how a writer sounds on the page</span></div>
      <div class="word"><b>tone</b><span>the feeling in the words</span></div>
      <div class="word"><b>pacing</b><span>where a reader speeds up, slows down and pauses</span></div>
      <div class="word"><b>claim</b><span>the main point you are trying to prove</span></div>
      <div class="word"><b>pitch</b><span>a short line that makes someone want to try something</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Roots, one last time</div>A root from every book&rsquo;s unit: <strong>struct, spect, script</strong> (build, look, write), <strong>rupt, dict</strong> (break, say), <strong>nav, port, graph</strong> (ship, carry, write), <strong>spir, vis, lum</strong> (breathe, see, light), <strong>aud, curr, tract, val</strong> (hear, run, pull, worth).<span class="eg">eruption · portable · illuminate · audition</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>The year&rsquo;s tricky words,</strong> checked in your student&rsquo;s own letter.<span class="eg">separate · definitely · occurred · receive</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>A final editing pass:</strong> capitals, agreement and end marks first.<span class="eg">Each of the boys was changed by the journey.</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">🗺️ The Year&rsquo;s Map</div>The last word game of the year. A map shows five stops, one for each novel&rsquo;s world, from Wethersfield to San Francisco. Each clue asks for a word built from a root your student learned while reading that book, and a right answer lights the stop.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: wisdom</div>Your student sorts a letter writer&rsquo;s choices, picks the wisest moment from the year&rsquo;s books, rates Nat Bowditch&rsquo;s quiet confidence, and chooses the piece of wisdom they would pass on.</div>
      <div class="box b-sky"><div class="box-label">✉️ Letters that crossed time</div>A Day 2 card shows how one real letter, written for one reader in 1852, has been read for more than 170 years.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer: voice, tone and pacing</div>Four real lines from the year&rsquo;s novels: three short sentences that slow down (<em>By the Great Horn Spoon!</em>), a voice in three words (&ldquo;We&rsquo;re partners, sir&rdquo;), a calm tone (<em>Carry On, Mr. Bowditch</em>), and a long list with a short ending (<em>Johnny Tremain</em>).</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: The Letter</h2><span class="tag">Part 2 of the year-end portfolio</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Seal &amp; Send</span></div>
    <p>The letter goes: <strong>Dear future 5th grader,</strong> then the Reader&rsquo;s Portrait, a claim (&ldquo;Read ___ before ___&rdquo;), two reasons with a moment from <em>both</em> books, one fair point for the other book, a closing and a signature. The Word Gift and the P.S. come after. Students write to a ten-year-old who hasn&rsquo;t read either book, so the letter never tells how a book ends.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: A Poem Read Aloud</h2></div>
    <div class="poem-wrap">
      <div class="poem">Greatly shining,<br>The Autumn moon floats in the thin sky;<small>Amy Lowell, &ldquo;Wind and Silver&rdquo; (1925), first two lines</small></div>
      <div><p>On Day 2 your student reads Lowell&rsquo;s short poem three ways (flat, too fast, and the way it asks to be read) and explains what changed. On Day 4 they choose any poem from the year and read it the way it asks to be read, and that poem goes into the final recording.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Which book would you hand a new fifth grader first? Why?</span><span class="listen">Listen for: two novels, and a reason with a moment from each.</span></li>
      <li><span class="q">What kind of reader were you in September? What changed?</span><span class="listen">Listen for: something specific, tied to a book.</span></li>
      <li><span class="q">Read me your favorite line from your letter.</span><span class="listen">Listen for: pauses in the right places and a warm, sure tone.</span></li>
      <li><span class="q">What&rsquo;s one root you would teach a younger kid?</span><span class="listen">Listen for: the root, its meaning and a word built from it.</span></li>
      <li><span class="q">Which poem did you choose to record, and why?</span><span class="listen">Listen for: a poem from the year and one thing about how it sounds.</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> the day&rsquo;s work and that day&rsquo;s part of the letter, copied and pasted into Canvas</li>
        <li><strong>Day 4:</strong> the envelope and the final letter</li>
        <li><strong>Recording:</strong> the letter and one poem, in the Canvas fluency assignment</li>
        <li><strong>Project:</strong> the Reader-Writer Portfolio booklet, one PDF</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> a clear claim, two reasons with evidence from both books, exact quotes with chapters, a voice that sounds like your student, and a recording with pauses where they help.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Be the audience</strong> for the letter before it is recorded.</li>
        <li><strong>Write a letter back:</strong> one book you loved at their age, and why.</li>
        <li><strong>Make a summer stack:</strong> three books your student wants to read next.</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong>The two novels in the letter</strong> (and the year&rsquo;s notes) · <strong>A device that records audio or video</strong> for the final recording</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🎓</span><h2>The Whole Year</h2></div>
    <p>This is the last week of 5th Grade ELA. The <a href="parent-guide-year-end.html" style="color:#1F6FA8;font-weight:700;">year-end family guide</a> looks back at all five novels, the writing, and what comes next.</p>
  </section>

  <p class="foot">Optima Academy Online · 5th Grade ELA · Week 32 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
""" % (LOGO, HOWTO)
YEAR = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand">%s Family Guide · 5th Grade ELA</div>
      <h1>The Year in Reading</h1>
      <div class="sub">32 weeks, five novels, and a reader who grew</div>
      <div class="chips">
        <span class="chip">5 novels</span>
        <span class="chip">32 weeks</span>
        <span class="chip">Year-end portfolio</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/year/homer-new-novel.jpg');background-position:center 40%%;" role="img" aria-label="A watercolor of a young woman lying in the grass, reading a book"></div>
  </header>

  <section class="card">
    <div class="card-head"><span class="ico">📚</span><h2>The Five Novels</h2></div>
    <table class="days">
      <thead><tr><th>Weeks</th><th>The book</th><th>What your student worked on</th></tr></thead>
      <tbody>
        <tr><td class="day-n">1&ndash;5</td><td><span class="ch"><em>The Witch of Blackbird Pond</em></span><br>Elizabeth George Speare. Kit Tyler leaves Barbados for a strict Puritan town in Connecticut and finds out what it costs to stand by a friend everyone else fears.</td><td>Setting, character, conflict and theme; the roots <em>spect</em>, <em>script</em> and <em>struct</em>.</td></tr>
        <tr><td class="day-n">6&ndash;8</td><td><span class="ch"><em>Johnny Tremain</em></span><br>Esther Forbes. An apprentice silversmith with a burned hand finds a new purpose in Boston as the Revolution begins.</td><td>Historical setting, perspective and argument writing; the roots <em>rupt</em>, <em>cess</em> and <em>dict</em>.</td></tr>
        <tr><td class="day-n">9&ndash;14</td><td><span class="ch"><em>Carry On, Mr. Bowditch</em></span><br>Jean Lee Latham. A boy who has to leave school teaches himself navigation at sea and finds the mistakes in the sailors&rsquo; own books.</td><td>Biography as literary nonfiction and perseverance; the roots <em>nav</em>, <em>port</em> and <em>graph</em>.</td></tr>
        <tr class="extra-row"><td class="day-n">15&ndash;17</td><td colspan="2"><span class="ch">Writer&rsquo;s Workshop</span><br>Three weeks of writing: historical detail, real sources, and a historical fiction story.</td></tr>
        <tr><td class="day-n">18&ndash;24</td><td><span class="ch"><em>How I Became a Ghost</em></span><br>Tim Tingle. Isaac, a Choctaw boy, tells the story of his people&rsquo;s forced journey west from Mississippi, and he tells it as a ghost.</td><td>First-person narrative voice, theme, and comparing a novel with real sources; the roots <em>vis</em>, <em>spect</em> and <em>voc</em>.</td></tr>
        <tr><td class="day-n">25&ndash;30</td><td><span class="ch"><em>By the Great Horn Spoon!</em></span><br>Sid Fleischman. Jack and the butler Praiseworthy sail around Cape Horn to the gold fields to save the family home, and find out what a fortune is really made of.</td><td>Humor, tone, voice and theme in an adventure; the roots <em>aud</em>, <em>curr</em>, <em>tract</em>, <em>fort</em> and <em>val</em>.</td></tr>
        <tr class="extra-row"><td class="day-n">31&ndash;32</td><td colspan="2"><span class="ch">The Reader-Writer Portfolio</span><br>A comparison essay on two of the five novels, then a letter to a future fifth grader.</td></tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>What Your Student Wrote This Year</h2></div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Every week</div>A writing task built a step at a time: plan, draft, revise, submit.</div>
      <div class="box b-gold"><div class="box-label">End-of-novel projects</div><strong>A Ghost&rsquo;s-Eye View</strong> (<em>How I Became a Ghost</em>) and <strong>From Boston to the Long Wharf</strong> (<em>By the Great Horn Spoon!</em>), each a four-page booklet.</div>
      <div class="box b-green"><div class="box-label">Spring</div>An adventure story of their own, a literary response about a novel&rsquo;s theme, and a five-paragraph comparison of two novels.</div>
      <div class="box b-plum"><div class="box-label">The last week</div>A real letter to next year&rsquo;s fifth graders, read aloud with one poem from the year.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💛</span><h2>How the Year Handled Hard History</h2></div>
    <p>Several of this year&rsquo;s books touch real history that was cruel or unfair. The lessons kept the story and the record apart and said the true history plainly and calmly. <em>How I Became a Ghost</em> was read alongside real words from the time: part of the 1830 Treaty of Dancing Rabbit Creek and a letter by Choctaw chief George W. Harkins. <em>By the Great Horn Spoon!</em> was written in 1963, and where it uses unkind words from that time, a short note on that day&rsquo;s page named them and gave the true history. No lesson put made-up words in a real person&rsquo;s mouth.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🌞</span><h2>Keep Reading This Summer</h2></div>
    <ul class="check">
      <li><strong>Read every day,</strong> even ten minutes. Let your student choose.</li>
      <li><strong>Ask the year&rsquo;s questions</strong> about any book: Who is telling this story? What does the main character want? What is the big idea?</li>
      <li><strong>Hunt for roots</strong> on signs, boxes and screens: <em>port</em>, <em>spect</em>, <em>aud</em>, <em>graph</em>.</li>
      <li><strong>Read aloud together.</strong> Take turns with the voices.</li>
      <li><strong>Write one letter</strong> to someone far away, about a book.</li>
    </ul>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🎓</span><h2>Thank You</h2></div>
    <p>Thank you for reading with your student this year. The last page of their portfolio is a letter to someone they will never meet, about books they loved. That is what a reader does.</p>
    <p class="small" style="margin-top:8px;"><a href="parent-guide-week-32.html" style="color:#1F6FA8;font-weight:700;">Open the Week 32 guide →</a></p>
  </section>

  <p class="foot">Optima Academy Online · 5th Grade ELA · Year-End Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
""" % LOGO
for fn, title, body in (('parent-guide-week-32.html', 'Week 32 Parent Guide · 5th Grade ELA · Optima Academy Online', WEEK),
                        ('parent-guide-year-end.html', 'The Year in Reading · 5th Grade ELA Family Guide · Optima Academy Online', YEAR)):
    h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, HEAD)
    t = h + body
    assert t.count('<div') == t.count('</div') and t.count('<section') == t.count('</section')
    io.open(fn, 'w', encoding='utf-8').write(t); print('wrote', fn, len(t))
