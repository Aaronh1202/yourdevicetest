// Spacebar counter / speed test
(() => {
  let dur = 10, n = 0, t0 = 0, timer = null, state = "idle";
  const big = $("#big"), sub = $("#sub"), S = (id, v) => $("#" + id).textContent = v, best = () => store.get("spBest" + dur, 0);
  function reset() { clearInterval(timer); state = "idle"; n = 0; big.textContent = "Press Space"; sub.textContent = `Press the spacebar (or tap here) to start a ${dur}-second test`; S("s-sps", "0.00"); S("s-count", "0"); S("s-time", dur.toFixed(1) + "s"); S("s-best", best() ? best().toFixed(2) : "—"); }
  function finish() { clearInterval(timer); state = "done"; const r = n / dur; big.textContent = r.toFixed(2) + " /s"; sub.innerHTML = `${n} presses in ${dur}s<br><small>Press again in a moment to retry</small>`; if (r > best()) store.set("spBest" + dur, r); S("s-best", best().toFixed(2)); setTimeout(() => { if (state === "done") state = "ready"; }, 900); }
  function hit() {
    if (state === "done") return; if (state === "ready") reset();
    if (state === "idle") { state = "run"; t0 = performance.now(); timer = setInterval(() => { const el = (performance.now() - t0) / 1000, left = Math.max(0, dur - el); S("s-time", left.toFixed(1) + "s"); S("s-sps", (n / Math.max(el, .1)).toFixed(2)); if (left <= 0) finish(); }, 50); }
    n++; big.textContent = n; S("s-count", n); sub.textContent = "Keep going!";
  }
  document.addEventListener("keydown", e => { if (e.code === "Space") { e.preventDefault(); if (!e.repeat) hit(); } });
  $("#sppad").addEventListener("pointerdown", e => { e.preventDefault(); hit(); });
  $$("#modes button").forEach(b => b.onclick = () => { dur = +b.dataset.s; $$("#modes button").forEach(x => x.classList.toggle("on", x === b)); reset(); b.blur(); });
  $("#reset").onclick = () => { reset(); $("#reset").blur(); };
  reset();
})();
