import re, json, os, pathlib, shutil
OUT = pathlib.Path("public")
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
for f in pathlib.Path("static").iterdir(): shutil.copy(f, OUT / f.name)
SITE = "YourDeviceTest"
DOMAIN = "https://yourdevicetest.com"
CONTACT = os.environ.get("CONTACT_EMAIL", "hello@example.com")
PRIVATE = "Everything runs inside your browser. Nothing is recorded, uploaded or saved on our servers."

def stats(*items):
    return '<div class="stats">' + "".join(f'<div class="stat"><span>{l}</span><b id="{i}">{d}</b></div>' for i, l, d in items) + "</div>"

def toolbar(status="Not started", extra=""):
    return f'<div class="toolbar"><span class="status" id="status"><i></i>{status}</span><div class="row">{extra}</div></div>'

def startbox(icon, text, btn):
    return f'<div class="start" id="start"><div class="ico">{icon}</div><p>{text}</p><button class="btn primary big" id="go">{btn}</button><p class="note">🔒 {PRIVATE}</p></div><div class="err hidden" id="err"></div>'

DEVSEL = '<label class="hidden"><select id="device" aria-label="Choose device"></select></label>'

T = {}
T["mic-test"] = dict(
    emoji="🎙️", color="#22d3ee", name="Mic Test", card="Check if your microphone works and hear yourself back",
    title="Mic Test – Check Your Microphone Online (Free)",
    desc="Test your microphone online in one click. See a live sound wave and volume level, record and play back your voice, and pick between mics. Free and private.",
    h1="Mic <span>Test</span>", sub="Find out in seconds if your microphone works. See a live sound wave, check the volume level and hear yourself back.",
    js="mic.js",
    tool=f'''<div class="panel stage">{toolbar(extra=DEVSEL)}
{startbox("🎙️", "Click the button and allow microphone access. Then say something and watch the sound wave move.", "Test my microphone")}
<div id="live" class="hidden"><canvas class="scope" id="scope"></canvas>
<div class="row" style="justify-content:space-between;margin-top:12px"><div class="seg" id="view"><button class="on" data-v="wave">Wave</button><button data-v="bars">Bars</button></div>
<div class="row"><button class="btn" id="rec">⏺ Record 5 seconds</button><button class="btn" id="stop">Stop</button></div></div>
<div style="margin-top:14px"><div class="meter" id="meter"><i></i></div></div>
<audio id="playback" class="hidden" controls style="width:100%;margin-top:12px"></audio>
{stats(("s-level","Volume","0%"),("s-peak","Peak","0%"),("s-rate","Sample rate","—"),("s-ch","Channels","—"))}
<p class="note" style="margin-top:12px">Microphone: <b id="s-name">—</b></p></div></div>''',
    content="""<h2>How to test your microphone</h2><ol><li>Click <b>Test my microphone</b> and allow access when your browser asks.</li><li>Talk, clap or tap the mic. The wave and the volume bar should move.</li><li>Press <b>Record 5 seconds</b> to hear exactly how you sound to others.</li></ol>
<h2>Microphone not working? Try this</h2><ul><li><b>Check permissions:</b> click the lock or camera icon in your address bar and allow the microphone.</li><li><b>Close other apps:</b> Zoom, Teams or Discord can lock your mic.</li><li><b>Pick the right mic:</b> if you have more than one, choose it from the dropdown above.</li><li><b>Check the mute switch:</b> many headsets have a mute button on the cable or earcup.</li><li><b>Windows:</b> Settings → Privacy → Microphone, and turn on access for apps and browsers.</li><li><b>Mac:</b> System Settings → Privacy & Security → Microphone, and allow your browser.</li></ul>""",
    faq=[("Is this mic test safe?", "Yes. The test runs entirely in your browser. Your audio is never uploaded, and your recording disappears when you leave the page."),
         ("What volume level is normal?", "When you speak at a normal volume, the bar should reach about 40–80%. If it barely moves, raise your mic volume in your computer's sound settings. If it hits the red constantly, lower it."),
         ("Why does my mic sound quiet or muffled?", "Move closer to the mic, check that nothing covers it, and raise the input level in your sound settings. Cheap built-in laptop mics often sound thin compared to a headset or USB mic.")])

T["webcam-test"] = dict(
    emoji="📷", color="#a78bfa", name="Webcam Test", card="See your camera live with its real resolution and FPS",
    title="Webcam Test – Check Your Camera Online (Free)",
    desc="Test your webcam online instantly. See a live preview plus your camera's real resolution, frame rate and quality. Take snapshots, mirror and switch cameras.",
    h1="Webcam <span>Test</span>", sub="Check that your camera works and see its real resolution, frame rate and picture quality.",
    js="webcam.js",
    tool=f'''<div class="panel stage">{toolbar(extra=DEVSEL)}
{startbox("📷", "Click the button and allow camera access to see yourself live.", "Test my webcam")}
<div id="live" class="hidden"><div class="video mirror" id="vbox"><video id="video" playsinline muted></video><span class="badge"><i></i>LIVE</span></div>
<div class="row" style="margin-top:12px;justify-content:center"><button class="btn primary" id="snap">📸 Take photo</button><button class="btn" id="mirror">⇋ Mirror</button><button class="btn" id="full">⛶ Fullscreen</button><button class="btn" id="stop">Stop</button></div>
<div class="shots" id="shots"></div>
{stats(("s-res","Resolution","—"),("s-q","Quality","—"),("s-fps","Frame rate","—"),("s-ar","Aspect ratio","—"))}
<p class="note" style="margin-top:12px">Camera: <b id="s-name">—</b></p></div></div>''',
    content="""<h2>How to test your webcam</h2><ol><li>Click <b>Test my webcam</b> and allow camera access.</li><li>You'll see yourself live, plus your camera's real resolution and frame rate.</li><li>Take a photo to check the picture quality up close.</li></ol>
<h2>Webcam not working? Try this</h2><ul><li><b>Allow access:</b> click the camera icon in your address bar and choose Allow.</li><li><b>Close other apps</b> that might be using the camera, like Zoom, Teams, Skype or OBS.</li><li><b>Check the privacy shutter:</b> many laptops have a tiny slider or a keyboard key that turns the camera off.</li><li><b>Windows:</b> Settings → Privacy → Camera, and turn on access.</li><li><b>Mac:</b> System Settings → Privacy & Security → Camera, and allow your browser.</li><li><b>Try another USB port</b> for external webcams.</li></ul>""",
    faq=[("Do you record or save my video?", "No. The video only shows on your screen and never leaves your device. Photos you take are created in your browser and only saved if you download them."),
         ("What resolution should my webcam be?", "720p is fine for most video calls. 1080p looks noticeably sharper, and 4K is great for streaming and content creation. This test shows the highest resolution your camera can deliver."),
         ("Why is my frame rate low?", "Webcams often drop to 15 fps in dim light so they can let in more light. Turn on more lights or face a window, and close other apps using your camera.")])

T["keyboard-test"] = dict(
    emoji="⌨️", color="#f472b6", name="Keyboard Test", card="Press every key and find dead or stuck keys",
    title="Keyboard Test – Check Every Key Online (Free Keyboard Tester)",
    desc="Free online keyboard tester. Press keys to see them light up, find dead or stuck keys, check key codes and test how many keys you can press at once.",
    h1="Keyboard <span>Test</span>", sub="Press every key on your keyboard. Working keys turn green, so dead or stuck keys are easy to spot.",
    js="keyboard.js",
    tool=f'''<div class="panel">{toolbar("Press any key to start", '<button class="btn" id="reset">↺ Reset</button>')}
<div class="center"><div class="lastkey" id="last"></div></div>
<div class="kb" id="kb"></div>
<div class="keylog" id="log"></div>
{stats(("s-tested","Keys tested","0"),("s-count","Total presses","0"),("s-max","Most at once","0"),("s-code","Key code","—"),("s-which","Key number","—"))}</div>''',
    content="""<h2>How to use the keyboard tester</h2><p>Just start typing. Each key lights up while you hold it and turns <b>green</b> once it has worked. When you're done, any key that never turned green may be broken, dirty or blocked.</p>
<h2>How many keys can I press at once?</h2><p>The <b>Most at once</b> counter shows your keyboard's rollover. Hold down several keys at once to find its limit. Gaming keyboards often support 6 keys or more (called NKRO), while cheaper keyboards may stop at 2–3 keys in some combinations. That limit is called ghosting.</p>
<h2>A key isn't working. What now?</h2><ul><li>Turn the keyboard upside down and gently shake out crumbs, or use compressed air.</li><li>For a mechanical keyboard, pull off the keycap and clean under it.</li><li>Try a different USB port or fresh batteries for wireless keyboards.</li><li>If a key repeats or sticks, a drop of isopropyl alcohol under the cap often fixes it.</li></ul>""",
    faq=[("Why doesn't the Windows key or Fn key show up?", "Some keys are handled by your computer or keyboard itself before your browser sees them. Fn usually never reaches the browser, and some system shortcuts can't be captured."),
         ("Does this work with laptop keyboards?", "Yes. It works with laptop, desktop, mechanical, wireless and Bluetooth keyboards."),
         ("Is my typing recorded?", "No. Keys are only shown on your screen and are never sent or saved anywhere.")])

T["cps-test"] = dict(
    emoji="🖱️", color="#a3e635", name="CPS Test", card="How many clicks per second can you do?",
    title="CPS Test – Check Your Clicks Per Second (Click Speed Test)",
    desc="Free CPS test. See how many clicks per second you can do in 1, 5, 10, 30 or 60 seconds. Track your best score and compare with average click speeds.",
    h1="CPS <span>Test</span>", sub="How fast can you click? Pick a time and start clicking to see your clicks per second.",
    js="click.js",
    tool=f'''<div class="panel">{toolbar("Ready", '<div class="seg" id="modes"><button data-s="1">1s</button><button data-s="5" class="on">5s</button><button data-s="10">10s</button><button data-s="30">30s</button><button data-s="60">60s</button></div><button class="btn" id="reset">↺</button>')}
<div class="clickpad" id="cpspad"><div><div class="big" id="big">Click here</div><div class="sub" id="sub"></div></div></div>
{stats(("s-cps","Clicks / second","0.00"),("s-clicks","Clicks","0"),("s-time","Time left","5.0s"),("s-best","Your best","—"))}</div>''',
    content="""<h2>What is a good CPS?</h2><p>Most people click about <b>6–7 times per second</b>. 8–10 CPS is fast, and anything over 10 is exceptional. Pro players who use special techniques like jitter clicking or butterfly clicking can reach 12–20 CPS.</p>
<h2>How to click faster</h2><ul><li><b>Jitter clicking:</b> tense your arm slightly so your finger vibrates on the button.</li><li><b>Butterfly clicking:</b> alternate two fingers on the same button.</li><li><b>Drag clicking:</b> drag your finger across a textured mouse button so it bounces.</li><li>Use a lightweight mouse with crisp switches, and warm up your hand first.</li></ul>
<h2>Why test your CPS?</h2><p>Click speed matters in games like Minecraft PvP, where faster clicking means more hits. It's also a fun challenge to play with friends.</p>""",
    faq=[("Which test length should I pick?", "5 seconds is the standard. 1 second shows your top burst speed, while 30 and 60 seconds test your stamina."),
         ("Is my best score saved?", "Yes, your best score for each length is saved in your browser so you can try to beat it next time."),
         ("Can a mouse register double clicks by mistake?", "Yes, worn-out switches can do that. Use our Mouse Test to check for accidental double clicks.")])

T["mouse-test"] = dict(
    emoji="🖲️", color="#fbbf24", name="Mouse Test", card="Check every button, scroll wheel and double-click issues",
    title="Mouse Test – Check Mouse Buttons, Scroll Wheel & Double Click",
    desc="Free online mouse tester. Check left, right and middle buttons, side buttons, scroll wheel and double-click. Detect a faulty mouse switch that double-clicks by itself.",
    h1="Mouse <span>Test</span>", sub="Check every mouse button, the scroll wheel and double-click, and spot a failing switch.",
    js="click.js",
    tool=f'''<div class="panel">{toolbar("Click inside the box to start", '<button class="btn" id="reset">↺ Reset</button>')}
<div class="grid2"><div class="clickpad" id="mousearea" style="cursor:crosshair"><div class="center"><div class="mouse"><div class="l"></div><div class="rb"></div><div class="m"></div></div><p class="sub" style="margin-top:14px">Click, right-click, double-click<br>and scroll in this box</p></div></div>
<div><div class="checks">''' + "".join(f'<div class="check" data-k="{k}">{n}</div>' for k, n in [("left", "Left click"), ("right", "Right click"), ("middle", "Middle click"), ("double", "Double click"), ("wheelup", "Scroll up"), ("wheeldown", "Scroll down")]) + '''</div>
''' + stats(("c-left", "Left", "0"), ("c-right", "Right", "0"), ("c-middle", "Middle", "0"), ("c-up", "Scroll up", "0"), ("c-down", "Scroll down", "0"), ("c-back", "Back button", "0"), ("c-forward", "Forward button", "0"), ("c-double", "Double clicks", "0"), ("s-dbl", "Accidental double", "0")) + '''
<p class="note">"Accidental double" counts left clicks less than 80 ms apart, which is too fast for a human and usually means a worn-out switch.</p></div></div></div>''',
    content="""<h2>How to test your mouse</h2><p>Move your pointer into the box and try every button: left, right, middle (press the wheel), scroll up and down, and double-click. Each check turns green when it works. Side buttons (back and forward) are counted too.</p>
<h2>Is my mouse double-clicking by itself?</h2><p>Single-click quickly about 20 times. If the <b>Accidental double</b> counter goes up, your mouse sent two clicks when you pressed once. This is a very common problem with worn-out switches. Cleaning the switch, using a debounce setting in your mouse software, or replacing the switch usually fixes it.</p>
<h2>Scroll wheel jumping?</h2><p>If scrolling down sometimes counts as scrolling up, the wheel's encoder is dirty or worn. A blast of compressed air into the wheel often helps.</p>""",
    faq=[("Why don't my side buttons register?", "Some mice need their own software to send back/forward clicks, and a few browsers handle them before the page sees them. Try a different browser if they don't show."),
         ("Does right-clicking open a menu?", "Not inside the test box. We block the menu there so you can test the right button freely.")])

T["gamepad-test"] = dict(
    emoji="🎮", color="#22d3ee", name="Controller Test", card="Test Xbox, PlayStation and other gamepads, plus stick drift",
    title="Controller Test – Gamepad Tester for Xbox, PS5 & More",
    desc="Free online gamepad tester. Test every button, trigger and joystick on Xbox, PS4, PS5, Switch Pro and PC controllers. Check stick drift and vibration.",
    h1="Controller <span>Test</span>", sub="Plug in your controller and press any button. Test every button, trigger and joystick, and check for stick drift.",
    js="gamepad.js",
    tool=f'''<div class="panel stage">{toolbar("Waiting for controller…")}
<div class="start" id="wait"><div class="ico">🎮</div><p><b>Connect your controller and press any button.</b><br>Works with Xbox, PlayStation (PS4/PS5), Switch Pro and most PC gamepads, wired or Bluetooth.</p><p class="note">🔒 {PRIVATE}</p></div>
<div id="live" class="hidden"><div class="sticks"><div class="stick" id="ls"><i></i><b>Left stick</b></div><div class="stick" id="rs"><i></i><b>Right stick</b></div></div>
<div class="pad" id="btns" style="margin-top:30px"></div>
<div class="row" style="justify-content:center;margin-top:14px"><button class="btn primary" id="rumble">📳 Test vibration</button></div>
{stats(("s-name","Controller","—"),("s-tested","Buttons tested","0"),("s-drift","Stick drift","—"),("s-btn","Buttons","—"),("s-axes","Axes","—"),("s-vib","Vibration","—"))}</div></div>''',
    content="""<h2>How to test your controller</h2><ol><li>Connect your controller with a USB cable or Bluetooth.</li><li>Press any button. Your browser only shows controllers after a button is pressed.</li><li>Press every button and move both sticks. Triggers fill up as you squeeze them.</li></ol>
<h2>How to check for stick drift</h2><p>Let go of both joysticks and look at the <b>Stick drift</b> reading. A perfect stick rests at 0.00. Small values under 0.08 are normal. If the dot keeps moving on its own or the number stays high, your controller has drift, which usually means a worn or dirty stick sensor.</p>
<h2>Controller not showing up?</h2><ul><li>Press a button. Browsers hide controllers until you do.</li><li>Try a different USB cable, as some cables only charge.</li><li>Use Chrome or Edge for the best support, including vibration.</li><li>For PS5 controllers on Bluetooth, hold PS + Create until the light flashes to pair.</li></ul>""",
    faq=[("Does it work with PS5 DualSense controllers?", "Yes. DualSense, DualShock 4, Xbox One and Series controllers, Switch Pro and most generic gamepads all work."),
         ("Why doesn't vibration work?", "Vibration testing works best in Chrome and Edge. Some browsers and some Bluetooth connections don't support it yet."),
         ("Can I fix stick drift?", "Sometimes. Cleaning around the stick with isopropyl alcohol can help. Otherwise the joystick module needs replacing.")])

T["dead-pixel-test"] = dict(
    emoji="🖥️", color="#f472b6", name="Dead Pixel Test", card="Fill your screen with colors to find dead or stuck pixels",
    title="Dead Pixel Test – Check Your Screen for Dead & Stuck Pixels",
    desc="Free dead pixel test. Fill your screen with solid colors to find dead pixels, stuck pixels, backlight bleed and screen damage on monitors, laptops, TVs and phones.",
    h1="Dead Pixel <span>Test</span>", sub="Fill your whole screen with solid colors to spot dead pixels, stuck pixels and backlight bleed.",
    js="screen.js",
    tool=f'''<div class="panel"><div class="start" style="min-height:260px"><div class="ico">🖥️</div><p>Your screen will go fullscreen and show one color at a time. Look closely for tiny dots that don't match.</p>
<div class="row" style="justify-content:center"><button class="btn primary big" id="go">Start test</button><button class="btn big" id="auto">▶ Auto-cycle colors</button></div>
<p class="note">Or tap a color to jump straight to it:</p><div class="swatches" id="swatches"></div><p class="note">Click or press → for the next color · Right-click or ← to go back · Esc to exit</p></div></div>
<div id="fs"><div class="hint"></div></div>''',
    content="""<h2>How to find dead pixels</h2><ol><li>Clean your screen so dust doesn't fool you.</li><li>Click <b>Start test</b>. Your screen fills with one solid color.</li><li>Look slowly over the whole screen, then click for the next color.</li></ol>
<h2>Dead vs stuck pixels</h2><ul><li><b>Dead pixel:</b> stays black on every color. Easiest to see on the white screen.</li><li><b>Stuck pixel:</b> stays one color (often red, green or blue). Easiest to see on the black screen.</li><li><b>Backlight bleed:</b> glowing patches near the edges on the black screen, usually with the lights off.</li></ul>
<h2>Can a stuck pixel be fixed?</h2><p>Stuck pixels sometimes fix themselves. Gently massaging the spot with a soft cloth while the screen is on can help. Dead pixels usually can't be repaired, but many brands replace a new screen that has them, so check your warranty and return window.</p>""",
    faq=[("Does this work on phones and TVs?", "Yes. Open this page on any phone, tablet, laptop or smart TV browser and tap through the colors."),
         ("How many dead pixels are acceptable?", "It depends on the brand's policy. Many will replace a screen with even one dead pixel in the center, while others allow a few. Test new screens right away so you're still within the return window.")])

T["refresh-rate-test"] = dict(
    emoji="⚡", color="#a3e635", name="Refresh Rate Test", card="See your screen's real Hz (60, 120, 144, 240…)",
    title="Refresh Rate Test – What Hz Is My Monitor? (60, 144, 240Hz)",
    desc="Check your monitor's real refresh rate in Hz instantly. See if your 120Hz, 144Hz, 165Hz or 240Hz screen is actually running at full speed.",
    h1="Refresh Rate <span>Test</span>", sub="Instantly see your screen's real refresh rate, and check that your high-Hz monitor is running at full speed.",
    js="hz.js",
    tool=f'''<div class="panel">{toolbar("Measuring…", '<button class="btn" id="reset">↺ Re-test</button>')}
<div class="center" style="padding:10px 0"><div class="hzbig"><span id="hz">--</span><small style="font-size:.35em"> Hz</small></div><p class="note">Your current refresh rate</p></div>
<div class="track" id="track"><i id="box"></i></div>
{stats(("s-ms","Frame time","—"),("s-range","Range","—"),("s-drops","Dropped frames","0"))}</div>''',
    content="""<h2>What is refresh rate?</h2><p>Refresh rate is how many times per second your screen draws a new picture, measured in hertz (Hz). A 60Hz screen updates 60 times a second, while a 144Hz gaming monitor updates 144 times, making motion look much smoother.</p>
<h2>My 144Hz monitor shows 60Hz. Why?</h2><ul><li><b>Windows:</b> Settings → Display → Advanced display, and pick the highest refresh rate.</li><li><b>Mac:</b> System Settings → Displays → Refresh rate.</li><li><b>Use the right cable:</b> DisplayPort or HDMI 2.0+ is needed for high refresh rates. Old HDMI cables can cap you at 60Hz.</li><li><b>Laptops</b> may drop to 60Hz on battery to save power. Plug in and test again.</li></ul>""",
    faq=[("How accurate is this test?", "It measures how often your browser draws frames, which matches your screen's refresh rate on almost all devices. Keep this tab in front and avoid heavy apps while testing."),
         ("Why does my phone show 60Hz?", "Many phones lower their refresh rate to save battery. Turn off battery saver or turn on the high refresh rate setting.")])

T["speaker-test"] = dict(
    emoji="🔊", color="#fbbf24", name="Speaker Test", card="Left/right sound check, tone generator and hearing sweep",
    title="Speaker Test – Left Right Audio Test & Tone Generator",
    desc="Free speaker and headphone test. Check left and right audio channels, play test tones from 20Hz to 20kHz and run a frequency sweep to test bass and treble.",
    h1="Speaker <span>Test</span>", sub="Check that your left and right speakers or headphones work, and test bass and treble with tones.",
    js="speaker.js",
    tool=f'''<div class="panel">{toolbar("Press a button to play")}
<div class="spk"><button class="btn" id="left"><span class="e">◀🔊</span>Left</button><button class="btn" id="both"><span class="e">🔊</span>Both</button><button class="btn" id="right"><span class="e">🔊▶</span>Right</button></div>
<div class="grid2" style="margin-top:18px"><div class="stat"><span>Volume</span><input type="range" id="vol" min="0" max="100" value="60" style="width:100%"></div>
<div class="stat"><span>Tone frequency · <b id="fv" style="display:inline;font-size:1em"></b></span><input type="range" id="freq" min="0" max="1000" value="433" style="width:100%"></div></div>
<div class="row" style="justify-content:center;margin-top:14px"><button class="btn primary" id="tone">▶ Play tone</button><button class="btn" id="sweep">〰 20Hz → 20kHz sweep</button></div>
<p class="note center">⚠️ Start with a low volume, especially with headphones.</p></div>''',
    content="""<h2>How to test your speakers</h2><p>Press <b>Left</b>, <b>Right</b> and <b>Both</b>. You should hear the chime only from the matching side. If the sides are swapped, your headphones are on backwards or your speakers are plugged into the wrong outputs.</p>
<h2>Test bass and treble</h2><p>Use the tone slider or the sweep. Most small laptop speakers can't play much below 100Hz. Most adults can't hear above 15–17kHz, and this upper limit naturally drops with age.</p>
<h2>No sound? Check these</h2><ul><li>Make sure the right output device is selected in your computer's sound settings.</li><li>Check the volume and mute in both your system and your browser tab.</li><li>For Bluetooth headphones, make sure they're connected for audio and not just calls.</li></ul>""",
    faq=[("Can this damage my speakers?", "Not at normal volume. Very loud low or high tones can strain small speakers and your ears, so keep the volume moderate."),
         ("Why do I hear the right sound on both sides?", "Your device might be set to mono audio. Check your accessibility settings, or the speakers may be wired as mono.")])

ORDER = ["mic-test", "webcam-test", "keyboard-test", "cps-test", "mouse-test", "gamepad-test", "dead-pixel-test", "refresh-rate-test", "speaker-test"]
import extra_tests
EXTRA_T = extra_tests.build(T, toolbar, stats, PRIVATE)
T.update(EXTRA_T)
MORE = list(EXTRA_T)
NAV = ["mic-test", "webcam-test", "keyboard-test", "cps-test", "gamepad-test"]

def card(slug):
    t = T[slug]
    return f'<a class="tool" href="{slug}" style="--c:{t["color"]}"><div class="ic">{t["emoji"]}</div><b>{t["name"]}</b><span>{t["card"]}</span><div class="go">Start test →</div></a>'

LOGO = '<a class="logo" href="./"><span class="mark"><svg viewBox="0 0 24 24" fill="none" stroke="#0a0b14" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span><span>Your<em>DeviceTest</em></span></a>'

def page(slug, title, desc, hero, body, content="", faq=None, js=None, related=""):
    url = DOMAIN + "/" + ("" if slug == "index" else slug)
    nav = "".join(f'<a href="{s}"{" class=active" if s == slug else ""}>{T[s]["name"]}</a>' for s in NAV) + f'<a href="./#all"{" class=active" if slug == "index" else ""}>All tests</a>'
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": re.sub("<.*?>", "", title.split(" – ")[0]), "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    faqhtml = ""
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        faqhtml = '<h2>Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq) + "</div>"
    foot = "".join(f'<a href="{s}">{T[s]["name"]}</a>' for s in ORDER + MORE)
    scripts = '<script src="common.js"></script>' + (f'<script src="{js}"></script>' if js else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#07080f">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%2322d3ee'/><stop offset='1' stop-color='%23a78bfa'/></linearGradient></defs><rect width='100' height='100' rx='26' fill='url(%23g)'/><path d='M28 52l15 15 30-32' stroke='%230a0b14' stroke-width='11' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(ld)}</script>
<!-- AdSense script goes here once approved -->
</head>
<body>
<header><div class="wrap topbar">{LOGO}<nav>{nav}</nav></div></header>
<main class="wrap">
{hero}
{body}
<div class="ad"></div>
<section class="content">{content}{faqhtml}</section>
{related}
</main>
<footer><div class="wrap"><div class="foot">{foot}</div>© {SITE} · Free online device tests · <a href="privacy">Privacy</a></div></footer>
{scripts}
</body>
</html>
"""

def hero(h1, sub, pill="Free · No download · Works in your browser"):
    return f'<section class="hero"><span class="pill"><i></i>{pill}</span><h1>{h1}</h1><p>{sub}</p><div class="trust"><span>100% free</span><span>Private</span><span>No sign-up</span><span>Works on phone</span></div></section>'

pages = []
home_body = '<div class="tools" id="all">' + "".join(card(s) for s in ORDER) + "</div>" + '<section class="content"><div class="section-h"><h2>More tests &amp; tools</h2></div></section><div class="tools">' + "".join(card(s) for s in MORE) + "</div>"
pages.append(("index", page("index", "Device Test – Test Your Mic, Webcam, Keyboard, Mouse & More",
    "Free online device tests. Check your microphone, webcam, keyboard, mouse, controller, speakers and screen in seconds. No download, private and mobile-friendly.",
    hero("Test any device <span>in seconds</span>", "Check your microphone, webcam, keyboard, mouse, controller, speakers and screen. Everything runs right in your browser."),
    home_body,
    """<h2>Free device tests, right in your browser</h2><p>Getting ready for a video call, setting up a new gaming rig or checking a used laptop before you buy it? Run quick tests to make sure everything works. There's nothing to install and nothing is uploaded.</p>
<h2>Why use YourDeviceTest?</h2><ul><li><b>Instant:</b> every test starts in one click.</li><li><b>Private:</b> your camera, mic and key presses never leave your device.</li><li><b>Detailed:</b> see real numbers like webcam resolution and FPS, mic levels, stick drift and refresh rate.</li><li><b>Works everywhere:</b> Windows, Mac, Chromebook, iPhone and Android.</li></ul>""",
    faq=[("Do I need to install anything?", "No. Every test runs in your web browser. Just open the page and click start."),
         ("Is it safe to allow camera and microphone access?", "Yes. Access is only used to show the test on your screen. Nothing is recorded or sent to our servers, and you can revoke permission anytime in your browser settings."),
         ("Which browser works best?", "Recent versions of Chrome, Edge, Firefox and Safari all work. Chrome and Edge have the best support for controllers and vibration.")])))

for s in ORDER + MORE:
    t = T[s]
    rel = [x for x in ORDER + MORE if x != s and T[x]["js"] == t["js"]][:3]
    rel += [x for x in ORDER if x != s and x not in rel][:6 - len(rel)]
    related = '<section class="content"><div class="section-h"><h2>More device tests</h2></div></section><div class="tools">' + "".join(card(x) for x in rel) + "</div>"
    pages.append((s, page(s, t["title"], t["desc"], hero(t["h1"], t["sub"]), t["tool"], t["content"], t["faq"], t["js"], related)))

pages.append(("privacy", page("privacy", "Privacy Policy – " + SITE, "Privacy policy for " + SITE, hero("Privacy <span>Policy</span>", "How we handle your data.", "Plain-English privacy"), "",
    f"""<h2>Your camera, mic and inputs stay on your device</h2><p>All device tests run inside your web browser. Video, audio, key presses and controller input are processed locally and are never uploaded, recorded or stored by us. Best scores and similar preferences are saved only in your own browser.</p>
<h2>Advertising</h2><p>This site may use third-party advertising partners such as Google AdSense, which may use cookies to serve ads based on your visits to this and other websites. You can opt out of personalized advertising at <a href="https://adssettings.google.com">Google Ads Settings</a>.</p>
<h2>Contact</h2><p>Questions? Contact us at {CONTACT}.</p>""")))

PREVIEW = os.environ.get("PREVIEW")
for slug, html in pages:
    if PREVIEW:
        html = re.sub(r'href="([a-z0-9-]+)(#[a-z]+)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', html).replace('href="./#all"', 'href="index.html#all"').replace('href="./"', 'href="index.html"')
    (OUT / f"{slug}.html").write_text(html)
urls = "".join(f"<url><loc>{DOMAIN}/{'' if s == 'index' else s}</loc></url>" for s, _ in pages)
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built", len(pages), "pages")

import adready
adready.run(OUT, SITE, DOMAIN, "All device tests on this site")
