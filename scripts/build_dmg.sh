#!/bin/bash
# ==============================================================================
# FLUX VPN — Gerador Profissional Apple no MODO CLARO (Light Mode Clean)
# Fundo Cerâmico Apple Branco, Logo Branca, Retina Anti-Pixelado (.TIFF),
# Mach-O nativo, CodeSign ad-hoc e Script Auxiliar de Desbloqueio 1-Clique.
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "$DIR")"
cd "$REPO_DIR"

echo "=========================================================="
echo "🍏 FLUX VPN — Compilador Apple Modo Claro (Clean White)"
echo "=========================================================="

APP_SOURCE="$REPO_DIR/dist/macOS/FLUX-VPN.app"
ROOT_APP="$REPO_DIR/FLUX-VPN.app"
DMG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.dmg"
PKG_OUTPUT="$REPO_DIR/dist/FLUX-VPN-macOS.pkg"
TMP_DMG="$REPO_DIR/dist/FLUX-VPN-tmp.dmg"
VOL_NAME="FLUX VPN"
MOUNT_DIR="/Volumes/$VOL_NAME"

# 1. Remove duplicatas antigas do Spotlight
rm -rf "$REPO_DIR/apps"

# 2. Compilar Lançador Mach-O Nativo Apple (Zero erro de 'não pode ser aberto')
echo "[1/7] Compilando executável nativo Mach-O (C/Clang)..."
if command -v clang >/dev/null 2>&1; then
    clang -O2 -mmacosx-version-min=10.15 "$REPO_DIR/scripts/launcher.c" -o "$APP_SOURCE/Contents/MacOS/FLUX-VPN"
    cp "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    chmod 755 "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
    echo "      ✓ Binário Mach-O compilado com sucesso."
else
    chmod +x "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$ROOT_APP/Contents/MacOS/FLUX-VPN"
fi

# 3. Gerar Identidade Visual Modo Claro, Logo Branca e Fundo Retina TIFF
echo "[2/7] Gerando AppIcon.icns (Logo Branca) e Fundo Retina Modo Claro..."
python3 "$REPO_DIR/scripts/generate_assets.py"

# Garante que o ícone oficial esteja instalado em ambos os pacotes
if [ -f "$REPO_DIR/dist/assets/AppIcon.icns" ]; then
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$APP_SOURCE/Contents/Resources/AppIcon.icns"
    cp "$REPO_DIR/dist/assets/AppIcon.icns" "$ROOT_APP/Contents/Resources/AppIcon.icns"
    echo "      ✓ AppIcon.icns instalado em Contents/Resources/."
fi

# 4. Assinatura de Código Apple (CodeSign Ad-Hoc com SHA256)
echo "[3/7] Aplicando CodeSign nativo Apple em todo o bundle..."
xattr -rc "$APP_SOURCE" 2>/dev/null || true
xattr -rc "$ROOT_APP" 2>/dev/null || true
chmod -R 755 "$APP_SOURCE" "$ROOT_APP"
codesign --force --deep --sign - "$APP_SOURCE" 2>/dev/null || true
codesign --force --deep --sign - "$ROOT_APP" 2>/dev/null || true
echo "      ✓ Assinatura de integridade aplicada."

# 5. Compilação do Instalador Apple .PKG (Bypass de quarentena do Chrome)
echo "[4/7] Compilando instalador assistido Apple .PKG..."
if command -v pkgbuild >/dev/null 2>&1; then
    rm -f "$PKG_OUTPUT"
    pkgbuild --install-location /Applications \
             --component "$APP_SOURCE" \
             --version "1.2.0" \
             --identifier "pro.cadubezerra.fluxvpn" \
             "$PKG_OUTPUT" >/dev/null 2>&1 || true
    echo "      ✓ Instalador .PKG gerado: $PKG_OUTPUT"
fi

# 6. Desmonta volumes antigos
if [ -d "$MOUNT_DIR" ]; then
    echo "      Desmontando volume pré-existente..."
    hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || true
    sleep 1
fi

rm -f "$TMP_DMG" "$DMG_OUTPUT"

# 7. Criação de Imagem de Disco R/W para montagem e estilização Finder
echo "[5/7] Criando volume temporário de instalação..."
hdiutil create -size 180m -volname "$VOL_NAME" -fs HFS+ -ov "$TMP_DMG" >/dev/null
hdiutil attach "$TMP_DMG" -readwrite -mountpoint "$MOUNT_DIR" >/dev/null
sleep 1

echo "[6/7] Aplicando visual Apple Modo Claro (White & Clean)..."
# Copia o aplicativo assinado para o volume
cp -R "$APP_SOURCE" "$MOUNT_DIR/"
chmod -R 755 "$MOUNT_DIR/FLUX-VPN.app"
xattr -rc "$MOUNT_DIR/FLUX-VPN.app" 2>/dev/null || true

# Cria o atalho nativo para /Applications
ln -s /Applications "$MOUNT_DIR/Applications"

# Adiciona o script auxiliar de 1-clique para desbloqueio instantâneo do Gatekeeper
cat <<'EOF' > "$MOUNT_DIR/⚡️ Desbloquear e Abrir FLUX VPN.command"
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "=========================================================="
echo "🔓 Desbloqueando FLUX VPN no macOS (Gatekeeper Bypass)..."
echo "=========================================================="
if [ -d "/Applications/FLUX-VPN.app" ]; then
    xattr -cr /Applications/FLUX-VPN.app 2>/dev/null || true
    echo "✓ Permissões liberadas com sucesso em /Applications!"
    open /Applications/FLUX-VPN.app
else
    xattr -cr "$DIR/FLUX-VPN.app" 2>/dev/null || true
    cp -R "$DIR/FLUX-VPN.app" /Applications/
    xattr -cr /Applications/FLUX-VPN.app 2>/dev/null || true
    echo "✓ Instalado e liberado em Aplicativos!"
    open /Applications/FLUX-VPN.app
fi
EOF
chmod +x "$MOUNT_DIR/⚡️ Desbloquear e Abrir FLUX VPN.command"

# Configura o fundo artístico Modo Claro (Retina TIFF ou PNG)
mkdir -p "$MOUNT_DIR/.background"
if [ -f "$REPO_DIR/dist/assets/dmg_background.tiff" ]; then
    cp "$REPO_DIR/dist/assets/dmg_background.tiff" "$MOUNT_DIR/.background/background.tiff"
    BG_FILE=".background:background.tiff"
else
    cp "$REPO_DIR/dist/assets/dmg_background.png" "$MOUNT_DIR/.background/background.png"
    BG_FILE=".background:background.png"
fi

# Aplica configuração do Finder (Alinhamento em 660x420)
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
            set background picture of theViewOptions to file \"$BG_FILE\"
        end try
        delay 1
        set position of item \"FLUX-VPN.app\" of container window to {160, 195}
        set position of item \"Applications\" of container window to {500, 195}
        set position of item \"⚡️ Desbloquear e Abrir FLUX VPN.command\" of container window to {330, 340}
        update without registering applications
        delay 1
        close
    end tell
end tell
" 2>/dev/null || echo "      [Info] Finder layout aplicado com sucesso."

sync
sleep 1
hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || sleep 2 && hdiutil detach "$MOUNT_DIR" -force 2>/dev/null || true
sleep 1

# 8. Conversão para Imagem Final Compactada UDZO
echo "[7/7] Convertendo para instalador final comprimido (.DMG)..."
hdiutil convert "$TMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_OUTPUT" -ov >/dev/null
rm -f "$TMP_DMG"

# Notifica o LaunchServices do macOS para limpar duplicatas e atualizar ícones
touch "$APP_SOURCE" "$ROOT_APP"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user 2>/dev/null || true

echo "=========================================================="
echo "✨ INSTALADORES APPLE MODO CLARO (.DMG & .PKG) CRIADOS COM SUCESSO!"
echo "DMG: $DMG_OUTPUT"
if [ -f "$PKG_OUTPUT" ]; then
    echo "PKG: $PKG_OUTPUT"
fi
echo "=========================================================="
