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

DEFAULT_CONF = os.path.join(REPO_DIR, "profiles", "FLUX-WireGuard-Real.conf")

def ensure_profile():
    """Garante a existência de um perfil WireGuard válido e ativo."""
    if not os.path.exists(DEFAULT_CONF) or os.path.getsize(DEFAULT_CONF) < 50:
        res = warp_provider.provision_real_wireguard_profile(DEFAULT_CONF)
        return res.get("output_path") or DEFAULT_CONF
    return DEFAULT_CONF

def is_wireguard_installed():
    """Verifica se o utilitário wg-quick ou wireguard-tools está disponível no sistema."""
    paths = [
        "/opt/homebrew/bin/wg-quick",
        "/usr/local/bin/wg-quick",
        shutil.which("wg-quick")
    ]
    for p in paths:
        if p and os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None

def is_tunnel_active():
    """Verifica se a interface WireGuard (utun) está ativada no sistema."""
    try:
        res = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=2)
        if "172.16.0.2" in res.stdout or "10.66.66.2" in res.stdout:
            return True
        wg_bin = shutil.which("wg") or "/opt/homebrew/bin/wg" or "/usr/local/bin/wg"
        if os.path.exists(wg_bin):
            wg_res = subprocess.run([wg_bin, "show"], capture_output=True, text=True, timeout=2)
            if "interface:" in wg_res.stdout:
                return True
    except Exception:
        pass
    return False

def activate_wireguard(conf_path=None):
    """
    Ativa o túnel WireGuard de Kernel.
    Tenta wg-quick com privilégios de helper ou scutil nativo do macOS.
    """
    conf = conf_path or ensure_profile()
    wg_quick = is_wireguard_installed()

    # 1. Garante que nenhum proxy SOCKS quebrado esteja ativo no Wi-Fi
    cleanup_system_proxies()

    if wg_quick:
        try:
            cmd = [wg_quick, "up", conf]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return True, "Túnel WireGuard Ativado com Sucesso (utun)"

            cmd_sudo = ["sudo", "-n", wg_quick, "up", conf]
            res_sudo = subprocess.run(cmd_sudo, capture_output=True, text=True, timeout=5)
            if res_sudo.returncode == 0:
                return True, "Túnel WireGuard Ativado com Sucesso via Helper"
        except Exception:
            pass

    try:
        res_scutil = subprocess.run(["scutil", "--nc", "start", "FLUX-WireGuard-Real"], capture_output=True, text=True, timeout=3)
        if res_scutil.returncode == 0:
            return True, "Túnel WireGuard Ativado via NetworkExtension Apple"
    except Exception:
        pass

    return False, "Requer ativação do Helper WireGuard nativo no macOS (sudo bash scripts/setup_wireguard.sh)"

def deactivate_wireguard(conf_path=None):
    """Desativa com segurança o túnel WireGuard e restaura 100% da rede Wi-Fi normal."""
    conf = conf_path or DEFAULT_CONF
    wg_quick = is_wireguard_installed()

    if wg_quick:
        try:
            subprocess.run([wg_quick, "down", conf], capture_output=True, timeout=4)
        except Exception:
            pass
        try:
            subprocess.run(["sudo", "-n", wg_quick, "down", conf], capture_output=True, timeout=4)
        except Exception:
            pass

    try:
        subprocess.run(["scutil", "--nc", "stop", "FLUX-WireGuard-Real"], capture_output=True, timeout=2)
    except Exception:
        pass

    cleanup_system_proxies()
    return True, "Túnel Desativado e Rede Normal Restaurada"

def cleanup_system_proxies():
    """Garante que nenhum proxy residual interfira em chamadas do Discord ou navegação."""
    try:
        subprocess.run(["networksetup", "-setsocksfirewallproxystate", "Wi-Fi", "off"], capture_output=True, timeout=2)
        subprocess.run(["networksetup", "-setwebproxystate", "Wi-Fi", "off"], capture_output=True, timeout=2)
        subprocess.run(["networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"], capture_output=True, timeout=2)
    except Exception:
        pass
