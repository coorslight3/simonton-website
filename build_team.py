"""Generate team.html and one bio page per team member from site/team-data.js.

Run after editing site/team-data.js or the header/footer in site/index.html:
    PATH=$HOME/.local/node/bin:$PATH python3 build_team.py
"""
import html, json, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import market_robert
import about_page
import areas_content as ac
import broker_market
import market_john

SITE = Path(__file__).parent / 'site'
NODE = shutil.which('node') or str(Path.home() / '.local/node/bin/node')


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def load_team():
    out = subprocess.run(
        [NODE, '-e', "global.window={};require('./team-data.js');console.log(JSON.stringify(window.TEAM))"],
        cwd=SITE, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


e = html.escape
index = (SITE / 'index.html').read_text()

# Shared chrome copied from the home page so every page stays in sync.
top = index[index.index('<a class="skip"'):index.index('<main id="main">')]
_band_start = index.index('<section class="meet-band"')
_band = index[_band_start:index.index('</section>', _band_start) + len('</section>')]
bottom = _band + '\n\n' + index[index.index('<footer class="footer">'):index.index('<script src="closings-data.js">')]
CONTENT = Path(__file__).parent / 'content'  # sections that no longer live on the home page


PAGES = {'about': 'about.html', 'team': 'team.html', 'listings': 'listings.html',
         'closings': 'closings.html', 'testimonials': 'testimonials.html',
         '1031': None, 'exchanges': '1031-exchanges.html', 'blog': 'blog.html',
         'faqs': 'faqs.html', 'contact': 'contact.html'}


def fix_links(s):
    """In-page #anchors from the home page become links to the right page."""
    def repl(m):
        name = m.group(1)
        if name == 'subscribe':  # the footer form exists on every page
            return m.group(0)
        if name == 'top':
            return 'href="index.html"'
        if PAGES.get(name):
            return f'href="{PAGES[name]}"'
        return f'href="index.html#{name}"'
    return re.sub(r'href="#([A-Za-z0-9_-]+)"', repl, s)


top, bottom = fix_links(top), fix_links(bottom)


def page(title, desc, body, bodyclass='', scripts=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=50">
</head>
<body class="{bodyclass}">
{top}<main id="main">
{body}
</main>

{bottom}{scripts}<script src="script.js?v=50"></script>
</body>
</html>
'''


def card(p):
    return (f'<a class="member" href="team-{slug(p["name"])}.html">'
            f'<img src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" loading="lazy">'
            f'<span class="team-cap"><strong>{e(p["name"])}</strong><span>{e(p.get("short") or p["title"])}</span>'
            f'<em>View profile</em></span></a>')


team = load_team()

# Team page
grid = '\n'.join(card(p) for p in team)
(SITE / 'team.html').write_text(page(
    'Our Team | Simonton Commercial',
    'Meet the multifamily investment brokerage team at Simonton Commercial, RE/MAX One Commercial.',
    f'''<section class="section dark page-top">
  <div class="wrap">
    <p class="eyebrow">Simonton Commercial &middot; RE/MAX One Commercial</p>
    <h1 class="page-title">Meet the Team</h1>
    <div class="team">
{grid}
    </div>
  </div>
</section>''', 'subpage'))

# About page
def md(s):
    s = e(s)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


# about.html#t-<agentid> points the embedded map at that broker and scrolls to it.
MAP_DEEPLINK_JS = """<script>
(function(){
  var f = document.querySelector('.map-frame'); if (!f) return;
  var base = f.getAttribute('src').split('#')[0];
  function sync(){
    var m = /^#t-([a-z]{2})$/.exec(location.hash || ''); if (!m) return;
    f.src = base + '#' + m[1];
    var s = document.getElementById('coverage');
    if (s) s.scrollIntoView({behavior:'smooth', block:'start'});
  }
  sync();
  window.addEventListener('hashchange', sync);
})();
</script>"""


(SITE / 'about.html').write_text(page(
    about_page.TITLE, about_page.DESC,
    f"""<section class="section dark page-top">
  <div class="wrap">
    <p class="eyebrow">Simonton Commercial &middot; RE/MAX One Commercial</p>
    <h1 class="page-title">{e(about_page.HEADLINE)}</h1>
  </div>
</section>
<section class="section">
  <div class="wrap narrow about-body">
{''.join(f'    <p>{md(t)}</p>' for t in about_page.LEAD)}
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow about-body">
    <div class="head"><h2>{e(about_page.MODEL_HEAD)}</h2></div>
{''.join(f'    <p>{md(t)}</p>' for t in about_page.MODEL)}
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <div class="head"><h2>What that is worth to an owner</h2></div>
    <ul class="why">
{''.join(f'      <li><strong>{e(h)}</strong> {e(b)}</li>' for h, b in about_page.BENEFITS)}
    </ul>
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow about-body">
    <div class="head"><h2>{e(about_page.TEAM_HEAD)}</h2></div>
{''.join(f'    <p>{md(t)}</p>' for t in about_page.TEAM)}
  </div>
</section>
<section class="section" id="coverage">
  <div class="wrap">
    <div class="head"><h2>{e(about_page.MAP_HEAD)}</h2></div>
    <p class="about-body">{e(about_page.MAP_INTRO)}</p>
    <iframe class="map-frame" src="coverage-map.html" loading="lazy"
            title="Map of Simonton Commercial broker territories across Los Angeles County"></iframe>
    <div class="table-wrap" role="region" aria-label="Broker territories" tabindex="0">
      <table class="closed">
        <caption class="sr-only">Which broker covers which Los Angeles submarkets</caption>
        <thead><tr><th scope="col">Broker</th><th scope="col">Submarkets</th></tr></thead>
        <tbody>
{''.join(f'          <tr><th scope="row">{e(n)}</th><td>{e(a)}</td></tr>' for n, a in about_page.TERRITORIES)}
        </tbody>
      </table>
    </div>
    <p class="note">{e(about_page.MAP_NOTE)}</p>
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow about-body">
{''.join(f'    <p>{md(t)}</p>' for t in about_page.CLOSE)}
    <div class="about-cta">
      <a class="btn btn-dark" href="team.html">Meet the team</a>
      <a class="btn btn-ghost-dark" href="index.html#valuation">Request a free valuation</a>
    </div>
  </div>
</section>""", 'subpage', MAP_DEEPLINK_JS))


# One page per top-menu tab that has no page of its own yet. Each reuses the home page section's content.
def section_html(sec_id):
    saved = CONTENT / f'{sec_id}.html'
    if saved.exists():
        s = fix_links(saved.read_text())
    else:
        start = index.index(f'id="{sec_id}"')
        start = index.rindex('<section', 0, start)
        end = index.index('</section>', start) + len('</section>')
        s = fix_links(index[start:end])
    return re.sub(r'<h2>(.*?)</h2>', r'<h1 class="sec-h1">\1</h1>', s, count=1, flags=re.S)


TAB_PAGES = [
    ('listings.html', 'listings', 'Listings | Simonton Commercial',
     'Current multifamily listings from Simonton Commercial, RE/MAX One Commercial.', ''),
    ('closings.html', 'closings', 'Closings | Simonton Commercial',
     'Recent apartment building closings by the Simonton Commercial Group in Los Angeles.',
     '<script src="closings-data.js"></script>\n'),
    ('testimonials.html', 'testimonials', 'Testimonials | Simonton Commercial',
     'What clients say about working with Simonton Commercial.', ''),
    ('1031-exchanges.html', 'exchanges', '1031 Exchanges | Simonton Commercial',
     'Multifamily 1031 exchange guidance from Simonton Commercial, RE/MAX One Commercial.', ''),
    ('blog.html', 'blog', 'Blog | Simonton Commercial',
     'Los Angeles multifamily market updates and guides from Simonton Commercial.', ''),
    ('faqs.html', 'faqs', 'FAQs | Simonton Commercial',
     'Answers to common questions about selling and buying apartment buildings in Los Angeles.', ''),
    ('contact.html', 'contact', 'Contact | Simonton Commercial',
     'Contact Simonton Commercial at RE/MAX One Commercial in Santa Monica.', ''),
]

# Three-stage process, shown on the 1031 Exchanges page only.
STAGES = [
    ('Stage 1', 'Premarketing', [
        ('Finalize the Offering Memorandum with our marketing team at RE/MAX One Commercial.',
         ['Property Photos', 'Design Layout', 'Highlight the Asset', 'Location Overview']),
        ('Prepare postcard and send out mailer to local apartment owners in Hollywood.', []),
        ('Email campaign to over 3,000 preferred investors in our company database.', []),
        ('Entire team will call our proprietary database of investors that own and purchase in Santa Monica.', []),
        ('RE/MAX One Commercial will present your listing to all RE/MAX agents on our weekly company \u201cdeal share\u201d conference call.', []),
    ]),
    ('Stage 2', 'Marketing Campaign Launch', [
        ('Upload the Offering Memorandum and information into all major real estate websites:',
         ['theMLS.com', 'Loopnet/Costar', 'ApartmentBuildings.com', 'Realtor.com', 'Zillow', 'Redfin', 'Trulia', 'Crexi', 'RE/MAX company website']),
        ('Cold Call local owners who have purchased properties in the last 4 years.', []),
        ('Cold Call owners who recently sold property in the past 6 months to verify if they are in 1031 Exchanges.', []),
        ('Cold Call apartment owners on Ocean Park Blvd and other neighboring streets in Santa Monica.', []),
        ('Personalized direct email to cooperating brokers who closed transactions in Santa Monica.', []),
    ]),
    ('Stage 3', 'Negotiations & Close', [
        ('As we receive offers, we will orchestrate a bidding atmosphere that will create competition and allow us to obtain the highest price and best terms.',
         ['Counter Offers', 'Multiple Counter Offers', 'Acceptance']),
        ('Send out final email campaign to all interested parties alerting them that offers are being presented.', []),
        ('Accept best offer and retain qualified Buyers in backup position.', []),
        ('Inspect property, provide due diligence, and remove contingencies.', []),
        ('Close escrow.', []),
    ]),
]


def process_html():
    cols = ''
    for i, (n, name, items) in enumerate(STAGES, 1):
        lis = ''
        for text, subs in items:
            if subs:
                tag = 'chips' if len(subs) > 4 else 'checks'
                sub = f'<ul class="{tag}">' + ''.join(f'<li>{e(s)}</li>' for s in subs) + '</ul>'
            else:
                sub = ''
            lis += f'<li><p>{e(text)}</p>{sub}</li>'
        cols += (f'<article class="stage"><header><span class="stage-num" aria-hidden="true">0{i}</span>'
                 f'<p class="stage-label">{n}</p><h3>{e(name)}</h3></header>'
                 f'<ol class="steps-line">{lis}</ol></article>')
    return f'''<section class="section dark" id="process">
  <div class="wrap">
    <p class="eyebrow">How we sell your building</p>
    <h2 class="proc-title">Our Process</h2>
    <div class="stages">{cols}</div>
  </div>
</section>'''


def contact_team_html():
    cards = ''
    for i, p in enumerate(team, 1):
        rows = ''
        if p.get('email'):
            rows += f'<div><dt>Email</dt><dd><a href="mailto:{e(p["email"])}">{e(p["email"])}</a></dd></div>'
        if p.get('phone'):
            digits = re.sub(r'\D', '', p['phone'])
            rows += f'<div><dt>Direct</dt><dd><a href="tel:+1{digits}">{e(p["phone"])}</a></dd></div>'
        if p.get('dre'):
            rows += f'<div><dt>DRE</dt><dd>#{e(p["dre"])}</dd></div>'
        cards += (f'<article class="ft-card" style="--i:{i}">'
                  f'<div class="ft-top"><span>// {i:02d}</span><span>RE/MAX ONE COMMERCIAL</span></div>'
                  f'<div class="ft-photo"><img src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" loading="lazy"><span class="ft-scan" aria-hidden="true"></span></div>'
                  f'<h3 class="ft-name">{e(p["name"])}</h3>'
                  f'<p class="ft-role">{e((p.get("short") or p["title"]).upper())}</p>'
                  f'<dl class="ft-data">{rows}</dl>'
                  f'<a class="ft-link" href="team-{slug(p["name"])}.html">View profile <span aria-hidden="true">&rarr;</span></a></article>')
    return f'''<section class="ft" id="team-contacts">
  <div class="wrap">
    <p class="ft-eyebrow">// TEAM DIRECTORY</p>
    <h2 class="ft-title">Contact Our Team</h2>
    <p class="ft-sub">Nine brokers. Reach any of us directly.</p>
    <div class="ft-grid">{cards}</div>
  </div>
</section>'''


for fname, sec, title, desc, extra in TAB_PAGES:
    if sec == 'contact':
        # Team cards first, then the dark contact form block.
        team_part = contact_team_html().replace('<h2 class="ft-title">', '<h1 class="ft-title">').replace('Contact Our Team</h2>', 'Contact Our Team</h1>')
        form_part = section_html(sec).replace('<h1 class="sec-h1">Contact</h1>', '<h2>Contact</h2>')
        body = team_part + form_part
    else:
        body = section_html(sec) + (process_html() if sec == 'exchanges' else '')
    (SITE / fname).write_text(page(title, desc, body, 'subpage', extra))

# One page per person
for p in team:
    s = slug(p['name'])
    contact = []
    if p.get('phone'):
        digits = re.sub(r'\D', '', p['phone'])
        contact.append(f'<a href="tel:+1{digits}">{e(p["phone"])}</a>')
    if p.get('email'):
        contact.append(f'<a href="mailto:{e(p["email"])}">{e(p["email"])}</a>')
    if p.get('handle'):
        contact.append(f'<span>{e(p["handle"])}</span>')
    if p.get('dre'):
        contact.append(f'<span>DRE #{e(p["dre"])}</span>')
    paras = ''.join(f'<p>{e(t)}</p>' for t in p.get('bio', [])) or '<p class="note">Full bio coming soon.</p>'
    others = '\n'.join(card(o) for o in team if o['name'] != p['name'])
    market_link = (f'<p><a class="link" href="{e(p["page"])}">{e(p["pageLabel"])} &rarr;</a></p>' if p.get('page') else '')
    # Button through to this broker's territory on the About Us coverage map.
    _ma = about_page.MAP_AGENTS.get(p['name'])
    if _ma and _ma[1]:
        _lbl = (about_page.MAP_LABEL_COUNTYWIDE if p['name'] in about_page.COUNTYWIDE
                else about_page.MAP_LABEL).format(first=p['name'].split()[0])
        territory_link = (f'<p class="person-territory">'
                          f'<a class="btn btn-ghost-dark" href="about.html#t-{_ma[0]}">{e(_lbl)}'
                          f' <span aria-hidden="true">&rarr;</span></a></p>')
    else:
        territory_link = ''
    # Robert's market content sits on his profile itself instead of behind a link
    market = market_robert.sections('', profile=True) if p['name'] == 'Robert Carlile' else ''
    if market:
        market_link = ''
    if market:
        # compact top so the closings table shows on first load; the bio moves below it
        body = f'''<section class="section person person-compact">
  <div class="wrap">
    <a class="back" href="team.html">&larr; All team members</a>
    <div class="person-grid">
      <img class="person-photo" src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" width="560" height="700">
      <div class="person-text">
        <h1>{e(p["name"])}</h1>
        <p class="person-title">{e(p["title"])}</p>
        <p class="person-contact">{''.join(contact)}</p>
        {territory_link}
      </div>
    </div>
    <div class="person-split">
      <div class="person-closings" id="closings">
      {market_robert.closings_table()}
      </div>
      <div class="person-bio bio-long"><h2>About {e(p["name"])}</h2>{paras}</div>
    </div>
  </div>
</section>
{market}<section class="section dark">
  <div class="wrap">
    <h2>More from the team</h2>
    <div class="team">
{others}
    </div>
  </div>
</section>'''
    else:
        body = f'''<section class="section person">
  <div class="wrap">
    <a class="back" href="team.html">&larr; All team members</a>
    <div class="person-grid">
      <img class="person-photo" src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" width="560" height="700">
      <div class="person-text">
        <h1>{e(p["name"])}</h1>
        <p class="person-title">{e(p["title"])}</p>
        <p class="person-contact">{''.join(contact)}</p>
        {paras}
        {market_link}
        {territory_link}
      </div>
    </div>
  </div>
</section>
<section class="section dark">
  <div class="wrap">
    <h2>More from the team</h2>
    <div class="team">
{others}
    </div>
  </div>
</section>'''
    (SITE / f'team-{s}.html').write_text(page(
        f'{p["name"]} | Simonton Commercial',
        f'{p["name"]}, {p["title"]} at Simonton Commercial, RE/MAX One Commercial.',
        body, 'subpage'))


# ---- Areas Served pages ------------------------------------------------------------------------------
def trim(text, n=155):
    if len(text) <= n:
        return text
    return text[:n].rsplit(' ', 1)[0].rstrip(',;:') + '\u2026'


def area_form(subject):
    return f'''<form class="form on-dark" action="#" method="post" data-form data-subject="New valuation request ({e(subject)} page)"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <div class="field"><label for="a-name">Full name</label><input id="a-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="a-email">Email</label><input id="a-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="a-phone">Phone</label><input id="a-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="a-addr">Property address</label><input id="a-addr" name="address" required></div>
      <div class="field"><label for="a-units">Number of units</label><input id="a-units" name="units" inputmode="numeric"></div>
      <button class="btn btn-light" type="submit">Request free valuation</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>'''


def valuation_block(heading, paras, subject):
    body = ''.join(f'<p>{e(t)}</p>' for t in paras)
    return (f'<section class="section dark" id="valuation"><div class="wrap split"><div><h2>{e(heading)}</h2>'
            f'<div class="area-copy">{body}</div></div>{area_form(subject)}</div></section>')


def other_areas(current):
    links = ''.join(f'<li><a href="{ac.filename(s)}"{" aria-current=page" if s == current else ""}>{e(l)}</a></li>'
                    for s, l in ac.ORDER if s != current)
    return f'<section class="section alt"><div class="wrap"><h2>Other Areas We Serve</h2><ul class="area-chips">{links}</ul></div></section>'


def area_hero(h1, eyebrow, intro=''):
    sub = f'<p class="mk-sub">{e(intro)}</p>' if intro else ''
    return (f'<section class="mk-hero area-hero"><div class="wrap"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1>{sub}'
            f'<div class="hero-actions"><a class="btn btn-light" href="#valuation">Get a free valuation</a>'
            f'<a class="btn btn-ghost" href="contact.html">Contact the team</a></div></div></section>')


def paras_html(paras):
    return ''.join(f'<p>{e(t)}</p>' for t in paras)


# Full market pages
for a in ac.FULL:
    n = a['name']
    tiles = ''.join(
        f'<div class="ind"><span class="ind-l">{e(l)}</span><strong>{e(v)}</strong>'
        + (f'<small>{e(note)}</small>' if note else '') + '</div>' for l, v, note in a['indicators'])
    body = (area_hero(f'{n} Multifamily Broker', 'RE/MAX One Commercial', a['intro'])
            + f'<section class="section"><div class="wrap narrow about-body"><h2>{e(n)} Multifamily Market Snapshot</h2>{paras_html(a["snapshot"])}</div></section>'
            + f'<section class="section alt"><div class="wrap"><h2>{e(n)} Multifamily Market Indicators</h2><div class="ind-grid">{tiles}</div><p class="disclaimer">{e(a["note"])}</p></div></section>'
            + valuation_block(f'What Is My {n} Apartment Building Worth?', a['worth'], n)
            )
    (SITE / ac.filename(a['slug'])).write_text(page(
        f'{n} Multifamily Broker | RE/MAX One Commercial', trim(a['intro']), body, 'subpage'))

# San Fernando Valley
v = ac.VALLEY
cards = ''.join(f'<article class="hood"><h3>{e(n)}</h3><p>{e(t)}</p></article>' for n, t in v['hoods'])
body = (area_hero(v['h1'], 'RE/MAX One Commercial')
        + f'<section class="section"><div class="wrap narrow about-body">{paras_html([v["intro"]] + v["paras"])}</div></section>'
        + f'<section class="section alt"><div class="wrap"><h2>Valley Neighborhoods</h2><div class="hood-grid">{cards}</div></div></section>'
        + valuation_block('What Is My Valley Apartment Building Worth?',
                          ['Request a free, confidential valuation for your San Fernando Valley apartment building from the RE/MAX One Commercial multifamily team.'],
                          v['name'])
        )
(SITE / ac.filename(v['slug'])).write_text(page(
    f'{v["h1"]} | RE/MAX One Commercial', trim(v['intro']), body, 'subpage'))

# Neighborhood pages
for h in ac.HOODS:
    body = (area_hero(h['name'], (f'ZIP {h["zip"]} \u00b7 ' if h.get('zip') else '') + 'Multifamily Broker')
            + f'<section class="section"><div class="wrap narrow about-body">{paras_html(h["paras"])}</div></section>'
            + valuation_block(f'What Is My {h["label"]} Apartment Building Worth?',
                              [f'Request a free, confidential valuation for your {h["label"]} apartment building from the RE/MAX One Commercial multifamily team.'],
                              h['label'])
            )
    (SITE / ac.filename(h['slug'])).write_text(page(
        f'{h["name"]} Multifamily Broker | RE/MAX One Commercial', trim(h['paras'][0]), body, 'subpage'))

# Placeholder pages for areas with no text yet
for slug_, label in ac.PLACEHOLDERS:
    body = (area_hero(f'{label} Multifamily Broker', 'RE/MAX One Commercial')
            + f'<section class="section"><div class="wrap narrow about-body"><p>Detailed {e(label)} market information is coming soon. In the meantime, request a free, confidential valuation for your apartment building below.</p></div></section>'
            + valuation_block(f'What Is My {label} Apartment Building Worth?',
                              [f'Request a free, confidential valuation for your {label} apartment building from the RE/MAX One Commercial multifamily team.'],
                              label)
            )
    (SITE / ac.filename(slug_)).write_text(page(
        f'{label} Multifamily Broker | RE/MAX One Commercial',
        f'{label} multifamily broker: free apartment building valuations from RE/MAX One Commercial.', body, 'subpage'))

# Robert Carlile's SEO market page, served at /apartment-broker/palms-mar-vista-mid-city/
out = SITE / market_robert.PATH
out.mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(market_robert.render(top, bottom))

# John Sarna's market page (same style as Robert's), with the version stamp used by the other pages.
_john = next(p for p in team if p['name'] == 'John Sarna')
_out = SITE / market_john.PATH
_out.mkdir(parents=True, exist_ok=True)
_ver = re.search(r'styles\.css\?v=(\d+)', index).group(1)
(_out / 'index.html').write_text(broker_market.render(market_john, _john, top, bottom).replace('__V__', _ver))

print('Generated tab pages, team.html,', len(team), 'profile pages and the Palms/Mar Vista/Mid City page')
