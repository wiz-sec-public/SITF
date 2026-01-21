# SITF Attack Flow Visualizer

Interactive web application for visualizing attack flows using the SDLC Infrastructure Threat Framework.

![Shai-Hulud-2 Attack Flow](screenshots/shai-hulud-2-flow.png)
*Example: Shai-Hulud-2 attack flow showing PWN request -> Secret exfiltration -> Malicious package -> Endpoint compromise*

## Quick Start

### Option 1: Use Pre-built HTML (Recommended)

Simply open the HTML files in your browser - no server needed! All data is embedded.

- **`techniques-library.html`** - Visual explorer for browsing techniques with filtering and search
- **`visualizer.html`** - Attack flow builder for creating and analyzing attack diagrams

### Option 2: Build from Source

If you modify `techniques.json`, rebuild the files:

```bash
python3 build-techniques.py
```

This generates:
- `TECHNIQUE_LIBRARY.md` - Human-readable technique documentation
- `app/techniques-library.html` - Visual technique explorer (~63 KB)
- `app/visualizer.html` - Attack flow builder application (~149 KB)

## Features

### Attack Flow Builder (`visualizer.html`)
- **Zero Dependencies**: Standalone HTML file with embedded data
- **Drag-and-drop interface** for building attack flows
- **63 attack techniques** with pre-mapped risks and controls
- **Auto-populating Controls Matrix** showing security controls by component and stage
- **Export options**: PNG, SVG, PDF, and CSV
- **Dark/light theme** toggle
- **Save/Load flows** as JSON files
- **Editable labels** on techniques and components

### Techniques Library Explorer (`techniques-library.html`)
- **Visual browsing** of all 63 techniques organized by component and attack stage
- **Real-time filtering** by component (Endpoint, VCS, CI/CD, Registry, Production)
- **Stage filtering** (Initial Access, Lateral Movement, Post-Compromise, Discovery)
- **Search functionality** across technique names, descriptions, risks, and controls
- **Interactive statistics** showing technique counts, risks, and controls
- **Color-coded components** for easy visual identification
- **Responsive design** works on desktop and mobile

## Architecture

```
techniques.json (Source of Truth)
         ↓
  build-techniques.py (Generator)
         ↓
    ┌────┴────┬────────────┐
    ↓         ↓            ↓
TECHNIQUE_LIBRARY.md   techniques-library.html   visualizer.html
(Documentation)        (Visual Explorer)         (Flow Builder)
```



## Development Workflow

### Adding/Editing Techniques

1. Edit techniques in `../techniques.json`
2. Run `python3 app/build-techniques.py` to regenerate files
3. Review generated `TECHNIQUE_LIBRARY.md` for documentation
4. Open `visualizer.html` in browser to test the web app
5. Commit changes to version control

### JSON Structure

```json
{
  "components": [...],
  "entryPoints": [...],
  "exitPoints": [...],
  "impactTypes": {...},
  "techniques": [
    {
      "id": "T-X001",
      "name": "Technique Name",
      "component": "endpoint|vcs|cicd|registry|production",
      "stage": "Initial Access|Lateral Movement|Post-Compromise|Discovery",
      "description": "What the attacker does",
      "risks": ["Risk 1", "Risk 2", ...],
      "controls": ["Control 1", "Control 2", ...]
    }
  ]
}
```

## Documentation

See [IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md) for complete usage instructions and methodology.

---

Part of the SDLC Infrastructure Threat Framework (SITF)
