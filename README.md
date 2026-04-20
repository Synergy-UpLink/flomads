# The Flomads — Jekyll Site

noMADS going with the FLO · [flomads.com](https://flomads.com)

## Structure

```
flomads/
├── _config.yml           # Site configuration
├── _layouts/
│   └── default.html      # Single shared layout
├── _includes/
│   ├── head.html         # <head> meta, fonts, CSS
│   ├── nav.html          # Navigation (active state via page.url)
│   └── footer.html       # Footer
├── assets/
│   ├── css/style.css     # All styles
│   ├── js/nav.js         # Scroll + mobile nav behavior
│   └── images/henry.png  # Chief Navigator
├── index.html            # Home
├── about/index.html      # About / Crew / Timeline
├── now/index.html        # Now page
└── Gemfile               # github-pages gem
```

## Local Development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Open `http://localhost:4000`

## Deployment

Push to the `gh-pages` branch (or `main`, configured in GitHub Pages settings).
GitHub Pages builds Jekyll automatically — no CI needed.

## Updating the Now Page

Edit `now/index.html`. Update the `now_updated` front matter value at the top:

```yaml
---
now_updated: "April 2026"
---
```

## Hidden Reference Page (for prospective homeowners)

**URL:** `/sit-with-us/flomads-references-a7x92k/`

This page is not linked anywhere on the public site, excluded from the sitemap,
and blocked in `robots.txt`. It's protected by both a secret URL slug and an
optional JS password prompt.

### Access controls

Edit `_data/sits.yml` → `access:` block:

```yaml
access:
  require_slug: true        # set false to remove slug requirement
  require_password: true    # set false to disable password gate
  password: "flomads2024"   # change this!
```

The lock icon (🔐) in the bottom-right corner of the page shows the current
config state. The toggles there are display-only — changes must be made in the
YAML and rebuilt.

### Adding a new sit

Add an entry to `_data/sits.yml` → `sits:` list (most recent first). Minimal example:

```yaml
- id: london-2026
  location: "London"
  country: "United Kingdom"
  flag: "🇬🇧"
  dates: "July – September 2026"
  lat: 51.505
  lng: -0.09
  current: false
  owners: "Jane"
  testimonial:
    quote: "Wonderful sitters."
    name: "Jane, London"
  photos:
    slideshow: []
    album_url: "https://photos.google.com/share/..."
    album_label: "View Google Photos Album"
  animals:
    - name: "Biscuit"
      species: "Dog"
      breed: "Labrador"
      age: "3 years"
      photo: ""
      personality: "Loves everyone."
      care_notes: "Fed twice daily."
      challenges: ""
```

### Adding photos

Place images in `assets/images/sits/<sit-id>/` and reference them in the
`slideshow` list as `<sit-id>/filename.jpg`.

For Google Photos albums, paste the share URL into `album_url`.

### Adding contact methods

Add entries to `_data/sits.yml` → `contact:` list:

```yaml
- type: phone          # email | phone | facebook | instagram | twitter | whatsapp | trustedhousesitters | website | other
  label: "+1 555 000 0000"
  value: "+15550000000"
  primary: true        # true = shown in main contact row
```

## Adding Pages

Create a new directory with an `index.html` file using the default layout:

```html
---
layout: default
title: "Page Title"
description: "Page description for SEO."
---

<!-- your HTML here -->
```
