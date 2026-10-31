# Notes for Claude (and anyone editing this project)

**Project history, decisions and the open to-do list live in `HANDOFF.md`**, which is kept outside this
repository (this repo is public). Ask Robert for it before making content decisions. `README.md` covers
the build, `EDITING.md` the browser workflow and `SETUP.md` local setup with Claude Code.

## How the site is built
- Published folder: `site/`. Static HTML/CSS/JS. No framework.
- `build_team.py` generates: `team.html`, `team-<name>.html`, `about.html`, the tab pages (`listings`, `closings`, `testimonials`,
  `1031-exchanges`, `blog`, `faqs`, `contact`), all area pages (`*-multifamily-broker.html`, the San Fernando Valley page),
  Robert's page and John's page under `site/apartment-broker/`. **Never hand-edit generated files; edit the source and rerun the build.**
- `site/index.html` is hand-edited. Its header and footer (including the Chase "Meet The Team" band) are copied to every page by the build.
- The "Areas We Serve" list appears in two places in `site/index.html` (header drop-down `nav-dd-menu` and footer `f-areas`).
  When adding an area in `areas_content.py` (`HOODS`/`FULL` and `ORDER`), regenerate both lists from `ORDER`.
- Asset links use a cache-busting `?v=NN` on `styles.css`/`script.js`. Bump the number everywhere when CSS or JS changes.

## Rules we've settled on
- Black and white palette only. Fonts: Archivo (headings) and DM Sans (body).
- Use the client's wording **verbatim** for bios, area text and market figures. Don't invent facts, stats or contact details,
  and don't guess emails (the pattern `firstname@remaxonecommercial.com` was confirmed by the client).
- Footer/Contact person is Chase Simonton. The chat bubble deliberately texts a different number, (310) 871-5380.
- Some stat tiles and the Blog/FAQ pages are awaiting final copy. Do not invent figures to fill them.
- Listings and closings come from MLS exports and are snapshots (as of Oct 2026). Photos are matched by MLS number.
- Accessibility matters: keep visible focus, labels on form fields, reduced-motion support, and 44px tap targets.

## Checking your work
- Run `python3 build_team.py` then `python3 serve.py` and open pages with a query string (e.g. `?r=1`) to avoid cached copies.
- Check desktop and phone widths and that all links resolve.
