# jasonyu-explorations.com — Hugo blog

Personal blog migrated from Squarespace, rebuilt as a static Hugo site for free GitHub Pages hosting. The design recreates the original Squarespace look: Manrope headings, Poppins body, monochrome palette, alternating side-by-side blog list.

## Structure

```
site/
├── hugo.toml              # Site config (title, menus, permalinks)
├── content/
│   ├── blog/*.md          # Blog posts (one markdown file each)
│   └── about.md           # About Me page
├── layouts/               # The "theme" — 5 small HTML templates
│   ├── _default/baseof.html   # Page shell (header/nav/footer)
│   ├── _default/single.html   # Single post/page
│   ├── _default/list.html     # Tag pages
│   ├── index.html             # Homepage (featured post + card grid)
│   └── partials/linkedin-icon.html
├── assets/css/main.css    # All styling in one file (~200 lines)
└── static/images/         # Post images (organized per post slug)
scripts/scrape.py          # One-time migration scraper (no longer needed)
```

## Everyday tasks

**Preview locally** (install Hugo once with `brew install hugo`):
```bash
cd site && hugo server
# open http://localhost:1313
```

**Write a new post:** create `site/content/blog/my-post-slug.md`:
```markdown
---
title: "My Post Title"
date: 2026-06-12T09:00:00-0800
slug: "my-post-slug"
tags: ["Optional", "Tags"]
---

First paragraph becomes the homepage excerpt...

![](/images/my-post-slug/cover.jpg)
```
Put images in `site/static/images/my-post-slug/`. The first image in the post is used as the homepage thumbnail.

**Publish:** commit and push to `main` — GitHub Actions builds and deploys automatically (see `.github/workflows/deploy.yml`).

**Change styling:** everything is in `site/assets/css/main.css`. Design tokens (colors, fonts) are CSS variables at the top.

**Edit footer quotes:** the rotating quotes live in `site/hugo.toml` under `[[params.quotes]]` — add/remove entries freely.

## One-time deployment setup

1. Create a GitHub repo and push this folder.
2. Repo Settings → Pages → Source: **GitHub Actions**.
3. Custom domain: in Settings → Pages set `www.jasonyu-explorations.com`, then at your DNS provider add a CNAME record pointing `www` to `<username>.github.io`. Keep `baseURL` in `site/hugo.toml` as the custom domain.
4. Once DNS is verified, enable "Enforce HTTPS".

Until the custom domain is set up, the workflow auto-adjusts the baseURL to the github.io URL, so the site works either way.
