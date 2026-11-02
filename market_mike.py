"""Mike Torres's closed sales in his ZIP codes (90035, 90036, 90046, 90048, 90069, 90731).

Source: CoStar export of team closings, Nov 2026. Built year = 2026 minus CoStar's age.
1224 S Mesa St (San Pedro, 90731) is from the team's MLS export (MLS 25589019), added Nov 2026.
"""

# Property, submarket, ZIP, units, built, sale price, $/unit
CLOSINGS = [
    ('210 S Fuller Ave', 'Hancock Park', '90036', 8, 1930, '$3,225,000', '$403,100'),
    ('1128 Larrabee St', 'West Hollywood', '90069', 6, 1951, '$2,450,000', '$408,300'),
    ('630 S Cochran Ave', 'Miracle Mile', '90036', 12, 1927, '$2,100,000', '$175,000'),
    ('1647 S Holt Ave', 'Pico-Robertson', '90035', 2, 1930, '$1,725,000', '$862,500'),
    ('8553 Alcott St', 'Pico-Robertson', '90035', 8, 1930, '$1,600,000', '$200,000'),
    ('1224 S Mesa St', 'San Pedro', '90731', 5, 1922, '$975,000', '$195,000'),
]
TOTAL = ('Total', '', '', 41, '', '$12,075,000', '$294,512 avg')
CAPTION = 'Closed apartment building sales in West Hollywood, Hancock Park, Miracle Mile, Pico-Robertson and San Pedro'
