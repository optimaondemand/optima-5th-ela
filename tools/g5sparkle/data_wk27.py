#!/usr/bin/env python3
"""Write data/g5ela-27-{1..4,fluency}.json (week 27, By the Great Horn Spoon! Ch. 7-9 + Taylor source day), Nov 23 2026.
Every book line checked against the By the Great Horn Spoon! text (project doc, Ch. 7-9).
History: National Park Service, San Francisco Maritime NHP ("Niantic: Buried Gold Rush Ship"; "Buried Ships of San Francisco";
"Maritime Shorts": crews left ships, hulls used as stores, warehouses, hotels, even jails; Niantic in the bay July 5 1849, crew gone
by July 11, hauled ashore, burned May 2 1851, Niantic Hotel 1851-1872, stern saved 1978 and shown in the Maritime Museum).
Oakland Museum of California, "Gold Rush!" (Maidu, Nisenan, Miwok homelands in the foothills; salmon runs ruined; forced labor).
Population estimate 150,000 (1848) to 30,000 (1870): A. L. Kroeber, Handbook of the Indians of California (1925); B. Madley (2016).
Qing law required Chinese men to wear the queue; California's Foreign Miners' Tax began in 1850 (and again in 1852).
Bethany's choices: hook "$38 in a dollar-a-bucket city" (27.2), Race to the Golden Gate (no answer word is on that day's page),
wow = the ships left in the harbor + the real Niantic (27.2), virtue generosity, brisk and light, Arrival plates, hard-history notes.
Q4 audio is paused: the Listen texts are Mason scripts, written to stay at or under 1,000 characters a lesson."""
import json, sys
LOOK = ("The Lady Wilma has no coal. Each right answer throws a plank of lumber in her furnace, and she surges toward the Golden Gate. "
        "A miss lets the Sea Raven creep up.")
HOW = {"do": ["Read the clue.", "Tap the word that really fits.", "Watch the Lady Wilma surge ahead.", "Tap Full steam."],
       "why": "The base word tells you -tion or -sion, and a real root tells you the meaning."}
def r(clue, opts, ok, why, miss=None):
    d = {"clue": clue, "opts": opts, "ok": ok, "why": why}
    if miss: d["miss"] = miss
    return d
def game(day, rounds):
    return {"type": "race", "title": "Race to the Golden Gate", "sub": "This week's word game · 8 planks today", "after": "Spelling",
            "look": LOOK, "how": HOW,
            "doneLine": "Come back tomorrow for eight more planks." if day < 4 else "Four days, thirty-two planks. The Lady Wilma wins the race.", "rounds": rounds}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted parts of the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Joining ideas the right way keeps action moving and shows cause and effect."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Read the tip.", "Answer the question in your reading journal."],
        "why": "A poem's beat and line length control how fast you read, just like a writer's sentences."}
def rh(ch):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
            "why": "The pause boxes are places to stop and think while you read."}
WS = lambda day: {"match": "Writer", "do": {1: ["Read today's step.", "Answer the three questions in a few words each. That is your plan.", "Start writing the middle of your adventure."],
                                          2: ["Read today's step.", "Keep writing your middle.", "Use the frames if you get stuck."],
                                          3: ["Read the checklist.", "Check your middle one item at a time.", "Fix anything that is missing."],
                                          4: ["Read your middle once more.", "Put the whole middle section in the box.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "The middle is where the stakes rise. Each fix should lead to a new problem."}
NOTE_CN = {"tab": "reading", "after": "Read: Chapter 8", "title": "A note before you read: words from 1963", "min": 2,
  "intro": "This book was written in 1963. A few lines in Chapter 8 describe people in ways that are unkind and untrue. Here is what to know.",
  "items": [{"term": "How the book describes Chinese people", "meaning": "Chapter 8 calls the Chinese people on the wharf silent and calls their braids pigtails, and it writes the laundryman's English as broken speech. Many books from that time made Chinese people into a joke this way. It is unfair to real people."},
            {"term": "The true history", "meaning": "Chinese immigrants began arriving in California in 1849 and soon numbered in the thousands. Many men wore a long braid called a queue, because the rulers of China required it. Chinese workers ran laundries, cooked, mined and later helped build the railroad, and they faced unfair laws, such as special taxes on foreign miners that began in 1850."},
            {"term": "A phrase to notice", "meaning": "Quartz Jackson thanks Praiseworthy by saying it is mighty white of him. It is an old saying that treats being white as the same as being good. It is a racist phrase, and we do not use it."}],
  "note": "When you meet these lines, notice them. The book shows what many people believed then, not what is true."}
NOTE_NA = {"tab": "reading", "after": "Read: Chapter 9", "title": "A note before you read: words from 1963", "min": 2,
  "intro": "On the riverboat in Chapter 9, Jack sees Native Californians for the first time. The book's words about them are unkind and untrue. Here is what to know.",
  "items": [{"term": "What the book says", "meaning": "Jack worries the people on the riverbank are savages who might take scalps. The steward calls them Digger Indians and says they are quite tame. These words were insults. Digger mocked people for gathering roots and acorns, and tame talks about people as if they were animals."},
            {"term": "The true history", "meaning": "The Sacramento Valley and the foothills were the homelands of Native peoples such as the Nisenan, Miwok and Maidu. Gathering and preparing acorns was a skilled tradition that fed families for generations. The Gold Rush brought terrible harm: miners took their land and ruined their rivers, and many people were killed or forced to work. Historians estimate that California's Native population fell from about 150,000 in 1848 to about 30,000 by 1870."},
            {"term": "Still here", "meaning": "California's Native nations are still here today, and many keep their languages and traditions alive."}],
  "note": "Sources: Oakland Museum of California; population estimate from A. L. Kroeber (1925) and historian Benjamin Madley (2016)."}
WOW = {"tab": "reading", "after": "Read: Chapter 8", "title": "Real history: the ships left in the harbor", "min": 2,
  "intro": "The Lady Wilma and the Sea Raven are made up. The crowded harbor in Chapter 8 was real.",
  "items": [{"term": "Crews ran off to the gold fields", "meaning": "In 1849 ship after ship sailed into San Francisco Bay, and many crews left for the gold fields as soon as they landed. Hundreds of empty ships sat in the cove. Some were pulled up onto the mud and used as stores, warehouses, hotels and even a jail."},
            {"term": "The real Niantic", "meaning": "In Chapter 8 a hotel runner shouts, Try the Niantic Hotel. The Niantic was a real ship. It sailed into the bay on July 5, 1849, and within a week its crew was gone. It was hauled ashore and used as a store and warehouse. After a fire in 1851, the Niantic Hotel was built on top of what was left of it, so Fleischman borrowed the hotel's name two years early."},
            {"term": "Found under the city", "meaning": "The town filled in the shallow cove with sand, and old ships ended up blocks from the water, under new streets. Workers dug up a large part of the Niantic in 1978, and a piece of its stern is in San Francisco's maritime museum today."}],
  "note": "Source: National Park Service, San Francisco Maritime National Historical Park."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "The race is nearly over. The Lady Wilma reaches Callao, in Peru, and trouble is waiting. Before you read, think of a time a problem turned out to help you. Then set your lens: watch how each fix leads to the next problem."},
  "words": {"text": "This week's roots are curr and curs, which mean run, and tract, which means pull. The spelling pattern is the shun sound at the end of a word. Look at the base word to choose t-i-o-n or s-i-o-n. In the game, every right answer throws a plank in the furnace."},
  "reading": {"text": "Read Chapter 7, End of the Race. Watch the coal. Who has it, who loses it, and what does that cause? Then watch who reminds the captain about the lumber, and listen to how he says it."},
  "assignment": {"text": "Three questions about Chapter 7. Then plan the middle of your adventure. Answer the three questions in a few words each. That is your plan. Then start writing."}},
 "how": [DOL, RW, dict(WGRD, why="Adventure stories run on problems. Each solution causes the next problem.", use="You will use it in reading question 1."),
  {"match": "Morphology", "do": ["Read what curr/curs and tract mean.", "Read the example words.", "Type the missing root in each word, then tap Check Roots."], "why": "Two roots unlock many words about running and pulling."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Notice which chapter each word comes from."], "why": "Knowing the words first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the two kinds of sentences.", "Think through the questions, then tap Now check your thinking.", "Tap a sentence, then tap the column that fits it."], "why": "Compound sentences show two things at once; complex ones show cause and effect."},
  {"match": "Spelling", "do": ["Read how -tion and -sion turn a verb into a noun.", "Read the word families.", "Tap a word, then tap the column for its ending."], "why": "The base word tells you which ending to use."},
  rh(7), WS(1)],
 "glossary": [{"word": "momentum", "in": "Grammar", "meaning": "the push that keeps something moving forward"},
              {"word": "consequences", "in": "What Good Readers Do", "meaning": "what happens because of something else"}],
 "hints": {"tract": ["This word is about pulling.", "It is the pull root.", "t, r, a, c, t"], "curs": ["This word is about running before.", "The run root that ends in s.", "c, u, r, s"],
           "curr": ["This word is about something that happens, as if it ran into you.", "The run root with two r's.", "c, u, r, r"]},
 "miss": {"decision": "decide ends in de, so it takes -sion: decision.", "division": "divide ends in de, so it takes -sion: division.", "collision": "collide ends in de, so it takes -sion: collision.",
          "attraction": "attract ends in ct, so it takes -tion.", "direction": "direct ends in ct, so it takes -tion.", "celebration": "celebrate ends in te, so it takes -tion."},
 "game": game(1, [r("The boilers roar. Which spelling names the act of exploding?", ["explosion", "explotion", "explodsion"], 0, "explode ends in de, so it takes -sion: explosion."),
                  r("Money that runs from hand to hand in San Francisco's shops. Which word has curr (run)?", ["currency", "curtain", "cargo"], 0, "curr (run) + ency: money that runs from person to person. A curtain only looks like it has the root."),
                  r("Writing where the letters run together, like Jack's letter home.", ["cursive", "curious", "curly"], 0, "curs (run) + ive: letters that run together."),
                  r("Captain Swain checks every inch of his ship. Which spelling names the act of inspecting?", ["inspecsion", "inspection", "inspectsion"], 1, "inspect ends in ct, so it takes -tion.", "Look at the end of the base word: inspect."),
                  r("Taking one number away from another, as Praiseworthy counts their money.", ["subtraction", "satisfaction", "substation"], 0, "sub (away) + tract (pull) + ion: pulling one number away from another."),
                  r("Which word is in the same family as protect?", ["protection", "protest", "profession"], 0, "protect, protection and protective all share the base protect."),
                  r("A builder who signs a deal to put up a hotel in San Francisco.", ["contractor", "conductor", "container"], 0, "con (together) + tract (pull) + or: someone who draws a deal together."),
                  r("A sudden run into someone else's land.", ["incursion", "insertion", "inspection"], 0, "in (into) + curs (run) + ion: a running in.")]),
 "virtue": {"name": "generosity", "kind": "sort", "title": "Generosity or not?", "intro": "This week's virtue is generosity: giving your time, help or things freely, without asking for anything back. Sort these everyday examples.",
   "items": [{"t": "You share your snack with someone who forgot their lunch.", "ok": True, "why": "You give what you have to someone who needs it."},
             {"t": "You help your neighbor carry groceries, then ask for a dollar.", "ok": False, "why": "Helping is kind, but asking to be paid makes it a deal, not a gift."},
             {"t": "You let your little sister have the bigger piece of cake.", "ok": True, "why": "You give up something you wanted so someone else can have it."},
             {"t": "You give away a toy only because it is broken.", "ok": False, "why": "Giving away what you do not want costs you nothing. Generosity gives something that matters."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Jack and Praiseworthy step off the boat into San Francisco, and everything costs too much. Before you read, answer the question on the card. Then read a galloping poem out loud and listen for the hoofbeats."},
  "words": {"text": "Write four sentences that join ideas with and, but, because, although or when. Find the run and pull roots hiding in new words. Then listen for the loud beat in the shun words. Eight more planks for the furnace today."},
  "reading": {"text": "Read Chapter 8, Saved by a Whisker. Watch the prices. Then watch a shaggy stranger, and one small choice that changes everything for Jack and Praiseworthy."},
  "assignment": {"text": "Three questions about Chapter 8. Then keep drafting your middle. If you get stuck, use the frames: first, then, finally."}},
 "hook": {"q": "You land in a city where one bucket of water costs a dollar. You have $38, and the riverboat to the gold fields costs $50 for two. What do you do first?",
  "options": [{"t": "Find a job right away.", "reply": "Smart thinking. Praiseworthy starts by counting what they have:"},
              {"t": "Walk to the gold fields and save the money.", "reply": "It is more than a hundred miles. Praiseworthy starts by counting what they have:"},
              {"t": "Look for a chance nobody else has noticed.", "reply": "That is exactly Praiseworthy's style. He starts by counting what they have:"}],
  "reveal": {"line": "Let me see. We have thirty-eight dollars left. That's a start, isn't it?", "cite": "Chapter 8",
             "then": "Read Chapter 8 to find out how a strange favor turns into the start they need."}},
 "how": [DOL, POEM, RW, dict(WGRD, why="Cause and effect is the engine of an adventure.", use="You will use it in reading question 3."),
  {"match": "Grammar", "do": ["Read the two kinds of sentences.", "Write your four sentences in the box.", "Label each one."], "why": "This is your Show What You Know for grammar this week."},
  {"match": "Morphology", "do": ["Read each meaning.", "Type the missing root.", "Tap Check."], "why": "Spotting a root in a new word gives you a head start on its meaning."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Answer the question in your reading journal."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Say each word and find the loud beat.", "Read the word families from Chapter 8.", "Tap every -tion and -sion word in the sentences."], "why": "The loud beat usually comes right before the ending."},
  rh(8), WS(2)],
 "glossary": [{"word": "meter", "in": "Poetry Corner", "meaning": "the regular beat under the words of a poem"},
              {"word": "postern", "in": "Poetry Corner", "meaning": "a small back gate in a town wall"}],
 "hints": {"curr": ["This word is about running.", "The run root with two r's.", "c, u, r, r"], "tract": ["This word is about pulling.", "The pull root.", "t, r, a, c, t"]},
 "game": game(2, [r("Jack wants to see everything. Which spelling names the act of exploring?", ["exploration", "explorasion", "exploretion"], 0, "explore + ation: exploration."),
                  r("Something that happens. Which spelling is right?", ["occurrence", "ocurrence", "occurence"], 0, "oc + curr (run) + ence: two c's and two r's.", "Count the c's and the r's."),
                  r("A machine that pulls gold out of rock.", ["extractor", "extractar", "exstractor"], 0, "ex (out) + tract (pull) + or."),
                  r("Which spelling names the act of persuading someone?", ["persuasion", "persuation", "persuadtion"], 0, "persuade ends in de, so it takes -sion."),
                  r("Which word carries tract (pull) and means to pull praise away from something?", ["detract", "detect", "decrease"], 0, "de (away) + tract (pull)."),
                  r("Which word is in the same family as collect?", ["collector", "college", "collar"], 0, "collect, collection and collector share the base collect."),
                  r("Something that runs before, like the hilltop signal that tells the town a ship is coming in Chapter 8.", ["precursor", "precaution", "predictor"], 0, "pre (before) + curs (run) + or: a forerunner."),
                  r("Which spelling names the act of preparing?", ["preparation", "prepasion", "preparetion"], 0, "prepare + ation: preparation.")]),
 "cards": [WOW, NOTE_CN],
 "virtue": {"name": "generosity", "kind": "log", "options": [
   {"t": "Praiseworthy will not take money for the haircut: “Consider it a modest wedding present.”"},
   {"t": "Quartz Jackson gives Jack every grain of gold dust panned from his whiskers."},
   {"t": "Quartz Jackson says the least he can do is teach them how to work a gold pan."}],
   "line": "Tap the moment that shows the most generosity. Then tell why in one sentence.", "placeholder": "This shows the most generosity because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "On to Sacramento City, then up toward the mountains. Before you read, think of a story where a villain you thought was gone comes back. What makes that moment so scary?"},
  "words": {"text": "Today you spell all eight shun words and build word families. Match each word to its parts. Then join sentence halves with but, so, because and although. Eight more planks."},
  "reading": {"text": "Read Chapter 9. Reread one problem from start to finish: the moment it starts, every try, and the result. Then notice how Fleischman slows down the very last moment."},
  "assignment": {"text": "Three questions, the last one about all three chapters. Then revise your middle with the checklist. End it on a question, not an answer."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read the eight words.", "Write the words and your four sentences in the box.", "Add one word family at the end."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap a word, then tap its parts and meaning.", "Match all four."], "why": "Taking a word apart shows how the root builds its meaning."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Write your four sentences in your reading journal.", "Type the joining word that fits each gap.", "Tap Check My Work."], "why": "The joining word shows how two ideas connect."},
  dict(WGRD, why="Rereading one problem shows how the author built it, step by step.", use="You will use it in reading question 2."),
  rh(9), WS(3)],
 "glossary": [{"word": "cliffhanger", "in": "Read: Chapter 9", "meaning": "an ending that stops at an exciting moment, so you have to keep reading"},
              {"word": "suspense", "in": "Read: Chapter 9", "meaning": "the nervous, excited feeling of waiting to find out what happens"}],
 "hints": {"but": ["The second half goes against the first.", "A short joining word for a surprise.", "b, u, t"], "so": ["The second half is a result.", "A two-letter joining word.", "s, o"],
           "Because": ["The first half gives a reason.", "A joining word that starts a reason.", "B, e, c, a, u, s, e"], "Although": ["The first half is true, but something else happens anyway.", "A joining word for a contrast.", "A, l, t, h, o, u, g, h"]},
 "game": game(3, [r("Which spelling names the act of inventing?", ["invension", "invention", "inventsion"], 1, "invent ends in t, so it takes -tion.", "Look at the last letter of invent."),
                  r("Money that runs from hand to hand. Which spelling is right?", ["currency", "curency", "currancy"], 0, "curr (run) + ency: two r's."),
                  r("Pleasing to look at, as if it pulls your eyes toward it.", ["attractive", "attentive", "active"], 0, "at (toward) + tract (pull) + ive."),
                  r("Which spelling names the act of growing larger?", ["expansion", "expantion", "expandsion"], 0, "expand ends in d, so it takes -sion."),
                  r("Which word is in the same family as explode?", ["explosive", "explore", "exploit"], 0, "explode, explosion and explosive share the base explode."),
                  r("To run into a cost or a problem. Here the root is spelled with one r.", ["incur", "incurr", "encur"], 0, "in (into) + cur (run): one r at the end."),
                  r("To pull something out longer than it should last, like a long wait at the dock.", ["protract", "protect", "protest"], 0, "pro (forward) + tract (pull)."),
                  r("Chapter 9 is full of suspense. Which spelling names the act of hanging something up?", ["suspension", "suspention", "suspendsion"], 0, "suspend ends in d, so it takes -sion.")]),
 "cards": [NOTE_NA],
 "virtue": {"name": "generosity", "kind": "meter", "title": "The generosity meter", "intro": "Think about one moment from Chapter 9.",
   "moment": "On the riverboat, Jack polishes his new horn spoon. Praiseworthy had let him buy it on the wharf with a pinch of gold dust, even though money is tight.",
   "ask": "How generous is Praiseworthy here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He is this generous because…",
   "take": "Mason's take: quite generous. It is a small gift, but Praiseworthy is careful with every grain. Spending a pinch on Jack's horn spoon shows he cares how Jack feels, not just about the money."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "Today a real person tells you about San Francisco in 1849. First, a poem that moves like a train. Read it fast, and notice the short lines."},
  "words": {"text": "Explain the roots and the shun rule in your own words. Pick an option on the choice board for your five words. The last eight planks take the Lady Wilma through the Golden Gate."},
  "reading": {"text": "Read the words of Bayard Taylor, a real reporter who landed in San Francisco in August 1849. Find what surprised him. Then compare his first day to Jack's."},
  "assignment": {"text": "Three questions about Taylor and the novel. Then read your middle once more and submit it. Copy your work and paste it into Canvas."}},
 "how": [DOL, POEM, RW,
  {"match": "Morphology", "do": ["Explain the two roots in your reading journal.", "Type the word that fits each sentence.", "Tap Check My Work."], "why": "Explaining a root shows you really know it."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and say which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right explanation in each question.", "Answer the question in your reading journal."], "why": "Explaining a choice shows you can make it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Tap the right spelling in each pair."], "why": "The base word decides the ending."},
  {"match": "Read: A Reporter Lands", "do": ["Read who Bayard Taylor was.", "Read his words slowly. Tap any dotted word.", "Answer the three questions, then do the Read Like a Writer box and the Virtue Watch."],
   "why": "A real eyewitness shows what the novel's San Francisco was based on."},
  dict(WGRD, why="Putting a real account beside a novel shows what each one does best.", use="You will use it in question 3."),
  WS(4)],
 "glossary": [{"word": "bewilderment", "in": "Read: A Reporter Lands", "meaning": "the feeling of being completely confused"},
              {"word": "porters", "in": "Read: A Reporter Lands", "meaning": "people paid to carry bags and trunks"},
              {"word": "speculation", "in": "Read: A Reporter Lands", "meaning": "buying something in hope of selling it later for more"}],
 "hints": {"excursion": ["A short trip out.", "ex + the run root + ion.", "ex + curs + ion"], "extract": ["To pull something out.", "ex + the pull root.", "ex + tract"],
           "current": ["Water that keeps running.", "The run root + ent.", "curr + ent"], "traction": ["The grip that keeps a wheel pulling.", "The pull root + ion.", "tract + ion"]},
 "game": game(4, [r("Captain Swain takes back an angry promise. Which spelling names the act of pulling back?", ["retraction", "retracsion", "retracktion"], 0, "re (back) + tract (pull) + ion. The base ends in ct, so -tion."),
                  r("Which spelling names the slow wearing away of a riverbank?", ["erosion", "erotion", "erodsion"], 0, "erode ends in de, so it takes -sion."),
                  r("Letters that run together.", ["cursive", "curious", "curfew"], 0, "curs (run) + ive."),
                  r("Which word is in the same family as decide?", ["decisive", "deceive", "decimal"], 0, "decide, decision and decisive share the base decide."),
                  r("Which spelling names the act of steering a ship?", ["navigation", "navigasion", "navigatsion"], 0, "navigate ends in te, so it takes -tion."),
                  r("To take one number away from another.", ["subtract", "subject", "suburb"], 0, "sub (away) + tract (pull)."),
                  r("Which spelling names the act of understanding?", ["comprehension", "comprehention", "comprehendtion"], 0, "comprehend ends in d, so it takes -sion."),
                  r("Money that runs from hand to hand.", ["currency", "curfew", "courage"], 0, "curr (run) + ency.")]),
 "virtue": {"name": "generosity", "kind": "best", "title": "The most generous moment this week", "intro": "Look back at Chapters 7 to 9. Tap the moment you think shows generosity the most.",
   "options": [{"t": "In Callao, Mr. Azariah Jones and Monsieur Gaunt each buy them a pick, a shovel and a washpan (Chapter 7)."},
               {"t": "Praiseworthy cuts Quartz Jackson's hair as a wedding present and takes no money (Chapter 8)."},
               {"t": "Quartz Jackson gives them all the gold dust from his whiskers (Chapter 8)."}],
   "line": "Finish the sentence: This shows generosity the most because…", "placeholder": "This shows generosity the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the haircut scene from Chapter 8 out loud. Snip by snip, keep it smooth. Make Quartz Jackson truly amazed when he sees himself. Let the last question land with a smile. When it sounds right, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
ART = {
 1: {"tab": "top", "file": "assets/art/btghs/steamship-europa-1849.jpg", "title": "Royal Mail Steam Ship Europa",
  "alt": "A black-and-white print of a long steamship with three masts, sails furled, a tall smokestack and a big paddlewheel on its side, moving through choppy waves.",
  "look": "A lithograph printed in 1849, the year of the novel. The Europa was a real sidewheel steamship that crossed the Atlantic, not the Pacific. Look at the big paddlewheel on her side, the smokestack and the masts for sails. The made-up Lady Wilma and Sea Raven are the same kind of ship: when the coal runs out, there is nothing to turn the wheel.",
  "lookBtn": "Tap to learn about this print", "creator": "Lithograph, publisher unknown (Library of Congress)", "date": "1849",
  "license": "Public domain (Library of Congress, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Royal_mail_steam_ship,_Europe_LCCN2001704214.jpg"},
 2: {"tab": "top", "file": "assets/art/btghs/burgess-san-francisco-1849.jpg", "title": "San Francisco in July, 1849",
  "alt": "A painting of a small town of white houses and tents spreading down hills to a bay crowded with ships' masts, with riders and miners camping in the front.",
  "look": "George Henry Burgess was in San Francisco during the Gold Rush. He painted this view in 1891 from his memories and sketches of July 1849, the same summer Jack and Praiseworthy land. Look at the forest of masts in the bay, the tents on the hillside, and how new and scattered the town still looks.",
  "lookBtn": "Tap to learn about this painting", "creator": "George Henry Burgess", "date": "1891 (showing July 1849)",
  "license": "Public domain (Oakland Museum of California, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:San_Francisco_in_July_1849_Painting_by_George_Henry_Burgess.jpg"},
 3: {"tab": "top", "file": "assets/art/btghs/sacramento-city-1849.jpg", "title": "Sacramento City, from the foot of J Street",
  "alt": "A tinted print of a river landing crowded with sailing ships and a paddle steamer, a wide street running back through tall trees, and mountains far in the distance.",
  "look": "A lithograph made from a drawing of 1849. This is the river landing at Sacramento City, with ships and a paddle steamer tied up along the bank and J Street running back through the trees. Far behind, the Sierra Nevada shows on the skyline, the mountains Jack keeps gazing at in Chapter 9.",
  "lookBtn": "Tap to learn about this print", "creator": "Charles Parsons, after George V. Cooper", "date": "1849 to 1850",
  "license": "Public domain (Library of Congress, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Sacramento_City_from_the_foot_of_J_Street_(LOC_pga.04015,_cropped).jpg"},
 4: {"tab": "top", "file": "assets/art/btghs/nahl-miners-in-the-sierras.jpg", "title": "Miners in the Sierras",
  "alt": "A painting of four miners in a rocky stream bed, shoveling dirt into a long wooden trough, with steep hills, pine trees and a small cabin behind them.",
  "look": "Charles Nahl and Frederick Wenderoth painted this in 1851 and 1852, soon after the first rush. Four miners work a long wooden trough in a rocky stream, washing dirt to catch the heavy gold. It is the kind of place Jack and Praiseworthy are heading for, and the kind of hard work Bayard Taylor saw too.",
  "lookBtn": "Tap to learn about this painting", "creator": "Charles Christian Nahl and Frederick August Wenderoth", "date": "1851 to 1852",
  "license": "Public domain (Smithsonian American Art Museum, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Smithsonian-Nahl_and_Wenderoth-Miners_in_the_Sierras-2099_(cropped).jpg"},
}
for _k, _a in ART.items(): D[_k]["art"] = _a
EIGHT = {'extraction', 'distraction', 'construction', 'excursion', 'attraction', 'direction', 'confusion', 'tension'}
PAGE = {1: EIGHT | {'decision', 'collision', 'celebration', 'division', 'current', 'occur', 'occurrence', 'curriculum', 'precursor', 'tractor', 'attract', 'distract', 'extract', 'contract', 'retract', 'invasion', 'invader', 'decisive', 'attractive', 'director'},
        2: EIGHT | {'concurrent', 'subtract', 'recurrent', 'abstract', 'decision', 'discussion', 'objection', 'expedition', 'ruination', 'conversation'},
        3: EIGHT | {'current', 'extract', 'traction', 'decisive'},
        4: EIGHT | {'extract', 'current', 'traction', 'decision', 'expression'}}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s or '–' in s: sys.exit('%s: dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK', 'classmate', 'partner up'):
        if bad in s: sys.exit('%s: %s' % (k, bad))
    if 'game' in v:
        seen = set()
        for e in v['game']['rounds']:
            w = e['opts'][e['ok']]
            if w in PAGE[k]: sys.exit('%s: game word %s is on that day\'s page' % (k, w))
            if len(e['opts']) != 3 or e['ok'] not in (0, 1, 2): sys.exit('opts?')
            if w in seen: sys.exit('dup ' + w)
            seen.add(w)
    json.dump(v, open('data/g5ela-27-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
