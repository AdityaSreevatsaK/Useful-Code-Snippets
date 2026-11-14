"""Responsive UI CSS for Utility Shelf Dashboard v2."""


def stylesheet(mode: str) -> str:
    dark = mode == "Dark"
    bg = "#0B1423" if dark else "#F5F8FC"
    surface = "#121F32" if dark else "#FFFFFF"
    aside = "#101B2D" if dark else "#EEF3FB"
    ink = "#ECF3FF" if dark else "#17243A"
    muted = "#ADBBD2" if dark else "#60708B"
    edge = "#293D58" if dark else "#DEE6F0"
    accent = "#9BB2FF" if dark else "#375BCB"
    tint = "#1C2B49" if dark else "#EAF0FF"
    return f"""
<style>
:root {{
  --shelf-bg:{bg};--shelf-surface:{surface};--shelf-aside:{aside};
  --shelf-ink:{ink};--shelf-muted:{muted};--shelf-edge:{edge};
  --shelf-accent:{accent};--shelf-tint:{tint};
}}
[data-testid="stAppViewContainer"] {{
  background:var(--shelf-bg);color:var(--shelf-ink);
}}
[data-testid="stSidebar"] {{
  background:var(--shelf-aside);border-right:1px solid var(--shelf-edge);
}}
[data-testid="stHeader"] {{background:transparent;}}
[data-testid="stMainBlockContainer"],.block-container {{
  max-width:1240px;padding-top:2rem;padding-bottom:4rem;
}}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {{
  color:var(--shelf-ink);letter-spacing:-.035em;
}}
[data-testid="stMarkdownContainer"] p {{color:var(--shelf-ink);}}
div.stButton > button,div.stDownloadButton > button {{
  border-radius:11px;min-height:2.5rem;
  border-color:var(--shelf-edge);font-weight:620;
}}
div.stButton > button:hover {{
  border-color:var(--shelf-accent);color:var(--shelf-accent);
}}
[data-testid="stVerticalBlockBorderWrapper"] > div {{border-color:var(--shelf-edge);}}
.shelf-kicker {{
  display:inline-block;background:var(--shelf-tint);color:var(--shelf-accent);
  padding:.38rem .7rem;border:1px solid var(--shelf-edge);
  border-radius:99px;font-size:.72rem;font-weight:740;
  text-transform:uppercase;letter-spacing:.07em;
}}
.shelf-hero {{
  padding:2.15rem 2.3rem;margin:.6rem 0 1.6rem;
  background:linear-gradient(125deg,var(--shelf-surface) 22%,var(--shelf-tint) 100%);
  border:1px solid var(--shelf-edge);border-radius:22px;
}}
.shelf-hero h1 {{
  margin:.95rem 0 .7rem;color:var(--shelf-ink);
  font-weight:780;font-size:clamp(2rem,3.4vw,3.25rem);
  line-height:1.1;letter-spacing:-.055em;
}}
.shelf-hero p {{
  margin:0;max-width:48rem;color:var(--shelf-muted);
  line-height:1.62;font-size:1.02rem;
}}
.shelf-section {{
  font-size:1.17rem;font-weight:740;letter-spacing:-.025em;
  margin:1.25rem 0 .6rem;color:var(--shelf-ink);
}}
.shelf-card-icon {{
  display:inline-grid;place-items:center;
  width:2.5rem;height:2.5rem;background:var(--shelf-tint);
  border-radius:11px;font-size:1.35rem;
}}
.shelf-card-title {{
  font-size:1.03rem;font-weight:740;color:var(--shelf-ink);
  margin:.55rem 0 .28rem;
}}
.shelf-card-desc {{
  font-size:.87rem;min-height:2.65rem;line-height:1.45;
  margin:0 0 .35rem;color:var(--shelf-muted);
}}
.shelf-muted {{color:var(--shelf-muted);font-size:.85rem;line-height:1.5;}}
.shelf-small {{color:var(--shelf-accent);font-weight:700;font-size:.78rem;}}
.shelf-file {{
  padding:.7rem .9rem;background:var(--shelf-tint);
  color:var(--shelf-muted);border-radius:9px;
  overflow-wrap:anywhere;font-size:.8rem;
  font-family:ui-monospace,Consolas,monospace;
}}
.shelf-empty {{
  border:1px dashed var(--shelf-edge);border-radius:18px;
  padding:2.3rem;text-align:center;
  background:var(--shelf-surface);color:var(--shelf-muted);
}}
@media(max-width:740px){{
  [data-testid="stMainBlockContainer"],.block-container {{
    padding-top:.9rem;padding-left:1rem;padding-right:1rem;
  }}
  .shelf-hero {{padding:1.4rem 1.25rem;border-radius:16px;}}
  .shelf-hero h1 {{font-size:1.95rem;}}
  .shelf-card-desc {{min-height:0;}}
}}
</style>
"""