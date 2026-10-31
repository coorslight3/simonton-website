"""Content for site/about.html (built by build_team.py). **bold** marks bold text.

The page argues the territory model: brokers are assigned by geography rather than by
product type. TERRITORIES below must be confirmed with Robert before launch.
"""

TITLE = 'About Us | Simonton Commercial Group, RE/MAX One Commercial'
DESC = ('Nine multifamily brokers, each assigned their own Los Angeles submarkets. See who covers '
        'your neighborhood and why a specialist prices and sells an apartment building better than a generalist.')

# Hero, above the fold.
HEADLINE = 'We do not cover Los Angeles. We cover your block.'

LEAD = [
    'Almost every multifamily broker in Los Angeles will tell you they cover Los Angeles. '
    'It is worth asking what that means in a county of eighty-eight cities, where an apartment '
    'building eight blocks from another can be worth a hundred thousand dollars more per unit.',
    'Nobody knows all of it. We decided to stop pretending otherwise.',
]

# The model.
MODEL_HEAD = 'One broker, one territory'
MODEL = [
    'The Simonton Commercial Group is nine commercial real estate professionals at RE/MAX One '
    'Commercial in Santa Monica. Chase Simonton, Vice President of Multifamily Investments, founded '
    'the team in 2014 and built it around one structural decision: **our brokers are assigned by '
    'geography, not by product type, not by seniority, and not by whoever answers the phone.**',
    'Each member owns a defined set of submarkets. Inside that territory, the standard is not '
    'familiarity. It is a record on every apartment building: the unit mix, the year built, how it is '
    'owned, when it last traded, what the owner paid, the assessed basis, and whether it falls under '
    'rent stabilization. Give one of our brokers an address in their territory and they are not '
    'starting from scratch.',
    'In Palms, Mar Vista and Mid City, for example, that record covers all **4,141 apartment buildings '
    'and 41,210 units** across the six ZIP codes. The same discipline applies across the rest of the team.',
]

# Why it matters to the owner. (heading, body) pairs, rendered as cards.
BENEFITS = [
    ('Your building gets priced, not estimated.',
     'Adjacent submarkets price very differently, and the spread inside a single one is wider still. '
     'A valuation built on Westside averages can be off by hundreds of thousands of dollars on a '
     'ten-unit building. A broker who sells only in your pocket knows what the last six comparable '
     'buildings actually traded for and why two of them should be thrown out.'),
    ('The buyer is already known.',
     'Working one market continuously means knowing who closed there last quarter, who is sitting in a '
     '1031 window, and who has been waiting two years for a particular street. That is what gets a '
     'building sold at the top of its range instead of to whoever happened to see the listing.'),
    ('Off-market works both directions.',
     'Years in the same few square miles produce relationships that a countywide broker never builds. '
     'For sellers that means a quiet sale when discretion matters. For buyers it means buildings that '
     'never reach the open market.'),
    ('You will be told not to sell.',
     'A broker who needs any transaction will find a reason to list. A broker whose reputation lives or '
     'dies in six ZIP codes, and who expects to be talking to the same owners in ten years, will tell you '
     'when holding is the better financial decision.'),
]

# The team layer.
TEAM_HEAD = 'Narrow individually, deep together'
TEAM = [
    'Specialization only works if the specialists talk. Our brokers share market intelligence, buyer '
    'relationships and transaction experience across the whole team, which means a listing in one '
    'territory is exposed to every buyer any of us knows.',
    'The result is the combination that is normally unavailable: an individual broker who genuinely knows '
    'your neighborhood, backed by the buyer pool and transaction volume of an entire team.',
    'Our work goes beyond listing and selling. We handle acquisitions and dispositions, broker opinions of '
    'value, 1031 exchange timing, financial underwriting, value-add and development analysis, and portfolio '
    'strategy, whether that is an owner selling a building held for three generations or an investor placing '
    'exchange funds before a deadline.',
]

# Coverage map section.
MAP_HEAD = 'Who covers your neighborhood'
MAP_INTRO = ('Our territories span Los Angeles County north of El Segundo, excluding Glendale. Select a broker '
             'to see their area, or click any ZIP code to find out who covers it.')
MAP_NOTE = ('Boundaries are Census ZIP Code Tabulation Areas, simplified for display. Territory assignments '
            'reflect broker focus areas and are not exclusive listing rights.')

# DRAFT, needs Robert's confirmation. (broker, submarkets) in team display order.
TERRITORIES = [
    ('Chase Simonton', 'Team lead, countywide'),
    ('Zvon Jedvaj',    'West Los Angeles, Downtown Los Angeles'),
    ('Andrew Wong',    'Santa Monica, Venice, Brentwood, Westwood, Culver City'),
    ('Robert Carlile', 'Palms, Mar Vista, Mid City'),
    ('John Sarna',     'Silver Lake, Echo Park, Los Feliz'),
    ('Mike Torres',    'Hollywood'),
    ('Brett Carlile',  'Pico-Robertson, Mid-Wilshire'),
    ('Josh Merrin',    'Sherman Oaks, Studio City, North Hollywood, Van Nuys, Valley Village'),
    ('Koby Sarna',     'To be assigned'),
]

CLOSE = [
    '**Narrowness is the strategy, not a limitation.** We would rather be the broker an owner in Mar Vista '
    'calls first than the ninth name on a countywide list.',
]

# ---- Profile-page link to this page's territory map --------------------------------------------
# Agent ids must match AGENTS in site/coverage-map.html. `shown` gates the button on each broker's
# profile page: switch it to True once that broker's `zips` are filled in on the map, otherwise the
# button would land the visitor on an empty territory.
MAP_AGENTS = {
    'Chase Simonton': ('cs', True),    # countywide, no ZIP list
    'Zvon Jedvaj':    ('zj', False),
    'Andrew Wong':    ('aw', False),
    'Robert Carlile': ('rc', True),
    'John Sarna':     ('js', False),
    'Mike Torres':    ('mt', False),
    'Brett Carlile':  ('bc', False),
    'Josh Merrin':    ('jm', False),
    'Koby Sarna':     ('ks', False),
}
COUNTYWIDE = {'Chase Simonton'}
MAP_LABEL            = "See {first}'s territory"
MAP_LABEL_COUNTYWIDE = "See {first}'s countywide coverage"
