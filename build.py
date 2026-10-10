"""Turn the Markdown pages into standalone HTML for the FlowState site.

No Jekyll, no build service, no dependencies. The output is plain HTML plus one stylesheet
(style.css) and the app icon, all linked by relative path, so it works on Vercel
(https://flowstatefit.app), GitHub Pages (the old /flowstate-legal/ address, which the app still
links to), or any static host. That matters because the App Store needs the privacy URL to keep
working for as long as the app is listed, and tying it to one host's build pipeline is how a
privacy policy 404s two years from now. Both hosts serve the committed .html files as they are.

Markdown stays the source of truth; this only renders it. Front matter keys (all optional):
title, description, layout (home or doc), and for the home layout: tagline, lede, status.

    python3 -B build.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# The one place the contact address lives. Markdown uses the {{contact}} token (the policy and
# the support page), so switching to an alias later is a one-line edit.
CONTACT = "ben@penchuk.com"

# The public address. Used only for the canonical and social-preview URLs; every link between
# pages is relative, so the old GitHub Pages copy keeps working.
SITE = "https://flowstatefit.app"

# Used when a page has no description of its own in its front matter.
DEFAULT_DESCRIPTION = "FlowState is a strength training log for iPhone."
DESCRIPTIONS = {"privacy": "How FlowState handles your data."}

# Markdown files that are repo docs, not published pages.
NOT_PAGES = {"README.md"}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#f7f5f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131217" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="icon.png">
<link rel="apple-touch-icon" href="icon.png">
<meta property="og:site_name" content="FlowState">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site}/icon.png">
<link rel="stylesheet" href="style.css">
</head>
<body class="{layout}">
{header}<main>
{hero}<article>
{body}
</article>
</main>
<footer>
<div class="foot">
<nav aria-label="Footer"><a href="privacy">Privacy</a><a href="support">Support</a></nav>
<p>Made by Ben Penchuk.</p>
</div>
</footer>
</body>
</html>
"""

ICON = (
    '<picture><source media="(prefers-color-scheme: dark)" srcset="icon-dark.png">'
    '<img src="icon.png" width="{size}" height="{size}" alt="" {extra}></picture>'
)

HEADER = (
    '<header class="site-header"><a class="brand" href="./">'
    + ICON.format(size=32, extra="")
    + "<span>FlowState</span></a></header>\n"
)

HERO = """<section class="hero">
""" + ICON.format(size=72, extra='fetchpriority="high"') + """
<h1>FlowState</h1>
<p class="tagline">{tagline}</p>
<p class="lede">{lede}</p>
<p class="status">{status}</p>
</section>
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # A link followed by {.button} is drawn as the kit's button: ink on a small Flame fill.
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)\{\.button\}", r'<a class="button" href="\2">\1</a>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def render(md: str) -> tuple[dict, str]:
    meta: dict[str, str] = {"title": "FlowState"}
    md = md.replace("{{mailto}}", f"mailto:{CONTACT}")
    md = md.replace("{{contact}}", f"[{CONTACT}](mailto:{CONTACT})")
    lines = md.splitlines()

    # YAML front matter, if any.
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), 0)
        for line in lines[1:end]:
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip().lower()] = value.strip()
        lines = lines[end + 1:]

    out: list[str] = []
    mode: str | None = None          # 'ul' | 'p' | 'table' | None
    para: list[str] = []

    def close():
        nonlocal mode, para
        if mode == "p" and para:
            out.append(f"<p>{' '.join(para)}</p>")
        elif mode == "ul":
            out.append("</ul>")
        elif mode == "table":
            out.append("</tbody></table>")
        mode, para = None, []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            close()
        elif line.startswith("#"):
            close()
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{level}>{inline(line.lstrip('#').strip())}</h{level}>")
        elif line.startswith("---") and set(line) == {"-"}:
            close()
            out.append("<hr>")
        elif mode == "ul" and raw[:1] in (" ", "\t") and out and out[-1].endswith("</li>"):
            # A wrapped bullet: indented text under a list item continues that item.
            out[-1] = out[-1][: -len("</li>")] + " " + inline(line) + "</li>"
        elif line.startswith(("- ", "* ")):
            if mode != "ul":
                close()
                out.append("<ul>")
                mode = "ul"
            out.append(f"<li>{inline(line[2:])}</li>")
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if mode != "table":
                close()
                out.append("<table><thead><tr>")
                out.extend(f"<th>{inline(c)}</th>" for c in cells)
                out.append("</tr></thead><tbody>")
                mode = "table"
                # Skip the |---|---| separator row.
                if i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
                    i += 1
            else:
                out.append("<tr>")
                out.extend(f"<td>{inline(c)}</td>" for c in cells)
                out.append("</tr>")
        else:
            if mode != "p":
                close()
                mode = "p"
            para.append(inline(line))
        i += 1
    close()

    body = "\n".join(out)
    # The "Last updated" line reads as metadata, not prose.
    body = re.sub(
        r"<p><strong>Last updated:</strong>([^<]*)</p>",
        r'<p class="updated"><strong>Last updated:</strong>\1</p>',
        body,
        count=1,
    )
    return meta, body


def page(stem: str, meta: dict, body: str) -> str:
    layout = meta.get("layout", "doc")
    esc = lambda text: html.escape(text, quote=True)
    if layout == "home":
        header = ""
        hero = HERO.format(
            tagline=inline(meta.get("tagline", "")),
            lede=inline(meta.get("lede", "")),
            status=inline(meta.get("status", "")),
        )
        canonical = f"{SITE}/"
    else:
        header, hero = HEADER, ""
        canonical = f"{SITE}/{stem}"
    return TEMPLATE.format(
        title=esc(meta["title"]),
        description=esc(meta.get("description") or DESCRIPTIONS.get(stem, DEFAULT_DESCRIPTION)),
        canonical=canonical,
        site=SITE,
        layout=layout,
        header=header,
        hero=hero,
        body=body,
    )


def main() -> int:
    built = []
    for source in sorted(ROOT.glob("*.md")):
        if source.name in NOT_PAGES:
            continue
        meta, body = render(source.read_text())
        target = ROOT / f"{source.stem}.html"
        target.write_text(page(source.stem, meta, body))
        built.append(f"{source.name} -> {target.name} ({target.stat().st_size:,} bytes)")
    print("\n".join(built) if built else "no markdown found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
