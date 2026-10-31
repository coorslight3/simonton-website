const $ = (s, r = document) => r.querySelector(s);

$('#year').textContent = new Date().getFullYear();

$('.topbar-close').addEventListener('click', () => $('#topbar').classList.add('hide'));

const toggle = $('.nav-toggle');
const nav = $('#nav');
const setNav = open => {
  nav.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
};
toggle.addEventListener('click', () => setNav(!nav.classList.contains('open')));
nav.addEventListener('click', e => { if (e.target.closest('a')) setNav(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setNav(false); });

// Forms email chase@remaxonecommercial.com through Web3Forms.
// Paste the access key (emailed to that address by web3forms.com) below to turn them on.
const FORM_KEY = 'c381dbb0-cb35-4388-8820-787174883e82';

document.querySelectorAll('form[data-form]').forEach(f => {
  const msg = $('.form-msg', f);
  f.addEventListener('submit', async e => {
    e.preventDefault();
    if (!FORM_KEY) { msg.textContent = 'Thanks! (Demo mode: form email is not switched on yet.)'; return; }
    const btn = $('button[type=submit]', f);
    btn.disabled = true;
    msg.textContent = 'Sending...';
    const data = new FormData(f);
    data.append('access_key', FORM_KEY);
    data.append('subject', f.dataset.subject);
    data.append('from_name', 'Simonton Commercial website');
    try {
      const r = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: data });
      const j = await r.json();
      if (!j.success) throw new Error(j.message);
      msg.textContent = 'Thank you! We received your request and will be in touch soon.';
      f.reset();
    } catch {
      msg.textContent = 'Sorry, something went wrong. Please call or text us instead.';
    } finally {
      btn.disabled = false;
    }
  });
});

// Recent Closings (data from closings-data.js; photos from assets/closings/<MLS>.jpg when present)
(() => {
  const data = window.CLOSINGS || [];
  const grid = $('#closings-grid');
  if (!grid) return;
  const PAGE = 12;
  let shown = PAGE;
  const usd = n => '$' + n.toLocaleString('en-US');
  const volume = data.reduce((s, d) => s + d.price, 0);
  if ($('#stat-vol')) {
    $('#stat-vol').textContent = '$' + Math.floor(volume / 1e6) + 'M+';
    $('#stat-count').textContent = data.length + '+';
  }

  const city = $('#f-city'), units = $('#f-units'), sort = $('#f-sort'), more = $('#closings-more');
  [...new Set(data.map(d => d.city))].sort().forEach(c => city.add(new Option(c, c)));

  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function render() {
    let list = data.filter(d => !city.value || d.city === city.value);
    if (units.value) { const [a, b] = units.value.split('-').map(Number); list = list.filter(d => d.units >= a && d.units <= b); }
    list.sort((a, b) => sort.value === 'units' ? b.units - a.units : sort.value === 'dom' ? a.dom - b.dom : b.price - a.price);
    $('#closings-count').textContent = list.length + ' closings';
    grid.innerHTML = list.slice(0, shown).map(d => `
      <article class="closing">
        <div class="ph" data-mls="${esc(d.mls)}"><span>Sold</span></div>
        <div class="closing-body">
          <h3>${esc(d.address)}</h3>
          <p class="loc">${esc(d.city)}, CA</p>
          <dl>
            <div><dt>Units</dt><dd>${d.units}</dd></div>
            <div><dt>Sold</dt><dd>${usd(d.price)}</dd></div>
            ${d.cap ? `<div><dt>Cap rate</dt><dd>${d.cap.toFixed(2)}%</dd></div>` : ''}
            <div><dt>Days on market</dt><dd>${d.dom}</dd></div>
          </dl>
        </div>
      </article>`).join('');
    // Swap in a photo if one exists for this MLS number; otherwise keep the placeholder.
    grid.querySelectorAll('.ph[data-mls]').forEach(el => {
      const img = new Image();
      img.alt = '';
      img.decoding = 'async';
      img.onload = () => { el.replaceChildren(img); el.classList.add('has-img'); };
      img.src = `assets/closings/${encodeURIComponent(el.dataset.mls)}.jpg`;
    });
    more.hidden = list.length <= shown;
  }
  [city, units, sort].forEach(el => el.addEventListener('change', () => { shown = PAGE; render(); }));
  more.addEventListener('click', () => { shown += PAGE; render(); });
  render();
})();

// Team grid on the home page (data from team-data.js); each card links to that person's page.
(() => {
  const team = window.TEAM || [];
  const grid = $('#team-grid');
  if (!grid) return;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const slug = n => n.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  grid.innerHTML = team.map(p => `
    <a class="member" href="team-${slug(p.name)}.html">
      <img src="assets/team/${esc(p.photo)}" alt="${esc(p.name)}" loading="lazy">
      <span class="team-cap"><strong>${esc(p.name)}</strong><span>${esc(p.short || p.title)}</span><em>View profile</em></span>
    </a>`).join('');
})();

// Chat bubble: an automated assistant answers common questions, then hands off to a real person by text.
(() => {
  const btn = $('#chat-btn'), panel = $('#chat-panel');
  if (!btn) return;
  const PHONE = '+13108715380', PHONE_LABEL = '(310) 871-5380';
  const root = (document.querySelector('meta[name=site-root]') || {}).content || '';
  const base = $('#listings') ? '' : root + 'index.html';
  const log = $('#chat-log'), quick = $('#chat-quick'), form = $('#chat-form'), input = $('#chat-input');

  const sep = /iPhone|iPad|iPod/.test(navigator.userAgent) ? '&' : '?';
  const smsHref = text => `sms:${PHONE}${sep}body=${encodeURIComponent(text)}`;
  $('#chat-sms').href = smsHref('Hi, I found you on your website and would like to speak with someone.');

  const topics = {
    sell: { q: 'Sell my building', keys: ['sell', 'selling', 'list', 'listing my', 'apartment building', 'owner'],
      a: 'We specialize in selling apartment buildings in Los Angeles. The best first step is a free, confidential valuation.', link: ['#valuation', 'Request a free valuation'] },
    value: { q: 'Free valuation', keys: ['value', 'valuation', 'worth', 'price', 'pricing', 'cap rate'],
      a: 'Tell us about your property and we will follow up with a confidential opinion of value.', link: ['#valuation', 'Request a free valuation'] },
    x1031: { q: '1031 exchange', keys: ['1031', 'exchange', 'tax', 'defer'],
      a: 'We help multifamily owners plan the sale and find a replacement property for a 1031 exchange. This is not tax or legal advice, so please check with your tax professional.', link: ['1031-exchanges.html', 'About 1031 exchanges'], abs: true },
    listings: { q: 'Current listings', keys: ['listing', 'listings', 'for sale', 'buy', 'available', 'property', 'properties'],
      a: 'You can see our current listings and what is in escrow on the listings section.', link: ['listings.html', 'View listings'], abs: true },
    closings: { q: 'Recent closings', keys: ['closing', 'closings', 'sold', 'track record', 'experience'],
      a: 'Browse our recent closings, with filters by city and building size.', link: ['closings.html', 'View closings'], abs: true },
    team: { q: 'Meet the team', keys: ['team', 'agent', 'broker', 'who'],
      a: 'Meet the brokers on our team and read their bios.', link: ['team.html', 'Meet the team'], abs: true }
  };
  const person = { q: 'Talk to a real person', keys: ['person', 'human', 'agent', 'call', 'text', 'phone', 'contact', 'speak', 'talk', 'representative', 'someone'] };

  const add = (who, html) => {
    const d = document.createElement('div');
    d.className = 'msg ' + who;
    d.innerHTML = html;
    log.appendChild(d);
    log.scrollTop = log.scrollHeight;
  };
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function handoff(userText) {
    add('bot', `Happy to connect you with a real person. Tap below to text our team at ${PHONE_LABEL}.`);
    const msg = userText ? `Hi, I found you on your website. ${userText}` : 'Hi, I found you on your website and would like to speak with someone.';
    add('bot', `<a class="chat-link" href="${smsHref(msg)}">Text ${PHONE_LABEL}</a> <a class="chat-link alt" href="tel:${PHONE}">Call</a>`);
  }
  function answer(t) {
    const text = t.toLowerCase();
    if (person.keys.some(k => text.includes(k))) return handoff(t);
    const hit = Object.values(topics).find(x => x.keys.some(k => text.includes(k)));
    if (hit) {
      const href = hit.abs ? root + hit.link[0] : base + hit.link[0];
      add('bot', `${esc(hit.a)} <a class="chat-link" href="${href}">${esc(hit.link[1])}</a>`);
    } else {
      add('bot', 'I am not sure about that one. I can point you to a topic below, or connect you with a real person.');
    }
  }

  function renderQuick() {
    quick.innerHTML = '';
    [...Object.values(topics).slice(0, 4), person].forEach(x => {
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = x.q;
      b.addEventListener('click', () => { add('user', esc(x.q)); x === person ? handoff('') : answer(x.q); });
      quick.appendChild(b);
    });
  }

  let started = false;
  const set = open => {
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    if (open) {
      if (!started) {
        started = true;
        add('bot', 'Hi! I am an automated assistant for Simonton Commercial. Ask me a question or pick a topic, and I can connect you with a real person any time.');
        renderQuick();
      }
      input.focus();
    }
  };
  btn.addEventListener('click', () => set(panel.hidden));
  $('#chat-x').addEventListener('click', () => { set(false); btn.focus(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) { set(false); btn.focus(); } });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const t = input.value.trim();
    if (!t) return;
    add('user', esc(t));
    input.value = '';
    answer(t);
  });
})();

// "Sign up" in the top bar jumps to the footer Subscribe form; put the cursor in the email field.
(() => {
  const form = $('#subscribe');
  if (!form) return;
  const focusEmail = () => { if (location.hash === '#subscribe') setTimeout(() => $('input[name=email]', form).focus({ preventScroll: true }), 400); };
  window.addEventListener('hashchange', focusEmail);
  focusEmail();
})();

// Team directory: cursor-following light on each card, and a staggered reveal on scroll.
(() => {
  const sec = $('.ft');
  if (!sec) return;
  const cards = [...sec.querySelectorAll('.ft-card')];
  cards.forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    c.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }));
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  sec.classList.add('ft-ready');
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }), { threshold: 0.12 });
  cards.forEach(c => io.observe(c));
})();

// Hero background video. Starts automatically on larger screens; people who prefer reduced motion
// (or Data Saver) get the still image plus a Play button. A Pause/Play button is always available.
(() => {
  const v = $('#hero-video');
  const hero = $('#top');
  if (!v || !hero || innerWidth < 768) return;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saver = navigator.connection && navigator.connection.saveData;

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'hero-toggle';
  hero.appendChild(btn);

  const label = playing => {
    btn.setAttribute('aria-pressed', String(playing));
    btn.innerHTML = playing
      ? '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg><span>Pause video</span>'
      : '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M7 4l13 8-13 8z"/></svg><span>Play video</span>';
  };
  const play = () => {
    if (!v.src) v.src = v.dataset.src;
    return v.play().then(() => label(true)).catch(() => label(false));
  };

  btn.addEventListener('click', () => { if (v.paused) play(); else { v.pause(); label(false); } });
  label(false);
  if (!calm && !saver) play();
})();

// "Areas We Serve" drop-down: click or hover to open; Escape or an outside click closes it.
(() => {
  const dd = $('.nav-dd');
  if (!dd) return;
  const btn = $('.nav-dd-btn', dd), menu = $('.nav-dd-menu', dd);
  const set = open => { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); };
  btn.addEventListener('click', () => set(menu.hidden));
  const hoverable = matchMedia('(hover: hover) and (min-width: 981px)');
  dd.addEventListener('mouseenter', () => { if (hoverable.matches) set(true); });
  dd.addEventListener('mouseleave', () => { if (hoverable.matches) set(false); });
  document.addEventListener('click', e => { if (!dd.contains(e.target)) set(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { set(false); btn.focus(); } });
  dd.addEventListener('focusout', e => { if (!dd.contains(e.relatedTarget)) set(false); });
})();
