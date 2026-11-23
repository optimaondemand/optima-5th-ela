#!/usr/bin/env python3
"""Week 26 accuracy fixes (approved by Bethany Nov 23 2026; audit claude/g5-ela-wk26-audit.md).
Book lines checked against the By the Great Horn Spoon! text (project doc, Ch. 4-6). Every replacement asserts its
count; div balance must not change; nothing is written unless every file passes. Run once from the repo root."""
import io, sys
F = {1: 'lesson-26-1-btghs-ch4.html', 2: 'lesson-26-2-btghs-ch5.html', 3: 'lesson-26-3-btghs-ch6.html', 4: 'lesson-26-4-btghs-humor.html'}
FIN = '<input class="fillin-input" data-answer="%s" style="width:150px;padding:4px 8px;border:2px solid #C8D6EA;border-radius:6px;font-size:15px;">'
ROW = '<div style="margin:10px 0;font-size:16px;line-height:2;">%s</div>'
GAP_OLD_START = '<p style="margin:8px 0;color:#3A4A6B;"><strong>Word bank:</strong> <em>a comma &middot; a full stop &middot; a question mark</em></p>'
GAP_OLD_END = '<button onclick="g5Fill(this)"'
GAP_NEW = ('<p style="margin:8px 0;color:#3A4A6B;"><strong>Word bank:</strong> <em>a comma &middot; a period &middot; a question mark &middot; an exclamation point</em></p>'
  + ROW % ('&ldquo;I am holding still' + FIN % ',' + '&rdquo; said Jack.')
  + ROW % ('&ldquo;Is Aunt Arabella an old maid' + FIN % '?' + '&rdquo; Jack asked solemnly.')
  + ROW % ('&ldquo;I&rsquo;ll buy your potatoes' + FIN % '!' + '&rdquo; exclaimed Monsieur Gaunt.')
  + ROW % ('The butler dismissed the thought. &ldquo;Stuff and nonsense' + FIN % '.' + '&rdquo;'))
FIX = {
 1: [
  ('<div class="quote-strip-text">&ldquo;Don&rsquo;t pay any attention to Master Jack,&rdquo; said Praiseworthy quickly. &ldquo;The boy is light-headed from sheer hunger.&rdquo; &ldquo;Yes, I do,&rdquo; said Jack.</div>',
   '<div class="quote-strip-text">&ldquo;This cabin leaks shamefully,&rdquo; answered Praiseworthy. &ldquo;But it ain&rsquo;t raining.&rdquo; &ldquo;One can never be too careful in these latitudes,&rdquo; said the butler.</div>', 1),
  ('''<span class="dol-highlight-word" onclick="dolWord(this,'A dialogue tag (he shouted) tells HOW the character spoke. It begins lowercase even after dialogue — because it is part of the same sentence.')">he shouted</span>,
        <span class="dol-highlight-word" onclick="dolWord(this,'A new action — describing what he did while speaking — still belongs to the same beat. Comma, then the action.')">&ldquo;Pigs is for eatin&rsquo;, not for pets.&rdquo;</span>''',
   '''<span class="dol-highlight-word" onclick="dolWord(this,'The tag (he shouted) tells how the cook spoke. It starts with a lowercase letter because it belongs to the same sentence as the speech. A comma, then what he did while shouting, then a period ends the sentence.')">he shouted, waving the meat cleaver.</span>
        <span class="dol-highlight-word" onclick="dolWord(this,'A new sentence of speech gets new quotation marks and a capital letter. The apostrophe in eatin\\u2019 stands for the missing g.')">&ldquo;Pigs is for eatin&rsquo;, not for pets.&rdquo;</span>''', 1),
  ('rubbed its ever fattening side', 'rubbed his ever fattening side', 1),
  ('rubbed its ever-fattening side', 'rubbed his ever-fattening side', 1),
  ('Chapter 4 is <em>ludicrous</em> in the best possible way &mdash; 183 passengers searching every corner of a ship for one pig.',
   'Chapter 4 is <em>ludicrous</em> in the best possible way: a cook with a meat cleaver, gold-seekers hunting above and below decks, and a boy hiding a pig in the captain&rsquo;s own cabin.', 1),
  ('<p>These words appear in Chapters 4&ndash;6. Tap each card to reveal the definition.</p>',
   '<p>Four of these words come from Chapters 4&ndash;6. <em>Ludicrous</em> is this week&rsquo;s root word. Tap each card to see the meaning.</p>', 1),
  ('I wrote my DOL correction and RWM journal in my reading journal.', 'I wrote my DOL correction in my reading journal.', 1),
  ('Humour', 'Humor', 1), ('humour', 'humor', 3),
 ],
 2: [
  ("Stuff and nonsense Praiseworthy would say even though he believed every word of it. Do you really think we'll make it Jack asked. We may hit a bit of inclement weather Praiseworthy answered but our captain will manage.",
   "Stuff and nonsense Praiseworthy would say even though he believed every word of it. We may hit a bit of inclement weather gentlemen but our good captain will give the back of his hand to the Cape. Well said Mr. Azariah Jones I hope he doesn't try that.", 1),
  ('you really think we&rsquo;ll make it?&rdquo; Jack asked.</p>', None, 1),
  ('<em>bellowed</em>, <em>exclaimed</em>, and <em>commanded</em> all stress the <em>second</em> syllable. <em>Grumbled</em>, <em>muttered</em>, and <em>chuckled</em> stress the <em>first</em>. This pattern helps your spelling.',
   '<em>exclaimed</em> and <em>commanded</em> stress the <em>second</em> syllable. <em>Bellowed</em>, <em>grumbled</em>, <em>muttered</em>, <em>stammered</em> and <em>chuckled</em> stress the <em>first</em>. <em>Interrupted</em> stresses the <em>third</em>. Say each word aloud and listen for the loud beat.', 1),
  ('bel&bull;LOWED', 'BEL&bull;lowed', 1), ('in&bull;ter&bull;RUP&bull;ted', 'in&bull;ter&bull;RUPT&bull;ed', 1), ('com&bull;MAN&bull;ded', 'com&bull;MAND&bull;ed', 1),
  ('Jack exclaims it was &ldquo;the most exciting moment of his life.&rdquo;', 'The narrator says it seemed to Jack &ldquo;the most exciting moment of his life.&rdquo;', 1),
  ('during the storm at Cape Horn.', 'during the storms near the tip of South America.', 1),
  ('characterisation', 'characterization', 1),
 ],
 3: [
  ('Praiseworthy says in his private thoughts that he doesn&rsquo;t believe they will find gold. Yet he keeps encouraging Jack.',
   'In today&rsquo;s chapter, Praiseworthy privately doubts that they will find lumps of gold lying on the ground. Yet he tells Jack, &ldquo;There&rsquo;ll be enough for all.&rdquo;', 1),
  ('Over three chapters this week, Praiseworthy has hidden a pig, calmed terrified passengers through a deadly strait, and solved two men&rsquo;s business problems. He calls himself &ldquo;just a butler.&rdquo;',
   'Over three chapters this week, Praiseworthy has helped Jack hide a pig, stayed calm through thirty-seven days of storms, and solved two men&rsquo;s business problems. Back in Chapter 1 he told the captain, &ldquo;I am a butler, sir.&rdquo;', 1),
  ('Every mark is inside the quotation marks, where it belongs.', 'Every mark sits inside the quotation marks, where it belongs.', 1),
  ('humour', 'humor', 2), ('centre', 'center', 1),
 ],
 4: [
  ('''<span class="dol-highlight-word" onclick="dolWord(this,'A dialogue tag split around a speech: both parts of the tag are lowercase and set off by commas. The second speech restarts with a lowercase letter because the sentence continued.')">&ldquo;The lad here,&rdquo;</span>
        Captain Swain said with a twinkling glance,
        <span class="dol-highlight-word" onclick="dolWord(this,'Second half of a split tag: lowercase. The closing speech is part of the same interrupted sentence, so it does NOT capitalize the first word.')">&ldquo;has found me out.&rdquo;</span>''',
   '''<span class="dol-highlight-word" onclick="dolWord(this,'The comma goes inside the closing quotation mark, before the tag.')">&ldquo;I confess,&rdquo;</span>
        <span class="dol-highlight-word" onclick="dolWord(this,'The tag starts lowercase because it belongs to the same sentence. A period ends that sentence.')">chuckled the captain.</span>
        <span class="dol-highlight-word" onclick="dolWord(this,'The captain keeps talking, so the new sentence gets new quotation marks and a capital letter. No new paragraph: it is the same speaker.')">&ldquo;The lad here has found me out.&rdquo;</span>''', 1),
  ('<div class="dol-fix-sentence">I confess chuckled captain swain. The lad here has found me out then he pointed to the sea raven. Look at her gentlemen. Following us like a chick after a hen</div>',
   '<div class="dol-fix-sentence">then he pointed to the sea raven. look at her following us gentlemen like a chick after a hen</div>', 1),
  ('<p><strong>Corrected:</strong> &ldquo;I confess,&rdquo; chuckled Captain Swain. &ldquo;The lad here has found me out.&rdquo; Then he pointed to the Sea Raven. &ldquo;Look at her, gentlemen. Following us like a chick after a hen!&rdquo;</p>',
   '<p><strong>Corrected:</strong> Then he pointed to the <em>Sea Raven</em>. &ldquo;Look at her! Following us, gentlemen, like a chick after a hen!&rdquo;</p>', 1),
  ('Key fixes: quotes around all dialogue; comma inside &ldquo;confess,&rdquo;; capitalize <em>Captain Swain</em>; new speech = new quotes; capitalize <em>Sea Raven</em> (proper noun); new paragraph for the action beat; exclamation mark inside closing quote.',
   'Key fixes: capital <em>T</em> to start the sentence; capitalize the ship&rsquo;s name, <em>Sea Raven</em>; quotation marks around the captain&rsquo;s words; capital <em>L</em>; an exclamation point after <em>her</em>; commas around <em>gentlemen</em> (he is speaking to them); an exclamation point inside the closing quotation mark.', 1),
  ('&ldquo;We shall walk across Panama&rdquo; Praiseworthy said</div>', '&ldquo;I am holding still&rdquo; said Jack</div>', 1),
  ('&ldquo;We shall walk across Panama,&rdquo; Praiseworthy said.</div>', '&ldquo;I am holding still,&rdquo; said Jack.</div>', 1),
  ('and a full stop at the end.', 'and a period at the end.', 1),
  ('Explain both roots to a classmate</div>', 'Explain both roots in your own words</div>', 1),
  ('to a classmate who missed the week.', 'as if you were teaching someone who missed the week.', 1),
  ('A classmate says &ldquo;I never know where to put the comma when someone talks.&rdquo;', 'Imagine a younger student says, &ldquo;I never know where to put the comma when someone talks.&rdquo;', 1),
  ('Make it clear enough that your classmate could', 'Make it clear enough that the student could', 1),
  ('humour', 'humor', 4), ('ynthesise', 'ynthesize', 1),
 ],
}
def p2_answer(s):
    a = s.find('<div class="dol-answer" id="dolAns">'); b = s.find('</div>', a)
    seg = s[a:b]
    if 'our captain will manage' not in seg: sys.exit('26.2 answer seg')
    new = ('<div class="dol-answer" id="dolAns">\n        <p><strong>Corrected (one paragraph for each speaker):</strong></p>\n'
           '        <p>&ldquo;Stuff and nonsense,&rdquo; Praiseworthy would say, even though he believed every word of it. &ldquo;We may hit a bit of inclement weather, gentlemen, but our good captain will give the back of his hand to the Cape.&rdquo;</p>\n'
           '        <p>&ldquo;Well,&rdquo; said Mr. Azariah Jones, &ldquo;I hope he doesn&rsquo;t try that.&rdquo;</p>\n'
           '        <p style="font-size:13px;color:#7A88A8;margin-top:6px;">Praiseworthy keeps talking, so both of his speeches stay in one paragraph. Mr. Azariah Jones is a new speaker, so he gets a new paragraph. His speech is split by the tag, so <em>I</em> keeps going after a comma.</p>\n      ')
    return s[:a] + new + s[b:]
def run(apply):
    out = {}
    for k, f in F.items():
        s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in FIX[k]:
            c = s.count(old)
            if c != n: sys.exit('%s: %d x %r' % (f, c, old[:70]))
            if new is not None: s = s.replace(old, new)
        if k == 2: s = p2_answer(s)
        if k == 3:
            a = s.find(GAP_OLD_START); b = s.find(GAP_OLD_END, a)
            if a < 0 or b < 0 or s.count(GAP_OLD_START) != 1: sys.exit('gap')
            s = s[:a] + GAP_NEW + s[b:]
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print('ok', f, len(s0), '->', len(s))
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
if __name__ == '__main__': run('--apply' in sys.argv)
