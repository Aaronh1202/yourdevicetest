(() => {
  const st = $("#status"), startBox = $("#start"), live = $("#live"), err = $("#err"), v = $("#video"), box = $("#vbox"), sel = $("#device");
  let stream, fpsRaf, frames = 0, t0 = 0;
  const S = id => $("#" + id);
  async function start(deviceId) {
    stop(true); err.classList.add("hidden");
    setStatus(st, "wait", "Waiting for permission…");
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { deviceId: deviceId ? { exact: deviceId } : undefined, width: { ideal: 3840 }, height: { ideal: 2160 } }, audio: false });
    } catch (e) { setStatus(st, "bad", "Camera not available"); err.textContent = mediaError(e, "camera"); err.classList.remove("hidden"); return; }
    v.srcObject = stream; await v.play().catch(() => { });
    startBox.classList.add("hidden"); live.classList.remove("hidden");
    const tr = stream.getVideoTracks()[0], set = tr.getSettings ? tr.getSettings() : {};
    S("s-name").textContent = tr.label || "Default camera";
    const upd = () => {
      const w = v.videoWidth, h = v.videoHeight;
      if (!w) return;
      S("s-res").textContent = w + " × " + h;
      const q = h >= 2160 ? "4K" : h >= 1440 ? "1440p" : h >= 1080 ? "1080p Full HD" : h >= 720 ? "720p HD" : h >= 480 ? "480p" : h + "p";
      S("s-q").textContent = q;
      const g = (a, b) => b ? g(b, a % b) : a, d = g(w, h);
      S("s-ar").textContent = (w / d) + ":" + (h / d);
      setStatus(st, "ok", "Your camera is working!");
    };
    v.onloadedmetadata = v.onresize = upd; upd();
    // measure real fps
    frames = 0; t0 = performance.now();
    if (v.requestVideoFrameCallback) {
      const cb = () => { frames++; const dt = performance.now() - t0; if (dt > 1000) { S("s-fps").textContent = Math.round(frames * 1000 / dt) + " fps"; frames = 0; t0 = performance.now(); } fpsRaf = v.requestVideoFrameCallback(cb); };
      fpsRaf = v.requestVideoFrameCallback(cb);
    } else S("s-fps").textContent = set.frameRate ? Math.round(set.frameRate) + " fps" : "—";
    await listDevices("videoinput", sel, set.deviceId);
  }
  function stop(silent) {
    if (fpsRaf && v.cancelVideoFrameCallback) v.cancelVideoFrameCallback(fpsRaf);
    if (stream) stream.getTracks().forEach(t => t.stop());
    stream = null; v.srcObject = null;
    if (!silent) { live.classList.add("hidden"); startBox.classList.remove("hidden"); setStatus(st, "", "Not started"); }
  }
  $("#go").onclick = () => start();
  $("#stop").onclick = () => stop();
  sel.onchange = () => start(sel.value);
  $("#mirror").onclick = () => box.classList.toggle("mirror");
  $("#full").onclick = () => (box.requestFullscreen || box.webkitRequestFullscreen || (() => { })).call(box);
  $("#snap").onclick = () => {
    if (!v.videoWidth) return;
    const c = document.createElement("canvas"); c.width = v.videoWidth; c.height = v.videoHeight;
    const x = c.getContext("2d");
    if (box.classList.contains("mirror")) { x.translate(c.width, 0); x.scale(-1, 1); }
    x.drawImage(v, 0, 0);
    c.toBlob(b => {
      const u = URL.createObjectURL(b), a = document.createElement("a");
      a.href = u; a.download = "webcam-photo.png"; a.title = "Download photo"; a.innerHTML = `<img src="${u}" alt="Webcam snapshot">`;
      $("#shots").prepend(a);
    }, "image/png");
    box.animate([{ filter: "brightness(2.5)" }, { filter: "none" }], { duration: 250 });
  };
})();
