# 🤖 FLUX VPN — Guia Universal para Agentes de IA e Desenvolvedores

> **Arquivo de Instruções de Execução Automatizada (`AGENTS.md`)**  
> Este documento é formatado especificamente para que qualquer Agente de IA (Claude, Cursor, Copilot, ChatGPT, Devin, Antigravity, etc.) ou desenvolvedor compreenda a arquitetura, faça o download, execute e valide o **FLUX VPN** de forma autônoma e imediata.

---

## ⬇️ 1. Onde Baixar pelo GitHub

| Método | Link / Comando | Descrição |
| :--- | :--- | :--- |
| **Download Direto (.ZIP)** | **[Baixar ZIP da Branch Main](https://github.com/cadubezerrapro/fluxvpn/archive/refs/heads/main.zip)** | Pacote completo pronto para descompactar e usar imediatamente sem Git |
| **Repositório Oficial** | `https://github.com/cadubezerrapro/fluxvpn` | Página principal do projeto no GitHub |
| **Git Clone (Terminal)** | `git clone https://github.com/cadubezerrapro/fluxvpn.git` | Clona o código fonte completo com histórico |

---

## ⚡ 2. Como Executar e Testar (Zero Instalação / Sem Dependências)

O projeto foi intencionalmente construído com **Zero Dependências Pesadas** (Pure HTML5, CSS3 moderno, Vanilla JavaScript ES6+ e WebExtensions Manifest V3). Não é necessário executar `npm install` nem compilar bundles para rodar.

### Comando Rápido em 1 Linha para IAs e Terminais:
```bash
git clone https://github.com/cadubezerrapro/fluxvpn.git && cd fluxvpn && open landing.html
```

### 3 Modos de Execução:

#### A. Landing Page Institucional
- **Arquivo principal:** `landing.html`
- **Como abrir:** Duplo clique no arquivo `landing.html` ou execute no terminal:
  ```bash
  open landing.html          # macOS
  xdg-open landing.html      # Linux
  start landing.html         # Windows
  ```
- **Ou via servidor HTTP local (Recomendado para IAs):**
  ```bash
  python3 -m http.server 8080 --directory .
  # Acesse: http://localhost:8080/landing.html
  ```

#### B. Simulador Operacional Interativo (Desktop + Mobile)
- **Arquivo principal:** `index.html`
- **Recursos para testar:** Alternância de nós mundiais (São Paulo, Frankfurt, Reykjavík, Tóquio, etc.), medidor de ping, gráfico de tráfego em tempo real, ativação do Kill Switch.

#### C. Extensão para Navegador Google Chrome / Brave / Edge / Opera
- **Diretório da extensão:** `clients/extensions/`
- **Passo a passo no navegador:**
  1. Abra o navegador e vá para `chrome://extensions/`
  2. Ative o botão **"Modo do desenvolvedor"** (canto superior direito).
  3. Clique no botão **"Carregar sem compactação"** (canto superior esquerdo).
  4. Selecione a pasta `clients/extensions/` do repositório.
- **Execução automatizada para Agentes de Teste / Selenium / Puppeteer:**
  ```bash
  google-chrome --load-extension=$(pwd)/clients/extensions http://localhost:8080/landing.html
  ```

---

## 🗺️ 3. Mapa de Arquivos do Repositório

```
FLUXVPN/
├── Iniciar FLUX VPN (macOS).command   # Executável de 1 clique para Mac (modo standalone)
├── Iniciar FLUX VPN (Windows).bat     # Executável de 1 clique para Windows (modo standalone)
├── FLUX-VPN.app/                      # Pacote de aplicativo nativo macOS
├── dist/                              # Pacotes isolados para download direto
│   ├── macOS/                         # Binário isolado para Mac (+ perfis WireGuard)
│   └── windows/                       # Executável isolado para Windows (+ perfis WireGuard)
├── profiles/                          # Perfis WireGuard® (.conf) pré-gerados para importação direta
│   ├── FLUX-Brasil-SaoPaulo.conf
│   ├── FLUX-Alemanha-Frankfurt.conf
│   ├── FLUX-EUA-NovaYork.conf
│   ├── FLUX-Suica-Zurique.conf
│   ├── FLUX-Islandia-Reykjavik.conf
│   └── FLUX-Japao-Toquio.conf
├── COMO_USAR_WIREGUARD.md             # Guia passo a passo de conexão 100% real de sistema (Kernel)
├── AGENTS.md                          # Este guia universal de automação para IAs
├── README.md                          # Apresentação do projeto e badges do GitHub
├── PLANO_MESTRE_FLUX_VPN.md           # Especificação técnica completa de arquitetura e infraestrutura
├── DESIGN_SYSTEM.md                   # Tokens de design, paleta visual e tipografia
├── LICENSE                            # Licença Open-Source GNU General Public License v3.0 (GPLv3)
├── landing.html                       # Landing page institucional com simulador embutido
├── landing.css                        # Estilização moderna da landing page (Dark mode, glassmorphism)
├── landing.js                         # Lógica de animações, modais, FAQ e download
├── index.html                         # Interface oficial do FLUX VPN (iPhone + macOS)
├── style.css                          # Estilização do aplicativo FLUX VPN
├── app.js                             # Motor reativo do aplicativo (WireGuard state, ping, kill switch)
└── clients/
    └── extensions/                    # Extensão WebExtensions Manifest V3
        ├── manifest.json              # Configuração da extensão (permissões mínimas)
        ├── background.js              # Service worker e bloqueador de WebRTC Leaks
        ├── popup.html                 # Interface compacta da extensão
        ├── popup.css                  # Estilos do popup
        └── popup.js                   # Lógica de conexão rápida da extensão
```

---

## 🛡️ 4. Regras e Invariantes do Projeto

1. **Zero Nomes de Concorrentes:** Nunca incluir nomes de marcas proprietárias ou concorrentes em commits, documentações ou landing pages. Use terminologia técnica ("redes P2P residenciais de terceiros", "aplicativos comerciais de código fechado").
2. **Zero Logs Garantido:** Toda a arquitetura foi desenhada para rodar em RAM volátil (PXE Diskless), sem gravação em disco físico.
3. **Usuário é Sempre Cliente Protegido:** O FLUX VPN **nunca** transforma o usuário em nó de saída (Exit Node).
4. **Sem Dependências Desnecessárias:** A interface e extensão devem permanecer limpas, leves e rápidas, sem frameworks monolíticos que comprometam a auditabilidade do código.

---

## 🧪 5. Comandos de Verificação Rápida para IAs

```bash
# 1. Verificar integridade dos arquivos:
ls -la landing.html index.html clients/extensions/manifest.json

# 2. Verificar ausência de erros de sintaxe nos scripts JS:
node -c app.js
node -c landing.js
node -c clients/extensions/popup.js
node -c clients/extensions/background.js

# 3. Testar se o servidor local responde com código 200:
python3 -m http.server 8080 &
PID=$!
sleep 1
curl -I http://localhost:8080/landing.html
kill $PID
```
