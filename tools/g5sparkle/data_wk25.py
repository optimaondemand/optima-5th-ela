#!/usr/bin/env python3
"""Write data/g5ela-25-{1..4,fluency}.json (week 25, By the Great Horn Spoon! Gold Rush background + Ch. 1-3),
Nov 22 2026. Every book line checked against the By the Great Horn Spoon! text (project doc); history against
LOC, NPS, PBS, Calisphere and NLM (see fix_wk25.py). Bethany's choices: hook "Pick your route" (25.1), The
Assayer's Scale game (HEAR / SPEAK / FOOL'S GOLD; no word is an answer on that day's page), plates found by
Claude (Ensigns & Thayer 1849 map, Lane Boston Harbor 1854, Currier 1849, Lane Becalmed 1860), virtue loyalty.
Q4 audio is paused: the Listen texts are Mason scripts, written to stay at or under 1,000 characters a lesson."""
import json, sys
A = 'assets/art/btghs/'
C = 'https://commons.wikimedia.org/wiki/File:'
LOOK = ("An assayer tested gold in the Gold Rush, to tell real gold from fool's gold. Here you test words. "
        "A word with aud (hear) goes on the HEAR pan. A word with or (speak) goes on the SPEAK pan. A word that only looks like one is fool's gold.")
HOW = {"do": ["Read the word on the nugget.", "Think about what it means.", "Tap HEAR, SPEAK, or Fool's gold.", "Tap Next word."],
       "why": "A root only helps if it is really there. Testing the meaning keeps you from being fooled."}
def N(w, pan, why, miss=None):
    d = {"w": w, "pan": pan, "why": why}
    if miss: d["miss"] = miss
    return d
def game(day, nuggets):
    return {"type": "scale", "title": "The Assayer's Scale", "sub": "This week's word game · 6 words today", "after": "Morphology",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow for six more words." if day < 4 else "Every word this week is weighed. Well done.", "nuggets": nuggets}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Fix the second sentence in the box.", "Tap See the Answer to check."],
       "why": "A phrase that tells where or when puts the reader in the scene."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Read the tip about tone.", "Answer the question in your reading journal."],
        "why": "Tone is how a writer feels about the subject. Funny poems show it clearly."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what loyalty means.", "Read the example.", "After you read, %s at the end of this tab." % job]}
def rh(ch, extra="Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, extra],
            "why": "The pause boxes are places to stop and think while you read."}
def art(file, title, alt, look, creator, date, url, lic, btn="Tap to learn about this painting"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": btn, "creator": creator, "date": date, "license": lic, "url": url}
HINT = {"aud": ["This word is about hearing.", "The hearing root has three letters.", "a, u, d"], "or": ["This word is about speaking.", "The speaking root has two letters.", "o, r"]}
WS = lambda day: {"match": "Writer", "do": {2: ["Read today's step.", "Turn your plan notes into full sentences.", "Use the frames if you get stuck."],
                                          3: ["Read today's step and the checklist.", "Check your plan one item at a time and fix what is missing.", "Add one thing that isn't what it seems."],
                                          4: ["Read what a complete plan includes.", "Put your whole plan in the box.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "A good plan makes the draft next week much easier."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "A new book starts this week, By the Great Horn Spoon! It begins in eighteen forty-nine, and the Gold Rush was real. Today you learn the real history first: who went to California, how they got there, and who was already living there."},
  "words": {"text": "This week's roots are aud, which means hear, and or, which means speak. Some words only look like they have them. In the game, test each word like an assayer tests gold: hear, speak, or fool's gold."},
  "reading": {"text": "Read about the California Gold Rush and study the map of the three routes. Keep the real history and the novel apart. The passage gives real numbers. The novel is a made-up adventure inside that history."},
  "assignment": {"text": "Your adventure story starts today. Plan four things: a hero, a problem, a setting, and what is at stake. Notes are fine. You will build on this plan all week."}},
 "hook": {"q": "It is 1849. You live in Boston, and you want to reach the gold fields in California. Which way do you go?",
  "options": [{"t": "Sail all the way around Cape Horn.", "reply": "More than 13,000 miles by ship, often five to eight months, with storms at the bottom of the world. Many New Englanders went this way. So does the novel:"},
              {"t": "Sail to Panama and cross the jungle.", "reply": "It was shorter, but yellow fever and malaria waited in the jungle, and the ships on the Pacific side were overbooked. The novel's heroes take the long way:"},
              {"t": "Walk the California Trail with a wagon.", "reply": "About 2,000 miles from Missouri, and cholera along the way. But you live by the sea. The novel's heroes go by ship:"}],
  "reveal": {"line": "A sailing ship with two great sidewheels went splashing out of Boston harbor on a voyage around the Horn to San Francisco.", "cite": "Chapter 1",
             "then": "Read today's passage to find out what that voyage was really like."}},
 "how": [DOL, RW,
  {"match": "Morphology", "do": ["Read what aud and or mean.", "Read the example words.", "Type the missing root in each word, then tap Check My Roots."], "why": "Two small roots unlock dozens of words about hearing and speaking."},
  {"match": "Vocabulary", "do": ["Read the sentence for each of the two words.", "Look at the word parts.", "Tap each card to check the other three words."], "why": "These words are in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the two sentences from the novel.", "Think through the questions, then tap Now check your thinking.", "Tap the sentence that puts you in a place."], "why": "Phrases like these build the setting of an adventure."},
  {"match": "Spelling", "do": ["Read each long word in syllables.", "Think through the questions.", "Tap a word, then tap the column that fits it."], "why": "Long words are easier to spell one syllable at a time."},
  {"match": "Read: The California Gold Rush", "do": ["Read the passage. It is real history.", "Study the map of the three routes.", "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
   "why": "The novel is set inside this history. Knowing it makes the story make sense."},
  dict(WGRD, why="Good readers bring what they know into a new book.", use="You will use it in reading question 3."),
  {"match": "Writer", "do": ["Read Alex's plan.", "Answer the four questions in the box: hero, problem, setting, stakes.", "Bullet points are fine."], "why": "Every adventure starts with someone who wants something and a world that makes it hard."}],
 "glossary": [{"word": "overbooked", "in": "Read: The California Gold Rush", "meaning": "sold more tickets than there were places"},
              {"word": "malaria", "in": "Read: The California Gold Rush", "meaning": "a sickness spread by mosquito bites"}],
 "hints": {"aud": HINT["aud"], "or": HINT["or"]},
 "miss": {"Massachusetts": "Look for the doubled letters: ss, then ss again, then tt.", "Mississippi": "Look for the doubled letters: ss, ss and pp.",
          "passengers": "pas-sen-gers. The ss in the middle is doubled.", "California": "No doubled letters. Say it: Cal-i-FOR-ni-a. The i in Cal-i is quiet.",
          "Sacramento": "No doubled letters. Say it: Sac-ra-MEN-to. The a in -ra- is quiet.", "Argonaut": "No doubled letters. Say it: AR-go-naut. The o is quiet."},
 "game": game(1, [N("audiobook", "hear", "aud + io + book: a book you listen to."), N("orally", "speak", "or + al + ly: by speaking, not in writing."),
                  N("horn", "fool", "No root here. A horn spoon is made of an ox's horn. The or is just part of the word.", "Look closely. Is horn about speaking?"),
                  N("audit", "hear", "Long ago, money records were read out loud and heard by a checker. Now an audit is a careful check."),
                  N("forest", "fool", "No root here. Forest comes from an old word for outside. The or is just letters.", "Does a forest have anything to do with speaking?"),
                  N("oratory", "speak", "or + atory: the skill of giving speeches.")]),
 "art": art("ensign-thayer-map.jpg", "Map of the Gold Regions of California", "An old printed map with a decorated border. It shows California, North America and South America, and long columns of small print at the bottom.",
            "This is a real map sold in New York in 1849 to people heading for the gold fields. It shows the routes by Panama and around Cape Horn, and the small print gives travel tips. Its own text says the Cape Horn voyage was about 18,000 miles and took nearly five months. Other sources from the time give different numbers.",
            "Ensigns & Thayer", "1849", C + "Map_Of_The_Gold_Regions_Of_California,_Showing_the_Routes_via_Chagres_and_Panama,_Cape_Horn,_etc._..._Published_by_Ensigns_%26_(IA_dr_map-of-the-gold-regions-of-california-showing-the-routes-via-chagres-and-p-3442000).jpg",
            "Public domain (David Rumsey Map Collection, via Wikimedia Commons)", "Tap to learn about this map"),
 "virtue": {"name": "loyalty", "kind": "sort", "title": "Loyalty or not?", "intro": "This week's virtue is loyalty: sticking with a person or a promise, even when it costs you something. Sort these everyday examples.",
   "items": [{"t": "You keep a friend's secret, even when others tease you to tell.", "ok": True, "why": "You stay true to your friend when it would be easier not to."},
             {"t": "You go along with friends who are being unkind to someone.", "ok": False, "why": "Going along is not loyalty. A loyal friend helps friends do the right thing."},
             {"t": "You keep a promise to help, even after a better plan comes up.", "ok": True, "why": "You stick with your word when it costs you."},
             {"t": "You stay with your team after a hard loss.", "ok": True, "why": "Loyalty shows most when things go badly."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Today you meet Jack, who is twelve, and Praiseworthy, the butler. Before you read, a funny poem about a silly voyage in a sieve. Listen for the tone: how sure the travelers sound, and what you can see that they cannot."},
  "words": {"text": "Find the aud and or roots in new words, and spot the phrases that tell where. In the game, weigh six more words. Watch for fool's gold: some words only look like they have a root."},
  "reading": {"text": "Read Chapter 1. Watch for Jack's problem at home and what he wants to do about it. Then look for the moment he chooses his partner. It happens in front of the captain."},
  "assignment": {"text": "Three questions about Chapter 1. Then draft your adventure plan in full sentences. Use the frames if you get stuck. Your hero needs one clear problem."}},
 "how": [DOL, POEM, RW,
  {"match": "Grammar", "do": ["Read the phrases from Chapter 1.", "Tap the three phrases in the sentence.", "Write your own sentence in the box."], "why": "Phrases that tell where help a reader see the scene."},
  {"match": "Morphology", "do": ["Read what aud and or mean.", "Type the missing root in each word.", "Tap Check It."], "why": "Spotting a root in a new word gives you a head start on its meaning."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Write a sentence with two of the words."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Say each word and find the loud syllable.", "Read the Gold Rush words too.", "Tap every place name in the sentence."], "why": "Knowing the loud syllable helps you spell the quiet ones."},
  rh(1), dict(WGRD, why="An adventure has a problem, a goal and a cost. Spotting them helps you follow the plot.", use="You will use it in the reading questions."),
  WS(2)],
 "glossary": [{"word": "butler", "in": "Read: Chapter 1", "meaning": "the head servant in a large house"},
              {"word": "contrast", "in": "What Good Readers Do", "meaning": "a big difference between two things placed side by side"}],
 "hints": {"aud": HINT["aud"], "or": HINT["or"]},
 "game": game(2, [N("audiologist", "hear", "aud + io + logist: a doctor who tests how well you hear."), N("laboratory", "fool", "No root here. It comes from labor, which means work: a place where scientists work.", "Is a laboratory about speaking? Look for a smaller word inside."),
                  N("oratorical", "speak", "or + atorical: sounding like a speech."), N("order", "fool", "No root here. Order comes from a Latin word for a row.", "Does order mean speaking?"),
                  N("auditioned", "hear", "aud + itioned: tried out while someone listened."), N("oracle", "speak", "or + acle: in old stories, someone who spoke wise words.")]),
 "art": art("lane-boston-harbor.jpg", "Boston Harbor", "A painting of Boston Harbor at sunset: a small steamboat with a smokestack and paddle box, tall sailing ships, and the city low on the horizon.",
            "Fitz Henry Lane painted Boston Harbor in 1854, five years after the novel's ship leaves it. Find the steamboat with its smokestack among the sailing ships. In the novel, the Lady Wilma is both: a sailing ship with paddlewheels and a smokestack.",
            "Fitz Henry Lane", "1854", C + "Fitz_Henry_Lane_-_Boston_Harbor_-_Google_Art_Project.jpg", "Public domain (via Wikimedia Commons)"),
 "virtue": {"name": "loyalty", "kind": "log", "options": [
   {"t": "Jack tells the captain, “We're partners, sir,” and picks the coal bunkers over the job of ship's boy."},
   {"t": "Praiseworthy keeps Jack's plan a secret and goes with him, paying with his own savings."},
   {"t": "Aunt Arabella will not let her servants go: “they are like members of the family.”"}],
   "line": "Tap the most loyal moment. Then tell why in one sentence.", "placeholder": "This is the most loyal because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Someone stole Jack and Praiseworthy's money, and the thief is on the ship. Before you read, predict: how could a butler catch a thief with no proof?"},
  "words": {"text": "Use the roots to work out new words, and put phrases where they belong. In the game, weigh six more words. One of them looks like a hear word, but it isn't."},
  "reading": {"text": "Read Chapter 2. At the first pause, guess how a pig could catch a thief. At the second, say when you figured out the trick, or how the book fooled you."},
  "assignment": {"text": "Three questions about Praiseworthy's plan and the thief. Then revise your adventure plan with the checklist, and add one thing that isn't what it seems."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read the six words.", "Break each place name into syllables and mark the loud one.", "Write your Gold Rush sentence in the box."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Read the two new words and how the roots explain them.", "Tap a word, then tap its meaning.", "Match all four."], "why": "Roots let you guess a new word before you look it up."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Read the stacked phrases.", "Type the word from the bank that fits each sentence.", "Tap Check My Work."], "why": "Stacked phrases put the reader right in the scene."},
  rh(2), dict(WGRD, why="An adventure needs obstacles. Watching how the hero gets past one is half the fun.", use="You will use it in reading question 1."),
  WS(3)],
 "glossary": [{"word": "obstacle", "in": "What Good Readers Do", "meaning": "something that stands in the way"},
              {"word": "heist", "in": "Read: Chapter 2", "meaning": "a story about a robbery and a clever plan"}],
 "hints": {"under": ["Where would rain come through?", "The canvas is above them.", "It means below."], "beside": ["He is next to something.", "Not on it, not in it.", "It starts with be."],
           "Across": ["They go from one side to the other.", "Start with a capital letter.", "It starts with A."], "inside": ["The nugget is hidden in something.", "In the boot.", "in + side"]},
 "game": game(3, [N("audio", "hear", "aud + io: sound you can hear."), N("audacious", "fool", "Fool's gold! It comes from a Latin word for bold, not hear. Audacious means boldly daring.", "It starts with aud, but does it mean hearing? Think about bold."),
                  N("orator", "speak", "or + ator: a skilled speaker."), N("organ", "fool", "No root here. Organ comes from a Greek word for tool.", "Is an organ about speaking?"),
                  N("auditory", "hear", "aud + itory: having to do with hearing."), N("oratorio", "speak", "A long piece of music with singing, first sung in a prayer hall. Its root means speak or pray.")]),
 "art": art("currier-way-they-go.jpg", "The Way They Go to California", "A black-and-white comic print: a crowded sailing ship, an air-ship and a rocket overhead, a man falling from a parachute, and a crowd on a dock waving picks and shovels.",
            "A comic print sold in New York in 1849, the year the novel begins. The artist pokes fun at the rush: an air-ship, a rocket, a man under a parachute, and a crowd on the dock shouting that they have paid and still can't get aboard. Fleischman's novel jokes about the same rush.",
            "N. Currier", "1849", C + "The_way_they_go_to_California_-_lith._%26_pub._by_N._Currier._LCCN91481165.jpg", "Public domain (Library of Congress, via Wikimedia Commons)", "Tap to learn about this print"),
 "virtue": {"name": "loyalty", "kind": "meter", "title": "The loyalty meter", "intro": "Think about one moment from Chapter 2.",
   "moment": "Praiseworthy has the idea for the coal-dust trick. But he tells the captain, “Master Jack here has hit upon a scheme to expose the rascal.” Jack only got the pig dusty.",
   "ask": "How loyal is Praiseworthy to his partner here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He shows this much because…",
   "take": "Mason's take: very loyal. He shares the credit so his young partner can stand tall."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "Last day of the week. A playful poem with a trick hidden inside it, a little like Praiseworthy's pig. Listen for how a friendly tone can hide what someone really wants."},
  "words": {"text": "Explain aud and or in your own words, and tell why writers use phrases that tell where. In the game, weigh the last six words of the week. Two are fool's gold."},
  "reading": {"text": "Read Chapter 3: a letter home, and a ship in trouble. Watch Captain Swain's choice. Then trace the whole week: the problem, the obstacle, and the hard choice. What is at stake now?"},
  "assignment": {"text": "Three questions, the last one about all three chapters. Then submit your adventure plan: hero, problem, setting and stakes. Copy your work and paste it into Canvas."}},
 "how": [DOL, POEM, RW,
  {"match": "Morphology", "do": ["Explain the two roots in your reading journal.", "Type the word that fits each sentence.", "Tap Check My Work."], "why": "Explaining a root shows you really know it."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and say which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right explanation in each pair.", "Answer the question in your reading journal."], "why": "Explaining a rule shows you can use it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Tap the right spelling in each pair."], "why": "Syllables make long words easier to spell."},
  rh(3), dict(WGRD, why="Synthesizing means putting the pieces of the week together into one idea.", use="You will use it in reading question 3."),
  WS(4)],
 "glossary": [{"word": "hawser", "in": "Read: Chapter 3", "meaning": "a thick rope for towing or tying up a ship"},
              {"word": "theme", "in": "What Good Readers Do", "meaning": "a big idea about life that a story shows"}],
 "hints": {"audible": ["The word means can be heard.", "It starts with aud.", "aud + ible"], "oration": ["A formal speech.", "It starts like orator.", "or + ation"],
           "audience": ["The people listening.", "It starts with aud.", "aud + ience"], "oral": ["Spoken, not written.", "Four letters.", "or + al"]},
 "game": game(4, [N("audiovisual", "hear", "audio + visual: something you hear and see."), N("odor", "fool", "No root here. Odor is a Latin word for smell.", "Is an odor about speaking?"),
                  N("orally", "speak", "or + al + ly: by speaking."), N("auditorium", "hear", "aud + itorium: a big room for hearing a show."),
                  N("ordinary", "fool", "No root here. Ordinary comes from a Latin word for order, a row.", "Does ordinary have to do with speaking?"),
                  N("oratory", "speak", "or + atory: the skill of giving speeches.")]),
 "art": art("lane-becalmed.jpg", "Becalmed off Halfway Rock", "A painting of sailing ships sitting still on a glassy sea at dawn, with a small rock island between them and a man rowing a little boat.",
            "Fitz Henry Lane painted this calm in 1860 near Halfway Rock, off the coast of Massachusetts. Not a breath of wind fills the sails. In Chapter 3, a square-rigger sits like this near the equator for a week, far from here.",
            "Fitz Henry Lane", "1860", C + "Fitz_Henry_Lane,_Becalmed_off_Halfway_Rock,_1860,_NGA_76213.jpg", "CC0 (National Gallery of Art, via Wikimedia Commons)"),
 "virtue": {"name": "loyalty", "kind": "best", "title": "The most loyal moment this week", "intro": "Look back at Chapters 1 to 3. Tap the moment you think shows loyalty the most.",
   "options": [{"t": "Jack picks the coal bunkers to stay with his partner (Chapter 1)."},
               {"t": "Praiseworthy gives Jack the credit for the coal-dust trick (Chapter 2)."},
               {"t": "In his letter home, Jack writes that Praiseworthy never takes credit for himself (Chapter 3)."}],
   "line": "Finish the sentence: This shows loyalty the most because…", "placeholder": "This shows loyalty the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the barrel scene from Chapter 1 out loud. Let the long sentences unfold slowly, the way Praiseworthy unfolds from the barrel. Keep his voice calm and dignified, right up to: All clear, Master Jack. When it sounds smooth, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
PAGE = {1: {'audible', 'audience', 'audition', 'oral', 'oration', 'oracle', 'orator', 'inaudible', 'auditorium'},
        2: {'inaudible', 'audio', 'auditory', 'oratory'}, 3: {'auditor', 'orifice', 'audible', 'audience', 'oration', 'oral'},
        4: {'inaudible', 'audible', 'oration', 'audience', 'oral'}}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s: sys.exit('%s: em dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload'):
        if bad in s: sys.exit('%s: %s' % (k, bad))
    if 'game' in v:
        for e in v['game']['nuggets']:
            if e['w'] in PAGE[k]: sys.exit('%s: game word %s is on that day\'s page' % (k, e['w']))
    json.dump(v, open('data/g5ela-25-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
