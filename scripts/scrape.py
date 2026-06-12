# One-time migration scraper: Squarespace -> Hugo markdown
import json
import os
import re
import html2text
from bs4 import BeautifulSoup

BASE = "https://www.jasonyu-explorations.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTS = [
  "the-ugly-cute-moat-what-disney-and-pop-mart-reveal-about-modern-brand-building",
  "the-librarians-dilemma-why-your-rag-system-lies-and-how-knowledge-graphs-can-fix-it",
  "from-messy-stories-to-mission-statements-a-product-driven-approach-to-rapid-ai-prototyping",
  "beyond-brittle-bots-building-resilient-ai-agents-with-the-react-framework",
  "conquer-yourself-how-to-use-ai-as-your-ultimate-sparring-partner",
  "why-pay-more-how-brands-can-wield-ai-tools-to-build-unscalable-human-value",
  "disney-ecommerce",
  "involution-or-evolution",
]
PAGES = ["about", "lets-connect"]

h2t = html2text.HTML2Text()
h2t.body_width = 0
h2t.ignore_emphasis = False
h2t.images_as_html = False

# Fetch via curl: it uses the macOS keychain, which has the corporate root cert
import subprocess

def fetch(url):
  return subprocess.run(
    ["curl", "-sSL", "--max-time", "60", url],
    check=True, capture_output=True, text=True
  ).stdout

def curl_download(url, dest):
  subprocess.run(["curl", "-sSL", "--max-time", "120", "-o", dest, url], check=True)

def download_image(url, slug, idx):
  url = url.split("?")[0]
  ext = os.path.splitext(url)[1].lower() or ".jpg"
  if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
    ext = ".jpg"
  rel = f"/images/{slug}/img{idx}{ext}"
  dest = os.path.join(ROOT, "site/static", rel.lstrip("/"))
  os.makedirs(os.path.dirname(dest), exist_ok=True)
  if not os.path.exists(dest):
    try:
      curl_download(url + "?format=1500w", dest)
    except subprocess.CalledProcessError:
      curl_download(url, dest)
  return rel

def localize_images(container, slug):
  count = 0
  for img in container.find_all("img"):
    src = img.get("data-src") or img.get("src") or ""
    if not src:
      img.decompose()
      continue
    count += 1
    rel = download_image(src, slug, count)
    img.attrs = {"src": rel, "alt": img.get("alt", "")}
  return count

def yaml_escape(s):
  return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def scrape_post(slug):
  html = fetch(f"{BASE}/blog/{slug}")
  soup = BeautifulSoup(html, "html.parser")
  meta = {}
  for s in soup.find_all("script", type="application/ld+json"):
    try:
      d = json.loads(s.string)
    except Exception:
      continue
    if d.get("@type") == "Article":
      meta = d
  item = soup.select_one(".blog-item-content")
  content = item.select_one(".sqs-html-content") if item else None
  assert content is not None, f"no content for {slug}"
  localize_images(item, slug)
  # body = all sqs-html-content blocks + image blocks inside the item, in document order
  parts = []
  for block in item.select(".sqs-block-content, .sqs-html-content"):
    if block.find_parent(class_="sqs-block-content"):
      continue
    parts.append(h2t.handle(str(block)))
  body = "\n".join(parts)
  body = re.sub(r"\n{3,}", "\n\n", body).strip()
  tags = sorted({a.get_text(strip=True) for a in soup.select(".blog-item-tag-wrapper a, .blog-meta-item--tags a")})
  if not tags:
    tags = sorted({a.get_text(strip=True) for a in soup.select('a[href*="/blog/tag/"]')})
  title = meta.get("headline") or soup.find("h1").get_text(strip=True)
  date = meta.get("datePublished", "")
  fm = ["---", f"title: {yaml_escape(title)}", f"date: {date}", f"slug: {yaml_escape(slug)}"]
  if tags:
    fm.append("tags: [" + ", ".join(yaml_escape(t) for t in tags) + "]")
  fm.append("---")
  out = os.path.join(ROOT, "site/content/blog", f"{slug}.md")
  os.makedirs(os.path.dirname(out), exist_ok=True)
  with open(out, "w") as f:
    f.write("\n".join(fm) + "\n\n" + body + "\n")
  print(f"post: {slug} ({len(body)} chars, {len(tags)} tags)")

def scrape_page(slug):
  html = fetch(f"{BASE}/{slug}")
  soup = BeautifulSoup(html, "html.parser")
  main = soup.select_one("#page") or soup.select_one("main")
  assert main is not None, f"no main for {slug}"
  localize_images(main, slug)
  parts = []
  for block in main.select(".sqs-block-content"):
    if block.find_parent(class_="sqs-block-content"):
      continue
    parts.append(h2t.handle(str(block)))
  body = re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip()
  title = soup.title.get_text().split("—")[-1].strip() if soup.title else slug
  out = os.path.join(ROOT, "site/content", f"{slug}.md")
  os.makedirs(os.path.dirname(out), exist_ok=True)
  with open(out, "w") as f:
    f.write(f"---\ntitle: {yaml_escape(title)}\nslug: {yaml_escape(slug)}\n---\n\n{body}\n")
  print(f"page: {slug} ({len(body)} chars)")

for p in POSTS:
  scrape_post(p)
for p in PAGES:
  scrape_page(p)
