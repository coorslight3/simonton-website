# Simonton Commercial website

A static website (plain HTML, CSS and JavaScript) for the Simonton Commercial Group at RE/MAX One Commercial.
The published site is the `site/` folder. Many pages are generated from data files, so edit the **source** files below, not the generated pages.

## Quick start (just to look at the site)
1. Unzip the folder.
2. Mac: double-click `Start-Preview.command` (if macOS blocks it, right-click it and choose Open). Windows: double-click `Start-Preview.bat`.
3. The site opens at http://localhost:8123. Close the black window to stop it.
This needs Python 3 only. To edit and rebuild pages you also need Node.js (see below).

## What you need
- Python 3 and Node.js installed (Node is only used to read `site/team-data.js`).

## Preview and rebuild
```bash
python3 build_team.py     # regenerates the generated pages after you edit content
python3 serve.py          # preview at http://localhost:8123 (never caches)
```

## Where content lives
| To change... | Edit this | Then |
|---|---|---|
| A team member's title, bio, phone, email, DRE, order | `site/team-data.js` | run `build_team.py` |
| About Us page text | `about_page.py` | run `build_team.py` |
| Area pages (Venice, Silver Lake, Downtown LA...) and the "Areas We Serve" list | `areas_content.py` | run `build_team.py`, then refresh the footer/menu list (see CLAUDE.md) |
| Robert's market page | `market_robert.py` | run `build_team.py` |
| John's market page and closings | `market_john.py` | run `build_team.py` |
| Home page, header menu, footer, Chase "Meet The Team" band | `site/index.html` | run `build_team.py` (it copies the header/footer to every page) |
| 1031, Blog, FAQs and Contact page sections | `content/*.html` | run `build_team.py` |
| Closings list (124 sales from the MLS) | `site/closings-data.js` | none |
| Colors, spacing, layout | `site/styles.css` | none |
| Site behavior (menu, chat, forms) | `site/script.js` | none |

## Forms
The valuation, contact and subscribe forms email chase@remaxonecommercial.com through Web3Forms.
The access key is the `FORM_KEY` constant at the top of `site/script.js`.

## Publishing
Drag the `site/` folder to a static host (for example Netlify Drop) or connect this repository to Netlify or Cloudflare Pages
with the publish folder set to `site`. Run `python3 build_team.py` first so the generated pages are up to date.
