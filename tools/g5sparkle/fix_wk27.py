#!/usr/bin/env python3
"""Week 27 accuracy fixes (approved by Bethany Nov 23 2026; audit claude/g5-ela-wk27-audit.md).
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 7-9). Every replacement asserts its
count; div balance must not change; nothing is written unless every file passes. Run once from the repo root."""
import io, re, sys
F = {1: 'lesson-27-1-btghs-ch7.html', 2: 'lesson-27-2-btghs-ch8.html', 3: 'lesson-27-3-btghs-ch9.html', 4: 'lesson-27-4-btghs-info.html',
     'flu': 'lesson-27-fluency.html'}
OLD_TIP = 'Fleischman&rsquo;s secret: each chapter ends with a new problem, not a solution. Chapter 7 ends with the race still undecided. Chapter 8 ends with no money. Chapter 9 ends with Cut-Eye Higgins on the same stagecoach. That momentum is your model.'
TIP = {
 1: 'Fleischman&rsquo;s secret: every solution opens the next problem. In Chapter 7 the Sea Raven buys up every lump of coal in Callao, so Captain Swain burns lumber, and the race is won. But winning the race only gets Jack and Praiseworthy to San Francisco. The gold is still far away. That chain is your model.',
 2: 'Fleischman&rsquo;s secret: every solution opens the next problem. Chapter 7 wins the race. Chapter 8 lands Jack and Praiseworthy in a city where water costs a dollar a bucket and the riverboat costs more than they have, until a favor for a shaggy miner turns into gold dust. That chain is your model.',
 3: 'Fleischman&rsquo;s secret: every solution opens the next problem. Chapter 7 wins the race. Chapter 8 solves the money problem with a haircut. Chapter 9 gets them onto the stagecoach at last, then ends with Cut-Eye Higgins sitting right across from Jack. That chain is your model.',
}
TIP[4] = TIP[3]
STOLE = ('The Sea Raven stole all the coal at Callao.', 'The Sea Raven bought up every lump of coal at Callao.')
EX_OLD = ('  <em>Example:</em> &ldquo;The Sea Raven passed with a blast of her whistle, <strong>and</strong> the gold-seekers on the Lady Wilma fell silent.&rdquo;</p>',
          '  <em>Example:</em> &ldquo;The paddlewheels twirled, faster and faster, <strong>and</strong> the bowsprit came around on course like a compass needle.&rdquo; (Chapter 7)</p>')
EX2_OLD = ('  <em>Example:</em> &ldquo;<strong>Because</strong> the Sea Raven had loaded too much coal, she sat low in the water — and the Lady Wilma crept ahead.&rdquo;</p>',
           '  <em>Example:</em> &ldquo;<strong>When</strong> the Lady Wilma entered the blue Bay of Callao, Jack counted thirty-one sailing ships at anchor.&rdquo; (Chapter 7)</p>')
SKED = ('Fled or left in a hurry. Informal American English — used by Captain Swain when the Sea Raven disappears with all the coal.',
        'Fled or left in a hurry. Informal American English. Captain Swain says it when he learns the Sea Raven has already left Callao.')
JIPI = ('A hat woven from fine palm leaves (also called a Panama hat); the hat that hides a very dangerous face on the stagecoach.',
        'A hat woven from fine palm-leaf straw (also called a Panama hat). A sleeping passenger on the stagecoach wears one in Chapter 9.')
ASSAY = ("To test or measure the purity and value of ore or gold. Quartz Jackson 'assays' his beard dust.",
         'To test the purity and value of ore or gold. Quartz Jackson says the gold dust in his beard would assay out at about $14 an ounce.')
ORDER = ['skedaddled', 'diggings', 'assay', 'grubstake', 'jipijapa']
CH = {'skedaddled': 7, 'diggings': 8, 'assay': 8, 'grubstake': 9, 'jipijapa': 9}
CARD = re.compile(r'<div class="flip-card fc-color-\d".*?<div class="fc-word">([a-z]+)</div>.*?</div></div></div></div>', re.S)
def reorder_cards(s, tag):
    m = re.search(r'<div class="flip-card-row"[^>]*>', s); a = m.end()
    cards = [(c.group(1), c.group(0)) for c in CARD.finditer(s, a)][:5]
    if sorted(w for w, _ in cards) != sorted(ORDER): sys.exit('cards %r' % [w for w, _ in cards])
    start = s.find(cards[0][1], a); end = s.find(cards[-1][1], a) + len(cards[-1][1])
    if s[start:end] != ''.join(c for _, c in cards): sys.exit('cards not contiguous')
    d = dict(cards); new = []
    for i, w in enumerate(ORDER):
        c = re.sub(r'fc-color-\d', 'fc-color-%d' % (i + 1), d[w], 1)
        if tag: c = c.replace('<div class="fc-tap">tap to flip</div>', '<div class="fc-tap">Ch. %d &middot; tap to flip</div>' % CH[w], 1)
        new.append(c)
    return s[:start] + ''.join(new) + s[end:]
def reorder_match(s):
    words = re.findall(r'<div class="match-item[^"]*" data-match="(sk|gs|dg|as|jp)" onclick="matchClick\(this\)">([a-z]+)</div>', s)
    # word tiles are the ones whose text is one of ORDER
    tiles = [m for m in re.finditer(r'(<div class="match-item[^"]*" data-match=")(sk|gs|dg|as|jp)(" onclick="matchClick\(this\)">)(skedaddled|grubstake|diggings|assay|jipijapa)(</div>)', s)]
    if [t.group(4) for t in tiles] != ['skedaddled', 'grubstake', 'diggings', 'assay', 'jipijapa']: sys.exit('match order %r' % [t.group(4) for t in tiles])
    key = {'skedaddled': 'sk', 'grubstake': 'gs', 'diggings': 'dg', 'assay': 'as', 'jipijapa': 'jp'}
    out = []; last = 0
    for t, w in zip(tiles, ORDER):
        out.append(s[last:t.start()]); out.append(t.group(1) + key[w] + t.group(3) + w + t.group(5)); last = t.end()
    out.append(s[last:]); return ''.join(out)
CHK = ('I wrote my DOL fix and RWM journal in my reading journal.', 'I wrote my DOL fix in my reading journal.')
FIX = {
 1: [(OLD_TIP, TIP[1], 1), STOLE + (2,),
     ('The Sea Raven stole all the coal at Callao, which seemed like a devastating blow. Explain how that theft ironically helps the Lady Wilma win the race.',
      'The Sea Raven bought up every lump of coal at Callao, which seemed like a devastating blow to the Lady Wilma. Explain how all that coal ironically helps the Lady Wilma win the race.', 1),
     ('data-label="Reading Q1: Cause-and-effect chain — how coal theft helped Lady Wilma win"', 'data-label="Reading Q1: Cause-and-effect chain — how the coal problem helped the Lady Wilma win"', 1),
     ('The Sea Raven tries to <em>distract</em> Captain Swain with its coal theft. When Praiseworthy notices the lumber, he helps the captain <em>extract</em> a solution. And the race itself is driven by a <em>contract</em> — Swain wins the race, he gets the new clipper ship.',
      'Losing the coal could <em>distract</em> any captain. When Praiseworthy reminds Captain Swain about the lumber, the captain finds a way to <em>extract</em> one more burst of speed. And the race has a prize: if Swain wins, he gets command of a new clipper ship.', 1),
     ('she sat dangerously low in the water <span class="dol-highlight-word"', 'she sat dangerously low in the water, <span class="dol-highlight-word"', 1),
     ('The coordinating conjunction &quot;and&quot; now connects a second independent clause', 'A comma and the coordinating conjunction &quot;and&quot; connect a second independent clause', 1),
     EX_OLD + (1,), EX2_OLD + (1,),
     ('<br><em>"The Lady Wilma entered the Golden Gate. The Sea Raven fell behind."</em></p>', '<br>Two made-up sentences to combine: <em>The Lady Wilma entered the Golden Gate. The Sea Raven fell behind.</em></p>', 1),
     ('<p>excurse → <strong>excursion</strong> &middot; attract → <strong>attraction</strong> &middot; direct → <strong>direction</strong></p>',
      '<p>decide → <strong>decision</strong> &middot; attract → <strong>attraction</strong> &middot; direct → <strong>direction</strong></p>', 1),
     ('Use <em>–sion</em> after most words ending in –s, –se, or –d. Use <em>–tion</em> after most other bases. When in doubt, say it aloud — the sound tells you: /shun/ is usually –tion; /zhun/ is usually –sion.',
      'Look at the base word. A base that ends in <em>t</em> or <em>ct</em> (attract, direct, construct) takes <em>–tion</em>. A base that ends in <em>d</em>, <em>de</em>, <em>se</em> or <em>s</em> (decide, confuse, tense) usually takes <em>–sion</em>. You cannot always tell by sound: <em>tension</em> and <em>attraction</em> end with the same sound.', 1),
     ('<p><em>&ndash;tion</em> and <em>&ndash;sion</em> sound identical. The base word decides which you get.</p>', '<p><em>&ndash;tion</em> and <em>&ndash;sion</em> often sound alike. The base word decides which you get.</p>', 1),
     ('<p>These words appear in Chapters 7–9. Tap each card to reveal the definition.</p>', '<p>These words appear in Chapters 7–9, in the order you will meet them. Tap each card to see the meaning.</p>', 1),
     SKED + (1,), JIPI + (1,), ASSAY + (1,), CHK + (1,)],
 2: [(OLD_TIP, TIP[2], 1),
     ('San Francisco — the wildest city in America, and they have $38', 'San Francisco — the fastest growing city in the world, and they have $38', 1),
     ('San Francisco is described as the wildest city in America, and that is not decoration', 'A hawker on the wharf calls San Francisco the fastest growing city in the world, and that is not decoration', 1),
     ('The wildest city in America — and Praiseworthy opens a barbershop', 'The fastest growing city in the world — and Praiseworthy picks up the shears', 1),
     ('arrive in San Francisco with $38, no coal, no plans, and no way to get to the mines.', 'arrive in San Francisco with $38, no plans, and no way to pay for the trip to the mines.', 1),
     ('By the end of Chapter 8, Praiseworthy and Jack have solved their money problem. Explain the chain of events: how did a chance encounter on the street lead to enough money for the riverboat?',
      'By the end of Chapter 8, Praiseworthy and Jack are well on their way to solving their money problem. Explain the chain of events: how did a chance encounter with a stranger lead to gold dust in Jack&rsquo;s pan?', 1),
     ('''Although the entire city of San Francisco had turned out to greet the sidewheeler, <span class="dol-highlight-word" onclick="dolWord(this,'Complex sentence: subordinating conjunction Although sets up a contrast. The main clause surprises us — despite the whole city being there, Jack was only looking for gold.')">Jack could not keep his eyes off a dusty miner pacing in the hotel lobby.</span>''',
      '''Although the hotel lobby was busy, <span class="dol-highlight-word" onclick="dolWord(this,'Complex sentence: the subordinating conjunction Although sets up a contrast, and a comma follows the dependent clause. The main clause tells what Jack did anyway.')">Jack could not take his eyes off the bearded miner pacing across the floor.</span>''', 1),
     EX_OLD + (1,), EX2_OLD + (1,), SKED + (1,), JIPI + (1,), ASSAY + (1,), CHK + (1,)],
 3: [(OLD_TIP, TIP[3], 1), ('Chapter 9: The Jipijapa Hat', 'Chapter 9: The Man in the Jipijapa Hat', 4),
     ('Match each word to its root. ', 'Match each word to its parts and meaning. ', 1),
     ('Root: <em>curs</em> &mdash; run', 'ex + <em>curs</em> + ion: a running out (a short trip)', 1),
     ('Root: <em>tract</em> &mdash; pull', 'ex + <em>tract</em>: to pull out', 1),
     ('Root: <em>tract</em> &mdash; drag', '<em>tract</em> + ion: the grip that keeps a wheel pulling', 1),
     ('Root: <em>curr</em> &mdash; run', '<em>curr</em> + ent: water that keeps running', 1),
     CHK + (1,)],
 4: [(OLD_TIP, TIP[4], 1),
     ('I will explain curr/curs and tract roots to a classmate.', 'I will explain the curr/curs and tract roots in my own words.', 1),
     ('Explain <em>curr/curs</em> and <em>tract</em> to a classmate.', 'Explain <em>curr/curs</em> and <em>tract</em> in your own words, as if teaching someone who missed the week.', 1),
     ('A classmate asks, &ldquo;Why use complex sentences', 'Imagine someone asks, &ldquo;Why use complex sentences', 1),
     ('Give the pronunciation clue (/shun/ vs. /zhun/) and two examples of each.', 'Give the base-word clue (a base ending in <em>t</em> or <em>ct</em> takes <em>–tion</em>; one ending in <em>d</em>, <em>de</em>, <em>se</em> or <em>s</em> usually takes <em>–sion</em>) and two examples of each.', 1),
     ('<strong>skedaddled &middot; grubstake &middot; diggings &middot; assay &middot; jipijapa</strong>', '<strong>skedaddled &middot; diggings &middot; assay &middot; grubstake &middot; jipijapa</strong>', 1)],
 'flu': [
     ('      Twenty minutes later the miner was seated on a nail keg in a corner of the hotel porch, and Praiseworthy was snipping away with the shears. Quartz Jackson insisted that every lock be caught as it fell. Jack was kept busy holding a washpan under Praiseworthy&rsquo;s busy scissors.<br><br>\n',
      '      &ldquo;Yes, sir,&rdquo; said Jack, catching the lock of hair.<br><br>\n', 1),
     ('When Praiseworthy had finished, the miner turned', 'When Praiseworthy had finished the miner turned', 1),
     ('      Quartz Jackson was obviously pleased. &ldquo;Why, I&rsquo;d forgot I was so young!&rdquo;',
      '      Quartz Jackson was obviously pleased. &ldquo;Why, I&rsquo;d forgot I was so young!&rdquo;<br><br>\n'
      '      Quartz Jackson was a fine-looking gent at that, Jack thought. He had good teeth and an easy smile. Except for his revolver, his horn spoon and his red flannel shirt, he hardly seemed the same man. But what did he expect them to do with the hair cuttings? Stuff a mattress?', 1)],
}
def run(apply):
    out = {}
    for k, f in F.items():
        s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in FIX[k]:
            c = s.count(old)
            if c != n: sys.exit('%s: %d x %r' % (f, c, old[:80]))
            s = s.replace(old, new)
        if k in (1, 2): s = reorder_cards(s, k == 1)
        if k == 3: s = reorder_match(s)
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print('ok', f, len(s0), '->', len(s))
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
if __name__ == '__main__': run('--apply' in sys.argv)
