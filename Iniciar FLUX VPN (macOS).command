#!/bin/bash
cd "$(dirname "$0")"

# Inicia o motor nativo de rede FLUX em segundo plano (se não estiver rodando)
if ! pgrep -f "flux_engine.py" > /dev/null; then
    if [ -f "core/flux_engine.py" ]; then
        python3 core/flux_engine.py >/dev/null 2>&1 &
    fi
fi

# Localiza o arquivo principal do aplicativo
APP_FILE="$(pwd)/index.html"

# Executa como Aplicativo Nativo Próprio (Processo Único no Dock e Menu Bar Apple)
if [ -d "/Applications/FLUX-VPN.app" ]; then
    open -a "/Applications/FLUX-VPN.app"
elif [ -d "./FLUX-VPN.app" ]; then
    open -a "./FLUX-VPN.app"
else
    open "$APP_FILE"
fi

# Fecha o terminal automaticamente apos iniciar
osascript -e 'tell application "Terminal" to close (every window whose name contains "Iniciar FLUX VPN")' 2>/dev/null &
exit
