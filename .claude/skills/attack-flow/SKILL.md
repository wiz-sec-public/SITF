---
name: attack-flow
description: Generate SITF-compliant attack flow JSON files from attack descriptions or incident reports. Use when analyzing supply chain attacks, breaches, or security incidents.
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
- `source`: URL, "websearch" for auto-research, or omit to use conversation context

Arguments: $ARGUMENTS

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

### Phase 2: Technique Mapping

1. Read `techniques.json` to get the full technique library.

2. For each attack step, find the best matching technique:
   - Match by **action semantics**, not surface keywords
   - Example: Uploading stolen data to repos → T-V003 (Secret Exfiltration), NOT T-V008 (Malicious Hosting)
   - Example: Accessing VCS with stolen creds → T-V001 must come BEFORE any VCS actions

3. If no matching technique exists:
   - Create a placeholder node with `"type": "technique-gap"`
   - Include suggested technique metadata in the data field
   - Note in output that `/technique-proposal` should be run for gaps

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
- Connect source.bottom → target.top for vertical flows within component
- Connect source.right → target.left for cross-component flows
- Add labels for significant transitions ("Stolen token", "pip install", etc.)
- Use `"type": "smoothstep"` for all edges

### Phase 4: JSON Generation

Generate the attack flow JSON with this exact structure:

```json
{
  "metadata": {
    "name": "Attack Name",
    "created": "ISO-8601 timestamp",
    "version": "1.0",
    "framework": "SITF",
    "description": "Brief attack description"
  },
  "nodes": [],
  "edges": []
}
```

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
    "controls": ["control1", "control2"],
    "customLabel": "Attack-specific context"
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
- `controls`: Copy full array from techniques.json
- `customLabel`: Add attack-specific context (e.g., "PRs #18018, #18020")

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
  "zIndex": 100,
  "markerEnd": { "type": "arrowclosed" },
  "label": "",
  "labelStyle": { "fill": "#DC2626", "fontWeight": 600, "fontSize": 12 },
  "labelBgStyle": { "fill": "#FEE2E2", "fillOpacity": 0.9 }
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
  "zIndex": 100,
  "style": { "stroke": "#9ca3af" },
  "markerEnd": { "type": "arrowclosed", "color": "#9ca3af" },
  "label": "Transition label",
  "labelStyle": { "fill": "#DC2626", "fontWeight": 600, "fontSize": 12 },
  "labelBgStyle": { "fill": "#FEE2E2", "fillOpacity": 0.9 }
}
```

Node types:
- `entryPoint`: Attack entry (Phishing, Vulnerability Exploit, Stolen Credentials, Malicious Fork PR, etc.)
- `component`: SITF component container (endpoint, vcs, cicd, registry, production)
- `technique`: Attack technique from techniques.json
- `technique-gap`: Placeholder for missing technique (flag for /technique-proposal)
- `exitPoint`: Attack outcome (Future Breach, Persistence, Secondary Supply Chain Attack, etc.)

### Phase 5: Validation

Run this checklist before outputting:

```
[ ] Valid JSON structure (parse test passes)
[ ] Required fields present: metadata.{name,created,version,framework}, nodes[], edges[]
[ ] All node IDs are unique
[ ] All edge source/target reference valid node IDs
[ ] Technique nodes use data.id and data.name (NOT techniqueId/label)
[ ] Technique nodes include full risks[] and controls[] arrays
[ ] All techniques centered within components (x = component.x + 45 for width=250)
[ ] Component heights are adequate (minimum 500px)
[ ] Techniques ordered by attack flow sequence
[ ] Initial Access techniques appear first when order is ambiguous
[ ] All technique IDs exist in techniques.json OR flagged as technique-gap
[ ] Exit points connected to terminal techniques
[ ] No orphaned nodes (every non-entry node has incoming edge)
[ ] Edges have sourceHandle, targetHandle, markerEnd, labelStyle, labelBgStyle
```

### Phase 6: Output

1. Write the JSON file to `sample-flows/<attack-name>.json`
2. Validate the JSON with Python: `python3 -c "import json; json.load(open('file'))"`
3. Provide a summary table of the attack flow
4. If any technique-gaps exist, list them and recommend running `/technique-proposal`

## Example

```
/attack-flow ultralytics websearch
```

This will:
1. Search for ultralytics attack details
2. Map attack steps to SITF techniques
3. Generate `sample-flows/ultralytics.json`
4. Output attack flow summary

## Reference: Working Sample

See `sample-flows/ultralytics.json` or `sample-flows/tj-actions.json` for correctly structured examples.
