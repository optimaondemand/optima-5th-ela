#!/usr/bin/env python3
"""Write data/g5ela-32-{1..4,fluency}.json (week 32, Letter to a Future 5th Grader), Nov 25 2026.
Book lines checked against: hbg_ocr.txt Ch. 1; Bowditch OCR Ch. 12 and 22; Johnny Tremain text Ch. 8; By the Great Horn Spoon!
project doc Ch. 1 and 18; Witch OCR (Kit and Hannah). Real source: Louise Clappe ("Dame Shirley"), The Shirley Letters, Letter the
Twenty-third (Indian Bar, November 1852), text from the 1922 Thomas C. Russell edition on archive.org (shirleylettersfr00shir);
the letters first ran in The Pioneer, San Francisco, 1854-55. Lowell's "Wind and Silver" checked against What's O'Clock (1925),
p. 221, on Wikisource.
Bethany's choices: hook "Which book first?" on 32.1; virtue wisdom; The Year's Map (a journey/lighting game: five stops, one per
novel, each lit by a word from a root taught in that book's unit); "Letters that crossed time" card on 32.2; letter-and-reader
paintings. Q4 audio paused: Listen texts are Mason scripts, at or under 1,000 characters a lesson."""
import json, re, sys, html, io
STOPS = [{"name": "The Witch of Blackbird Pond", "place": "Wethersfield", "icon": "📜"}, {"name": "Johnny Tremain", "place": "Boston", "icon": "⚒️"},
         {"name": "Carry On, Mr. Bowditch", "place": "Salem", "icon": "🧭"}, {"name": "How I Became a Ghost", "place": "Mississippi", "icon": "🐕"},
         {"name": "By the Great Horn Spoon!", "place": "San Francisco", "icon": "⛏️"}]
UNIT_ROOTS = ['spect, script/scribe, struct, in-/im-', 'rupt, cede/ceed/cess, dict', 'nav/naut, port, graph, meter, scope, fract, fer, duct',
              'mem, anim, spir, path, sens/sent, vis/vid, luc/lum, photo, voc/voke', 'aud, or, rid/ris, lud/lus, curr/curs, tract, fort, val']
LOOK = "A map of your whole year: five stops, one for each novel's world, from Wethersfield to San Francisco. Each clue asks for a word built from a root you learned while you read that book. A right answer lights the stop."
HOW = {"do": ["Read the clue.", "Tap the word that fits.", "A right word lights the stop. Then tap On to the next stop."],
       "why": "Every root you learned this year still works. Here you use one from each book."}
_N = [0]
def rd(stop, clue, opts, ok, why, miss=None):
    """opts are written right answer first; rotate so the right answer moves through all three places"""
    right = opts[ok]; others = [o for o in opts if o != right]; pos = _N[0] % 3; _N[0] += 1
    opts = others[:pos] + [right] + others[pos:]
    return {"stop": stop, "clue": clue, "opts": opts, "ok": pos, "why": why, "miss": miss or "Look for the root in the clue's meaning."}
def game(day, rounds):
    return {"type": "yearmap", "title": "The Year's Map", "sub": "This week's word game · 5 stops today", "after": "Spelling", "look": LOOK, "how": HOW,
            "stops": STOPS, "doneLine": "Come back next lesson to light the map again with new words." if day < 4 else "Twenty stops lit this week. Five books, one year, and every root still works.",
            "rounds": rounds}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you work. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Read the first sentence. It is correct.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Fixing one sentence at a time trains your eye for your own letter."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on."], "why": "Thinking first gives you something to say in your letter."}
POEM = lambda why: {"match": "Poetry Corner", "do": ["Read the poem out loud three times.", "Read the tip.", "Answer the question in your reading journal."], "why": why}
def readnow(text, step): return {"text": text, "step": step}
SHIRLEY = {"tab": "reading", "after": "Your Passage: Read It Aloud", "title": "Real history: letters that crossed time", "min": 2,
  "intro": "Real letters can outlive the people who wrote them. Here is one from the Gold Rush.",
  "items": [{"term": "Who wrote it", "meaning": "Louise Clappe, who signed her letters “Dame Shirley.” In 1851 and 1852 she lived in two mining camps on the Feather River in California and wrote 23 letters to her sister Molly in Massachusetts."},
            {"term": "Her goodbye to the mining camp", "meaning": "She wrote this when she had to leave. Barbarous means rough and wild.",
             "line": "My heart is heavy at the thought of departing forever from this place. I like this wild and barbarous life. I leave it with regret.",
             "cite": "Letter the Twenty-third, Indian Bar, November 1852"},
            {"term": "Why we can still read it", "meaning": "Her letters were printed in The Pioneer, a San Francisco magazine, in 1854 and 1855, and in books ever since. A letter written for one reader reached readers for more than 170 years."}],
  "note": "Source: The Shirley Letters from California Mines in 1851-52, edited by Thomas C. Russell (1922), on the Internet Archive. Your letter is written for one new reader too."}
VPLAN = "This week's virtue is wisdom: knowing what matters and making good choices with what you know."
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "This is the last week of fifth grade reading. Start with the question on the card: a new reader can take only one of your five books. Which one do you hand them? Then set your lens for the week."},
  "words": {"text": "Word Study looks back at the whole year. You choose the root family that helped you most, sort sentences that are ready to publish, and check the spelling words that trip writers up. Then light the first stops on the year's map."},
  "reading": {"text": "No new chapter today. Write the opening of your letter: who you were as a reader in September, and who you are now. Then make five postcards, one for each novel. Copy every quote exactly from your book."},
  "assignment": {"text": "Plan your letter. Pick two novels and finish the claim: read this one before that one. Then give two reasons, each with a moment from both books, and one fair point for the other book."}},
 "hook": {"q": "A new 5th grader can read only one of your five books this summer. Which one do you hand them?",
  "options": [{"t": "A funny one, like By the Great Horn Spoon!", "reply": "Funny pulls a new reader in. One of your books starts with a warning instead:"},
              {"t": "A brave one, like Johnny Tremain or The Witch of Blackbird Pond.", "reply": "Courage is a good reason. One of your books starts with a warning:"},
              {"t": "The one that changed me most.", "reply": "That is the best reason of all, if you can show why. One of your books starts with a warning:"}],
  "reveal": {"line": "Be careful what you wish for", "cite": "How I Became a Ghost, Chapter 1",
             "then": "Isaac gives his reader advice on the very first page. This week you do the same for a new reader: your letter tells them which book to open first, and why."}},
 "readnow": readnow("No new chapter today. Look back over the year, then write your Reader’s Portrait and five Book Postcards.", "Today: look back"),
 "how": [dict(WGRD, why="A letter about books starts with remembering what stayed with you.", use="You will use it in your Reader’s Portrait."), DOL, RW,
  {"match": "Morphology", "do": ["Read the root families.", "Think through the questions, then tap See if you were right.", "Write about one root family in the box."], "why": "A root you know unlocks words you have never seen."},
  {"match": "Grammar", "do": ["Read each line.", "Tap it, then tap Ready or Needs an edit.", "Look at what the edits have in common."], "why": "Capitals, agreement and end marks are what a reader notices first."},
  {"match": "Speaking", "do": ["Read the three tools: voice, tone and pacing.", "Answer the question in your reading journal."], "why": "Your letter will be read aloud. How it sounds is part of what it says."},
  {"match": "Spelling", "do": ["Read the list.", "Do the task in your reading journal.", "Tap every word that is spelled correctly."], "why": "Your letter will go to a real reader. Clean spelling shows you care."},
  {"match": "Reader’s Portrait", "do": ["Read the plan for the week.", "Write your Reader’s Portrait in the first box.", "Fill in one postcard for each novel."], "why": "The portrait opens your letter. The postcards give you something to choose from."},
  {"match": "Letter Packet", "do": ["Read the three parts of the plan.", "Write your claim, two reasons and a fair point in the box."], "why": "A plan keeps both books in every reason."}],
 "glossary": [{"word": "pitch", "in": "Reader’s Portrait", "meaning": "a short line that makes someone want to try something"},
              {"word": "claim", "in": "Letter Packet", "meaning": "the main point you are trying to prove"}],
 "miss": {"seperate": "There's a rat in separate: sep-a-rate.", "embarass": "Two r's and two s's: em-bar-rass.", "diffrent": "Say all three beats: dif-fer-ent."},
 "game": game(1, [
   rd(0, "Which word means the act of building something, like a new house?", ["construction", "constitution", "consultation"], 0, "struct means build, so construction is the act of building."),
   rd(1, "Which word means a sudden bursting out, like a volcano?", ["eruption", "erosion", "emotion"], 0, "rupt means break or burst. An eruption bursts out."),
   rd(2, "Which word has the root that means ship or sailor?", ["nautical", "natural", "national"], 0, "naut means sailor or ship. Nautical means having to do with ships and sailing."),
   rd(3, "Which word names the act of breathing?", ["respiration", "reputation", "restoration"], 0, "spir means breathe. Respiration is breathing."),
   rd(4, "Which word names a try-out where judges listen to you?", ["audition", "addition", "edition"], 0, "aud means hear. At an audition, someone listens to you.")]),
 "virtue": {"name": "wisdom", "kind": "sort", "title": "Wise, or not?", "intro": VPLAN + " Sort these choices a letter writer might make.",
   "items": [{"t": "Before you give advice, you think about who will read it.", "ok": True, "why": "Wisdom starts with knowing your reader."},
             {"t": "You tell a new reader how a book ends so they don't have to read it.", "ok": False, "why": "That takes away the best part of reading: finding out."},
             {"t": "You admit a book was hard for you and say why it was worth it.", "ok": True, "why": "Honest advice is the most useful kind."},
             {"t": "You recommend a book you never finished because the cover looked good.", "ok": False, "why": "Advice should come from what you know, not what you guess."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Before you write, read the poem on the Poetry Corner card out loud three ways: flat, too fast, and the way you think it should sound. That last reading is the one you are practicing for."},
  "words": {"text": "Today the word work points at your own writing. You edit your Reader's Portrait, match four roots to their meanings, and hunt for misspellings. Then light five more stops on the year's map."},
  "reading": {"text": "Pick a short passage from one of your two novels, the one you will quote in your letter. Copy it exactly, mark where you will pause, and read it aloud three times. Then read the card about a real letter from the Gold Rush."},
  "assignment": {"text": "Draft your whole letter today. Start with Dear future fifth grader, then your Reader's Portrait, your claim, two reasons with a moment from each book, one fair point, and your closing."}},
 "readnow": readnow("No new chapter today. Pick a passage to read aloud, then draft your letter.", "Today: read aloud and draft"),
 "how": [dict(WGRD, why="Proof from both books is what makes a recommendation believable.", use="You will use it in your letter's two reasons."), DOL, RW,
  POEM("Reading a poem aloud shows what you understood: where it slows down and where it rushes."),
  {"match": "Grammar", "do": ["Read the checklist.", "Edit your Reader’s Portrait with it.", "Write the edited version in the box."], "why": "Your portrait opens your letter, so it should be your cleanest writing."},
  {"match": "Morphology", "do": ["Read each word.", "Tap the root and meaning that match it.", "Then do the journal task."], "why": "Matching a root to its meaning is how you read a word nobody taught you."},
  {"match": "Spelling", "do": ["Read the short draft.", "Find the misspelled words.", "Then check your own letter draft in your reading journal."], "why": "Finding mistakes in someone else's writing trains you to find them in yours."},
  {"match": "Your Passage", "do": ["Read Pick, Mark, Practice.", "Answer the three questions, one box at a time."], "why": "A quote you can read well is a quote a new reader will remember."},
  {"match": "Letter Packet", "do": ["Read how your letter goes, from greeting to closing.", "Draft your whole letter in the box."], "why": "Getting it all down first gives you something to revise."}],
 "glossary": [{"word": "claim", "in": "Letter Packet", "meaning": "the main point you are trying to prove"},
              {"word": "pause", "in": "Your Passage", "meaning": "a short stop while reading aloud"}],
 "cards": [SHIRLEY],
 "game": game(2, [
   rd(0, "Which word names old-fashioned glasses that help you see?", ["spectacles", "spatulas", "specials"], 0, "spect means look or see. Spectacles help you see."),
   rd(1, "Which word names something a person says will happen?", ["prediction", "production", "protection"], 0, "dict means say. A prediction is said before it happens."),
   rd(2, "Which word names the true story of a person's life, written by someone else?", ["biography", "biology", "bicycle"], 0, "graph means write and bio means life: a written life."),
   rd(3, "Which word means you cannot see it?", ["invisible", "invincible", "inedible"], 0, "vis means see, and in- means not."),
   rd(4, "Which word means to pull back, or take back words you said?", ["retract", "retreat", "retain"], 0, "tract means pull. To retract is to pull back.")]),
 "virtue": {"name": "wisdom", "kind": "log", "title": "Wisdom in the year's books", "intro": "Tap the moment from this year's novels that you think shows the most wisdom.",
   "options": [{"t": "Kit keeps visiting Hannah Tupper when the town turns against her (The Witch of Blackbird Pond)."},
               {"t": "Nat: “when you depend on a book and it has a mistake, you’d have been safer not depending on it” (Carry On, Mr. Bowditch, Chapter 22)."},
               {"t": "James Otis: “we fight, we die, for a simple thing. Only that a man can stand up” (Johnny Tremain, Chapter 8)."},
               {"t": "Isaac, on the very first page: “Be careful what you wish for” (How I Became a Ghost, Chapter 1)."}],
   "line": "In one sentence: would you pass this on in your letter? Why?", "placeholder": "I would pass it on because..."},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Today is revision day. Read your letter draft aloud, slowly, as if you were hearing it for the first time. Notice which sentence sounds most like you, and which one sounds like filler."},
  "words": {"text": "Today you check your letter's spelling, build four words from roots, and give your sentences the voice test. Then light five more stops on the year's map."},
  "reading": {"text": "Make three revisions: a vague sentence made specific, the honest thing you almost didn't say, and your best last sentence. Then pack two gifts for your reader, a Word Gift of three roots and a P.S."},
  "assignment": {"text": "Write your revised letter with your Word Gift and your P.S. at the end. Then read the whole thing aloud twice and time it. Two to three minutes is just right."}},
 "readnow": readnow("No new chapter today. Reread your passage, then revise your letter.", "Today: revise"),
 "how": [dict(WGRD, why="Noticing how an author wrote a passage helps you explain why it matters.", use="You will use it when you revise your letter."), DOL, RW,
  {"match": "Spelling", "do": ["Read the list.", "Check your letter draft for spelling.", "Write five words from the list in the box."], "why": "A clean letter shows a new reader you mean it."},
  {"match": "Morphology", "do": ["Write the journal sentence first.", "Type each word from its root.", "Tap Check My Work."], "why": "Building a word from its root proves you know the root."},
  {"match": "Grammar", "do": ["Read the voice test.", "Do the journal task.", "Type was or were in each blank, then tap Check My Work."], "why": "Was and were must match their subject, even in a long sentence."},
  {"match": "Revision", "do": ["Read the three revision moves.", "Answer the three questions, one box at a time."], "why": "Specific, honest sentences are what a reader remembers."},
  {"match": "Word Gift", "do": ["Write three roots, each with a word and a tip.", "Write your P.S. in the second box."], "why": "A Word Gift hands a new reader a tool they can use all year."},
  {"match": "Letter Packet", "do": ["Read the four checks.", "Write your revised letter in the box, with your Word Gift and P.S."], "why": "Putting every part together shows you what the reader will get."}],
 "glossary": [{"word": "vague", "in": "Revision", "meaning": "not clear or specific"}],
 "game": game(3, [
   rd(0, "Which word names a doctor's written order for medicine?", ["prescription", "protection", "perception"], 0, "script means write. A prescription is written by the doctor."),
   rd(1, "Which word names a line of people moving forward, like a parade?", ["procession", "profession", "possession"], 0, "cess means go. A procession goes forward."),
   rd(2, "Which word means able to be carried?", ["portable", "potable", "possible"], 0, "port means carry."),
   rd(3, "Which word means to light up?", ["illuminate", "eliminate", "imitate"], 0, "lum means light."),
   rd(4, "Which word means happening again and again?", ["recurring", "recovering", "referring"], 0, "curr means run. Something recurring keeps running back.")]),
 "virtue": {"name": "wisdom", "kind": "meter", "moment": "Captain Prince doubts that Nat can find their longitude with a lunar. Nat works the figures anyway, says they will sight land on the eighth, and they do (Carry On, Mr. Bowditch, Chapter 12).",
   "ask": "How wise was Nat?", "line": "In one sentence: why did you put the slider there?", "placeholder": "I put it there because...",
   "take": "I'd put it near the top. Nat didn't argue or brag. He did the work, checked it, and let the land prove him right."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "The last lesson of fifth grade reading. Choose any poem from this year for Poetry Corner and read it the way it asks to be read. That poem goes in your recording, right after your letter."},
  "words": {"text": "One last look at the year's words: six words you will keep, the word parts that do the work, and a final spelling and grammar check. Then light the last five stops on the year's map."},
  "reading": {"text": "Look back across the whole year. Which book surprised you, which character would you want beside you in sixth grade, and what one sentence about reading do you want to stay true?"},
  "assignment": {"text": "Seal and send. Write your envelope, paste your final letter, and record your letter and your poem in Canvas. Then put your booklet together. You finished fifth grade reading."}},
 "readnow": readnow("No new chapter today. Put the year together, then seal and send your letter.", "Today: seal and send"),
 "how": [dict(WGRD, why="Seeing one idea across many books is what a whole year of reading gives you.", use="You will use it in the Year-End Synthesis."), DOL, RW,
  POEM("Choosing how to read a poem aloud shows what you understand about it."),
  {"match": "Vocabulary", "do": ["Read the three word groups.", "Choose two words from each group.", "Define each word and use it in a sentence in the box."], "why": "Words you can use in a sentence are words you own."},
  {"match": "Morphology", "do": ["Write your advice in your reading journal.", "Tap the answer for each question."], "why": "Knowing what a word part does is how you read new words."},
  {"match": "Spelling", "do": ["Type the right spelling of each word.", "Tap Check My Work."], "why": "These are the words writers miss most."},
  {"match": "Grammar", "do": ["Read the checklist.", "Do the journal task.", "Tap the right answer for each question."], "why": "One last check, so your letter is ready to send."},
  {"match": "Year-End Synthesis", "do": ["Read the year in review.", "Answer the three questions, one box at a time."], "why": "Looking back is how you see how far you came."},
  {"match": "Letter Packet", "do": ["Read the three steps.", "Write your envelope in the first box.", "Paste your final letter in the second box."], "why": "A real letter gets a real envelope."}],
 "glossary": [{"word": "seal", "in": "Letter Packet", "meaning": "a blob of wax pressed shut with a stamp, used to close a letter"}],
 "game": game(4, [
   rd(0, "Which word means not possible?", ["impossible", "impressive", "important"], 0, "im- means not here: not possible."),
   rd(1, "Which word describes a business that has broken down because it ran out of money?", ["bankrupt", "banquet", "bandit"], 0, "rupt means break."),
   rd(2, "Which word names a tool that measures heat?", ["thermometer", "thermostat", "theater"], 0, "meter means measure, and therm means heat."),
   rd(3, "Which word means able to feel things strongly?", ["sensitive", "positive", "secretive"], 0, "sens means feel."),
   rd(4, "Which word means to lower what something is worth?", ["devalue", "deliver", "develop"], 0, "val means worth. De- means down.")]),
 "virtue": {"name": "wisdom", "kind": "best", "title": "The wisdom you will pass on", "intro": "Look back at this year's novels. Tap the piece of wisdom you would pass on to a new 5th grader.",
   "options": [{"t": "Isaac: “Be careful what you wish for” (How I Became a Ghost, Chapter 1)."},
               {"t": "Nat: “when you depend on a book and it has a mistake, you’d have been safer not depending on it” (Carry On, Mr. Bowditch, Chapter 22)."},
               {"t": "James Otis: “Only that a man can stand up” (Johnny Tremain, Chapter 8)."},
               {"t": "Jack to Praiseworthy: “We’re partners, sir” (By the Great Horn Spoon!, Chapter 1)."}],
   "line": "Finish the sentence: I would pass this on because…", "placeholder": "I would pass this on because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Your last fluency recording of fifth grade. Read your letter the way you want a new reader to hear it, pausing where you marked. Then read one poem from this year, whole, at the pace it asks for."}},
                "glossary": [{"word": "pace", "meaning": "how fast or slow you read"}]}
ART = {
 1: {"tab": "top", "file": "assets/art/year/homer-new-novel.jpg", "title": "The New Novel",
     "alt": "A watercolor of a young woman in an orange dress lying on her side in the grass, her head on a pillow, reading a book held close to her face.",
     "look": "Winslow Homer painted this reader in 1877. She is lying in the grass so deep in her book that she has forgotten everything around her. Who were you as a reader when this year began?",
     "lookBtn": "Tap to learn about this painting", "creator": "Winslow Homer", "date": "1877",
     "license": "Public domain (via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:1877-winslow-homer-the-new-novel.jpg"},
 2: {"tab": "top", "file": "assets/art/year/metsu-man-writing-letter.jpg", "title": "Man Writing a Letter",
     "alt": "A painting of a young man with long hair sitting at a table by a window, writing a letter with a quill pen. A patterned rug covers the table and a framed painting hangs on the wall.",
     "look": "Gabriël Metsu painted this man writing a letter in the Netherlands around 1665. Look at his face: he is choosing every word. Today you draft your own letter.",
     "lookBtn": "Tap to learn about this painting", "creator": "Gabriël Metsu", "date": "about 1665",
     "license": "Public domain (National Gallery of Ireland, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Man_Writing_a_Letter_by_Gabri%C3%ABl_Metsu.jpg"},
 3: {"tab": "top", "file": "assets/art/year/terborch-woman-writing-letter.jpg", "title": "Woman Writing a Letter",
     "alt": "A painting of a young woman in a pale yellow jacket seated at a small table, bent close over a sheet of paper, writing with a quill.",
     "look": "Gerard ter Borch painted this young woman around 1655. She leans close to the page and takes her time. Revising is like that: slow and careful.",
     "lookBtn": "Tap to learn about this painting", "creator": "Gerard ter Borch", "date": "about 1655",
     "license": "Public domain (Mauritshuis, The Hague, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Gerard_ter_Borch_-_Woman_Writing_a_Letter_-_797_-_Mauritshuis.jpg"},
 4: {"tab": "top", "file": "assets/art/year/vermeer-woman-reading-letter.jpg", "title": "Woman Reading a Letter",
     "alt": "A painting of a woman in a blue jacket standing by a table in soft window light, holding a letter with both hands and reading it. A large map hangs on the wall behind her.",
     "look": "Johannes Vermeer painted this woman reading a letter around 1663. She stands very still, holding it with both hands. Someday a new 5th grader will read your letter like this.",
     "lookBtn": "Tap to learn about this painting", "creator": "Johannes Vermeer", "date": "about 1663",
     "license": "Public domain (Rijksmuseum, Amsterdam, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Brieflezende_vrouw_Rijksmuseum_SK-C-251.jpeg"},
}
for _k, _a in ART.items(): D[_k]["art"] = _a
FILES = {1: 'lesson-32-1-portfolio-plan.html', 2: 'lesson-32-2-fluency-draft.html', 3: 'lesson-32-3-final-prep.html', 4: 'lesson-32-4-final-present.html'}
WK31 = {'verdict', 'dictionary', 'navigator', 'navy', 'fortress', 'comfort', 'vision', 'provisions', 'spectral', 'spectators', 'transport', 'import', 'current',
        'courier', 'extractor', 'distraction', 'scribble', 'scribe', 'audience', 'audible', 'chronometer', 'chronicle', 'valuable', 'evaluate', 'manuscript',
        'postscript', 'perspective', 'inspect', 'porter', 'export', 'incredible', 'credit'}
ROOTS = {0: ['struct', 'spect', 'script', 'im'], 1: ['rupt', 'cess', 'dict'], 2: ['naut', 'graph', 'port', 'meter'], 3: ['spir', 'vis', 'lum', 'sens'], 4: ['aud', 'tract', 'curr', 'val']}
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
            pw = page_words(FILES[k]); stops = [r['stop'] for r in v['game']['rounds']]
            if stops != [0, 1, 2, 3, 4]: sys.exit('%s: stops %r' % (k, stops))
            for r in v['game']['rounds']:
                w = r['opts'][r['ok']].lower()
                if w in allw or w in WK31: sys.exit('%s: %s used before' % (k, w))
                allw.add(w)
                if w in pw: sys.exit("%s: %s is on that day's page" % (k, w))
                if not any(x in w for x in ROOTS[r['stop']]): sys.exit('%s: %s has no root from its unit' % (k, w))
                if len(set(r['opts'])) != 3: sys.exit('%s: options' % k)
        json.dump(v, open('data/g5ela-32-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
