// CPS test + mouse button test
(() => {
  const pad = $("#cpspad");
  if (pad) {
    let dur = 5, clicks = 0, t0 = 0, timer = null, state = "idle";
    const big = $("#big"), sub = $("#sub"), S = id => $("#" + id);
    const best = () => store.get("cpsBest" + dur, 0);
    const showBest = () => S("s-best").textContent = best() ? best().toFixed(2) : "—";
    function reset() { clearInterval(timer); state = "idle"; clicks = 0; big.textContent = "Click here"; big.style.fontSize = ""; sub.textContent = `Start clicking to begin a ${dur}-second test`; S("s-cps").textContent = "0.00"; S("s-clicks").textContent = "0"; S("s-time").textContent = dur.toFixed(1) + "s"; showBest(); }
    function finish() {
      clearInterval(timer); state = "done";
      const cps = clicks / dur;
      big.textContent = cps.toFixed(2) + " CPS";
      const rank = cps >= 12 ? "🚀 Insane speed!" : cps >= 9 ? "⚡ Super fast!" : cps >= 7 ? "🔥 Great job!" : cps >= 5 ? "👍 Nice, keep practicing" : "🐢 Warm up and try again";
      sub.innerHTML = `${clicks} clicks in ${dur}s · ${rank}<br><small>Click again in a moment to retry</small>`;
      S("s-cps").textContent = cps.toFixed(2);
      if (cps > best()) { store.set("cpsBest" + dur, cps); sub.innerHTML += "<br><b style='color:var(--lime)'>🏆 New personal best!</b>"; }
      showBest();
      setTimeout(() => { if (state === "done") state = "ready"; }, 900);
    }
    pad.addEventListener("pointerdown", e => {
      if (e.button !== 0 && e.pointerType === "mouse") return;
      const r = document.createElement("i"); r.className = "ripple"; const b = pad.getBoundingClientRect();
      r.style.left = (e.clientX - b.left) + "px"; r.style.top = (e.clientY - b.top) + "px"; pad.appendChild(r); setTimeout(() => r.remove(), 500);
      if (state === "done") return;
      if (state === "ready") reset();
      if (state === "idle") {
        state = "run"; t0 = performance.now(); clicks = 0;
        timer = setInterval(() => {
          const el = (performance.now() - t0) / 1000, left = Math.max(0, dur - el);
          S("s-time").textContent = left.toFixed(1) + "s"; S("s-cps").textContent = (clicks / Math.max(el, .1)).toFixed(2);
          if (left <= 0) finish();
        }, 50);
      }
      clicks++; big.textContent = clicks; S("s-clicks").textContent = clicks; sub.textContent = "Keep clicking!";
    });
    $$("#modes button").forEach(b => b.onclick = () => { dur = +b.dataset.s; $$("#modes button").forEach(x => x.classList.toggle("on", x === b)); reset(); });
    $("#reset").onclick = reset;
    reset();
  }

  const area = $("#mousearea");
  if (area) {
    const L = $(".mouse .l"), R = $(".mouse .rb"), M = $(".mouse .m"), S = id => $("#" + id);
    const done = k => { const c = $(`.check[data-k="${k}"]`); if (c && !c.classList.contains("ok")) { c.classList.add("ok"); if ($$(".check.ok").length === $$(".check").length) setStatus($("#status"), "ok", "All mouse buttons work!"); } };
    const parts = { 0: L, 1: M, 2: R }, names = { 0: "left", 1: "middle", 2: "right", 3: "back", 4: "forward" };
    const counts = store.get("mouseCounts", null) || {};
    area.addEventListener("contextmenu", e => e.preventDefault());
    area.addEventListener("mousedown", e => {
      e.preventDefault();
      setStatus($("#status"), "ok", "Mouse is registering clicks");
      if (parts[e.button]) parts[e.button].classList.add("on", "hit");
      const n = names[e.button]; if (n) { done(n); counts[n] = (counts[n] || 0) + 1; S("c-" + n).textContent = counts[n]; }
    });
    window.addEventListener("mouseup", e => { if (parts[e.button]) parts[e.button].classList.remove("on"); });
    area.addEventListener("dblclick", () => { done("double"); counts.double = (counts.double || 0) + 1; S("c-double").textContent = counts.double; });
    area.addEventListener("wheel", e => {
      e.preventDefault(); const k = e.deltaY < 0 ? "up" : "down"; done("wheel" + k);
      counts[k] = (counts[k] || 0) + 1; S("c-" + k).textContent = counts[k];
      M.classList.add("on"); clearTimeout(M._t); M._t = setTimeout(() => M.classList.remove("on"), 120);
    }, { passive: false });
    // double-click detector: flag clicks closer than 80ms (common sign of a failing switch)
    let lastDown = 0, dbl = 0;
    area.addEventListener("mousedown", e => { if (e.button !== 0) return; const t = performance.now(); if (t - lastDown < 80) { dbl++; S("s-dbl").textContent = dbl; S("s-dbl").style.color = "var(--red)"; } lastDown = t; });
    $("#reset").onclick = () => { $$(".check").forEach(c => c.classList.remove("ok")); Object.keys(counts).forEach(k => delete counts[k]); $$("[id^=c-]").forEach(x => x.textContent = "0"); dbl = 0; S("s-dbl").textContent = "0"; S("s-dbl").style.color = ""; $$(".mouse .hit").forEach(x => x.classList.remove("hit")); setStatus($("#status"), "", "Click inside the box to start"); };
  }
})();
