#!/usr/bin/env python3
"""Week 31 accuracy fixes (approved by Bethany Nov 24 2026; audit claude/g5-ela-wk31-audit.md).
Groups: real sources (no invented diary or invented 'secondary source'), five novels with How I Became a Ghost back,
wrong book claims rewritten from checked facts, page fixes, fluency menu of five checked continuous passages.
Book lines checked against: Witch OCR (Ch. 14), Johnny Tremain PDF text (Ch. 8, Ch. 12), Bowditch OCR (Ch. 22),
hbg_ocr.txt (Ch. 1), the By the Great Horn Spoon! project doc (Ch. 1). Real sources: Bigler (30.1 card), Taylor (27.4), Harkins (24.3).
Every replacement asserts its count; div balance must not change; nothing is written unless every file passes.
    python tools/g5sparkle/fix_wk31.py [--apply]"""
import io, re, sys
F = {1: 'lesson-31-1-comparison-plan.html', 2: 'lesson-31-2-comparison-sources.html', 3: 'lesson-31-3-comparison-draft.html',
     4: 'lesson-31-4-comparison-submit.html', 'flu': 'lesson-31-fluency.html'}
def grp(a, mid, b, new, n=1):
    return (re.compile('(' + a + ')' + mid + '(' + b + ')', re.S), lambda m: m.group(1) + new + m.group(2), n)
def QUOTE(text, attr):
    return [grp(r'<div class="quote-strip-text">', r'.*?', r'</div>', text), grp(r'<div class="quote-strip-attr">', r'.*?', r'</div>', attr)]
NOTES = ('As you read, pay close attention to the characters&#x27; actions and motivations. Think about how events connect to the bigger ideas in the story. Use your journal to capture your thoughts and any questions that come up.',
         'This week you look back across all five novels and compare how two of them handle the same big idea. Keep your reading journal and your notes from the year close by.', 1)
def stop(icon, color, wk, title, cls='umap-done'):
    return ('<div class="umap-stop %s"><div class="umap-circle" style="background:%s;border-color:%s;">%s</div><div class="umap-label">%s</div>'
            '<div class="umap-sub" style="max-width:60px;white-space:normal;text-align:center;line-height:1.2;font-size:9px;">%s</div></div>') % (cls, color, color, icon, wk, title)
CON = '<div class="umap-connector"></div>'
JOURNEY = CON.join([stop('📜', '#7B5EA7', 'Wks 1–5', 'The Witch of Blackbird Pond'), stop('🎨', '#C0392B', 'Wks 6–8', 'Johnny Tremain'),
                    stop('🧭', '#1565C0', 'Wks 9–14', 'Carry On, Mr. Bowditch'), stop('✍️', '#2E7D32', 'Wks 15–17', 'Writer&rsquo;s Workshop'),
                    stop('🐕', '#5D4037', 'Wks 18–24', 'How I Became a Ghost'), stop('⛏️', '#C8862A', 'Wks 25–30', 'By the Great Horn Spoon!'),
                    stop('🔍', '#00695C', 'Wks 31–32', 'Journey&rsquo;s End', 'umap-active')])
JOURNEY_FIX = grp(r'<div class="umap-row">', r'.*?', r'</div>\s*<div class="tracker-chapter-label"', JOURNEY + '</div>\n    ', 1)
JOURNEY_FIX = (re.compile(r'(<div class="umap-row">).*?(</div>\s*<div class="tracker-chapter-label")', re.S), lambda m: m.group(1) + JOURNEY + '</div>\n    <div class="tracker-chapter-label"', 1)
CAST = 'Kit Tyler (WOBP) · Johnny Tremain · Nat Bowditch (CMB) · Jack &amp; Praiseworthy (BTGHS)'
CAST_NEW = 'Kit Tyler (<em>Witch</em>) · Johnny Tremain · Nat Bowditch (<em>Bowditch</em>) · Isaac (<em>Ghost</em>) · Jack &amp; Praiseworthy (<em>Horn Spoon</em>)'
CHK = ('I wrote my DOL edit and RWM journal in my reading journal.', 'I wrote my Daily Oral Language fix in my reading journal.', 1)

SOURCES = '''<div class="passage-block">
  <div class="passage-label">📜 Background — the five novels and their real times</div>
  <div class="passage-text">
    <p>Each novel this year is set in a real time and place. <em>The Witch of Blackbird Pond</em> opens in 1687 in Wethersfield, in the Connecticut colony. <em>Johnny Tremain</em> runs from 1773 to 1775 in Boston, as the Revolution begins. <em>Carry On, Mr. Bowditch</em> follows a real boy, Nathaniel Bowditch, in Salem from 1779 into the early 1800s. <em>How I Became a Ghost</em> begins in 1830, when the Choctaw Nation was forced to leave its homeland in Mississippi. <em>By the Great Horn Spoon!</em> starts on January 27, 1849, the year of the California Gold Rush.</p>
    <p>A novel can show you a made-up character&rsquo;s thoughts. A <strong>primary source</strong> is something made at the time by someone who was there: a diary, a letter, a newspaper report. It cannot show you a character&rsquo;s thoughts, but it shows you what one real person saw and believed.</p>
    <p style="font-size:12px;color:#7A88A8;margin-top:12px;font-style:italic;">Background written by Optima for this lesson. Not a primary source.</p>
  </div>
</div>
      <div class="passage-block">
  <div class="passage-label">📜 Primary Source A — Henry Bigler&rsquo;s diary, January 24, 1848</div>
  <div class="passage-text">
    <p><em>Henry Bigler worked at the sawmill James Marshall was building for John Sutter at Coloma, California. On the day Marshall found gold in the mill&rsquo;s tailrace, Bigler wrote this in his diary. The spelling is his own.</em></p>
    <p>&ldquo;This day some kind of mettle was found in the tailrace that looks like goald.&rdquo;</p>
    <p style="font-size:12px;color:#7A88A8;margin-top:12px;font-style:italic;">Henry W. Bigler, diary entry, January 24, 1848. Public domain. You met this line on the Sutter&rsquo;s Mill card in Week 30.</p>
  </div>
</div>
      <div class="passage-block">
  <div class="passage-label">📜 Primary Source B — Bayard Taylor, <em>Eldorado</em> (1850)</div>
  <div class="passage-text">
    <p><em>Bayard Taylor was a newspaper reporter. He sailed into San Francisco on August 18, 1849, a few months after the Lady Wilma, and wrote what he saw.</em></p>
    <p>A furious wind was blowing down through a gap in the hills, filling the streets with clouds of dust. On every side stood buildings of all kinds, begun or half-finished, and the greater part of them mere canvas sheds, open in front, and covered with all kinds of signs, in all languages. &hellip; I asked the landlord whether he could send a porter for our trunks. &ldquo;There is none belonging to the house,&rdquo; said he; &ldquo;every man is his own porter here.&rdquo;</p>
    <p style="font-size:12px;color:#7A88A8;margin-top:12px;font-style:italic;">Bayard Taylor, <em>Eldorado, or, Adventures in the Path of Empire</em>, vol. 1 (1850), chapters V&ndash;VI. Public domain. &hellip; marks words left out. You read more of it in Week 27.</p>
  </div>
</div>
      <div class="passage-block">
  <div class="passage-label">📜 Primary Source C — George W. Harkins, &ldquo;To the American People&rdquo; (1831)</div>
  <div class="passage-text">
    <p><em>George W. Harkins was a Choctaw leader. He wrote this letter as the Choctaw people were being forced to leave Mississippi, the history behind <em>How I Became a Ghost</em>.</em></p>
    <p>&ldquo;Yet it is said that our present movements are our own voluntary acts &mdash; such is not the case. &hellip; We go forth sorrowful, knowing that wrong has been done. &hellip; Here is the land of our progenitors, and here are their bones &hellip; it is dear to us, yet we cannot stay, my people are dear to me, with them I must go.&rdquo;</p>
    <p style="font-size:12px;color:#7A88A8;margin-top:12px;font-style:italic;">George W. Harkins, &ldquo;To the American People&rdquo; (1831), from the Choctaw Nation&rsquo;s text. &hellip; marks words left out. You studied this letter in Week 24.</p>
  </div>
</div>
'''
SQ1 = ('The primary source diary defines courage as &ldquo;the quiet thing a man does when no one is watching.&rdquo; Which of the year&rsquo;s novel characters best fits this definition? Give one specific example from the novel.',
       'Choose the primary source that fits your theme and your novels best: A, B or C. Name who made it, when, and why they were writing. Then tell which of your two novels it connects to.', 1)
SQ1L = ('data-label="Source Q1: Which novel character best fits the primary source definition of courage — with specific evidence" placeholder="The character who best fits this definition is ___ from ___.&#10;&#10;Specifically, in chapter ___, ..."',
        'data-label="Source Q1: My primary source, who made it, when and why, and which novel it connects to" placeholder="I chose Source ___.&#10;It was written by ___ in ___ because...&#10;It connects to ___ because..."', 1)
SQ2 = ('The secondary source identifies three kinds of courage: <em>endurance</em> (Puritan era), <em>resistance</em> (Revolutionary era), and <em>persistence</em> (Gold Rush era). Match each of the year&rsquo;s four novels to one of these three kinds. Explain your choices in 2–3 sentences.',
       'What can your primary source tell you that your novel cannot? What can your novel show that the source cannot? Write 2&ndash;3 sentences.', 1)
SQ2L = ('data-label="Source Q2: Match each year\'s novel to endurance/resistance/persistence — explained" placeholder="Witch of Blackbird Pond → ___ because...&#10;Johnny Tremain → ___ because...&#10;Carry On, Mr. Bowditch → ___ because...&#10;By the Great Horn Spoon! → ___ because..."',
        'data-label="Source Q2: What the source can tell that the novel cannot, and the other way round" placeholder="My source can tell me... that the novel cannot.&#10;My novel can show... that the source cannot."', 1)

FIX = {
 1: QUOTE('&ldquo;We give all we have, lives, property, safety, skills &hellip; we fight, we die, for a simple thing. Only that a man can stand up.&rdquo;',
          'Esther Forbes, <em>Johnny Tremain</em>, Chapter 8 &bull; James Otis speaking') + [
   ('You have read four major novels this year. Each tells a different story — but all four share big themes. This week you write your final comparison project: a multi-paragraph essay arguing how two novels explore the same theme in different ways. Today you choose your theme and your texts, and you plan.',
    'You have read five novels this year. Each tells a different story, but they share big themes. This week you write your final comparison project: a five-paragraph essay showing how two novels explore the same theme in different ways. Today you choose your theme and your two novels, and you plan.', 1),
   NOTES,
   ('the limits that colonial society places on a self educated sailor however', 'an indenture that ends his schooling however', 1),
   ('the limits that colonial society places on a self-educated sailor. However,', 'an indenture that ends his schooling. However,', 1),
   ('Consequently, all four novels suggest that the bravest act', 'Consequently, both novels suggest that the bravest act', 1),
   ('Like Isaac, Jack measures himself against an adult he admires.', 'Like Isaac, Jack faces a long, hard journey west.', 1),
   ('Whereas Isaac walks toward grief, Jack walks toward fortune.', 'Whereas Isaac walks the Trail with his family, Jack runs away from his.', 1),
   ('Isaac loses a family; Jack only risks one.', 'Isaac loses his home; Jack leaves his by choice.', 1),
   JOURNEY_FIX,
   ('You have met six books this year,', 'You have read five novels this year,', 1),
   (CAST, CAST_NEW, 3),
   ('then write a 3–4 paragraph comparison essay', 'then write a five-paragraph comparison essay', 1),
   CHK],
 2: QUOTE('&ldquo;This day some kind of mettle was found in the tailrace that looks like goald.&rdquo;',
          'Henry Bigler&rsquo;s diary, January 24, 1848 &bull; Real primary source, his own spelling') + [
   ('A novel shows you the inside of a character&rsquo;s mind. A primary source — a letter, diary, speech — shows you what a real person actually said in the moment. A secondary source gives historical context. Good comparisons draw from all three.',
    'A novel shows you the inside of a character&rsquo;s mind. A primary source, like a letter, a diary or a news report, shows what a real person saw and wrote at the time. Today you read three real ones from this year and choose one for your essay.', 1),
   NOTES,
   (re.compile(r'(<div class="dol-model-sentence" id="dolModel">).*?(</div>)', re.S),
    lambda m: m.group(1) + '<span class="dol-highlight-word" onclick="dolWord(this,\'A <em>while</em> clause opens the sentence and sets one book beside the other, and a comma ends it. Two things are happening in two places, and one sentence holds both.\')">While Kit Tyler stands trial in Wethersfield,</span> Johnny Tremain carries messages for the patriots in Boston.' + m.group(2), 1),
   (re.compile(r'(<div class="dol-fix-sentence">)[^<]*(</div>)'), lambda m: m.group(1) + 'henry bigler worked at sutters mill in 1848 he wrote in his diary that gold was found however a diary cannot tell us how jack and praiseworthy felt about the diggings' + m.group(2), 1),
   (re.compile(r'(id="dolAns2"><p><strong>Corrected:</strong> ).*?(</p>)', re.S),
    lambda m: m.group(1) + 'Henry Bigler worked at Sutter&rsquo;s Mill in 1848. He wrote in his diary that gold was found. However, a diary cannot tell us how Jack and Praiseworthy felt about the diggings.</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capitals for names and places; an apostrophe in <em>Sutter&rsquo;s</em>; periods to end two sentences; a comma after <em>However</em>.' + m.group(2), 1),
   ('Today you read two short source texts — a diary excerpt (primary) and a historical analysis (secondary). In your journal: What is the difference between a primary and secondary source? Write 2 sentences defining each before you read.',
    'Today you read three short primary sources, all from this year. In your journal: What is a primary source? Write 2 sentences before you read.', 1),
   JOURNEY_FIX,
   ('Today you read a primary source beside a secondary one. They are not two versions of the same thing. A primary source was made by somebody who was there; a secondary source was written later, by somebody deciding what it meant. Both are useful, and they are useful in different ways.',
    'Today you read real primary sources beside the novels. They are not two versions of the same thing. A primary source was made by somebody who was there; a novel was written later, by an author who imagined people living through it. Both are useful, in different ways.', 1),
   ('What can the primary source tell you that the secondary one cannot? And the other way round?', 'What can your primary source tell you that your novel cannot? And the other way round?', 1),
   ('Where do these sources disagree, and what might explain it?', 'Where does the source agree with your novel, and where does it show something different?', 1),
   ('<div class="activity-title">Read: Primary &amp; Secondary Sources on Courage</div><div class="activity-sub">What does historical evidence add to a literary argument?</div>',
    '<div class="activity-title">Read: Three Real Primary Sources</div><div class="activity-sub">What does a real voice from the time add to your comparison?</div>', 1),
   ('<p><strong>1. Connect:</strong> Does this source support, complicate, or add to what the novel shows?</p>',
    '<p><strong>1. Connect:</strong> Does this source agree with, complicate, or add to what your novel shows?</p>', 1),
   (re.compile(r'<div class="passage-block">\s*<div class="passage-label">📜 Primary Source — Diary of a Forty-Niner \(1849\)</div>.*?Written for Optima Academy Online, 5th Grade ELA\.</p>\s*</div>\s*</div>\n', re.S), lambda m: SOURCES, 1),
   SQ1, SQ1L, SQ2, SQ2L,
   ('Using <strong>both</strong> a literary source (one of the year&rsquo;s novels) and one of today&rsquo;s informational sources, write a 3-sentence argument',
    'Using <strong>both</strong> one of your novels and your primary source, write a 3-sentence argument', 1),
   ('Source evidence: The [primary/secondary] source confirms this when it states...', 'Source evidence: In [source], [who] writes...', 1),
   ('<span class="obj-icon">📜</span><span><strong>Sources:</strong> I will read a primary and secondary source and identify evidence relevant to my theme.</span>',
    '<span class="obj-icon">📜</span><span><strong>Sources:</strong> I will read three real primary sources and choose one that fits my theme.</span>', 1),
   CHK],
 3: QUOTE('&ldquo;And when you depend on a book and it has a mistake, you&rsquo;d have been safer not depending on it.&rdquo;',
          'Jean Lee Latham, <em>Carry On, Mr. Bowditch</em>, Chapter 22 &bull; Nat Bowditch speaking') + [
   NOTES,
   (re.compile(r'(<div class="dol-model-sentence" id="dolModel">).*?(</div>)', re.S),
    lambda m: m.group(1) + 'In contrast to Kit Tyler, <span class="dol-highlight-word" onclick="dolWord(this,\'This clause adds extra facts about Kit, so commas go on both sides of it. Take it out and the sentence still stands: In contrast to Kit Tyler, Jack Flagg tells the captain the truth.\')">who keeps her visits to Hannah a secret,</span> Jack Flagg tells the captain the truth the moment he meets him.' + m.group(2), 1),
   ('This difference is significant because it shows two distinct social contexts: in Puritan New England, courage had to be invisible to be safe; in Gold Rush California, courage could be visible because no one had the authority to punish it.',
    'This difference matters because of where they live: in Wethersfield, Kit&rsquo;s friendship with Hannah Tupper could get her tried as a witch, so she keeps it quiet; at Shirt-tail Camp, Praiseworthy&rsquo;s calm speech works because the crowd stops to listen.', 1),
   ('> Isaac walks toward grief, Jack walks toward fortune.', '> Isaac walks the Trail with his family, Jack runs away from his.', 1),
   ('> Isaac, Jack measures himself against an adult.', '> Isaac, Jack faces a long, hard journey west.', 1),
   ('Isaac loses a family; Jack, <input', 'Isaac loses his home; Jack, <input', 1),
   ('>, only risks one.</div>', '>, leaves his by choice.</div>', 1)],
 4: QUOTE('&ldquo;Maybe you have never read a book written by a ghost before. I am a ghost.&rdquo;',
          'Tim Tingle, <em>How I Became a Ghost</em>, Chapter 1 &bull; Isaac speaking') + [
   NOTES,
   ('memorise', 'memorize', 1), ('Synthesise &mdash;', 'Synthesize &mdash;', 1), ('recognise', 'recognize', 1),
   ('<div class="activity-num" style="background:#7B5EA7;">4</div><div style="flex:1;"><div class="activity-title">&#x1F520; Spelling: Cumulative Review</div>',
    '<div class="activity-num" style="background:#7B5EA7;">3</div><div style="flex:1;"><div class="activity-title">&#x1F520; Spelling: Cumulative Review</div>', 1),
   ('<div class="activity-num" style="background:#52B788;">3</div><div style="flex:1;"><div class="activity-title">✏️ Grammar: Final Conventions Check</div>',
    '<div class="activity-num" style="background:#52B788;">4</div><div style="flex:1;"><div class="activity-title">✏️ Grammar: Final Conventions Check</div>', 1),
   ('<p><strong>Gold Rush/adventure (BTGHS):</strong>', '<p><strong>Choctaw history (<em>How I Became a Ghost</em>):</strong> ancestors, honored, distraction, speechless</p>\n  <p><strong>Gold Rush/adventure (<em>Horn Spoon</em>):</strong>', 1),
   ('at least one from each of the three novel units', 'from at least three different novels', 1)],
}
PASS = [
 ('The Witch of Blackbird Pond', 'Elizabeth George Speare', 'Chapter 14', 'Kit sees the Dolphin come up the river.',
  ['An odd confusion, half eagerness and half reluctance, tossed Kit&rsquo;s spirits to and fro. She was minded to stay at home and help Mercy, even as her feet hurried her along the path beside Judith. But the moment they rounded the bend in the road she forgot her uncertainty. There was the Dolphin coming up the river with all her sails. The curving tail of the prow was chipped and dull; the hull was battered and knobby with barnacles, the canvas dark and weathered, yet how beautiful she was! In a surge of memories, Kit could almost feel the deck lifting beneath her feet, and a longing almost like homesickness caught at her throat. How she would love to sail on the Dolphin again!']),
 ('Johnny Tremain', 'Esther Forbes', 'Chapter 12', 'The last page of the novel.',
  ['Everywhere else in the village was silence. The music, small as the chirping of a cricket, filled that silence. Down the road came twenty or thirty tired and ragged men. Some were bloodstained. No uniforms. A curious arsenal of weapons. The long horizontal light of the sinking sun struck into their faces and made them seem much alike. Thin-faced in the manner of Yankee men. High cheek-boned. Unalterably determined. The tired men marched unevenly, but Johnny noticed the swing of the lithe, independent bodies. The set of chin and shoulders. Rab had been like that.',
   'Please God, out of this New England soil such men would forever rise up ready to fight when need came. The one generation after the other.']),
 ('Carry On, Mr. Bowditch', 'Jean Lee Latham', 'Chapter 22', 'Dr. Holyoke and Nat talk about science and mistakes.',
  ['&ldquo;All my life, I&rsquo;ve felt as though I made three steps forward with science, and got dragged back two steps by the ignorance and superstitions of mankind. And every time a doctor &lsquo;loses&rsquo; a patient, no matter why, it gives science another setback.&rdquo;',
   '&ldquo;And every time a ship is lost,&rdquo; Nat added, &ldquo;it gives scientific navigation a setback, too. Men blame the books. They&rsquo;ve been right to blame them, sometimes. There have been errors in the books. And when you depend on a book and it has a mistake, you&rsquo;d have been safer not depending on it.&rdquo;',
   '&ldquo;But your book isn&rsquo;t going to have mistakes!&rdquo; Polly said. &ldquo;When men depend on it &mdash;&rdquo;',
   'Nat didn&rsquo;t smile. &ldquo;It will take a long time to convince them.&rdquo;']),
 ('How I Became a Ghost', 'Tim Tingle', 'Chapter 1', 'Isaac introduces himself.',
  ['Maybe you have never read a book written by a ghost before. I am a ghost. I am not a ghost when this book begins, so you have to pay very close attention. I should tell you something else. I see things before they happen. You are probably thinking, &ldquo;I wish I could see things before they happen.&rdquo;',
   'Be careful what you wish for.',
   'I&rsquo;m ten years old and I&rsquo;m not a ghost yet. My name is Isaac and I have a mother and a father and a big brother, Luke. I have a dog, too. His name is Jumper and he is my best friend. We go everywhere together. We swim in the river together; we chase chickens together.']),
 ('By the Great Horn Spoon!', 'Sid Fleischman', 'Chapter 1', 'Jack answers the captain.',
  ['&ldquo;Sir,&rdquo; said Jack, trembling inwardly. &ldquo;I don&rsquo;t care to be ship&rsquo;s boy.&rdquo;', '&ldquo;What!&rdquo;',
   '&ldquo;If Praiseworthy is going to the coal bunkers &mdash; I&rsquo;ll shovel coal too.&rdquo; Jack met Praiseworthy&rsquo;s glance, but only for a moment. &ldquo;We&rsquo;re partners, sir. Either send me to the coal bunkers or &mdash;,&rdquo; he gulped, &ldquo;or put me in chains.&rdquo;',
   'The wild bull of the seas was struck absolutely speechless.',
   '&ldquo;Don&rsquo;t pay any attention to Master Jack,&rdquo; said Praiseworthy quickly. &ldquo;The boy is light-headed from sheer hunger. He hasn&rsquo;t eaten since yesterday and he doesn&rsquo;t know what he&rsquo;s saying.&rdquo;',
   '&ldquo;Yes, I do,&rdquo; said Jack. &ldquo;You told me yourself we&rsquo;d stick together &mdash; through thick and thin.&rdquo;']),
]
def passages():
    out = ['  <div class="passage">\n    <div class="passage-label">📜 Choose One Passage — five real stretches, one from each novel</div>\n'
           '    <p style="font-size:14px;color:#3A4A6B;margin:6px 0 12px;">Tap a novel to open its passage. Each one is copied from the book, one stretch with nothing left out. Pick the one you want to read aloud.</p>\n']
    for i, (book, author, ch, what, paras) in enumerate(PASS):
        body = ''.join('<p>%s</p>' % p for p in paras)
        out.append(('    <details class="flu-choice" style="border:1.5px solid #E2E8F4;border-radius:12px;margin:10px 0;background:#FFFDF8;">'
                   '<summary style="cursor:pointer;padding:12px 16px;font-weight:800;color:#0E1C42;">%s. <em>%s</em> &middot; %s <span style="font-weight:600;color:#7A88A8;">&mdash; %s</span></summary>'
                   '<div class="passage-text" style="padding:4px 18px 8px;font-family:Georgia,serif;font-size:18px;line-height:1.9;color:#0E1C42;">%s</div>'
                   '<div class="passage-source" style="padding:0 18px 12px;">%s, <em>%s</em>, %s</div></details>\n') % ('ABCDE'[i], book, ch, what, body, author, book, ch))
    out.append('  </div>\n')
    return ''.join(out)
FIX['flu'] = [
   ('This week you don&rsquo;t read a passage your teacher assigned. You choose one. Look back over the year&rsquo;s reading — five novels, dozens of chapters — and find the passage that stuck with you most. It might be funny, moving, dramatic, or just beautifully written. Whatever made you think: <em>this is what great writing can do</em>.',
    'This week you choose your own passage. Below are five real passages, one from each novel you read this year. Open them, read a few, and pick the one you most want to read aloud.', 1),
   (re.compile(r'  <div class="passage">\s*<div class="passage-label">📜 Your Choice — Best Passage from This Year</div>.*?Your novel &bull; Your choice &bull; Your year</div>\s*</div>\n', re.S), lambda m: passages(), 1),
   ('📋 How to Choose Your Passage', '📋 How to Choose', 1),
   ('Then read. Upload to Canvas.', 'Then read. Record it in this week&rsquo;s Canvas fluency assignment.', 1),
   ('Then read the passage with your best accuracy, smoothness, and expression. Upload to Canvas.', 'Then read the passage with your best accuracy, smoothness, and expression. Record it in this week&rsquo;s Canvas fluency assignment.', 1),
]
def run(apply):
    ok = True; out = {}
    for k, reps in FIX.items():
        fn = F[k]; t = io.open(fn, encoding='utf-8', newline='').read(); o = t
        for i, r in enumerate(reps):
            pat, new, n = r
            if isinstance(pat, str):
                c = t.count(pat)
                if c != n: print('FAIL', fn, i, 'count', c, '!=', n, repr(pat[:80])); ok = False; continue
                t = t.replace(pat, new)
            else:
                t, c = pat.subn(new, t)
                if c != n: print('FAIL', fn, i, 'regex count', c, '!=', n, pat.pattern[:80]); ok = False
        if o.count('<div') - o.count('</div>') != t.count('<div') - t.count('</div>'):
            print('FAIL div balance', fn, o.count('<div') - o.count('</div>'), t.count('<div') - t.count('</div>')); ok = False
        out[fn] = t; print(fn, len(o), '->', len(t))
    if ok and apply:
        for fn, t in out.items(): io.open(fn, 'w', encoding='utf-8', newline='').write(t)
        print('written')
    elif not ok: sys.exit(1)
run('--apply' in sys.argv)
