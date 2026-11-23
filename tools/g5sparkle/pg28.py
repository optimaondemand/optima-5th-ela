#!/usr/bin/env python3
"""Week 28 family guide (parent-guide-week-28.html) in the week 18 guide's look. Every line from the finished
week 28 lessons, Ch. 10-12 of By the Great Horn Spoon! (project doc text). History as on the 28.2 card (City of Placerville, CA State Parks, Calisphere).
Nov 23 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 28 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 28' in head
B = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 28: Pan for Color</h1>
      <div class="sub"><em>By the Great Horn Spoon!</em> by Sid Fleischman, Chapters 10&ndash;12 and a theme response</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Fourth week of the book</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/btghs/currier-gold-mining-california.jpg');background-position:center 60%;" role="img" aria-label="A hand-colored print of miners panning and shoveling dirt into a long trough in a mountain stream, with pine trees and snowy peaks behind"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment (on Day 4 the Reading tab is called Theme). A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson. Keep the book nearby.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>The stagecoach climbs into the gold country with Cut-Eye Higgins aboard. Road agents stop the stage, and Praiseworthy keeps their gold dust safe in the fingers of his glove, until a robber takes the one thing he will not give up. In Hangtown, Jack learns to pan from a miner named Pitch-pine Billy, earns the name Jamoka Jack, and Praiseworthy&rsquo;s umbrella becomes a gold pan. Back in town, the partners find that the story of the robbery has grown. On Day 4 your student names a theme of the novel and argues for it with evidence.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families: real history this week</div>Chapters 10 to 12 do not use the 1963 language about any group of people that appeared in Chapters 8 and 9. The hard history this week is the name <strong>Hangtown</strong>. It was a real gold camp, first called Dry Diggings. In 1849 a crowd there hanged three men accused of robbery, without a real trial, and the camp was called Hangtown after that; in 1854 it became Placerville, the name it still has. The book jokes about the name, as many old stories did. A short folded card on Day 2 says what really happened, calmly, and keeps it apart from the novel. The same card notes that dry washing, which Pitch-pine Billy shows Jack, was a method of miners from Sonora, Mexico, and that in 1850 California taxed miners who were not American citizens $20 a month, a law that drove many Mexican and Latin American miners from the mines before it was ended in 1851. Sources: City of Placerville; California State Parks; Calisphere (University of California).</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>How events and conflicts build a theme.</strong> Your student collects events and conflicts, watches what each character chooses, and names the big idea they add up to.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Honesty.</strong> Praiseworthy tries to tell Hangtown the truth, &ldquo;But not under false colors,&rdquo; and then has to decide what to do when no one wants to hear it.</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">28.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 10 · The Rogue Out-Rogued</span><br>Cut-Eye Higgins on the stagecoach, a nap, a steep climb, road agents in red bandanas, and gold dust hidden in a white glove.<br><span class="pill p-museum">The Old Stage-Coach of the Plains, 1901</span></td>
          <td>What separates someone who is brave from someone who is reckless?</td>
        </tr>
        <tr>
          <td class="day-n">28.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 11 · Jamoka Jack</span><br>Hangtown at last, bread at a dollar a slice, a washpan shot by mistake, dry washing, icy water, and a cup of coffee Jack can hardly swallow.<br><span class="pill p-extra">Real history: Hangtown</span><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Gold Mining in California, about 1871</span></td>
          <td>What do you do when a long journey leads to frozen feet and terrible coffee?</td>
        </tr>
        <tr>
          <td class="day-n">28.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 12 · Bullwhip</span><br>A barefoot walk home by the campfires, a question about Aunt Arabella&rsquo;s picture, and a town with a story to tell.<br><span class="pill p-extra">A hero story that isn&rsquo;t quite true</span><span class="pill p-museum">Sunday Morning in the Mines, 1872</span></td>
          <td>What does a legend tell you about what a community values?</td>
        </tr>
        <tr>
          <td class="day-n">28.4<span>Day 4</span></td>
          <td><span class="ch">Theme response</span><br>Your student chooses one of four theme claims or writes their own, finds evidence in Chapters 1&ndash;12, then argues the other side and answers it with evidence.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Among the Sierra Nevada, 1868</span></td>
          <td>What theme has Fleischman been building from Chapter 1 to Chapter 12?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">The Bullwhip scene from Chapter 12, from the porch of the Empire Hotel to &ldquo;Yes, sir &mdash; Bullwhip.&rdquo; Your student reads it once to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up: transitions and introductory phrases, the roots fort and val/valid, the endings -ity, -ment and -ness, four reading questions (one on a character&rsquo;s choice, one on the poem), and the opening of a literary response.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>fortitude</b><span>strength and courage in hard times</span></div>
      <div class="word"><b>valor</b><span>great bravery in danger</span></div>
      <div class="word"><b>validity</b><span>being sound and true</span></div>
      <div class="word"><b>highwayman</b><span>a robber who stops travelers on the road</span></div>
      <div class="word"><b>exasperation</b><span>great annoyance</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Roots</div><strong>fort</strong> means strong and <strong>val / valid</strong> mean strong or worth.<span class="eg">fortify · comfort · valuable · evaluate</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>-ity, -ment and -ness</strong> turn a word into the name of an idea. Watch the base: lonely → loneliness, argue → argument, curious → curiosity.<span class="eg">boldness · achievement · validity</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Transitions and introductory phrases</strong> link ideas and take a comma.<span class="eg">At first, Jack could barely swallow the coffee. However, he kept drinking.</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">🪙 Pan for Color</div>The week&rsquo;s word game. Each pan holds four words: two are gold and two are slickens (mud). Your student washes out the misspelled endings and the look-alike words with no real fort or val root (like <em>fortune</em> and <em>valley</em>), and the gold goes into Jack&rsquo;s pouch.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: honesty</div>After reading, your student sorts everyday examples, picks the most honest moment in Chapters 10 and 11, rates how honest Praiseworthy is with the tall tale, and on Day 4 picks the most honest moment of the week.</div>
      <div class="box b-sky"><div class="box-label">🗺️ Real history, kept apart</div>Two short cards on Day 2: the true story of Hangtown and the miners from Sonora, and the miners&rsquo; words in the book (jamoka, spangles, slickens, mountain canary), each with the line where it appears.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer, every day</div>One line from the book a day, chosen to show how a character&rsquo;s choice builds a theme, like Praiseworthy&rsquo;s warning about Aunt Arabella&rsquo;s picture: &ldquo;I&rsquo;ll thank you to return that picture to my bag.&rdquo;</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: A Literary Response</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>This week your student writes <em>about</em> the novel: a claim about its theme, proved with what characters choose to do. <strong>Day 1:</strong> plan a one-sentence theme claim and two character choices that could prove it. <strong>Day 2:</strong> draft, with sentence frames for help. <strong>Day 3:</strong> revise with a checklist: a claim that is an idea, not a topic; two pieces of evidence, each explained; a transition; and a closing that says why it matters. <strong>Day 4:</strong> submit.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: More Than One Theme</h2></div>
    <div class="poem-wrap">
      <div class="poem">He clasps the crag with crooked hands;<br>Close to the sun in lonely lands,<br>Ring&rsquo;d with the azure world, he stands.<small>Alfred, Lord Tennyson, &ldquo;The Eagle&rdquo; (1851)</small></div>
      <div><p>Is this a poem about <strong>power</strong> or about <strong>being alone</strong>? Both are in the words. On Day 2 your student argues for both readings; on Day 4 they look for one scene in the novel that carries two themes at once.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">How did Praiseworthy keep the gold dust safe from the road agents?</span><span class="listen">Listen for: it was in the fingertips of his glove; he pulled the glove off &ldquo;carefully but casually,&rdquo; and the dust stayed inside.</span></li>
      <li><span class="q">What finally made calm Praiseworthy lose his temper?</span><span class="listen">Listen for: a robber took Aunt Arabella&rsquo;s picture.</span></li>
      <li><span class="q">How did Jack earn the name Jamoka Jack?</span><span class="listen">Listen for: he kept drinking Pitch-pine Billy&rsquo;s terrible coffee so the miner wouldn&rsquo;t take the name back.</span></li>
      <li><span class="q">Why was the town called Hangtown?</span><span class="listen">Listen for: a crowd hanged men there in 1849 without a real trial; later the town was renamed Placerville.</span></li>
      <li><span class="q">What theme did you choose, and what is your best evidence?</span><span class="listen">Listen for: an idea about life (not just a topic) and a character&rsquo;s choice from the book.</span></li>
      <li><span class="q">What do fort and val mean? Name a word for each.</span><span class="listen">Listen for: strong (fortify, comfort); strong or worth (valor, valuable).</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 reading or theme questions, that day&rsquo;s Word Study response, the Read Like a Writer box and the Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Bullwhip scene in Chapter 12</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> a theme claim that is an idea, evidence from a character&rsquo;s choice, and a sentence that explains what the choice shows.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Gold or mud?</strong> Say a word like <em>fortune</em>, <em>fortress</em>, <em>valley</em> or <em>valuable</em>, and let your student say if it has a real fort or val root.</li>
        <li><strong>Name the idea:</strong> pick a word like <em>kind</em>, <em>pay</em> or <em>curious</em> and turn it into an idea word with -ness, -ment or -ity.</li>
        <li><strong>Find it on a map:</strong> Sacramento, then Placerville in the Sierra foothills.</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong><em>By the Great Horn Spoon!</em></strong> by Sid Fleischman · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 29</h2></div>
    <p><strong>Chapters 13&ndash;15.</strong> Life in the diggings goes on, and Jack and Praiseworthy look for a claim of their own.</p>
  </section>

  <p class="foot"><a href="parent-guide-btghs-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole By the Great Horn Spoon! unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 28 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
"""
io.open('parent-guide-week-28.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-28.html')
