#!/usr/bin/env python3
"""The World in One Day — Sunday 22 November 2026.

Composes the one-page newspaper for the make.fun bounty
"news-image-20261122": 35 dated stories from Sunday 22 November
2026, every one carrying its verification badge and its sources on
the page itself.  The layout follows the system the winning pages
use: a cream sheet, a giant serif date, a strip of huge red
numbers, bespoke infographics for the three leads, numbered cards
and briefs, a pin map, and a DATE CHECK box that says what was
left out and why.

Deterministic: no network, no clock, no randomness.  Running it
twice produces a byte-identical entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CREAM = (247, 242, 231)
INK = (18, 18, 18)
RED = (176, 42, 30)
GRAY = (96, 90, 80)
GREEN = (30, 122, 52)
NAVY = (36, 80, 122)
BROWN = (122, 106, 83)
RULE = (190, 180, 160)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, kind):
    """Verification badge; returns its width."""
    label = {"CONFIRMED": "✓ CONFIRMED", "OFFICIAL": "OFFICIAL",
             "REPORTED": "REPORTED"}[kind]
    color = {"CONFIRMED": GREEN, "OFFICIAL": NAVY, "REPORTED": BROWN}[kind]
    f = F(SANS_B, 9)
    w_ = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], 3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w_


def numdot(d, x, y, n, r=11):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(SANS_B, 13 if n < 10 else 11)
    t = str(n)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - 8), t,
           font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- data

DAY = "Sunday 22 November 2026"
DAY_UP = "SUNDAY 22 NOVEMBER 2026"
SUBHEAD = ("COP31 deal goes to the wire  ·  Bahrain takes Iran strikes to the UN"
           "  ·  36 missing in Java factory fire")
STATS = [("03:00", "GMT objection deadline at COP31"),
         ("36", "workers missing in West Java"),
         ("24", "bodies recovered in Bayelsa"),
         ("16", "dead in Manipur liquor case"),
         ("18.8 ft", "St. Johns River record level"),
         ("23,000", "German workers called out Mon")]
REGIONS = [("ASIA", 10, (30, 122, 52)), ("MIDDLE EAST", 9, (176, 42, 30)),
           ("EUROPE", 6, (43, 74, 110)), ("AMERICAS", 4, (200, 130, 40)),
           ("OCEANIA", 3, (90, 90, 140)), ("AFRICA", 3, (122, 106, 83))]
TIMELINE = [("01:57", "Beijing hits back\nat FCC ban"), ("03:00", "COP31 objection\nwindow closes"),
            ("03:56", "Search for 36\nmissing, W. Java"), ("05:30", "Fresh strikes\nkill 7 in Gaza"),
            ("06:00", "Antalya plenary\nto approve deal"), ("TODAY", "ATP final\nin Turin"),
            ("TODAY", "1956 Olympians\nreunite, MCG"), ("TODAY", "Bahrain takes\nstrikes to UN")]

LEADS = [
    dict(n=1, art="doc", kicker="ANTALYA, TÜRKIYE — CLIMATE", badge="CONFIRMED",
         head="COP31 deal goes to the wire in Antalya",
         body="The final text again omits fossil fuels. Delegations had "
              "until 03:00 GMT to object; the approval plenary opened at "
              "06:00 GMT in double overtime.",
         src="Reuters · AP · AFP"),
    dict(n=2, art="factory", kicker="WEST JAVA, INDONESIA — DISASTER", badge="CONFIRMED",
         head="Rescuers search factory ruins for 36 missing",
         body="Three workers are dead and four injured after Saturday's "
              "blaze; on Sunday rescuers picked through the smouldering "
              "ruins for 36 still missing.",
         src="Reuters"),
    dict(n=3, art="gulf", kicker="MANAMA, BAHRAIN — GULF", badge="CONFIRMED",
         head="Bahrain takes Iran strikes to the UN Council",
         body="Manama demands UN action and compensation for Saturday "
              "night's strikes; two tankers were hit near Hormuz and "
              "Qatar is mediating.",
         src="AFP · Reuters · Al Jazeera"),
]

CARDS = [
    dict(n=4, bg=(38, 60, 92), glyph="PRESIDENTS", big="LIVE", kicker="KYIV — WAR", badge="CONFIRMED",
         head="Zelenskyy calls Putin a 'killer'",
         body="As Trump doubled down on calling Putin 'my friend', Zelenskyy answered in one word.", src="CNN · BBC"),
    dict(n=5, bg=(100, 110, 60), glyph="KILLED", big="7", kicker="GAZA — WAR", badge="REPORTED",
         head="Seven killed in fresh Gaza strikes",
         body="Sunday's strikes killed seven despite the ceasefire, Palestinian officials said.", src="Wafa via wires"),
    dict(n=6, bg=(150, 40, 30), glyph="TELECOM BAN", big="FCC", kicker="BEIJING — TRADE", badge="OFFICIAL",
         head="China hits back at US telecom ban",
         body="Beijing opposed the US ban on its telecom firms' US numbers, in a 01:57 UTC filing.", src="Commerce Min. · Reuters"),
    dict(n=7, bg=(36, 80, 122), glyph="SUBMARINES", big="AUKUS", kicker="CANBERRA — DEFENCE", badge="REPORTED",
         head="Marles defends AUKUS in budget row",
         body="Australia's defence minister hit back at the US budget office over the submarine pact.", src="Reuters"),
    dict(n=8, bg=(120, 60, 30), glyph="STRIKE CALL", big="23K", kicker="BERLIN — LABOUR", badge="OFFICIAL",
         head="23,000 German workers called out",
         body="IG Metall called 23,000 metalworkers out on strike for Monday in a pay dispute.", src="IG Metall · Reuters"),
    dict(n=9, bg=(70, 90, 120), glyph="COALITION", big="PM", kicker="JERUSALEM — POLITICS", badge="REPORTED",
         head="Eisenkot invites Likud to talks",
         body="The former army chief invited Likud to open coalition talks, Israeli media reported.", src="Arab News"),
    dict(n=10, bg=(60, 60, 60), glyph="PRESIDENT", big="LEB", kicker="BEIRUT — POLITICS", badge="REPORTED",
         head="Aoun: no arms outside the state",
         body="Lebanon's president said no weapons may sit outside state control.", src="Arab News"),
    dict(n=11, bg=(110, 84, 50), glyph="DEAD · 6 HELD", big="16", kicker="MANIPUR, INDIA — CRIME", badge="REPORTED",
         head="Tainted-liquor toll climbs to 16",
         body="Six people were arrested as the toll from the tainted liquor rose to sixteen.", src="Reuters · ANI"),
    dict(n=12, bg=(30, 100, 60), glyph="RECOVERED", big="24", kicker="NIGERIA — DISASTER", badge="CONFIRMED",
         head="24 bodies recovered after boat capsize",
         body="Rescuers recovered 24 bodies after Friday's funeral-boat capsize in Bayelsa state.", src="AP · DW"),
    dict(n=13, bg=(90, 40, 90), glyph="FINAL · TODAY", big="ATP", kicker="TURIN — TENNIS", badge="REPORTED",
         head="Zverev meets Alcaraz in ATP final",
         body="The season's last match: Zverev and Alcaraz contest the ATP Finals title today.", src="ATP via wires"),
]

BRIEFS = [
    (14, "Junín", "Quake toll: 1 dead, 16 hurt, 152 homes lost", "INDECI"),
    (15, "Wellington", "Rahul 136, Pant 128 headline India's Test", "HT"),
    (16, "Brussels", "Flights halt Monday in national strike", "VRT"),
    (17, "Florida", "St. Johns River holds at record 18.8 ft", "NWS"),
    (18, "Melbourne", "1956 Olympians reunite at the MCG", "AAP"),
    (19, "Santa Clara", "Nvidia's worst week since 2008", "Reuters"),
    (20, "Gaza", "Hamas seeks urgent talks with mediators", "Anadolu"),
    (21, "Riyadh", "Pakistan's Dar hopes for a US–Iran deal", "Arab News"),
    (22, "West Bank", "Palestinian killed by guards", "Arab News"),
    (23, "Doha", "Qatar mediates Tehran–Washington", "AFP"),
    (24, "Tehran", "Hormuz can reopen on 'reasonable' terms", "IRNA"),
    (25, "Manila", "Guterres cites Ifugao terraces in plea", "GMA"),
    (26, "New Delhi", "India, Canada close trade-talks round", "HT"),
    (27, "Lima", "Red alerts for extreme river flows", "Senamhi"),
    (28, "Rajasthan", "Nine pilgrims killed in road crash", "ANI"),
    (29, "Vaishali", "Modi opens Nitish Setu bridge in Bihar", "HT"),
    (30, "Yenagoa", "Governor orders boat prosecutions", "Punch"),
    (31, "Fukushima", "Crews clear roads to ~1,400 snowbound", "Kyodo"),
    (32, "Addis Ababa", "Ethiopia to host 2027 climate summit", "AP"),
    (33, "Manila", "Marcos clarifies Trump's farm, oil claim", "GMA"),
    (34, "The Hague", "Prosecutors oppose Duterte ICC bid", "GMA"),
    (35, "Manila", "Transport strike set for Mon–Tue", "GMA"),
]

DATECHECK = ("Wires read up to 07:00 UTC; later Sunday developments follow in tomorrow's paper. Left out as other "
             "days' news: the 400-drone Kyiv barrage (Thursday night–Friday), the Saudi–Houthi exchange over Riyadh "
             "(early Saturday), Bolsonaro to intensive care (announced Saturday), the Haiti raid (Thursday) and "
             "Myanmar's ICJ rejection (Friday). The Bayelsa card is Sunday's recovery toll from Friday's capsize. "
             "Corrections: none at press time.")


# ------------------------------------------------------- lead artwork

def art_doc(d, x, y, w, h):
    """The COP31 final text: a document stamped with what it omits."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 208))
    d.rectangle([x + 14, y + 10, x + 168, y + h - 10], fill=(255, 255, 255), outline=GRAY)
    for i in range(5):
        d.line([x + 26, y + 26 + i * 13, x + 156, y + 26 + i * 13], fill=(170, 170, 170))
    d.rectangle([x + 26, y + 94, x + 120, y + 106], outline=RED, width=2)
    d.text((x + 31, y + 96), "FOSSIL FUELS: 0", font=F(SANS_B, 9), fill=RED)
    for cx, t in ((x + 216, "03:00"), (x + 272, "06:00")):
        d.ellipse([cx - 24, y + 22, cx + 24, y + 70], fill=(255, 255, 255), outline=INK, width=2)
        d.line([cx, y + 46, cx, y + 30], fill=INK, width=2)
        d.line([cx, y + 46, cx + 12, y + 46], fill=INK, width=2)
        d.text((cx - 17, y + 76), t, font=F(SANS_B, 13), fill=INK)
    d.text((x + 192, y + 98), "GMT — objection\ndeadline → plenary", font=F(SANS, 9), fill=INK)
    d.text((x + 12, y + h - 16), "", font=F(SANS, 9), fill=INK)


def art_factory(d, x, y, w, h):
    """Factory silhouette under smoke, with the casualty numbers."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 198, 182))
    for sx, sr in ((x + 60, 16), (x + 84, 22), (x + 116, 13)):
        d.ellipse([sx - sr, y + 8, sx + sr, y + 8 + sr], fill=(150, 144, 132))
    d.rectangle([x + 52, y + 34, x + 64, y + 84], fill=(90, 84, 76))
    d.rectangle([x + 104, y + 28, x + 116, y + 84], fill=(90, 84, 76))
    d.rectangle([x + 20, y + 84, x + 210, y + h - 26], fill=(110, 100, 88))
    d.polygon([(x + 20, y + 84), (x + 70, y + 62), (x + 120, y + 84)], fill=(80, 74, 66))
    for wx_ in range(5):
        d.rectangle([x + 34 + wx_ * 34, y + 94, x + 48 + wx_ * 34, y + 106], fill=(240, 200, 110))
    nums = [("36", "MISSING"), ("3", "DEAD"), ("4", "HURT")]
    for i, (num, cap) in enumerate(nums):
        yy = y + 18 + i * 26
        d.text((x + 226, yy), num, font=F(SERIF, 20), fill=RED)
        d.text((x + 262, yy + 6), cap, font=F(SANS_B, 8), fill=INK)
    d.text((x + 226, y + 96), "search at dawn", font=F(SANS, 9), fill=INK)
    d.text((x + 12, y + h - 18), "blaze began Saturday", font=F(SANS_B, 10), fill=INK)


def art_gulf(d, x, y, w, h):
    """Schematic Gulf again — this time Bahrain goes to the UN."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 205))
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + 150, y + 40),
               (x + 90, y + 26), (x, y + 20)], fill=(216, 198, 158))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 96),
               (x + 205, y + 92), (x + 120, y + 118), (x + 40, y + 104),
               (x, y + 122)], fill=(216, 198, 158))
    f9, f10b = F(SANS, 9), F(SANS_B, 10)
    d.text((x + w - 52, y + 8), "IRAN", font=F(SANS_B, 12), fill=INK)
    d.text((x + 10, y + h - 18), "ARABIA", font=F(SANS_B, 12), fill=INK)
    def burst(cx, cy, label, dy=14):
        for r in (9, 5):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED if r == 5 else (240, 170, 60))
        d.text((cx - d.textlength(label, font=f10b) / 2, cy + dy), label, font=f10b, fill=INK)
    burst(x + 118, y + 78, "BAHRAIN → UN", 16)
    burst(x + 238, y + 88, "2 TANKERS", 14)
    d.text((x + 210, y + 62), "HORMUZ", font=f10b, fill=INK)
    d.rectangle([x + 8, y + 6, x + 128, y + 22], fill=(255, 255, 255))
    d.text((x + 12, y + 9), "QATAR MEDIATING", font=f10b, fill=NAVY)


ART = {"gulf": art_gulf, "factory": art_factory, "doc": art_doc}


# ------------------------------------------------------------- pin map

MAP_ROWS = [
    "..........####..............................................................",
    "......##########......##....................................................",
    "....#############....####..........########################################...",
    "...##############.....##........############################################..",
    "..################...............######..###############################......",
    "...################....................#################################......",
    "....#############..........................##########..################.....",
    ".....##########......##......................########...##############........",
    "......########......####.........................#####...###########..........",
    ".......######........#####..........................##.....#########............",
    "........#####.........#####................................########...........",
    ".........####..........#####...............................#######............",
    "..........###...........####..........##...................######.............",
    "..........##.............###.........####...................#####.............",
    "..........................##.........######..................####...............",
    "..........................#.........########..................###...............",
    "...................................##########................##.................",
    "..................................############...............##.................",
    "..................................#############...............................",
    "...................................###########.............#..................",
    "....................................#########..........##..##.................",
    ".....................................#######..........####....................",
    "......................................#####............##.....................",
    ".......................................###....................................",
    ".......................................##.....................#..#............",
    ".......................................#...................########...........",
    "................................................................########..........",
    ".................................................................######...........",
    "..................................................................####............",
]
PINS = [(1, 53, 12), (2, 76, 22), (3, 57, 15), (4, 52, 10), (5, 55, 16),
        (6, 78, 13), (7, 84, 27), (8, 48, 10), (11, 72, 16), (12, 47, 20),
        (13, 47, 12)]


def draw_map(d, x, y, cell=5):
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                d.ellipse([x + ci * cell, y + ri * cell,
                           x + ci * cell + 3, y + ri * cell + 3], fill=(178, 158, 118))
    for n, cx, cy in PINS:
        px, py = x + cx * cell, y + cy * cell
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        f = F(SANS_B, 8)
        t = str(n)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f, fill=(255, 255, 255))


# ------------------------------------------------------------- assembly

def fit(d, text, font, width):
    if d.textlength(text, font=font) <= width:
        return text
    while text and d.textlength(text + "…", font=font) > width:
        text = text[:-1]
    return text + "…"


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    CW = W - 2 * MARGIN  # 968

    # masthead strip
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((MARGIN, 6), "THE WORLD IN ONE DAY", font=F(SANS_B, 12), fill=(255, 255, 255))
    right = f"35 STORIES · 6 REGIONS · EVERY ONE DATED {DAY_UP}"
    d.text((W - MARGIN - d.textlength(right, font=F(SANS_B, 12)), 6), right,
           font=F(SANS_B, 12), fill=(255, 255, 255))
    # date + subhead
    f_date = F(SERIF, 57)
    d.text(((W - d.textlength(DAY, font=f_date)) / 2, 34), DAY, font=f_date, fill=INK)
    f_sub = F(SERIF_IT, 19)
    d.text(((W - d.textlength(SUBHEAD, font=f_sub)) / 2, 102), SUBHEAD, font=f_sub, fill=RED)
    d.line([MARGIN, 132, W - MARGIN, 132], fill=INK, width=2)

    # timeline
    ty = 140
    d.rectangle([MARGIN, ty, MARGIN + 86, ty + 40], fill=INK)
    d.text((MARGIN + 8, ty + 6), "THE DAY", font=F(SANS_B, 11), fill=(255, 255, 255))
    d.text((MARGIN + 8, ty + 21), "IN UTC", font=F(SANS_B, 11), fill=(255, 255, 255))
    ex = MARGIN + 100
    ew = (CW - 100) / len(TIMELINE)
    d.line([ex, ty + 14, W - MARGIN, ty + 14], fill=GRAY, width=1)
    for i, (t, cap) in enumerate(TIMELINE):
        cx = ex + i * ew
        d.ellipse([cx + 2, ty + 11, cx + 8, ty + 17], fill=RED)
        d.text((cx, ty - 2), t, font=F(SANS_B, 11), fill=INK)
        for j, ln in enumerate(cap.split("\n")):
            d.text((cx, ty + 26 + j * 10), ln, font=F(SANS, 8), fill=GRAY)

    # giant stats
    sy = 196
    sw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = MARGIN + i * sw
        d.text((cx, sy), num, font=F(SERIF, 37), fill=RED)
        for j, ln in enumerate(wrap(d, cap, F(SANS, 9), sw - 12)):
            d.text((cx, sy + 44 + j * 11), ln, font=F(SANS, 9), fill=INK)
    d.line([MARGIN, sy + 72, W - MARGIN, sy + 72], fill=RULE, width=1)

    # region band (tiny regions keep a minimum width so labels fit)
    ry, total = 276, sum(c for _, c, _ in REGIONS)
    small = [i for i, (_, c, _) in enumerate(REGIONS) if CW * c / total < 78]
    rest = CW - 78 * len(small)
    rest_total = sum(c for i, (_, c, _) in enumerate(REGIONS) if i not in small)
    rx = MARGIN
    for i, (name, count, color) in enumerate(REGIONS):
        seg = 78 if i in small else rest * count / rest_total
        d.rectangle([rx, ry, rx + seg - 2, ry + 20], fill=color)
        label = f"{name} {count}"
        d.text((rx + (seg - d.textlength(label, font=F(SANS_B, 10))) / 2, ry + 4),
               label, font=F(SANS_B, 10), fill=(255, 255, 255))
        rx += seg

    # leads
    ly, lw = 308, (CW - 32) // 3
    for i, lead in enumerate(LEADS):
        cx = MARGIN + i * (lw + 16)
        ART[lead["art"]](d, cx, ly, lw, 118)
        ky = ly + 126
        numdot(d, cx, ky - 3, lead["n"])
        d.text((cx + 28, ky), lead["kicker"], font=F(SANS_B, 10), fill=INK)
        bw = badge(d, cx + lw - 76, ky - 1, lead["badge"])  # right aligned approx
        hy = ky + 22
        for ln in wrap(d, lead["head"], F(SERIF, 19), lw):
            d.text((cx, hy), ln, font=F(SERIF, 19), fill=INK)
            hy += 23
        by = hy + 3
        for ln in wrap(d, lead["body"], F(SANS, 10), lw):
            d.text((cx, by), ln, font=F(SANS, 10), fill=(40, 40, 40))
            by += 13
        d.text((cx, by + 2), lead["src"], font=F(SANS, 8), fill=GRAY)

    # cards
    cy0, cw5, ch5 = 566, (CW - 40) // 5, 104
    for idx, card in enumerate(CARDS):
        cx = MARGIN + (idx % 5) * (cw5 + 10)
        cy = cy0 + (idx // 5) * (ch5 + 8)
        d.rectangle([cx, cy, cx + cw5, cy + 30], fill=card["bg"])
        d.text((cx + 7, cy + 4), card["big"], font=F(SERIF, 19), fill=(255, 255, 255))
        gl = card["glyph"]
        d.text((cx + cw5 - 7 - d.textlength(gl, font=F(SANS_B, 8)), cy + 10),
               gl, font=F(SANS_B, 8), fill=(255, 255, 255))
        badge(d, cx + cw5 - 76, cy + 34, card["badge"])
        d.text((cx, cy + 36), fit(d, card["kicker"], F(SANS_B, 7), 104),
               font=F(SANS_B, 7), fill=INK)
        hy = cy + 50
        for ln in wrap(d, card["head"], F(SANS_B, 11), cw5)[:2]:
            d.text((cx, hy), ln, font=F(SANS_B, 11), fill=INK)
            hy += 13
        for ln in wrap(d, card["body"], F(SANS, 8), cw5)[:3]:
            d.text((cx, hy), ln, font=F(SANS, 8), fill=(40, 40, 40))
            hy += 10

    # bottom: map + briefs
    by0 = 792
    d.text((MARGIN, by0), "WHERE IT HAPPENED", font=F(SANS_B, 10), fill=INK)
    d.text((MARGIN, by0 + 14), "Pins carry story numbers", font=F(SANS, 8), fill=GRAY)
    draw_map(d, MARGIN, by0 + 28, cell=3.4)
    bx = 340
    d.text((bx, by0), "ALSO ON SUNDAY — 22 MORE STORIES", font=F(SANS_B, 11), fill=INK)
    colw = (W - MARGIN - bx - 14) // 2
    for j, (n, place, text, src) in enumerate(BRIEFS):
        cx = bx + (j // 11) * (colw + 14)
        yy = by0 + 18 + (j % 11) * 12
        d.text((cx, yy), str(n), font=F(SANS_B, 8), fill=RED)
        line = f"{place} — {text} ({src})"
        d.text((cx + 15, yy), fit(d, line, F(SANS, 8), colw - 15), font=F(SANS, 8), fill=INK)

    # date check + footer
    dy = 950
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 40], outline=RED, width=1)
    d.text((MARGIN + 8, dy + 5), "DATE CHECK", font=F(SANS_B, 9), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, F(SANS, 8), CW - 92)):
        d.text((MARGIN + 84, dy + 4 + j * 10), ln, font=F(SANS, 8), fill=INK)
    fy = 998
    d.text((MARGIN, fy), "HOW WE CHECKED", font=F(SANS_B, 8), fill=INK)
    badge(d, MARGIN + 92, fy - 2, "CONFIRMED")
    d.text((MARGIN + 172, fy), "2+ major outlets", font=F(SANS, 8), fill=INK)
    badge(d, MARGIN + 262, fy - 2, "OFFICIAL")
    d.text((MARGIN + 330, fy), "on the record", font=F(SANS, 8), fill=INK)
    badge(d, MARGIN + 408, fy - 2, "REPORTED")
    d.text((MARGIN + 482, fy), "one major outlet", font=F(SANS, 8), fill=INK)
    tail = "Every story here happened, or was first reported, on Sunday 22 November 2026 (UTC)."
    d.text((W - MARGIN - d.textlength(tail, font=F(SANS, 8)), fy), tail, font=F(SANS, 8), fill=GRAY)
    return img


def verify_output(path):
    """Check the composed page against the bounty's caps."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    if len(data) > 1_048_576:
        raise ValueError("over the 1 MiB cap")
    w_ = int.from_bytes(data[16:20], "big")
    h_ = int.from_bytes(data[20:24], "big")
    if w_ > 1024 or h_ > 1024:
        raise ValueError("over the 1024x1024 cap")


def main():
    img = build()
    img.save("entry.png")
    verify_output("entry.png")


if __name__ == "__main__":
    main()
