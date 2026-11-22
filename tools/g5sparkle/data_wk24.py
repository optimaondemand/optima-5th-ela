#!/usr/bin/env python3
"""Write data/g5ela-24-{1..4,fluency}.json (week 24, How I Became a Ghost Ch. 28-29 + the Trail of Tears
source study), Nov 22 2026. Every book line checked against planning docs/hbg_ocr.txt; history against the
1830 treaty and Harkins's 1831 letter (see scope_wk24.py). Bethany's choices: hook "The person who hurt you is
in danger" (24.1), Ears of Corn game (take a long word apart; the words are not on the pages or the check-in),
plates found by Claude (Audubon, King, Boisseau, Catlin), virtue courage (the pages' own). Listen texts are
Mason scripts; Choctaw words and Choctaw names are never in them. Each lesson's four Listen clips stay at or
under 1,000 characters."""
import json, sys
A = 'assets/art/hbg/'
C = 'https://commons.wikimedia.org/wiki/File:'
LOOK = ("Each long word is an ear of corn, like the corn the families cook in Chapter 29. The parts added to the front or the end are the husks. "
        "Tap each husk to peel it away. The base word is the ear inside.")
HOW = {"do": ["Read the long word.", "Find the part that can stand alone as a word. Leave it.", "Tap each part added to the front or the end.", "Tap Next word."],
       "why": "Long words in history writing are short words with parts added. Find the base and you can read and spell the rest."}
def E(w, parts, base, why, means): return {"w": w, "parts": parts, "base": base, "why": why, "means": means}
def game(day, ears):
    return {"type": "corn", "title": "Ears of Corn", "sub": "This week's word game · 3 words today", "after": "Spelling",
            "look": LOOK, "how": HOW, "doneLine": "Come back tomorrow for three more words." if day < 4 else "Every ear this week is open. Well done.", "ears": ears}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Say the second one in formal style, out loud.", "Tap Check My Work."],
       "why": "An essay about history uses exact words and names its sources."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud once.", "Read who wrote it, and when.", "Read Think About It and keep your answer in mind."],
        "why": "A poem written at the time is a primary source. It shows what someone thought back then."}
def vh(job): return {"match": "Virtue Watch", "do": ["Read what courage means.", "Read the example from this week.", "After you read, %s at the end of this tab." % job]}
def ih(read, then="Then do the Read Like a Writer box and the Virtue Watch below."): return {"match": "Chapter Introduction", "do": ["Read the introduction below.", read, then]}
def th(first, extra=None): return {"match": "Chapter Thinking", "do": [first, "Answer each question in 2 or more sentences.", extra or "Use details from the chapter as evidence."],
                                   "why": "These questions check what happened and what the author shows you."}
def art(file, title, alt, look, creator, date, url, lic, btn="Tap to learn about this painting"):
    return {"tab": "top", "file": A + file, "title": title, "alt": alt, "look": look, "lookBtn": btn, "creator": creator, "date": date, "license": lic, "url": url}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
ATION = "The ending is -ation. Say the last part: it sounds like ay-shun."
MENT = "The ending is -ment, added to a whole word."
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "This is the last week of How I Became a Ghost. In Chapter 28, the wolf comes back, and Naomi has to choose in a moment. This week you also set the novel beside real history. Start noticing what only a story can tell you."},
  "words": {"text": "This week's words are the ones a historian uses with care: claim, evidence, reasoning, treaty, removal, nation. Then formal style, the way an essay talks. In the game, peel the husks off a long word to find the base word inside."},
  "reading": {"text": "Read Chapter 28 in your book. Watch the panther and the wolf, and listen to what Naomi says when Leader asks her why. Then study the Read Like a Writer sentence, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 28. Then plan your source comparison. You need a claim, one detail from the novel, one line from a real source, and your reasoning. Today you only plan."}},
 "hook": {"q": "The person who hurt you is in danger. Only you can help. Do you?",
  "options": [{"t": "Yes. It is the right thing.", "reply": "That is hard to do. In Chapter 28, someone is asked why she did it. She answers:"},
              {"t": "No. Not after what they did.", "reply": "That is an honest answer, and many people would feel the same. In Chapter 28, someone chooses differently. When she is asked why, she says:"},
              {"t": "I am not sure.", "reply": "It is a hard question. In Chapter 28, someone has only a moment to decide. Afterward she says:"}],
  "reveal": {"line": "It was the right thing to do. It is the Choctaw way.", "cite": "Chapter 28",
             "then": "As you read Chapter 28, find out who says this, and whom she helps."}},
 "how": [dict(WGRD, why="A novel and a real source do different jobs. Knowing the difference makes you a sharper reader.", use="You will use this in your source comparison."),
  DOL,
  {"match": "Morphology", "do": ["Read the six words in the box.", "Tap a word, then tap its meaning.", "Think through the three questions, then tap See if you cracked it."], "why": "These six words are the tools of anyone who writes about history."},
  {"match": "Vocabulary", "do": ["Read the book sentence on each card.", "Guess what the word means.", "Tap the card to check.", "Match each word to its meaning."], "why": "These words show up in this week's chapters. Knowing them first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the two sentences. They say the same thing.", "Think through the questions.", "Tap Now check your thinking.", "Tap the formal version in each pair, then write in the box."], "why": "Formal style tells the reader you are being exact, and a source transition tells where a fact came from."},
  {"match": "Spelling", "do": ["Look at the long words.", "Think through the questions.", "Tap a word, then tap the column for its ending."], "why": "The ending tells you the word's job, and it is spelled the same way every time."},
  th("Read Chapter 28 first."),
  {"match": "Workshop", "do": ["Read the two real sources in the blue box.", "Choose one line to use.", "In the box, write your claim, a detail from the novel, the source line, and your reasoning."],
   "why": "A source comparison shows what a story and a real record each tell you.", "use": "Tomorrow you will draft it."},
  vh("sort the moments"), ih("Open your book and read Chapter 28.")],
 "glossary": [{"word": "primary source", "in": "What Good Readers Do", "meaning": "something written or made at the time, by someone who was there"},
              {"word": "secondary source", "in": "What Good Readers Do", "meaning": "something written later, by someone who studied the event"}],
 "miss": {"authority": "author + ity. The ending is -ty.", "declaration": ATION, "displacement": MENT, "government": "govern + ment. Do not lose the n before -ment.",
          "negotiation": ATION, "relocation": ATION, "settlement": MENT, "sovereignty": "sovereign + ty. The ending is -ty.", "liberty": "The ending is -ty, as in safety and loyalty."},
 "game": game(1, [E("mistreatment", ["mis", "treat", "ment"], 1, "mis- means badly, and -ment makes a noun.", "treating someone badly."),
                  E("unfairness", ["un", "fair", "ness"], 1, "un- means not, and -ness makes a noun.", "the state of not being fair."),
                  E("rebuilding", ["re", "build", "ing"], 1, "re- means again.", "building again.")]),
 "art": art("audubon-black-american-wolf.jpg", "Black American Wolf", "A hand-colored print of a black wolf running across open grassland with its mouth open.",
            "This print comes from The Viviparous Quadrupeds of North America, a book of animal pictures by John James Audubon and his sons, printed in 1845. John Woodhouse Audubon, his son, drew this wolf. Viviparous quadrupeds means four-legged animals that give birth to live young. In Chapter 28, the wolf returns.",
            "John Woodhouse Audubon", "1845", C + "Black_American_Wolf_(Canis_lupus)_from_the_viviparous_quadrupeds_of_North_America_(1845)_illustrated_by_John_Woodhouse_Audubon_(1812-1862).jpg",
            "Public domain artwork; scan by rawpixel from the John James Audubon Center (CC BY 2.0), via Wikimedia Commons", "Tap to learn about this print"),
 "virtue": {"name": "courage", "kind": "sort", "title": "Courage or not?", "intro": "You just read Chapter 28. Read each moment. Tap Courage or Not courage.",
   "items": [{"t": "Joseph, as the panther, leaps between the wolf and Leader.", "ok": True, "why": "He risks himself to save a man who tried to kill him."},
             {"t": "Naomi says, “We cannot let this happen,” about the man who vowed she would die.", "ok": True, "why": "Doing right by an enemy is one of the hardest kinds of courage."},
             {"t": "Leader kicks the dead wolf so it lands at Naomi's feet.", "ok": False, "why": "The danger is already over. Showing off your strength takes no courage."},
             {"t": "Roundman aims his shotgun at Naomi and Joseph and shouts.", "ok": False, "why": "Pointing a weapon at two children who just saved a life is not brave."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Chapter 29 is the last chapter. Read it closely and mark the moments you would want to check against a real record. Today's poem was written in eighteen thirty-four. That makes the poem itself a piece of history."},
  "words": {"text": "Today, decide what each history word really claims. Then tell formal writing from casual talk, and sort long words by the part at their center. Three new ears of corn are waiting in the game."},
  "reading": {"text": "Read Chapter 29 in your book. It is short. Notice how the families end the day, and who promises to return. Then write a sentence shaped like the one in the Read Like a Writer box, and finish with the Virtue Watch."},
  "assignment": {"text": "Three questions about Chapter 29. Then draft your source comparison paragraph. Use formal style, and begin each piece of evidence with a source transition, so your reader knows where it came from."}},
 "how": [dict(WGRD, why="Some things in a novel can be checked against a record, and some cannot. Good readers notice which.", use="You will use this in your draft today."),
  DOL, POEM,
  {"match": "Morphology", "do": ["Read the six words in the box.", "Ask what each word claims.", "Tap a word, then tap its meaning."], "why": "A word like treaty or removal carries a point of view inside it."},
  {"match": "Vocabulary", "do": ["Read each sentence from the book.", "Look for clues around the word.", "Tap a word, then tap its meaning."], "why": "Clues in a sentence can tell you what a word means."},
  {"match": "Grammar", "do": ["Read the casual and formal pair.", "Tap the formal version in each pair.", "Add a source transition to each claim in the box."], "why": "A source transition tells your reader whether a fact comes from the novel or from the record."},
  {"match": "Spelling", "do": ["Find the root inside each long word.", "Tap a word.", "Then tap the column for its root."], "why": "You already know these roots. They hold the long word together."},
  th("Read Chapter 29 first."),
  {"match": "Workshop", "do": ["Use your plan from Day 1 and the two sources in the blue box.", "Write the whole paragraph in the box.", "Start each piece of evidence with a source transition."], "why": "A first draft gets every idea down. You will revise it tomorrow.", "use": "Next lesson you will revise it."},
  vh("fill in your courage log"), ih("Open your book and read Chapter 29.")],
 "glossary": [{"word": "register", "in": "Grammar", "meaning": "how formal or casual your words are"},
              {"word": "primary source", "in": "Poetry Corner", "meaning": "something written or made at the time, by someone who was there"}],
 "miss": {"advocate": "ad + voc + ate. voc means voice or call.", "contradict": "contra + dict. dict means say.", "displacement": "dis + place + ment. The base is place.",
          "evidence": "e + vid + ence. vid means see, like vis.", "perspective": "per + spect + ive. spect means look.", "replacement": "re + place + ment. The base is place.", "verdict": "ver + dict. dict means say."},
 "game": game(2, [E("friendship", ["friend", "ship"], 0, "-ship makes a noun about a bond between people.", "the bond between friends."),
                  E("peacefully", ["peace", "ful", "ly"], 0, "-ful means full of, and -ly tells how. This word has two husks at the end.", "in a way that is full of peace."),
                  E("retelling", ["re", "tell", "ing"], 1, "re- means again.", "telling a story again.")]),
 "art": art("king-pushmataha.jpg", "Pushmataha, a Choctaw chief", "A printed portrait of a man with dark hair, wearing a blue army coat with gold shoulder pieces and a white ruffled shirt.",
            "This is the real Pushmataha. Charles Bird King painted him in Washington, D.C., in 1824, the year the chief died there. This print was made from that painting between 1837 and 1844. Look at the army coat: he held the rank of brigadier general. He died six years before the novel begins, so in the story he comes as a ghost.",
            "Print after a painting by Charles Bird King; published by McKenney and Hall", "painted 1824; printed 1837–1844", C + "Pushmataha_high_resolution.jpg", "Public domain (Smithsonian American Art Museum, via Wikimedia Commons)", "Tap to learn about this portrait"),
 "virtue": {"name": "courage", "kind": "log", "title": "My courage log", "intro": "In Chapter 29, tap the moment you think shows the most courage.",
   "options": [{"t": "Naomi, home for one day, insists on cooking for both families."},
               {"t": "Isaac and Nita join the gathering in full view of everyone."},
               {"t": "The winter is fierce and food is scarce, and the families keep going together."}],
   "line": "Finish the sentence: This shows the most courage because…", "placeholder": "This shows the most courage because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "The novel is finished. Today you read two real sources from the years of the Choctaw removal: part of a treaty, and part of a letter by a Choctaw chief. Ask of each one: who wrote this, when, and why?"},
  "words": {"text": "Put the history words to work: primary source, secondary source, perspective, bias. Then practice naming your source before every claim. In the game, look for the part that can stand alone as a word."},
  "reading": {"text": "Read the two sources slowly. They are short, and the plain words under each one will help. Keep the story and the record apart: the novel says eighteen thirty, and the treaty sets the removal for eighteen thirty-one to eighteen thirty-three."},
  "assignment": {"text": "Three questions about the novel and the sources. Then revise your draft with the checklist: formal style, two source transitions, a claim with evidence and reasoning, and every fact tied to its source."}},
 "readnow": {"text": "Today you read two real sources on this page. Keep your book open to Chapters 28 and 29.", "step": "Read the introduction"},
 "how": [
  DOL,
  {"match": "Morphology", "do": ["Read each meaning.", "Tap a word, then tap its meaning.", "Match all four."], "why": "You need these four words to talk about where information comes from."},
  {"match": "Vocabulary", "do": ["Type the word that fits each sentence.", "Open the Word Bank if you need it.", "Tap Check My Words."], "why": "Putting a word back in its sentence shows you really know it."},
  {"match": "Grammar", "do": ["Read the example with two sources.", "Tap the version that names its source in each pair.", "Write your paragraph in the box, with two source transitions."], "why": "When every claim names its source, the reader can tell the story from the record."},
  {"match": "Spelling", "do": ["Look at each word's ending.", "Tap a word.", "Then tap the column for its ending."], "why": "You will need these words in your own paragraph."},
  {"match": "What Good Readers Do", "do": ["Tap your lens for today.", "Read the two sources on the Reading tab.", "Ask what each one can tell you, and what it leaves out."], "why": "No single source tells the whole story.", "use": "You will use this for questions 1 and 2."},
  {"match": "Two Real Sources", "do": ["Read Source A, then its plain words.", "Read Source B, then its plain words.", "Read the note about the story and the record."], "why": "These are real words from 1830 and 1831. They are the record you will set beside the novel."},
  th("Read the two sources first.", "Name the source each fact comes from."),
  {"match": "Workshop", "do": ["Read your draft from Day 2.", "Check it against the list, one pass at a time.", "Show your strongest sentence and one you rewrote."], "why": "Revising means making the piece clearer, not starting over.", "use": "Next lesson you will write the final version."},
  vh("use the courage meter"), ih("Read the two real sources.", "Then do the Read Like a Writer box and the Virtue Watch below.")],
 "glossary": [{"word": "bias", "in": "Morphology", "meaning": "a leaning toward one side that shapes what someone writes down"},
              {"word": "attribute", "in": "Grammar", "meaning": "say where a fact or idea came from"}],
 "hints": {"lifeless": ["Without life.", "The wolf, after the fight.", "life + less"],
           "survived": ["Stayed alive.", "Leader says it about Joseph and the cave.", "It starts with sur."],
           "honor": ["To show great respect.", "Why the old chief comes that day.", "It starts with a silent h."],
           "reunited": ["Back together.", "Naomi and her parents.", "re + united"],
           "protector": ["Someone who keeps you safe.", "The families meet one in the last chapter.", "protect + or"]},
 "miss": {"agreement": MENT, "declaration": ATION, "displacement": MENT, "documentation": ATION, "federal": "It ends in -al and describes a noun, as in federal law.",
          "historical": "It ends in -al and describes a noun, as in historical record.", "negotiation": ATION, "settlement": MENT, "national": "nation + al. It describes a noun, as in national law."},
 "game": game(3, [E("unjustly", ["un", "just", "ly"], 1, "un- means not, and -ly tells how.", "in a way that is not fair or right."),
                  E("encampment", ["en", "camp", "ment"], 1, "en- means in, and -ment makes a noun.", "a place where people have set up camp."),
                  E("leadership", ["lead", "er", "ship"], 0, "-er makes a person who leads, and -ship makes a noun. Two husks at the end.", "the work of leading people.")]),
 "art": art("boisseau-louisiana-indians-bayou.jpg", "Louisiana Indians Walking Along a Bayou", "A painting of a family walking in a line beside a bayou under tall trees: a man with a long gun, a child, and two women carrying loads on their backs.",
            "Alfred Boisseau painted this family in Louisiana in 1847. They are believed to be Choctaw. This is not the Trail of Tears: it was painted about fifteen years later, and some Choctaw families stayed in Mississippi and Louisiana. It is one of very few paintings of Choctaw people made in those years by someone who saw them.",
            "Alfred Boisseau", "1847", C + "Louisiana_Indians_Walking_Along_a_Bayou_-_Alfred_Boisseau_(New_Orleans_Mus_of_Art_56.34).jpg", "Public domain (New Orleans Museum of Art, via Wikimedia Commons)"),
 "virtue": {"name": "courage", "kind": "meter", "title": "The courage meter", "intro": "Think about one moment from real history, in Source B.",
   "moment": "George W. Harkins, a real Choctaw chief, wrote in 1831: “my people are dear to me, with them I must go.” He wrote that he could not stay behind and leave them to struggle alone.",
   "ask": "How much courage did Harkins show? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He showed this much because…",
   "take": "Mason's take: a great deal. He chose a hard road so his people would not walk it without him."},
}
D[4] = {
 "listen": {
  "warmup": {"text": "Last day of the unit. Today's poem imagines a Native speaker, but a white poet wrote it. Set it beside the letter a Choctaw chief wrote for himself, and ask which one you would trust, and for what."},
  "words": {"text": "One last time: say why the exact word matters when you write about history. Keep the novel and the record apart in every sentence. Then open the last three ears of corn."},
  "reading": {"text": "Reread the two sources, then look back through Chapters 28 and 29. Choose one moment from the novel and one line from a source to set side by side. Then try the Read Like a Writer box on your own."},
  "assignment": {"text": "Write your claim, then your final source comparison paragraph, formal and complete. Last, tell what a story told by a ghost taught you about real history. Copy your work and paste it into Canvas."}},
 "readnow": {"text": "Reread the two sources on this page. Then look back at Chapters 28 and 29 in your book.", "step": "Read the introduction"},
 "how": [
  DOL, POEM,
  {"match": "Morphology", "do": ["Read why the exact word matters.", "Tap a word, then tap its meaning.", "Match all four."], "why": "The word you choose for an event is part of your argument about it."},
  {"match": "Vocabulary", "do": ["Read each word and its meaning.", "Write one sentence for each word.", "Make each sentence show the meaning."], "why": "Using a word in your own sentence is the best proof you know it."},
  {"match": "Grammar", "do": ["Read the blurred and the distinct sentence.", "Tap the version that keeps the novel and the record apart.", "Explain the problem in the box, with one blurred and one fixed sentence."], "why": "A reader must always know what is made up and what is on the record."},
  {"match": "Spelling", "do": ["Ask what job each word does.", "Tap a word.", "Then tap noun, verb or adjective."], "why": "The ending of a long word tells you its job in the sentence."},
  {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Say what the novel is for and what the sources are for."], "why": "Synthesizing means putting the pieces together into one big idea.", "use": "You will use this in your final paragraph."},
  {"match": "Sources Again", "do": ["Reread Source A.", "Reread Source B.", "Choose the line you will quote."], "why": "Your paragraph needs the exact words of one real source."},
  th("Look back at Chapters 28 and 29 and the two sources.", "For question 1, write only your claim and name your two pieces of evidence."),
  {"match": "Workshop", "do": ["Write the final paragraph in the box.", "Check: claim, evidence from the novel, evidence from a source, reasoning.", "Add what this ghost story taught you about history."], "why": "Today you finish your comparison and turn it in."},
  vh("pick the strongest moment of the week"), ih("Reread the two sources. Then look back at Chapters 28 and 29.")],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "put ideas together to make one bigger idea"},
              {"word": "sovereignty", "in": "Daily Oral Language", "meaning": "a nation's right to govern itself"}],
 "miss": {"contradict": "It names an action: to say the opposite. A verb.", "displacement": "It ends in -ment, so it names a thing. A noun.", "federal": "It ends in -al and describes, as in federal law. An adjective.",
          "historical": "It ends in -al and describes, as in historical record. An adjective.", "negotiate": "It ends in -ate and names an action. A verb.", "primary": "It describes, as in primary source. An adjective.",
          "sovereignty": "It ends in -ty, so it names a thing. A noun.", "testify": "It ends in -ify and names an action. A verb.", "testimony": "It names a thing: what a witness says. A noun."},
 "game": game(4, [E("unwillingly", ["un", "will", "ing", "ly"], 1, "un- means not. This word has three husks: one at the front and two at the end.", "without wanting to."),
                  E("truthfulness", ["truth", "ful", "ness"], 0, "-ful means full of, and -ness makes a noun.", "the habit of telling the truth."),
                  E("renewal", ["re", "new", "al"], 1, "re- means again, and here -al makes a noun.", "making something new again.")]),
 "art": art("catlin-mosholatubbee.jpg", "Mó-sho-la-túb-bee, a Choctaw chief", "A painted portrait of a seated man in a blue-green patterned coat with a red sash, holding a feather fan and a long pipe.",
            "George Catlin painted this Choctaw chief in 1834, in Indian Territory, west of the Mississippi River. He was one of the leaders who signed the Treaty of Dancing Rabbit Creek in 1830. Four years later, after the removal, he sat for this portrait in the West. The Choctaw Nation is still there today, in Oklahoma.",
            "George Catlin", "1834", C + "Mosholatubbee.jpg", "Public domain (Smithsonian American Art Museum, via Wikimedia Commons)", "Tap to learn about this portrait"),
 "virtue": {"name": "courage", "kind": "best", "title": "The strongest moment of courage this week", "intro": "Look back at Chapters 28 and 29 and the two sources. Tap the moment you think shows courage the most.",
   "options": [{"t": "Joseph, as the panther, faces the wolf to save Leader."},
               {"t": "Naomi helps save the man who vowed she would die."},
               {"t": "The families keep going together through a fierce winter."},
               {"t": "In real history, George W. Harkins goes with his people instead of staying behind."}],
   "line": "Finish the sentence: This shows courage the most because…", "placeholder": "This shows courage the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the opening of Chapter 29 out loud. The first paragraph is good news, so let it arrive calmly. Then let Naomi and her mother sound like two different people. When it sounds smooth, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
BAD = ['Yakoke', 'pisa', 'lachike', 'Nahullo', 'Nani Humma', 'Pushmataha', 'Mosholatubbee', 'Choctaw word']
PAGE_WORDS = {'authority', 'declaration', 'displacement', 'government', 'negotiation', 'relocation', 'settlement', 'sovereignty', 'liberty', 'advocate', 'contradict', 'evidence',
              'perspective', 'replacement', 'verdict', 'agreement', 'documentation', 'federal', 'historical', 'national', 'negotiate', 'primary', 'testify', 'testimony',
              'lifeless', 'survived', 'honor', 'reunited', 'protector', 'govern', 'settle', 'declare', 'relocate'}
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    for b in BAD:
        if any(b in t for t in txt): sys.exit('%s: Choctaw word or name %s in a Listen script' % (k, b))
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    if '—' in json.dumps(v, ensure_ascii=False): sys.exit('%s: em dash' % k)
    if 'game' in v:
        for e in v['game']['ears']:
            if e['w'] in PAGE_WORDS: sys.exit('%s: game word %s is on the pages' % (k, e['w']))
            if ''.join(e['parts']) != e['w']: sys.exit('%s: parts of %s do not rebuild it' % (k, e['w']))
    json.dump(v, open('data/g5ela-24-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
