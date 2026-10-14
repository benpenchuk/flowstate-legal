# FlowState — website and legal pages

Public site for the [FlowState](https://github.com/benpenchuk/FlowState) iOS app, separate from the
app repo so that repo can stay private while these pages stay reachable.

- **Home:** https://flowstatefit.app/
- **Privacy policy:** https://flowstatefit.app/privacy
- **Support:** https://flowstatefit.app/support
- **Old privacy URL, still live because the app links to it:**
  https://benpenchuk.github.io/flowstate-legal/privacy.html

## Editing

There are two kinds of page.

**The home page is hand-written.** `index.html` (the markup), `home.css` (the styles), `home.js`
(a small script for scroll reveals, the rest clock and the "log a set" demo), `mark.png` (the brand
mark, drawn as a Flame-coloured CSS mask), `fonts/` (Nunito, SIL OFL, latin variable woff2 plus its
licence; Safari on Apple devices uses its own SF Rounded and does not download it) and `og.png` (the link
preview). Edit those files directly. `build.py` does not touch `index.html`. The page has no build
step, no framework and makes no request to any other origin. Everything is visible without JavaScript
or with reduced motion; the script only adds motion, and hides nothing until it is running. The page
has no call-to-action button for now (Ben, 2026-10-13); the hero and the closing section say "private
beta" only. The `.btn` styles are kept for when one returns: a waitlist, then the App Store link.

**`support.md` and `privacy.md` are rendered.** They are the sources; edit one, then regenerate:

```bash
python3 -B build.py
```

That writes `support.html` and `privacy.html`, which are what both hosts serve. `style.css` is their
stylesheet, and `icon.png` / `icon-dark.png` are the app icon (the favicon and the touch icon).
`privacy.html`, `privacy.md`, `support.html`, `support.md` and `style.css` are what the App Store's
registered privacy URL points at: change them only on purpose.

There is no Jekyll and no build step on either host. `.nojekyll` tells GitHub Pages to serve the
files verbatim, and `vercel.json` turns on `cleanUrls` so `/privacy` and `/support` work without
`.html`. Every link and asset path is relative, so the GitHub Pages copy under `/flowstate-legal/`
keeps working. The App Store needs the privacy URL to keep resolving for as long as the app is
listed.

Front matter on a document page can set `title` and `description`.

The contact address is set once, as `CONTACT` in `build.py`. Write `{{contact}}` in the Markdown
and it becomes a mailto link, or `{{mailto}}` for a bare `mailto:` URL. `[Text](url){.button}`
draws a link as a button. Indented lines under a bullet continue that bullet. The privacy policy
and the support page both use the constant, so switching to an alias is a one-line edit.

Commit both the `.md` and the regenerated `.html`.
