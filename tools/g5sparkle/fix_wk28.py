#!/usr/bin/env python3
"""Week 28 accuracy fixes (approved by Bethany Nov 23 2026; audit claude/g5-ela-wk28-audit.md).
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 10-12). Every replacement asserts its
count; div balance must not change; nothing is written unless every file passes. Run once from the repo root."""
import io, sys
F = {1: 'lesson-28-1-btghs-ch10.html', 2: 'lesson-28-2-btghs-ch11.html', 3: 'lesson-28-3-btghs-ch12.html', 4: 'lesson-28-4-btghs-theme.html',
     'flu': 'lesson-28-fluency.html'}
CHK = ('I wrote my DOL fix and RWM journal in my reading journal.', 'I wrote my DOL fix in my reading journal.', 1)
VALID = ('The town&rsquo;s story about Bullwhip has creative validity — it\'s exaggerated, but captures something true.',
         'To test the validity of a claim, you check it against the facts.', 1)
FLU_OLD = '''      Praiseworthy stopped in the doorway. He looked at Jack, who broke into a muddy smile. Then the butler turned, peering at the whiskered faces grinning in the yellow light from the hotel.<br><br>
      &ldquo;Gents,&rdquo; he said, &ldquo;from where I was standing &mdash; it looked twenty-three feet at least.&rdquo;<br><br>
      A miner swallowed his cud of tobacco. &ldquo;O be joyful.&rdquo;<br><br>
      &ldquo;Come along, Jamoka Jack,&rdquo; said Praiseworthy, turning into the hotel.
'''
FLU_NEW = '''      Praiseworthy stopped in the doorway. He looked at Jack, who broke into a muddy smile as if they had been saved from the limb of a tree. And then the butler turned, peering at the whiskered faces grinning in the yellow light from the hotel.<br><br>
      A miner shifted the lump of chewing tobacco in his mouth and said, &ldquo;Stranger, you must have a fightin&rsquo; arm like the butt end of a bullwhip. Pleased to have you in our town.&rdquo;<br><br>
      &ldquo;Pleased to be here,&rdquo; Praiseworthy said, lowering the pick from his shoulder. &ldquo;But not under false colors. Gentlemen, allow me to explain &mdash;&rdquo;<br><br>
      &ldquo;Hey, Bullwhip, where you and the young&rsquo;un from?&rdquo;<br><br>
      &ldquo;Boston, sir. Gentlemen, our good friend and traveling companion, Mr. Jonas T. Fletcher, appears to have spread a grossly exaggerated account of what happened. You see &mdash;&rdquo;<br><br>
      &ldquo;Hold on. You callin&rsquo; him a liar?&rdquo;<br>
      &ldquo;No, but &mdash;&rdquo;<br>
      &ldquo;Well, did you knock that road agent up hill or not?&rdquo;<br>
      &ldquo;Yes, but &mdash;&rdquo;<br><br>
      The miners began to chuckle and chewing tobacco went squirting in all directions. They had taken an immediate fancy to Praiseworthy and one by one they picked up the nickname.<br><br>
      &ldquo;How long you stayin&rsquo;, Bullwhip?&rdquo;<br><br>
      Praiseworthy shouldered the pick. He gave up trying to explain. It seemed to him that every man in the diggings became hard of hearing when he wanted to, and he&rsquo;d had enough of that for one day. If they preferred a tall tale to the facts, let them have it.<br><br>
      &ldquo;Bullwhip, you was there. Exactly how far was it?&rdquo;<br><br>
      Praiseworthy gave Jack a passing wink. As long as the citizens of Hangtown were determined to hang a reputation on him, it might as well be the best. &ldquo;Gents,&rdquo; he said, &ldquo;from where I was standing &mdash; it looked twenty-three feet at least.&rdquo;<br><br>
      A miner swallowed his cud of tobacco. &ldquo;O be joyful,&rdquo; he uttered.<br><br>
      &ldquo;Come along, Jamoka Jack,&rdquo; said Praiseworthy, turning into the hotel.<br><br>
      Jack felt a brand new smile reach across his face. &ldquo;Yes, sir &mdash; Bullwhip,&rdquo; he said.
'''
FIX = {
 1: [('<div class="quote-strip-text">&ldquo;Leave the scoundrel to me.&rdquo;</div>',
      '<div class="quote-strip-text">&ldquo;Easy, Master Jack, easy. Leave the scoundrel to me.&rdquo;</div>', 1),
     ('Praiseworthy remains completely calm — he even introduces Higgins to the undertaker by name. What is his strategy, and how does it work?',
      'Praiseworthy stays completely calm. He even introduces the undertaker to Higgins and remarks that a man in Higgins&rsquo;s line of work never knows when he&rsquo;ll need a good undertaker. What is his strategy, and how does it work?', 1),
     ('calm, wit, naming the undertaker"', 'calm, wit, introducing the undertaker"', 1),
     ('His <em>valor</em> peaks when he punches the ruffian in Chapter 10.', 'Watch for an act of <em>valor</em> in Chapter 10.', 1),
     ("Praiseworthy's punch in Chapter 10 is an act of valor.", 'Watch for an act of valor in this week&rsquo;s chapters.', 1),
     VALID,
     ('Jack&rsquo;s emotion as Praiseworthy insists on eating lunch before visiting the diggings.', 'Watch for it in Chapter 11.', 1),
     ('<em>brave → brav</em><strong><em>ity</em></strong>', '<em>active → activ</em><strong><em>ity</em></strong>', 1),
     ('data-group="ity" onclick="g5Pick(this)">loyalty</span>', 'data-group="ity" onclick="g5Pick(this)">scarcity</span>', 1),
     ('Sorted. <em>loneliness</em> keeps the y&rarr;i change; <em>argument</em> drops the e.',
      'Sorted. <em>loneliness</em> changes y to i; <em>argument</em> and <em>scarcity</em> drop the e.', 1),
     CHK],
 2: [('Praiseworthy&rsquo;s umbrella gets used as a gold pan. A thimbleful of gold is the reward for a full afternoon&rsquo;s work. And Fleischman',
      'And Fleischman', 1),
     ('Watch how he makes a <em>thimbleful of gold</em> feel like a victory. Notice also how Pitch-pine Billy&rsquo;s use of Praiseworthy&rsquo;s umbrella as a gold pan captures something important about how the old world and the new collide throughout the novel.',
      'Watch how he makes a very small find feel like a victory, and watch what Praiseworthy has to give up along the way.', 1),
     ('was enormous; but Praiseworthy', 'was enormous, but Praiseworthy', 1),
     ('HOW&middot;ev&middot;er', 'how&middot;EV&middot;er', 1), ('fur&middot;THER&middot;more', 'FUR&middot;ther&middot;more', 1),
     ('con&middot;SE&middot;quent&middot;ly', 'CON&middot;se&middot;quent&middot;ly', 1),
     ('e<input class="fillin-input" id="m22" data-answer="quival" maxlength="7"', 'equi<input class="fillin-input" id="m22" data-answer="val" maxlength="7"', 1),
     VALID, CHK],
 3: [('<div class="quote-strip-text">&ldquo;Come along, Jamoka Jack,&rdquo; said Praiseworthy, turning into the hotel.</div>',
      '<div class="quote-strip-text">&ldquo;Campfires along the river lit their way back to town.&rdquo;</div>', 1),
     ('The miners of Hangtown have heard a story about a stranger who knocked a road agent nineteen feet uphill. They have given this stranger a name: Bullwhip. They have accepted him instantly. What does this tell us about what life in the diggings valued? And what does Praiseworthy do with this reputation?',
      'Word of the stagecoach robbery has reached Hangtown, and the story has grown in the telling. What does a town&rsquo;s favorite story tell you about what it values? Read to see what Praiseworthy does when he hears it.', 1),
     ('Chapter 12 ends with Praiseworthy called Bullwhip and Jack called Jamoka Jack. In your journal: Why do the miners&rsquo; nicknames fit — what has each character actually proven about himself? Write 2–3 sentences before reading.',
      'Yesterday Pitch-pine Billy gave Jack a nickname. In your journal: Why do people give each other nicknames? What does a nickname you earn say about you? Write 2–3 sentences before reading.', 1),
     ('Then the town greets them with a legend. Praiseworthy, who values honesty and precision above almost everything else, decides to accept the exaggerated story. Watch for what this decision reveals about who he has become.',
      'Then the partners walk back into town. Praiseworthy cares about honesty and about getting things exactly right. Watch how Hangtown greets him, and what he decides to do about it.', 1),
     ('Jack says &ldquo;Partners were the next best thing to being related.&rdquo;', 'Jack thinks, &ldquo;Partners were the next best thing to being related.&rdquo;', 1),
     ('Praiseworthy tries three times to correct', 'Praiseworthy tries to correct', 1),
     ('in a decision about money &mdash;', 'in a choice about the truth &mdash;', 1),
     ('''Praiseworthy should not have been called Bullwhip; <span class="dol-highlight-word" onclick="dolWord(this,'Nevertheless = despite what just came before. It shows a contrast or concession. Semicolon before; comma after — correct transition punctuation.')">nevertheless</span>, he gave up trying to explain and played along.''',
      '''Pitch-pine Billy shot a hole in their washpan; <span class="dol-highlight-word" onclick="dolWord(this,'Nevertheless means in spite of what just came before. It joins two complete sentences: a semicolon before it and a comma after it.')">nevertheless</span>, Praiseworthy accepted a cup of his coffee.''', 1),
     ('however praiseworthy had tried to correct the miners exaggerated story they preferred the tall tale therefore he accepted the nickname consequently he was known throughout hangtown as bullwhip',
      'at first jack could barely swallow the coffee however he kept drinking as a result pitch-pine billy named him jamoka jack', 1),
     ('However, Praiseworthy had tried to correct the miners&rsquo; exaggerated story; they preferred the tall tale. Therefore, he accepted the nickname. Consequently, he was known throughout Hangtown as Bullwhip.',
      'At first, Jack could barely swallow the coffee. However, he kept drinking. As a result, Pitch-pine Billy named him Jamoka Jack.', 1),
     ('loyal + ty = <input class="fillin-input" data-answer="loyalty"', 'bold + ness = <input class="fillin-input" data-answer="boldness"', 1),
     ('Only <em>loyalty</em> left it alone.', 'Only <em>boldness</em> left it alone.', 1),
     ('Match each word to its root. <em>fort</em> = strong. <em>val / valid</em> = worth, strength.', 'Match each word to its meaning. <em>fort</em> = strong. <em>val / valid</em> = strong, worth.', 1),
     ('data-match="B" onclick="g5Match(this)">Root: <em>fort</em> &mdash; strong</div>', 'data-match="B" onclick="g5Match(this)">to make a place stronger</div>', 1),
     ('data-match="C" onclick="g5Match(this)">Root: <em>val</em> &mdash; worth</div>', 'data-match="C" onclick="g5Match(this)">brave and strong in danger</div>', 1),
     ('data-match="D" onclick="g5Match(this)">Root: <em>valid</em> &mdash; strength</div>', 'data-match="D" onclick="g5Match(this)">to show that something is true</div>', 1),
     ('data-match="A" onclick="g5Match(this)">Root: <em>fort</em> &mdash; strong</div>', 'data-match="A" onclick="g5Match(this)">strength to bear hard times</div>', 1),
     ('Both roots mean strength &mdash; one of the body, one of an argument.', 'Each meaning carries its root: strong for <em>fort</em>, strong or worth for <em>val</em>.', 1),
     CHK],
 4: [('<div class="quote-strip-text">&ldquo;Partners were the next best thing to being related. Better, maybe.&rdquo;</div>',
      '<div class="quote-strip-text">&ldquo;Partners were the next best thing to being related, he thought. Better, maybe.&rdquo;</div>', 1),
     ('of their partnership. &ldquo;Partners were the next best thing to being related.&rdquo;', 'of their partnership. Jack thinks, &ldquo;Partners were the next best thing to being related.&rdquo;', 1),
     ('Synthesise the week', 'Synthesize the week', 1), ('worth memorising.', 'worth memorizing.', 1),
     ('<em>val/valid</em> to a classmate.', '<em>val/valid</em> in your own words, as if teaching someone who missed the week.', 1),
     ('In your journal: A classmate says &ldquo;I always confuse', 'In your journal: Imagine someone says &ldquo;I always confuse', 1),
     ('–ity, –ment, and –ness to a classmate in 3–4 sentences.', '–ity, –ment, and –ness in your own words in 3–4 sentences.', 1),
     ('<div class="activity-title">Q4 — Talk It Over</div>', '<div class="activity-title">Q4: Argue the Other Side</div>', 1),
     ('Before you finish, discuss your theme claim with someone. Ask them to argue for a <em>different</em> theme in the book, or to push back on yours. Listen to their whole argument, then answer with evidence from Chapters 1&ndash;12. Write what they argued, how you responded, and whether you changed or strengthened your claim.',
      'Pick a theme from the four above that you did <em>not</em> choose. Write the best case for it in 1 or 2 sentences, using one event from Chapters 1&ndash;12. Then answer it with your own evidence, and say whether your claim changed or got stronger.', 1),
     ('Disagreeing well means restating their point fairly before you answer it: &ldquo;You&rsquo;re saying ___. But in Chapter ___ &hellip;&rdquo;',
      'Answering well means stating the other side fairly first: &ldquo;Someone could argue ___. But in Chapter ___ &hellip;&rdquo;', 1),
     ('data-label="Q4: talk it over" placeholder="They argued ... I responded ... Now my claim is ..."', 'data-label="Q4: argue the other side" placeholder="Someone could argue ... But in Chapter ... Now my claim is ..."', 1),
     ('I discussed my theme claim with someone and wrote how I responded.', 'I argued the other side and answered it with evidence.', 1),
     ('<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I am ready for Week 29 — voice, tone analysis, and the final stretch of the story.</div></div>', '', 1)],
 'flu': [(FLU_OLD, FLU_NEW, 1)],
}
def run(apply):
    out = {}
    for k, f in F.items():
        s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in FIX[k]:
            c = s.count(old)
            if c != n: sys.exit('%s: %d x %r' % (f, c, old[:90]))
            s = s.replace(old, new)
        d0 = s0.count('<div') - s0.count('</div>'); d1 = s.count('<div') - s.count('</div>')
        if d0 != d1: sys.exit('div balance ' + f)
        out[f] = s; print('ok', f, len(s0), '->', len(s))
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
if __name__ == '__main__': run('--apply' in sys.argv)
