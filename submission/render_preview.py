"""Render the canonical listing as a self-contained mobile-friendly preview."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def paragraphs(text):
    return "".join("<p>" + escape(part) + "</p>" for part in text.split("\n\n"))


def render():
    listing = json.loads((ROOT / "listing.json").read_text())
    included = "".join("<li>" + escape(item) + "</li>" for item in listing["included"])
    permissions = "".join("<li>" + escape(item) + "</li>" for item in listing["permissions"])
    name, creator = escape(listing["name"]), escape(listing["creator"])
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Benchmark Audit — Listing Preview</title>
<style>
:root{color-scheme:light;--ink:#142b40;--muted:#53677a;--line:#d8e0e6;--bg:#f5f7fa;--gold:#e2af53;--green:#187d67}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1000px;margin:auto;padding:28px 24px 60px}a{color:var(--green);overflow-wrap:anywhere}
.notice{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:16px}
.hero{display:grid;grid-template-columns:1fr 185px;gap:35px;align-items:start;padding:42px 0 26px}
.brand{display:flex;align-items:center;gap:12px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.mark{background:var(--ink);color:white;width:42px;height:42px;border-radius:10px;display:grid;place-items:center;font-size:16px;font-weight:800}
h1{font-size:clamp(31px,5vw,48px);line-height:1.13;letter-spacing:-.04em;margin:21px 0 18px}h2{font-size:24px;line-height:1.3;margin:0 0 14px;letter-spacing:-.02em}
p{margin:0 0 18px}.lede{font-size:19px;color:var(--muted)}.price{background:white;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:12px;padding:22px}
.amount{font-size:43px;line-height:1.2;font-weight:800;letter-spacing:-.04em}.small{font-size:13px;color:var(--muted)}.pill{display:inline-block;padding:4px 10px;background:#e9f3ef;border-radius:18px;color:var(--green);font-size:12px;margin:0 8px 9px 0}
.panel{padding:30px;background:white;border:1px solid var(--line);border-radius:14px;margin:24px 0}.panel.dark{background:var(--ink);color:white;border-color:var(--ink)}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:24px 0}.number{font-size:35px;font-weight:750;letter-spacing:-.03em}.caption{font-size:13px;color:#becbd6}
.callout{border-left:3px solid var(--gold);padding-left:18px;color:#e0e8ee}.columns{display:grid;grid-template-columns:1fr 1fr;gap:35px}
section{margin-top:36px}ul{padding-left:22px;margin:0}li{padding:5px 0}.request{font-style:italic;color:var(--muted);background:#f4f7fa;padding:18px;border-radius:8px}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media(max-width:650px){main{padding:18px 18px 40px}.hero{grid-template-columns:1fr;gap:15px;padding-top:28px}.price{display:flex;align-items:center;gap:20px;padding:16px}.columns{grid-template-columns:1fr;gap:26px}.panel{padding:22px}.metrics{gap:12px}.number{font-size:28px}.caption{font-size:12px}h1{font-size:34px}}
@media print{body{background:white;font-size:11pt}.notice{color:#333}.panel{break-inside:avoid}main{padding:0}.hero{padding-top:20px}a{color:inherit}.panel.dark{background:#142b40!important;print-color-adjust:exact}}
</style></head><body><main>
<div class="notice">Bobby’s preview · Proposed listing · Not published on Agensi</div>
<header class="hero"><div><div class="brand"><span class="mark">RCV</span>""" + creator + """</div>
<h1>""" + name + """</h1><p class="lede">""" + escape(listing["summary"]) + """</p>
<span class="pill">Paired results</span><span class="pill">Offline reproduction</span><span class="pill">No model API key</span></div>
<aside class="price"><div class="amount">$""" + str(listing["price_usd"]) + """</div><div><strong>One-time purchase</strong><div class="small">Recommended launch price<br>Version """ + escape(listing["version"]) + """ · Buyer taxes may apply</div></div></aside></header>
<div class="panel dark"><h2>Same score. Changed correctness.</h2>
<div class="metrics"><div><div class="number">50% → 50%</div><div class="caption">Accuracy in the runnable toy</div></div><div><div class="number">0 pp</div><div class="caption">Accuracy drift</div></div><div><div class="number">100%</div><div class="caption">Items changing correctness</div></div></div>
<p class="callout">Two synthetic items. Both switch correctness after option rotation. Unchanged aggregate accuracy does not establish invariance or readiness.</p></div>
<section><h2>What your agent will do</h2>""" + paragraphs(listing["description"]) + """</section>
<section class="columns"><div><h2>Included</h2><ul>""" + included + """</ul></div><div><h2>What you need</h2>""" + paragraphs(listing["compatibility"]) + """</div></section>
<section class="panel"><h2>See it in action</h2><p class="request">“""" + escape(listing["example_request"]) + """”</p>""" + paragraphs(listing["example_result"]) + """</section>
<section><h2>Where it stops</h2>""" + paragraphs(listing["limitations"]) + """</section>
<section class="columns"><div><h2>Permissions</h2><ul>""" + permissions + """</ul></div><div><h2>Open source, clearly stated</h2>""" + paragraphs(listing["source_note"]) + """<a href=""" + '"' + escape(listing["docs_url"], quote=True) + '"' + """>View source and documentation</a></div></section>
<footer>This is a content preview prepared for Bobby’s review, not Agensi’s actual checkout or an approved marketplace listing. No purchase or publication occurs on this page. The live host preview must be checked after sign-in.</footer>
</main></body></html>"""


if __name__ == "__main__":
    (ROOT / "listing-preview.html").write_text(render(), encoding="utf-8")
