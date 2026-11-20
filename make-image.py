#!/usr/bin/env python3
"""Draw the entry image for make.fun's news-image-20261119 competition.

The image is a one-page newspaper front page, "The World in One Day",
summing up the real world news of Thursday 19 November 2026: three lead
stories with drawn illustrations, seven regional sections of shorter
stories, and an "In brief" strip. Every story is dated to that day and
carries the source it was reported by.

Run it with:  python3 make-image.py
It writes entry.png next to this file (1024 x 1024, well under 1 MiB).
main.ts then copies that file to the grader's output directory.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 236)
INK = (18, 20, 24)
GRAY = (92, 92, 88)
ACCENT = (176, 42, 33)
RULE = (18, 20, 24)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = "LiberationSerif-Bold.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"
SANS_I = "LiberationSans-Italic.ttf"


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, measuring with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, line_h, fill=INK):
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += line_h
    return y


# ---------------------------------------------------------------- stories
# (headline, summary, source) — all events of Thursday 19 November 2026.

LEADS = [
    {
        "kicker": "THE HAGUE · WORLD COURT",
        "art": "scales",
        "headline": "World Court Rules Myanmar Committed Genocide Against the Rohingya",
        "summary": (
            "The International Court of Justice ruled 9-6 that Myanmar's 2017 "
            "clearance operations in northern Rakhine were genocide and ordered "
            "reparations — a first such finding, watched live by a million "
            "Rohingya in Bangladesh's refugee camps."
        ),
        "source": "International Court of Justice · Reuters",
    },
    {
        "kicker": "SHENZHEN · TRILATERAL SUMMIT",
        "art": "flags",
        "headline": "Trump, Xi and Putin End First Trilateral Summit With Pledge Against Nuclear War",
        "summary": (
            "The three leaders met in Shenzhen for their first three-way summit "
            "and issued a joint declaration on nuclear-risk talks, UN reform and "
            "energy security. No deal was reached on Ukraine or Iran."
        ),
        "source": "Reuters",
    },
    {
        "kicker": "WALL STREET · RECORD IPO",
        "art": "chart",
        "headline": "Anthropic's Record $81 Billion IPO Fails to Stop the AI Slide",
        "summary": (
            "Anthropic priced its debut at $83 a share — the largest IPO in "
            "history — and the stock leapt 34% before closing at $97. The wider "
            "market still slumped 2% to seven-month lows."
        ),
        "source": "Reuters · Dow Jones",
    },
]

SECTIONS = [
    ("MIDDLE EAST & THE GULF", [
        ("US Senate Rejects Iran War-Powers Bill, 51-48",
         "It would have forced Trump to end the Iran war or seek Congress's approval; three Republicans backed it.",
         "Reuters"),
        ("Iran Widens Gulf Attacks as US Blockade Holds",
         "Tehran fired on Kuwait and Bahrain; a tanker was struck in the Strait of Hormuz as fighting intensified.",
         "10 Things Global News"),
        ("Suspected Houthi Missile Damages Riyadh Tower",
         "Windows were blown out across seven floors of the PIF Tower early Thursday; no casualties reported.",
         "The Top Five Brief"),
        ("Israeli Forces Cross Gaza Ceasefire Line",
         "Israel said a tank operation in central Gaza dismantled a Hamas tunnel, beyond the ceasefire boundary.",
         "Wire reports"),
        ("IEA: Iran War May Cut Reliance on Hormuz",
         "The agency says the war may permanently slash world dependence on the strait as other routes grow.",
         "Dow Jones"),
    ]),
    ("EUROPE", [
        ("EU Proposes €45 Billion Loan for Ukraine",
         "Brussels put the package forward as European leaders prepared to join new Ukraine peace talks.",
         "10 Things Global News"),
        ("UK Pledges 1,000 Drones for Ukraine, £260m",
         "The package covers long-range drones and other capabilities, London announced on Thursday.",
         "Wire reports"),
        ("UK and Norway Fund Two Ukrainian Naval Craft",
         "The two will split over £100 million through the Maritime Capability Coalition; built in the UK.",
         "Wire reports"),
        ("Denmark Approves Greenland-US Security Pact",
         "All 109 lawmakers backed the expanded Arctic defence arrangement with Washington and Nuuk.",
         "Wire reports"),
        ("Serbia Elects Student-Backed Speaker",
         "Aleksandar Cupic of the Student List won with 140 votes on day three of the new parliament.",
         "Wire reports"),
    ]),
    ("ASIA-PACIFIC", [
        ("India Evacuates 47,000 as Cyclone Akvan Nears",
         "Odisha moved 47,000 people to safety and shut schools as the third cyclone in a month neared landfall.",
         "Reuters"),
        ("South Korea Court Overturns Ex-PM's Sentence",
         "The Supreme Court ordered a retrial for Han Duck-soo but reaffirmed martial law was unconstitutional.",
         "Wire reports"),
        ("Mongolia President Resigns; Parliament Accepts",
         "Khurelsukh Ukhnaa stepped down amid claims he benefited financially from a railway project.",
         "Wire reports"),
        ("Russian Bombers Back in Vietnam, Near Taiwan",
         "Taiwan tracked two Tu-95s near the island, the week's second such flight, as bombers returned to Vietnam.",
         "Wire reports"),
        ("Bangladesh Garment Protests Enter Third Week",
         "Police used tear gas as dozens of factories stayed shut; workers demand a 30,000-taka minimum wage.",
         "Global 5 Brief"),
    ]),
    ("THE AMERICAS", [
        ("Walmart Revenue Hits $188.8 Billion, Up 5.2%",
         "US e-commerce grew 23% as value shoppers drove growth; the retailer raised its full-year outlook.",
         "Dow Jones"),
        ("US Jobless Claims Unexpectedly Move Higher",
         "New claims rose last week and continuing claims surged the week before, the Labor Department said.",
         "Dow Jones"),
        ("Florida River Tops Its 1953 Flood Record",
         "The St. Johns River near Cocoa passed 18 feet after days of rain, closing schools, prompting rescues.",
         "The Top Five Brief"),
        ("Democrats Probe Nvidia Role in Chip Inquiry",
         "House lawmakers asked Commerce what influence Nvidia had over the Megaspeed chip-diversion probe.",
         "Reuters"),
        ("Trump to Pardon Pete Rose Posthumously",
         "The president said the late baseball star will receive a posthumous pardon.",
         "Wire reports"),
    ]),
    ("AFRICA", [
        ("Dozens Missing as Boat Capsizes Off Senegal",
         "The Europe-bound boat capsized off the Senegalese coast Thursday, an NGO said — the route's latest loss.",
         "Reuters"),
        ("Ethiopia, Eritrea Mass Troops Along Border",
         "Monitors say both armies gathered within striking distance; Eritrea calls clash reports propaganda.",
         "Global 5 Brief"),
        ("Somalia Orders UAE Envoy Out in 72 Hours",
         "Mogadishu recalled its own envoy too, accusing Abu Dhabi of undermining Somali sovereignty.",
         "Wire reports"),
    ]),
    ("SCIENCE & SPACE", [
        ("Voyager 1 Phones Home From One Light-Day Away",
         "NASA got a signal sent 24 hours earlier from 16 billion miles out — a first for any spacecraft.",
         "NASA via Phys.org"),
        ("Google Books New Glenn for AI Satellites",
         "Blue Origin will launch Project Suncatcher satellites carrying Google's AI chips in early 2029.",
         "Tickline News"),
        ("BepiColombo Arrives at Mercury",
         "The probe prepared for orbit insertion; its UK-built telescope sent first X-ray views en route.",
         "Orbital Wire"),
        ("China Rolls Out Rocket for Shenzhou-24",
         "A Long March 2F was rolled out for the flight, which will carry a Pakistani astronaut.",
         "Orbital Wire"),
    ]),
    ("SPORT", [
        ("Shelton Reaches ATP Finals Semi-Finals",
         "Shelton beat Jodar 7-6(8), 7-5 in Turin; Zverev finished group play 3-0 by beating Fils.",
         "Sports Wire"),
        ("Barcelona Women Rout Servette 6-0",
         "Lyon won 2-0 at Arsenal and Chelsea beat PSG 1-0 to top the league phase in the Champions League.",
         "Sports Wire"),
        ("England Beat Australia to Win ODI Series",
         "The 97-run win in Hobart sealed the one-day series 2-1 for England over Australia.",
         "Sports Wire"),
    ]),
]

BRIEFS = [
    "COP31: outcry as fossil fuels vanish from draft climate deal — Le Monde",
    "Japan and India agree to deepen military cooperation — Wire reports",
    "South Africa's Reserve Bank holds its repo rate at 7.25% — Dow Jones",
    "Euclid telescope releases 15,000 gravitational-lens candidates — Orbital Wire",
    "Darts: Wattimena knocks out champion Littler at the Grand Slam — BehindLines",
    "EU agrees to delay methane emissions law to 2029 — Le Monde",
    "France orders internet giants to share revenue with media — Le Monde",
    "Japan inflation accelerates as BOJ chief signals near-term rate hike — Reuters",
    "Australia's jobless rate rises to its highest since 2021 — Dow Jones",
    "Nearly a quarter of the world's children live in conflict zones — Save the Children",
    "US sanctions Comancheros bikers and 'Ndrangheta mafia — Wire reports",
    "FIFA presidency: France's Diallo and Japan's Tashima confirmed as challengers — Le Monde",
    "Fed's Goolsbee won't rule out larger rate increases — Dow Jones",
]


# ------------------------------------------------------------- artwork
def art_scales(d, x, y, w, h):
    """A simple balance scale for the World Court lead story."""
    cx = x + w // 2
    top = y + 4
    d.line([cx, top, cx, y + h - 12], fill=INK, width=4)
    d.line([x + 10, top + 7, x + w - 10, top + 7], fill=INK, width=4)
    d.ellipse([cx - 5, top - 3, cx + 5, top + 7], outline=INK, width=3)
    for px in (x + 26, x + w - 26):
        d.line([px - 14, top + 7, px, top + 28], fill=INK, width=2)
        d.line([px + 14, top + 7, px, top + 28], fill=INK, width=2)
        d.arc([px - 21, top + 17, px + 21, top + 39], 0, 180, fill=INK, width=3)
        d.line([px - 21, top + 28, px + 21, top + 28], fill=INK, width=2)
    d.rectangle([cx - 24, y + h - 12, cx + 24, y + h - 7], fill=INK)
    d.rectangle([cx - 33, y + h - 7, cx + 33, y + h - 2], fill=INK)


def art_flags(d, x, y, w, h):
    """Three flags on poles for the Shenzhen trilateral summit."""
    base = y + h - 4
    d.line([x + 4, base, x + w - 4, base], fill=INK, width=3)
    cols = [(196, 30, 42), (24, 44, 110), (200, 40, 40)]
    for i, col in enumerate(cols):
        px = x + 24 + i * (w // 3)
        d.line([px, y + 3, px, base], fill=INK, width=3)
        fw, fh = w // 3 - 18, 30
        d.rectangle([px, y + 3, px + fw, y + 3 + fh], fill=col, outline=INK, width=2)
        if i == 0:  # China: one yellow star
            d.polygon([(px + 11, y + 8), (px + 14, y + 15), (px + 21, y + 15),
                       (px + 15, y + 20), (px + 17, y + 27), (px + 11, y + 22),
                       (px + 5, y + 27), (px + 7, y + 20), (px + 1, y + 15),
                       (px + 8, y + 15)], fill=(250, 210, 60))
        elif i == 1:  # United States: canton + stripes
            for s in range(4):
                d.line([px, y + 10 + s * 6, px + fw, y + 10 + s * 6], fill=(240, 240, 240), width=2)
            d.rectangle([px, y + 3, px + fw // 2, y + 19], fill=(30, 40, 120))
        else:  # Russia: white / blue / red bands
            d.rectangle([px, y + 3, px + fw, y + 13], fill=(240, 240, 240))
            d.rectangle([px, y + 13, px + fw, y + 23], fill=(40, 70, 170))
            d.rectangle([px, y + 23, px + fw, y + 3 + fh], fill=(200, 40, 40))


def art_chart(d, x, y, w, h):
    """A rising debut-day chart for the Anthropic IPO lead story."""
    base = y + h - 8
    d.line([x + 8, y + 4, x + 8, base], fill=INK, width=3)
    d.line([x + 8, base, x + w - 4, base], fill=INK, width=3)
    for i, bh in enumerate((13, 21, 18, 31, 45)):
        bx = x + 22 + i * 34
        d.rectangle([bx, base - bh, bx + 20, base], fill=(120, 130, 145) if i < 4 else ACCENT)
    pts = [(x + 26, base - 16), (x + 62, base - 27), (x + 98, base - 24),
           (x + 134, base - 42), (x + 172, base - 60)]
    d.line(pts, fill=ACCENT, width=4)
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 13, ay + 2), (ax - 4, ay + 11)], fill=ACCENT)
    d.text((x + w - 58, y + 0), "+34%", font=font(SANS_B, 19), fill=ACCENT)


ART = {"scales": art_scales, "flags": art_flags, "chart": art_chart}


# ------------------------------------------------------------- layout
def draw_masthead(d):
    d.rectangle([0, 0, W, H], fill=PAPER)
    margin = 28
    d.line([margin, 18, W - margin, 18], fill=RULE, width=2)
    tag = "THE ONE-PAGE WORLD BRIEFING · EVERY STORY SOURCED"
    f_tag = font(SANS_B, 13)
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 24), tag, font=f_tag, fill=GRAY)
    title = "THE WORLD IN ONE DAY"
    f_title = font(SERIF_B, 60)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 42), title, font=f_title, fill=INK)
    d.rectangle([margin, 114, W - margin, 119], fill=RULE)
    d.line([margin, 123, W - margin, 123], fill=RULE, width=1)
    d.text((margin, 131), "Thursday 19 November 2026", font=font(SERIF_B, 23), fill=ACCENT)
    right = "46 stories · 6 continents · one day"
    f_r = font(SANS_I, 15)
    tw = d.textlength(right, font=f_r)
    d.text((W - margin - tw, 137), right, font=f_r, fill=GRAY)
    d.line([margin, 159, W - margin, 159], fill=RULE, width=2)
    return 168


def draw_lead(d, lead, x, y, w):
    d.text((x, y), lead["kicker"], font=font(SANS_B, 12), fill=ACCENT)
    y += 17
    ART[lead["art"]](d, x, y, w, 60)
    y += 64
    y = text_block(d, x, y, lead["headline"], font(SERIF_B, 19), w, 23)
    y += 3
    y = text_block(d, x, y, lead["summary"], font(SANS, 11.5), w, 14.5)
    y += 3
    d.text((x, y), "— " + lead["source"], font=font(SANS_I, 10.5), fill=GRAY)
    return y + 11


def draw_section(d, title, stories, x, y, w):
    d.rectangle([x, y, x + w, y + 18], fill=INK)
    d.text((x + 7, y + 3), title, font=font(SANS_B, 12), fill=PAPER)
    y += 23
    for head, summ, src in stories:
        y = text_block(d, x, y, head, font(SANS_B, 11.5), w, 13.5)
        y = text_block(d, x, y, summ + " — " + src, font(SANS, 9.5), w, 12)
        y += 4
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d)

    margin, gap = 28, 18
    col_w = (W - 2 * margin - 2 * gap) // 3
    xs = [margin, margin + col_w + gap, margin + 2 * (col_w + gap)]

    lead_bottom = y
    for i, lead in enumerate(LEADS):
        b = draw_lead(d, lead, xs[i], y, col_w)
        lead_bottom = max(lead_bottom, b)
    for i in range(2):
        vx = xs[i] + col_w + gap // 2
        d.line([vx, y, vx, lead_bottom], fill=(200, 195, 180), width=1)
    y = lead_bottom + 3
    d.line([margin, y, W - margin, y], fill=RULE, width=2)
    y += 9

    columns = [[SECTIONS[0], SECTIONS[1]],
               [SECTIONS[2], SECTIONS[3]],
               [SECTIONS[4], SECTIONS[5], SECTIONS[6]]]
    grid_bottom = y
    for ci, secs in enumerate(columns):
        cy = y
        for title, stories in secs:
            cy = draw_section(d, title, stories, xs[ci], cy, col_w)
            cy += 3
        print(f"column {ci} ends at {cy}")
        grid_bottom = max(grid_bottom, cy)
    for ci in range(2):
        vx = xs[ci] + col_w + gap // 2
        d.line([vx, y, vx, grid_bottom], fill=(200, 195, 180), width=1)

    y = grid_bottom + 1
    d.line([margin, y, W - margin, y], fill=RULE, width=2)
    y += 7
    d.text((margin, y), "IN BRIEF", font=font(SANS_B, 13), fill=ACCENT)
    y += 16
    brief_text = "  ·  ".join(BRIEFS)
    y = text_block(d, margin, y, brief_text, font(SANS, 10), W - 2 * margin, 13)
    print("briefs end at", y)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
