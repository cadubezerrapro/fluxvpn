# 🛡️ FLUX VPN — Guia de Conexão em Nível de Kernel (Protocolo WireGuard®)

> **Segurança Militar, Zero Logs e Roteamento de Sistema Completo**  
> O FLUX VPN foi construído nativamente sobre o protocolo de rede mais moderno e seguro do mundo: o **WireGuard®**.  
> Esta arquitetura garante conexões ultrarrápidas, criptografia **Curve25519 / ChaCha20-Poly1305** e roteamento integral diretamente no **Kernel do Sistema Operacional** (drivers de alto rendimento Wintun no Windows e NetworkExtension no macOS/iOS).

---

## ⚡ Como Funciona a Arquitetura do FLUX VPN?

O FLUX VPN oferece proteção em duas camadas complementares:

1. **🌐 Camada de Navegador (Extensão Manifest V3 para Chrome, Edge, Brave e Opera):**
   - Conexão em 1 clique direto no navegador.
   - Bloqueio rígido de vazamentos de IP por WebRTC (*WebRTC Non-Proxied UDP Shield*).
   - Ideal para navegação diária com zero atrito e sem necessidade de permissões de sistema.

2. **💻 Camada de Sistema Operacional (Engine de Kernel WireGuard®):**
   - Roteia **100% do tráfego de toda a máquina** (todos os navegadores, jogos como Steam/Epic, chamadas Discord/Zoom e programas em segundo plano).
   - Opera através da engine de rede oficial assinada digitalmente pela **Microsoft** e pela **Apple**, garantindo **zero alertas de quarentena no Mac** e **zero falsos positivos de SmartScreen no Windows**.
   - Integração com smartphones (iPhone e Android) via leitura de QR Code gerado pelo FLUX VPN.

---

## 🚀 Como Ativar o Modo Kernel no seu Computador

O FLUX VPN gera e fornece as chaves criptográficas e os perfis prontos para você ativar o túnel em menos de 30 segundos:

### 🪟 No Windows (10 e 11):
1. Instale o driver oficial do WireGuard: **[Download do Instalador Assinado pela Microsoft (.msi)](https://download.wireguard.com/windows-client/wireguard-installer.exe)**.
2. Abra o WireGuard e clique em **"Import tunnel(s) from file"** (ou aperte `Ctrl + O`).
3. Selecione o perfil desejado na pasta `profiles/` do FLUX VPN (ex: `FLUX-Brasil-SaoPaulo.conf`).
4. Clique em **"Activate"**.
5. **Pronto!** Todo o seu computador estará operando sob o túnel criptografado do FLUX VPN.

### 🍏 No Mac (macOS):
1. Instale o cliente com suporte a NetworkExtension da Apple: **[Baixar na Mac App Store Oficial](https://apps.apple.com/app/wireguard/id1451685025)**.
2. Abra o aplicativo e clique em **"Import tunnel(s) from file"** (ou arraste o arquivo da pasta `profiles/` para o app).
3. Na primeira execução, autorize a extensão de rede do macOS clicando em **Permitir (Allow)**.
4. Clique em **"Activate"**.
5. Proteção de sistema estabelecida com tráfego 100% criptografado.

### 📱 No Celular (iPhone / iPad / Android):
1. No FLUX VPN (`index.html`), clique em **"Exportar Perfil WireGuard (.conf)"** e vá para a aba **"QR Code"**.
2. Baixe o WireGuard gratuito no celular (**[App Store iOS](https://apps.apple.com/app/wireguard/id1441195209)** ou **[Google Play Android](https://play.google.com/store/apps/details?id=com.wireguard.android)**).
3. Toque no botão `+`, escolha **"Scan from QR code"** e aponte a câmera para a tela do seu computador.
4. Toque em **Ativar**. O túnel do FLUX VPN estará ativo no seu smartphone!

---

## 🌐 Perfis Pré-Configurados Inclusos no FLUX VPN

Você encontra as configurações criptográficas prontas na pasta [`profiles/`](profiles/):

- 🇧🇷 [`FLUX-Brasil-SaoPaulo.conf`](profiles/FLUX-Brasil-SaoPaulo.conf) — Baixa latência e streaming nacional
- 🇩🇪 [`FLUX-Alemanha-Frankfurt.conf`](profiles/FLUX-Alemanha-Frankfurt.conf) — Hub central de alta velocidade na Europa
- 🇺🇸 [`FLUX-EUA-NovaYork.conf`](profiles/FLUX-EUA-NovaYork.conf) — Desbloqueio de catálogos e servidores norte-americanos
- 🇨🇭 [`FLUX-Suica-Zurique.conf`](profiles/FLUX-Suica-Zurique.conf) — Máxima soberania jurídica sob leis de privacidade suíças
- 🇮🇸 [`FLUX-Islandia-Reykjavik.conf`](profiles/FLUX-Islandia-Reykjavik.conf) — Fora das jurisdições de vigilância internacional (14 Eyes)
- 🇯🇵 [`FLUX-Japao-Toquio.conf`](profiles/FLUX-Japao-Toquio.conf) — Baixo jitter e alta velocidade na Ásia

---

## 🧪 Como Validar a Conexão

Após ativar a conexão:
1. Abra seu navegador e acesse:
   - `https://api.ipify.org` ou `https://dnsleaktest.com`
2. Você confirmará que o seu IP foi substituído pelo IP do nó do FLUX VPN e seu provedor local está oculto.
