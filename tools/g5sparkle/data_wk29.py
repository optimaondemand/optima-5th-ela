#!/usr/bin/env python3
"""Write data/g5ela-29-{1..4,fluency}.json (week 29, By the Great Horn Spoon! Ch. 13-15 + voice/tone day), Nov 23-24 2026.
Every book line checked against the By the Great Horn Spoon! text (project doc, Ch. 13-15; nothing from Ch. 16 on).
History: California State Parks (coyote holes 20-40 feet, miners lowered in buckets; rockers and long toms, "The Evolution of
Gold Panning"); Sierra College Journal of Sierra Nevada History & Biography 2009 (long tom 10-20 feet); H. H. Bancroft, California
Inter Pocula (1888): gold dust fixed at $16 an ounce in San Francisco, much less in the mines; Benjamin Madley, Journal of American
History 111.1 (2024), Native Hawaiians in the Gold Rush; Kanaka Creek (Sierra County), Kanaka Bar (Trinity County); PBS American
Experience and Calisphere (Native population about 150,000 in 1848 to about 30,000 by 1870; Chinese miners on abandoned claims;
the 1852 $3-a-month foreign miners' tax aimed at Chinese miners); Oakland Museum of California (Miwok woman washing gold in a basket).
Bethany's choices: hook on 29.2 (leaving vs coming back); virtue integrity (keeping your word); Climb Out of the Coyote Hole (a bucket of
pay dirt climbs the rope; no mascot); 1963 notes on 29.1-29.3; real-history card on 29.1. Q4 audio paused: Listen texts are Mason
scripts, at or under 1,000 characters a lesson."""
import json, re, sys, html, io
LOOK = ("A coyote hole is a deep shaft miners dug straight down to bedrock, where heavy gold settles. "
        "Each right answer hauls the bucket of pay dirt up one notch of the rope. A wrong answer lets loose dirt slide it back down one notch.")
HOW = {"do": ["Read the clue.", "Tap the word that fits.", "Tap Haul it up for the next clue."],
       "why": "A suffix is spelled the same way every time, and a word family keeps its base. Knowing both keeps your spelling right."}
def r(clue, opts, ok, why, miss=None):
    d = {"clue": clue, "opts": opts, "ok": ok, "why": why}
    if miss: d["miss"] = miss
    return d
def game(day, rounds):
    return {"type": "climb", "title": "Climb Out of the Coyote Hole", "sub": "This week's word game · 8 notches today", "after": "Spelling", "look": LOOK, "how": HOW,
            "doneLine": "Come back tomorrow for eight more notches." if day < 4 else "Four days, thirty-two notches. The pay dirt is out of the hole.", "rounds": rounds}
WGRD = {"match": "What Good Readers Do", "do": ["Read the three lenses.", "Tap the one you will use today.", "Keep it in mind as you read. You will use it at the end."]}
DOL = {"match": "Daily Oral Language", "do": ["Tap the highlighted words in the first sentence.", "Write the second sentence correctly in your reading journal.", "Tap See the Answer to check."],
       "why": "Starting sentences in different ways is one of the easiest ways to make writing lively."}
RW = {"match": "Read & Write", "do": ["Read the question.", "Write 2 or 3 sentences in your reading journal.", "Then go on to Word Study."], "why": "Thinking before you read gives you something to watch for."}
POEM = {"match": "Poetry Corner", "do": ["Read the poem out loud twice.", "Read the tip.", "Answer the question in your reading journal."],
        "why": "Naming each part of a poem shows how they work together, the same way voice works in a novel."}
def rh(ch):
    return {"match": "Read: Chapter %d" % ch, "do": ["Read the reading focus below.", "Open your book and read Chapter %d." % ch, "Then do the Read Like a Writer box and the Virtue Watch at the end of this tab."],
            "why": "The pause boxes are places to stop and think while you read."}
WS = lambda day: {"match": "Writer", "do": {1: ["Read today's step.", "Copy one paragraph from your adventure draft into the box.", "List three spots to change: voice, dialogue, description."],
                                          2: ["Read today's step.", "Rewrite your paragraph, starting with the dialogue.", "Use the frames if you get stuck."],
                                          3: ["Read the five checklist points.", "Check your paragraph one point at a time.", "Write the revised paragraph."],
                                          4: ["Read your paragraph out loud once more.", "Put the final version in the box.", "Copy your work and paste it into Canvas."]}[day],
                  "why": "Voice, dialogue and description are what make an adventure sound like nobody else's."}
NOTE_HAW = {"tab": "reading", "after": "Read: Chapter 13", "title": "A note before you read: words from 1963", "min": 2,
  "intro": "This book was written in 1963. One line in Chapter 13 uses an old name for some of the people at the auction. Here is what to know.",
  "items": [{"term": "What the book says", "meaning": "The auction crowd includes Kanakas from the Sandwich Islands. Sandwich Islands was the old English name for Hawaii. Outsiders used Kanaka as a label for Native Hawaiians and other Pacific Islanders, often in an unkind way."},
            {"term": "The true history", "meaning": "Kānaka is the Hawaiian word for people. Native Hawaiians sailed to California on trading and whaling ships long before the Gold Rush, and in 1839 John Sutter brought a group of Hawaiian workers with him. Many Hawaiians mined gold in 1848 and 1849, and places such as Kanaka Creek and Kanaka Bar are named for them."},
            {"term": "A crowd from everywhere", "meaning": "The auction crowd, with miners from France, Mexico, Chile, Germany, Hawaii and the eastern states, is true to life. The gold fields drew people from all over the world."}],
  "note": "Sources: historian Benjamin Madley, Journal of American History (2024); California place names in Sierra and Trinity counties."}
HIST = {"tab": "reading", "after": "Read: Chapter 13", "title": "Real history: how miners dug for gold", "min": 2,
  "intro": "Pitch-pine Billy is made up. The ways he digs for gold are real.",
  "items": [{"term": "Coyote holes", "meaning": "Where gold lay deep, miners dug narrow shafts straight down, often 20 to 40 feet, to reach bedrock, where heavy gold settles. Miners were lowered into them in buckets."},
            {"term": "The rocker", "meaning": "A rocker, or cradle, was a wooden box on rockers. Miners shoveled in dirt, poured in water and rocked it, and the gold caught on wooden bars at the bottom. It washed more dirt than a pan, and two or three men often worked one together."},
            {"term": "The long tom", "meaning": "A long tom was a wooden trough 10 to 20 feet long set in running water. Several men shoveled dirt in, and the gold caught on bars at the bottom. It washed more dirt than a rocker."},
            {"term": "Sixteen dollars an ounce", "meaning": "In San Francisco, gold dust was traded at about $16 an ounce, a price merchants agreed on. Out in the camps, miners often got much less for it. The prices in Chapter 13 are the novel's, but prices in the camps really were very high, because everything had to be hauled in."}],
  "note": "Sources: California State Parks; Journal of Sierra Nevada History and Biography; H. H. Bancroft, California Inter Pocula (1888)."}
NOTE_SAV = {"tab": "reading", "after": "Read: Chapter 14", "title": "A note before you read: words from 1963", "min": 1,
  "intro": "One word near the end of Chapter 14 needs a note.",
  "items": [{"term": "What the book says", "meaning": "As the partners head into the mountains, Jack keeps an eye out for rabbits, squirrels, savages and outlaws. Savages was an insult for Native people. Putting them in a list with animals treats them as wild and dangerous."},
            {"term": "The true history", "meaning": "The hills the partners walk into were the homelands of the Nisenan, Miwok and Maidu peoples, who had lived there for thousands of years. The danger ran the other way: miners took their land and rivers, and many Native people were killed or driven out."},
            {"term": "Still here", "meaning": "California's Native nations are still here today, and many keep their languages and traditions alive."}],
  "note": "Sources: Oakland Museum of California; PBS American Experience."}
NOTE_15 = {"tab": "reading", "after": "Read: Chapter 15", "title": "A note before you read: words from 1963", "min": 2,
  "intro": "Chapter 15 has a few lines about Native Californians and Chinese miners. Here is what to know.",
  "items": [{"term": "What the book says", "meaning": "The partners see Native women panning for gold, and a prospector calls them Digger Indians. He says they trade their gold for cloth and calls them poor devils, like a bunch of young'uns. Digger was an insult, and calling grown people children is unkind and untrue."},
            {"term": "The true history", "meaning": "Many Native Californians mined gold in 1848 and 1849. Miwok and Nisenan women washed gold in tightly woven baskets, just as the chapter shows. Then miners took their land and rivers, and disease and violence followed. California's Native population fell from about 150,000 in 1848 to about 30,000 by 1870."},
            {"term": "Chinese miners", "meaning": "The chapter says Chinese miners moved into camps others had left. That was common. Chinese miners often worked old claims with great care and found gold others had missed. In 1852 California passed a tax of $3 a month on foreign miners that was aimed at them."}],
  "note": "Sources: Oakland Museum of California; PBS American Experience; Calisphere, University of California."}
D = {}
D[1] = {
 "listen": {
  "warmup": {"text": "Before you read, answer the question on the card in your reading journal. Then set your lens. This week is all about voice: the way Fleischman sounds like nobody else. Listen for it from the very first page."},
  "words": {"text": "This week's endings are o u s, which means full of, i v e, which means tending to, and i t y, which names a quality. The spelling focus is word families, words that grow from one base. In the game, every right word hauls the bucket up the coyote hole."},
  "reading": {"text": "Read Chapter 13, A Bushel of Neckties. The partners settle into the diggings, and then comes an auction. Watch what Jack does when one small word costs him real gold. Then try the Read Like a Writer box."},
  "assignment": {"text": "Three questions about Chapter 13. Then plan your revision. Copy one paragraph from your adventure draft, and list three spots to change: one for voice, one for dialogue, and one for description."}},
 "how": [dict(WGRD, why="Voice is built from word choices. Noticing them is the first step.", use="You will use it in reading question 3."), DOL, RW,
  {"match": "Morphology", "do": ["Read the three endings and what they mean.", "Think through the questions, then tap See what was hiding.", "Type the missing ending in each word, then tap Check Suffixes."], "why": "Three small endings turn words into describing words and names for qualities."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Watch for the words as you read."], "why": "Knowing the words first keeps the reading smooth."},
  {"match": "Grammar", "do": ["Read the sentences and listen to the rhythm.", "Think through the questions, then tap Now check your thinking.", "Tap a sentence, then tap the column for how it opens."], "why": "Starting sentences in different ways keeps writing lively."},
  {"match": "Spelling", "do": ["Look at the four families.", "Think through the questions, then tap Now name the pattern.", "Tap a word, then tap its family."], "why": "If you know one word in a family, you can check the spelling of the others."},
  rh(13), WS(1)],
 "glossary": [{"word": "voice", "in": "What Good Readers Do", "meaning": "the way a writer sounds on the page, like a speaking voice"},
              {"word": "suffix", "in": "Morphology", "meaning": "an ending added to a word that changes its meaning or job"}],
 "hints": {"ous": ["This ending means full of.", "Three letters: o, then two more.", "o, u, s"], "ive": ["This ending means tending to.", "Three letters, ending in e.", "i, v, e"],
           "ty": ["This word names a quality. The i is already there.", "Two letters finish -ity.", "t, y"]},
 "miss": {"signature": "sign + ature: the sign family keeps its silent g.", "signal": "sign + al: you can see sign inside it.",
          "natural": "nature + al: the e drops.", "naturally": "natural + ly: two l's.",
          "decision": "decide + ion: the d becomes s.", "decisive": "decide + ive: the d becomes s again."},
 "game": game(1, [r("Full of courage (a brave miner)", ["courageous", "couragous", "courageious"], 0, "courage keeps its e before -ous, so the g stays soft.", "Keep the whole base word courage, then add -ous."),
                  r("Tending to catch the eye (bright neckties)", ["atractive", "attractive", "attracktive"], 1, "attract + ive: two t's, then c, t.", "Spell attract first, then add -ive."),
                  r("The state of being generous", ["generousity", "generocity", "generosity"], 2, "generous drops its u before -ity.", "Watch the ous: one letter drops before -ity."),
                  r("Full of mystery", ["mysterious", "mysterous", "mysteryous"], 0, "mystery changes y to i before -ous.", "The y in mystery changes before the ending."),
                  r("Which word is in the same family as camp?", ["cramp", "campfire", "champ"], 1, "camp + fire: a fire in camp.", "Look for the whole word camp inside."),
                  r("Which word is in the same family as miner?", ["minor", "minute", "mine"], 2, "A miner is someone who works a mine.", "minor sounds the same but is a different word."),
                  r("Which word is in the same family as reputation?", ["repute", "report", "repeat"], 0, "repute + ation: what people think of you.", "Look for the base rep-u-t inside."),
                  r("Tending to talk a lot", ["talketive", "talkative", "talkive"], 1, "talk + ative.", "The ending here is -ative, with an a.")]),
 "cards": [HIST, NOTE_HAW],
 "virtue": {"name": "integrity", "kind": "sort", "title": "Keeping your word, or not?", "intro": "This week's virtue is integrity: keeping your word and doing what you said you would, even when it costs you. Sort these everyday examples.",
   "items": [{"t": "You promised to help a neighbor rake leaves. A friend invites you to the movies, and you rake the leaves anyway.", "ok": True, "why": "You do what you said, even though something more fun came up."},
             {"t": "You said you'd return a book on Friday, but you keep it because no one reminds you.", "ok": False, "why": "Your word should not depend on someone checking."},
             {"t": "You agreed to a trade, then found out your card was worth more. You trade anyway.", "ok": True, "why": "A deal is a promise, even when it turns out to cost you."},
             {"t": "You tell your team you'll be at practice, then skip because it's raining.", "ok": False, "why": "A little rain is not a good reason to go back on your word."}]},
}
D[2] = {
 "listen": {
  "warmup": {"text": "Answer the question on the card first. Then read a poem by Robert Louis Stevenson out loud, twice. Listen for the gallop. Today you name every part of the poem at work: form, rhyme, beat, line breaks, and comparisons."},
  "words": {"text": "Today you find the endings o u s, i v e and i t y in new words, and you spot the spelling shifts inside a word family. Then write your paragraph with sentences that start in different ways. Eight more notches up the coyote hole."},
  "reading": {"text": "Read Chapter 14, The Prospectors. The partners get ready to leave Hangtown. Watch Stubb the burro, listen to how each person talks, and notice what Praiseworthy reveals about his plan."},
  "assignment": {"text": "Three questions about Chapter 14. Then rewrite your paragraph, starting with the dialogue. Make each person sound like themselves. Use the frames if you get stuck."}},
 "hook": {"q": "Your friends are staying in camp. You're heading into the mountains with your partner. Which is harder: leaving, or coming back?",
  "options": [{"t": "Leaving. Saying goodbye is the hard part.", "reply": "Jack feels that too. But listen to what he thinks next:"},
              {"t": "Coming back. Things will have changed.", "reply": "Jack agrees with you. Listen:"},
              {"t": "Neither. It's an adventure!", "reply": "Jack is excited too, but he notices something. Listen:"}],
  "reveal": {"line": "Still, coming back would be even harder.", "cite": "Chapter 14",
             "then": "Read Chapter 14 to find out why Jack thinks so."}},
 "how": [dict(WGRD, why="Every word that carries a tone is a choice the author made.", use="You will use it in reading question 1."), DOL, RW, POEM,
  {"match": "Grammar", "do": ["Read the four ways to vary sentences.", "Write your paragraph of 5 to 7 sentences in the box.", "Label each kind of sentence in parentheses."], "why": "This is your Show What You Know for grammar this week."},
  {"match": "Morphology", "do": ["Read each meaning.", "Type the missing ending.", "Tap Check."], "why": "Spotting an ending in a new word tells you what job the word does."},
  {"match": "Vocabulary", "do": ["Say each word out loud.", "Tap each card to read its meaning.", "Answer the question in your reading journal."], "why": "Saying and using a word helps you keep it."},
  {"match": "Spelling", "do": ["Read how each family's spelling shifts.", "Write the prospect family in your reading journal.", "Tap every word in the sign family."], "why": "Knowing where a family's spelling shifts keeps every member right."},
  rh(14), WS(2)],
 "glossary": [{"word": "meter", "in": "Poetry Corner", "meaning": "the beat of a poem, the pattern of strong and weak sounds"},
              {"word": "personification", "in": "Poetry Corner", "meaning": "giving a thing human actions or feelings"},
              {"word": "tone", "in": "What Good Readers Do", "meaning": "the feeling a writer's words give, like funny, serious or warm"}],
 "hints": {"ety": ["notorious drops its ous and takes a different ending.", "Three letters: e, then two more.", "e, t, y"], "ive": ["This ending means tending to.", "Three letters, ending in e.", "i, v, e"],
           "ous": ["This ending means full of.", "Three letters: o, then two more.", "o, u, s"], "ty": ["This word names a quality. The i is already there.", "Two letters finish -ity.", "t, y"]},
 "game": game(2, [r("Full of venom (a rattlesnake)", ["venomus", "venomous", "venemous"], 1, "venom + ous: keep venom whole.", "Spell venom first: v, e, n, o, m."),
                  r("Tending to protect (a burro guarding its pack)", ["protective", "protectiv", "protecktive"], 0, "protect + ive.", "-ive always ends in e."),
                  r("The state of being able", ["ablity", "abileity", "ability"], 2, "able becomes abil before -ity.", "able changes to abil, then add -ity."),
                  r("Full of nerves (before a goodbye)", ["nerveous", "nervous", "nervos"], 1, "nerve drops its e before -ous.", "Drop the e of nerve, then add -ous."),
                  r("Which word is in the same family as friend?", ["friendship", "fried", "fiend"], 0, "friend + ship.", "Look for the whole word friend inside."),
                  r("Which word is in the same family as respect?", ["response", "respectful", "rest"], 1, "respect + ful.", "Look for the whole word respect inside."),
                  r("Tending to impress (a fine sight)", ["impresive", "impressiv", "impressive"], 2, "impress + ive: keep both s's.", "Spell impress first, then add -ive."),
                  r("The state of being popular", ["popularity", "populartiy", "populareity"], 0, "popular + ity.", "Add -ity straight onto popular.")]),
 "cards": [NOTE_SAV],
 "virtue": {"name": "integrity", "kind": "log", "options": [
   {"t": "Praiseworthy says he will come back to fight the Mountain Ox: “I gave my word, didn't I?”"},
   {"t": "Buffalo John says they'll be looking for him back next month, and Praiseworthy answers, “I'll be here.”"},
   {"t": "Praiseworthy tells Jack the truth about the boxing book, even though it means saying he did not destroy it."}],
   "line": "Tap the moment that shows the most integrity. Then tell why in one sentence.", "placeholder": "This shows the most integrity because…"},
}
D[3] = {
 "listen": {
  "warmup": {"text": "Answer the question on the card first. Then think about the voice of this book. In Chapter 15 something scary happens. As you read, notice whether the narrator ever sounds scared."},
  "words": {"text": "Today you use the word families yourself: spell each member and mark where it changes. Match each word to its meaning, then rewrite sentence openings. Eight more notches up the coyote hole."},
  "reading": {"text": "Read Chapter 15, The Man Who Couldn't Sit Down. Day after day, the partners hunt for gold. Then Jack goes hunting alone. Reread the most dangerous moment, and listen to how calm the telling stays."},
  "assignment": {"text": "Three questions, the last one about all three chapters. Then check your paragraph against the five checklist points, and fix anything that is missing."}},
 "how": [DOL, RW,
  {"match": "Spelling", "do": ["Read the four families.", "Choose three families and write every member.", "Underline the spelling changes and write two sentences per family."], "why": "This is your Show What You Know for spelling this week."},
  {"match": "Morphology", "do": ["Answer the question in your reading journal.", "Tap a word, then tap its meaning.", "Match all four."], "why": "Each meaning carries its ending's job."},
  {"match": "Vocabulary", "do": ["Tap a word.", "Tap its meaning.", "Match all five."], "why": "Matching shows you know each word on its own."},
  {"match": "Grammar", "do": ["Answer the question in your reading journal.", "Type the word that starts each sentence a new way.", "Tap Check My Work."], "why": "Changing how a sentence starts changes how it sounds."},
  dict(WGRD, why="A calm voice in a scary moment is a choice. Rereading shows you how it works.", use="You will use it in reading question 1."),
  rh(15), WS(3)],
 "glossary": [{"word": "word family", "in": "Spelling", "meaning": "a group of words that grow from the same base"},
              {"word": "narrator", "in": "What Good Readers Do", "meaning": "the voice that tells the story"}],
 "hints": {"Because": ["This opener gives a reason.", "It starts with B.", "B, e, c, a, u, s, e"], "After": ["This opener tells when.", "It starts with A.", "A, f, t, e, r"],
           "When": ["This opener tells when something happened.", "It starts with W.", "W, h, e, n"], "In": ["This opener tells where.", "Two letters.", "I, n"]},
 "game": game(3, [r("Full of glory", ["gloryous", "glorious", "glorous"], 1, "glory changes y to i before -ous.", "The y in glory changes before the ending."),
                  r("Tending to explode (a gunshot)", ["explosive", "explodive", "explosiv"], 0, "explode: the d becomes s before -ive, like decide and decisive.", "The d in explode changes before the ending."),
                  r("The state of being real", ["realety", "realitty", "reality"], 2, "real + ity.", "Add -ity straight onto real."),
                  r("Full of humor", ["humorus", "humorous", "humerous"], 1, "humor + ous.", "Spell humor first, then add all of -ous."),
                  r("Which word is in the same family as courage?", ["encourage", "cottage", "carriage"], 0, "en + courage: to give someone courage.", "Look for the whole word courage inside."),
                  r("Which word is in the same family as hunt?", ["hundred", "hurt", "hunter"], 2, "hunt + er: someone who hunts.", "Look for the whole word hunt inside."),
                  r("The state of being rapid (very fast)", ["rapidity", "rapiddity", "rapidety"], 0, "rapid + ity.", "Add -ity straight onto rapid."),
                  r("Tending to inform (full of facts)", ["informitive", "informative", "informive"], 1, "inform + ative.", "The ending here is -ative, with an a.")]),
 "cards": [NOTE_15],
 "virtue": {"name": "integrity", "kind": "meter", "title": "The integrity meter", "intro": "Think about one moment from Chapter 15.",
   "moment": "The road agent stole Cut-Eye Higgins's linen coat in the holdup. When Jack says it belongs to someone he knows, the man says it gives him a bad conscience to wear it, and he gives it back.",
   "ask": "How much integrity does the road agent show here? Slide to show.", "line": "Tell why in one sentence.", "placeholder": "He shows this much integrity because…",
   "take": "Mason's take: more than you might expect from a robber. He doesn't have to give the coat back, and Jack's gun isn't even loaded. But he stole it in the first place. Fleischman lets a bad man do one right thing, and leaves you to weigh it."},
}
D[4] = {
 "readnow": {"text": "No new chapter today. Keep Chapters 13 to 15 open in your book as you study Fleischman's voice.", "step": "Study the voice"},
 "listen": {
  "warmup": {"text": "Today a very different poem: Carl Sandburg's Fog, only six lines long. Read it slowly. Then compare it with Windy Nights. Same five parts, used to do the opposite thing."},
  "words": {"text": "Explain the three endings in your own words, and add each ending to a base. Pick an option on the vocabulary choice board. The last eight notches bring the bucket out of the hole."},
  "reading": {"text": "Read the five voice techniques. Find one example of each kind in Chapters 13 to 15. Then answer the voice questions, and pick the technique your own adventure needs most."},
  "assignment": {"text": "Read your paragraph out loud one last time. Put the final version in the box, with one sentence about your biggest change. Then copy your work into Canvas."}},
 "how": [DOL, RW, POEM,
  {"match": "Morphology", "do": ["Explain the three endings in your reading journal.", "Add the ending to each base word.", "Tap Check My Work."], "why": "Explaining an ending shows you really know it."},
  {"match": "Vocabulary", "do": ["Read the four options.", "Pick one and say which at the top of the box.", "Use all five words."], "why": "This is your Show What You Know for vocabulary this week."},
  {"match": "Grammar", "do": ["Read the before and after.", "Tap the right answer in each question.", "Answer the question in your reading journal."], "why": "Explaining a choice shows you can make it on purpose."},
  {"match": "Spelling", "do": ["Answer the question in your reading journal.", "Tap the right spelling in each pair."], "why": "Knowing the family keeps every spelling right."},
  dict(WGRD, why="Naming the voice pulls the whole week together.", use="You will use it in voice question 1."),
  {"match": "Analyzing Fleischman", "do": ["Read the five voice techniques.", "Answer the two pause questions.", "Answer the three voice questions."], "why": "Naming a writer's moves lets you borrow them."},
  WS(4)],
 "glossary": [{"word": "synthesize", "in": "What Good Readers Do", "meaning": "put ideas together into one big idea"},
              {"word": "technique", "in": "Analyzing Fleischman", "meaning": "a way of doing something, a move a writer uses on purpose"}],
 "hints": {"dangerous": ["danger + the ending that means full of.", "Keep danger whole.", "d, a, n, g, e, r, o, u, s"], "creative": ["create + the ending that means tending to.", "The e of create drops.", "c, r, e, a, t, i, v, e"],
           "curiosity": ["curious + the ending for a quality.", "The u in curious drops.", "c, u, r, i, o, s, i, t, y"], "poisonous": ["poison + the ending that means full of.", "Keep poison whole.", "p, o, i, s, o, n, o, u, s"]},
 "game": game(4, [r("Full of joy", ["joyus", "joyous", "joyeous"], 1, "joy + ous: the y stays, because a vowel comes before it.", "Keep joy whole, then add -ous."),
                  r("Tending to imagine", ["imaginative", "imaginitive", "imagintive"], 0, "imagine drops its e, then + ative.", "Drop the e, then add -ative with an a."),
                  r("The state of being similar", ["similarety", "simularity", "similarity"], 2, "similar + ity.", "Spell similar first: s, i, m, i, l, a, r."),
                  r("Full of adventure", ["adventureous", "adventurous", "adventerous"], 1, "adventure drops its e before -ous.", "One letter of adventure drops before the ending."),
                  r("Which word is in the prospect family?", ["prosperity", "prospectus", "propeller"], 1, "prospect + us: a paper that describes a plan.", "prosperity looks close, but it comes from prosper."),
                  r("Which word is in the same family as luck?", ["lucky", "lick", "lock"], 0, "luck + y.", "Look for the whole word luck inside."),
                  r("Tending to persuade", ["persuadive", "persuasiv", "persuasive"], 2, "persuade: the d becomes s before -ive.", "The d in persuade changes before the ending."),
                  r("The state of being humid (damp air)", ["humidity", "humidaty", "humiddity"], 0, "humid + ity.", "Add -ity straight onto humid.")]),
 "virtue": {"name": "integrity", "kind": "best", "title": "The moment of most integrity this week", "intro": "Look back at Chapters 13 to 15. Tap the moment you think shows integrity the most.",
   "options": [{"t": "Jack pays for the neckties with half his nugget rather than go back on his word (Chapter 13)."},
               {"t": "Praiseworthy promises he will be back to fight the Mountain Ox: “I gave my word, didn't I?” (Chapter 14)."},
               {"t": "The road agent gives back the coat he stole (Chapter 15)."}],
   "line": "Finish the sentence: This shows integrity the most because…", "placeholder": "This shows integrity the most because…"},
}
D['fluency'] = {"listen": {"page": {"text": "Read the scene from Chapter 15 where Jack meets the stranger who pulled him out of the hole. Make Jack sound suspicious and the stranger easygoing. Save a pause for the very last line. When it sounds right, record yourself."}},
                "glossary": [{"word": "expression", "meaning": "reading with feeling, so your voice shows what the words mean"}]}
FILES = {1: 'lesson-29-1-btghs-ch13.html', 2: 'lesson-29-2-btghs-ch14.html', 3: 'lesson-29-3-btghs-ch15.html', 4: 'lesson-29-4-btghs-voice.html'}
def page_words(f):
    s = io.open(f, encoding='utf-8').read()
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s); s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s).lower()
    return set(re.findall(r"[a-z]+", s))
allw = set()
for k, v in D.items():
    txt = [c['text'] for c in v['listen'].values()]
    n = sum(len(t) for t in txt)
    if k != 'fluency' and n > 1000: sys.exit('%s: Listen clips are %d characters (over 1,000)' % (k, n))
    s = json.dumps(v, ensure_ascii=False)
    if '—' in s or '–' in s: sys.exit('%s: dash' % k)
    for bad in ('Quick check', 'quick check', 'download', 'upload', 'RWM', 'SWYK', 'classmate', 'partner up', 'humour'):
        if bad in s: sys.exit('%s: %s' % (k, bad))
    if 'game' in v:
        pw = page_words(FILES[k]); oks = [0, 0, 0]
        for R in v['game']['rounds']:
            if len(R['opts']) != 3 or len(set(R['opts'])) != 3: sys.exit('%s: round shape %r' % (k, R['clue']))
            w = R['opts'][R['ok']]; oks[R['ok']] += 1
            if w in allw: sys.exit('%s: answer %s used twice this week' % (k, w))
            allw.add(w)
            if w in pw: sys.exit('%s: answer %s is on that day\'s page' % (k, w))
        if min(oks) < 2: sys.exit('%s: right answers not spread %r' % (k, oks))
    json.dump(v, open('data/g5ela-29-%s.json' % k, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('wrote', k, n, 'chars', [len(t) for t in txt])
