(() => {
  let ac, playing = null, nodes = [];
  const ctx = () => ac || (ac = new (window.AudioContext || window.webkitAudioContext)());
  const vol = $("#vol");
  function stopAll() { nodes.forEach(n => { try { n.stop(); } catch (e) { } }); nodes = []; $$(".spk button,.playbtn").forEach(b => b.classList.remove("playing")); playing = null; }
  // pleasant chime pattern panned to a side
  function chime(pan, btn) {
    stopAll(); const a = ctx(); a.resume(); playing = btn; btn.classList.add("playing");
    const p = a.createStereoPanner ? a.createStereoPanner() : null, g = a.createGain();
    g.gain.value = vol.value / 100;
    if (p) { p.pan.value = pan; g.connect(p).connect(a.destination); } else g.connect(a.destination);
    const notes = [523.25, 659.25, 783.99, 1046.5];
    let t = a.currentTime + .02;
    for (let r = 0; r < 2; r++) notes.forEach(f => {
      const o = a.createOscillator(), e = a.createGain(); o.type = "sine"; o.frequency.value = f;
      e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(.6, t + .02); e.gain.exponentialRampToValueAtTime(.001, t + .4);
      o.connect(e).connect(g); o.start(t); o.stop(t + .45); nodes.push(o); t += .2;
    });
    setTimeout(() => { if (playing === btn) { btn.classList.remove("playing"); playing = null; } }, (t - a.currentTime) * 1000);
    setStatus($("#status"), "ok", pan < 0 ? "Playing on the LEFT speaker" : pan > 0 ? "Playing on the RIGHT speaker" : "Playing on BOTH speakers");
  }
  $("#left").onclick = e => chime(-1, e.currentTarget);
  $("#both").onclick = e => chime(0, e.currentTarget);
  $("#right").onclick = e => chime(1, e.currentTarget);
  // tone generator / frequency test
  const fr = $("#freq"), fv = $("#fv"); let osc, og;
  const fval = () => Math.round(20 * Math.pow(1000, fr.value / 1000));
  const showF = () => fv.textContent = fval() >= 1000 ? (fval() / 1000).toFixed(1) + " kHz" : fval() + " Hz";
  fr.oninput = () => { showF(); if (osc) osc.frequency.setTargetAtTime(fval(), ctx().currentTime, .02); };
  vol.oninput = () => { if (og) og.gain.setTargetAtTime(vol.value / 100 * .3, ctx().currentTime, .02); };
  $("#tone").onclick = e => {
    const b = e.currentTarget;
    if (osc) { osc.stop(); osc = null; b.classList.remove("playing"); b.innerHTML = "▶ Play tone"; return; }
    const a = ctx(); a.resume(); osc = a.createOscillator(); og = a.createGain(); osc.type = "sine"; osc.frequency.value = fval();
    og.gain.value = vol.value / 100 * .3; osc.connect(og).connect(a.destination); osc.start(); b.classList.add("playing"); b.innerHTML = "■ Stop tone";
  };
  $("#sweep").onclick = e => {
    const b = e.currentTarget; stopAll(); const a = ctx(); a.resume();
    const o = a.createOscillator(), g = a.createGain(); o.type = "sine";
    o.frequency.setValueAtTime(20, a.currentTime); o.frequency.exponentialRampToValueAtTime(20000, a.currentTime + 10);
    g.gain.value = vol.value / 100 * .25; o.connect(g).connect(a.destination); o.start(); o.stop(a.currentTime + 10); nodes.push(o);
    b.classList.add("playing"); const t0 = a.currentTime;
    const iv = setInterval(() => { const el = a.currentTime - t0; if (el >= 10 || !nodes.includes(o)) { clearInterval(iv); b.classList.remove("playing"); fv.textContent = "Sweep done"; return; } const f = 20 * Math.pow(1000, el / 10); fv.textContent = (f >= 1000 ? (f / 1000).toFixed(1) + " kHz" : Math.round(f) + " Hz"); }, 50);
  };
  showF();
})();
