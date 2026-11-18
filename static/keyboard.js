(() => {
  const ROWS = [
    [["Escape", "Esc"], ["F1"], ["F2"], ["F3"], ["F4"], ["F5"], ["F6"], ["F7"], ["F8"], ["F9"], ["F10"], ["F11"], ["F12"], ["Delete", "Del", "w15"]],
    [["Backquote", "`"], ["Digit1", "1"], ["Digit2", "2"], ["Digit3", "3"], ["Digit4", "4"], ["Digit5", "5"], ["Digit6", "6"], ["Digit7", "7"], ["Digit8", "8"], ["Digit9", "9"], ["Digit0", "0"], ["Minus", "-"], ["Equal", "="], ["Backspace", "⌫ Backspace", "w2"]],
    [["Tab", "Tab", "w15"], ["KeyQ", "Q"], ["KeyW", "W"], ["KeyE", "E"], ["KeyR", "R"], ["KeyT", "T"], ["KeyY", "Y"], ["KeyU", "U"], ["KeyI", "I"], ["KeyO", "O"], ["KeyP", "P"], ["BracketLeft", "["], ["BracketRight", "]"], ["Backslash", "\\", "w15"]],
    [["CapsLock", "Caps", "w175"], ["KeyA", "A"], ["KeyS", "S"], ["KeyD", "D"], ["KeyF", "F"], ["KeyG", "G"], ["KeyH", "H"], ["KeyJ", "J"], ["KeyK", "K"], ["KeyL", "L"], ["Semicolon", ";"], ["Quote", "'"], ["Enter", "Enter ↵", "w2"]],
    [["ShiftLeft", "Shift", "w25"], ["KeyZ", "Z"], ["KeyX", "X"], ["KeyC", "C"], ["KeyV", "V"], ["KeyB", "B"], ["KeyN", "N"], ["KeyM", "M"], ["Comma", ","], ["Period", "."], ["Slash", "/"], ["ShiftRight", "Shift", "w25"]],
    [["ControlLeft", "Ctrl", "w15"], ["MetaLeft", "Win/⌘", "w15"], ["AltLeft", "Alt", "w15"], ["Space", "Space", "w6"], ["AltRight", "Alt", "w15"], ["ArrowLeft", "←"], ["ArrowUp", "↑"], ["ArrowDown", "↓"], ["ArrowRight", "→"], ["ControlRight", "Ctrl", "w15"]],
  ];
  const kb = $("#kb");
  kb.innerHTML = ROWS.map(r => `<div class="r">${r.map(k => `<div class="k ${k[2] || ""}" data-code="${k[0]}">${(k[1] || k[0]).replace(/</g, "&lt;")}</div>`).join("")}</div>`).join("");
  const total = $$(".k", kb).length, seen = new Set(), held = new Set();
  let maxHeld = 0, count = 0;
  const S = id => $("#" + id), log = $("#log"), last = $("#last");
  function upd() {
    S("s-tested").textContent = $$(".k.done", kb).length + " / " + total;
    S("s-max").textContent = maxHeld;
    S("s-count").textContent = count;
  }
  document.addEventListener("keydown", e => {
    if (e.target.matches("input,textarea,select")) return;
    if (!(e.ctrlKey && ["KeyR", "KeyW", "KeyT", "KeyL"].includes(e.code)) && e.code !== "F5" && e.code !== "F12") e.preventDefault();
    const el = kb.querySelector(`[data-code="${e.code}"]`);
    if (el) el.classList.add("down", "done");
    if (!e.repeat) {
      count++; held.add(e.code); maxHeld = Math.max(maxHeld, held.size); seen.add(e.code);
      last.textContent = e.key === " " ? "Space" : e.key.length === 1 ? e.key.toUpperCase() : e.key;
      S("s-code").textContent = e.code || "—";
      S("s-which").textContent = e.keyCode || "—";
      const s = document.createElement("span"); s.textContent = e.key === " " ? "Space" : e.key; log.prepend(s);
      while (log.children.length > 24) log.lastChild.remove();
      setStatus($("#status"), "ok", "Keys are registering!");
    }
    upd();
  });
  document.addEventListener("keyup", e => {
    held.delete(e.code);
    const el = kb.querySelector(`[data-code="${e.code}"]`);
    if (el) el.classList.remove("down");
    // PrintScreen only fires keyup on some systems
    if (e.code === "PrintScreen") count++;
    upd();
  });
  window.addEventListener("blur", () => { held.clear(); $$(".k.down", kb).forEach(k => k.classList.remove("down")); });
  $("#reset").onclick = () => { $$(".k", kb).forEach(k => k.classList.remove("done", "down")); held.clear(); maxHeld = 0; count = 0; log.innerHTML = ""; last.textContent = ""; setStatus($("#status"), "", "Press any key to start"); upd(); };
  upd();
})();
