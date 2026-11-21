# G5 ELA Word Study films (Mason)

Each film reuses that lesson's own Word Study Listen clip (`assets/audio/guide/g5ela-W-D-listen-words.mp3`), so it costs no new credits. It plays on the Word Study Listen card in place of the audio button (g5-sparkle.js `filmControl`, `assets/video/guide/<same name>.mp4` + `.jpg` poster + `.vtt` captions). If the film is missing or fails, the audio button comes back.

Ported from optima-4th-ela/tools/g4video (Marcus) with Mason's portrait (`assets/companions/mason-v2.jpg` → `mason.jpg` beside render.html).

Rules: show the activity with a fresh example that is not an answer anywhere on that week's pages, DATA or check-in (check the word list first); never show or voice Choctaw words; Day 1 never names a root the page wants students to notice on their own.

Run (cloud, Playwright + ffmpeg + `pip install pocketsphinx`):

    mkdir -p /tmp/vid/build; cp <the week's listen-words mp3s> /tmp/vid/
    cp render.html capture.js /tmp/vid/build/; cp ../../assets/companions/mason-v2.jpg /tmp/vid/build/mason.jpg
    SPECS=specs_g5wkNN python3 timeline.py scripts_g5wkNN.json && cp timeline.json /tmp/vid/build/
    (cd /tmp/vid/build && node capture.js <clip> 12)      # each clip
    python3 encode.py <clip> ...                          # mp4 + jpg + vtt + /tmp/vid/sheet.png

Scripts JSON = the DATA `listen.words.text` exactly as recorded. Read the contact sheet before shipping.
Weeks 18-21: specs_g5wk18_21.py.
