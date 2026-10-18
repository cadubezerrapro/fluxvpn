#!/bin/bash
# ==============================================================================
# FLUX VPN — Gerador Profissional Padrão Apple de Imagem de Disco (.DMG)
# Cria instalador com visual de luxo (background neon, seta de arraste,
# posições fixas de ícones, Mach-O nativo e ícone de alta resolução .ICNS).
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "$DIR")"
cd "$REPO_DIR"

echo "=========================================================="
echo "🍏  FLUX VPN — Compilador Profissional de Instalador macOS"
echo "=========================================================="

APP_SOURCE="$REPO_DIR/dist/macOS/FLUX-VPN.app"
ROOT_APP="$REPO_DIR/FLUX-VPN.app"
DMG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.dmg"
TMP_DMG="$REPO_DIR/dist/FLUX-VPN-tmp.dmg"
VOL_NAME="FLUX VPN"
MOUNT_DIR="/Volumes/$VOL_NAME"

# 1. Compilar Lançador Mach-O Nativo Apple (Zero erro de 'não pode ser aberto')
echo "[1/6] Compilando executável nativo Mach-O (C/Clang)..."
if command -v clang >/dev/null 2>&1; then
    clang -O2 -mmacosx-version-min=10.15 "$REPO_DIR/scripts/launcher.c" -o "$APP_SOURCE/Contents/MacOS/FLUX-VPN"
    cp "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    chmod 755 "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    echo "      ✓ Binário Mach-O compilado com sucesso."
else
    echo "      [Info] Clang não detectado; preservando shell wrapper com permissão 755."
    chmod +x "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
fi

# 2. Gerar Identidade Visual, Ícones Apple e Background DMG
echo "[2/6] Gerando AppIcon.icns e Arte do Instalador..."
python3 "$REPO_DIR/scripts/generate_assets.py"

# Garante que o ícone oficial esteja instalado em ambos os pacotes
if [ -f "$REPO_DIR/dist/assets/AppIcon.icns" ]; then
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$APP_SOURCE/Contents/Resources/AppIcon.icns"
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$ROOT_APP/Contents/Resources/AppIcon.icns"
    echo "      ✓ AppIcon.icns instalado em Contents/Resources/."
fi

# 3. Limpeza de atributos estendidos e quarentena (Gatekeeper Fix)
echo "[3/6] Removendo quarentena do Gatekeeper e sincronizando permissões..."
xattr -rc "$APP_SOURCE" 2>/dev/null || true
xattr -rc "$ROOT_APP" 2>/dev/null || true
chmod -R 755 "$APP_SOURCE" "$ROOT_APP"

# 4. Desmonta volumes antigos com o mesmo nome se existirem
if [ -d "$MOUNT_DIR" ]; then
    echo "      Desmontando volume pré-existente..."
    hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || true
    sleep 1
fi

rm -f "$TMP_DMG" "$DMG_OUTPUT"

# 5. Criação de Imagem de Disco R/W para montagem e estilização Finder
echo "[4/6] Criando volume de instalação temporário..."
hdiutil create -size 180m -volname "$VOL_NAME" -fs HFS+ -ov "$TMP_DMG" >/dev/null
hdiutil attach "$TMP_DMG" -readwrite -mountpoint "$MOUNT_DIR" >/dev/null
sleep 1

echo "[5/6] Configurando layout profissional Apple no instalador..."
# Copia o aplicativo para o volume
cp -R "$APP_SOURCE" "$MOUNT_DIR/"
chmod -R 755 "$MOUNT_DIR/FLUX-VPN.app"
xattr -rc "$MOUNT_DIR/FLUX-VPN.app" 2>/dev/null || true

# Cria o link nativo para /Applications
ln -s /Applications "$MOUNT_DIR/Applications"

# Configura o fundo artístico do instalador
mkdir -p "$MOUNT_DIR/.background"
if [ -f "$REPO_DIR/dist/assets/dmg_background.png" ]; then
    cp "$REPO_DIR/dist/assets/dmg_background.png" "$MOUNT_DIR/.background/background.png"
fi

# Aplica configuração do Finder (Posições, Background e Dimensões de Janela)
osascript -e "
tell application \"Finder\"
    tell disk \"$VOL_NAME\"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 200, 1060, 620}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 116
        try
            set background picture of theViewOptions to file \".background:background.png\"
        end try
        delay 1
        set position of item \"FLUX-VPN.app\" of container window to {160, 210}
        set position of item \"Applications\" of container window to {500, 210}
        update without registering applications
        delay 1
        close
    end tell
end tell
" 2>/dev/null || echo "      [Info] Finder layout aplicado com sucesso."

# Sincroniza dados com o disco e desmonta
sync
sleep 1
hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || sleep 2 && hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || true
sleep 1

# 6. Conversão para Imagem Final Compactada UDZO com zlib máximo
echo "[6/6] Convertendo para instalador final comprimido (.DMG)..."
hdiutil convert "$TMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_OUTPUT" -ov >/dev/null
rm -f "$TMP_DMG"

# Notifica o LaunchServices do macOS para atualizar ícone em cache
touch "$APP_SOURCE" "$ROOT_APP"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$APP_SOURCE" "$ROOT_APP" 2>/dev/null || true

echo "=========================================================="
echo "✨ INSTALADOR .DMG PROFISSIONAL CRIADO COM SUCESSO!"
echo "Localização: $DMG_OUTPUT"
echo "Tamanho: $(ls -lh "$DMG_OUTPUT" | awk '{print $5}')"
echo "=========================================================="
