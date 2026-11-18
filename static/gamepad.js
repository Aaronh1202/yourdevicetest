(() => {
  const NAMES = ["A / ✕", "B / ○", "X / □", "Y / △", "LB / L1", "RB / R1", "LT / L2", "RT / R2", "Back / Share", "Start / Options", "L3 (stick)", "R3 (stick)", "D-pad ↑", "D-pad ↓", "D-pad ←", "D-pad →", "Home / PS"];
  const st = $("#status"), wait = $("#wait"), live = $("#live"), btns = $("#btns"), S = id => $("#" + id);
  let idx = null, raf, pressed = new Set();
  function build(gp) {
    btns.innerHTML = gp.buttons.map((_, i) => `<div class="pbtn" data-i="${i}"><div class="fill"></div><span>${NAMES[i] || "Button " + i}</span></div>`).join("");
    S("s-name").textContent = gp.id.replace(/\(.*?Vendor.*?\)/i, "").trim() || "Controller";
    S("s-btn").textContent = gp.buttons.length; S("s-axes").textContent = gp.axes.length;
    S("s-vib").textContent = gp.vibrationActuator ? "Supported" : "Not supported";
    $("#rumble").disabled = !gp.vibrationActuator;
  }
  function loop() {
    raf = requestAnimationFrame(loop);
    const gps = navigator.getGamepads ? navigator.getGamepads() : [];
    let gp = idx !== null ? gps[idx] : null;
    if (!gp) { gp = [...gps].find(Boolean); if (gp) { idx = gp.index; build(gp); wait.classList.add("hidden"); live.classList.remove("hidden"); setStatus(st, "ok", "Controller connected!"); } else return; }
    gp.buttons.forEach((b, i) => {
      const el = btns.children[i]; if (!el) return;
      const v = typeof b === "object" ? b.value : b, p = typeof b === "object" ? b.pressed : b > .5;
      el.firstChild.style.height = (v * 100) + "%"; el.classList.toggle("on", p || v > .5);
      if (p) pressed.add(i);
    });
    S("s-tested").textContent = pressed.size + " / " + gp.buttons.length;
    const stick = (el, x, y) => { el.querySelector("i").style.transform = `translate(${x * 60}px,${y * 60}px)`; el.querySelector("b").textContent = `X ${x.toFixed(2)}  Y ${y.toFixed(2)}`; };
    stick($("#ls"), gp.axes[0] || 0, gp.axes[1] || 0);
    stick($("#rs"), gp.axes[2] || 0, gp.axes[3] || 0);
    const drift = Math.max(...gp.axes.slice(0, 4).map(Math.abs));
    S("s-drift").textContent = drift < .08 ? "None ✓" : drift < .2 ? "Slight (" + drift.toFixed(2) + ")" : "Possible (" + drift.toFixed(2) + ")";
    S("s-drift").style.color = drift < .08 ? "var(--lime)" : drift < .2 ? "var(--amber)" : "var(--red)";
  }
  window.addEventListener("gamepadconnected", e => { idx = e.gamepad.index; });
  window.addEventListener("gamepaddisconnected", e => { if (e.gamepad.index === idx) { idx = null; live.classList.add("hidden"); wait.classList.remove("hidden"); setStatus(st, "bad", "Controller disconnected"); } });
  $("#rumble").onclick = () => { const gp = navigator.getGamepads()[idx]; if (gp && gp.vibrationActuator) gp.vibrationActuator.playEffect("dual-rumble", { duration: 1000, strongMagnitude: 1, weakMagnitude: 1 }).catch(() => { }); };
  if (!navigator.getGamepads) { setStatus(st, "bad", "Your browser doesn't support controllers"); return; }
  loop();
})();
