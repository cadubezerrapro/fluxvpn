# 🛡️ FLUX VPN — PLANO MESTRE DE ENGENHARIA & ARQUITETURA OPEN-SOURCE
**Documento Técnico de Especificação, Análise Forense e Diretrizes de Implementação**
*Versão 1.0 — Confidencial & Estratégico*

---

## 📑 ÍNDICE GERAL

1. [Sumário Executivo e Manifesto FLUX VPN](#1-sumário-executivo-e-manifesto-flux-vpn)
2. [Auditoria Forense da Indústria: Riscos de Redes P2P Residenciais e Softwares Fechados](#2-auditoria-forense-da-indústria-riscos-de-redes-p2p-residenciais-e-softwares-fechados)
   - 2.1 A Armadilha de Redes P2P Residenciais (Exit Node Hijacking)
   - 2.2 O Modelo Freemium Fechado (Código Proprietário e Telemetria)
   - 2.3 Matriz Comparativa Definitiva: Redes P2P vs Softwares Fechados vs FLUX VPN
3. [Engenharia de "Zero Leaks" e Segurança de Nível Militar](#3-engenharia-de-zero-leaks-e-segurança-de-nível-militar)
   - 3.1 Anatomia e Blindagem contra DNS Leaks
   - 3.2 Erradicação de Vazamentos IPv6 (Dual-Stack vs Blackholing)
   - 3.3 Neutralização de WebRTC Leaks (Desktop e Navegadores)
   - 3.4 Kill Switch em Nível de Kernel (WFP, PF e nftables)
   - 3.5 Blindagem contra Ataques em Wi-Fi Públicas & Ameaças Locais (Zero-Trust LAN)
4. [Pilha de Protocolos e Criptografia do FLUX VPN](#4-pilha-de-protocolos-e-criptografia-do-flux-vpn)
   - 4.1 WireGuard: O Núcleo de Alta Performance
   - 4.2 Camada Ofuscada Anti-DPI (AmneziaWG / VLESS Reality)
   - 4.3 OpenVPN Otimizado (Legado para Roteadores)
5. [Estratégia Multiplataforma (13 Ecossistemas Alvo)](#5-estratégia-multiplataforma-13-ecossistemas-alvo)
   - 5.1 Windows (WPF/Tauri + WinTun + WFP)
   - 5.2 macOS (SwiftUI + NetworkExtension + PF)
   - 5.3 Linux (Rust Core Daemon + CLI + nftables + GUI)
   - 5.4 Android & Android TV (Kotlin + WireGuard Android + Leanback UI)
   - 5.5 iOS (Swift + NEPacketTunnelProvider + Secure Enclave)
   - 5.6 Huawei (Build HMS + F-Droid independente)
   - 5.7 Extensões de Navegador (Chrome, Firefox, Opera, Edge - Manifest V3)
   - 5.8 Roteadores & Perfis Manuais (OpenWrt, DD-WRT, pfSense, .ovpn, .conf)
6. [Infraestrutura de Servidores 100% em RAM (RAM-Only Diskless)](#6-infraestrutura-de-servidores-100-em-ram-ram-only-diskless)
   - 6.1 Boot PXE/Tmpfs e Destruição Criptográfica de Logs
   - 6.2 Mitigação do Armazenamento de IP de Handshake do WireGuard
   - 6.3 Egress NAT e Anonymity Pool
   - 6.4 Jurisdições Estratégicas Fora dos 14 Eyes
7. [Arquitetura de Software do Repositório (Monorepo FLUX)](#7-arquitetura-de-software-do-repositório-monorepo-flux)
8. [Modelo de Sustentabilidade Ético e Governança](#8-modelo-de-sustentabilidade-ético-e-governança)
9. [Roadmap de Execução Passo a Passo (Fases 1 a 6)](#9-roadmap-de-execução-passo-a-passo-fases-1-a-6)

---

## 1. SUMÁRIO EXECUTIVO E MANIFESTO FLUX VPN

O mercado de "VPNs gratuitas" é amplamente dominado por ilusões de segurança, modelos de monetização predatórios e vazamentos massivos de dados. Serviços comerciais gratuitos populares atraem dezenas de milhões de downloads com promessas de "100% grátis e ilimitado", porém escondem contrapartidas graves que comprometem a segurança e a integridade jurídica do usuário final.

O **FLUX VPN** nasce com uma missão clara:
> **Criar a primeira suíte de VPN verdadeiramente Open-Source, com infraestrutura verificável, proteção matemática contra vazamentos (DNS, IPv6, WebRTC) e ausência absoluta de rastreamento.**

### Os 5 Pilares Inegociáveis do FLUX VPN:
1. **Transparência Auditável (100% Open-Source):** Todo o código-fonte (clientes, daemons, scripts de servidor e extensões) aberto no GitHub sob licença GPLv3 / Apache 2.0, com *Reproducible Builds* (compilações determinísticas verificáveis via SHA256).
2. **Zero Leaks de Fato:** Kill Switch acoplado diretamente aos drivers de rede do kernel dos sistemas operacionais, impedindo a passagem de qualquer pacote desprotegido em caso de oscilação do túnel.
3. **Nenhum Usuário como Cobaia ou Exit Node:** Rejeição veemente do modelo de proxy residencial P2P. A infraestrutura FLUX é composta exclusivamente por nós dedicados de alta performance.
4. **Infraestrutura Volátil (RAM-Only):** Servidores de VPN que operam puramente em memória RAM através de sistemas diskless (PXE/tmpfs). Ao desligar ou reiniciar o servidor, qualquer vestígio de tráfego é instantaneamente aniquilado.
5. **Universalidade Sem Degradação:** Clientes dedicados e otimizados para todos os sistemas operacionais modernos, televisores inteligentes, extensões de navegadores e roteadores.

---

## 2. AUDITORIA FORENSE DA INDÚSTRIA: RISCOS DE MODELOS P2P RESIDENCIAIS E CÓDIGO FECHADO

Para conceber uma solução superior, realizamos uma engenharia reversa conceitual e análise detalhada dos modelos dominantes no mercado de VPNs.

### 2.1 A Armadilha de Redes P2P Residenciais (Exit Node Hijacking)
Ao examinar termos de uso, políticas de privacidade e tráfego de pacotes em redes VPN gratuitas baseadas em P2P, constata-se a realidade por trás do serviço "100% Gratuito e Ilimitado":

* **Rede P2P Residencial (Exit Node Hijacking):** Ao aceitar o plano gratuito, o computador ou celular do usuário se transforma silenciosamente em um **nó de saída (Exit Node)** para outros usuários da rede e clientes corporativos de proxies residenciais.
* **O Risco Penal e Civil:** Se outro membro da rede ou cliente corporativo utilizar o nó de saída para cometer cibercrimes (ataques DDoS, scraping agressivo, disseminação de conteúdo ilícito, estelionato digital), **o endereço IP residencial do usuário comum aparecerá nos registros das autoridades e provedores de internet (ISPs)**.
* **Vazamento Sistêmico de WebRTC e DNS:** As extensões de navegador dessas redes atuam meramente como proxies HTTP/SOCKS com injeção de scripts, sem isolamento de socket UDP. Isso resulta em vazamentos frequentes do endereço IP real através de requisições STUN/TURN da API WebRTC dos navegadores.
* **Coleta de Telemetria Comercial:** Os dados de navegação e performance de rede são minerados e anonimizados para alimentação de inteligência de mercado e pesquisa corporativa.

### 2.2 O Modelo Freemium Fechado (Código Proprietário e Telemetria)
Em provedores comerciais de código fechado convencionais:

* **Arquitetura Base:** Utilizam servidores centrais com protocolos proprietários ou fechados, sem auditabilidade pública.
* **O Funil Gratuito vs. Pago:** O plano gratuito restringe o usuário a poucas localidades com velocidades deliberadamente estranguladas, servindo como funil para forçar assinaturas mensais.
* **Propriedade Fechada (Closed Source):** Apesar de alegarem política rigorosa de "No-Logs" e servidores em RAM, **não há como auditar externamente o código do cliente ou dos servidores**. O usuário é forçado a confiar cegamente nas declarações de marketing da empresa.
* **SDKs de Terceiros e Monetização por Publicidade:** As versões mobile gratuitas frequentemente integram bibliotecas de analytics e redes de anúncio, que coletam identificadores de hardware (GAID/IDFA) e dados de telemetria.
* **Extensões de Navegador como Simples Proxies:** Extensões que funcionam apenas como proxies HTTP simples sem criptografia no sistema operacional e sem blindagem contra vazamento de WebRTC.

### 2.3 Matriz Comparativa Definitiva: Redes P2P vs Softwares Fechados vs FLUX VPN

| Critério Técnico | ❌ Redes P2P Gratuitas | ⚠️ Softwares Fechados Comuns | 🛡️ FLUX VPN (Nossa Solução) |
| :--- | :--- | :--- | :--- |
| **Arquitetura de Rede** | P2P / Rede Residencial (Perigoso) | Servidores Dedicados Centralizados | Nós Dedicados de Alta Velocidade + RAM-Only |
| **Uso da Conexão do Usuário** | **SIM** (Você vira Exit Node para estranhos) | Não | **NUNCA** (Usuário é puramente cliente) |
| **Código-Fonte** | 100% Fechado / Obscuro | 100% Fechado | **100% Open-Source (GPLv3 / Apache 2.0)** |
| **Auditoria & Reproducible Builds** | Inexistente | Inexistente | Totalmente Auditável + CI/CD Determinístico |
| **Protocolo de Rede** | Proxy proprietário / P2P Mesh | Protocolos proprietários fechados | **WireGuard Kernel + AmneziaWG + OpenVPN 2.6** |
| **Proteção contra DNS Leak** | Fraca / Frequentes vazamentos | Média (DNS proprietário fechado) | **Absoluta (Unbound local + DNS forçado via Firewall)** |
| **Proteção contra IPv6 Leak** | Incompleta (Frequentemente vaza) | Desativa IPv6 ou vaza | **Dual-Stack nativo com isolamento ou Blackhole total** |
| **Proteção contra WebRTC** | Nula nas extensões | Média nas extensões | **Bloqueio rígido de IP Handling Policy via MV3** |
| **Kill Switch** | Básico / Soft (falha se o app travar) | Soft Kill Switch em nível de app | **Hard Kill Switch (WFP / PF / nftables no kernel)** |
| **Monetização** | Venda de banda/IP residencial | Anúncios no app + Paywall agressivo | Financiamento Comunitário + Open Core Ético |
| **Armazenamento nos Servidores** | Desconhecido | Afirma RAM-Only (sem provas públicas) | **Diskless PXE Boot verificável (Zero disco)** |

---

## 3. ENGENHARIA DE "ZERO LEAKS" E SEGURANÇA DE NÍVEL MILITAR

Para garantir que o **FLUX VPN** jamais vaze dados do usuário sob nenhuma circunstância de rede (quedas, trocas de Wi-Fi, reconexão 4G/5G, ataques de spoofing), implementamos uma arquitetura de prevenção em 4 frentes:

```
+-----------------------------------------------------------------------------------+
|                           DISPOSITIVO DO USUÁRIO                                  |
|                                                                                   |
|  +--------------------+   +---------------------+   +--------------------------+  |
|  |  Aplicações / Web  |   | Extensão Navegador  |   | Requisições DNS / WebRTC |  |
|  +---------+----------+   +----------+----------+   +------------+-------------+  |
|            |                         |                           |                |
|            v                         v                           v                |
|  +-----------------------------------------------------------------------------+  |
|  |             FIREWALL DE KERNEL FLUX (WFP / PF / NFTABLES)                   |  |
|  |  -> Permite APENAS pacotes criptografados destinados ao IP do Servidor FLUX|  |
|  |  -> Bloqueia QUALQUER tráfego desprotegido em caso de queda do túnel (KS)   |  |
|  |  -> Roteia 100% do tráfego DNS para o Resolver Seguro do Túnel (Porta 53)  |  |
|  |  -> Aplica Blackhole/Drop imediato a todos os pacotes IPv6 desprotegidos    |  |
|  +-----------------------------------+-----------------------------------------+  |
|                                      |                                            |
|                                      v                                            |
|                  +---------------------------------------+                        |
|                  |     INTERFACE TÚNEL WIREGUARD / WINTUN|                        |
|                  +-------------------+-------------------+                        |
+--------------------------------------|--------------------------------------------+
                                       | Conexão Criptografada (ChaCha20-Poly1305)
                                       v
                     +-----------------------------------+
                     |  SERVIDOR FLUX (RAM-ONLY DISKLESS)|
                     |  - Resolver DNS Local (Unbound)   |
                     |  - WireGuard Memory Clean Daemon  |
                     |  - IP Masquerade Coletivo (NAT)   |
                     +-----------------+-----------------+
                                       |
                                       v
                               Internet Pública
```

### 3.1 Anatomia e Blindagem contra DNS Leaks
* **O Problema:** A maioria das VPNs falha quando o sistema operacional (Windows, macOS, Android) envia requisições DNS paralelas para o servidor do roteador local ou provedor de internet (ISP) via "Smart Multi-Homed Name Resolution" para acelerar respostas.
* **A Solução FLUX:**
  1. O cliente FLUX cria uma interface virtual de rede (`flux0`) e atribui o DNS do túnel (ex: `10.8.0.1`).
  2. No Windows, acionamos a API **WFP (Windows Filtering Platform)** para bloquear qualquer tráfego na porta UDP/TCP 53 que não saia pela interface `flux0`. Além disso, desativamos programaticamente o *Smart Multi-Homed Name Resolution* via Group Policy API durante a conexão.
  3. No Linux, manipulamos o `systemd-resolved` ou `/etc/resolv.conf` através de um link simbólico temporário imutável, garantindo que o resolvedor exclusivo seja o túnel.
  4. Nos servidores FLUX, cada nó roda um resolvedor **Unbound recursivo com DNSSEC** diretamente na memória RAM, sem utilizar Google DNS, Cloudflare ou ISPs. Nenhuma consulta sai descriptografada ou é logada.

### 3.2 Erradicação de Vazamentos IPv6 (Dual-Stack vs Blackholing)
* **O Problema:** Muitos servidores VPN suportam apenas IPv4. Quando o usuário acessa um site moderno com suporte a IPv6 (como Google, Netflix, Facebook), o sistema operacional contorna a VPN e envia o tráfego IPv6 pela placa de rede física local, revelando a localização e o provedor real do usuário.
* **A Solução FLUX:**
  * **Modo A (Dual-Stack):** Quando o nó de servidor possui bloco IPv6 dedicado, o túnel atribui um endereço IPv6 ULA/roteável ao cliente, criptografando ambos os fluxos no mesmo túnel WireGuard.
  * **Modo B (Deterministic Blackhole):** Em nós IPv4 puros, o cliente FLUX instala uma regra de firewall a nível de kernel que descarta (`DROP`) instantaneamente qualquer pacote de saída da família `AF_INET6` na placa de rede física, impedindo 100% de qualquer vazamento de IPv6.

### 3.3 Neutralização de WebRTC Leaks (Desktop e Navegadores)
* **O Problema:** A API WebRTC dos navegadores modernos faz chamadas STUN diretas em busca de caminhos de conexão peer-to-peer diretos, contornando proxies HTTP/SOCKS configurados no navegador e descobrindo o IP público local.
* **A Solução FLUX:**
  * No cliente desktop/mobile: O Kill Switch do firewall bloqueia qualquer pacote STUN/TURN que tente alcançar servidores STUN fora da interface virtual da VPN.
  * Nas extensões de navegador (Chrome, Edge, Firefox, Opera): A extensão utiliza a API nativa `chrome.privacy.network.webRTCIPHandlingPolicy` setada estritamente para `disable_non_proxied_udp`, forçando o navegador a nunca disparar pacotes STUN fora do túnel seguro.

### 3.4 Hard Kill Switch em Nível de Kernel
Diferente de concorrentes que usam "Soft Kill Switch" (um timer em JavaScript ou C# que monitora a conexão e, se o app travar, a internet fica aberta e desprotegida), o **FLUX VPN implementa um Hard Kill Switch**:
* **Windows:** Filtros persistentes injetados no **WFP (Windows Filtering Platform)** na camada `FWPM_LAYER_OUTBOUND_IPPACKET_V4` e `V6`. Se o processo da interface gráfica do FLUX for encerrado abruptamente ou travar, o filtro do Windows continua ativo no kernel, bloqueando todo o tráfego da placa física.
* **macOS:** Submissão de regras ao **PF (Packet Filter)** nativo do BSD/macOS e `NEFilterDataProvider`.
* **Linux:** Conjunto atômico de regras no **nftables** com chain prioritária bloqueando a interface `eth0/wlan0` para tudo exceto o handshake WireGuard na porta designada.

### 3.5 Blindagem contra Ataques em Wi-Fi Públicas & Ameaças Locais (Zero-Trust LAN)
Redes Wi-Fi abertas em aeroportos, hotéis, cafés e shoppings são os principais vetores de invasão ativa. O FLUX VPN implementa uma defesa em 5 camadas:

1. **Defesa contra Evil Twin (Rogue Hotspots) & Man-in-the-Middle (MitM):**
   * *O Ataque:* Invasores criam pontos de acesso Wi-Fi falsos com o mesmo nome do local ("Aeroporto_Free_WiFi") para interceptar credenciais.
   * *A Blindagem FLUX:* O cliente monitora as mudanças de interface de rede (`Network Reachability`). No milissegundo em que o dispositivo se conecta a uma rede desconhecida ou aberta, o **Escudo Wi-Fi ativa o túnel antes que qualquer outro processo do SO envie um único pacote**. Como a autenticação do WireGuard é baseada em chaves assimétricas **Curve25519 pré-compartilhadas**, o roteador falso não consegue interceptar, forjar certificados ou inspecionar o túnel.
2. **Neutralização de ARP Spoofing / Poisoning:**
   * *O Ataque:* Dispositivos maliciosos na mesma sub-rede enviam respostas ARP forjadas alegando ser o roteador, redirecionando o tráfego de todos os usuários para si.
   * *A Blindagem FLUX:* O firewall de kernel do FLUX descarta todo pacote de saída que não seja o datagrama UDP criptografado endereçado estritamente ao IP público do servidor FLUX. Mesmo que o invasor redirecione o fluxo para sua própria máquina, ele recebe apenas blocos ininteligíveis criptografados por **ChaCha20-Poly1305**.
3. **Invisibilidade Total de Rede Local (LAN Isolation):**
   * *O Ataque:* Hackers usam scanners (Nmap, Nessus) para explorar vulnerabilidades em compartilhamentos SMB (Porta 445), NetBIOS (Porta 137/138), mDNS (5353) ou portas abertas no computador do usuário.
   * *A Blindagem FLUX:* A regra de isolamento fecha sumariamente todas as portas de escuta locais para a placa física. Seu computador ou smartphone **desaparece completamente da rede local**. Ninguém na mesma cafeteria ou aeroporto consegue pingar, varrer ou infectar seu dispositivo.
4. **Isolamento de Portais Cativos (Hotéis e Aeroportos):**
   * Muitos locais exigem login via página web (Portal Cativo). Em vez de expor a máquina à internet enquanto o usuário faz login, o FLUX isola essa navegação temporária dentro de um sandbox restrito e, imediatamente após a autenticação, fecha a trava do túnel com Kill Switch.
5. **Criptografia Nível Zero-Trust:**
   * Todo tráfego (navegação, apps em segundo plano, chamadas de sistema, telemetria de SO) é encapsulado no túnel. Nenhuma chave criptográfica sai do dispositivo do usuário.

---

## 4. PILHA DE PROTOCOLOS E CRIPTOGRAFIA DO FLUX VPN

O FLUX VPN não reinventa a roda com algoritmos proprietários duvidosos. Utilizamos as tecnologias criptográficas mais avançadas, comprovadas e auditadas do mundo:

### 4.1 WireGuard: O Coração do FLUX VPN
* **Criptografia:**
  * Troca de chaves autenticada: **Noise Protocol Framework (Noise_IKpsk2)**.
  * Troca de chaves assimétricas: **Curve25519 (ECDH)**.
  * Criptografia simétrica autenticada: **ChaCha20-Poly1305 (AEAD)**.
  * Hashing e derivação de chaves: **BLAKE2s**.
* **Vantagens Competitivas:**
  * Base de código minúscula (~4.000 linhas vs >100.000 do OpenVPN), tornando-o imune a falhas complexas de buffer overflow e 100% auditável.
  * Velocidades até 4x a 6x superiores ao OpenVPN tradicional com consumo de bateria extremamente reduzido em smartphones.
  * Troca de redes sem interrupção (Roaming instantâneo de Wi-Fi para 4G/5G sem queda de sessão).

### 4.2 Camada Ofuscada Anti-DPI (AmneziaWG / VLESS Reality)
Para usuários em redes corporativas, universidades, escolas ou países com Deep Packet Inspection (DPI) e censura agressiva (onde handshakes padrão do WireGuard ou OpenVPN são bloqueados):
* **AmneziaWG (WireGuard com Ofuscação de Handshake):** Adição de bytes de padding aleatórios e cabeçalhos randômicos nos pacotes `Initiation` e `Response`, transformando o tráfego do túnel em ruído indistinguível de streams HTTPS comuns.
* **VLESS + Reality (Fallback de Máxima Furtividade):** Camada de transporte baseada em TLS que mascara o túnel como se fosse uma conexão segura com sites de altíssima reputação (ex: `dl.google.com` ou `apple.com`), tornando o bloqueio por DPI quase impossível sem quebrar o acesso à web legítima.

### 4.3 OpenVPN 2.6 Otimizado (Legado e Roteadores)
* Para roteadores com chips mais antigos e dispositivos sem suporte a módulos modernos do kernel:
  * Suporte a perfis `.ovpn` com cifra **AES-256-GCM**, autenticação **SHA-512** e troca de chaves **ECDH com curva secp384r1** via TLS 1.3.

---

## 5. ESTRATÉGIA MULTIPLATAFORMA (13 ECOSSISTEMAS ALVO)

O FLUX VPN é disponibilizado de forma universal e unificada em todas as plataformas e ecossistemas modernos.

```
                                +---------------------------+
                                |    FLUX CORE ENGINE       |
                                |  (Escrito em Rust / Go)   |
                                |  - Criptografia WireGuard |
                                |  - Gerenciador de Chaves  |
                                |  - Roteamento e Handshake |
                                +-------------+-------------+
                                              |
      +-------------------+-------------------+-------------------+-------------------+
      |                   |                   |                   |                   |
      v                   v                   v                   v                   v
+------------+     +------------+      +------------+      +------------+      +------------+
|  WINDOWS   |     |   macOS    |      |   LINUX    |      |  ANDROID   |      |    iOS     |
| C# / Tauri |     |  SwiftUI   |      | Rust / GTK |      |   Kotlin   |      |   Swift    |
|   WinTun   |     | NetworkExt |      |  nftables  |      | VpnService |      | NetworkExt |
+------------+     +------------+      +------------+      +------------+      +------------+
      |                   |                   |                   |                   |
      +-------------------+-------------------+-------------------+-------------------+
                                              |
      +-------------------+-------------------+-------------------+-------------------+
      |                   |                   |                   |                   |
      v                   v                   v                   v                   v
+------------+     +------------+      +------------+      +------------+      +------------+
| ANDROID TV |     | HUAWEI HMS |      | EXTENSÕES  |      | ROTEADORES |      | PERFIS WG  |
|  Leanback  |     |   Sem GMS  |      | Chrome/Edge|      |  OpenWrt   |      |  & OpenVPN |
|   D-Pad    |     |  AppGall.  |      | Firefox/Op.|      |  pfSense   |      |  Configs   |
+------------+     +------------+      +------------+      +------------+      +------------+
```

### 5.1 Windows
* **Stack Tecnológico:** C# (.NET 8 com WinUI 3) ou Rust + Tauri para máxima leveza e baixo consumo de RAM.
* **Driver de Rede:** **WinTun** (desenvolvido pela equipe oficial do WireGuard, operando em Ring 0 com throughput superior a 5 Gbps).
* **Kill Switch:** Windows Filtering Platform (WFP) nativo em C++ integrado via DLL segura.

### 5.2 macOS
* **Stack Tecnológico:** Swift nativo com interface SwiftUI elegante, suporte a modo escuro/claro e Apple Silicon (M1/M2/M3/M4) + Intel.
* **Driver de Rede:** `NEPacketTunnelProvider` da Apple NetworkExtension API.
* **Segurança:** Isolamento total através do Keychain nativo do macOS para proteção de chaves privadas do WireGuard e proteção PF Firewall.

### 5.3 Linux
* **Stack Tecnológico:** Daemon `fluxd` escrito em Rust com controle via linha de comando (`flux-cli`) e interface gráfica opcional em Tauri/GTK4.
* **Roteamento:** Integração direta com `wg-quick` e o módulo `wireguard.ko` do kernel Linux.
* **Pacotes:** `.deb` (Debian/Ubuntu), `.rpm` (Fedora/RHEL), AUR (Arch Linux), Flatpak e AppImage universais.

### 5.4 Android & Android TV
* **Stack Tecnológico:** Kotlin com Jetpack Compose moderno.
* **Integração:** `VpnService` oficial do Android com ativação da flag `Always-on VPN` e bloqueio de conexões fora da VPN pelo sistema.
* **Android TV:** Interface dedicada compatível com especificações Android TV Leanback, totalmente navegável através do controle remoto (D-Pad), conexão em 1 clique e seleção rápida de servidores em tela cheia.

### 5.5 iOS
* **Stack Tecnológico:** Swift com SwiftUI, compatível com iOS 16+.
* **Túnel:** Implementação através do framework `NetworkExtension` com chave privada armazenada de forma impenetrável no **Apple Secure Enclave**.
* **Funcionalidade:** Conexão "On Demand" automática ao ingressar em redes Wi-Fi desconhecidas ou desprotegidas.

### 5.6 Huawei (HarmonyOS / EMUI)
* **Build Flavor Independente:** Uma compilação dedicada sem dependências da biblioteca Google Play Services, utilizando APIs puras do Android Open Source Project (AOSP) e compatível com **Huawei AppGallery** e catálogo aberto **F-Droid**.

### 5.7 Extensões de Navegador (Chrome, Firefox, Opera, Edge)
* **Arquitetura Manifest V3:**
  * Uso da API `chrome.proxy` configurando um túnel HTTPS/SOCKS5 sobre WebSockets TLS autenticado com os nós de borda do FLUX.
  * Injeção automática das regras de isolamento de WebRTC via `privacy.network.webRTCIPHandlingPolicy`.
  * Filtro de anúncios e rastreadores DNS integrado via `declarativeNetRequest` (bloqueio de banners, trackers de telemetria e malwares conhecidos).
  * Código único compatível com todos os navegadores baseados em Chromium e adaptação direta para a API `browser.proxy` do Mozilla Firefox.

### 5.8 Roteadores e Perfis Universais
* **Gerador de Configurações 1-Click:** Painel web e no app onde o usuário gera arquivos `.conf` (WireGuard) e `.ovpn` (OpenVPN).
* **Suporte a Roteadores:**
  * **OpenWrt:** Script de instalação automatizada (`opkg install flux-vpn`).
  * **pfSense & OPNsense:** Guia e perfis de túnel com Gateway Failover e regras de Outbound NAT configuradas.
  * **DD-WRT e Asus-Merlin:** Scripts nativos para cliente WireGuard/OpenVPN embutido.

---

## 6. INFRAESTRUTURA DE SERVIDORES 100% EM RAM (RAM-ONLY DISKLESS)

Enquanto soluções proprietárias de código fechado alegam política de "No-Logs" sem possibilidade de verificação, o FLUX VPN adota uma infraestrutura arquiteturalmente incapaz de armazenar dados persistentes:

```
+-----------------------------------------------------------------------------------+
|               SERVIDOR FLUX VPN EM RAM PURA (DISKLESS PXE BOOT)                   |
|                                                                                   |
|  [Hardware Físico / Bare-Metal]                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Memória RAM (Tmpfs)                                                         |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | Kernel Linux Otimizado (Alpine Minimal / Debian Tmpfs)                |  |  |
|  |  |                                                                       |  |  |
|  |  |   [Módulo WireGuard Kernel] <---> [Daemon de Limpeza de IPs Ativos]   |  |  |
|  |  |                                                                       |  |  |
|  |  |   [Unbound DNS Resolver Local]  <- Sem logs / Somente Cache em RAM    |  |  |
|  |  |                                                                       |  |  |
|  |  |   [journald / syslog DESATIVADOS] -> /dev/null                         |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
|  [DISCO RÍGIDO / SSD]: INEXISTENTE OU DESMONTADO (Zero escrita em mídia física)   |
|                                                                                   |
|  * Se o servidor for desligado, desplugado ou apreendido:                         |
|    -> Toda e qualquer chave e sessão se desintegra instantaneamente da RAM        |
+-----------------------------------------------------------------------------------+
```

### 6.1 Boot PXE / Tmpfs e Aniquilação de Logs
* O sistema operacional base é inicializado remotamente via rede (iPXE) carregando uma imagem criptografada do Alpine Linux diretamente na memória volátil (`tmpfs`).
* **Desativação Total de Logs:**
  * Parâmetros de kernel: `systemd.journald.forward_to_syslog=0` e `Storage=none`.
  * Todos os logs de serviços em `/var/log` são direcionados para `/dev/null`.
* Nenhuma consulta, timestamp, IP de origem ou volume de tráfego é gravado em disco. Se um servidor for confiscado judicialmente ou desconectado da tomada, ele é apenas um pedaço de metal inerte sem dados recuperáveis.

### 6.2 Mitigação da Tabela de Memória do WireGuard (IP Handshake Flush)
* **Atenção a este detalhe crítico:** Por design, o WireGuard mantém em memória o último endereço IP público e porta de handshake do cliente para possibilitar a entrega dos pacotes de retorno.
* **A Inovação do FLUX VPN:** Implementamos um daemon leve em Rust (`flux-wg-scrubber`) rodando no servidor que monitora a inatividade do cliente. Imediatamente após 180 segundos sem troca de pacotes (ou no evento de desconexão explícita enviada pelo cliente), o IP do peer é removido da tabela de peers do WireGuard via chamada netlink `wg set <interface> peer <pubkey> remove`, eliminando qualquer rastreio de qual IP físico estava associado àquela sessão.

### 6.3 Egress NAT e Anonymity Pool
* Centenas de conexões simultâneas de usuários em um mesmo servidor FLUX são mapeadas através de regras `iptables MASQUERADE` para um pool compartilhado de IPs de saída do data center.
* Desta forma, o tráfego de um usuário se mistura com o tráfego de centenas de outros no mesmo milissegundo, tornando a correlação estatística de tráfego externamente impraticável.

### 6.4 Jurisdições Estratégicas Fora dos 14 Eyes
Os nós centrais de coordenação e primeiros servidores de saída serão alocados em jurisdições com legislação rigorosa de proteção à privacidade e fora de tratados de espionagem em massa (Five Eyes / Nine Eyes / Fourteen Eyes):
* **Suíça:** Legislação estrita de privacidade (DPA / FADP), sem obrigação de retenção de logs para serviços VPN.
* **Islândia:** Pioneira em proteção de direitos digitais e liberdade de expressão.
* **Romênia:** Jurisdição com histórico consolidado contra leis de retenção arbitrária e vigilância da UE.
* **Panamá:** Fora de qualquer pacto internacional de vigilância de dados.

---

## 7. ARQUITETURA DE SOFTWARE DO REPOSITÓRIO (MONOREPO FLUX)

Para manter o projeto fácil de auditar, compilar e gerenciar pela comunidade open-source, estruturamos o repositório como um Monorepo limpo e modular:

```
FLUXVPN/
├── .github/
│   ├── workflows/             # Pipelines CI/CD com Reproducible Builds
│   │   ├── build-windows.yml
│   │   ├── build-macos.yml
│   │   ├── build-linux.yml
│   │   ├── build-android.yml
│   │   ├── build-ios.yml
│   │   └── build-extensions.yml
├── core/                       # Biblioteca base em Rust (compartilhada via C-FFI)
│   ├── Cargo.toml
│   ├── src/
│   │   ├── crypto/            # Wrappers de WireGuard, ChaCha20, Noise
│   │   ├── tunnel/            # Lógica de interface TUN e socketing
│   │   ├── dns/               # Forçador e verificador de vazamento de DNS
│   │   └── killswitch/        # Implementações nativas de firewall
├── clients/
│   ├── desktop/
│   │   ├── windows/           # Interface C# / WPF + WinTun bindings
│   │   ├── macos/             # App nativo Swift + SwiftUI
│   │   └── linux/             # CLI Rust (`flux-cli`) + GUI Tauri/GTK
│   ├── mobile/
│   │   ├── android/           # Kotlin (Phone, Tablet, Huawei Flavor)
│   │   ├── android-tv/        # UI Leanback com controle D-Pad
│   │   └── ios/               # Swift (iPhone, iPad) + NetworkExtension
│   ├── extensions/            # WebExtensions Manifest V3 (Chrome, Edge, Opera, Firefox)
│   │   ├── src/
│   │   │   ├── background.ts  # Gerenciador de proxy e isolamento WebRTC
│   │   │   ├── popup/         # Interface gráfica do usuário da extensão
│   │   │   └── rules/         # Listas declarativas anti-ad e anti-tracker
│   │   └── manifest.json
│   └── routers/               # Scripts para OpenWrt, pfSense, DD-WRT
├── server/                     # Infraestrutura de Servidor
│   ├── pxe-image/             # Imagem Alpine Linux Diskless RAM-Only
│   ├── docker/                # Containers de desenvolvimento local
│   ├── unbound/               # Configurações do resolver DNS isolado
│   └── scripts/
│       ├── wg-scrubber.rs     # Daemon que limpa IPs de handshake da RAM
│       └── iptables-rules.sh  # Regras de NAT, isolamento e mitigação DDoS
├── docs/                      # Documentação de segurança, auditoria e guias
├── LICENSE                    # GNU General Public License v3.0 (GPLv3)
└── README.md
```

---

## 8. MODELO DE SUSTENTABILIDADE ÉTICO E GOVERNANÇA

O maior erro de VPNs ditas "gratuitas" comerciais é recorrer à venda de telemetria ou ao sequestro de banda e IPs residenciais de usuários. Para que o FLUX VPN seja viável a longo prazo mantendo a ética absoluta:

1. **Camada Gratuita Comunitária (Community Free Tier):**
   * Nós básicos de alta qualidade mantidos por patrocinadores e doadores (fundos de liberdade na internet, doações comunitárias via Open Collective e GitHub Sponsors).
   * Sem anúncios intrusivos, sem rastreadores, sem limites artificiais de privacidade (o nível de criptografia e proteção contra vazamento é 100% o mesmo para todos).
2. **Camada Pro / Supporter Opcional (Para Cobrir Servidores 10Gbps):**
   * Acesso a nós dedicados de altíssima velocidade otimizados para streaming 4K, rotas de baixa latência para games e nós com Double-VPN (Multi-hop).
   * Pagamento totalmente anônimo: Aceite de **Monero (XMR)** e Bitcoin via **BTCPay Server** auto-hospedado (sem processadores terceiros ou KYC), além de cartão tradicional para quem preferir conveniência.
3. **Auditoria Aberta e Programa de Bug Bounty:**
   * Recompensas para pesquisadores de segurança que reportarem qualquer falha ou potencial vetor de vazamento.

---

## 9. ROADMAP DE EXECUÇÃO PASSO A PASSO (FASES 1 A 6)

```
FASE 1: Fundação & Núcleo (Core Engine em Rust + Servidor RAM-Only de Referência)
   │
   ├── [Semana 1-2] Desenvolvimento do `flux-core` (Rust): WireGuard FFI, WinTun e Kill Switch
   ├── [Semana 2-3] Montagem do ambiente de Servidor PXE/Diskless RAM-Only (Docker/Alpine)
   └── [Semana 3-4] Bateria de testes de estresse contra DNS, IPv6 e WebRTC leaks
   │
FASE 2: Clientes Desktop (Windows, macOS, Linux)
   │
   ├── [Semana 5-6] Cliente Windows nativo com WinTun e WFP Hard Kill Switch
   ├── [Semana 6-7] Cliente macOS nativo em SwiftUI com NetworkExtension
   └── [Semana 7-8] Daemon Linux `fluxd` + CLI + GUI universal em Tauri
   │
FASE 3: Extensões de Navegador (Chrome, Firefox, Opera, Edge)
   │
   ├── [Semana 9-10] Implementação da extensão Manifest V3 com WebRTC Hard Block
   └── [Semana 10] Homologação e submissão na Chrome Web Store, Firefox Add-ons e Edge Add-ons
   │
FASE 4: Mobile & TV (Android, iOS, Android TV, Huawei)
   │
   ├── [Semana 11-12] App Android nativo (Kotlin) com suporte Always-on VPN
   ├── [Semana 12-13] Adaptação para interface Android TV (Leanback + D-Pad)
   ├── [Semana 13] Build independente Huawei HMS para AppGallery e F-Droid
   └── [Semana 14-15] App iOS nativo em Swift com integração Apple Secure Enclave
   │
FASE 5: Roteadores, Perfis Manuais e Portal Web
   │
   ├── [Semana 16] Gerador de perfis WireGuard (.conf) e OpenVPN (.ovpn) no site
   └── [Semana 17] Scripts homologados para OpenWrt, pfSense e DD-WRT
   │
FASE 6: Auditoria de Segurança, Lançamento Público e Governança Open-Source
   │
   ├── [Semana 18] Execução de auditoria independente e publicação dos relatórios
   └── [Semana 19-20] Publicação do Monorepo no GitHub e liberação dos binários
```

---

## 🏁 CONCLUSÃO & PRÓXIMOS PASSOS IMEDIATOS

Com este plano mestre em mãos, possuímos a fórmula técnica exata para estabelecer o novo padrão ouro de segurança e privacidade em todas as frentes:
* Enquanto serviços P2P residenciais comprometem o usuário transformando sua máquina em nó de tráfego de terceiros, o **FLUX VPN** protege a máquina do usuário com um cofre criptográfico impenetrável.
* Enquanto VPNs comerciais operam sob código fechado e táticas comerciais agressivas, o **FLUX VPN** entrega total auditabilidade, builds reproduzíveis e transparência em nível de hardware.

**O projeto está pronto para iniciar a fase de implementação imediata.**
