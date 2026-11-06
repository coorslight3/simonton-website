"""Top of each team member's profile page. Every person has a different arrangement in the same style as
Mike Torres's and Robert Carlile's pages (those two stay in build_team.py). Bios are the client's wording."""
import html
import re

e = html.escape


def _bits(p, links):
    digits = re.sub(r'\D', '', p.get('phone') or '')
    return {
        'name': e(p['name']),
        'title': e(p['title']),
        'photo': f'assets/team/{e(p["photo"])}',
        'phone': e(p.get('phone') or ''),
        'tel': f'tel:+1{digits}',
        'email': e(p.get('email') or ''),
        'dre': e(p.get('dre') or ''),
        'bio': ''.join(f'<p>{e(t)}</p>' for t in p.get('bio', [])) or '<p>Full bio coming soon.</p>',
        'links': links,
    }


def _img(b):
    return f'<img src="{b["photo"]}" alt="{b["name"]}" width="800" height="960">'


def _back(dark=False):
    cls = 'back back-light' if dark else 'back'
    return f'<a class="{cls}" href="team.html">&larr; All Team Members</a>'


def _eyebrow():
    return '<p class="eyebrow">Simonton Commercial &middot; RE/MAX One Commercial</p>'


def _buttons(b, dark=True):
    """Stacked Call and Email buttons, the same ones as Mike's page."""
    solid, ghost = ('btn-light', 'btn-ghost') if dark else ('btn-dark', 'btn-ghost-dark')
    out = ''
    if b['phone']:
        out += f'<a class="btn {solid} pm-contact" href="{b["tel"]}"><span>Call</span>{b["phone"]}</a>'
    if b['email']:
        out += f'<a class="btn {ghost} pm-contact" href="mailto:{b["email"]}"><span>Email</span>{b["email"]}</a>'
    if not out:
        out = f'<a class="btn {ghost}" href="contact.html">Contact The Team</a>'
    return f'<div class="pm-actions">{out}</div>'


def _dre(b):
    return f'<p class="pl-dre">DRE #{b["dre"]}</p>' if b['dre'] else ''


def _links(b, dark=True):
    cls = 'btn-ghost' if dark else 'btn-ghost-dark'
    inner = ''.join(f'<a class="btn {cls}" href="{e(h)}">{e(l)} <span aria-hidden="true">&rarr;</span></a>' for h, l in b['links'])
    return f'<div class="pm-links">{inner}</div>' if inner else ''


def _about(b, cls=''):
    return f'''<section class="section pl-about {cls}">
  <div class="wrap"><h2>About {b["name"]}</h2><div class="pl-bio">{b["bio"]}</div></div>
</section>'''


def photo_right(b):
    """Chase: dark header with the photo on the right."""
    return f'''<section class="pl pl-dark pl-right">
  <div class="wrap">
    {_back(True)}
    <div class="pl-grid">
      <div>{_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>{_buttons(b)}{_dre(b)}{_links(b)}</div>
      <div class="pl-photo">{_img(b)}</div>
    </div>
  </div>
</section>
{_about(b)}'''


def white_compact(b):
    """Zvon: white header with a small photo and a rule, like Robert's page."""
    return f'''<section class="pl pl-white">
  <div class="wrap">
    {_back()}
    <div class="pl-grid">
      <div class="pl-photo">{_img(b)}</div>
      <div><h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>
        <p class="pl-contact"><a href="{b["tel"]}">{b["phone"]}</a><a href="mailto:{b["email"]}">{b["email"]}</a><span>DRE #{b["dre"]}</span></p>
        {_links(b, False)}</div>
    </div>
  </div>
</section>
{_about(b, 'pl-about-tight')}'''


def centered(b):
    """Andrew: everything centered, with one narrow column of bio."""
    return f'''<section class="pl pl-dark pl-center">
  <div class="wrap">
    {_back(True)}
    <div class="pl-photo">{_img(b)}</div>
    {_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>{_buttons(b)}{_dre(b)}{_links(b)}
  </div>
</section>
{_about(b, 'pl-about-center')}'''


def all_dark(b):
    """John: the whole intro is dark, with the bio beside the photo."""
    return f'''<section class="pl pl-dark pl-full">
  <div class="wrap">
    {_back(True)}
    {_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>
    <div class="pl-grid">
      <div><div class="pl-photo">{_img(b)}</div>{_buttons(b)}{_dre(b)}{_links(b)}</div>
      <div><h2>About {b["name"]}</h2><div class="pl-bio">{b["bio"]}</div></div>
    </div>
  </div>
</section>'''


def side_column(b):
    """Brett: white page, with the photo and buttons staying in a left column beside the bio."""
    return f'''<section class="pl pl-white pl-side">
  <div class="wrap">
    {_back()}
    <h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>
    <div class="pl-grid">
      <div class="pl-stick"><div class="pl-photo">{_img(b)}</div>{_buttons(b, False)}{_dre(b)}{_links(b, False)}</div>
      <div><h2>About {b["name"]}</h2><div class="pl-bio">{b["bio"]}</div></div>
    </div>
  </div>
</section>'''


def edge_photo(b):
    """Josh: the photo runs to the left edge of the screen, with the dark panel beside it."""
    return f'''<section class="pl pl-dark pl-edge">
  <div class="pl-photo">{_img(b)}</div>
  <div class="pl-edge-text">{_back(True)}{_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>{_buttons(b)}{_dre(b)}{_links(b)}</div>
</section>
{_about(b)}'''


def contact_bar(b):
    """Koby: white name header, a black contact bar, then the photo beside the bio."""
    return f'''<section class="pl pl-white pl-bar">
  <div class="wrap">
    {_back()}
    {_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>
  </div>
  <div class="pl-bar-strip"><div class="wrap"><a href="{b["tel"]}"><span>Call</span>{b["phone"]}</a><a href="mailto:{b["email"]}"><span>Email</span>{b["email"]}</a><p><span>DRE</span>#{b["dre"]}</p></div></div>
  <div class="wrap pl-grid">
    <div class="pl-photo">{_img(b)}</div>
    <div><h2>About {b["name"]}</h2><div class="pl-bio">{b["bio"]}</div>{_links(b, False)}</div>
  </div>
</section>'''


def soft_gray(b):
    """Rochelle: a light gray band with the details beside the photo."""
    return f'''<section class="pl pl-gray">
  <div class="wrap">
    {_back()}
    <div class="pl-grid">
      <div class="pl-photo">{_img(b)}</div>
      <div>{_eyebrow()}<h1>{b["name"]}</h1><p class="pl-title">{b["title"]}</p>{_buttons(b, False)}
        <div class="pl-bio">{b["bio"]}</div></div>
    </div>
  </div>
</section>'''


LAYOUTS = {
    'Chase Simonton': photo_right, 'Zvon Jedvaj': white_compact, 'Andrew Wong': centered, 'John Sarna': all_dark,
    'Brett Carlile': side_column, 'Josh Merrin': edge_photo, 'Koby Sarna': contact_bar, 'Rochelle Becker': soft_gray,
}


def render(p, links):
    return LAYOUTS[p['name']](_bits(p, links))
