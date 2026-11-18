(() => {
  const COLORS = [["#ff0000", "Red"], ["#00ff00", "Green"], ["#0000ff", "Blue"], ["#ffffff", "White"], ["#000000", "Black"], ["#00ffff", "Cyan"], ["#ff00ff", "Magenta"], ["#ffff00", "Yellow"], ["#808080", "Gray"]];
  const fs = $("#fs"), hint = $("#fs .hint"), sw = $("#swatches");
  let i = 0, auto = null, hideT;
  sw.innerHTML = COLORS.map((c, k) => `<button class="sw" data-i="${k}" style="background:${c[0]}" title="${c[1]}" aria-label="${c[1]} screen"></button>`).join("");
  function paint() { fs.style.background = COLORS[i][0]; hint.textContent = `${COLORS[i][1]} · ${i + 1}/${COLORS.length} · Click or → for next · Esc to exit`; showHint(); }
  function showHint() { hint.style.opacity = 1; clearTimeout(hideT); hideT = setTimeout(() => hint.style.opacity = 0, 2200); }
  function open(k) {
    i = k || 0; fs.classList.add("show"); paint();
    const r = fs.requestFullscreen || fs.webkitRequestFullscreen; if (r) r.call(fs).catch(() => { });
  }
  function close() { fs.classList.remove("show"); clearInterval(auto); auto = null; if (document.fullscreenElement) document.exitFullscreen().catch(() => { }); }
  const next = d => { i = (i + d + COLORS.length) % COLORS.length; paint(); };
  $("#go").onclick = () => open(0);
  $("#auto").onclick = () => { open(0); auto = setInterval(() => next(1), 2000); };
  sw.onclick = e => { const b = e.target.closest(".sw"); if (b) open(+b.dataset.i); };
  fs.onclick = () => next(1);
  fs.oncontextmenu = e => { e.preventDefault(); next(-1); };
  fs.onmousemove = showHint;
  document.addEventListener("keydown", e => {
    if (!fs.classList.contains("show")) return;
    if (e.key === "Escape") close(); else if (["ArrowRight", " ", "ArrowDown", "Enter"].includes(e.key)) { e.preventDefault(); next(1); } else if (["ArrowLeft", "ArrowUp"].includes(e.key)) next(-1);
  });
  document.addEventListener("fullscreenchange", () => { if (!document.fullscreenElement && fs.classList.contains("show")) close(); });
})();
