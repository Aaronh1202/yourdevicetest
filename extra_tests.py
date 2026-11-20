"""More device tests for YourDeviceTest: variants of the core tests plus new tools."""
import math

def build(T, toolbar, stats, PRIVATE):
    E = {}

    # ---- CPS test lengths ----
    base_cps = T["cps-test"]["tool"]
    CPS_FACTS = {
        1: ("1 Second", "A 1-second test measures your top burst speed. Because there's no time to tire, scores are usually higher than in longer tests: 8–10 clicks in one second is very good.",
            "Great for warming up, or for comparing pure finger speed with friends."),
        10: ("10 Second", "Ten seconds is long enough that your speed starts to drop near the end, so it's a better measure of real click speed than shorter tests. Most people average 6–7 CPS here.",
             "A good middle ground between burst speed and stamina, often used for Minecraft PvP practice."),
        30: ("30 Second", "Over 30 seconds your arm and finger muscles start to fatigue. Holding 7 CPS or more for the whole time takes real stamina and a relaxed technique.",
             "Use it to build endurance: try to keep your speed steady instead of starting fast and fading."),
        60: ("60 Second", "The one-minute test is the ultimate click stamina challenge. Even fast clickers often drop to 5–6 CPS by the end. Count your total clicks: 400 or more in a minute is excellent.",
             "Shake out your hand first, sit comfortably and keep a steady rhythm."),
    }
    for sec, (lbl, about, tip) in CPS_FACTS.items():
        tool = base_cps.replace('<button data-s="5" class="on">5s</button>', '<button data-s="5">5s</button>').replace(f'<button data-s="{sec}">', f'<button data-s="{sec}" class="on">')
        tool = tool.replace('("s-time","Time left","5.0s")', f'("s-time","Time left","{sec}.0s")')
        tool = f"<script>window.CPS_DUR={sec}</script>" + tool
        E[f"cps-test-{sec}-second" + ("s" if sec > 1 else "")] = dict(
            emoji="🖱️", color="#a3e635", name=f"{lbl} CPS Test", card=f"Clicks per second over {sec} second{'s' if sec > 1 else ''}",
            title=f"{lbl} CPS Test – Clicks Per Second in {sec} Second{'s' if sec > 1 else ''}",
            desc=f"Free {sec}-second CPS test. Click as fast as you can for {sec} second{'s' if sec > 1 else ''} and see your clicks per second, total clicks and personal best.",
            h1=f"{lbl} <span>CPS Test</span>", sub=f"Start clicking to begin a {sec}-second click speed test.", js="click.js", tool=tool,
            content=f"<h2>About the {sec}-second CPS test</h2><p>{about}</p><h2>Tip</h2><p>{tip}</p>"
                    "<h2>Average CPS</h2><p>Most people click 6–7 times per second. 8–10 CPS is fast, and pros using jitter or butterfly clicking can pass 12.</p>",
            faq=[("Is my best score saved?", f"Yes. Your best {sec}-second score is saved in your browser."),
                 ("Does it work on phones?", "Yes, tap the box as fast as you can. Touch screens often allow faster tapping with two fingers.")])

    # ---- solid color screens ----
    def solid(slug, name, color, emoji, title, desc, sub, content, faq):
        sw = "".join(f'<button class="sw" data-c="{c}" style="background:{c}" title="{n}" aria-label="{n}"></button>' for c, n in
                     [("#ffffff", "White"), ("#000000", "Black"), ("#00ff00", "Green"), ("#0000ff", "Blue"), ("#ff0000", "Red"), ("#ffff00", "Yellow"), ("#ff00ff", "Magenta"), ("#808080", "Gray")])
        tool = f'''<div class="panel"><div class="start" style="min-height:220px"><div class="solidprev" id="preview"></div>
<div class="row" style="justify-content:center"><button class="btn primary big" id="go">⛶ Open full screen</button><label class="btn big">🎨 <input type="color" id="pick" value="{color}" style="width:44px;height:28px;border:0;background:none"></label></div>
<p class="note">Or pick a color:</p><div class="swatches">{sw}</div><p class="note">Click anywhere or press Esc to exit full screen</p></div></div>
<div id="fs"><div class="hint"></div></div>'''
        E[slug] = dict(emoji=emoji, color="#f472b6", name=name, card=desc.split(".")[0], title=title, desc=desc,
                       h1=name.replace(" ", " <span>", 1) + "</span>", sub=sub, js="solid.js", tool=tool, content=content, faq=faq)

    solid("white-screen", "White Screen", "#ffffff", "⬜", "White Screen – Full Screen White Light (Free)",
          "Turn your screen fully white in one click. Use it as a light, to clean your monitor, check for dead pixels or as a ring light for video calls.",
          "Make your whole screen bright white. Great as a light, for cleaning your screen or for spotting dead pixels.",
          """<h2>What can I use a white screen for?</h2><ul><li><b>Video call light:</b> a white screen in front of you works like a soft ring light in a dark room.</li><li><b>Cleaning:</b> dust, smudges and fingerprints are much easier to see on a white screen.</li><li><b>Dead pixels:</b> dead pixels show up as black dots on white.</li><li><b>Tracing and art:</b> put thin paper on a tablet to trace drawings.</li><li><b>Photography:</b> use a laptop or tablet as a small fill light or a white background for product photos.</li></ul>
<h2>Tips</h2><p>Turn your screen brightness all the way up for the most light. On phones, turn off auto-brightness and night mode, which tint the screen yellow.</p>""",
          [("Does a white screen use more battery?", "On OLED screens (most new phones), yes: white pixels use much more power than black. On LCD screens the backlight is always on, so the difference is small."),
           ("Can I use a different color?", "Yes. Pick any color with the color picker or the swatches.")])
    solid("black-screen", "Black Screen", "#000000", "⬛", "Black Screen – Full Screen Black (Free)",
          "Turn your screen fully black. Hide your screen, check for backlight bleed and stuck pixels, or use it for OLED-friendly darkness.",
          "Make your whole screen pure black. Check for backlight bleed and stuck pixels, or just dim the room.",
          """<h2>What can I use a black screen for?</h2><ul><li><b>Backlight bleed:</b> in a dark room, light leaking around the edges of an LCD screen is easy to see on black.</li><li><b>Stuck pixels:</b> pixels stuck on red, green, blue or white stand out against black.</li><li><b>Darkness:</b> keep a screen on without lighting up the room, for example while listening to a video, or so a presentation doesn't distract.</li><li><b>Cleaning:</b> some smudges are easier to see on black from an angle.</li></ul>
<h2>Is a black screen the same as turning it off?</h2><p>On OLED screens, black pixels are switched off completely, so it's nearly the same. LCD screens still have their backlight on, so you'll see a dark gray glow.</p>""",
          [("Does a black screen save battery?", "Yes on OLED screens, where black pixels use almost no power. On LCDs the saving is small."),
           ("Why do I see glowing patches at the edges?", "That's backlight bleed or IPS glow, common on LCD monitors. Small amounts are normal.")])
    solid("green-screen", "Green Screen", "#00ff00", "🟩", "Green Screen – Full Screen Green for Chroma Key (Free)",
          "Fill your screen with pure chroma-key green. Use a monitor or tablet as a green screen for video editing, or test your display.",
          "Fill your whole screen with chroma-key green for video effects, or to test your display.",
          """<h2>Using your screen as a green screen</h2><p>Video editors replace a solid green color with another image or video (chroma keying). For small objects or close-up shots, a monitor, tablet or phone showing pure green can work as a mini green screen. Green is used because it's far from skin tones and digital camera sensors are most sensitive to it.</p>
<h2>Tips</h2><p>Turn down room lights that reflect on the screen, keep the subject a little in front of the screen to avoid green spill, and set your camera's exposure so the green looks even.</p>""",
          [("What green is used for chroma key?", "Pure digital green (#00FF00) works well on screens. Painted green screens use a slightly darker green."),
           ("Can I use blue instead?", "Yes, pick blue from the swatches. Blue screens are used when the subject contains green.")])

    # ---- stuck pixel fixer ----
    E["stuck-pixel-fixer"] = dict(
        emoji="🩹", color="#f472b6", name="Stuck Pixel Fixer", card="Flash colors over a stuck pixel to try to revive it",
        title="Stuck Pixel Fixer – Try to Fix Stuck Pixels Online (Free)",
        desc="Free stuck pixel fixer. Flash rapidly changing colors over a stuck pixel to try to unstick it. Works on monitors, laptops and phones.",
        h1="Stuck Pixel <span>Fixer</span>", sub="Flash rapidly changing colors over a stuck pixel to try to bring it back to life.", js="fixer.js",
        tool=f'''<div class="panel">{toolbar("Not running")}<p class="err" style="display:block">⚠️ Warning: this tool shows rapidly flashing colors. Don't use it if you are sensitive to flashing lights or have photosensitive epilepsy, and don't look directly at it while it runs.</p>
<div class="row" style="justify-content:center;margin:14px 0"><button class="btn primary big" id="go">▶ Start fixer</button><label class="btn">Size <input type="range" id="size" min="40" max="400" value="120"></label></div>
<p class="note center">Drag the flashing square over the stuck pixel. Find stuck pixels first with the <a href="dead-pixel-test">Dead Pixel Test</a>.</p></div>
<div id="fixbox" class="hidden"><canvas id="fixcanvas" width="48" height="48"></canvas></div>''',
        content="""<h2>How to fix a stuck pixel</h2><ol><li>Find the stuck pixel with the Dead Pixel Test (it stays one color when the screen changes).</li><li>Start the fixer and drag the flashing square over it.</li><li>Leave it running for 10–30 minutes, then check again. Repeat a few times if needed.</li></ol>
<h2>Does it really work?</h2><p>It can help with <b>stuck</b> pixels, where a sub-pixel is stuck on or off. Rapidly switching the colors can sometimes free it. It cannot fix <b>dead</b> pixels, which are permanently black because the transistor has failed. Results vary, so check your warranty too.</p>""",
        faq=[("Is it safe for my screen?", "Yes. It just displays colors, which is what your screen does all day."),
             ("How long should I run it?", "Start with 10–20 minutes. Some people run it for a few hours. If nothing changes after several tries, the pixel is probably dead.")])

    # ---- audio variants ----
    sp = T["speaker-test"]["tool"]
    def fval(f): return round(1000 * math.log(f / 20) / math.log(1000))
    E["headphone-test"] = dict(
        emoji="🎧", color="#fbbf24", name="Headphone Test", card="Check left and right channels on your headphones",
        title="Headphone Test – Left Right Headphone & Earbud Check",
        desc="Free headphone test. Check that your headphones or earbuds play sound on the correct left and right side, and test bass and treble with tones.",
        h1="Headphone <span>Test</span>", sub="Put on your headphones and check that the left and right sides play correctly.", js="speaker.js", tool=sp,
        content="""<h2>How to test your headphones</h2><p>Put your headphones on (L on your left ear) and lower the volume. Press <b>Left</b>: you should only hear the chime in your left ear. Then press <b>Right</b>. If the sound comes from the wrong side, the headphones are on backwards or the channels are swapped.</p>
<h2>Only one earbud works?</h2><ul><li>Clean the earbud mesh gently with a dry brush: earwax often blocks the sound.</li><li>Check your device's audio balance setting (it may be shifted to one side).</li><li>Turn off mono audio in accessibility settings.</li><li>Re-pair Bluetooth earbuds, or reset them to sync both sides.</li><li>For wired headphones, wiggle the plug: a crackle means a loose or damaged cable.</li></ul>
<h2>Test the bass</h2><p>Use the tone slider to play low notes (30–100 Hz). Good headphones should play bass clearly without rattling.</p>""",
        faq=[("Why is my headphone sound only on one side?", "Usually a balance setting, mono audio, a dirty earbud or a damaged cable. Run the left/right test to see which side is affected."),
             ("Is the test safe for my ears?", "Yes, at a moderate volume. Always start quiet and increase slowly.")])
    E["tone-generator"] = dict(
        emoji="🎵", color="#fbbf24", name="Tone Generator", card="Play any frequency from 20 Hz to 20 kHz",
        title="Tone Generator – Online Frequency Generator (20 Hz – 20 kHz)",
        desc="Free online tone generator. Play a pure sine wave at any frequency from 20 Hz to 20 kHz. Test speakers, tune instruments or check your hearing range.",
        h1="Tone <span>Generator</span>", sub="Play a pure tone at any frequency from 20 Hz to 20,000 Hz.", js="speaker.js",
        tool=sp.replace('value="433"', f'value="{fval(440)}"'),
        content="""<h2>How to use the tone generator</h2><p>Drag the frequency slider and press <b>Play tone</b>. You can change the frequency and volume while it plays. The sweep plays every frequency from 20 Hz to 20 kHz over 10 seconds.</p>
<h2>Useful frequencies</h2><ul><li><b>440 Hz:</b> the note A above middle C, the standard tuning pitch for instruments.</li><li><b>50–60 Hz:</b> the hum of electrical mains power.</li><li><b>20–60 Hz:</b> deep sub-bass, felt as much as heard.</li><li><b>1,000 Hz:</b> the standard test tone used in audio and broadcasting.</li><li><b>15,000+ Hz:</b> very high pitches many adults can no longer hear.</li></ul>""",
        faq=[("Can I tune a guitar with this?", "You can match a reference pitch, for example A = 440 Hz, but a dedicated tuner app is easier for tuning every string."),
             ("Why can't I hear very high or low tones?", "Small speakers can't reproduce deep bass, and human hearing at high frequencies declines with age.")])
    E["hearing-test"] = dict(
        emoji="👂", color="#fbbf24", name="Hearing Range Test", card="Find the highest frequency you can hear",
        title="Hearing Range Test – How High Can You Hear? (Frequency Test)",
        desc="Free online hearing range test. Play tones from 20 Hz to 20 kHz and find the highest frequency you can hear. For fun, not a medical test.",
        h1="Hearing <span>Range Test</span>", sub="Find the highest pitch you can hear. Use headphones and a moderate volume.", js="speaker.js",
        tool=sp.replace('value="433"', f'value="{fval(8000)}"'),
        content="""<h2>How to test your hearing range</h2><ol><li>Use good headphones and set a comfortable, moderate volume.</li><li>Press <b>Play tone</b> and slowly drag the slider up.</li><li>Note the frequency where the sound disappears. That's roughly your upper hearing limit.</li></ol>
<h2>Typical hearing range by age</h2><p>Young people can usually hear up to about 17–20 kHz. The upper limit naturally drops with age (called presbycusis): many adults over 40 can't hear above 14–15 kHz, and over 60 often stop around 10–12 kHz. Lower frequencies are much less affected.</p>
<p><b>Note:</b> this is a fun self-check, not a medical hearing test. Results depend on your headphones and device. If you notice hearing loss, ringing or muffled sound, see a doctor or audiologist.</p>""",
        faq=[("Why can kids hear sounds I can't?", "Sensitivity to high frequencies declines with age, so a high tone at 17 kHz may be obvious to a teenager and silent to their parents."),
             ("Are my speakers the limit?", "Possibly. Laptop and phone speakers often can't play above 15–16 kHz, so use decent headphones.")])

    # ---- keyboard / mouse variants ----
    E["keyboard-ghosting-test"] = dict(
        emoji="⌨️", color="#f472b6", name="Keyboard Ghosting Test", card="How many keys can your keyboard register at once?",
        title="Keyboard Ghosting Test – Check Key Rollover (NKRO)",
        desc="Free keyboard ghosting and rollover test. Hold down several keys at once to see how many your keyboard registers, and find combinations that ghost.",
        h1="Keyboard <span>Ghosting Test</span>", sub="Hold down several keys at once and see how many your keyboard can register.", js="keyboard.js",
        tool=T["keyboard-test"]["tool"],
        content="""<h2>What is keyboard ghosting?</h2><p>Ghosting happens when you press several keys at once and some presses go missing (or, on old keyboards, extra phantom keys appear). Cheaper keyboards share wiring between keys, so certain combinations can't be detected together.</p>
<h2>How to test rollover</h2><p>Press and hold keys one by one, for example W, A, S, D, Shift and Space, and watch the <b>Most at once</b> counter. A keyboard with 6-key rollover (6KRO) registers six keys plus modifiers; N-key rollover (NKRO) registers every key you press.</p>
<h2>Why it matters for gaming</h2><p>Games often need you to run, strafe, jump and use an ability at the same time. If your keyboard drops one of those keys, your character won't respond. Gaming keyboards advertise anti-ghosting or NKRO for this reason.</p>""",
        faq=[("Is it my keyboard or the browser?", "Browsers report every key the keyboard sends. If presses go missing in the test, the keyboard didn't send them."),
             ("Do USB and Bluetooth keyboards differ?", "Some keyboards only offer full NKRO over USB and fall back to 6KRO over Bluetooth.")])
    E["double-click-test"] = dict(
        emoji="🖲️", color="#fbbf24", name="Double Click Test", card="Detect a mouse that double-clicks by itself",
        title="Double Click Test – Is My Mouse Double Clicking by Itself?",
        desc="Free double click test. Find out if your mouse is registering accidental double clicks, a common sign of a worn-out mouse switch.",
        h1="Double Click <span>Test</span>", sub="Single-click quickly in the box. If the Accidental double counter goes up, your mouse switch is failing.", js="click.js",
        tool=T["mouse-test"]["tool"],
        content="""<h2>How to test for double clicking</h2><p>Click once at a time, about 20–30 times, in the box. A healthy mouse shows 0 under <b>Accidental double</b>. If it counts up even though you only clicked once, the switch bounced and sent two clicks within 80 milliseconds.</p>
<h2>Why does my mouse double click?</h2><p>Mouse buttons use tiny metal switches. Over time the contacts wear or oxidize and \"bounce\", sending more than one signal per press. It's very common on mice that are a few years old, especially gaming mice that get heavy use.</p>
<h2>How to fix it</h2><ul><li>Increase the debounce time in your mouse software, if it has one.</li><li>Blow compressed air into the button gap.</li><li>Check if the mouse is still under warranty: many brands replace mice with this problem.</li><li>Replace the switch if you're comfortable soldering.</li></ul>""",
        faq=[("What's the difference between this and the Windows double-click speed setting?", "The Windows setting decides how fast two intentional clicks must be to count as a double click. This test finds unintentional extra clicks from a faulty switch."),
             ("Can software cause double clicks?", "Rarely. Test in a second browser or on another computer: if it still happens, it's the mouse.")])

    # ---- new tools ----
    E["spacebar-counter"] = dict(
        emoji="⌨️", color="#a3e635", name="Spacebar Counter", card="How fast can you press the spacebar?",
        title="Spacebar Counter – Spacebar Speed Test & Clicker",
        desc="Free spacebar counter and speed test. See how many times you can press the spacebar in 5, 10, 30 or 60 seconds and track your best score.",
        h1="Spacebar <span>Counter</span>", sub="Press the spacebar as fast as you can. Pick a time and go!", js="spacebar.js",
        tool=f'''<div class="panel">{toolbar("Ready", '<div class="seg" id="modes"><button data-s="5">5s</button><button data-s="10" class="on">10s</button><button data-s="30">30s</button><button data-s="60">60s</button></div><button class="btn" id="reset">↺</button>')}
<div class="clickpad" id="sppad"><div><div class="big" id="big">Press Space</div><div class="sub" id="sub"></div></div></div>
{stats(("s-sps","Presses / second","0.00"),("s-count","Presses","0"),("s-time","Time left","10.0s"),("s-best","Your best","—"))}</div>''',
        content="""<h2>How fast can you press the spacebar?</h2><p>Most people manage 5–7 presses per second. Fast typists and gamers often reach 8–10, and anything above 10 per second is exceptional.</p>
<h2>Tips for a higher score</h2><p>Use the side of your thumb, keep your wrist relaxed and make small, quick movements instead of lifting your thumb high. On phones, tap the box with two thumbs alternating.</p>
<h2>Why test spacebar speed?</h2><p>It's a fun challenge, and it's useful for games that need rapid jumping or button mashing. It also helps check that a spacebar isn't sticking or missing presses.</p>""",
        faq=[("Does holding the spacebar count?", "No. Only separate presses count; key repeat from holding the key is ignored."),
             ("Is my best score saved?", "Yes, for each time length, in your browser.")])
    E["reaction-time-test"] = dict(
        emoji="⚡", color="#a3e635", name="Reaction Time Test", card="How fast are your reflexes?",
        title="Reaction Time Test – Check Your Reflexes in Milliseconds",
        desc="Free reaction time test. Click as soon as the box turns green and see your reaction time in milliseconds. Compare with the average of about 250 ms.",
        h1="Reaction <span>Time Test</span>", sub="When the box turns green, click as fast as you can.", js="reaction.js",
        tool=f'''<div class="panel">{toolbar("Ready", '<button class="btn" id="reset">↺ Reset</button>')}
<div class="clickpad rt" id="rpad"><div><div class="big" id="big">Click to start</div><div class="sub" id="sub"></div></div></div>
{stats(("s-last","Last","—"),("s-avg","Average","—"),("s-tries","Tries","0"),("s-best","Best","—"))}</div>''',
        content="""<h2>What is a good reaction time?</h2><p>The average visual reaction time is around <b>250 milliseconds</b> (a quarter of a second). Under 200 ms is very fast; many esports players average 150–200 ms. Your result also includes a few milliseconds of mouse and screen delay.</p>
<h2>How to get a faster reaction time</h2><ul><li>Rest and stay hydrated: tiredness slows reactions a lot.</li><li>Keep your finger resting lightly on the button.</li><li>Use a high refresh rate monitor and a wired mouse to cut input lag.</li><li>Practice: reaction time improves with training, especially in games.</li></ul>
<h2>Why does reaction time matter?</h2><p>It plays a role in driving, sports and competitive gaming. Your average over 5 tries is a more reliable measure than a single result.</p>""",
        faq=[("Why did it say 'Too soon'?", "You clicked before the box turned green. The delay is random so you can't predict it."),
             ("Does my device affect the result?", "Yes, slightly. Screens and mice add a few milliseconds of delay, and 60 Hz screens can add up to 16 ms.")])
    E["touch-screen-test"] = dict(
        emoji="👆", color="#22d3ee", name="Touch Screen Test", card="Find dead zones and count multi-touch points",
        title="Touch Screen Test – Check Multi-Touch & Dead Zones Online",
        desc="Free touch screen test for phones, tablets and touch laptops. Draw to find unresponsive dead zones and see how many fingers your screen detects at once.",
        h1="Touch Screen <span>Test</span>", sub="Draw over the whole box with your fingers. Gaps in your lines show dead zones.", js="touch.js",
        tool=f'''<div class="panel">{toolbar("Touch the box to start", '<button class="btn" id="reset">↺ Clear</button>')}
<canvas id="touchcanvas"></canvas>
{stats(("s-now","Touching now","0"),("s-max","Most at once","0"),("s-total","Total touches","0"))}</div>''',
        content="""<h2>How to test a touch screen</h2><ol><li>Slowly draw lines across the whole box, edge to edge, covering every area.</li><li>Look for gaps or breaks in your lines: those are spots where the screen didn't register your finger.</li><li>Put several fingers down at once to see how many touches your screen detects.</li></ol>
<h2>How many touches should my screen support?</h2><p>Most phones and tablets detect 5–10 simultaneous touches. Touch-screen laptops usually support 10. If fewer register, the screen or digitizer may be faulty.</p>
<h2>Touch screen not responding?</h2><ul><li>Remove the case and screen protector, which can block touches near the edges.</li><li>Clean the screen and dry your hands.</li><li>Restart the device to rule out software glitches.</li><li>If a fixed area never responds, the digitizer is probably damaged.</li></ul>""",
        faq=[("Does it work with a stylus?", "Yes. Pens and styluses draw just like fingers."),
             ("Can I test a touch laptop?", "Yes. It works on Windows touch laptops, Chromebooks, iPads, iPhones and Android devices.")])
    E["screen-resolution"] = dict(
        emoji="📐", color="#22d3ee", name="Screen Resolution", card="What is my screen resolution?",
        title="What Is My Screen Resolution? – Check Your Display Size",
        desc="Instantly see your screen resolution, real physical pixels, pixel ratio, browser window size, aspect ratio and color depth.",
        h1="What's my <span>screen resolution?</span>", sub="Your screen resolution is shown instantly below.", js="resolution.js",
        tool=f'''<div class="panel"><div class="center" style="padding:10px 0"><div class="resbig" id="res">—</div><p class="note">Screen resolution (CSS pixels)</p></div>
{stats(("s-phys","Physical pixels","—"),("s-dpr","Pixel ratio","—"),("s-view","Browser window","—"),("s-ar","Aspect ratio","—"),("s-depth","Color depth","—"),("s-orient","Orientation","—"))}</div>''',
        content="""<h2>Screen resolution explained</h2><p>Resolution is the number of pixels across and down your screen, for example 1920 × 1080. Phones and many laptops use high-density screens with a <b>pixel ratio</b> of 2 or 3: they have more physical pixels than the resolution websites see, which makes text extra sharp. The physical pixels value shows your display's real resolution.</p>
<h2>Common resolutions</h2><ul><li><b>1366 × 768:</b> budget laptops.</li><li><b>1920 × 1080 (Full HD / 1080p):</b> the most common monitor resolution.</li><li><b>2560 × 1440 (QHD / 1440p):</b> popular for gaming monitors.</li><li><b>3840 × 2160 (4K UHD):</b> large monitors and TVs.</li></ul>
<h2>Why is my resolution lower than advertised?</h2><p>Windows and macOS scale the display (for example 150%) so text isn't tiny. That lowers the resolution websites see, while the physical pixel count stays the same.</p>""",
        faq=[("What's the difference between screen and window size?", "Screen resolution is your whole display. Window size is just the browser area, which is smaller because of toolbars and taskbars."),
             ("Is this information sent anywhere?", "No. It's read by your browser and shown only to you.")])

    # ---- more solid color screens (Nov 20) ----
    COLORS = [
        ("red-screen", "Red Screen", "#ff0000", "🟥", "a soft red night light, testing for stuck pixels, photography color gels and as a dim light that's easy on night vision",
         "Red light preserves night vision better than white, which is why astronomers and pilots use it in the dark."),
        ("blue-screen", "Blue Screen", "#0000ff", "🟦", "chroma-key (blue screen) video effects, testing for stuck pixels and checking the blue sub-pixels on your display",
         "Blue screens were the original chroma-key color in film. Today green is more common because cameras capture it with less noise, but blue is still used when the subject wears green."),
        ("yellow-screen", "Yellow Screen", "#ffff00", "🟨", "a warm reading light, mood lighting, checking for stuck pixels and testing color uniformity",
         "Yellow is made by turning on the red and green sub-pixels together, so it's a quick way to check both at once."),
        ("orange-screen", "Orange Screen", "#ff8000", "🟧", "a warm evening light, mood lighting for videos and checking color uniformity",
         "Warm orange light has less blue in it, so it's gentler on your eyes late at night than a white screen."),
        ("pink-screen", "Pink Screen", "#ff69b4", "🩷", "a soft colored light for photos and video calls, mood lighting and parties",
         "A pink screen in front of you gives a warm, flattering glow on video calls."),
        ("purple-screen", "Purple Screen", "#8000ff", "🟪", "mood and party lighting, colored backgrounds for photos and checking the red and blue sub-pixels",
         "Purple mixes the red and blue sub-pixels, so a pixel that shows only one of them will stand out."),
        ("gray-screen", "Gray Screen", "#808080", "🩶", "checking for uneven backlight, banding and dirty screen effect, and as a neutral background for color checking",
         "A mid-gray screen is the best way to spot the 'dirty screen effect': blotchy, uneven patches that are hard to see on white or black."),
    ]
    for slug, name, col, emo, uses, fact in COLORS:
        cname = name.split()[0].lower()
        solid(slug, name, col, emo, f"{name} – Full Screen {name.split()[0]} Color (Free)",
              f"Turn your whole screen {cname} in one click. Use it for {uses.split(',')[0]} and more.",
              f"Fill your whole screen with solid {cname}. Click the button to go full screen.",
              f"""<h2>What can I use a {cname} screen for?</h2><p>People use a full {cname} screen for {uses}.</p>
<h2>Did you know?</h2><p>{fact}</p>
<h2>How to use it</h2><ol><li>Press <b>Open full screen</b>.</li><li>Turn your screen brightness up (or down for a softer light).</li><li>Click anywhere or press Esc to exit.</li></ol><p>You can switch to any other color with the swatches or the color picker.</p>""",
              [(f"Will a {cname} screen damage my display?", "No. It's just showing a color, which your screen does all the time. Avoid leaving any static image on an OLED screen for many hours to prevent burn-in."),
               ("Does it work on phones?", "Yes. On iPhone, full screen mode may be limited by Safari, but the color still fills the page.")])

    E["bass-test"] = dict(
        emoji="🔊", color="#fbbf24", name="Bass Test", card="Test your speakers' and subwoofer's low end",
        title="Bass Test – Subwoofer & Speaker Low Frequency Test (20–200 Hz)",
        desc="Free bass test. Play low tones from 20 to 200 Hz to check how deep your speakers, headphones or subwoofer can go, and listen for rattles.",
        h1="Bass <span>Test</span>", sub="Play low tones to see how deep your speakers or subwoofer can go. Start at a low volume.", js="speaker.js",
        tool=sp.replace('value="433"', f'value="{fval(60)}"'),
        content="""<h2>How to test bass</h2><ol><li>Set your volume low, then press <b>Play tone</b>.</li><li>Drag the slider down slowly from 200 Hz toward 20 Hz.</li><li>Note where the tone fades away: that's roughly the lowest note your speakers can play.</li></ol>
<h2>What to expect</h2><ul><li><b>Phone and laptop speakers:</b> usually fade out around 150–250 Hz.</li><li><b>Headphones:</b> many reach 20–40 Hz.</li><li><b>Bookshelf speakers:</b> typically 50–80 Hz.</li><li><b>Subwoofers:</b> 20–40 Hz, often felt more than heard.</li></ul>
<h2>Listen for problems</h2><p>Buzzing or rattling at certain frequencies usually means something loose: a speaker grille, a shelf or an object nearby. A crackle at every frequency can point to a damaged speaker cone.</p>""",
        faq=[("Can a bass test damage my speakers?", "Very loud low tones can. Keep the volume moderate and stop if you hear distortion."),
             ("Why can't I hear 20 Hz?", "Most speakers can't reproduce it, and even when they can, very low bass is felt more than heard.")])
    E["left-right-sound-test"] = dict(
        emoji="🔈", color="#fbbf24", name="Left Right Sound Test", card="Check stereo left and right channels",
        title="Left Right Sound Test – Stereo Audio Channel Check",
        desc="Free left and right sound test. Play audio on the left channel, right channel or both to check your stereo speakers, headphones or car audio wiring.",
        h1="Left Right <span>Sound Test</span>", sub="Press Left or Right and check that the sound comes from the correct side.", js="speaker.js", tool=sp,
        content="""<h2>How to check stereo channels</h2><p>Press <b>Left</b>, then <b>Right</b>. Each sound should come only from that side. If both sides play the same, mono audio may be switched on. If they're swapped, your speakers are plugged into the wrong outputs.</p>
<h2>Common fixes</h2><ul><li><b>Swapped sides:</b> swap the speaker cables, or wear headphones the right way round (look for the L and R marks).</li><li><b>Sound on both sides:</b> turn off mono audio in your accessibility settings.</li><li><b>One side quiet:</b> check the balance slider in your sound settings.</li></ul>
<h2>Why stereo matters</h2><p>Games use left and right sound to tell you where footsteps come from, and music and movies are mixed for stereo. A swapped or missing channel changes how everything sounds.</p>""",
        faq=[("Does this work for car audio or soundbars?", "Yes. Connect your phone by Bluetooth or cable and run the test."),
             ("Why is there no sound at all?", "Check the volume, mute switch and which output device is selected, then try the Speaker Test.")])
    E["jitter-click-test"] = dict(
        emoji="🖱️", color="#a3e635", name="Jitter Click Test", card="Test your jitter clicking speed",
        title="Jitter Click Test – Jitter Clicking CPS Speed Test",
        desc="Free jitter click test. Measure your jitter clicking speed in clicks per second, compare with normal clicking and track your best score.",
        h1="Jitter Click <span>Test</span>", sub="Tense your arm and jitter click as fast as you can. Pick a time and start clicking.", js="click.js", tool=base_cps,
        content="""<h2>What is jitter clicking?</h2><p>Jitter clicking means tensing the muscles in your forearm and wrist so your hand vibrates, which makes your finger click very fast. Good jitter clickers reach 10–14 CPS, compared with 6–7 CPS for normal clicking.</p>
<h2>How to jitter click safely</h2><ul><li>Rest your hand on the mouse with your finger on the button.</li><li>Tense your forearm until your hand shakes slightly, and let the shaking press the button.</li><li>Keep sessions short and take breaks: jitter clicking puts strain on your wrist and arm.</li></ul>
<h2>Jitter vs butterfly clicking</h2><p>Butterfly clicking alternates two fingers on the same button and can be even faster, but some games and servers limit it. Jitter clicking uses one finger, so it works on any mouse.</p>""",
        faq=[("Is jitter clicking bad for you?", "Doing it for long periods can cause wrist and arm strain. Warm up, keep sessions short and stop if it hurts."),
             ("What CPS is good for jitter clicking?", "10 CPS is good, 12 is great and 14+ is exceptional.")])

    return E
