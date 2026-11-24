#!/usr/bin/env python3
"""Write data/g5ela-30-{1..4,fluency}.json (week 30, By the Great Horn Spoon! Ch. 16-18 + whole-book synthesis), Nov 24 2026.
Every book line checked against the By the Great Horn Spoon! text (project doc, Ch. 1-18).
History: California State Parks (Marshall Gold Discovery State Historic Park brochure; OHP landmarks 530 and 748: Marshall found gold
in the tailrace of Sutter's sawmill at Coloma on January 24, 1848; the valley of the Cul-luh-mah; the Coloma Road to Sutter's Fort;
about 1,000 people at Coloma by July 1848; the reconstructed mill); Henry Bigler's diary, January 24, 1848, as quoted on the park's
markers; PBS American Experience and the Library of Congress (Chinese gold-seekers, the queue, the 1852 foreign miners' tax);
Benjamin Madley, Journal of American History (2024) (Native Hawaiians in the Gold Rush). California had no state courts until 1850.
Bethany's choices: hook on 30.2 ('your real name'); virtue hope; Jack's Letter Home (proofreading; letters made up, only events already
read); Sutter's Mill card on 30.1 (the crowd trial in one calm line); 1963 notes on 30.2 and 30.3. Q4 audio paused: Listen texts are Mason
scripts, at or under 1,000 characters a lesson."""
import json, re, sys, html, io
LOOK = ("This letter is made up for the game, the way Jack writes letters home in Chapters 2 and 3. "
        "Every line has one misspelled word. Tap it, then tap the right spelling to ink the line clean. A clean letter gets a wax seal.")
HOW = {"do": ["Read the line of the letter.", "Tap the word that is spelled wrong.", "Tap the right spelling to ink it clean."],
       "why": "Proofreading means checking every word on purpose, the way an editor does before a piece is published."}
def l(text, opts, ok, why, miss=None):
    d = {"text": text, "opts": opts, "ok": ok, "why": why}
    if miss: d["miss"] = miss
    return d
def game(day, lines, greet="Dear Aunt Arabella, Constance and Sarah,", sign="Your devoted partner, Jack"):
    return {"type": "letter", "title": "Jack's Letter Home" if day < 4 else "Jack's Letter to the Diggings",
            "sub": "This week's word game · 6 lines today", "after": "Spelling", "look": LOOK, "how": HOW, "greet": greet, "sign": sign,
            "doneLine": "Come back tomorrow for the next letter." if day < 4 else "Four letters, twenty-four lines, every one clean.", "lines": lines}
WGRD = {"match": "What Good Readers Do", "do": ["Read the four lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Fixing one kind of mistake at a time catches more of them."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = lambda why: {"match": "Poetry Corner", "do": ["Read the poem out loud twice.", "Read the tip.", "Answer the question in your reading journal."], "why": why}
def rh(ch):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
            "why": "The pause boxes are places to stop and think while you read."}
WS = lambda day: {"match": "Writer", "do": {1: ["Read today's step.", "Write your three notes in the box.", "Don't write the ending yet."],
                                          2: ["Read today's step.", "Write your conclusion paragraph in the box.", "Use the frames if you get stuck."],
                                          3: ["Read the four checks for your conclusion.", "Check your whole story with the Final Publishing Checklist.", "Write the revised story, with its title, in the box."],
                                          4: ["Read your whole story out loud one last time.", "Put the final version in the box with its title.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "A strong ending ties together what happened, who your hero became and what the story means."}
MILL = {"tab": "reading", "after": "Read: Chapter 16", "title": "Real history: the real Sutter's Mill", "min": 3,
  "intro": "Old Cap Sutter's sawmill is real, and the miners' yarn in Chapter 16 is close to what really happened.",
  "items": [{"term": "January 24, 1848", "meaning": "James Marshall was building a sawmill for John Sutter at Coloma, on the South Fork of the American River. That morning he saw flakes of gold in the tailrace, the ditch that carries water away from the mill."},
            {"term": "A worker's diary", "meaning": "Henry Bigler, who worked at the mill, wrote that day: “This day some kind of mettle was found in the tailrace that looks like goald.” The spelling is his own."},
            {"term": "The news gets out", "meaning": "Marshall carried the gold down the Coloma Road to Sutter's Fort, where the city of Sacramento grew up later. The secret did not keep. By July 1848 about 1,000 people were digging around Coloma, and in 1849 the rush was on."},
            {"term": "Whose valley", "meaning": "The valley was Cullumah, a home of the Nisenan people. By 1848 many Nisenan had died of disease and conflict with settlers, and some worked for Sutter. The rush that started here took most of their land."},
            {"term": "Justice in the camps", "meaning": "In 1848 and 1849 California had no state courts yet. In some camps, crowds held quick trials of their own and hanged people with no lawyer and no judge, as the crowd in Chapter 16 means to do. Many of those trials were not fair. California's first state courts began in 1850."},
            {"term": "You can visit", "meaning": "The spot is now Marshall Gold Discovery State Historic Park. A copy of the sawmill stands near where the first one stood."}],
  "note": "Sources: California State Parks, Marshall Gold Discovery State Historic Park; California Historical Landmarks 530 and 748."}
NOTE_CHN = {"tab": "reading", "after": "Read: Chapter 17", "title": "A note before you read: words from 1963", "min": 2,
  "intro": "This book was written in 1963. Two spots near the end of Chapter 17 talk about Chinese people in an old, unkind way. Here is what to know.",
  "items": [{"term": "What the book says", "meaning": "When the partners leave their claim, Chinese miners “with pigtails” move in to work it. Later the Mountain Ox eats oysters at the “Chinese chow chow” and orders a cook named Ah Lee around. Pigtails was a mocking word outsiders used for the long braids Chinese men wore."},
            {"term": "The true history", "meaning": "Thousands of Chinese gold-seekers came to California in the early 1850s. Under China's rulers at the time, men had to wear their hair in one long braid called a queue, so cutting it off could keep a man from ever going home."},
            {"term": "Hard workers, unfair laws", "meaning": "Chinese miners often worked old claims carefully and found gold others had missed, and many ran restaurants, laundries and stores. In 1852 California passed a $3-a-month tax on foreign miners that was aimed at them."}],
  "note": "Sources: PBS American Experience; Library of Congress."}
NOTE_KAN = {"tab": "reading", "after": "Read: Chapter 18", "title": "A note before you read: words from 1963", "min": 1,
  "intro": "One line early in Chapter 18 needs a note.",
  "items": [{"term": "What the book says", "meaning": "On the riverboat, “Kanaka sailors” keep throwing wood into the furnace. Outsiders used Kanaka as a label for Native Hawaiians and other Pacific Islanders, often in an unkind way."},
            {"term": "The true history", "meaning": "Kānaka is the Hawaiian word for people. Hawaiian sailors worked on many ships in the Pacific long before the Gold Rush, and many Hawaiians came to California to sail, work and mine."}],
  "note": "Source: historian Benjamin Madley, Journal of American History (2024)."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "This is the last week of By the Great Horn Spoon. Answer the question on the card first. Then set your lens. This week you hold all four at once: what happens, who it happens to, what makes you smile, and what it all means."},
  "words": {"text": "This week you look back at every root family from the unit, and you practice editing: catching spelling slips and fixing one kind of mistake at a time. In the game, you proofread a letter from Jack."},
  "reading": {"text": "Read Chapter 16, The Gravediggers. The partners reach Shirt-tail Camp, and Praiseworthy has to speak up fast. Watch what he says and why it works. Then try the Read Like a Writer box."},
  "assignment": {"text": "Three questions about Chapter 16. Then plan the ending of your own adventure. Write three notes: what happens at the very end, who your hero has become, and what your story means."}},
 "how": [dict(WGRD, why="Good readers finish a book by holding all four parts of a story at once.", use="You will use it in reading question 1."), DOL, RW,
  {"match": "Morphology", "do": ["Read the five root families.", "Think through the questions, then tap See if you were right.", "Write about three roots from three different weeks in the box."], "why": "Roots you already know open up words you have never seen."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Watch for the words as you read."], "why": "Knowing the words first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the editing checklist.", "Fix the passage in your reading journal, then tap Now check your thinking.", "Tap a sentence, then tap the pass that would catch its mistake."], "why": "Checking for one kind of mistake at a time is how editors catch them all."},
  {"match": "Spelling", "do": ["Read the list of tricky words.", "Do the task in your reading journal.", "Tap a word, then tap Spelled correctly or Misspelled."], "why": "A few words cause most spelling mistakes. Learn those and your writing gets cleaner fast."},
  rh(16), WS(1)],
 "glossary": [{"word": "theme", "in": "What Good Readers Do", "meaning": "the big idea a story is about, like courage or what really matters"},
              {"word": "root", "in": "Morphology", "meaning": "the main part of a word that carries its meaning, often from Latin"}],
 "miss": {"recieve": "Not quite. It is i before e except after c: receive.", "occured": "occur + ed: the r doubles because you say oc-CUR. occurred.",
          "embarass": "Two r's and two s's: embarrass.", "definitely": "definite + ly. You can see finite inside it.",
          "separate": "There's a rat in separate: sep-a-rate.", "necessary": "One c, two s's: ne-ces-sa-ry."},
 "game": game(1, [l("Praiseworthy and I are [truely] well, though the fleas are not.", ["truley", "truly", "truely"], 1, "true drops its e before -ly: truly.", "true + ly: one letter of true drops."),
                  l("Our burro Stubb is a [valient] animal, when he wants to be.", ["valiant", "valient", "valliant"], 0, "val means strong. valiant: strong and brave, with -ant.", "Find the root val, then the ending -ant."),
                  l("I took the squirrel gun out alone, feeling a little [nervus].", ["nervus", "nerveous", "nervous"], 2, "nerve drops its e before -ous: nervous.", "nerve + ous: one letter of nerve drops."),
                  l("The man who pulled me out of a coyote hole was a retired road agent, which was a [suprise] to us both.", ["surprise", "suprise", "surprize"], 0, "sur + prise: say both r's.", "Say it slowly: sur-prise."),
                  l("Our pouch of gold dust is not very [valueable] yet.", ["valueable", "valuable", "valuble"], 1, "value drops its e before -able: valuable. Same val root as valiant.", "value + able: one letter of value drops."),
                  l("[Tommorow] we start for Shirt-tail Camp.", ["Tommorow", "Tomorow", "Tomorrow"], 2, "One m, two r's: to-mor-row.", "Count the m's and the r's.")]),
 "cards": [MILL],
 "virtue": {"name": "hope", "kind": "sort", "title": "Hope, or not?", "intro": "This week's virtue is hope: believing good things can still happen, and keeping at it when things look bad. Sort these everyday examples.",
   "items": [{"t": "Your team is losing at halftime. You tell yourself the game isn't over and keep playing your best.", "ok": True, "why": "Hope keeps you trying while there is still time."},
             {"t": "You don't try out for the play because you're sure you won't get a part.", "ok": False, "why": "Giving up before you start leaves no room for hope."},
             {"t": "Your science project falls apart the night before. You fix what you can and bring it anyway.", "ok": True, "why": "You expect something good can still come of it, so you keep going."},
             {"t": "You decide a hard book is too hard after one page, and you stop.", "ok": False, "why": "Hope means giving something a fair try first."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Answer the question on the card first. Then read a poem Edgar Allan Poe wrote in 1849, the year the Gold Rush began. Read it out loud twice. Listen for the word that keeps coming back."},
  "words": {"text": "Today you match words to their roots and hunt for misspelled words in a line. Then edit a passage, and name each kind of mistake you fix. Jack's next letter is waiting to be proofread."},
  "reading": {"text": "Read Chapter 17, The Fifteenth of August. Watch for things that pay off moments from early in the book, like a name, an umbrella, and a promise. Then try the Read Like a Writer box."},
  "assignment": {"text": "Three questions about Chapter 17. Then draft your conclusion paragraph from your three notes. Use the frames if you get stuck."}},
 "hook": {"q": "Someone who has always called you by a formal title suddenly calls you by your plain first name. What do you think it means?",
  "options": [{"t": "They're closer to me now, like a friend.", "reply": "That is what Jack feels. Listen:"},
              {"t": "They were just in a hurry.", "reply": "Maybe. But Jack notices it, and it matters to him. Listen:"},
              {"t": "They forgot their manners.", "reply": "Praiseworthy never forgets his manners. Listen:"}],
  "reveal": {"line": "Not Master Jack. Just Jack.", "cite": "Chapter 17",
             "then": "Read Chapter 17 to find out when it happens, and why it means so much."}},
 "how": [dict(WGRD, why="Payoffs show how carefully a book was built.", use="You will use it in reading question 1."), DOL, RW,
  POEM("Seeing how two parts of a poem work together shows what the poem means."),
  {"match": "Grammar", "do": ["Read the editing checklist.", "Fix every mistake in the passage and write it in the box.", "List the kind of each mistake after it."], "why": "This is your Show What You Know for grammar this week."},
  {"match": "Morphology", "do": ["Write every root you remember in your reading journal.", "Tap a word, then tap its root.", "Match all four."], "why": "Spotting a root inside a word tells you what the word is about."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Answer the question in your reading journal."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Fix the ten words in your reading journal.", "Tap every misspelled word in the line."], "why": "Finding mistakes in someone else's writing trains your eye for your own."},
  rh(17), WS(2)],
 "glossary": [{"word": "stanza", "in": "Poetry Corner", "meaning": "a group of lines in a poem, like a paragraph"},
              {"word": "bedight", "in": "Poetry Corner", "meaning": "an old word for dressed up or decorated"},
              {"word": "payoff", "in": "What Good Readers Do", "meaning": "a later moment that finishes something set up earlier"}],
 "game": game(2, [l("At Coloma we walked right past the [famus] sawmill.", ["famus", "famous", "famouse"], 1, "fame drops its e before -ous: famous.", "fame + ous: one letter of fame drops."),
                  l("At Shirt-tail Camp a crowd had [allready] decided Cut-Eye was guilty.", ["already", "allready", "alredy"], 0, "already has one l: al + ready.", "Find the word ready inside, with one l before it."),
                  l("Praiseworthy gave a speech so [persuasiv] that the crowd changed its mind.", ["perswasive", "persuasiv", "persuasive"], 2, "persuade: the d becomes s, then -ive. -ive always ends in e.", "The ending -ive always ends with e."),
                  l("He won the [arguement] without a single law book.", ["argument", "arguement", "argumint"], 0, "argue drops its e before -ment: argument.", "argue + ment: one letter of argue drops."),
                  l("We dug and dug, and [finaly] we hit bedrock, and the dirt shone with gold!", ["finaly", "finally", "finnaly"], 1, "final + ly: keep both l's. finally.", "final + ly: final ends in l, and -ly starts with l."),
                  l("My hands are so sore I can [barly] hold this pencil, but it is a good kind of sore.", ["barley", "barly", "barely"], 2, "bare keeps its e before -ly: barely. Barley is a grain.", "bare + ly: keep the whole word bare.")]),
 "cards": [NOTE_CHN],
 "virtue": {"name": "hope", "kind": "log", "options": [
   {"t": "On the morning of the fight, Jack wonders if Praiseworthy has changed his mind. Praiseworthy says, “Not on your life, Jack. We'll make it.”"},
   {"t": "Before the fight, Praiseworthy says, “And anyway, I intend to lick him.”"},
   {"t": "After Praiseworthy dodges the first punches, Jack watches “with a leap of hope.”"}],
   "line": "Tap the moment that shows the most hope. Then tell why in one sentence.", "placeholder": "This shows the most hope because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Answer the question on the card first. This is the last chapter of the book. As you read, watch for each surprise, and think about what it does to the story."},
  "words": {"text": "Today you fix the misspellings in two passages, build words from their roots, and match the last five vocabulary words. Then choose was or were. One more letter from Jack to proofread."},
  "reading": {"text": "Read Chapter 18, Arrival at the Long Wharf, the last chapter. Then reread the passage that surprised you most, and ask which part of the story it carries: plot, character, humor, or theme."},
  "assignment": {"text": "Three questions, the last one about the whole novel. Then put your new conclusion at the end of your story, and check it against the checklist."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read both passages.", "Fix every misspelled word and write both passages in the box.", "Put the right spelling in brackets after each fix."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Write your summary in your reading journal.", "Type the word that fits each sentence.", "Tap Check My Work."], "why": "Building a word from its root shows you really know the root."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Edit one paragraph of your story in your reading journal.", "Type was or were in each sentence.", "Tap Check My Work."], "why": "Using the checklist on your own writing is the whole point of learning it."},
  dict(WGRD, why="Rereading shows you the choices the author made.", use="You will use it in reading question 2."),
  rh(18), WS(3)],
 "glossary": [{"word": "brackets", "in": "Spelling", "meaning": "the marks [ and ] that set off a few words"},
              {"word": "agreement", "in": "Grammar", "meaning": "when a verb matches its subject, like one miner was and two miners were"}],
 "hints": {"fortitude": ["fort means strong. This word names a kind of strength.", "It ends in -itude.", "f, o, r, t, i, t, u, d, e"],
           "audible": ["aud means hear.", "It ends in -ible.", "a, u, d, i, b, l, e"],
           "extract": ["tract means pull. Add a prefix meaning out.", "It starts with ex.", "e, x, t, r, a, c, t"],
           "ridicule": ["rid means laugh.", "It ends in -icule.", "r, i, d, i, c, u, l, e"],
           "were": ["More than one, or one?", "This one is for more than one.", "w, e, r, e"],
           "was": ["More than one, or one?", "This one is for one.", "w, a, s"]},
 "game": game(3, [l("Gold dust is the only [currancy] anyone wants out here.", ["currency", "currancy", "curency"], 0, "curr means run: money that runs from hand to hand. Two r's, then -ency.", "Find the root curr, with two r's."),
                  l("Praiseworthy called me Jack, just plain Jack, and I could hardly [breath].", ["breeth", "breath", "breathe"], 2, "breathe (with an e) is the verb, what you do. breath is the noun.", "This word is something you do."),
                  l("On the fifteenth of [Augest] the whole town came to watch the fight.", ["August", "Augest", "Agust"], 0, "August: A-u-g-u-s-t, with a capital A.", "Say each part: Au-gust."),
                  l("Praiseworthy stayed calm and [couragous] the whole time.", ["couragous", "courageous", "curageous"], 1, "courage keeps its e before -ous, so the g stays soft.", "Keep the whole word courage, then add -ous."),
                  l("The Mountain Ox was [massiv], but Praiseworthy was quicker.", ["masive", "massiv", "massive"], 2, "mass + ive. -ive always ends in e.", "Keep both s's of mass."),
                  l("Now we have [enuf] gold to go home to Boston.", ["enough", "enuf", "enouf"], 0, "enough is spelled with ough, even though it sounds like uff.", "This word uses o, u, g, h.")]),
 "cards": [NOTE_KAN],
 "virtue": {"name": "hope", "kind": "meter", "title": "The hope meter", "intro": "Think about one moment from Chapter 18.",
   "moment": "The partners have just lost every bit of their gold in the bay. Jack says it is gone forever. Praiseworthy grins and says, “Mere bits of colored metal. We have our good health, damp as it may be at the moment.”",
   "ask": "How much hope does Praiseworthy show here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He shows this much hope because…",
   "take": "Mason's take: a great deal. He has just lost a fortune, and he looks at what he still has instead. A few minutes later Jack is the one with a plan: maybe they can work their passage home. Hope is catching."},
}
D[4] = {
 "readnow": {"text": "No new chapter today. Keep your book close so you can look back at the whole novel.", "step": "Look back at the novel"},
 "listen": {
  "warmup": {"text": "Read Eldorado again, slowly. On Day 2 you saw two parts of the poem work together. Today put all of them together and say what the poem means about searching for gold."},
  "words": {"text": "Explain a root in your own words, pick an option on the vocabulary choice board, and explain one editing rule. Then proofread Jack's last letter, to an old friend in the diggings."},
  "reading": {"text": "Look back over the whole novel: the voyage, the diggings, and the ending. Answer the pause questions and the three synthesis questions. Use moments from the beginning, the middle, and the end."},
  "assignment": {"text": "This is it. Read your whole story out loud one last time, ending and all. Put the final version in the box with its title. Then copy your work into Canvas."}},
 "how": [DOL, RW, POEM("Putting all the parts of a poem together is how you find what it means."),
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap the root inside each word."], "why": "Explaining a root shows you can use it on your own."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and write which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right answer in each question.", "Answer the question in your reading journal."], "why": "Explaining a rule shows you can use it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Type the right spelling of each word.", "Tap Check My Work."], "why": "Spelling right lets your reader think about your story, not your mistakes."},
  dict(WGRD, why="Synthesizing pulls the whole book together into one big idea.", use="You will use it in synthesis question 2."),
  {"match": "Unit Synthesis", "do": ["Read the six-week journey.", "Answer the two pause questions.", "Answer the three synthesis questions."], "why": "Looking back at the whole book shows how its parts fit together."},
  WS(4)],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "put ideas together into one big idea"},
              {"word": "pilgrim", "in": "Poetry Corner", "meaning": "a traveler on a long journey, often a search"}],
 "hints": {"receive": ["i before e, except after c.", "It has c, then e, i.", "r, e, c, e, i, v, e"], "occurred": ["occur + ed.", "Double the r before -ed.", "o, c, c, u, r, r, e, d"],
           "embarrass": ["Double letters, twice.", "Two r's and two s's.", "e, m, b, a, r, r, a, s, s"], "definitely": ["definite + ly.", "You can see finite inside it.", "d, e, f, i, n, i, t, e, l, y"]},
 "game": game(4, [l("You will never [gess] what happened in San Francisco Bay.", ["guess", "gess", "guesse"], 0, "guess has a silent u after the g.", "There is a silent letter after the g."),
                  l("The riverboat's boiler [exploaded], and our gold sank to the bottom.", ["exploded", "exploaded", "explodded"], 0, "explode drops its e before -ed: exploded.", "explode + ed: one e drops."),
                  l("Praiseworthy said it was only bits of [coloured] metal, and he meant it.", ["collored", "colored", "coloured"], 1, "American spelling is colored. Coloured is the British way.", "This is an American book. Use the American spelling."),
                  l("Every storekeeper in the [audiance] wanted a cat for a ratter.", ["audiense", "audiance", "audience"], 2, "aud means hear. audience: the people who hear, ending in -ence.", "Find the root aud, then the ending -ence."),
                  l("Aunt Arabella and my sisters [arived] on a ship the very same day!", ["arrived", "arived", "arrivved"], 0, "arrive has two r's.", "Count the r's."),
                  l("We are building a cabin, and you are [invitted].", ["invitted", "invited", "envited"], 1, "invite drops its e before -ed: invited. One t.", "invite + ed: one t, and one e drops.")],
              greet="Dear Pitch-pine Billy,", sign="Your friend, Jamoka Jack"),
 "virtue": {"name": "hope", "kind": "best", "title": "The most hopeful moment this week", "intro": "Look back at Chapters 16 to 18. Tap the moment you think shows hope the most.",
   "options": [{"t": "The whole trip looks like a wild-goose chase to Jack, but the partners keep digging on the hill (Chapter 16)."},
               {"t": "Praiseworthy on the morning of the fight: “Not on your life, Jack. We'll make it.” (Chapter 17)."},
               {"t": "After the gold sinks: “Mere bits of colored metal” (Chapter 18)."},
               {"t": "Jack, soaking wet and penniless: “Maybe he'll let us work our passage back” (Chapter 18)."}],
   "line": "Finish the sentence: This shows hope the most because…", "placeholder": "This shows hope the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the last scene of the book. Praiseworthy starts and stops, again and again, before he gets his question out. Let him stumble. Let Aunt Arabella stay calm and a little amused. Save your biggest voice for the very last line. When it sounds right, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
ART = {
 1: {"tab": "top", "file": "assets/art/btghs/hutton-sutters-mill.jpg", "title": "Sutter's Saw Mill",
     "alt": "A watercolor drawing of a valley with tall pine trees: the open-sided sawmill at the left beside its water race, and the tents and log cabins of miners on the right.",
     "look": "William Rich Hutton drew Sutter's sawmill at Coloma on April 16, 1849, a little more than a year after gold was found in its tailrace. Look for the mill at the left, the water race running past it, and the tents and cabins of the first miners. In Chapter 16 the partners walk right past it.",
     "lookBtn": "Tap to learn about this drawing", "creator": "William Rich Hutton", "date": "April 16, 1849",
     "license": "Public domain (Huntington Library, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Sutter%27s_Saw_Mill_-_16_April_1849_-_William_Rich_Hutton.jpg"},
 2: {"tab": "top", "file": "assets/art/btghs/bruff-mountain-camp.jpg", "title": "Mountain Camp in California",
     "alt": "A watercolor of two white canvas tents joined together under tall pine trees, with a man walking past carrying a gun.",
     "look": "Joseph Goldsborough Bruff led a wagon company to California in 1849 and painted his camp in the Sierra Nevada that year: canvas tents under tall pines. In Chapter 17 the partners camp on their own claim on a hill above the river.",
     "lookBtn": "Tap to learn about this painting", "creator": "Joseph Goldsborough Bruff", "date": "1849",
     "license": "Public domain (via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Bruff%27s_Mountain_Camp_in_California,_1849.jpg"},
 3: {"tab": "top", "file": "assets/art/btghs/marryat-high-and-dry.jpg", "title": "High and Dry",
     "alt": "A colored print of a San Francisco street: an old ship turned into a store with a STORESHIP sign, and another ship built into the front of the Niantic Hotel, with masts rising behind.",
     "look": "This print appeared in 1855 in Frank Marryat's book about his years in California. So many crews ran off to the diggings that old ships were left in the bay. Some were pulled up on the mud and made into stores and hotels. The ship on the right became part of the Niantic Hotel. In Chapter 18 the partners come back to San Francisco Bay.",
     "lookBtn": "Tap to learn about this print", "creator": "Frank Marryat", "date": "1855",
     "license": "Public domain (British Library, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:MARYATT(1855)_p060_HIGH_AND_DRY_(-_FORMER_SHIPS_IN_SAN_FRANCISCO).jpg"},
 4: {"tab": "top", "file": "assets/art/btghs/burgess-san-francisco-1850.jpg", "title": "View of San Francisco in 1850",
     "alt": "An oil painting of a young town of wooden buildings on sandy hills, with the bay and far hills behind and a few people and horses on a dirt road.",
     "look": "George Henry Burgess lived in San Francisco during the Gold Rush. In 1878 he painted the city as it looked in 1850, when it had grown from a small town almost overnight. This is the place where the novel begins and ends.",
     "lookBtn": "Tap to learn about this painting", "creator": "George Henry Burgess", "date": "painted 1878 (the city in 1850)",
     "license": "Public domain (Oakland Museum of California, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:%27View_of_San_Francisco_in_1850%27,_1878,_oil_on_canvas_painting_by_George_Henry_Burgess,_1878.jpg"},
}
for _k, _a in ART.items(): D[_k]["art"] = _a
FILES = {1: 'lesson-30-1-btghs-ch16.html', 2: 'lesson-30-2-btghs-ch17.html', 3: 'lesson-30-3-btghs-ch18.html', 4: 'lesson-30-4-btghs-synthesis.html'}
def page_words(f):
    s = io.open(f, encoding='utf-8').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s).lower()
    return set(re.findall(r"[a-z]+", s))
allw = set(); tot = {}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt); tot[k] = n
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s or '–' in s: sys.exit('%s: dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK', 'classmate', 'partner up', 'humour', 'colour', 'synthesise'):
        if bad in json.dumps({a: b for a, b in v.items() if a != 'game'}, ensure_ascii=False): sys.exit('%s: %s' % (k, bad))  # the game plants misspellings on purpose
    if 'game' in v:
        pw = page_words(FILES[k]); oks = [0, 0, 0]
        for L in v['game']['lines']:
            m = re.search(r'\[([^\]]+)\]', L['text'])
            if not m or len(L['opts']) != 3 or len(set(L['opts'])) != 3: sys.exit('%s: line shape %r' % (k, L['text']))
            if m.group(1) not in L['opts'] or m.group(1) == L['opts'][L['ok']]: sys.exit('%s: slip not a wrong option %r' % (k, L['text']))
            w = L['opts'][L['ok']].lower(); oks[L['ok']] += 1
            if w in allw: sys.exit('%s: answer %s used twice this week' % (k, w))
            allw.add(w)
            if w in pw: sys.exit("%s: answer %s is on that day's page" % (k, w))
        if min(oks) < 1: sys.exit('%s: right answers not spread %r' % (k, oks))
    json.dump(v, open('data/g5ela-30-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
