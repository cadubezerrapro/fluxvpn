/* ==========================================================================
   FLUX VPN — MOTOR REATIVO & LÓGICA OPERACIONAL COMPLETA
   ========================================================================== */

// Base de Dados de Servidores Realistas
const SERVERS = [
  {
    id: "br-sp",
    country: "Brasil",
    city: "São Paulo #1",
    flag: "🇧🇷",
    ip: "185.220.101.42",
    ping: 18,
    type: "speed",
    favorite: true
  },
  {
    id: "br-rio",
    country: "Brasil",
    city: "Rio de Janeiro #2",
    flag: "🇧🇷",
    ip: "185.220.101.55",
    ping: 24,
    type: "speed",
    favorite: false
  },
  {
    id: "us-ny",
    country: "Estados Unidos",
    city: "Nova York #3",
    flag: "🇺🇸",
    ip: "198.51.100.88",
    ping: 68,
    type: "speed",
    favorite: true
  },
  {
    id: "us-mia",
    country: "Estados Unidos",
    city: "Miami #1",
    flag: "🇺🇸",
    ip: "198.51.100.102",
    ping: 72,
    type: "speed",
    favorite: false
  },
  {
    id: "de-fra",
    country: "Alemanha",
    city: "Frankfurt #1",
    flag: "🇩🇪",
    ip: "194.26.29.14",
    ping: 110,
    type: "all",
    favorite: true
  },
  {
    id: "ch-zur",
    country: "Suíça",
    city: "Zurique #1 (Privado)",
    flag: "🇨🇭",
    ip: "185.156.172.90",
    ping: 118,
    type: "privacy",
    favorite: true
  },
  {
    id: "is-rey",
    country: "Islândia",
    city: "Reykjavík #1 (No 14 Eyes)",
    flag: "🇮🇸",
    ip: "193.107.86.3",
    ping: 124,
    type: "privacy",
    favorite: false
  },
  {
    id: "nl-ams",
    country: "Holanda",
    city: "Amsterdã #2",
    flag: "🇳🇱",
    ip: "146.70.160.10",
    ping: 115,
    type: "speed",
    favorite: false
  },
  {
    id: "jp-tyo",
    country: "Japão",
    city: "Tóquio #1",
    flag: "🇯🇵",
    ip: "103.152.220.4",
    ping: 230,
    type: "all",
    favorite: false
  }
];

// Estado Inicial da Aplicação (100% Desconectado por Padrão)
const state = {
  isConnected: false,
  isConnecting: false,
  isDisconnecting: false,
  selectedServer: SERVERS[0],
  seconds: 0,
  timerInterval: null,
  activeTab: "all",
  searchQuery: "",
  killSwitchActive: true,
  wifiShieldActive: true,
  lanShieldActive: true,
  leakShieldActive: true,
  realIp: "Detectando IP real...",
  handshakeStepText: "",
  trafficInterval: null,
  downloadSpeed: 0,
  uploadSpeed: 0
};

// ==========================================================================
// 1. SÍNTESE SONORA CYBER (Web Audio API Nativa — Zero arquivos externos)
// ==========================================================================
function playCyberSound(type) {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();

    if (type === "click") {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(600, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.05);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } else if (type === "handshake") {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(550, ctx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.03, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.08);
    } else if (type === "connect") {
      // Chime harmônico de sucesso duplo (587Hz -> 880Hz)
      const osc1 = ctx.createOscillator();
      const osc2 = ctx.createOscillator();
      const gain = ctx.createGain();
      osc1.type = "sine";
      osc2.type = "triangle";
      osc1.frequency.setValueAtTime(587.33, ctx.currentTime);
      osc1.frequency.exponentialRampToValueAtTime(880.00, ctx.currentTime + 0.18);
      osc2.frequency.setValueAtTime(293.66, ctx.currentTime);
      osc2.frequency.exponentialRampToValueAtTime(440.00, ctx.currentTime + 0.18);
      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.38);
      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(ctx.destination);
      osc1.start();
      osc2.start();
      osc1.stop(ctx.currentTime + 0.38);
      osc2.stop(ctx.currentTime + 0.38);
    } else if (type === "disconnect") {
      // Som suave de desativação (880Hz -> 440Hz)
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(740, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(370, ctx.currentTime + 0.18);
      gain.gain.setValueAtTime(0.06, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.22);
    }
  } catch (err) {
    // Silencioso se o áudio estiver desativado no navegador
  }
}

// ==========================================================================
// 2. DETECÇÃO REAL DO IP PÚBLICO (Quando Desconectado)
// ==========================================================================
async function detectUserRealIp() {
  try {
    const res = await fetch("https://api.ipify.org?format=json");
    const data = await res.json();
    if (data && data.ip) {
      state.realIp = data.ip;
      updateUI();
    }
  } catch (e) {
    state.realIp = "177.18.92.10 (Provedor Local)";
    updateUI();
  }
}

// ==========================================================================
// 3. FORMATAÇÃO E CONTROLE DO TIMER
// ==========================================================================
function formatTimer(totalSeconds) {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function startTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
  state.seconds = 0;
  state.timerInterval = setInterval(() => {
    state.seconds++;
    updateTimerDisplays();
  }, 1000);
  updateTimerDisplays();
}

function stopTimer() {
  if (state.timerInterval) {
    clearInterval(state.timerInterval);
    state.timerInterval = null;
  }
  state.seconds = 0;
  updateTimerDisplays();
}

function updateTimerDisplays() {
  const formatted = state.isConnected ? formatTimer(state.seconds) : "00:00";
  const mobileTimer = document.getElementById("mobileTimer");
  const desktopTimer = document.getElementById("desktopTimer");
  if (mobileTimer) mobileTimer.textContent = formatted;
  if (desktopTimer) desktopTimer.textContent = formatted;
}

// ==========================================================================
// 4. SIMULAÇÃO DE TELEMETRIA E TRÁFEGO EM TEMPO REAL
// ==========================================================================
function startTrafficSimulation() {
  if (state.trafficInterval) clearInterval(state.trafficInterval);
  state.trafficInterval = setInterval(() => {
    if (!state.isConnected) return;
    // Oscilação realista de tráfego
    state.downloadSpeed = (Math.random() * 35 + 25).toFixed(1); // 25 a 60 MB/s
    state.uploadSpeed = (Math.random() * 12 + 6).toFixed(1);   // 6 a 18 MB/s

    // Jitter sutil de ping (±2 ms)
    const basePing = state.selectedServer.ping;
    const jitter = Math.floor(Math.random() * 5) - 2;
    const currentPing = Math.max(8, basePing + jitter);

    const mobilePingBadge = document.getElementById("mobilePingBadge");
    if (mobilePingBadge) mobilePingBadge.textContent = `${currentPing} ms`;

    const statDownSpeed = document.getElementById("statDownSpeed");
    const statUpSpeed = document.getElementById("statUpSpeed");
    if (statDownSpeed) statDownSpeed.textContent = `↓ ${state.downloadSpeed} MB/s`;
    if (statUpSpeed) statUpSpeed.textContent = `↑ ${state.uploadSpeed} MB/s`;

    const mobileTrafficSpeed = document.getElementById("mobileTrafficSpeed");
    if (mobileTrafficSpeed) mobileTrafficSpeed.textContent = `↓ ${state.downloadSpeed} MB/s`;
  }, 1500);
}

function stopTrafficSimulation() {
  if (state.trafficInterval) {
    clearInterval(state.trafficInterval);
    state.trafficInterval = null;
  }
  state.downloadSpeed = 0;
  state.uploadSpeed = 0;

  const statDownSpeed = document.getElementById("statDownSpeed");
  const statUpSpeed = document.getElementById("statUpSpeed");
  if (statDownSpeed) statDownSpeed.textContent = "↓ 0.0 MB/s";
  if (statUpSpeed) statUpSpeed.textContent = "↑ 0.0 MB/s";

  const mobileTrafficSpeed = document.getElementById("mobileTrafficSpeed");
  if (mobileTrafficSpeed) mobileTrafficSpeed.textContent = "0.0 MB/s";

  const mobilePingBadge = document.getElementById("mobilePingBadge");
  if (mobilePingBadge) mobilePingBadge.textContent = `${state.selectedServer.ping} ms`;
}

// ==========================================================================
// 5. ATUALIZAÇÃO DA INTERFACE (DESKTOP E MOBILE REATIVOS)
// ==========================================================================
function updateUI() {
  const { isConnected, isConnecting, selectedServer, realIp, handshakeStepText } = state;

  // Elementos Mobile
  const mobileShieldBtn = document.getElementById("mobileShieldBtn");
  const mobileStatusDot = document.getElementById("mobileStatusDot");
  const mobileStatusText = document.getElementById("mobileStatusText");
  const mobileActionBtn = document.getElementById("mobileActionBtn");
  const mobileVirtualIp = document.getElementById("mobileVirtualIp");
  const mobilePillFlag = document.getElementById("mobilePillFlag");
  const mobilePillCountry = document.getElementById("mobilePillCountry");
  const mobilePillCity = document.getElementById("mobilePillCity");
  const mobilePingBadge = document.getElementById("mobilePingBadge");
  const mobileKillBadge = document.getElementById("mobileKillBadge");

  // Elementos Desktop
  const desktopShieldBtn = document.getElementById("desktopShieldBtn");
  const desktopStatusDot = document.getElementById("desktopStatusDot");
  const desktopStatusText = document.getElementById("desktopStatusText");
  const desktopActionBtn = document.getElementById("desktopActionBtn");
  const desktopVirtualIp = document.getElementById("desktopVirtualIp");
  const desktopTitleStatus = document.getElementById("desktopTitleStatus");

  // Definições visuais conforme o estado
  let statusText = "Desconectado";
  let dotClass = "red";
  let shieldClass = "disconnected";
  let btnClass = "connect";
  let btnLabel = "Proteger Minha Conexão";
  let displayIp = `Exposto: ${realIp}`;
  let titleSub = "Conexão Desprotegida • Clique para Conectar";

  if (isConnecting) {
    statusText = handshakeStepText || "Conectando...";
    dotClass = "yellow";
    shieldClass = "connecting";
    btnClass = "connecting";
    btnLabel = "Negociando Túnel...";
    displayIp = "Criptografando rota...";
    titleSub = `Conectando a ${selectedServer.city}...`;
  } else if (isConnected) {
    statusText = "Protegido";
    dotClass = "green";
    shieldClass = "connected";
    btnClass = "disconnect";
    btnLabel = "Desconectar";
    displayIp = selectedServer.ip;
    titleSub = `Protegido • ${selectedServer.city}`;
  }

  // Atualizar Mobile
  if (mobileShieldBtn) {
    mobileShieldBtn.className = `shield-button mobile-shield ${shieldClass}`;
  }
  if (mobileStatusDot) mobileStatusDot.className = `status-dot ${dotClass}`;
  if (mobileStatusText) mobileStatusText.textContent = statusText;
  if (mobileActionBtn) {
    mobileActionBtn.className = `action-btn-primary ${btnClass}`;
    mobileActionBtn.textContent = btnLabel;
  }
  if (mobileVirtualIp) mobileVirtualIp.textContent = displayIp;
  if (mobilePillFlag) mobilePillFlag.textContent = selectedServer.flag;
  if (mobilePillCountry) mobilePillCountry.textContent = selectedServer.country;
  if (mobilePillCity) mobilePillCity.textContent = selectedServer.city;
  if (mobilePingBadge) mobilePingBadge.textContent = `${selectedServer.ping} ms`;
  if (mobileKillBadge) {
    mobileKillBadge.className = `metric-badge ${isConnected ? 'green' : ''}`;
    mobileKillBadge.textContent = isConnected ? 'Ativo' : 'Pronto';
  }

  // Atualizar Desktop
  if (desktopShieldBtn) {
    desktopShieldBtn.className = `shield-button desktop-shield ${shieldClass}`;
  }
  if (desktopStatusDot) desktopStatusDot.className = `status-dot ${dotClass}`;
  if (desktopStatusText) desktopStatusText.textContent = statusText;
  if (desktopActionBtn) {
    desktopActionBtn.className = `action-btn-primary ${btnClass}`;
    desktopActionBtn.textContent = btnLabel;
  }
  if (desktopVirtualIp) desktopVirtualIp.textContent = displayIp;
  if (desktopTitleStatus) desktopTitleStatus.textContent = titleSub;

  updateTimerDisplays();
  renderServerList();
  renderFavoritesChips();
}

// ==========================================================================
// 6. MOTOR DE CONEXÃO & HANDSHAKE REALISTA
// ==========================================================================
function connectVPN() {
  if (state.isConnecting || state.isConnected) return;

  state.isConnecting = true;
  playCyberSound("handshake");

  // Etapa 1: Início
  state.handshakeStepText = "Negociando WireGuard®...";
  updateUI();

  // Etapa 2: Troca de chaves Curve25519
  setTimeout(() => {
    if (!state.isConnecting) return;
    state.handshakeStepText = "Trocando Chaves Curve25519...";
    playCyberSound("handshake");
    updateUI();
  }, 400);

  // Etapa 3: Criptografia ChaCha20
  setTimeout(() => {
    if (!state.isConnecting) return;
    state.handshakeStepText = "Criptografando ChaCha20-Poly1305...";
    updateUI();
  }, 850);

  // Etapa 4: Conexão Estabelecida com Sucesso
  setTimeout(() => {
    if (!state.isConnecting) return;
    state.isConnecting = false;
    state.isConnected = true;
    state.handshakeStepText = "";
    startTimer();
    startTrafficSimulation();
    playCyberSound("connect");
    updateUI();
  }, 1250);
}

function disconnectVPN() {
  if (state.isConnecting) {
    // Cancela tentativa em andamento
    state.isConnecting = false;
    state.handshakeStepText = "";
    updateUI();
    return;
  }

  if (!state.isConnected) return;

  playCyberSound("disconnect");
  state.isConnected = false;
  state.isConnecting = false;
  state.handshakeStepText = "";
  stopTimer();
  stopTrafficSimulation();
  updateUI();
}

function toggleConnection() {
  playCyberSound("click");
  if (state.isConnected) {
    disconnectVPN();
  } else {
    connectVPN();
  }
}

// ==========================================================================
// 7. SELEÇÃO DE SERVIDOR
// ==========================================================================
function selectServer(server) {
  playCyberSound("click");
  const wasConnected = state.isConnected;
  state.selectedServer = server;

  if (wasConnected) {
    // Se estava conectado, simula re-roteamento suave para o novo nó
    state.isConnecting = true;
    state.handshakeStepText = `Alternando para ${server.city}...`;
    updateUI();

    setTimeout(() => {
      state.isConnecting = false;
      state.isConnected = true;
      state.handshakeStepText = "";
      playCyberSound("connect");
      updateUI();
    }, 650);
  } else {
    // Se estava desconectado, apenas atualiza a escolha SEM conectar sozinho!
    updateUI();
  }
}

// ==========================================================================
// 8. RENDERIZAÇÃO DA LISTA DE SERVIDORES
// ==========================================================================
function renderServerList() {
  const container = document.getElementById("serverListContainer");
  if (!container) return;

  const query = state.searchQuery.toLowerCase().trim();

  const filtered = SERVERS.filter(s => {
    const matchesSearch = s.country.toLowerCase().includes(query) ||
                          s.city.toLowerCase().includes(query);
    if (!matchesSearch) return false;

    if (state.activeTab === "speed") return s.ping <= 75;
    if (state.activeTab === "privacy") return s.type === "privacy";
    return true;
  });

  const countBadge = document.getElementById("countAll");
  if (countBadge) countBadge.textContent = filtered.length;

  container.innerHTML = "";

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 32px 16px; color: var(--text-muted); font-size: 13px;">
        Nenhum servidor encontrado para "${state.searchQuery}"
      </div>
    `;
    return;
  }

  filtered.forEach(server => {
    const isSelected = state.selectedServer.id === server.id;
    const pingQuality = server.ping < 50 ? "good" : (server.ping < 120 ? "medium" : "low");

    const item = document.createElement("div");
    item.className = `server-item ${isSelected ? "active" : ""}`;
    item.innerHTML = `
      <div class="server-main-info">
        <span class="server-flag">${server.flag}</span>
        <div class="server-text">
          <span class="server-country">${server.country}</span>
          <span class="server-city">${server.city}</span>
        </div>
      </div>
      <div class="server-meta">
        <div class="server-ping">
          <div class="ping-bars ${pingQuality}">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
          </div>
          <span>${server.ping} ms</span>
        </div>
        <button class="btn-star ${server.favorite ? "starred" : ""}" data-star="${server.id}" title="Favoritar">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="${server.favorite ? "currentColor" : "none"}" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </button>
      </div>
    `;

    item.addEventListener("click", (e) => {
      if (e.target.closest(".btn-star")) return;
      selectServer(server);
    });

    const starBtn = item.querySelector(".btn-star");
    starBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      playCyberSound("click");
      server.favorite = !server.favorite;
      renderServerList();
      renderFavoritesChips();
    });

    container.appendChild(item);
  });
}

function renderFavoritesChips() {
  const container = document.querySelector(".favorites-chips");
  if (!container) return;

  const favs = SERVERS.filter(s => s.favorite);
  container.innerHTML = "";

  favs.forEach(server => {
    const isSelected = state.selectedServer.id === server.id;
    const btn = document.createElement("button");
    btn.className = `fav-chip ${isSelected ? "active" : ""}`;
    btn.innerHTML = `<span class="flag">${server.flag}</span><span class="name">${server.country}</span>`;
    btn.addEventListener("click", () => selectServer(server));
    container.appendChild(btn);
  });
}

// ==========================================================================
// 9. CONFIGURAÇÃO DE EVENTOS
// ==========================================================================
function setupEventListeners() {
  // Cliques nos Escudos e Botões de Conexão
  const mobileShieldBtn = document.getElementById("mobileShieldBtn");
  const desktopShieldBtn = document.getElementById("desktopShieldBtn");
  const mobileActionBtn = document.getElementById("mobileActionBtn");
  const desktopActionBtn = document.getElementById("desktopActionBtn");

  if (mobileShieldBtn) mobileShieldBtn.addEventListener("click", toggleConnection);
  if (desktopShieldBtn) desktopShieldBtn.addEventListener("click", toggleConnection);
  if (mobileActionBtn) mobileActionBtn.addEventListener("click", toggleConnection);
  if (desktopActionBtn) desktopActionBtn.addEventListener("click", toggleConnection);

  // Busca de Servidores
  const searchInput = document.getElementById("serverSearchInput");
  const searchClearBtn = document.getElementById("searchClearBtn");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      if (searchClearBtn) {
        searchClearBtn.style.display = state.searchQuery ? "block" : "none";
      }
      renderServerList();
    });
  }

  if (searchClearBtn) {
    searchClearBtn.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      state.searchQuery = "";
      searchClearBtn.style.display = "none";
      renderServerList();
    });
  }

  // Abas de Categoria
  const tabButtons = document.querySelectorAll(".server-tabs .tab-btn");
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      playCyberSound("click");
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.activeTab = btn.getAttribute("data-tab");
      renderServerList();
    });
  });

  // Switch de Modo de Visualização (Desktop / Mobile / Ambos)
  const switcherButtons = document.querySelectorAll(".switcher-btn");
  const showcaseContainer = document.getElementById("showcaseContainer");

  switcherButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      playCyberSound("click");
      switcherButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const view = btn.getAttribute("data-view");
      if (showcaseContainer) {
        showcaseContainer.classList.remove("view-desktop-only", "view-mobile-only");
        if (view === "desktop") showcaseContainer.classList.add("view-desktop-only");
        if (view === "mobile") showcaseContainer.classList.add("view-mobile-only");
      }
    });
  });

  // Pill Mobile abre seleção rápida
  const mobileServerPill = document.getElementById("mobileServerPill");
  if (mobileServerPill) {
    mobileServerPill.addEventListener("click", () => {
      const currentIndex = SERVERS.findIndex(s => s.id === state.selectedServer.id);
      const nextIndex = (currentIndex + 1) % SERVERS.length;
      selectServer(SERVERS[nextIndex]);
    });
  }

  // Toggles de Segurança (Kill Switch, Wi-Fi, LAN, Leaks)
  const checkKillSwitch = document.getElementById("checkKillSwitch");
  if (checkKillSwitch) {
    checkKillSwitch.addEventListener("change", (e) => {
      state.killSwitchActive = e.target.checked;
      playCyberSound("click");
    });
  }

  // Relógio do Mobile sincronizado com horário local
  const mobileTime = document.getElementById("mobileTime");
  if (mobileTime) {
    const updateTime = () => {
      const now = new Date();
      mobileTime.textContent = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    };
    updateTime();
    setInterval(updateTime, 30000);
  }
}

// ==========================================================================
// 10. INICIALIZAÇÃO CONTROLADA
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  updateUI();
  detectUserRealIp();
});
