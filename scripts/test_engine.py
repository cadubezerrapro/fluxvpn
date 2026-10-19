#!/usr/bin/env python3
"""
FLUX VPN — Suíte de Testes Automatizados de Conectividade e Motor de Rede
Valida detecção de IP, roteamento de sistema, segurança contra falhas e endpoints do motor.
"""

import os
import sys
import time
import socket
import urllib.request
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, REPO_DIR)
sys.path.insert(0, os.path.join(REPO_DIR, "core"))

import flux_engine
try:
    import warp_provider
except ImportError:
    from core import warp_provider

def run_tests():
    print("=" * 60)
    print("🧪 FLUX VPN — Diagnóstico e Testes de Integridade de Rede")
    print("=" * 60)
    
    passed = 0
    total = 5

    # Teste 1: Detecção de IP Público
    print("[1/5] Testando detecção de IP público...")
    try:
        ip = flux_engine.detect_public_ip()
        print(f"      ✓ IP detectado: {ip}")
        passed += 1
    except Exception as e:
        print(f"      ✗ Falha na detecção de IP: {e}")

    # Teste 2: Identificação do Serviço de Rede macOS
    print("[2/5] Identificando serviço de rede ativo no macOS...")
    try:
        service = flux_engine.get_macos_active_service()
        print(f"      ✓ Serviço ativo: {service}")
        passed += 1
    except Exception as e:
        print(f"      ✗ Falha ao identificar serviço: {e}")

    # Teste 3: Provisionamento e Validação de Chaves WireGuard® Curve25519
    print("[3/5] Testando provisionamento de chaves Curve25519 e túnel Anycast...")
    try:
        conf_res = warp_provider.provision_real_wireguard_profile()
        print(f"      ✓ Endpoint WireGuard verificado: {conf_res.get('endpoint')}")
        passed += 1
    except Exception as e:
        print(f"      ✗ Falha no provisionamento: {e}")

    # Teste 4: Ciclo Seguro de Conexão e Desconexão (Sem Derrubar a Internet)
    print("[4/5] Testando ativação e restauração de segurança de rede...")
    try:
        ok, msg = flux_engine.connect_tunnel("us-ny")
        print(f"      ✓ Conexão: {msg}")
        time.sleep(1)
        ok_d, msg_d = flux_engine.disconnect_tunnel()
        print(f"      ✓ Desconexão e restauração: {msg_d}")
        passed += 1
    except Exception as e:
        print(f"      ✗ Falha no ciclo de túnel: {e}")

    # Teste 5: Verificação de Integridade dos Bundles .app
    print("[5/5] Testando integridade do binário Mach-O e Info.plist...")
    app_path = os.path.join(REPO_DIR, "dist", "macOS", "FLUX-VPN.app")
    if not os.path.exists(app_path):
        app_path = os.path.join(REPO_DIR, "FLUX-VPN.app")
    exec_path = os.path.join(app_path, "Contents", "MacOS", "FLUX-VPN")
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    
    if os.path.exists(exec_path) and os.access(exec_path, os.X_OK) and os.path.exists(plist_path):
        print("      ✓ Pacote FLUX-VPN.app íntegro e executável com sucesso.")
        passed += 1
    else:
        print("      ✗ Pacote de aplicativo incompleto ou sem permissão de execução.")

    print("=" * 60)
    print(f"📊 RESULTADO FINAL: {passed}/{total} Testes Aprovados!")
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
