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

# Executa em modo Janela de Aplicativo Independente
if [ -d "/Applications/Google Chrome.app" ]; then
    open -na "Google Chrome" --args --app="file://$APP_FILE" --window-size=1040,700
elif [ -d "/Applications/Brave Browser.app" ]; then
    open -na "Brave Browser" --args --app="file://$APP_FILE" --window-size=1040,700
elif [ -d "/Applications/Microsoft Edge.app" ]; then
    open -na "Microsoft Edge" --args --app="file://$APP_FILE" --window-size=1040,700
else
    open "$APP_FILE"
fi

# Fecha o terminal automaticamente apos iniciar
osascript -e 'tell application "Terminal" to close (every window whose name contains "Iniciar FLUX VPN")' 2>/dev/null &
exit
