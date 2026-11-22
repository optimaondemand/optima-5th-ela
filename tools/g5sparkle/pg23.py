#!/usr/bin/env python3
"""Week 23 family guide (parent-guide-week-23.html) from the week 18 guide's look. Every line from the
finished week 23 lessons and Ch. 24-27 of the book (checked in planning docs/hbg_ocr.txt). Nov 21 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head, body = s[:s.index('<body>')], s[s.index('<body>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 23 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 23' in head
B = '''<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 23: A Soldier&rsquo;s Vow</h1>
      <div class="sub"><em>How I Became a Ghost</em> by Tim Tingle, Chapters 24–27</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Ch. 24–27</span>
        <span class="chip">Check-In at week’s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/hbg/monet-the-magpie.jpg');background-position:center 50%;" role="img" aria-label="A painting of a snowy field and a wooden gate on a quiet winter morning"></div>
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
    <p>Naomi is still hidden in the bonepickers&rsquo; wagon, and Leader is furious. In Chapter 24 he vows, &ldquo;Someone will die today.&rdquo; His soldiers shoot into the trees above the Choctaw Council, burn blankets at every camp, and reach Isaac&rsquo;s family, where a rattlesnake stops a soldier from taking Nita&rsquo;s body. At the bonepickers&rsquo; wagon, Leader orders the wagon burned with Naomi still inside, and Joseph leaps through the flames to pull her out. The week ends with Joseph and Naomi running for the river and Isaac seeing something frightening. In Writer&rsquo;s Workshop, your student chooses their best writing from this unit and takes it all the way to a published piece.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A heads-up for families</div>This is a tense week. In Chapter 24, Leader strikes one of his own soldiers with his shotgun, and the cut bleeds. In Chapter 25, falling branches knock an elderly woman unconscious. In Chapter 26, Nita&rsquo;s mother shows the soldiers her daughter&rsquo;s body. In Chapter 27, Leader throws an old woman to the ground and burns the wagon with Naomi hiding inside; she gets out, and the chapter ends on a frightening moment that is answered next week. The lessons name these moments calmly. Checking in after Chapters 26 and 27 can help.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Summarizing plot and theme.</strong> A summary is a choice: keep the events the story could not do without and leave the rest out. On Day 4, your student puts the book together so far: character, conflict, point of view and theme.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Justice starts with refusing to look away.</strong> Mister Tibbi stands his ground, Ruth tells the truth without a word of argument, and the soldiers start to see the man they follow.</div>
    </div>
    <p class="quote">&ldquo;We did nothing to deserve this.&rdquo;<small>Mister Tibbi, Chapter 25</small></p>
  </section>

  <!-- DAY BY DAY -->
  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">23.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 24 · A Soldier&rsquo;s Vow</span><br>Isaac, who no longer sleeps, visits the soldiers&rsquo; camp in the night. By morning Leader has struck Pointy Nose and vowed, &ldquo;Someone will die today.&rdquo;<br><span class="pill p-museum">Monet&rsquo;s snowy morning</span></td>
          <td>Which events could this chapter not do without?</td>
        </tr>
        <tr>
          <td class="day-n">23.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 25 · A Day of Death</span><br>The soldiers fire into the trees above the Choctaw Council, and Stella is hurt. Blankets burn at every camp. Isaac tells the families, &ldquo;We are stronger than the soldiers.&rdquo; Despite the title, no one dies in this chapter.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Friedrich&rsquo;s oak in the snow</span><span class="pill p-extra">Do you keep following him?</span></td>
          <td>What actually changed, one turn at a time?</td>
        </tr>
        <tr>
          <td class="day-n">23.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 26 · Choctaw Rattlesnake</span><br>Leader demands Ruth&rsquo;s little girl. Ruth lays Nita&rsquo;s body by the fire. When Pointy Nose reaches for it, a rattlesnake rises over Nita, and the soldiers ride away.<br><span class="pill p-museum">Catesby&rsquo;s rattlesnake</span></td>
          <td>Can you sum up one passage in two honest sentences?</td>
        </tr>
        <tr>
          <td class="day-n">23.4<span>Day 4</span></td>
          <td><span class="ch">Chapter 27 · Wagon of the Bonepickers</span><br>Leader burns the bonepickers&rsquo; wagon with Naomi inside. Joseph pulls her out through the flames, and they run for the river.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Friedrich&rsquo;s ancient grave in the snow</span></td>
          <td>What does the book add up to so far?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The opening of Chapter 24: Joseph asleep in the snow after a long day, and Isaac awake all night. Your student reads it once to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up on the week: sentence combining and editing, the roots <em>voc/voke</em> and <em>dict</em>, the year&rsquo;s spelling patterns, two reading questions, and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- WORDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>exhausted</b><span>completely worn out</span></div>
      <div class="word"><b>revenge</b><span>hurting someone back for something they did to you</span></div>
      <div class="word"><b>unconscious</b><span>not awake and not able to feel anything, usually after being hurt</span></div>
      <div class="word"><b>gratitude</b><span>thankfulness, and the showing of it</span></div>
      <div class="word"><b>prophecy</b><span>a prediction of what will happen in the future</span></div>
    </div>
    <div class="skills">
      <div class="box b-sky"><div class="box-label">Word parts</div><strong>voc / voke</strong> means &ldquo;voice, call,&rdquo; and <strong>dict</strong> means &ldquo;say.&rdquo; An <em>advocate</em> raises a voice for someone; a <em>verdict</em> is the truth, spoken.<span class="eg">vocal · advocate · provoke · evoke · predict · contradict · verdict · dictate</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>A year of patterns, used on a real draft.</strong> Suffixes that change the base, prefixes that stay whole, sound-alikes, -able and -ible, and Greek and Latin parts.<span class="eg">decision · illegal · their / there · dependable · visible · manuscript</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Editing for clarity and sentence combining.</strong> Short sentences are joined so the reader can see how ideas connect, and transition words (<em>but, because, when, instead</em>) show the link.<span class="eg">It was freezing, but Joseph was so worn out that he fell asleep in minutes.</span></div>
    </div>
  </section>

  <!-- EXTRAS -->
  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="extras">
      <div class="box b-plum"><div class="box-label">📣 Raise Your Voice</div>The week&rsquo;s word game. Each line has a blank, and your student taps the <em>voc</em> or <em>dict</em> word that fits (<em>dictionary</em>, <em>vocation</em>, <em>unpredictable</em>). Each finished line sends a gold voice ring into the sky. Three lines a day.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: justice</div>After reading, your student sorts moments, keeps a log, rates a moment on a meter, and on Day 4 picks the strongest moment of justice in the week.</div>
      <div class="box b-sky"><div class="box-label">🖼️ Art from long ago</div>Each lesson opens with a work of art: Monet&rsquo;s snowy morning, Friedrich&rsquo;s oak and his ancient grave in the snow, and a hand-colored rattlesnake from a 1743 book about Carolina. They were made far from Mississippi, and the captions say so.</div>
      <div class="box b-green"><div class="box-label">❓ Do you keep following him?</div>Day 2 opens with a question: if your leader hurt one of your own, would you keep following him? Chapter 25 shows what Leader&rsquo;s soldiers start to wonder.</div>
    </div>
  </section>

  <!-- WRITING -->
  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: A Published Piece</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Your student finishes the unit by publishing their best writing. <strong>Day 1:</strong> look back at the writing from weeks 18 to 22, choose the strongest piece (or combine the best parts), and plan what to keep, cut, and how to begin and end. <strong>Day 2:</strong> write a full draft. <strong>Day 3:</strong> revise with a checklist: strong verbs, a combined sentence, clear pronouns, and at least one transition word. <strong>Day 4:</strong> write the final version and one sentence about what it shows about them as a writer.</p>
    <p>Every day also has a <strong>Read Like a Writer</strong> box with one of the book&rsquo;s sentences, like &ldquo;The soldiers continued their search, burning blankets and questioning Choctaws at every camp.&rdquo; This week they show how one sentence can sum up a lot without retelling every event.</p>
  </section>

  <!-- POETRY -->
  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: Why This Shape?</h2></div>
    <div class="poem-wrap">
      <div class="poem">Under the wide and starry sky,<br>Dig the grave and let me lie.<br>Glad did I live and gladly die,<br>And I laid me down with a will.<small>Robert Louis Stevenson, &ldquo;Requiem&rdquo; (1887), first stanza, Day 4. On Day 2: Emma Lazarus, &ldquo;The New Colossus&rdquo; (1883).</small></div>
      <div><p>This week&rsquo;s poems are about shape. Lazarus wrote a sonnet, a strict fourteen-line form, for the words the Statue of Liberty speaks. Stevenson shaped &ldquo;Requiem&rdquo; like a gravestone: two short, calm stanzas, with the words he wanted carved on the stone.</p><p><strong>How to help:</strong> Read &ldquo;Requiem&rdquo; aloud together. Ask why a poem about the end of a life might be so short and calm.</p></div>
    </div>
  </section>

  <!-- ASK AT HOME -->
  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">What did Leader vow, and how did his own soldiers feel about him?</span><span class="listen">Listen for: &ldquo;Someone will die today.&rdquo; After he struck Pointy Nose, they became afraid of him; by Chapter 27 they see him as a cruel man.</span></li>
      <li><span class="q">Chapter 25 is called &ldquo;A Day of Death.&rdquo; Does anyone die in it?</span><span class="listen">Listen for: no. Stella is hurt and blankets are burned, but Leader says no one died. A careful summary notices that.</span></li>
      <li><span class="q">What did Ruth do when Leader demanded her little girl?</span><span class="listen">Listen for: she did not argue. She laid Nita&rsquo;s body by the fire and said, &ldquo;Here is my daughter.&rdquo; Then a rattlesnake guarded Nita.</span></li>
      <li><span class="q">How did Naomi get out of the burning wagon?</span><span class="listen">Listen for: Joseph leapt through the burning curtain, lifted the false floor of the trunk, and jumped out with her through the cloth wall.</span></li>
      <li><span class="q">Sum up this week&rsquo;s chapters in three sentences.</span><span class="listen">Listen for: only the events the story could not do without, not every detail.</span></li>
      <li><span class="q">Read me your published piece. What does it show about you as a writer?</span><span class="listen">Listen for: a clean, finished piece and one honest sentence about their writing.</span></li>
    </ol>
  </section>

  <!-- TURN IN + TRY AT HOME -->
  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 chapter questions answered with evidence from the book, the grammar response, the Read Like a Writer box and that day&rsquo;s Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 24 passage</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers that use the book&rsquo;s own words as evidence, summaries that choose instead of retell, and a finished piece that is clean and complete.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Join it up:</strong> say three short sentences about your day and let your student join them into one with <em>but</em>, <em>because</em> or <em>when</em>.</li>
        <li><strong>Hunt the voice words:</strong> a <em>dictionary</em>, a <em>vocal</em> singer, a <em>prediction</em> about the weather.</li>
        <li><strong>One-sentence movie:</strong> sum up a favorite movie in one sentence. What did you leave out?</li>
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
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 24</h2></div>
    <p><strong><em>How I Became a Ghost</em>, Chapters 28–29, the end of the novel.</strong> Then a study of real sources about the Trail of Tears. Words move to <strong>the vocabulary of history</strong>, grammar to <strong>formal style and transitions</strong>, and Writer&rsquo;s Workshop to <strong>comparing sources</strong> with a claim, evidence and reasoning.</p>
  </section>

  <p class="foot"><a href="parent-guide-hbg-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole How I Became a Ghost unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 23 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-23.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-23.html')
