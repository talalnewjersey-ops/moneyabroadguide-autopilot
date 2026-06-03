"""
Landing page conversion optimizer for the ebook page.

Targets: /build-your-credit-score-in-the-usa-2026-edition/

What it does:
  - Injects conversion sections after the hero (What's Included, Who It's For,
    Table of Contents, Social Proof, Author Story, Guarantee)
  - Replaces #buy / placeholder checkout links with the real CTA destination
  - Removes unverified social-proof claims (Trusted by 15,000+, etc.)
  - Adds a sticky-bottom mobile CTA section marker (handled by the plugin)
"""

import os
import re
import base64
import json
import requests

print("🚀 LANDING PAGE OPTIMIZER — STARTING")

WP_URL      = os.getenv("WP_URL", "https://moneyabroadguide.com")
WP_USER     = os.getenv("WP_USER", "")
WP_PASSWORD = os.getenv("WP_PASSWORD", "")

EBOOK_SLUG     = "build-your-credit-score-in-the-usa-2026-edition"
EBOOK_FULL_URL = f"{WP_URL}/{EBOOK_SLUG}/"

# Gumroad checkout — all purchase buttons on the landing page point here.
CHECKOUT_URL = "https://moneyabroadguide.gumroad.com/l/vemvxw"

credentials = f"{WP_USER}:{WP_PASSWORD}"
token       = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json",
}

# ── Injection markers ─────────────────────────────────────────────────────────
START = "<!-- MAG_LP_SECTIONS_START -->"
END   = "<!-- MAG_LP_SECTIONS_END -->"

# ── Brand colour (kept inline so sections are self-contained) ─────────────────
GREEN  = "#1a9e5f"
GREEN_D = "#157a49"


# ─────────────────────────────────────────────────────────────────────────────
# HTML section builders
# ─────────────────────────────────────────────────────────────────────────────

def _section(title: str, body: str, bg: str = "#ffffff", extra_style: str = "") -> str:
    return f"""
<section style="background:{bg};padding:48px 20px;{extra_style}">
  <div style="max-width:720px;margin:0 auto;">
    <h2 style="font-size:clamp(22px,4vw,30px);font-weight:800;text-align:center;margin-bottom:32px;color:#111;">{title}</h2>
    {body}
  </div>
</section>"""


def _check_item(text: str, color: str = GREEN) -> str:
    return (
        f'<div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px;">'
        f'<span style="color:{color};font-size:20px;font-weight:800;flex-shrink:0;line-height:1.3;">&#10003;</span>'
        f'<span style="font-size:16px;color:#333;line-height:1.5;">{text}</span>'
        f'</div>'
    )


def section_whats_included() -> str:
    items = [
        "184-Page PDF Guide",
        "Beginner-Friendly",
        "Updated for 2026",
        "Instant Download",
        "Mobile, Tablet &amp; Desktop Compatible",
        "Bonus Templates Included",
    ]
    rows = "".join(_check_item(i) for i in items)
    body = (
        f'<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:28px 24px;">'
        f'{rows}'
        f'</div>'
    )
    return _section("What&#8217;s Included", body, bg="#f9fafb")


def section_who_is_it_for() -> str:
    items = [
        "New immigrants to the USA",
        "International students",
        "New permanent residents",
        "People with no credit history",
        "Future home buyers",
        "People planning to finance a car",
        "Anyone who wants to build credit faster",
    ]
    rows = "".join(_check_item(i) for i in items)
    body = (
        f'<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:28px 24px;">'
        f'{rows}'
        f'</div>'
    )
    return _section("Who Is This Guide For?", body)


def section_toc() -> str:
    chapters = [
        ("1", "Understanding Credit Scores"),
        ("2", "Your First Credit Card"),
        ("3", "Building Credit Without Debt"),
        ("4", "Credit Utilization"),
        ("5", "Avoiding Common Credit Mistakes"),
        ("6", "Credit Building Tools"),
        ("7", "Credit Score Recovery"),
        ("8", "Long-Term Credit Growth"),
        ("9", "Credit and Housing"),
        ("10", "Credit and Financing"),
    ]
    rows = ""
    for num, title in chapters:
        rows += (
            f'<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-bottom:1px solid #e5e7eb;">'
            f'<span style="background:{GREEN};color:#fff;font-weight:700;font-size:13px;border-radius:50%;'
            f'width:30px;height:30px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{num}</span>'
            f'<span style="font-size:16px;color:#222;">Chapter {num} &#8211; {title}</span>'
            f'</div>'
        )
    body = f'<div style="border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">{rows}</div>'
    return _section("Inside This Guide", body, bg="#f9fafb")


def section_social_proof() -> str:
    profiles = [
        ("Ahmed",  "560", "750"),
        ("Julien", "580", "780"),
        ("Maria",  "610", "790"),
    ]
    cards = ""
    for name, before, after in profiles:
        improvement = int(after) - int(before)
        cards += f"""
<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:24px 20px;text-align:center;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-weight:700;font-size:17px;color:#111;margin-bottom:16px;">{name}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:16px;">
    <div>
      <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">Before</div>
      <div style="font-size:32px;font-weight:800;color:#ef4444;">{before}</div>
    </div>
    <div style="font-size:24px;color:{GREEN};font-weight:800;">&#8594;</div>
    <div>
      <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">After</div>
      <div style="font-size:32px;font-weight:800;color:{GREEN};">{after}</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:13px;color:#555;">+{improvement} point improvement</div>
</div>"""
    body = (
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;">'
        f'{cards}'
        f'</div>'
        f'<p style="text-align:center;font-size:13px;color:#888;margin-top:16px;">'
        f'Results shown are examples. Individual results may vary.</p>'
    )
    return _section("Real Credit Score Improvement Examples", body, bg="#f0fdf4")


def section_author_story() -> str:
    body = f"""
<div style="display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start;">
  <div style="flex:1;min-width:240px;">
    <p style="font-size:16px;color:#333;line-height:1.7;margin-bottom:14px;">
      When I arrived in North America, I quickly realized that having money wasn&#8217;t enough.
      Without a credit score, renting an apartment, getting approved for a credit card, or
      financing a car became much harder.
    </p>
    <p style="font-size:16px;color:#333;line-height:1.7;margin-bottom:14px;">
      I created this guide to help newcomers avoid the mistakes I made and build strong credit
      from day one.
    </p>
    <p style="font-size:16px;color:#333;line-height:1.7;">
      Today, MoneyAbroadGuide helps immigrants better understand banking, credit, money transfers
      and personal finance in the USA and Canada.
    </p>
    <p style="font-weight:700;color:#111;margin-top:18px;">&#8212; Talal Eddaouahiri, Founder of MoneyAbroadGuide</p>
  </div>
</div>"""
    return _section("Why I Created This Guide", body, bg="#f9fafb")


def section_guarantee() -> str:
    body = f"""
<div style="text-align:center;max-width:520px;margin:0 auto;">
  <div style="font-size:56px;margin-bottom:16px;">&#128737;</div>
  <h3 style="font-size:22px;font-weight:800;color:#111;margin-bottom:12px;">
    30-Day Money Back Guarantee
  </h3>
  <p style="font-size:16px;color:#555;line-height:1.7;">
    If you&#8217;re not satisfied with the guide, simply contact us within 30 days of purchase
    for a full refund. No questions asked.
  </p>
</div>"""
    return _section("Our Promise to You", body, bg="#f0fdf4")


def section_final_cta() -> str:
    return f"""
<section style="background:linear-gradient(135deg,#0d3b26 0%,#1a9e5f 100%);padding:56px 20px;text-align:center;">
  <div style="max-width:600px;margin:0 auto;">
    <h2 style="font-size:clamp(22px,4vw,32px);font-weight:800;color:#fff;margin-bottom:12px;line-height:1.3;">
      Ready to Build Your Credit Score?
    </h2>
    <p style="font-size:17px;color:#cffce5;margin-bottom:28px;">
      Get instant access to the complete 184-page guide for just <strong style="color:#fff;">$19.99</strong>.
    </p>
    <a href="{CHECKOUT_URL}"
       style="display:inline-block;background:#fff;color:#0d3b26 !important;font-weight:800;font-size:17px;
              padding:16px 40px;border-radius:50px;text-decoration:none;
              box-shadow:0 4px 20px rgba(0,0,0,.25);transition:transform .15s ease;"
       onmouseover="this.style.transform='translateY(-2px)'"
       onmouseout="this.style.transform='translateY(0)'">
      Get Instant Access — $19.99
    </a>
    <p style="font-size:13px;color:#a8f5d2;margin-top:16px;">
      &#128274; Secure payment &nbsp;&#183;&nbsp; Instant download &nbsp;&#183;&nbsp; 30-day money back guarantee
    </p>
  </div>
</section>"""


def build_all_sections() -> str:
    return (
        "\n" + START + "\n"
        + section_whats_included()
        + section_who_is_it_for()
        + section_toc()
        + section_social_proof()
        + section_author_story()
        + section_guarantee()
        + section_final_cta()
        + "\n" + END + "\n"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Content sanitizers
# ─────────────────────────────────────────────────────────────────────────────

UNVERIFIED_PATTERNS = [
    r'Trusted by\s+[\d,]+\+?',
    r'[\d,]+\+?\s+customers',
    r'Expert Verified',
    r'4\.9\s*/\s*5\s*Rated?',
    r'4\.9\s*Stars?',
    r'Rated 4\.9',
    r'15,?000\+',
]


def remove_unverified_claims(content: str) -> str:
    for pattern in UNVERIFIED_PATTERNS:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    return content


def fix_placeholder_links(content: str) -> str:
    """Replace #buy and other placeholder hrefs with the checkout URL."""
    content = re.sub(r'href=["\']#buy["\']', f'href="{CHECKOUT_URL}"', content, flags=re.IGNORECASE)
    content = re.sub(r'href=["\']#checkout["\']', f'href="{CHECKOUT_URL}"', content, flags=re.IGNORECASE)
    content = re.sub(r'href=["\']#purchase["\']', f'href="{CHECKOUT_URL}"', content, flags=re.IGNORECASE)
    content = re.sub(r'href=["\']#get-now["\']', f'href="{CHECKOUT_URL}"', content, flags=re.IGNORECASE)
    content = re.sub(r'href=["\']#order["\']', f'href="{CHECKOUT_URL}"', content, flags=re.IGNORECASE)
    return content


def clean_old_sections(content: str) -> str:
    if START in content and END in content:
        before = content.split(START)[0]
        after  = content.split(END, 1)[-1]
        return before + after
    return content


# ─────────────────────────────────────────────────────────────────────────────
# WordPress API helpers
# ─────────────────────────────────────────────────────────────────────────────

def find_ebook_page() -> dict | None:
    """Try pages first, then posts."""
    for endpoint in ["pages", "posts"]:
        url = f"{WP_URL}/wp-json/wp/v2/{endpoint}?slug={EBOOK_SLUG}&_fields=id,title,content,link,type"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                print(f"  Found as {endpoint[:-1]}: ID {data[0]['id']}")
                return data[0]
    return None


def update_page(page_id: int, new_content: str, post_type: str = "posts") -> int:
    url  = f"{WP_URL}/wp-json/wp/v2/{post_type}/{page_id}"
    resp = requests.post(url, headers=HEADERS, json={"content": new_content}, timeout=30)
    return resp.status_code


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if not WP_USER or not WP_PASSWORD:
        print("⚠️  WP_USER / WP_PASSWORD not set — skipping REST API updates")
        print("   Set environment variables to enable live updates.")
        return

    print(f"🔍 Looking for ebook page: {EBOOK_SLUG}")
    page = find_ebook_page()

    if not page:
        print(f"❌ Ebook page not found (slug: {EBOOK_SLUG})")
        print("   Verify the page exists and the slug matches exactly.")
        return

    page_id   = page["id"]
    post_type = "pages" if page.get("type") == "page" else "posts"
    content   = page["content"]["rendered"]

    print(f"📄 Processing page ID {page_id} ({post_type})")

    # 1. Remove old injected sections
    content = clean_old_sections(content)

    # 2. Remove unverified claims
    content = remove_unverified_claims(content)

    # 3. Fix placeholder checkout links
    content = fix_placeholder_links(content)

    # 4. Append new conversion sections
    new_sections = build_all_sections()

    # Insert after the first <p> or after opening content (before the first <h2>)
    # so sections appear below the hero but above the fold content.
    hero_end_patterns = [
        r'(</figure>)',        # after hero image
        r'(<hr\s*/?>)',        # after horizontal rule
        r'(</p>\s*<h2)',       # before first h2
    ]
    inserted = False
    for pat in hero_end_patterns:
        match = re.search(pat, content, re.IGNORECASE)
        if match:
            pos     = match.end(1)
            content = content[:pos] + new_sections + content[pos:]
            inserted = True
            print(f"  ✓ Sections inserted after pattern: {pat}")
            break

    if not inserted:
        # Fallback: append to end
        content += new_sections
        print("  ℹ️  Sections appended to end of content (no hero marker found)")

    # 5. Push update
    status = update_page(page_id, content, post_type)
    if status in (200, 201):
        print(f"✅ Page {page_id} updated successfully (HTTP {status})")
    else:
        print(f"❌ Update failed: HTTP {status}")


if __name__ == "__main__":
    main()
