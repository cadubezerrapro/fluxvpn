#!/bin/bash
# ==============================================================================
# FLUX VPN — Gerador Automático de Instalador Nativo Apple (.DMG)
# Cria uma imagem de disco profissional padrão macOS com atalho para /Applications
# ==============================================================================

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "$DIR")"
cd "$REPO_DIR"

echo "=========================================================="
echo "🍏  FLUX VPN — Compilando Instalador .DMG Profissional para macOS"
echo "=========================================================="

DMG_TEMP="$REPO_DIR/build_dmg_temp"
DMG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.dmg"
APP_SOURCE="$REPO_DIR/dist/macOS/FLUX-VPN.app"

# 1. Limpa resíduos anteriores
rm -rf "$DMG_TEMP" "$DMG_OUTPUT"
mkdir -p "$DMG_TEMP"

# 2. Copia o pacote do aplicativo oficial
echo "[1/4] Copiando FLUX-VPN.app..."
cp -R "$APP_SOURCE" "$DMG_TEMP/"

# 3. Cria o atalho nativo para a pasta Aplicativos do Mac
echo "[2/4] Criando atalho nativo para /Applications..."
ln -s /Applications "$DMG_TEMP/Applications"

# 4. Adiciona arquivo descritivo de boas-vindas
cat <<EOF > "$DMG_TEMP/LEIA-ME.txt"
FLUX VPN para macOS
===================
Para instalar, basta arrastar o ícone 'FLUX-VPN.app' para a pasta 'Applications'.

Recursos embutidos:
• Conexão com 1 clique (Plug & Play)
• Criptografia de ponta a ponta
• Proteção contra vazamentos de IP/DNS
• Desbloqueio automático de serviços regionais (Discord, etc.)
EOF

# 5. Gera a imagem de disco compactada .DMG (UDZO)
echo "[3/4] Empacotando imagem de disco .DMG..."
hdiutil create -volname "FLUX VPN" \
               -srcfolder "$DMG_TEMP" \
               -ov \
               -format UDZO \
               "$DMG_OUTPUT"

# 6. Limpeza da pasta temporária
echo "[4/4] Limpando arquivos temporários..."
rm -rf "$DMG_TEMP"

echo "=========================================================="
echo "✅ Instalador macOS criado com sucesso!"
echo "Arquivo: $DMG_OUTPUT"
echo "=========================================================="
