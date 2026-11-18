// Shared helpers
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
function setStatus(el, cls, text) { el.className = "status " + cls; el.innerHTML = "<i></i>" + text; }
function mediaError(e, what) {
  const n = e && e.name;
  if (n === "NotAllowedError" || n === "SecurityError") return `Access was blocked. Click the camera/lock icon in your browser's address bar, allow ${what}, then try again.`;
  if (n === "NotFoundError" || n === "OverconstrainedError") return `No ${what} was found. Make sure it's plugged in and not turned off.`;
  if (n === "NotReadableError" || n === "AbortError") return `Your ${what} is being used by another app (like Zoom, Teams or Discord). Close it and try again.`;
  if (!navigator.mediaDevices) return "Your browser doesn't support this test. Try the latest Chrome, Edge, Firefox or Safari.";
  return `Something went wrong starting your ${what}. Try reloading the page.`;
}
async function listDevices(kind, select, currentId) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) return;
  const devs = (await navigator.mediaDevices.enumerateDevices()).filter(d => d.kind === kind);
  select.innerHTML = devs.map((d, i) => `<option value="${d.deviceId}"${d.deviceId === currentId ? " selected" : ""}>${(d.label || (kind === "videoinput" ? "Camera " : "Microphone ") + (i + 1)).replace(/</g, "&lt;")}</option>`).join("");
  select.parentElement.classList.toggle("hidden", devs.length < 2);
}
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
};
