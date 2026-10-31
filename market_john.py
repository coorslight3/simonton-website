"""Closings and page settings for John Sarna's market page (rendered by broker_market.py)."""

PATH = 'apartment-broker/los-feliz-silver-lake-echo-park-studio-city-sherman-oaks/'

NAME = 'John Sarna'
PHOTO = 'john-sarna-1.jpg'
AREA_NAMES = 'Los Feliz, Silver Lake, Echo Park, Studio City & Sherman Oaks'
TITLE = f'Multifamily Broker for {AREA_NAMES} | John Sarna, RE/MAX One Commercial'
DESC = ('Multifamily broker John Sarna sells apartment buildings in Los Feliz, Silver Lake, Echo Park, '
        'Studio City and Sherman Oaks. Closed sales and free valuations.')
H1 = f'Multifamily Broker for {AREA_NAMES}'

# (property, area, units, sale price) in the order given; the page sorts by price.
CLOSINGS = [
    ('1717-1725 Park Ave', 'Echo Park', 36, 7350000),
    ('2809 W 8th St', 'Koreatown', 24, 2205000),
    ('4221 Burns Ave', 'Virgil Village', 28, 5950000),
    ('1846 Silver Lake Blvd', 'Silver Lake', 6, 1550000),
    ('13412 Vanowen St', 'Van Nuys', 17, 2350000),
    ('4120-4124 Normal Ave', 'Virgil Village', 20, 5800000),
    ('4462 Murietta Ave', 'Sherman Oaks', 21, 4950000),
    ('604 Venice Way', 'Inglewood', 6, 1640000),
    ('10020 Zelzah Ave', 'Northridge', 50, 15700000),
    ('15405 Vanowen St', 'Van Nuys', 30, 4550000),
    ('7460 Canby Ave', 'Reseda', 9, 1505000),
    ('6525 Sepulveda Blvd', 'Van Nuys', 8, 1250000),
    ('3916-3920 Kentucky Dr', 'Studio City', 12, 2740000),
    ('1242 N New Hampshire Ave', 'Hollywood', 14, 2135000),
    ('1747 N Kingsley Dr', 'Los Feliz', 20, 6375000),
    ('1501-1509 Bellevue Ave', 'Echo Park', 10, 2000000),
    ('4351 Normal Ave', 'Virgil Village', 12, 2100000),
    ('11848 Oxnard St - 5591 Carpenter Ave', 'North Hollywood', 14, 2750000),
    ('331 S Harvard Blvd', 'Koreatown', 10, 2075000),
    ('111 N Normandie Ave', 'Koreatown', 14, 2425000),
    ('14217 Vanowen St', 'Van Nuys', 6, 1300000),
    ('4071 Melrose Ave', 'Virgil Village', 6, 1385000),
    ('5666 Fountain Ave', 'Hollywood', 8, 2270000),
    ('1245 N Harvard Blvd', 'Hollywood', 7, 1750000),
    ('1028 N Ardmore Ave', 'Hollywood', 12, 2000000),
    ('5446 Romaine St', 'Hollywood', 8, 1550000),
    ('1724 El Cerrito Pl', 'Hollywood', 8, 3800000),
    ('1528 N Hobart Blvd', 'Hollywood', 12, 3600000),
    ('1602-1606 N Bush St', 'Santa Ana', 3, 1530000),
    ('1002 N Mariposa Ave', 'Hollywood', 30, 3600000),
]

# Areas John covers (from his profile) -> existing area pages
AREAS = ['los-feliz', 'silver-lake', 'echo-park', 'studio-city', 'sherman-oaks']

CTA_H = 'Free Valuation on Your Apartment Building'
CTA_P = ('Send the address and a rent roll and John will come back with a written valuation, the comparable '
         'sales behind it, and an honest read on the market for your building.')
