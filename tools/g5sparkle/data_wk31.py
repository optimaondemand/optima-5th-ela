#!/usr/bin/env python3
"""Write data/g5ela-31-{1..4,fluency}.json (week 31, year-end synthesis: cross-text comparison), Nov 24 2026.
Book lines checked against: Witch OCR Ch. 14; Johnny Tremain text Ch. 8 and 12; Bowditch OCR Ch. 22; hbg_ocr.txt Ch. 1;
By the Great Horn Spoon! project doc (Ch. 1, 2, 4, 8, 13, 16, 17). Real people: Nathaniel Bowditch (1773-1838; The New American Practical
Navigator, 1802), Paul Revere (1735-1818), James Otis, Samuel Adams and Joseph Warren (all appear in Johnny Tremain), Pushmataha (about
1764-1824), James Marshall and John Sutter (gold at Sutter's sawmill, January 24, 1848).
Bethany's choices: hook on 31.1 (Kit and Jack on one ship); virtue wisdom; Two Books, One Root (memory game: two words with one root,
a thread between two worlds on a shelf); 'Who was real?' card on 31.2. Q4 audio paused: Listen texts are Mason scripts, at or under
1,000 characters a lesson."""
import json, re, sys, html, io
SHELF = [{"id": "witch", "name": "Witch"}, {"id": "jt", "name": "Johnny Tremain"}, {"id": "bow", "name": "Bowditch"},
         {"id": "ghost", "name": "Ghost"}, {"id": "hs", "name": "Horn Spoon"}, {"id": "you", "name": "You"}]
LOOK = 'Five novels and one more book on the shelf: You. Two words with the same root are a pair. Each pair you find ties two worlds together with a gold thread.'
HOW = {"do": ["Tap a card to turn it over.", "Tap a second card.", "Same root? The pair stays up. Different roots? They turn back over."],
       "why": "A root is the same in every book. Spotting it lets you read a word you have never seen."}
def pr(root, means, a, at, b, bt, why): return {"root": root, "means": means, "a": {"w": a, "at": at}, "b": {"w": b, "at": bt}, "why": why}
def game(day, pairs):
    return {"type": "pairs", "title": "Two Books, One Root", "sub": "This week's word game · 4 pairs today", "after": "Spelling", "look": LOOK, "how": HOW,
            "shelf": SHELF, "miss": "Look for the same few letters inside both words.",
            "doneLine": "Come back next lesson for four new pairs." if day < 4 else "Sixteen threads. Every book on the shelf is tied to another.", "pairs": pairs}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you work. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Fixing one kind of mistake at a time catches more of them."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on."], "why": "Thinking first gives you something to watch for."}
POEM = lambda why: {"match": "Poetry Corner", "do": ["Read the poem out loud three times.", "Read the tip.", "Answer the question in your reading journal."], "why": why}
def readnow(text, step): return {"text": text, "step": step}
WHO = {"tab": "reading", "after": "Read: Three Real Primary Sources", "title": "Real history: who was real?", "min": 2,
  "intro": "Every novel this year mixes made-up people with real ones. Here is who really lived.",
  "items": [{"term": "Made up", "meaning": "Kit Tyler, Johnny Tremain, Isaac, Jack Flagg and Praiseworthy are characters the authors invented."},
            {"term": "Nathaniel Bowditch (1773 to 1838)", "meaning": "Real. He grew up in Salem, taught himself mathematics and navigation, and in 1802 published The New American Practical Navigator, a book sailors used for more than a hundred years."},
            {"term": "Paul Revere, Samuel Adams, James Otis, Joseph Warren", "meaning": "Real. They were Boston patriots in the 1770s, and all of them appear in Johnny Tremain."},
            {"term": "Pushmataha (about 1764 to 1824)", "meaning": "Real. He was a Choctaw leader. In How I Became a Ghost he appears as a ghost who helps the children."},
            {"term": "James Marshall and John Sutter", "meaning": "Real. Marshall found gold at Sutter's sawmill on January 24, 1848, the find the miners tell about in Chapter 16 of By the Great Horn Spoon!"}],
  "note": "Sources: the novels themselves; National Park Service and California State Parks; you met Bowditch, Pushmataha and Sutter's Mill on earlier cards."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "This week you look back across all five novels. Answer the question on the card first: two heroes from two different books, stuck on the same ship. Then set your lens for the week."},
  "words": {"text": "This week is a year-long review. You look back at the roots you learned in every unit and at the words that trip writers up. In the game, find two words that share a root, and tie two books together."},
  "reading": {"text": "No new chapter today. Choose a theme, courage, independence or survival, and two novels that treat it differently. Then try the Read Like a Writer box. It shows you how to sort a comparison into categories."},
  "assignment": {"text": "Write your comparison claim: what both novels say about your theme, and how they say it differently. Then name two categories and one piece of evidence from each novel for each one."}},
 "hook": {"q": "Kit Tyler and Jack Flagg are stuck on the same ship in a storm. Who handles it better?",
  "options": [{"t": "Kit. She grew up sailing and loves the sea.", "reply": "Kit does love the sea. Listen to her in Chapter 14:"},
              {"t": "Jack. He'd grab a shovel and work.", "reply": "Jack would work, and he would not leave his partner. Listen to Kit first:"},
              {"t": "Both, in different ways.", "reply": "That is exactly the kind of answer a comparison essay is built on. Listen to Kit first:"}],
  "reveal": {"line": "How she would love to sail on the Dolphin again!", "cite": "The Witch of Blackbird Pond, Chapter 14",
             "then": "And Jack, in Chapter 1 of By the Great Horn Spoon!: “We’re partners, sir.” Same sea, two kinds of courage. That difference is what you write about this week."}},
 "readnow": readnow("No new chapter today. Choose your theme and your two novels, then plan by category.", "Today: plan your comparison"),
 "how": [dict(WGRD, why="Comparing two books starts with knowing what you are looking for in both.", use="You will use it in planning question 1."), DOL, RW,
  {"match": "Morphology", "do": ["Read the root families.", "Think through the questions, then tap See if you were right.", "Write about three words from three novels in the box."], "why": "A root you know in one book unlocks words in every book."},
  {"match": "Grammar", "do": ["Read the four comparison tools.", "Write one contrast and one similarity sentence in your reading journal.", "Sort the six sentences."], "why": "A comparison essay is built from sentences that hold two books at once."},
  {"match": "Spelling", "do": ["Read the list.", "Do the task in your reading journal.", "Tap a word, then tap the rule it depends on."], "why": "A few rules explain most of the words writers misspell."},
  {"match": "Cross-Text Comparison", "do": ["Read the three theme options.", "Pick one theme and two novels.", "Answer the three planning questions."], "why": "A good comparison starts with two books that disagree about something."},
  {"match": "Comparison Project", "do": ["Read the claim formula.", "Write your claim and your two categories in the box.", "Add one piece of evidence from each novel for each category."], "why": "Categories keep both books side by side, so your reader never has to remember one book for a whole page."}],
 "glossary": [{"word": "theme", "in": "Cross-Text Comparison", "meaning": "the big idea a story is about, like courage or survival"},
              {"word": "categories", "in": "Cross-Text Comparison", "meaning": "groups you sort ideas into, like how they arrive or what it costs"}],
 "miss": {"separate": "There's a rat in separate: sep-a-rate. The a is the schwa you cannot hear.", "definitely": "definite + ly. The i in fin is the vowel you cannot hear clearly.",
          "loneliness": "lonely + ness: the y changes to i. A suffix changed the base.", "curiosity": "curious + ity: the u drops out. A suffix changed the base.",
          "occurred": "occur + ed: the r doubles because you say oc-CUR.", "embarrass": "Two r's and two s's: em-bar-rass."},
 "game": game(1, [pr("dict", "say", "verdict", "hs", "dictionary", "you", "A verdict is what a jury says; a dictionary tells what words say."),
                  pr("nav", "ship", "navigator", "bow", "navy", "hs", "A navigator steers a ship; a navy is a country's fleet of ships, like the Navy frigates in San Francisco Bay."),
                  pr("fort", "strong", "fortress", "hs", "comfort", "witch", "A fortress is a strong place, like the one guarding Rio; comfort makes someone strong again, as Rachel tries to do for Mercy."),
                  pr("vis/vid", "see", "vision", "ghost", "provisions", "hs", "A vision is something seen, like the things Isaac sees before they happen; provisions are supplies you see to ahead of time.")]),
 "virtue": {"name": "wisdom", "kind": "sort", "title": "Wise, or not?", "intro": "This week's virtue is wisdom: knowing what matters and making good choices with what you know. Sort these everyday examples.",
   "items": [{"t": "Before you argue, you check the facts.", "ok": True, "why": "Wisdom looks at what is true before it decides."},
             {"t": "You copy a friend's answer because it sounds right.", "ok": False, "why": "Sounding right is not the same as being right."},
             {"t": "You ask someone who has done it before how they did it.", "ok": True, "why": "Wise people learn from others' experience."},
             {"t": "You make a big choice in a hurry so you don't have to think about it.", "ok": False, "why": "Wisdom takes time to think."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Read Carl Sandburg's poem Buffalo Dusk three times before you write anything. Notice which lines are short and which one is very long. This is a benchmark check: name every element you can find."},
  "words": {"text": "Write four comparison sentences today, then match words to their roots and hunt for misspellings. In the game, four new pairs of root words are waiting on the shelf."},
  "reading": {"text": "Today you read three real primary sources from this year: a worker's diary from Sutter's Mill, a reporter's San Francisco, and a Choctaw leader's letter. Choose the one that fits your essay. Then try the Read Like a Writer box."},
  "assignment": {"text": "Your essay has five paragraphs, organized by category. Today write paragraph one, your opening, and paragraph two, your first category, with both novels side by side."}},
 "readnow": readnow("No new chapter today. Read three real primary sources and choose one for your essay.", "Today: real sources"),
 "how": [dict(WGRD, why="Knowing who made a source, and when, tells you what it can prove.", use="You will use it in source question 2."), DOL, RW,
  POEM("Naming every element at work shows you how a poem is built."),
  {"match": "Grammar", "do": ["Read the grammar tools.", "Write the four sentences in the box.", "Label each one with the tool you used."], "why": "This is your Show What You Know for grammar this week."},
  {"match": "Morphology", "do": ["Find one root word in a source and write about it in your reading journal.", "Tap a word, then tap its root.", "Match all four."], "why": "Roots work the same way in a novel and in a real diary."},
  {"match": "Spelling", "do": ["Fix the eight words in your reading journal.", "Tap every misspelled word in the line."], "why": "Finding mistakes in someone else's writing trains your eye for your own."},
  {"match": "Read: Three Real Primary Sources", "do": ["Read the background card.", "Read sources A, B and C.", "Answer the three source questions."], "why": "A real voice from the time shows what one real person saw, which a novel cannot."},
  {"match": "Comparison Project", "do": ["Read the five-paragraph plan.", "Write paragraph 1 and paragraph 2 in the box.", "Use your claim and categories from Day 1."], "why": "Starting with the opening and one category gets the hardest part done."}],
 "glossary": [{"word": "primary source", "in": "Read: Three Real Primary Sources", "meaning": "something made at the time by someone who was there, like a diary or a letter"},
              {"word": "benchmark", "in": "Poetry Corner", "meaning": "a check that shows how far you have come"}],
 "cards": [WHO],
 "game": game(2, [pr("spect", "look", "spectral", "ghost", "spectators", "hs", "Spectral means ghostly, a shape you seem to see; spectators look on, like the crowd at the big fight."),
                  pr("port", "carry", "transport", "hs", "import", "bow", "Ships transport gold-seekers; Salem ships carried goods home to import them."),
                  pr("curr/cour", "run", "current", "bow", "courier", "jt", "A current is water that runs; a courier runs with messages, as Johnny rides for the patriots. The French spelling of the root is cour."),
                  pr("tract", "pull", "extractor", "hs", "distraction", "ghost", "A tooth extractor pulls teeth; a distraction pulls attention away, like Jumper in the river.")]),
 "virtue": {"name": "wisdom", "kind": "log", "title": "Wisdom in the year's books", "intro": "Tap the moment from this year's novels that you think shows the most wisdom.",
   "options": [{"t": "Praiseworthy talks a crowd out of a hanging with no trial (By the Great Horn Spoon!, Chapter 16)."},
               {"t": "Nat: “when you depend on a book and it has a mistake, you’d have been safer not depending on it” (Carry On, Mr. Bowditch, Chapter 22)."},
               {"t": "James Otis: “we fight, we die, for a simple thing. Only that a man can stand up” (Johnny Tremain, Chapter 8)."},
               {"t": "Isaac, on the very first page: “Be careful what you wish for” (How I Became a Ghost, Chapter 1)."}],
   "line": "In one sentence: why is this wise?", "placeholder": "This is wise because..."},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Today's sentence has a clause tucked inside two commas. Tap it to see why. Then write: what is the most interesting difference between your two novels?"},
  "words": {"text": "Edit two passages for spelling and mark every fix. Build words from their roots, then check your draft's sentence openers. Four new pairs are waiting in the game."},
  "reading": {"text": "Reread to test your claim against the books. Then finish your draft: your second category, your real-voice paragraph, and your closing. Read all five paragraphs out loud. The Read Like a Writer box helps you start the source paragraph."},
  "assignment": {"text": "Today is the revise day. Check your essay against the Revision Checklist, line by line. Fix what it finds, then paste the revised essay and write one change you made at the top."}},
 "readnow": readnow("No new chapter today. Finish your draft, then revise it with the checklist.", "Today: finish and revise"),
 "how": [dict(WGRD, why="Testing a claim against the books makes it stronger, or shows you where to change it.", use="You will use it in draft question 3."), DOL, RW,
  {"match": "Spelling", "do": ["Edit both passages in the box.", "Mark each fix in [brackets]."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Revise one sentence in your draft with a root word, in your reading journal.", "Type each word, then tap Check My Work."], "why": "A precise word is often a root word."},
  {"match": "Grammar", "do": ["Revise one sentence opener in your reading journal.", "Type the joining word in each sentence.", "Tap Check My Work."], "why": "Joining words hold the two sides of a comparison together."},
  {"match": "Writing Workshop", "do": ["Read the How to Write box.", "Write paragraphs 3 and 4 in the first box and your closing in the second.", "Read all five out loud, then answer question 3."], "why": "Finishing the draft first gives you something whole to revise."},
  {"match": "Comparison Project", "do": ["Read the Revision Checklist.", "Revise all five paragraphs.", "Paste the revised essay, with one change noted at the top."], "why": "A checklist catches what your eyes skip."}],
 "glossary": [{"word": "transition", "in": "Writing Workshop", "meaning": "a word or phrase that joins ideas, like however or in contrast"}],
 "hints": {"manuscript": ["Think of a book written before printing presses.", "manu (hand) + script (write).", "manu + script"],
           "sympathy": ["Feeling with someone.", "sym (with) + path (feeling) + y.", "sym + pathy"],
           "excursion": ["A short trip out.", "ex (out) + curs (run) + ion.", "ex + cursion"],
           "fortitude": ["Strength that holds when things are hard.", "fort (strong) + itude.", "fort + itude"],
           "Both": ["It shows two things are alike.", "It goes before the two names.", "B _ _ _"],
           "Whereas": ["It sets up a contrast at the start.", "It means while on the other hand.", "W _ _ _ _ _ _"],
           "Like": ["It shows a similarity, before a name.", "Four letters.", "L _ _ _"],
           "however": ["A contrast word set off by commas.", "It means but.", "h _ _ _ _ _ _"]},
 "game": game(3, [pr("scrib", "write", "scribble", "hs", "scribe", "you", "Jack's hair falls in a yellow scribble in Chapter 1; a scribe is someone who writes things down, like you this week."),
                  pr("aud", "hear", "audience", "jt", "audible", "you", "An audience hears a speech, like the Observers hearing James Otis; audible means loud enough to hear, like your read-aloud."),
                  pr("chron", "time", "chronometer", "bow", "chronicle", "you", "A chronometer keeps exact time at sea; a chronicle tells events in time order, like a year of reading."),
                  pr("val", "worth", "valuable", "hs", "evaluate", "you", "Valuable means worth a lot; to evaluate is to decide what something is worth, like the evidence in your essay.")]),
 "virtue": {"name": "wisdom", "kind": "meter", "moment": "Praiseworthy powders the black sow with coal dust, so the thief gives himself away by never touching her (By the Great Horn Spoon!, Chapter 2).",
   "ask": "How wise was Praiseworthy's plan?", "line": "In one sentence: why did you put the slider there?", "placeholder": "I put it there because...",
   "take": "I'd put it near the top. Praiseworthy knew a guilty man would be afraid of a squeal, so he planned for what the thief would do, not just what the pig would do."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "Read Buffalo Dusk again. On Day 2 you named its elements. Today explain how they work together. Ask yourself what the poem would lose if every line were the same length."},
  "words": {"text": "Choose five words from across the year and use them in sentences about your theme. Then check roots, spellings and your own sentence types. The last four pairs finish the shelf."},
  "reading": {"text": "Read your own essay as if someone else wrote it. Answer the three reviewer questions. Then argue the other side: what would a reader who disagrees say, and how would you answer?"},
  "assignment": {"text": "Pick two revision targets and make the changes. Paste your final essay, and note the two changes at the top. This is part one of your year-end portfolio."}},
 "readnow": readnow("No new chapter today. Review your essay as a reviewer, revise it twice, and submit.", "Today: review and submit"),
 "how": [dict(WGRD, why="Reading your own work as a stranger shows you what it really says.", use="You will use it in reviewer question 1."), DOL, RW,
  POEM("Explaining how the parts work together is the last step of reading a poem well."),
  {"match": "Vocabulary", "do": ["Read the word lists.", "Choose five words from at least three novels.", "Write about each one in the box."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap the right root for each word."], "why": "Roots let you read words you have never seen."},
  {"match": "Spelling", "do": ["Type the right spelling of each word.", "Tap Check My Work.", "Check your own essay the same way."], "why": "The words you misspell most are the ones to check first."},
  {"match": "Grammar", "do": ["Count your sentence types in your reading journal.", "Read the before and after.", "Tap the stronger sentence."], "why": "A comparison lives in sentences that connect two things."},
  {"match": "Reviewer", "do": ["Read your draft out loud.", "Answer the three reviewer questions.", "Argue the other side, then write what you learned this week."], "why": "Arguing the other side makes your own argument stronger."},
  {"match": "Comparison Project", "do": ["Pick two revision targets.", "Make the changes.", "Paste the final essay, with the two changes noted at the top."], "why": "Two careful changes beat ten quick ones."}],
 "glossary": [{"word": "reasoning", "in": "What Good Readers Do", "meaning": "the sentences that explain why your evidence proves your point"}],
 "hints": {"separate": ["There's a rat in it.", "sep-a-rate", "sep _ rate"], "definitely": ["You can see finite inside it.", "definite + ly", "defin _ tely"],
           "occurred": ["Say oc-CUR-red.", "occur + ed: the r doubles.", "occu _ _ ed"], "different": ["Say all three beats: dif-fer-ent.", "Two f's.", "diff _ rent"]},
 "game": game(4, [pr("script", "write", "manuscript", "bow", "postscript", "you", "Nat's book began as a manuscript; a postscript is the P.S. written after a letter, like the one you write next week."),
                  pr("spect", "look", "perspective", "ghost", "inspect", "you", "Perspective is where you look from, like Isaac's; to inspect is to look closely, like you at your draft today."),
                  pr("port", "carry", "porter", "hs", "export", "bow", "Bayard Taylor found that every man was his own porter in 1849 San Francisco; Salem ships carried goods out to export them."),
                  pr("cred", "believe", "incredible", "hs", "credit", "you", "Praiseworthy's win was hard to believe, incredible; giving credit to a source tells readers whom to believe.")]),
 "virtue": {"name": "wisdom", "kind": "best", "title": "The wisest character of the year", "intro": "Look back at this year's novels. Tap the character you think acted most wisely.",
   "options": [{"t": "Kit Tyler, who keeps visiting Hannah Tupper when the town turns against her (The Witch of Blackbird Pond)."},
               {"t": "Nat Bowditch, who checks every figure because sailors' lives depend on it (Carry On, Mr. Bowditch)."},
               {"t": "Praiseworthy, who keeps his word and comes back to fight the Mountain Ox (By the Great Horn Spoon!)."},
               {"t": "Isaac, who tells you on page one to be careful what you wish for (How I Became a Ghost)."}],
   "line": "Finish the sentence: This character was wise because…", "placeholder": "This character was wise because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Five passages, one from each novel. Open a few and read them under your breath. Pick the one you most want to perform. Then read it three times, smoothly, with expression, and with your best voice for the people in it."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
ART = {
 1: {"tab": "top", "file": "assets/art/year/connecticut-1766-map.jpg", "title": "Plan of the Colony of Connecticut",
     "alt": "An old hand-colored map of the Connecticut colony, with its towns and counties in soft colors and the Connecticut River running down the middle to Long Island Sound.",
     "look": "Moses Park made this map of the Connecticut colony in 1766, about eighty years after Kit Tyler's story. Find the Connecticut River running down the middle of the map. Wethersfield, where Kit lands, sits on its banks just south of Hartford.",
     "lookBtn": "Tap to learn about this map", "creator": "Moses Park", "date": "1766",
     "license": "Public domain (Library of Congress, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Plan_of_the_Colony_of_Connecticut,_Moses_Park,_1766.jpg"},
 2: {"tab": "top", "file": "assets/art/year/revere-boston-1768.jpg", "title": "A View of Part of the Town of Boston",
     "alt": "A hand-colored print of Boston seen from the harbor: church steeples and rooftops along the shore, a long wharf, and British warships with small boats carrying soldiers to land.",
     "look": "Paul Revere engraved this view of British warships landing soldiers at Boston in 1768. This copy was colored and printed again in 1898. Revere is a real person in Johnny Tremain, and this is the harbor and the Long Wharf Johnny knows.",
     "lookBtn": "Tap to learn about this print", "creator": "Paul Revere (color reproduction, 1898)", "date": "engraved 1770 (the landing of 1768)",
     "license": "Public domain (Boston Public Library via DPLA and Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:A_view_of_the_Town_of_Boston_in_New_England_and_British_ships_of_war_landing_their_troops,_1768_-_DPLA_-_4ed4e8f50042094f750ac013412bb26d.jpg"},
 3: {"tab": "top", "file": "assets/art/year/corne-mount-vernon-1799.jpg", "title": "The Ship Mount Vernon of Salem",
     "alt": "A painting of a large three-masted sailing ship with full sails on a calm gray sea, puffs of cannon smoke near its side, and other ships far behind.",
     "look": "Michele Felice Corné painted the Salem ship Mount Vernon in 1799, the year he sailed on her to America. Here she fights off French privateers near Gibraltar. Nat Bowditch sailed from Salem on trading ships like this in those same years.",
     "lookBtn": "Tap to learn about this painting", "creator": "Michele Felice Corné", "date": "1799",
     "license": "Public domain (Naval History and Heritage Command, NH 1697, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Mount_Vernon_(ship,_1798)_-_Michele_Felice_Corn%C3%A8_-_NH_1697.tiff"},
 4: {"tab": "top", "file": "assets/art/year/fragonard-young-girl-reading.jpg", "title": "Young Girl Reading",
     "alt": "A painting of a girl in a bright yellow dress sitting against a large pillow, holding a small open book in one hand and reading.",
     "look": "Jean-Honor\u00e9 Fragonard painted this girl lost in a book around 1769. Look at how still she sits and how close she holds the page. This week you have been the reader too, across five novels.",
     "lookBtn": "Tap to learn about this painting", "creator": "Jean-Honor\u00e9 Fragonard", "date": "about 1769",
     "license": "CC0 (National Gallery of Art, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Jean_Honor%C3%A9_Fragonard,_Young_Girl_Reading,_c._1769,_NGA_46303.jpg"},
}
for _k, _a in ART.items(): D[_k]["art"] = _a
FILES = {1: 'lesson-31-1-comparison-plan.html', 2: 'lesson-31-2-comparison-sources.html', 3: 'lesson-31-3-comparison-draft.html', 4: 'lesson-31-4-comparison-submit.html'}
def page_words(f):
    s = io.open(f, encoding='utf-8').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s).lower()
    return set(re.findall(r"[a-z]+", s))
if __name__ == '__main__':
    allw = set()
    for k, v in D.items():
        txt = [c['text'] for c in v['listen'].values()]
        n = sum(len(t) for t in txt)
        if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
        s = json.dumps(v, ensure_ascii=False)
        if '—' in s or '–' in s: sys.exit('%s: dash' % k)
        for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK', 'classmate', 'partner up', 'humour', 'colour', 'synthesise', 'tomorrow', 'Tomorrow'):
            if bad in s: sys.exit('%s: %s' % (k, bad))
        if 'game' in v:
            pw = page_words(FILES[k]); shelf = {x['id'] for x in SHELF}
            for p in v['game']['pairs']:
                for side in ('a', 'b'):
                    w = p[side]['w'].lower()
                    if p[side]['at'] not in shelf: sys.exit('%s: shelf %s' % (k, p[side]['at']))
                    if w in allw: sys.exit('%s: %s used twice this week' % (k, w))
                    allw.add(w)
                    if w in pw: sys.exit("%s: %s is on that day's page" % (k, w))
                    if not re.search(p['root'].split('/')[0][:3], w) and not re.search(p['root'].split('/')[-1][:3], w): sys.exit('%s: %s lacks %s' % (k, w, p['root']))
                if p['a']['at'] == p['b']['at']: sys.exit('%s: pair in one world %r' % (k, p['root']))
        json.dump(v, open('data/g5ela-31-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
