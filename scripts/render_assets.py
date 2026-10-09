#!/usr/bin/env python3
"""Render all self-hosted visuals for the GitHub profile from config/profile.json.

Run: python scripts/render_assets.py
Verify reproducibility: python scripts/render_assets.py --check
No network calls or external Python dependencies.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "config/profile.json").read_text(encoding="utf-8"))
ASSETS = ROOT / "assets"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def svg_start(width: int, height: int, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>')


def palette(theme: str) -> dict[str, str]:
    if theme == "dark":
        return dict(bg="#07111F", bg2="#111C33", surface="#122238", text="#F4F8FF",
                    muted="#9DB4CD", border="#2C4664", grid="#213A54", accent="#58E1EF", purple="#A78BFA")
    return dict(bg="#F6FAFF", bg2="#E6F0FD", surface="#FFFFFF", text="#102A43",
                muted="#486581", border="#CADCEC", grid="#D7E5F2", accent="#007F9A", purple="#7453C7")


def hero(theme: str) -> str:
    p = palette(theme)
    g = f"hgrad-{theme}"
    s = [svg_start(1280, 366, PROFILE["full_name"] + " profile banner"),
        '<defs>',
        f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["bg"]}"/><stop offset="1" stop-color="{p["bg2"]}"/></linearGradient>',
        f'<linearGradient id="stroke-{theme}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["accent"]}"/><stop offset="1" stop-color="{p["purple"]}"/></linearGradient>',
        '</defs>',
        f'<rect width="1280" height="366" rx="25" fill="url(#{g})"/>',
        f'<rect x="1" y="1" width="1278" height="364" rx="24" fill="none" stroke="{p["border"]}"/>',
        f'<g stroke="{p["grid"]}" opacity=".48" stroke-width="1">',
        *[f'<path d="M {x} 0 V 366"/>' for x in range(0,1281,48)],
        *[f'<path d="M 0 {y} H 1280"/>' for y in range(0,367,48)], '</g>',
        '<circle cx="1042" cy="183" r="154" fill="none" stroke="'+p['purple']+'" stroke-width="1" opacity=".25"/>',
        '<circle cx="1042" cy="183" r="117" fill="none" stroke="'+p['accent']+'" stroke-width="1.3" opacity=".42"/>',
        '<circle cx="1042" cy="183" r="85" fill="none" stroke="'+p['purple']+'" stroke-width="1.5" opacity=".53"/>',
        f'<path d="M 889 183 H 1198 M 1042 30 V 336 M 934 75 L 1150 290 M 934 290 L 1150 75" stroke="{p["grid"]}" stroke-width="1.4"/>',
        f'<circle cx="1042" cy="183" r="58" fill="{p["surface"]}" stroke="url(#stroke-{theme})" stroke-width="2.5"/>',
        f'<text x="1042" y="191" text-anchor="middle" font-size="26" font-family="Arial,Helvetica,sans-serif" font-weight="800" fill="{p["text"]}">AI</text>',
        ]
    coords = [(1042,30),(1150,75),(1198,183),(1150,290),(1042,336),(934,290),(889,183),(934,75)]
    for i,(x,y) in enumerate(coords):
        c = p['accent'] if i%2 == 0 else p['purple']
        s.append(f'<circle cx="{x}" cy="{y}" r="{5 if i%2 else 7}" fill="{c}"/>')
    s += [
        f'<rect x="52" y="43" width="242" height="34" rx="17" fill="{p["surface"]}" stroke="{p["border"]}"/>',
        f'<circle cx="70" cy="60" r="5" fill="{p["accent"]}"/>',
        f'<text x="84" y="65" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="{p["muted"]}">ENGINEER / RESEARCHER</text>',
        f'<text x="50" y="151" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="54" fill="{p["text"]}">HABIB AHMAD</text>',
        f'<text x="51" y="216" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="62" fill="{p["accent"]}">GILLANI</text>',
        f'<text x="52" y="255" font-family="Arial,Helvetica,sans-serif" font-size="15" fill="{p["muted"]}">{esc(PROFILE["full_name"])}</text>',
        f'<path d="M52 284 H758" stroke="url(#stroke-{theme})" stroke-width="2" opacity=".75"/>',
        f'<text x="52" y="319" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" letter-spacing="1.6" fill="{p["text"]}">{esc(PROFILE["subtitle"])}</text>',
        f'<text x="52" y="345" font-family="Arial,Helvetica,sans-serif" font-size="12" fill="{p["muted"]}">Research-minded. Product-focused. Always building.</text>',
        '</svg>']
    return ''.join(s)


def card(project: dict, theme: str, idx: int) -> str:
    p=palette(theme)
    accent = project['accent'] if theme == "dark" else p['purple']
    # Preserve a strong per-project brand accent in both themes.
    if theme == "light":
        accent = ["#0376A8", "#7453C7", "#0B8279", "#B26C00", "#BE4262", "#167C56", "#7556AD", "#255DA5"][idx]
    title = project['title']
    subtitle = project['description']
    s = [svg_start(620,192,f"Project: {title}"),
         f'<rect x="1" y="1" width="618" height="190" rx="18" fill="{p["surface"]}" stroke="{p["border"]}" stroke-width="2"/>',
         f'<rect x="1" y="1" width="7" height="190" rx="3" fill="{accent}"/>',
         f'<circle cx="548" cy="53" r="57" fill="none" stroke="{accent}" opacity=".23" stroke-width="2"/>',
         f'<circle cx="548" cy="53" r="38" fill="none" stroke="{accent}" opacity=".43" stroke-width="2"/>',
         f'<path d="M500 53 H596 M548 5 V101 M515 20 L581 86 M515 86 L581 20" stroke="{accent}" opacity=".28"/>',
         f'<circle cx="548" cy="53" r="14" fill="{accent}" opacity=".9"/>',
         f'<text x="29" y="35" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="{accent}">{esc(project["category"])}</text>',
         f'<text x="29" y="75" font-family="Arial,Helvetica,sans-serif" font-size="26" font-weight="800" fill="{p["text"]}">{esc(title)}</text>',
         f'<text x="29" y="105" font-family="Arial,Helvetica,sans-serif" font-size="14" fill="{p["muted"]}">{esc(subtitle)}</text>',
        ]
    x = 29
    for t in project['tech']:
        w = max(48,len(t)*8+20)
        s.append(f'<rect x="{x}" y="134" rx="10" width="{w}" height="28" fill="{p["bg2"]}" stroke="{p["border"]}"/>')
        s.append(f'<text x="{x + w/2}" y="152" text-anchor="middle" font-size="12" font-family="Arial,Helvetica,sans-serif" fill="{p["text"]}">{esc(t)}</text>')
        x+=w+8
    s += [f'<text x="584" y="160" text-anchor="end" font-size="12" font-family="Arial,Helvetica,sans-serif" fill="{accent}">VIEW REPO  ↗</text>', '</svg>']
    return ''.join(s)


def terminal(theme: str) -> str:
    p=palette(theme)
    commands = [
      ("~/profile", "$ whoami", p['accent']),
      ("", "AI engineer · Python developer · MSc Artificial Intelligence", p['text']),
      ("~/focus", "$ currently_building", p['accent']),
      ("", "LLM applications  /  document AI  /  automation", p['text']),
      ("~/principles", "$ cat values.txt", p['accent']),
      ("", "clarity > complexity  |  evidence > hype  |  ship & learn", p['text']),
    ]
    s=[svg_start(1100,250,"Developer terminal profile"),
       f'<rect x="1" y="1" width="1098" height="248" rx="20" fill="{p["surface"]}" stroke="{p["border"]}" stroke-width="2"/>',
       f'<path d="M20 1 H1080 Q1099 1 1099 22 V51 H1 V22 Q1 1 20 1" fill="{p["bg2"]}"/>',
       *[f'<circle cx="{x}" cy="26" r="6" fill="{c}"/>' for x,c in [(25,"#FB7185"),(45,"#FBBF24"),(65,"#34D399")]],
       f'<text x="550" y="32" text-anchor="middle" font-size="12" font-family="Courier New,monospace" fill="{p["muted"]}">~/habib-ahmad/profile</text>']
    y=78
    for path,line,color in commands:
        if path:
            s.append(f'<text x="27" y="{y}" font-size="13" font-family="Courier New,monospace" fill="{p["purple"]}">{esc(path)}</text>')
            s.append(f'<text x="158" y="{y}" font-size="13" font-family="Courier New,monospace" font-weight="700" fill="{color}">{esc(line)}</text>')
        else:
            s.append(f'<text x="27" y="{y}" font-size="13" font-family="Courier New,monospace" fill="{color}">{esc(line)}</text>')
        y+=29
    s.append('</svg>')
    return ''.join(s)


def generate() -> dict[Path,str]:
    files={}
    for theme in ("dark","light"):
        files[ASSETS/f"hero-{theme}.svg"]=hero(theme)
        files[ASSETS/f"terminal-{theme}.svg"]=terminal(theme)
        for index,project in enumerate(PROFILE['projects']):
            files[ASSETS/'projects'/f"{project['slug']}-{theme}.svg"]=card(project,theme,index)
    return files


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Check that generated assets are up to date')
    args=parser.parse_args()
    generated=generate()
    bad=[]
    for path,content in generated.items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                bad.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding='utf-8')
    if bad:
        raise SystemExit('Assets need regeneration:\n'+'\n'.join(bad))
    print(f"{'Verified' if args.check else 'Generated'} {len(generated)} self-hosted SVG assets.")

if __name__=='__main__':
    main()
