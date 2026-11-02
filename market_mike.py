"""Mike Torres's closed sales in his ZIP codes (90035, 90036, 90046, 90048, 90069).

Source: CoStar export of team closings, Nov 2026. Built year = 2026 minus CoStar's age.
"""

# Property, submarket, units, built, sale price, $/unit
CLOSINGS = [
    ('210 S Fuller Ave', 'Hancock Park', 8, 1930, '$3,225,000', '$403,100'),
    ('1128 Larrabee St', 'West Hollywood', 6, 1951, '$2,450,000', '$408,300'),
    ('630 S Cochran Ave', 'Miracle Mile', 12, 1927, '$2,100,000', '$175,000'),
    ('1647 S Holt Ave', 'Pico-Robertson', 2, 1930, '$1,725,000', '$862,500'),
    ('8553 Alcott St', 'Pico-Robertson', 8, 1930, '$1,600,000', '$200,000'),
]
TOTAL = ('Total', '', 36, '', '$11,100,000', '$308,333 avg')
CAPTION = 'Closed apartment building sales in West Hollywood, Hancock Park, Miracle Mile and Pico-Robertson'
