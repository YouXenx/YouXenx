"""
Build achievement tiles for the profile README (assets/achievements/*.svg).

Edit ACHIEVEMENTS below — set earned=True only for achievements you really have —
then run:  python3 scripts/build_achievements.py

Badge artwork is GitHub's own achievement image, embedded so the tile works inside
an <img> tag. Locked tiles are greyscale, dimmed and marked LOCKED.
Uses only the Python standard library (plus macOS `sips` for resizing, if available).
"""
import base64
import os
import shutil
import subprocess
import tempfile
import urllib.request

ACHIEVEMENTS = [
    # (slug, title, earned)
    ('pull-shark', 'Pull Shark', True),
    ('yolo', 'YOLO', True),
    ('quickdraw', 'Quickdraw', True),
    ('galaxy-brain', 'Galaxy Brain', False),
    ('pair-extraordinaire', 'Pair Extraordinaire', False),
    ('starstruck', 'Starstruck', False),
    ('arctic-code-vault-contributor', 'Arctic Code Vault', False),
    ('public-sponsor', 'Public Sponsor', False),
    ('heart-on-your-sleeve', 'Heart On Your Sleeve', False),
    ('open-sourcerer', 'Open Sourcerer', False),
]

BASE_URL = 'https://github.githubassets.com/images/modules/profile/achievements/{slug}-default.png'
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'achievements')
W, H = 150, 176
BADGE = 104
ACCENT = '#845adf'
GREEN = '#26bf94'
GRAY = '#8b949e'  # readable on both light and dark GitHub themes
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"


def badge_png(slug):
    """Download the badge and shrink it to 128px when `sips` is available."""
    with urllib.request.urlopen(BASE_URL.format(slug=slug)) as resp:
        data = resp.read()
    if shutil.which('sips'):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = os.path.join(tmp, 'in.png'), os.path.join(tmp, 'out.png')
            with open(src, 'wb') as fh:
                fh.write(data)
            subprocess.run(['sips', '-Z', '128', src, '--out', dst], check=True, capture_output=True)
            with open(dst, 'rb') as fh:
                data = fh.read()
    return base64.b64encode(data).decode()


def tile(slug, title, earned):
    png = badge_png(slug)
    x = (W - BADGE) / 2
    frame = ACCENT if earned else GRAY
    pill_text, pill_color = ('UNLOCKED', GREEN) if earned else ('LOCKED', GRAY)
    pill_w = 74 if earned else 62
    lock = '' if earned else f"""
  <g transform="translate({x + BADGE - 30}, {14 + BADGE - 30})">
    <circle cx="14" cy="14" r="14" fill="#1f2328" stroke="#ffffff" stroke-opacity="0.85" stroke-width="2"/>
    <rect x="8.5" y="13" width="11" height="9" rx="2" fill="#ffffff"/>
    <path d="M10.5 13v-2.5a3.5 3.5 0 0 1 7 0V13" fill="none" stroke="#ffffff" stroke-width="2"/>
  </g>"""
    image_attrs = '' if earned else ' filter="url(#gray)" opacity="0.38"'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title} ({'unlocked' if earned else 'locked'})">
  <title>{title} — {'unlocked' if earned else 'locked'}</title>
  <defs>
    <filter id="gray"><feColorMatrix type="saturate" values="0"/></filter>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{frame}" fill-opacity="0.07" stroke="{frame}" stroke-opacity="{0.45 if earned else 0.3}"/>
  <image x="{x}" y="14" width="{BADGE}" height="{BADGE}" xlink:href="data:image/png;base64,{png}"{image_attrs}/>{lock}
  <text x="{W / 2}" y="138" text-anchor="middle" font-family="{FONT}" font-size="12.5" font-weight="700" fill="{ACCENT if earned else GRAY}">{title}</text>
  <rect x="{(W - pill_w) / 2}" y="147" width="{pill_w}" height="18" rx="9" fill="{pill_color}" fill-opacity="0.14"/>
  <text x="{W / 2}" y="160" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="1" fill="{pill_color}">{pill_text}</text>
</svg>
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, title, earned in ACHIEVEMENTS:
        with open(os.path.join(OUT_DIR, f'{slug}.svg'), 'w') as fh:
            fh.write(tile(slug, title, earned))
        print(f"{'unlocked' if earned else 'locked  '}  {slug}")


if __name__ == '__main__':
    main()
