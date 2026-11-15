"""
SITF static site generator.

Generates crawlable, JavaScript-free pages from techniques.json and the attack
flows in flows/, so that search engines, AI crawlers, and RAG pipelines can
index SITF content (the interactive apps embed their data in JavaScript, which
most crawlers do not execute).

Outputs (all under app/, which GitHub Pages serves):
  techniques/index.html          technique reference index
  techniques/<ID>.html           one page per technique
  incidents/index.html           index of mapped incidents and engagements
  incidents/<slug>.html          one page per attack flow
  llms.txt, llms-full.txt        LLM-oriented summaries (https://llmstxt.org)
  sitemap.xml                    all static pages
  techniques.json                copy of the source data at a stable URL

Output is deterministic: the same inputs always produce the same files.
"""

import json
import shutil
from html import escape
from pathlib import Path

SITE_URL = "https://wiz-sec-public.github.io/SITF/"
REPO_URL = "https://github.com/wiz-sec-public/SITF"
FULL_NAME = "SDLC Infrastructure Threat Framework (SITF)"

COMPONENT_ORDER = ["endpoint", "vcs", "cicd", "registry", "production"]
STAGE_ORDER = ["Initial Access", "Discovery and Lateral Movement", "Post-Compromise"]

FLOW_DIRS = [
    ("incidents", "Incident"),
    ("red-team", "Red team engagement"),
]

# Display names for flow files (flows/<dir>/<slug>.json). New flows fall back
# to a title-cased slug; add an entry here for proper capitalization.
FLOW_TITLES = {
    "aqua-trivy-vscode": "Aqua Trivy VS Code Extension",
    "asyncapi-generator-2026": "AsyncAPI Generator (2026)",
    "circleci-flow": "CircleCI",
    "clinejection": "Clinejection",
    "codebreach": "CodeBreach",
    "litellm-oct-2026": "LiteLLM (October 2026)",
    "miasma-redhat": "Miasma (Red Hat)",
    "s1ngularity": "s1ngularity",
    "shai-hulud-2-flow": "Shai-Hulud 2.0",
    "solarwinds": "SolarWinds",
    "teampcp-campaign": "TeamPCP Campaign",
    "tj-actions": "tj-actions/changed-files",
    "trivy-act-ii": "Trivy Act II",
    "trustwallet": "Trust Wallet",
    "ultralytics": "Ultralytics",
    "gitlab-pipeline-hijack": "GitLab Pipeline Hijack",
    "synacktiv-cicd-red-team-engagement": "Synacktiv CI/CD Red Team Engagement",
}

TAGLINE = (
    "SITF is an open threat framework for attacks on software development "
    "lifecycle (SDLC) infrastructure: developer endpoints and IDEs, version "
    "control (VCS), CI/CD pipelines, artifact and container registries, and "
    "production cloud. Each SITF technique is mapped to the risks that enable "
    "it and to protective and detective controls."
)

CSS = """
:root { --fg:#1f2937; --muted:#6b7280; --accent:#7c3aed; --border:#e5e7eb; --bg:#ffffff; --soft:#f9fafb; }
@media (prefers-color-scheme: dark) {
  :root { --fg:#e5e7eb; --muted:#9ca3af; --accent:#c084fc; --border:#374151; --bg:#0f1220; --soft:#171a2b; }
}
* { box-sizing: border-box; }
body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       color:var(--fg); background:var(--bg); line-height:1.6; }
main, header.site, footer.site { max-width: 920px; margin: 0 auto; padding: 0 20px; }
header.site { padding-top: 18px; font-size: .95rem; }
header.site a { margin-right: 14px; }
footer.site { margin-top: 48px; padding-bottom: 32px; border-top: 1px solid var(--border);
              color: var(--muted); font-size: .9rem; }
a { color: var(--accent); }
h1 { font-size: 1.9rem; line-height: 1.25; margin: 24px 0 8px; }
h2 { font-size: 1.3rem; margin-top: 32px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
.lead { font-size: 1.08rem; }
.meta { color: var(--muted); font-size: .95rem; }
.tag { display:inline-block; padding: 1px 8px; border:1px solid var(--border); border-radius: 999px;
       font-size: .85rem; margin-right: 6px; background: var(--soft); }
table { border-collapse: collapse; width: 100%; font-size: .95rem; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
th { color: var(--muted); font-weight: 600; }
code { background: var(--soft); padding: 1px 5px; border-radius: 4px; }
ol.steps li { margin-bottom: 6px; }
.small { font-size: .9rem; color: var(--muted); }
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def e(text):
    return escape(str(text), quote=True)


def mitre_url(tid):
    base, _, sub = tid.partition(".")
    return f"https://attack.mitre.org/techniques/{base}/" + (f"{sub}/" if sub else "")


def control_name(control):
    return control.get("name", "") if isinstance(control, dict) else str(control)


def sitf_ref(tech):
    """Canonical way to refer to a technique in prose."""
    return f"SITF technique {tech['id']} ({tech['name']})"


def page(title, description, canonical_path, body, depth, json_ld=None):
    """Wrap body HTML in a full page. depth = directory depth below app/."""
    up = "../" * depth
    ld = ""
    if json_ld:
        ld = ('<script type="application/ld+json">'
              + json.dumps(json_ld, ensure_ascii=False, indent=1).replace("</", "<\\/")
              + "</script>\n")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{canonical_path}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{SITE_URL}{canonical_path}">
<meta property="og:site_name" content="{e(FULL_NAME)}">
<link rel="icon" type="image/png" href="{up}sitf-icon-round.png">
<link rel="stylesheet" href="{up}site.css">
{ld}</head>
<body>
<header class="site">
<a href="{up}index.html"><strong>SITF</strong></a>
<a href="{up}techniques/index.html">Techniques</a>
<a href="{up}incidents/index.html">Incidents</a>
<a href="{up}techniques-library.html">Interactive library</a>
<a href="{up}visualizer.html">Flow builder</a>
<a href="{REPO_URL}">GitHub</a>
</header>
<main>
{body}
</main>
<footer class="site">
<p>{e(FULL_NAME)} by <a href="https://www.wiz.io">Wiz</a>. Source and data:
<a href="{REPO_URL}">github.com/wiz-sec-public/SITF</a>
(<a href="{up}techniques.json">techniques.json</a>).
Licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>.</p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Flow parsing
# ---------------------------------------------------------------------------

def _box(node):
    pos = node.get("positionAbsolute") or node.get("position") or {}
    w = node.get("width") or (node.get("style") or {}).get("width") or 0
    h = node.get("height") or (node.get("style") or {}).get("height") or 0
    return pos.get("x", 0), pos.get("y", 0), w, h


def _container(node, candidates):
    """Smallest candidate box containing the node's center."""
    x, y, w, h = _box(node)
    cx, cy = x + w / 2, y + h / 2
    best = None
    for c in candidates:
        bx, by, bw, bh = _box(c)
        if bx <= cx <= bx + bw and by <= cy <= by + bh:
            if best is None or bw * bh < _box(best)[2] * _box(best)[3]:
                best = c
    return best


def parse_flow(path, kind, tech_by_id):
    flow = json.loads(path.read_text(encoding="utf-8"))
    nodes = flow.get("nodes", [])
    edges = flow.get("edges", [])
    by_node_id = {n["id"]: n for n in nodes}
    components = [n for n in nodes if n["type"] == "component"]
    zones = [n for n in nodes if n["type"] == "victimZone"]

    # Order technique nodes along the attack path: topological order over
    # edges, breaking ties by vertical then horizontal position.
    tech_nodes = [n for n in nodes if n["type"] == "technique"]
    tech_ids = {n["id"] for n in tech_nodes}
    indeg = {nid: 0 for nid in tech_ids}
    succ = {nid: [] for nid in tech_ids}
    for ed in edges:
        s, t = ed.get("source"), ed.get("target")
        if s in tech_ids and t in tech_ids and s != t:
            succ[s].append(t)
            indeg[t] += 1

    def key(nid):
        x, y, _, _ = _box(by_node_id[nid])
        return (y, x, nid)

    ready = sorted([n for n, d in indeg.items() if d == 0], key=key)
    order = []
    while ready:
        nid = ready.pop(0)
        order.append(nid)
        for t in succ[nid]:
            indeg[t] -= 1
            if indeg[t] == 0:
                ready.append(t)
        ready.sort(key=key)
    order += sorted([n for n in tech_ids if n not in order], key=key)  # cycles

    steps = []
    for nid in order:
        n = by_node_id[nid]
        tid = n["data"].get("id")
        comp = _container(n, components)
        zone = _container(n, zones)
        steps.append({
            "id": tid,
            "name": (tech_by_id.get(tid) or n["data"]).get("name", ""),
            "known": tid in tech_by_id,
            "note": (n["data"].get("customLabel") or "").strip(),
            "where": ((comp or {}).get("data", {}).get("customLabel") or "").strip(),
            "zone": ((zone or {}).get("data", {}).get("label") or "").strip(),
        })

    def labels(node_type):
        out = []
        for n in nodes:
            if n["type"] == node_type:
                d = n["data"]
                lab = d.get("label", "")
                custom = (d.get("customLabel") or "").strip()
                out.append(f"{lab}: {custom}" if custom and custom != lab else lab)
        return out

    slug = path.stem
    return {
        "slug": slug,
        "kind": kind,
        "title": FLOW_TITLES.get(slug) or slug.replace("-flow", "").replace("-", " ").title(),
        "source": f"flows/{path.parent.name}/{path.name}",
        "zones": [z["data"].get("label", "") for z in zones],
        "entries": labels("entryPoint"),
        "exits": labels("exitPoint"),
        "steps": steps,
        "technique_ids": sorted({s["id"] for s in steps if s["known"]}),
    }


def load_flows(root_dir, tech_by_id):
    flows = []
    for dirname, kind in FLOW_DIRS:
        for path in sorted((root_dir / "flows" / dirname).glob("*.json")):
            if path.name.startswith("._"):  # macOS resource forks
                continue
            flows.append(parse_flow(path, kind, tech_by_id))
    return flows


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def technique_description(tech, components):
    comp = components[tech["component"]]["name"]
    return (f"{sitf_ref(tech)}: {tech['description']}. "
            f"{tech['stage']} technique targeting {comp} in the {FULL_NAME}, "
            f"with enabling risks and protective and detective controls.")


def build_technique_page(tech, ctx):
    components, spvs, flows_by_tech, neighbors = (
        ctx["components"], ctx["spvs"], ctx["flows_by_tech"], ctx["neighbors"])
    comp = components[tech["component"]]
    tid, name = tech["id"], tech["name"]
    b = []
    b.append(f'<p class="meta"><a href="index.html">Techniques</a> › {e(comp["name"])} › {e(tid)}</p>')
    b.append(f"<h1>SITF technique {e(tid)}: {e(name)}</h1>")
    b.append(f'<p><span class="tag">Component: {e(comp["name"])}</span>'
             f'<span class="tag">Stage: {e(tech["stage"])}</span>'
             f'<span class="tag">ID: {e(tid)}</span></p>')
    b.append(f'<p class="lead">{e(tech["description"])}.</p>')
    b.append(f"<p>{e(sitf_ref(tech))} is a <strong>{e(tech['stage'])}</strong> technique "
             f"in the {e(FULL_NAME)}. It targets the <strong>{e(comp['name'])}</strong> "
             f"component ({e(comp['description'])}).</p>")

    b.append("<h2>Risks that enable this technique</h2><ul>")
    b += [f"<li>{e(r)}</li>" for r in tech.get("risks", [])]
    b.append("</ul>")

    def controls_section(title, items):
        b.append(f"<h2>{title}</h2>")
        if not items:
            b.append("<p class='small'>None mapped yet.</p>")
            return
        b.append("<ul>")
        for c in items:
            line = f"<strong>{e(control_name(c))}</strong>"
            if isinstance(c, dict):
                if c.get("description"):
                    line += f" — {e(c['description'])}"
                refs = (c.get("frameworks") or {}).get("spvs", [])
                if refs:
                    parts = []
                    for r in refs:
                        cat = spvs.get("categories", {}).get(r, {})
                        label = f"{r} {cat.get('name', '')}".strip()
                        parts.append(e(label))
                    line += f'<br><span class="small">OWASP SPVS: {"; ".join(parts)}</span>'
                for rule in c.get("detectionRules", []):
                    line += (f'<br><span class="small">Detection rule ({e(rule.get("source", ""))}): '
                             f'<code>{e(rule.get("ruleId", ""))}</code> {e(rule.get("ruleName", ""))}</span>')
            b.append(f"<li>{line}</li>")
        b.append("</ul>")

    controls = tech.get("controls", {})
    controls_section("Protective controls", controls.get("protective", []))
    controls_section("Detective controls", controls.get("detective", []))

    fw = tech.get("frameworks") or {}
    if fw:
        b.append("<h2>Framework mappings</h2><ul>")
        for t in fw.get("mitre_attack", []):
            b.append(f'<li>MITRE ATT&amp;CK: <a href="{mitre_url(t)}">{e(t)}</a></li>')
        for t in fw.get("aws_catalog", []):
            b.append(f'<li>AWS Threat Technique Catalog: '
                     f'<a href="https://aws-samples.github.io/threat-technique-catalog-for-aws/">{e(t)}</a></li>')
        b.append("</ul>")

    seen = flows_by_tech.get(tid, [])
    if seen:
        b.append("<h2>Observed in</h2><ul>")
        for f in seen:
            b.append(f'<li><a href="../incidents/{e(f["slug"])}.html">{e(f["title"])}</a> '
                     f'<span class="small">({e(f["kind"].lower())})</span></li>')
        b.append("</ul>")

    prev_t, next_t = neighbors.get(tid, (None, None))
    b.append("<h2>Explore</h2><ul>")
    b.append(f'<li><a href="../techniques-library.html#{e(tid)}">Open {e(tid)} in the interactive technique library</a></li>')
    b.append(f'<li><a href="../visualizer.html">Map an attack using {e(tid)} in the SITF flow builder</a></li>')
    if prev_t:
        b.append(f'<li>Previous {e(comp["name"])} technique: <a href="{e(prev_t["id"])}.html">'
                 f'{e(prev_t["id"])} {e(prev_t["name"])}</a></li>')
    if next_t:
        b.append(f'<li>Next {e(comp["name"])} technique: <a href="{e(next_t["id"])}.html">'
                 f'{e(next_t["id"])} {e(next_t["name"])}</a></li>')
    b.append("</ul>")

    b.append("<h2>How to reference</h2>")
    b.append(f"<p>Cite as <em>{e(sitf_ref(tech))}</em>, {e(FULL_NAME)}, "
             f'<a href="{SITE_URL}techniques/{e(tid)}.html">{SITE_URL}techniques/{e(tid)}.html</a>.</p>')

    url = f"{SITE_URL}techniques/{tid}.html"
    json_ld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "@id": url,
        "url": url,
        "termCode": tid,
        "name": f"SITF {tid}: {name}",
        "alternateName": name,
        "description": tech["description"],
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "@id": f"{SITE_URL}techniques/",
            "name": f"{FULL_NAME} technique library",
            "url": f"{SITE_URL}techniques/index.html",
        },
    }
    title = f"SITF {tid}: {name} | SDLC Infrastructure Threat Framework"
    return page(title, technique_description(tech, components),
                f"techniques/{tid}.html", "\n".join(b), depth=1, json_ld=json_ld)


def build_technique_index(data, ctx):
    components = ctx["components"]
    techs = data["techniques"]
    b = [f"<h1>SITF technique library</h1>",
         f'<p class="lead">{e(TAGLINE)}</p>',
         f"<p>The library contains <strong>{len(techs)} techniques</strong> across "
         f"{len(components)} SDLC components and {len(STAGE_ORDER)} attack stages "
         f"({', '.join(STAGE_ORDER)}). Technique IDs use the prefix of their component: "
         f"T-E (Endpoint/IDE), T-V (VCS), T-C (CI/CD), T-R (Registry), T-P (Production/Cloud).</p>",
         f'<p class="small">Also available as <a href="../techniques.json">techniques.json</a>, '
         f'<a href="../llms-full.txt">llms-full.txt</a>, and an '
         f'<a href="../techniques-library.html">interactive explorer</a>.</p>']
    for cid in COMPONENT_ORDER:
        group = sorted([t for t in techs if t["component"] == cid], key=lambda t: t["id"])
        if not group:
            continue
        comp = components[cid]
        b.append(f'<h2 id="{e(cid)}">{e(comp["name"])} techniques</h2>')
        b.append(f'<p class="small">{e(comp["description"])}</p>')
        b.append("<table><tr><th>ID</th><th>Technique</th><th>Stage</th></tr>")
        for t in group:
            b.append(f'<tr><td><a href="{e(t["id"])}.html">{e(t["id"])}</a></td>'
                     f'<td><a href="{e(t["id"])}.html">{e(t["name"])}</a><br>'
                     f'<span class="small">{e(t["description"])}</span></td>'
                     f'<td>{e(t["stage"])}</td></tr>')
        b.append("</table>")
    desc = (f"All {len(techs)} techniques of the {FULL_NAME}: attacks on developer endpoints, "
            f"VCS, CI/CD pipelines, registries and production cloud, with risks and controls.")
    return page("SITF Technique Library | SDLC Infrastructure Threat Framework", desc,
                "techniques/index.html", "\n".join(b), depth=1)


def build_flow_page(flow, ctx):
    tech_by_id = ctx["tech_by_id"]
    b = [f'<p class="meta"><a href="index.html">Incidents</a> › {e(flow["title"])}</p>',
         f"<h1>{e(flow['title'])}: attack mapped to SITF techniques</h1>",
         f'<p><span class="tag">{e(flow["kind"])}</span>'
         f'<span class="tag">{len(flow["technique_ids"])} SITF techniques</span></p>',
         f"<p class='lead'>This page maps the {e(flow['title'])} "
         f"{'attack' if flow['kind'] == 'Incident' else 'engagement'} to the {e(FULL_NAME)}, "
         f"step by step, from initial access to impact.</p>"]
    if flow["zones"]:
        b.append("<p><strong>Organizations involved:</strong> " + "; ".join(e(z) for z in flow["zones"]) + "</p>")
    if flow["entries"]:
        b.append("<h2>Entry points</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in flow["entries"]) + "</ul>")
    b.append("<h2>Attack path</h2><ol class='steps'>")
    for s in flow["steps"]:
        label = (f'<a href="../techniques/{e(s["id"])}.html">SITF {e(s["id"])}: {e(s["name"])}</a>'
                 if s["known"] else f"{e(s['id'])}: {e(s['name'])}")
        extra = []
        if s["note"]:
            extra.append(e(s["note"]))
        if s["where"]:
            extra.append(f"in {e(s['where'])}")
        b.append(f"<li>{label}" + (f" — {' · '.join(extra)}" if extra else "") + "</li>")
    b.append("</ol>")
    if flow["exits"]:
        b.append("<h2>Outcomes</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in flow["exits"]) + "</ul>")

    b.append("<h2>Techniques and controls</h2>")
    b.append("<table><tr><th>Technique</th><th>Key protective controls</th></tr>")
    for tid in flow["technique_ids"]:
        t = tech_by_id[tid]
        prot = [control_name(c) for c in t.get("controls", {}).get("protective", [])][:3]
        b.append(f'<tr><td><a href="../techniques/{e(tid)}.html">{e(tid)} {e(t["name"])}</a></td>'
                 f'<td>{e("; ".join(prot)) or "—"}</td></tr>')
    b.append("</table>")
    b.append(f'<p class="small">Source flow: <a href="{REPO_URL}/blob/main/{e(flow["source"])}">'
             f'{e(flow["source"])}</a>. Load it in the <a href="../visualizer.html">SITF flow builder</a> '
             f"to view the diagram.</p>")
    names = ", ".join(f"{tid} {tech_by_id[tid]['name']}" for tid in flow["technique_ids"][:6])
    desc = (f"The {flow['title']} {'attack' if flow['kind'] == 'Incident' else 'engagement'} "
            f"mapped to the {FULL_NAME}: {names}.")
    return page(f"{flow['title']} {'attack' if flow['kind'] == 'Incident' else 'red team'} analysis with SITF | SDLC Infrastructure Threat Framework",
                desc, f"incidents/{flow['slug']}.html", "\n".join(b), depth=1)


def build_flow_index(flows):
    b = ["<h1>Supply chain incidents mapped to SITF</h1>",
         "<p class='lead'>Real-world software supply chain and CI/CD attacks, and published red team "
         f"engagements, analyzed step by step with the {e(FULL_NAME)}.</p>"]
    for _, kind in FLOW_DIRS:
        group = [f for f in flows if f["kind"] == kind]
        if not group:
            continue
        b.append(f"<h2>{e(kind)}s</h2><table><tr><th>Name</th><th>SITF techniques</th></tr>")
        for f in group:
            b.append(f'<tr><td><a href="{e(f["slug"])}.html">{e(f["title"])}</a></td>'
                     f'<td>{" ".join(e(t) for t in f["technique_ids"])}</td></tr>')
        b.append("</table>")
    return page("Supply chain incidents mapped to SITF | SDLC Infrastructure Threat Framework",
                f"Software supply chain and CI/CD attacks analyzed with the {FULL_NAME}.",
                "incidents/index.html", "\n".join(b), depth=1)


# ---------------------------------------------------------------------------
# Text outputs
# ---------------------------------------------------------------------------

def build_llms_txt(data, ctx, flows):
    components = ctx["components"]
    lines = [f"# {FULL_NAME}", "", f"> {TAGLINE}", "",
             "SITF technique IDs look like T-C003 (prefix by component: T-E Endpoint/IDE, "
             "T-V VCS, T-C CI/CD, T-R Registry, T-P Production/Cloud). Refer to them as "
             "\"SITF technique T-C003\". Stages: " + ", ".join(STAGE_ORDER) + ".",
             "",
             "## Data",
             f"- [techniques.json]({SITE_URL}techniques.json): machine-readable source of truth "
             "(techniques, risks, controls, framework mappings to OWASP SPVS and MITRE ATT&CK)",
             f"- [llms-full.txt]({SITE_URL}llms-full.txt): every technique with risks and controls as plain text",
             f"- [Repository]({REPO_URL}): source, attack flows, Claude Code skills",
             ""]
    for cid in COMPONENT_ORDER:
        group = sorted([t for t in data["techniques"] if t["component"] == cid], key=lambda t: t["id"])
        lines.append(f"## {components[cid]['name']} techniques")
        for t in group:
            lines.append(f"- [SITF {t['id']}: {t['name']}]({SITE_URL}techniques/{t['id']}.html): {t['description']}")
        lines.append("")
    lines.append("## Incidents mapped to SITF")
    for f in flows:
        lines.append(f"- [{f['title']}]({SITE_URL}incidents/{f['slug']}.html): {f['kind'].lower()}, "
                     f"techniques {', '.join(f['technique_ids'])}")
    lines += ["", "## Optional",
              f"- [Interactive technique library]({SITE_URL}techniques-library.html)",
              f"- [Attack flow builder]({SITE_URL}visualizer.html)",
              f"- [Implementation guide]({REPO_URL}/blob/main/IMPLEMENTATION_GUIDE.md)", ""]
    return "\n".join(lines)


def build_llms_full(data, ctx, flows_by_tech):
    components = ctx["components"]
    out = [f"# {FULL_NAME} — full technique reference", "", TAGLINE, "",
           f"Source: {SITE_URL}techniques.json", ""]
    for cid in COMPONENT_ORDER:
        group = sorted([t for t in data["techniques"] if t["component"] == cid], key=lambda t: t["id"])
        out += [f"## {components[cid]['name']}", ""]
        for t in group:
            out += [f"### SITF technique {t['id']}: {t['name']}", "",
                    f"URL: {SITE_URL}techniques/{t['id']}.html",
                    f"Component: {components[cid]['name']}. Stage: {t['stage']}.", "",
                    t["description"] + ".", "", "Risks:"]
            out += [f"- {r}" for r in t.get("risks", [])]
            for kind in ("protective", "detective"):
                out += ["", f"{kind.capitalize()} controls:"]
                items = t.get("controls", {}).get(kind, [])
                out += [f"- {control_name(c)}" for c in items] or ["- (none)"]
            fw = t.get("frameworks") or {}
            if fw.get("mitre_attack"):
                out += ["", "MITRE ATT&CK: " + ", ".join(fw["mitre_attack"])]
            seen = flows_by_tech.get(t["id"], [])
            if seen:
                out += ["", "Observed in: " + ", ".join(f["title"] for f in seen)]
            out.append("")
    return "\n".join(out)


def build_sitemap(paths):
    urls = "\n".join(f"  <url><loc>{SITE_URL}{p}</loc></url>" for p in paths)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def generate_site(data, root_dir, app_dir):
    """Generate all static pages. Returns a dict of counts for reporting."""
    root_dir, app_dir = Path(root_dir), Path(app_dir)
    tech_by_id = {t["id"]: t for t in data["techniques"]}
    components = {c["id"]: c for c in data["components"]}
    flows = load_flows(root_dir, tech_by_id)

    flows_by_tech = {}
    for f in flows:
        for tid in f["technique_ids"]:
            flows_by_tech.setdefault(tid, []).append(f)

    neighbors = {}
    for cid in COMPONENT_ORDER:
        group = sorted([t for t in data["techniques"] if t["component"] == cid], key=lambda t: t["id"])
        for i, t in enumerate(group):
            neighbors[t["id"]] = (group[i - 1] if i > 0 else None,
                                  group[i + 1] if i + 1 < len(group) else None)

    ctx = {
        "tech_by_id": tech_by_id,
        "components": components,
        "spvs": data.get("frameworkDefinitions", {}).get("spvs", {}),
        "flows_by_tech": flows_by_tech,
        "neighbors": neighbors,
    }

    # Recreate generated directories so removed techniques/flows disappear.
    for sub in ("techniques", "incidents"):
        d = app_dir / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    def write(rel, content):
        (app_dir / rel).write_text(content, encoding="utf-8")

    sitemap_paths = ["", "techniques-library.html", "visualizer.html",
                     "techniques/index.html", "incidents/index.html"]

    write("site.css", CSS.lstrip())
    write("techniques/index.html", build_technique_index(data, ctx))
    for t in sorted(data["techniques"], key=lambda t: t["id"]):
        write(f"techniques/{t['id']}.html", build_technique_page(t, ctx))
        sitemap_paths.append(f"techniques/{t['id']}.html")

    write("incidents/index.html", build_flow_index(flows))
    for f in flows:
        write(f"incidents/{f['slug']}.html", build_flow_page(f, ctx))
        sitemap_paths.append(f"incidents/{f['slug']}.html")

    write("llms.txt", build_llms_txt(data, ctx, flows))
    write("llms-full.txt", build_llms_full(data, ctx, flows_by_tech))
    write("sitemap.xml", build_sitemap(sitemap_paths))
    shutil.copyfile(root_dir / "techniques.json", app_dir / "techniques.json")

    return {"techniques": len(data["techniques"]), "flows": len(flows), "pages": len(sitemap_paths)}
