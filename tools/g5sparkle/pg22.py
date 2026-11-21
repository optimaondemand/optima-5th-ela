#!/usr/bin/env python3
"""Week 22 family guide (parent-guide-week-22.html) from the week 18 guide's look. Every line from the
finished week 22 lessons and Ch. 20-23 of the book (checked in planning docs/hbg_ocr.txt). Nov 21 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head, body = s[:s.index('<body>')], s[s.index('<body>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 22 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 22' in head
B = '''<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 22: Naomi the Strong</h1>
      <div class="sub"><em>How I Became a Ghost</em> by Tim Tingle, Chapters 20–23</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Ch. 20–23</span>
        <span class="chip">Check-In at week’s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/hbg/kyhn-winter-evening.jpg');background-position:center 55%;" role="img" aria-label="A painting of a snowy forest at dusk with bare trees"></div>
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
    <p>Isaac, now a ghost, reaches Naomi in the soldiers&rsquo; wagon, and she learns her little sister Nita has died. When Leader hears voices, he punishes Naomi. That night Isaac, Joseph, Nita&rsquo;s ghost, a dog named Jumper and the Choctaw Council work together to free her: Jumper splashes into the river, Joseph as the panther gnaws through the rope and sets a wagon on fire, and Naomi runs. Luke takes her to the bonepickers, four old women who hide her in a trunk with a secret bottom. At the end of the week, a hundred Choctaw ghosts appear to thank the three boys. In Writer&rsquo;s Workshop, your student writes a one-paragraph literary analysis.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A heads-up for families</div>This is a hard week to read. In Chapter 20, Leader hangs Naomi from a tree by her tied wrists and slaps her. Chapter 22 explains, plainly, how the bonepickers cared for the dead in the old Choctaw way. In Chapter 23, the women wring a bloody raccoon over the bones in the trunk so the soldiers will not look inside, and the blood drips on Naomi. The lessons name these moments calmly and do not dwell on them. Reading Chapters 20 and 23 together, or checking in afterward, can help.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Figurative language and the author&rsquo;s choices.</strong> Your student marks comparisons and images, like Nita shining &ldquo;like a pale moon,&rdquo; and asks what each one makes a reader feel.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Strength can look quiet.</strong> Naomi protects her friends with two words, &ldquo;No one,&rdquo; and later lies still in the dark to stay hidden.</div>
    </div>
    <p class="quote">&ldquo;I have to be watchful to stay alive.&rdquo;<small>Naomi, Chapter 20</small></p>
  </section>

  <!-- DAY BY DAY -->
  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">22.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 20 · Naomi the Strong</span><br>Naomi has dreamed of Isaac for a week. She learns Nita has died, and Nita&rsquo;s ghost hugs her. Leader hears voices and punishes Naomi. Joseph decides, &ldquo;Naomi comes with us tonight.&rdquo;<br><span class="pill p-museum">Inness&rsquo;s moonlit night</span></td>
          <td>What does &ldquo;strong&rdquo; look like for Naomi?</td>
        </tr>
        <tr>
          <td class="day-n">22.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 21 · The Panther and the Fire</span><br>Jumper&rsquo;s splash pulls the guards away. The panther gnaws the rope and scatters the fire, and Naomi runs. A councilwoman cuts the rope from her wrists, and she hugs her parents before Luke leads her away.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A bronze panther</span></td>
          <td>What is the panther doing, besides being an animal?</td>
        </tr>
        <tr>
          <td class="day-n">22.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 22 · Buried with the Bones</span><br>Naomi climbs into the wagon of the bonepickers, which smells of dried roses. The women hide her in a trunk with a secret bottom, under the bones.<br><span class="pill p-museum">Fantin-Latour&rsquo;s roses</span><span class="pill p-extra">Where would you hide her?</span></td>
          <td>Why does the author put the comparison before the fact?</td>
        </tr>
        <tr>
          <td class="day-n">22.4<span>Day 4</span></td>
          <td><span class="ch">Chapter 23 · Naomi and the Bonepickers</span><br>The women&rsquo;s plan goes into action so the soldiers will not search the trunk. A hundred Choctaw ghosts appear to thank Isaac, Joseph and Luke. Then sleet falls, and Isaac and Joseph keep watch.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Kyhn&rsquo;s winter woods</span></td>
          <td>Which image carries the most in the book so far?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The last page of Chapter 23, a cold, quiet night that ends with words from the book&rsquo;s first page. Your student reads it once to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up on the week: clear pronouns, the roots <em>luc/lum</em> and <em>photo</em>, Greek and Latin roots in book words, two reading questions, and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- WORDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>distraction</b><span>something that pulls attention away, so something else can happen unnoticed</span></div>
      <div class="word"><b>bonepickers</b><span>Choctaws whose sacred job was to prepare the dead for burial</span></div>
      <div class="word"><b>speechless</b><span>so surprised or moved that you cannot say a word</span></div>
      <div class="word"><b>ancestors</b><span>the family members who lived long before you</span></div>
      <div class="word"><b>honored</b><span>treated with great respect</span></div>
    </div>
    <div class="skills">
      <div class="box b-sky"><div class="box-label">Word parts</div><strong>luc / lum</strong> (Latin) and <strong>photo</strong> (Greek) both mean &ldquo;light.&rdquo; Something <em>translucent</em> lets light pass through.<span class="eg">lucid · translucent · illuminate · luminous · photograph · photosynthesis</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Greek and Latin roots in book words.</strong> Long words about stories are short parts stacked together.<span class="eg">chron (time) · graph (write) · log (word) · phor/fer (carry): chronology · paragraph · dialogue · metaphor</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Pronoun clarity.</strong> A pronoun must point back to one clear noun. With Isaac, Joseph, Luke and Leader all called &ldquo;he,&rdquo; names matter.<span class="eg">Isaac told Joseph that Joseph should go first.</span></div>
    </div>
  </section>

  <!-- EXTRAS -->
  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="extras">
      <div class="box b-plum"><div class="box-label">🏮 Light the Lanterns</div>The week&rsquo;s word game. Each lantern shows a meaning, and your student taps the word parts in order to build the word (<em>photo + copy</em>, <em>syn + chron + ize</em>). A finished word lights its lantern. Four words a day.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: perseverance</div>After reading, your student sorts moments, keeps a log, rates a moment on a meter, and on Day 4 picks the strongest moment of perseverance in the week.</div>
      <div class="box b-sky"><div class="box-label">🖼️ Art from the 1800s</div>Each lesson opens with a work of art: a moonlit Florida night, a bronze panther, a bowl of roses, and a snowy forest at dusk. They were made far from Mississippi, and the captions say so.</div>
      <div class="box b-green"><div class="box-label">❓ Where would you hide her?</div>Day 3 opens with a question: where would you hide a girl the soldiers are hunting? The answer in Chapter 22 surprises everyone.</div>
    </div>
  </section>

  <!-- WRITING -->
  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: A Literary Analysis Paragraph</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>Your student writes one paragraph that makes a claim about the novel and proves it. <strong>Day 1:</strong> choose a topic (Naomi&rsquo;s strength, Isaac&rsquo;s role as a ghost, or justice), write a claim, and find two pieces of evidence. <strong>Day 2:</strong> draft the paragraph: claim, two pieces of evidence with explanation, and a closing sentence. <strong>Day 3:</strong> revise with a checklist: clear pronouns, one better transition, no extra words. <strong>Day 4:</strong> write the final paragraph, then explain the difference between a summary and an analysis.</p>
    <p>Every day also has a <strong>Read Like a Writer</strong> box with one of the book&rsquo;s sentences, like &ldquo;Fat balls of tears rolled down her cheeks.&rdquo; This week they show how imagery and comparisons let a reader feel a moment.</p>
  </section>

  <!-- POETRY -->
  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: Pictures Instead of Feelings</h2></div>
    <div class="poem-wrap">
      <div class="poem">Whose woods these are I think I know.<br>His house is in the village though;<br>He will not see me stopping here<br>To watch his woods fill up with snow.<small>Robert Frost, &ldquo;Stopping by Woods on a Snowy Evening&rdquo; (1923), first stanza, Day 4. On Day 2: William Blake, &ldquo;The Tyger&rdquo; (1794).</small></div>
      <div><p>Neither poet tells you what to feel. Blake gives you a tiger &ldquo;burning bright&rdquo; in a dark forest. Frost gives you woods filling up with snow on the darkest evening of the year. That is imagery: pictures that carry the feeling.</p><p><strong>How to help:</strong> Read the Frost poem aloud together. Ask which picture makes the woods feel quiet, and why he repeats the last line.</p></div>
    </div>
  </section>

  <!-- ASK AT HOME -->
  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Why did Naomi say at first that she could not escape?</span><span class="listen">Listen for: she thought the soldiers would take her little sister, Nita. Then she learned Nita had already died.</span></li>
      <li><span class="q">Who helped Naomi get away, and what did each one do?</span><span class="listen">Listen for: Jumper splashed into the river, the panther gnawed the rope and set a wagon on fire, Nita woke the council, a councilwoman cut the rope, Luke led her to the bonepickers.</span></li>
      <li><span class="q">Who are the bonepickers, and why is their wagon a safe hiding place?</span><span class="listen">Listen for: old Choctaw women whose sacred job was caring for the dead. Most people stay away from them, and the trunk has a secret bottom under the bones.</span></li>
      <li><span class="q">What did the ghosts say to Isaac, Joseph and Luke?</span><span class="listen">Listen for: they were proud of the boys and said &ldquo;thank you.&rdquo; Making the ancestors proud is the highest honor.</span></li>
      <li><span class="q">Find a comparison in this week&rsquo;s chapters. What does it make you feel?</span><span class="listen">Listen for: an image like Nita shining like a pale moon, or Naomi&rsquo;s realization &ldquo;like a thunderbolt.&rdquo;</span></li>
      <li><span class="q">Read me your paragraph. What is your claim, and what proves it?</span><span class="listen">Listen for: one clear claim, two pieces of evidence from the book, and an explanation of each.</span></li>
    </ol>
  </section>

  <!-- TURN IN + TRY AT HOME -->
  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 chapter questions answered with evidence from the book, the grammar response, the Read Like a Writer box and that day&rsquo;s Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 23 passage</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers that use the book&rsquo;s own words as evidence, and a paragraph whose claim is proved, not just retold.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Who is &ldquo;he&rdquo;?</strong> Tell a story about two people with only &ldquo;he&rdquo; or &ldquo;she,&rdquo; and let your student fix it.</li>
        <li><strong>Hunt the light words:</strong> a <em>photograph</em>, a <em>luminous</em> watch, a <em>lucid</em> explanation.</li>
        <li><strong>Build a word:</strong> <em>tele</em> (far) + <em>graph</em> (write) = ?</li>
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
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 23</h2></div>
    <p><strong><em>How I Became a Ghost</em>, Chapters 24–27.</strong> The soldiers search for Naomi. Grammar moves to <strong>editing for clarity</strong>, the roots are <strong>voc</strong> and <strong>dict</strong>, spelling reviews the year&rsquo;s patterns, and Writer&rsquo;s Workshop moves toward <strong>publishing</strong> a finished piece.</p>
  </section>

  <p class="foot"><a href="parent-guide-hbg-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole How I Became a Ghost unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 22 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-22.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-22.html')
