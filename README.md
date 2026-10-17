<div align="center">

# 🛡️ FLUX VPN
### A Suíte de VPN 100% Open-Source, Sem Logs & Zero Vazamentos

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Protocol: WireGuard](https://img.shields.io/badge/Protocol-WireGuard%C2%AE-red.svg)](https://www.wireguard.com/)
[![Architecture: RAM--Only](https://img.shields.io/badge/Architecture-RAM--Only%20PXE-green.svg)](#)
[![Zero Logs](https://img.shields.io/badge/Logs-Zero%20Persistent-brightgreen.svg)](#)
[![Chrome Extension: MV3](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-yellow.svg)](clients/extensions/)
[![Platforms: 13](https://img.shields.io/badge/Platforms-13%20Supported-purple.svg)](#plataformas-suportadas)

<p align="center">
  <strong>Construída em resposta direta a abusos da indústria como Urban VPN (rede P2P onde seu IP vira nó de saída) e Planet VPN (código fechado e monetização agressiva).</strong>
</p>

[Testar Simulador Interativo](index.html) • [Ver Landing Page](landing.html) • [Extensão Chrome](clients/extensions/) • [Plano Mestre de Arquitetura](PLANO_MESTRE_FLUX_VPN.md)

</div>

---

## 📌 Por que o FLUX VPN existe?

No ecossistema atual de VPNs gratuitas, existem duas armadilhas críticas comprovadas por análises forenses de tráfego:

1. **O Perigo da Urban VPN (Rede P2P Residencial):**  
   A Urban VPN opera como uma rede P2P corporativa (BIScience). Ao utilizá-la gratuitamente, seu computador ou smartphone é silenciosamente transformado em um **Exit Node (nó de saída)**. Terceiros anônimos na internet navegam utilizando o seu IP residencial, expondo você a graves riscos jurídicos e criminais.
2. **O Modelo Planet VPN (Código Fechado e Funil Publicitário):**  
   Aplicativos com código fechado, anúncios invasivos, SDKs de rastreamento de dados de terceiros e estrangulamento deliberado de banda para forçar assinaturas premium.

O **FLUX VPN** foi projetado para ser o padrão ouro de privacidade digital:
- **100% Código Aberto e Auditável**: Sem backdoors, sem telemetria, sem SDKs de publicidade.
- **Você é Cliente Protegido, NUNCA Nó de Saída**: O FLUX VPN jamais roteia tráfego de outros aparelhos através da sua máquina.
- **Servidores em RAM Pura (Diskless PXE)**: Inicialização de nós via rede sem armazenamento magnético ou SSD persistente. Se a energia for cortada, 100% dos dados voláteis desaparecem instantaneamente.
- **Zero Cadastro e Sem E-mail**: Conecte sem informar nenhum dado pessoal ou financeiro.

---

## 🏗️ Arquitetura e Engenharia de Defesa

```mermaid
graph TD
    UserClient[Cliente FLUX VPN\nmacOS / Windows / Linux / iOS / Android] -->|Túnel WireGuard®\nChaCha20-Poly1305| Gateway[Nó de Entrada FLUX\nServidor em RAM PXE]
    
    subgraph Servidor RAM Volátil (Diskless)
        Gateway --> LocalDNS[Unbound DNS Local\nRecursivo com DNSSEC]
        Gateway --> IPv6Blackhole[IPv6 Blackhole\nDescarte Atômico]
        Gateway --> RAMKernel[Kernel Linux Otimizado\nSem Gravação em Disco]
    end

    RAMKernel -->|IP Mascarado de Alta Performance| Internet((Internet Pública))
    
    subgraph Defesas no Dispositivo do Usuário
        ClientFirewall[Hard Kill Switch de Kernel\nWFP / PF / nftables]
        WiFiShield[Escudo Anti-ARP & Wi-Fi Público]
        WebRTCShield[Bloqueio de WebRTC Stun Leaks]
    end
```

### 1. Hard Kill Switch no Kernel
Diferente de VPNs convencionais que falham silenciosamente quando o aplicativo trava, as regras de firewall do FLUX são gravadas no **Windows Filtering Platform (WFP)**, **Packet Filter (macOS PF)** e **Linux nftables**. Se o handshake com o servidor oscilar por mais de 500ms, o tráfego da placa física é fisicamente bloqueado até que o túnel seja restabelecido.

### 2. Escudo Wi-Fi Público & Anti-ARP Spoofing
Ao conectar em redes Wi-Fi abertas (cafeterias, aeroportos, hotéis):
- Aplica filtragem estrita contra pacotes ARP gratuitos (impedindo ataques de *Man-in-the-Middle*).
- Oculta o dispositivo contra varreduras de portas de rede local (Nmap / NetBIOS / mDNS).
- Criptografa imediatamente todo o fluxo com **ChaCha20-Poly1305** e chaves efêmeras renovadas a cada 180 segundos.

### 3. Neutralizador de WebRTC e DNS Leaks
- **No Navegador (Chrome / Edge / Chromium)**: Força a diretiva `disable_non_proxied_udp` para eliminar de raiz a exposição do IP real via JavaScript WebRTC.
- **No Sistema Operacional**: Roteamento obrigatório de todas as portas UDP 53 e TCP 853 para o nó Unbound interno, bloqueando sequestro de DNS de provedores.

---

## 💻 Extensão para Google Chrome (Manifest V3)

A extensão do FLUX VPN para navegadores baseados em Chromium está localizada na pasta [`clients/extensions/`](clients/extensions/).

### Como instalar no Google Chrome (Modo Desenvolvedor):
1. Abra o Google Chrome e acesse a URL: `chrome://extensions/`
2. No canto superior direito da tela, ative a chave **"Modo do desenvolvedor"**.
3. No menu superior esquerdo que surgirá, clique no botão **"Carregar sem compactação"**.
4. Selecione a pasta do projeto: `FLUXVPN/clients/extensions`.
5. Pronto! O ícone do **FLUX VPN** aparecerá na barra de ferramentas do Chrome com proteção ativa contra vazamentos WebRTC.

---

## 📱 Plataformas Suportadas (13 Ambientes)

| Plataforma | Status | Tecnologia Utilizada |
| :--- | :--- | :--- |
| **Windows** | 🟢 Suportado | Driver WinTun nativo + Firewall WFP |
| **macOS** | 🟢 Suportado | SwiftUI nativo + NetworkExtension (M1/M2/M3/M4) |
| **Linux** | 🟢 Suportado | Daemon Rust de alta performance + nftables |
| **Android** | 🟢 Suportado | Always-on VPN + Kotlin puro |
| **iOS** | 🟢 Suportado | SwiftUI + Secure Enclave Keyring |
| **Huawei (HarmonyOS)** | 🟢 Suportado | Pacotes de rede ArkTS nativos |
| **Google Chrome** | 🟢 Suportado | Manifest V3 com WebRTC Shield |
| **Mozilla Firefox** | 🟢 Suportado | WebExtensions API |
| **Microsoft Edge** | 🟢 Suportado | Manifest V3 Chromium |
| **Opera** | 🟢 Suportado | Chromium Extension Engine |
| **Android TV** | 🟢 Suportado | Interface Leanback para controle remoto |
| **Roteadores (OpenWrt / pfSense)**| 🟢 Suportado | Perfis WireGuard `.conf` e OpenVPN `.ovpn` |
| **Perfis Manuais WireGuard** | 🟢 Suportado | Chaves criptográficas padrão IETF |

---

## 🚀 Como Executar o Simulador Localmente

O repositório inclui tanto a landing page institucional quanto o simulador operacional side-by-side de desktop e mobile:

1. **Abrir a Landing Page Institucional**:
   Abra `landing.html` diretamente em qualquer navegador moderno.
2. **Abrir o Simulador Técnico Side-by-Side**:
   Abra `index.html` para testar os mockups interativos do iPhone 15 Pro e da janela macOS.
3. **Testar o Popup da Extensão**:
   Abra `clients/extensions/popup.html` para testar a interface da extensão de forma isolada.

---

## ⚖️ Licença

Este projeto é software livre licenciado sob a **GNU General Public License v3.0 (GPLv3)**. Você tem total liberdade para auditar, modificar e redistribuir o código, desde que todas as derivações permaneçam 100% de código aberto e sob a mesma licença. Consulte o arquivo [LICENSE](LICENSE) para maiores detalhes.

---

<div align="center">
  <sub>Desenvolvido com foco obsessivo em segurança, transparência e respeito à privacidade dos usuários.</sub>
</div>
