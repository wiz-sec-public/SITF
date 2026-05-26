---
name: red-team-flow
description: Generate SITF-compliant attack flow JSON from red team or pentest reports. Accepts report files, URLs, or pasted findings. Use when documenting offensive security engagements.
argument-hint: <engagement-name> [--file path | --url url | paste report text]
tools: Read, Grep, Glob, WebFetch, Write, Bash
---

# Red Team Flow Generator

Generate SITF-compliant attack flow JSON files from red team or penetration testing reports.

## Usage

```
/red-team-flow <engagement-name> [source]
```

- `engagement-name`: Identifier for the engagement (e.g., "acme-2026q1", "client-sdlc-audit")
- `source`: One of:
  - `--file <path>`: Path to report file (markdown, txt, json, pdf)
  - `--url <url>`: URL to report or findings page
  - Omit to paste report text directly in conversation

Arguments: $ARGUMENTS

## Supported Input Formats

The skill accepts red team and pentest reports in various formats:

### Text-Based Reports
- Markdown reports with findings sections
- Plain text engagement notes
- Bullet-point attack chains
- Executive summaries with technical appendix

### Structured Formats
- JSON findings export
- CSV with columns: finding, target, technique, evidence
- YAML engagement summaries

### Report Sections Recognized
The skill looks for these common report patterns:
- "Findings", "Vulnerabilities", "Attack Path", "Kill Chain"
- "Initial Access", "Lateral Movement", "Privilege Escalation"  
- "Recommendations", "Remediation" (used for control mapping)
- Numbered steps (1., 2., 3. or Step 1, Step 2)
- MITRE ATT&CK references (T1xxx)

## Instructions

When this skill is invoked:

### Phase 1: Report Ingestion

1. **If `--file` specified:**
   - Read the file content
   - Detect format (markdown, txt, json, csv, yaml)
   - Extract structured findings

2. **If `--url` specified:**
   - Fetch the URL content
   - Parse as report or findings page

3. **If no source specified:**
   - Prompt user to paste report content
   - Or use context from current conversation

4. **Normalize the input:**
   - Extract attack steps/findings into a structured list
   - Identify: target component, action taken, evidence, outcome
   - Preserve attack chain order if present

### Phase 2: Technique Mapping

1. Read `techniques.json` to get the full SITF technique library.

2. For each finding/attack step, find the best matching technique:
   - Match by **action semantics**, not surface keywords
   - Map pentest terminology to SITF:
     - "GitHub Actions exploit" → T-C003 (PWN Request) or T-C004 (Script Injection)
     - "Stole AWS creds from logs" → T-C005 (Secret Exfiltration from Workflow)
     - "Published malicious package" → T-R004 (Publishing Malicious Package)
     - "Accessed prod via stolen token" → T-P001 (Abuse Production Credentials)
   - If MITRE ATT&CK IDs are in the report, cross-reference with SITF mappings

3. If no matching SITF technique exists:
   - Check if finding is **in-scope** for SITF (SDLC/supply-chain related)
   - If in-scope: Create placeholder with `"type": "technique-gap"`
   - If out-of-scope (generic infra attack): Note in output, reference MITRE ATT&CK

4. For pentest reports with isolated findings (not chained):
   - Group findings by target component
   - Create parallel technique nodes within each component
   - Connect entry point to each finding independently

### Phase 3: Layout Calculation

Apply these layout rules (consistent with `/attack-flow`):

#### Rule 1: Component Layout (Left-to-Right by Attack Flow)
- Order components by their **sequence in the attack chain**
- If findings aren't chained, order by: endpoint → vcs → cicd → registry → production
- Component x-positions: Use increments of ~300px starting from x=50

#### Rule 2: Technique Ordering (Top-to-Bottom)
- **Chained attacks**: Order by attack sequence
- **Isolated findings**: Order by severity (Critical → High → Medium → Low)
- Vertical gap between techniques: ~130px
- First technique starts at y = component.y + 80

#### Rule 3: Technique-Component Centering
- technique.x = component.x + (component.width - technique.width) / 2
- With component.width=250 and technique.width=160: offset = 45
- Example: component at x=50 → technique at x=95

#### Rule 4: Component Sizing
- Width = 250px (standard)
- Height = max(500, (technique_count × 130) + 160)

#### Rule 5: Edge Connections
- Connect source.bottom → target.top for vertical flows within component
- Connect source.right → target.left for cross-component flows
- Add labels from report evidence ("Stolen AWS_ACCESS_KEY_ID", "via PR #123")
- Use `"type": "smoothstep"` for all edges

### Phase 4: JSON Generation

Generate attack flow JSON with this structure (identical to `/attack-flow` output):

```json
{
  "metadata": {
    "title": "Human-readable title for canvas display",
    "name": "Engagement Name",
    "created": "ISO-8601 timestamp",
    "version": "1.0",
    "framework": "SITF",
    "source": "red-team-report",
    "description": "Red team engagement against ACME Corp SDLC infrastructure"
  },
  "nodes": [],
  "edges": []
}
```

**Node types** (same as /attack-flow):
- `entryPoint`: How the engagement started (Assumed Breach, External Attacker, Insider, etc.)
- `component`: SITF component container (endpoint, vcs, cicd, registry, production)
- `technique`: Attack technique from techniques.json
- `technique-gap`: Placeholder for missing SITF technique
- `exitPoint`: Engagement outcome (Data Exfiltration, Persistence, Supply Chain Compromise, etc.)

**Special metadata for red team flows:**
- Add `"source": "red-team-report"` to metadata
- Add `"engagement"` field if client/engagement name is known
- Add `"scope"` array listing in-scope components

#### Node Structure - Technique (with evidence)
```json
{
  "id": "technique-c003-1",
  "type": "technique",
  "position": { "x": 95, "y": 160 },
  "data": {
    "id": "T-C003",
    "name": "PWN Request / Poisoned Pipeline Execution",
    "component": "cicd",
    "stage": "Initial Access",
    "description": "Full description from techniques.json",
    "risks": ["risk1", "risk2"],
    "controls": { "protective": [], "detective": [] },
    "customLabel": "Exploited workflow in repo X",
    "evidence": "PR #142 triggered workflow with write permissions",
    "severity": "Critical"
  },
  "zIndex": 10,
  "width": 160,
  "height": 96
}
```

### Phase 5: Control Gap Analysis

After generating the flow, analyze defensive gaps:

1. For each technique used in the attack:
   - List the protective controls from techniques.json
   - Identify which controls were missing (enabled the attack)
   
2. Generate a **Controls Gap Summary**:
   ```
   | Technique | Missing Control | OWASP SPVS |
   |-----------|-----------------|------------|
   | T-C003    | Minimal workflow permissions | V3.1 |
   | T-C005    | Log sanitization | V2.5 |
   ```

3. Prioritize recommendations by:
   - Number of techniques the control would prevent
   - Severity of findings it addresses

### Phase 6: Validation

Run this checklist before outputting:

```
[ ] Valid JSON structure (parse test passes)
[ ] Required fields: metadata.{title,name,created,version,framework,source}, nodes[], edges[]
[ ] All node IDs are unique
[ ] All edge source/target reference valid node IDs
[ ] Technique nodes use data.id and data.name (NOT techniqueId/label)
[ ] Technique nodes include full risks[] and controls from techniques.json
[ ] All techniques centered within components (x = component.x + 45)
[ ] Component heights adequate for technique count
[ ] Out-of-scope findings noted but not forced into SITF
[ ] Evidence preserved in customLabel or evidence fields
[ ] Exit points connected to terminal techniques
```

### Phase 7: Output

1. Write the JSON file to `flows/red-team/<engagement-name>.json`
2. Validate JSON: `python3 -c "import json; json.load(open('file'))"`
3. Provide output summary:

```markdown
## Red Team Flow: <engagement-name>

### Attack Chain
1. Initial Access via [entry point]
2. [Technique] → [Technique] → ...
3. Impact: [exit point]

### Techniques Used
| ID | Name | Component | Evidence |
|----|------|-----------|----------|
| T-C003 | PWN Request | CI/CD | PR #142 |
| ... | ... | ... | ... |

### Control Gaps Identified
| Missing Control | Would Prevent | Priority |
|-----------------|---------------|----------|
| Minimal workflow permissions | T-C003, T-C005 | High |
| ... | ... | ... |

### Out-of-Scope Findings
- [Finding X]: Generic cloud attack, see MITRE ATT&CK T1078

### Technique Gaps
- [Finding Y]: No matching SITF technique, run `/technique-proposal`
```

4. If technique-gaps exist, recommend `/technique-proposal` for each

## Examples

### From File
```
/red-team-flow acme-2026q1 --file ./reports/acme-final-report.md
```

### From URL
```
/red-team-flow client-audit --url https://internal.wiki/engagements/client-findings
```

### From Pasted Text
```
/red-team-flow demo-engagement

We started with access to a developer laptop (assumed breach). Found GitHub 
PAT in ~/.config/gh/hosts.yml. Used the token to access private repos and 
discovered hardcoded AWS credentials in a workflow file. The AWS creds had 
admin access to production S3 buckets. We exfiltrated customer data as POC.
```

## Pentest vs Red Team Handling

**Red Team Reports** (attack chains):
- Typically have sequential steps (A → B → C → D)
- Generate connected flow with edges between techniques
- Entry point connects to first technique, exit point to last

**Pentest Reports** (isolated findings):
- May have unconnected findings per component
- Generate parallel techniques within components
- Entry point fans out to multiple techniques
- Each finding may have its own exit point or shared "Findings Reported" exit

The skill auto-detects based on report structure:
- Sequential numbering / "then we..." / "next..." → chained flow
- Bullet lists / severity ratings / individual findings → parallel flow
