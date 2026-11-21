#!/usr/bin/env python3
"""Write data/g5ela-22-{1..4,fluency}.json (week 22, How I Became a Ghost Ch. 20-23), Nov 21 2026.
Every book line checked against planning docs/hbg_ocr.txt. Bethany's choices: hook "Where is the safest
hiding place?" (on 22.3, Ch. 22), Light the Lanterns game, plates found by Claude (Inness, Barye, Fantin-Latour,
Kyhn), virtue perseverance (the pages' own). Ch. 20 and 23 are hard: every line here is calm and plain.
Listen texts are Mason scripts; Choctaw words are never in them. Each lesson's four Listen clips must stay
at or under 1,000 characters (Bethany, Nov 21): the script asserts it."""
import json, sys
A = 'assets/art/hbg/'
C = 'https://commons.wikimedia.org/wiki/File:'
LOOK = ("Each lantern on the branch waits for one word. Read the meaning, then tap the word parts in order "
        "to build the word. When the word is whole, its lantern lights up.")
HOW = {"do": ["Read the meaning under the lantern.", "Tap the first part of the word.", "Tap the next parts in order.", "Tap Next lantern."],
       "why": "Long words are built from parts. If you know the parts, you can build a word and spell it."}
def W(w, parts, decoys, means, clue, why): return {"w": w, "parts": parts, "decoys": decoys, "means": means, "clue": clue, "why": why}
def game(day, words):
    return {"type": "lantern", "title": "Light the Lanterns", "sub": "This week's word game · 4 words today", "after": "Spelling",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow to light more." if day < 4 else "Every lantern this week is lit. Well done.", "words": words}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Find the pronoun that could mean two people in the second.", "Fix it out loud, then tap Check My Work."],
       "why": "A pronoun like he, she or they should point to only one person."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Find the picture you see most clearly.", "Read Think About It and keep your answer in mind."],
        "why": "Poets use pictures instead of telling you what to feel. That is imagery."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what perseverance means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def ih(ch): return {"match": "Chapter Introduction", "do": ["Read the chapter introduction below.", "Open your book and read %s." % ch, "Then do the Read Like a Writer box and the Virtue Watch below."]}
def th(ch, extra=None): return {"match": "Chapter Thinking", "do": ["Read %s first." % ch, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
                               "why": "These questions check what happened and what the author shows you."}
def art(file, title, alt, look, creator, date, url, lic="Public domain (Wikimedia Commons)", btn="Tap to learn about this painting"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": btn, "creator": creator, "date": date, "license": lic, "url": url}
MISS = {
 "autograph": "Find g-r-a-p-h at the end: auto + graph. Graph means write.",
 "paragraph": "Find g-r-a-p-h at the end: para + graph. Graph means write.",
 "photograph": "Look at the end, not the start: photo + graph. Graph means write.",
 "biography": "Find g-r-a-p-h inside: bio + graph + y. Graph means write.",
 "chronicle": "Find c-h-r-o-n at the start. Chron means time.",
 "anachronism": "Find c-h-r-o-n in the middle: ana + chron + ism. Chron means time.",
 "chronology": "Find c-h-r-o-n at the start. Chron means time.",
 "chronological": "Find c-h-r-o-n at the start. Chron means time.",
 "dialogue": "Find l-o-g-u-e at the end: dia + logue. Log means word or speech.",
 "monologue": "Find l-o-g-u-e at the end: mono + logue. Log means word or speech.",
 "prologue": "Find l-o-g-u-e at the end: pro + logue. Log means word or speech.",
 "illuminate": "Find l-u-m-i-n inside: il + lumin + ate. Lum means light, and it is Latin.",
 "lucid": "Find l-u-c at the start. Luc means light, and it is Latin.",
 "luminous": "Find l-u-m-i-n at the start. Lum means light, and it is Latin.",
 "photosynthesis": "Find p-h-o-t-o at the start. Photo means light, and it is Greek.",
 "perspective": "Find s-p-e-c-t in the middle. Spect means look.",
 "spectacle": "Find s-p-e-c-t at the start. Spect means look.",
 "vision": "Find v-i-s at the start. Vis means see.",
 "metaphor": "Find p-h-o-r at the end. Phor means carry: a metaphor carries meaning from one thing to another.",
 "reference": "Find f-e-r in the middle: re + fer + ence. Fer means carry.",
 "transfer": "Find f-e-r at the end: trans + fer. Fer means carry.",
 "evidence": "Vid means see, and it comes from Latin.",
 "narrative": "Narr means tell, and it comes from Latin.",
 "protagonist": "Prot means first and agon means struggle. Both are Greek.",
}
def pick(*ws): return {w: MISS[w] for w in ws}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "In Chapter 20, Isaac finally reaches Naomi, and the chapter takes a hard turn. Your reading lens this week is figurative language. Watch for comparisons, where one thing is described as another. Each time, ask what the picture makes you feel."},
  "words": {"text": "Two roots this week mean light. One came from Latin, one from Greek. Then long words about books, built from parts you already know. In the lantern game, build each word from its parts, and watch the lantern light up."},
  "reading": {"text": "Read Chapter 20 in your book. Watch what Naomi does to stay strong, and what goes wrong with Isaac's plan. This chapter is hard. Take it slowly. Then do the Read Like a Writer box and the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 20. Then a new piece of writing begins: a paragraph about the novel. Today you only plan. Choose a topic, write your claim, and find two pieces of evidence."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."],
   "why": "A comparison can make you feel something the author never says.", "use": "You will use this when you answer the chapter questions."},
  DOL,
  {"match": "Morphology", "do": ["Read the two roots and what they mean.", "Tap a word, then tap its meaning.", "Match all four."], "why": "This week's chapters are full of moonlight, firelight and glowing ghosts. These roots name light."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Find the noun that he points back to.", "Think through the questions.", "Tap Now check your thinking.", "Tap the clear version in each pair, then write in the box."], "why": "A pronoun should point back to only one noun."},
  {"match": "Spelling", "do": ["Find the root in the middle of each word.", "Think through the questions.", "Tap a word, then tap its column."], "why": "Long book words are short parts stacked together."},
  th("Chapter 20"),
  {"match": "Workshop", "do": ["Choose one topic from the list.", "Write your claim in one sentence.", "Find two pieces of evidence in the book and note them."],
   "why": "A literary analysis makes a claim about a book and proves it with evidence.", "use": "Tomorrow you will draft the paragraph."},
  vh("sort the moments"), ih("Chapter 20")],
 "glossary": [{"word": "figurative language", "in": "What Good Readers Do", "meaning": "words that describe one thing as if it were another, not meant word for word"},
              {"word": "comparison", "in": "What Good Readers Do", "meaning": "showing how two different things are alike"}],
 "miss": pick("autograph", "chronicle", "anachronism", "dialogue", "monologue", "paragraph", "photograph", "prologue"),
 "game": game(1, [W("photocopy", ["photo", "copy"], ["graph"], "a copy made by a machine that uses light", "photo = light", "photo (light) + copy. A copier uses a flash of light."),
                  W("photographer", ["photo", "graph", "er"], ["log"], "a person who takes pictures with a camera", "graph = write; -er = a person who", "photo + graph + er: a person who writes with light."),
                  W("illumination", ["il", "lumin", "ation"], ["luc"], "the light that is shone on something", "lumin = light", "il (into) + lumin (light) + ation."),
                  W("epilogue", ["epi", "logue"], ["chron"], "a part at the end of a book, after the story is over", "logue = words", "epi (after) + logue (words): the words after the story.")]),
 "art": art("inness-moonlight-tarpon.jpg", "Moonlight, Tarpon Springs", "A painting of a dark grove of trees at night, with the moon low in the sky, a small fire and a woman walking.",
            "George Inness painted this moonlit night in Tarpon Springs, Florida, in 1892. It is not Isaac's road, but it feels like the start of Chapter 20: a quiet camp at night, a small fire, and the moon over the trees.",
            "George Inness", "1892", C + "George_Inness_-_Moonlight,_Tarpon_Springs_-_Google_Art_Project.jpg"),
 "virtue": {"name": "perseverance", "kind": "sort", "title": "Perseverance or not?", "intro": "You just read Chapter 20. Read each moment. Tap Perseverance or Not perseverance.",
   "items": [{"t": "Leader shouts, “Who were you talking to?” Naomi keeps saying, “No one.”", "ok": True, "why": "She keeps protecting Isaac and Nita, even when Leader gets louder. That is perseverance."},
             {"t": "Isaac tries to drag Naomi away, but his hands pass right through her.", "ok": False, "why": "That is something he cannot do. What he does next is what counts."},
             {"t": "Isaac tells Nita, “We will not leave her here,” and hurries to find Joseph.", "ok": True, "why": "The plan went wrong, and he does not give up. He goes for help."},
             {"t": "The other soldiers stand and stare without saying a word.", "ok": False, "why": "They do nothing. Perseverance means you keep working toward what is right."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "In Chapter 21, Joseph becomes the panther again, and a dog surprises everyone. The poem today is about a tiger burning bright. Watch which pictures Blake gives you, and listen for fire in the chapter too."},
  "words": {"text": "Today, decide whether each light word came from Latin or from Greek. Then sort long book words by the root at their center. Then four new lanterns to light."},
  "reading": {"text": "Read Chapter 21 in your book. Track what the panther does, one action at a time, and how each one helps Naomi get away. Then try the Read Like a Writer sentence about the fire, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 21. Then write the full draft of your paragraph: a claim, two pieces of evidence with your explanation, and a closing sentence. Use at least one transition word."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap the lens you will use today.", "Collect the pictures in Chapter 21 as you read."], "why": "An image can mean more than what it shows.", "use": "You will use this for question 2."},
  DOL, POEM,
  {"match": "Morphology", "do": ["Ask: Latin light or Greek light?", "Tap a word, then tap its root and meaning.", "Match all four."], "why": "luc and lum lean toward brightness. photo leans toward light you can capture."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Read both versions in each pair.", "Tap the one that leaves the reader guessing.", "Name the pronoun with no noun, then rewrite it in the box."], "why": "A reader should never have to guess who he or they means."},
  {"match": "Spelling", "do": ["Find the root in each word.", "Ask: light, light, or look and see?", "Tap a word, then tap its column."], "why": "The root in the middle tells you the word's family."},
  th("Chapter 21"),
  {"match": "Workshop", "do": ["Start with your claim sentence.", "Add two pieces of evidence, each with your explanation.", "End with a closing sentence. Use one transition word."], "why": "Evidence only proves a claim when you explain how.", "use": "Next lesson you will revise it."},
  vh("fill in your perseverance log"), ih("Chapter 21")],
 "glossary": [{"word": "images", "in": "What Good Readers Do", "meaning": "pictures a writer puts in your mind with words"}],
 "miss": pick("illuminate", "lucid", "luminous", "perspective", "photograph", "photosynthesis", "spectacle", "vision"),
 "game": game(2, [W("telegraph", ["tele", "graph"], ["photo"], "a machine that sent messages far away over wires", "tele = far", "tele (far) + graph (write): writing sent far away."),
                  W("autobiography", ["auto", "bio", "graphy"], ["log"], "the story of a person's life, written by that person", "auto = self; bio = life", "auto (self) + bio (life) + graphy (writing)."),
                  W("chronic", ["chron", "ic"], ["graph"], "lasting a long time, or coming back again and again", "chron = time", "chron (time) + ic. A chronic cough lasts a long time."),
                  W("luminary", ["lumin", "ary"], ["photo"], "a person who lights the way for others", "lumin = light", "lumin (light) + ary. Others look to a luminary like a light.")]),
 "art": art("barye-walking-panther.jpg", "Walking Panther", "A dark bronze plaque with a big cat walking to the right, its long tail curled behind it.",
            "Antoine-Louis Barye made this small bronze plaque in Paris in 1831. His panther is the big cat of Africa and Asia. Joseph becomes an American panther, but you can see the same long, quiet steps, the way he creeps up on the soldiers' camp in Chapter 21.",
            "Antoine-Louis Barye", "1831", C + "Antoine-Louis_Barye_-_Walking_Panther_-_1981.224_-_Cleveland_Museum_of_Art.tif",
            "CC0 (Cleveland Museum of Art, via Wikimedia Commons)", "Tap to learn about this bronze"),
 "virtue": {"name": "perseverance", "kind": "log", "title": "My perseverance log", "intro": "In Chapter 21, tap the moment you think shows the most perseverance.",
   "options": [{"t": "Naomi, her wrists still tied to the rope, says “Lead the way” and runs."},
               {"t": "Panther Joseph keeps fighting after the soldiers fire at the tree."},
               {"t": "Nita goes alone in the night to wake the whole Choctaw Council."}],
   "line": "Finish the sentence: This shows the most perseverance because…", "placeholder": "This shows the most perseverance because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Chapter 22 takes Naomi somewhere nobody would think to look. Part of it explains how some Choctaw women cared for people who had died. Read it calmly. Today you will reread one sentence and notice how it is built."},
  "words": {"text": "Put the light words to work today. Then try book words you have never studied. Break each one into its parts, and work out the meaning before anyone tells you. Then four new lanterns."},
  "reading": {"text": "Read Chapter 22 in your book. Watch who welcomes Naomi, and why their wagon is the safest place for her. Then reread the thunderbolt sentence in the Read Like a Writer box, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 22. Then revise your paragraph with the checklist. Check every he, she and they. Improve one transition. Cut words you do not need. Show one sentence before and after."}},
 "hook": {"q": "Soldiers are hunting for a girl. Where would you hide her?",
  "options": [{"t": "Deep in the woods", "reply": "The woods are a good guess, but soldiers search there first. The women in Chapter 22 have a stranger idea:"},
              {"t": "In a crowd of people", "reply": "Hiding in plain sight is clever. The women in Chapter 22 go even further:"},
              {"t": "Inside a hollow tree", "reply": "A good hiding place, if nobody looks. The women in Chapter 22 pick a place soldiers will not want to look:"}],
  "reveal": {"line": "This is the safest place for you now.", "cite": "a woman in the wagon, Chapter 22",
             "then": "As you read Chapter 22, find out where Naomi hides, and why the soldiers will not want to look there."}},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Read each meaning.", "Tap a word, then tap its meaning.", "Match all four words."], "why": "If you know the root, you can work out a word you have never seen."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Tap the version a reader can follow in each pair.", "Write three sentences about Chapter 22.", "Underline the noun each pronoun points to."], "why": "When several people act in one scene, names keep the reader on track."},
  {"match": "Spelling", "do": ["Break each word at its parts.", "Find the root, even in words you have not studied.", "Tap a word, then tap its column."], "why": "The parts let you read and spell a word you have never met."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Reread the thunderbolt sentence in Chapter 22.", "Notice what comes first: the picture or the fact."], "why": "Where a writer puts a comparison changes how you feel the moment.", "use": "You will use this in the Read Like a Writer box."},
  th("Chapter 22", "For question 3, use one detail from each chapter."),
  {"match": "Workshop", "do": ["Read your draft from Day 2.", "Check every he, she and they.", "Improve one transition and cut extra words.", "Show one sentence before and after."], "why": "Revising means making the paragraph clearer, not starting over.", "use": "Next lesson you will write the final version."},
  vh("use the perseverance meter"), ih("Chapter 22")],
 "glossary": [{"word": "comparison", "in": "What Good Readers Do", "meaning": "showing how two different things are alike"}],
 "hints": {"distraction": ["Something that pulls attention away.", "Jumper is ready to be one.", "It starts with dis."],
           "bonepickers": ["The women in the wagon.", "Their job was to care for the dead.", "bone + pickers"],
           "speechless": ["Too surprised to talk.", "Luke stands this way when the ghosts appear.", "speech + less"],
           "ancestors": ["Family who lived long ago.", "Making them proud is the highest honor.", "It starts with an."],
           "honored": ["Treated with great respect.", "The ghosts do this to the boys.", "It ends with -ed."]},
 "miss": pick("autograph", "biography", "chronological", "chronology", "metaphor", "reference", "transfer"),
 "game": game(3, [W("synchronize", ["syn", "chron", "ize"], ["log"], "to make things happen at the same time", "syn = together; chron = time", "syn (together) + chron (time) + ize (to make)."),
                  W("catalog", ["cata", "log"], ["graph"], "a list of things, like the books in a library", "log = word", "cata (down) + log (word): words written down in a list."),
                  W("photogenic", ["photo", "gen", "ic"], ["lumin"], "looking good in pictures", "photo = light", "photo (light) + gen (made) + ic."),
                  W("luminosity", ["lumin", "osity"], ["luc"], "how much light something gives off", "lumin = light", "lumin (light) + osity. Some stars have more luminosity than others.")]),
 "art": art("fantin-roses-bowl.jpg", "Roses in a Bowl", "A painting of pink, white, red and yellow roses in a dark bowl on a brown table.",
            "Henri Fantin-Latour painted these roses in France in 1883. The book does not show the wagon, but it tells you how it smells: Naomi climbs into a wagon sweetened by the smell of dried roses.",
            "Henri Fantin-Latour", "1883", C + "Henri_Fantin-Latour_-_Roses_in_a_Bowl_MET_DT10260.jpg", "CC0 (The Metropolitan Museum of Art, via Wikimedia Commons)"),
 "virtue": {"name": "perseverance", "kind": "meter", "title": "The perseverance meter", "intro": "Think about one moment from Chapter 22.",
   "moment": "Naomi lies in a secret space at the bottom of a trunk, under a blanket in the dark. The air is stuffy, and she can hear the wagon rattle, but she stays still and waits.",
   "ask": "How much perseverance did Naomi show? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "She showed this much because…",
   "take": "Mason's take: a lot. She was scared, and she stayed. Sometimes perseverance means holding still and waiting."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "This is the last day of the week. In Chapter 23, the plan to hide Naomi goes into action, and the three boys get a visit they will never forget. The poem today is about snowy woods at night. Listen for how quiet it feels."},
  "words": {"text": "Last day with the light roots. Explain why writers use light to talk about understanding. Then build words of your own from Greek and Latin parts, and light the last lanterns of the week."},
  "reading": {"text": "Read Chapter 23 in your book. Watch how the women's plan works, and what the ghosts tell the boys. Then put the week together with your lens: choose the picture that carries the most. Finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 23. Then write the final version of your paragraph, with every pronoun clear. Last, explain how a summary and an analysis are different. Copy your work and paste it into Canvas."}},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap its meaning.", "Say out loud how lucid and translucent are different."], "why": "Explaining two close words out loud shows you know them."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Tap the version that names who acted in each pair.", "Write one sentence that hides who acted and one that names them.", "Explain the difference in the box."], "why": "In writing about history, naming who acted keeps the record true."},
  {"match": "Spelling", "do": ["Decide if each root is Greek or Latin.", "Tap a word, then tap its column.", "Build two words of your own in the box."], "why": "Knowing where a part comes from helps you build new words."},
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap your lens for today.", "Choose the one picture from this week that carries the most."], "why": "The strongest images in a book are often the ones the author never explains.", "use": "You will use this for question 2."},
  th("Chapter 23"),
  {"match": "Workshop", "do": ["Write the final paragraph.", "Check that every pronoun is clear.", "Then explain summary and analysis in the box."], "why": "Today you finish your paragraph and turn it in."},
  vh("pick the strongest moment of the week"), ih("Chapter 23")],
 "glossary": [{"word": "symbol", "in": "What Good Readers Do", "meaning": "a thing in a story that stands for a bigger idea"}],
 "miss": pick("chronology", "dialogue", "evidence", "metaphor", "narrative", "perspective", "protagonist"),
 "game": game(4, [W("geography", ["geo", "graphy"], ["log"], "the study of the earth and its places", "geo = earth", "geo (earth) + graphy (writing about)."),
                  W("chronometer", ["chrono", "meter"], ["graph"], "a clock that keeps very exact time", "meter = measure", "chrono (time) + meter (measure). Sailors used them at sea."),
                  W("calligraphy", ["calli", "graphy"], ["photo"], "beautiful handwriting", "calli = beautiful", "calli (beautiful) + graphy (writing)."),
                  W("luminescent", ["lumin", "escent"], ["photo"], "glowing with a soft light", "lumin = light", "lumin (light) + escent. A firefly is luminescent.")]),
 "art": art("kyhn-winter-evening.jpg", "Winter Evening in a Forest", "A painting of a snowy forest at dusk, with bare trees, a frozen pond and a small sleigh on a snowy road.",
            "Vilhelm Kyhn painted this winter evening in a forest in Denmark in 1853. It is far from Isaac's road, but it fits the end of Chapter 23: the snow falls thick, and Isaac and Joseph wait in the cold woods by the river.",
            "Vilhelm Kyhn", "1853", C + "Vilhelm_Kyhn,_Vinteraften_i_en_skov,_1853,_KMS719,_Statens_Museum_for_Kunst.jpg", "Public domain (Statens Museum for Kunst, via Wikimedia Commons)"),
 "virtue": {"name": "perseverance", "kind": "best", "title": "The strongest moment of perseverance this week", "intro": "Look back at Chapters 20 to 23. Tap the moment you think shows perseverance the most.",
   "options": [{"t": "Naomi keeps saying “No one” to protect Isaac and Nita."},
               {"t": "Joseph decides, “Naomi comes with us tonight.”"},
               {"t": "Naomi runs with the rope still tied to her wrists."},
               {"t": "Naomi waits in the dark trunk until the soldiers are gone."},
               {"t": "Joseph waits all night in the freezing sleet to keep watch."}],
   "line": "Finish the sentence: This shows perseverance the most because…", "placeholder": "This shows perseverance the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read this part of Chapter 23 out loud. Start slowly, like the wind and the sleet. Let Joseph's words shiver. Pause when the branch cracks, then let the last line land. You heard it on the first page of the book. When it sounds smooth, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
BAD = ['Yakoke', 'pisa', 'lachike', 'Nahullo', 'Choctaw word']
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    for b in BAD:
        if any(b in t for t in txt): sys.exit('%s: Choctaw word %s in a Listen script' % (k, b))
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    if '—' in json.dumps(v, ensure_ascii=False): sys.exit('%s: em dash' % k)
    json.dump(v, open('data/g5ela-22-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars')
