#!/usr/bin/env python3
"""Week 29 family guide (parent-guide-week-29.html) in the week 18 guide's look. Every line from the finished
week 29 lessons, Ch. 13-15 of By the Great Horn Spoon! (project doc text). History as on the 29.1-29.3 cards (Oakland Museum, PBS,
Calisphere, CA State Parks, Madley 2024). Nov 24 2026."""
import io, re
s = io.open('parent-guide-week-18.html', encoding='utf-8').read()
head = s[:s.index('<body>')]
head = re.sub(r'<title>[^<]*</title>', '<title>Week 29 Parent Guide · 5th Grade ELA · Optima Academy Online</title>', head)
assert '<title>Week 29' in head
B = """<body>
<div class="wrap">

  <header class="hero">
    <div class="hero-text">
      <div class="brand"><img src="https://raw.githubusercontent.com/optimaondemand/optima-assets/eeb0b335630058906d52f478028361d352253a93/images/Optima%20Final%20Circle%20-%20Owl%20Only.png" alt="Optima Academy Online">Family Guide · 5th Grade ELA</div>
      <h1>Week 29: Climb Out of the Coyote Hole</h1>
      <div class="sub"><em>By the Great Horn Spoon!</em> by Sid Fleischman, Chapters 13&ndash;15 and a voice and tone day</div>
      <div class="chips">
        <span class="chip">4 lessons</span>
        <span class="chip">1 fluency recording</span>
        <span class="chip">Fifth week of the book</span>
        <span class="chip">Check-In at week&rsquo;s end</span>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ Print this guide</button>
    </div>
    <div class="hero-art" style="background-image:url('assets/art/btghs/wenderoth-miners-cabin.jpg');background-position:center 40%;" role="img" aria-label="A colored print of miners inside a log cabin at night, one cooking at the fire and one holding out a little gold in his hand"></div>
  </header>

  <section class="howto">
    <h2>🧭 How the Lesson Pages Work</h2>
    <ul>
      <li><span>🗂️</span><strong>Four tabs, in order:</strong> Warm-Up → Word Study → Reading → Assignment (on Day 4 the Reading tab is called Voice &amp; Tone). A button at the bottom of each tab moves to the next.</li>
      <li><span>👣</span><strong>One step at a time.</strong> Each tab shows one activity at a time, and a Next button moves through its steps.</li>
      <li><span>📝</span><strong>Every answer goes on the page.</strong> There&rsquo;s a box for each one.</li>
      <li><span>💾</span><strong>Answers save as you type</strong>, but only in that browser on that computer. Switching computers or clearing the browser loses them.</li>
      <li><span>📓</span><strong>Copy your work</strong> at the bottom of the Assignment tab, then <strong>paste it into the assignment in Canvas and submit</strong>. A lesson isn&rsquo;t turned in until it&rsquo;s submitted there.</li>
      <li><span>🎙️</span><strong>Fluency is a separate page</strong> in the Canvas module, because recording doesn&rsquo;t work inside a lesson. Keep the book nearby.</li>
    </ul>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🧭</span><h2>This Week at a Glance</h2></div>
    <p>Jack and Praiseworthy settle into the diggings: red shirts, flea traps, and prices that are hard to believe. At an auction, one misheard word leaves Jack owing money for a whole bushel of neckties, and he pays rather than go back on his word. Then the partners buy a burro named Stubb, say goodbye to their friends in Hangtown, and go prospecting in the mountains, where Jack's hunting trip turns into an adventure. On Day 4 your student studies how Fleischman's voice works, and revises a paragraph of their own adventure story.</p>
    <div class="box b-rose" style="margin-bottom:12px;"><div class="box-label">💛 A note for families: words from 1963 and real history</div>This book was written in 1963, and three short passages this week use words from that time that are unkind and untrue. A folded note on each day's Reading tab names the words plainly and gives the true history, with no made-up voices. <strong>Chapter 13</strong> calls some of the auction crowd <em>Kanakas</em> from the Sandwich Islands, an old outsider label for Native Hawaiians; in fact Native Hawaiians came to California even before the Gold Rush, mined gold in it, and gave their name to places like Kanaka Creek. <strong>Chapter 14</strong> lists <em>savages</em> beside rabbits and outlaws; the hills the partners walk into were the homelands of the Nisenan, Miwok and Maidu peoples. <strong>Chapter 15</strong> has a prospector call Native people <em>Digger Indians</em> and compare them to children. Many Native Californians mined gold themselves (the chapter shows women panning in baskets), and then miners took their land and rivers; California's Native population fell from about 150,000 in 1848 to about 30,000 by 1870. The same chapter mentions Chinese miners working old claims, which was common, and in 1852 California passed a $3-a-month tax aimed at them. A separate card on Day 1 explains how miners really dug for gold. Sources: Oakland Museum of California; PBS <em>American Experience</em>; Calisphere (University of California); California State Parks.</div>
    <div class="glance">
      <div class="box b-sky"><div class="box-label">Reading skill</div><strong>How an author's choices create voice and tone.</strong> Your student notices word choices, short and long sentences, and how calm the narrator stays even in danger.</div>
      <div class="box b-green"><div class="box-label">Big idea</div><strong>Integrity: keeping your word.</strong> Jack pays for the neckties; Praiseworthy says of a promised fight, &ldquo;I gave my word, didn't I?&rdquo;</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">📅</span><h2>Day by Day</h2></div>
    <table class="days">
      <thead><tr><th>Lesson</th><th>Reading</th><th>Big question</th></tr></thead>
      <tbody>
        <tr>
          <td class="day-n">29.1<span>Day 1</span></td>
          <td><span class="ch">Chapter 13 · A Bushel of Neckties</span><br>Life in the diggings, a nugget in the grass roots, a letter from Dr. Buckbee, and a Cheap John auction where one word is misheard.<br><span class="pill p-extra">Real history: how miners dug for gold</span><span class="pill p-museum">Mining with the Long Tom, 1850s</span></td>
          <td>What does it mean to keep your word even when it costs you?</td>
        </tr>
        <tr>
          <td class="day-n">29.2<span>Day 2</span></td>
          <td><span class="ch">Chapter 14 · The Prospectors</span><br>Stubb the burro, who sometimes thinks he's a mule, the goodbyes in Hangtown, and a plan that comes from a book about boxing.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">On the Way to the Mines, 1850s</span></td>
          <td>What is Jack becoming?</td>
        </tr>
        <tr>
          <td class="day-n">29.3<span>Day 3</span></td>
          <td><span class="ch">Chapter 15 · The Man Who Couldn't Sit Down</span><br>Days of prospecting, news of an old enemy, and a hunting trip that goes wrong.<br><span class="pill p-museum">Grizzly Bear, 1848</span></td>
          <td>What keeps you going when the gold won't show up?</td>
        </tr>
        <tr>
          <td class="day-n">29.4<span>Day 4</span></td>
          <td><span class="ch">Voice and tone</span><br>Your student studies five of Fleischman's voice techniques, finds examples in Chapters 13&ndash;15, and picks the one their own adventure needs most.<br><span class="pill p-poem">Poetry Corner</span><span class="pill p-museum">Miner's Cabin, Result of the Day, 1852</span></td>
          <td>What gives Fleischman's writing its voice, and how can you use it in your own?</td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">🎙️<span>Fluency</span></td>
          <td colspan="2">A scene from Chapter 15, where Jack talks with the stranger who pulled him out of a hole, ending with &ldquo;Thank you, sir!&rdquo; Your student reads it to themselves, again for smoothness, and once more with expression, then <strong>records and submits it in Canvas.</strong></td>
        </tr>
        <tr class="extra-row">
          <td class="day-n">📋<span>Check-In</span></td>
          <td colspan="2">A 14-point wrap-up: sentence variety, the endings -ous, -ive and -ity, word families, four reading questions (one on description, one on the two poems), and a revised sentence from their adventure.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🔤</span><h2>Words to Know</h2><span class="tag">Use them at home!</span></div>
    <div class="words">
      <div class="word"><b>notoriety</b><span>being well known for something bold</span></div>
      <div class="word"><b>tenacious</b><span>holding on; refusing to give up</span></div>
      <div class="word"><b>evasive</b><span>tending to avoid or escape</span></div>
      <div class="word"><b>benefactor</b><span>a person who gives help</span></div>
      <div class="word"><b>prospector</b><span>a person who searches for gold</span></div>
    </div>
    <div class="glance" style="margin-top:12px;">
      <div class="box b-sky"><div class="box-label">Endings</div><strong>-ous</strong> means full of, <strong>-ive</strong> means tending to, and <strong>-ity</strong> names a quality.<span class="eg">courageous · attractive · generosity</span></div>
      <div class="box b-gold"><div class="box-label">Spelling</div><strong>Word families</strong> grow from one base. Know one member and you can check the others: decide, decision, decisive.<span class="eg">prospect · prospector · prospecting</span></div>
      <div class="box b-green"><div class="box-label">Grammar</div><strong>Sentence variety:</strong> mix short and long sentences, and start them in different ways.<span class="eg">After breakfast, they struck the tent. Stubb kicked. Jack held on.</span></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✨</span><h2>New This Week</h2></div>
    <div class="glance">
      <div class="box b-plum"><div class="box-label">⛏️ Climb Out of the Coyote Hole</div>The week&rsquo;s word game. A coyote hole is a deep shaft miners dug down to bedrock. Each clue has three choices; a right word hauls the bucket of pay dirt up one notch, and a wrong one lets it slide back down.</div>
      <div class="box b-gold"><div class="box-label">🌿 Virtue Watch: integrity</div>After reading, your student sorts everyday examples of keeping your word, picks a moment from Chapter 14, rates the road agent who gives back a stolen coat, and on Day 4 picks the moment of most integrity in the week.</div>
      <div class="box b-sky"><div class="box-label">🗺️ Real history, kept apart</div>A Day 1 card on coyote holes, rockers and long toms, and what gold dust was worth, plus the notes on 1963 words described above.</div>
      <div class="box b-green"><div class="box-label">📖 Read Like a Writer, every day</div>One line from the book a day, chosen to show voice, dialogue or description, like &ldquo;Yellow poppies had burst open on the hillsides like scatterings of fools&rsquo; gold.&rdquo;</div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">✍️</span><h2>Your Student&rsquo;s Writing: Revising an Adventure</h2><span class="tag">Writer&rsquo;s Workshop</span></div>
    <div class="essay"><span class="now">Day 1 · Plan</span><span class="now">Day 2 · Draft</span><span class="now">Day 3 · Revise</span><span class="now">Day 4 · Submit</span></div>
    <p>This week your student goes back to their own adventure story and makes one paragraph sound alive. <strong>Day 1:</strong> pick a paragraph and list three spots to change: the voice, a line of dialogue, and a vague detail. <strong>Day 2:</strong> rewrite it, starting with the dialogue, with sentence frames for help. <strong>Day 3:</strong> check it against a five-point checklist. <strong>Day 4:</strong> submit the final paragraph with one sentence about the biggest change.</p>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">🪶</span><h2>Poetry Corner: Every Part at Work</h2></div>
    <div class="poem-wrap">
      <div class="poem">Whenever the moon and stars are set,<br>Whenever the wind is high,<br>All night long in the dark and wet,<br>A man goes riding by.<small>Robert Louis Stevenson, &ldquo;Windy Nights&rdquo; (1885)</small></div>
      <div><p>On Day 2 your student names every part working in this galloping poem: its form, rhyme, beat, line breaks and comparisons. On Day 4 they read Carl Sandburg&rsquo;s quiet six-line &ldquo;Fog&rdquo; (1916) and explain how the same five parts can make the opposite feeling.</p></div>
    </div>
  </section>

  <section class="card">
    <div class="card-head"><span class="ico">💬</span><h2>Ask at Home</h2><span class="tag">Better than &ldquo;How was school?&rdquo;</span></div>
    <ol class="ask">
      <li><span class="q">How did Jack end up with a whole bushel of neckties?</span><span class="listen">Listen for: he said &ldquo;ate&rdquo; to a friend and the auctioneer heard &ldquo;eight&rdquo;; Jack paid rather than go back on his word.</span></li>
      <li><span class="q">What was Praiseworthy&rsquo;s plan for the neckties?</span><span class="listen">Listen for: he knew the miners would want them soon, and the money would buy them a burro.</span></li>
      <li><span class="q">What is a coyote hole, and what happened at one?</span><span class="listen">Listen for: a deep shaft dug to bedrock; Jack fell into one and fired his gun to call for help.</span></li>
      <li><span class="q">What happened when Praiseworthy opened the coat?</span><span class="listen">Listen for: there was no map, and he went right on to the next plan: &ldquo;Put some beans on to fry.&rdquo;</span></li>
      <li><span class="q">What makes Fleischman&rsquo;s writing sound like nobody else&rsquo;s?</span><span class="listen">Listen for: funny specific details, short sentences at big moments, a calm voice in danger, dialogue that sounds like real people.</span></li>
      <li><span class="q">Give me a word that ends in -ous, one in -ive, and one in -ity.</span><span class="listen">Listen for: courageous, creative, curiosity (or any real ones).</span></li>
    </ol>
  </section>

  <div class="two">
    <section class="card">
      <div class="card-head"><span class="ico">📬</span><h2>What Gets Turned In</h2></div>
      <ul class="check">
        <li><strong>Each lesson:</strong> 3 reading or voice questions, that day&rsquo;s Word Study response, the Read Like a Writer box and the Writer&rsquo;s Workshop step, copied and pasted into Canvas</li>
        <li><strong>Fluency:</strong> a recording of the Chapter 15 scene</li>
        <li><strong>Check-In:</strong> at the end of the week</li>
      </ul>
      <p class="small" style="margin-top:10px;"><strong>Done well looks like:</strong> a revised paragraph with one specific detail, dialogue that sounds like the character, and sentences that start in different ways.</p>
    </section>
    <section class="card">
      <div class="card-head"><span class="ico">🏡</span><h2>Try at Home</h2><span class="tag">5 minutes</span></div>
      <ul class="check">
        <li><strong>Build a family:</strong> start with <em>act</em> or <em>sign</em> and see how many family members your student can name.</li>
        <li><strong>Make it specific:</strong> say a plain sentence (&ldquo;The dog was big&rdquo;) and let your student make it vivid.</li>
        <li><strong>Read it two ways:</strong> read a scary sentence in a scared voice, then in a calm voice. Which is funnier?</li>
      </ul>
    </section>
  </div>

  <section class="card">
    <div class="card-head"><span class="ico">🎒</span><h2>Have on Hand</h2></div>
    <p><strong><em>By the Great Horn Spoon!</em></strong> by Sid Fleischman · <strong>A device that records audio</strong> for the fluency reading</p>
  </section>

  <section class="card next">
    <div class="card-head"><span class="ico">🔭</span><h2>Coming Up in Week 30</h2></div>
    <p><strong>Chapters 16&ndash;18, the last three chapters.</strong> The partners set out for Shirt-tail Camp, and the novel comes to its end.</p>
  </section>

  <p class="foot"><a href="parent-guide-btghs-unit.html" style="color:#1F6FA8;font-weight:700;">See the whole By the Great Horn Spoon! unit →</a><br><br>Optima Academy Online · 5th Grade ELA · Week 29 Family Guide<br>Questions? Reach out to your student&rsquo;s teacher anytime.</p>
</div>
</body>
</html>
"""
io.open('parent-guide-week-29.html', 'w', encoding='utf-8').write(head + B)
print('wrote parent-guide-week-29.html')
