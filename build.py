#!/usr/bin/env python3
"""Turn the Markdown policy into standalone HTML.

No Jekyll, no build service, no dependencies. The output is one self-contained file that
works on GitHub Pages, Vercel, Cloudflare, Supabase Storage, or a USB stick - which matters
because the App Store needs this URL to keep working for as long as the app is listed, and
tying it to one host's build pipeline is how a privacy policy 404s two years from now.

Markdown stays the source of truth; this only renders it.

    python3 build.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# The one place the contact address lives. Markdown uses the {{contact}} token and the page
# footer uses this constant, so changing to an alias later is a one-line edit.
CONTACT = "ben@penchuk.com"

# Markdown files that are repo docs, not published pages.
NOT_PAGES = {"README.md"}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="How FlowState handles your data.">
<style>
  :root {{
    color-scheme: light dark;
    --bg: #ffffff;
    --fg: #1c1c1e;
    --muted: #6b6b70;
    --rule: #e5e5ea;
    --accent: #e8590c;
    --code-bg: #f5f5f7;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #000000;
      --fg: #f2f2f7;
      --muted: #9a9aa0;
      --rule: #2c2c2e;
      --accent: #ff7a33;
      --code-bg: #1c1c1e;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--fg);
    font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-text-size-adjust: 100%;
  }}
  main {{ max-width: 44rem; margin: 0 auto; padding: 3rem 1.25rem 6rem; }}
  h1 {{ font-size: 2rem; line-height: 1.2; letter-spacing: -0.02em; margin: 0 0 .5rem; }}
  h2 {{ font-size: 1.3rem; margin: 2.5rem 0 .75rem; letter-spacing: -0.01em; }}
  h3 {{ font-size: 1.05rem; margin: 1.75rem 0 .5rem; }}
  p, ul, ol {{ margin: 0 0 1rem; }}
  ul, ol {{ padding-left: 1.4rem; }}
  li {{ margin-bottom: .4rem; }}
  a {{ color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }}
  strong {{ font-weight: 650; }}
  code {{
    background: var(--code-bg); padding: .15em .4em; border-radius: 4px;
    font: .875em ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  hr {{ border: 0; border-top: 1px solid var(--rule); margin: 2.5rem 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0 0 1.25rem; font-size: .95rem; }}
  th, td {{ text-align: left; padding: .55rem .6rem; border-bottom: 1px solid var(--rule); vertical-align: top; }}
  th {{ font-weight: 650; }}
  .updated {{ color: var(--muted); font-size: .95rem; margin: 0 0 2rem; }}
  footer {{ margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--rule); color: var(--muted); font-size: .9rem; }}
</style>
</head>
<body>
<main>
{body}
<footer>FlowState · <a href="mailto:{contact}">{contact}</a></footer>
</main>
</body>
</html>
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def render(md: str) -> tuple[str, str]:
    title = "FlowState"
    md = md.replace("{{contact}}", f"[{CONTACT}](mailto:{CONTACT})")
    lines = md.splitlines()

    # YAML front matter, if any.
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), 0)
        for line in lines[1:end]:
            if line.lower().startswith("title:"):
                title = line.split(":", 1)[1].strip()
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
    return title, body


def main() -> int:
    built = []
    for source in sorted(ROOT.glob("*.md")):
        if source.name in NOT_PAGES:
            continue
        title, body = render(source.read_text())
        target = ROOT / f"{source.stem}.html"
        target.write_text(TEMPLATE.format(title=title, body=body, contact=CONTACT))
        built.append(f"{source.name} -> {target.name} ({target.stat().st_size:,} bytes)")
    print("\n".join(built) if built else "no markdown found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
