#!/usr/bin/env python3
"""
SITF Build Script
Reads techniques.json and generates TECHNIQUE_LIBRARY.md and index.html
"""

import json
from pathlib import Path

def load_techniques_data(json_path):
    """Load techniques data from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data, output_path):
    """Generate TECHNIQUE_LIBRARY.md from techniques data"""
    
    md_lines = []
    
    # Header
    md_lines.append("# SDLC Infrastructure Threat Framework - Technique Library")
    md_lines.append("")
    md_lines.append("## How to Use This Library")
    md_lines.append("")
    md_lines.append("This library contains **technique triplets** - each entry shows:")
    md_lines.append("1. **The Technique** - The attack method")
    md_lines.append("2. **The Risks** - Underlying conditions that enable this technique")
    md_lines.append("3. **The Controls** - Security measures that prevent or detect this technique")
    md_lines.append("")
    md_lines.append("**To analyze an attack:** Find the techniques used in this library, and you'll immediately see what risks enabled them and what controls would have prevented them.")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Impact Types
    md_lines.append("## Impact Types")
    md_lines.append("")
    md_lines.append("When mapping attack flows, connections between techniques can be annotated with impact types to show the consequences of successful exploitation.")
    md_lines.append("")
    md_lines.append("### PRIMARY IMPACTS")
    md_lines.append("Primary impacts occur when an attacker achieves their main objective through the SDLC infrastructure:")
    md_lines.append("")
    for impact in data['impactTypes']['primary']:
        if impact == "Data Exfiltration":
            md_lines.append("- **Data Exfiltration** - Theft of sensitive data, source code, or intellectual property")
        elif impact == "Resource Hijacking":
            md_lines.append("- **Resource Hijacking** - Unauthorized use of computational resources (cryptomining, etc.)")
        elif impact == "Destruction":
            md_lines.append("- **Destruction** - Deletion or corruption of critical assets")
        elif impact == "Pivot to Other Internal Systems":
            md_lines.append("- **Pivot to Other Internal Systems** - Using SDLC access to reach other organizational systems")
        elif impact == "Supply Chain":
            md_lines.append("- **Supply Chain** - Compromising downstream consumers through poisoned artifacts")
    md_lines.append("")
    md_lines.append("### SECONDARY IMPACTS")
    md_lines.append("Secondary impacts are collateral effects or intermediate objectives during an attack:")
    md_lines.append("")
    for impact in data['impactTypes']['secondary']:
        if impact == "Data Exfiltration":
            md_lines.append("- **Data Exfiltration** - Credentials, secrets, or configuration data used for further attacks")
        elif impact == "Resource Hijacking":
            md_lines.append("- **Resource Hijacking** - Temporary resource abuse during attack execution")
        elif impact == "Destruction":
            md_lines.append("- **Destruction** - Covering tracks or causing disruption")
        elif impact == "Pivot to Other Internal Systems":
            md_lines.append("- **Pivot to Other Internal Systems** - Lateral movement within SDLC infrastructure")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Technique Triplets by Component
    md_lines.append("## Technique Triplets by Component")
    md_lines.append("")
    
    # Component headers mapping
    component_headers = {
        'endpoint': 'ENDPOINT / IDE',
        'vcs': 'VCS (Version Control System)',
        'cicd': 'CI/CD',
        'registry': 'REGISTRY (Container / Artifact Registry)',
        'production': 'PRODUCTION / CLOUD'
    }
    
    # Group techniques by component
    techniques_by_component = {}
    for tech in data['techniques']:
        comp = tech['component']
        if comp not in techniques_by_component:
            techniques_by_component[comp] = []
        techniques_by_component[comp].append(tech)
    
    # Sort techniques within each component by ID
    for comp in techniques_by_component:
        techniques_by_component[comp].sort(key=lambda t: t['id'])
    
    # Output techniques by component
    for comp_id in ['endpoint', 'vcs', 'cicd', 'registry', 'production']:
        if comp_id not in techniques_by_component:
            continue
            
        md_lines.append(f"### {component_headers[comp_id]}")
        md_lines.append("")
        
        for tech in techniques_by_component[comp_id]:
            md_lines.append(f"#### {tech['id']}: {tech['name']}")
            md_lines.append("")
            md_lines.append(f"**Technique:** {tech['description']}")
            md_lines.append("")
            md_lines.append("**Risks:**")
            for risk in tech['risks']:
                md_lines.append(f"- {risk}")
            md_lines.append("")
            md_lines.append("**Controls:**")
            for control in tech['controls']:
                md_lines.append(f"- {control}")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
    
    # Quick Reference
    md_lines.append("## Quick Reference: Technique Index by Attack Stage")
    md_lines.append("")
    
    # Group techniques by stage
    techniques_by_stage = {
        'Initial Access': [],
        'Lateral Movement': [],
        'Post-Compromise': [],
        'Discovery': []
    }
    
    for tech in data['techniques']:
        stage = tech.get('stage', 'Post-Compromise')
        if stage in techniques_by_stage:
            techniques_by_stage[stage].append(tech)
    
    # Sort techniques within each stage by ID
    for stage in techniques_by_stage:
        techniques_by_stage[stage].sort(key=lambda t: t['id'])
    
    # Output by stage
    for stage_name in ['Initial Access', 'Lateral Movement', 'Post-Compromise', 'Discovery']:
        if not techniques_by_stage[stage_name]:
            continue
        
        md_lines.append(f"### {stage_name} Techniques")
        for tech in techniques_by_stage[stage_name]:
            md_lines.append(f"- {tech['id']}: {tech['name']}")
        md_lines.append("")
    
    md_lines.append("---")
    md_lines.append("")
    
    # Usage example
    md_lines.append("## How to Use This Library for Attack Analysis")
    md_lines.append("")
    md_lines.append("### Example: Analyzing the Shai-Hulud-2 Attack")
    md_lines.append("")
    md_lines.append("**Step 1: Identify the techniques used**")
    md_lines.append("- T-C003: PWN Request / Poisoned Pipeline Execution")
    md_lines.append("- T-C005: Secret Exfiltration from Workflow")
    md_lines.append("- T-R004: Publishing Malicious Package")
    md_lines.append("- T-E001: Malicious Execution on Endpoint")
    md_lines.append("- T-E003: Harvest Local Secrets / Credentials from Endpoint")
    md_lines.append("- T-E006: Register Local Machine as CI Runner")
    md_lines.append("")
    md_lines.append("**Step 2: Look up each technique in the library**")
    md_lines.append("")
    md_lines.append("Each technique entry shows you:")
    md_lines.append("- The risks that enabled it")
    md_lines.append("- The controls that would have prevented it")
    md_lines.append("")
    md_lines.append("**Step 3: Create your defense plan**")
    md_lines.append("")
    md_lines.append("Map all the controls from the techniques used:")
    md_lines.append("- Branch protection rules (VCS)")
    md_lines.append("- Require explicit approval for workflows from forks (VCS)")
    md_lines.append("- OIDC setup in workflows")
    md_lines.append("- Runtime agent on runner")
    md_lines.append("- Trusted publishing")
    md_lines.append("- EDR on endpoint")
    md_lines.append("- Local DLP")
    md_lines.append("- Using managed runners only")
    md_lines.append("")
    md_lines.append("**Step 4: Prioritize based on attack path**")
    md_lines.append("")
    md_lines.append("Focus on controls that break the most critical pivot points:")
    md_lines.append("1. OIDC (prevents secret theft from CI/CD)")
    md_lines.append("2. Trusted publishing (prevents registry compromise)")
    md_lines.append("3. EDR (detects endpoint compromise)")
    md_lines.append("4. Network segmentation (prevents production pivot)")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

def generate_standalone_html(template_path, output_path, data):
    """Generate standalone HTML with embedded data"""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Convert data to JavaScript
    js_data = f"const techniquesData = {json.dumps(data, indent=2)};"
    
    # Replace the placeholder
    html = template.replace('{{EMBEDDED_DATA}}', js_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_techniques_library_html(template_path, output_path, data):
    """Generate techniques library visual explorer HTML"""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Convert data to JavaScript
    js_data = f"const techniquesData = {json.dumps(data, indent=2)};"
    
    # Replace the placeholder
    html = template.replace('{{EMBEDDED_DATA}}', js_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Main build process"""
    
    # Paths
    script_dir = Path(__file__).parent
    root_dir = script_dir  # Script is in root directory
    json_path = root_dir / 'techniques.json'
    md_path = root_dir / 'TECHNIQUE_LIBRARY.md'
    template_path = root_dir / 'app' / 'index.html.template'
    output_path = root_dir / 'app' / 'index.html'
    library_template_path = root_dir / 'app' / 'techniques-library.html.template'
    library_output_path = root_dir / 'app' / 'techniques-library.html'
    
    print("🔨 SITF Build Script")
    print("=" * 50)
    
    # Check if files exist
    if not json_path.exists():
        print(f"❌ Error: {json_path} not found")
        print("   Run extract_to_json.py first to create techniques.json")
        return 1
    
    if not template_path.exists():
        print(f"❌ Error: {template_path} not found")
        return 1
    
    if not library_template_path.exists():
        print(f"❌ Error: {library_template_path} not found")
        return 1
    
    # Load JSON data
    print(f"📖 Loading {json_path.name}...")
    data = load_techniques_data(json_path)
    
    print(f"   ✓ Found {len(data['components'])} components")
    print(f"   ✓ Found {len(data['techniques'])} techniques")
    print(f"   ✓ Found {len(data['entryPoints'])} entry points")
    print(f"   ✓ Found {len(data['exitPoints'])} exit points")
    
    # Generate Markdown
    print(f"\n📝 Generating {md_path.name}...")
    generate_markdown(data, md_path)
    md_size = md_path.stat().st_size / 1024
    print(f"   ✓ Generated: {md_size:.1f} KB")
    
    # Generate Flow Builder HTML
    print(f"\n🏗️  Generating flow builder HTML...")
    generate_standalone_html(template_path, output_path, data)
    
    # Calculate file sizes
    template_size = template_path.stat().st_size / 1024
    output_size = output_path.stat().st_size / 1024
    data_size = output_size - template_size
    
    print(f"   ✓ Template: {template_size:.1f} KB")
    print(f"   ✓ Embedded data: {data_size:.1f} KB")
    print(f"   ✓ Output: {output_size:.1f} KB")
    
    # Generate Techniques Library HTML
    print(f"\n📚 Generating techniques library HTML...")
    generate_techniques_library_html(library_template_path, library_output_path, data)
    
    library_template_size = library_template_path.stat().st_size / 1024
    library_output_size = library_output_path.stat().st_size / 1024
    library_data_size = library_output_size - library_template_size
    
    print(f"   ✓ Template: {library_template_size:.1f} KB")
    print(f"   ✓ Embedded data: {library_data_size:.1f} KB")
    print(f"   ✓ Output: {library_output_size:.1f} KB")
    
    print(f"\n✅ Build complete!")
    print(f"   Markdown: {md_path}")
    print(f"   Flow Builder: {output_path}")
    print(f"   Techniques Library: {library_output_path}")
    print(f"\n💡 To explore techniques: Open {library_output_path.name} in your browser")
    print(f"💡 To create flows: Open {output_path.name} in your browser")
    
    return 0

if __name__ == '__main__':
    exit(main())
