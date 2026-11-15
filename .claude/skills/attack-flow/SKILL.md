---
name: attack-flow
description: Map a software supply chain, CI/CD, or SDLC security incident to SITF (SDLC Infrastructure Threat Framework) techniques and generate an attack flow JSON for the SITF flow builder, with the risks and controls that would have stopped it. Use when analyzing or reconstructing an attack on developer endpoints or IDEs, GitHub/GitLab repositories, GitHub Actions or other CI/CD pipelines, package or container registries (npm, PyPI, Docker), or build and release infrastructure, such as compromised packages, poisoned pipelines, or stolen CI secrets.
argument-hint: <attack-name> [websearch|url]
tools: Read, Grep, Glob, WebSearch, WebFetch, Write, Bash
---

# Attack Flow Generator

Generate SITF-compliant attack flow JSON files from attack descriptions or incident reports.

## Usage

```
/attack-flow <attack-name> [source]
```

- `attack-name`: Identifier for the attack (e.g., "s1ngularity", "solarwinds")
- `source`: URL, local file path (report, write-up), "websearch" for auto-research, or omit to use conversation context. A name plus a document ("X, and use this report to augment") means: research X **and** fold in the document

Arguments: $ARGUMENTS

## SITF Data Location

This skill runs either inside the SITF repository or, when installed as the `sitf` Claude Code plugin, inside any other project. Resolve the **SITF root** once before starting:

1. If the current project root contains both `techniques.json` and `build-techniques.py`, you are in the SITF repository: the SITF root is the project root.
2. Otherwise the SITF root is the installed plugin directory: `${CLAUDE_PLUGIN_ROOT}`. (If that placeholder appears literally, unresolved, the plugin is not installed; fetch the library from https://wiz-sec-public.github.io/SITF/techniques.json instead and read example flows from https://github.com/wiz-sec-public/SITF/tree/main/flows.)

Every reference below to `techniques.json`, `flows/...`, or `app/...` means that path under the SITF root. Never write into the plugin directory.

## Instructions

When this skill is invoked:

### Phase 1: Research

1. If source is "websearch" or a URL, gather attack details:
   - Attack timeline and phases
   - Entry point and initial access method
   - Lateral movement and persistence techniques
   - Data exfiltration or impact
   - Affected components (CI/CD, VCS, Registry, Endpoint, Production)

2. If source is omitted, use context from the current conversation.

3. If the user supplies a document (internal report, write-up), treat it as a primary source but still cross-check:
   - Find the **official post-mortem** from the affected organization, plus the original disclosure (e.g. the GitHub issue)
   - Add details the document lacks (exact timestamps, commit SHAs, accounts involved) and cite where each came from
   - **Flag conflicts** between sources in the output, especially where a new fact weakens a recommendation in the document (e.g. "approval gate would have stopped it" vs. the approval was given by a second stolen account)
   - Keep internal documents out of anything public (node evidence, PR bodies): cite public sources only

### Phase 2: Technique Mapping

1. Read `techniques.json` to get the full technique library.

2. For each attack step, find the best matching technique:
   - Match by **action semantics**, not surface keywords
   - Example: Uploading stolen data to repos → T-V003 (Secret Exfiltration), NOT T-V008 (Malicious Hosting)
   - Example: Accessing VCS with stolen creds → T-V001 must come BEFORE any VCS actions

3. If no matching technique exists:
   - Check if attack step is **in-scope** for SITF (SDLC/supply-chain related)
   - If in-scope: Create placeholder with `"type": "technique-gap"`
   - If out-of-scope (generic cloud/infra attack): Note in output, reference MITRE ATT&CK
   - Note in output that `/technique-proposal` should be run for in-scope gaps

4. **Out-of-scope initial access**: when the way in has no SITF technique (e.g. exploiting an internet-exposed app, MITRE T1190), do NOT force a mapping. Describe it in the entry point's `customLabel` and connect the entry point directly to the first in-scope technique.

5. **Contributing conditions**: a condition that enabled the attack but wasn't an attacker action (e.g. AI coding agent traffic leaking tokens into logs) can be shown as a technique node when it carries useful controls:
   - Prefix its `customLabel` with "Contributing:" and say in `evidence` that it is not an attacker action
   - Connect it with a **dashed** edge (see Phase 4); it is a legitimate root node with no incoming edge

6. **Attacker infrastructure** (dead-drop repos, lookalike forks, exfil domains): put it in the `evidence` of the technique that uses it, or as a single technique (e.g. T-V008) in the relevant component. Do NOT create a separate zone for it; zones are for victims.

7. **Downstream consumers** (any malicious package, image, or extension): walk every consumer type and either map it or note "not observed":
   - Developer endpoints (local installs): T-E001, T-E003, C2 techniques
   - CI/CD runners: T-C010, T-C005
   - Production / Kubernetes / cloud: T-P011, T-P007, T-P009
   - Downstream registries (worm-style republishing): T-R004
   - Mark mappings inferred from payload capabilities (vs. observed victims) as `[Inference]` in `evidence`

### Phase 3: Layout Calculation

Apply these layout rules:

#### Rule 1: Component Layout (Left-to-Right by Attack Flow)
- Order components by their **sequence in the attack chain**, not by standard SITF order
- If attack flows CI/CD → Registry → Endpoint → VCS, layout left-to-right accordingly
- Minimum horizontal gap between components: 80-100px
- Component x-positions: Use increments of ~300px starting from x=50

#### Rule 2: Technique Ordering (Top-to-Bottom)
- **Primary**: Order techniques by their **sequence in the attack flow**
- **Secondary**: Within same attack step, order by stage (Initial Access → Discovery → Post-Compromise)
- Vertical gap between techniques: ~130px
- First technique starts at y = component.y + 80

#### Rule 3: Technique-Component Centering
- Every technique node MUST be visually centered within its parent component
- **Centering formula**: `technique.x = component.x + (component.width - technique.width) / 2`
- With component.width=250 and technique.width=160: offset = (250-160)/2 = 45
- Example: component at x=50 → technique at x=95
- Example: component at x=350 → technique at x=395
- Validate technique.data.component matches parent component.data.componentId

#### Rule 4: Component Sizing
- Width = 250px (standard)
- Height = max(500, (technique_count × 130) + 160) — ensures adequate vertical space
- All components should have consistent height for visual alignment

#### Rule 5: Edge Connections
- Technique nodes only have a `top` target handle and a `bottom` source handle (`app/visualizer.html`). Entry points expose `right`/`bottom` sources, exit points `left`/`top` targets
- Use `sourceHandle: "bottom"`, `targetHandle: "top"` within a component. For cross-component edges, `right`/`left` is the convention, but on technique nodes it falls back to bottom/top. Don't design layouts that rely on side connections
- Use `"type": "smoothstep"` for all edges

#### Rule 6: Edge Labels (Minimal)
- Labels overlap nodes on the canvas. Leave most edges unlabeled (`"label": ""`)
- Label at most 3-5 key pivots (typically cross-component or cross-zone), 1-2 words each: "Tokens", "Build source", "Install"
- Timestamps, commit SHAs and other details go in technique `customLabel` / `evidence`, never on edges
- Use a transparent label background and 10px font (see Phase 4 edge structure)

### Phase 4: JSON Generation

Generate the attack flow JSON with this exact structure:

```json
{
  "metadata": {
    "name": "Attack Name",
    "title": "Canvas Display Title",
    "created": "ISO-8601 timestamp",
    "version": "1.0",
    "framework": "SITF",
    "description": "Brief attack description"
  },
  "nodes": [],
  "edges": []
}
```

**Metadata field guidelines:**
- `name`: Short identifier (e.g., "tj-actions", "circleci")
- `title`: Concise canvas title, max 5-7 words (e.g., "tj-actions/changed-files Compromise", "CircleCI Security Incident (2023)")
- `description`: One sentence summary, max 150 characters
- Do NOT write paragraph-length titles — save details for technique customLabels and evidence fields

#### Node Structure - Entry Point
```json
{
  "id": "entryPoint-attackname-1",
  "type": "entryPoint",
  "position": { "x": -150, "y": 200 },
  "data": {
    "label": "Entry Point Label"
  },
  "zIndex": 10,
  "width": 195,
  "height": 46
}
```

#### Node Structure - Component
```json
{
  "id": "component-cicd-1",
  "type": "component",
  "position": { "x": 50, "y": 80 },
  "data": {
    "label": "CI/CD",
    "componentId": "cicd",
    "techniques": [],
    "customLabel": "Context-specific label"
  },
  "zIndex": -1,
  "width": 250,
  "height": 500,
  "style": { "width": 250, "height": 500 }
}
```

#### Node Structure - Technique (CRITICAL: use exact field names)
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
    "controls": {
      "protective": [{ "name": "control1", "frameworks": {...} }],
      "detective": [{ "name": "control2", "frameworks": {...} }]
    },
    "customLabel": "Attack-specific context",
    "evidence": "Optional: specific evidence from the attack"
  },
  "zIndex": 10,
  "width": 160,
  "height": 96
}
```

**IMPORTANT technique.data fields:**
- `id`: Use technique ID (e.g., "T-C003") — NOT "techniqueId"
- `name`: Use technique name — NOT "label"
- `risks`: Copy full array from techniques.json
- `controls`: Copy full object with `protective` and `detective` arrays from techniques.json
- `customLabel`: Add attack-specific context (e.g., "PRs #18018, #18020")
- `evidence`: Optional field for attack-specific evidence

#### Node Structure - Exit Point
```json
{
  "id": "exitPoint-attackname-1",
  "type": "exitPoint",
  "position": { "x": 950, "y": 200 },
  "data": {
    "label": "Secondary Supply Chain Attack"
  },
  "zIndex": 10,
  "width": 144,
  "height": 46
}
```

#### Edge Structure (with full styling)
```json
{
  "id": "edge-source-target",
  "source": "technique-c003-1",
  "sourceHandle": "bottom",
  "target": "technique-c004-1",
  "targetHandle": "top",
  "type": "smoothstep",
  "animated": false,
  "markerEnd": { "type": "arrowclosed" },
  "label": "",
  "labelStyle": { "fill": "#DC2626", "fontWeight": 600, "fontSize": 10 },
  "labelBgStyle": { "fill": "#FFFFFF", "fillOpacity": 0 }
}
```

#### Cross-component Edge (with gray styling)
```json
{
  "id": "edge-cross-component",
  "source": "technique-c011-1",
  "sourceHandle": "right",
  "target": "technique-r001-1",
  "targetHandle": "left",
  "type": "smoothstep",
  "animated": false,
  "style": { "stroke": "#9ca3af" },
  "markerEnd": { "type": "arrowclosed", "color": "#9ca3af" },
  "label": "Tokens",
  "labelStyle": { "fill": "#DC2626", "fontWeight": 600, "fontSize": 10 },
  "labelBgStyle": { "fill": "#FFFFFF", "fillOpacity": 0 }
}
```

#### Contributing-condition Edge (dashed)
Same as the cross-component edge, with `"style": { "stroke": "#9ca3af", "strokeDasharray": "5,5" }` and usually `"label": ""`. Also used for attacker infrastructure the payload depends on (e.g. a C2 dead drop). See `flows/incidents/trivy-act-ii.json`.

Node types:
- `entryPoint`: Attack entry (Phishing, Vulnerability Exploit, Stolen Credentials, Malicious Fork PR, etc.)
- `component`: SITF component container (endpoint, vcs, cicd, registry, production)
- `technique`: Attack technique from techniques.json
- `technique-gap`: Placeholder for missing technique (flag for /technique-proposal)
- `exitPoint`: Attack outcome (Future Breach, Persistence, Secondary Supply Chain Attack, etc.)
- `victimZone`: Visual container grouping components belonging to a single victim organization

#### Victim Zones (Multi-Organization Attacks)

When an attack involves multiple victim organizations (e.g., supply chain attacks that cascade across vendors), use `victimZone` nodes to visually group each victim's components.

**When to use victim zones:**
- Attack spreads from one organization to another (e.g., TeamPCP: Aqua → Checkmarx → GitHub)
- Multiple independent victims are compromised via shared dependency
- Supply chain attack where upstream compromise affects downstream organizations

**Victim Zone Structure:**
```json
{
  "id": "victimZone-aqua",
  "type": "victimZone",
  "position": { "x": -24, "y": 15 },
  "data": {
    "label": "Aqua Security",
    "color": "#3B82F6"
  },
  "zIndex": -10,
  "width": 1444,
  "height": 945,
  "style": { "width": 1444, "height": 945 }
}
```

**Layout rules for victim zones:**
- Place victim zones left-to-right in order of compromise (first victim on left)
- Size each zone to fully contain its components with ~20px padding
- Use distinct colors for each victim (e.g., `#3B82F6` blue, `#06B6D4` cyan, `#8B5CF6` purple)
- Set `zIndex: -10` so zones render behind components and techniques
- Connect cross-zone techniques with edges showing the pivot between organizations
- For a package/image compromise, add a "Downstream Consumers" zone covering the consumer types from Phase 2 step 7
- Don't create zones for attacker infrastructure (see Phase 2 step 6)

**Reference:** See `flows/incidents/teampcp-campaign.json` for a multi-victim example with 4 victim zones.

### Phase 5: Control Gap Analysis

After generating the flow, analyze defensive gaps:

1. For each technique used in the attack:
   - List the protective controls from techniques.json
   - Identify which controls were missing (enabled the attack)
   
2. Generate a **Controls Gap Summary**:
   ```
   | Technique | Missing Control | Type | OWASP SPVS |
   |-----------|-----------------|------|------------|
   | T-C003    | Minimal workflow permissions | Protective | V3.1 |
   | T-C005    | Log sanitization | Protective | V2.5 |
   | T-C005    | Runtime agent on runner | Detective | V5.4 |
   ```

3. Prioritize recommendations by:
   - Number of techniques the control would prevent
   - Stage of attack it would block (earlier = higher priority)

### Phase 6: Validation

Run this checklist before outputting:

```
[ ] Valid JSON structure (parse test passes)
[ ] Required fields present: metadata.{name,title,created,version,framework}, nodes[], edges[]
[ ] All node IDs are unique
[ ] All edge source/target reference valid node IDs
[ ] Technique nodes use data.id and data.name (NOT techniqueId/label)
[ ] Technique nodes include full risks[] array and controls object with protective/detective arrays
[ ] Out-of-scope attack steps noted but not forced into SITF techniques
[ ] All techniques centered within components (x = component.x + 45 for width=250)
[ ] Component heights are adequate (minimum 500px)
[ ] Techniques ordered by attack flow sequence
[ ] Initial Access techniques appear first when order is ambiguous
[ ] All technique IDs exist in techniques.json OR flagged as technique-gap
[ ] Exit points connected to terminal techniques
[ ] No orphaned nodes: every non-entry node has an incoming edge, EXCEPT roots whose customLabel marks them as "Contributing:" or attacker preparation
[ ] Edges have sourceHandle, targetHandle, markerEnd, labelStyle, labelBgStyle
[ ] Edge labels: at most 3-5 non-empty, each 1-2 words, transparent background
[ ] Downstream consumer types each mapped or noted "not observed" (package/image compromises)
[ ] Source conflicts and inferred steps flagged in output
```

### Phase 7: Output

1. Write the JSON file to `flows/incidents/<attack-name>.json` when running in the SITF repository. In any other project, write it to `sitf-flows/<attack-name>.json` under the current project root and tell the user to open it with **Import** in the SITF flow builder (https://wiz-sec-public.github.io/SITF/visualizer.html)
2. Validate the JSON with Python: `python3 -c "import json; json.load(open('file'))"`
3. Provide output summary:

```markdown
## Attack Flow: <attack-name>

### Attack Chain
1. Initial Access via [entry point]
2. [Technique] → [Technique] → ...
3. Impact: [exit point]

### Techniques Used
| ID | Name | Component | Stage |
|----|------|-----------|-------|
| T-C003 | PWN Request | CI/CD | Initial Access |
| ... | ... | ... | ... |

### Control Gaps Identified
| Missing Control | Type | Would Prevent | OWASP SPVS |
|-----------------|------|---------------|------------|
| Minimal workflow permissions | Protective | T-C003 | V3.1 |
| ... | ... | ... | ... |

### Out-of-Scope Steps
- [Step X]: Generic cloud attack, see MITRE ATT&CK T1078

### Technique Gaps
- [Step Y]: No matching SITF technique, run `/technique-proposal`
```

4. If any technique-gaps exist, list them and recommend running `/technique-proposal`

### Iterating on a User-Edited Flow

Users often adjust the layout in the visualizer and save over the file, then ask for more changes.
- Edit the file in place. Preserve the user's positions and sizes, and only move what the new change requires (e.g. widen a zone, shift exits)
- Saving from the visualizer currently resets `metadata.name` to "Attack Flow" and drops `title`/`description`. Check the metadata after every user save and restore it
- To summarize the user's edits, diff the file against your last generated version (nodes/edges added or removed, positions, sizes)

## Example

```
/attack-flow ultralytics websearch
```

This will:
1. Search for ultralytics attack details
2. Map attack steps to SITF techniques
3. Generate `flows/incidents/ultralytics.json`
4. Output attack flow summary

## Reference: Working Sample

See `flows/incidents/ultralytics.json` or `flows/incidents/tj-actions.json` for correctly structured examples.
