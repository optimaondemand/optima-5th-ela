#!/usr/bin/env python3
"""Week 30 family guide (parent-guide-week-30.html) in the week 18 guide's look. Every line from the finished
week 30 lessons, Ch. 16-18 of By the Great Horn Spoon! (project doc text). History as on the 30.1-30.3 cards (CA State Parks, PBS, LOC,
Madley 2024). Nov 24 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 30 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 30' in head
B = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 30: Jack&rsquo;s Letter Home</h1>
      <div class="sub"><em>By the Great Horn Spoon!</em> by Sid Fleischman, Chapters 16&ndash;18 and a whole-book day</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Last week of the book</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/btghs/burgess-san-francisco-1850.jpg');background-position:center 55%;" role="img" aria-label="An oil painting of San Francisco in 1850: wooden buildings on sandy hills, with the bay full of ships behind"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment (on Day 4 the Reading tab is called Synthesis and the last one Publish). A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson. Keep the book nearby.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>The novel ends this week. At Shirt-tail Camp, a crowd is about to punish Cut-Eye Higgins for stealing a horse, and Praiseworthy, who has never made a speech in his life, speaks up for him to keep a promise. The punishment he gets in return leads somewhere nobody expects. Then comes a day of celebration, the fight Praiseworthy promised to the Mountain Ox, a fast boat to San Francisco and one more surprise on the Long Wharf. On Day 4 your student looks back at the whole book: how the plot, the characters, the humor and the big ideas fit together.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families: words from 1963 and real history</div>This book was written in 1963. Two short passages this week use words from that time that are unkind, and a folded note on that day&rsquo;s Reading tab names them plainly and gives the true history, with no made-up voices. <strong>Chapter 17</strong> calls Chinese miners men &ldquo;with pigtails&rdquo; (a mocking word for the long braid, or queue, Chinese men were required to wear under the Qing rulers) and has the Mountain Ox order a cook named Ah Lee around at the &ldquo;Chinese chow chow.&rdquo; The note says that thousands of Chinese gold-seekers came in the early 1850s, worked old claims carefully, ran restaurants, laundries and stores, and faced unfair laws such as the 1852 tax on foreign miners. <strong>Chapter 18</strong> mentions &ldquo;Kanaka sailors&rdquo;; the note explains that <em>K&#257;naka</em> is the Hawaiian word for people and that Hawaiian sailors worked on many Pacific ships. <strong>Chapter 16</strong> has no slur, but its crowd means to hang a man with no lawyer and no judge; a real-history card on Day 1 says calmly that some mining camps really did hold quick, often unfair trials before California had state courts in 1850.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>Putting it all together.</strong> Your student reads with four lenses at once (plot, character, humor and theme) and then looks back at the whole novel.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Hope.</strong> When everything goes wrong, Praiseworthy looks at what he still has: &ldquo;Mere bits of colored metal.&rdquo;</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">30.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 16 · The Gravediggers</span><br>Coloma and Sutter&rsquo;s sawmill, Shirt-tail Camp, and a speech nobody expected.<br><span class="pill p-extra">Real history: the real Sutter&rsquo;s Mill</span><span class="pill p-museum">Sutter&rsquo;s Saw Mill, 1849</span></td>
          <td>What would make you speak up for someone who cheated you?</td>
        </tr>
        <tr>
          <td class="day-n">30.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 17 · The Fifteenth of August</span><br>A celebration, a claim staked with an umbrella, and the day of the fight.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Mountain Camp in California, 1849</span></td>
          <td>What does it mean to call someone simply by their name?</td>
        </tr>
        <tr>
          <td class="day-n">30.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 18 · Arrival at the Long Wharf</span><br>A fast riverboat, San Francisco Bay, and the last surprises of the book.<br><span class="pill p-museum">High and Dry, 1855</span></td>
          <td>What does &ldquo;home&rdquo; mean at the end of a great adventure?</td>
        </tr>
        <tr>
          <td class="day-n">30.4<span>Day 4</span></td>
          <td><span class="ch">The whole book</span><br>Your student looks back at the voyage, the diggings and the ending, and says what the novel is finally about.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">View of San Francisco in 1850</span></td>
          <td>What did this story teach you about adventure, courage and finding your way?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The last scene of the novel on the Long Wharf, from &ldquo;Will you be returning to Boston?&rdquo; to &ldquo;By the Great Horn Spoon!&rdquo; Your student reads it to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up: editing for punctuation, capitals and spelling, root families from the unit, a word in context, four reading questions (one on the poem), and the ending of their own adventure.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>reprieve</b><span>a delay of a punishment</span></div>
      <div class="word"><b>counsel</b><span>a lawyer who speaks for someone; advice</span></div>
      <div class="word"><b>exuberance</b><span>joyful, overflowing energy</span></div>
      <div class="word"><b>spirited</b><span>lively and eager</span></div>
      <div class="word"><b>reunion</b><span>a gathering of people who have been apart</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Root families</div>A look back at every root in the unit: <strong>aud</strong> (hear), <strong>rid, lud</strong> (laugh, play), <strong>curr, tract</strong> (run, pull), <strong>fort, val</strong> (strong, worth).<span class="eg">audience · ridiculous · extract · fortitude · valuable</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Editing for spelling:</strong> the words fifth graders miss most, and endings added to a base.<span class="eg">receive · occurred · embarrass · argue → argument</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Editing in passes:</strong> one pass for capitals, one for punctuation, one for clarity.<span class="eg">&ldquo;We&rsquo;ve struck it rich!&rdquo; Jack shouted.</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">✉️ Jack&rsquo;s Letter Home</div>The week&rsquo;s word game. Each day there is a short, made-up letter from Jack with one misspelled word in every line. Your student taps the wrong word, picks the right spelling to ink the line clean, and seals the finished letter.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: hope</div>After reading, your student sorts everyday examples of hope, picks a hopeful moment from the day of the fight, rates Praiseworthy&rsquo;s hope after a big loss, and on Day 4 picks the most hopeful moment of the week.</div>
      <div class="box b-sky"><div class="box-label">🗺️ Real history, kept apart</div>A Day 1 card on the real Sutter&rsquo;s Mill: James Marshall&rsquo;s discovery on January 24, 1848, a worker&rsquo;s diary from that day, and the Nisenan valley of Cullumah, plus the notes on 1963 words described above.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer: endings</div>Each day your student studies a real chapter ending, like &ldquo;They hit bedrock. And struck gold.&rdquo; and uses it to shape the ending of their own story.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: Publishing the Adventure</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>This week your student finishes the adventure story they have built over the unit by giving it a strong ending. <strong>Day 1:</strong> write three notes: what happens at the very end, who the hero has become, and what the story means. <strong>Day 2:</strong> draft the conclusion paragraph, with sentence frames for help. <strong>Day 3:</strong> put it at the end of the story and check the whole piece against a checklist. <strong>Day 4:</strong> read it out loud one last time and submit it with its title.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: How the Parts Combine</h2></div>
    <div class="poem-wrap">
      <div class="poem">Gaily bedight,<br>A gallant knight,<br>In sunshine and in shadow,<br>Had journeyed long,<br>Singing a song,<br>In search of Eldorado.<small>Edgar Allan Poe, &ldquo;Eldorado&rdquo; (1849)</small></div>
      <div><p>Poe wrote this poem in 1849, the year the Gold Rush began. On Day 2 your student explains how two parts of the poem work together, like its rhyme and the word <em>shadow</em> that comes back in every stanza. On Day 4 they put all the parts together and say what the poem means about searching for gold.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">Why did Praiseworthy speak up for Cut-Eye Higgins, a man who had cheated them?</span><span class="listen">Listen for: he had given his word in a bargain for the map, and he kept it.</span></li>
      <li><span class="q">How did the partners finally find gold?</span><span class="listen">Listen for: they were made to dig a grave, and at four feet they hit bedrock and gold.</span></li>
      <li><span class="q">Why did it matter so much when Praiseworthy called him &ldquo;Jack&rdquo;?</span><span class="listen">Listen for: he had always said &ldquo;Master Jack&rdquo;; dropping it showed they were true partners.</span></li>
      <li><span class="q">How did Praiseworthy beat the Mountain Ox?</span><span class="listen">Listen for: by dodging, jabbing and following what he read in a book about boxing, not by being bigger.</span></li>
      <li><span class="q">How did the book end? Were you surprised?</span><span class="listen">Listen for: the gold was lost in the bay, the family came to California, and Praiseworthy proposed to Aunt Arabella.</span></li>
      <li><span class="q">Tell me a word from the aud or val family.</span><span class="listen">Listen for: audience, audible; valiant, valuable (or any real ones).</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 reading or synthesis questions, that day&rsquo;s Word Study response, the Read Like a Writer box and the Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Day 4:</strong> the finished adventure story, with its title</li>
        <li><strong>Fluency:</strong> a recording of the last scene of the book</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> an ending that finishes the story&rsquo;s main problem, shows how the hero changed, and hints at what the story means.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Favorite ending:</strong> talk about the ending of a movie or book you both know. What made it work?</li>
        <li><strong>Root hunt:</strong> find an <em>aud</em> or <em>tract</em> word on a sign, a box or a screen.</li>
        <li><strong>Read the last line aloud:</strong> &ldquo;They looked very much like a family. They felt like a family. They were a family.&rdquo; Why three sentences?</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong><em>By the Great Horn Spoon!</em></strong> by Sid Fleischman · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 31</h2></div>
    <p><strong>Looking across the whole year.</strong> Your student compares the books they read this year on courage, independence and survival, and plans a cross-text comparison.</p>
  </section>

  <p class="foot"><a href="parent-guide-btghs-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole By the Great Horn Spoon! unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 30 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
"""
io.open('parent-guide-week-30.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-30.html')
