#!/usr/bin/env python3
"""Week 19 family guide (parent-guide-week-19.html) from the week 18 guide's look. Every line from the
finished week 19 lessons and Ch. 8-11 of the book (checked in planning docs/hbg_ocr.txt). Nov 21 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head, body = s[:s.index('<body>')], s[s.index('<body>'):]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 19 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 19' in head
B = '''<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 19: The Walk Begins</h1>
      <div class="sub"><em>How I Became a Ghost</em> by Tim Tingle, Chapters 8–11</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Ch. 8–11</span>
        <span class="chip">Check-In at week’s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/hbg/savrasov-winter-road.jpg');background-position:center 60%;" role="img" aria-label="A painting of an empty snowy country road with thin bare birch trees"></div>
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
    <p>Sickness spreads through the swamp camp, and Isaac’s family leaves. They follow a long line of Choctaw walkers and soldiers on a frozen road, then join a family they meet there: Gabe, Ruth, and their five-year-old daughter, Nita, who asks Isaac to be her big brother. The ghost of Mister Jonah tells Isaac the new blankets are safe and shows him the ghost walkers, the people who died and still walk beside the living. On the coldest day of the walk, Isaac’s feet freeze to the ground. His father’s words bring him back. In Writer’s Workshop, your student writes a scene where the tension keeps rising.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A heads-up for families</div>These are some of the hardest chapters in the book. In Chapter 8, people in the swamp camp fall sick; in the novel, the blankets the soldiers handed out carried smallpox. (On the real walk, people suffered from cold, hunger and sickness; the smallpox blankets are part of Tim Tingle’s story.) In Chapter 10, Isaac stands in the ice so long that the skin of his feet tears away, and he leaves bloody footprints in the snow. In Chapter 11, Nita gives Isaac her blanket shoes. That night she rolls out of her blanket, and in the morning she has died in the snow. The women burn cedar bark and sing the Choctaw death song, and one soldier says something cruel. The lessons name these moments plainly and do not dwell on them. Reading together, or checking in after Chapters 10 and 11, helps. The <a href="parent-guide-hbg-unit.html" style="color:#A8434A;font-weight:700;">unit guide</a> has the history and what comes later.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>How characterization builds a perspective.</strong> Your student watches what each person does, what they carry, and what they have lost, and compares how two people see the same moment on the road.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>What a person holds on to shows how they see the world.</strong> Isaac holds on to his family and his promise to Nita. His father holds on to one piece of advice.</div>
    </div>
    <p class="quote">“You cannot keep your eyes on the bloody footprints you have left behind you. You must keep your eyes on where you are going.”<small>Isaac’s father, Chapter 10</small></p>
  </section>

  <!-- DAY BY DAY -->
  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">19.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 8 · Walking People</span><br>Sickness spreads through the swamp camp, so Isaac’s family leaves. They follow the walkers for three days, then join Gabe, Ruth and Nita. Mister Jonah’s ghost tells Isaac the new blankets are safe.<br><span class="pill p-museum">Savrasov’s painting of a winter road</span><span class="pill p-extra">The real walk</span></td>
          <td>Isaac tells you on the first page that he is already a ghost. How does knowing the ending change how you read?</td>
        </tr>
        <tr>
          <td class="day-n">19.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 9 · Nita and the Ghost Walkers</span><br>Nita asks Isaac to be her big brother, and he promises to take care of her. He cuts blanket shoes for her feet. Mister Jonah shows him hundreds of ghost walkers beside the living.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A spruce forest at sunset</span><span class="pill p-extra">Choctaw words</span></td>
          <td>What does Isaac’s promise to Nita show about who he is?</td>
        </tr>
        <tr>
          <td class="day-n">19.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 10 · Bloody Footprints</span><br>On the coldest day, Isaac stands too long in the ice and his feet freeze to the ground. The ghosts invite him to come with them. His father calls him back.<br><span class="pill p-museum">Shishkin’s snowy forest</span></td>
          <td>What can one sentence of advice carry?</td>
        </tr>
        <tr>
          <td class="day-n">19.4<span>Day 4</span></td>
          <td><span class="ch">Chapter 11 · Nita’s Walk</span><br>Nita gives Isaac her blanket shoes, and he cuts her a new pair. Isaac sees that it is her time. Luke tells him, “Whatever happens, we are strong.” In the morning, Nita has died.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">A lone pine in the snow</span></td>
          <td>How do two people see the same road differently?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The moment in Chapter 10 when Isaac’s father calls him back. Your student reads it once to themselves, again for smoothness, and once more with expression for the father’s calm words, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up on the week: strong verbs and active voice, the roots <em>anim</em> and <em>spir</em>, the endings <em>-ive</em>, <em>-al</em> and <em>-ic</em>, two reading questions, and two short writing questions.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- WORDS -->
  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>smallpox</b><span>a deadly disease that spreads from person to person; in the story, blankets carry it</span></div>
      <div class="word"><b>belongings</b><span>the things a person owns and carries with them</span></div>
      <div class="word"><b>sickness</b><span>being ill; disease</span></div>
      <div class="word"><b>refused</b><span>said no firmly, even when told to do something</span></div>
      <div class="word"><b>vanished</b><span>disappeared suddenly and completely</span></div>
    </div>
    <div class="skills">
      <div class="box b-sky"><div class="box-label">Word parts</div><strong>anim</strong> means “life, spirit.” <strong>spir</strong> means “breathe.” Long ago, breath and life meant almost the same thing.<span class="eg">animal · animate · unanimous · inspire · respire · expire · spirit</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>-ive, -al and -ic</strong> turn a word into a describing word. Sometimes a silent e drops; sometimes the base changes more.<span class="eg">protect → protective · season → seasonal · hero → heroic · create → creative</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Strong verbs and active voice.</strong> In active voice the subject does the action, so the reader knows who did it. Passive voice can hide that.<span class="eg">The soldiers burned the houses. (active) · The houses were burned. (passive)</span></div>
    </div>
  </section>

  <!-- EXTRAS -->
  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="extras">
      <div class="box b-plum"><div class="box-label">👣 Footprints Forward</div>The week’s word game. Each footprint in the snow holds a word, and your student picks the ending (-ive, -al or -ic) that turns it into a describing word. Six new words a day.</div>
      <div class="box b-gold"><div class="box-label">🏮 Virtue Watch: perseverance</div>After reading, your student sorts moments, keeps a log, rates a moment on a meter, and on Day 4 picks the strongest moment of perseverance in the week.</div>
      <div class="box b-sky"><div class="box-label">🖼️ Winter paintings</div>Each lesson opens with a painting from the 1800s: a winter road, a spruce forest at sunset, a snowy forest, a lone pine. They were painted far from Mississippi, and the captions say so.</div>
      <div class="box b-green"><div class="box-label">🗣️ Choctaw words</div>A card on Day 2 explains <em>Halito</em> (hello), <em>Yakoke</em> (thank you) and <em>Pashofa</em> (corn soup). The narrator never says Choctaw words aloud.</div>
    </div>
  </section>

  <!-- WRITING -->
  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student’s Writing: Rising Action</h2><span class="tag">Writer’s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>One short scene about conflict, start to finish this week. <strong>Day 1:</strong> note a moment, from the novel or your own life, when danger and hope existed at the same time. <strong>Day 2:</strong> write 3–5 sentences about the conflict and let the tension build, without solving it. <strong>Day 3:</strong> reread with a checklist (Is the conflict clear? Does the tension build? Is it still unresolved?), then add one sentence where everything is about to break. <strong>Day 4:</strong> write the final scene in 5–7 sentences, ending while the tension is still high, plus one sentence on what Isaac taught you about rising action.</p>
    <p>Every day also has a <strong>Read Like a Writer</strong> box with one of Isaac’s sentences. This week they show first-person voice: a thought, a detail only Isaac could feel, and his reaction.</p>
  </section>

  <!-- POETRY -->
  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: The Speaker’s Perspective</h2></div>
    <div class="poem-wrap">
      <div class="poem">I’ve known rivers:<br>I’ve known rivers ancient as the world and older than the flow of human blood in human veins.<br><br>My soul has grown deep like the rivers.<small>Langston Hughes, “The Negro Speaks of Rivers” (1921), opening lines, Day 2. On Day 4: Langston Hughes, “Mother to Son” (1922).</small></div>
      <div><p>Both poems have a first-person <strong>speaker</strong>, a voice saying “I,” who is not the poet. Hughes’s river speaker has lived for thousands of years and speaks for a whole people. The speaker of “Mother to Son” is a mother. It’s the same idea as the novel: Isaac tells the story, but Tim Tingle wrote it.</p><p><strong>How to help:</strong> Read “Mother to Son” aloud together. Ask what the mother tells her son to do, and how that sounds like what Isaac’s father says in Chapter 10.</p></div>
    </div>
  </section>

  <!-- ASK AT HOME -->
  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than “How was school?”</span></div>
    <ol class="ask">
      <li><span class="q">Why did Isaac’s family wait before taking blankets on the walk?</span><span class="listen">Listen for: they remembered the swamp blankets carried smallpox. Mister Jonah’s ghost told Isaac the new blankets were safe, so his father asked for them in the morning.</span></li>
      <li><span class="q">What did Isaac promise Nita, and how did he keep it?</span><span class="listen">Listen for: he promised to take care of her as her big brother. The next morning he cut two pieces from his own blanket and tied them on her feet as shoes.</span></li>
      <li><span class="q">Who are the ghost walkers?</span><span class="listen">Listen for: Choctaws who died from fire, sickness and hunger and still walk beside the living. Mister Jonah says, “Our lives are over, but we can still help the living.”</span></li>
      <li><span class="q">What did Isaac’s father tell him in the snow?</span><span class="listen">Listen for: not to keep his eyes on the bloody footprints behind him, but on where he is going. Isaac stopped looking back, and three days later his feet healed.</span></li>
      <li><span class="q">What did Nita give Isaac, and what did he do?</span><span class="listen">Listen for: her blanket shoes. He took them, because he had learned never to refuse a gift, and cut her a new pair.</span></li>
      <li><span class="q">Read me your scene. Where does the tension climb?</span><span class="listen">Listen for: a moment that gets more and more tense and is not solved at the end.</span></li>
    </ol>
  </section>

  <!-- TURN IN + TRY AT HOME -->
  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 chapter questions answered with evidence from the book, the grammar response, the Read Like a Writer box and that day’s Writer’s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 10 passage</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> answers that use the book’s own words as evidence, and a final scene that ends while the tension is still high.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Trace the route</strong> on a map from Mississippi west to Oklahoma, where the Choctaw Nation has its headquarters today.</li>
        <li><strong>Share a piece of advice</strong> someone once gave you that stayed with you, like Isaac’s father’s words.</li>
        <li><strong>Hunt the roots:</strong> an <em>animal</em>, an <em>animated</em> movie, a deep breath that <em>inspires</em>.</li>
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
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 20</h2></div>
    <p><strong><em>How I Became a Ghost</em>, Chapters 12–15.</strong> The walk west goes on, and Isaac learns what his promise to Nita can still mean. Grammar moves to <strong>commas with clauses and transitions</strong>, spelling to <strong>accent shifts in related words</strong>, the roots are <strong>path</strong> and <strong>sens/sent</strong>, and Writer’s Workshop begins a <strong>theme paragraph</strong>.</p>
  </section>

  <p class="foot"><a href="parent-guide-hbg-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole How I Became a Ghost unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 19 Family Guide<br>Questions? Reach out to your student’s teacher anytime.</p>
</div>
</body>
</html>
'''
io.open('parent-guide-week-19.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-19.html')
