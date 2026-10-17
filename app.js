/* ==========================================================================
   FLUX VPN — LÓGICA INTERATIVA & SINCRONIZAÇÃO DESKTOP / MOBILE
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

// Estado da Aplicação
const state = {
  isConnected: true,
  isConnecting: false,
  selectedServer: SERVERS[0],
  seconds: 942, // Começa em 00:15:42
  timerInterval: null,
  activeTab: "all",
  searchQuery: "",
  killSwitchActive: true
};

// Formatação do Timer (HH:MM:SS)
function formatTimer(totalSeconds) {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  if (h > 0) {
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// Inicia o Relógio
function startTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);
  state.timerInterval = setInterval(() => {
    state.seconds++;
    updateTimerDisplays();
  }, 1000);
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

// Sincronização da Interface (Desktop e Mobile)
function updateUI() {
  const { isConnected, isConnecting, selectedServer } = state;

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

  // Elementos Desktop
  const desktopShieldBtn = document.getElementById("desktopShieldBtn");
  const desktopStatusDot = document.getElementById("desktopStatusDot");
  const desktopStatusText = document.getElementById("desktopStatusText");
  const desktopActionBtn = document.getElementById("desktopActionBtn");
  const desktopVirtualIp = document.getElementById("desktopVirtualIp");
  const desktopTitleStatus = document.getElementById("desktopTitleStatus");

  // Status Texts e Classes
  let statusText = "Conectado";
  let dotClass = "green";
  let btnClass = "disconnect";
  let btnLabel = "Desconectar";

  if (isConnecting) {
    statusText = "Conectando...";
    dotClass = "yellow";
    btnClass = "connect";
    btnLabel = "Cancelar";
  } else if (!isConnected) {
    statusText = "Desprotegido";
    dotClass = "red";
    btnClass = "connect";
    btnLabel = "Conectar Agora";
  }

  // Atualizar Mobile
  if (mobileShieldBtn) {
    mobileShieldBtn.className = `shield-button mobile-shield ${isConnected ? "connected" : "disconnected"}`;
  }
  if (mobileStatusDot) mobileStatusDot.className = `status-dot ${dotClass}`;
  if (mobileStatusText) mobileStatusText.textContent = statusText;
  if (mobileActionBtn) {
    mobileActionBtn.className = `action-btn-primary ${btnClass}`;
    mobileActionBtn.textContent = btnLabel;
  }
  if (mobileVirtualIp) {
    mobileVirtualIp.textContent = isConnected ? selectedServer.ip : "---.---.---.---";
  }
  if (mobilePillFlag) mobilePillFlag.textContent = selectedServer.flag;
  if (mobilePillCountry) mobilePillCountry.textContent = selectedServer.country;
  if (mobilePillCity) mobilePillCity.textContent = selectedServer.city;
  if (mobilePingBadge) mobilePingBadge.textContent = `${selectedServer.ping} ms`;

  // Atualizar Desktop
  if (desktopShieldBtn) {
    desktopShieldBtn.className = `shield-button desktop-shield ${isConnected ? "connected" : "disconnected"}`;
  }
  if (desktopStatusDot) desktopStatusDot.className = `status-dot ${dotClass}`;
  if (desktopStatusText) desktopStatusText.textContent = statusText;
  if (desktopActionBtn) {
    desktopActionBtn.className = `action-btn-primary ${btnClass}`;
    desktopActionBtn.textContent = btnLabel;
  }
  if (desktopVirtualIp) {
    desktopVirtualIp.textContent = isConnected ? selectedServer.ip : "---.---.---.---";
  }
  if (desktopTitleStatus) {
    desktopTitleStatus.textContent = isConnected
      ? `Protegido • ${selectedServer.city}`
      : "Conexão Desprotegida";
  }

  updateTimerDisplays();
  renderServerList();
  renderFavoritesChips();
}

// Alternar Conexão (Toggle Connect / Disconnect)
function toggleConnection() {
  if (state.isConnecting) return;

  if (state.isConnected) {
    // Desconectar
    state.isConnected = false;
    stopTimer();
    updateUI();
  } else {
    // Iniciar Conexão com feedback suave
    state.isConnecting = true;
    updateUI();

    setTimeout(() => {
      state.isConnecting = false;
      state.isConnected = true;
      state.seconds = 0;
      startTimer();
      updateUI();
    }, 700);
  }
}

// Selecionar Servidor
function selectServer(server) {
  state.selectedServer = server;
  if (!state.isConnected) {
    // Se estava desconectado, conecta automaticamente ao selecionar
    state.isConnected = true;
    state.seconds = 0;
    startTimer();
  }
  updateUI();
}

// Renderiza a Lista de Servidores na Barra Direita do Desktop
function renderServerList() {
  const container = document.getElementById("serverListContainer");
  if (!container) return;

  const query = state.searchQuery.toLowerCase().trim();

  const filtered = SERVERS.filter(s => {
    // Filtro por busca
    const matchesSearch = s.country.toLowerCase().includes(query) ||
                          s.city.toLowerCase().includes(query);
    if (!matchesSearch) return false;

    // Filtro por aba
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
      server.favorite = !server.favorite;
      renderServerList();
      renderFavoritesChips();
    });

    container.appendChild(item);
  });
}

// Renderiza Chips de Acesso Rápido
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

// Configuração dos Listeners de Eventos
function setupEventListeners() {
  // Conectar/Desconectar em ambos os escudos
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
      // Rotaciona para o próximo servidor na lista
      const currentIndex = SERVERS.findIndex(s => s.id === state.selectedServer.id);
      const nextIndex = (currentIndex + 1) % SERVERS.length;
      selectServer(SERVERS[nextIndex]);
    });
  }

  // Relógio do Mobile
  const mobileTime = document.getElementById("mobileTime");
  if (mobileTime) {
    const now = new Date();
    mobileTime.textContent = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  }
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  startTimer();
  updateUI();
});
