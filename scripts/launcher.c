#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>
#include <mach-o/dyld.h>
#include <sys/stat.h>

/**
 * FLUX VPN — Native macOS Mach-O Launcher
 * Substitui scripts de shell por um binário executável Mach-O nativo Apple.
 * Evita bloqueios de quarentena do Gatekeeper e a mensagem "O aplicativo não pode ser aberto".
 */
int main(int argc, char *argv[]) {
    char path[2048];
    uint32_t size = sizeof(path);
    if (_NSGetExecutablePath(path, &size) != 0) {
        return 1;
    }

    char real_path[2048];
    if (realpath(path, real_path) == NULL) {
        strncpy(real_path, path, sizeof(real_path));
    }

    // real_path: .../FLUX-VPN.app/Contents/MacOS/FLUX-VPN
    char *dir = dirname(real_path);          // .../Contents/MacOS
    char *contents = dirname(dir);           // .../Contents

    char engine_path[2048];
    snprintf(engine_path, sizeof(engine_path), "%s/Resources/core/flux_engine.py", contents);

    char index_path[2048];
    snprintf(index_path, sizeof(index_path), "%s/Resources/index.html", contents);

    // 1. Inicia o motor nativo Python em background se ainda não estiver em execução
    if (access(engine_path, F_OK) == 0) {
        char bg_cmd[4096];
        snprintf(bg_cmd, sizeof(bg_cmd), "pgrep -f flux_engine.py >/dev/null 2>&1 || (python3 \"%s\" >/dev/null 2>&1 &)", engine_path);
        system(bg_cmd);
    }

    // 2. Abre a interface moderna em janela nativa de aplicativo
    char launch_cmd[4096];
    if (access("/Applications/Google Chrome.app", F_OK) == 0) {
        snprintf(launch_cmd, sizeof(launch_cmd), "open -na \"Google Chrome\" --args --app=\"file://%s\" --window-size=1040,700", index_path);
    } else if (access("/Applications/Brave Browser.app", F_OK) == 0) {
        snprintf(launch_cmd, sizeof(launch_cmd), "open -na \"Brave Browser\" --args --app=\"file://%s\" --window-size=1040,700", index_path);
    } else if (access("/Applications/Microsoft Edge.app", F_OK) == 0) {
        snprintf(launch_cmd, sizeof(launch_cmd), "open -na \"Microsoft Edge\" --args --app=\"file://%s\" --window-size=1040,700", index_path);
    } else {
        snprintf(launch_cmd, sizeof(launch_cmd), "open \"%s\"", index_path);
    }

    system(launch_cmd);
    return 0;
}
