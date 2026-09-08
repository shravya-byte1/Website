#!/usr/bin/env python3
"""
Static site generator for Pranic Healing with Shravya.
Produces plain HTML/CSS/JS — no build step needed to view or host.
Run: python3 generate.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Small reusable SVG motifs (concentric "aura" rings — grounded in the
# subject matter instead of a generic gradient blob or stock icon)
# ---------------------------------------------------------------------------

def hero_rings_svg():
    return """<svg viewBox="0 0 460 460" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Concentric energy rings">
      <circle cx="230" cy="230" r="210" stroke="#E7A23A" stroke-opacity="0.28" stroke-width="1.5"/>
      <circle cx="230" cy="230" r="168" stroke="#1C5C54" stroke-opacity="0.35" stroke-width="1.5"/>
      <circle cx="230" cy="230" r="126" stroke="#E0577C" stroke-opacity="0.4" stroke-width="1.5"/>
      <circle cx="230" cy="230" r="84" fill="#0F3D39" fill-opacity="0.06"/>
      <circle cx="230" cy="230" r="84" stroke="#0F3D39" stroke-opacity="0.5" stroke-width="1.5"/>
      <circle cx="230" cy="230" r="44" fill="#E7A23A"/>
      <circle cx="230" cy="230" r="44" fill="url(#g1)" fill-opacity="0.5"/>
      <defs>
        <radialGradient id="g1" cx="0.35" cy="0.3" r="0.9">
          <stop offset="0" stop-color="#FFF9EE"/>
          <stop offset="1" stop-color="#E7A23A" stop-opacity="0"/>
        </radialGradient>
      </defs>
    </svg>"""

def corner_rings_svg():
    return """<svg width="360" height="360" viewBox="0 0 360 360" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="180" cy="180" r="178" stroke="#FFF9EE" stroke-opacity="0.14" stroke-width="1"/>
      <circle cx="180" cy="180" r="132" stroke="#E7A23A" stroke-opacity="0.3" stroke-width="1"/>
      <circle cx="180" cy="180" r="88" stroke="#FFF9EE" stroke-opacity="0.18" stroke-width="1"/>
      <circle cx="180" cy="180" r="46" stroke="#E0577C" stroke-opacity="0.35" stroke-width="1"/>
    </svg>"""

def logo_mark_svg():
    return """<svg class="mark" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="20" cy="20" r="19" stroke="#0F3D39" stroke-width="1.3" opacity="0.5"/>
      <circle cx="20" cy="20" r="13" stroke="#E0577C" stroke-width="1.3" opacity="0.7"/>
      <circle cx="20" cy="20" r="7" fill="#E7A23A"/>
    </svg>"""

# ---------------------------------------------------------------------------
# Navigation / footer
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("events.html", "Community &amp; Calendar"),
    ("blog.html", "Resources"),
    
]

def nav_html(active, depth=""):
    items = []
    for href, label in NAV_ITEMS:
        cls = " active" if href == active else ""
        items.append(f'<li><a class="{cls.strip()}" href="{depth}{href}">{label}</a></li>')
    return "\n        ".join(items)

def header_html(active, depth=""):
    return f"""  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="{depth}index.html">
        {logo_mark_svg()}
        <span>Pranic Healing <span class="italic">with Shravya</span><span class="brand-sub">ONLINE &amp; IN-PERSON</span></span>
      </a>
      <ul class="nav-links" id="nav-links">
        {nav_html(active, depth)}
      </ul>
      <div class="nav-cta">
        <a class="btn btn-primary" href="{depth}contact.html">Get in Touch</a>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
          <span></span>
        </button>
      </div>
    </div>
  </header>"""

def footer_html(depth=""):
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">Pranic Healing <span class="italic">with Shravya</span></div>
          <p style="max-width:34ch;">A space for healing, learning and inner growth — rooted in the modern Pranic Healing system, offered online and in Bengaluru.</p>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><a href="{depth}about.html">About Shravya</a></li>
            <li><a href="{depth}services.html">Services</a></li>
            <li><a href="{depth}events.html">Community &amp; calendar</a></li>
            <li><a href="{depth}blog.html">Resources</a></li>
          </ul>
        </div>
        <div>
          <h4>Get in touch</h4>
          <ul>
            <li><a href="mailto:gm.sushravya@gmail.com">gm.sushravya@gmail.com</a></li>
            <li><a href="tel:+918861318805">+91 88613-18805</a></li>
            <li>Bengaluru, India</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 Pranic Healing with Shravya. All rights reserved.</span>
        <span>Pranic Healing is a complementary practice and is not a substitute for professional medical or financial advice.</span>
      </div>
    </div>
  </footer>
  <script src="{depth}js/main.js"></script>"""

def page_shell(title, description, active, body, depth="", extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0F3D39">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{depth}css/style.css">
{extra_head}</head>
<body>
{header_html(active, depth)}
<main id="main">
{body}
</main>
{footer_html(depth)}
</body>
</html>"""

# ---------------------------------------------------------------------------
# Event data — one entry per event type, each becomes /events/<slug>.html
# ---------------------------------------------------------------------------

EVENTS = [
    {
        "slug": "mass-pranic-healing",
        "name": "Mass Pranic Healing",
        "mode": "Online", "cadence": "Weekly", "day": "Every Tuesday",
        "duration": "Roughly 45–60 minutes",
        "audience": "Open to everyone, no experience needed",
        "intro": "Mass Pranic Healing brings a small group together online to receive healing at the same time. One or more practitioners scan, cleanse and re-energise each person's energy field in turn, while the whole group holds a calm, supportive space. Because the healing is done without physical touch, you take part from wherever you are — you simply get comfortable, relax, and receive.",
        "benefits": [
            ("Support for the body's own repair process", "Clearing blocked energy and channeling fresh prana is used to support the body's natural healing and recovery processes."),
            ("Steadier stress and emotions", "Group energy work is commonly used to help release built-up tension, easing stress, anxiety and low mood."),
            ("A gentle, no-touch format", "Nothing is physically done to you — you stay seated, relaxed, and simply notice how you feel before and after."),
            ("Works alongside your regular care", "Pranic Healing is offered as a complement to medical treatment, not a replacement for it — keep seeing your doctor for any ongoing condition."),
        ],
        "steps": [
            ("Settle in", "Join the video call a few minutes early, find a quiet spot, and simply get comfortable in a chair — no equipment needed."),
            ("A short centering", "We open with a few slow breaths together to help everyone arrive and settle."),
            ("Group healing", "The practitioner works through the group, scanning and energising each person's field while you rest and receive."),
            ("Closing & questions", "We close gently and leave a little time for anyone who'd like to share how the session felt or ask a question."),
        ],
        "faqs": [
            ("Do I need to do anything during the session?", "No. You simply relax in a comfortable seated position with your eyes closed. The practitioner does the active work — your job is just to receive."),
            ("Is this a substitute for medical treatment?", "No. Pranic Healing is a complementary practice. Please continue any prescribed treatment and speak with your doctor about ongoing or serious health concerns."),
            ("Can children or older adults join?", "Yes, Mass Pranic Healing is gentle and suitable for most ages. If you have a specific medical condition, mention it beforehand so the session can be adapted sensibly."),
            ("Is it normal to feel emotional afterward?", "Occasionally, yes. Releasing stored tension can bring feelings to the surface for a short while. This usually settles within a day or two and is considered a normal part of the process."),
        ],
        "who": None,
        "links": [
            ("World Pranic Healing", "https://www.worldpranichealing.com/"),
            ("Pranic Healing USA", "https://pranichealingusa.com/"),
            ("Institute for Inner Studies", "https://pranichealing.com/"),
        ],
    },
    {
        "slug": "introduction-to-pranic-healing",
        "name": "Introduction to Pranic Healing & Its Applications",
        "mode": "Online", "cadence": "Weekly", "day": "Every Wednesday",
        "duration": "About 60 minutes, talk + live Q&A",
        "audience": "Best for first-timers and the curious — no background needed",
        "intro": "A beginner-friendly walkthrough of what Pranic Healing actually is: the aura (your energy field), the chakras (energy centres) and prana (life force), and how a no-touch session of scanning, cleansing and energising works. Each week's session leans into a different area of life — physical health, mental health, relationships, financial abundance, or spiritual growth — so the ideas always land somewhere practical.",
        "benefits": [
            ("A clear starting point", "Leave with a plain-language understanding of prana, the aura and the chakras, without needing any prior reading."),
            ("A holistic lens on wellbeing", "Pranic Healing is presented as a holistic approach spanning the physical, emotional, mental and spiritual, so you see how the pieces connect."),
            ("Ideas you can use immediately", "Each themed week ties the fundamentals to a real area of life, so you leave with something practical to try, not just theory."),
            ("A path to what's next", "It's the natural first step before joining a Mass Healing, Twin Hearts session, or a full workshop."),
        ],
        "steps": [
            ("A short talk", "We introduce prana, the aura and the chakras in everyday language, with simple analogies."),
            ("This week's theme", "We connect the fundamentals to that week's focus area — physical health, mind, relationships, money, or spiritual growth."),
            ("Live Q&A", "Bring your questions — skepticism is welcome, and nothing is assumed."),
            ("Where to go next", "We point you toward the right next session or workshop based on what you're curious about."),
        ],
        "faqs": [
            ("Who developed Pranic Healing?", "The modern system was developed by Grand Master Choa Kok Sui, a Philippines-based researcher and teacher, who codified it into a structured, teachable method in the late 20th century."),
            ("Is Pranic Healing tied to a religion?", "No. It doesn't follow any particular religious belief, and people of any faith — or none — take part."),
            ("Do I need any prior experience?", "None at all. This session is designed as the entry point, with no assumed background."),
            ("Is there scientific evidence for it?", "Pranic Healing has a growing body of small studies and practitioner-reported outcomes, alongside a much larger base of anecdotal experience. It isn't yet part of mainstream medical consensus, so it's best approached as a complementary practice rather than a proven medical treatment."),
        ],
        "who": None,
        "links": [
            ("World Pranic Healing — Get started", "https://www.worldpranichealing.com/getstarted"),
            ("Institute for Inner Studies", "https://pranichealing.com/"),
        ],
    },
    {
        "slug": "twin-hearts-meditation",
        "name": "Meditation on the Twin Hearts",
        "mode": "Online", "cadence": "Weekly", "day": "Every Thursday",
        "duration": "About 20–25 minutes of guided meditation",
        "audience": "Generally suitable from age 16+ — see the note below",
        "intro": "One of the best-known techniques in the Pranic Healing system, the Meditation on the Twin Hearts is a short guided practice that opens the heart and crown energy centres, inviting a flow of calming, uplifting energy. Part of the practice includes a simple blessing of loving-kindness sent out to the earth, which many practitioners describe as deeply peaceful and quietly joyful.",
        "benefits": [
            ("Noticeably calmer, clearer", "Regular practitioners commonly report reduced stress and anxiety, more peace, and greater everyday happiness."),
            ("A sharper, steadier mind", "Greater mental clarity and a calmer response to daily pressure are among the most frequently reported effects."),
            ("A simple structure, big depth", "The full guided practice takes about 20–25 minutes, making it realistic to build into a weekly rhythm."),
            ("A practice of service", "Because part of the meditation involves blessing the wider world with goodwill, many people find it shifts their mood from self-focus to genuine care for others."),
        ],
        "steps": [
            ("A brief warm-up", "A few simple stretches and breathing cues to settle the body before we begin."),
            ("Opening the heart & crown", "Guided visualisation gently invites the heart and crown energy centres to open."),
            ("Blessing the earth", "A short, simple blessing of loving-kindness is offered outward — this is the heart of the practice."),
            ("Stillness & closing", "A few minutes of quiet stillness, then a gentle, grounded return to the room."),
        ],
        "faqs": [
            ("Is this meditation religious?", "No — it doesn't follow any specific religion or guru, and is practised by people from many faith backgrounds and none."),
            ("How long does it take to learn?", "The technique itself is simple to follow from the first session, though the full teaching (including the reasoning behind each step) takes about an hour to properly absorb."),
            ("Is there research behind it?", "Small pilot studies have looked at physiological markers such as melatonin and serotonin levels after the practice, alongside a large volume of practitioner-reported experience. As with most meditation research, larger studies are still needed."),
            ("Can I do this if I'm pregnant?", "Pregnant women are generally advised to practise gently — once or twice a week rather than daily — since a strong energy flow is best kept moderate at this time. Always check with your doctor first."),
        ],
        "who": "This meditation is generally recommended from around age 16, with children 10–15 able to join around once a week. If you have a heart condition, unregulated high blood pressure, glaucoma, or a serious kidney or liver condition, please speak with a practitioner before joining, as the practice may need to be adapted for you.",
        "links": [
            ("World Pranic Healing — Twin Hearts", "https://www.worldpranichealing.com/en/twin-hearts-meditation-benefits"),
            ("Institute for Inner Studies", "https://pranichealing.com/content/meditation-twin-hearts"),
        ],
    },
    {
        "slug": "community-catchup",
        "name": "Community Catchup",
        "mode": "Online", "cadence": "Weekly", "day": "Every Friday",
        "duration": "About 45 minutes, informal",
        "audience": "Open to anyone in the community — regulars and newcomers alike",
        "intro": "A relaxed, informal close to the week where the community gathers to share experiences, ask questions, and simply stay connected. There's no set curriculum here — it's a space to talk about what's come up during the week's practices, celebrate small wins, and get to know fellow practitioners.",
        "benefits": [
            ("A sense of belonging", "Regular, low-pressure contact with others on a similar path helps practice feel less solitary."),
            ("Space to ask anything", "Questions that come up mid-week — about a technique, an experience, or just curiosity — get an easy home here."),
            ("Gentle accountability", "Sharing your week with others tends to make it easier to keep a regular practice going."),
            ("A softer entry point", "If workshops feel like a big first step, this is a low-key way to meet the community first."),
        ],
        "steps": [
            ("Open check-in", "Everyone is welcome to share (or just listen) — how the week's practices went, or how things are generally."),
            ("Open floor", "Questions, reflections and requests for the coming week's sessions are all welcome."),
            ("Community notices", "Any updates on upcoming events or workshops are shared."),
            ("Wind down together", "A relaxed close to the online week."),
        ],
        "faqs": [
            ("Do I have to speak?", "Not at all — plenty of people join just to listen, and that's completely fine."),
            ("Is this a healing session?", "No, it's purely a community and conversation space. For an actual healing session, join Mass Pranic Healing or Group Meditation & Free Healing."),
            ("Can I join if I'm brand new?", "Yes — it's often a lovely, low-pressure way to meet the community for the first time."),
        ],
        "who": None,
        "links": [
            ("World Pranic Healing", "https://www.worldpranichealing.com/"),
        ],
    },
    {
        "slug": "group-meditation-free-healing",
        "name": "Group Meditation & Free Healing",
        "mode": "In-person · Bengaluru", "cadence": "Weekly", "day": "Most Saturdays",
        "duration": "About 90 minutes, in person",
        "audience": "Ideal first in-person experience — no experience needed",
        "intro": "An in-person introduction to Pranic Healing, held in Bengaluru. This session pairs a short, practical teaching with a complimentary group healing demonstration, so newcomers can actually feel the practice rather than just hear about it, alongside a supportive group of fellow participants.",
        "benefits": [
            ("Experience it firsthand", "There's a real difference between reading about energy healing and sitting in a room where it's happening — this session is built around that first felt experience."),
            ("No cost to try it", "The healing portion of this session is offered free, removing the barrier to a first experience."),
            ("Community, in person", "Meeting fellow practitioners face to face tends to deepen commitment and connection in a way online sessions can't fully replicate."),
            ("A gentle group meditation", "Sessions typically include a short guided group meditation alongside the healing demonstration."),
        ],
        "steps": [
            ("Welcome & short talk", "A brief, practical introduction to what you'll experience and why."),
            ("Guided group meditation", "A short seated meditation to settle the room together."),
            ("Free healing demonstration", "A complimentary group healing is offered so you can feel the practice directly."),
            ("Questions & connect", "Time afterward to ask questions and meet other participants."),
        ],
        "faqs": [
            ("Is it really free?", "Yes — the healing portion of this session is offered at no cost as an introduction to the practice."),
            ("Do I need to book in advance?", "It's best to confirm your spot beforehand through the contact page, as group size is kept manageable."),
            ("What should I wear or bring?", "Comfortable clothing you can sit in for an hour or so. It also helps to avoid a heavy meal right before the session."),
            ("Where exactly in Bengaluru is it held?", "The venue is shared directly with confirmed participants — reach out via the contact page for the current location."),
        ],
        "who": None,
        "links": [
            ("Institute for Inner Studies", "https://pranichealing.com/"),
        ],
    },
    {
        "slug": "pranic-self-care-practices",
        "name": "Pranic Self-Care Practices",
        "mode": "Online", "cadence": "Weekly", "day": "Every Monday",
        "duration": "About 45–60 minutes",
        "audience": "Great for regular practitioners building a home routine",
        "intro": "This weekly session is about building your own toolkit — simple self-scanning, self-cleansing and self-energising techniques you can use between sessions, plus practical guidance on breathing, light movement and diet that support the effects of energy work day to day.", 
        "benefits": [
            ("A personal daily toolkit", "You leave each session with a small, practical technique you can practise on your own, without needing a practitioner present."),
            ("Better integration between sessions", "Gentle daily habits — breathing, light movement, mindful eating — are commonly recommended to help stabilise and extend the benefits of healing work."),
            ("More consistency over time", "A regular self-care rhythm tends to compound, much like any wellness habit."),
            ("Practical, not theoretical", "Sessions favour hands-on practice over lecture, so you actually try each technique in real time."),
        ],
        "steps": [
            ("This week's technique", "A short teaching on one self-care technique — a breathing pattern, a self-cleansing method, or a grounding practice."),
            ("Guided practice", "We do it together live, so you leave having actually tried it, not just heard about it."),
            ("Everyday integration tips", "Simple notes on diet and rest that are commonly recommended to support energy work — for instance, favouring lighter meals and avoiding heavy or processed food right after a session."),
            ("Take it home", "A short recap so you can repeat the technique on your own during the week."),
        ],
        "faqs": [
            ("How often should I self-practice?", "Little and often works best — even five to ten minutes a day builds more consistency than one long session a week."),
            ("Do I need any equipment?", "No — just a quiet seated spot. Some weeks include an optional simple prop, always mentioned in advance."),
            ("Is this suitable for total beginners?", "It's most useful once you've joined at least one Introduction session, so the basic vocabulary of prana, aura and chakras already feels familiar."),
        ],
        "who": None,
        "links": [
            ("Pranic Healing USA — self-care resources", "https://pranichealingusa.com/"),
        ],
    },
    {
        "slug": "financial-abundance-intro",
        "name": "Introduction Session — Pranic Healing for Financial Abundance",
        "mode": "In-person · Bengaluru", "cadence": "Monthly", "day": "Once a month",
        "duration": "About 90 minutes, in person",
        "audience": "Entrepreneurs, professionals, and anyone wanting more clarity around money",
        "intro": "A monthly in-person introduction to how the Pranic Healing system approaches prosperity — not as a promise of instant wealth, but as a way of clearing self-limiting energy patterns, building a steadier money mindset, and practising simple techniques like blessing and gratitude that many practitioners use alongside sound financial planning.",
        "benefits": [
            ("A clearer, calmer relationship with money", "The session focuses on removing self-doubt and limiting beliefs, so financial decisions can be made from a clearer, less anxious place."),
            ("Practical grounding techniques", "You're introduced to simple practices — gratitude, blessing your income and workspace, and basic visualisation — that are easy to keep using at home."),
            ("An introduction to Kriyashakti", "You'll hear about Kriyashakti, the Pranic Healing system's approach to consciously shaping intentions into action, as a taster for the full workshop."),
            ("A path forward", "This session is designed as a starting point, pointing toward deeper workshops for those who want to go further."),
        ],
        "steps": [
            ("Talk: energy & prosperity", "An accessible introduction to how the system connects our energetic state to our habits around money and opportunity."),
            ("A simple prosperity meditation", "A short guided practice focused on clearing blocks and building a positive, grounded mindset around abundance."),
            ("Gratitude & blessing practice", "A simple technique for blessing your income, work and environment, which you can continue using at home."),
            ("Next steps", "Guidance on the fuller Kriyashakti workshop path for anyone who wants to continue."),
        ],
        "faqs": [
            ("Will this guarantee financial success?", "No. This is a complementary, mindset-and-energy-based practice, not financial advice and not a guarantee of any outcome. It works best alongside — never instead of — sound financial planning and professional advice."),
            ("Who is this session for?", "Anyone curious about the connection between energy, mindset and money — entrepreneurs, employees, freelancers, and students alike."),
            ("Do I need the Introduction to Pranic Healing session first?", "It helps, but isn't required — the session opens with enough grounding for newcomers to follow along."),
        ],
        "who": None,
        "links": [
            ("Global Pranic Healing — Prosperity & Abundance", "https://www.globalpranichealing.com/prosperity-abundance/"),
            ("World Pranic Healing — Prosperity", "https://www.worldpranichealing.com/getstarted/prosperity"),
        ],
    },
    {
        "slug": "full-moon-meditation",
        "name": "Guided Full Moon Group Meditation Circle",
        "mode": "In-person · Bengaluru", "cadence": "Monthly", "day": "On the full moon",
        "duration": "About 90 minutes, in person",
        "audience": "Open to all, meditation experience welcomed but not required",
        "intro": "Once a month, on the full moon, the community gathers in person for an extended group meditation. In the Pranic Healing tradition, the full moon is considered a time of naturally heightened collective energy, and group practice — especially the Meditation on the Twin Hearts — is used to deepen stillness, set clear intentions, and mark the month's close together.",
        "benefits": [
            ("A deeper group experience", "Meditating together is described as amplifying the effect for each individual well beyond meditating alone — the Pranic Healing tradition holds that even a handful of people meditating together can have an outsized collective effect."),
            ("Space for intention-setting", "The full moon is used as a natural checkpoint to reflect on the month and set clear, positive intentions going forward."),
            ("Renewed calm and clarity", "Extended group meditation is commonly reported to leave people feeling lighter, calmer and more emotionally settled."),
            ("A monthly community rhythm", "It's a lovely way to mark time together and stay connected with the wider practice community."),
        ],
        "steps": [
            ("Opening circle", "A short welcome and grounding to bring everyone into a shared, calm space."),
            ("Guided Meditation on the Twin Hearts", "The core group meditation, extended slightly for the full moon setting."),
            ("Collective intention & blessing", "Space to quietly set an intention for the month ahead, often shared as a group blessing."),
            ("Closing & sharing", "A gentle close, with time for anyone who'd like to share their experience."),
        ],
        "faqs": [
            ("Do I need meditation experience?", "No — the session is guided throughout, so first-timers are very welcome."),
            ("Is this tied to a particular religion?", "The practice draws on a long meditation and service tradition within Pranic Healing, but isn't tied to any single religion — people from many backgrounds take part."),
            ("Why the full moon specifically?", "In this tradition, the full moon is considered a period of stronger, more available collective energy, making group meditation especially effective at this time — though the underlying practice is the same one used year-round."),
        ],
        "who": None,
        "links": [
            ("World Pranic Healing — Full Moon Meditations", "https://www.worldpranichealing.com/events/full-moon-meditations"),
        ],
    },
]

EVENT_BY_SLUG = {e["slug"]: e for e in EVENTS}

# ---------------------------------------------------------------------------
# Event detail page template
# ---------------------------------------------------------------------------

def render_event_page(e):
    chip_mode_class = "chip-offline" if "person" in e["mode"].lower() else "chip-online"
    cadence_class = "chip-monthly" if e["cadence"] == "Monthly" else "chip-online"

    benefits_html = "\n".join(
        f'''        <li><span class="dot"></span><p><strong>{title}</strong>{body}</p></li>'''
        for title, body in e["benefits"]
    )
    steps_html = "\n".join(
        f'''        <div class="step"><div class="num"></div><div><h3>{title}</h3><p>{body}</p></div></div>'''
        for title, body in e["steps"]
    )
    faqs_html = "\n".join(
        f'''        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>{q}</span><span class="plus"></span></button>
          <div class="faq-a"><p>{a}</p></div>
        </div>'''
        for q, a in e["faqs"]
    )
    links_html = "\n".join(
        f'<li><a href="{url}" target="_blank" rel="noopener">{label} ↗</a></li>'
        for label, url in e["links"]
    )

    who_html = ""
    if e["who"]:
        who_html = f'''
      <div class="callout">
        <p><strong>Good to know —</strong> {e["who"]}</p>
      </div>'''

    other_events = [ev for ev in EVENTS if ev["slug"] != e["slug"]][:3]
    other_html = "\n".join(
        f'<li><a href="{ev["slug"]}.html">{ev["name"]} <span class="small" style="color:var(--ink-soft);">— {ev["day"]}</span></a></li>'
        for ev in other_events
    )

    body = f"""
  <section class="event-hero">
    <div class="corner-deco" style="position:absolute;right:-60px;top:-60px;">{corner_rings_svg()}</div>
    <div class="container">
      <a class="back-link" href="../events.html">&larr; Back to community &amp; events</a>
      <div class="chips">
        <span class="chip {chip_mode_class}">{e["mode"]}</span>
        <span class="chip {cadence_class}">{e["cadence"]} · {e["day"]}</span>
      </div>
      <h1>{e["name"]}</h1>
      <p class="lede">{e["intro"]}</p>
      <div class="event-facts">
        <div><div class="label">When</div><div class="value">{e["day"]}</div></div>
        <div><div class="label">Format</div><div class="value">{e["mode"]}</div></div>
        <div><div class="label">Duration</div><div class="value">{e["duration"]}</div></div>
        <div><div class="label">Best for</div><div class="value" style="font-size:1rem;">{e["audience"]}</div></div>
      </div>
      <div class="hero-actions">
        <a class="btn btn-marigold" href="../contact.html">Reserve your spot</a>
        <a class="btn btn-ghost-light" href="../events.html">See full schedule</a>
      </div>
    </div>
  </section>

  <section>
    <div class="container detail-grid">
      <div>
        <div class="section-head">
          <div class="eyebrow"><span class="ring"></span>Benefits</div>
          <h2>What this practice offers</h2>
        </div>
        <ul class="benefit-list">
{benefits_html}
        </ul>
        {who_html}

        <div class="section-head" style="margin-top:64px;">
          <div class="eyebrow"><span class="ring"></span>What to expect</div>
          <h2>How the session flows</h2>
        </div>
        <div class="steps">
{steps_html}
        </div>

        <div class="section-head" style="margin-top:64px;">
          <div class="eyebrow"><span class="ring"></span>FAQ</div>
          <h2>Common questions</h2>
        </div>
        <div class="faq">
{faqs_html}
        </div>
      </div>

      <aside class="sticky-side">
        <div class="side-card">
          <h4>Join this session</h4>
          <p class="small" style="margin-bottom:16px;">Get in touch to confirm your spot and receive the joining link or venue details.</p>
          <a class="btn btn-primary" style="width:100%; justify-content:center;" href="../contact.html">Book your place</a>
        </div>
        <div class="side-card">
          <h4>Useful links</h4>
          <ul class="links">
{links_html}
          </ul>
        </div>
        <div class="side-card">
          <h4>Other sessions you might like</h4>
          <ul>
{other_html}
          </ul>
        </div>
      </aside>
    </div>
  </section>

  <section class="bg-teal section-tight">
    <div class="container" style="text-align:center;">
      <h2 style="max-width:26ch; margin:0 auto 18px;">Ready to experience it for yourself?</h2>
      <p style="max-width:50ch; margin:0 auto 28px; color:rgba(255,249,238,0.8);">Reach out and we'll help you find the right first session, whether that's this one or another on the calendar.</p>
      <a class="btn btn-marigold" href="../contact.html">Get in touch</a>
    </div>
  </section>
"""
    html = page_shell(
        title=f'{e["name"]} — Pranic Healing with Shravya',
        description=e["intro"][:155],
        active="events.html",
        body=body,
        depth="../",
    )
    return html

# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

def render_home():
    weekly = [
        ("Mon", "Pranic Self-Care Practices", "pranic-self-care-practices"),
        ("Tue", "Mass Pranic Healing", "mass-pranic-healing"),
        ("Wed", "Introduction to Pranic Healing", "introduction-to-pranic-healing"),
        ("Thu", "Meditation on the Twin Hearts", "twin-hearts-meditation"),
        ("Fri", "Community Catchup", "community-catchup"),
    ]
    rhythm_html = "\n".join(
        f'''      <div class="rhythm-cell"><span class="day">{d}</span><h4>{name}</h4><p>Online, weekly</p><a class="arrow" style="display:inline-flex;gap:6px;margin-top:10px;font-size:0.88rem;font-weight:600;color:var(--teal-900);" href="events/{slug}.html">Details &rarr;</a></div>'''
        for d, name, slug in weekly
    )

    featured = [e for e in EVENTS if e["slug"] in ("group-meditation-free-healing", "financial-abundance-intro", "full-moon-meditation")]
    featured_html = "\n".join(
        f'''      <div class="card">
        <div class="chips" style="margin-bottom:14px;"><span class="chip chip-offline">{e["mode"]}</span><span class="chip chip-monthly">{e["cadence"]}</span></div>
        <h3>{e["name"]}</h3>
        <p>{e["intro"][:120]}&hellip;</p>
        <a class="btn btn-outline" style="margin-top:6px;" href="events/{e["slug"]}.html">Learn more</a>
      </div>'''
        for e in featured
    )

    body = f"""
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <div class="eyebrow"><span class="ring"></span>Welcome to Pranic Healing with Shravya</div>
        <h1>Cleanse. Revitalise. <span class="italic">Balance.</span></h1>
        <p class="lede">Pranic Healing is a no-touch, energy-based complementary practice that works with prana — the life force — to support a calmer mind, a healthier body and a more grounded, abundant life. Explore weekly sessions and community events in Bengaluru and online.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="events.html">Explore events</a>
          <a class="btn btn-outline" href="services.html">See services</a>
        </div>
      </div>
      <div class="hero-rings">{hero_rings_svg()}</div>
    </div>
  </section>

  <section class="pathways">
    <div class="container">
      <div class="section-head">
        <div class="eyebrow"><span class="ring"></span>Where to begin</div>
        <h2>Three ways people arrive here</h2>
      </div>
      <div class="pathway-row">
        <div class="pathway-cell">
          <span class="idx">01</span>
          <h3>Mental &amp; emotional balance</h3>
          <p>Sessions and practices aimed at easing stress, anxiety and mental fatigue by clearing and stabilising the energy body.</p>
          <a class="arrow" href="services.html#mental-health">Explore &rarr;</a>
        </div>
        <div class="pathway-cell">
          <span class="idx">02</span>
          <h3>Financial abundance</h3>
          <p>A complementary approach to money and opportunity — clearing self-limiting patterns and building a steadier, more grounded mindset.</p>
          <a class="arrow" href="services.html#financial-abundance">Explore &rarr;</a>
        </div>
        <div class="pathway-cell">
          <span class="idx">03</span>
          <h3>Physical well-being</h3>
          <p>Energy work used alongside your regular care to support the body's own recovery and day-to-day vitality.</p>
          <a class="arrow" href="services.html#physical-wellbeing">Explore &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-ivory-deep section-tight">
    <div class="container about-grid">
      <div class="portrait-ring">
        <div class="inner">Shravya's<br>portrait</div>
      </div>
      <div>
        <div class="eyebrow"><span class="ring"></span>About the healer</div>
        <h2>Hi, <span class="italic">lovely to meet you.</span></h2>
        <p>I'm Shravya, and I practise and teach Pranic Healing — a modern, structured system of energy healing that works with the body's aura and chakras using prana, the universal life force. My own path into this work grew from a simple curiosity about how much of our wellbeing sits just beneath the surface, in the energy we carry every day.</p>
        <p>Today I hold weekly online sessions and in-person gatherings in Bengaluru, welcoming complete beginners and long-time practitioners alike into a steady, supportive practice.</p>
        <a class="btn btn-outline" href="about.html">More about Shravya &amp; this approach</a>
      </div>
    </div>
  </section>

  <section class="testimonial">
    <div class="container">
      <div class="eyebrow"><span class="ring"></span>From the community</div>
      <blockquote>&ldquo;Shravya is an amazing healer. I reached out to her for healing my ankle, and I was truly amazed by the results. Within just one session, the pain in my ankle completely disappeared. I am incredibly grateful for her healing and the care she provides.&rdquo;</blockquote>
      <cite>— Swarali Patil, Client</cite>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head">
        <div class="eyebrow"><span class="ring"></span>Community &amp; calendar</div>
        <h2>Come together. <span class="italic">Experience more.</span></h2>
        <p>A steady weekly rhythm online, plus in-person gatherings in Bengaluru — workshops, meditation circles and free introductory sessions.</p>
      </div>
      <div class="rhythm-strip">
{rhythm_html}
      </div>
      <div class="card-grid grid-3" style="margin-top:26px;">
{featured_html}
      </div>
      <div style="text-align:center; margin-top:40px;">
        <a class="btn btn-primary" href="events.html">View the full calendar &amp; all sessions</a>
      </div>
    </div>
  </section>

  <section class="bg-ivory-deep">
    <div class="container">
      <div class="section-head center">
        <div class="eyebrow" style="justify-content:center;"><span class="ring"></span>Blog</div>
        <h2>Ideas for your <span class="italic">inner journey.</span></h2>
        <p style="margin:0 auto;">Reflections, practical techniques and community stories — new posts arriving soon.</p>
      </div>
      <div style="text-align:center;">
        <a class="btn btn-outline" href="blog.html">Visit the blog</a>
      </div>
    </div>
  </section>

  <section class="bg-teal">
    <div class="container" style="text-align:center;">
      <div class="eyebrow" style="justify-content:center; color:var(--marigold);"><span class="ring" style="border-color:var(--marigold);"></span>Contact us</div>
      <h2 style="max-width:22ch; margin:0 auto 16px;">Begin your <span class="italic">journey.</span></h2>
      <p style="margin:0 auto 30px; max-width:52ch;">Have a question, want to book a session, or want to join an upcoming event? Get in touch — we'd love to hear from you.</p>
      <a class="btn btn-marigold" href="contact.html">Get in touch</a>
    </div>
  </section>
"""
    return page_shell(
        title="Pranic Healing with Shravya — Energy Healing, Meditation & Community in Bengaluru",
        description="Discover Pranic Healing sessions, meditation, workshops and community events with Shravya — online and in Bengaluru.",
        active="index.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------

def render_about():
    body = """
  <section class="hero" style="padding-bottom:60px;">
    <div class="container hero-grid">
      <div>
        <div class="eyebrow"><span class="ring"></span>About</div>
        <h1>Hi, <span class="italic">lovely to meet you.</span></h1>
        <p class="lede">I'm Shravya — a Pranic Healing practitioner and teacher based in Bengaluru, holding space for online and in-person sessions rooted in the modern Pranic Healing system.</p>
      </div>
      <div class="hero-rings"><div class="portrait-ring" style="max-width:340px; margin-left:auto;"><div class="inner">Shravya's<br>portrait</div></div></div>
    </div>
  </section>

  <section class="section-tight">
    <div class="container" style="max-width:760px;">
      <h2>My path to this work</h2>
      <p>[This is the space to share your personal story — what drew you to Pranic Healing, your training and certification history within the MCKS Pranic Healing lineage, the years you've been practising, and what this work means to you. Keep it warm and personal; a few paragraphs is plenty.]</p>
      <p>Pranic Healing itself was developed by Grand Master Choa Kok Sui, who researched and codified a structured, teachable system of energy healing using prana — the universal life force. It's taught today by practitioners around the world, always as a complement to, never a replacement for, conventional medical care.</p>

      <h2 style="margin-top:52px;">How I work</h2>
      <p>Every session — whether it's a one-to-one healing, a weekly online class or an in-person gathering — follows the same core principle: cleanse first, then energise. No touch is involved. You stay fully clothed and seated or lying comfortably, while the energy work is done around your energy field rather than your physical body.</p>
      <p>[Add specifics here: your certification level, any specialisations, session formats offered one-to-one, and what a first session with you looks like.]</p>

      <h2 style="margin-top:52px;">What I believe</h2>
      <div class="card-grid grid-3" style="margin-top:24px;">
        <div class="card"><h3>Complementary, not a replacement</h3><p>This work sits alongside your doctor, therapist or financial advisor — never in place of them.</p></div>
        <div class="card"><h3>Open to everyone</h3><p>No particular belief system or prior experience is required to benefit from these practices.</p></div>
        <div class="card"><h3>Practice over perfection</h3><p>Small, consistent habits — a weekly session, a few minutes of self-care daily — matter more than any single dramatic moment.</p></div>
      </div>
    </div>
  </section>

  <section class="bg-teal section-tight">
    <div class="container" style="text-align:center;">
      <h2 style="max-width:26ch; margin:0 auto 18px;">Curious to experience a session?</h2>
      <a class="btn btn-marigold" href="events.html">Browse upcoming sessions</a>
    </div>
  </section>
"""
    return page_shell(
        title="About Shravya — Pranic Healing with Shravya",
        description="Meet Shravya, a Pranic Healing practitioner and teacher based in Bengaluru, offering online and in-person energy healing sessions.",
        active="about.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Services page
# ---------------------------------------------------------------------------

def render_services():
    body = """
  <section class="hero" style="padding-bottom:60px;">
    <div class="container">
      <div class="eyebrow"><span class="ring"></span>Services</div>
      <h1 style="max-width:16ch;">Choose your <span class="italic">next step.</span></h1>
      <p class="lede">Pranic Healing works with the aura and chakras — your energy field — using prana to cleanse what's blocked and re-energise what's depleted. Every path below starts with the same simple, no-touch approach.</p>
    </div>
  </section>

  <section class="section-tight" id="mental-health">
    <div class="container detail-grid">
      <div>
        <div class="eyebrow"><span class="ring"></span>01 · Mental &amp; emotional health</div>
        <h2>Mental Health</h2>
        <p>Emotional strain — stress, anxiety, low mood — is approached here as an energetic imbalance as much as a mental one. Sessions focus on clearing blocked energy from the chakras connected to emotion, then re-energising them, with the aim of restoring a calmer, steadier baseline.</p>
        <p>This path pairs well with the weekly <strong>Meditation on the Twin Hearts</strong> and <strong>Mass Pranic Healing</strong> sessions, both built around stress reduction and emotional balance.</p>
        <a class="btn btn-outline" href="events.html">See related sessions</a>
      </div>
      <aside class="side-card">
        <h4>Good to pair with</h4>
        <ul class="links">
          <li><a href="events/twin-hearts-meditation.html">Meditation on the Twin Hearts →</a></li>
          <li><a href="events/mass-pranic-healing.html">Mass Pranic Healing →</a></li>
        </ul>
      </aside>
    </div>
  </section>

  <section class="section-tight bg-ivory-deep" id="financial-abundance">
    <div class="container detail-grid">
      <div>
        <div class="eyebrow"><span class="ring"></span>02 · Financial abundance</div>
        <h2>Financial Abundance</h2>
        <p>Drawing on the Pranic Healing system's teachings around prosperity — sometimes called Kriyashakti — this path looks at the energetic patterns behind our relationship with money: self-doubt, limiting beliefs, and a scattered focus. The aim is a clearer, more grounded mindset, practised alongside — never instead of — sound financial planning.</p>
        <p>Techniques introduced include simple gratitude and blessing practices, prosperity meditation, and an introduction to thought-form work.</p>
        <a class="btn btn-outline" href="events/financial-abundance-intro.html">See the introduction session</a>
      </div>
      <aside class="side-card">
        <h4>Good to know</h4>
        <p class="small">This is a complementary mindset-and-energy practice, not financial advice, and carries no guarantee of any financial outcome.</p>
      </aside>
    </div>
  </section>

  <section class="section-tight" id="physical-wellbeing">
    <div class="container detail-grid">
      <div>
        <div class="eyebrow"><span class="ring"></span>03 · Physical well-being</div>
        <h2>Physical Well-Being</h2>
        <p>Used alongside your regular medical care, energy work here focuses on supporting the body's own recovery processes — scanning for blocked or depleted energy around an area of concern, clearing it, then channeling fresh prana to support natural healing.</p>
        <p>This is never presented as a replacement for medical treatment. It's offered as a gentle complementary layer, and anyone with an ongoing condition should keep working with their doctor.</p>
        <a class="btn btn-outline" href="events/mass-pranic-healing.html">See Mass Pranic Healing</a>
      </div>
      <aside class="side-card">
        <h4>Good to pair with</h4>
        <ul class="links">
          <li><a href="events/mass-pranic-healing.html">Mass Pranic Healing →</a></li>
          <li><a href="events/pranic-self-care-practices.html">Pranic Self-Care Practices →</a></li>
        </ul>
      </aside>
    </div>
  </section>

  <section class="bg-teal">
    <div class="container" style="text-align:center;">
      <h2 style="max-width:26ch; margin:0 auto 18px;">Not sure where to start?</h2>
      <p style="margin:0 auto 28px; max-width:50ch; color:rgba(255,249,238,0.8);">The weekly Introduction to Pranic Healing session is the easiest first step — a beginner-friendly walkthrough with no assumptions made.</p>
      <a class="btn btn-marigold" href="events/introduction-to-pranic-healing.html">Join the introduction session</a>
    </div>
  </section>
"""
    return page_shell(
        title="Services — Pranic Healing with Shravya",
        description="Explore Pranic Healing pathways for mental health, financial abundance and physical well-being with Shravya.",
        active="services.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Events index page
# ---------------------------------------------------------------------------

def render_events_index():
    rows = []
    for e in EVENTS:
        chip_mode_class = "chip-offline" if "person" in e["mode"].lower() else "chip-online"
        cadence_class = "chip-monthly" if e["cadence"] == "Monthly" else "chip-online"
        rows.append(f'''      <a class="event-row" href="events/{e["slug"]}.html">
        <div class="when">{e["day"]}</div>
        <div class="meta">
          <div class="chips"><span class="chip {chip_mode_class}">{e["mode"]}</span><span class="chip {cadence_class}">{e["cadence"]}</span></div>
          <h3>{e["name"]}</h3>
          <p style="margin:0;">{e["intro"][:110]}&hellip;</p>
        </div>
        <div class="go">Details &rarr;</div>
      </a>''')
    rows_html = "\n".join(rows)

    body = f"""
  <section class="hero" style="padding-bottom:50px;">
    <div class="container">
      <div class="eyebrow"><span class="ring"></span>Community &amp; calendar</div>
      <h1 style="max-width:20ch;">Pranic Healing for <span class="italic">free &amp; abundant living.</span></h1>
      <p class="lede">Come together. Experience more. A steady weekly rhythm online, plus monthly and weekly in-person gatherings in Bengaluru — workshops, meditation circles and free introductory sessions.</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="container">
      <div class="month-note">
        <div>
          <strong style="color:var(--teal-950); font-family:var(--font-display); font-size:1.1rem;">Two ways to browse</strong>
          <p class="small" style="margin:6px 0 0;">See the calendar laid out day by day, or switch to a plain list of every session type. Weekly sessions repeat every week; the two in-person specials land on the last Friday and Saturday of each month.</p>
        </div>
        <div class="view-switch" role="tablist" aria-label="Switch event view">
          <button type="button" class="active" data-view-target="calendar" role="tab" aria-selected="true">Calendar view</button>
          <button type="button" data-view-target="list" role="tab" aria-selected="false">List view</button>
        </div>
      </div>

      <div class="view-panel active" data-view="calendar">
        <div class="cal-shell">
          <div class="cal-toolbar">
            <h3 id="cal-month-label">Loading…</h3>
            <div class="cal-nav">
              <button type="button" id="cal-prev" aria-label="Previous month">&larr;</button>
              <button type="button" id="cal-today" class="today-btn">Today</button>
              <button type="button" id="cal-next" aria-label="Next month">&rarr;</button>
            </div>
          </div>
          <div class="cal-legend">
            <span><span class="cal-dot online"></span> Online session</span>
            <span><span class="cal-dot offline"></span> In-person · Bengaluru</span>
          </div>
          <div class="cal-weekdays">
            <div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div><div>Sun</div>
          </div>
          <div class="cal-grid" id="cal-grid" data-base=""></div>
          <div class="cal-day-panel" id="cal-day-panel"></div>
        </div>
      </div>

      <div class="view-panel" data-view="list">
        <div class="section-head">
          <div class="eyebrow"><span class="ring"></span>All sessions</div>
          <h2>Every type of event, explained</h2>
        </div>
        <div class="event-list">
{rows_html}
        </div>
      </div>
    </div>
  </section>
"""
    return page_shell(
        title="Community & Events — Pranic Healing with Shravya",
        description="Browse every Pranic Healing session — weekly online classes and in-person gatherings in Bengaluru — with full details for each.",
        active="events.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Blog page
# ---------------------------------------------------------------------------

def render_blog():
    drafts = [
        ("What is prana, really?", "A plain-language primer on the life force at the centre of Pranic Healing, and how it relates to concepts like qi and chi in other traditions."),
        ("Building a five-minute daily energy habit", "Small, sustainable self-care practices worth trying between weekly sessions."),
        ("Inside a Meditation on the Twin Hearts", "What actually happens, step by step, in this cornerstone practice — and what first-timers tend to notice."),
    ]
    cards = "\n".join(
        f'''      <div class="card">
        <span class="chip chip-monthly" style="margin-bottom:14px; display:inline-flex;">Coming soon</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>'''
        for t, d in drafts
    )
    body = f"""
  <section class="hero" style="padding-bottom:50px;">
    <div class="container">
      <div class="eyebrow"><span class="ring"></span>Blog</div>
      <h1 style="max-width:18ch;">Ideas for your <span class="italic">inner journey.</span></h1>
      <p class="lede">Reflections, practical techniques and community stories from the practice — new posts are on their way. Here's a preview of what's coming.</p>
    </div>
  </section>
  <section class="section-tight">
    <div class="container card-grid grid-3">
{cards}
    </div>
  </section>
  <section class="bg-teal section-tight">
    <div class="container" style="text-align:center;">
      <h2 style="max-width:24ch; margin:0 auto 18px;">Want to be notified when we publish?</h2>
      <a class="btn btn-marigold" href="contact.html">Get in touch</a>
    </div>
  </section>
"""
    return page_shell(
        title="Resources — Pranic Healing with Shravya",
        description="Reflections, practical techniques and community stories from the Pranic Healing practice. New posts coming soon.",
        active="blog.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Contact page
# ---------------------------------------------------------------------------

def render_contact():
    body = """
  <section class="hero" style="padding-bottom:50px;">
    <div class="container">
      <div class="eyebrow"><span class="ring"></span>Contact us</div>
      <h1 style="max-width:16ch;">Begin your <span class="italic">journey.</span></h1>
      <p class="lede">Have a question, want to book a session, or want to join an upcoming event? Get in touch — we'd love to hear from you.</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="container contact-grid">
      <div>
        <h2>Your space is waiting.</h2>
        <p>Reach out by phone, email or the form here — whichever's easiest. We typically reply within a day or two.</p>
        <div class="contact-item"><div class="label">EMAIL</div><div class="value"><a href="mailto:gm.sushravya@gmail.com">gm.sushravya@gmail.com</a></div></div>
        <div class="contact-item"><div class="label">PHONE</div><div class="value"><a href="tel:+918861318805">+91 88613-18805</a></div></div>
        <div class="contact-item"><div class="label">ADDRESS</div><div class="value">Bengaluru, India</div></div>
        <div class="contact-item">
          <div class="label">FOLLOW ALONG</div>
          <div class="value" style="font-size:1rem; display:flex; gap:14px; margin-top:6px;">
            <a href="#" style="text-decoration:underline;">Instagram</a>
            <a href="#" style="text-decoration:underline;">WhatsApp</a>
            <a href="#" style="text-decoration:underline;">YouTube</a>
          </div>
        </div>
      </div>

      <div class="side-card">
        <h4>Send a message</h4>
        <form id="contact-form">
          <div class="form-field">
            <label for="name">Name</label>
            <input id="name" name="name" type="text" required placeholder="Your full name">
          </div>
          <div class="form-field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" required placeholder="you@example.com">
          </div>
          <div class="form-field">
            <label for="interest">I'm interested in</label>
            <select id="interest" name="interest">
              <option>A one-to-one healing session</option>
              <option>Mass Pranic Healing</option>
              <option>Introduction to Pranic Healing</option>
              <option>Meditation on the Twin Hearts</option>
              <option>Community Catchup</option>
              <option>Group Meditation &amp; Free Healing</option>
              <option>Pranic Self-Care Practices</option>
              <option>Financial Abundance session</option>
              <option>Full Moon Meditation Circle</option>
              <option>Something else</option>
            </select>
          </div>
          <div class="form-field">
            <label for="message">Message</label>
            <textarea id="message" name="message" placeholder="Tell us a little about what you're looking for..."></textarea>
          </div>
          <button class="btn btn-primary" type="submit" style="width:100%; justify-content:center;">Send message</button>
          <p id="form-note" class="small" style="display:none; margin-top:14px; color:var(--teal-700);"></p>
        </form>
      </div>
    </div>
  </section>
"""
    return page_shell(
        title="Contact — Pranic Healing with Shravya",
        description="Get in touch to book a Pranic Healing session, ask a question, or join an upcoming event in Bengaluru or online.",
        active="contact.html",
        body=body,
    )

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

def main():
    write("index.html", render_home())
    write("about.html", render_about())
    write("services.html", render_services())
    write("events.html", render_events_index())
    write("blog.html", render_blog())
    write("contact.html", render_contact())
    for e in EVENTS:
        write(f'events/{e["slug"]}.html', render_event_page(e))

if __name__ == "__main__":
    main()
