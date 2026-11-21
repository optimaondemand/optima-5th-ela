#!/usr/bin/env python3
"""Write data/g5ela-20-{1..4,fluency}.json (week 20, How I Became a Ghost Ch. 12-15), Nov 21 2026.
Every book line checked against planning docs/hbg_ocr.txt. Bethany's choices: hook "keep a secret or tell?",
trip points Ch. 12 (Nita: "You can find my sister") and Ch. 15 (the Choctaw Council), Council Fire game,
1800s winter and night paintings. Listen texts are Mason scripts (recorded later)."""
import json
A = 'assets/art/hbg/'
LOOK = ("On the walk, families gather around a fire every night. In this game, each pair of related words is a log. "
        "Say each word and tap the beat you say the strongest. Get both words right and the log goes on the fire. "
        "Your fire keeps burning all week.")
HOW = {"do": ["Say the first word out loud.", "Tap the beat you say the strongest.", "Do the same for the second word.", "Tap Next log."],
       "why": "When a word grows, its strong beat can move. Hearing the move helps you spell the quiet vowels."}
def game(day, pairs):
    logs = []
    for a, sa, b, sb in pairs:
        A_, B_ = a.split('·'), b.split('·')
        why = 'Yes: %s, then %s. The strong beat moves.' % ('-'.join(p.upper() if i == sa else p for i, p in enumerate(A_)),
                                                             '-'.join(p.upper() if i == sb else p for i, p in enumerate(B_)))
        logs.append({"a": a, "sa": sa, "b": b, "sb": sb, "why": why})
    return {"type": "fire", "title": "Council Fire", "sub": "This week's word game · 5 logs today", "after": "Spelling",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow for more." if day < 4 else "That is the whole week's fire. Well done.", "logs": logs}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Fix the second sentence out loud.", "Tap Check My Work to compare."],
       "why": "A comma in the right place shows the reader where one part of a sentence ends and the next begins."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Pause at every line break.", "Read Think About It and keep your answer in mind."],
        "why": "Where a poet breaks a line changes how a reader feels the words. A break can make you wait."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what justice means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def ih(ch): return {"match": "Chapter Introduction", "do": ["Read the chapter introduction below.", "Open your book and read %s." % ch, "Then do the Virtue Watch and the Read Like a Writer box below."]}
def th(ch, extra=None): return {"match": "Chapter Thinking", "do": ["Read %s first." % ch, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
                               "why": "These questions check what happened and what each event made harder."}
def art(file, title, alt, look, creator, date, url, lic="Public domain (Wikimedia Commons)"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": "Tap to learn about this painting", "creator": creator, "date": date, "license": lic, "url": url}
SORT = {"define": "de-FINE: the strong beat is FINE, syllable 2.", "definite": "DEF-i-nite: the strong beat is DEF, syllable 1.",
        "historic": "his-TOR-ic: the strong beat is TOR, syllable 2.", "history": "HIS-to-ry: the strong beat is HIS, syllable 1.",
        "photograph": "PHO-to-graph: the strong beat is PHO, syllable 1.", "photography": "pho-TOG-ra-phy: the strong beat is TOG, syllable 2.",
        "compete": "com-PETE: the strong beat is PETE, syllable 2.", "competitor": "com-PET-i-tor: the strong beat is PET, syllable 2.",
        "familiar": "fa-MIL-iar: the strong beat is MIL, syllable 2.", "family": "FAM-i-ly: the strong beat is FAM, syllable 1.",
        "origin": "OR-i-gin: the strong beat is OR, syllable 1.", "original": "o-RIG-i-nal: the strong beat is RIG, syllable 2.",
        "medicinal": "me-DIC-i-nal: the strong beat is DIC, syllable 2.", "medicine": "MED-i-cine: the strong beat is MED, syllable 1.",
        "atom": "AT-om: the strong beat is AT, syllable 1.", "atomic": "a-TOM-ic: the strong beat is TOM, syllable 2.",
        "metal": "MET-al: the strong beat is MET, syllable 1.", "metallic": "me-TAL-lic: the strong beat is TAL, syllable 2.",
        "memorial": "me-MOR-i-al: the strong beat is MOR, syllable 2.", "memory": "MEM-o-ry: the strong beat is MEM, syllable 1.",
        "relation": "re-LA-tion: the strong beat is LA, syllable 2.", "relative": "REL-a-tive: the strong beat is REL, syllable 1.",
        "major": "MA-jor: the strong beat is MA, syllable 1.", "majority": "ma-JOR-i-ty: the strong beat is JOR, syllable 2."}
def pick(*ws): return {w: SORT[w] for w in ws}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "Nita has died, and her family carries her on the walk. In Chapter 12, Isaac learns that Nita's family has a secret. Before you read, think about secrets. When is it right to keep one, and when is it right to tell? Your reading lens this week is how a story's pressure builds."},
  "words": {"text": "Two new roots this week, and both are about feeling. One leans toward emotion. One leans toward the senses. Then listen to long words. When a word grows, its strongest beat can move. In the council fire game, say each word out loud and tap the beat you say the strongest."},
  "reading": {"text": "Read Chapter 12 of How I Became a Ghost in your book. Nita's ghost comes to Isaac with a request: find her sister. Watch what happens when Isaac asks Gabe about it, and notice what makes the tension grow. Then do the Virtue Watch and the Read Like a Writer box."},
  "assignment": {"text": "Three questions about Chapter 12, then the plan for a theme paragraph. A theme is a big idea the book shows, like courage or justice. Today you only pick one and note two pieces of evidence. Copy your work into Canvas when you finish."}},
 "hook": {"q": "Someone you trust says, “Do not tell anyone.” When is it right to keep a secret, and when is it right to tell?",
  "options": [{"t": "Always keep it", "reply": "Keeping your word matters. But some secrets hurt people. Here is what Gabe says:"},
              {"t": "Tell if someone could get hurt", "reply": "That is a careful answer. In this chapter, a family is too afraid to tell. Here is what Gabe says:"},
              {"t": "It depends who is asking", "reply": "Trust matters. Watch who Gabe finally trusts. Here is what he says:"}],
  "reveal": {"line": "We do not have another daughter. Do not speak of this!", "cite": "Gabe, Chapter 12",
             "then": "As you read Chapter 12, watch what this secret is protecting, and who finally gets Gabe to talk."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."],
   "why": "A story's pressure comes from each event making the next one harder. Tracking it helps you see where the story is going.", "use": "You will use this when you answer the chapter questions."},
  DOL,
  {"match": "Morphology", "do": ["Read the two roots and what they mean.", "Tap a word, then tap its meaning.", "Match all four."], "why": "This book asks you to feel what other people feel. These roots name feeling."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Find the comma in the sentence.", "Think through the question.", "Tap Now check your thinking.", "Tap the right version in each pair, then answer in the box."], "why": "Commas mark where one part of a sentence ends and the next begins."},
  {"match": "Spelling", "do": ["Say each word out loud.", "Lean on each beat until one sounds right.", "Tap a word, then tap its column."], "why": "Knowing where the stress falls helps you spell the quiet vowels."},
  th("Chapter 12"),
  {"match": "Workshop", "do": ["Pick one theme you see in the book.", "In the box, name it and note two pieces of evidence.", "A few lines is enough."],
   "why": "A theme paragraph explains a big idea and proves it with the book's own details. Today you only choose.", "use": "Tomorrow you will start writing it."},
  vh("sort the moments"), ih("Chapter 12")],
 "glossary": [{"word": "conflict", "in": "What Good Readers Do", "meaning": "a problem between what a character wants and what stands in the way"},
              {"word": "rising action", "in": "What Good Readers Do", "meaning": "the part of a story where the problem grows and the tension climbs"}],
 "miss": pick("define", "definite", "historic", "history", "photograph", "photography"),
 "game": game(1, [("cour·age", 0, "cou·ra·geous", 1), ("hu·man", 0, "hu·man·i·ty", 1), ("mu·sic", 0, "mu·si·cian", 1), ("e·qual", 0, "e·qual·i·ty", 1), ("ac·tive", 0, "ac·tiv·i·ty", 1)]),
 "art": art("hahn-snowstorm-sierras.jpg", "Snowstorm in the Sierras", "A painting of a stagecoach pulled by horses through a thick snowstorm, with bare trees and a pale sun.",
            "William Hahn painted this snowstorm in the Sierra Nevada mountains of California in 1876. It is far from Isaac's road, but it shows the kind of storm in Chapter 12: snow swirling so thick that the walkers are blinded by it.",
            "William Hahn", "1876", "https://commons.wikimedia.org/wiki/File:William_Hahn_-_Snowstorms_in_the_Sierras,_1876.jpg"),
 "virtue": {"name": "justice", "kind": "sort", "title": "Justice or not?", "intro": "You just read Chapter 12. Read each moment. Tap Justice or Not justice.",
   "items": [{"t": "Isaac follows Gabe into the woods and says, “I want to help you find your other daughter.”", "ok": True, "why": "He sees that something is wrong and offers to help set it right. That is the start of justice."},
             {"t": "Gabe says, “We do not have another daughter. Do not speak of this!”", "ok": False, "why": "Gabe is frightened, and his fear makes sense. But keeping a wrong hidden is not justice yet."},
             {"t": "To make Gabe listen, Isaac shares his own secret: he will soon be a ghost.", "ok": True, "why": "He trusts Gabe with the truth so the truth about Nita's sister can come out. Telling the truth is part of justice."},
             {"t": "Walking blind in the snow, Isaac imagines an icicle falling on him.", "ok": False, "why": "That is a frightening daydream, not a choice about right and wrong."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "In Chapter 13, two secrets come out around one campfire, and then someone new arrives in the dark. The poem today is about choosing a road. Look at where its lines break. A line break can make a reader wait, the same way a writer builds tension."},
  "words": {"text": "Today you decide which feeling root is in each word: the one for emotion, or the one for the senses. Then sort words by where the stress falls. Say each word twice, leaning on a different beat each time. Only one way sounds right."},
  "reading": {"text": "Read Chapter 13 in your book. Listen for Gabe's secret and Isaac's secret, and notice why each one was kept. Then look at how Tingle orders the events in the Read Like a Writer sentence. Finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 13, then the first sentences of your theme paragraph. Start with a sentence that names the theme. Then add one piece of evidence from the book, and connect them with a complex sentence."}},
 "how": [
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap the lens you will use today.", "Watch what changes for Isaac's family the moment they know."], "why": "Saying a secret out loud can raise the tension instead of ending it.", "use": "You will use this for the chapter questions."},
  DOL, POEM,
  {"match": "Morphology", "do": ["Ask: is this word about emotion or about the senses?", "Tap a word, then tap its root.", "Match all four."], "why": "Both roots mean feel, but they lean different ways."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Find where the two parts of the sentence meet.", "Tap the version with the comma in the right place.", "Write both sentences in the box and explain."], "why": "The order of the parts decides whether a comma is needed."},
  {"match": "Spelling", "do": ["Say each word twice, leaning on a different beat.", "Keep the way that sounds like English.", "Tap a word, then tap its column."], "why": "The stress can jump when a word grows."},
  th("Chapter 13"),
  {"match": "Workshop", "do": ["Write a topic sentence that names your theme.", "Add one piece of evidence from the book.", "Join them with a complex sentence and a comma."], "why": "A clear topic sentence tells the reader what the whole paragraph will prove.", "use": "Next lesson you will revise and add more evidence."},
  vh("fill in your justice log"), ih("Chapter 13")],
 "glossary": [{"word": "line break", "in": "Poetry Corner", "meaning": "the place where a poet ends one line and starts the next"},
              {"word": "rising action", "in": "What Good Readers Do", "meaning": "the part of a story where the problem grows and the tension climbs"}],
 "miss": pick("compete", "competitor", "familiar", "family", "origin", "original"),
 "game": game(2, [("in·vite", 1, "in·vi·ta·tion", 2), ("ex·plain", 1, "ex·pla·na·tion", 2), ("pre·pare", 1, "prep·a·ra·tion", 2), ("ad·mire", 1, "ad·mi·ra·tion", 2), ("in·form", 1, "in·for·ma·tion", 2)]),
 "art": art("kuindzhi-moon-night-winter.jpg", "Moon Night. Winter.", "A painting of a snowy field at night under a dark blue sky, with mounds of snow catching pale moonlight.",
            "Arkhip Kuindzhi painted this winter night in Russia around 1900. It is not Isaac's road, but it feels like Chapter 13: the snow has stopped, the air is bitter cold, and the night holds secrets.",
            "Arkhip Kuindzhi", "around 1900", "https://commons.wikimedia.org/wiki/File:Kuindzhi_Moon_night_Winter.jpg"),
 "virtue": {"name": "justice", "kind": "log", "title": "My justice log", "intro": "In Chapter 13, the truth comes out. Tap the moment you think did the most for justice.",
   "options": [{"t": "Gabe finally tells everyone that the soldiers took his daughter Naomi."},
               {"t": "Isaac tells his family he will soon be a ghost, and asks them not to stop him from helping Naomi."},
               {"t": "Joseph wakes Isaac in the night: “Right now, we need to find Naomi.”"}],
   "line": "Finish the sentence: This did the most for justice because…", "placeholder": "This did the most for justice because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "In Chapter 14, Joseph tells Isaac his story: how he was caught, and how he got away. He tells it calmly, but a lot happens. Today you will reread part of it and put the events in order. Notice which event made the next one possible."},
  "words": {"text": "Put the feeling roots to work today. Then the spelling words: when a vowel is too quiet to hear, say a related word where that beat is strong. The vowel comes back. The council fire game uses the same trick."},
  "reading": {"text": "Read Chapter 14 in your book. Joseph tells his story in order, from the hunt to the cave. Follow each step. Then try the Read Like a Writer box, where one sentence skips a whole night, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 14. The last one connects three secrets from Chapters 12, 13 and 14. Then revise your theme paragraph with the checklist, and add a second piece of evidence."}},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap the root it belongs to.", "Match all four words."], "why": "If you know the root, you can work out a word you have never seen."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Tap the correct version in each pair.", "Watch for two sentences joined by only a comma.", "Fix the comma splice three ways in the box."], "why": "A comma alone cannot join two complete sentences."},
  {"match": "Spelling", "do": ["Say the word, then say its relative.", "Find where the stress falls.", "Tap a word, then tap its column."], "why": "A related word can make a quiet vowel loud again."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Reread part of Joseph's story.", "Put the events in order, and ask which one made the next possible."], "why": "Rereading for order shows how one event leads to the next.", "use": "You will use this for question 1."},
  th("Chapter 14", "For question 3, use one detail from each chapter."),
  {"match": "Workshop", "do": ["Reread your draft with the checklist.", "Add a second piece of evidence.", "Explain how both pieces prove your theme."], "why": "Revising means making the proof stronger, not starting over.", "use": "Next lesson you will write the final paragraph."},
  vh("use the justice meter"), ih("Chapter 14")],
 "glossary": [{"word": "sequence", "in": "What Good Readers Do", "meaning": "the order in which things happen"}],
 "hints": {"determined": ["Her mind is made up.", "In Chapter 12, Gabe says this about Nita.", "It starts with deter."],
           "treaty": ["An agreement between governments.", "Joseph says the soldiers must follow it.", "It starts with treat."],
           "council": ["A group of leaders.", "They ride in their own wagon.", "It starts with coun."],
           "invisible": ["Impossible to see.", "Joseph jokes he will be like a ghost.", "in + vis + ible"],
           "permission": ["Being allowed.", "Isaac says his parents gave it to him.", "It ends with -ssion."]},
 "miss": pick("medicinal", "medicine", "atom", "atomic", "metal", "metallic"),
 "game": game(3, [("pub·lic", 0, "pub·lic·i·ty", 1), ("strat·e·gy", 0, "stra·te·gic", 1), ("har·mo·ny", 0, "har·mon·ic", 1), ("e·lec·tric", 1, "e·lec·tric·i·ty", 2), ("a·cad·e·my", 1, "ac·a·dem·ic", 2)]),
 "art": art("kuindzhi-moonlight-forest.jpg", "Moonlight in the Forest. Winter.", "A painting of a dark winter forest at night, with bright patches of moonlight on the snow.",
            "Arkhip Kuindzhi painted these patches of moonlight in a winter forest in Russia in the early 1900s. In Chapter 14, Joseph runs through the night: “The moon shone bright and I could see where I was going.”",
            "Arkhip Kuindzhi", "early 1900s", "https://commons.wikimedia.org/wiki/File:Kuindzhi_Moonlight_spots_in_a_forest_Winter_1898_1908.jpg"),
 "virtue": {"name": "justice", "kind": "meter", "title": "The justice meter", "intro": "Think about one moment from Chapter 14.",
   "moment": "The soldiers laughed about the deaths in Joseph's town. Joseph escaped. Instead of running far away, he followed the walkers and found where the same soldiers hold Naomi.",
   "ask": "How much did Joseph act for justice? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He acted this much because…",
   "take": "Mason's take: a lot. Joseph could have stayed far away from those soldiers. He came back to help a girl they had taken. In Chapter 13 he says, “Right now, we need to find Naomi.”"},
}
D[4] = {
 "listen": {
  "warmup": {"text": "This is the last day of the week. In Chapter 15, Isaac learns that Choctaw leaders travel with the walkers in a council wagon, and a ghost gives him a plan. The poem today never names what it describes. Let each line break show you a little more."},
  "words": {"text": "Last day with the feeling roots. Explain the difference between feeling with someone and feeling from inside their experience. In spelling, the vowel you cannot hear hides in the quiet beat. Find a relative that makes it loud."},
  "reading": {"text": "Read Chapter 15 in your book. Watch how the Choctaw Council welcomes Isaac, and listen to what Nani Humma asks him. Then put the week together with your lens: where did the danger change? Finish with the Virtue Watch at the end of this tab."},
  "assignment": {"text": "Three questions about Chapter 15, then your finished theme paragraph: five to seven sentences, with a topic sentence, two pieces of evidence and a closing. Then one sentence about the hardest part. Copy your work and paste it into Canvas."}},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap its meaning.", "Say out loud how sympathy and empathy are different."], "why": "Explaining two close words out loud shows you know them."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Tap the version a reader can follow the first time.", "Find a sentence in this week's chapters that joins two ideas.", "Copy it and explain each comma in the box."], "why": "Commas help a reader follow a long sentence on the first read."},
  {"match": "Spelling", "do": ["Say the word, then a related word.", "Listen for the vowel that comes back.", "Tap a word, then tap its column."], "why": "The schwa hides in quiet beats. A relative brings it out."},
  {"match": "What Good Readers Do", "do": ["Read today's skill.", "Tap your lens for today.", "Lay the week's events in order and find where the danger changed."], "why": "Putting the week together shows how the story's pressure has grown.", "use": "You will use this for question 3."},
  th("Chapter 15"),
  {"match": "Workshop", "do": ["Write the full paragraph, 5 to 7 sentences.", "Use a topic sentence, two pieces of evidence and a closing.", "Add one sentence about the hardest part."], "why": "Today you finish your theme paragraph and turn it in."},
  vh("pick the strongest moment of the week"), ih("Chapter 15")],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "to put ideas from different parts together into one bigger idea"}],
 "miss": pick("memorial", "memory", "relation", "relative", "major", "majority"),
 "game": game(4, [("cel·e·brate", 0, "ce·leb·ri·ty", 1), ("pa·tri·ot", 0, "pa·tri·ot·ic", 2), ("per·son", 0, "per·son·al·i·ty", 2), ("com·pose", 1, "com·po·si·tion", 2), ("com·bine", 1, "com·bi·na·tion", 2)]),
 "art": art("homer-camp-fire.jpg", "Camp Fire", "A painting of a campfire at night in a dark forest, with sparks rising and two men resting by a lean-to.",
            "Winslow Homer painted this campfire in the Adirondack mountains of New York in 1880. It is far from Isaac's road, but it fits Chapter 15: a fire in the woods at night, where the Choctaw councilmen eat pashofa and welcome Isaac.",
            "Winslow Homer", "1880", "https://commons.wikimedia.org/wiki/File:Camp_Fire_MET_DT2829.jpg", "CC0 (The Metropolitan Museum of Art, via Wikimedia Commons)"),
 "cards": [{"tab": "reading", "after": "Chapter Introduction", "title": "Choctaw words in Chapters 12 to 15", "min": 1,
            "intro": "Isaac tells his story in English, but some Choctaw words stay in it.",
            "items": [{"term": "Halito", "meaning": "Hello. Nani Humma says it when Isaac walks into the council camp.", "line": "“Halito,” he said. “Welcome to our camp.”", "cite": "Chapter 15"},
                      {"term": "Yakoke", "meaning": "Thank you. Isaac says it to Gabe in Chapter 12 and to the council in Chapter 15.", "line": "“Yakoke. Gabe, I miss her, too.”", "cite": "Chapter 12"},
                      {"term": "Hoke", "meaning": "Okay. Isaac's father asks if he is hoke after his bad dream in the snow.", "line": "", "cite": "Chapter 12"},
                      {"term": "Pashofa", "meaning": "Choctaw corn soup. The councilmen are eating bowls of it.", "line": "", "cite": "Chapter 15"}],
            "note": "The narrator does not say these words aloud. Choctaw has its own sounds, and we would rather not teach them wrong."}],
 "virtue": {"name": "justice", "kind": "best", "title": "The strongest moment of justice this week", "intro": "Look back at Chapters 12 to 15. Tap the moment you think shows justice the most.",
   "options": [{"t": "Isaac offers to help Gabe find his other daughter."},
               {"t": "Gabe tells everyone the truth: the soldiers took Naomi."},
               {"t": "Isaac tells his family his own secret so they can help."},
               {"t": "Joseph comes back to find Naomi instead of running away for good."},
               {"t": "Isaac decides to tell Nani Humma the whole truth as soon as he can."}],
   "line": "Finish the sentence: This shows justice the most because…", "placeholder": "This shows justice the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read this part of Chapter 12 out loud. Isaac is walking blind through the snow, and his mind tells him a frightening story. Let the tension build as the icicle waits. Whisper the first no, and shout the second. When it sounds smooth, record yourself and turn it in."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
for k, v in D.items():
    json.dump(v, open('data/g5ela-20-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k)
