#!/usr/bin/env python3
"""Week 25 accuracy fixes (approved by Bethany Nov 22 2026; audit claude/g5-ela-wk25-audit.md).
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 1-3). History checked against
LOC "Discovery of Gold" (Marshall Jan 24 1848; Polk Dec 5 1848), NPS (Cape Horn: more than 13,000 miles, as long
as eight months), PBS American Experience ($10 million 1849, $81 million 1852; ~100,000 non-native by end of 1849),
Calisphere/UC (Native population ~150,000 in 1848 to ~30,000 twelve years later) and NLM Native Voices (Miwok,
Maidu and Nisenan workers at the millrace). Every replacement asserts its count; div balance must not change;
nothing is written unless every file passes. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-25-1-btghs.html', 2: 'lesson-25-2-btghs-ch1.html', 3: 'lesson-25-3-btghs-ch2.html',
     4: 'lesson-25-4-btghs-ch3.html', 'flu': 'lesson-25-fluency.html'}
HI1 = '<span style="background:#FFF3D8;padding:2px 6px;border-radius:4px;"><em>'
HI2 = '<span style="background:#EEF8FF;padding:2px 6px;border-radius:4px;"><em>'
def spot(id_, words):
    out = []
    for w, ok in words:
        if ok:
            out.append('<span class="spotter-word" onclick="g5Spot(this,\'%s\')" data-correct="true" data-explain="&#9989; Yes &mdash; that one counts."><strong>%s</strong></span>' % (id_, w))
        else:
            out.append('<span class="spotter-word" onclick="g5Spot(this,\'%s\')" data-correct="false" data-explain="&#129300; Not that one. Look again.">%s</span>' % (id_, w))
    return ' '.join(out)
OLD_SPOT = re.compile(r'(<div class="spotter-sentence" id="g25d2ss1"><span[^>]*>[^<]*</span>)(.*?)( <div class="spotter-result")', re.S)
NEW_SPOT = spot('g25d2ss1', [(w, w in ('Boston', 'Patagonia,', 'Cape Horn', 'San Francisco.')) for w in
    ['The', 'brig', 'sailed', 'from', 'Boston', 'down', 'the', 'coast', 'of', 'Patagonia,', 'rounded', 'Cape Horn', 'in', 'a', 'gale,', 'and', 'made', 'for', 'San Francisco.']])
CARD = '<div class="flip-card" onclick="this.classList.toggle(\'flipped\')"><div class="flip-card-inner"><div class="flip-card-front"><div class="fc-emoji">%s</div><div class="fc-word">%s</div><div class="fc-tap">%s</div></div><div class="flip-card-back"><div class="fc-word-back">%s</div><div class="fc-def">%s</div></div></div></div>'
UND_DEF = 'Not scared off or discouraged, even when something is hard. From <em>un-</em> (not) + <em>daunt</em> (frighten).'
PASSAGE_OLD = re.compile(r'<p><strong>The Discovery That Changed Everything</strong></p>.*?(?=\n        </div>\n        <div class="passage-source">)', re.S)
PASSAGE = '''<p><strong>The Discovery That Changed Everything</strong></p>
          <p>On January 24, 1848, a carpenter named James Marshall spotted something shining in the ditch below a sawmill he was building for John Sutter near Coloma, California. It was gold. Some of the workers who dug that ditch were Native Californians: Nisenan, Maidu and Miwok people. Word spread slowly at first. On December 5, 1848, President James K. Polk confirmed the news in his yearly message to Congress, and the rush was on.</p>

          <p><strong>The Rush Begins: Who Were the Forty-Niners?</strong></p>
          <p>The people who rushed to California in 1849 became known as the <strong>Forty-Niners</strong>, named for the year they arrived. By the end of 1849, about 90,000 newcomers had reached California (historians&rsquo; estimates run from about 80,000 to 100,000). In all, about 300,000 people came during the Gold Rush years. They came from across the United States and from many other countries, including China, Chile, Mexico, France and Australia. Most were men. Many left their families at home with a promise: <em>I&rsquo;ll come back rich.</em></p>

          <p><strong>Three Routes West</strong></p>
          <p>Getting to California was nearly as dangerous as the gold fields themselves. There were three main routes, and none was easy.</p>
          <p>The first route was the <strong>California Trail</strong>, a 2,000-mile walk beside covered wagons through plains, deserts and mountains. The wagons rolled from Missouri toward Sacramento. The trip took many months, and cholera, a deadly disease, killed thousands of travelers along the way.</p>
          <p>The second route cut across Central America. Travelers sailed from the East Coast to Panama, crossed through jungle to the Pacific side, and boarded another ship north to San Francisco. It was shorter, but yellow fever and malaria waited in the jungle, and ships on the Pacific side were badly overbooked.</p>
          <p>The third route was the longest: the <strong>Cape Horn sea voyage</strong>. Ships left Boston or New York, sailed south along the whole Atlantic coast of South America, rounded Cape Horn at its stormy southern tip, and turned north up the Pacific to San Francisco. The voyage was more than 13,000 miles and often took five to eight months. Ships were crowded. Passengers faced rough seas, spoiled food and sickness. Many New Englanders chose it anyway: the ships sailed from their own harbors, and they could carry their tools and supplies on board.</p>

          <p><strong>Life in the Gold Fields</strong></p>
          <p>Gold mining was usually hard. Most Forty-Niners panned for gold in streams, swirling muddy water in a metal pan until the heavier gold settled to the bottom. The work was backbreaking, the camps were muddy, prices were sky-high, and most miners found little or nothing. Many of the people who did best were the ones who sold the miners food, tools and supplies.</p>
          <p>Still, there was real gold. In 1849, about $10 million worth came out of California&rsquo;s streams and hills. In 1852, the peak year, it was about $81 million. Newspapers back East printed amazing stories of easy riches, and many of those stories were far bigger than the truth.</p>

          <p><strong>The People Who Were Already There</strong></p>
          <p>California was not empty. In 1848, about 150,000 Native Californians lived there, in many nations with their own languages and homelands. For them, the Gold Rush was a disaster. Miners took over their land, rivers and food, brought new diseases, and attacked their villages. Twelve years later, only about 30,000 Native Californians were left. Their nations are still in California today.</p>

          <p>In the novel, the dream of gold is what sends Jack Flagg and Praiseworthy into those potato barrels. Keep the real history in mind as you read their made-up adventure.</p>'''
SOURCE_OLD = 'Background passage for educational use &mdash; based on historical sources including Britannica Kids and Library of Congress records.'
SOURCE = 'Sources: Library of Congress, &ldquo;Discovery of Gold&rdquo;; National Park Service; PBS <em>American Experience</em>, &ldquo;The Gold Rush&rdquo;; Calisphere (University of California), &ldquo;Gold Rush, Statehood, and the Western Movement&rdquo;; National Library of Medicine, <em>Native Voices</em>. Numbers with &ldquo;about&rdquo; are historians&rsquo; estimates.'
DIARY = '&ldquo;The truth of the matter was that neither Jack nor the butler had the slightest idea how to go about catching a thief. But Praiseworthy was <span class="decode-word">undaunted</span>.&rdquo;'
OLD_W1 = re.compile(r'<div class="key-concept-label" style="margin-bottom:12px;">🔍 Word 1: <strong>expedition</strong></div>\n      <div class="decode-steps">.*?</div>\n      </div>\n\n      <div class="key-concept-label" style="margin:16px 0 12px;">🔍 Word 2: <strong>argonaut</strong></div>(\n      <div class="decode-steps">.*?</div>\n      </div>\n)', re.S)
W2_UND = '''
      <div class="key-concept-label" style="margin:16px 0 12px;">🔍 Word 2: <strong>undaunted</strong></div>
      <div class="decode-steps">
        <div class="decode-step"><div class="decode-num">1</div><div class="decode-content"><div class="decode-label">Read the sentence from Chapter 2</div><div class="decode-text">%s</div></div></div>
        <div class="decode-step"><div class="decode-num">2</div><div class="decode-content"><div class="decode-label">Look at word parts</div><div class="decode-text"><em>un-</em> = not &middot; <em>daunt</em> = frighten or discourage &middot; <em>-ed</em>. Together: &ldquo;not frightened off.&rdquo;</div></div></div>
        <div class="decode-step"><div class="decode-num">3</div><div class="decode-content"><div class="decode-label">Confirm the meaning</div><div class="decode-text"><span class="decode-word">undaunted</span> = not scared off or discouraged, even when something is hard.</div></div></div>
      </div>
''' % DIARY
MATCH_OLD = re.compile(r'(<div class="match-grid">\n).*?(\n        </div>\n        <div class="match-feedback">)', re.S)
MI = '          <div class="match-item%s" data-match="%s" onclick="matchClick(this)">%s</div>'
MATCH_NEW = '\n'.join([MI % (' is-word', 'sw', 'stowaway'), MI % ('', 'pw', 'A large rotating wheel with paddles that pushes a steamship through the water'),
    MI % (' is-word', 'pw', 'paddlewheel'), MI % ('', 'und', 'Not scared off or discouraged, even when something is hard'),
    MI % (' is-word', 'arg', 'argonaut'), MI % ('', 'sw', 'Someone who hides on a ship to travel without paying'),
    MI % (' is-word', 'ph', 'porthole'), MI % ('', 'arg', 'A Gold Rush seeker; first, a sailor in a Greek myth who sailed after the Golden Fleece'),
    MI % (' is-word', 'und', 'undaunted'), MI % ('', 'ph', 'A small round window in the side of a ship')])
RM_OLD = re.compile(r'<p><strong>Match each word to the root it carries\. <em>aud</em> = hear\. <em>oral / or</em> = speak\.</strong></p></div><div class="root-match-game g5-match" id="g25d3m"><div class="root-match-grid">.*?</div><div class="g5-fb">', re.S)
RMI = '<div class="root-match-item%s" data-match="%s" onclick="g5Match(this)">%s</div>'
RM_NEW = ('<p><strong>Match each word to its meaning. <em>aud</em> = hear. <em>oral / or</em> = speak.</strong></p></div><div class="root-match-game g5-match" id="g25d3m"><div class="root-match-grid">'
    + RMI % (' is-word', 'A', 'audible') + RMI % ('', 'C', 'a formal speech') + RMI % (' is-word', 'B', 'audience') + RMI % ('', 'D', 'spoken, not written')
    + RMI % (' is-word', 'C', 'oration') + RMI % ('', 'A', 'loud enough to be heard') + RMI % (' is-word', 'D', 'oral') + RMI % ('', 'B', 'the people listening') + '</div><div class="g5-fb">')
CHK_RW = '<div>I wrote my DOL correction and my Read &amp; Write answer in my reading journal.</div>'
FIX = {
 1: [('&ldquo;Argonauts of old, they are, chasing after the golden fleece,&rdquo; roared Captain Swain, his brass buttons glowing in the firelight.',
      'Captain Swain grumbles about the gold-seekers crowding his ship: &ldquo;Argonauts of old, they are, chasing after the golden fleece.&rdquo;', 1),
     ('<p>&ldquo;' + HI1 + 'In the creaking darkness</em></span> ' + HI2 + 'of her cargo hold</em></span>, there sat eighteen barrels of potatoes.&rdquo;</p>',
      '<p>&ldquo;Below decks, ' + HI1 + 'in the creaking darkness</em></span> ' + HI2 + 'of her cargo hold</em></span>, there sat eighteen barrels of potatoes.&rdquo;</p>', 1),
     ('out of Boston harbor</em></span>.&rdquo;', 'out of Boston harbor</em></span> ' + HI1 + 'on a voyage</em></span> ' + HI2 + 'around the Horn</em></span> ' + HI1 + 'to San Francisco</em></span>.&rdquo;', 1),
     ('cleared the harbour.', 'cleared the harbor.', 1),
     ('<p>This sentence is missing a prepositional phrase to describe the setting. Add one that tells <em>where</em> or <em>when</em>, and write the improved sentence in your reading journal.</p>\n      <div class="dol-fix-sentence">the gold-seekers scrambled and pushed, desperate to reach their cabins aboard the Lady Wilma.</div>',
      '<p>This sentence starts with a prepositional phrase that tells <em>when</em>. Fix the four missing capital letters and add the comma after the opening phrase.</p>\n      <div class="dol-fix-sentence">in january 1849 hundreds of gold-seekers crowded the docks of boston harbor.</div>', 1),
     ('🔍 See One Possible Answer', '🔍 See the Answer', 1),
     (re.compile(r'<p><strong>One possible fix:</strong>.*?</p>\n        <p style="font-size:13px;color:#7A88A8;margin-top:6px;">.*?</p>', re.S),
      '<p><strong>Corrected:</strong> <em>In January 1849,</em> hundreds of gold-seekers crowded the docks of Boston Harbor.</p>\n        <p style="font-size:13px;color:#7A88A8;margin-top:6px;">Capitalize <em>In</em> (the first word), <em>January</em> (a month), <em>Boston</em> and <em>Harbor</em> (a place name). Put a comma after the opening phrase &ldquo;In January 1849.&rdquo; The phrases &ldquo;of gold-seekers&rdquo; and &ldquo;of Boston Harbor&rdquo; are prepositional phrases too.</p>', 1),
     (PASSAGE_OLD, PASSAGE, 1), (SOURCE_OLD, SOURCE, 1),
     ('① Oregon-California Trail (overland, ~6 mo.)', '① California Trail (overland, 2,000 mi)', 1),
     ('② Panama Route (sea+land, ~3 mo.)', '② Panama Route (ship, jungle, ship)', 1),
     ('③ Cape Horn Sea Voyage (~4–6 mo., 18,000 mi)', '③ Cape Horn (13,000+ mi, 5–8 mo.)', 1),
     ('Jack &amp; Praiseworthy take this route!', 'In the novel, Jack &amp; Praiseworthy go this way', 1),
     (OLD_W1, lambda m: '<div class="key-concept-label" style="margin-bottom:12px;">🔍 Word 1: <strong>argonaut</strong></div>' + m.group(1) + W2_UND, 1),
     ('<div class="fc-word">stowaway</div><div class="fc-tap">tap to flip</div>', '<div class="fc-word">stowaway</div><div class="fc-tap">Ch. 1 &middot; tap to flip</div>', 1),
     ('<div class="fc-word">paddlewheel</div><div class="fc-tap">tap to flip</div>', '<div class="fc-word">paddlewheel</div><div class="fc-tap">Ch. 1 &middot; tap to flip</div>', 1),
     ('<div class="fc-word">porthole</div><div class="fc-tap">tap to flip</div>', '<div class="fc-word">porthole</div><div class="fc-tap">Ch. 1 &middot; tap to flip</div>', 1),
     ('Read the sentence from Chapter 1</div><div class="decode-text">Captain Swain', 'Read the sentence from Chapter 1</div><div class="decode-text">Captain Swain', 1),
     ('<div>I wrote my RWM journal response and my DOL correction in my reading journal.</div>', CHK_RW, 1)],
 2: [('&ldquo;We&rsquo;re partners, sir. Either send me to the coal bunkers or &mdash; put me in chains.&rdquo;',
      '&ldquo;We&rsquo;re partners, sir. Either send me to the coal bunkers or &mdash;,&rdquo; he gulped, &ldquo;or put me in chains.&rdquo;', 1),
     ('This sentence has a capitalization error and a missing comma. Find both and write the corrected sentence in your reading journal.',
      'This sentence needs one capital letter and two commas. Find them and write the corrected sentence.', 1),
     ('the most formal, rule-bound profession in Victorian society', 'the most formal, rule-bound job in a fine Boston house', 1),
     ('Jack and Praiseworthy choose each other over comfort, twice in the same chapter.', 'Jack chooses his partner over an easy job, and he says so to the captain&rsquo;s face.', 1),
     (re.compile(r'He hooked a black umbrella <span class="dol-highlight-word"([^>]*)>on his arm</span> and pulled <span class="dol-highlight-word"[^>]*>on a pair</span> (<span class="dol-highlight-word"[^>]*>of spotless white gloves</span>)\.'),
      lambda m: 'He hooked a black umbrella <span class="dol-highlight-word"%s>on his arm</span>, for he never traveled <span class="dol-highlight-word"%s>without it</span>, and pulled on a pair %s.' % (m.group(1), m.group(1), m.group(2)), 1),
     ('in<input class="fillin-input" id="m21" data-answer="ible"', 'in<input class="fillin-input" id="m21" data-answer="aud"', 0),
     (re.compile(r'<div class="fillin-item">inAUD<input class="fillin-input" id="m21" data-answer="ible" maxlength="6" placeholder="____"> &mdash; cannot be heard \(7 letters total\)</div>\n(.*?)<div class="fillin-item">lab<input class="fillin-input" id="m24" data-answer="or" maxlength="3" placeholder="__">at<input class="fillin-input" id="m24b" data-answer="or" maxlength="3" placeholder="__">y &mdash; a place where work \(or tests\) are performed</div>', re.S),
      '<div class="fillin-item">in<input class="fillin-input" id="m21" data-answer="aud" maxlength="4" placeholder="___">ible &mdash; too quiet to be heard</div>\n        <div class="fillin-item"><input class="fillin-input" id="m22" data-answer="aud" maxlength="4" placeholder="___">io &mdash; sound you can hear, like music or a recording</div>\n        <div class="fillin-item"><input class="fillin-input" id="m23" data-answer="aud" maxlength="4" placeholder="___">itory &mdash; having to do with hearing</div>\n        <div class="fillin-item"><input class="fillin-input" id="m24" data-answer="or" maxlength="3" placeholder="__">atory &mdash; the skill of giving speeches</div>', 1),
     (OLD_SPOT, lambda m: m.group(1) + NEW_SPOT + m.group(3), 1),
     ('<div>I wrote my RWM and Poetry Corner responses in my reading journal.</div>', '<div>I wrote my Read &amp; Write and Poetry Corner answers in my reading journal.</div>', 1)],
 3: [('<p>This sentence has a punctuation error and a word choice problem. Find both and rewrite it in your reading journal.</p>\n      <div class="dol-fix-sentence">praiseworthy stepped forward calm as you please and said his plan was very simple.</div>',
      '<p>This sentence needs one capital letter and two commas. Find them and write the corrected sentence.</p>\n      <div class="dol-fix-sentence">praiseworthy tall and calm stepped forward.</div>', 1),
     (re.compile(r'<p><strong>Corrected:</strong> Praiseworthy stepped forward, as unconcerned as you please, and said his plan was very simple\.</p>\n        <p style="font-size:13px;color:#7A88A8;margin-top:6px;">Fixes:.*?</p>', re.S),
      '<p><strong>Corrected:</strong> Praiseworthy, tall and calm, stepped forward.</p>\n        <p style="font-size:13px;color:#7A88A8;margin-top:6px;">Capitalize <em>Praiseworthy</em> (a name). Put a comma before and after &ldquo;tall and calm,&rdquo; the extra describing words in the middle. This is how Fleischman wrote it in Chapter 2.</p>', 1),
     ('<div class="socratic-label">⏸️ Pause: The Sow and the Plan</div>\n            <p class="socratic-q">Praiseworthy tells the passengers the sow will squeal if a dishonest man touches her. But that&rsquo;s not really the plan at all. Why does the pig need to be there?</p>',
      '<div class="socratic-label">⏸️ Pause: Before the Lamps Go Out</div>\n            <p class="socratic-q">Stop when Praiseworthy says the sow will squeal if the thief touches her. Before you read on, guess: how could a pig really help catch a thief?</p>', 1),
     ('placeholder="The pig needs to be there because..."', 'placeholder="My guess is..."', 1),
     ('<div class="socratic-label">⏸️ Pause: &ldquo;Humbug&rdquo;</div>\n            <p class="socratic-q">When Cut-Eye Higgins is caught, he says they&rsquo;ll meet again. Praiseworthy responds: &ldquo;Humbug.&rdquo; Based on context, what do you think this word means?</p>',
      '<div class="socratic-label">⏸️ Pause: The Lamps Come Back On</div>\n            <p class="socratic-q">Stop when the lamps are lit again and the sow never squealed. Was your guess right? Name the moment you figured out the trick, or say how the book fooled you.</p>', 1),
     ('placeholder="I think \'humbug\' means..."', 'placeholder="I figured it out when..."', 1),
     ('Ask what the humour hides:', 'Ask what the humor hides:', 1),
     (RM_OLD, RM_NEW, 1), (MATCH_OLD, lambda m: m.group(1) + MATCH_NEW + m.group(2), 1),
     ('<div>I wrote my DOL correction and RWM in my reading journal.</div>', CHK_RW, 1)],
 4: [('Praiseworthy insists he was &ldquo;born to be a butler&rdquo; &mdash; yet this week he has shoveled coal, trapped a thief, and helped a fever ship.',
      'Praiseworthy says, &ldquo;I was born to my calling&rdquo; &mdash; he means he was born to be a butler. Yet this week he has hidden in a barrel, shoveled coal, and trapped a thief.', 1),
     ('Chapter 3 ends with Praiseworthy looking at the Southern Cross and saying, calmly, that he was &ldquo;born to his calling&rdquo; &mdash; born to be a butler, just like his father, and his father before him. But think about what he has done in three chapters: he&rsquo;s survived hidden in a barrel, shoveled coal, outwitted a thief, and helped a ship in distress.',
      'In Chapter 3, under the southern stars, Jack asks Praiseworthy to call him plain Jack. Praiseworthy says no. &ldquo;I was born to my calling,&rdquo; he says, &ldquo;like my father before me and his father before him.&rdquo; But think about what he has done in three chapters: he hid in a barrel, shoveled coal, and outwitted a thief.', 1),
     ('He calls himself &ldquo;just a butler.&rdquo;', 'He tells the captain, &ldquo;I am a butler, sir.&rdquo;', 1),
     ('something he had previously described only as &ldquo;a certain misfortune.&rdquo; What specific details did Jack include in the letter that he hadn&rsquo;t mentioned before?',
      'which the letter first calls only &ldquo;a certain misfortune.&rdquo; What details does Jack add once he decides to tell the whole story?', 1),
     ('At the end of Chapter 3, Praiseworthy says he was &ldquo;born to his calling&rdquo; as a butler', 'In Chapter 3, Praiseworthy says, &ldquo;I was born to my calling&rdquo; (he means a butler)', 1),
     ('Explain <em>aud</em> and <em>or</em> to a classmate who missed the week.', 'Explain <em>aud</em> and <em>or</em> to someone who has never heard of them.', 1),
     ('<p>A classmate asks: &ldquo;Why does Fleischman', '<p>Someone asks you: &ldquo;Why does Fleischman', 1),
     ('<strong>expedition &middot; argonaut &middot; stowaway &middot; paddlewheel &middot; porthole</strong>', '<strong>stowaway &middot; paddlewheel &middot; argonaut &middot; porthole &middot; undaunted</strong>', 1),
     ('data-label="Vocabulary Choice Board SWYK — expedition, argonaut, stowaway, paddlewheel, porthole"', 'data-label="Vocabulary Choice Board SWYK — stowaway, paddlewheel, argonaut, porthole, undaunted"', 1)],
 'flu': [('emerging from their potato barrels after two freezing days at sea', 'climbing out of their potato barrels on their second day at sea', 1),
         ('&ldquo;permits himself a most contented smile.&rdquo;', '&ldquo;permitted himself a most contented smile.&rdquo;', 1)],
}
def flip25_2(s):
    cards = dict((m.group(2), m.group(0)) for m in re.finditer(r'<div class="flip-card" onclick="[^"]*"><div class="flip-card-inner"><div class="flip-card-front"><div class="fc-emoji">([^<]*)</div><div class="fc-word">([^<]*)</div>.*?</div></div></div></div>', s))
    if sorted(cards) != ['argonaut', 'expedition', 'paddlewheel', 'porthole', 'stowaway']: sys.exit('flip cards 25.2: %s' % sorted(cards))
    und = CARD % ('🦁', 'undaunted', 'tap to flip', 'undaunted', UND_DEF)
    first = s.find(cards['expedition']); last = max(s.find(c) + len(c) for c in cards.values())
    seg = s[first:last]
    if seg.count('<div class="flip-card" ') != 5: sys.exit('flip seg')
    return s[:first] + '\n        '.join([cards['stowaway'], cards['paddlewheel'], cards['argonaut'], cards['porthole'], und]) + s[last:]
def run(apply):
    out = {}
    for k, f in F.items():
        s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in FIX[k]:
            if n == 0: continue
            if isinstance(old, str):
                c = s.count(old)
                if c != n: sys.exit('%s: %d x %r' % (f, c, old[:70]))
                s = s.replace(old, new)
            else:
                s, c = old.subn(new, s)
                if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:70]))
        if k == 2: s = flip25_2(s)
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        if '\r\n' in s0 and s.count('\n') != s.count('\r\n'): sys.exit('line ending ' + f)
        out[f] = s
        print('ok', f, len(s0), '->', len(s))
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
if __name__ == '__main__': run('--apply' in sys.argv)
