"""Renderer for a broker's market page (stats, closed-transactions table, bio, areas, valuation form).

Same look as Robert Carlile's page; content comes from a settings module such as market_john.py.
"""
import html, json, re
import areas_content as ac

e = html.escape
DOMAIN = 'https://simontoncommercial.com'
ROOT = '../../'  # from apartment-broker/<slug>/ back to the site root


def money(n):
    return f'${round(n):,}'


def rebase(s):
    return re.sub(r'(src|href)="(assets/|[a-z0-9-]+\.html)', lambda m: f'{m.group(1)}="{ROOT}{m.group(2)}', s)


def trim(text, n=150):
    if len(text) <= n:
        return text
    return text[:n].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def render(m, member, top, bottom):
    top, bottom = rebase(top), rebase(bottom)
    rows = sorted(m.CLOSINGS, key=lambda r: -r[3])
    units = sum(r[2] for r in rows)
    volume = sum(r[3] for r in rows)
    avg = volume / units
    canon = f'{DOMAIN}/{m.PATH}'

    body_rows = ''.join(
        f'<tr><th scope="row">{e(p)}</th><td>{e(a)}</td><td class="num">{u}</td>'
        f'<td class="num">{money(price)}</td><td class="num">{money(price / u)}</td></tr>'
        for p, a, u, price in rows)
    foot = (f'<tr><th scope="row">Total</th><td></td><td class="num">{units}</td>'
            f'<td class="num">{money(volume)}</td><td class="num">{money(avg)} avg</td></tr>')
    stats = ''.join(f'<div><strong>{e(n)}</strong><span>{e(l)}</span></div>' for n, l in [
        (str(len(rows)), 'Closed sales'), (str(units), 'Units sold'),
        (f'${volume / 1e6:.1f}M', 'Sales volume'), (money(avg), 'Average price per unit')])
    bio = ''.join(f'<p>{e(t)}</p>' for t in member.get('bio', []))

    cards = ''
    for slug in m.AREAS:
        a = next(x for x in ac.FULL if x['slug'] == slug)
        cards += (f'<a class="area-card" href="{ROOT}{ac.filename(slug)}"><h3>{e(a["name"])}</h3>'
                  f'<p>{e(trim(a["intro"]))}</p><span>View {e(a["name"])} market &rarr;</span></a>')

    contact = []
    if member.get('phone'):
        contact.append(f'<a href="tel:+1{re.sub(chr(92) + "D", "", member["phone"])}">{e(member["phone"])}</a>')
    if member.get('email'):
        contact.append(f'<a href="mailto:{e(member["email"])}">{e(member["email"])}</a>')
    if member.get('dre'):
        contact.append(f'<span>DRE #{e(member["dre"])}</span>')

    agent = {
        '@context': 'https://schema.org', '@type': 'RealEstateAgent', 'name': m.NAME, 'description': m.DESC,
        'url': canon, 'image': f'{DOMAIN}/assets/team/{m.PHOTO}', 'jobTitle': member.get('short', 'Senior Partner'),
        'worksFor': {'@type': 'RealEstateAgent', 'name': 'RE/MAX One Commercial'},
        'address': {'@type': 'PostalAddress', 'streetAddress': '2601 Ocean Park Blvd, Ste 311',
                    'addressLocality': 'Santa Monica', 'addressRegion': 'CA', 'postalCode': '90405', 'addressCountry': 'US'},
        'areaServed': [{'@type': 'Place', 'name': f'{n}, CA'} for n in
                       ['Los Feliz', 'Silver Lake', 'Echo Park', 'Studio City', 'Sherman Oaks']],
        'knowsAbout': ['Multifamily investment sales', 'Apartment building valuation', '1031 exchanges'],
    }
    if member.get('email'):
        agent['email'] = member['email']
    if member.get('phone'):
        agent['telephone'] = '+1 ' + member['phone']
    schema = '<script type="application/ld+json">' + json.dumps(agent, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="site-root" content="{ROOT}">
<title>{e(m.TITLE)}</title>
<meta name="description" content="{e(m.DESC)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(m.TITLE)}">
<meta property="og:description" content="{e(m.DESC)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/team/{m.PHOTO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ROOT}styles.css?v=__V__">
{schema}</head>
<body class="subpage">
{top}<main id="main">
<section class="mk-hero">
  <div class="wrap mk-hero-grid">
    <div>
      <p class="eyebrow">{e(m.NAME)} &middot; RE/MAX One Commercial</p>
      <h1>{e(m.H1)}</h1>
      <p class="mk-sub">{len(rows)} closed sales. {units} units. {money(volume)} in sales volume.</p>
      <div class="hero-actions"><a class="btn btn-light" href="#valuation">Get a free valuation</a><a class="btn btn-ghost" href="#closings">See closed sales</a></div>
      <p class="mk-contact">{''.join(contact)}</p>
    </div>
    <img class="mk-photo" src="{ROOT}assets/team/{m.PHOTO}" alt="{e(m.NAME)}, multifamily broker" width="560" height="700">
  </div>
</section>

<section class="stats" aria-label="Closed sales summary"><div class="wrap stats-grid">{stats}</div></section>

<section class="section" id="closings">
  <div class="wrap">
    <div class="head"><h2>Closed Transactions</h2></div>
    <div class="table-wrap" role="region" aria-label="Closed transactions table" tabindex="0">
      <table class="closed">
        <caption class="sr-only">Closed apartment building sales by {e(m.NAME)}</caption>
        <thead><tr><th scope="col">Property</th><th scope="col">Area</th><th scope="col" class="num">Units</th><th scope="col" class="num">Sale Price</th><th scope="col" class="num">$/Unit</th></tr></thead>
        <tbody>{body_rows}</tbody>
        <tfoot>{foot}</tfoot>
      </table>
    </div>
  </div>
</section>

<section class="section alt" id="about">
  <div class="wrap narrow bio-long"><h2>About {e(m.NAME)}</h2>{bio}
  <p><a class="link" href="{ROOT}team-{re.sub(r"[^a-z0-9]+", "-", m.NAME.lower()).strip("-")}.html">{e(m.NAME)}&rsquo;s full profile &rarr;</a></p></div>
</section>

<section class="section" id="coverage">
  <div class="wrap">
    <div class="head"><h2>Areas Covered</h2></div>
    <div class="area-cards">{cards}</div>
  </div>
</section>

<section class="section dark" id="valuation">
  <div class="wrap split">
    <div><h2>{e(m.CTA_H)}</h2><p class="lead">{e(m.CTA_P)}</p></div>
    <form class="form on-dark" action="#" method="post" data-form data-subject="New valuation request ({e(m.NAME)} page)"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <div class="field"><label for="m-name">Full name</label><input id="m-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="m-email">Email</label><input id="m-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="m-phone">Phone</label><input id="m-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="m-addr">Property address</label><input id="m-addr" name="address" required></div>
      <div class="field"><label for="m-units">Number of units</label><input id="m-units" name="units" inputmode="numeric"></div>
      <button class="btn btn-light" type="submit">Request free valuation</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
</main>

{bottom}<script src="{ROOT}script.js?v=__V__"></script>
</body>
</html>
'''
