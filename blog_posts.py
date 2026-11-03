"""Blog posts. Edit this file to publish a post, then rerun build_team.py.

Each post becomes its own page at blog-<slug>.html and a card on blog.html. Newest first.

Body blocks:
    'text'                      a paragraph
    ('h2', 'Heading')           a subheading
    ('pull', 'A line to set off')  the left-ruled emphasis line used on the area pages
    ('ul', ['item', 'item'])    a bulleted list
**bold** works inside a paragraph, a pull line and a list item.
"""

POSTS = [
    {
        'slug': 'rso-value-add-yield-on-cost',
        'title': 'Why a 1996 Price Does Not Mean a 2006 Buyer Overpaid',
        'dek': 'Purchase prices, going-in GRMs and going-in cap rates describe the terms of entry. '
               'They say almost nothing about the yield on cost an RSO operator actually achieved.',
        'date': '2026-11-03',
        'author': 'Robert Carlile',
        'author_title': 'Senior Partner',
        'author_page': 'team-robert-carlile.html',
        'body': [
            'Just because prices are back to 1996 levels today does not mean those of you who bought '
            'between 1997 and 2019 overpaid.',

            ('h2', 'Why RSO properties repriced'),

            'One reason rent-stabilized properties have repriced so dramatically is that the cost of '
            'repositioning a rent-controlled apartment has become absurdly high. That cost is not only the '
            'construction bid. It is the buyout, the permitting timeline, the carry while a unit sits empty, '
            'and the legal exposure that now attaches to each of those steps. Buyers underwrite all of it, '
            'and the price they are willing to pay reflects it.',

            'But it was not always this way. Operators who bought years ago renovated at a fraction of '
            "today's cost, and, importantly, without incurring all of today's many risks and pitfalls. They "
            'captured the rental upside, and they have been enjoying the resulting cash flow, and a high '
            'yield on cost, for years.',

            ('h2', 'Value already extracted does not get clawed back'),

            ('pull', "A decline in an asset's market value does not undo all of the economic value an "
                     'operator has already extracted from it.'),

            'This is the part that gets lost when owners compare notes on where the market is today. The '
            'rent an operator collected in 2012, and in every year since, was banked. The debt that got paid '
            'down with it is paid down. The basis that was set at acquisition and renovation is fixed. None '
            'of that reverses because the next buyer will pay less per unit than the last one did.',

            ('h2', 'What going-in metrics actually tell you'),

            'So be wary of comparisons of purchase prices, going-in GRMs and going-in cap rates across years '
            'or decades. Those metrics tell you very little about the yield on cost an operator ultimately '
            'achieved. They are a snapshot of the day the deal closed, taken before any of the work that '
            'determines the outcome has happened.',

            'Yield on cost is the number that settles the question, and it is driven by three things, only '
            'one of which appears in a going-in cap rate:',

            ('ul', [
                '**What was paid** for the building.',
                '**What it cost to reposition it**, including everything that was spent to get a unit from a '
                'stabilized rent to a market rent.',
                '**What market rent turned out to be** once the work was done, and how long it held.',
            ]),

            'Two buildings bought in the same year at the same going-in cap rate can end up hundreds of basis '
            'points apart on yield on cost, because the second and third items moved and the first one never '
            'changed. A buyer in 2006 who turned units for a fraction of what a turn costs today, into a '
            'rental market that then ran for a decade, can be far ahead of a buyer who paid a lower price '
            'more recently and has yet to spend a dollar on repositioning.',

            ('h2', 'If you own one of these buildings today'),

            'The decision to hold or sell should be run off your own basis and your actual yield on cost, '
            'not off a headline price per unit from a nearby sale. A number that looks like a loss against '
            "today's comparable sales can still be a strong outcome against what you have in the building "
            'and what it has paid you since.',

            'We track ownership, rent regulation exposure and sales at the building level across our '
            'coverage areas, which is what it takes to answer this properly rather than by county average. '
            'If you want the figures on your own building, including what you are into it for against what '
            'it would bring today, ask us for a valuation.',
        ],
    },
]
