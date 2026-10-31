"""Content + renderer for Robert Carlile's Palms / Mar Vista / Mid City market page.

Output: site/apartment-broker/palms-mar-vista-mid-city/index.html (built by build_team.py).
"""
import html, json, re

e = html.escape

DOMAIN = 'https://simontoncommercial.com'
PATH = 'apartment-broker/palms-mar-vista-mid-city/'
ROOT = '../../'  # path from the page back to the site root

TITLE = 'Apartment Broker for Palms, Mar Vista & Mid City | Robert Carlile, RE/MAX One Commercial'
DESC = ('Multifamily specialist for Palms, Mar Vista and Mid City. Apartment building sales across '
        '90016, 90018, 90019, 90034, 90064 and 90066. Free valuations.')
H1 = 'The Apartment Specialist for Palms, Mar Vista & Mid City'
SUB = 'Three submarkets. Six ZIP codes. 4,141 apartment buildings, tracked one by one.'

STATS = [('135', 'Units sold'), ('$29.1M', 'Sales volume'), ('$215,592', 'Average price per unit')]

# Property, submarket, units, built, sale price, $/unit
CLOSINGS = [
    ('3320 Woodbine St', 'Mar Vista', 12, 1954, '$4,700,000', '$391,700'),
    ('3763 S Bentley Ave', 'Palms', 12, 1985, '$3,700,000', '$308,300'),
    ('4646 Coliseum St', 'Mid City', 18, 1954, '$3,150,000', '$175,000'),
    ('3741-3745 Jasmine Ave', 'Palms', 14, 1953, '$3,000,000', '$214,300'),
    ('1909 Buckingham Rd', 'Mid City', 16, 1964, '$2,950,000', '$184,400'),
    ('2610 S Bundy Dr', 'Mar Vista', 9, 1970, '$2,385,000', '$265,000'),
    ('3421 & 3427 S Norton Ave', 'Mid City', 16, 1930, '$2,275,000', '$142,200'),
    ('1514 S Bronson Ave', 'Mid City', 5, 1920, '$1,580,000', '$316,000'),
    ('8960 Hargis St', 'Palms', 6, 1956, '$1,475,000', '$245,800'),
    ('3018 9th Ave', 'Mid City', 8, 1947, '$1,350,000', '$168,800'),
    ('1542 2nd Ave', 'Mid City', 8, 1962, '$1,250,000', '$156,200'),
    ('1506 W 36th St', 'Mid City', 5, 1929, '$880,000', '$176,000'),
    ('1714 3rd Ave', 'Mid City', 6, 1907, '$410,000', '$68,300'),
]
TOTAL = ('Total', '', 135, '', '$29,105,000', '$215,592 avg')

BIO = [
    'Robert Carlile is a multifamily investment broker with RE/MAX One Commercial in Santa Monica. He sells apartment buildings in Palms, Mar Vista and Mid City.',
    'That restraint is the whole practice. Most brokers who take a listing in Mar Vista on Tuesday are pitching in Van Nuys on Thursday, pricing both off the same countywide averages. Carlile works three adjacent submarkets across six ZIP codes, and tracks all 4,141 apartment buildings of five to thirty units inside them: who owns each one, how long they have held it, the unit mix, the assessed basis, the rent-regulation exposure. When an owner calls about a building on Keystone or Cattaraugus or Hauser, he knows the building before the conversation starts.',
    'It shows in how the deals come together. His closings in these neighborhoods run from five-unit 1920s buildings in Mid City to eighteen-unit mid-century properties. That is 135 units and $29.1 million in sales volume, all of it inside the three submarkets, at an average of $215,592 per unit. Those are not countywide numbers padded with deals from the Valley. They are from these streets.',
    'Much of his business begins before a building is ever listed. Robert is in direct contact with owners across his coverage area year-round, which means sellers reach a broker who already knows which buyers are active in their specific pocket, and buyers reach one who knows which owners are thinking about it.',
    "A graduate of the University of Southern California, Carlile works as part of the Simonton Commercial Group, RE/MAX One Commercial's multi-family investments team. He lives in Orange County with his wife and young family.",
]

COVERAGE_INTRO = 'Most brokers say they cover "the Westside." Here is precisely what Carlile covers, down to the pocket.'
COVERAGE = [
    dict(name='Mid City', zips='90016, 90018, 90019',
         stats='1,871 apartment buildings / 17,215 units / median year built 1949 / 94% built before 1979',
         text='The oldest apartment stock in the coverage area and the most rent-regulated. 1920s and 1930s courtyard buildings along the Adams, Jefferson and Washington corridors, 1950s and 1960s walk-ups filling in between. Values swing sharply block to block, and the Expo Line has reshaped what buyers will pay within walking distance of a station.',
         hoods='West Adams, Jefferson Park, Arlington Heights, Harvard Heights, Country Club Park, Picfair Village, Victoria Park, Lafayette Square, Wellington Square, Sycamore Square, Oxford Square, Western Heights, Brookside, Faircrest Heights, Crestview, Blackwelder, Baldwin Vista, Wilshire Vista, and the Mid-Wilshire and Carthay edges.',
         corridors='Adams Blvd, Jefferson Blvd, Washington Blvd, Pico Blvd, Venice Blvd, Crenshaw Blvd, La Brea Ave, Fairfax Ave.'),
    dict(name='Palms', zips='90034',
         stats='1,252 apartment buildings / 13,352 units / median year built 1963 / 83% built before 1979',
         text='The densest apartment market of the three. Block after block of 1950s and 1960s buildings on 6,500 to 8,000 square foot lots, built when Palms absorbed more rental housing than almost anywhere on the Westside. Proximity to Culver City, Playa Vista and the Expo Line keeps demand steady, and buyers here underwrite tighter than in Mid City.',
         hoods='Palms, Cheviot Vista, Monte Mar Vista, Westside Village, Reynier Village, and the western edge of Beverlywood.',
         corridors='National Blvd, Venice Blvd, Motor Ave, Overland Ave, Palms Blvd, Sepulveda Blvd.'),
    dict(name='Mar Vista', zips='90064, 90066',
         stats='1,018 apartment buildings / 10,643 units / median year built 1962 / 78% built before 1979',
         text='The highest price per unit in the coverage area and the newest stock of the three. Mid-century buildings on wider streets, with a meaningful share of owner-occupied and long-held family properties. Tenant demand is strong and turnover is low, which changes how a rent roll should be read.',
         hoods='Mar Vista, Westdale, Westdale Trousdale, Mar Vista Hill, Mar Vista Gardens, Rancho Park, Cheviot Hills, and the southern edge of West Los Angeles.',
         corridors='Venice Blvd, Centinela Ave, Palms Blvd, National Blvd, Sepulveda Blvd, Pico Blvd.'),
]

WHY = [
    ('He knows the building before the call.', 'A record on all 4,141 apartment buildings in these six ZIP codes: unit mix, year built, ownership structure, last sale, assessed basis, rent-regulation status. Give him an address and he is not starting from scratch.'),
    ('He prices by pocket, not by region.', 'Mid City, Palms and Mar Vista are adjacent and price very differently, and the spread inside each one is wider still. A valuation built on Westside averages can be off by hundreds of thousands of dollars on a ten-unit building.'),
    ('He runs the numbers before quoting one.', 'Every valuation is underwritten: vacancy, taxes at a stepped-up basis, insurance, management, reserves, and a loan sized to what a lender will actually fund. A price per unit without a rent roll behind it is a guess.'),
    ('He knows the buyers by name.', 'Working one market continuously means knowing who closed last quarter, who is in a 1031 window, and who has been waiting for a particular street. That is what gets a building sold at the top of its range.'),
]

SERVICES = [
    ('Broker Opinion of Value', 'A written, underwritten valuation with comparable sales, rent analysis and a defensible price range. Free, no listing agreement, usually returned within 48 hours of receiving a rent roll.'),
    ('Exclusive Listing & Sale', 'Full marketing to the Westside buyer pool, offer management and a competitive process across all six covered ZIP codes.'),
    ('Off-Market Acquisition', 'For buyers with a specific mandate, whether unit count, submarket, timing or a 1031 clock. Carlile sources buildings that never reach the market.'),
    ('1031 Exchange & Estate Sales', 'Timeline coordination for exchange buyers and sellers, and date-of-death valuations for trustees and heirs administering an estate that includes an apartment building.'),
]

FAQ = [
    ('What is my apartment building in Palms, Mar Vista or Mid City worth?',
     'The rent roll drives it more than anything else. Two identical buildings on the same block can be worth very different numbers depending on how far below market the rents sit and how long tenants have been in place. Buildings in these submarkets trade on a multiple of gross annual rent, adjusted for condition, unit mix and rent-regulation exposure. Carlile provides a free written valuation with the comparable sales behind it. Send the address and a rent roll.'),
    ('Why does Robert Carlile only work three neighborhoods?',
     'Because apartment pricing is local to a degree most owners underestimate. Mid City, Palms and Mar Vista sit next to one another, share similar housing stock, and still price very differently, and the variation within each one is wider still. A broker covering all of Los Angeles cannot know 4,141 buildings. A broker covering six ZIP codes can, and that knowledge is what produces an accurate price and the right buyer.'),
    ('Is my apartment building subject to LA rent control?',
     'Most likely yes. The City of Los Angeles Rent Stabilization Ordinance generally applies to multi-unit rental properties with a certificate of occupancy issued before October 1, 1978. Across these six ZIP codes, 88% of apartment buildings of five to thirty units were built before 1979, and 94% in Mid City, where the median building dates to 1949. RSO status affects allowable rent increases, relocation obligations and therefore value. The LA Housing Department maintains the rent registry, and status should be confirmed property by property rather than assumed from the year built.'),
    ('How does Measure ULA affect my sale?',
     'Measure ULA adds a City of Los Angeles transfer tax on higher-value property sales, on top of the existing documentary transfer tax. The threshold is adjusted annually, so the current figure needs confirming at the time of sale. It matters most to owners whose building prices out near that threshold, where a modest difference in sale price produces a large difference in tax. If your building is near the line, model it before going to market. This is general information, not tax advice. Talk to your CPA.'),
    ('Should I sell now or wait?',
     'It depends on why you would sell. With no particular reason to transact, waiting is reasonable. With one, whether that is a maturing loan, an estate or trust distribution, a partnership that wants out, a 1031 deadline, deferred maintenance you do not want to fund, or a building you no longer want to manage, the question becomes pricing and timing rather than whether. The three submarkets also do not move in step, so the answer depends partly on which one your building is in.'),
    ('What does a valuation cost, and is there any obligation?',
     'Nothing, and none. Carlile provides a written valuation with comparable sales whether or not an owner ever lists with him. Many owners he speaks with are years from selling, or never selling. Knowing the number is useful either way, for estate planning, refinancing or a partnership conversation. He will need the rent roll and unit mix to give anything accurate.'),
    ('Can I do a 1031 exchange on an apartment building?',
     'Generally yes, if you are selling investment property and reinvesting in like-kind investment property. The timelines are strict. You have 45 days to identify replacement property and 180 days to close, and both run from the sale closing, so the replacement search should start before escrow rather than after. For long-held buildings in these neighborhoods an exchange is often the difference between a sale that makes sense and one that does not, because the embedded gain on a decades-long hold can be substantial. Your CPA and a qualified intermediary should be involved early.'),
    ('How long does it take to sell an apartment building here?',
     'Plan on 30 to 45 days of marketing to a signed contract and 30 to 60 days to close, depending on financing. Cash and 1031 buyers move faster. Pricing is the bigger variable. A building listed above the market tends to sit, then sell at a discount to where it would have cleared if priced correctly at launch.'),
    ('Do you work with buyers as well as sellers?',
     'Yes. Carlile represents buyers acquiring apartment buildings in these three submarkets, including off-market acquisitions for buyers with a specific mandate or a 1031 deadline.'),
]

CTA_H = 'Free Valuation on Your Apartment Building'
CTA_P = ('Send the address and rent roll and Robert will come back with a written valuation, the comparable '
         'sales behind it, and an honest read on whether this is the right market for your situation.')


def schema():
    agent = {
        '@context': 'https://schema.org',
        '@type': 'RealEstateAgent',
        'name': 'Robert Carlile',
        'description': DESC,
        'url': f'{DOMAIN}/{PATH}',
        'image': f'{DOMAIN}/assets/team/robert-carlile.jpg',
        'jobTitle': 'Multifamily Investment Broker',
        'worksFor': {'@type': 'RealEstateAgent', 'name': 'RE/MAX One Commercial'},
        'address': {'@type': 'PostalAddress', 'streetAddress': '2601 Ocean Park Blvd, Ste 311',
                    'addressLocality': 'Santa Monica', 'addressRegion': 'CA', 'postalCode': '90405',
                    'addressCountry': 'US'},
        'areaServed': [{'@type': 'Place', 'name': n} for n in
                       ['Palms, Los Angeles, CA', 'Mar Vista, Los Angeles, CA', 'Mid City, Los Angeles, CA']]
                      + [{'@type': 'Place', 'name': f'ZIP {z}'}
                         for z in ['90016', '90018', '90019', '90034', '90064', '90066']],
        'knowsAbout': ['Multifamily investment sales', 'Apartment building valuation', '1031 exchanges'],
    }
    faq = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ],
    }
    out = ''
    for obj in (agent, faq):
        out += '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    return out


def rebase(s):
    """Point shared header/footer links at the site root from this nested page."""
    s = re.sub(r'(src|href)="(assets/|[a-z0-9-]+\.html)', lambda m: f'{m.group(1)}="{ROOT}{m.group(2)}', s)
    return s


def closings_table():
    """Heading and table of Robert's closed sales."""
    rows = ''.join(
        f'<tr><th scope="row">{e(p)}</th><td>{e(s)}</td><td class="num">{u}</td><td class="num">{b}</td>'
        f'<td class="num">{e(sp)}</td><td class="num">{e(pu)}</td></tr>' for p, s, u, b, sp, pu in CLOSINGS)
    t = TOTAL
    foot = (f'<tr><th scope="row">{t[0]}</th><td></td><td class="num">{t[2]}</td><td></td>'
            f'<td class="num">{t[4]}</td><td class="num">{t[5]}</td></tr>')
    return f'''<div class="head"><h2>Recently Closed Transactions</h2></div>
    <div class="table-wrap" role="region" aria-label="Closed transactions table" tabindex="0">
      <table class="closed">
        <caption class="sr-only">Closed apartment building sales in Palms, Mar Vista and Mid City</caption>
        <thead><tr><th scope="col">Property</th><th scope="col">Submarket</th><th scope="col" class="num">Units</th><th scope="col" class="num">Built</th><th scope="col" class="num">Sale Price</th><th scope="col" class="num">$/Unit</th></tr></thead>
        <tbody>{rows}</tbody>
        <tfoot>{foot}</tfoot>
      </table>
    </div>'''


def sections(root, profile=False):
    """The market content below the hero. With profile=True it is embedded in Robert's
    profile page, which shows the closings table and his bio itself, so the stats bar,
    closings and About sections are left out."""
    stats = ''.join(f'<div><strong>{e(n)}</strong><span>{e(l)}</span></div>' for n, l in STATS)
    bio = ''.join(f'<p>{e(p)}</p>' for p in BIO)
    cov = ''.join(
        f'''<article class="cov"><h3>{e(c["name"])} <span>{e(c["zips"])}</span></h3>
        <p class="cov-stats">{e(c["stats"])}</p><p>{e(c["text"])}</p>
        <p><strong>Neighborhoods:</strong> {e(c["hoods"])}</p>
        <p><strong>Corridors:</strong> {e(c["corridors"])}</p></article>''' for c in COVERAGE)
    why = ''.join(f'<li><strong>{e(h)}</strong> {e(b)}</li>' for h, b in WHY)
    svc = ''.join(f'<article class="card"><div class="card-body"><h3>{e(h)}</h3><p>{e(b)}</p></div></article>' for h, b in SERVICES)
    faq = ''.join(f'<details name="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    top = '' if profile else f'''<section class="stats" aria-label="Closed sales summary"><div class="wrap stats-grid stats-3">{stats}</div></section>

<section class="section" id="closings">
  <div class="wrap">
    {closings_table()}
  </div>
</section>

<section class="section alt" id="about">
  <div class="wrap narrow bio-long"><h2>About Robert Carlile</h2>{bio}
  <p><a class="link" href="{root}team-robert-carlile.html">Robert&rsquo;s full profile &rarr;</a></p></div>
</section>
'''
    return f'''{top}
<section class="section" id="coverage">
  <div class="wrap">
    <div class="head"><h2>Coverage Area</h2></div>
    <p class="lead">{e(COVERAGE_INTRO)}</p>
    <div class="cov-grid">{cov}</div>
  </div>
</section>

<section class="section dark" id="why">
  <div class="wrap narrow"><h2>Why Owners Call Him</h2><ol class="why">{why}</ol></div>
</section>

<section class="section" id="services">
  <div class="wrap"><div class="head"><h2>Services</h2></div><div class="cards">{svc}</div></div>
</section>

<section class="section alt" id="faqs">
  <div class="wrap narrow"><div class="head"><h2>Frequently Asked Questions</h2></div><div class="acc">{faq}</div>
  <p class="disclaimer">General information only, not tax or legal advice. Confirm details with your CPA and attorney.</p></div>
</section>

<section class="section dark" id="valuation">
  <div class="wrap split">
    <div><h2>{e(CTA_H)}</h2><p class="lead">{e(CTA_P)}</p></div>
    <form class="form on-dark" action="#" method="post" data-form data-subject="New valuation request (Palms / Mar Vista / Mid City page)"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <div class="field"><label for="m-name">Full name</label><input id="m-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="m-email">Email</label><input id="m-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="m-phone">Phone</label><input id="m-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="m-addr">Property address</label><input id="m-addr" name="address" required></div>
      <div class="field"><label for="m-units">Number of units</label><input id="m-units" name="units" inputmode="numeric"></div>
      <p class="note">After you submit, reply to our email with your rent roll so we can underwrite the valuation.</p>
      <button class="btn btn-light" type="submit">Request free valuation</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''


def render(top, bottom):
    top, bottom = rebase(top), rebase(bottom)
    canon = f'{DOMAIN}/{PATH}'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="site-root" content="{ROOT}">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/team/robert-carlile.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ROOT}styles.css?v=50">
{schema()}</head>
<body class="subpage">
{top}<main id="main">
<section class="mk-hero">
  <div class="wrap mk-hero-grid">
    <div>
      <p class="eyebrow">Robert Carlile &middot; RE/MAX One Commercial</p>
      <h1>{e(H1)}</h1>
      <p class="mk-sub">{e(SUB)}</p>
      <div class="hero-actions"><a class="btn btn-light" href="#valuation">Get a free valuation</a><a class="btn btn-ghost" href="#closings">See closed sales</a></div>
    </div>
    <img class="mk-photo" src="{ROOT}assets/team/robert-carlile.jpg" alt="Robert Carlile, multifamily broker" width="560" height="700">
  </div>
</section>

{sections(ROOT)}</main>

{bottom}<script src="{ROOT}script.js?v=50"></script>
</body>
</html>
'''
