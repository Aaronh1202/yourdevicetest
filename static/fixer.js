// Stuck pixel fixer: rapidly flashing random colors in a movable square
(() => {
  const box = $("#fixbox"), c = $("#fixcanvas"), g = c.getContext("2d"); let run = false, raf, full = false;
  function frame() {
    const w = c.width, h = c.height, img = g.createImageData(w, h), d = img.data;
    for (let i = 0; i < d.length; i += 4) { const k = Math.random() * 3 | 0; d[i] = k === 0 ? 255 : (Math.random() < .5 ? 255 : 0); d[i + 1] = k === 1 ? 255 : (Math.random() < .5 ? 255 : 0); d[i + 2] = k === 2 ? 255 : (Math.random() < .5 ? 255 : 0); d[i + 3] = 255; }
    g.putImageData(img, 0, 0); if (run) raf = requestAnimationFrame(frame);
  }
  $("#go").onclick = () => {
    run = !run; $("#go").textContent = run ? "■ Stop" : "▶ Start fixer"; box.classList.toggle("hidden", !run);
    setStatus($("#status"), run ? "ok" : "", run ? "Flashing… drag the square over the stuck pixel" : "Stopped");
    if (run) frame(); else cancelAnimationFrame(raf);
  };
  $("#size").oninput = e => { box.style.width = box.style.height = e.target.value + "px"; };
  let drag = null;
  box.addEventListener("pointerdown", e => { drag = [e.clientX - box.offsetLeft, e.clientY - box.offsetTop]; box.setPointerCapture(e.pointerId); });
  box.addEventListener("pointermove", e => { if (!drag) return; box.style.left = (e.clientX - drag[0]) + "px"; box.style.top = (e.clientY - drag[1]) + "px"; });
  box.addEventListener("pointerup", () => drag = null);
})();
