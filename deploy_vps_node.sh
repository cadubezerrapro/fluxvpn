#!/bin/bash
# ==============================================================================
# FLUX VPN — Script de Implantação Automatizada de Nó na Nuvem (Zero Custo)
# Compatível com: Ubuntu 20.04/22.04/24.04, Debian 11/12, Oracle Linux 8/9
# Ideal para: Oracle Cloud Free Tier (Gratuito Vitalício) ou VPS Hetzner/DigitalOcean
# ==============================================================================

set -e

echo "=========================================================="
echo "🛡️  FLUX VPN — Instalando Nó de Conexão Criptografada"
echo "=========================================================="

if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute este script como root (sudo bash deploy_vps_node.sh)"
    exit 1
fi

# 1. Atualiza repositórios e instala dependências básicas
apt-get update -y
apt-get install -y wireguard qrencode curl iptables-persistent

# 2. Habilita IP Forwarding no Kernel
echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/99-fluxvpn.conf
echo "net.ipv6.conf.all.forwarding = 1" >> /etc/sysctl.d/99-fluxvpn.conf
sysctl -p /etc/sysctl.d/99-fluxvpn.conf

# 3. Detecta IP público e interface de rede principal
SERVER_PUB_IP=$(curl -4 -s https://api.ipify.org)
DEFAULT_INTERFACE=$(ip route get 8.8.8.8 | awk -- '{print $5}')
WG_PORT=51820

# 4. Gera chaves criptográficas do Servidor
cd /etc/wireguard
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
SERVER_PRIV_KEY=$(cat server_private.key)
SERVER_PUB_KEY=$(cat server_public.key)

# 5. Gera chaves criptográficas do Cliente FLUX VPN
wg genkey | tee client_private.key | wg pubkey > client_public.key
CLIENT_PRIV_KEY=$(cat client_private.key)
CLIENT_PUB_KEY=$(cat client_public.key)

# 6. Cria configuração do Servidor (wg0.conf)
cat <<EOF > /etc/wireguard/wg0.conf
[Interface]
Address = 10.66.66.1/24, fd42:42:42::1/64
ListenPort = $WG_PORT
PrivateKey = $SERVER_PRIV_KEY
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o $DEFAULT_INTERFACE -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o $DEFAULT_INTERFACE -j MASQUERADE

[Peer]
PublicKey = $CLIENT_PUB_KEY
AllowedIPs = 10.66.66.2/32, fd42:42:42::2/128
EOF

# 7. Inicia e habilita o serviço no boot
systemctl enable wg-quick@wg0
systemctl restart wg-quick@wg0

# 8. Gera o perfil de configuração pronto para o FLUX VPN
cat <<EOF > /root/FLUX-EUA-NovaYork.conf
[Interface]
# FLUX VPN — Servidor Privado Dedicado
PrivateKey = $CLIENT_PRIV_KEY
Address = 10.66.66.2/32, fd42:42:42::2/128
DNS = 1.1.1.1, 1.0.0.1

[Peer]
PublicKey = $SERVER_PUB_KEY
Endpoint = $SERVER_PUB_IP:$WG_PORT
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

echo "=========================================================="
echo "✅ NÓ FLUX VPN ATIVADO COM SUCESSO!"
echo "IP do Servidor: $SERVER_PUB_IP"
echo "Porta: $WG_PORT"
echo "=========================================================="
echo ""
echo "Copie o conteúdo abaixo e salve na pasta 'profiles/FLUX-EUA-NovaYork.conf' do seu FLUX VPN:"
echo "----------------------------------------------------------"
cat /root/FLUX-EUA-NovaYork.conf
echo "----------------------------------------------------------"
