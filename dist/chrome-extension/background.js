/* ==========================================================================
   FLUX VPN EXTENSION — BACKGROUND SERVICE WORKER (MANIFEST V3)
   Proteção Rígida contra WebRTC Leaks e Roteamento Seguro de Proxy
   ========================================================================== */

// 1. NEUTRALIZADOR DE VAZAMENTOS WEBRTC
// Bloqueia tentativas de requisições STUN/TURN UDP fora do proxy seguro
function enforceWebRTCShield(enable = true) {
  if (chrome.privacy && chrome.privacy.network && chrome.privacy.network.webRTCIPHandlingPolicy) {
    chrome.privacy.network.webRTCIPHandlingPolicy.set({
      value: enable ? "disable_non_proxied_udp" : "default"
    }, () => {
      console.log(`[FLUX VPN] WebRTC Shield definido para: ${enable ? 'disable_non_proxied_udp' : 'default'}`);
    });
  }
}

// 2. APLICADOR DE PROXY DO TÚNEL FLUX
function setFluxProxy(server) {
  if (!server) {
    // Desativa o proxy (Conexão Direta)
    chrome.proxy.settings.clear({ scope: "regular" }, () => {
      console.log("[FLUX VPN] Proxy desativado (Conexão direta)");
    });
    enforceWebRTCShield(false);
    return;
  }

  // Configuração PAC / Proxy Script seguro
  const config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "https",
        host: server.host || "br-sp.node.fluxvpn.net",
        port: server.port || 443
      },
      bypassList: ["localhost", "127.0.0.1", "*.local"]
    }
  };

  chrome.proxy.settings.set({ value: config, scope: "regular" }, () => {
    console.log(`[FLUX VPN] Proxy conectado a: ${server.host}:${server.port}`);
    enforceWebRTCShield(true);
  });
}

// 3. OUVINTE DE MENSAGENS DO POPUP
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "CONNECT") {
    setFluxProxy(message.server);
    chrome.storage.local.set({ isConnected: true, selectedServer: message.server });
    sendResponse({ status: "CONNECTED" });
  } else if (message.action === "DISCONNECT") {
    setFluxProxy(null);
    chrome.storage.local.set({ isConnected: false });
    sendResponse({ status: "DISCONNECTED" });
  } else if (message.action === "GET_STATUS") {
    chrome.storage.local.get(["isConnected", "selectedServer"], (data) => {
      sendResponse(data);
    });
    return true; // Resposta assíncrona
  }
});

// Inicialização: Garante WebRTC seguro por padrão
chrome.runtime.onInstalled.addListener(() => {
  enforceWebRTCShield(true);
  console.log("[FLUX VPN] Extensão instalada com proteção WebRTC ativa.");
});
