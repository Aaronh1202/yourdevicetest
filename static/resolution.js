// What is my screen resolution
(() => {
  const S = (id, v) => $("#" + id).textContent = v;
  function g(a, b) { return b ? g(b, a % b) : a; }
  function upd() {
    const w = screen.width, h = screen.height, d = devicePixelRatio || 1, k = g(w, h);
    $("#res").textContent = w + " × " + h;
    S("s-phys", Math.round(w * d) + " × " + Math.round(h * d));
    S("s-dpr", (+d.toFixed(2)) + "×");
    S("s-view", innerWidth + " × " + innerHeight);
    S("s-ar", (w / k) + ":" + (h / k));
    S("s-depth", screen.colorDepth + "-bit");
    S("s-orient", (screen.orientation && screen.orientation.type || (w >= h ? "landscape" : "portrait")).replace("-primary", "").replace("-secondary", ""));
  }
  upd(); addEventListener("resize", upd);
})();
