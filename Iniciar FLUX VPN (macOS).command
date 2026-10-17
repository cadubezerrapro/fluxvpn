#!/bin/bash
cd "$(dirname "$0")"

# Localiza o arquivo principal do aplicativo
APP_FILE="$(pwd)/index.html"

# Executa em modo Janela de Aplicativo Independente
if [ -d "/Applications/Google Chrome.app" ]; then
    open -na "Google Chrome" --args --app="file://$APP_FILE" --window-size=1200,850
elif [ -d "/Applications/Brave Browser.app" ]; then
    open -na "Brave Browser" --args --app="file://$APP_FILE" --window-size=1200,850
elif [ -d "/Applications/Microsoft Edge.app" ]; then
    open -na "Microsoft Edge" --args --app="file://$APP_FILE" --window-size=1200,850
else
    open "$APP_FILE"
fi

# Fecha o terminal automaticamente apos iniciar
osascript -e 'tell application "Terminal" to close (every window whose name contains "Iniciar FLUX VPN")' 2>/dev/null &
exit
