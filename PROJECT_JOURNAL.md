# PROJECT_JOURNAL — Blog Migration (Squarespace → Hugo + GitHub Pages)

## Goal
Migrate www.jasonyu-explorations.com off Squarespace to a free, self-maintained Hugo site on GitHub Pages, preserving the original design language and URL structure.

## Status: Build complete, pending deployment

### 2026-06-12 — Initial build
- **Design extracted from live Squarespace site** (template "cinnamon-sepia"):
  - Headings: Manrope 500, letter-spacing -0.02em, line-height 1.2
  - Body: Poppins 400, line-height 1.5
  - Palette: bg hsl(0,0%,98%), text black, accent hsl(0,0%,86%), dark accent hsl(0,0%,11%)
  - Blog list: alternating side-by-side layout, meta on top (author • date), excerpts shown
- **Content migrated:** 8 blog posts + About + Let's Connect via `scripts/scrape.py`
  (parses Squarespace HTML + JSON-LD, converts to markdown, localizes 20MB of images).
  Only the involution post had tags on the original site — confirmed via Squarespace JSON API.
- **Theme:** hand-written, no external theme dependency. 5 templates + 1 CSS file (~200 lines).
- **URLs preserved:** `/blog/<slug>/`, `/about/`, `/lets-connect/` match the original site
  (tag pages moved from `/blog/tag/X` to `/tags/x/` — minor, low traffic).
- **Verified:** local build + visual check of homepage, post page, about page vs original.

## Technical decisions
- Layouts live in `site/layouts/` directly (no theme folder) — simplest to maintain solo.
- Used `curl` for scraping instead of Python requests (corporate SSL inspection breaks Python certs).
- Homepage thumbnail = first image in each post (matches original behavior, no extra front matter).
- GitHub Actions deploy (not docs/ folder) so source and built site stay separate.

## Remaining steps (need Jason)
1. Create GitHub repo + push (`gh repo create` or github.com).
2. Repo Settings → Pages → Source: GitHub Actions.
3. Verify site on `<username>.github.io/<repo>` URL.
4. DNS cutover: CNAME `www` → `<username>.github.io`, set custom domain in Pages settings.
5. Decide on "Let's Connect" contact form: original Squarespace form doesn't carry over.
   Options: Formspree free tier, or just link LinkedIn/email.
6. After cutover: cancel Squarespace subscription (keep until DNS verified!).

### 2026-06-12 — Template iteration (Jason feedback)
- Homepage: featured hero (latest post, large) + card grid of earlier posts.
  Decided AGAINST homepage = full latest post (duplicate content, no overview).
- Removed Let's Connect page and nav entry (contact form question now moot).
- Footer: rotating quotes pulled from Jason's own posts (config: [[params.quotes]]
  in hugo.toml, random start, 8s fade rotation). Replaced redundant LinkedIn icon.
- Added prev/next article navigation on posts (earlier today).
