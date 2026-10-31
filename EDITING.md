# How to change the website

You do not need to install anything. Every change below is made by editing a file in
GitHub in your web browser. Saving the file publishes the site automatically, and the
new version is live in about a minute.

## The one rule

**Never edit a page that ends in `.html` inside `site/`** (except `site/index.html`).
Those pages are *built* from the files below, so an edit there is thrown away on the
next publish. Edit the source, and the page rebuilds itself.

## Where to change what

| To change | Edit this file |
|---|---|
| Someone's title, phone, email, DRE, bio, or the order people appear in | `site/team-data.js` |
| The About Us page wording | `about_page.py` |
| An area page, or the "Areas We Serve" menu | `areas_content.py` |
| Robert's market page content | `market_robert.py` |
| John's market page content and closings | `market_john.py` |
| The 1031, Blog, FAQs or Contact page text | `content/` folder |
| The home page, top menu, or footer | `site/index.html` |
| The closings list | `site/closings-data.js` |
| Who covers which ZIP codes on the coverage map | `site/coverage-map.html`, the `AGENTS` list near the top |
| Colours, fonts, spacing | `site/styles.css` |

## How to make a change

1. Open the file on GitHub and click the pencil icon.
2. Make your edit. Keep the punctuation and quote marks exactly as they are: these are
   data files, and a missing quote or comma will stop the site building.
3. Scroll down, write one line describing the change, and click **Commit changes**.
4. Wait about a minute, then reload the site.

## If the site does not update

The build probably failed, which almost always means a typo in a data file. On GitHub,
open the **Actions** tab (or the Cloudflare Pages dashboard) and look at the most recent
run: the error names the file and line. The previous version stays live in the meantime,
so a mistake never takes the site down.

## If you both edit at once

GitHub will not let one of you silently overwrite the other. If you edit the same file at
the same time it will say so and ask you to resolve it. Every past version is kept, so any
change can be undone.

## House rules for this site

- Black and white only. The exception is team photos, which are in colour and turn black
  and white on hover, and the coverage map, which needs colour to tell territories apart.
- Use the client's own wording for bios, area copy and market figures. Do not invent
  facts, statistics or contact details.
- No em dashes. Use commas, colons or full stops.
- Team emails follow `firstname@remaxonecommercial.com`.

To work on this locally with full preview and Claude Code, see `SETUP.md`.
More detail for whoever maintains the code is in `README.md` and `CLAUDE.md`.
