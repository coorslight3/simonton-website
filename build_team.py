"""Generate team.html and one bio page per team member from site/team-data.js.

Run after editing site/team-data.js or the header/footer in site/index.html:
    PATH=$HOME/.local/node/bin:$PATH python3 build_team.py
"""
import datetime, html, json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import market_robert
import market_mike
import area_comps
import about_page
import blog_posts
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
bottom = index[index.index('<footer class="footer">'):index.index('<script src="closings-data.js">')]
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
<link rel="stylesheet" href="styles.css?v=77">
</head>
<body class="{bodyclass}">
{top}<main id="main">
{body}
</main>

{bottom}{scripts}<script src="script.js?v=77"></script>
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


def post_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d:%B} {d.day}, {d.year}'


def post_file(post):
    return f'blog-{post["slug"]}.html'


def post_body_html(post):
    """A post's blocks: paragraphs, subheadings, a left-ruled emphasis line and lists."""
    out = ''
    for b in post['body']:
        if isinstance(b, str):
            out += f'    <p>{md(b)}</p>\n'
            continue
        kind, val = b
        if kind == 'h2':
            out += f'    <h2>{e(val)}</h2>\n'
        elif kind == 'pull':
            out += f'    <p class="figures">{md(val)}</p>\n'
        elif kind == 'ul':
            # a plain list: .checks is white-on-dark and would vanish in the light post body
            items = ''.join(f'<li>{md(t)}</li>' for t in val)
            out += f'    <ul>{items}</ul>\n'
        else:
            raise ValueError(f'unknown blog block {kind!r}')
    return out


def blog_card(post):
    return (f'        <article class="card">\n'
            f'          <div class="card-body">\n'
            f'            <span class="tag">{e(post_date(post["date"]))}</span>\n'
            f'            <h3><a href="{post_file(post)}">{e(post["title"])}</a></h3>\n'
            f'            <p>{e(post["dek"])}</p>\n'
            f'            <p><a class="link" href="{post_file(post)}">Read the post &rarr;</a></p>\n'
            f'          </div>\n'
            f'        </article>\n')


def blog_list_html():
    """The post list on blog.html. Newest first, one card each."""
    if not blog_posts.POSTS:
        return ''
    cards = ''.join(blog_card(p) for p in blog_posts.POSTS)
    return ('<section class="section">\n'
            '    <div class="wrap">\n'
            '      <div class="head"><h2>Market Notes</h2></div>\n'
            f'      <div class="cards">\n{cards}      </div>\n'
            '    </div>\n'
            '  </section>')


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
    ('trust-estate-probate-sales.html', 'trust', 'Trust / Estate / Probate Sales | Simonton Commercial',
     'Trust, estate and probate sales of apartment buildings from Simonton Commercial, RE/MAX One Commercial.', ''),
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


# PREVIEW (not linked from anywhere, local builds only): the team page in the Contact Our Team card style, one wide card per broker,
# photo and contact details on the left and the bio on the right. If the client approves it, it replaces team.html.
def team_wide_html():
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
        bio = ''.join(f'<p>{e(t)}</p>' for t in p.get('bio', [])) or '<p>Full bio coming soon.</p>'
        cards += (f'<article class="ft-card ft-wide" style="--i:{i}">'
                  f'<div class="ft-side">'
                  f'<div class="ft-top"><span>// {i:02d}</span><span>RE/MAX ONE COMMERCIAL</span></div>'
                  f'<div class="ft-photo"><img src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" loading="lazy"><span class="ft-scan" aria-hidden="true"></span></div>'
                  f'<h2 class="ft-name">{e(p["name"])}</h2>'
                  f'<p class="ft-role">{e((p.get("short") or p["title"]).upper())}</p>'
                  f'<dl class="ft-data">{rows}</dl>'
                  f'<a class="ft-link" href="team-{slug(p["name"])}.html">View profile <span aria-hidden="true">&rarr;</span></a></div>'
                  f'<div class="ft-bio"><p class="ft-label">// BIO</p>{bio}</div></article>')
    return f'''<section class="ft ft-team" id="team-list">
  <div class="wrap">
    <p class="ft-eyebrow">// SIMONTON COMMERCIAL &middot; RE/MAX ONE COMMERCIAL</p>
    <h1 class="ft-title">Meet the Team</h1>
    <div class="ft-list">{cards}</div>
  </div>
</section>'''


# Built only on local machines: GitHub Actions sets CI, so the deployed site never includes the preview.
if not os.environ.get('CI'):
    (SITE / 'team-preview.html').write_text(page(
        'Our Team (preview) | Simonton Commercial',
        'Meet the multifamily investment brokerage team at Simonton Commercial, RE/MAX One Commercial.',
        team_wide_html(), 'subpage'))


for fname, sec, title, desc, extra in TAB_PAGES:
    if sec == 'contact':
        # Team cards first, then the dark contact form block.
        team_part = contact_team_html().replace('<h2 class="ft-title">', '<h1 class="ft-title">').replace('Contact Our Team</h2>', 'Contact Our Team</h1>')
        form_part = section_html(sec).replace('<h1 class="sec-h1">Contact</h1>', '<h2>Contact</h2>')
        body = team_part + form_part
    elif sec == 'blog':
        body = section_html(sec) + blog_list_html()
    else:
        body = section_html(sec)
    (SITE / fname).write_text(page(title, desc, body, 'subpage', extra))

def expertise_html(zips):
    """Areas of Expertise on a profile: each ZIP the broker covers, linked to its area page, with a
    one-line read of that market from the CoStar stats."""
    by_zip = {h['zip']: h for h in ac.HOODS if h.get('zip')}
    tiles = ''
    for z in zips:
        h = by_zip.get(z)
        if not h:
            continue
        st = area_comps.STATS.get(h['slug']) or {}
        stat = (f'{st["count"]} sales in 12 months &middot; ${st["ppu"] // 1000}K median per unit'
                if st.get('count', 0) >= 3 else '')
        tiles += (f'<li><a href="{ac.filename(h["slug"])}"><span class="xp-zip">{z}</span>'
                  f'<strong>{e(h["label"])}</strong>' + (f'<small>{stat}</small>' if stat else '') + '</a></li>')
    return f'<div class="expertise"><h2>Areas of Expertise</h2><ul class="xp-list">{tiles}</ul></div>' if tiles else ''


EXPERTISE = {'Mike Torres': market_mike.ZIPS}

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
        closings = market_robert.closings_table()
    elif p['name'] == 'Mike Torres':
        closings = market_robert.closings_table(market_mike.CLOSINGS, market_mike.TOTAL, market_mike.CAPTION)
    else:
        closings = ''
    # a short table sits at its natural height instead of stretching to the bio's length
    split_cls = 'person-split' + (' person-split-short' if p['name'] == 'Mike Torres' else '')
    if closings and p['name'] in EXPERTISE:
        # Mike's profile: a dark intro band with photo, name, contact and his numbers, then the bio beside an
        # at-a-glance panel, his areas, his closings and a valuation prompt.
        first = p['name'].split()[0]
        digits = re.sub(r'\D', '', p.get('phone', ''))
        units = sum(r[3] for r in market_mike.CLOSINGS)
        volume = sum(int(re.sub(r'\D', '', r[5])) for r in market_mike.CLOSINGS)
        zips = EXPERTISE[p['name']]
        bio = p.get('bio', [])
        lead = f'<p class="pm-lead">{e(bio[0])}</p>' if bio else ''
        rest = ''.join(f'<p>{e(t)}</p>' for t in bio[1:])
        glance = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in market_mike.GLANCE)
        body = f'''<section class="pm-hero">
  <div class="wrap">
    <a class="back back-light" href="team.html">&larr; All team members</a>
    <div class="pm-hero-grid">
      <img class="pm-photo" src="assets/team/{e(p["photo"])}" alt="{e(p["name"])}" width="560" height="700">
      <div class="pm-intro">
        <p class="eyebrow">Simonton Commercial &middot; RE/MAX One Commercial</p>
        <h1>{e(p["name"])}</h1>
        <p class="pm-title">{e(p["title"])} &middot; Multifamily Investment Sales</p>
        <div class="pm-actions">
          <a class="btn btn-light" href="tel:+1{digits}">Call {e(p.get("phone", ""))}</a>
          <a class="btn btn-ghost" href="mailto:{e(p.get("email", ""))}">Email {e(first)}</a>
        </div>
        <p class="pm-meta"><span>{e(p.get("email", ""))}</span><span>{e(p.get("handle", ""))}</span><span>DRE #{e(p.get("dre", ""))}</span></p>
        <dl class="pm-stats">
          <div><dt>Units closed</dt><dd>{units}</dd></div>
          <div><dt>Sales volume</dt><dd>${volume / 1e6:.1f}M</dd></div>
          <div><dt>ZIP codes covered</dt><dd>{len(zips)}</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>
<section class="section pm-about">
  <div class="wrap pm-about-grid">
    <div class="pm-bio"><h2>About {e(first)}</h2>{lead}{rest}</div>
    <aside class="pm-glance" aria-label="{e(first)} at a glance"><h2>At a Glance</h2><dl>{glance}</dl></aside>
  </div>
</section>
<section class="section alt pm-areas">
  <div class="wrap">{expertise_html(zips)}</div>
</section>
<section class="section pm-closings" id="closings">
  <div class="wrap">{closings}</div>
</section>
<section class="section dark pm-cta">
  <div class="wrap pm-cta-grid">
    <div><h2>What Is Your Building Worth?</h2>
      <p class="lead">Send {e(first)} the address and rent roll for a free, confidential valuation with the comparable sales behind it.</p></div>
    <div class="pm-actions"><a class="btn btn-light" href="mailto:{e(p.get("email", ""))}?subject=Valuation%20request">Request a valuation</a>
      <a class="btn btn-ghost" href="tel:+1{digits}">Call {e(first)}</a></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2>More from the team</h2>
    <div class="team">
{others}
    </div>
  </div>
</section>'''
    elif closings:
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
    {expertise_html(EXPERTISE.get(p['name'], []))}
    <div class="{split_cls}">
      <div class="person-closings" id="closings">
      {closings}
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


def comps_html(slug, label):
    """The area's most recent apartment building sales (from CoStar via tools/costar_comps.py)."""
    rows = area_comps.COMPS.get(slug)
    if not rows:
        return ''
    when = lambda d: datetime.date.fromisoformat(d).strftime('%b %Y')
    # the Neighborhood column only earns its space when the rows span more than one neighborhood
    hood = len({r[1] for r in rows}) > 1
    body = ''.join(
        f'<tr><th scope="row">{e(a)}</th>{f"<td>{e(n)}</td>" if hood else ""}<td class="num">{u}</td><td class="num">{b or ""}</td>'
        f'<td class="num">{when(d)}</td><td class="num">${p:,}</td><td class="num">${pu:,}</td>'
        f'<td class="num">{f"${sf:,}" if sf else "&ndash;"}</td><td class="num">{f"{g:.2f}" if g else "&ndash;"}</td></tr>'
        for a, n, u, b, d, p, pu, sf, g in rows)
    return f'''<div class="comps">
  <h2>Recent {e(label)} Apartment Sales</h2>
  <p class="comps-sub">The {len(rows)} most recent multifamily sales{" in " + e(label) if slug != "los-angeles" else " with a Los Angeles address"}.</p>
  <div class="table-wrap" role="region" aria-label="Recent {e(label)} sales" tabindex="0">
    <table class="closed">
      <caption class="sr-only">Recent apartment building sales in {e(label)}</caption>
      <thead><tr><th scope="col">Property</th>{'<th scope="col">Neighborhood</th>' if hood else ''}<th scope="col" class="num">Units</th><th scope="col" class="num">Built</th><th scope="col" class="num">Sold</th><th scope="col" class="num">Sale Price</th><th scope="col" class="num">$/Unit</th><th scope="col" class="num">$/SF</th><th scope="col" class="num"><abbr title="Gross rent multiplier">GRM</abbr></th></tr></thead>
      <tbody>{body}</tbody>
    </table>
  </div>
  <p class="disclaimer">Source: {e(area_comps.SOURCE)}. Prices, unit counts and GRM as reported; a dash means not reported. Not verified by RE/MAX One Commercial.</p>
</div>'''


def money(n):
    return f'${n / 1e9:.1f} billion' if n >= 1e9 else f'${n / 1e6:.1f} million' if n >= 1e6 else f'${n:,.0f}'


def figures(slug, label):
    """One paragraph of the area's numbers over the CoStar period; regenerated with the comps."""
    st = area_comps.STATS.get(slug)
    if not st or st['count'] < 3:
        return ''
    where = 'Los Angeles (properties with a Los Angeles address)' if slug == 'los-angeles' else label
    units = round(st['units'])
    t = (f"By the numbers: over the past 12 months, CoStar recorded {st['count']} multifamily sales in {where} "
         f"totaling {money(st['volume'])}. The median sale was {money(st['price'])}, or ${st['ppu']:,} per unit, "
         f"for a building of about {units} unit{'s' if units != 1 else ''}")
    t += f" built around {st['built']}." if st['built'] else '.'
    if st['pre1979'] is not None:
        t += f" {st['pre1979']}% of the buildings that sold were built before 1979"
        t += ('.' if slug in ac.OWN_CITY
              else ', roughly the cutoff for the City of Los Angeles Rent Stabilization Ordinance.')
    if st['cap']:
        t += f" Where a cap rate was reported, the median was {st['cap']:.1f}%."
    return f'<p class="figures">{e(t)}</p>'


def indicators_html(slug, label, client=()):
    """Market indicator tiles from the CoStar stats. Cap rate and $/unit fall back to the client's tiles when
    there are too few sales; the client's vacancy and rent growth tiles (full market pages) are kept as they are."""
    st = area_comps.STATS.get(slug) or {}
    theirs = {l: (v, note) for l, v, note in client}
    k = lambda n: f'${n / 1000:,.0f}K'
    tiles = []
    if st.get('cap_mid'):
        lo, hi = st['cap_mid']
        tiles.append(('Cap rate', f'{lo:.1f}%–{hi:.1f}%', f'middle half of {st["caps"]} reported sales'))
    elif 'Cap rate' in theirs:
        tiles.append(('Cap rate',) + theirs['Cap rate'])
    if st.get('ppu_mid'):
        lo, hi = st['ppu_mid']
        tiles.append(('Price per unit', f'{k(lo)}–{k(hi)}', f'middle half; median ${st["ppu"]:,}'))
    elif 'Price per unit' in theirs:
        tiles.append(('Price per unit',) + theirs['Price per unit'])
    if st.get('psf_mid'):
        lo, hi = st['psf_mid']
        tiles.append(('Price per SF', f'${lo:,.0f}\u2013${hi:,.0f}', f'middle half; median ${st["psf"]:,}'))
    if st.get('grm_mid'):
        lo, hi = st['grm_mid']
        tiles.append(('GRM', f'{lo:.1f}\u2013{hi:.1f}', f'middle half of {st["grms"]} reported sales'))
    if st.get('count'):
        tiles.append(('Sales, last 12 months', f'{st["count"]}', f'{money(st["volume"])} total'))
    if st.get('count', 0) >= 3 and st.get('built'):
        units = round(st['units'])
        tiles.append(('Typical building', f'{units} unit{"s" if units != 1 else ""}', f'median; built around {st["built"]}'))
    tiles += [(l,) + theirs[l] for l in ('Vacancy rate', 'Rental growth') if l in theirs]
    if not tiles:
        return ''
    html_tiles = ''.join(f'<div class="ind"><span class="ind-l">{e(l)}</span><strong>{e(v)}</strong>'
                         + (f'<small>{e(n)}</small>' if n else '') + '</div>' for l, v, n in tiles)
    note = (f'Cap rate, price per unit, price per SF, GRM (gross rent multiplier), sales and building figures are '
            f'from {area_comps.SOURCE}; ranges show the middle half of sales (25th to 75th percentile).')
    if any(l in theirs for l in ('Vacancy rate', 'Rental growth')):
        note += ' Vacancy and rental growth are broader apartment-market indicators.'
    return (f'<section class="ind-banner" aria-labelledby="ind-{slug}"><div class="wrap">'
            f'<h2 class="ind-banner-h" id="ind-{slug}">{e(label)} Market Indicators</h2>'
            f'<div class="ind-row" style="--n:{len(tiles)}">{html_tiles}</div><p class="disclaimer">{e(note)}</p></div></section>')


def robert_link(slug, label):
    """Palms, Mid City and Mar Vista point to Robert's in-depth market page."""
    if slug not in ac.ROBERT_AREAS:
        return ''
    return (f'<p><a class="link" href="{market_robert.PATH}">See Robert Carlile\u2019s in-depth Palms, Mar Vista '
            f'and Mid City market page &rarr;</a></p>')


def snapshot_html(title, paras, extra=''):
    return f'<div class="area-snap about-body"><h2>{e(title)}</h2>{paras_html(paras)}{extra}</div>'


def area_main(comps, snapshot):
    """Recent sales and the market snapshot side by side (stacked on phones)."""
    return f'<section class="section area-main"><div class="wrap area-split">{comps}{snapshot}</div></section>'


def paras_html(paras):
    return ''.join(f'<p>{e(t)}</p>' for t in paras)


# Every area page runs in the same order: hero, indicator banner, recent sales beside the market snapshot,
# page extras, valuation form.

# Full market pages
for a in ac.FULL:
    n = a['name']
    body = (area_hero(f'{n} Multifamily Broker', 'RE/MAX One Commercial', a['intro'])
            + indicators_html(a['slug'], n, a['indicators'])
            + area_main(comps_html(a['slug'], n),
                        snapshot_html(f'{n} Multifamily Market Snapshot', ac.SNAPSHOTS.get(a['slug'], a['snapshot']),
                                      figures(a['slug'], n) + robert_link(a['slug'], n)))
            + valuation_block(f'What Is My {n} Apartment Building Worth?', a['worth'], n)
            )
    (SITE / ac.filename(a['slug'])).write_text(page(
        f'{n} Multifamily Broker | RE/MAX One Commercial', trim(a['intro']), body, 'subpage'))

# San Fernando Valley
v = ac.VALLEY
cards = ''.join(f'<article class="hood"><h3>{e(n)}</h3><p>{e(t)}</p></article>' for n, t in v['hoods'])
body = (area_hero(v['h1'], 'RE/MAX One Commercial')
        + indicators_html(v['slug'], v['name'])
        + area_main(comps_html(v['slug'], v['name']),
                    snapshot_html(f'{v["name"]} Multifamily Market Snapshot', [v['intro']] + v['paras']))
        + f'<section class="section alt"><div class="wrap"><h2>Valley Neighborhoods</h2><div class="hood-grid">{cards}</div></div></section>'
        + valuation_block('What Is My Valley Apartment Building Worth?',
                          ['Request a free, confidential valuation for your San Fernando Valley apartment building from the RE/MAX One Commercial multifamily team.'],
                          v['name'])
        )
(SITE / ac.filename(v['slug'])).write_text(page(
    f'{v["h1"]} | RE/MAX One Commercial', trim(v['intro']), body, 'subpage'))

# Neighborhood pages: the client's overview paragraph leads the snapshot
for h in ac.HOODS:
    body = (area_hero(h['name'], (f'ZIP {h["zip"]} \u00b7 ' if h.get('zip') else '') + 'Multifamily Broker')
            + indicators_html(h['slug'], h['label'])
            + area_main(comps_html(h['slug'], h['label']),
                        snapshot_html(f'{h["label"]} Multifamily Market Snapshot', h['paras'] + ac.SNAPSHOTS.get(h['slug'], []),
                                      figures(h['slug'], h['label'])))
            + valuation_block(f'What Is My {h["label"]} Apartment Building Worth?',
                              [f'Request a free, confidential valuation for your {h["label"]} apartment building from the RE/MAX One Commercial multifamily team.'],
                              h['label'])
            )
    (SITE / ac.filename(h['slug'])).write_text(page(
        f'{h["name"]} Multifamily Broker | RE/MAX One Commercial', trim(h['paras'][0]), body, 'subpage'))

# Pages with no client text yet: the written snapshot plus figures
for slug_, label in ac.PLACEHOLDERS:
    snap = ac.SNAPSHOTS.get(slug_)
    body = (area_hero(f'{label} Multifamily Broker', 'RE/MAX One Commercial')
            + indicators_html(slug_, label)
            + area_main(comps_html(slug_, label),
                        snapshot_html(f'{label} Multifamily Market Snapshot', snap or [
                            f'Detailed {label} market information is coming soon. In the meantime, request a free, confidential valuation for your apartment building below.'],
                            figures(slug_, label) + robert_link(slug_, label)))
            + valuation_block(f'What Is My {label} Apartment Building Worth?',
                              [f'Request a free, confidential valuation for your {label} apartment building from the RE/MAX One Commercial multifamily team.'],
                              label)
            )
    desc = trim(snap[0]) if snap else f'{label} multifamily broker: free apartment building valuations from RE/MAX One Commercial.'
    (SITE / ac.filename(slug_)).write_text(page(
        f'{label} Multifamily Broker | RE/MAX One Commercial', desc, body, 'subpage'))

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

# One page per blog post (source: blog_posts.py)
for _post in blog_posts.POSTS:
    _byline = (f'<p class="note">By <a href="{_post["author_page"]}">{e(_post["author"])}</a>, '
               f'{e(_post["author_title"])}, Simonton Commercial at RE/MAX One Commercial. '
               f'Published {e(post_date(_post["date"]))}.</p>')
    _body = (area_hero(_post['title'], f'Blog · {post_date(_post["date"])}', _post['dek'])
             + '<section class="section alt">\n  <div class="wrap narrow about-body">\n'
             + '    <a class="back" href="blog.html">&larr; All posts</a>\n'
             + post_body_html(_post)
             + _byline
             + '\n  </div>\n</section>'
             + valuation_block('What Is My Apartment Building Worth?',
                               ['Request a free, confidential valuation of your Los Angeles apartment '
                                'building from the RE/MAX One Commercial multifamily team.'],
                               'blog'))
    (SITE / post_file(_post)).write_text(page(
        f'{_post["title"]} | Simonton Commercial', _post['dek'], _body, 'subpage'))

print('Generated tab pages, team.html,', len(team), 'profile pages and the Palms/Mar Vista/Mid City page')
