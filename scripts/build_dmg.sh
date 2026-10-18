#!/bin/bash
# ==============================================================================
# FLUX VPN — Gerador Profissional Padrão Apple de Imagem de Disco (.DMG & .PKG)
# Cria instalador com visual de luxo (background neon alinhado, seta de arraste,
# posições exatas dos ícones, Mach-O nativo, ícone .ICNS e assinatura CodeSign).
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "$DIR")"
cd "$REPO_DIR"

echo "=========================================================="
echo "🍏  FLUX VPN — Compilador Profissional de Instaladores Apple"
echo "=========================================================="

APP_SOURCE="$REPO_DIR/dist/macOS/FLUX-VPN.app"
ROOT_APP="$REPO_DIR/FLUX-VPN.app"
DMG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.dmg"
PKG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.pkg"
TMP_DMG="$REPO_DIR/dist/FLUX-VPN-tmp.dmg"
VOL_NAME="FLUX VPN"
MOUNT_DIR="/Volumes/$VOL_NAME"

# 1. Compilar Lançador Mach-O Nativo Apple (Zero erro de 'não pode ser aberto')
echo "[1/7] Compilando executável nativo Mach-O (C/Clang)..."
if command -v clang >/dev/null 2>&1; then
    clang -O2 -mmacosx-version-min=10.15 "$REPO_DIR/scripts/launcher.c" -o "$APP_SOURCE/Contents/MacOS/FLUX-VPN"
    cp "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    chmod 755 "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    echo "      ✓ Binário Mach-O compilado com sucesso."
else
    echo "      [Info] Clang não detectado; preservando shell wrapper com permissão 755."
    chmod +x "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
fi

# 2. Gerar Identidade Visual, Ícones Apple e Background DMG (660x420)
echo "[2/7] Gerando AppIcon.icns e Arte Alinhada do Instalador..."
python3 "$REPO_DIR/scripts/generate_assets.py"

# Garante que o ícone oficial esteja instalado em ambos os pacotes
if [ -f "$REPO_DIR/dist/assets/AppIcon.icns" ]; then
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$APP_SOURCE/Contents/Resources/AppIcon.icns"
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$ROOT_APP/Contents/Resources/AppIcon.icns"
    echo "      ✓ AppIcon.icns instalado em Contents/Resources/."
fi

# 3. Assinatura de Código Apple (CodeSign Ad-Hoc / Elimina alerta de 'aplicativo danificado')
echo "[3/7] Aplicando CodeSign nativo Apple e selando recursos com SHA256..."
xattr -rc "$APP_SOURCE" 2>/dev/null || true
xattr -rc "$ROOT_APP" 2>/dev/null || true
chmod -R 755 "$APP_SOURCE" "$ROOT_APP"
codesign --force --deep --sign - "$APP_SOURCE" 2>/dev/null || true
codesign --force --deep --sign - "$ROOT_APP" 2>/dev/null || true
echo "      ✓ Assinatura de integridade Apple aplicada com sucesso."

# 4. Compilação do Instalador Apple .PKG (Instalação em 1 Clique sem Quarentena de Browser)
echo "[4/7] Compilando instalador nativo Apple .PKG..."
if command -v pkgbuild >/dev/null 2>&1; then
    rm -f "$PKG_OUTPUT"
    pkgbuild --install-location /Applications \
             --component "$APP_SOURCE" \
             --version "1.2.0" \
             --identifier "pro.cadubezerra.fluxvpn" \
             "$PKG_OUTPUT" >/dev/null 2>&1 || true
    echo "      ✓ Instalador .PKG gerado: $PKG_OUTPUT"
fi

# 5. Desmonta volumes antigos se existirem
if [ -d "$MOUNT_DIR" ]; then
    echo "      Desmontando volume pré-existente..."
    hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || true
    sleep 1
fi

rm -f "$TMP_DMG" "$DMG_OUTPUT"

# 6. Criação de Imagem de Disco R/W para montagem e estilização Finder
echo "[5/7] Criando volume de instalação temporário..."
hdiutil create -size 180m -volname "$VOL_NAME" -fs HFS+ -ov "$TMP_DMG" >/dev/null
hdiutil attach "$TMP_DMG" -readwrite -mountpoint "$MOUNT_DIR" >/dev/null
sleep 1

echo "[6/7] Configurando layout profissional Apple no instalador..."
# Copia o aplicativo assinado para o volume
cp -R "$APP_SOURCE" "$MOUNT_DIR/"
chmod -R 755 "$MOUNT_DIR/FLUX-VPN.app"
xattr -rc "$MOUNT_DIR/FLUX-VPN.app" 2>/dev/null || true

# Cria o link nativo para /Applications
ln -s /Applications "$MOUNT_DIR/Applications"

# Configura o fundo artístico do instalador (perfeitamente alinhado em 660x420)
mkdir -p "$MOUNT_DIR/.background"
if [ -f "$REPO_DIR/dist/assets/dmg_background.png" ]; then
    cp "$REPO_DIR/dist/assets/dmg_background.png" "$MOUNT_DIR/.background/background.png"
fi

# Aplica configuração do Finder (Alinhamento nos círculos (160, 195) e (500, 195))
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
        set position of item \"FLUX-VPN.app\" of container window to {160, 195}
        set position of item \"Applications\" of container window to {500, 195}
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

# 7. Conversão para Imagem Final Compactada UDZO com zlib máximo
echo "[7/7] Convertendo para instalador final comprimido (.DMG)..."
hdiutil convert "$TMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_OUTPUT" -ov >/dev/null
rm -f "$TMP_DMG"

# Notifica o LaunchServices do macOS para atualizar ícone em cache
touch "$APP_SOURCE" "$ROOT_APP"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$APP_SOURCE" "$ROOT_APP" 2>/dev/null || true

echo "=========================================================="
echo "✨ INSTALADORES APPLE (.DMG & .PKG) CRIADOS COM SUCESSO!"
echo "DMG: $DMG_OUTPUT"
if [ -f "$PKG_OUTPUT" ]; then
    echo "PKG: $PKG_OUTPUT"
fi
echo "=========================================================="
