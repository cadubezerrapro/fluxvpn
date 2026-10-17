/* ==========================================================================
   FLUX VPN EXTENSION — LÓGICA DO POPUP
   ========================================================================== */

const EXT_SERVERS = [
  { id: "br-sp", country: "Brasil", city: "São Paulo #1", flag: "🇧🇷", ping: 18, host: "br-sp.node.fluxvpn.net", port: 443 },
  { id: "us-ny", country: "Estados Unidos", city: "Nova York #3", flag: "🇺🇸", ping: 68, host: "us-ny.node.fluxvpn.net", port: 443 },
  { id: "ch-zur", country: "Suíça", city: "Zurique #1", flag: "🇨🇭", ping: 118, host: "ch-zur.node.fluxvpn.net", port: 443 }
];

let isConnected = true;
let currentServerIndex = 0;
let timerSeconds = 765;
let timerInterval = null;

function updatePopupUI() {
  const btnToggle = document.getElementById("btnToggleConnect");
  const btnAction = document.getElementById("btnAction");
  const statusDot = document.getElementById("statusDot");
  const statusText = document.getElementById("statusText");
  const timer = document.getElementById("popupTimer");

  const server = EXT_SERVERS[currentServerIndex];
  document.getElementById("flagDisplay").textContent = server.flag;
  document.getElementById("countryDisplay").textContent = server.country;
  document.getElementById("cityDisplay").textContent = server.city;
  document.getElementById("pingDisplay").textContent = `${server.ping} ms`;

  if (isConnected) {
    btnToggle.className = "shield-btn connected";
    btnAction.className = "action-btn disconnect";
    btnAction.textContent = "Desconectar";
    statusDot.className = "status-dot green";
    statusText.textContent = "Protegido";
  } else {
    btnToggle.className = "shield-btn disconnected";
    btnAction.className = "action-btn connect";
    btnAction.textContent = "Conectar Agora";
    statusDot.className = "status-dot red";
    statusText.textContent = "Desprotegido";
    timer.textContent = "00:00";
  }
}

function startPopupTimer() {
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (isConnected) {
      timerSeconds++;
      const m = Math.floor(timerSeconds / 60);
      const s = timerSeconds % 60;
      document.getElementById("popupTimer").textContent =
        `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }
  }, 1000);
}

function toggleExtensionConnection() {
  isConnected = !isConnected;
  const server = EXT_SERVERS[currentServerIndex];

  if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.sendMessage) {
    chrome.runtime.sendMessage({
      action: isConnected ? "CONNECT" : "DISCONNECT",
      server: server
    });
  }

  if (isConnected) {
    timerSeconds = 0;
    startPopupTimer();
  } else {
    if (timerInterval) clearInterval(timerInterval);
  }

  updatePopupUI();
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btnToggleConnect").addEventListener("click", toggleExtensionConnection);
  document.getElementById("btnAction").addEventListener("click", toggleExtensionConnection);

  document.getElementById("btnSelectLocation").addEventListener("click", () => {
    currentServerIndex = (currentServerIndex + 1) % EXT_SERVERS.length;
    if (isConnected) {
      toggleExtensionConnection();
      setTimeout(toggleExtensionConnection, 300);
    } else {
      updatePopupUI();
    }
  });

  startPopupTimer();
  updatePopupUI();

  // Recupera status real do service worker no Chrome
  if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.sendMessage) {
    try {
      chrome.runtime.sendMessage({ action: "GET_STATUS" }, (response) => {
        if (chrome.runtime.lastError) return;
        if (response && typeof response.isConnected !== "undefined") {
          isConnected = response.isConnected;
          if (response.selectedServer) {
            const foundIdx = EXT_SERVERS.findIndex(s => s.id === response.selectedServer.id);
            if (foundIdx !== -1) currentServerIndex = foundIdx;
          }
          updatePopupUI();
        }
      });
    } catch (e) {
      // Fallback gracioso
    }
  }
});
