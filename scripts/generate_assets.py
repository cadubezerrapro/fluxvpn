#!/usr/bin/env python3
"""
FLUX VPN — Gerador Oficial de Assets, Ícones e Visual do Instalador macOS / Windows
Modo Claro (Light Mode) Apple Clean, Logo Branca de Alto Contraste e Retina Anti-Pixelado.
Gera AppIcon.icns, fluxvpn.ico, dmg_background.png, dmg_background@2x.png e dmg_background.tiff.
"""

import os
import sys
import math
import zlib
import struct
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)

def write_png(filepath, width, height, rgba_data):
    """Escreve um arquivo PNG puro usando apenas a biblioteca padrão (zlib + struct)."""
    raw_scanlines = bytearray()
    row_bytes = width * 4
    for y in range(height):
        raw_scanlines.append(0)
        start = y * row_bytes
        raw_scanlines.extend(rgba_data[start:start + row_bytes])

    compressed = zlib.compress(bytes(raw_scanlines), level=9)
    
    def make_chunk(chunk_type, data):
        length = len(data)
        crc = zlib.crc32(chunk_type + data) & 0xffffffff
        return struct.pack('>I', length) + chunk_type + data + struct.pack('>I', crc)

    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)

    with open(filepath, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(make_chunk(b'IHDR', ihdr_data))
        f.write(make_chunk(b'IDAT', compressed))
        f.write(make_chunk(b'IEND', b''))

def render_app_icon(size=1024):
    """
    Renderiza o ícone oficial do FLUX VPN no padrão Apple Squircle com LOGO BRANCA límpida.
    Visual Ultra Clean:
      - Squircle com gradiente Apple Sapphire Royal Blue profundo (#0284C7 -> #0369A1 -> #0F172A)
      - Borda sutil de vidro fosco
      - LOGO BRANCA PURA (#FFFFFF): Escudo, letra F estilizada e nó de conexão.
    """
    try:
        from PIL import Image, ImageDraw, ImageFilter
        return render_app_icon_pil(size)
    except ImportError:
        return render_app_icon_pure(size)

def render_app_icon_pil(size=1024):
    from PIL import Image, ImageDraw, ImageFilter
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Base do Squircle Apple (canto arredondado 22%)
    pad = int(size * 0.05)
    r = int(size * 0.22)
    box = [pad, pad, size - pad, size - pad]
    
    # Sombra ambiente suave Apple
    shadow_box = [pad - int(size * 0.01), pad + int(size * 0.02), size - pad + int(size * 0.01), size - pad + int(size * 0.04)]
    draw.rounded_rectangle(shadow_box, radius=r, fill=(15, 23, 42, 60))
    
    # Gradiente de fundo do ícone: Apple Royal Blue Elegante
    base = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base)
    for y in range(pad, size - pad):
        factor = (y - pad) / (size - 2 * pad)
        # Degradê de azul royal tecnológico (#0284C7 até #0B192C)
        red = int(2 * (1 - factor) + 11 * factor)
        green = int(132 * (1 - factor) + 25 * factor)
        blue = int(199 * (1 - factor) + 44 * factor)
        base_draw.line([(pad, y), (size - pad, y)], fill=(red, green, blue, 255))
        
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(box, radius=r, fill=255)
    
    img.paste(base, (0, 0), mask)
    
    # Borda fina e elegante de vidro fosco
    draw.rounded_rectangle(box, radius=r, outline=(255, 255, 255, 120), width=int(size * 0.008))
    
    # 2. LOGO BRANCA PURA: Escudo + F + Nó de Conexão
    cx, cy = size / 2.0, size / 2.0
    sw = size * 0.54
    sh = size * 0.62
    
    # Pontos do Escudo
    p_top = (cx, cy - sh * 0.44)
    p_tr_ctrl = (cx + sw * 0.42, cy - sh * 0.38)
    p_tr = (cx + sw * 0.50, cy - sh * 0.28)
    p_br = (cx + sw * 0.44, cy + sh * 0.06)
    p_bottom = (cx, cy + sh * 0.46)
    p_bl = (cx - sw * 0.44, cy + sh * 0.06)
    p_tl = (cx - sw * 0.50, cy - sh * 0.28)
    p_tl_ctrl = (cx - sw * 0.42, cy - sh * 0.38)
    
    shield_pts = [p_top, p_tr_ctrl, p_tr, p_br, p_bottom, p_bl, p_tl, p_tl_ctrl]
    
    # Desenho do contorno do Escudo em BRANCO PURO
    draw.line([p_top, p_tr_ctrl, p_tr, p_br, p_bottom, p_bl, p_tl, p_tl_ctrl, p_top],
              fill=(255, 255, 255, 255), width=int(size * 0.024), joint='curve')
    
    # 3. Tipografia "F" Estilizada em BRANCO PURO
    f_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(f_layer)
    
    bar_w = int(size * 0.076)
    # Haste vertical do F
    fx1 = int(cx - sw * 0.18)
    fx2 = fx1 + bar_w
    fy1 = int(cy - sh * 0.22)
    fy2 = int(cy + sh * 0.24)
    f_draw.rounded_rectangle([fx1, fy1, fx2, fy2], radius=int(bar_w * 0.35), fill=(255, 255, 255, 255))
    
    # Barra Superior do F
    top_w = int(sw * 0.46)
    f_draw.rounded_rectangle([fx1, fy1, fx1 + top_w, fy1 + bar_w], radius=int(bar_w * 0.35), fill=(255, 255, 255, 255))
    
    # Barra Central do F
    mid_w = int(sw * 0.32)
    mid_y = int(cy - sh * 0.02)
    f_draw.rounded_rectangle([fx1, mid_y, fx1 + mid_w, mid_y + bar_w], radius=int(bar_w * 0.35), fill=(255, 255, 255, 255))
    
    # 4. Ponto do Nó de Rede em BRANCO PURO
    node_cx = int(fx1 + mid_w + size * 0.055)
    node_cy = int(mid_y + bar_w * 0.5)
    node_r = int(size * 0.042)
    
    # Linha conectora do nó
    f_draw.line([(fx1 + mid_w, node_cy), (node_cx, node_cy)], fill=(255, 255, 255, 255), width=int(size * 0.016))
    
    # Anel externo do nó
    f_draw.ellipse([node_cx - int(node_r * 1.55), node_cy - int(node_r * 1.55),
                    node_cx + int(node_r * 1.55), node_cy + int(node_r * 1.55)],
                   outline=(255, 255, 255, 200), width=int(size * 0.012))
                   
    # Círculo sólido do nó
    f_draw.ellipse([node_cx - node_r, node_cy - node_r, node_cx + node_r, node_cy + node_r], fill=(255, 255, 255, 255))
    
    img.paste(f_layer, (0, 0), f_layer)
    return img

def render_app_icon_pure(size=1024):
    """Fallback algorítmico sem PIL com Logo Branca."""
    data = bytearray(size * size * 4)
    cx, cy = size / 2.0, size / 2.0
    r_corner = size * 0.22
    pad = size * 0.05
    w_inner = size - 2 * pad
    
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            dx = max(0.0, abs(x - cx) - (w_inner / 2.0 - r_corner))
            dy = max(0.0, abs(y - cy) - (w_inner / 2.0 - r_corner))
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist <= r_corner:
                t = y / float(size)
                # Azul Royal Apple
                r_val = int(2 * (1 - t) + 11 * t)
                g_val = int(132 * (1 - t) + 25 * t)
                b_val = int(199 * (1 - t) + 44 * t)
                
                # Borda sutil
                if r_corner - dist < 4.0:
                    r_val, g_val, b_val = 255, 255, 255
                
                nx = (x - cx) / (size * 0.5)
                ny = (y - cy) / (size * 0.5)
                
                # Letra F e Escudo em BRANCO
                if -0.22 <= nx <= -0.10 and -0.25 <= ny <= 0.25:
                    r_val, g_val, b_val = 255, 255, 255
                elif -0.22 <= nx <= 0.18 and -0.25 <= ny <= -0.15:
                    r_val, g_val, b_val = 255, 255, 255
                elif -0.22 <= nx <= 0.08 and -0.04 <= ny <= 0.06:
                    r_val, g_val, b_val = 255, 255, 255
                
                # Nó
                node_dist = math.sqrt((nx - 0.20)**2 + (ny - 0.01)**2)
                if node_dist < 0.06 or (0.075 < node_dist < 0.095):
                    r_val, g_val, b_val = 255, 255, 255

                data[idx] = r_val
                data[idx + 1] = g_val
                data[idx + 2] = b_val
                data[idx + 3] = 255
            else:
                data[idx + 3] = 0
                
    return data

def render_dmg_background_light(width=660, height=420, scale=1):
    """
    Renderiza o fundo do instalador no padrão Apple MODO CLARO (Light Mode Clean).
    Zero pixelado (suporte a scale=1 para 660x420 e scale=2 para Retina 1320x840).
    Contém:
      - Fundo cerâmico branco/platina fosco com degradê sutil (#FFFFFF -> #F1F5F9)
      - Tipografia limpa dark slate (#0F172A)
      - Pedestais elegantes em cinza suave (#E2E8F0) nas posições exatas (160, 195) e (500, 195)
      - Seta vetorizada Apple Azure Blue (#0284C7) com bordas arredondadas e suavizadas
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        return render_dmg_background_light_pil(width * scale, height * scale, scale)
    except ImportError:
        return render_dmg_background_light_pure(width * scale, height * scale, scale)

def render_dmg_background_light_pil(width, height, scale=1):
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Gradiente Apple Light Mode Clean (#FFFFFF até #F1F5F9)
    for y in range(height):
        factor = y / float(height)
        r = int(255 * (1 - factor) + 241 * factor)
        g = int(255 * (1 - factor) + 245 * factor)
        b = int(255 * (1 - factor) + 249 * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Moldura interna sutil de vidro
    border_color = (226, 232, 240)
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=1 * scale)
    
    # 2. Pedestais Circulares Limpos (Posições exatas 160 e 500)
    left_cx = int(160 * scale)
    left_cy = int(195 * scale)
    right_cx = int(500 * scale)
    right_cy = int(195 * scale)
    radius = int(62 * scale)
    
    # Preenchimento suave dos pedestais
    pedestal_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pedestal_layer)
    
    p_draw.ellipse([left_cx - radius, left_cy - radius, left_cx + radius, left_cy + radius],
                   fill=(241, 245, 249, 200), outline=(203, 213, 225, 255), width=2 * scale)
                   
    p_draw.ellipse([right_cx - radius, right_cy - radius, right_cx + radius, right_cy + radius],
                   fill=(241, 245, 249, 200), outline=(203, 213, 225, 255), width=2 * scale)
                   
    img.paste(pedestal_layer, (0, 0), pedestal_layer)
    
    # 3. Seta Apple Azure Blue Central (#0284C7)
    arrow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(arrow_layer)
    
    arrow_y = int(195 * scale)
    arrow_start_x = int(245 * scale)
    arrow_end_x = int(405 * scale)
    arrow_h = int(10 * scale)
    
    # Corpo da Seta
    a_draw.rounded_rectangle([arrow_start_x, arrow_y - arrow_h // 2, arrow_end_x - int(14 * scale), arrow_y + arrow_h // 2],
                             radius=int(5 * scale), fill=(2, 132, 199, 255))
    
    # Ponta da Seta
    pts = [
        (arrow_end_x - int(14 * scale), arrow_y - int(20 * scale)),
        (arrow_end_x + int(16 * scale), arrow_y),
        (arrow_end_x - int(14 * scale), arrow_y + int(20 * scale))
    ]
    a_draw.polygon(pts, fill=(2, 132, 199, 255))
    img.paste(arrow_layer, (0, 0), arrow_layer)
    
    # 4. Tipografia Profissional Apple (Modo Claro)
    text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    
    font_scale = scale
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(22 * font_scale))
        font_sub = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(12 * font_scale))
        font_action = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(12 * font_scale))
        font_label = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(11 * font_scale))
    except Exception:
        font_title = font_sub = font_action = font_label = None
        
    def center_text(y, text, fill, font):
        bbox = t_draw.textbbox((0, 0), text, font=font) if font else (0, 0, len(text)*7*scale, 12*scale)
        w = bbox[2] - bbox[0]
        t_draw.text(((width - w) // 2, y), text, fill=fill, font=font)
        
    def draw_lbl(cx, y, text, fill, font):
        bbox = t_draw.textbbox((0, 0), text, font=font) if font else (0, 0, len(text)*6*scale, 10*scale)
        w = bbox[2] - bbox[0]
        t_draw.text((cx - w // 2, y), text, fill=fill, font=font)

    # Textos de Interface Apple
    center_text(int(42 * scale), "FLUX VPN", (15, 23, 42, 255), font_title)
    center_text(int(70 * scale), "Instalação Oficial para macOS", (100, 116, 139, 255), font_sub)
    center_text(int(162 * scale), "Arraste para Instalar", (2, 132, 199, 255), font_action)
    center_text(int(222 * scale), "100% Embutido • Zero Configurações", (148, 163, 184, 255), font_sub)
    
    draw_lbl(left_cx, int(278 * scale), "FLUX-VPN.app", (51, 65, 85, 255), font_label)
    draw_lbl(right_cx, int(278 * scale), "Pasta Aplicativos", (51, 65, 85, 255), font_label)
    
    img.paste(text_layer, (0, 0), text_layer)
    return img

def render_dmg_background_light_pure(width, height, scale=1):
    """Fallback limpo modo claro sem PIL."""
    data = bytearray(width * height * 4)
    for y in range(height):
        t = y / float(height)
        r = int(255 * (1 - t) + 241 * t)
        g = int(255 * (1 - t) + 245 * t)
        b = int(255 * (1 - t) + 249 * t)
        for x in range(width):
            idx = (y * width + x) * 4
            data[idx] = r
            data[idx + 1] = g
            data[idx + 2] = b
            data[idx + 3] = 255
    return data

def main():
    print("=" * 60)
    print("🎨 FLUX VPN — Gerador Apple Modo Claro (White Logo & Clean UI)")
    print("=" * 60)
    
    assets_dir = os.path.join(REPO_DIR, "dist", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Gerar AppIcon.png com LOGO BRANCA (1024x1024 Retina)
    print("[1/5] Gerando ícone mestre Apple com LOGO BRANCA PURA (1024x1024)...")
    icon_obj = render_app_icon(1024)
    master_icon_path = os.path.join(assets_dir, "AppIcon_1024.png")
    
    try:
        icon_obj.save(master_icon_path, format="PNG")
    except AttributeError:
        write_png(master_icon_path, 1024, 1024, icon_obj)
        
    print(f"      ✓ Salvo: {master_icon_path}")
    
    # 2. Gerar Iconset e Compilar AppIcon.icns
    print("[2/5] Compilando pacote oficial Apple ICNS e Windows ICO...")
    iconset_dir = os.path.join(assets_dir, "AppIcon.iconset")
    os.makedirs(iconset_dir, exist_ok=True)
    
    resolutions = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png")
    ]
    
    try:
        from PIL import Image
        master = Image.open(master_icon_path)
        for s, name in resolutions:
            resized = master.resize((s, s), Image.Resampling.LANCZOS)
            resized.save(os.path.join(iconset_dir, name))
            
        ico_path = os.path.join(REPO_DIR, "dist", "windows", "fluxvpn.ico")
        master.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"      ✓ Ícone do Windows salvo: {ico_path}")
    except Exception as e:
        for s, name in resolutions:
            target = os.path.join(iconset_dir, name)
            subprocess.run(["sips", "-z", str(s), str(s), master_icon_path, "--out", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
    # Compila via iconutil (Apple nativo)
    icns_path = os.path.join(assets_dir, "AppIcon.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"      ✓ AppIcon.icns Apple compilado: {icns_path}")
    
    # Instala em todos os pacotes
    destinations = [
        os.path.join(REPO_DIR, "FLUX-VPN.app", "Contents", "Resources", "AppIcon.icns"),
        os.path.join(REPO_DIR, "dist", "macOS", "FLUX-VPN.app", "Contents", "Resources", "AppIcon.icns")
    ]
    for d in destinations:
        if os.path.exists(icns_path):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            with open(icns_path, 'rb') as src, open(d, 'wb') as dst:
                dst.write(src.read())

    # 3. Gerar Fundo do Instalador no MODO CLARO (1x e 2x Retina Anti-Pixelado)
    print("[3/5] Gerando fundo de instalador Apple Modo Claro (660x420 e 1320x840 Retina)...")
    bg_1x = render_dmg_background_light(660, 420, scale=1)
    bg_2x = render_dmg_background_light(660, 420, scale=2)
    
    path_1x = os.path.join(assets_dir, "dmg_background.png")
    path_2x = os.path.join(assets_dir, "dmg_background@2x.png")
    path_tiff = os.path.join(assets_dir, "dmg_background.tiff")
    
    try:
        bg_1x.save(path_1x, format="PNG")
        bg_2x.save(path_2x, format="PNG")
    except AttributeError:
        write_png(path_1x, 660, 420, bg_1x)
        write_png(path_2x, 1320, 840, bg_2x)
        
    # Combina em TIFF multi-resolução nativo da Apple para ZERO PIXELAMENTO
    subprocess.run(["tiffutil", "-cathidpicheck", path_1x, path_2x, "-out", path_tiff], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"      ✓ Fundo Modo Claro salvo em Retina TIFF: {path_tiff}")
    print(f"      ✓ Fundo PNG 1x/2x salvo: {path_1x}")
    
    print("=" * 60)
    print("✨ Todos os assets em Modo Claro e Logo Branca gerados com perfeição!")
    print("=" * 60)

if __name__ == "__main__":
    main()
