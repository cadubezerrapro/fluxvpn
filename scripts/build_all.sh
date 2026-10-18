#!/bin/bash
# ==============================================================================
# FLUX VPN — Compilação e Empacotamento Oficial de Todas as Plataformas
# Executa a geração de ícones, compilação Mach-O nativa, DMG estilizado e ZIPs
# ==============================================================================

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "$DIR")"
cd "$REPO_DIR"

echo "=========================================================="
echo "🚀 FLUX VPN — Iniciando Compilação Global de Produção"
echo "=========================================================="

# 1. Executa o gerador de assets e compilador do Instalador .DMG
bash "$REPO_DIR/scripts/build_dmg.sh"

# 2. Atualiza o pacote macOS (.ZIP) contendo o App com o ícone oficial
echo "📦 Atualizando dist/FLUX-VPN-macOS.zip..."
cd "$REPO_DIR/dist/macOS" && zip -r -q "$REPO_DIR/dist/FLUX-VPN-macOS.zip" . -x "*.DS_Store" && cd "$REPO_DIR"

# 3. Atualiza o pacote Windows (.ZIP) contendo motor, VBS silencioso e ícone
echo "📦 Atualizando dist/FLUX-VPN-Windows.zip..."
cd "$REPO_DIR/dist/windows" && zip -r -q "$REPO_DIR/dist/FLUX-VPN-Windows.zip" . -x "*.DS_Store" && cd "$REPO_DIR"

# 4. Atualiza o pacote da Extensão Web (.ZIP)
echo "📦 Atualizando dist/FLUX-VPN-Chrome-Extension.zip..."
cd "$REPO_DIR/dist/chrome-extension" && zip -r -q "$REPO_DIR/dist/FLUX-VPN-Chrome-Extension.zip" . -x "*.DS_Store" && cd "$REPO_DIR"

echo "=========================================================="
echo "✅ Todos os instaladores e pacotes estão 100% prontos para distribuição!"
echo "=========================================================="
