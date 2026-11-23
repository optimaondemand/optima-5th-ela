#!/usr/bin/env python3
"""Write data/g5ela-28-{1..4,fluency}.json (week 28, By the Great Horn Spoon! Ch. 10-12 + theme day), Nov 23 2026.
Every book line checked against the By the Great Horn Spoon! text (project doc, Ch. 10-12; nothing from Ch. 13 on).
History: City of Placerville, "Placerville City History"; California State Parks, Office of Historic Preservation, Historical Landmark
No. 475 (Old Dry Diggins, Old Hangtown, Placerville); Calisphere (University of California), "1848-1865: Gold Rush, Statehood, and the
Western Movement" (the 1850 foreign miners' license tax, $20 a month, aimed at Latin American miners); the tax was repealed in 1851.
Hangtown: three men hanged in 1849 without a real trial (accounts differ on the month); the camp incorporated as Placerville in 1854.
Bethany's choices: trip points the picture (Ch. 10) + the tall tale (Ch. 12); hook "a whole town tells a hero story about you" (28.3);
virtue honesty; wow = Hangtown was real (28.2 card); Words of the diggings card; Pan for Color (no gold word is on that day's page);
calm and steady; diggings-life plates. Q4 audio is paused: Listen texts are Mason scripts, at or under 1,000 characters a lesson."""
import json, re, sys, html, io
LOOK = ("Each pan holds four words from the diggings. Two are color, the real gold. Two are slickens, the mud. "
        "Tap the slickens to wash them over the side. When only gold is left, the spangles slide into Jack's pouch.")
HOW = {"do": ["Read the clue on the pan.", "Tap a word that does not belong to wash it out.", "Keep going until only gold is left.", "Tap Next pan."],
       "why": "A real ending is spelled the same way every time, and a real root carries its meaning into every word it builds."}
SP = "Wash out the misspelled words. Keep the gold."
RT = "Wash out the words with no real fort or val root. Keep the gold."
def c(w, why, gold=False): return {"w": w, "gold": gold, "why": why}
def g(w, why): return c(w, why, True)
def pan(clue, *chips): return {"clue": clue, "chips": list(chips)}
def game(day, pans):
    return {"type": "pan", "title": "Pan for Color", "sub": "This week's word game · 6 pans today", "after": "Spelling", "look": LOOK, "how": HOW,
            "doneLine": "Come back tomorrow for six more pans." if day < 4 else "Four days, twenty-four pans. Jack's pouch is full of color.", "pans": pans}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted word in the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Transitions and openers tell a reader how one idea connects to the next."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud twice.", "Read the tip.", "Answer the question in your reading journal."],
        "why": "A short poem can carry two themes at once. Spotting both trains you to find more than one theme in the novel."}
def rh(ch):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
            "why": "The pause boxes are places to stop and think while you read."}
WS = lambda day: {"match": "Writer", "do": {1: ["Read today's step.", "Write your theme claim in one sentence.", "List two character choices that could prove it."],
                                          2: ["Read today's step.", "Turn your plan into sentences.", "Use the frames if you get stuck."],
                                          3: ["Read the checklist.", "Check your response one item at a time.", "Fix anything that is missing."],
                                          4: ["Read your response once more.", "Put the whole response in the box.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "A literary response proves a theme with what characters choose to do."}
HANGTOWN = {"tab": "reading", "after": "Read: Chapter 11", "title": "Real history: Hangtown and the dry washers", "min": 2,
  "intro": "Pitch-pine Billy and his friends are made up. Hangtown was a real gold camp, and the history below is real.",
  "items": [{"term": "A real town with a hard name", "meaning": "Miners first called the camp Dry Diggings, because they carried the dry dirt down to water to wash out the gold. In 1849 a crowd there hanged three men accused of robbery, without a real trial. After that, people called the camp Hangtown. Many people did not like the name, and in 1854 the town took a new one: Placerville, the name it still has."},
            {"term": "Dry washing came from Sonora", "meaning": "Pitch-pine Billy says dry washing is a trick from Sonora, Mexico. That part is true. Miners from Sonora, where water is scarce, knew how to get gold out of dry dirt, and thousands of them came to California in 1849."},
            {"term": "An unfair tax", "meaning": "In 1850 California made miners who were not American citizens pay $20 a month to dig, a huge sum then. It fell hardest on Mexican and other Latin American miners, and many were driven from the mines. The law was ended in 1851."},
            {"term": "Each camp made its own rules", "meaning": "There was no state mining law yet. In each camp the miners met and voted on their own rules: how big a claim could be, how to mark it, and how often you had to work it to keep it. Billy's rules in Chapter 11 are the novel's version."}],
  "note": "Sources: City of Placerville; California State Parks, Historical Landmark No. 475; Calisphere, University of California."}
WORDS = {"tab": "reading", "after": "Read: Chapter 11", "title": "Words of the diggings", "min": 1,
  "intro": "Miners' words from Chapters 10 and 11, each with the line where you meet it.",
  "items": [{"term": "road agent", "meaning": "a robber who stops coaches on the road", "line": "Road agents!", "cite": "Chapter 10"},
            {"term": "grubstake", "meaning": "money or supplies to live on while you look for gold", "line": "Their gold dust, their grubstake would soon be exposed.", "cite": "Chapter 10"},
            {"term": "jamoka", "meaning": "coffee", "line": "How about a cup of jamoka?", "cite": "Chapter 11"},
            {"term": "spangles", "meaning": "tiny flakes of gold", "line": "It's places like that the spangles like to hide, if there is any.", "cite": "Chapter 11"},
            {"term": "dry washing", "meaning": "getting gold out of dirt by pouring it and blowing, with no water", "line": "We call this dry washin'.", "cite": "Chapter 11"},
            {"term": "slickens", "meaning": "mud with the gold already washed out of it", "line": "You get rid of the rocks and slickens, little by little.", "cite": "Chapter 11"},
            {"term": "color", "meaning": "gold that shows in the pan", "line": "At first, you'll lose more color over the side than you'll save in the bottom.", "cite": "Chapter 11"},
            {"term": "mountain canary", "meaning": "a mule or a burro", "line": "You and your boy will be needin' a tent and a mountain canary.", "cite": "Chapter 11"}],
  "note": "Fleischman spells the miners' words the way they sound, so dry washing is dry washin' in the book."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "Jack and Praiseworthy are on the stagecoach to the diggings, and Cut-Eye Higgins is sitting right across from them. Before you read, write what you think Praiseworthy will do. Then set your lens: watch what each event costs a character."},
  "words": {"text": "This week's roots are fort, which means strong, and val, which means strong or worth. The spelling pattern is the endings i t y, m e n t, and n e s s, which turn words into names for ideas. In the game, wash the mud out of each pan and keep the gold."},
  "reading": {"text": "Read Chapter 10, The Rogue Out-Rogued. Watch Praiseworthy closely. He stays calm through almost everything. Notice the one thing that makes him stop being calm, and ask what that shows he cares about."},
  "assignment": {"text": "Three questions about Chapter 10. Then plan your literary response: one sentence for your theme claim, and two character choices that could prove it. A few words each is enough today."}},
 "how": [DOL, RW, dict(WGRD, why="A theme is built from events. Collect them before you name it.", use="You will use it in reading question 3."),
  {"match": "Morphology", "do": ["Read what fort and val mean.", "Read the example words.", "Type the missing root in each word, then tap Check Roots."], "why": "Two roots unlock many words about strength and worth."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Watch for the words as you read."], "why": "Knowing the words first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Look at what sits in front of each comma.", "Think through the questions, then tap Now check your thinking.", "Tap an opener, then tap the column that fits it."], "why": "Openers and transitions tell when, where, and how ideas link."},
  {"match": "Spelling", "do": ["Look at each base word and the longer word.", "Think through the questions, then tap Now name the pattern.", "Tap a word, then tap the column for its ending."], "why": "These endings turn a word into the name of an idea."},
  rh(10), WS(1)],
 "glossary": [{"word": "theme", "in": "What Good Readers Do", "meaning": "a big idea about life that a story shows through what happens"},
              {"word": "abstract", "in": "Spelling", "meaning": "naming an idea or feeling you cannot see or touch"}],
 "hints": {"fort": ["This root means strong.", "It is the strong root.", "f, o, r, t"], "val": ["This root means strong or worth.", "It is the worth root, three letters.", "v, a, l"],
           "vail": ["This root means to be stronger than. It is the worth root with one extra letter.", "Four letters: the worth root with an i before the l.", "v, a, i, l"]},
 "miss": {"kindness": "kind + ness: kindness keeps the whole base word.", "loneliness": "lonely + ness: the y changes to i, but the ending is still -ness.",
          "judgment": "judge + ment: judgment ends in -ment.", "argument": "argue + ment: the e drops, and the ending is -ment.",
          "scarcity": "scarce + ity: the e drops before -ity.", "curiosity": "curious + ity: curiosity ends in -ity."},
 "game": game(1, [pan(SP, c("lazyness", "lazy changes y to i: laziness."), g("happiness", "happy changes y to i before -ness."), c("readyness", "ready changes y to i: readiness."), g("emptiness", "empty changes y to i before -ness.")),
                  pan(SP, g("amusement", "amuse keeps its e before -ment."), c("statment", "state keeps its e before -ment: statement."), g("measurement", "measure keeps its e before -ment."), c("encouragment", "encourage keeps its e: encouragement.")),
                  pan(SP, c("majorety", "The ending is -ity: majority."), g("generosity", "generous drops the u before -ity, like curious and curiosity."), c("possibilty", "Do not drop the i before -ty: possibility."), g("ability", "able becomes abil before -ity.")),
                  pan(RT, c("fortune", "fortune comes from a Latin word for luck, not fort (strong)."), g("fortification", "fort (strong) + ify + cation: a wall built to make a place strong."), c("valley", "valley comes from a Latin word for a valley, not val (worth)."), g("valuable", "val (worth) + uable: worth a lot.")),
                  pan(RT, g("effortless", "ef + fort (strong) + less: needing no strength."), c("forty", "forty is a number word. No fort root inside."), g("invalid", "in (not) + valid (strong): not strong enough to count."), c("oval", "oval comes from the Latin word for egg.")),
                  pan(RT, c("arrival", "arrival comes from a word for reaching the shore. No val root."), g("comforting", "com + fort (strong): making someone feel strong again."), c("fortnight", "a fortnight is fourteen nights. No fort root."), g("devalue", "de (down) + val (worth): to lower something's worth."))]),
 "virtue": {"name": "honesty", "kind": "sort", "title": "Honest or not?", "intro": "This week's virtue is honesty: telling the truth and not trying to trick people, even when the truth costs you something. Sort these everyday examples.",
   "items": [{"t": "You find a wallet and turn it in with all the money still inside.", "ok": True, "why": "You give back what is not yours, even though no one would know."},
             {"t": "You tell a friend you loved their drawing, but you never looked at it.", "ok": False, "why": "It sounds kind, but it is not true."},
             {"t": "You tell your teacher you forgot your homework instead of making up a story.", "ok": True, "why": "The truth costs you something, and you tell it anyway."},
             {"t": "You let your brother take the blame for a plate you broke.", "ok": False, "why": "Staying quiet so someone else gets in trouble is a way of lying."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Hangtown at last. Before you read, think about why Praiseworthy keeps slowing Jack down. Then read a six line poem about an eagle, twice. It may be about more than one thing."},
  "words": {"text": "Today you hunt for openers and transitions, the words that link one idea to the next. Find the fort and val roots in new words. Then spot the endings that name ideas. Six more pans to wash."},
  "reading": {"text": "Read Chapter 11, Jamoka Jack. The diggings are not what Jack imagined. Watch what Jack is willing to do to be accepted, and watch what Praiseworthy has to give up along the way."},
  "assignment": {"text": "Three questions about Chapter 11. Then turn your plan into sentences. If you get stuck, use the frames on the card. Name a character's choice, and say what it shows."}},
 "how": [DOL, POEM, RW, dict(WGRD, why="Conflicts test what characters care about. That is where a theme shows.", use="You will use it in reading question 1."),
  {"match": "Grammar", "do": ["Read the syllables of the transitions.", "Write your sentences in your reading journal.", "Tap every opener and transition in the sentences."], "why": "Spotting openers in real sentences shows you how writers use them."},
  {"match": "Morphology", "do": ["Read each meaning.", "Type the missing root.", "Tap Check."], "why": "Spotting a root in a new word gives you a head start on its meaning."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Answer the question in your reading journal."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Read how each ending changes its base word.", "Write your five sentences in the box.", "Underline each idea word and name its ending."], "why": "This is your Show What You Know for spelling this week."},
  rh(11), WS(2)],
 "glossary": [{"word": "azure", "in": "Poetry Corner", "meaning": "bright sky blue"},
              {"word": "crag", "in": "Poetry Corner", "meaning": "a steep, rough rock on a mountain"},
              {"word": "isolation", "in": "Poetry Corner", "meaning": "being alone and cut off from others"}],
 "hints": {"fort": ["This root means strong.", "It is the strong root.", "f, o, r, t"], "val": ["This root means worth.", "It is the worth root, three letters.", "v, a, l"],
           "valid": ["This word means sound and true.", "The worth root plus i and d.", "v, a, l, i, d"]},
 "game": game(2, [pan(SP, g("politeness", "polite keeps its e before -ness."), c("politness", "polite keeps its e: politeness."), c("eagernes", "-ness has two s's: eagerness."), g("eagerness", "eager + ness.")),
                  pan(SP, c("paymint", "The ending is -ment: payment."), g("punishment", "punish + ment."), g("payment", "pay + ment."), c("punishmant", "The ending is -ment: punishment.")),
                  pan(SP, g("security", "secure drops its e before -ity."), c("securety", "The ending is -ity: security."), g("equality", "equal + ity."), c("equallity", "equal has one l: equality.")),
                  pan(RT, g("fortified", "fort (strong) + ified: made strong."), c("fortunate", "fortunate comes from fortune, a word for luck. No fort (strong) root."), c("festival", "festival comes from a word for a feast. No val root."), g("devalued", "de (down) + val (worth) + ued: made worth less.")),
                  pan(RT, c("interval", "interval comes from a word for the space between walls. No val (worth) root."), g("comfortable", "com + fort (strong) + able: at ease."), g("validation", "valid (strong) + ation: proof that something counts."), c("forty", "forty is a number word. No fort root.")),
                  pan(RT, g("uncomfortable", "un + com + fort (strong) + able: not at ease."), c("rival", "rival comes from a word for a stream. No val root."), c("carnival", "carnival comes from an old word for a feast. No val root."), g("valiantly", "val (strong) + iant + ly: bravely."))]),
 "cards": [HANGTOWN, WORDS],
 "virtue": {"name": "honesty", "kind": "log", "options": [
   {"t": "On the stage, Praiseworthy tells the road agent he is “Not a gentleman. Merely a butler.”"},
   {"t": "In Hangtown, Praiseworthy writes to Dr. Buckbee that Cut-Eye Higgins is in town and the map was taken by highwaymen."},
   {"t": "Praiseworthy tells Pitch-pine Billy, “The name is Praiseworthy, not Butler, sir.”"}],
   "line": "Tap the moment that shows the most honesty. Then tell why in one sentence.", "placeholder": "This shows the most honesty because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Answer the question on the card first. Then think about nicknames. What does a name you earn say about you? Today the partners walk back into Hangtown."},
  "words": {"text": "Today you build the idea words yourself, and watch what happens to each base word. Match the fort and val words to their meanings. Then write a paragraph with five transitions. Six more pans."},
  "reading": {"text": "Read Chapter 12, Bullwhip. Walk home with the partners by the campfires. Then watch what Praiseworthy does when the truth and his welcome pull different ways."},
  "assignment": {"text": "Three questions, the last one about all three chapters. Then revise your literary response with the checklist. Make sure each piece of evidence is a character's choice."}},
 "hook": {"q": "A whole town is telling a story about you. It isn't quite true, but it makes you a hero, and everyone welcomes you because of it. Do you set them straight?",
  "options": [{"t": "Yes. The truth matters more than being liked.", "reply": "That is where Praiseworthy starts. Listen:"},
              {"t": "No. It's harmless, and they like me.", "reply": "Praiseworthy is not so sure, at first. Listen:"},
              {"t": "Tell the truth, but laugh about it.", "reply": "Maybe the best of both. Praiseworthy starts like this:"}],
  "reveal": {"line": "But not under false colors. Gentlemen, allow me to explain", "cite": "Chapter 12",
             "then": "Read Chapter 12 to find out whether Hangtown lets him."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read the four base words and endings.", "Type each new word.", "Tap Check My Work."], "why": "Some bases change when an ending is added. Watching for that keeps your spelling right."},
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap a word, then tap its meaning.", "Match all four."], "why": "Each meaning carries its root."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Read the eight transitions and the comma rule.", "Spell all eight in the box.", "Write your paragraph with five of them, underlined."], "why": "This is your Show What You Know for grammar this week."},
  dict(WGRD, why="Rereading a choice shows how a character's values carry the theme.", use="You will use it in reading question 2."),
  rh(12), WS(3)],
 "glossary": [{"word": "exaggerated", "in": "Read: Chapter 12", "meaning": "made to sound bigger than it really was"},
              {"word": "reputation", "in": "Read: Chapter 12", "meaning": "what people believe about someone"}],
 "hints": {"loneliness": ["lonely ends in y. Watch what happens to it.", "The y changes to i before -ness.", "l, o, n, e, l, i, n, e, s, s"], "argument": ["argue ends in e. Watch what happens to it.", "The e drops before -ment.", "a, r, g, u, m, e, n, t"],
           "curiosity": ["curious ends in ous. One letter drops.", "The u drops before -ity.", "c, u, r, i, o, s, i, t, y"], "boldness": ["This base does not change.", "Just add -ness.", "b, o, l, d, n, e, s, s"]},
 "game": game(3, [pan(SP, g("weariness", "weary changes y to i before -ness."), c("wearyness", "weary changes y to i: weariness."), c("stilness", "still keeps both l's: stillness."), g("stillness", "still + ness.")),
                  pan(SP, c("enjoyement", "There is no e before -ment here: enjoyment."), g("enjoyment", "enjoy + ment."), g("equipment", "equip + ment."), c("equippment", "equip keeps one p: equipment.")),
                  pan(SP, g("necessity", "necessary becomes necess before -ity."), c("necesity", "necessity has two s's in the middle."), g("majority", "major + ity."), c("majorety", "The ending is -ity: majority.")),
                  pan(RT, g("fortifying", "fort (strong) + ifying: making strong."), c("fortune", "fortune comes from a Latin word for luck, not fort (strong)."), g("invaluable", "in + val (worth) + uable: worth more than you can count."), c("valley", "valley comes from a Latin word for a valley, not val (worth).")),
                  pan(RT, c("survival", "survival comes from a word for living. No val root."), g("effortlessly", "ef + fort (strong) + less + ly: with no strain."), g("evaluation", "e + val (worth) + uation: deciding what something is worth."), c("forty", "forty is a number word. No fort root.")),
                  pan(RT, g("comforter", "com + fort (strong) + er: someone who makes you feel strong again."), c("oval", "oval comes from the Latin word for egg."), c("fortnight", "a fortnight is fourteen nights. No fort root."), g("valued", "val (worth) + ued: thought to be worth a lot."))]),
 "virtue": {"name": "honesty", "kind": "meter", "title": "The honesty meter", "intro": "Think about one moment from Chapter 12.",
   "moment": "The miners say Praiseworthy knocked the outlaw nineteen feet uphill. First he tries to explain that Mr. Fletcher spread a grossly exaggerated account. When no one will listen, he winks at Jack and says it looked twenty-three feet at least.",
   "ask": "How honest is Praiseworthy here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He is this honest because…",
   "take": "Mason's take: somewhere in the middle. He tries to tell the truth first, and he never lies about the punch itself. But then he plays along with a tall tale, and he winks while he does it. Fleischman makes it funny, and leaves you to decide where honesty ends and a good joke begins."},
}
D[4] = {
 "readnow": {"text": "No new chapter today. Keep Chapters 10 to 12 open in your book as you choose your theme.", "step": "Choose your theme"},
 "listen": {
  "warmup": {"text": "Today you name the theme. First, read the eagle poem again. You found two themes in six lines. Now look for two themes in one scene from the novel."},
  "words": {"text": "Explain the roots and the endings in your own words. Pick an option on the choice board. The last six pans fill Jack's pouch."},
  "reading": {"text": "Choose a theme claim, or write your own. Find a second piece of evidence. Then argue the other side yourself, and answer it with evidence from the book."},
  "assignment": {"text": "Read your literary response once more. Check the claim, the two choices, the transitions, and the closing. Then submit it, and copy your work into Canvas."}},
 "how": [DOL, POEM, RW,
  {"match": "Morphology", "do": ["Explain the two roots in your reading journal.", "Type the word that fits each sentence.", "Tap Check My Work."], "why": "Explaining a root shows you really know it."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and say which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right answer in each question.", "Answer the question in your reading journal."], "why": "Explaining a choice shows you can make it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Tap the right spelling in each pair."], "why": "Knowing how the base changes keeps the ending right."},
  dict(WGRD, why="Naming the theme pulls the whole week together.", use="You will use it in theme question 1."),
  {"match": "Theme Analysis", "do": ["Read the four theme claims.", "Pick one, or write your own.", "Answer the three theme questions."], "why": "A theme claim is only as strong as its evidence."},
  {"match": "Argue the Other Side", "do": ["Pick a theme you did not choose.", "Write the best case for it in 1 or 2 sentences.", "Answer it with your own evidence."], "why": "Answering the other side makes your own claim stronger."},
  WS(4)],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "put ideas together into one big idea"},
              {"word": "claim", "in": "Theme Analysis", "meaning": "a sentence that says what you think and that you can prove"}],
 "hints": {"fortitude": ["Courage that lasts. It comes from the strong root.", "The strong root + itude.", "f, o, r, t, i, t, u, d, e"], "fortify": ["To make strong.", "The strong root + ify.", "f, o, r, t, i, f, y"],
           "valiant": ["Brave in danger. It comes from the strong-or-worth root.", "val + iant.", "v, a, l, i, a, n, t"], "validate": ["To prove something holds.", "valid + ate.", "v, a, l, i, d, a, t, e"]},
 "game": game(4, [pan(SP, g("carelessness", "careless + ness: two s's and then two more."), c("carelesness", "careless + ness keeps every s: carelessness."), c("dampnes", "-ness has two s's: dampness."), g("dampness", "damp + ness.")),
                  pan(SP, c("settlment", "settle keeps its e before -ment: settlement."), g("settlement", "settle keeps its e before -ment."), g("agreement", "agree + ment."), c("agreemant", "The ending is -ment: agreement.")),
                  pan(SP, g("probability", "probable becomes probabil before -ity."), c("probabilty", "Do not drop the i before -ty: probability."), c("prosperety", "The ending is -ity: prosperity."), g("prosperity", "prosper + ity.")),
                  pan(RT, g("discomfort", "dis + com + fort (strong): a feeling of not being at ease."), c("arrival", "arrival comes from a word for reaching the shore. No val root."), c("festival", "festival comes from a word for a feast. No val root."), g("valuation", "val (worth) + uation: a judgment of what something is worth.")),
                  pan(RT, c("fortunately", "fortunately comes from fortune, a word for luck. No fort (strong) root."), g("uncomfortably", "un + com + fort (strong) + ably: not at ease."), g("undervalue", "under + val (worth) + ue: to think something is worth less than it is."), c("interval", "interval comes from a word for the space between walls. No val root.")),
                  pan(RT, g("fortifications", "fort (strong) + ifications: walls that make a place strong."), c("forty", "forty is a number word. No fort root."), g("evaluating", "e + val (worth) + uating: judging what something is worth."), c("rival", "rival comes from a word for a stream. No val root."))]),
 "virtue": {"name": "honesty", "kind": "best", "title": "The most honest moment this week", "intro": "Look back at Chapters 10 to 12. Tap the moment you think shows honesty the most.",
   "options": [{"t": "On the stage, Praiseworthy tells the road agent he is not a gentleman, merely a butler (Chapter 10)."},
               {"t": "Praiseworthy writes to warn Dr. Buckbee about Cut-Eye Higgins and the map (Chapter 11)."},
               {"t": "Back in Hangtown, Praiseworthy tries to tell the miners the story has been exaggerated (Chapter 12)."}],
   "line": "Finish the sentence: This shows honesty the most because…", "placeholder": "This shows honesty the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the Bullwhip scene from Chapter 12 out loud. Give each porch voice its own sound, and let the numbers climb. Keep Praiseworthy calm and dry. When it sounds right, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
ART = {
 1: {"tab": "top", "file": "assets/art/btghs/remington-old-stagecoach.jpg", "title": "The Old Stage-Coach of the Plains",
  "alt": "A dark painting of a stagecoach pulled by a team of horses up a rocky rise at night, its lamps glowing, with a driver and riders on top against a moonlit sky.",
  "look": "Frederic Remington painted this in 1901, long after the Gold Rush, to show the old stagecoach days. It is set on the Plains, not in the Sierra, but look how small the coach seems on the dark hill, how hard the horses pull, and how the lamps glow. Jack's stage climbs the same way at twilight in Chapter 10.",
  "lookBtn": "Tap to learn about this painting", "creator": "Frederic Remington", "date": "1901",
  "license": "Public domain (Amon Carter Museum of American Art, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Remington_The_Old_Stage-Coach_of_the_Plains_1901.jpg"},
 2: {"tab": "top", "file": "assets/art/btghs/currier-gold-mining-california.jpg", "title": "Gold Mining in California",
  "alt": "A colored print of miners in red shirts working a mountain stream: one pans for gold, two shovel dirt into a long wooden trough, and others work a hillside, with a cabin, pine trees and snowy peaks behind.",
  "look": "A hand-colored print by Currier and Ives, sold in 1871. It shows many ways of washing gold at once: a miner crouches with a pan in the stream, two men shovel dirt into a long trough, and up on the hill others wash the bank with a hose, a method from the later years. Find the pan. That is how Pitch-pine Billy teaches Jack in Chapter 11.",
  "lookBtn": "Tap to learn about this print", "creator": "Currier and Ives", "date": "about 1871",
  "license": "Public domain (Library of Congress, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Gold_mining_in_California_-_Currier_%26_Ives_c.1871.jpg"},
 3: {"tab": "top", "file": "assets/art/btghs/nahl-sunday-morning-mines.jpg", "title": "Sunday Morning in the Mines (detail)",
  "alt": "A painting of three miners resting outside a log cabin under pine trees; one reads aloud from a book, inside the doorway a man writes a letter, and a small cooking fire and a wooden rocker sit on the ground in front.",
  "look": "Charles Nahl was a miner and artist in the gold country. He painted this in 1872. This is one part of a larger painting: on their day off, these miners read, rest and write letters home by the cabin. Look at the fire, the pans and the wooden rocker on the ground. It is the kind of camp the partners walk back to in Chapter 12.",
  "lookBtn": "Tap to learn about this painting", "creator": "Charles Christian Nahl", "date": "1872",
  "license": "Public domain (Crocker Art Museum, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Nahl_1872,_Sunday_Morning_in_the_Mines.jpg"},
 4: {"tab": "top", "file": "assets/art/btghs/bierstadt-among-sierra-nevada.jpg", "title": "Among the Sierra Nevada, California",
  "alt": "A large painting of a calm mountain lake with deer at the water's edge, tall cliffs and a waterfall on the left, and snowy peaks lit by sunlight breaking through clouds.",
  "look": "Albert Bierstadt painted this in 1868, after travels in the mountains where the gold camps were. He made the light and the peaks grander than real life. Look at the storm clouds and the sunlight breaking through at the same time. One painting, two feelings, like a poem or a novel that carries two themes.",
  "lookBtn": "Tap to learn about this painting", "creator": "Albert Bierstadt", "date": "1868",
  "license": "Public domain (Smithsonian American Art Museum, via Wikimedia Commons)", "url": "https://commons.wikimedia.org/wiki/File:Albert_Bierstadt_-_Among_the_Sierra_Nevada,_California_-_Google_Art_Project.jpg"},
}
for _k, _a in ART.items(): D[_k]["art"] = _a
FILES = {1: 'lesson-28-1-btghs-ch10.html', 2: 'lesson-28-2-btghs-ch11.html', 3: 'lesson-28-3-btghs-ch12.html', 4: 'lesson-28-4-btghs-theme.html'}
def page_words(f):
    s = io.open(f, encoding='utf-8').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s).lower()
    return set(re.findall(r"[a-z]+", s))
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s or '–' in s: sys.exit('%s: dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK', 'classmate', 'partner up'):
        if bad in s: sys.exit('%s: %s' % (k, bad))
    if 'game' in v:
        pw = page_words(FILES[k]); seen = set()
        for p in v['game']['pans']:
            gs = [c for c in p['chips'] if c['gold']]
            if len(p['chips']) != 4 or len(gs) != 2: sys.exit('%s: pan shape' % k)
            for c in p['chips']:
                if c['w'] in seen: sys.exit('%s: dup %s' % (k, c['w']))
                seen.add(c['w'])
                if c['gold'] and c['w'] in pw: sys.exit('%s: gold word %s is on that day\'s page' % (k, c['w']))
    json.dump(v, open('data/g5ela-28-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
