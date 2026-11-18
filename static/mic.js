(() => {
  const st = $("#status"), startBox = $("#start"), live = $("#live"), err = $("#err");
  const cv = $("#scope"), ctx = cv.getContext("2d"), meter = $("#meter i"), sel = $("#device");
  let stream, ac, an, raf, peak = 0, heard = false, rec, chunks = [], mode = "wave";
  const S = id => $("#" + id);

  async function start(deviceId) {
    stop(true);
    err.classList.add("hidden");
    setStatus(st, "wait", "Waiting for permission…");
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: { deviceId: deviceId ? { exact: deviceId } : undefined, echoCancellation: false, noiseSuppression: false, autoGainControl: false } });
    } catch (e) { setStatus(st, "bad", "Microphone not available"); err.textContent = mediaError(e, "microphone"); err.classList.remove("hidden"); return; }
    ac = new (window.AudioContext || window.webkitAudioContext)();
    const src = ac.createMediaStreamSource(stream);
    an = ac.createAnalyser(); an.fftSize = 2048; an.smoothingTimeConstant = .75;
    src.connect(an);
    const tr = stream.getAudioTracks()[0], set = tr.getSettings ? tr.getSettings() : {};
    S("s-name").textContent = tr.label || "Default microphone";
    S("s-rate").textContent = ac.sampleRate ? (ac.sampleRate / 1000) + " kHz" : "—";
    S("s-ch").textContent = set.channelCount ? (set.channelCount === 1 ? "Mono" : set.channelCount === 2 ? "Stereo" : set.channelCount) : "Mono";
    startBox.classList.add("hidden"); live.classList.remove("hidden");
    setStatus(st, "wait", "Listening… say something");
    peak = 0; heard = false;
    await listDevices("audioinput", sel, set.deviceId);
    draw();
  }
  function stop(silent) {
    cancelAnimationFrame(raf);
    if (stream) stream.getTracks().forEach(t => t.stop());
    if (ac) ac.close().catch(() => { });
    stream = ac = an = null;
    if (!silent) { live.classList.add("hidden"); startBox.classList.remove("hidden"); setStatus(st, "", "Not started"); }
  }
  function draw() {
    const W = cv.width = cv.clientWidth * devicePixelRatio, H = cv.height = cv.clientHeight * devicePixelRatio;
    const td = new Float32Array(an.fftSize), fd = new Uint8Array(an.frequencyBinCount);
    const loop = () => {
      raf = requestAnimationFrame(loop);
      an.getFloatTimeDomainData(td);
      let sum = 0, pk = 0; for (const v of td) { sum += v * v; pk = Math.max(pk, Math.abs(v)); }
      const rms = Math.sqrt(sum / td.length), db = 20 * Math.log10(rms || 1e-8), lvl = Math.max(0, Math.min(100, (db + 60) / 60 * 100));
      meter.style.width = lvl + "%";
      peak = Math.max(peak, lvl);
      S("s-level").textContent = Math.round(lvl) + "%";
      S("s-peak").textContent = Math.round(peak) + "%";
      if (lvl > 18 && !heard) { heard = true; setStatus(st, "ok", "Your microphone is working!"); }
      ctx.clearRect(0, 0, W, H);
      const g = ctx.createLinearGradient(0, 0, W, 0); g.addColorStop(0, "#22d3ee"); g.addColorStop(.55, "#a78bfa"); g.addColorStop(1, "#f472b6");
      if (mode === "wave") {
        ctx.lineWidth = 2.5 * devicePixelRatio; ctx.strokeStyle = g; ctx.shadowColor = "#a78bfa"; ctx.shadowBlur = 12; ctx.beginPath();
        for (let i = 0; i < td.length; i++) { const x = i / td.length * W, y = H / 2 + td[i] * H * 1.6; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
        ctx.stroke(); ctx.shadowBlur = 0;
      } else {
        an.getByteFrequencyData(fd); const n = 64, bw = W / n;
        ctx.fillStyle = g;
        for (let i = 0; i < n; i++) { const v = fd[Math.floor(Math.pow(i / n, 1.7) * fd.length * .7)] / 255, h = Math.max(2, v * H * .92); ctx.beginPath(); ctx.roundRect ? ctx.roundRect(i * bw + 2, H - h, bw - 4, h, 4) : ctx.rect(i * bw + 2, H - h, bw - 4, h); ctx.fill(); }
      }
    };
    loop();
  }
  $("#go").onclick = () => start();
  $("#stop").onclick = () => stop();
  sel.onchange = () => start(sel.value);
  $$("#view button").forEach(b => b.onclick = () => { mode = b.dataset.v; $$("#view button").forEach(x => x.classList.toggle("on", x === b)); });
  // record & play back
  const recBtn = $("#rec"), audio = $("#playback");
  recBtn.onclick = () => {
    if (!stream || !window.MediaRecorder) return;
    chunks = []; rec = new MediaRecorder(stream);
    rec.ondataavailable = e => chunks.push(e.data);
    rec.onstop = () => { audio.src = URL.createObjectURL(new Blob(chunks, { type: rec.mimeType })); audio.classList.remove("hidden"); audio.play().catch(() => { }); recBtn.disabled = false; recBtn.innerHTML = "⏺ Record 5 seconds"; };
    rec.start(); recBtn.disabled = true;
    let t = 5; recBtn.innerHTML = `🔴 Recording… ${t}`;
    const iv = setInterval(() => { t--; recBtn.innerHTML = `🔴 Recording… ${t}`; if (t <= 0) { clearInterval(iv); rec.stop(); } }, 1000);
  };
  if (!window.MediaRecorder) recBtn.classList.add("hidden");
})();
