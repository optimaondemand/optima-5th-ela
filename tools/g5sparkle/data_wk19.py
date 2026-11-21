#!/usr/bin/env python3
"""Write data/g5ela-19-{1..4,fluency}.json (week 19, How I Became a Ghost Ch. 8-11), Nov 21 2026.
Every book line checked against planning docs/hbg_ocr.txt. Bethany's choices: hook "one bag",
calm tone, trip points Ch. 8 (Jonah: the blankets are safe) and Ch. 11 (Nita's gift), Footprints Forward,
winter paintings. Listen texts are Mason scripts (recorded later; no voicing this month)."""
import json
A = 'assets/art/hbg/'
GAME_LOOK = ("Isaac's family walks for days on a snowy road. In this game, each footprint in the snow holds a word. "
             "Pick the ending, -ive, -al or -ic, that turns it into a describing word, and the footprint lights up. "
             "Your walk keeps going all week.")
GAME_HOW = {"do": ["Read the word on the footprint.", "Say it with each ending.", "Tap the ending that makes a real describing word.", "Tap Next footprint."],
            "why": "These are the same three endings from Spelling, with new words. If you can build a word you have never practiced, you know the endings."}
def game(day, steps):
    return {"type": "footprints", "title": "Footprints Forward", "sub": "This week's word game · 6 footprints today", "after": "Spelling",
            "look": GAME_LOOK, "how": GAME_HOW, "doneLine": "Come back tomorrow for more." if day < 4 else "That is the whole week's walk. Well done.",
            "steps": [{"base": b, "end": e, "word": w, "why": y} for b, e, w, y in steps]}
def st(b, e, w, extra=''):
    return (b, e, w, 'Yes: %s + -%s = %s.%s' % (b, e, w, (' ' + extra) if extra else ''))
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Fix the second sentence out loud.", "Tap Check My Work to compare."],
       "why": "Commas after an opening phrase or clause tell the reader where to pause."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Read Think About It.", "Keep your answer in mind as you read."],
        "why": "Knowing who is speaking, and that it may not be the writer, helps you understand any poem or story."}
def virtue_how(job):
    return {"match": "Virtue Watch", "do": ["Read what perseverance means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def intro_how(ch):
    return {"match": "Chapter Introduction", "do": ["Read the chapter introduction below.", "Open your book and read %s." % ch, "Then do the Virtue Watch and the Read Like a Writer box below."]}
def think_how(ch, extra=None):
    return {"match": "Chapter Thinking", "do": ["Read %s first." % ch, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
            "why": "These questions check what happened and what it shows about the people on the road."}
def art(file, title, alt, look, creator, date, url, btn="Tap to learn about this painting"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": btn, "creator": creator, "date": date,
            "license": "Public domain (Wikimedia Commons)", "url": url}
SORT_MISS = {
 "brutal": "Find brute inside. The silent e drops, then -al: brutal.", "destructive": "Find destruct, from destroy. It takes -ive: destructive.",
 "expressive": "Find express inside. It takes -ive: expressive.", "heroic": "Find hero inside. It takes -ic: heroic.",
 "historic": "Find history inside. The y drops, then -ic: historic.", "personal": "Find person inside. It takes -al: personal.",
 "protective": "Find protect inside. It takes -ive: protective.", "seasonal": "Find season inside. It takes -al: seasonal.",
 "tragic": "Find tragedy inside. Its end changes, then -ic: tragic.",
 "creative": "Find create inside. The silent e drops, then -ive: creative.", "dramatic": "Find drama inside. It takes -ic, with a t: dramatic.",
 "national": "Find nation inside. It takes -al: national.", "poetic": "Find poet inside. It takes -ic: poetic.",
 "secretive": "Find secret inside. It takes -ive: secretive.", "supportive": "Find support inside. It takes -ive: supportive.",
 "survival": "Find survive inside. The silent e drops, then -al: survival.", "symbolic": "Find symbol inside. It takes -ic: symbolic.",
 "traditional": "Find tradition inside. It takes -al: traditional.",
 "active": "Find act inside. It takes -ive: active.", "angelic": "Find angel inside. It takes -ic: angelic.",
 "athletic": "Find athlete inside. The silent e drops, then -ic: athletic.", "cultural": "Find culture inside. The silent e drops, then -al: cultural.",
 "inventive": "Find invent inside. It takes -ive: inventive.", "massive": "Find mass inside. It takes -ive: massive.",
 "musical": "Find music inside. It takes -al: musical.", "rhythmic": "Find rhythm inside. It takes -ic: rhythmic.",
 "tribal": "Find tribe inside. The silent e drops, then -al: tribal.",
}
MISS4 = {
 "national": "nation + -al. Nothing in the base changes.", "creative": "create: the silent e drops before -ive.",
 "descriptive": "describe → descriptive: the b changes to p. The base changes its spelling.", "narrative": "narrate: the silent e drops before -ive.",
 "expressive": "express + -ive. Nothing in the base changes.", "historic": "history → historic: the y drops. The base changes its spelling.",
 "personal": "person + -al. Nothing in the base changes.", "protective": "protect + -ive. Nothing in the base changes.",
 "supportive": "support + -ive. Nothing in the base changes.", "tragic": "tragedy → tragic: the end of the base changes.",
}
def pick(*ws, src=SORT_MISS): return {w: src[w] for w in ws}

D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "Isaac's family has been hiding in the swamp. In Chapter 8 they have to decide whether to stay or go, and what to take with them. Before you read, think about what people carry when they leave home. What someone holds on to can show how they see the world. That is your reading lens this week."},
  "words": {"text": "Two roots this week. One means life. One means breath. Long ago, people thought those were almost the same thing. Look for them in words you already know. Then three endings that turn a word into a describing word. In the footprint game, say each word out loud before you pick an ending."},
  "reading": {"text": "Read Chapter 8 of How I Became a Ghost in your book. Keep your reading lens in mind. Watch how Isaac's family meets new people on the road, and listen for what Mister Jonah tells Isaac about the blankets. When you finish, do the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 8, then the first step of a new piece of writing. When a question asks why, give the reason and the words from the book that show it. In the Writer's Workshop you are only planning today. A few notes are enough."}},
 "hook": {"q": "You have to leave home with one bag, and you will carry it for days. What goes in first?",
  "options": [{"t": "Food", "reply": "Smart. On the road in this book, food is never certain. Here is what Isaac's family does:"},
              {"t": "Something warm", "reply": "In winter, warmth matters most. In this chapter, even warm things are a hard choice. Here is what Isaac's family does:"},
              {"t": "Something that reminds me of home", "reply": "Many readers pick that. It shows what they hold on to. Here is what Isaac's family does:"}],
  "reveal": {"line": "Early the next morning we gathered our belongings and left the camp.", "cite": "Isaac, Chapter 8",
             "then": "As you read Chapter 8, watch what each person carries, and what it shows about how they see the world."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."],
   "why": "A character's perspective is built from what they have lived through. Watching what they do shows it.", "use": "You will use this when you answer the chapter questions."},
  DOL,
  {"match": "Morphology", "do": ["Read the two roots and what they mean.", "Tap a word, then tap its meaning.", "Match all four."], "why": "Isaac tells his story after his life has ended. These roots name life and breath."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the two sentences in the box.", "Think through the questions.", "Tap Now check your thinking.", "Tap the active sentence in each pair, then answer in the box."], "why": "Active voice tells the reader who did the action. In this book, that matters."},
  {"match": "Spelling", "do": ["Find the smaller word inside each describing word.", "Tap a word, then tap the column for its ending."], "why": "Spotting the base and the ending helps you spell long describing words."},
  think_how("Chapter 8"),
  {"match": "Workshop", "do": ["Think of a moment where danger and hope came together.", "In the box, note the conflict, what makes it tense, and one small hope.", "A few lines is enough."],
   "why": "This week you will write a scene where the tension keeps rising. Today you only choose it.", "use": "Tomorrow you will draft this moment."},
  virtue_how("sort the moments"), intro_how("Chapter 8")],
 "glossary": [{"word": "characterization", "in": "What Good Readers Do", "meaning": "how an author shows what a character is like"},
              {"word": "perspective", "in": "What Good Readers Do", "meaning": "the way a person sees what is happening, based on what they have lived through"}],
 "miss": pick("brutal", "destructive", "expressive", "heroic", "historic", "personal", "protective", "seasonal", "tragic"),
 "game": game(1, [st("effect", "ive", "effective"), st("emotion", "al", "emotional"), st("artist", "ic", "artistic"),
                  st("attract", "ive", "attractive"), st("origin", "al", "original"), st("magnet", "ic", "magnetic")]),
 "art": art("savrasov-winter-road.jpg", "Winter Road", "A painting of an empty country road in snow, with thin bare birch trees under a gray sky.",
            "Alexei Savrasov painted this snowy road in Russia in the 1870s. It is not Mississippi, but it shows the kind of winter road Isaac's family comes to in Chapter 8: wide, cold and empty, with no shelter in sight.",
            "Alexei Savrasov", "1870s", "https://commons.wikimedia.org/wiki/File:Зімовая_дарога._Аляксей_Саўрасаў.jpg"),
 "cards": [{"tab": "reading", "after": "Chapter Introduction", "title": "The real walk", "min": 2,
            "intro": "Isaac's story is made up, but the walk he is on really happened.",
            "items": [{"term": "1830", "meaning": "U.S. commissioners and Choctaw leaders signed the Treaty of Dancing Rabbit Creek. It gave up the Choctaw homeland in Mississippi.", "line": "", "cite": ""},
                      {"term": "1831 to 1833", "meaning": "Thousands of Choctaw people were moved west to what is now Oklahoma, in groups, many of them in winter.", "line": "", "cite": ""},
                      {"term": "The cold", "meaning": "The winter of 1831 was very hard. People on the real walk suffered from cold, hunger and sickness, and many died.", "line": "", "cite": ""}],
            "note": "The smallpox blankets are part of Tim Tingle's story. When you read, keep the book's events and the real history side by side."}],
 "virtue": {"name": "perseverance", "kind": "sort", "title": "Perseverance or not?", "intro": "You just read Chapter 8. Read each moment. Tap Perseverance or Not perseverance.",
   "items": [{"t": "Isaac's family leaves the swamp, walks all day and sleeps in the woods.", "ok": True, "why": "They keep going with nowhere certain to go. That is perseverance."},
             {"t": "Isaac's mother says, “I hate to leave our friends.”", "ok": False, "why": "Saying how you feel is honest, but it is not perseverance yet. Perseverance is what she does next: she walks on."},
             {"t": "Isaac carries Jumper for three days so he won't chase the walking people.", "ok": True, "why": "Carrying his dog day after day is hard, steady work. That is perseverance."},
             {"t": "For three days the family follows the walkers, hiding in the tree shadows, before they step out and ask to join.", "ok": True, "why": "They keep watching and waiting until it is safe. Patience that keeps going is perseverance."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Isaac's family is walking with Gabe, Ruth and their little girl, Nita. Nita is five, and she has something to ask Isaac. The poem today has an I in it, but that I is not the poet. Keep that in mind. A voice in a poem or a story can belong to someone the writer made."},
  "words": {"text": "You met the life root and the breath root. Now decide which one is hiding in each word. Some words carry both ideas. Then sort the describing words by their endings. Find the smaller word inside first. Then the footprint game has six new words to build."},
  "reading": {"text": "Read Chapter 9 in your book. Watch what Isaac promises, and what he does the next morning to keep that promise. Then read the Read Like a Writer sentence and notice how Isaac lets you inside his head. Finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 9, then a first draft. Write three to five sentences about the conflict you planned. Let the tension build, and do not solve the problem yet. Copy your work into Canvas when you finish."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap the lens you will use today.", "Watch who can see the ghost walkers and who cannot."], "why": "When two people look at the same thing, their perspectives show.", "use": "You will use this for the chapter questions."},
  DOL, POEM,
  {"match": "Morphology", "do": ["Ask: is this word about life or about breath?", "Tap a word, then tap its root.", "Match all four."], "why": "Finding the root tells you what a long word is about."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Look for was, were or by.", "Tap the sentence that hides who acted.", "Rewrite all three in the box."], "why": "A passive sentence can leave out who did the action. Noticing that makes you a sharper reader."},
  {"match": "Spelling", "do": ["Find the smaller word inside each describing word.", "Tap a word, then tap its column."], "why": "The ending a word takes often depends on its base."},
  think_how("Chapter 9"),
  {"match": "Workshop", "do": ["Look at your Day 1 notes.", "Write 3 to 5 sentences about the conflict.", "Start one sentence with a transition or a when clause, then a comma.", "Do not solve the problem yet."],
   "why": "Rising action means the tension climbs. Leaving it unsolved keeps your reader reading.", "use": "Next lesson you will revise this draft."},
  virtue_how("fill in your perseverance log"), intro_how("Chapter 9")],
 "glossary": [{"word": "speaker", "in": "Poetry Corner", "meaning": "the voice talking in a poem, which may not be the poet"},
              {"word": "perspective", "in": "What Good Readers Do", "meaning": "the way a person sees what is happening, based on what they have lived through"}],
 "miss": pick("creative", "dramatic", "national", "poetic", "secretive", "supportive", "survival", "symbolic", "traditional"),
 "game": game(2, [st("collect", "ive", "collective"), st("magic", "al", "magical"), st("scene", "ic", "scenic", "The silent e drops."),
                  st("impress", "ive", "impressive"), st("parent", "al", "parental"), st("organ", "ic", "organic")]),
 "art": art("klever-spruce-sunset.jpg", "Winter Sunset in a Spruce Forest", "A painting of a snowy spruce forest with a warm orange sunset glowing between the dark trunks.",
            "Julius Klever painted this forest in Russia in 1889. It is far from Isaac's road, but it feels like Chapter 9: the cold all around, and one warm light where the families gather at the end of the day.",
            "Julius Klever", "1889", "https://commons.wikimedia.org/wiki/File:Зимний_закат_в_еловом_лесу.jpg"),
 "cards": [{"tab": "reading", "after": "Chapter Introduction", "title": "Choctaw words in Chapters 8 and 9", "min": 1,
            "intro": "Isaac tells his story in English, but some Choctaw words stay in it.",
            "items": [{"term": "Halito", "meaning": "Hello. Isaac's family says it to Nita when they meet her in Chapter 8.", "line": "“Halito, Nita!” we all said.", "cite": "Chapter 8"},
                      {"term": "Yakoke", "meaning": "Thank you. Isaac explains it in Chapter 9.", "line": "(Yakoke means “thank you” in Choctaw.)", "cite": "Chapter 9"},
                      {"term": "Pashofa", "meaning": "Choctaw corn soup, made with soft corn in milk.", "line": "We had Choctaw corn soup for supper that night. Pashofa, we call it.", "cite": "Chapter 9"}],
            "note": "The narrator does not say these words aloud. Choctaw has its own sounds, and we would rather not teach them wrong."}],
 "virtue": {"name": "perseverance", "kind": "log", "title": "My perseverance log", "intro": "Chapter 9 has moments where people keep going. Tap the one you think took the most perseverance.",
   "options": [{"t": "Isaac stands up at the campfire and promises Nita, “I will take care of you.”"},
               {"t": "Isaac cuts two pieces from his own blanket and ties them on Nita's feet as shoes."},
               {"t": "The rain turns to ice, and the families walk all day without stopping, with nothing to eat."}],
   "line": "Finish the sentence: It took perseverance because…", "placeholder": "It took perseverance because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Chapter 10 is the coldest day of the walk. Mister Jonah warned Isaac it would be hard. As you read, notice the moment Isaac almost gives up, and the words that bring him back. Today you will reread one line closely. One sentence can hold a whole way of seeing the world."},
  "words": {"text": "Today you put the roots to work. In Spelling, the words are new. Build each describing word in your head before you place it. If the base ends in a silent e, check whether it stays or goes. The footprint game works the same way."},
  "reading": {"text": "Read Chapter 10 in your book. It is a hard chapter. Read the part where Isaac's father speaks to him twice: once for the story, and once to hear how his father says it. Then try the Read Like a Writer box, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 10. The last one looks back across Chapters 8, 9 and 10. Then revise your draft. Read it with the checklist first and fix what it shows you. Then add one sentence where everything is about to break."}},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap the root it belongs to.", "Match all four words."], "why": "If you know the root, you can work out a word you have never seen."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Tap the stronger rewrite in each pair.", "Replace the weak verbs in the box.", "Name the verb you chose and why."], "why": "One strong verb says more than a weak verb plus extra words."},
  {"match": "Spelling", "do": ["Build each describing word in your head first.", "Tap a word, then tap its column."], "why": "Long words get easier to spell when you see the base and the ending."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Reread the part where Isaac's father speaks to him.", "Ask what kind of person says that, at that moment."], "why": "Rereading one line slowly shows you things you missed the first time.", "use": "You will use this for question 2."},
  think_how("Chapter 10", "For question 3, use one detail from each chapter."),
  {"match": "Workshop", "do": ["Reread your draft with the checklist.", "Fix one thing it shows you.", "Add one sentence where everything is about to break."],
   "why": "Revising means making your draft stronger, not starting over.", "use": "Next lesson you will write the final version."},
  virtue_how("use the perseverance meter"), intro_how("Chapter 10")],
 "glossary": [{"word": "outlook", "in": "What Good Readers Do", "meaning": "a person's way of looking at life"}],
 "hints": {"smallpox": ["A dangerous sickness.", "In Chapter 8 the blankets carry it. It starts with small.", "small + pox"],
           "belongings": ["The things a family owns and carries.", "It ends with -ings.", "It starts with belong."],
           "sickness": ["Another word for illness.", "sick + an ending that makes a noun.", "It ends with -ness."],
           "refused": ["He said no, firmly.", "Past tense of refuse.", "It ends with -ed."],
           "vanished": ["They disappeared all at once.", "Past tense of vanish.", "It starts with van."]},
 "miss": pick("active", "angelic", "athletic", "cultural", "inventive", "massive", "musical", "rhythmic", "tribal"),
 "game": game(3, [st("decorate", "ive", "decorative", "The silent e drops."), st("region", "al", "regional"), st("acid", "ic", "acidic"),
                  st("select", "ive", "selective"), st("form", "al", "formal"), st("base", "ic", "basic", "The silent e drops.")]),
 "art": art("shishkin-winter.jpg", "Winter", "A painting of a deep pine forest buried in snow, with bent branches and drifts between the dark trunks.",
            "Ivan Shishkin painted this snowy forest in Russia in 1890. Isaac's road is in a different place, but Chapter 10 has this kind of snow: so thick that he cannot see the branches above him.",
            "Ivan Shishkin", "1890", "https://commons.wikimedia.org/wiki/File:Ivan_Shishkin_-_Winter.JPG"),
 "virtue": {"name": "perseverance", "kind": "meter", "title": "The perseverance meter", "intro": "Think about one moment from Chapter 10.",
   "moment": "Isaac's feet are bleeding and burning. His father tells him to keep his eyes on where he is going. From that moment on, Isaac refuses to look behind him.",
   "ask": "How much perseverance did Isaac show? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He showed this much because…",
   "take": "Mason's take: a lot. The pain did not stop, but Isaac kept walking. He says, “I was stronger than the pain.”"},
}
D[4] = {
 "listen": {
  "warmup": {"text": "This is the last day of the week. In Chapter 11, Nita gives Isaac a gift, and the chapter ends with a hard loss. Read it slowly. The poem today is spoken by a mother to her son. Listen for how her advice sounds like the words Isaac's father said in Chapter 10."},
  "words": {"text": "Last day with life and breath. Today you explain why one idea needed two roots. In Spelling, the words change in different ways when an ending is added. Sometimes a silent e drops. Sometimes the base changes more. Sometimes nothing changes. Look closely at the base each time."},
  "reading": {"text": "Read Chapter 11 in your book. Go slowly. Notice Nita's gift to Isaac, and how Isaac's family and friends take care of each other. Then put the week together with your lens: pick two people and compare how they see the same road. Finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 11, then your final piece. Write your conflict scene in five to seven sentences, and end while the tension is still high. Then write one sentence about what Isaac taught you about rising action. Copy your work and paste it into Canvas."}},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap the root it belongs to.", "Say out loud why each word fits its root."], "why": "Explaining a root out loud is how you know you own it."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Tap the version that takes responsibility.", "Read the last question carefully.", "Give one example of each in the box."], "why": "Choosing active or passive voice is choosing whether to say who did it."},
  {"match": "Spelling", "do": ["Find the base word inside.", "Decide: did an e drop, did the base change, or did nothing change?", "Tap a word, then tap its column."], "why": "Knowing how a base changes keeps you from misspelling long words."},
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap your lens for today.", "Pick two people from Chapters 8 to 11 to compare."], "why": "Putting the week together shows how each person's life shapes how they see the same road.", "use": "You will use this for question 2."},
  think_how("Chapter 11"),
  {"match": "Workshop", "do": ["Write your final scene, 5 to 7 sentences.", "End while the tension is still high.", "Add one sentence about what Isaac taught you."], "why": "Today you finish your scene and turn it in."},
  virtue_how("pick the strongest moment of the week"), intro_how("Chapter 11")],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "to put ideas from different parts together into one bigger idea"},
              {"word": "rising action", "in": "Writer", "meaning": "the part of a story where the problem grows and the tension climbs"}],
 "miss": pick("national", "creative", "descriptive", "narrative", "expressive", "historic", "personal", "protective", "supportive", "tragic", src=MISS4),
 "game": game(4, [st("instruct", "ive", "instructive"), st("globe", "al", "global", "The silent e drops."), st("ocean", "ic", "oceanic"),
                  st("possess", "ive", "possessive"), st("logic", "al", "logical"), st("patriot", "ic", "patriotic")]),
 "art": art("shishkin-wild-north.jpg", "In the Wild North", "A painting of a single tall pine tree heavy with snow, standing on a rocky cliff under a dark night sky.",
            "Ivan Shishkin painted this lone pine in 1891. It is not Isaac's Mississippi, but it fits Chapter 11: one quiet tree in the cold, standing still after a loss.",
            "Ivan Shishkin", "1891", "https://commons.wikimedia.org/wiki/File:Шишкин_И._И._(1891)_На_севере_диком.jpg"),
 "virtue": {"name": "perseverance", "kind": "best", "title": "The strongest moment of perseverance this week", "intro": "Look back at Chapters 8 to 11. Tap the moment you think shows the most perseverance.",
   "options": [{"t": "Isaac's family leaves the swamp and walks on, with nowhere certain to go."},
               {"t": "Isaac cuts pieces from his own blanket to make shoes for Nita."},
               {"t": "Isaac keeps walking on bleeding feet after his father's words."},
               {"t": "When Nita gives Isaac her blanket shoes, he takes them, then cuts her a new pair."},
               {"t": "Luke tells Isaac, “Whatever happens, we are strong.”"}],
   "line": "Finish the sentence: This shows the most perseverance because…", "placeholder": "This shows the most perseverance because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read this part of Chapter 10 out loud. First Isaac tells what happens. Then his father speaks, calm and sure. Let your voice change for the father's words, and give each short sentence its own beat. When it sounds smooth, record yourself and turn it in."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
for k, v in D.items():
    json.dump(v, open('data/g5ela-19-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote data/g5ela-19-%s.json' % k)
