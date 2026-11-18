// Touch screen test: draw with every finger, count simultaneous touches, find dead zones
(() => {
  const c = $("#touchcanvas"), g = c.getContext("2d"); let max = 0, total = 0; const cols = ["#22d3ee", "#a78bfa", "#f472b6", "#a3e635", "#fbbf24", "#fb7185", "#34d399", "#60a5fa", "#f97316", "#e879f9"];
  const last = new Map();
  function size() { const r = c.getBoundingClientRect(), d = devicePixelRatio || 1; c.width = r.width * d; c.height = r.height * d; g.scale(d, d); g.lineCap = "round"; g.lineWidth = 6; }
  size(); addEventListener("resize", size);
  const S = (id, v) => $("#" + id).textContent = v;
  c.addEventListener("pointerdown", e => { e.preventDefault(); c.setPointerCapture(e.pointerId); const r = c.getBoundingClientRect(); last.set(e.pointerId, [e.clientX - r.left, e.clientY - r.top]); total++; max = Math.max(max, last.size); S("s-now", last.size); S("s-max", max); S("s-total", total); setStatus($("#status"), "ok", last.size + " touch" + (last.size > 1 ? "es" : "") + " detected"); });
  c.addEventListener("pointermove", e => { if (!last.has(e.pointerId)) return; const r = c.getBoundingClientRect(), p = last.get(e.pointerId), x = e.clientX - r.left, y = e.clientY - r.top; g.strokeStyle = cols[e.pointerId % cols.length]; g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(x, y); g.stroke(); last.set(e.pointerId, [x, y]); });
  const up = e => { last.delete(e.pointerId); S("s-now", last.size); };
  c.addEventListener("pointerup", up); c.addEventListener("pointercancel", up);
  $("#reset").onclick = () => { g.clearRect(0, 0, c.width, c.height); max = total = 0; S("s-max", 0); S("s-total", 0); S("s-now", 0); };
})();
