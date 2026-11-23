#!/usr/bin/env python3
"""Week 27 accuracy: 27.4's invented 'California Diggings' passage replaced with a real, checked source (Bethany, Nov 23 2026).
Source: Bayard Taylor, Eldorado, or, Adventures in the Path of Empire, vol. 1 (1850), ch. V-VI, pp. 52-57. Words copied from the
1850 edition's scanned text (Internet Archive, eldoradooradvent01tayluoft), OCR slips corrected against the page; Taylor's
spelling and punctuation kept (new-comer, a-piece). Cuts marked with an ellipsis. Left out on purpose: his list of the people in the
streets (dated labels for Chinese, Malay and Hawaiian people), the gambling-house rents.
Facts in the intro: Taylor, New York Tribune correspondent, left New York June 28 1849, crossed Panama, reached San Francisco on
the steamer Panama on August 18 1849 (51 days, ch. V; LOC record rc01000822). The questions are rewritten to the new source."""
import io, sys
f = 'lesson-27-4-btghs-info.html'
PASS = '''          <p><strong>From <em>Eldorado</em> (1850), by Bayard Taylor</strong></p>
          <p>At last we are through the Golden Gate&mdash;fit name for such a magnificent portal to the commerce of the Pacific! Yerba Buena Island is in front; southward and westward opens the renowned harbor, crowded with the shipping of the world, mast behind mast and vessel behind vessel, the flags of all nations fluttering in the breeze! Around the curving shore of the Bay and upon the sides of three hills which rise steeply from the water, &hellip; the town is planted and seems scarcely yet to have taken root, for tents, canvas, plank, mud and adobe houses are mingled together with the least apparent attempt at order and durability.</p>
          <p>A furious wind was blowing down through a gap in the hills, filling the streets with clouds of dust. On every side stood buildings of all kinds, begun or half-finished, and the greater part of them mere canvas sheds, open in front, and covered with all kinds of signs, in all languages. Great quantities of goods were piled up in the open air, for want of a place to store them.</p>
          <p>&hellip; we discharged the porters, after paying them two dollars each&mdash;a sum so immense in comparison to the service rendered that there was no longer any doubt of our having actually landed in California. &hellip; I asked the landlord whether he could send a porter for our trunks. &ldquo;There is none belonging to the house,&rdquo; said he; &ldquo;every man is his own porter here.&rdquo;</p>
          <p>Many of the passengers began speculation at the moment of landing. The most ingenious and successful operation was made by a gentleman of New York, who took out fifteen hundred copies of The Tribune and other papers, which he disposed of in two hours, at one dollar a-piece!</p>
          <p>&hellip; Every new-comer in San Francisco is overtaken with a sense of complete bewilderment. &hellip; One knows not whether he is awake or in some wonderful dream.</p>
'''
a0 = '          <p><strong>The California Diggings: What the Gold Rush Was Really Like</strong></p>\n'
b0 = '        </div>\n        <div class="passage-source">Background passage for educational use &mdash; based on Britannica, Library of Congress, and National Park Service Gold Rush records.</div>'
NEWSRC = ('        </div>\n        <div class="passage-source">Bayard Taylor, <em>Eldorado, or, Adventures in the Path of Empire</em>, vol. 1 (1850), chapters V&ndash;VI, pages 52&ndash;57. '
          'Public domain. Words checked against the 1850 edition. &hellip; marks a place where words were left out.</div>')
REP = [
 ('font-family="Georgia,serif" font-weight="700">Gold Rush: The Diggings</text>', 'font-family="Georgia,serif" font-weight="700">Gold Rush: A Reporter Lands</text>', 1),
 ('What Jack and Praiseworthy are about to face — the real thing</text>', 'San Francisco in 1849, in the words of a man who was there</text>', 1),
 ('What was life in the diggings actually like?', 'What was San Francisco really like in 1849?', 1),
 ('Jack has been dreaming of gold fields since Boston. Today you read an informational passage about what mining actually looked like in 1849 — and connect it to Chapters 7–9.',
  'Jack has just stepped onto the Long Wharf. Today you read the words of a real reporter, Bayard Taylor, who landed in San Francisco in August 1849, and connect them to Chapters 7–9.', 1),
 ('I will read about the California diggings and connect it to the novel.', 'I will read a real 1849 account of San Francisco and connect it to the novel.', 1),
 ('Jack has pictured gold fields since Boston — nuggets the size of pumpkins, grizzly bears, outlaws. In your journal: What do you think the reality will actually look like? Write 2–3 sentences predicting what Jack is about to discover.',
  'In Chapter 8, Jack and Praiseworthy land in San Francisco. Today you read the words of a real man who landed there in 1849. In your journal: What do you think a real visitor noticed first? Write 2–3 sentences.', 1),
 ('<div class="activity-title">Read: Life in the California Diggings</div><div class="activity-sub">What Jack and Praiseworthy are about to face — the real Gold Rush</div>',
  '<div class="activity-title">Read: A Reporter Lands in San Francisco</div><div class="activity-sub">A real eyewitness, two months after the novel&rsquo;s Lady Wilma</div>', 1),
 ('<p>Jack imagined gold fields with nuggets the size of pumpkins. Praiseworthy privately doubted they&rsquo;d find anything. The truth was somewhere between — but closer to Praiseworthy&rsquo;s version.</p>',
  '<p>Jack and Praiseworthy are made up. Bayard Taylor was real. He wrote for the <em>New York Tribune</em>, a newspaper. He left New York on June 28, 1849, crossed Panama, and sailed into San Francisco on the steamer <em>Panama</em> on August 18, 1849. His reports became a book, <em>Eldorado</em> (1850). Here is part of what he wrote about his first day. The words are his, with his 1850 spelling.</p>', 1),
 ('<div class="passage-label">📜 Informational Passage — Week 27</div>', '<div class="passage-label">📜 Primary Source — Week 27</div>', 1),
 ('<p>When you understand how placer mining works, Quartz Jackson&rsquo;s explanation in Chapter 8 becomes a real lesson, not just a plot detail. When you see that flour cost $1 a pound, you understand why Praiseworthy guards their gold dust so carefully. History makes the novel vivid; the novel makes history human.</p>',
  '<p>A real eyewitness turns Chapter 8 into more than a story. Taylor paid two dollars just to have his trunks carried; Jack and Praiseworthy hear that water costs a dollar a bucket. History makes the novel vivid; the novel makes history human.</p>', 1),
 ('<li><strong>Read the informational text first:</strong> Get the facts straight before you carry them into the story.</li>',
  '<li><strong>Read the real account first:</strong> Get the facts straight before you carry them into the story.</li>', 1),
 ('Where does the fiction show what the article explained?', 'Where does the novel show what Taylor saw?', 1),
 ('<div class="swyk-prompt">Explain how placer mining worked. What tool did most miners use, and why did gold settle to the bottom of the pan? Use at least one specific detail from the passage.</div>\n        <textarea class="journal-box" id="journal-q1" data-label="Info Q1: How placer mining worked" placeholder="Placer mining worked by..."',
  '<div class="swyk-prompt">What surprised Bayard Taylor when he landed in San Francisco? Give two details from his words, and tell what each one shows about the city in 1849.</div>\n        <textarea class="journal-box" id="journal-q1" data-label="Info Q1: What surprised Taylor — two details" placeholder="One thing that surprised Taylor was..."', 1),
 ('<div class="swyk-prompt">Using both the informational passage and Chapter 8, explain why prices were so extreme in California in 1849. Name at least one specific price from each source.</div>\n        <textarea class="journal-box" id="journal-q2" data-label="Info Q2: Why prices were extreme — passage + Ch. 8 evidence"',
  '<div class="swyk-prompt">Prices in San Francisco were sky-high in 1849. Name one price Taylor reports and one price from Chapter 8. Then explain in 2 or more sentences why things cost so much, using clues from both (who was arriving, who was left to do the work, where the goods sat).</div>\n        <textarea class="journal-box" id="journal-q2" data-label="Info Q2: Why prices were so high — Taylor + Ch. 8 evidence"', 1),
 ('<div class="swyk-prompt">The passage says most Forty-Niners did not get rich. Praiseworthy privately doubts they&rsquo;ll find gold. Yet Fleischman keeps us rooting for Jack. Using both the passage and Chapters 7&ndash;9, explain what Fleischman is saying about hope versus reality. What makes Jack&rsquo;s journey worth reading about even when the odds are against him?</div>\n        <textarea class="journal-box" id="journal-q3" data-label="Info Q3 (Text-to-Novel): Hope vs. reality — what Fleischman is saying" placeholder="Fleischman seems to be saying..."',
  '<div class="swyk-prompt">Taylor wrote that every newcomer felt &ldquo;complete bewilderment.&rdquo; How does Jack&rsquo;s first day in San Francisco in Chapter 8 show the same feeling? Then tell one thing the real account gives you that the novel does not, and one thing the novel gives you that the real account does not.</div>\n        <textarea class="journal-box" id="journal-q3" data-label="Info Q3 (Text-to-Novel): Bewilderment — Taylor and Jack" placeholder="Like Taylor, Jack..."', 1),
 ('Week 27 &mdash; Gold Rush Informational Connection</strong>', 'Week 27 &mdash; A Real Account of 1849 San Francisco</strong>', 1),
]
s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
for old, new, n in REP:
    c = s.count(old)
    if c != n: sys.exit('%d x %r' % (c, old[:80]))
    s = s.replace(old, new)
a = s.find(a0); b = s.find(b0)
if a < 0 or b < 0 or s.count(a0) != 1: sys.exit('passage bounds')
s = s[:a] + PASS + NEWSRC + s[b + len(b0):]
for bad in ('Hangtown, Angels Camp', 'Jack Flagg&rsquo;s stagecoach', 'flour cost $1'):
    if bad in s: sys.exit('left: ' + bad)
if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance')
print('ok', len(s0), '->', len(s))
if '--apply' in sys.argv: io.open(f, 'w', encoding='utf-8', newline='').write(s); print('written')
