/* ==========================================================================
   FLUX VPN — LANDING PAGE INTERATIVIDADE & ANIMAÇÕES
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

  // 1. ANIMAÇÕES DE ENTRADA SUAVE (INTERSECTION OBSERVER)
  const revealElements = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.12,
      rootMargin: "0px 0px -40px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));
    // Ativa imediatamente elementos na dobra da Hero para renderização instantânea
    document.querySelectorAll(".hero-section .reveal").forEach(el => el.classList.add("active"));
  } else {
    // Fallback caso navegador antigo não suporte
    revealElements.forEach(el => el.classList.add("active"));
  }

  // 2. FAQ ACCORDION INTERATIVO
  const faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach(item => {
    const questionBtn = item.querySelector(".faq-question");

    questionBtn.addEventListener("click", () => {
      const isActive = item.classList.contains("active");

      // Fecha outros itens para foco limpo
      faqItems.forEach(other => {
        if (other !== item) other.classList.remove("active");
      });

      // Alterna o atual
      if (isActive) {
        item.classList.remove("active");
      } else {
        item.classList.add("active");
      }
    });
  });

  // 3. RELÓGIO AO VIVO NA VITRINE HERO
  const liveTimer = document.getElementById("heroLiveTimer");
  if (liveTimer) {
    let heroSeconds = 1122; // Começa em 00:18:42
    setInterval(() => {
      heroSeconds++;
      const m = Math.floor((heroSeconds % 3600) / 60);
      const s = heroSeconds % 60;
      liveTimer.textContent = `00:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }, 1000);
  }

  // 4. HEADER COM SOMBRA SUAVE NO SCROLL
  const siteHeader = document.getElementById("siteHeader");
  if (siteHeader) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 20) {
        siteHeader.style.boxShadow = "0 4px 20px rgba(15, 23, 42, 0.08)";
      } else {
        siteHeader.style.boxShadow = "none";
      }
    });
  }

  // 5. INTERATIVIDADE DA VITRINE DA EXTENSÃO GOOGLE CHROME
  const extShieldBtn = document.getElementById("extShieldBtn");
  const extActionBtn = document.getElementById("extActionBtn");
  const extStatusDot = document.getElementById("extStatusDot");
  const extStatusText = document.getElementById("extStatusText");
  const extTimerDisplay = document.getElementById("extTimerDisplay");
  const extServerPill = document.getElementById("extServerPill");
  const extPillFlag = document.getElementById("extPillFlag");
  const extPillCountry = document.getElementById("extPillCountry");
  const extPillCity = document.getElementById("extPillCity");
  const extPingBadge = document.getElementById("extPingBadge");

  if (extShieldBtn && extActionBtn) {
    let extConnected = true;
    let extSeconds = 1122; // 00:18:42
    let extTimerInterval = null;

    const EXT_NODES = [
      { flag: "🇧🇷", country: "Brasil", city: "São Paulo #1", ping: "18 ms" },
      { flag: "🇺🇸", country: "Estados Unidos", city: "Nova York #3", ping: "68 ms" },
      { flag: "🇨🇭", country: "Suíça", city: "Zurique #1", ping: "118 ms" }
    ];
    let currentNodeIndex = 0;

    function startExtTimer() {
      if (extTimerInterval) clearInterval(extTimerInterval);
      extTimerInterval = setInterval(() => {
        if (extConnected) {
          extSeconds++;
          const m = Math.floor(extSeconds / 60);
          const s = extSeconds % 60;
          if (extTimerDisplay) {
            extTimerDisplay.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
          }
        }
      }, 1000);
    }
    startExtTimer();

    function updateExtState() {
      if (extConnected) {
        extShieldBtn.className = "shield-button mobile-shield connected";
        extActionBtn.className = "action-btn-primary disconnect";
        extActionBtn.textContent = "Desconectar Extensão";
        if (extStatusDot) extStatusDot.className = "status-dot green";
        if (extStatusText) extStatusText.textContent = "Navegador Protegido";
        startExtTimer();
      } else {
        extShieldBtn.className = "shield-button mobile-shield disconnected";
        extActionBtn.className = "action-btn-primary connect";
        extActionBtn.textContent = "Conectar Extensão Agora";
        if (extStatusDot) extStatusDot.className = "status-dot red";
        if (extStatusText) extStatusText.textContent = "Desprotegido";
        if (extTimerInterval) clearInterval(extTimerInterval);
        if (extTimerDisplay) extTimerDisplay.textContent = "00:00";
      }
    }

    function toggleExt() {
      extConnected = !extConnected;
      if (extConnected) extSeconds = 0;
      updateExtState();
    }

    extShieldBtn.addEventListener("click", toggleExt);
    extActionBtn.addEventListener("click", toggleExt);

    if (extServerPill) {
      extServerPill.addEventListener("click", () => {
        currentNodeIndex = (currentNodeIndex + 1) % EXT_NODES.length;
        const node = EXT_NODES[currentNodeIndex];
        if (extPillFlag) extPillFlag.textContent = node.flag;
        if (extPillCountry) extPillCountry.textContent = node.country;
        if (extPillCity) extPillCity.textContent = node.city;
        if (extPingBadge) extPingBadge.textContent = node.ping;
      });
    }
  }

});
