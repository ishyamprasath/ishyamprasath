#!/usr/bin/env python3
"""Generate GitHub-safe, dependency-free profile artwork from public data."""

import argparse
import base64
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
from math import hypot
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "dark": dict(bg="#090e1a", panel="#101a2b", line="#26364b", text="#edf4ff",
                 muted="#a3b4cd", dim="#7086a5", accent="#66e5d3", violet="#b6a0ff",
                 levels=["#19273b", "#20574f", "#2d8878", "#44baa2", "#66e5d3"]),
    "light": dict(bg="#f5f7fc", panel="#ffffff", line="#d7dfed", text="#14233a",
                  muted="#435b79", dim="#5c718d", accent="#087e70", violet="#6b46c1",
                  levels=["#e4eaf3", "#b6dfd4", "#76bda9", "#32917e", "#087e70"]),
}


def text(x, y, value, size=16, color="text", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{escape(color)}" '
            f'{extra}>{escape(str(value))}</text>')


def label(x, y, value, c, size=11):
    return text(x, y, value, size, c, 'font-family="monospace" letter-spacing="1.5"')


def start(height, title, c, width=1180):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title" '
            'font-family="DejaVu Sans,Arial,sans-serif">',
            f'<title id="title">{escape(title)}</title>',
            '<defs><linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">'
            f'<stop stop-color="{c["accent"]}"/><stop offset=".48" stop-color="{c["violet"]}"/>'
            '<stop offset="1" stop-color="#edbd70"/></linearGradient>'
            '<linearGradient id="sheen"><stop stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".16"/>'
            '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">'
            f'<path d="M36 0H0V36" fill="none" stroke="{c["line"]}" stroke-width=".6"/>'
            '</pattern></defs>',
            '<style>.pulse{animation:pulse 3s ease-in-out infinite}'
            '.id-card{transform-origin:260px 390px;animation:cardFloat 9s ease-in-out infinite}'
            '.shine{animation:shine 7s ease-in-out infinite}'
            '.edge{stroke-dasharray:80 1000;animation:edge 12s linear infinite}'
            '.project{animation:levitate 7s ease-in-out infinite;animation-delay:var(--delay,0s)}'
            '.circuit{stroke-dasharray:12 140;animation:circuit 9s linear infinite}'
            '.orbit{transform-origin:260px 337px;animation:orbit 32s linear infinite}'
            '.cursor{animation:blink 1.2s steps(1) infinite}'
            '.phase-a{animation:phaseA 12s infinite}'
            '.phase-b{opacity:0;animation:phaseB 12s infinite}'
            '.phase-c{opacity:0;animation:phaseC 12s infinite}'
            '@keyframes cardFloat{0%,100%{transform:perspective(1100px) rotateY(-9deg) rotateX(5deg) rotateZ(-2deg) translateY(-5px)}'
            '50%{transform:perspective(1100px) rotateY(9deg) rotateX(-4deg) rotateZ(2deg) translateY(7px)}}'
            '@keyframes shine{0%,20%{transform:translateX(-500px)}70%,100%{transform:translateX(900px)}}'
            '@keyframes edge{to{stroke-dashoffset:-2160}}'
            '@keyframes circuit{to{stroke-dashoffset:-608}}'
            '@keyframes orbit{to{transform:rotate(360deg)}}'
            '@keyframes pulse{50%{opacity:.3}}'
            '@keyframes blink{50%{opacity:0}}'
            '@keyframes levitate{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}'
            '@keyframes phaseA{0%,28%,100%{opacity:1}33%,95%{opacity:0}}'
            '@keyframes phaseB{0%,28%,66%,100%{opacity:0}33%,61%{opacity:1}}'
            '@keyframes phaseC{0%,61%,100%{opacity:0}66%,95%{opacity:1}}'
            '@keyframes travel{from{stroke-dashoffset:var(--start)}to{stroke-dashoffset:var(--end)}}'
            '@media(prefers-reduced-motion:reduce){*{animation:none!important}'
            '.snake{display:none}}</style>',
            f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" '
            f'fill="{c["bg"]}" stroke="{c["line"]}"/>']


def hero(profile, c, mobile=False):
    portrait = base64.b64encode((ROOT/'assets/portrait.png').read_bytes()).decode('ascii')
    first, _, last = profile['name'].partition(' ')
    s = start(760, f'{profile["name"]} — animated developer ID, AI and full-stack engineering', c,
              width=520 if mobile else 1180)
    s += ['<defs><clipPath id="photo"><rect x="102" y="184" width="316" height="278" rx="12"/></clipPath>'
          '<clipPath id="card"><rect x="80" y="122" width="360" height="536" rx="20"/></clipPath>'
          '<linearGradient id="photoFade" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset=".6" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
          '<mask id="portraitFade"><rect x="102" y="180" width="316" height="300" fill="url(#photoFade)"/></mask></defs>',
          '<rect x="3" y="62" width="1174" height="636" fill="url(#grid)" opacity=".22"/>',
          label(36, 36, 'SP / DIGITAL IDENTITY', c['muted']),
          f'<circle class="pulse" cx="893" cy="31" r="4" fill="{c["accent"]}"/>',
          label(908, 36, 'ALWAYS BUILDING SOMETHING', c['accent']),
          f'<path d="M1 60H1179M1 699H1179" stroke="{c["line"]}"/>',
          f'<ellipse class="pulse" cx="260" cy="670" rx="145" ry="13" fill="{c["violet"]}" opacity=".12"/>',
          f'<path class="circuit" d="M36 240H60V110H460V635H484" fill="none" stroke="{c["accent"]}" opacity=".3"/>',
          '<g class="id-card">',
          '<path d="M211 62L245 137M307 62L275 137" fill="none" stroke="#c5914c" stroke-width="18"/>',
          '<path d="M211 62L245 137M307 62L275 137" fill="none" stroke="#f0c67e" stroke-width="2" stroke-dasharray="2 5"/>',
          f'<rect x="86" y="130" width="360" height="536" rx="20" fill="{c["line"]}" opacity=".5"/>',
          f'<rect x="80" y="122" width="360" height="536" rx="20" fill="{c["panel"]}" stroke="url(#holo)" stroke-width="1.5"/>',
          '<rect class="edge" x="80" y="122" width="360" height="536" rx="20" fill="none" stroke="#e9bd75" stroke-width="2.5"/>',
          f'<rect x="229" y="134" width="62" height="8" rx="4" fill="{c["bg"]}"/>',
          label(102, 168, 'DEVELOPER / ALL ACCESS', c['muted'], 10),
          text(402, 169, 'SP', 15, c['accent'], 'font-weight="700" text-anchor="end"'),
          '<g clip-path="url(#photo)">',
          f'<rect x="102" y="184" width="316" height="278" fill="{c["bg"]}"/>',
          f'<circle cx="260" cy="325" r="114" fill="none" stroke="{c["line"]}" stroke-width="30"/>',
          f'<circle cx="260" cy="325" r="130" fill="none" stroke="{c["accent"]}" opacity=".3"/>',
          f'<path class="circuit" d="M102 215H418M102 445H418" stroke="{c["violet"]}" fill="none" opacity=".6"/>',
          f'<image href="data:image/png;base64,{portrait}" x="83" y="174" width="354" height="354" '
          'preserveAspectRatio="xMidYMin meet" mask="url(#portraitFade)"/>',
          '</g>',
          f'<path d="M112 204H128M112 204V220M408 204H392M408 204V220M112 444H128M112 444V428M408 444H392M408 444V428" '
          f'stroke="{c["accent"]}" stroke-width="2" fill="none"/>',
          text(102, 496, profile['name'], 26, c['text'], 'font-weight="700" letter-spacing="-.6"'),
          text(102, 524, 'AI & FULL-STACK ENGINEER', 12, c['violet'], 'letter-spacing="1.2"'),
          text(102, 551, '@' + profile['username'], 13, c['muted'], 'font-family="monospace"'),
          f'<path d="M102 572H418" stroke="{c["line"]}"/>']
    # Decorative barcode, deliberately not an official credential or scannable identity.
    for i in range(45):
        x = 103+i*4
        s.append(f'<rect x="{x}" y="589" width="{1 if i % 3 else 2}" height="26" fill="{c["muted"]}" opacity=".6"/>')
    s += [label(102, 638, 'COIMBATORE / INDIA', c['dim'], 9),
          f'<circle class="pulse" cx="344" cy="600" r="4" fill="{c["accent"]}"/>',
          label(355, 605, 'BUILD', c['accent'], 9),
          '<g clip-path="url(#card)"><rect class="shine" x="-200" y="110" width="200" height="600" '
          'fill="url(#sheen)" transform="skewX(-15)"/></g>',
          '</g>',
          '<g display="none">' if mobile else '<g>',
          label(512, 109, '01 / HUMAN IDEAS. USEFUL AI.', c['accent']),
          text(508, 181, first.upper(), 66, c['text'], 'font-weight="800" letter-spacing="-2"'),
          text(508, 251, last.upper(), 66, c['text'], 'font-weight="800" letter-spacing="-2"'),
          text(512, 292, 'AI & Full-Stack Engineer', 23, c['violet']),
          text(512, 346, 'Ideas become agents.', 25, c['text']),
          text(512, 381, 'Agents become useful systems.', 25, c['text']),
          f'<rect x="512" y="414" width="622" height="146" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>',
          text(534, 447, '$ ./shyam --build', 14, c['accent'], 'font-family="monospace"'),
          '<g class="phase-a">' + text(534, 482, 'Multi-agent systems + contextual RAG', 16, c['text'], 'font-family="monospace"') + '</g>',
          '<g class="phase-b">' + text(534, 482, 'Computer vision + autonomous robotics', 16, c['text'], 'font-family="monospace"') + '</g>',
          '<g class="phase-c">' + text(534, 482, 'Mobile experiences + cloud-native apps', 16, c['text'], 'font-family="monospace"') + '</g>',
          text(534, 533, 'Python · FastAPI · React Native · Azure · AWS', 13, c['muted']),
          f'<rect class="cursor" x="1098" y="470" width="8" height="15" fill="{c["accent"]}"/>',
          label(512, 605, 'LEARNING / SHIPPING / REPEATING', c['accent'], 10),
          text(512, 635, 'SKCT · CSE (AI & ML) · 2024–2028', 15, c['muted']),
          text(512, 662, 'IIT Guwahati · Micro Credit Program in CS · Completed', 13, c['muted']),
          '</g>',
          label(36, 736, 'DESIGN. CODE. DEPLOY. REPEAT.', c['muted']),
          label(923, 736, '@' + profile['username'], c['accent']), '</svg>']
    return '\n'.join(s)


def projects(profile, c):
    s = start(830, 'Selected projects by ' + profile['name'], c)
    s += [label(36, 38, 'SELECTED WORK / 2024–2026', c['accent']),
          text(36, 82, 'From experiments to useful systems.', 28, c['text'], 'font-weight="700"')]
    for i, project in enumerate(profile['projects']):
        x, y = 30 + i % 2 * 566, 110 + i // 2 * 230
        accent = c['accent'] if i % 2 == 0 else c['violet']
        s += [f'<g class="project" style="--delay:-{i*1.1}s">',
              f'<rect x="{x}" y="{y}" width="554" height="212" rx="14" '
              f'fill="{c["panel"]}" stroke="{c["line"]}"/>',
              f'<path class="circuit" d="M{x+22} {y+1}H{x+532}" fill="none" stroke="{accent}" opacity=".7"/>',
              label(x+22, y+30, project['category'], accent, 10),
              text(x+22, y+66, project['name'], 25, c['text'], 'font-weight="700"')]
        for j, line in enumerate(project['lines']):
            s.append(text(x+22, y+99+j*22, line, 16, c['muted']))
        s += [text(x+22, y+157, project['stack'], 12, accent, 'font-family="monospace"'),
              f'<path d="M{x+22} {y+173}H{x+532}" stroke="{c["line"]}"/>',
              text(x+22, y+195, project['context'], 12, c['dim']), '</g>']
    s += [label(36, 812, 'BUILT WITH CURIOSITY. GROUNDED IN REAL PROBLEMS.', c['muted']), '</svg>']
    return '\n'.join(s)


def toolkit(profile, c):
    s = start(350, 'Engineering toolkit — AI, applications, cloud, and robotics', c)
    s += [label(36, 38, 'TOOLKIT / CONNECTED BY CURIOSITY', c['accent']),
          text(36, 83, 'Different tools. One builder.', 28, c['text'], 'font-weight="700"')]
    groups = [
        ('01 / INTELLIGENCE', ['Google ADK · LangGraph', 'CrewAI · RAG · n8n', 'TensorFlow · YOLO', 'Pinecone · ChromaDB']),
        ('02 / EXPERIENCES', ['Python · Java', 'FastAPI · Spring Boot', 'React · Next.js', 'React Native']),
        ('03 / INFRASTRUCTURE', ['Azure · GCP · AWS', 'Docker · Kubernetes', 'CI/CD · Linux', 'PostgreSQL · MongoDB']),
        ('04 / PHYSICAL WORLD', ['ROS 2 Jazzy', 'OpenCV · ONNX', 'NVIDIA Jetson Nano', 'Edge AI · Robotics']),
    ]
    for i, (title, lines) in enumerate(groups):
        x = 30+i*282
        accent = c['accent'] if i % 2 == 0 else c['violet']
        s += [f'<g class="project" style="--delay:-{i*1.5}s">',
              f'<rect x="{x}" y="112" width="274" height="190" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>',
              label(x+18, 141, title, accent, 9)]
        for j, line in enumerate(lines):
            s.append(text(x+18, 174+j*30, line, 14, c['muted']))
        s += [f'<circle class="pulse" cx="{x+245}" cy="136" r="3" fill="{accent}"/>', '</g>']
    s += ['<path class="circuit" d="M36 326H1144" fill="none" stroke="url(#holo)" stroke-width="2"/>', '</svg>']
    return '\n'.join(s)


class CalendarParser(HTMLParser):
    """Join GitHub's dated calendar cells with their count tooltips by id."""

    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.tip_id = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip':
            self.tip_id = a.get('for')
            if self.tip_id:
                self.tips[self.tip_id] = ''

    def handle_data(self, data):
        if self.tip_id:
            self.tips[self.tip_id] += data

    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.tip_id = None

    def days(self):
        days = []
        for key, cell in self.cells.items():
            tip = self.tips.get(key, '').strip()
            match = re.match(r'(No|[\d,]+) contributions? on\b', tip)
            if not match:
                raise ValueError(f'Cannot read contribution count for {cell["date"]}')
            count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
            days.append(dict(cell, count=count))
        return sorted(days, key=lambda d: d['date'])


def validate_days(days):
    if not days:
        raise ValueError('Contribution calendar is empty')
    previous = None
    for day in days:
        current = date.fromisoformat(day['date'])
        if previous is not None and current != previous + timedelta(days=1):
            raise ValueError('Contribution dates must be unique and consecutive')
        if type(day['count']) is not int or day['count'] < 0 or day['level'] not in range(5):
            raise ValueError('Invalid contribution count or level')
        if (day['count'] == 0) != (day['level'] == 0):
            raise ValueError('Contribution count and level disagree')
        previous = current


def refresh(username):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}', username):
        raise ValueError('Invalid GitHub username')
    request = urllib.request.Request(
        f'https://github.com/users/{username}/contributions',
        headers={'User-Agent': 'GitHub-profile-artwork', 'Accept': 'text/html'})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode('utf-8')
    parser = CalendarParser()
    parser.feed(html)
    days = parser.days()
    validate_days(days)
    today = datetime.now(timezone.utc).date()
    if not 365 <= len(days) <= 372:
        raise ValueError(f'Expected a full contribution year, got {len(days)} days')
    if not today - timedelta(days=1) <= date.fromisoformat(days[-1]['date']) <= today:
        raise ValueError('GitHub returned an outdated or future calendar')
    return {'username': username, 'updated': today.isoformat(), 'days': days}


def metrics(days):
    streak = longest = 0
    for day in days:
        streak = streak + 1 if day['count'] else 0
        longest = max(longest, streak)
    return sum(d['count'] for d in days), sum(d['count'] > 0 for d in days), longest


def activity(snapshot, c):
    days = snapshot['days']
    validate_days(days)
    total, active, longest = metrics(days)
    s = start(410, f'Public contribution activity for {snapshot["username"]}, updated {snapshot["updated"]}', c)
    s += [label(36, 38, 'GITHUB / CONTRIBUTION PLAYGROUND', c['accent']),
          label(842, 38, 'SNAPSHOT / ' + snapshot['updated'], c['muted'])]
    for x, value, title in [(36, total, 'CONTRIBUTIONS'), (390, active, 'ACTIVE DAYS'), (744, longest, 'LONGEST STREAK / DAYS')]:
        s += [text(x, 98, f'{value:,}', 38, c['text'], 'font-weight="700"'),
              label(x, 124, title, c['muted'])]
    first = date.fromisoformat(days[0]['date'])
    # Sunday is row zero, as in GitHub's contribution calendar.
    origin = first - timedelta(days=(first.weekday()+1) % 7)
    positions = []
    for day in days:
        offset = (date.fromisoformat(day['date']) - origin).days
        week, row = divmod(offset, 7)
        x, y = 64+week*20, 177+row*20
        positions.append((week, row, x+7, y+7))
        s.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" '
                 f'fill="{c["levels"][day["level"]]}"><title>{day["date"]}: '
                 f'{day["count"]} contributions</title></rect>')
    for row, name in [(1, 'M'), (3, 'W'), (5, 'F')]:
        s.append(text(36, 188+row*20, name, 11, c['dim']))
    positions.sort(key=lambda p: (p[0], p[1] if p[0] % 2 == 0 else -p[1]))
    path = 'M' + ' L'.join(f'{p[2]},{p[3]}' for p in positions)
    length = sum(hypot(b[2]-a[2], b[3]-a[3]) for a, b in zip(positions, positions[1:]))
    tail = length * .018
    s.append(f'<path class="snake" d="{path}" fill="none" '
             f'stroke="{c["violet"]}" stroke-width="10" stroke-linecap="round" '
             f'stroke-linejoin="round" stroke-dasharray="{tail:.2f} {length+tail:.2f}" '
             f'style="--start:{tail:.2f};--end:{-length:.2f};animation:travel 32s linear infinite"/>')
    s += [text(64, 350, days[0]['date'] + ' → ' + days[-1]['date'], 12, c['muted']),
          text(889, 350, 'Less', 11, c['muted']), text(1074, 350, 'More', 11, c['muted'])]
    for i, color in enumerate(c['levels']):
        s.append(f'<rect x="{930+i*26}" y="338" width="16" height="16" rx="3" fill="{color}"/>')
    s += [label(36, 390, 'REAL GITHUB ACTIVITY. A LITTLE PLAY.', c['muted']),
          label(822, 390, 'REFRESHED BY GITHUB ACTIONS', c['muted']), '</svg>']
    return '\n'.join(s)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Fetch the public GitHub contribution calendar')
    args = parser.parse_args()
    profile = json.loads((ROOT/'profile/profile.json').read_text())
    snapshot_path = ROOT/'profile/contributions.json'
    snapshot = refresh(profile['username']) if args.refresh else json.loads(snapshot_path.read_text())
    if snapshot['username'] != profile['username']:
        raise ValueError('Contribution snapshot belongs to another account; run with --refresh')
    validate_days(snapshot['days'])
    # Render everything before writing; failed refreshes retain the previous artwork.
    output = {}
    for theme, colors in THEMES.items():
        output[f'hero-{theme}.svg'] = hero(profile, colors)
        output[f'hero-mobile-{theme}.svg'] = hero(profile, colors, mobile=True)
        output[f'projects-{theme}.svg'] = projects(profile, colors)
        output[f'toolkit-{theme}.svg'] = toolkit(profile, colors)
        output[f'activity-{theme}.svg'] = activity(snapshot, colors)
    assets = ROOT/'assets'
    assets.mkdir(exist_ok=True)
    for filename, svg in output.items():
        (assets/filename).write_text(svg+'\n', encoding='utf-8')
    if args.refresh:
        snapshot_path.write_text(json.dumps(snapshot, indent=2)+'\n')
    print(f'Generated {len(output)} SVGs; activity snapshot: {snapshot["updated"]}')


if __name__ == '__main__':
    main()
