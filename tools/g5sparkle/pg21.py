#!/usr/bin/env python3
"""Week 21 family guide (parent-guide-week-21.html) from the week 18 guide's look. Every line from the
finished week 21 lessons and Ch. 16-19 of the book (checked in planning docs/hbg_ocr.txt). Nov 21 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head, body = s[:s.index('<body>')], s[s.index('<body>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 21 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 21' in head
B = '''<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 21: Chi Pisa Lachike</h1>
      <div class="sub"><em>How I Became a Ghost</em> by Tim Tingle, Chapters 16–19</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Ch. 16–19</span>
        <span class="chip">Check-In at week’s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/hbg/church-twilight-wilderness.jpg');background-position:center 40%;" role="img" aria-label="A painting of a fiery red sunset sky over dark hills and a river"></div>
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
    <p>Nani Humma catches Isaac and Joseph talking by the creek, and the Choctaw Council decides to help rescue Naomi in secret. Isaac and Joseph walk back along the line to visit Isaac&rsquo;s family for one last day. On the way back, a wolf attacks Isaac, and he becomes a ghost. Joseph, as the panther, drives the wolf away, and Isaac&rsquo;s family carries his body on the walk. As a ghost, Isaac learns the soldiers cannot hurt him. He walks into their camp, finds Naomi tied in a wagon, and whispers her name. In Writer&rsquo;s Workshop, your student revises an earlier story to make its pictures stronger.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A heads-up for families</div>Chapter 18 is the chapter the whole book has been leading to: Isaac dies. A wolf attacks him in the woods, and the chapter describes the bite, the blood, and his family&rsquo;s grief as they carry his body. Isaac tells it calmly, as a ghost who is not afraid, and he keeps helping the people he loves. In Chapter 19, Naomi is tied up at night in the soldiers&rsquo; wagon. The lessons name these moments plainly and do not dwell on them. Reading Chapter 18 together, or checking in afterward, can help.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>How a theme grows.</strong> Your student tracks pictures and ideas that come back in the book, like the bloody footprints from Chapter 10, and explains what they mean when they return.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>The people we love never really leave us.</strong> Choctaws say <em>chi pisa lachike</em>, &ldquo;I will see you again, in the future,&rdquo; instead of good-bye.</div>
    </div>
    <p class="quote">&ldquo;Choctaws never go away.&rdquo;<small>Isaac, Chapter 17</small></p>
  </section>

  <!-- DAY BY DAY -->
  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">21.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 16 · Seeking Naomi</span><br>Nani Humma catches the boys at night, and they tell him everything. The council decides Naomi&rsquo;s best chance is Isaac and Joseph, with the council helping in secret. The councilwomen spot Naomi, dressed as a boy.<br><span class="pill p-museum">Durand&rsquo;s forest</span></td>
          <td>What does it take to tell the whole truth?</td>
        </tr>
        <tr>
          <td class="day-n">21.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 17 · Good-bye to My Family</span><br>Isaac spends one last day with his family. Luke gives Joseph his blowgun. As the sun sets, they say <em>chi pisa lachike</em>.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A red sunset sky</span><span class="pill p-extra">Is good-bye ever final?</span><span class="pill p-extra">Choctaw words</span></td>
          <td>What do the things that come back in a story mean?</td>
        </tr>
        <tr>
          <td class="day-n">21.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 18 · Trail of Tears</span><br>A wolf attacks Isaac, and he becomes a ghost. Joseph, as the panther, fights the wolf off. Isaac wants to go back into his body, but he remembers his father&rsquo;s words and lets go.<br><span class="pill p-museum">Duncanson&rsquo;s quiet river</span></td>
          <td>What does an idea mean when it comes back late in a book?</td>
        </tr>
        <tr>
          <td class="day-n">21.4<span>Day 4</span></td>
          <td><span class="ch">Chapter 19 · Naomi Meets the Ghost</span><br>Isaac&rsquo;s family sees panther tracks and learns Joseph&rsquo;s secret. Isaac walks into the soldiers&rsquo; camp unseen and finds Naomi. When he whispers her name, she says, &ldquo;What took you so long?&rdquo;<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Blakelock&rsquo;s moonlight</span></td>
          <td>What theme does the book show, in one full sentence?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">Isaac&rsquo;s walk into the soldiers&rsquo; camp in Chapter 19. Your student reads it once to themselves, again for smoothness, and once more with expression for Isaac&rsquo;s surprise, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up on the week: compound and complex sentences, the roots <em>vis/vid</em> and <em>spect</em>, words that sound alike, two reading questions, and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- WORDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>terrified</b><span>extremely frightened</span></div>
      <div class="word"><b>stickball</b><span>a traditional Choctaw game played with sticks and a ball</span></div>
      <div class="word"><b>mourning</b><span>deep sadness after someone dies, and the quiet way people show it</span></div>
      <div class="word"><b>suffering</b><span>pain or hardship a person is living through</span></div>
      <div class="word"><b>courage</b><span>facing something frightening anyway</span></div>
    </div>
    <div class="skills">
      <div class="box b-sky"><div class="box-label">Word parts</div><strong>vis / vid</strong> means &ldquo;see.&rdquo; <strong>spect</strong> means &ldquo;look.&rdquo; <em>Evidence</em> is what can be seen; a <em>spectator</em> looks on.<span class="eg">vision · visible · invisible · evidence · spectator · inspect · perspective</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Words that sound alike.</strong> A spell checker won&rsquo;t catch them, so meaning decides the spelling.<span class="eg">their / there / they&rsquo;re · its / it&rsquo;s · council / counsel · affect / effect · principal / principle</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Compound and complex sentences.</strong> A compound sentence joins two ideas that could each stand alone. A complex sentence makes one idea depend on the other.<span class="eg">When Luke returned, the bowl was empty. (complex)</span></div>
    </div>
  </section>

  <!-- EXTRAS -->
  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="extras">
      <div class="box b-plum"><div class="box-label">🔭 The Spyglass</div>The week&rsquo;s word game. A brass spyglass shows one word at a time. Your student taps the root inside it (<em>vis</em> or <em>spect</em>), watches it light up, then taps what the word means. Five words a day.</div>
      <div class="box b-gold"><div class="box-label">🦁 Virtue Watch: courage</div>After reading, your student sorts moments, keeps a log, rates a moment on a meter, and on Day 4 picks the strongest moment of courage in the week.</div>
      <div class="box b-sky"><div class="box-label">🖼️ Paintings from the 1800s</div>Each lesson opens with an American painting: a deep forest, a red sunset over a river, a quiet river pool, and a moonlit night. They were painted far from Mississippi, and the captions say so.</div>
      <div class="box b-green"><div class="box-label">🗣️ Choctaw words</div>A card on Day 2 explains <em>Yakoke</em> (thank you), <em>Pashofa</em> (corn soup) and <em>chi pisa lachike</em> (I will see you again). The narrator never says Choctaw words aloud.</div>
    </div>
  </section>

  <!-- WRITING -->
  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: Imagery and Description</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Your student goes back to a story written in week 18 or 19 and makes its pictures stronger. <strong>Day 1:</strong> choose three moments that need stronger imagery. <strong>Day 2:</strong> revise the first moment with one detail you can see, hear, smell or feel, and one comparison. <strong>Day 3:</strong> check the first moment with a short checklist, then revise the second with a comparison that fits its feeling. <strong>Day 4:</strong> write the final revised story in 5 to 7 sentences, plus one sentence on what imagery adds.</p>
    <p>Every day also has a <strong>Read Like a Writer</strong> box with one of Isaac&rsquo;s sentences. This week they show how to explain a theme with details from more than one part of the book.</p>
  </section>

  <!-- POETRY -->
  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: Pictures That Come Back</h2></div>
    <div class="poem-wrap">
      <div class="poem">Who has seen the wind?<br>Neither I nor you:<br>But when the leaves hang trembling<br>The wind is passing thro&rsquo;.<small>Christina Rossetti, &ldquo;Who Has Seen the Wind?&rdquo; (1872), first stanza, Day 4. On Day 2: Langston Hughes, &ldquo;Dreams&rdquo; (1923).</small></div>
      <div><p>Both poems repeat something. Hughes opens both stanzas with &ldquo;Hold fast to dreams,&rdquo; and each time a new picture follows. Rossetti asks the same question twice and answers it with two pictures of the wind at work. That is how a theme grows: the same idea comes back and means more.</p><p><strong>How to help:</strong> Read the Rossetti poem aloud together. Ask how you can know something is there when you can&rsquo;t see it, and how that fits Isaac and Joseph after Chapter 18.</p></div>
    </div>
  </section>

  <!-- ASK AT HOME -->
  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Why doesn&rsquo;t the council just go to the soldiers and demand Naomi back?</span><span class="listen">Listen for: the soldiers would lie, Naomi would be too afraid to tell the truth, and she might disappear. The council helps in secret instead.</span></li>
      <li><span class="q">What do Choctaws say instead of good-bye, and what does it mean?</span><span class="listen">Listen for: <em>chi pisa lachike</em>, &ldquo;I will see you again, in the future.&rdquo;</span></li>
      <li><span class="q">What did Luke give Joseph, and why?</span><span class="listen">Listen for: his blowgun. He told Joseph to take care of Isaac.</span></li>
      <li><span class="q">What does Isaac almost do after he becomes a ghost, and what stops him?</span><span class="listen">Listen for: he wants to go back into his body to end his family&rsquo;s grief. He remembers his father&rsquo;s words about keeping his eyes on where he is going.</span></li>
      <li><span class="q">What did Isaac figure out in the soldiers&rsquo; camp?</span><span class="listen">Listen for: the soldiers can&rsquo;t hurt him because he is already a ghost, and the young man serving stew is really Naomi.</span></li>
      <li><span class="q">Read me your revised story. Which picture is stronger now?</span><span class="listen">Listen for: a detail you can see, hear, smell or feel, and a comparison.</span></li>
    </ol>
  </section>

  <!-- TURN IN + TRY AT HOME -->
  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 chapter questions answered with evidence from the book, the grammar response, the Read Like a Writer box and that day&rsquo;s Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 19 passage</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers that use the book&rsquo;s own words as evidence, and a revised story where the reader can see and feel the moment.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Talk about good-byes:</strong> what does your family say when someone leaves for a long time?</li>
        <li><strong>Catch the sound-alikes:</strong> spot <em>their</em>, <em>there</em> and <em>they&rsquo;re</em> in a sign, a text or a menu.</li>
        <li><strong>Hunt the roots:</strong> a <em>visitor</em>, a <em>television</em>, a pair of <em>spectacles</em>.</li>
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
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 22</h2></div>
    <p><strong><em>How I Became a Ghost</em>, Chapters 20–23.</strong> Isaac and Joseph work to bring Naomi home. Grammar moves to <strong>pronoun clarity</strong>, spelling to <strong>Greek and Latin roots in literary words</strong>, the roots are <strong>luc/lum</strong> and <strong>photo</strong>, and Writer&rsquo;s Workshop begins a <strong>literary analysis</strong>.</p>
  </section>

  <p class="foot"><a href="parent-guide-hbg-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole How I Became a Ghost unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 21 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-21.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-21.html')
