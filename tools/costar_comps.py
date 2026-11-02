"""Turn CoStar sales exports into area_comps.py: the 15 most recent sales for each Areas We Serve page.

Usage:  python3 tools/costar_comps.py ~/Downloads/CostarExport*.xlsx

The raw exports stay off GitHub (the repo is public); only the rows shown on the site are written.
Each sale is placed by CoStar's neighborhood (Submarket Name), city or ZIP, per RULES below.
"""
import datetime, re, statistics, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

PER_AREA = 15
MONTHS = 12  # only sales this recent count as comps
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

# Valley ZIPs inside the City of LA plus San Fernando (city); Burbank and Glendale are left out.
VALLEY_ZIPS = {'91040', '91042', '91303', '91304', '91306', '91307', '91311', '91316', '91324', '91325', '91326',
               '91330', '91331', '91335', '91340', '91342', '91343', '91344', '91345', '91352', '91356', '91364',
               '91367', '91401', '91402', '91403', '91405', '91406', '91411', '91423', '91436', '91601', '91602',
               '91604', '91605', '91606', '91607'}


def sub(*names):
    return lambda s: s['sub'] in names


def city(*names):
    names = {n.lower() for n in names}
    return lambda s: s['city'].lower() in names


def zips(*codes):
    return lambda s: s['zip'] in codes


def expo_park(s):
    """Exposition Blvd to Vernon Ave, Normandie Ave to the 110."""
    return s['lat'] is not None and 34.0035 <= s['lat'] < 34.0183 and -118.3005 <= s['lon'] <= -118.274


RULES = {
    'los-angeles': city('Los Angeles'),
    'west-hollywood': city('West Hollywood'),
    'beverly-grove': sub('Beverly Grove'),
    'beverly-hills': city('Beverly Hills'),
    'fairfax-miracle-mile': sub('Miracle Mile', 'Melrose'),
    'mid-wilshire': sub('Koreatown', 'Hancock Park'),
    'downtown-la': sub('Historic Downtown LA', 'Financial District', 'South Park', 'City West', 'Chinatown',
                       'Flower District', 'Little Tokyo', 'Arts District', 'Bunker Hill', 'Fashion District'),
    'westlake': sub('Westlake North', 'Westlake South'),
    'macarthur-park': sub('MacArthur Park'),
    'pico-union': sub('Pico-Union'),
    'west-adams': sub('West Adams'),
    'exposition-park': expo_park,
    'pico-robertson-beverlywood': sub('Pico-Robertson', 'Beverlywood'),
    'hollywood-hills-laurel-canyon': sub('Hollywood Hills'),
    'los-feliz': sub('Los Feliz'),
    'silver-lake': sub('Silver Lake'),
    'echo-park': sub('Echo Park'),
    'santa-monica': city('Santa Monica'),
    'venice': sub('Venice'),
    'marina-del-rey': city('Marina del Rey'),
    'mar-vista': sub('Mar Vista'),
    'west-la': lambda s: s['sub'] == 'West Los Angeles' and s['zip'] != '90049',  # 90049 is Brentwood
    'studio-city': sub('Studio City'),
    'sherman-oaks': sub('Sherman Oaks'),
    'san-fernando-valley': lambda s: s['zip'] in VALLEY_ZIPS,
    'san-pedro': city('San Pedro'),
    'hollywood': sub('Hollywood'),
    'east-hollywood': sub('East Hollywood', 'Little Armenia', 'Thai Town'),
    'koreatown': sub('Koreatown'),
    'mid-city': sub('Mid-City'),
    'palms': sub('Palms'),
    'culver-city': city('Culver City'),
    'westwood': sub('Westwood'),
    'brentwood': zips('90049'),
    'el-segundo': city('El Segundo'),
    'inglewood': city('Inglewood'),
    'north-hollywood': sub('North Hollywood'),
    'valley-village': sub('Valley Village'),
    'van-nuys': sub('Van Nuys'),
    'encino': zips('91316', '91436'),
    'reseda': sub('Reseda'),
    'northridge': sub('Northridge'),
}


def read_xlsx(path):
    """Rows of the first sheet as dicts keyed by the header row (no openpyxl needed)."""
    z = zipfile.ZipFile(path)
    strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(NS + 'si'):
            strings.append(''.join(t.text or '' for t in si.iter(NS + 't')))
    rows = []
    for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter(NS + 'row'):
        row = {}
        for c in r.iter(NS + 'c'):
            col = re.match(r'[A-Z]+', c.get('r')).group()
            v, t = c.find(NS + 'v'), c.get('t')
            if t == 'inlineStr':
                row[col] = ''.join(x.text or '' for x in c.iter(NS + 't'))
            elif v is not None:
                row[col] = strings[int(v.text)] if t == 's' else v.text
        rows.append(row)
    head = rows[0]
    return [{head[k]: v for k, v in r.items() if k in head} for r in rows[1:]]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def summary(area):
    if not area:
        return None
    med = lambda xs: statistics.median(xs) if xs else None
    # middle half of the sales (25th to 75th percentile); None with fewer than 4 data points
    mid = lambda xs, d: (tuple(round(q, d) for q in statistics.quantiles(xs, n=4, method='inclusive')[::2])
                         if len(xs) >= 4 else None)
    built = [s['built'] for s in area if s['built']]
    caps = [s['cap'] for s in area if s['cap']]
    psfs = [s['psf'] for s in area if s['psf']]
    grms = [s['grm'] for s in area if s['grm']]
    return dict(count=len(area), volume=sum(s['price'] for s in area),
                price=round(med([s['price'] for s in area])), ppu=round(med([s['ppu'] for s in area])),
                units=med([s['units'] for s in area]), built=round(med(built)) if built else None,
                pre1979=round(100 * sum(b < 1979 for b in built) / len(built)) if built else None,
                cap=round(med(caps), 2) if len(caps) >= 3 else None, caps=len(caps),
                ppu_mid=mid([s['ppu'] for s in area], -3), cap_mid=mid(caps, 1),
                psf=round(med(psfs)) if psfs else None, psf_mid=mid(psfs, 0), psfs=len(psfs),
                grm=round(med(grms), 2) if len(grms) >= 3 else None, grm_mid=mid(grms, 1), grms=len(grms))


def month(iso):
    return datetime.date.fromisoformat(iso).strftime('%b %Y')


def main(paths):
    sales = {}
    for p in paths:
        for r in read_xlsx(p):
            price, units, when = num(r.get('Sale Price')), num(r.get('Number of Units')), num(r.get('Sale Date'))
            if r.get('Sale Status') != 'Sold' or not price or not units or not when:
                continue
            age = num(r.get('Age'))
            sales[r['Comp ID']] = dict(
                address=re.sub(r'\s*\(Part of .*?\)', '', r['Property Address']).strip(),
                city=r.get('Property City', ''), zip=(r.get('Property Zip Code') or '')[:5],
                sub=r.get('Submarket Name', ''), lat=num(r.get('Latitude')), lon=num(r.get('Longitude')),
                units=int(units), price=int(price), ppu=round(price / units),
                built=(2026 - int(age)) if age is not None else None, cap=num(r.get('Actual Cap Rate')),
                psf=num(r.get('Price Per SF')), grm=num(r.get('GRM')),
                date=(datetime.date(1899, 12, 30) + datetime.timedelta(days=int(when))).isoformat())
    latest = datetime.date.fromisoformat(max(s['date'] for s in sales.values()))
    cutoff = latest.replace(year=latest.year - MONTHS // 12).isoformat()
    sales = {k: s for k, s in sales.items() if s['date'] > cutoff}
    newest = sorted(sales.values(), key=lambda s: (s['date'], s['price']), reverse=True)
    out, stats = {}, {}
    for slug, rule in RULES.items():
        area = [s for s in newest if rule(s)]
        stats[slug] = summary(area)
        out[slug] = [(s['address'], s['sub'] or s['city'], s['units'], s['built'], s['date'], s['price'], s['ppu'],
                      round(s['psf']) if s['psf'] else None, round(s['grm'], 2) if s['grm'] else None)
                     for s in newest if rule(s)][:PER_AREA]
    dates = [s['date'] for s in sales.values()]
    lines = ['"""Recent apartment building sales per area page. Generated by tools/costar_comps.py from CoStar exports;',
             'do not edit by hand."""', '',
             f'SOURCE = {"CoStar, sales from " + month(min(dates)) + " to " + month(max(dates))!r}', '',
             '# slug: [(address, neighborhood, units, year built, sale date, sale price, price per unit, price per SF, GRM)]', 'COMPS = {']
    for slug, rows in out.items():
        lines.append(f'    {slug!r}: [')
        lines += [f'        {r!r},' for r in rows]
        lines.append('    ],')
    lines.append('}')
    lines += ['', '# Every sale in the area over the period, not just the 15 shown:',
              '# count, total volume, median price, median $/unit, median units, median year built,',
              '# share built before 1979, median reported cap rate (None if under 3 reported), cap rates reported,',
              '# middle-half ranges (25th-75th percentile) of $/unit and cap rate (None if under 4 data points),',
              '# median and middle half of $/SF and GRM, with how many sales reported each',
              'STATS = {']
    lines += [f'    {k!r}: {v!r},' for k, v in stats.items()]
    lines.append('}')
    Path(__file__).resolve().parent.parent.joinpath('area_comps.py').write_text('\n'.join(lines) + '\n')
    print(f'{len(sales)} sales read')
    for slug, rows in out.items():
        print(f'  {slug:32} {len(rows):2}  {rows[-1][4] if rows else ""}')


if __name__ == '__main__':
    main(sys.argv[1:])
