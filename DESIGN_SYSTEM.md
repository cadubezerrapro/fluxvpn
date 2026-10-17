# 🎨 FLUX VPN — DESIGN SYSTEM & DIRETRIZES DE UI/UX CLEAN
**Padrão Visual Humano, Minimalista e Profissional (Sem "Cara de IA")**

---

## 🎯 1. Filosofia de Design: "Clean, Utilitário e Seguro"

Inspirado nos mais altos padrões da indústria moderna de software e nas Apple Human Interface Guidelines, o **FLUX VPN** adota uma identidade visual pautada por:

* **Superfícies Claras e Arejadas:** Fundo suave off-white (`#F8FAFC` e `#FFFFFF`), evitando poluição visual, temas espalhafatosos ou elementos sci-fi futuristas exagerados que transmitem amadorismo.
* **Tipografia Moderna e Legível:** Família tipográfica *Plus Jakarta Sans* para títulos e controles (usada por grandes fintechs e produtos SaaS) e *JetBrains Mono* para exibição de endereços IP e portas criptográficas.
* **Hierarquia Clara em 3 Níveis:**
  1. **Nível 1 (Status Imediato):** O usuário deve saber em menos de 1 segundo se está protegido (Escudo ciano/verde ativo, status "Protegido", timer em execução).
  2. **Nível 2 (Ação Primária Única):** Botão principal de conexão em destaque (verde esmeralda ou ciano suave para conectar, vermelho coral suave para desconectar).
  3. **Nível 3 (Navegação & Servidores):** Barra lateral direita ou gaveta inferior com busca rápida de países, bandeiras nítidas e indicadores de latência em barrinhas de sinal.

---

## 🎨 2. Paleta de Cores Oficial

```
+-------------------+--------------------+-------------------------------------------+
| Cor               | Hexadecimal        | Aplicação no FLUX VPN                     |
+-------------------+--------------------+-------------------------------------------+
| Primary Cyan      | #0284C7            | Destaques principais, escudo conectado, abas|
| Cyan Light        | #E0F2FE            | Fundo de badges de status e chips ativos  |
| Clean White       | #FFFFFF            | Superfície das janelas, cards e modais    |
| Soft Slate Gray   | #F1F5F9            | Fundo geral da aplicação / tela de fundo  |
| Border Light      | #E2E8F0            | Bordas finas de separação de 1px           |
| Text Dark         | #0F172A            | Títulos, números do timer e nomes de país |
| Text Muted        | #64748B            | Legendas, latência e informações de nó    |
| Emerald Green     | #10B981            | Ponto indicador de "Protegido" / Kill Sw. |
| Coral Red         | #EF4444            | Botão de desconectar / alerta de queda    |
+-------------------+--------------------+-------------------------------------------+
```

---

## 📱 3. Componentes Centrais da Interface

### 3.1 O Escudo Minimalista (Shield Control)
* Um único vetor geométrico de escudo com espessura de borda de 5px.
* No centro, um círculo sólido representando o ponto de ancoragem seguro.
* **Estado Conectado:** Borda ciano com sombra difusa suave (`box-shadow: 0 8px 24px rgba(2, 132, 199, 0.18)`).
* **Estado Desconectado:** Borda cinza suave (`#94A3B8`), sem brilho, transmitindo inatividade imediata.

### 3.2 Pill de Localização (Country Selector)
* Exibe a bandeira oficial do país em alta definição.
* Nome do país em peso Semi-Bold (`700`) e cidade/número do nó logo abaixo.
* Badge de latência à direita (ex: `18 ms` em verde).

### 3.3 Indicador de Ping em 3 Barras
* 3 barras verticais de altura progressiva (4px, 8px, 12px).
* **Verde (Ótimo):** Latência < 50ms.
* **Amarelo (Médio):** Latência entre 50ms e 120ms.
* **Cinza (Distante):** Latência > 120ms.

---

### 3.4 Controles Nativos Uniformes (Padrão Apple Settings)
* **Regra de Ouro contra "Cara de IA":** Nunca misturar rótulos estáticos de marketing (ex: "100% Blindado") com interruptores reais.
* Configurações ativáveis/desativáveis pelo usuário (Kill Switch, Proteção Wi-Fi, Invisibilidade LAN, Prevenção de Vazamentos) utilizam estritamente o interruptor deslizante Apple (`.switch`).
* Rótulos e badges informativos devem ser estritamente concisos (uma única palavra: `Ativo`, `Invisível`, `0 Detectados`) e com propriedade `white-space: nowrap` para impedir quebras artificiais de linha.

## 🖥️ 4. Como Executar e Testar o Protótipo no seu Computador

O protótipo interativo completo foi construído em tecnologia web nativa (HTML5 + CSS3 + Vanilla JS) sem nenhuma dependência externa pesada.

Para abrir e visualizar:
1. Abra a pasta `/Users/cadubezerra/Desktop/FLUXVPN/` no seu Finder.
2. Dê um duplo-clique no arquivo **`index.html`** (ele abrirá no seu Google Chrome, Safari ou navegador padrão).
3. Você poderá:
   * Clicar no botão ou escudo para alternar entre **Conectado** e **Desconectado**.
   * Buscar servidores pelo nome ou país (ex: digite `Suíça` ou `Brasil`).
   * Alternar a visualização superior entre **Desktop (macOS)**, **Mobile (iPhone)** ou **Lado a Lado**.
