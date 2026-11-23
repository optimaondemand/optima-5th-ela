#!/usr/bin/env python3
"""Write data/g5ela-26-{1..4,fluency}.json (week 26, By the Great Horn Spoon! Ch. 4-6 + humor day), Nov 23 2026.
Every book line checked against the By the Great Horn Spoon! text (project doc, Ch. 4-6, earlier chapters for
the speech spellings). History: Britannica (Strait of Magellan: about 350 miles long, 2-20 miles wide; Magellan's
ships 1520), Britannica Kids / Wikipedia "Fuegians" (Tierra del Fuego named for the Native peoples' fires seen by
Magellan's expedition; Selk'nam, Yaghan, Kawesqar, Haush), maritimeheritage.org and Wikipedia "SS California (1848)"
(left New York Oct 1848; Rio de Janeiro, the Strait of Magellan, Callao; San Francisco Feb 28, 1849).
Bethany's choices: hook "A free ticket home?" (26.1), Through the Strait game (no word is an answer on that day's
page), wow = the real Strait route (kept apart from the novel), virtue self-control.
Q4 audio is paused: the Listen texts are Mason scripts, written to stay at or under 1,000 characters a lesson."""
import json, sys
LOOK = ("The Strait of Magellan is a narrow, twisting passage of water at the bottom of South America. Here your ship works west through it, "
        "from the Atlantic to the Pacific. At each narrows, read the clue and pick the safe channel: the word that really fits. "
        "Every narrows you pass lights a fire on the shore of Tierra del Fuego, the Land of Fire.")
HOW = {"do": ["Read the clue at the narrows.", "Look at the word in each channel.", "Tap the channel with the word that really fits.", "Tap Sail on."],
       "why": "A root only helps if it is really there, and a speech spelling only works if the apostrophe is in the right place."}
def nw(clue, a, b, ok, why, miss=None):
    d = {"clue": clue, "a": a, "b": b, "ok": ok, "why": why}
    if miss: d["miss"] = miss
    return d
def game(day, narrows):
    return {"type": "strait", "title": "Through the Strait", "sub": "This week's word game · 6 narrows today", "after": "Morphology",
            "look": LOOK, "how": HOW, "doneLine": "The Pacific is open. Come back tomorrow for six more narrows." if day < 4 else "Through the Strait every day this week. Well sailed.", "narrows": narrows}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted parts of the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "The marks around a speech tell the reader who is talking and when they stop."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Read the tip.", "Answer the question in your reading journal."],
        "why": "Funny poems show voice and word choice very clearly."}
def rh(ch):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
            "why": "The pause boxes are places to stop and think while you read."}
WS = lambda day: {"match": "Writer", "do": {1: ["Read today's step and jot your four planning notes.", "Read Alex's draft and what makes it work.", "Start your scene in the middle of the action."],
                                          2: ["Read today's step.", "Keep writing your scene.", "Use the frames if you get stuck."],
                                          3: ["Read the checklist.", "Check your scene one item at a time.", "Fix anything that is missing."],
                                          4: ["Add one comic moment to your scene.", "Put your whole scene in the box.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "Voice, dialogue and reaction make a reader feel they are inside the scene."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "The Lady Wilma is heading south toward the bottom of South America. Today there is a pig, a cook with a cleaver, and a hard question for Jack. Before you read, think about what you would do if someone offered you a ticket home."},
  "words": {"text": "This week's roots are rid and ris, which mean laugh, and lud and lus, which mean play. In the game, sail through the narrows. Pick the channel with the word that really carries the root."},
  "reading": {"text": "Read Chapter 4. Notice who the joke is on as the pig hunt grows. Then watch the chapter turn serious in the harbor at Rio. Listen to how Jack sounds when the jokes stop."},
  "assignment": {"text": "Three questions about Chapter 4. Then plan your adventure scene: who is there, where it happens, what goes wrong, and one line your hero says. Start in the middle of the action."}},
 "hook": {"q": "You are halfway through a long, hard voyage. The most dangerous waters are just ahead. Someone you trust offers you a free ticket home. Do you take it?",
  "options": [{"t": "Yes. Home is safe.", "reply": "Nobody would blame you. Jack hears this offer in Chapter 4:"},
              {"t": "No. I came this far.", "reply": "Brave, but the danger is real. Jack hears this warning in Chapter 4:"},
              {"t": "It depends who I'm traveling with.", "reply": "That may matter most of all. Jack hears this from his partner in Chapter 4:"}],
  "reveal": {"line": "Cape Horn lies ahead of us. It's a bad stretch of water.", "cite": "Chapter 4",
             "then": "Read Chapter 4 to find out what Jack decides, and why Praiseworthy asked."}},
 "how": [DOL, RW,
  {"match": "Morphology", "do": ["Read what rid/ris and lud/lus mean.", "Read the example words.", "Type the missing root in each word, then tap Check Roots."], "why": "Two pairs of roots unlock many words about laughing and playing."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Notice which chapter each word comes from."], "why": "Knowing the words first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Look at where the marks sit in the two sentences.", "Think through the questions, then tap Now check your thinking.", "Tap a line, then tap the column that fits it."], "why": "Dialogue marks tell the reader who is speaking and when."},
  {"match": "Spelling", "do": ["Read the eight dialogue tags.", "Read how speech spellings use an apostrophe.", "Tap a tag, then tap the column that fits it."], "why": "A strong tag tells the reader how a line was spoken."},
  rh(4), dict(WGRD, why="Humor tells you how the author sees a character.", use="You will use it in reading question 2."),
  WS(1)],
 "glossary": [{"word": "stateroom", "in": "Read: Chapter 4", "meaning": "a private bedroom on a ship"},
              {"word": "tone", "in": "What Good Readers Do", "meaning": "the attitude a writer takes toward what is happening"}],
 "hints": {"rid": ["This word is about laughing at someone.", "It is the laugh root that ends in d.", "r, i, d"], "lud": ["This word is about a game or a joke.", "It is the play root that ends in d.", "l, u, d"],
           "ris": ["This word is about mocking laughter.", "It is the laugh root that ends in s.", "r, i, s"], "lus": ["This word is about a trick on your eyes.", "It is the play root that ends in s.", "l, u, s"],
           "lude": ["A playful pause between two acts.", "The play root, plus a silent e.", "l, u, d, e"]},
 "miss": {"whispered": "Whispered tells how loud: very quietly.", "bellowed": "Bellowed tells how loud: a huge, deep shout.",
          "pleaded": "Pleaded tells a feeling: someone begging.", "grumbled": "Grumbled tells a feeling: someone cross and complaining.",
          "said": "Said only tells who spoke.", "replied": "Replied only tells that someone answered."},
 "game": game(1, [nw("Find the word with lud (play): to slip away from someone, as if in a game of tag.", "elude", "include", "a", "e (out) + lud (play): to play your way out. Include comes from clud, which means close."),
                  nw("Which word really carries rid (laugh)?", "riddle", "deride", "b", "de (down) + rid (laugh): to laugh down at someone. A riddle is a puzzle; it only looks like it has the root.", "Is a riddle about laughing at someone? Look at the other channel."),
                  nw("Find the word with lus (play): a secret trick that two people play together.", "collusion", "conclusion", "a", "col (together) + lus (play). Conclusion comes from clud, which means close."),
                  nw("Find the word with ris (laugh): laughter that mocks someone.", "decision", "derision", "b", "de + ris + ion: mocking laughter. Decision comes from cis, which means cut."),
                  nw("Chapter 1: a cold passenger shouts that someone has been hogging the stove. Which spelling shows how he says it?", "You been hoggin' that stove", "You been hog'gin that stove", "a", "hoggin' = hogging. The apostrophe sits where the g is missing, at the end."),
                  nw("Chapter 1: Captain Swain roars at the stowaways for inviting in the weather. Which spelling is his?", "invitin", "invitin'", "b", "invitin' = inviting. A missing letter needs an apostrophe in its place.", "A letter is missing. What marks the spot?")]),
 "virtue": {"name": "self-control", "kind": "sort", "title": "Self-control or not?", "intro": "This week's virtue is self-control: staying calm and choosing what you do, even when you feel scared, angry or excited. Sort these everyday examples.",
   "items": [{"t": "You feel nervous before a test, so you take a slow breath and start with the first question.", "ok": True, "why": "You notice the feeling and choose a calm next step."},
             {"t": "Your little brother knocks over your tower, and you yell and knock over his.", "ok": False, "why": "The anger is choosing for you. Self-control means you choose."},
             {"t": "You want to blurt out the answer, but you wait for your turn.", "ok": True, "why": "You hold back what you feel like doing because waiting is right."},
             {"t": "A friend wins the game, and you say good game even though you feel let down.", "ok": True, "why": "You keep your disappointment from hurting someone else."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Before you read, a famous poem full of words that don't exist, and yet you can almost understand them. Listen to the sounds. Then think: why is nonsense funny?"},
  "words": {"text": "Find rid, ris, lud and lus in new words. Then look at speech spellings, where an apostrophe takes the place of a missing letter. In the game, six more narrows. One channel is a speech spelling."},
  "reading": {"text": "Read Chapter 5, Land of Fire. The storms are fierce. Watch what Praiseworthy says out loud, and what the narrator tells you he really believes. Then watch for the surprise at the end of the chapter."},
  "assignment": {"text": "Three questions about Chapter 5. Then keep drafting your scene. Give one character a line of dialogue and a reaction that shows how they feel. Use the frames if you get stuck."}},
 "how": [DOL, POEM, RW,
  {"match": "Grammar", "do": ["Read the four rules.", "Write your dialogue in the box.", "Give each speaker a new paragraph."], "why": "This is your Show What You Know for grammar this week."},
  {"match": "Morphology", "do": ["Read each clue.", "Type the missing root.", "Tap Check."], "why": "Spotting a root in a new word gives you a head start on its meaning."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Answer the question in your reading journal."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Say each tag and find the loud beat.", "Read the speech spelling note.", "Tap every tag, then tap the right speech spelling."], "why": "Knowing the loud beat helps you spell the quiet ones."},
  rh(5), dict(WGRD, why="Tone is how the telling feels. A calm voice in a storm is a choice.", use="You will use it in reading question 2."),
  WS(2)],
 "glossary": [{"word": "inclement", "in": "Daily Oral Language", "meaning": "stormy and unpleasant (weather)"},
              {"word": "diction", "in": "Poetry Corner", "meaning": "a writer's choice of words"}],
 "hints": {"ris": ["This word means laughable.", "It is the laugh root that ends in s.", "r, i, s"], "lu": ["A secret game between people.", "Two letters of the play root.", "l, u"],
           "lude": ["To slip away, as in a game.", "The play root, plus a silent e.", "l, u, d, e"], "rid": ["To laugh down at someone.", "The laugh root that ends in d.", "r, i, d"]},
 "game": game(2, [nw("Find the word with lud (play): to trick someone into believing something false.", "deliver", "delude", "b", "de + lud: to play someone false. Deliver comes from liber, which means free."),
                  nw("Find the word with lud (play): to hint at something without saying it straight out.", "allude", "allow", "a", "al (toward) + lud (play): to play toward an idea. Allow has no play root."),
                  nw("Which word carries rid (laugh) and means so silly it deserves a laugh?", "rigorous", "ridiculous", "b", "rid + iculous: worth laughing at. Rigorous means strict and careful; it has no laugh root."),
                  nw("Which word really carries ris (laugh)?", "derisive", "rider", "a", "de + ris + ive: full of mocking laughter. A rider rides; the r-i-d is just letters.", "Does rider have anything to do with laughing?"),
                  nw("Chapter 4: Mountain Jim says a boy needs all the schooling he can get. Which spelling is his?", "educatin'", "educat'in", "a", "educatin' = educating. The apostrophe goes where the g was, at the end."),
                  nw("Chapter 1: a gold-seeker pushing toward the stove calls someone partner. Which spelling shows how he says it?", "pard'ner", "pardner", "b", "pardner is how he says partner. No letter is missing, just a sound changed, so there is no apostrophe.", "Is a letter really left out here, or just changed?")]),
 "cards": [{"tab": "reading", "after": "Read: Chapter 5", "title": "Real history: the Strait of Magellan", "min": 2,
   "intro": "The Lady Wilma and the Sea Raven are made up. The places in Chapter 5 are real.",
   "items": [{"term": "The Strait of Magellan", "meaning": "A narrow, twisting passage of water between the tip of South America and the islands south of it. It is about 350 miles long and from 2 to 20 miles wide. In 1520 Ferdinand Magellan's ships became the first European ships to sail through it."},
             {"term": "Tierra del Fuego", "meaning": "Spanish for Land of Fire. Magellan's crew saw the fires of the people who lived there and named the land for them. The Selk'nam, Yaghan, Kaweskar and Haush peoples had lived there for thousands of years."},
             {"term": "A real steamship took this route", "meaning": "The paddle steamer SS California left New York in October 1848. She stopped at Rio de Janeiro, steamed through the Strait of Magellan, stopped at Callao in Peru, and reached San Francisco on February 28, 1849, the first steamship to arrive there in the Gold Rush."}],
   "note": "Sources: Encyclopaedia Britannica; the Maritime Heritage Project (San Francisco ship arrivals, 1849)."}],
 "virtue": {"name": "self-control", "kind": "log", "options": [
   {"t": "Praiseworthy calls the scary sea stories “Stuff and nonsense,” even though he believes every word of them."},
   {"t": "Holding onto a post with the hook of his umbrella, Praiseworthy calls the storm “A mere squall.”"},
   {"t": "In the boiler room, the butler seems unafraid, and Jack finds comfort in being at his side."}],
   "line": "Tap the moment that shows the most self-control. Then tell why in one sentence.", "placeholder": "This shows the most self-control because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "The wind has died. The ship sits still on the sea, day after day. Two men think they are ruined. Before you read, think: can one problem ever be the answer to another?"},
  "words": {"text": "Use the roots to work out words, and use the tags in your own scene. In the game, six more narrows. Two channels test speech spellings from today's chapter."},
  "reading": {"text": "Read Chapter 6. Reread one funny part and take it apart: the setup, then the turn. Then notice who thinks of the potato idea, and who gets the credit."},
  "assignment": {"text": "Three questions, the last one about all three chapters. Then revise your scene with the checklist. Make sure each new speaker gets a new paragraph."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read the eight tags.", "Write your scene in the box.", "Underline each tag you use."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap a word, then tap its root.", "Match all four."], "why": "Roots let you guess a new word before you look it up."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Write the bargain scene in your reading journal.", "Type the mark that belongs in each gap.", "Tap Check My Work."], "why": "The right mark tells the reader how a line was said."},
  rh(6), dict(WGRD, why="Taking a joke apart shows how the author built it.", use="You will use it in reading question 1."),
  WS(3)],
 "glossary": [{"word": "setup", "in": "What Good Readers Do", "meaning": "the first part of a joke, which makes you expect something"},
              {"word": "action beat", "in": "Grammar", "meaning": "a short sentence about what a character does while speaking"}],
 "hints": {",": ["Look at what comes after the closing quotation mark.", "A tag follows, so the sentence keeps going.", "The mark that keeps a sentence going."],
           "?": ["Read the speech out loud. Is it a question?", "The tag says Jack asked.", "The mark that ends a question."],
           "!": ["How does Monsieur Gaunt feel?", "The tag says exclaimed.", "The mark for a strong feeling."],
           ".": ["Is there a tag after this speech?", "No tag, so the sentence ends inside the quotation marks.", "The mark that ends a plain statement."]},
 "game": game(3, [nw("Find the word with lus (play): hard to catch, always slipping away.", "exclusive", "elusive", "b", "e (out) + lus (play) + ive. Exclusive comes from clus, which means shut."),
                  nw("Find the word with lus (play): a false belief, as if your mind were being tricked.", "delusion", "dilution", "a", "de + lus + ion. Dilution means making something weaker with water."),
                  nw("Find the word with ris (laugh): able to make people laugh.", "visible", "risible", "b", "ris + ible: laughable. Visible comes from vis, which means see."),
                  nw("Find the word with lud (play): a short break between the acts of a play.", "interlude", "interval", "a", "inter (between) + lude (play). Interval has no play root."),
                  nw("Chapter 6: Mountain Jim says the haircut needs evening up on one side. Which spelling is his?", "even'in", "evenin'", "b", "evenin' = evening. The apostrophe stands where the g was.", "Where is the letter that is missing? Put the apostrophe there."),
                  nw("Chapter 6: asked if he will eat the shark, Mountain Jim says he sure will. Which spelling shows how he says sure?", "shore", "sho're", "a", "shore is how he says sure. A sound changes but no letter is left out, so there is no apostrophe.", "Is anything missing, or is a sound just changed?")]),
 "virtue": {"name": "self-control", "kind": "meter", "title": "The self-control meter", "intro": "Think about one moment from Chapter 6.",
   "moment": "Jack thinks of the potato idea. But Praiseworthy tells the two men the idea is so simple that “a boy could have thought of it.” Jack remained silent, but stuck his hands in his pockets and felt proud of himself.",
   "ask": "How much self-control does Jack show here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He shows this much because…",
   "take": "Mason's take: a lot. Jack could have shouted that it was his idea. He kept quiet and let the good news belong to the two men."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "Last day of the week. A funny poem told as a conversation between a young man and his very strange father. Listen for two different voices, and for how calmly the father says ridiculous things."},
  "words": {"text": "Explain the roots in your own words, and tell what an apostrophe does in a speech spelling. In the game, the last six narrows of the week."},
  "reading": {"text": "Today you look back at Chapters 4, 5 and 6. Find what made you laugh, and find the one moment that is not funny at all. Then decide what the humor does for the story."},
  "assignment": {"text": "Three questions, the last one about the whole week. Then add one comic moment and submit your scene. Copy your work and paste it into Canvas."}},
 "how": [DOL, POEM, RW,
  {"match": "Morphology", "do": ["Explain the two roots in your reading journal.", "Type the word that fits each sentence.", "Tap Check My Work."], "why": "Explaining a root shows you really know it."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and say which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right version in each pair.", "Answer the question in your reading journal."], "why": "Explaining a rule shows you can use it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Tap the stronger tag in each pair.", "Tap the spelling that shows how Mountain Jim talks."], "why": "Tags and speech spellings both bring a voice to life."},
  {"match": "How Fleischman Makes You Laugh", "do": ["Read the three comic techniques.", "Answer the two pause boxes and the three questions.", "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
   "why": "Naming the technique helps you use it in your own writing."},
  dict(WGRD, why="Synthesizing means putting the week together into one idea.", use="You will use it in question 3."),
  WS(4)],
 "glossary": [{"word": "contrast", "in": "How Fleischman Makes You Laugh", "meaning": "a big difference between two things placed side by side"},
              {"word": "absurd", "in": "How Fleischman Makes You Laugh", "meaning": "so silly or strange that it makes no sense"}],
 "hints": {"ludicrous": ["Silly enough to laugh at.", "It starts with the play root.", "lud + icrous"], "ridicule": ["To make fun of someone cruelly.", "It starts with the laugh root.", "rid + icule"],
           "illusion": ["A trick your eyes play.", "il + the play root + ion.", "il + lus + ion"], "derision": ["Scornful laughter.", "de + the laugh root + ion.", "de + ris + ion"]},
 "game": game(4, [nw("Find the word with lude (play): a short piece played before the main event.", "prepare", "prelude", "b", "pre (before) + lude (play). Prepare comes from par, which means get ready."),
                  nw("Find the word with lus (play): a secret plan between two people.", "collusion", "collision", "a", "col (together) + lus (play). Collision comes from a root that means strike.", "One means crashing. Which one means playing together?"),
                  nw("Which word carries ris (laugh)?", "decisive", "derisive", "b", "de + ris + ive: mocking. Decisive comes from cis, which means cut."),
                  nw("Find the word with lus (play): a quick mention that plays on something the reader already knows.", "allusion", "allowance", "a", "al (toward) + lus (play) + ion. Allowance has no play root."),
                  nw("Chapter 4: the cook shouts about what pigs are for. Which spelling is his?", "Pigs is for eatin', not for pets.", "Pigs is for eat'in, not for pets.", "a", "eatin' = eating. The apostrophe goes where the g was."),
                  nw("Chapter 4: the cook says there is no rain in the cabin. Which spelling is his?", "But it aint raining.", "But it ain't raining.", "b", "ain't is a squeezed-together word, so it needs an apostrophe. It is fine in a character's speech; spell it out in your own sentences.")]),
 "virtue": {"name": "self-control", "kind": "best", "title": "The moment of most self-control this week", "intro": "Look back at Chapters 4 to 6. Tap the moment you think shows self-control the most.",
   "options": [{"t": "At Rio, Jack feels a welling up inside him, then answers, “I'm not scared” (Chapter 4)."},
               {"t": "Praiseworthy calls the storm stories “Stuff and nonsense” while he believes every word (Chapter 5)."},
               {"t": "Jack stays silent while Praiseworthy gives the potato idea away (Chapter 6)."}],
   "line": "Finish the sentence: This shows self-control the most because…", "placeholder": "This shows self-control the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the pig hunt from Chapter 4 out loud. Pick up speed through the list of places they search, then slow down for the talking. Make the cook sound cross and Monsieur Gaunt sound polite. Let the last word land. When it sounds smooth, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
PAGE = {1: {'ridicule', 'ridiculous', 'derisive', 'risible', 'ludicrous', 'prelude', 'interlude', 'illusion'},
        2: {'risible', 'collusion', 'elude', 'deride'}, 3: {'ridicule', 'derision', 'ludicrous', 'illusion', 'ridiculous'},
        4: {'ludicrous', 'ridicule', 'illusion', 'derision', 'ridiculous', 'deride'}}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s or '–' in s: sys.exit('%s: dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK'):
        if bad in s: sys.exit('%s: %s' % (k, bad))
    if 'game' in v:
        for e in v['game']['narrows']:
            if e[e['ok']] in PAGE[k]: sys.exit('%s: game word %s is on that day\'s page' % (k, e[e['ok']]))
            if e['ok'] not in ('a', 'b'): sys.exit('ok?')
    json.dump(v, open('data/g5ela-26-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
