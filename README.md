# The Flomads — Jekyll Site

noMADS going with the FLO · [flomads.com](https://flomads.com)

Personal site for the Flomads: a home page, an About page, a Now page, a public
sitter Profile page with sit history and reviews, and two small content
collections (blog and articles). Built with Jekyll 4 and deployed to GitHub
Pages by a GitHub Actions workflow.

## Structure

```
flomads/
├── _config.yml               # Site config, collections, front-matter defaults
├── Gemfile                   # jekyll + sitemap, feed, seo-tag, kramdown-parser-gfm
├── Dockerfile                # Local dev image (ruby:3.2-slim)
├── .devcontainer/            # VS Code dev container (expects image local-jekyll:latest)
├── .github/workflows/
│   └── deploy.yml            # Build + deploy to GitHub Pages on push to main
├── _layouts/
│   ├── default.html          # Shared page shell (head, nav, content, footer, nav.js)
│   └── post.html             # Blog/article layout (applied via _config.yml defaults)
├── _includes/
│   ├── head.html             # <head>: meta, fonts, CSS, favicons, {% seo %}
│   ├── nav.html              # Header nav (active state via page.url)
│   ├── nav_v2_with_blog.html # Alternate nav that includes Blog/Articles (not in use)
│   ├── footer.html           # Footer + footer nav
│   ├── newsletter.html       # Newsletter signup banner (inline CSS + JS)
│   └── now_map.html          # Leaflet map of locations, centred on the current visit
├── _data/
│   ├── locations.yml         # Places and dated visits
│   └── sits.yml              # Sitter platforms, sits, animals, testimonials
├── _blog/                    # Blog collection  -> /blog/<slug>/
├── _articles/                # Articles collection -> /articles/<slug>/
├── index.html                # Home
├── about/index.html          # About: story, crew cards, "Where We've Been" timeline
├── now/index.html            # Now page
├── profile/index.html        # Sitter profiles, sit history, reviews (built from _data)
├── blog/index.html           # Blog index
├── articles/index.html       # Articles index
├── assets/
│   ├── css/style.css         # Site styles
│   ├── css/blog-articles.css # Blog/article styles
│   ├── js/nav.js             # Scroll + mobile nav behaviour
│   └── images/               # henry.png, henry-profile.png, jordan.png, admiral.png
│       └── sits/<sit>/       # Photos for each sit (see "Adding a sit")
├── robots.txt
├── site.webmanifest
└── favicon files
```

## Local development

Either use the dev container, or run Jekyll directly.

**Dev container (VS Code):** the container uses an image tagged
`local-jekyll:latest`, built from the `Dockerfile` in this repo:

```
docker build -t local-jekyll .
```

Then "Reopen in Container". On start it runs `bundle install` if needed and
serves the site on port 4000 with LiveReload (35729).

**Directly:**

```
bundle install
bundle exec jekyll serve --livereload
```

Open `http://localhost:4000`.

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site
with `bundle exec jekyll build` (Ruby 3.3, `JEKYLL_ENV=production`) and
deploys it with the official Pages actions. The workflow can also be started
manually from the Actions tab (`workflow_dispatch`).

The repository's Pages source must be set to **GitHub Actions**
(Settings → Pages). Nothing is deployed from a `gh-pages` branch.

## Content and data

### Pages

Create a directory with an `index.html`:

```
---
layout: default
title: "Page Title"
description: "Page description for SEO."
---

<!-- your HTML here -->
```

`default` is already the site-wide layout default (see `_config.yml`), but it
is kept explicit in front matter. Add the page to `_includes/nav.html`, and to
`_includes/footer.html` if it should appear there.

### Blog posts and articles

Add a Markdown file named `YYYY-MM-DD-slug.md` to `_blog/` or `_articles/`.
The `post` layout and the collection label/path are applied automatically by
the defaults in `_config.yml`. Front matter:

```
---
title: "Post title"
date: 2026-02-20
author: "The Admiral"
location: "Albrighton, Shropshire"
tags: ["slow travel", "village life"]
cover_image: ""            # optional path; leave "" for the plain hero
excerpt_text: "One or two sentences shown under the title."
---
```

### The Now page

Edit `now/index.html` and update `now_updated` in the front matter:

```
---
now_updated: "July 2026"
---
```

The map on the Now page centres on the visit marked `current: true` in
`_data/locations.yml`. When you move on, set the old visit's `current` to
`false` and the new one's to `true`. Only one visit should be current. If none
is, the map falls back to the first location in the list.

### Locations and visits — `_data/locations.yml`

Two lists:

- `locations` — one entry per physical place: `id` (slug), `name`, `country`,
  `flag`, `lat`, `lng`, and `description` (facts about the place itself, not a
  personal account of a stay). Names are kept deliberately general in places
  (e.g. "Space Coast, FL") so homeowners' exact locations aren't pinpointed.
  `lat` / `lng` are kept to two decimal places (about 1 km) for the same
  reason; the coordinates are published in the page source, so use a town or
  city centre, never an exact address.
- `visits` — a flat, chronological list of stays: `id`, `location_id` (must
  match a `locations` id), `type` (`sit`, `rental`, `sailing`, `vacation`,
  `home_base`; freeform), `start` / `end` (`YYYY-MM-DD`, or `""` if unknown),
  `label` (optional display override for the date range), `current`, and
  `blurb` (optional note about that stay).

### Sits, animals, and reviews — `_data/sits.yml`

Three top-level keys, all rendered on the public Profile page:

- `platforms` — cards linking to our sitter profiles: `name`, `icon`, `url`,
  `blurb`.
- `sits` — one entry per documented sit. `id` **must match** the `id` of a
  `visits` entry in `locations.yml`; that shared id is the only link between
  the two files. Fields: `owners`, `testimonial` (`quote`, `name`), `photos`,
  `animals`.
- `testimonials` — standalone reviews not tied to a documented sit: `quote`,
  `name`, `location`, `platform`. Don't duplicate a review that already lives
  on a sit's `testimonial`; the Profile page pulls those in automatically.

Animal fields: `name`, `species`, `breed` (required), `age`, `photo`, and
`notes`. `notes` is used as the photo caption/hover text; if it is empty a
caption is generated from the other fields. `personality`, `care_notes` and
`challenges` may also be present on older entries but are not currently
rendered.

### Adding a sit

1. Add the place to `locations` in `_data/locations.yml` if it isn't there.
2. Add a `visits` entry with `type: sit`.
3. Add a `sits` entry with the **same `id`** as the visit (newest first).
4. Put photos in `assets/images/sits/<folder>/` and reference them relative to
   `assets/images/sits/`, e.g. `photos: ["albi/albi.jpg"]` and
   `photo: "albi/mimi.jpg"`. Use one or two `photos`: a second image enables
   the arrival-vs-departure cross-fade.

```yaml
- id: albi-2026
  owners: "First & First"
  testimonial:
    quote: "Their words."
    name: "How they want to be credited"
  photos: ["albi/albi.jpg"]
  animals:
    - name: "Mimi"
      species: "Cat"
      breed: "Domestic Shorthair"
      photo: "albi/mimi.jpg"
```

## Newsletter

The signup banner (`_includes/newsletter.html`) is a small client-side form
with a honeypot field. It POSTs JSON (`siteId: flomads-main`) to a Cloudflare
Worker, which forwards the address to us as an email. Subscribers are added to
the list by hand; there is no mailing-list service behind it. If the request
fails, the form shows a fallback `mailto:` link.

## Third-party resources

- Google Fonts (Playfair Display, DM Sans, Cinzel Decorative) — `head.html`
- Leaflet 1.9.4 from unpkg and OpenStreetMap tiles — `now_map.html`
