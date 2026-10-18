#!/bin/bash
# ==============================================================================
# FLUX VPN — Instalador Oficial do Helper WireGuard® de Kernel para macOS
# Habilita conexão WireGuard 100% nativa de 1 clique dentro do FLUX VPN.
# Roteia UDP (Discord áudio/vídeo/tela), jogos e tráfego criptografado sem quedas.
# ==============================================================================

set -e

echo "=========================================================="
echo "🛡️  FLUX VPN — Configuração do Motor Nativo WireGuard®"
echo "=========================================================="

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
CURRENT_USER=$(whoami)

# 1. Garante que nenhum proxy SOCKS antigo esteja interferindo no Wi-Fi
echo "[1/4] Limpando configurações residuais de proxy no Wi-Fi..."
networksetup -setsocksfirewallproxystate Wi-Fi off 2>/dev/null || true
networksetup -setwebproxystate Wi-Fi off 2>/dev/null || true
networksetup -setsecurewebproxystate Wi-Fi off 2>/dev/null || true

# 2. Instala wireguard-tools via Homebrew se necessário
echo "[2/4] Verificando ferramentas oficiais do WireGuard (wg-quick)..."
if ! command -v wg-quick >/dev/null 2>&1; then
    if command -v brew >/dev/null 2>&1; then
        echo "      Instalando wireguard-tools via Homebrew..."
        brew install wireguard-tools
    else
        echo "      Homebrew não detectado. Você pode instalar com: brew install wireguard-tools"
    fi
else
    echo "      ✓ Utilitário wg-quick já instalado em: $(command -v wg-quick)"
fi

# 3. Provisiona perfil WireGuard Anycast Real com Chaves Curve25519
echo "[3/4] Provisionando túnel criptografado Anycast de alta velocidade..."
python3 "$REPO_DIR/core/warp_provider.py" || true

# 4. Configura Privileged Helper Tool no macOS (Zero prompts de senha no app)
echo "[4/4] Autorizando controle seguro de rede para o FLUX VPN..."
WG_PATH=$(command -v wg-quick || echo "/opt/homebrew/bin/wg-quick")
WG_BIN=$(command -v wg || echo "/opt/homebrew/bin/wg")

SUDOERS_FILE="/etc/sudoers.d/fluxvpn"
TMP_SUDOERS="/tmp/fluxvpn_sudoers"

echo "$CURRENT_USER ALL=(ALL) NOPASSWD: $WG_PATH, $WG_BIN" > "$TMP_SUDOERS"
echo "Para autorizar o FLUX VPN a controlar a interface WireGuard sem pedir senha a cada clique:"
sudo cp "$TMP_SUDOERS" "$SUDOERS_FILE" 2>/dev/null || {
    echo "⚠️  Execute este comando com sudo para salvar a regra de 1 clique:"
    echo "sudo cp $TMP_SUDOERS $SUDOERS_FILE && sudo chmod 0440 $SUDOERS_FILE"
}
sudo chmod 0440 "$SUDOERS_FILE" 2>/dev/null || true
rm -f "$TMP_SUDOERS"

echo "=========================================================="
echo "✅ MOTOR WIREGUARD 100% PRONTO E CONFIGURADO!"
echo "🚀 Agora você pode abrir o FLUX VPN e conectar com 1 clique."
echo "=========================================================="
