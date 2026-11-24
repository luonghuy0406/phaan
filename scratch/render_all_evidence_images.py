#!/usr/bin/env python3
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases"

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
FONT_ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_COURIER = "/System/Library/Fonts/Supplemental/Courier New.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(FONT_ARIAL, size)
        except Exception:
            return ImageFont.load_default()

def add_grain(img, strength=14):
    w, h = img.size
    noise = Image.new('RGB', (w, h))
    npix = noise.load()
    random.seed(101)
    for y in range(h):
        for x in range(w):
            v = random.randint(128 - strength, 128 + strength)
            npix[x, y] = (v, v, v)
    return Image.blend(img, noise, 0.14)

def draw_forensic_backdrop(draw, w, h, bg_color=(45, 48, 52)):
    # Subtle gradient on forensic table
    for y in range(h):
        t = y / h
        r = int(bg_color[0] * (1 - t*0.25))
        g = int(bg_color[1] * (1 - t*0.25))
        b = int(bg_color[2] * (1 - t*0.25))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    
    # Forensic measurement grid (100px lines)
    grid_col = (bg_color[0] + 15, bg_color[1] + 15, bg_color[2] + 15)
    for x in range(0, w, 80):
        draw.line([(x, 0), (x, h)], fill=grid_col, width=1)
    for y in range(0, h, 80):
        draw.line([(0, y), (w, y)], fill=grid_col, width=1)

def draw_scale_bar(draw, x, y, length_cm=15):
    # Standard crime scene scale bar (1cm blocks alternating black/white)
    cm_px = 30
    h_bar = 16
    f_num = get_font(FONT_COURIER, 11)
    for i in range(length_cm):
        col = (240, 240, 240) if i % 2 == 0 else (20, 20, 20)
        draw.rectangle([x + i*cm_px, y, x + (i+1)*cm_px, y + h_bar], fill=col, outline=(30, 30, 30))
        if i % 5 == 0 or i == length_cm - 1:
            draw.text((x + i*cm_px + 2, y + h_bar + 3), f"{i}cm", fill=(200, 200, 200), font=f_num)

def draw_evidence_marker(draw, x, y, label="A"):
    # Yellow triangular folding tent evidence marker
    w_m, h_m = 44, 52
    draw.polygon([(x, y + h_m), (x + w_m//2, y), (x + w_m, y + h_m)], fill=(245, 210, 25), outline=(20, 20, 20), width=2)
    f_lbl = get_font(FONT_HELVETICA, 26)
    draw.text((x + w_m//2, y + h_m//2 + 4), label, fill=(15, 15, 15), font=f_lbl, anchor="mm")

def save_evidence(img, case_id, filename):
    final_img = add_grain(img, 12)
    out_dir = os.path.join(BASE_DIR, case_id, "images")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, filename)
    final_img.save(out_p, "WEBP", quality=86)
    print(f"✓ Saved evidence: {case_id}/images/{filename} ({os.path.getsize(out_p)//1024} KB)")

# ==================== CASE BUILDERS ====================

def gen_buc_thu_dem_tuyet_trang():
    w, h = 800, 600
    
    # d05-buc-thu.webp: 3-page ransom letter on wooden desk
    img = Image.new('RGB', (w, h), (40, 32, 26))
    draw = ImageDraw.Draw(img)
    # Wooden desk planks
    for y in range(0, h, 60):
        draw.line([(0, y), (w, y)], fill=(30, 24, 18), width=3)
    # 3 Pages of white letter
    for idx, (ox, oy, rot) in enumerate([(140, 100, -3), (220, 90, 2), (320, 80, 0)]):
        draw.rectangle([ox, oy, ox + 320, oy + 440], fill=(240, 238, 230), outline=(160, 155, 145), width=2)
        # Typewriter text lines
        for ly in range(oy + 40, oy + 400, 16):
            draw.line([(ox + 30, ly), (ox + 290, ly)], fill=(70, 70, 75), width=2)
    # Red Sharpie note on corner
    draw.line([(480, 120), (600, 140)], fill=(180, 30, 30), width=4)
    draw_evidence_marker(draw, 60, 480, "A")
    draw_scale_bar(draw, 140, 540, 15)
    save_evidence(img, "buc-thu-dem-tuyet-trang", "d05-buc-thu.webp")

    # d11-soi-len.webp: Forensic microscope view of red fibers
    img = Image.new('RGB', (w, h), (15, 16, 20))
    draw = ImageDraw.Draw(img)
    # Microscope circular viewport
    cx, cy, cr = 400, 300, 250
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(210, 220, 230))
    # Microscope crosshair and micrometer reticle
    draw.line([(cx - cr, cy), (cx + cr, cy)], fill=(120, 130, 140), width=1)
    draw.line([(cx, cy - cr), (cx, cy + cr)], fill=(120, 130, 140), width=1)
    for tick in range(-200, 201, 20):
        draw.line([(cx + tick, cy - 6), (cx + tick, cy + 6)], fill=(100, 110, 120), width=1)
        draw.line([(cx - 6, cy + tick), (cx + 6, cy + tick)], fill=(100, 110, 120), width=1)
    # Red wool fibers (crimped microscopic structure)
    for fx in range(250, 550, 40):
        pts = [(fx + random.randint(-15, 15), fy) for fy in range(120, 480, 30)]
        draw.line(pts, fill=(190, 40, 35), width=5)
        # Splotch of yellow synthetic thread
        draw.line([(fx+10, 200), (fx-15, 380)], fill=(220, 180, 40), width=3)
    # Dark vignette mask around circle
    mask = Image.new('L', (w, h), 255)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=0)
    img_black = Image.new('RGB', (w, h), (10, 12, 15))
    img.paste(img_black, (0, 0), mask)
    f_lab = get_font(FONT_COURIER, 14)
    draw = ImageDraw.Draw(img)
    draw.text((40, 40), "MAGNIFICATION: 400X // POLARIZED LIGHT", fill=(180, 185, 195), font=f_lab)
    draw.text((40, 65), "SPECIMEN: CRIMSON ACRYLIC WOOL (SAMPLE #11)", fill=(220, 190, 80), font=f_lab)
    save_evidence(img, "buc-thu-dem-tuyet-trang", "d11-soi-len.webp")

def gen_chuyen_tau_dem_muong_man():
    w, h = 800, 600
    
    # d05-cua-truot.webp: Train door latch & fresh friction marks
    img = Image.new('RGB', (w, h), (70, 75, 80))
    draw = ImageDraw.Draw(img)
    # Aluminum door frame texture
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=(int(65 + y/h*20), int(70 + y/h*20), int(75 + y/h*20)))
    draw.rectangle([120, 80, 320, 520], fill=(95, 100, 108), outline=(45, 48, 52), width=4)
    # Door latch bracket
    draw.rectangle([280, 240, 520, 360], fill=(45, 48, 52), outline=(120, 125, 135), width=3)
    # Stainless bolt mechanism
    draw.rectangle([240, 275, 460, 325], fill=(180, 185, 195), outline=(30, 30, 35), width=2)
    # Abrasive fresh scratches (revealing shiny silver aluminum)
    for _ in range(16):
        sy = random.randint(285, 315)
        draw.line([(210, sy), (260, sy + random.randint(-4, 4))], fill=(245, 250, 255), width=2)
    draw_evidence_marker(draw, 560, 120, "1")
    draw_scale_bar(draw, 80, 540, 20)
    save_evidence(img, "chuyen-tau-dem-muong-man", "d05-cua-truot.webp")

    # d12-cuon-cuoc.webp: Spool of nylon fishing line & steel awl
    img = Image.new('RGB', (w, h), (200, 200, 205))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (190, 195, 200))
    # Spool of transparent fishing line
    cx, cy = 300, 300
    draw.ellipse([cx-90, cy-90, cx+90, cy+90], fill=(225, 235, 245), outline=(100, 110, 120), width=4)
    draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(160, 165, 175), outline=(80, 85, 95), width=3)
    # Winding lines
    for r in range(45, 88, 5):
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(240, 245, 255), width=2)
    # Steel awl tool
    draw.polygon([(480, 160), (510, 175), (580, 380), (550, 395)], fill=(30, 30, 35)) # handle
    draw.polygon([(565, 390), (575, 395), (660, 480), (655, 485)], fill=(190, 195, 205)) # sharp steel point
    draw_evidence_marker(draw, 100, 100, "B")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "chuyen-tau-dem-muong-man", "d12-cuon-cuoc.webp")

def gen_dem_sung_no_tay_son():
    w, h = 800, 600
    
    # d05-vo-dan.webp: 3 K54 bullet casings stamped 1968
    img = Image.new('RGB', (w, h), (50, 52, 56))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (45, 48, 52))
    # 3 Brass casings
    for idx, (cx, cy, ang) in enumerate([(280, 260, 20), (440, 320, -15), (520, 220, 45)]):
        draw.ellipse([cx-50, cy-35, cx+50, cy+35], fill=(210, 165, 55), outline=(140, 100, 30), width=3)
        draw.ellipse([cx-25, cy-18, cx+25, cy+18], fill=(160, 120, 40), outline=(90, 65, 20), width=2)
        # Firing pin indent in primer
        draw.ellipse([cx-8, cy-6, cx+8, cy+6], fill=(40, 30, 15))
        # Stamp "1968 // 71"
        f_st = get_font(FONT_COURIER, 10)
        draw.text((cx-20, cy-30), "1968", fill=(80, 55, 15), font=f_st)
    draw_evidence_marker(draw, 120, 120, "1")
    draw_evidence_marker(draw, 640, 380, "2")
    draw_scale_bar(draw, 120, 530, 18)
    save_evidence(img, "dem-sung-no-tay-son", "d05-vo-dan.webp")

    # d11-bao-thuoc.webp: Crushed Du Lich cigarette pack with fingerprint powder
    img = Image.new('RGB', (w, h), (40, 40, 45))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (35, 38, 42))
    # Crushed red cigarette soft pack
    draw.polygon([(260, 180), (490, 150), (470, 450), (230, 430)], fill=(180, 35, 35), outline=(80, 15, 15), width=3)
    # White label band
    draw.polygon([(250, 250), (480, 220), (475, 320), (240, 340)], fill=(240, 240, 235))
    f_cig = get_font(FONT_HELVETICA, 24)
    draw.text((360, 270), "DU LỊCH", fill=(180, 20, 20), font=f_cig, anchor="mm")
    # Fine white fingerprint powder splotch
    for _ in range(40):
        px = random.randint(310, 370)
        py = random.randint(280, 350)
        draw.ellipse([px, py, px+3, py+3], fill=(240, 245, 255))
    draw_evidence_marker(draw, 100, 140, "E")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "dem-sung-no-tay-son", "d11-bao-thuoc.webp")

def gen_gac_den_hon_dau():
    w, h = 800, 600
    
    # d11-may-phat.webp: Yanmar generator thermal strip jammed
    img = Image.new('RGB', (w, h), (35, 38, 42))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (40, 42, 48))
    # Generator copper stator coils
    for x in range(140, 640, 40):
        draw.rectangle([x, 180, x + 25, 420], fill=(180, 95, 35), outline=(90, 45, 15), width=2)
    # Bent bimetallic strip wedged
    draw.polygon([(280, 260), (440, 220), (460, 250), (300, 290)], fill=(210, 215, 225), outline=(50, 55, 60), width=3)
    draw.ellipse([430, 220, 470, 260], fill=(240, 200, 50)) # electrical contact point
    draw_evidence_marker(draw, 80, 100, "M")
    draw_scale_bar(draw, 80, 530, 20)
    save_evidence(img, "gac-den-hon-dau", "d11-may-phat.webp")

    # d15-ao-mua.webp: Yellow raincoat and torn diary page
    img = Image.new('RGB', (w, h), (45, 45, 50))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (50, 52, 58))
    # Folded yellow PVC raincoat
    draw.polygon([(180, 160), (520, 120), (560, 480), (140, 450)], fill=(235, 195, 35), outline=(120, 95, 15), width=4)
    # Dark muddy / grease smear
    draw.ellipse([260, 240, 420, 360], fill=(70, 45, 25))
    # Torn lighthouse diary page
    draw.polygon([(460, 260), (680, 220), (660, 460), (440, 440)], fill=(245, 240, 225), outline=(140, 130, 110), width=2)
    for ly in range(290, 420, 18):
        draw.line([(480, ly), (640, ly-10)], fill=(60, 60, 70), width=2)
    draw_evidence_marker(draw, 80, 80, "R")
    draw_scale_bar(draw, 80, 530, 18)
    save_evidence(img, "gac-den-hon-dau", "d15-ao-mua.webp")

def gen_hoi_chuong_chua_thay():
    w, h = 800, 600
    
    # d05-gac-chuong.webp: Ancient bronze bell & suspended striker log
    img = Image.new('RGB', (w, h), (30, 28, 25))
    draw = ImageDraw.Draw(img)
    # Wooden rafters
    draw.line([(0, 80), (w, 80)], fill=(75, 55, 35), width=18)
    draw.line([(120, 0), (120, h)], fill=(75, 55, 35), width=22)
    draw.line([(680, 0), (680, h)], fill=(75, 55, 35), width=22)
    # Bell hanging chains
    draw.line([(320, 80), (320, 180)], fill=(80, 85, 90), width=6)
    draw.line([(440, 80), (440, 180)], fill=(80, 85, 90), width=6)
    # Massive ancient bronze bell
    draw.polygon([(260, 180), (500, 180), (560, 480), (200, 480)], fill=(65, 95, 80), outline=(35, 60, 45), width=6)
    draw.ellipse([200, 450, 560, 510], fill=(55, 85, 70), outline=(35, 60, 45), width=5)
    # Wooden striker log suspended horizontally
    draw.line([(580, 80), (580, 360)], fill=(120, 95, 60), width=4)
    draw.rectangle([540, 340, 740, 400], fill=(85, 55, 30), outline=(40, 25, 10), width=3)
    save_evidence(img, "hoi-chuong-chua-thay", "d05-gac-chuong.webp")

    # d11-ong-tre.webp: Bamboo tube counterweight hydraulic lever
    img = Image.new('RGB', (w, h), (40, 42, 45))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (45, 48, 52))
    # Bamboo pipe tube
    draw.polygon([(200, 240), (580, 200), (580, 280), (200, 320)], fill=(140, 155, 90), outline=(75, 85, 45), width=4)
    # Bamboo nodes
    draw.line([(320, 225), (320, 305)], fill=(90, 100, 55), width=4)
    draw.line([(450, 210), (450, 290)], fill=(90, 100, 55), width=4)
    # Pivot pin hole in center
    draw.ellipse([375, 245, 395, 265], fill=(30, 20, 15))
    # Thin hemp trigger cord
    draw.line([(210, 310), (210, 480)], fill=(160, 140, 100), width=3)
    draw_evidence_marker(draw, 100, 100, "T")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "hoi-chuong-chua-thay", "d11-ong-tre.webp")

def gen_lua_than_tay_nguyen():
    w, h = 800, 600
    
    # d05-xa-gac.webp: Traditional machete axe (xà gạc) engraved "B" in ash
    img = Image.new('RGB', (w, h), (25, 22, 20))
    draw = ImageDraw.Draw(img)
    # Ash and charred ground
    for _ in range(80):
        ax = random.randint(40, w-40)
        ay = random.randint(40, h-40)
        draw.ellipse([ax, ay, ax + random.randint(10, 50), ay + random.randint(5, 20)], fill=(55, 52, 50))
    # Curved iron blade of Xa Gac
    draw.polygon([(220, 220), (380, 180), (460, 260), (320, 310)], fill=(140, 145, 155), outline=(40, 40, 45), width=3)
    # Wooden curved handle
    draw.polygon([(360, 240), (620, 380), (600, 420), (340, 280)], fill=(95, 60, 35), outline=(45, 25, 10), width=3)
    # Engraved "B" on wooden handle
    f_b = get_font(FONT_HELVETICA, 32)
    draw.text((480, 330), "B", fill=(210, 180, 120), font=f_b)
    draw_evidence_marker(draw, 80, 80, "X")
    draw_scale_bar(draw, 80, 530, 20)
    save_evidence(img, "lua-than-tay-nguyen", "d05-xa-gac.webp")

    # d11-rui-dien.webp: Lamp socket & incubator thermal relay timer
    img = Image.new('RGB', (w, h), (42, 40, 38))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (40, 38, 36))
    # Bulb socket
    draw.rectangle([200, 220, 320, 360], fill=(45, 45, 50), outline=(20, 20, 20), width=3)
    draw.ellipse([220, 180, 300, 240], fill=(210, 180, 70), outline=(140, 110, 40), width=2) # brass screw base
    # Bimetallic incubator thermal relay
    draw.rectangle([420, 200, 580, 380], fill=(160, 165, 175), outline=(70, 75, 80), width=3)
    # Temp adjustment dial
    draw.ellipse([460, 240, 540, 320], fill=(60, 65, 70), outline=(200, 200, 200), width=2)
    # Burned wires
    draw.line([(320, 290), (420, 290)], fill=(190, 40, 30), width=4)
    draw_evidence_marker(draw, 80, 100, "H")
    draw_scale_bar(draw, 80, 530, 18)
    save_evidence(img, "lua-than-tay-nguyen", "d11-rui-dien.webp")

def gen_ly_tra_trao_doc():
    w, h = 800, 600
    
    # d05-nap-coc.webp: Microscopic needle puncture on sealed plastic film
    img = Image.new('RGB', (w, h), (30, 32, 35))
    draw = ImageDraw.Draw(img)
    # Circle view of cup lid
    cx, cy, cr = 400, 300, 240
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(225, 230, 240))
    # Brand sticker edge
    draw.polygon([(260, 160), (420, 140), (440, 340), (280, 360)], fill=(240, 210, 70))
    # Microscopic needle hole
    draw.ellipse([435, 235, 445, 245], fill=(20, 20, 25), outline=(180, 40, 40), width=2)
    # Measurement reticle circle
    draw.ellipse([400, 200, 480, 280], outline=(180, 40, 40), width=1)
    f_lab = get_font(FONT_COURIER, 14)
    draw.text((60, 50), "PUNCTURE DIAMETER: 0.32mm // NEEDLE GAUGE: 30G", fill=(230, 200, 50), font=f_lab)
    save_evidence(img, "ly-tra-trao-doc", "d05-nap-coc.webp")

    # d11-ong-tiem.webp: Insulin syringe and potassium cyanide vial on tray
    img = Image.new('RGB', (w, h), (180, 185, 190))
    draw = ImageDraw.Draw(img)
    # Stainless steel tray
    draw.rectangle([80, 80, 720, 500], fill=(215, 220, 225), outline=(130, 135, 140), width=6)
    # 1ml Insulin syringe
    draw.rectangle([180, 220, 460, 250], fill=(245, 250, 255), outline=(100, 105, 115), width=2)
    # Graduations
    for gx in range(200, 440, 15):
        draw.line([(gx, 220), (gx, 232)], fill=(40, 40, 45), width=1)
    # Plunger
    draw.rectangle([460, 228, 560, 242], fill=(230, 235, 240), outline=(80, 85, 90), width=2)
    # Needle
    draw.line([(180, 235), (110, 235)], fill=(150, 155, 165), width=2)
    # Amber glass vial
    draw.rectangle([540, 300, 640, 450], fill=(160, 95, 30), outline=(75, 40, 15), width=3)
    draw.rectangle([555, 330, 625, 420], fill=(240, 240, 235))
    f_warn = get_font(FONT_HELVETICA, 12)
    draw.text((590, 365), "KCN", fill=(180, 20, 20), font=f_warn, anchor="mm")
    draw.text((590, 385), "TOXIC", fill=(20, 20, 20), font=f_warn, anchor="mm")
    draw_evidence_marker(draw, 120, 360, "S")
    draw_scale_bar(draw, 140, 530, 16)
    save_evidence(img, "ly-tra-trao-doc", "d11-ong-tiem.webp")

def gen_mua_dong_binh_ty():
    w, h = 800, 600
    
    # d12-inhaler.webp: Ventolin asthma inhaler on forensic grid
    img = Image.new('RGB', (w, h), (55, 58, 62))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (50, 52, 56))
    # Ventolin L-shaped light blue body
    draw.polygon([(260, 160), (370, 160), (370, 380), (520, 380), (520, 470), (260, 470)], fill=(70, 155, 215), outline=(35, 90, 130), width=3)
    # Mouthpiece oval opening
    draw.ellipse([490, 395, 535, 455], fill=(35, 90, 130))
    # Aluminum canister top inserted
    draw.rectangle([285, 110, 345, 175], fill=(200, 205, 215), outline=(110, 115, 125), width=2)
    f_lbl = get_font(FONT_ARIAL, 14)
    draw.text((315, 280), "VENTOLIN", fill=(245, 250, 255), font=f_lbl, anchor="mm")
    draw_evidence_marker(draw, 120, 140, "4")
    draw_scale_bar(draw, 120, 530, 18)
    save_evidence(img, "mua-dong-binh-ty", "d12-inhaler.webp")

def gen_quai_vat_21_khuon_mat():
    w, h = 800, 600
    
    # d05-buc-thu.webp: Typewritten blackmailer letter on graph paper with smirking logo
    img = Image.new('RGB', (w, h), (235, 235, 230))
    draw = ImageDraw.Draw(img)
    # Blue grid graph paper
    for x in range(60, 740, 20):
        draw.line([(x, 60), (x, 540)], fill=(200, 215, 230), width=1)
    for y in range(60, 540, 20):
        draw.line([(60, y), (740, y)], fill=(200, 215, 230), width=1)
    # Typewritten Japanese/Latin lines
    for ly in range(100, 400, 24):
        draw.line([(100, ly), (680, ly)], fill=(50, 52, 58), width=3)
    # Smirking monster mask logo at bottom right
    cx, cy = 600, 460
    draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(240, 240, 235), outline=(30, 40, 140), width=3)
    # Fox eyes
    draw.line([(cx-25, cy-12), (cx-5, cy-8)], fill=(30, 40, 140), width=4)
    draw.line([(cx+5, cy-8), (cx+25, cy-12)], fill=(30, 40, 140), width=4)
    # Wide smirk
    draw.arc([cx-25, cy-5, cx+25, cy+25], 0, 180, fill=(30, 40, 140), width=4)
    draw_evidence_marker(draw, 80, 440, "M")
    save_evidence(img, "quai-vat-21-khuon-mat", "d05-buc-thu.webp")

    # d11-hop-keo.webp: Chocolate box with polyurethane reseal mark
    img = Image.new('RGB', (w, h), (45, 48, 52))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (40, 42, 46))
    # Red chocolate box
    draw.polygon([(180, 160), (580, 120), (550, 440), (150, 480)], fill=(160, 30, 30), outline=(80, 15, 15), width=4)
    # Gold foil banner
    draw.polygon([(200, 240), (560, 200), (550, 280), (190, 320)], fill=(210, 175, 60))
    # Macro hot-melt glue residue seam
    for _ in range(25):
        gx = random.randint(160, 540)
        gy = int(140 + (gx - 160) * -0.05) + random.randint(0, 15)
        draw.ellipse([gx, gy, gx+8, gy+6], fill=(230, 225, 200))
    draw_evidence_marker(draw, 100, 100, "C")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "quai-vat-21-khuon-mat", "d11-hop-keo.webp")

def gen_suong_mu_trai_trai():
    w, h = 800, 600
    
    # d05-hien-truong.webp: Red basalt hill slope & wheelbarrow tire track in mist
    img = Image.new('RGB', (w, h), (85, 45, 30))
    draw = ImageDraw.Draw(img)
    # Basalt mud hill gradient
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=(int(110 - y/h*40), int(55 - y/h*20), int(35 - y/h*15)))
    # Pine trees in misty background
    draw.polygon([(60, 0), (140, 160), (0, 160)], fill=(40, 55, 45))
    draw.polygon([(240, 0), (320, 140), (180, 140)], fill=(40, 55, 45))
    draw.polygon([(w-120, 0), (w, 180), (w-200, 180)], fill=(40, 55, 45))
    # Wheelbarrow single tire track
    track_pts = [(180 + i*15, 120 + i*16 + int(math.sin(i*0.5)*15)) for i in range(26)]
    draw.line(track_pts, fill=(50, 20, 12), width=18)
    draw.line(track_pts, fill=(35, 15, 8), width=8)
    # Scattered pine needles
    for _ in range(50):
        nx = random.randint(60, w-60)
        ny = random.randint(150, h-60)
        draw.line([(nx, ny), (nx+random.randint(10, 25), ny+random.randint(5, 15))], fill=(160, 110, 50), width=2)
    save_evidence(img, "suong-mu-trai-trai", "d05-hien-truong.webp")

    # d12-kho-lanh.webp: Cold storage & flake ice machine
    img = Image.new('RGB', (w, h), (50, 75, 95))
    draw = ImageDraw.Draw(img)
    # Industrial cold storage walls
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=(int(40 + y/h*25), int(60 + y/h*30), int(80 + y/h*35)))
    # Steel flake ice machine
    draw.rectangle([340, 140, 660, 480], fill=(175, 190, 205), outline=(90, 110, 130), width=4)
    # Frost crusting on machine
    for _ in range(60):
        fx = random.randint(350, 650)
        fy = random.randint(150, 470)
        draw.ellipse([fx, fy, fx+random.randint(4, 12), fy+random.randint(4, 12)], fill=(240, 248, 255))
    # Crate of red roses
    draw.rectangle([80, 280, 300, 480], fill=(120, 85, 55), outline=(60, 40, 25), width=3)
    for _ in range(20):
        rx = random.randint(100, 280)
        ry = random.randint(300, 440)
        draw.ellipse([rx, ry, rx+20, ry+20], fill=(160, 20, 25))
    save_evidence(img, "suong-mu-trai-trai", "d12-kho-lanh.webp")

def gen_tieng_dan_day_pho_hien():
    w, h = 800, 600
    
    # d04-dan-day.webp: Traditional Dan Day musical instrument on mat
    img = Image.new('RGB', (w, h), (45, 38, 30))
    draw = ImageDraw.Draw(img)
    # Woven reed mat pattern
    for x in range(0, w, 20):
        draw.line([(x, 0), (x, h)], fill=(75, 62, 45), width=1)
    for y in range(0, h, 20):
        draw.line([(0, y), (w, y)], fill=(65, 52, 38), width=1)
    # Dan Day long neck
    draw.polygon([(180, 80), (210, 75), (420, 480), (390, 485)], fill=(60, 30, 18), outline=(25, 10, 5), width=2)
    # Rectangular soundbox
    draw.polygon([(360, 360), (560, 330), (520, 520), (320, 550)], fill=(75, 35, 20), outline=(30, 15, 8), width=4)
    # 3 silk strings
    draw.line([(195, 78), (440, 460)], fill=(220, 220, 225), width=1)
    draw.line([(200, 78), (445, 460)], fill=(220, 220, 225), width=1)
    draw.line([(205, 78), (450, 460)], fill=(220, 220, 225), width=1)
    # Horn plectrum
    draw.polygon([(560, 420), (610, 400), (590, 460)], fill=(25, 25, 30), outline=(80, 80, 85), width=2)
    draw_evidence_marker(draw, 100, 120, "D")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "tieng-dan-day-pho-hien", "d04-dan-day.webp")

    # d13-khan-lua.webp: Silk scarf & antique poison jar
    img = Image.new('RGB', (w, h), (40, 42, 45))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (42, 45, 48))
    # Folded silk scarf with crane pattern
    draw.polygon([(180, 200), (520, 160), (560, 460), (140, 420)], fill=(215, 200, 175), outline=(140, 125, 105), width=3)
    # Celadon eel-skin glazed mini ceramic jar
    cx, cy = 460, 320
    draw.ellipse([cx-55, cy-70, cx+55, cy+70], fill=(85, 105, 95), outline=(45, 60, 50), width=3)
    draw.ellipse([cx-35, cy-80, cx+35, cy-50], fill=(60, 75, 65))
    # Fine white arsenic powder residue on rim
    for _ in range(30):
        px = random.randint(cx-30, cx+30)
        py = random.randint(cy-75, cy-55)
        draw.ellipse([px, py, px+3, py+3], fill=(250, 250, 255))
    draw_evidence_marker(draw, 100, 100, "P")
    draw_scale_bar(draw, 100, 530, 18)
    save_evidence(img, "tieng-dan-day-pho-hien", "d13-khan-lua.webp")

def gen_tieng_huan_van_don():
    w, h = 800, 600
    
    # d05-nap-khoang.webp: Trawler deck cargo hatch & iron bolt latch
    img = Image.new('RGB', (w, h), (45, 52, 58))
    draw = ImageDraw.Draw(img)
    # Wet ship deck planks
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(35, 42, 48), width=3)
    # Heavy galvanized hatch cover
    draw.rectangle([160, 120, 640, 460], fill=(140, 150, 160), outline=(65, 75, 85), width=6)
    # Iron locking crossbar & padlock
    draw.rectangle([200, 260, 600, 310], fill=(55, 60, 68), outline=(25, 30, 35), width=3)
    draw.ellipse([540, 275, 580, 325], fill=(180, 140, 45), outline=(40, 40, 40), width=2)
    # Cold condensation droplets seeping
    for _ in range(40):
        cx = random.randint(180, 620)
        draw.ellipse([cx, 455, cx+6, 465], fill=(220, 240, 255))
    save_evidence(img, "tieng-huan-van-don", "d05-nap-khoang.webp")

    # d11-da-kho.webp: Dry ice pellets sublimating CO2 vapor
    img = Image.new('RGB', (w, h), (160, 165, 175))
    draw = ImageDraw.Draw(img)
    # Stainless lab tray
    draw.rectangle([100, 80, 700, 500], fill=(195, 205, 215), outline=(110, 115, 125), width=5)
    # Dense white CO2 vapor cloud
    for _ in range(50):
        vx = random.randint(200, 600)
        vy = random.randint(180, 420)
        draw.ellipse([vx, vy, vx + random.randint(40, 90), vy + random.randint(25, 60)], fill=(240, 248, 255))
    # Dry ice white solid pellets
    for _ in range(35):
        px = random.randint(300, 500)
        py = random.randint(250, 380)
        draw.rectangle([px, py, px+random.randint(14, 28), py+random.randint(12, 22)], fill=(255, 255, 255), outline=(180, 200, 220), width=1)
    draw_evidence_marker(draw, 120, 120, "C")
    draw_scale_bar(draw, 140, 530, 18)
    save_evidence(img, "tieng-huan-van-don", "d11-da-kho.webp")

def gen_vang_bong_cho_lon():
    w, h = 800, 600
    
    # d05-num-ket.webp: Antique Chubb safe combination dial with latent powder
    img = Image.new('RGB', (w, h), (35, 38, 42))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (40, 42, 46))
    # Heavy iron safe door plate
    draw.rectangle([120, 80, 680, 500], fill=(50, 55, 60), outline=(25, 28, 32), width=6)
    # Circular brass/chrome dial
    cx, cy, cr = 400, 290, 140
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(180, 185, 195), outline=(80, 85, 95), width=5)
    draw.ellipse([cx-90, cy-90, cx+90, cy+90], fill=(60, 65, 75), outline=(30, 35, 40), width=4)
    # Dial numbers ticks
    for a in range(0, 360, 15):
        rad = math.radians(a)
        x1 = cx + math.cos(rad) * 110
        y1 = cy + math.sin(rad) * 110
        x2 = cx + math.cos(rad) * 135
        y2 = cy + math.sin(rad) * 135
        draw.line([(x1, y1), (x2, y2)], fill=(20, 20, 25), width=2)
    # Latent fingerprint white powder smudges on numbers 3, 7, 8, 2
    for sa in [45, 135, 210, 300]:
        rad = math.radians(sa)
        sx = cx + math.cos(rad) * 122
        sy = cy + math.sin(rad) * 122
        for _ in range(15):
            ox = sx + random.randint(-8, 8)
            oy = sy + random.randint(-8, 8)
            draw.ellipse([ox, oy, ox + 3, oy + 3], fill=(250, 250, 255))
    draw_evidence_marker(draw, 160, 110, "K")
    draw_scale_bar(draw, 160, 530, 16)
    save_evidence(img, "vang-bong-cho-lon", "d05-num-ket.webp")

    # d10-manh-giay.webp: Traditional Chinese medicine paper scrap with 24 permutations
    img = Image.new('RGB', (w, h), (42, 35, 28))
    draw = ImageDraw.Draw(img)
    # Dark mahogany tea table wood
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill=(32, 26, 20), width=3)
    # Aged yellowish paper scrap
    draw.polygon([(180, 140), (620, 110), (600, 480), (150, 460)], fill=(235, 225, 195), outline=(130, 115, 90), width=2)
    # Handwritten 4-digit permutations
    perms = ["1378", "1387", "1738", "1783", "1837", "1873", "3178", "3187", "3718", "3781", "3817", "3871"]
    f_num = get_font(FONT_COURIER, 18)
    for idx, p in enumerate(perms):
        col_x = 220 if idx < 6 else 420
        row_y = 170 + (idx % 6) * 44
        draw.text((col_x, row_y), p, fill=(40, 35, 30), font=f_num)
    draw_evidence_marker(draw, 80, 80, "P")
    draw_scale_bar(draw, 80, 530, 18)
    save_evidence(img, "vang-bong-cho-lon", "d10-manh-giay.webp")

def gen_vet_muc_lang_dong_ho():
    w, h = 800, 600
    
    # d03-ban-khac.webp: Cracked woodblock for folk print with red cinnabar
    img = Image.new('RGB', (w, h), (40, 35, 30))
    draw = ImageDraw.Draw(img)
    # Workbench surface
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(55, 45, 38), width=1)
    # Pear-wood printing block split in two halves
    # Left half
    draw.polygon([(160, 140), (380, 130), (360, 480), (140, 470)], fill=(95, 60, 35), outline=(45, 25, 10), width=3)
    # Right half
    draw.polygon([(410, 130), (640, 120), (620, 470), (390, 480)], fill=(95, 60, 35), outline=(45, 25, 10), width=3)
    # Carved relief lines (Đám cưới chuột)
    for ly in range(180, 440, 35):
        draw.line([(180, ly), (340, ly-10)], fill=(40, 20, 10), width=3)
        draw.line([(430, ly), (600, ly-10)], fill=(40, 20, 10), width=3)
    # Bright red sticky cinnabar vermilion ink splotches
    for _ in range(30):
        rx = random.randint(340, 430)
        ry = random.randint(180, 450)
        draw.ellipse([rx, ry, rx+12, ry+8], fill=(210, 35, 35))
    draw_evidence_marker(draw, 80, 80, "W")
    draw_scale_bar(draw, 80, 530, 20)
    save_evidence(img, "vet-muc-lang-dong-ho", "d03-ban-khac.webp")

    # d10-dam-go.webp: Sharp wood chips and white rubber sandal (dép tổ ong)
    img = Image.new('RGB', (w, h), (45, 48, 52))
    draw = ImageDraw.Draw(img)
    draw_forensic_backdrop(draw, w, h, (42, 45, 48))
    # Transparent evidence bag
    draw.rectangle([140, 160, 380, 440], fill=(60, 65, 72), outline=(180, 190, 205), width=2)
    # Sharp red-stained wood chips inside bag
    for _ in range(18):
        wx = random.randint(180, 340)
        wy = random.randint(220, 400)
        draw.polygon([(wx, wy), (wx+random.randint(8, 20), wy+random.randint(-10, 10)), (wx+random.randint(5, 15), wy+random.randint(10, 25))], fill=(185, 40, 35))
    # Classic Vietnamese white honeycomb rubber sandal (dép tổ ong)
    draw.polygon([(460, 140), (620, 160), (590, 480), (430, 460)], fill=(225, 225, 220), outline=(130, 130, 125), width=3)
    # Honeycomb grid on sandal
    for gy in range(200, 440, 24):
        draw.line([(450, gy), (600, gy+20)], fill=(150, 150, 145), width=2)
    # Alluvial river mud caked on heel
    draw.ellipse([430, 400, 520, 480], fill=(85, 55, 30))
    draw_evidence_marker(draw, 80, 80, "S")
    draw_scale_bar(draw, 80, 530, 18)
    save_evidence(img, "vet-muc-lang-dong-ho", "d10-dam-go.webp")

def main():
    print("Generating all 27 missing forensic evidence images...")
    gen_buc_thu_dem_tuyet_trang()
    gen_chuyen_tau_dem_muong_man()
    gen_dem_sung_no_tay_son()
    gen_gac_den_hon_dau()
    gen_hoi_chuong_chua_thay()
    gen_lua_than_tay_nguyen()
    gen_ly_tra_trao_doc()
    gen_mua_dong_binh_ty()
    gen_quai_vat_21_khuon_mat()
    gen_suong_mu_trai_trai()
    gen_tieng_dan_day_pho_hien()
    gen_tieng_huan_van_don()
    gen_vang_bong_cho_lon()
    gen_vet_muc_lang_dong_ho()
    print("All 27 evidence images successfully rendered!")

if __name__ == "__main__":
    main()
