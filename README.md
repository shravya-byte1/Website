# Pranic Healing with Shravya — website codebase

A modern, colourful, static rebuild of pranichealingwithshravya.com. Plain HTML/CSS/JS —
no build tools, frameworks, or install step required.

## What's inside

```
index.html          Home page
about.html           About Shravya
services.html        3 pillars: Mental Health / Financial Abundance / Physical Well-Being
events.html           Full community & events index (links to every event page)
blog.html             Blog placeholder ("coming soon" cards, ready to fill in)
contact.html          Contact details + working front-end form (needs a form backend, see below)
events/
  mass-pranic-healing.html
  introduction-to-pranic-healing.html
  twin-hearts-meditation.html
  community-catchup.html
  group-meditation-free-healing.html
  pranic-self-care-practices.html
  financial-abundance-intro.html
  full-moon-meditation.html
css/style.css         Full design system (colours, type, components)
js/main.js             Mobile nav toggle, FAQ accordion, contact form handler
generate.py            The Python script that generated every HTML page from shared
                        templates + a data file — edit this once, regenerate everywhere
```

## How to view it

Just open `index.html` in a browser — no server needed. To preview with clean URLs, run
a tiny local server from this folder: `python3 -m http.server 8000`, then visit
`http://localhost:8000`.

## How to edit content

Everything text-related — event names, days, benefits, FAQs, links — lives in the
`EVENTS` list near the top of `generate.py`. Change the data there, then re-run:

```
python3 generate.py
```

This regenerates all HTML files instantly with consistent styling, so you never have to
hand-edit repeated header/footer/nav markup across 14 files. If you'd rather hand-edit the
HTML files directly instead, that works fine too — just don't re-run `generate.py`
afterwards, or your manual edits will be overwritten.

## Things to personalise before publishing

- **About page** (`about.html`): replace the bracketed placeholder paragraphs with
  Shravya's real bio, certifications and training lineage.
- **Contact form** (`contact.html` / `js/main.js`): the form currently shows a friendly
  confirmation message but doesn't send anywhere. Wire it up to a free service like
  [Formspree](https://formspree.io) or [Netlify Forms](https://www.netlify.com/products/forms/)
  by adding an `action` attribute to the `<form>` tag — takes about five minutes.
- **Social links** (`contact.html`): the Instagram / WhatsApp / YouTube links are placeholders
  (`href="#"`) — add real URLs.
- **Photos**: the homepage and about page use a decorative ring placeholder instead of a
  real portrait. Swap in a photo of Shravya by replacing the `.portrait-ring` markup with
  an `<img>` tag.
- **Exact event dates/times**: each event page intentionally avoids hard-coding a specific
  calendar month (the original site's September 2026 dates will age quickly). Update the
  `month-note` callout on `events.html` and/or add a real calendar embed if you want live dates.

## Hosting

Because this is a static site, it can be deployed for free on:
- **Netlify** or **Vercel** — drag-and-drop the whole folder
- **GitHub Pages** — push this folder to a repo and enable Pages
- Any standard web host — just upload everything via FTP

## Design notes

- Palette: warm ivory background, deep peacock teal, marigold and lotus-pink accents —
  chosen to evoke prana/energy rather than a generic template look.
- Typography: Fraunces (display) + Work Sans (body), loaded from Google Fonts.
- Motif: concentric "aura rings" (SVG, inline, no external images needed) used in the
  hero, event headers and logo mark — grounded in the chakra/energy-field subject matter.
- Fully responsive down to mobile, with a working hamburger nav and accordion FAQs.
- Content for each event page (benefits, FAQs, useful links) was researched from
  established Pranic Healing sources and written in original wording — see the "Useful
  links" panel on each event page for further reading.


### Event images
Each event details page now includes an **Upload event image** area. Selected images are previewed immediately and saved locally in the browser for that specific event page. For production-wide uploads visible to every visitor, connect the input to a server/cloud storage service.
