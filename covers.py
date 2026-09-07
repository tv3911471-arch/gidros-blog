#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация обложек статей. Шаблонные, фирменные, без фейковых фото.
Размер 1100x619 (16:9) — подходит и для блога, и для обложки статьи в Дзене.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1100, 619
MARGIN = 70

# Windows-шрифты с кириллицей
F_BOLD = "C:/Windows/Fonts/arialbd.ttf"
F_REG = "C:/Windows/Fonts/arial.ttf"

# Фирменная палитра (синяя, из стиля Гидрос)
TOP = (11, 58, 107)      # тёмно-синий
BOT = (11, 99, 182)      # синий
ACCENT = (94, 200, 255)  # голубой акцент
WHITE = (255, 255, 255)

CLUSTER_LABEL = {
    "skvazhina-osnovy": "СКВАЖИНА · РАЗБОР",
    "skvazhina-montazh": "БУРЕНИЕ И ОБУСТРОЙСТВО",
    "skvazhina-cena": "СКВАЖИНА · ЦЕНЫ",
    "skvazhina-geo": "СКВАЖИНА · РАЙОНЫ МО",
    "septik-osnovy": "СЕПТИК · РАЗБОР",
    "septik-vybor": "ВЫБОР СЕПТИКА",
    "septik-montazh": "МОНТАЖ СЕПТИКА",
    "septik-cena": "СЕПТИК · ЦЕНЫ",
    "septik-geo": "СЕПТИК · РАЙОНЫ МО",
    "septik-ekspluataciya": "ЭКСПЛУАТАЦИЯ СЕПТИКА",
    "filtraciya": "ВОДА И ФИЛЬТРЫ",
}


def _gradient():
    base = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        base.putpixel((0, y), tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))
    return base.resize((W, H))


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_cover(slug, title, cluster, phone, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}.png"

    img = _gradient()
    d = ImageDraw.Draw(img)

    # водяной знак — крупный круг-капля справа снизу
    d.ellipse([W - 190, H - 190, W + 120, H + 120], fill=(255, 255, 255, 0),
              outline=(255, 255, 255), width=3)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([W - 210, H - 130, W + 160, H + 240], fill=(255, 255, 255, 18))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)

    # вордмарк
    f_mark = ImageFont.truetype(F_BOLD, 34)
    d.text((MARGIN, MARGIN), "ГИДРО-С", font=f_mark, fill=WHITE)
    mark_w = d.textlength("ГИДРО-С", font=f_mark)
    d.text((MARGIN + mark_w + 16, MARGIN + 8), "бурение · септики · Подмосковье",
           font=ImageFont.truetype(F_REG, 20), fill=ACCENT)

    # категория
    f_cat = ImageFont.truetype(F_BOLD, 21)
    label = CLUSTER_LABEL.get(cluster, "РАЗБОР")
    d.text((MARGIN, MARGIN + 58), label, font=f_cat, fill=ACCENT)

    # заголовок
    size = 58 if len(title) < 60 else (50 if len(title) < 95 else 42)
    f_title = ImageFont.truetype(F_BOLD, size)
    lines = _wrap(d, title, f_title, W - 2 * MARGIN)
    lh = size + 14
    block_h = lh * len(lines)
    y = (H - block_h) // 2 + 20
    for ln in lines:
        d.text((MARGIN, y), ln, font=f_title, fill=WHITE)
        y += lh

    # нижняя линия + телефон
    d.rectangle([MARGIN, H - 92, MARGIN + 64, H - 88], fill=ACCENT)
    d.text((MARGIN, H - 74), f"Выезд инженера · {phone}",
           font=ImageFont.truetype(F_REG, 22), fill=WHITE)

    img.save(path, "PNG")
    return path.name


if __name__ == "__main__":
    make_cover("demo", "Обман при бурении скважин: 6 схем, на которых теряют деньги",
               "skvazhina-osnovy", "+7 968 870-82-25", "docs/img")
    print("docs/img/demo.png")
