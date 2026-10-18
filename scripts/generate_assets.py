#!/usr/bin/env python3
"""
FLUX VPN — Gerador Oficial de Assets, Ícones e Visual do Instalador macOS / Windows
Gera AppIcon.icns (Apple Retina), fluxvpn.ico (Windows) e dmg_background.png (DMG Profissional).
Zero dependências externas obrigatórias (usa Pillow se disponível, ou renderizador puro em Python + zlib).
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
        raw_scanlines.append(0)  # Filtro 0 (None)
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
    Renderiza o ícone oficial do FLUX VPN no padrão Apple Squircle com iluminação cibernética.
    Prioriza a imagem de alta fidelidade gerada com máscara de cantos arredondados macOS.
    """
    candidate_paths = [
        "/Users/cadubezerra/.gemini/antigravity-ide/brain/eb4bbabb-1f5b-4f8a-a7a9-3f3e29a76295/flux_app_icon_master_1792341409439.jpg",
        os.path.join(REPO_DIR, "dist", "assets", "flux_app_icon_master.jpg")
    ]
    
    for c_path in candidate_paths:
        if os.path.exists(c_path):
            try:
                from PIL import Image, ImageDraw
                raw_img = Image.open(c_path).convert('RGBA')
                if raw_img.size != (size, size):
                    raw_img = raw_img.resize((size, size), Image.Resampling.LANCZOS)
                
                # Aplica máscara de squircle para tornar o fundo externo 100% transparente
                mask = Image.new('L', (size, size), 0)
                mask_draw = ImageDraw.Draw(mask)
                pad = int(size * 0.096)
                r = int(size * 0.22)
                mask_draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=r, fill=255)
                
                result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                result.paste(raw_img, (0, 0), mask)
                return result
            except Exception as e:
                print(f"      [Info] Erro ao carregar mestre IA: {e}")
                
    try:
        from PIL import Image, ImageDraw, ImageFilter
        return render_app_icon_pil(size)
    except ImportError:
        return render_app_icon_pure(size)

def render_app_icon_pil(size=1024):
    from PIL import Image, ImageDraw, ImageFilter
    
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Base do Squircle Apple (canto arredondado ~22% do tamanho)
    pad = int(size * 0.05)
    r = int(size * 0.22)
    box = [pad, pad, size - pad, size - pad]
    
    # Glow externo sutil
    glow_box = [pad - int(size * 0.02), pad - int(size * 0.02), size - pad + int(size * 0.02), size - pad + int(size * 0.02)]
    draw.rounded_rectangle(glow_box, radius=r + int(size * 0.02), fill=(14, 165, 233, 40))
    
    # Corpo do Squircle - Gradiente Vertical Dark Obsidian
    base = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base)
    for y in range(pad, size - pad):
        factor = (y - pad) / (size - 2 * pad)
        red = int(10 * (1 - factor) + 5 * factor)
        green = int(15 * (1 - factor) + 8 * factor)
        blue = int(26 * (1 - factor) + 16 * factor)
        base_draw.line([(pad, y), (size - pad, y)], fill=(red, green, blue, 255))
        
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(box, radius=r, fill=255)
    
    img.paste(base, (0, 0), mask)
    
    # Borda sutil de neon ciano
    draw.rounded_rectangle(box, radius=r, outline=(14, 165, 233, 160), width=int(size * 0.008))
    
    # 2. Escudo Cibernético Central
    cx, cy = size / 2.0, size / 2.0
    sw = size * 0.58
    sh = size * 0.65
    
    # Pontos do Escudo
    p_top = (cx, cy - sh * 0.44)
    p_tr_ctrl = (cx + sw * 0.42, cy - sh * 0.38)
    p_tr = (cx + sw * 0.50, cy - sh * 0.30)
    p_br = (cx + sw * 0.45, cy + sh * 0.05)
    p_bottom = (cx, cy + sh * 0.46)
    p_bl = (cx - sw * 0.45, cy + sh * 0.05)
    p_tl = (cx - sw * 0.50, cy - sh * 0.30)
    p_tl_ctrl = (cx - sw * 0.42, cy - sh * 0.38)
    
    shield_pts = [p_top, p_tr_ctrl, p_tr, p_br, p_bottom, p_bl, p_tl, p_tl_ctrl]
    
    # Camada de Glow do Escudo
    shield_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shield_layer)
    
    # Preenchimento do Escudo com Gradiente Royal Blue -> Cyan
    s_draw.polygon(shield_pts, fill=(2, 132, 199, 230))
    
    # Gradiente vertical no escudo
    shield_mask = Image.new('L', (size, size), 0)
    sm_draw = ImageDraw.Draw(shield_mask)
    sm_draw.polygon(shield_pts, fill=255)
    
    shield_grad = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    sg_draw = ImageDraw.Draw(shield_grad)
    top_y = int(cy - sh * 0.44)
    bot_y = int(cy + sh * 0.46)
    for y in range(top_y, bot_y):
        t = (y - top_y) / max(1, (bot_y - top_y))
        # #0284C7 -> #0EA5E9 -> #06B6D4
        r_c = int(2 * (1-t) + 6 * t)
        g_c = int(132 * (1-t) + 182 * t)
        b_c = int(199 * (1-t) + 212 * t)
        sg_draw.line([(0, y), (size, y)], fill=(r_c, g_c, b_c, 240))
        
    img.paste(shield_grad, (0, 0), shield_mask)
    
    # Borda brilhante do escudo
    draw.line([p_top, p_tr_ctrl, p_tr, p_br, p_bottom, p_bl, p_tl, p_tl_ctrl, p_top], fill=(6, 182, 212, 255), width=int(size * 0.015), joint='curve')
    
    # 3. Tipografia "F" Estilizada Central em Branco e Ciano
    f_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(f_layer)
    
    bar_w = int(size * 0.075)
    # Haste vertical do F
    fx1 = int(cx - sw * 0.18)
    fx2 = fx1 + bar_w
    fy1 = int(cy - sh * 0.22)
    fy2 = int(cy + sh * 0.26)
    f_draw.rounded_rectangle([fx1, fy1, fx2, fy2], radius=int(bar_w * 0.4), fill=(255, 255, 255, 255))
    
    # Barra Superior do F
    top_w = int(sw * 0.44)
    f_draw.rounded_rectangle([fx1, fy1, fx1 + top_w, fy1 + bar_w], radius=int(bar_w * 0.4), fill=(255, 255, 255, 255))
    
    # Barra Central do F
    mid_w = int(sw * 0.32)
    mid_y = int(cy - sh * 0.02)
    f_draw.rounded_rectangle([fx1, mid_y, fx1 + mid_w, mid_y + bar_w], radius=int(bar_w * 0.4), fill=(255, 255, 255, 255))
    
    # 4. Ponto do Nó de Conexão (Network Node) com Anel de Pulso
    node_cx = int(fx1 + mid_w + size * 0.06)
    node_cy = int(mid_y + bar_w * 0.5)
    node_r = int(size * 0.045)
    
    # Linha conectando o F ao nó
    f_draw.line([(fx1 + mid_w, node_cy), (node_cx, node_cy)], fill=(255, 255, 255, 255), width=int(size * 0.012))
    
    # Anel externo do nó (pulsing wave)
    f_draw.ellipse([node_cx - int(node_r * 1.6), node_cy - int(node_r * 1.6),
                    node_cx + int(node_r * 1.6), node_cy + int(node_r * 1.6)],
                   outline=(6, 182, 212, 200), width=int(size * 0.01))
                   
    # Círculo sólido do nó
    f_draw.ellipse([node_cx - node_r, node_cy - node_r, node_cx + node_r, node_cy + node_r], fill=(255, 255, 255, 255))
    
    img.paste(f_layer, (0, 0), f_layer)
    return img

def render_app_icon_pure(size=1024):
    """Renderizador puramente algorítmico em memória sem PIL."""
    data = bytearray(size * size * 4)
    cx, cy = size / 2.0, size / 2.0
    r_corner = size * 0.22
    pad = size * 0.05
    w_inner = size - 2 * pad
    
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 4
            # Distância para squircle
            dx = max(0.0, abs(x - cx) - (w_inner / 2.0 - r_corner))
            dy = max(0.0, abs(y - cy) - (w_inner / 2.0 - r_corner))
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist <= r_corner:
                t = y / float(size)
                # Fundo Obsidian escuro com leve azul
                r_val = int(10 * (1 - t) + 4 * t)
                g_val = int(16 * (1 - t) + 8 * t)
                b_val = int(28 * (1 - t) + 16 * t)
                
                # Borda neon
                if r_corner - dist < 6.0:
                    r_val, g_val, b_val = 14, 165, 233
                
                # Escudo interno
                nx = (x - cx) / (size * 0.5)
                ny = (y - cy) / (size * 0.5)
                if -0.6 < nx < 0.6 and -0.7 < ny < 0.7:
                    # Formato aproximado do escudo
                    shield_bound = 0.55 * (1.0 - max(0.0, ny) * 0.6)
                    if abs(nx) < shield_bound and ny > -0.6:
                        # Cor do escudo (#0284C7 até #06B6D4)
                        st = (ny + 0.6) / 1.3
                        r_val = int(2 * (1 - st) + 6 * st)
                        g_val = int(132 * (1 - st) + 182 * st)
                        b_val = int(199 * (1 - st) + 212 * st)
                        
                        # Letra F simplificada
                        if -0.25 <= nx <= -0.12 and -0.35 <= ny <= 0.35:
                            r_val, g_val, b_val = 255, 255, 255
                        elif -0.25 <= nx <= 0.20 and -0.35 <= ny <= -0.22:
                            r_val, g_val, b_val = 255, 255, 255
                        elif -0.25 <= nx <= 0.10 and -0.05 <= ny <= 0.08:
                            r_val, g_val, b_val = 255, 255, 255
                        # Nó
                        node_dist = math.sqrt((nx - 0.25)**2 + (ny - 0.015)**2)
                        if node_dist < 0.08:
                            r_val, g_val, b_val = 255, 255, 255
                        elif 0.09 < node_dist < 0.12:
                            r_val, g_val, b_val = 6, 182, 212

                data[idx] = r_val
                data[idx + 1] = g_val
                data[idx + 2] = b_val
                data[idx + 3] = 255
            else:
                data[idx + 3] = 0
                
    return data

def render_dmg_background(width=660, height=420):
    """
    Renderiza o fundo profissional do instalador DMG em 660x420 (escala 1:1 nativa do Finder).
    Contém:
      - Fundo Dark Titanium com grid suave
      - Header "FLUX VPN — Instalação Oficial macOS"
      - Pedestal iluminado para FLUX-VPN.app em (160, 195)
      - Pedestal iluminado para Applications em (500, 195)
      - Seta futurista neon central (de 245 a 415, y=195)
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        return render_dmg_background_pil(width, height)
    except ImportError:
        return render_dmg_background_pure(width, height)

def render_dmg_background_pil(width=660, height=420):
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.new('RGB', (width, height), (9, 13, 22))
    draw = ImageDraw.Draw(img)
    
    # 1. Gradiente de Fundo Dark Obsidian
    for y in range(height):
        factor = y / float(height)
        r = int(10 * (1 - factor) + 5 * factor)
        g = int(15 * (1 - factor) + 8 * factor)
        b = int(26 * (1 - factor) + 14 * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # 2. Tech Grid Sutil
    grid_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_img)
    for x in range(0, width, 30):
        g_draw.line([(x, 0), (x, height)], fill=(14, 165, 233, 10))
    for y in range(0, height, 30):
        g_draw.line([(0, y), (width, y)], fill=(14, 165, 233, 10))
    img.paste(grid_img, (0, 0), grid_img)
    
    # 3. Pedestais / Alvos com Brilho Circular Exatos
    left_cx, left_cy = 160, 195
    right_cx, right_cy = 500, 195
    radius = 65
    
    # Brilho esquerdo (App)
    for r in range(radius + 25, radius, -1):
        alpha = int(45 * (1 - (r - radius) / 25.0))
        g_draw.ellipse([left_cx - r, left_cy - r, left_cx + r, left_cy + r], outline=(14, 165, 233, alpha), width=1)
        
    # Brilho direito (Applications)
    for r in range(radius + 25, radius, -1):
        alpha = int(45 * (1 - (r - radius) / 25.0))
        g_draw.ellipse([right_cx - r, right_cy - r, right_cx + r, right_cy + r], outline=(6, 182, 212, alpha), width=1)
    
    # Círculo base iluminado
    g_draw.ellipse([left_cx - radius, left_cy - radius, left_cx + radius, left_cy + radius], outline=(14, 165, 233, 140), width=2)
    g_draw.ellipse([right_cx - radius, right_cy - radius, right_cx + radius, right_cy + radius], outline=(6, 182, 212, 140), width=2)
    img.paste(grid_img, (0, 0), grid_img)
    
    # 4. Seta Futurista Luminosa Central (de x=245 até x=415, y=195)
    arrow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(arrow_layer)
    
    arrow_y = 195
    arrow_start_x = 245
    arrow_end_x = 405
    arrow_shaft_h = 12
    
    # Corpo da Seta
    a_draw.rounded_rectangle([arrow_start_x, arrow_y - arrow_shaft_h // 2, arrow_end_x - 16, arrow_y + arrow_shaft_h // 2], radius=6, fill=(14, 165, 233, 230))
    
    # Ponta da Seta
    pts = [
        (arrow_end_x - 16, arrow_y - 24),
        (arrow_end_x + 18, arrow_y),
        (arrow_end_x - 16, arrow_y + 24)
    ]
    a_draw.polygon(pts, fill=(6, 182, 212, 255))
    a_draw.line(pts, fill=(255, 255, 255, 240), width=2, joint='curve')
    
    img.paste(arrow_layer, (0, 0), arrow_layer)
    
    # 5. Textos e Identidade Visual no Fundo
    text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    
    # Carrega fontes padrão ou básicas
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 22)
        font_sub = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 12)
        font_label = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 11)
    except Exception:
        font_title = font_sub = font_label = None
        
    def center_text(y, text, fill, font):
        bbox = t_draw.textbbox((0, 0), text, font=font) if font else (0, 0, len(text)*7, 12)
        w = bbox[2] - bbox[0]
        t_draw.text(((width - w) // 2, y), text, fill=fill, font=font)
        
    def draw_lbl(cx, y, text, fill, font):
        bbox = t_draw.textbbox((0, 0), text, font=font) if font else (0, 0, len(text)*6, 10)
        w = bbox[2] - bbox[0]
        t_draw.text((cx - w // 2, y), text, fill=fill, font=font)

    center_text(35, "FLUX VPN", (255, 255, 255, 255), font_title)
    center_text(65, "Instalação Oficial para macOS", (14, 165, 233, 230), font_sub)
    center_text(160, "ARRAS TE PARA INSTALAR", (255, 255, 255, 200), font_label)
    center_text(220, "100% Embutido • Zero Logs", (6, 182, 212, 180), font_label)
    
    draw_lbl(left_cx, 285, "Arraste o FLUX VPN", (14, 165, 233, 220), font_label)
    draw_lbl(right_cx, 285, "Solte em Aplicativos", (6, 182, 212, 220), font_label)
    
    img.paste(text_layer, (0, 0), text_layer)
    return img

def render_dmg_background_pure(width=1320, height=840):
    """Fundo puro para caso PIL não esteja instalado."""
    data = bytearray(width * height * 4)
    for y in range(height):
        t = y / float(height)
        r = int(9 * (1 - t) + 4 * t)
        g = int(14 * (1 - t) + 7 * t)
        b = int(24 * (1 - t) + 12 * t)
        for x in range(width):
            idx = (y * width + x) * 4
            # Grid
            if x % 60 == 0 or y % 60 == 0:
                data[idx] = min(255, r + 8)
                data[idx + 1] = min(255, g + 16)
                data[idx + 2] = min(255, b + 30)
            else:
                data[idx] = r
                data[idx + 1] = g
                data[idx + 2] = b
            data[idx + 3] = 255
            
            # Seta horizontal
            if 500 <= x <= 800 and 405 <= y <= 435:
                data[idx] = 14
                data[idx + 1] = 165
                data[idx + 2] = 233
    return data

def main():
    print("=" * 60)
    print("🎨 FLUX VPN — Gerador Oficial de Identidade Visual e Instalador")
    print("=" * 60)
    
    assets_dir = os.path.join(REPO_DIR, "dist", "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Gerar AppIcon.png (1024x1024)
    print("[1/5] Gerando ícone mestre de alta resolução (1024x1024 Retina)...")
    icon_obj = render_app_icon(1024)
    master_icon_path = os.path.join(assets_dir, "AppIcon_1024.png")
    
    try:
        icon_obj.save(master_icon_path, format="PNG")
    except AttributeError:
        write_png(master_icon_path, 1024, 1024, icon_obj)
        
    print(f"      ✓ Salvo: {master_icon_path}")
    
    # 2. Gerar Iconset e Compilar AppIcon.icns (para macOS)
    print("[2/5] Gerando pasta Apple Iconset e compilando AppIcon.icns...")
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
            
        # Também gera o ícone para Windows (.ico)
        ico_path = os.path.join(REPO_DIR, "dist", "windows", "fluxvpn.ico")
        master.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        print(f"      ✓ Ícone do Windows salvo: {ico_path}")
    except Exception as e:
        print(f"      [Info] Usando sips/builtin para redimensionamento ({e})")
        for s, name in resolutions:
            target = os.path.join(iconset_dir, name)
            subprocess.run(["sips", "-z", str(s), str(s), master_icon_path, "--out", target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Gerador nativo de .ico sem dependências
        ico_path = os.path.join(REPO_DIR, "dist", "windows", "fluxvpn.ico")
        ico_sources = [
            (16, os.path.join(iconset_dir, "icon_16x16.png")),
            (32, os.path.join(iconset_dir, "icon_32x32.png")),
            (64, os.path.join(iconset_dir, "icon_32x32@2x.png")),
            (128, os.path.join(iconset_dir, "icon_128x128.png")),
            (256, os.path.join(iconset_dir, "icon_256x256.png"))
        ]
        entries = []
        raw_images = []
        offset = 6 + len(ico_sources) * 16
        for sz, p in ico_sources:
            if os.path.exists(p):
                with open(p, 'rb') as f:
                    img_data = f.read()
                w_b = 0 if sz >= 256 else sz
                h_b = 0 if sz >= 256 else sz
                entry = struct.pack('<BBBBHHII', w_b, h_b, 0, 0, 1, 32, len(img_data), offset)
                entries.append(entry)
                raw_images.append(img_data)
                offset += len(img_data)
        if entries:
            header = struct.pack('<HHH', 0, 1, len(entries))
            with open(ico_path, 'wb') as f:
                f.write(header)
                for entry in entries:
                    f.write(entry)
                for img_data in raw_images:
                    f.write(img_data)
            print(f"      ✓ Ícone do Windows salvo via empacotamento nativo: {ico_path}")
            
    # Compila via iconutil (nativo macOS)
    icns_path = os.path.join(assets_dir, "AppIcon.icns")
    res = subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"      ✓ Pacote Apple ICNS gerado com sucesso: {icns_path}")
    else:
        print(f"      [Aviso iconutil]: {res.stderr}")
        
    # Copia o AppIcon.icns para os pacotes do app
    destinations = [
        os.path.join(REPO_DIR, "FLUX-VPN.app", "Contents", "Resources", "AppIcon.icns"),
        os.path.join(REPO_DIR, "dist", "macOS", "FLUX-VPN.app", "Contents", "Resources", "AppIcon.icns")
    ]
    for d in destinations:
        if os.path.exists(icns_path):
            os.makedirs(os.path.dirname(d), exist_ok=True)
            with open(icns_path, 'rb') as src, open(d, 'wb') as dst:
                dst.write(src.read())
            print(f"      ✓ Instalado em: {d}")

    # 3. Gerar Fundo do Instalador DMG
    print("[3/5] Gerando fundo artístico oficial do instalador .DMG...")
    dmg_bg = render_dmg_background(1320, 840)
    dmg_bg_path = os.path.join(assets_dir, "dmg_background.png")
    try:
        dmg_bg.save(dmg_bg_path, format="PNG")
    except AttributeError:
        write_png(dmg_bg_path, 1320, 840, dmg_bg)
    print(f"      ✓ Fundo do DMG salvo: {dmg_bg_path}")
    
    print("=" * 60)
    print("✨ Todos os assets visuais profissionais foram gerados com perfeição!")
    print("=" * 60)

if __name__ == "__main__":
    main()
