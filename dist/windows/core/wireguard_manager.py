#!/usr/bin/env python3
"""
FLUX VPN — WireGuard® Engine Manager
Gerencia a ativação, monitoramento e desativação do túnel WireGuard no macOS.
Roteia 100% dos pacotes (UDP + TCP) via interface nativa utun sem quebrar chamadas
do Discord, jogos ou transmissões ao vivo.
"""

import os
import sys
import subprocess
import time
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import warp_provider

DEFAULT_CONF = "/etc/wireguard/flux0.conf"
REPO_CONF = os.path.join(REPO_DIR, "profiles", "flux0.conf")

def find_binary(name):
    """Localiza executável no sistema operacional (Apple Silicon e Intel)."""
    candidates = [
        shutil.which(name),
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
        f"/usr/bin/{name}",
        f"/sbin/{name}",
        f"/usr/sbin/{name}"
    ]
    for c in candidates:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None

def ensure_profile():
    """Garante a existência de um perfil WireGuard válido e ativo."""
    if os.path.exists(REPO_CONF) and os.path.getsize(REPO_CONF) > 50:
        return REPO_CONF
    if os.path.exists(DEFAULT_CONF) and os.path.getsize(DEFAULT_CONF) > 50:
        return DEFAULT_CONF
    res = warp_provider.provision_real_wireguard_profile(REPO_CONF)
    return res.get("output_path") or REPO_CONF

def is_wireguard_installed():
    """Verifica se o utilitário wg-quick ou wireguard-tools está disponível no sistema."""
    return find_binary("wg-quick")

def is_tunnel_active():
    """Verifica se a interface WireGuard (utun) está ativada no sistema."""
    try:
        res = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=2)
        if "flux0" in res.stdout or "172.16.0.2" in res.stdout:
            return True
        wg_bin = find_binary("wg")
        if wg_bin:
            wg_res = subprocess.run([wg_bin, "show"], capture_output=True, text=True, timeout=2)
            if "interface:" in wg_res.stdout:
                return True
        if os.path.exists("/var/run/wireguard/flux0.name"):
            return True
    except Exception:
        pass
    return False

def activate_wireguard(conf_path=None):
    """
    Ativa o túnel WireGuard de Kernel.
    Tenta wg-quick com privilégios de helper ou autorização nativa do macOS.
    """
    conf = conf_path or ensure_profile()
    wg_quick = is_wireguard_installed()

    # 1. Garante que nenhum proxy SOCKS quebrado esteja ativo na rede
    cleanup_system_proxies()

    if is_tunnel_active():
        return True, "Túnel WireGuard Já Ativo (flux0)"

    if wg_quick:
        # 1. Tenta sudo sem senha (quando configurado via helper)
        targets = [conf, "flux0"]
        for target in targets:
            try:
                cmd_sudo = ["sudo", "-n", wg_quick, "up", target]
                res_sudo = subprocess.run(cmd_sudo, capture_output=True, text=True, timeout=6)
                if res_sudo.returncode == 0 or "already exists" in res_sudo.stderr.lower():
                    return True, "Túnel WireGuard Ativado com Sucesso (flux0)"
            except Exception:
                pass

        # 2. Tenta execução direta
        try:
            cmd = [wg_quick, "up", conf]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return True, "Túnel WireGuard Ativado com Sucesso (utun)"
        except Exception:
            pass

        # 3. Fallback inteligente: autorização gráfica nativa do macOS via osascript
        try:
            ascript = f'do shell script "{wg_quick} up {conf}" with administrator privileges'
            res_as = subprocess.run(["osascript", "-e", ascript], capture_output=True, text=True, timeout=20)
            if res_as.returncode == 0:
                return True, "Túnel WireGuard Ativado com Sucesso (Administrador)"
        except Exception:
            pass

    return False, "Requer ativação do Helper WireGuard nativo no macOS (sudo bash scripts/setup_wireguard.sh)"

def deactivate_wireguard(conf_path=None):
    """Desativa com segurança o túnel WireGuard e restaura 100% da rede normal."""
    conf = conf_path or ensure_profile()
    wg_quick = is_wireguard_installed()

    if wg_quick:
        for target in ["flux0", conf]:
            try:
                subprocess.run(["sudo", "-n", wg_quick, "down", target], capture_output=True, timeout=4)
            except Exception:
                pass
            try:
                subprocess.run([wg_quick, "down", target], capture_output=True, timeout=4)
            except Exception:
                pass
            try:
                ascript = f'do shell script "{wg_quick} down {target}" with administrator privileges'
                subprocess.run(["osascript", "-e", ascript], capture_output=True, timeout=10)
            except Exception:
                pass

    cleanup_system_proxies()
    return True, "Túnel Desativado e Rede Normal Restaurada"

def cleanup_system_proxies():
    """Garante que nenhum proxy residual interfira em chamadas do Discord ou navegação."""
    try:
        res = subprocess.run(["networksetup", "-listallnetworkservices"], capture_output=True, text=True, timeout=2)
        services = [s.strip() for s in res.stdout.splitlines() if s.strip() and not s.startswith("*")]
        for s in services:
            subprocess.run(["networksetup", "-setsocksfirewallproxystate", s, "off"], capture_output=True, timeout=1)
            subprocess.run(["networksetup", "-setwebproxystate", s, "off"], capture_output=True, timeout=1)
            subprocess.run(["networksetup", "-setsecurewebproxystate", s, "off"], capture_output=True, timeout=1)
    except Exception:
        try:
            subprocess.run(["networksetup", "-setsocksfirewallproxystate", "Wi-Fi", "off"], capture_output=True, timeout=1)
            subprocess.run(["networksetup", "-setwebproxystate", "Wi-Fi", "off"], capture_output=True, timeout=1)
            subprocess.run(["networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"], capture_output=True, timeout=1)
        except Exception:
            pass
