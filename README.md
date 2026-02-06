# SDLC Infrastructure Threat Framework (SITF)

A comprehensive framework for analyzing and defending against attacks targeting Software Development Lifecycle infrastructure.

## Quick Start

### 🌐 Try Online (No Installation Required)

**[Launch the Flow Builder](https://wiz-sec-public.github.io/SITF/visualizer.html)** - Interactive tool for mapping attack flows
![Project Demo](app/demo-visualizer.gif)

**[Explore Techniques Visually](https://wiz-sec-public.github.io/SITF/techniques-library.html)** - Interactive visual explorer with filtering and search
![Project Demo](app/demo-library.gif)

### 🤖 Use with Claude AI

**Automated Attack Flow Generation** - Use Claude skills to automatically generate SITF-compliant attack flows and technique proposals:
- `/attack-flow` - Generate attack flow JSON from incident reports or attack descriptions
- `/technique-proposal` - Create PR-ready proposals for new techniques when gaps are identified

See [Claude Skills Documentation](#claude-ai-skills) below for detailed usage instructions.

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
- **75+ Attack Techniques**: Pre-mapped with enabling risks and security controls
- **Dual Control Types**: Protective controls (prevent attacks) and Detective controls (detect attacks)
- **Framework Mappings**: Controls mapped to industry frameworks (OWASP SPVS)
- **Interactive Visualizer**: Drag-and-drop interface for building attack flow diagrams
- **Real-World Case Studies**: CircleCI breach, Shai-Hulud-2, TrustWallet, tj-actions, CodeBreach, s1ngularity

## Documentation

- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Start here for complete framework overview
- [TECHNIQUE_LIBRARY.md](TECHNIQUE_LIBRARY.md) - Reference catalog of all techniques
- [techniques.json](techniques.json) - Machine-readable source of truth for all techniques
- [app/README.md](app/README.md) - Visualizer setup and usage
- [.claude/skills/](.claude/skills/) - Claude AI skills for automated attack flow generation

## Claude AI Skills

SITF includes two Claude AI skills that automate attack flow generation and technique proposal creation:

#### `/attack-flow` - Attack Flow Generator

Automatically generates SITF-compliant attack flow JSON files from attack descriptions or incident reports.

**Usage:**
```
/attack-flow <attack-name> [websearch|url]
/attack-flow solarwinds websearch
/attack-flow codecov https://about.codecov.io/security-update/
```

**What it does:**
1. Researches the attack (via web search or provided URL)
2. Maps attack steps to SITF techniques from [`techniques.json`](techniques.json)
3. Calculates proper layout for visualization
4. Generates JSON file in `sample-flows/` directory
5. Identifies technique gaps and recommends using `/technique-proposal`

See [.claude/skills/attack-flow/SKILL.md](.claude/skills/attack-flow/SKILL.md) for detailed documentation.

#### `/technique-proposal` - Technique Proposal Generator

Generates PR-ready technique proposals when an attack step doesn't map to existing SITF techniques.

**Usage:**
```
/technique-proposal "<description>" [component]
/technique-proposal "Malware invokes AI CLI tools with permission-bypass flags" endpoint
```

**What it does:**
1. Analyzes the gap against existing techniques
2. Assigns the next sequential technique ID
3. Generates complete technique definition (name, description, risks, controls)
4. Produces PR-ready markdown with rationale and references

See [.claude/skills/technique-proposal/SKILL.md](.claude/skills/technique-proposal/SKILL.md) for detailed documentation.

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

### Creating Attack Flows

**Manual Method:**
- Use the [online visualizer](https://wiz-sec-public.github.io/SITF/visualizer.html) to build flows interactively

**Automated Method (with Claude):**
- Use `/attack-flow <attack-name> websearch` to automatically generate flows from incident reports

---

**Target Audience**: Incident Response Teams, Security Architects, Threat Intelligence Teams, Security Engineers

**Focus**: Protecting producer organizations (software vendors, OSS maintainers) who create supply chain components
