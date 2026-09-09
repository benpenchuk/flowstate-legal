# FlowState — legal pages

Public hosting for the [FlowState](https://github.com/benpenchuk/FlowState) iOS app's privacy
policy. Separate from the app repo so that repo can stay private while these pages stay
reachable.

- **Privacy policy:** https://benpenchuk.github.io/flowstate-legal/privacy.html

## Editing

`privacy.md` is the source of truth. Edit it, then regenerate:

```bash
python3 build.py
```

That writes the `.html` files, which are what GitHub Pages serves. There is no Jekyll and no
build step on GitHub's side — `.nojekyll` tells Pages to serve the files verbatim — so the
page cannot break because of a build pipeline. The App Store needs this URL to keep resolving
for as long as the app is listed.

Commit both the `.md` and the regenerated `.html`.
