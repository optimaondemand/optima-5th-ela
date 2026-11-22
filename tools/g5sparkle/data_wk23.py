#!/usr/bin/env python3
"""Write data/g5ela-23-{1..4,fluency}.json (week 23, How I Became a Ghost Ch. 24-27), Nov 21 2026.
Every book line checked against planning docs/hbg_ocr.txt. Bethany's choices: hook "Your leader just hurt one of
your own" (on 23.2, Ch. 25), Raise Your Voice game (voc/voke + dict cloze; the lines are made up, not from the
book), plates found by Claude (Monet, Friedrich x2, Catesby), virtue justice (the pages' own). Listen texts are
Mason scripts; Choctaw words are never in them. Each lesson's four Listen clips stay at or under 1,000 characters."""
import json, sys
A = 'assets/art/hbg/'
C = 'https://commons.wikimedia.org/wiki/File:'
LOOK = ("Each line is something a person in Isaac's time could say. These lines are made up; they are not from the book. "
        "Read the whole line, then tap the word that fits the blank. Each line you finish sends a gold voice ring into the sky.")
HOW = {"do": ["Read the whole line, blank and all.", "Ask: voice and calling, or saying?", "Tap the word that fits.", "Tap Next line."],
       "why": "If you know voc, voke and dict, you can work out words you have never studied."}
def V(who, before, after, opts, ok, why): return {"who": who, "before": before, "after": after, "opts": opts, "ok": ok, "why": why}
def game(day, lines):
    return {"type": "voice", "title": "Raise Your Voice", "sub": "This week's word game · 3 lines today", "after": "Spelling",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow for three more lines." if day < 4 else "Every voice this week is raised. Well done.", "lines": lines}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Join the second one into one clear sentence, out loud.", "Tap Check My Work."],
       "why": "Joining short sentences shows the reader how the ideas connect."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Look at its shape: how many lines, how it rhymes.", "Read Think About It and keep your answer in mind."],
        "why": "A poet chooses a poem's shape to fit what it says."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what justice means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def ih(ch, rwm=True): return {"match": "Chapter Introduction", "do": ["Read the chapter introduction below.", "Open your book and read %s." % ch, "Then do the Read Like a Writer box and the Virtue Watch below." if rwm else "Then do the Virtue Watch below."]}
def th(ch, extra=None): return {"match": "Chapter Thinking", "do": ["Read %s first." % ch, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
                               "why": "These questions check what happened and what the author shows you."}
def art(file, title, alt, look, creator, date, url, lic, btn="Tap to learn about this painting"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": btn, "creator": creator, "date": date, "license": lic, "url": url}
MISS = {
 "creative": "create drops its last e before -ive: creat + ive.", "curiosity": "curious drops its u before -ity: curios + ity.",
 "decision": "decide drops its d-e before -sion: deci + sion.", "illegal": "il means not: il + legal.", "impossible": "im means not: im + possible.",
 "irregular": "ir means not: ir + regular.", "governor": "Say gov-er-nor. The ending sounds like nur, but it is spelled o-r.",
 "mariner": "Say mar-i-ner. The middle i makes a quiet uh sound.", "separate": "Say sep-a-rate. The quiet middle is spelled a.",
 "ability": "able changes to abil before -ity.", "perceptive": "perceive changes to percept before -ive.", "permission": "permit changes to permiss before -ion.",
 "interrupt": "inter + rupt. The prefix stays whole, so there are two r's.", "submerge": "sub + merge. The prefix stays whole.", "transport": "trans + port. The prefix stays whole.",
 "council": "council (a group that meets) sounds like counsel (advice). Check the meaning.", "it's": "it's means it is. its means belonging to it.",
 "their": "their means belonging to them. there and they're sound the same.",
 "dependable": "depend is a whole word, so it takes -able.", "remarkable": "remark is a whole word, so it takes -able.",
 "possible": "poss is not a word by itself, so it takes -ible.", "terrible": "terr is not a word by itself, so it takes -ible.", "visible": "vis is not a word by itself, so it takes -ible.",
 "navigator": "a person who navigates: -or.", "printer": "a person or machine that prints: -er.", "teacher": "a person who teaches: -er.",
 "affect": "affect (to change) sounds like effect (a result). Check the meaning.", "principle": "principle (a rule) sounds like principal (the head of a school).",
 "whose": "whose (belonging to who) sounds like who's (who is).", "chronology": "chron (time) + logy (study): Greek parts.",
 "manuscript": "manu (hand) + script (write): Latin parts.", "photograph": "photo (light) + graph (write): Greek parts.",
 "competition": "Say com-pe-ti-tion. The quiet e: think of compete.", "definition": "Say def-i-ni-tion. The quiet i: think of define.",
}
def pick(*ws): return {w: MISS[w] for w in ws}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "In Chapter 24, Isaac spends a whole night awake while everyone else sleeps, and by morning Leader has made a dangerous vow. Your reading skill this week is summarizing. A good summary keeps only the events the story could not do without."},
  "words": {"text": "Two roots this week are about speaking. Voc, or voke, means voice or call. Dict means say. Then a year of spelling patterns, all in one sort. In the game, read each line and choose the word that fits the blank."},
  "reading": {"text": "Read Chapter 24 in your book. Watch what Leader vows, and how his own soldiers react. Then try the Read Like a Writer sentence about the wagon fire, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 24. Then your final writing piece of the unit begins. Today you only plan. Choose your strongest writing from the last five weeks, and decide what to keep, what to cut, and how to begin."}},
 "how": [dict(WGRD, why="A summary is a choice, not a shorter retelling.", use="You will use this when you answer the chapter questions."),
  DOL,
  {"match": "Morphology", "do": ["Read the two roots and what they mean.", "Tap a word, then tap its meaning.", "Match all four."], "why": "This book is about who gets to speak. These roots name voice and saying."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the three short sentences, then the joined one.", "Think through the questions.", "Tap Now check your thinking.", "Tap the clearer version in each pair, then write in the box."], "why": "Joining sentences shows how ideas connect, so the reader does not have to guess."},
  {"match": "Spelling", "do": ["Compare each base word with its longer form.", "Think through the questions.", "Tap a word, then tap its column."], "why": "A few patterns explain most hard spellings. This week you use all of them."},
  th("Chapter 24"),
  {"match": "Workshop", "do": ["Look back at your writing from weeks 18 to 22.", "Choose your strongest piece.", "In the box, plan what to keep, what to cut, and how to begin and end."],
   "why": "Publishing means choosing your best work and making it ready for a reader.", "use": "Tomorrow you will draft it."},
  vh("sort the moments"), ih("Chapter 24")],
 "glossary": [{"word": "summarize", "in": "What Good Readers Do", "meaning": "tell only the most important events, in a few words"}],
 "miss": pick("creative", "curiosity", "decision", "governor", "illegal", "impossible", "irregular", "mariner", "separate"),
 "game": game(1, [V("A grandmother", "When you do not know a word, look it up in the ", ".", ["vocalist", "dictionary", "advocate"], 1, "dict (say) + ionary: a book that says what words mean."),
                  V("A choir leader", "She has the strongest voice in our choir. She is our best ", ".", ["dictator", "verdict", "vocalist"], 2, "voc (voice) + al + ist: a person who uses their voice to sing."),
                  V("A storyteller", "The ", " gave orders, and no one was allowed to speak against him.", ["dictator", "vocalist", "dictionary"], 0, "dict (say) + ator: a ruler whose word is the law.")]),
 "art": art("monet-the-magpie.jpg", "The Magpie", "A painting of a snowy field and a wooden gate on a quiet morning, with a black and white bird sitting on the gate.",
            "Claude Monet painted this snowy morning in France in the winter of 1868 to 1869. It is far from Isaac's road, but it feels like the morning in Chapter 24: the light comes slow and quiet, with no red streaks in the sky.",
            "Claude Monet", "1868–1869", C + "Claude_Monet_-_The_Magpie_-_Google_Art_Project.jpg", "Public domain (Musée d'Orsay, via Wikimedia Commons)"),
 "virtue": {"name": "justice", "kind": "sort", "title": "Justice or not?", "intro": "You just read Chapter 24. Read each moment. Tap Justice or Not justice.",
   "items": [{"t": "Roundman leaps to help Pointy Nose and packs the cut with snow.", "ok": True, "why": "He helps a hurt man when the leader will not. That is working to right a wrong."},
             {"t": "Leader swings his shotgun at Pointy Nose for asking a question.", "ok": False, "why": "That is cruelty. Justice never means hurting someone to scare everyone else."},
             {"t": "Jumper jumps into the cold river so Isaac and Joseph can save Naomi.", "ok": True, "why": "He took a risk to free someone who was held wrongly."},
             {"t": "Leader says the girl and her family will pay.", "ok": False, "why": "He wants to get even. Getting even is not the same as making things right."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Chapter 25 is called A Day of Death, but read closely: by the end of the chapter, who has actually died? Today's poem is a sonnet about a statue that speaks. Notice how its shape fits its voice."},
  "words": {"text": "Today, decide whether each word carries voc and voke, calling out, or dict, saying and declaring. Then sort words by the rule that explains their spelling. Then three new lines to finish in the game."},
  "reading": {"text": "Read Chapter 25 in your book. After each big moment, say in one sentence what changed. Then write your own summary sentence in the Read Like a Writer box, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 25. Then write the first full draft of your final piece. Use what you have learned this year: strong verbs, clear pronouns, and sentences that show how ideas connect."}},
 "hook": {"q": "Your leader just hurt one of your own. Do you keep following him?",
  "options": [{"t": "Yes. He is the leader.", "reply": "Many people feel that way, especially when they are afraid. Watch what the soldiers in Chapter 25 start to wonder:"},
              {"t": "No. I would walk away.", "reply": "That takes courage. The soldiers in Chapter 25 do not walk away, but something changes inside them:"},
              {"t": "I would stay, but I would be scared.", "reply": "That is just what Tingle shows in Chapter 25:"}],
  "reveal": {"line": "Privately they wondered, What might he do to me?", "cite": "Chapter 25",
             "then": "As you read Chapter 25, watch how the soldiers' fear changes into something else."}},
 "how": [dict(WGRD, why="Summing up as you read keeps a busy chapter clear.", use="You will use this for question 1."),
  DOL, POEM,
  {"match": "Morphology", "do": ["Ask: is this word about calling out or about saying?", "Tap a word, then tap its meaning.", "Match all four."], "why": "voc and voke lean toward calling out. dict leans toward saying and declaring."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Read both versions in each pair.", "Tap the one that slows the reader down.", "Fix the passage in the box and name the three problems."], "why": "A reader should never have to stop and work out what the writer meant."},
  {"match": "Spelling", "do": ["Compare each base word with its longer form.", "Ask: did the base change, did a prefix stay whole, or is it a sound-alike?", "Tap a word, then tap its column."], "why": "Naming the rule tells you how to spell the word next time."},
  th("Chapter 25"),
  {"match": "Workshop", "do": ["Use your plan from Day 1.", "Write the whole piece in the box.", "Use strong verbs, clear pronouns and one combined sentence."], "why": "A first draft gets every idea down. You will polish it tomorrow.", "use": "Next lesson you will revise it."},
  vh("fill in your justice log"), ih("Chapter 25")],
 "glossary": [{"word": "antecedent", "in": "Grammar", "meaning": "the noun a pronoun points back to"},
              {"word": "sonnet", "in": "Poetry Corner", "meaning": "a poem of fourteen lines with a set rhyme pattern"}],
 "miss": pick("ability", "council", "interrupt", "it's", "perceptive", "permission", "submerge", "their", "transport"),
 "game": game(2, [V("A teacher", "Speak slowly and clearly. Good ", " helps listeners understand every word.", ["vocation", "diction", "provoke"], 1, "dict (say) + ion: the way you say your words."),
                  V("A wagon maker", "Building wagons is not just a job to me. It is my ", ".", ["vocation", "diction", "verdict"], 0, "voc (call) + ation: work you feel called to do."),
                  V("An elder", "Before the long walk, we ", " the memory of those who came before us.", ["dictate", "predict", "invoke"], 2, "in (on) + voke (call): to call on someone or something for help.")]),
 "art": art("friedrich-oak-in-snow.jpg", "Oak Tree in the Snow", "A painting of a huge old oak tree in a snowy field under a gray sky, with a broken branch lying on the ground.",
            "Caspar David Friedrich painted this old oak in the snow in Germany in 1827. Look at the broken branch on the ground. In Chapter 25, the soldiers fire into the treetops, and ice-covered branches crash down on the Choctaw Council's camp.",
            "Caspar David Friedrich", "1827", C + "Eiche_im_Schnee_-_Caspar_David_Friedrich.jpg", "Public domain (Wallraf-Richartz-Museum, via Wikimedia Commons)"),
 "virtue": {"name": "justice", "kind": "log", "title": "My justice log", "intro": "In Chapter 25, tap the moment you think shows the most justice.",
   "options": [{"t": "Mister Tibbi stands his ground: “We did nothing to deserve this.”"},
               {"t": "Isaac stops Joseph from fighting twenty soldiers, so Naomi will not lose him."},
               {"t": "Isaac tells both families, “We are stronger than the soldiers.”"}],
   "line": "Finish the sentence: This shows the most justice because…", "placeholder": "This shows the most justice because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "In Chapter 26, Leader reaches Isaac's family, still hunting for Naomi. Ruth answers him without arguing at all. Today you will reread one passage and sum it up in two sentences: what happened, and what it meant."},
  "words": {"text": "Put the speaking roots to work today. Then learn how transition words, like but, because and instead, show how ideas connect. Then check your own draft, one spelling pattern at a time."},
  "reading": {"text": "Read Chapter 26 in your book. Watch what Ruth does when Leader demands her little girl, and what stops Pointy Nose. Then try the Read Like a Writer sentence that begins with Instead, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 26. Then revise your draft with the checklist: strong verbs, a combined sentence, clear pronouns, and at least one transition word. Star your three best sentences."}},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Read each meaning.", "Tap a word, then tap its meaning.", "Match all four words."], "why": "If you know the root, you can work out a word you have never seen."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Read the Transitions box.", "Tap the better combination in each pair.", "Revise a paragraph of your own in the box, with one transition word."], "why": "Transition words tell the reader how one idea connects to the next."},
  {"match": "Spelling", "do": ["Ask: is the base a whole word?", "Is it a person who does something?", "Tap a word, then tap its column."], "why": "These are the spellings students most often miss in a final draft."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Reread one passage from Chapter 26.", "Sum it up in two sentences: what happened, and what it meant."], "why": "A short summary only works if it would not mislead someone who has not read it.", "use": "You will use this in the Read Like a Writer box."},
  th("Chapter 26", "For question 3, use one detail from each chapter."),
  {"match": "Workshop", "do": ["Read your draft from Day 2.", "Check it against the list, one pass at a time.", "Star your three best sentences and rewrite one."], "why": "Revising means making the piece clearer, not starting over.", "use": "Next lesson you will write the final version."},
  vh("use the justice meter"), ih("Chapter 26")],
 "glossary": [{"word": "transition", "in": "Grammar", "meaning": "a word that shows how one idea connects to the next"}],
 "hints": {"exhausted": ["Completely worn out.", "Joseph had a very long day.", "It starts with ex."],
           "revenge": ["Hurting someone back.", "Leader wants this in the morning.", "It starts with re."],
           "unconscious": ["Not awake.", "Stella, after the branch falls.", "un + conscious"],
           "gratitude": ["Thankfulness.", "Isaac whispers his thanks.", "It starts with grat."],
           "prophecy": ["A prediction.", "Leader says his comes true.", "It starts with pro."]},
 "miss": pick("dependable", "navigator", "possible", "printer", "remarkable", "teacher", "terrible", "visible"),
 "game": game(3, [V("A teacher", "I will read the sentences slowly, and you write them down. This is called ", ".", ["invocation", "dictation", "advocate"], 1, "dict (say) + ation: words said out loud for someone to write."),
                  V("A farmer", "The weather is ", " this winter. Snow one day, rain the next.", ["unpredictable", "vocal", "evoked"], 0, "un (not) + pre (before) + dict (say) + able: no one can say ahead of time."),
                  V("A singing teacher", "Hum first. Then open your mouth and ", " the sound.", ["dictate", "predict", "vocalize"], 2, "voc (voice) + al + ize: to make a sound with your voice.")]),
 "art": art("catesby-timber-rattlesnake.jpg", "The Rattle-Snake", "A hand-colored drawing of a coiled brown and black rattlesnake with its head raised and its rattle in the air.",
            "Mark Catesby drew and colored this timber rattlesnake for a book about the animals and plants of Carolina and Florida, printed in London in 1743. The small words are Latin labels: Vipera caudisona means the viper with a sounding tail. In Chapter 26, a rattlesnake rises over Nita.",
            "Mark Catesby", "1743", C + "Catesby_Natural_History_of_Carolina_plate_141_Timber_Rattlesnake.jpg", "Public domain (Missouri Botanical Garden, via Wikimedia Commons)", "Tap to learn about this drawing"),
 "virtue": {"name": "justice", "kind": "meter", "title": "The justice meter", "intro": "Think about one moment from Chapter 26.",
   "moment": "Leader demands Ruth's little girl. Ruth does not argue. She carries Nita's body, wrapped in a blanket, lays it by the fire, and says, “Here is my daughter.”",
   "ask": "How much justice did Ruth show? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "She showed this much because…",
   "take": "Mason's take: a lot. She told the truth calmly, and the soldiers had to see what had happened."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "This is the last day of the week. In Chapter 27, the soldiers reach the bonepickers' wagon, where Naomi is still hiding. Today's poem was written in the shape of a gravestone. Listen for how calm it is."},
  "words": {"text": "Last day with the speaking roots. Match words to the roots you have collected all year. Then explain a spelling pattern the way you would teach it to a friend, and finish the last lines of the game."},
  "reading": {"text": "Read Chapter 27 in your book. It ends in a frightening moment, so take it slowly. Then put the book together so far: who Isaac has become, what he faces, and what being a ghost lets him see."},
  "assignment": {"text": "Three questions about Chapter 27. Then write the final version of your piece, clean and complete. Add one sentence about what it shows about you as a writer. Copy your work and paste it into Canvas."}},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Tap a word.", "Then tap the root that unlocks it.", "Match all four."], "why": "Roots you learned months ago still unlock new words."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Tap the approach that catches more errors in each pair.", "Write your own three editing passes in the box.", "Say why that order works."], "why": "Editing one thing at a time catches more mistakes."},
  {"match": "Spelling", "do": ["Name the pattern before you place each word.", "Tap a word, then tap its column.", "Explain three words from your draft in the box."], "why": "If you can teach a pattern, you own it."},
  {"match": "What Good Readers Do", "do": ["Read the four lenses.", "Tap the one you will use today.", "Put the book together so far: character, conflict, point of view and theme."], "why": "Synthesizing means putting the pieces together into one big idea.", "use": "You will use this for question 3."},
  th("Chapter 27"),
  {"match": "Workshop", "do": ["Write the final version in the box.", "Check every pronoun and comma.", "Add one sentence: what does this piece show about you as a writer?"], "why": "Today you finish your piece and turn it in."},
  vh("pick the strongest moment of the week"), ih("Chapter 27")],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "put ideas together to make one bigger idea"}],
 "miss": pick("affect", "chronology", "competition", "definition", "manuscript", "photograph", "principle", "whose"),
 "game": game(4, [V("A grandfather", "You say you are cold, but you will not wear your coat. That is a ", ".", ["contradiction", "vocalist", "invocation"], 0, "contra (against) + dict (say) + ion: two things that say opposite things."),
                  V("A school principal", "The student with the best grades gives the farewell speech. She is the ", ".", ["advocate", "valedictorian", "dictator"], 1, "vale (farewell) + dict (say): the student who says farewell for the class."),
                  V("A council member", "The meeting began with an ", ", words that called everyone to listen.", ["edict", "prediction", "invocation"], 2, "in (on) + voc (call) + ation: words that call on everyone at the start.")]),
 "art": art("friedrich-dolmen-in-snow.jpg", "Dolmen in the Snow", "A painting of three old oak trees on a snowy hill around a low pile of large stones, under a pale winter sky.",
            "Caspar David Friedrich painted this ancient grave under old oaks in the snow in Germany in 1807. People built it thousands of years earlier to honor their dead. It is far from Isaac's road, but it fits Chapter 27, where the bonepickers search the ashes for every last bone to honor.",
            "Caspar David Friedrich", "1807", C + "Caspar_David_Friedrich_-_Cairn_in_Snow_-_Google_Art_Project.jpg", "Public domain (Galerie Neue Meister, Dresden, via Wikimedia Commons)"),
 "virtue": {"name": "justice", "kind": "best", "title": "The strongest moment of justice this week", "intro": "Look back at Chapters 24 to 27. Tap the moment you think shows justice the most.",
   "options": [{"t": "Roundman helps Pointy Nose after Leader hurts him."},
               {"t": "Mister Tibbi says, “We did nothing to deserve this.”"},
               {"t": "Ruth shows the soldiers her daughter's body."},
               {"t": "The bonepickers help their fallen friend while Leader shouts at them."},
               {"t": "Joseph leaps through the burning curtain to pull Naomi out."}],
   "line": "Finish the sentence: This shows justice the most because…", "placeholder": "This shows justice the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read this part of Chapter 24 out loud. Let the long list in the third sentence roll along without stopping. Then slow down while Isaac watches Joseph sleep. When it sounds smooth, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
BAD = ['Yakoke', 'pisa', 'lachike', 'Nahullo', 'Nani Humma', 'Choctaw word']
PAGE_WORDS = {'vocal', 'vocabulary', 'advocate', 'provoke', 'evoke', 'revoke', 'predict', 'contradict', 'verdict', 'dictate', 'edict', 'illuminate', 'empathy'}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    for b in BAD:
        if any(b in t for t in txt): sys.exit('%s: Choctaw word %s in a Listen script' % (k, b))
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    if '—' in json.dumps(v, ensure_ascii=False): sys.exit('%s: em dash' % k)
    if 'game' in v:
        for L in v['game']['lines']:
            ans = L['opts'][L['ok']]
            if ans in PAGE_WORDS: sys.exit('%s: game answer %s is on the pages' % (k, ans))
    json.dump(v, open('data/g5ela-23-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars')
