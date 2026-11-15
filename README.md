# SDLC Infrastructure Threat Framework (SITF)

A comprehensive framework for analyzing and defending against attacks targeting Software Development Lifecycle infrastructure: developer endpoints and IDEs, version control (VCS), CI/CD pipelines, artifact and container registries, and production cloud.

**Website:** [wiz-sec-public.github.io/SITF](https://wiz-sec-public.github.io/SITF/) · **[Technique reference](https://wiz-sec-public.github.io/SITF/techniques/index.html)** · **[Incidents mapped to SITF](https://wiz-sec-public.github.io/SITF/incidents/index.html)**

## Quick Start

### 🌐 Try Online (No Installation Required)

**[Launch the Flow Builder](https://wiz-sec-public.github.io/SITF/visualizer.html)** - Interactive tool for mapping attack flows
![Project Demo](app/demo-visualizer.gif)

**[Explore Techniques Visually](https://wiz-sec-public.github.io/SITF/techniques-library.html)** - Interactive visual explorer with filtering and search
![Project Demo](app/demo-library.gif)

### 🤖 Use with Claude AI

**Automated Attack Flow Generation** - Use Claude skills to automatically generate SITF-compliant attack flows and technique proposals:

| Skill | Purpose |
|-------|---------|
| `/attack-flow` | Generate flows from public incidents and breach reports |
| `/red-team-flow` | Generate flows from red team/pentest engagement reports |
| `/technique-proposal` | Create new technique definitions when gaps are identified |

See **[SKILLS.md](SKILLS.md)** for detailed usage instructions and examples.

### 📁 Use Locally

**Launch builder locally** - Download [visualizer.html](app/visualizer.html) locally, open and build offline

**Explore techniques** - Download [techniques-library.html](app/techniques-library.html) locally, open and browse techniques offline

### 📖 Documentation


**[Read the Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Complete methodology, case studies, and usage instructions

## What is SITF?

SITF helps security teams analyze supply chain attacks by:
- Visualizing attack stages across SDLC components (Endpoint, VCS, CI/CD, Registry, Production)
- Identifying the risks that enabled each attack technique
- Mapping risks to appropriate security controls
- Understanding attack paths and lateral movement patterns

## Framework Components

- **5 Infrastructure Components**: Endpoint/IDE, VCS, CI/CD, Registry, Production/Cloud
- **80+ Attack Techniques**: Pre-mapped with enabling risks and security controls
- **Dual Control Types**: Protective controls (prevent attacks) and Detective controls (detect attacks)
- **Framework Mappings**: Controls mapped to industry frameworks (OWASP SPVS)
- **Interactive Visualizer**: Drag-and-drop interface for building attack flow diagrams
- **Real-World Case Studies**: CircleCI breach, Shai-Hulud-2, TrustWallet, tj-actions, CodeBreach, s1ngularity

## Documentation

- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Start here for complete framework overview
- [TECHNIQUE_LIBRARY.md](TECHNIQUE_LIBRARY.md) - Reference catalog of all techniques
- [techniques.json](techniques.json) - Machine-readable source of truth for all techniques
- [Technique reference](https://wiz-sec-public.github.io/SITF/techniques/index.html) - One web page per technique (e.g. [SITF T-C003](https://wiz-sec-public.github.io/SITF/techniques/T-C003.html))
- [app/README.md](app/README.md) - Visualizer setup and usage
- [SKILLS.md](SKILLS.md) - Claude AI skills documentation and usage examples

## Claude AI Skills

SITF includes Claude AI skills for automated attack flow generation. See **[SKILLS.md](SKILLS.md)** for complete documentation.

| Skill | Input | Output |
|-------|-------|--------|
| `/attack-flow` | Incident name, URL, or web search | `sample-flows/<name>.json` |
| `/red-team-flow` | Engagement report (file/URL/text) | `flows/red-team/<name>.json` |
| `/technique-proposal` | Gap description | `technique-proposals/<id>.md` |

## Using SITF Data

SITF content is published in machine-readable forms for tools, RAG pipelines, and AI agents:

| Resource | URL |
|----------|-----|
| Full dataset (techniques, risks, controls, framework mappings) | https://wiz-sec-public.github.io/SITF/techniques.json |
| Per-technique pages | `https://wiz-sec-public.github.io/SITF/techniques/<ID>.html` |
| LLM index ([llms.txt](https://llmstxt.org)) | https://wiz-sec-public.github.io/SITF/llms.txt |
| All techniques as plain text | https://wiz-sec-public.github.io/SITF/llms-full.txt |
| Attack flows (incidents and red team) | [flows/](flows/) |

Technique IDs are prefixed by component: `T-E` Endpoint/IDE, `T-V` VCS, `T-C` CI/CD, `T-R` Registry, `T-P` Production/Cloud.

## Citing SITF

When referencing a technique, include the framework name, e.g. **"SITF technique T-C003 (PWN Request / Poisoned Pipeline Execution)"**, and link to its page. To cite the framework itself, use [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button).

## Contributing

### Adding or Modifying Techniques

**Manual Method:**
1. Edit [`techniques.json`](techniques.json) - the source of truth
2. Run `python3 build-techniques.py` to regenerate documentation and web app
3. Commit all changes (JSON, Markdown, and HTML)
4. Submit PR or use locally

**Automated Method (with Claude):**
1. Use `/technique-proposal` to generate a complete technique definition
2. Add the generated JSON to [`techniques.json`](techniques.json)
3. Run `python3 build-techniques.py` to regenerate documentation
4. Submit PR with the proposal rationale

The build script generates:
- `TECHNIQUE_LIBRARY.md` - Human-readable documentation
- `app/techniques-library.html` - Visual technique explorer with filtering and search
- `app/visualizer.html` - Interactive attack flow builder
- `app/techniques/`, `app/incidents/` - Static, crawlable per-technique and per-incident pages (via `build_site.py`)
- `app/llms.txt`, `app/llms-full.txt`, `app/sitemap.xml`, `app/techniques.json` - Machine-readable and search-engine outputs

New flows in `flows/incidents/` or `flows/red-team/` get an incident page automatically on the next build; add a display name to `FLOW_TITLES` in `build_site.py`.

### Creating Attack Flows

**Manual Method:**
- Use the [online visualizer](https://wiz-sec-public.github.io/SITF/visualizer.html) to build flows interactively

**Automated Method (with Claude):**
- Use `/attack-flow <attack-name> websearch` to automatically generate flows from incident reports

---

**Target Audience**: Incident Response Teams, Security Architects, Threat Intelligence Teams, Security Engineers

**Focus**: Protecting producer organizations (software vendors, OSS maintainers) who create supply chain components

---

Starting April 14 2026, SITF is licensed under CC BY-NC 4.0. Versions prior to this date remain under CC BY-NC-ND 4.0.
