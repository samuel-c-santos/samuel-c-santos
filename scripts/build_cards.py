"""Gera os cartões SVG neobrutalistas usados no README do perfil.

Uso:  python scripts/build_cards.py      (requer Pillow)

Cada cartão é escrito em files/cards/. As versões "-dark" só existem para os
cartões que têm fundo de papel; os demais funcionam nos dois temas.
"""

from pathlib import Path

from PIL import ImageFont

OUT = Path(__file__).resolve().parent.parent / "files" / "cards"

# Fontes locais usadas só para medir o texto e encaixar as caixas com precisão.
# No SVG os nomes de família continuam genéricos (Arial Black, Consolas...).
FONT_FILES = {
    "black": Path("C:/Windows/Fonts/ariblk.ttf"),
    "sans": Path("C:/Windows/Fonts/arialbd.ttf"),
    "mono": Path("C:/Windows/Fonts/consolab.ttf"),
}
_FONT_CACHE = {}


def measure(value, size, kind="black", ls=0):
    """Largura aproximada do texto, medida na fonte real do sistema."""
    key = (kind, size)
    if key not in _FONT_CACHE:
        path = FONT_FILES.get(kind)
        _FONT_CACHE[key] = (
            ImageFont.truetype(str(path), size) if path and path.exists() else None
        )
    font = _FONT_CACHE[key]
    if font is None:
        factor = {"black": 0.70, "sans": 0.58, "mono": 0.61}[kind]
        return len(value) * size * factor + ls * max(len(value) - 1, 0)
    return font.getlength(value) + ls * max(len(value) - 1, 0)

BLACK = "'Arial Black','Arial Bold',Impact,Haettenschweiler,sans-serif"
SANS = "Arial,Helvetica,sans-serif"
MONO = "'Cascadia Mono','JetBrains Mono',Consolas,'Courier New',monospace"

LIGHT = {
    "paper": "#FDFAF3",
    "grid": "#E9E1CD",
    "ink": "#0A0A0A",
    "card": "#FFFFFF",
    "muted": "#5B5648",
    "yellow": "#FFE600",
    "red": "#FF4D4D",
    "green": "#00E676",
    "violet": "#A78BFA",
    "blue": "#90A8ED",
    "pink": "#FF90E8",
    "orange": "#FF7A3C",
    "shadow": "#0A0A0A",
}

DARK = {
    "paper": "#0D0D12",
    "grid": "#1F1F29",
    "ink": "#F7F2E7",
    "card": "#16161E",
    "muted": "#B4AD9E",
    "yellow": "#FFE600",
    "red": "#FF5C5C",
    "green": "#2CF08D",
    "violet": "#B49CFF",
    "blue": "#9FB6F5",
    "pink": "#FF9BEC",
    "orange": "#FF8A52",
    "shadow": "#000000",
}

ACCENTS = ["yellow", "blue", "pink", "green", "violet", "orange"]


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def rect(x, y, w, h, fill, stroke=None, sw=0, rx=0, shadow=None, sdx=7, sdy=7):
    parts = []
    if shadow:
        parts.append(
            f'<rect x="{x + sdx}" y="{y + sdy}" width="{w}" height="{h}" rx="{rx}" fill="{shadow}"/>'
        )
    shape = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        shape += f' stroke="{stroke}" stroke-width="{sw}"'
    shape += "/>"
    parts.append(shape)
    return "".join(parts)


def txt(
    x,
    y,
    value,
    size,
    fill,
    family=BLACK,
    weight=900,
    anchor="start",
    ls=0,
    extra="",
):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
        f'letter-spacing="{ls}" {extra}>{esc(value)}</text>'
    )


def wrap(width, height, body, p):
    """Envolve o conteúdo com fundo de papel + grid."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <pattern id="grid" width="34" height="34" patternUnits="userSpaceOnUse">
      <path d="M 34 0 L 0 0 0 34" fill="none" stroke="{p['grid']}" stroke-width="1.4"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" fill="{p['paper']}"/>
  <rect width="{width}" height="{height}" fill="url(#grid)"/>
{body}
</svg>
"""


def tape(x, y, label, p, fill_key="yellow", size=14, pad=22):
    width = int(measure(label, size, "black", 1.2) + pad * 2)
    return (
        rect(x, y, width, 38, p[fill_key], p["ink"], 3.5, 0, p["shadow"], 5, 5)
        + txt(
            x + width // 2,
            y + 25,
            label,
            size,
            p["ink"],
            BLACK,
            900,
            "middle",
            1.2,
        )
    )


# --------------------------------------------------------------------------- #
# HERO
# --------------------------------------------------------------------------- #
def build_hero(p):
    b = []

    b.append(tape(56, 40, "★ ENGENHARIA DE DADOS & GEOTECNOLOGIA", p, "yellow", 14))

    # bloco do nome
    name_size = 104
    name2_w = measure("C. SANTOS", name_size, "black", -4)
    b.append(rect(40, 196, int(name2_w) + 34, 100, p["yellow"], p["ink"], 4))
    b.append(txt(56, 190, "SAMUEL", name_size, p["ink"], BLACK, 900, "start", -4))
    b.append(txt(56, 282, "C. SANTOS", name_size, p["ink"], BLACK, 900, "start", -4))
    b.append(
        txt(
            58,
            348,
            "ciência de dados · geoprocessamento · automação",
            20,
            p["ink"],
            MONO,
            700,
        )
    )

    # stats
    stats = [("7+", "ANOS DE CAMPO"), ("20+", "PROJETOS"), ("5", "CERTIFICAÇÕES")]
    x = 56
    for big, small in stats:
        big_w = measure(big, 30, "black")
        small_w = measure(small, 10.5, "mono")
        w = int(18 + big_w + 12 + small_w + 18)
        b.append(rect(x, 382, w, 62, p["card"], p["ink"], 3.5, 3, p["shadow"], 5, 5))
        b.append(txt(x + 18, 423, big, 30, p["ink"], BLACK, 900))
        b.append(
            txt(x + 18 + int(big_w) + 12, 416, small, 10.5, p["muted"], MONO, 700)
        )
        x += w + 16

    # terminal
    tx, ty, tw, th = 744, 92, 480, 258
    b.append(rect(tx, ty, tw, th, "#0B0B0E", p["ink"], 4, 4, p["shadow"], 8, 8))
    b.append(rect(tx, ty, tw, 34, p["yellow"], p["ink"], 4, 4))
    b.append(rect(tx, ty + 24, tw, 10, p["yellow"]))
    b.append(txt(tx + 14, ty + 24, "samuel@portfolio: ~", 13, p["ink"], MONO, 700))
    b.append(txt(tx + tw - 16, ty + 24, "● ● ●", 12, p["ink"], MONO, 700, "end"))

    lines = [
        ("$ whoami", "samuel c. santos"),
        ("$ cat foco.txt", "geo · dados · automação"),
        ("$ pwd", "belém / pará / brasil"),
        ("$ status", "coordenando geotecnologias"),
    ]
    y = ty + 70
    for cmd, out in lines:
        b.append(txt(tx + 18, y, cmd, 15.5, p["yellow"], MONO, 700))
        b.append(txt(tx + 18, y + 22, out, 15.5, "#F7F2E7", MONO, 700))
        y += 49

    # sticker
    sticker_w = int(measure("MESTRE EM BIOLOGIA AMBIENTAL", 15, "black", 0.4) + 44)
    b.append(
        '<g transform="rotate(-3 968 380)">'
        + rect(968 - sticker_w // 2, 358, sticker_w, 44, p["red"], p["ink"], 3.5, 2, p["shadow"], 4, 4)
        + txt(968, 386, "MESTRE EM BIOLOGIA AMBIENTAL", 15, "#0A0A0A", BLACK, 900, "middle", 0.4)
        + "</g>"
    )

    # estrela decorativa
    b.append(txt(1214, 74, "✦", 34, p["ink"], BLACK, 900, "end"))

    return wrap(1280, 480, "\n  ".join(b), p)


# --------------------------------------------------------------------------- #
# TICKER (funciona nos dois temas)
# --------------------------------------------------------------------------- #
def build_ticker():
    items = "GEO ★ DADOS ★ AUTOMAÇÃO ★ PYTHON ★ POSTGIS ★ QGIS ★ POWER BI ★ SQL ★ "
    b = [
        '<rect width="1280" height="64" fill="#0A0A0A"/>',
        '<rect x="0" y="0" width="1280" height="4" fill="#FFE600"/>',
        '<rect x="0" y="60" width="1280" height="4" fill="#FFE600"/>',
        txt(
            8,
            41,
            items * 3,
            21,
            "#FFE600",
            MONO,
            700,
            "start",
            2.5,
        ),
    ]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="64" viewBox="0 0 1280 64">
  {chr(10).join(b)}
</svg>
"""


# --------------------------------------------------------------------------- #
# STACK
# --------------------------------------------------------------------------- #
def build_stack(p):
    b = []
    b.append(tape(48, 32, "STACK TÉCNICA", p, "yellow", 14))
    b.append(
        txt(1072, 56, "▲ o que eu abro todo dia", 13, p["muted"], MONO, 700, "end")
    )

    groups = [
        ("DADOS & BI", "yellow", ["Python", "R", "SQL", "Pandas", "Power BI", "Streamlit"]),
        ("GEO", "green", ["PostGIS", "QGIS", "GDAL", "GeoPandas", "Earth Engine", "Leaflet"]),
        ("DEV & WEB", "blue", ["Flask", "JavaScript", "HTML/CSS", "React", "Git/GitHub", "Render"]),
        ("ANÁLISE & AUTOMAÇÃO", "pink", ["Estatística", "Machine Learning", "ETL", "Data Viz", "Colab", "Flet"]),
    ]

    cw, ch = 500, 216
    positions = [(48, 100), (572, 100), (48, 332), (572, 332)]
    for (title, color, items), (x, y) in zip(groups, positions):
        b.append(rect(x, y, cw, ch, p["card"], p["ink"], 4, 4, p["shadow"], 7, 7))
        label_w = int(measure(title, 13, "mono", 1.2) + 34)
        b.append(rect(x + 18, y + 16, label_w, 30, p[color], p["ink"], 3, 2))
        b.append(
            txt(
                x + 18 + label_w // 2,
                y + 37,
                title,
                13,
                "#0A0A0A",
                MONO,
                700,
                "middle",
                1.2,
            )
        )

        chip_w, chip_h = 226, 40
        for i, item in enumerate(items):
            col, row = i % 2, i // 2
            cx = x + 18 + col * (chip_w + 12)
            cy = y + 58 + row * (chip_h + 10)
            fill = p[ACCENTS[(i + 2 * row + positions.index((x, y))) % len(ACCENTS)]]
            b.append(rect(cx, cy, chip_w, chip_h, fill, p["ink"], 2.6, 2))
            size = 16.0
            while size > 10 and measure(item, size, "mono", 0.4) > chip_w - 20:
                size -= 0.5
            b.append(
                txt(
                    cx + chip_w // 2,
                    cy + chip_h // 2 + size * 0.36,
                    item,
                    size,
                    "#0A0A0A",
                    MONO,
                    700,
                    "middle",
                    0.4,
                )
            )

    return wrap(1120, 570, "\n  ".join(b), p)


# --------------------------------------------------------------------------- #
# CTA
# --------------------------------------------------------------------------- #
def build_cta(p):
    b = []
    b.append(rect(56, 36, 1168, 178, p["ink"], p["ink"], 4, 4, p["shadow"], 9, 9))

    size = 54.0
    while size > 34 and measure("QUE AGUENTA DADO DE VERDADE.", size, "black", -2) > 930:
        size -= 1

    b.append(txt(96, 104, "VAMOS CONSTRUIR ALGO", size, p["paper"], BLACK, 900, "start", -2))
    b.append(
        txt(96, 166, "QUE AGUENTA DADO DE VERDADE.", size, p["yellow"], BLACK, 900, "start", -2)
    )
    b.append(
        txt(1200, 78, "GEO · DADOS · CÓDIGO", 14, p["paper"], MONO, 700, "end", 2)
    )
    b.append(txt(1200, 200, "samuelsantos.site ↗", 17, p["yellow"], MONO, 700, "end"))

    # botão-seta
    ax, ay, aw = 1092, 84, 84
    b.append(rect(ax, ay, aw, aw, p["yellow"], p["ink"], 4, 3, p["paper"], 5, 5))
    b.append(
        f'<rect x="{ax + 18}" y="{ay + 34}" width="34" height="16" fill="#0A0A0A"/>'
        f'<polygon points="{ax + 50},{ay + 22} {ax + 50},{ay + 62} {ax + 70},{ay + 42}" fill="#0A0A0A"/>'
    )

    return wrap(1280, 250, "\n  ".join(b), p)


# --------------------------------------------------------------------------- #
# CHIPS DE LINK (um por arquivo, servem nos dois temas)
# --------------------------------------------------------------------------- #
def build_chip(label):
    w, h = 162, 46
    b = [
        '<rect x="4" y="4" width="150" height="38" rx="3" fill="#0A0A0A"/>',
        '<rect x="0" y="0" width="150" height="38" rx="3" fill="#FFE600" stroke="#0A0A0A" stroke-width="3.5"/>',
        txt(75, 25, label, 14, "#0A0A0A", MONO, 700, "middle", 1.4),
    ]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {chr(10).join(b)}
</svg>
"""


def build_marker():
    return """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <rect x="1.5" y="1.5" width="17" height="17" fill="#FFE600" stroke="#0A0A0A" stroke-width="3"/>
</svg>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}

    for name, palette in (("light", LIGHT), ("dark", DARK)):
        files[f"hero-{name}.svg"] = build_hero(palette)
        files[f"stack-{name}.svg"] = build_stack(palette)
        files[f"cta-{name}.svg"] = build_cta(palette)

    files["ticker.svg"] = build_ticker()
    files["marker.svg"] = build_marker()
    for slug, label in (
        ("github", "GITHUB"),
        ("linkedin", "LINKEDIN"),
        ("email", "E-MAIL"),
        ("whatsapp", "WHATSAPP"),
        ("site", "SITE"),
    ):
        files[f"chip-{slug}.svg"] = build_chip(label)

    for filename, content in files.items():
        path = OUT / filename
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"{filename:24} {len(content):6} bytes")


if __name__ == "__main__":
    main()
