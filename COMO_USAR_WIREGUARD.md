# ⚡ Como Usar o FLUX VPN com o WireGuard® Oficial (Conexão 100% Real)

> **O Método Definitivo de Alta Performance e Zero Vazamentos**  
> O WireGuard® é o protocolo de VPN de código aberto mais moderno, auditado e veloz do mundo. Ele roda diretamente dentro do **Kernel do Sistema Operacional** (através do driver de alto rendimento **Wintun** no Windows e do framework nativo **utun/NetworkExtension** no macOS e iOS).

---

## 🚀 Por que este método é 100% Real e Superior?

1. **Roteamento Total do Computador:** Não é uma simulação nem apenas um proxy de navegador. Todos os navegadores, jogos (Steam, Riot, Epic), chamadas Discord/Zoom e downloads torrent passam criptografados pelo túnel.
2. **Criptografia Militar Nativa:** Utiliza **Curve25519** para troca de chaves e **ChaCha20-Poly1305** para autenticação e cifra de pacotes.
3. **Zero Avisos de Segurança / Zero Quarentena:** O cliente WireGuard é **assinado oficialmente pela Microsoft e pela Apple**, instalando com 1 clique sem nenhum bloqueio de SmartScreen ou Gatekeeper (`xattr -cr`).
4. **Sem Bateria Gasta:** O WireGuard foi desenhado para economizar até 80% mais bateria do que protocolos legados (como OpenVPN).

---

## ⬇️ 1. Onde Baixar o Cliente Oficial do WireGuard

O aplicativo do WireGuard é **gratuito e livre de anúncios**. Baixe diretamente dos canais oficiais:

| Sistema Operacional | Onde Baixar | Observação |
| :--- | :--- | :--- |
| **🪟 Windows (10 e 11)** | **[Baixar Instalador Oficial (.msi)](https://download.wireguard.com/windows-client/wireguard-installer.exe)** | Instalador direto com certificado digital da Microsoft |
| **🍏 macOS (Apple Silicon / Intel)** | **[Baixar na Mac App Store](https://apps.apple.com/app/wireguard/id1451685025)** | Instalação em 1 clique pela loja oficial da Apple |
| **📱 iPhone & iPad (iOS)** | **[Baixar na App Store](https://apps.apple.com/app/wireguard/id1441195209)** | Suporte a leitura de QR Code direto pela câmera |
| **🤖 Android & TV** | **[Baixar no Google Play](https://play.google.com/store/apps/details?id=com.wireguard.android)** | Ou via F-Droid Open Source |

---

## ⚙️ 2. Como Conectar em Menos de 30 Segundos

### No Windows:
1. Abra o aplicativo **WireGuard**.
2. Clique no botão **"Import tunnel(s) from file"** (ou pressione `Ctrl + O`).
3. Selecione qualquer arquivo `.conf` da pasta `profiles/` do FLUX VPN (exemplo: `FLUX-Brasil-SaoPaulo.conf`).
4. Clique no botão **"Activate"** (Ativar).
5. **Pronto!** O ícone do WireGuard ficará verde na barra de tarefas e seu IP estará 100% mascarado e seguro.

### No Mac (macOS):
1. Abra o aplicativo **WireGuard** baixado da App Store.
2. Clique em **"Import tunnel(s) from file"** (ou arraste o arquivo `.conf` para dentro do app).
3. Na primeira vez, o macOS perguntará se você permite adicionar configurações de VPN ("Allow"). Clique em **Permitir**.
4. Clique em **"Activate"**.
5. Conexão estabelecida com proteção ativa contra vazamentos.

### No Celular (iPhone / Android):
1. Abra o simulador do FLUX VPN no seu computador (`index.html`) e clique em **"Exportar Perfil WireGuard (.conf)"**.
2. Clique na aba **"QR Code"**.
3. Abra o app **WireGuard** no seu celular, toque no botão `+` e selecione **"Scan from QR code"**.
4. Aponte a câmera para a tela do seu computador.
5. Dê um nome (ex: `FLUX Brasil`) e toque em **Ativar**. Conectado instantaneamente!

---

## 🌐 3. Perfis Pré-Configurados Disponíveis no Repositório

Você encontra os arquivos prontos para importar na pasta [`profiles/`](profiles/):

- [`FLUX-Brasil-SaoPaulo.conf`](profiles/FLUX-Brasil-SaoPaulo.conf) — Nó de baixa latência em São Paulo
- [`FLUX-Alemanha-Frankfurt.conf`](profiles/FLUX-Alemanha-Frankfurt.conf) — Nó central europeu com altíssima banda
- [`FLUX-EUA-NovaYork.conf`](profiles/FLUX-EUA-NovaYork.conf) — Otimizado para streaming e catálogos americanos
- [`FLUX-Suica-Zurique.conf`](profiles/FLUX-Suica-Zurique.conf) — Proteção jurídica sob legislação de privacidade suíça
- [`FLUX-Islandia-Reykjavik.conf`](profiles/FLUX-Islandia-Reykjavik.conf) — Fora das jurisdições de vigilância dos 14 Eyes
- [`FLUX-Japao-Toquio.conf`](profiles/FLUX-Japao-Toquio.conf) — Rota asiática de altíssima velocidade

---

## 🧪 4. Como Conferir se Está Funcionando

Após clicar em **Activate** no WireGuard:
1. Abra seu navegador e acesse qualquer verificador de IP público:
   - `https://api.ipify.org`
   - `https://dnsleaktest.com`
2. Você verá que o seu IP mudou para o IP do nó do FLUX VPN e seu provedor local foi completamente ocultado.
