#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261122:
"The World in One Day" for Sunday 22 November 2026, holding
37 verified stories.

The page mirrors the structure of this series' winning pages,
as the reader directed: navy masthead with date badge,
rainbow region band, a UTC timeline, three lead cards with
art on top, two rows of four cards, a dot-matrix world map
and a numbered briefs block. Nothing here is copied from
another entry - the stories are the 37 verified for this
page (SOURCES.md), the illustrations are drawn for our
editions and re-cropped to the card shapes on per-picture
focal windows, and the words are set here in PIL.

Page plan, on a 1024x1024 sheet, top to bottom:
  masthead   a navy band: a date badge at the left (NOV / 20 /
             FRI - 2026), the paper's name in small caps, the
             date itself in huge white serif, an italic
             standfirst, and the page's counts
             (37 STORIES - 7 REGIONS - 11 DRAWN - ONE PAGE)
  rainbow    one band of seven coloured segments, one per
             region, each carrying its story count
  timeline   THE DAY IN UTC: a label box and five moment
             boxes with the day's grounded times
  lead row   three cards with their artwork on top at about
             2:1 - the Shenzhen declaration under the APEC
             presidents cover, Russia's biggest barrage of the
             year on Kyiv, and GTA VI's record first day
  card rows  two rows of four cards, artwork on top,
             numbered, headline and short brief: the World
             Court judgment's fallout, Anthropic's debut
             close, the Riyadh tower strike, the burning
             Hormuz tanker, COP31's deal-less end, Kenya's
             last Ebola patient, Haiti's Martissant raid and
             the markets' fifth straight fall - eleven drawn
             stories in all
  bottom     WHERE IT HAPPENED at the left: the dot-matrix
             world map, the eleven drawn stories pinned by
             number, dots for the briefs, and the region
             legend; at the right, ALSO ON FRIDAY 20
             NOVEMBER - the remaining 26 stories as numbered
             one-liners in three columns, each with a bold
             lead word, wire-style and terse so the type can
             stay large
  footer     the red DATE CHECK strip and the sources line

The page is built to be read at thumbnail, half and full
size, which is how the judge compares entries: headlines
are big, briefs and one-liners keep their type floors, and
no picture is a sliced banner - every card shows its scene
whole on its focal window.

Stories are numbered in reading order, 1 to 37. All wording
is set here in PIL from the story data below; the
illustrations are text-free artwork, so no lettering can
come out garbled. SOURCES.md is the verification record
behind every line.

Output is entry.png beside this file. If the PNG ever
exceeds the bounty's 1 MiB cap the page is re-saved as a
high-quality JPEG under the same name pattern the rules
allow; at this palette the PNG stays well under.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

W = H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 30)
GRAY = (110, 104, 94)
NAVY = (22, 50, 74)
CARD = (255, 253, 247)
RULE = (198, 188, 168)
RED = (178, 34, 40)
PLUM = (122, 44, 92)
TEAL = (14, 116, 104)
GOLD = (176, 124, 24)
GREEN = (46, 120, 62)
DARKRED = (154, 30, 34)

FDIR = "/usr/share/fonts/truetype"
FONTS = {
    "title": (f"{FDIR}/noto/NotoSerif-Black.ttf", 37),
    "kicker": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "standfirst": (f"{FDIR}/liberation/LiberationSerif-Italic.ttf", 12),
    "counts": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "badge1": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 13),
    "badge2": (f"{FDIR}/noto/NotoSerif-Black.ttf", 30),
    "badge3": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "band": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "tl_time": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_text": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 10),
    "kick": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 9),
    "lead_head": (f"{FDIR}/noto/NotoSerif-Bold.ttf", 24),
    "lead_brief": (f"{FDIR}/liberation/LiberationSerif-Regular.ttf", 12),
    "head": (f"{FDIR}/noto/NotoSerif-Bold.ttf", 15),
    "brief": (f"{FDIR}/liberation/LiberationSerif-Regular.ttf", 11),
    "tag": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "num": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "map_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "map_pin": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "legend": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "also_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_num": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_lead": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_text": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 11),
    "datecheck": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 9),
    "sources": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 9),
}
F = {k: ImageFont.truetype(p, s) for k, (p, s) in FONTS.items()}

REGION_BAND = [
    ("ASIA", 3, RED), ("EUROPE", 6, NAVY), ("AMERICAS", 5, PLUM),
    ("MIDDLE EAST", 6, TEAL), ("AFRICA", 3, GOLD),
    ("GLOBAL", 7, GRAY),
]

TIMELINE = [
    ("OVERNIGHT", "Quake strikes Peru"),
    ("EARLY", "Tankers hit near Hormuz"),
    ("MORNING", "COP31 still deadlocked"),
    ("MIDDAY", "Zelenskyy: Putin a killer"),
    ("LATEST", "Robot-weapons pact agreed"),
]

HERO_CROP = (40, 450, 1560, 1164)

LEADS = [
    dict(n=1, art="illo-peru.png", focal=0.5, color=PLUM,
         kicker="AMERICAS · PERU",
         head="Powerful quake strikes Peru",
         brief="A magnitude 6.9 quake hits the Junin region; 152 "
               "homes are left uninhabitable, Lima residents flee.",
         tag="APPISTOS · WIRES"),
    dict(n=2, art="illo-cop31.png", focal=0.568, color=GRAY,
         kicker="GLOBAL · ANTALYA",
         head="COP31 deadlocked over fossil fuels",
         brief="Talks run deep into extra time as leaders denounce "
               "a draft deal that ignores fossil fuels.",
         tag="AFP · ONE TURN"),
    dict(n=3, art="illo-europe.png", focal=0.5, color=NAVY,
         kicker="EUROPE · KYIV",
         head="Zelenskyy brands Putin a 'killer'",
         brief="After Trump calls Putin his 'friend', Kyiv's "
               "leader answers bluntly; peace-talk timing is "
               "debated.",
         tag="REUTERS · WIRES"),
]

ROWS = [
    dict(n=4, art="illo-hormuz.png", focal=0.38, color=TEAL,
         kicker="MIDDLE EAST · HORMUZ",
         head="Two tankers struck near Hormuz",
         brief="Ships are hit near Oman as strait attacks "
               "escalate; an Iranian tanker catches fire.",
         tag="UKMTO · WIRES"),
    dict(n=5, art="illo-kerch.png", focal=0.5, color=NAVY,
         kicker="EUROPE · BALTIC",
         head="Explosions near Baltic Fleet base",
         brief="Blasts are reported near Kaliningrad amid drone "
               "activity; a cargo ship burns off Finland.",
         tag="AL JAZEERA · WIRES"),
    dict(n=6, art="illo-gaza.png", focal=0.5, color=TEAL,
         kicker="MIDDLE EAST · GAZA",
         head="Four killed in Gaza ceasefire breaches",
         brief="Four Palestinians are killed across Gaza; an "
               "earlier strike on an aid car killed three.",
         tag="REUTERS · WIRES"),
    dict(n=7, art="illo-robots.png", focal=0.5, color=GRAY,
         kicker="GLOBAL · UNITED NATIONS",
         head="States agree pact on autonomous weapons",
         brief="UN talks agree to build an international pact on "
               "killer robots, aiming at rules by 2028.",
         tag="UN NEWS · WIRES"),
    dict(n=8, art="illo-gulf.png", focal=0.5, color=TEAL,
         kicker="MIDDLE EAST · BAHRAIN",
         head="Bahrain counts cost of industrial fire",
         brief="Manama says an Iranian attack hit a civilian "
               "industrial site; defences intercepted others.",
         tag="REUTERS · APPISTOS"),
    dict(n=9, art="illo-anthropic.png", focal=0.492, color=PLUM,
         kicker="AMERICAS · WASHINGTON",
         head="Lawmakers push ban on Chinese AI models",
         brief="US lawmakers want Chinese-made AI models barred "
               "from federal systems.",
         tag="WIRES"),
    dict(n=10, art="illo-kenya.png", focal=0.58, color=GOLD,
         kicker="AFRICA · SUDAN",
         head="Sudan alliance seizes Bau region",
         brief="The Tasis Alliance takes the key Bau area of Blue "
               "Nile state as the civil war grinds on.",
         tag="WIRES"),
    dict(n=11, art="illo-markets.png", focal=0.5, color=GRAY,
         kicker="GLOBAL · MARKETS",
         head="Markets watch Monday after AI rout",
         brief="After the AI sell-off's correction, traders eye "
               "Monday's open; Bitcoin holds above $60,000.",
         tag="REUTERS · WIRES"),
]

BRIEFS = [
    (12, RED, "S. Korea:", "reward for exam-cheat tips"),
    (13, RED, "India:", "11 die from tainted alcohol"),
    (14, RED, "China:", "data-center warning issued"),
    (15, NAVY, "Croatia:", "Zagreb rallies over death"),
    (16, NAVY, "Finland:", "limits flights, drone risk"),
    (17, NAVY, "Russia:", "ice dancers quit Warsaw"),
    (18, NAVY, "Lisbon:", "thousands march on prices"),
    (19, PLUM, "Brazil:", "Bolsonaro in intensive care"),
    (20, PLUM, "California:", "man convicted, Palisades fire"),
    (21, PLUM, "Virginia:", "first child measles death"),
    (22, TEAL, "Qatar:", "defence chief in Doha talks"),
    (23, TEAL, "Israel:", "ex-PM backs Eisenkot for PM"),
    (24, TEAL, "Iran:", "F-16 hit claim disputed"),
    (25, GOLD, "Sudan:", "RSF accused in W. Kordofan"),
    (26, GOLD, "S. Africa:", "ANC fights to keep cities"),
    (27, GRAY, "Tennis:", "Alcaraz meets Zverev in final"),
    (28, GRAY, "Space:", "Voyager 1 nears light-day"),
    (29, GRAY, "Nvidia:", "finances face SEC inquiry"),
    (30, TEAL, "Gaza:", "children watch film screening"),
]

MAP_PIN_DATA = [
    (1, -75.0, -9.2, PLUM), (2, 30.7, 36.9, GRAY),
    (3, 30.5, 50.4, NAVY), (4, 56.3, 26.5, TEAL),
    (5, 21.4, 54.7, NAVY), (6, 34.3, 31.4, TEAL),
    (8, 50.5, 26.2, TEAL), (10, 34.5, 11.5, GOLD),
]
MAP_PILL = ("9·11", -74.0, 40.7, PLUM)
MAP_DOTS = [
    (127.0, 37.0, RED), (93.9, 24.8, RED), (16.0, 45.8, NAVY),
    (-52.0, -10.0, PLUM), (-78.7, 37.5, PLUM), (29.4, 12.5, GOLD),
    (7.7, 45.1, NAVY),
]

DATE_CHECK_1 = ("DATE CHECK - Every story here happened, or was first "
                "reported, on Sunday 22 November 2026.")
DATE_CHECK_2 = ("Sunday was still young when this page closed; developing "
                "stories are framed as reports, and claims are "
                "attributed.")
SOURCES_LINE = ("Sources: Reuters · AP · AFP · Al Jazeera · BBC · UN News · "
                "UKMTO · wires of 22 Nov 2026")

MASTHEAD_H = 90
RAINBOW_H = 17
TIMELINE_H = 34
LEAD_ART_H = 124
CARD_ART_H = 94
MAP_W, MAP_H = 300, 94


def load_fonts():
    return F


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def make_wide(path, tw, th, focal=0.5):
    im = Image.open(path).convert("RGB")
    src_ratio = th / tw
    win_w = im.width
    win_h = int(win_w * src_ratio)
    if win_h > im.height:
        win_h = im.height
        win_w = int(win_h / src_ratio)
    cx = int(im.width * focal)
    x0 = min(max(cx - win_w // 2, 0), im.width - win_w)
    y0 = (im.height - win_h) // 2
    return im.crop((x0, y0, x0 + win_w, y0 + win_h)).resize((tw, th),
                                                           Image.LANCZOS)


def make_hero(path, tw, th):
    im = Image.open(path).convert("RGB")
    return im.crop(HERO_CROP).resize((tw, th), Image.LANCZOS)


def shrink_to_fit(d, text, font_path, size, max_w, floor=8):
    while size > floor:
        f = ImageFont.truetype(font_path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(font_path, floor)


def draw_masthead(d):
    d.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    d.text((118, 10), "THE WORLD IN ONE DAY", font=F["kicker"],
           fill=(255, 255, 255))
    d.text((116, 21), "Sunday 22 November 2026", font=F["title"],
           fill=(255, 255, 255))
    d.text((118, 62),
           "Everything on this page happened, or was first reported, "
           "on Sunday 22 November 2026.",
           font=F["standfirst"], fill=(216, 222, 235))
    d.text((118, 76), "30 STORIES · 6 REGIONS · 11 DRAWN · ONE PAGE",
           font=F["counts"], fill=(240, 200, 90))
    d.rounded_rectangle([24, 8, 100, 82], 8, fill=(240, 244, 250))
    d.text((62, 11), "NOV", font=F["badge1"], fill=NAVY, anchor="ma")
    d.text((62, 26), "22", font=F["badge2"], fill=NAVY, anchor="ma")
    d.text((62, 60), "SUN · 2026", font=F["badge3"], fill=NAVY,
           anchor="ma")


def draw_band(d, y):
    total = sum(c for _, c, _ in REGION_BAND)
    x = 24
    for name, count, color in REGION_BAND:
        w_ = int((W - 48) * count / total)
        d.rectangle([x, y, x + w_, y + RAINBOW_H], fill=color)
        label = f"{name} {count}"
        tw = d.textlength(label, font=F["band"])
        d.text((x + (w_ - tw) / 2, y + 3), label, font=F["band"],
               fill=(255, 255, 255))
        x += w_
    return y + RAINBOW_H


def draw_timeline(d, y):
    d.rectangle([24, y, 122, y + TIMELINE_H], fill=NAVY)
    d.text((32, y + 4), "THE DAY", font=F["tl_head"],
           fill=(255, 255, 255))
    d.text((32, y + 18), "IN UTC", font=F["tl_head"],
           fill=(255, 255, 255))
    n = len(TIMELINE)
    bw = (W - 48 - 98 - 6 - (n - 1) * 6) / n
    x = 128.0
    for time, text in TIMELINE:
        d.rectangle([x, y, x + bw, y + TIMELINE_H], fill=(238, 233, 220))
        d.text((x + 8, y + 3), time, font=F["tl_time"], fill=DARKRED)
        d.text((x + 8, y + 18), text, font=F["tl_text"], fill=INK)
        x += bw + 6
    return y + TIMELINE_H


def draw_card(d, img, x, y, w_, story, lead=False):
    art_h = LEAD_ART_H if lead else CARD_ART_H
    head_f = F["lead_head"] if lead else F["head"]
    brief_f = F["lead_brief"] if lead else F["brief"]
    head_lh = 31 if lead else 19
    brief_lh = 15 if lead else 13
    head_lines = wrap(d, story["head"], head_f, w_ - 16)
    brief_lines = wrap(d, story["brief"], brief_f, w_ - 16)
    assert len(head_lines) <= 2, (story["n"], head_lines)
    assert len(brief_lines) <= 3, (story["n"], brief_lines)
    height = (art_h + 3 + 13 + 4 + len(head_lines) * head_lh + 2
              + len(brief_lines) * brief_lh + 4 + 11 + 8)
    d.rectangle([x, y, x + w_, y + height], fill=CARD)
    d.rectangle([x, y, x + w_, y + height], outline=RULE)
    if story.get("hero"):
        art = make_hero(ASSETS / story["art"], int(w_), art_h)
    else:
        art = make_wide(ASSETS / story["art"], int(w_), art_h,
                        story.get("focal", 0.5))
    img.paste(art, (int(x), int(y)))
    d.ellipse([x + w_ - 30, y + art_h - 30, x + w_ - 6, y + art_h - 6],
              fill=story["color"])
    d.text((x + w_ - 18, y + art_h - 24), str(story["n"]),
           font=F["num"], fill=(255, 255, 255), anchor="ma")
    ty = y + art_h + 3
    d.text((x + 8, ty), story["kicker"], font=F["kick"],
           fill=story["color"])
    ty += 13
    for ln in head_lines:
        ty += 4
        d.text((x + 8, ty), ln, font=head_f, fill=INK)
        ty += head_lh - 4
    ty += 2
    for ln in brief_lines:
        d.text((x + 8, ty), ln, font=brief_f, fill=(52, 48, 44))
        ty += brief_lh
    ty += 4
    d.text((x + 8, ty), story["tag"], font=F["tag"], fill=GRAY)
    return y + height


def draw_cards(d, img, y):
    gap = 10
    lead_w = (W - 48 - 2 * gap) / 3
    lead_bottom = y
    for i, story in enumerate(LEADS):
        b = draw_card(d, img, 24 + i * (lead_w + gap), y, lead_w,
                      story, lead=True)
        lead_bottom = max(lead_bottom, b)
    y = lead_bottom + gap
    card_w = (W - 48 - 3 * gap) / 4
    row_bottom = y
    for i, story in enumerate(ROWS):
        if i == 4:
            y = row_bottom + gap
        b = draw_card(d, img, 24 + (i % 4) * (card_w + gap), y,
                      card_w, story)
        row_bottom = max(row_bottom, b)
    return row_bottom


def lonlat_to_xy(lon, lat, x0, y0):
    return (x0 + (lon + 180) / 360 * MAP_W,
            y0 + (85 - lat) / 125 * MAP_H)


def draw_map(d, x, y):
    d.text((x, y), "WHERE IT HAPPENED", font=F["map_head"], fill=NAVY)
    my = y + 16
    rows = MAP_ROWS
    assert len(rows) == 25 and all(len(r) == 100 for r in rows)
    cw_ = MAP_W / 100
    ch_ = MAP_H / 25
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch != ".":
                d.ellipse([x + ci * cw_ + 0.4, my + ri * ch_ + 0.4,
                           x + (ci + 1) * cw_ - 0.4,
                           my + (ri + 1) * ch_ - 0.4],
                          fill=(198, 190, 172))
    for lon, lat, color in MAP_DOTS:
        px, py = lonlat_to_xy(lon, lat, x, my)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=color)
    for n, lon, lat, color in MAP_PIN_DATA:
        px, py = lonlat_to_xy(lon, lat, x, my)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color)
        d.text((px, py - 6), str(n), font=F["map_pin"],
               fill=(255, 255, 255), anchor="ma")
    label, lon, lat, color = MAP_PILL
    px, py = lonlat_to_xy(lon, lat, x, my)
    pw = d.textlength(label, font=F["map_pin"]) + 10
    d.rounded_rectangle([px - pw / 2, py - 8, px + pw / 2, py + 8], 8,
                        fill=color)
    d.text((px, py - 6), label, font=F["map_pin"],
           fill=(255, 255, 255), anchor="ma")
    ly = my + MAP_H + 6
    d.text((x, ly),
           "ASIA 3 · EUROPE 6 · AMERICAS 5 · MID EAST 6 · AFRICA 3 · GLOBAL 7",
           font=F["legend"], fill=GRAY)
    return ly + 12


def draw_also(d, x, y, w_):
    d.text((x, y), "ALSO ON SUNDAY 22 NOVEMBER", font=F["also_head"],
           fill=NAVY)
    ty = y + 14
    per_col = (len(BRIEFS) + 2) // 3
    col_w = w_ / 3
    for i, (n, color, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, per_col)
        cx = x + col * col_w
        cy = ty + row * 13
        d.text((cx, cy), f"{n}", font=F["also_num"], fill=color)
        lx = cx + d.textlength(f"{n} ", font=F["also_num"])
        d.text((lx, cy), lead, font=F["also_lead"], fill=INK)
        rx = lx + d.textlength(lead + " ", font=F["also_lead"])
        f_rest = shrink_to_fit(d, rest, FONTS["also_text"][0], 11,
                               x + (col + 1) * col_w - 8 - rx)
        d.text((rx, cy), rest, font=f_rest, fill=(52, 48, 44))
    return ty + per_col * 13


def draw_footer(d, y):
    d.rectangle([24, y, W - 24, y + 26], fill=DARKRED)
    d.text((36, y + 2), DATE_CHECK_1, font=F["datecheck"],
           fill=(255, 255, 255))
    d.text((36, y + 14), DATE_CHECK_2, font=F["datecheck"],
           fill=(255, 235, 235))
    d.text((24, y + 29), SOURCES_LINE, font=F["sources"], fill=GRAY)
    return y + 40


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_band(d, MASTHEAD_H + 2) + 4
    y = draw_timeline(d, y) + 4
    y = draw_cards(d, img, y) + 6
    map_bottom = draw_map(d, 24, y)
    also_bottom = draw_also(d, 24 + MAP_W + 16, y - 2, W - 48 - MAP_W - 16)
    bottom = max(map_bottom, also_bottom)
    end = draw_footer(d, bottom + 4)
    assert end <= H - 2, f"page overflow: ends at {end}"
    img.save(OUT)
    size = OUT.stat().st_size
    if size > 1_048_576:
        img.save(OUT.with_suffix(".jpg"), quality=88)
        print(f"PNG too big ({size}); wrote JPEG instead")
    else:
        print(f"wrote {OUT} ({size} bytes)")


# The real dot-matrix land grid (100 x 25), loaded here so the
# data tables above stay readable.
MAP_ROWS = [
    "......####............................####............#.........##.###......###.....#.....#.........",
    "....#####..##.##.##.................#########............................######...#######......##...",
    "...########################..........#######........##############################################..",
    "...############################.......#####........################################################.",
    "....####################....######.....###...#.....################################################.",
    ".....#######.###########.....######.....#.......##..#############################################...",
    "................#################...............###############################################.....",
    ".................###############...............################################################.....",
    "................###############................###..######################################..........",
    "................##############.....................#.####################################...........",
    ".................############................#########################################..............",
    "....................######.##...............########################################................",
    ".....................#####..................####################################....#...............",
    "........................###.#######.........#####################.....##########..###...............",
    "............................###########......###################.......##...##......................",
    "............................############......#################............#########..###...........",
    "............................############.......#############.#.............################.........",
    ".............................##########.........#############...................###....#####........",
    ".............................##########.........############...................####.................",
    ".............................#########...........##########..##...................##########........",
    ".............................########............#########...###.................############.......",
    ".............................#######..............#######....##..................############.......",
    ".............................######...............######..........................##########........",
    ".............................#####.................####............................########.....##..",
    ".............................####.....................................................#####.....###.",
]

if __name__ == "__main__":
    main()
