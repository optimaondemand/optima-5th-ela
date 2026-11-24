#!/usr/bin/env python3
"""Week 29 accuracy fixes (approved by Bethany Nov 23 2026; audit claude/g5-ela-wk29-audit.md).
Groups: Oct 11 items + the Ch. 14 day, spoilers, word-study errors, book + page details, fluency lengthened.
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 11-15; nothing from Ch. 16 on).
Every replacement asserts its count; div balance must not change; nothing is written unless every file passes."""
import io, re, sys
F = {1: 'lesson-29-1-btghs-ch13.html', 2: 'lesson-29-2-btghs-ch14.html', 3: 'lesson-29-3-btghs-ch15.html', 4: 'lesson-29-4-btghs-voice.html',
     'flu': 'lesson-29-fluency.html'}
CHK = ('I wrote my DOL fix and RWM journal in my reading journal.', 'I wrote my DOL fix in my reading journal.', 1)
PERSIST = ('persistently (adv.) &middot; impersistently (rare)', 'persistently (adv.)', 1)
PROSPECT = ('prospect (n./v.) &middot; prospector (n.) &middot; prospective (adj.) &middot; prospectus (n.) &middot; prosperous (adj.) &middot; prosperity (n.)',
            'prospect (n./v.) &middot; prospector (n.) &middot; prospecting (v.) &middot; prospective (adj.) &middot; prospectus (n.) <span style="font-size:13px;color:#5A6B8C;">(<em>prosperous</em> looks close, but it comes from <em>prosper</em>, a different word.)</span>', 1)
CARDS = [('Jack and Praiseworthy&rsquo;s daily prospecting shows tenacious effort.', 'Watch for tenacious work in this week&rsquo;s chapters.', 1),
         ('Cut-Eye Higgins proves evasive — he&rsquo;s always one step ahead.', 'A slippery character like Cut-Eye Higgins is often evasive.', 1),
         ('The reformed road agent is Jack&rsquo;s unlikely benefactor in Ch.15.', 'Watch for an unlikely benefactor in this week&rsquo;s chapters.', 1)]
TECH = ('He often pairs a very short sentence with a longer one immediately after — the short one lands the fact, the longer one explores it. <em>&ldquo;Pay dirt eluded them — but the next bend in the river might make their fortune.&rdquo;</em>',
        'He often puts a very short sentence right after a longer one. <em>&ldquo;The bear steak was greasy and stringy, but something to write home about. Jack forced it down.&rdquo;</em> (Chapter 11)', 1)
SECRET1 = ('Not &ldquo;a tool&rdquo; — an &ldquo;umbrella turned gold pan.&rdquo;', 'Not &ldquo;a tool&rdquo; but a horn spoon.', 1)
SECRET3 = ('&ldquo;Pay dirt eluded them.&rdquo; Period. Then the longer thought.', '&ldquo;Jack forced it down.&rdquo; Then the longer thought.', 1)
HUMOUR = ('humour', 'humor', 1)
def dolmodel(inner):
    return (re.compile(r'<div class="dol-model-sentence" id="dolModel">.*?</div>', re.S), '<div class="dol-model-sentence" id="dolModel">%s</div>' % inner, 1)
FIX = {
 1: [('<div class="quote-strip-text">&ldquo;That was a fine purchase,&rdquo; he smiled. &ldquo;A brilliant purchase.&rdquo;</div>',
      '<div class="quote-strip-text">&ldquo;In the days that followed Praiseworthy&rsquo;s name and reputation spread through the diggings.&rdquo;</div>', 1),
     ('quote-strip-attr">Praiseworthy, Chapter 13 &bull;', 'quote-strip-attr">Chapter 13 &bull;', 1),
     ('Jack says &ldquo;ate&rdquo; meaning the number 8, and ends up buying a whole bushel of neckties. Pitch-pine Billy says: &ldquo;I&rsquo;d rather see you break your leg than your word, boy.&rdquo; Jack pays. And Praiseworthy calls it brilliant. Chapter 13 is about integrity — and creative thinking.',
      'In Chapter 13 Jack and Praiseworthy settle into life in the diggings, and one small word gets Jack into trouble at an auction. Watch what Jack does when keeping his word costs him something, and what Praiseworthy makes of it.', 1),
     dolmodel('<span class="dol-highlight-word" onclick="dolWord(this,\'Opener: the sentence starts with two phrases, not with the subject. The comma shows where the opener ends and the main idea begins.\')">And then, as if to live up to his reputation,</span> <span class="dol-highlight-word" onclick="dolWord(this,\'The main idea comes last and is short: he stopped shaving. A long opener and a short ending make the joke land.\')">he stopped shaving.</span>'),
     ('jack paid his debt he was tenacious (–ous) even though the purchase of a whole bushel of neckties at the Cheap John auction was the result of an impulsive (–ive) misunderstanding about a-t-e versus eight',
      'jack was a tenacious (–ous) miner he shoveled dirt and panned mud from morning till night', 1),
     (re.compile(r'(id="dolAns1"><p><strong>Corrected:</strong> ).*?(</div>)', re.S),
      r'\1Jack was a tenacious miner. He shoveled dirt and panned mud from morning till night.</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capital <em>J</em> in <em>Jack</em>; a period after <em>miner</em> makes two sentences, one short and one longer.</p>\2', 1),
     ("Jack accidentally bids on a whole bushel of neckties. He has to pay. Pitch-pine Billy says he'd rather see Jack break his leg than his word. In your journal: Why does keeping your word matter more than being right? Write 2–3 sentences before reading.",
      'Chapter 13 has an auction where one word is misheard. In your journal: If someone misunderstands you and you end up owing them, should you still pay? Write 2&ndash;3 sentences before reading.', 1),
     ('<em>describe</em> → <em>descript</em><strong>ive</strong> → <em>descriptive</em> → <em>descriptivi</em><strong>ty</strong><br>',
      '<em>act</em> → <em>act</em><strong>ive</strong> → <em>activ</em><strong>ity</strong><br>', 1),
     ('In Chapters 13–15, Praiseworthy&rsquo;s <em>notori</em><strong>ety</strong> spreads through the diggings. The partners prove <em>tenaci</em><strong>ous</strong> — working claim after claim. Cut-Eye Higgins remains <em>evas</em><strong>ive</strong> — always just out of reach.',
      'At the start of Chapter 13, Praiseworthy&rsquo;s <em>notori</em><strong>ety</strong> spreads through the diggings. Watch for people in these chapters who are <em>tenaci</em><strong>ous</strong> or <em>evas</em><strong>ive</strong>.', 1),
     ('<em>tenacity → tenaci</em><strong><em>ous</em></strong>', '<em>fame → fam</em><strong><em>ous</em></strong>', 1),
     ("Jack fell into the coyote hole and he couldn't get out and he tried to climb but he fell back and then he fired his gun and a man came and threw him a rope and pulled him out.",
      'Jack and Praiseworthy walked back to town and they carried their shoes and their feet ached and the miners on the porch stared at them and then someone called Praiseworthy Bullwhip.', 1),
     ('Build the word family for <em>persist</em>. Write: persist (v.), then add –ent, –ence, –ently, and the prefix im– to make <em>impersistent</em> (is this a real word?). For each form, write the part of speech and one sentence using it in context.',
      'Build the word family for <em>persist</em>. Write <em>persist</em> (v.), then add –ent, –ence and –ently. For each form, write the part of speech and one sentence using it.', 1),
     ('Chapter 13 settles Jack and Praiseworthy into the rhythms of the diggings — flea traps, coyote holes, prices that defy belief. Then comes the necktie incident. Watch how Fleischman uses misunderstanding as comedy, but also as a character test: Jack pays up. Then Praiseworthy calls it brilliant. The second half of the chapter shows why: <strong>how do you turn an embarrassment into an asset?</strong> That&rsquo;s the Praiseworthy way.',
      'Chapter 13 settles Jack and Praiseworthy into the diggings: flea traps, coyote holes and prices that are hard to believe. Then comes an auction. Watch how Fleischman uses a misunderstanding for comedy and as a test of character. <strong>Watch what each character does when a small mistake costs real gold.</strong>', 1),
     ('Jack accidentally bids on a whole bushel of neckties because &ldquo;ate&rdquo; and &ldquo;eight&rdquo; sound the same.',
      'At the auction, Jack answers a friend with the word &ldquo;ate,&rdquo; and the auctioneer hears &ldquo;eight.&rdquo;', 1),
     ("data-label=\"Reading Q1: What 'notoriety' means — why Praiseworthy enjoys it\"", 'data-label="Reading Q1: Keeping his word — how Jack has changed since Boston"', 1),
     PERSIST, PROSPECT, TECH, SECRET1, SECRET3, CHK] + CARDS,
 2: [('<div class="quote-strip-text">&ldquo;Not woodpeckers,&rdquo; he imagined himself explaining to Constance and Sarah. &ldquo;We call &rsquo;em carpentaros in the diggings.&rdquo;</div>',
      '<div class="quote-strip-text">&ldquo;We&rsquo;re going to be friends,&rdquo; he said. &ldquo;Yes, sir.&rdquo;</div>', 1),
     ('quote-strip-attr">Chapter 14 &bull;', 'quote-strip-attr">Jack to Stubb, Chapter 14 &bull;', 1),
     ('Chapter 14 shows Jack as a genuine Forty-Niner: he has a burro, a squirrel gun, and a way of explaining things to his imaginary sisters. He can pan gold. He knows the mountains. He is becoming someone Constance and Sarah really would not recognize — and he loves it.',
      'Chapter 14 is about getting ready to leave. Jack meets a burro with opinions, the partners say goodbye to their friends in camp, and Praiseworthy explains how he plans to win a fight he never asked for. Watch how each of them gets ready for what is ahead.', 1),
     ('He gave a little kick — just to get it out of his system.</p>', 'He gave a little kick, just to get it out of his system.</p>', 1),
     ('em dash before <em>just to get it out of his system</em> (adds Fleischman-style comic punch)', 'comma before <em>just to get it out of his system</em>', 1),
     ('Chapter 14 has Jack with a squirrel gun, practicing his aim at a mountain cat he imagines in a tree. He thinks about explaining carpentaros to his sisters. In your journal: What does this inner monologue tell us about who Jack is becoming? Write 2–3 sentences.',
      'In Chapter 14 the partners get ready to leave Hangtown for the mountains. In your journal: What is the hardest part of leaving friends behind, even for an adventure? Write 2&ndash;3 sentences before reading.', 1),
     ('or the coyote hole rescue (Ch. 15).', 'or the necktie auction (Ch. 13).', 1),
     ('about Jack&rsquo;s character in Chapters 13–15.', 'about Jack&rsquo;s character in Chapters 13–14.', 1),
     ('prospect, prospector, prospective, prospectus, prosperous, prosperity.', 'prospect, prospector, prospecting, prospective, prospectus.', 1),
     ('activity-sub">Stubb the stubborn burro, a squirrel gun, and the mountains', 'activity-sub">Stubb the stubborn burro, the goodbyes, and a book about boxing', 1),
     ('Chapter 14 is a chapter about becoming. Jack learns to ride Stubb (after falling off), learns to handle a squirrel gun, and wanders the mountains imagining his sisters&rsquo; reactions. Praiseworthy practices shadow boxing when Jack isn&rsquo;t watching. Fleischman uses small, specific details to show how these two characters are changing — and how each is keeping something private from the other. Watch for the <strong>interior voice</strong> — what characters think but don&rsquo;t say.',
      'Chapter 14 is about getting ready. Jack learns to ride Stubb (after falling off), the partners say goodbye to their friends, and Praiseworthy explains how he plans to beat the Mountain Ox. Fleischman uses small, specific details to show how both characters are changing. Watch for the <strong>inner voice</strong>: what characters think but don&rsquo;t say.', 1),
     ('Stubb kicks Jack off, then lets him back on after &ldquo;flagging his ears as if satisfied that he had been shown the proper respect.&rdquo;',
      'Stubb throws Jack off. On the second try the burro &ldquo;flagged his ears and seemed satisfied that he had been shown the proper respect.&rdquo;', 1),
     ('Jack practices with his squirrel gun, then imagines explaining carpentaros to his sisters. What does this inner monologue reveal about the gap between the Jack who left Boston and the Jack who is here now?',
      'Jack finds it hard to walk away from Pitch-pine Billy and his friends, and he thinks &ldquo;coming back would be even harder.&rdquo; Why might coming back be harder than leaving?', 1),
     ('Fleischman shows Praiseworthy shadow-boxing when Jack isn&rsquo;t watching. He keeps this private. What does this detail reveal about Praiseworthy — and why does Fleischman let us see it but keep it from Jack?',
      'Praiseworthy tells Jack about a book Miss Arabella once asked him to destroy, <em>The Gentleman&rsquo;s Book of Boxing</em>. He read it instead. What does his plan to outread the Mountain Ox reveal about Praiseworthy?', 1),
     ("data-label=\"Reading Q2: Praiseworthy's private shadow-boxing — what it reveals and why Jack can't see it\"", 'data-label="Reading Q2: The boxing book — what Praiseworthy\'s plan reveals"', 1),
     ('Chapter 14 shows Jack practicing with a squirrel gun, exploring the mountain trails alone, and imagining his life to his sisters.',
      'Chapter 14 shows Jack riding Stubb, saying goodbye to his friends, and carrying the squirrel gun into the mountains.', 1),
     PERSIST, PROSPECT, TECH, SECRET1, SECRET3, HUMOUR, CHK] + CARDS,
 3: [('<div class="quote-strip-text">&ldquo;Boy, the next time you point that squirrel gun at a bad hombre like me, you really ought to trouble yourself to reload it first.&rdquo;</div>',
      '<div class="quote-strip-text">&ldquo;They pitched camp and they broke camp.&rdquo;</div>', 1),
     ('quote-strip-attr">The reformed road agent, Chapter 15 &bull;', 'quote-strip-attr">Chapter 15 &bull;', 1),
     ('intro-card-head-title">What do you do when the answer you needed was never in the coat?', 'intro-card-head-title">What keeps you going when the gold won&rsquo;t show up?', 1),
     ('Jack falls into a coyote hole. A grizzly bear appears from the shadows. A reformed road agent pulls him out — wearing Cut-Eye Higgins&rsquo;s coat. The coat, when ripped open, has no map. Cut-Eye Higgins lied. And Praiseworthy&rsquo;s response: &ldquo;Put some beans on to fry, partner Jack. First thing in the morning we&rsquo;ll start for Shirt-tail Camp.&rdquo;',
      'In Chapter 15 the partners go prospecting, day after day, from ravine to ravine. Then Jack goes hunting alone and finds more trouble than he bargained for. Watch how the narrator&rsquo;s voice stays steady when things go wrong.', 1),
     dolmodel('<span class="dol-highlight-word" onclick="dolWord(this,\'Opener: a prepositional phrase. Starting with when it happened (After breakfast) instead of the subject is one easy way to vary sentences.\')">After breakfast</span> they struck the tent, blindfolded Stubb and cinched the wooden pack saddle to his back.'),
     ('the reformed road agent laughed at jack for pointing an unloaded squirrel gun at him but he gave jack a useful piece of advice and told him that next time he really ought to trouble himself to reload it first',
      "jack took stubb's rope and the burro followed with a clanging of drinking cups coffee pot gold pans and empty tin cans", 1),
     (re.compile(r'(id="dolAns3"><p><strong>Corrected:</strong> ).*?(</div>)', re.S),
      r'\1Jack took Stubb&rsquo;s rope, and the burro followed with a clanging of drinking cups, coffee pot, gold pans and empty tin cans.</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capital <em>J</em> and <em>S</em>; apostrophe in <em>Stubb&rsquo;s</em>; a comma before <em>and</em> that joins two complete sentences; commas between the things in the list.</p>\2', 1),
     ('The road agent who rescues Jack from the coyote hole is wearing Cut-Eye Higgins&rsquo;s coat. When Praiseworthy rips it open, there is no map. In your journal: How do you think Praiseworthy will respond to this discovery? Write 2–3 sentences before reading.',
      'In Chapter 15 the partners go prospecting on their own. In your journal: When a plan keeps failing, what helps a person keep going? Write 2&ndash;3 sentences before reading.', 1),
     ('(4) prospect/prospector/prospective/prosperous/prosperity', '(4) prospect/prospector/prospecting/prospective', 1),
     ('Match each suffix to what it makes the word do.', 'Match each word to its meaning.', 1),
     ('data-match="B" onclick="g5Match(this)">Suffix <em>&ndash;ous</em>: full of</div>', 'data-match="B" onclick="g5Match(this)">full of poison</div>', 1),
     ('data-match="A" onclick="g5Match(this)">Suffix <em>&ndash;ous</em>: full of</div>', 'data-match="A" onclick="g5Match(this)">full of danger</div>', 1),
     ('data-match="C" onclick="g5Match(this)">Suffix <em>&ndash;ive</em>: tending to</div>', 'data-match="C" onclick="g5Match(this)">tending to make new things</div>', 1),
     ('data-match="D" onclick="g5Match(this)">Suffix <em>&ndash;ity</em>: the state of being</div>', 'data-match="D" onclick="g5Match(this)">the wish to know or learn</div>', 1),
     ('info-value">Chapter 15: Man Who', 'info-value">Chapter 15: The Man Who', 1),
     ('Chapter 15 combines three of Fleischman&rsquo;s best comic-adventure techniques: (1) escalating danger that turns absurd (grizzly + coyote hole + unloaded gun); (2) a villain redeemed by circumstance (the road agent who can&rsquo;t sit down); (3) a hope dashed — but Praiseworthy responds immediately with the next plan. Watch how Fleischman handles the disappointment of the empty coat. <strong>How does tone prevent this moment from feeling like a failure?</strong>',
      'Chapter 15 mixes adventure and comedy: days of hard prospecting, news about an old enemy, and a hunting trip that goes wrong. Watch how Fleischman handles danger and disappointment. <strong>How does the narrator&rsquo;s calm voice change how a scary or sad moment feels?</strong>', 1),
     ('Jack falls into a coyote hole while a grizzly bear circles nearby. He fires his gun to get help. Fleischman plays this scene for comedy. What specific comic elements make a frightening situation funny?',
      'Jack falls into a coyote hole while backing away from a grizzly. He fires his gun to call for help. Fleischman plays this scene partly for comedy. What details make a frightening moment funny?', 1),
     ('Jack is trapped in a coyote hole with a grizzly nearby and only an unloaded squirrel gun.', 'Jack is trapped at the bottom of a coyote hole after running into a grizzly, with only a squirrel gun.', 1),
     ('data-label="Reading Q1: Coyote hole + grizzly + unloaded gun', 'data-label="Reading Q1: Coyote hole + grizzly', 1),
     PERSIST, PROSPECT, HUMOUR, CHK],
 4: [('by a poet writing thirty years later, in a country Stevenson never saw.', 'by an American poet writing about thirty years later.', 1),
     ('Explain the difference between –ous, –ive, and –ity to a classmate in 4 sentences.', 'Explain the difference between –ous, –ive, and –ity in 4 sentences, as if you were teaching it.', 1),
     ('create</em> dropped its e. The other three did not change.', 'create</em> dropped its e, and <em>curious</em> dropped its u. The other two did not change.', 1),
     ('they hope for <em>prosperity</em>.', 'they go <em>prospecting</em>.', 1),
     ('Synthesise the week', 'Synthesize the week', 1),
     ('Not &ldquo;a miner&rdquo; — &ldquo;a miner with chestnut hair tumbling out on all sides like mattress stuffing coming loose.&rdquo;',
      'Not just &ldquo;a miner with long hair&rdquo; but a miner whose &ldquo;chestnut hair tumbled out on all sides like mattress stuffing coming loose&rdquo; (Chapter 8).', 1),
     ('&ldquo;Pay dirt eluded them.&rdquo; &ldquo;He couldn&rsquo;t get out.&rdquo; &ldquo;There was no map.&rdquo;', '&ldquo;It was.&rdquo; &ldquo;He couldn&rsquo;t get out.&rdquo; &ldquo;There was no map.&rdquo;', 1),
     ('Praiseworthy notices the lumber. Jack notices the pistol. Neither says anything. The reader draws the conclusion.',
      'On the stage, Jack notices the dueling pistol in Cut-Eye Higgins&rsquo;s belt and says nothing. In Chapter 15, Jack catches Praiseworthy gazing at a view &ldquo;as if it didn&rsquo;t matter if they ever got back to Boston.&rdquo; The reader draws the conclusion.', 1),
     ('&ldquo;Put some beans on to fry. First thing in the morning we&rsquo;ll start for Shirt-tail Camp.&rdquo;',
      '&ldquo;Put some beans on to fry, partner Jack. First thing in the morning we&rsquo;ll start for Shirt-tail Camp.&rdquo;', 1),
     ('<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I am ready for Week 30 — the final week, the conclusion, and the long voyage home.</div></div>', '', 1),
     SECRET1, SECRET3],
}
FLU_OLD = '''      The ex-highwayman started away and then turned with a final laugh.<br><br>
      &ldquo;Boy, the next time you point that squirrel gun at a bad hombre like me, you really ought to trouble yourself to reload it first. Good luck, boy.&rdquo;<br><br>
'''
FLU_NEW = io.open('planning docs/_pv/w29/flu_new.html', encoding='utf-8').read() if len(sys.argv) > 0 else ''
FIX['flu'] = [(FLU_OLD, FLU_NEW, 1),
  ('This week Jack fell into a coyote hole with a grizzly nearby, an unloaded squirrel gun, and no one in earshot. The man who rescued him had some parting advice. Today you practice the most comic exit line in the novel — the road agent who is totally right and knows it.',
   'This week Jack fell into a coyote hole with no one in earshot. Today you read the whole talk between Jack and the stranger who pulled him out, right up to the stranger&rsquo;s parting advice.', 1),
  ('Then Jack&rsquo;s reaction should feel slower, more internal: &ldquo;His face reddened under the layers of dust.&rdquo;', 'Then Jack&rsquo;s reaction should feel slower, more internal: &ldquo;Jack&rsquo;s face reddened under the layers of dust.&rdquo;', 1),
  ('Did Jack&rsquo;s embarrassment come through in &ldquo;His face reddened under the layers of dust&rdquo;?', 'Did Jack&rsquo;s embarrassment come through in &ldquo;Jack&rsquo;s face reddened under the layers of dust&rdquo;?', 1),
  ('<div class="step-detail">The road agent&rsquo;s speech is one long sentence that builds', '<div class="step-detail">Jack is suspicious and the road agent is easygoing; let the two voices sound different. The road agent&rsquo;s last speech is one long sentence that builds', 1),
]
def main():
    apply = '--apply' in sys.argv; out = {}
    for k, reps in FIX.items():
        f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in reps:
            if isinstance(old, str):
                c = s.count(old)
                if c != n: sys.exit('%s: %d x %r' % (f, c, old[:80]))
                s = s.replace(old, new)
            else:
                s, c = old.subn(new, s, count=n)
                if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:60]))
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print('ok', f)
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
main()
