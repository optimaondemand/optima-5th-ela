#!/usr/bin/env python3
"""Week 30 accuracy fixes (approved by Bethany Nov 24 2026; audit claude/g5-ela-wk30-audit.md).
Groups: Oct 11 items, spoilers before reading, invented DOL lines + numbers, page fixes + fluency (continuous Ch. 18 stretch).
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 1-18).
Every replacement asserts its count; div balance must not change; nothing is written unless every file passes.
    python tools/g5sparkle/fix_wk30.py [--apply]"""
import io, re, sys
F = {1: 'lesson-30-1-btghs-ch16.html', 2: 'lesson-30-2-btghs-ch17.html', 3: 'lesson-30-3-btghs-ch18.html', 4: 'lesson-30-4-btghs-synthesis.html',
     'flu': 'lesson-30-fluency.html'}
def RX(pat, new, n=1, flags=re.S):
    return (re.compile(pat, flags), new, n)
def grp(pat_a, mid, pat_b, new):
    """replace what sits between two anchors (anchors kept)"""
    return (re.compile('(' + pat_a + ')' + mid + '(' + pat_b + ')', re.S), lambda m: m.group(1) + new + m.group(2), 1)
QUOTE = lambda text, attr: [grp(r'<div class="quote-strip-text">', r'.*?', r'</div>', text), grp(r'<div class="quote-strip-attr">', r'.*?', r' &bull;', attr)]
SUBT = lambda t: grp(r'<text x="625" y="107"[^>]*>', r'[^<]*', r'</text>', t)
OVQ = lambda t: grp(r'theme-question">.*?intro-card-head-title">', r'[^<]*', r'</div>', t)
OVB = lambda t: grp(r'theme-question">.*?intro-card-body"><p>', r'.*?', r'</p>', t)
OBJ = lambda t: grp(r'<strong>Reading:</strong> ', r'.*?', r'</span>', t)
BYR = lambda t: grp(r'Before You Read</div><p class="socratic-q">', r'.*?', r'</p>', t)
FOCUS = lambda t: grp(r'Reading Focus</div><p>', r'.*?', r'</p>', t)
RSUB = lambda t: grp(r'activity-title">Read: Chapter \d+[^<]*</div><div class="activity-sub">', r'[^<]*', r'</div>', t)
DOLM = lambda t: grp(r'<div class="dol-model-sentence" id="dolModel">', r'.*?', r'</div>', t)
DOLF = lambda t: grp(r'<div class="dol-fix-sentence">', r'[^<]*', r'</div>', t)
DOLA = lambda t: grp(r'id="dolAns\d"><p><strong>Corrected:</strong> ', r'.*?', r'</p>', t)
def CARD(word, t): return grp(r'fc-word-back">' + word + r'</div><div class="fc-def">', r'.*?', r'</div>', t)
CHK = ('I wrote my DOL edit and RWM journal in my reading journal.', 'I wrote my Daily Oral Language fix in my reading journal.', 1)
NEUTRAL_CARDS = [
    CARD('exuberance', 'Joyful, overflowing energy. From Latin <em>exuberare</em> (to overflow). Watch for a moment of sheer exuberance in this week&rsquo;s chapters.'),
    CARD('spirited', 'Lively, eager and full of energy. From Latin <em>spiritus</em> (breath, spirit). A spirited crowd is loud and eager, not shy.'),
    CARD('reunion', 'A gathering of people who have been apart for a long time. From French <em>r&eacute;union</em>. Think of a family meeting at a dock after a long voyage.'),
]
FIX = {
 1: QUOTE('&ldquo;They followed the South Fork of the American River into the winding Coloma Valley.&rdquo;', 'Chapter 16') + [
     SUBT('Coloma, Shirt-tail Camp, and a speech nobody expected'),
     OVQ('What would make you speak up for someone who cheated you?'),
     OVB('In Chapter 16 the partners reach Shirt-tail Camp and find a crowd that has already decided what to do with Cut-Eye Higgins. Praiseworthy has no time to plan. Watch what he says, why it works on the crowd, and where the day leads.'),
     OBJ('I will analyze Praiseworthy&rsquo;s speech at Shirt-tail Camp and how Ch. 16 ends.'),
     DOLM('<span class="dol-highlight-word" onclick="dolWord(this,\'A comma before <em>but</em> joins the two halves. The question answers itself: Praiseworthy asks it to make the crowd think, not to get a reply.\')">He may deserve his fate, but what of the innocent whose only crime is to come down with the toothache?</span>'),
     DOLF('praiseworthy had never made a speech in his life but the words rolled off his tongue and he could feel their effect on the crowd when he finished he was greeted with a yell of approval hes talkin sense someone called out'),
     DOLA('Praiseworthy had never made a speech in his life, but the words rolled off his tongue and he could feel their effect on the crowd. When he finished he was greeted with a yell of approval. &ldquo;He&rsquo;s talkin&rsquo; sense,&rdquo; someone called out.</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capital <em>P</em>; a comma before <em>but</em>; a period after <em>crowd</em>; quotation marks with the comma inside them; apostrophes in <em>He&rsquo;s</em> and <em>talkin&rsquo;</em> (the second one stands for the missing <em>g</em>, the way the miners talk).'),
     BYR('In Chapter 16 the partners reach a camp where a crowd has already decided a man is guilty, with no judge and no lawyer. In your journal: Should someone get the chance to speak up for him first? Why? Write 2&ndash;3 sentences before reading.'),
     ('<p class="tab-transition-voice">Final week. Review everything you&rsquo;ve learned.</p>', '<p class="tab-transition-voice">The last week of the novel. Word Study is next.</p>', 1),
     RSUB('Coloma, Shirt-tail Camp, and a speech nobody expected'),
     FOCUS('Chapter 16 holds Praiseworthy&rsquo;s most unlikely triumph: a speech to save the man who tricked them. Watch three things: how Praiseworthy wins over the crowd, what Cut-Eye Higgins hands over in return, and the job the Justice of the Peace gives the partners at the end.'),
     ('Praiseworthy says he&rsquo;s &ldquo;never made a speech in his life&rdquo; — but then delivers a brilliant one about toothaches.',
      'Fleischman tells us Praiseworthy &ldquo;had never made a speech in his life.&rdquo; Then he gives a brilliant one about toothaches.', 1),
     CARD('reprieve', 'A delay or cancellation of a punishment. From Old French <em>repris</em> (taken back). A judge can grant a reprieve, a delay before a sentence is carried out.'),
     CARD('counsel', 'A lawyer who speaks for someone in a trial; it also means advice. In a fair trial, each side has counsel to speak for it.'),
     CHK] + NEUTRAL_CARDS,
 2: QUOTE('&ldquo;We&rsquo;ve done it, Jack, we&rsquo;ve done it!&rdquo; Praiseworthy roared.', 'Chapter 17') + [
     OVB('Chapter 17 opens in the pit where Chapter 16 ended, and in the excitement Praiseworthy calls him &ldquo;Jack&rdquo; instead of &ldquo;Master Jack.&rdquo; Just Jack. Plain Jack, &ldquo;the way he&rsquo;d always wanted it to be.&rdquo; One small word dropped carries the weight of the whole partnership.'),
     OBJ('I will analyze the celebration, the claim and the day of the match in Ch. 17.'),
     DOLF('the two partners flung their hats in the air in sheer exuberance they clasped arms and swung around and around in the oblong pit weve done it jack weve done it praiseworthy roared'),
     DOLA('The two partners flung their hats in the air. In sheer exuberance, they clasped arms and swung around and around in the oblong pit. &ldquo;We&rsquo;ve done it, Jack, we&rsquo;ve done it!&rdquo; Praiseworthy roared.</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capital <em>T</em>; a period after <em>air</em>; a comma after the opener <em>In sheer exuberance</em>; quotation marks; commas around <em>Jack</em>, the person spoken to; apostrophes in <em>We&rsquo;ve</em>.'),
     BYR('Chapter 17 opens with the partners in the pit they dug. Later comes the day Praiseworthy promised to fight the Mountain Ox. In your journal: Which do you think will matter more to the story, the gold or keeping that promise? Why? Write 2&ndash;3 sentences before reading.'),
     FOCUS('Chapter 17 is the joy chapter. It opens right where Chapter 16 ended. The partners stake a claim with Praiseworthy&rsquo;s tattered umbrella and work it day after day. Then comes the fifteenth of August, the day of the match with the Mountain Ox. Watch how Praiseworthy gets ready, and what he trusts to carry him through.'),
     ('where are aunt arabella and sarah and constance asked Jack. I believe said praiseworthy tugging at his white glove they are on there way here now.',
      'where is the mountain ox asked Jack. I believe said praiseworthy pushing back his hat the hangtown miners are on there way to watch.', 1),
     CARD('reprieve', 'A delay or cancellation of a punishment. From Old French <em>repris</em> (taken back). The Justice of Shirt-tail Camp gives Cut-Eye Higgins a temporary reprieve, until another tooth extractor shows up.'),
     CARD('counsel', 'A lawyer who speaks for someone in a trial; it also means advice. The Justice tells Praiseworthy, &ldquo;you appointed yourself counsel for the defense.&rdquo;'),
     CHK] + NEUTRAL_CARDS,
 3: QUOTE('&ldquo;Fine-looking country,&rdquo; Praiseworthy would say from time to time.', 'Chapter 18') + [
     SUBT('A fast boat, the Long Wharf, and the last chapter'),
     ('<text x="140" y="142" font-size="22" opacity=".75">💍</text>', '<text x="140" y="142" font-size="22" opacity=".75">⚓</text>', 1),
     ('<text x="625" y="136" text-anchor="middle" font-size="22">🚢 🐱 🤗 💍</text>', '<text x="625" y="136" text-anchor="middle" font-size="22">🚢 ⛵ ⚓ 🌊</text>', 1),
     OVB('The partners leave the diggings and head for San Francisco and a ship home to Boston. Chapter 18 is the last chapter, and it holds more than one surprise. As you read, ask what &ldquo;home&rdquo; means to Jack and Praiseworthy by the last page.'),
     OBJ('I will analyze how the last chapter brings plot, character, humor and theme together.'),
     DOLF('they were not the only miners aboard who were heading for home they met passengers who had abandoned the diggings in disgust as poor as when they had arrived some standing for months in the chill streams had picked up nothing but the rheumatism'),
     DOLA('They were not the only miners aboard who were heading for home. They met passengers who had abandoned the diggings in disgust, as poor as when they had arrived. Some, standing for months in the chill streams, had picked up nothing but the rheumatism.'),
     RSUB('The last chapter: a fast boat, the Long Wharf, and one more surprise'),
     FOCUS('Chapter 18 is the ending Fleischman has been building toward from the first page, and it does not go the way the partners planned. Watch for each surprise. For each one, ask what it does to the plot, what it shows about a character, whether it is funny, and what it says about the book&rsquo;s big idea.'),
     ('Looking at the full novel: Jack came to California a proper Boston boy, reluctantly following Praiseworthy. Praiseworthy came as a butler following his duty.',
      'Looking at the full novel: Jack made the plan to run away to the gold fields to help Aunt Arabella. Praiseworthy found him out and came along as his partner, still a butler.', 1),
     ('Fleischman argues that true valour comes not from physical strength', 'Fleischman argues that true corage comes not from physical strength', 1),
     CHK],
 4: [OVB('This is the last lesson of the unit. You have read 18 chapters, reviewed root families from five weeks, analyzed Fleischman&rsquo;s humor and voice, written and revised your own adventure, and built a literary response. Today you pull it all together, and celebrate.'),
     ('Cats auctioned for $400.', 'Cats auctioned for almost $400.', 1),
     ('Praiseworthy says: &ldquo;Out here, one man is as good as another.&rdquo; Jack replies: &ldquo;Only more so.&rdquo; Why is this exchange the perfect ending — in eight words?',
      'Near the end, Praiseworthy says, &ldquo;Out here, one man is as good as another.&rdquo; Jack answers, &ldquo;Only more so.&rdquo; What do these two lines say about how both characters changed in California? Use one moment from earlier in the book.', 1),
     ('placeholder="These eight words work as an ending because..."', 'placeholder="These two lines show that..."', 1),
     DOLM('&ldquo;Out here, <span class="dol-highlight-word" onclick="dolWord(this,\'Two speakers, two sets of quotation marks. The comma after <em>Out here</em> sets off the opener; the comma after <em>so</em> sits inside the closing quotation mark, before <em>said Jack</em>.\')">one man is as good as another.&rdquo; &ldquo;Only more so,&rdquo; said Jack.</span>'),
     DOLF('aunt arabella was smiling through a wet sparkle in her eyes marry you why of course i thought youd never ask'),
     DOLA('Aunt Arabella was smiling through a wet sparkle in her eyes. &ldquo;Marry you? Why, of course. I thought you&rsquo;d never ask.&rdquo;</p><p style=\'font-size:13px;color:#7A88A8;margin-top:6px;\'>Fixes: capitals for <em>Aunt Arabella</em>, <em>Marry</em>, <em>Why</em> and <em>I</em>; a period after <em>eyes</em>; quotation marks around everything she says; a question mark after <em>Marry you</em>; a comma after <em>Why</em>; an apostrophe in <em>you&rsquo;d</em>.'),
     ('and a full stop where two sentences had been run together.', 'and a period where two sentences had been run together.', 1),
     ('Four words that will appear in your final project. Now you know them.', 'Four words to know by sight. Now you know them.', 1)],
}
FLU_NEW = '''      &ldquo;Will you be returning to Boston?&rdquo; asked Praiseworthy.<br><br>
      &ldquo;Certainly not.&rdquo;<br><br>
      That changed everything and Praiseworthy crimped an eye, just like Pitch-pine Billy. Then he scratched through his whiskers. &ldquo;In that case &mdash;&rdquo; He stopped to gather up his courage. &ldquo;I mean &mdash;&rdquo;<br><br>
      &ldquo;Yes?&rdquo; said Aunt Arabella.<br><br>
      &ldquo;If I&rsquo;m no longer a butler &mdash; what I&rsquo;m trying to say is &mdash; well, in California we say a thing straight out.&rdquo;<br><br>
      Aunt Arabella smiled. &ldquo;Then do stop beating around the bush, Praiseworthy.&rdquo;<br><br>
      &ldquo;You see &mdash;&rdquo;<br><br>
      &ldquo;Yes?&rdquo;<br><br>
      &ldquo;I mean, women are scarce out here, Miss Arabella. Before you can walk a block you&rsquo;re going to have ten proposals of marriage.&rdquo;<br><br>
      &ldquo;How delightful.&rdquo;<br><br>
      &ldquo;What I mean to say is &mdash;&rdquo;<br><br>
      &ldquo;Yes?&rdquo;<br><br>
      He cleared his throat. &ldquo;Maybe this isn&rsquo;t the time or the place, Miss Arabella, but when a man strikes gold he doesn&rsquo;t lose any time staking a claim.&rdquo; With sudden decision, Praiseworthy whipped off his hat. His mouth was as dry as a cured salmon, but he kept talking. &ldquo;If there&rsquo;s going to be any proposals of marriage I intend to be the first in line. I&rsquo;ve got no vices to speak of, although I have taken to smoking strong cigars. To say it right out, Miss Arabella, will you do me the honor of becoming my wife?&rdquo;<br><br>
      Constance and Sarah began jumping up and down on their toes. &ldquo;Oh, do, Aunt Arabella! We know you gave him your picture &mdash; a long time ago.&rdquo;<br><br>
      &ldquo;He carries it in his shirt pocket!&rdquo; Jack exclaimed.<br><br>
      Aunt Arabella was smiling through a wet sparkle in her eyes. &ldquo;Marry you? Why, of course. I thought you&rsquo;d never ask.&rdquo;<br><br>
      &ldquo;By the Great Horn Spoon!&rdquo; Praiseworthy gasped.
'''
FIX['flu'] = [
  grp(r'<div class="passage-text">\n', r'.*?', r'    </div>\n    <div class="passage-source">', FLU_NEW),
  ('Praiseworthy proposes to Aunt Arabella on the Long Wharf in San Francisco. He has been building to this moment since Chapter 1.',
   'On the Long Wharf in San Francisco, Praiseworthy finally says what he has been trying to say. The passage starts with one question and keeps him stumbling until he gets it out.', 1),
  ('Let the movement feel natural: whip off the hat (action), dry mouth (interior), then the speech (dialogue), then the girls jumping (action), then Arabella&rsquo;s answer (dialogue), then his shock (one line).',
   'Let the movement feel natural: the short back-and-forth (&ldquo;Yes?&rdquo;), the hat whipped off (action), the dry mouth (inside his head), the speech, the girls jumping, Arabella&rsquo;s answer, then his shock (one line).', 1),
]
def main():
    apply = '--apply' in sys.argv; out = {}
    for k, reps in FIX.items():
        f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in reps:
            if isinstance(old, str):
                c = s.count(old)
                if c != n: sys.exit('%s: %d x %r' % (f, c, old[:90]))
                s = s.replace(old, new)
            else:
                s, c = old.subn(new, s, count=n)
                if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:80]))
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print('ok', f)
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
main()
