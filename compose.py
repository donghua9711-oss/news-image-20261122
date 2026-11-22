#!/usr/bin/env python3
"""Compose the entry page for make.fun news-image-20261122.

"The World in One Day" for Sunday 22 November 2026: thirty
stories from that day's reporting, set as a single newspaper
page of 1024x1024 pixels.  This edition was composed on the
morning of the day itself, while its news was still
developing; developing stories are framed on the page as
reports, and claims are attributed.

How the page is organised, top to bottom:

  * a navy masthead carrying the paper's name, the date in a
    large serif, a one-line standfirst and the page counts,
    with a small date badge at the left;
  * a coloured band split by region, each segment labelled
    with that region's story count;
  * a timeline strip, "THE DAY IN UTC", with five moments;
  * three lead cards with their artwork on top, then two
    rows of four smaller cards, eleven drawn stories in all;
  * a dot-matrix world map, "WHERE IT HAPPENED", with the
    drawn stories pinned by number, beside the remaining
    stories as numbered one-line briefs;
  * a red date-check strip and a sources line as the footer.

All lettering is typeset here with Pillow from the story
tables below, so the page text is always crisp; the artwork
in assets/ carries no lettering of its own, so nothing can
come out garbled.  SOURCES.md in this repository is the
verification record behind each line.

The composed page is written to entry.png beside this file.
If a PNG ever exceeded the bounty's 1 MiB cap the page would
be re-saved as a high-quality JPEG instead; at this palette
the PNG stays well under the cap.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

# Canvas and palette.
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

# Type: serif display faces for headlines, sans for labels,
# serif text faces for the briefs.  Sizes are chosen so the
# page stays readable from thumbnail to full size.
FONT_DIR = "/usr/share/fonts/truetype"
FONT_FILES = {
    "title": (f"{FONT_DIR}/noto/NotoSerif-Black.ttf", 37),
    "kicker": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "standfirst": (f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf", 12),
    "counts": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "badge_month": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 13),
    "badge_day": (f"{FONT_DIR}/noto/NotoSerif-Black.ttf", 30),
    "badge_year": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "band": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "tl_time": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_text": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 10),
    "kick": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 9),
    "lead_head": (f"{FONT_DIR}/noto/NotoSerif-Bold.ttf", 24),
    "lead_brief": (f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf", 12),
    "head": (f"{FONT_DIR}/noto/NotoSerif-Bold.ttf", 15),
    "brief": (f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf", 11),
    "tag": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "num": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "map_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "map_pin": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "legend": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "also_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_num": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_lead": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_text": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 11),
    "datecheck": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 9),
    "sources": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 9),
}
F = {name: ImageFont.truetype(path, size)
     for name, (path, size) in FONT_FILES.items()}

# Region segments for the coloured band, in reading order,
# with the number of this page's stories from each region.
# This edition carries six regions.
REGION_BAND = [
    ("ASIA", 3, RED), ("EUROPE", 6, NAVY), ("AMERICAS", 5, PLUM),
    ("MIDDLE EAST", 6, TEAL), ("AFRICA", 3, GOLD),
    ("GLOBAL", 7, GRAY),
]

# Five grounded moments for the timeline strip.
TIMELINE = [
    ("OVERNIGHT", "Quake strikes Peru"),
    ("EARLY", "Tankers hit near Hormuz"),
    ("MORNING", "COP31 still deadlocked"),
    ("MIDDAY", "Zelenskyy: Putin a killer"),
    ("LATEST", "Robot-weapons pact agreed"),
]

# Crop window kept for compatibility with earlier editions;
# this edition's leads all use the focal crop below.
HERO_CROP = (40, 450, 1560, 1164)

# The three lead stories, numbered 1 to 3.
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

# The eight card stories that follow the leads, numbered
# 4 to 11, in two rows of four.
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

# The remaining stories as numbered one-liners: number,
# region colour, a bold lead word or two, then the rest of
# the line in wire style.
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

# Map pins for the drawn stories, as (story number,
# longitude, latitude, region colour); a shared pill covers
# the two United States cards, and plain dots mark a spread
# of the briefs.
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

# The footer strip: what the date check promises, and the
# sources line that closes the page.
DATE_CHECK_1 = ("DATE CHECK - Every story here happened, or was first "
                "reported, on Sunday 22 November 2026.")
DATE_CHECK_2 = ("Sunday was still young when this page closed; developing "
                "stories are framed as reports, and claims are "
                "attributed.")
SOURCES_LINE = ("Sources: Reuters · AP · AFP · Al Jazeera · BBC · UN News · "
                "UKMTO · wires of 22 Nov 2026")

# Vertical layout measurements for the page furniture.
MASTHEAD_H = 90
RAINBOW_H = 17
TIMELINE_H = 34
LEAD_ART_H = 124
CARD_ART_H = 94
MAP_W, MAP_H = 300, 94


def wrap_text(draw, text, font, max_w):
    """Split text into lines that fit max_w, word by word."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def crop_to_box(path, box_w, box_h, focal=0.5):
    """Crop an artwork to a card's box around a focal point.

    The window keeps the box's aspect ratio, is centred
    vertically, and slides horizontally so the focal point
    (a fraction of the image width) stays in frame.
    """
    im = Image.open(path).convert("RGB")
    ratio = box_h / box_w
    win_w = im.width
    win_h = int(win_w * ratio)
    if win_h > im.height:
        win_h = im.height
        win_w = int(win_h / ratio)
    centre_x = int(im.width * focal)
    x0 = min(max(centre_x - win_w // 2, 0), im.width - win_w)
    y0 = (im.height - win_h) // 2
    return im.crop((x0, y0, x0 + win_w, y0 + win_h)).resize(
        (box_w, box_h), Image.LANCZOS)


def shrink_font(draw, text, font_path, size, max_w, floor=8):
    """Largest size at or below `size` that fits max_w."""
    while size > floor:
        candidate = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=candidate) <= max_w:
            return candidate
        size -= 1
    return ImageFont.truetype(font_path, floor)


def paint_masthead(draw):
    """The navy masthead: badge, paper name, date, counts."""
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    draw.text((118, 10), "THE WORLD IN ONE DAY", font=F["kicker"],
              fill=(255, 255, 255))
    draw.text((116, 21), "Sunday 22 November 2026", font=F["title"],
              fill=(255, 255, 255))
    draw.text((118, 62),
              "Everything on this page happened, or was first reported, "
              "on Sunday 22 November 2026.",
              font=F["standfirst"], fill=(216, 222, 235))
    draw.text((118, 76), "30 STORIES · 6 REGIONS · 11 DRAWN · ONE PAGE",
              font=F["counts"], fill=(240, 200, 90))
    draw.rounded_rectangle([24, 8, 100, 82], 8, fill=(240, 244, 250))
    draw.text((62, 11), "NOV", font=F["badge_month"], fill=NAVY,
              anchor="ma")
    draw.text((62, 26), "22", font=F["badge_day"], fill=NAVY,
              anchor="ma")
    draw.text((62, 60), "SUN · 2026", font=F["badge_year"], fill=NAVY,
              anchor="ma")


def paint_region_band(draw, top):
    """The rainbow band: one segment per region, by count."""
    total = sum(count for _, count, _ in REGION_BAND)
    x = 24
    for name, count, colour in REGION_BAND:
        seg_w = int((W - 48) * count / total)
        draw.rectangle([x, top, x + seg_w, top + RAINBOW_H], fill=colour)
        label = f"{name} {count}"
        label_w = draw.textlength(label, font=F["band"])
        draw.text((x + (seg_w - label_w) / 2, top + 3), label,
                  font=F["band"], fill=(255, 255, 255))
        x += seg_w
    return top + RAINBOW_H


def paint_timeline(draw, top):
    """The day-in-UTC strip: a label box and five moments."""
    draw.rectangle([24, top, 122, top + TIMELINE_H], fill=NAVY)
    draw.text((32, top + 4), "THE DAY", font=F["tl_head"],
              fill=(255, 255, 255))
    draw.text((32, top + 18), "IN UTC", font=F["tl_head"],
              fill=(255, 255, 255))
    n = len(TIMELINE)
    box_w = (W - 48 - 98 - 6 - (n - 1) * 6) / n
    x = 128.0
    for moment, text in TIMELINE:
        draw.rectangle([x, top, x + box_w, top + TIMELINE_H],
                       fill=(238, 233, 220))
        draw.text((x + 8, top + 3), moment, font=F["tl_time"],
                  fill=DARKRED)
        draw.text((x + 8, top + 18), text, font=F["tl_text"], fill=INK)
        x += box_w + 6
    return top + TIMELINE_H


def paint_card(draw, page, x, y, card_w, story, lead=False):
    """One story card: artwork on top, then kicker, headline,
    brief and source tag; returns the card's bottom edge."""
    art_h = LEAD_ART_H if lead else CARD_ART_H
    head_font = F["lead_head"] if lead else F["head"]
    brief_font = F["lead_brief"] if lead else F["brief"]
    head_step = 31 if lead else 19
    brief_step = 15 if lead else 13
    head_lines = wrap_text(draw, story["head"], head_font, card_w - 16)
    brief_lines = wrap_text(draw, story["brief"], brief_font, card_w - 16)
    assert len(head_lines) <= 2, (story["n"], head_lines)
    assert len(brief_lines) <= 3, (story["n"], brief_lines)
    height = (art_h + 3 + 13 + 4 + len(head_lines) * head_step + 2
              + len(brief_lines) * brief_step + 4 + 11 + 8)
    draw.rectangle([x, y, x + card_w, y + height], fill=CARD)
    draw.rectangle([x, y, x + card_w, y + height], outline=RULE)
    art = crop_to_box(ASSETS / story["art"], int(card_w), art_h,
                      story.get("focal", 0.5))
    page.paste(art, (int(x), int(y)))
    # The story's number rides on a coloured disc over the art.
    draw.ellipse([x + card_w - 30, y + art_h - 30,
                  x + card_w - 6, y + art_h - 6], fill=story["color"])
    draw.text((x + card_w - 18, y + art_h - 24), str(story["n"]),
              font=F["num"], fill=(255, 255, 255), anchor="ma")
    ty = y + art_h + 3
    draw.text((x + 8, ty), story["kicker"], font=F["kick"],
              fill=story["color"])
    ty += 13
    for line in head_lines:
        ty += 4
        draw.text((x + 8, ty), line, font=head_font, fill=INK)
        ty += head_step - 4
    ty += 2
    for line in brief_lines:
        draw.text((x + 8, ty), line, font=brief_font, fill=(52, 48, 44))
        ty += brief_step
    ty += 4
    draw.text((x + 8, ty), story["tag"], font=F["tag"], fill=GRAY)
    return y + height


def paint_cards(draw, page, top):
    """The lead row of three, then two rows of four cards."""
    gap = 10
    lead_w = (W - 48 - 2 * gap) / 3
    lead_bottom = top
    for i, story in enumerate(LEADS):
        bottom = paint_card(draw, page, 24 + i * (lead_w + gap), top,
                            lead_w, story, lead=True)
        lead_bottom = max(lead_bottom, bottom)
    y = lead_bottom + gap
    card_w = (W - 48 - 3 * gap) / 4
    row_bottom = y
    for i, story in enumerate(ROWS):
        if i == 4:
            y = row_bottom + gap
        bottom = paint_card(draw, page, 24 + (i % 4) * (card_w + gap),
                            y, card_w, story)
        row_bottom = max(row_bottom, bottom)
    return row_bottom


def lonlat_to_xy(lon, lat, x0, y0):
    """Project a longitude/latitude onto the map's box."""
    return (x0 + (lon + 180) / 360 * MAP_W,
            y0 + (85 - lat) / 125 * MAP_H)


def paint_map(draw, x, y):
    """The dot-matrix world map with pins, dots and legend."""
    draw.text((x, y), "WHERE IT HAPPENED", font=F["map_head"], fill=NAVY)
    map_y = y + 16
    rows = MAP_ROWS
    assert len(rows) == 25 and all(len(r) == 100 for r in rows)
    cell_w = MAP_W / 100
    cell_h = MAP_H / 25
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch != ".":
                draw.ellipse([x + ci * cell_w + 0.4,
                              map_y + ri * cell_h + 0.4,
                              x + (ci + 1) * cell_w - 0.4,
                              map_y + (ri + 1) * cell_h - 0.4],
                             fill=(198, 190, 172))
    for lon, lat, colour in MAP_DOTS:
        px, py = lonlat_to_xy(lon, lat, x, map_y)
        draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                     fill=colour)
    for n, lon, lat, colour in MAP_PIN_DATA:
        px, py = lonlat_to_xy(lon, lat, x, map_y)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=colour)
        draw.text((px, py - 6), str(n), font=F["map_pin"],
                  fill=(255, 255, 255), anchor="ma")
    label, lon, lat, colour = MAP_PILL
    px, py = lonlat_to_xy(lon, lat, x, map_y)
    pill_w = draw.textlength(label, font=F["map_pin"]) + 10
    draw.rounded_rectangle([px - pill_w / 2, py - 8,
                            px + pill_w / 2, py + 8], 8, fill=colour)
    draw.text((px, py - 6), label, font=F["map_pin"],
              fill=(255, 255, 255), anchor="ma")
    legend_y = map_y + MAP_H + 6
    draw.text((x, legend_y),
              "ASIA 3 · EUROPE 6 · AMERICAS 5 · MID EAST 6 · "
              "AFRICA 3 · GLOBAL 7",
              font=F["legend"], fill=GRAY)
    return legend_y + 12


def paint_briefs(draw, x, y, width):
    """The one-line briefs in three columns, numbered."""
    draw.text((x, y), "ALSO ON SUNDAY 22 NOVEMBER",
              font=F["also_head"], fill=NAVY)
    ty = y + 14
    per_col = (len(BRIEFS) + 2) // 3
    col_w = width / 3
    for i, (n, colour, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, per_col)
        cx = x + col * col_w
        cy = ty + row * 13
        draw.text((cx, cy), f"{n}", font=F["also_num"], fill=colour)
        lead_x = cx + draw.textlength(f"{n} ", font=F["also_num"])
        draw.text((lead_x, cy), lead, font=F["also_lead"], fill=INK)
        rest_x = lead_x + draw.textlength(lead + " ",
                                          font=F["also_lead"])
        rest_font = shrink_font(draw, rest, FONT_FILES["also_text"][0],
                                11, x + (col + 1) * col_w - 8 - rest_x)
        draw.text((rest_x, cy), rest, font=rest_font, fill=(52, 48, 44))
    return ty + per_col * 13


def paint_footer(draw, y):
    """The red date-check strip and the sources line."""
    draw.rectangle([24, y, W - 24, y + 26], fill=DARKRED)
    draw.text((36, y + 2), DATE_CHECK_1, font=F["datecheck"],
              fill=(255, 255, 255))
    draw.text((36, y + 14), DATE_CHECK_2, font=F["datecheck"],
              fill=(255, 235, 235))
    draw.text((24, y + 29), SOURCES_LINE, font=F["sources"], fill=GRAY)
    return y + 40


def verify_output(path):
    """Re-read the composed page and check it against the
    bounty's caps, so a bad page is caught here rather than
    by the grader: the file must be a PNG of at most
    1024x1024 pixels and at most 1 MiB.

    The width and height come from the PNG's IHDR chunk -
    the first chunk after the 8-byte signature: 4 bytes of
    length, the type "IHDR", then width and height as
    big-endian integers - never from the file name.
    """
    import struct

    blob = path.read_bytes()
    signature = b"\x89PNG\r\n\x1a\n"
    if not blob.startswith(signature):
        raise SystemExit(f"{path} is not a PNG file")
    if blob[12:16] != b"IHDR":
        raise SystemExit(f"{path}: first chunk is not IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(
            f"{path} is {width}x{height}, over the 1024x1024 cap")
    if len(blob) > 1_048_576:
        raise SystemExit(
            f"{path} is {len(blob)} bytes, over the 1 MiB cap")
    print(f"verified {path.name}: {width}x{height}, "
          f"{len(blob)} bytes, within both caps")
    return width, height


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    paint_masthead(draw)
    y = paint_region_band(draw, MASTHEAD_H + 2) + 4
    y = paint_timeline(draw, y) + 4
    y = paint_cards(draw, page, y) + 6
    map_bottom = paint_map(draw, 24, y)
    also_bottom = paint_briefs(draw, 24 + MAP_W + 16, y - 2,
                               W - 48 - MAP_W - 16)
    bottom = max(map_bottom, also_bottom)
    end = paint_footer(draw, bottom + 4)
    assert end <= H - 2, f"page overflow: ends at {end}"
    page.save(OUT)
    verify_output(OUT)
    size = OUT.stat().st_size
    if size > 1_048_576:
        page.save(OUT.with_suffix(".jpg"), quality=88)
        print(f"PNG too big ({size}); wrote JPEG instead")
    else:
        print(f"wrote {OUT} ({size} bytes)")


# The dot-matrix land grid for the map (100 columns by 25
# rows), kept at the end so the story tables above stay
# readable.  Each '#' is one dot of land.
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
