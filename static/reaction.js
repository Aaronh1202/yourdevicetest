// Reaction time test
(() => {
  const pad = $("#rpad"), big = $("#big"), sub = $("#sub"); let state = "idle", t0 = 0, to, times = [];
  const best = () => store.get("rtBest", 0), S = (id, v) => $("#" + id).textContent = v;
  function set(cls, b, s) { pad.className = "clickpad rt " + cls; big.textContent = b; sub.innerHTML = s; }
  function idle() { state = "idle"; set("", "Click to start", "When the box turns green, click as fast as you can."); }
  function arm() { state = "wait"; set("wait", "Wait for green…", "Don't click yet!"); to = setTimeout(() => { state = "go"; t0 = performance.now(); set("go", "CLICK!", ""); }, 1500 + Math.random() * 3000); }
  pad.addEventListener("pointerdown", e => {
    e.preventDefault();
    if (state === "idle" || state === "done") return arm();
    if (state === "wait") { clearTimeout(to); state = "done"; set("early", "Too soon!", "Click to try again."); return; }
    if (state === "go") {
      const ms = Math.round(performance.now() - t0); times.push(ms); state = "done";
      const avg = Math.round(times.reduce((a, b) => a + b, 0) / times.length);
      if (!best() || ms < best()) store.set("rtBest", ms);
      set("", ms + " ms", (ms < 200 ? "⚡ Lightning fast!" : ms < 250 ? "🔥 Great reflexes" : ms < 300 ? "👍 About average" : "🐢 Keep practicing") + "<br><small>Click to go again</small>");
      S("s-last", ms + " ms"); S("s-avg", avg + " ms"); S("s-tries", times.length); S("s-best", best() + " ms");
    }
  });
  $("#reset").onclick = () => { times = []; S("s-last", "—"); S("s-avg", "—"); S("s-tries", "0"); idle(); };
  if (best()) S("s-best", best() + " ms");
  idle();
})();
