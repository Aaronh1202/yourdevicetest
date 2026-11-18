(() => {
  const big = $("#hz"), box = $("#box"), track = $("#track"), S = id => $("#" + id);
  const buf = []; let last = 0, x = 0, dir = 1, minHz = Infinity, maxHz = 0, drops = 0, start = performance.now();
  const common = [60, 75, 90, 100, 120, 144, 165, 170, 180, 200, 240, 280, 300, 360, 480, 500, 540];
  function frame(t) {
    requestAnimationFrame(frame);
    if (last) {
      const dt = t - last;
      if (dt < 200) { buf.push(dt); if (buf.length > 120) buf.shift(); }
      const med = [...buf].sort((a, b) => a - b)[buf.length >> 1];
      if (med && dt > med * 1.7 && t - start > 1500) { drops++; S("s-drops").textContent = drops; }
      if (buf.length > 20 && document.visibilityState === "visible") {
        const hz = 1000 / med, near = common.reduce((a, b) => Math.abs(b - hz) < Math.abs(a - hz) ? b : a);
        const show = Math.abs(near - hz) / hz < .04 ? near : Math.round(hz);
        big.textContent = show;
        S("s-ms").textContent = med.toFixed(2) + " ms";
        if (t - start > 1500) { minHz = Math.min(minHz, show); maxHz = Math.max(maxHz, show); }
        S("s-range").textContent = isFinite(minHz) ? (minHz === maxHz ? minHz + " Hz" : minHz + "–" + maxHz + " Hz") : "—";
        setStatus($("#status"), "ok", show >= 120 ? "High refresh rate display! 🚀" : "Measured your refresh rate");
      }
      const W = track.clientWidth - 40;
      x += dir * W / 90; if (x > W) { x = W; dir = -1; } if (x < 0) { x = 0; dir = 1; }
      box.style.transform = `translateX(${x}px)`;
    }
    last = t;
  }
  document.addEventListener("visibilitychange", () => { last = 0; buf.length = 0; });
  $("#reset").onclick = () => { buf.length = 0; minHz = Infinity; maxHz = 0; drops = 0; S("s-drops").textContent = "0"; start = performance.now(); };
  requestAnimationFrame(frame);
})();
