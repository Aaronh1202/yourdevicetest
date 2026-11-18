// Full-screen solid color screen (white screen, black screen, green screen…)
(() => {
  const fs = $("#fs"), hint = $("#fs .hint"), pick = $("#pick"); let hideT;
  const color = () => pick.value;
  function showHint() { hint.style.opacity = 1; clearTimeout(hideT); hideT = setTimeout(() => hint.style.opacity = 0, 2000); }
  function open() {
    fs.style.background = color(); fs.classList.add("show"); hint.textContent = "Click or press Esc to exit"; showHint();
    const r = fs.requestFullscreen || fs.webkitRequestFullscreen; if (r) r.call(fs).catch(() => { });
  }
  function close() { fs.classList.remove("show"); if (document.fullscreenElement) document.exitFullscreen().catch(() => { }); }
  $("#go").onclick = open;
  $$(".swatches .sw").forEach(b => b.onclick = () => { pick.value = b.dataset.c; $("#preview").style.background = pick.value; open(); });
  pick.oninput = () => $("#preview").style.background = pick.value;
  fs.onclick = close; fs.onmousemove = showHint;
  document.addEventListener("keydown", e => { if (e.key === "Escape" && fs.classList.contains("show")) close(); });
  document.addEventListener("fullscreenchange", () => { if (!document.fullscreenElement) fs.classList.remove("show"); });
  $("#preview").style.background = pick.value;
})();
