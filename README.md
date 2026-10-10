# FlowState — website and legal pages

Public site for the [FlowState](https://github.com/benpenchuk/FlowState) iOS app, separate from the
app repo so that repo can stay private while these pages stay reachable.

- **Home:** https://flowstatefit.app/
- **Privacy policy:** https://flowstatefit.app/privacy
- **Support:** https://flowstatefit.app/support
- **Old privacy URL, still live because the app links to it:**
  https://benpenchuk.github.io/flowstate-legal/privacy.html

## Editing

`index.md`, `support.md` and `privacy.md` are the sources. Edit one, then regenerate:

```bash
python3 -B build.py
```

That writes the `.html` files, which are what both hosts serve. `style.css` is the one shared
stylesheet, and `icon.png` / `icon-dark.png` are the app icon (the favicon and the page mark).
There is no Jekyll and no build step on either host. `.nojekyll` tells GitHub Pages to serve the
files verbatim, and `vercel.json` turns on `cleanUrls` so `/privacy` and `/support` work without
`.html`. Every link between pages is relative, so the GitHub Pages copy under `/flowstate-legal/`
keeps working. The App Store needs the privacy URL to keep resolving for as long as the app is
listed.

Front matter on a page can set `title`, `description` and `layout` (`home` or `doc`). The home
layout also reads `tagline`, `lede` and `status` for the top of the page.

The contact address is set once, as `CONTACT` in `build.py`. Write `{{contact}}` in the Markdown
and it becomes a mailto link, or `{{mailto}}` for a bare `mailto:` URL. `[Text](url){.button}`
draws a link as a button. Indented lines under a bullet continue that bullet. The privacy policy
and the support page both use the constant, so switching to an alias is a one-line edit.

Commit both the `.md` and the regenerated `.html`.
