# Claude AI Skills for SITF

SITF includes Claude AI skills that automate attack flow generation, red team report processing, and technique proposal creation. These skills integrate with Claude Code to streamline security analysis workflows.

## Available Skills

| Skill | Purpose | Input |
|-------|---------|-------|
| `/attack-flow` | Generate flows from public incidents | Attack name, URL, or web search |
| `/red-team-flow` | Generate flows from engagement reports | Report file, URL, or pasted text |
| `/technique-proposal` | Create new technique definitions | Gap description and component |

## `/attack-flow` - Attack Flow Generator

Automatically generates SITF-compliant attack flow JSON files from attack descriptions or incident reports.

### Usage

```
/attack-flow <attack-name> [websearch|url]
```

**Examples:**
```
/attack-flow solarwinds websearch
/attack-flow codecov https://about.codecov.io/security-update/
/attack-flow tj-actions-compromise
```

### What It Does

1. Researches the attack (via web search or provided URL)
2. Maps attack steps to SITF techniques from `techniques.json`
3. Calculates proper layout for visualization
4. Generates JSON file in `sample-flows/` directory
5. Identifies technique gaps and recommends `/technique-proposal`

### Output

- JSON file: `sample-flows/<attack-name>.json`
- Attack chain summary with technique mappings
- Control gap analysis
- Technique gap identification (if any)

See [.claude/skills/attack-flow/SKILL.md](.claude/skills/attack-flow/SKILL.md) for detailed documentation.

---

## `/red-team-flow` - Red Team Flow Generator

Generates SITF-compliant attack flow JSON from red team or penetration testing engagement reports.

### Usage

```
/red-team-flow <engagement-name> [--file <path> | --url <url>]
```

**Examples:**
```
# From file
/red-team-flow acme-2026q1 --file ./reports/acme-final-report.md

# From URL
/red-team-flow synacktiv-cicd --url https://www.synacktiv.com/en/publications/cicd-secrets-extraction

# From pasted text (omit source, then paste)
/red-team-flow demo-engagement
```

### What It Does

1. Ingests report content (file, URL, or conversation context)
2. Extracts attack steps and findings
3. Maps to SITF techniques with evidence preservation
4. Handles both chained attacks and isolated findings
5. Generates JSON file in `flows/red-team/` directory
6. Produces control gap analysis

### Supported Input Formats

- Markdown reports with findings sections
- Plain text engagement notes
- JSON/YAML findings exports
- URLs to published reports

### Output

- JSON file: `flows/red-team/<engagement-name>.json`
- Attack chain summary with evidence
- Control gaps table with OWASP SPVS mappings
- Out-of-scope findings noted (non-SDLC attacks)
- Technique gap recommendations

See [.claude/skills/red-team-flow/SKILL.md](.claude/skills/red-team-flow/SKILL.md) for detailed documentation.

---

## `/technique-proposal` - Technique Proposal Generator

Generates PR-ready technique proposals when an attack step doesn't map to existing SITF techniques.

### Usage

```
/technique-proposal "<description>" [component]
```

**Examples:**
```
/technique-proposal "Malware invokes AI CLI tools with permission-bypass flags" endpoint
/technique-proposal "Attacker exploits self-hosted runner shared across repos" cicd
/technique-proposal "Dependency confusion via internal package name squatting"
```

### What It Does

1. Analyzes the gap against existing techniques
2. Assigns the next sequential technique ID
3. Generates complete technique definition:
   - Name, description, attack stage
   - Enabling risks
   - Protective and detective controls
   - OWASP SPVS mappings
4. Produces PR-ready markdown with rationale

### Output

- Markdown file: `technique-proposals/<id>-<name>.md`
- JSON snippet ready for `techniques.json`
- Rationale and references
- Similar existing techniques (for deduplication check)

See [.claude/skills/technique-proposal/SKILL.md](.claude/skills/technique-proposal/SKILL.md) for detailed documentation.

---

## Workflow Integration

### Analyzing a Public Incident

```
/attack-flow codecov websearch
# → Generates sample-flows/codecov.json
# → If gaps found: "Run /technique-proposal for..."
```

### Processing an Engagement Report

```
/red-team-flow client-2026q1 --file ./reports/findings.md
# → Generates flows/red-team/client-2026q1.json
# → Control gaps summary for remediation planning
```

### Filling Technique Gaps

```
/technique-proposal "Novel CI bypass via X" cicd
# → Generates technique-proposals/T-C0XX-name.md
# → Add to techniques.json, run build-techniques.py
```

### Visualization

After generating any flow, open in the visualizer:
- **Online**: [SITF Flow Builder](https://wiz-sec-public.github.io/SITF/visualizer.html)
- **Local**: `app/visualizer.html`

Load the JSON file to visualize and refine the attack flow.

---

## Data Source Recommendations

| Source Type | Best Skill | Notes |
|-------------|------------|-------|
| Public breach/incident | `/attack-flow` | Uses web search for comprehensive coverage |
| Published security research | `/attack-flow` with URL | Direct URL for focused analysis |
| Internal engagement report | `/red-team-flow` | Preserves evidence and findings structure |
| Methodology guides | `/red-team-flow` | May produce parallel techniques, not chains |

### URL vs File for Red Team Flows

When processing the same content from different sources:

| Aspect | Direct URL | Curated File |
|--------|------------|--------------|
| Granularity | Higher - captures all details | May consolidate during curation |
| Portability | Requires network access | Works offline |
| Context | Raw source only | Can add organizational context |

For maximum fidelity, generate flows directly from source URLs. Use curated files when combining multiple sources or adding context not in the original.
