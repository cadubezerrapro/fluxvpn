#!/bin/bash
# ==============================================================================
# FLUX VPN — Instalador Oficial Automático para macOS (Zero Quarentena / Sem Bloqueios)
# Instala diretamente em /Applications, remove quarentena do Chrome e inicia o app.
# ==============================================================================

set -e

echo "=========================================================="
echo "⚡️ Instalador Oficial FLUX VPN para macOS"
echo "=========================================================="

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
APP_TARGET="/Applications/FLUX-VPN.app"
APP_SOURCE="$REPO_DIR/dist/macOS/FLUX-VPN.app"

if [ ! -d "$APP_SOURCE" ]; then
    APP_SOURCE="$REPO_DIR/FLUX-VPN.app"
fi

echo "[1/4] Removendo versões anteriores e limpando proxies residuais..."
rm -rf "$APP_TARGET"
rm -rf "$REPO_DIR/apps"
networksetup -setsocksfirewallproxystate Wi-Fi off 2>/dev/null || true
networksetup -setwebproxystate Wi-Fi off 2>/dev/null || true

# Provisiona chaves reais WireGuard Anycast de alta velocidade
python3 "$REPO_DIR/core/warp_provider.py" 2>/dev/null || true

echo "[2/4] Compilando executável nativo Cocoa WebKit (App Próprio no Dock e Menu Bar)..."
if command -v clang >/dev/null 2>&1 && [ -f "$REPO_DIR/scripts/launcher.m" ]; then
    clang -O2 -mmacosx-version-min=10.15 -framework Cocoa -framework WebKit "$REPO_DIR/scripts/launcher.m" -o "$APP_SOURCE/Contents/MacOS/FLUX-VPN"
    cp "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$REPO_DIR/FLUX-VPN.app/Contents/MacOS/FLUX-VPN"
    chmod 755 "$APP_SOURCE/Contents/MacOS/FLUX-VPN" "$REPO_DIR/FLUX-VPN.app/Contents/MacOS/FLUX-VPN"
fi

echo "[3/4] Instalando FLUX-VPN.app em /Applications..."
cp -R "$APP_SOURCE" "$APP_TARGET"

echo "[3/4] Removendo quarentena do Gatekeeper (Bypass permanente de alertas de malware)..."
xattr -cr "$APP_TARGET"
chmod -R 755 "$APP_TARGET"
codesign --force --deep --sign - "$APP_TARGET" 2>/dev/null || true

echo "[4/4] Limpando cache do Spotlight (Garante apenas 1 ícone oficial)..."
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain user 2>/dev/null || true

echo "=========================================================="
echo "✅ FLUX VPN INSTALADO COM SUCESSO!"
echo "🚀 Iniciando aplicativo agora..."
echo "=========================================================="

open "$APP_TARGET"
