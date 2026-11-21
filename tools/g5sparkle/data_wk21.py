#!/usr/bin/env python3
"""Write data/g5ela-21-{1..4,fluency}.json (week 21, How I Became a Ghost Ch. 16-19), Nov 21 2026.
Every book line checked against planning docs/hbg_ocr.txt. Bethany's choices: hook "Is good-bye ever final?"
(chi pisa lachike, on 21.2 where Ch. 17 is read), The Spyglass game, 1800s woods / river / night paintings,
virtue courage (the pages' own). Ch. 18 is Isaac's death: every line here is calm and plain.
Listen texts are Mason scripts (recorded later); Choctaw words are never in them."""
import json
A = 'assets/art/hbg/'
LOOK = ("Isaac sees what other people cannot see. In this game, a brass spyglass looks at one word at a time. "
        "First tap the root hiding inside it: vis or vid means see, and spect means look. The root lights up. "
        "Then tap what the word means. Every word you get adds a star to the spyglass.")
HOW = {"do": ["Look at the word in the spyglass.", "Tap the root you find inside it.", "Tap what the word means.", "Tap Next word."],
       "why": "If you can spot a root, you can work out a long word you have never seen."}
def W(w, root, part, opts, ok, why): return {"w": w, "root": root, "part": part, "opts": opts, "ok": ok, "why": why}
def game(day, words):
    return {"type": "spy", "title": "The Spyglass", "sub": "This week's word game · 5 words today", "after": "Spelling",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow for more." if day < 4 else "That is the whole week's sky. Well done.", "words": words}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Find the pronoun that could mean two people in the second.", "Fix it out loud, then tap Check My Work."],
       "why": "A pronoun like he or they should point to only one person or group."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Find the line or picture that comes back.", "Read Think About It and keep your answer in mind."],
        "why": "When a poet repeats something, each new picture adds to the idea. That is how a theme grows."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what courage means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def ih(ch): return {"match": "Chapter Introduction", "do": ["Read the chapter introduction below.", "Open your book and read %s." % ch, "Then do the Virtue Watch and the Read Like a Writer box below."]}
def th(ch, extra=None): return {"match": "Chapter Thinking", "do": ["Read %s first." % ch, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
                               "why": "These questions check what happened and what it shows about the people in the story."}
def art(file, title, alt, look, creator, date, url, lic="Public domain (Wikimedia Commons)"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": "Tap to learn about this painting", "creator": creator, "date": date, "license": lic, "url": url}
MISS = {"its": "Its shows ownership, with no apostrophe: the wagon and its wheels.", "it's": "It's is two words squeezed: it is. Try saying it is in the sentence.",
        "their": "Their shows ownership: their wagon.", "there": "There points to a place: over there.", "they're": "They're is two words squeezed: they are.",
        "whose": "Whose asks who owns something: whose blanket?", "who's": "Who's is two words squeezed: who is.",
        "capital": "A capital is a city where a government meets. It names a place.", "council": "A council is a group of leaders. It names a thing.",
        "effect": "An effect is a result. It names a thing (a noun).", "affect": "To affect is to change or influence. It is an action (a verb).",
        "principle": "A principle is a rule or belief. It names a thing.", "principal": "A principal is the chief or head of something.",
        "accept": "To accept is to take what is offered. It is an action (a verb).", "led": "Led is the past of lead: she led the way. It is an action."}
def pick(*ws): return {w: MISS[w] for w in ws}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "In Chapter 16, Nani Humma catches Isaac and Joseph talking by the creek at night, and the Choctaw Council learns about Naomi. Your reading lens this week is theme. Watch for things that come back in the story, like blankets and footprints. Each time, ask what they mean now."},
  "words": {"text": "Two roots this week, and both are about sight. One means see. One means look. Then words that sound the same but are spelled differently. A spell checker will not catch them. In the spyglass game, find the root first, then the meaning."},
  "reading": {"text": "Read Chapter 16 of How I Became a Ghost in your book. Watch what the boys tell Nani Humma, and what the council decides to do about Naomi. Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 16. Then a new piece of writing begins. This week you will go back to a story you wrote and make the pictures in it stronger. Today you only choose three moments to work on."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."],
   "why": "A theme grows when the same picture comes back and means a little more each time.", "use": "You will use this when you answer the chapter questions."},
  DOL,
  {"match": "Morphology", "do": ["Read the two roots and what they mean.", "Tap a word, then tap its meaning.", "Match all four."], "why": "This book is about seeing what others cannot. These roots name seeing and looking."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Find where the two halves meet.", "Think through the questions.", "Tap Now check your thinking.", "Tap the compound sentence in each pair, then write in the box."], "why": "Joining ideas in different ways changes how a sentence sounds and what it says."},
  {"match": "Spelling", "do": ["Read each word and think of its meaning.", "Ask what job it does in a sentence.", "Tap a word, then tap its column."], "why": "Words that sound the same are spelled by meaning, not by sound."},
  th("Chapter 16"),
  {"match": "Workshop", "do": ["Open a story you wrote in week 18 or 19.", "Pick three moments that need stronger pictures.", "In the box, copy each one and note what you want to add."],
   "why": "Imagery helps a reader see, hear and feel a moment. Today you only choose.", "use": "Tomorrow you will revise the first moment."},
  vh("sort the moments"), ih("Chapter 16")],
 "glossary": [{"word": "repetition", "in": "What Good Readers Do", "meaning": "saying or showing the same thing more than once"},
              {"word": "theme", "in": "What Good Readers Do", "meaning": "a big idea a book shows about people, said as a full sentence"}],
 "miss": pick("capital", "council", "it's", "its", "their", "there", "they're", "who's", "whose"),
 "game": game(1, [W("visitor", "vis", "vis", ["someone who comes to see you", "someone who writes you a letter", "someone who leads a group"], 0, "Yes. A visitor comes to see you. vis = see."),
                  W("respect", "spect", "spect", ["to forget about someone", "to look up to someone", "to run away from someone"], 1, "Yes. To respect someone is to look up to them. spect = look."),
                  W("visual", "vis", "vis", ["about sounds", "about seeing", "about smells"], 1, "Yes. A visual is something you see, like a picture or a map."),
                  W("inspector", "spect", "spect", ["a person who looks closely to check things", "a person who sings in a choir", "a person who drives a wagon"], 0, "Yes. An inspector looks closely at things to check them."),
                  W("vista", "vis", "vis", ["a loud noise", "a wide view you can see", "a kind of soup"], 1, "Yes. A vista is a wide view, like a valley seen from a hill.")]),
 "art": art("durand-in-the-woods.jpg", "In the Woods", "A painting of a deep forest with tall trees, a thin path and light coming through the leaves.",
            "Asher Durand painted this forest in New York in 1855. It is far from Isaac's road, but it fits Chapter 16: the boys meet behind a big tree by the creek, and the councilwomen head into the woods to look for berries.",
            "Asher Brown Durand", "1855", "https://commons.wikimedia.org/wiki/File:In_the_Woods_MET_co.ap.95.13.1_1.jpg", "CC0 (The Metropolitan Museum of Art, via Wikimedia Commons)"),
 "virtue": {"name": "courage", "kind": "sort", "title": "Courage or not?", "intro": "You just read Chapter 16. Read each moment. Tap Courage or Not courage.",
   "items": [{"t": "Isaac tells Nani Humma his biggest secret: “I will soon be a ghost.”", "ok": True, "why": "He tells the truth to someone who could send him away. That takes courage."},
             {"t": "Caught in the woods, Isaac hangs his head and says nothing.", "ok": False, "why": "Being caught is not a choice. What he does next, telling the whole story, is the brave part."},
             {"t": "The councilwomen walk close to the soldiers and wave, so they can look for Naomi.", "ok": True, "why": "They get close to dangerous men on purpose to help a girl. That is courage."},
             {"t": "The councilmen are angry when they hear Naomi was taken.", "ok": False, "why": "Feeling angry is not courage yet. Courage is what a person does about it."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "In Chapter 17, Isaac goes back to visit his family. The poem today repeats one line, and a new picture follows it each time. Watch what the second picture adds. Then think about something that keeps coming back in Isaac's story."},
  "words": {"text": "Today you decide which root each word carries: see, or look. Then sort the sound alike words by the job they do. Does the word show who owns something, name a thing, or squeeze two words together? Then five new words in the spyglass."},
  "reading": {"text": "Read Chapter 17 in your book. Watch how Isaac spends the day with his family, and what he says when it is time to go. Then read the Read Like a Writer sentence about Nani Humma, and finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 17, then your first revision. Take the first moment from your plan. Add one detail you can see, hear, smell or feel, and one comparison. Show the old version first, then the new one."}},
 "hook": {"q": "When someone you love leaves for a long time, what do you say?",
  "options": [{"t": "Good-bye", "reply": "That is what most of us say. Isaac's family says something different. Here is why:"},
              {"t": "See you soon", "reply": "That is close to what Isaac's family says. Here is how Isaac explains it:"},
              {"t": "Nothing, just a hug", "reply": "Sometimes a hug says it all. Isaac's family has words for it too. Here is what Isaac says:"}],
  "reveal": {"line": "Choctaws never say “good-bye.” There is no word for it.", "cite": "Isaac, Chapter 17",
             "then": "As you read Chapter 17, find what Choctaws say instead, and what it means."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap the lens you will use today.", "Watch for things from earlier chapters that come back in this one."], "why": "A theme is built from things that return, not from one moment.", "use": "You will use this for question 3."},
  DOL, POEM,
  {"match": "Morphology", "do": ["Ask: does this word have see or look in it?", "Tap a word, then tap its root and meaning.", "Match all four."], "why": "vis and vid lean toward what is seen. spect leans toward looking."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Count the halves that could stand alone.", "Tap the complex sentence in each pair.", "Label the three sentences in the box and explain."], "why": "Two halves that can stand alone make a compound sentence. One makes it complex."},
  {"match": "Spelling", "do": ["Read each word.", "Ask: owner, thing, or two words squeezed?", "Tap a word, then tap its column."], "why": "Meaning picks the spelling, not sound."},
  th("Chapter 17"),
  {"match": "Workshop", "do": ["Copy the first moment from your plan.", "Add one detail you can see, hear, smell or feel.", "Add one comparison with like or as."], "why": "One strong detail can put a reader inside the moment.", "use": "Next lesson you will revise the second moment."},
  vh("fill in your courage log"), ih("Chapter 17")],
 "glossary": [{"word": "image", "in": "What Good Readers Do", "meaning": "a picture a writer puts in your mind with words"},
              {"word": "theme", "in": "What Good Readers Do", "meaning": "a big idea a book shows about people, said as a full sentence"}],
 "miss": pick("effect", "it's", "its", "principle", "their", "there", "they're"),
 "game": game(2, [W("revise", "vis", "vis", ["to look at again and make better", "to throw away", "to read out loud"], 0, "Yes. To revise is to see your work again and improve it."),
                  W("spectacles", "spect", "spect", ["a kind of boots", "glasses that help you look", "a loud song"], 1, "Yes. Spectacles is an old word for glasses."),
                  W("evident", "vid", "vid", ["hard to find", "easy to see", "very old"], 1, "Yes. Something evident is easy to see. vid = see."),
                  W("prospect", "spect", "spect", ["something you look forward to", "a broken tool", "a kind of tree"], 0, "Yes. A prospect is something ahead that you look toward."),
                  W("supervise", "vis", "vis", ["to sleep late", "to watch over other people's work", "to cook a meal"], 1, "Yes. To supervise is to watch over others as they work.")]),
 "art": art("church-twilight-wilderness.jpg", "Twilight in the Wilderness", "A painting of a fiery red and orange sunset sky over dark hills, a river and trees.",
            "Frederic Edwin Church painted this sunset in 1860 from his sketches of the northern woods. It is far from Isaac's road, but it matches the end of Chapter 17: “Soon the sky streaked red and the sun dipped below the hills.”",
            "Frederic Edwin Church", "1860", "https://commons.wikimedia.org/wiki/File:Twilight_in_the_Wilderness_by_Frederic_Edwin_Church_(3).jpg"),
 "cards": [{"tab": "reading", "after": "Chapter Introduction", "title": "Choctaw words in Chapters 16 and 17", "min": 1,
            "intro": "Isaac tells his story in English, but some Choctaw words stay in it.",
            "items": [{"term": "Yakoke", "meaning": "Thank you. Isaac says it to Nani Humma in Chapter 16.", "line": "", "cite": "Chapter 16"},
                      {"term": "Pashofa", "meaning": "Choctaw corn soup. Isaac's family eats it together at noon.", "line": "It was the best bowl of corn soup I'd ever had.", "cite": "Chapter 17"},
                      {"term": "Chi pisa lachike", "meaning": "What Choctaws say instead of good-bye: I will see you again, in the future.", "line": "", "cite": "Chapter 17"}],
            "note": "The narrator does not say these words aloud. Choctaw has its own sounds, and we would rather not teach them wrong."}],
 "virtue": {"name": "courage", "kind": "log", "title": "My courage log", "intro": "In Chapter 17, tap the moment you think shows the most courage.",
   "options": [{"t": "Isaac tells Nani Humma that Naomi might not want to go, even though it means disagreeing with his best friend."},
               {"t": "Joseph sneaks into camp before sunrise to take Isaac to see his family."},
               {"t": "Luke gives Joseph his blowgun and tells him to take care of Isaac."}],
   "line": "Finish the sentence: This shows the most courage because…", "placeholder": "This shows the most courage because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Chapter 18 is the hardest chapter in the book. It is the chapter Isaac told you about on the first page. Read it slowly. If it feels heavy, that is all right. Today you will reread one passage and trace an idea back to where you first met it."},
  "words": {"text": "Put the sight roots to work today. Then the sound alike words again, sorted a new way: is the word a thing, an action, or two words squeezed? Say it in a sentence to check. Then five new words in the spyglass."},
  "reading": {"text": "Read Chapter 18 in your book. Isaac says good-bye to his mother, and then the chapter changes everything. Notice the words from his father that Isaac remembers. Then try the Read Like a Writer box, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 18. The last one looks back across Chapters 16, 17 and 18. Then revise with the checklist, and work on your second moment. Choose a comparison that fits the feeling of the moment."}},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Read each meaning.", "Tap a word, then tap its meaning.", "Match all four words."], "why": "If you know the root, you can work out a word you have never seen."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Read both versions in each pair.", "Tap the one whose shape fits the meaning.", "Write the four sentences in the box."], "why": "Because and although show how ideas connect. And only lists them."},
  {"match": "Spelling", "do": ["Say the word in a sentence.", "Ask: thing, action, or two words squeezed?", "Tap a word, then tap its column."], "why": "Knowing a word's job tells you which spelling to use."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Reread the part where Isaac remembers his father's words.", "Think back to Chapter 10, where you first heard them."], "why": "An idea that comes back late in a book usually means more the second time.", "use": "You will use this for question 2."},
  th("Chapter 18", "For question 3, use one detail from each chapter."),
  {"match": "Workshop", "do": ["Check Moment 1 with the checklist.", "Revise Moment 2 with a comparison.", "Make the comparison fit the feeling."], "why": "Revising means making a moment stronger, not starting over.", "use": "Next lesson you will write the final version."},
  vh("use the courage meter"), ih("Chapter 18")],
 "glossary": [{"word": "symbol", "in": "What Good Readers Do", "meaning": "a thing in a story that stands for a bigger idea"}],
 "hints": {"terrified": ["Very, very scared.", "A councilwoman says this about Naomi.", "It starts with terr."],
           "stickball": ["A Choctaw game.", "Young ghosts hold a bat for it.", "stick + ball"],
           "mourning": ["Deep sadness after a death.", "It turns a sunny day quiet.", "It sounds like morning."],
           "suffering": ["Pain or hardship.", "Nani Humma asks if it will ever be over.", "It ends with -ing."],
           "courage": ["Being brave.", "Isaac walks to the campfire with it.", "It starts with cour."]},
 "miss": pick("affect", "council", "accept", "effect", "it's", "led", "principle", "they're"),
 "game": game(3, [W("television", "vis", "vis", ["pictures you can see from far away", "a kind of letter", "a tool for digging"], 0, "Yes. Tele means far. Television lets you see things far away."),
                  W("expect", "spect", "spect", ["to look forward to something happening", "to forget something", "to fix something"], 0, "Yes. To expect is to look ahead for something you think will happen."),
                  W("visibility", "vis", "vis", ["how loud it is", "how far you can see", "how cold it is"], 1, "Yes. On a foggy day, visibility is low."),
                  W("aspect", "spect", "spect", ["one side of something you look at", "a kind of bird", "the end of a story"], 0, "Yes. An aspect is one side of a thing, the way it looks from one place."),
                  W("visualize", "vis", "vis", ["to picture something in your mind", "to sing quietly", "to walk fast"], 0, "Yes. To visualize is to see a picture in your head.")]),
 "art": art("duncanson-blue-hole.jpg", "Blue Hole, Little Miami River", "A painting of a calm pool in a river, surrounded by green trees, with three small figures on the rocks.",
            "Robert S. Duncanson painted this quiet river in Ohio in 1851. It is far from Isaac's road, but it fits Chapter 18: the snow has melted, the sun shines, and the walkers rest by an old pine near the river.",
            "Robert S. Duncanson", "1851", "https://commons.wikimedia.org/wiki/File:Robert_Duncanson_-_Blue_Hole,_Little_Miami_River.JPG"),
 "virtue": {"name": "courage", "kind": "meter", "title": "The courage meter", "intro": "Think about one moment from Chapter 18.",
   "moment": "Isaac watches his family grieve. He wants to float back into his body and tell them he is all right. Then he remembers his father's words about the bloody footprints, and he does not go back.",
   "ask": "How much courage did Isaac show? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He showed this much because…",
   "take": "Mason's take: a lot. Going back would have felt easier. Isaac kept his eyes on where he was going, the way his father taught him in Chapter 10."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "This is the last day of the week. In Chapter 19, Isaac learns what he can and cannot do as a ghost, and he goes looking for Naomi. The poem today asks the same question twice. Notice how you can know something is there, even when you cannot see it."},
  "words": {"text": "Last day with the sight roots. Explain the difference between looking and seeing. Then the academic pairs that trip up even grown writers: affect and effect, principal and principle. Then the last five words in the spyglass."},
  "reading": {"text": "Read Chapter 19 in your book. Watch what Isaac discovers in the soldiers' camp, and listen to what Naomi says when he whispers her name. Then put the week together with your lens: name the theme. Finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 19, then your final revised story: five to seven sentences with at least one detail you can sense and one comparison. Then one sentence about what imagery adds. Copy your work and paste it into Canvas."}},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap its meaning.", "Say out loud how a spectator and a visionary are different."], "why": "Explaining two close words out loud shows you know them."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Tap the passage with better variety in each pair.", "Find a place in this week's chapters with short and long sentences.", "Copy two sentences and explain in the box."], "why": "Mixing short and long sentences controls where a reader slows down."},
  {"match": "Spelling", "do": ["Read each word.", "Match it to its meaning.", "Tap a word, then tap its column."], "why": "These pairs sound alike but mean different things in an essay."},
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap your lens for today.", "Pick one picture that came back this week and say what it shows about people."], "why": "Naming a theme means saying what the book shows, in a full sentence.", "use": "You will use this for question 3."},
  th("Chapter 19"),
  {"match": "Workshop", "do": ["Write the full revised story, 5 to 7 sentences.", "Include one detail you can sense and one comparison.", "Add one sentence about what imagery adds."], "why": "Today you finish your revision and turn it in."},
  vh("pick the strongest moment of the week"), ih("Chapter 19")],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "to put ideas from different parts together into one bigger idea"}],
 "miss": pick("affect", "effect", "principal", "principle"),
 "game": game(4, [W("retrospect", "spect", "spect", ["looking back at the past", "a kind of map", "a loud cheer"], 0, "Yes. Retro means back. In retrospect means looking back."),
                  W("spectrum", "spect", "spect", ["the range of colors you can look at in a rainbow", "a heavy box", "a quiet song"], 0, "Yes. A spectrum is the band of colors you see in a rainbow."),
                  W("envision", "vis", "vis", ["to picture something in your mind", "to close a door", "to count money"], 0, "Yes. To envision is to see a future picture in your mind."),
                  W("advise", "vis", "vis", ["to tell someone what you think they should do", "to hide something away", "to build a fence"], 0, "Yes. To advise is to share how you see a problem."),
                  W("spectacular", "spect", "spect", ["boring and plain", "amazing to look at", "small and hidden"], 1, "Yes. Something spectacular is amazing to look at.")]),
 "art": art("blakelock-moonlight.jpg", "Moonlight", "A dark painting of trees against a glowing moonlit sky, with moonlight on still water.",
            "Ralph Albert Blakelock painted this moonlit night around 1885 to 1890. It is not Isaac's road, but it feels like Chapter 19: night by the river, the soldiers' fire burning low, and frogs calling from the water.",
            "Ralph Albert Blakelock", "around 1885 to 1890", "https://commons.wikimedia.org/wiki/File:Ralph_Albert_Blakelock_-_Moonlight_-_54.48_-_Indianapolis_Museum_of_Art.jpg"),
 "virtue": {"name": "courage", "kind": "best", "title": "The strongest moment of courage this week", "intro": "Look back at Chapters 16 to 19. Tap the moment you think shows courage the most.",
   "options": [{"t": "Isaac tells Nani Humma his biggest secret."},
               {"t": "Isaac says Naomi might not want to go, even though Joseph disagrees."},
               {"t": "Joseph fights the wolf to save Isaac."},
               {"t": "Isaac does not go back into his body, and lets his family carry him."},
               {"t": "Isaac walks into the soldiers' camp to find Naomi."}],
   "line": "Finish the sentence: This shows courage the most because…", "placeholder": "This shows courage the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read this part of Chapter 19 out loud. Isaac has just realized the soldiers cannot hurt him. Let that surprise come through in your voice. Then slow down as he watches the young man by the fire, and laugh at yourself with Isaac when he figures out who it is. When it sounds smooth, record yourself and turn it in."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
for k, v in D.items():
    json.dump(v, open('data/g5ela-21-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k)
