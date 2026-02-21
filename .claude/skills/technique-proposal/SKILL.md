---
name: technique-proposal
description: Generate a PR-ready technique proposal when an attack step doesn't map to existing SITF techniques. Use after /attack-flow identifies technique gaps.
argument-hint: "<description>" [component]
tools: Read, Grep, Glob
---

# Technique Proposal Generator

Generate a PR-ready technique proposal when an attack step doesn't map to existing SITF techniques.

## Usage

```
/technique-proposal <description> [component]
```

- `description`: Description of the attack step or gap
- `component`: Target component (endpoint, vcs, cicd, registry, production) - optional, will be inferred if omitted

Arguments: $ARGUMENTS

## Instructions

When this skill is invoked:

### Phase 1: Gap Analysis

1. Read `techniques.json` to understand existing techniques.

2. Confirm the gap:
   - Search for semantically similar techniques
   - Verify no existing technique covers this attack step
   - If a match exists, report it and exit

3. **Verify the attack step is within SITF scope** (see Scope Boundaries below)

4. Identify the correct component:
   - endpoint: Developer workstations, IDEs, local tools
   - vcs: Version control systems (GitHub, GitLab, etc.)
   - cicd: CI/CD pipelines, runners, workflows
   - registry: Package registries, container registries
   - production: Production infrastructure **as it relates to supply chain attacks**

5. Determine the attack stage:
   - Initial Access: First foothold in the component
   - Discovery and Lateral Movement: Enumeration, pivoting, credential theft
   - Post-Compromise: Data exfiltration, destruction, persistence

### Scope Boundaries

**SITF covers SDLC infrastructure and software supply chain attacks specifically.** Not all attack steps in an incident warrant new SITF techniques.

#### In Scope (propose technique)
- Attacks on developer workstations, IDEs, and local development tools
- Attacks on version control systems and source code
- Attacks on CI/CD pipelines, runners, and build systems
- Attacks on package/container registries
- Production techniques that are **supply-chain-specific**:
  - Backdooring deployed artifacts to compromise downstream consumers
  - Stealing code signing keys or certificates
  - Modifying release pipelines or deployment configurations
  - Accessing production to pivot back into SDLC systems

#### Out of Scope (do NOT propose technique)
- Generic cloud infrastructure attacks (IAM privilege escalation, cloud misconfigurations)
- Generic container/Kubernetes attacks (pod escape, RBAC abuse, kubelet exploits)
- Generic network attacks (lateral movement via SSH, RDP exploitation)
- Post-exploitation techniques that don't relate to software supply chain

**Example:** If an attacker uses CI/CD as initial access, then pivots to cloud production and uses a Kubernetes privilege escalation technique, the K8s privesc is **out of scope** for SITF. Instead:

1. For attack flows: Mark the step with `"type": "out-of-scope"` and reference the appropriate framework (e.g., "MITRE ATT&CK: Escape to Host - T1611")
2. For technique proposals: Report that the attack step is outside SITF's domain and does not warrant a new technique

**Rationale:** These generic infrastructure techniques are already well-documented in:
- MITRE ATT&CK for Enterprise (Cloud, Containers matrices)
- MITRE ATT&CK for ICS
- Cloud-specific frameworks (AWS Security Maturity Model, Azure Security Benchmark)

SITF adds value by covering the **unique attack surface of SDLC infrastructure** that these frameworks don't address comprehensively.

### Phase 2: Technique ID Assignment

1. Find the highest existing ID for the target component:
   - Endpoint: T-E###
   - VCS: T-V###
   - CI/CD: T-C###
   - Registry: T-R###
   - Production: T-P###

2. Assign the next sequential number.

### Phase 3: Technique Definition

Generate the technique entry following these conventions:

#### Name
- Action-oriented verb phrase
- Match style of existing techniques in same component
- Avoid vendor-specific terms unless unavoidable
- Examples: "Abuse Local AI Tools", "Harvest Local Secrets", "Turn Private Repos Public"

#### Description
- Single sentence describing the attack action
- Focus on what the attacker does, not the impact
- Start with "Attacker..." for consistency

#### Risks
- Focus on **why** this attack is possible (enabling conditions)
- Describe misconfigurations, missing controls, insecure defaults
- Keep each risk as a concise phrase, not a full sentence
- Reference similar risks from related techniques for consistency

#### Controls (Protective vs Detective)

Controls MUST be split into two categories:

**Protective Controls** - Configuration-based measures that prevent attacks:
- Settings, policies, permissions that block attacks before they happen
- Static configurations that don't require active monitoring
- Examples: MFA enforcement, branch protection, network segmentation, sandboxing

**Detective Controls** - Monitoring and detection capabilities:
- Requires active observation and alerting
- Identifies attacks in progress or after the fact
- Examples: EDR, audit log monitoring, secret scanning, runtime agents

For each control, include:
- `name`: Control name (action-oriented)
- `description`: Optional detailed description
- `frameworks`: Array of OWASP SPVS categories (see Framework Mappings)

For detective controls, optionally include:
- `detectionRules`: Array of detection rule references (Sigma, etc.)

#### Framework Mappings

Map each control to the appropriate OWASP SPVS category:

| Category | Description | Typical Controls |
|----------|-------------|------------------|
| **V1.1** | Identity and Access Management | MFA, SSO, OIDC, PAT policies |
| **V1.2** | Hardening User Machines | IDE sandboxing, app whitelisting, credential storage |
| **V1.3** | Security Requirements | Policies, security awareness training |
| **V1.4** | Developer Tool Operation | AI tool policies, WebRTC restrictions |
| **V1.5** | Source Code Management Hardening | Branch protection, commit signing, code review |
| **V2.1** | Secure Coding Practices | Input sanitization, Unicode normalization |
| **V2.3** | Code Review and Analysis | Workflow review, IaC review |
| **V2.5** | Credential Hygiene | Credential rotation, log sanitization |
| **V2.6** | 3rd Party Library Audit | Package pinning, dependency review |
| **V3.1** | Security of Pipeline Environment | Runner isolation, workflow permissions |
| **V3.2** | Credential Hygiene (CI/CD) | OIDC in workflows, trusted publishing |
| **V3.3** | Continuous Security Checks | Cache verification, artifact signing |
| **V3.4** | Integrity of Artifacts | Image signing, provenance attestation |
| **V4.1** | Final Security Assessments | Extension review, canary testing |
| **V4.2** | Compliance Checks | CSPM/CNAPP, resource tagging |
| **V4.3** | Secure Deployment Practices | Deployment approval gates |
| **V4.4** | Transition Security | Network segmentation |
| **V5.1** | Access Audit | Access reviews, least privilege |
| **V5.2** | Security Standard Enforcement | Rate limiting, metadata restrictions |
| **V5.3** | Secure Maintenance Practices | Patching, backups, recovery |
| **V5.4** | Detection & Monitoring | EDR, runtime agents, audit logs, scanning |
| **V5.5** | Incident Response & Recovery | HSM, encryption, key management |

Also map to MITRE ATT&CK techniques where applicable:
- Include technique ID (e.g., T1059.004)
- Include technique name
- Include tactic (Initial Access, Execution, etc.)

### Phase 4: Generate Output

Produce a structured proposal with four sections:

#### Section 1: Rationale
Explain:
- What attack behavior this technique covers
- Why existing techniques don't cover it
- Reference to real-world attack(s) demonstrating this technique

#### Section 2: Technique JSON
```json
{
  "id": "T-X###",
  "name": "Technique Name",
  "component": "component-id",
  "stage": "Attack Stage",
  "description": "Attacker does X to achieve Y",
  "risks": [
    "Enabling condition 1",
    "Enabling condition 2"
  ],
  "controls": {
    "protective": [
      {
        "name": "Control name",
        "description": "What this control does",
        "frameworks": ["V3.1"]
      }
    ],
    "detective": [
      {
        "name": "Control name",
        "description": "What this control detects",
        "frameworks": ["V5.4"],
        "detectionRules": [
          {
            "source": "sigma",
            "ruleId": "rule_id",
            "ruleName": "Rule Name",
            "description": "What the rule detects"
          }
        ]
      }
    ]
  },
  "frameworkMappings": {
    "mitre_attack": [
      {
        "techniqueId": "T1234",
        "techniqueName": "Technique Name",
        "tactic": "Tactic Name"
      }
    ],
    "owasp_spvs": ["V3.1", "V5.4"]
  }
}
```

#### Section 3: Controls Summary Table

Provide a summary table of all controls:

```markdown
| Control | Type | OWASP SPVS |
|---------|------|------------|
| Control name 1 | Protective | V3.1 |
| Control name 2 | Detective | V5.4 |
```

#### Section 4: PR Description
Markdown-formatted PR description including:
- Title: "Add technique T-X###: Technique Name"
- Summary of the technique
- Controls count (protective/detective)
- Framework mappings summary
- Real-world references
- Link to related attack flow if applicable

### Phase 5: Validation

Run this checklist before outputting:

```
[ ] Attack step is within SITF scope (SDLC/supply-chain-specific, not generic infra)
[ ] ID follows component naming pattern (T-E/V/C/R/P + number)
[ ] ID doesn't conflict with existing techniques in techniques.json
[ ] Name is action-oriented verb phrase
[ ] Name matches naming style of component's existing techniques
[ ] Stage correctly reflects attack progression semantics
[ ] Description starts with "Attacker..."
[ ] Risks explain enabling conditions, not impacts
[ ] Controls are split into protective and detective arrays
[ ] Each control has name and frameworks array
[ ] Framework mappings use valid OWASP SPVS categories (V1-V5)
[ ] MITRE ATT&CK mappings included where applicable
[ ] No semantic duplicate of existing technique
[ ] JSON is valid and properly formatted
```

**If scope check fails:** Do not generate a technique proposal. Instead, explain why the attack step is out of scope and recommend the appropriate framework (MITRE ATT&CK, etc.).

### Phase 6: Output Location

1. Display the full proposal in the conversation
2. Optionally create a file at `technique-proposals/<technique-id>.md` if requested

## Example

```
/technique-proposal "Malware invokes AI CLI tools with permission-bypass flags to scan filesystem" endpoint
```

### Example Output

```markdown
## Technique Proposal: T-E019

### Rationale

The s1ngularity attack (August 2025) demonstrated a novel technique where
malware invoked AI CLI tools (Claude, Gemini, Q) with permission-bypass
flags like `--dangerously-skip-permissions` to scan filesystems and catalog
sensitive files.

Existing technique T-E009 (Abuse Local AI Tools) focuses on using AI
assistants to exfiltrate code or inject malicious suggestions via AI
services. It does not cover the scenario where attackers weaponize local
AI tools for automated reconnaissance by exploiting dangerous CLI flags.

### Proposed Addition to techniques.json

{
  "id": "T-E019",
  "name": "Weaponize AI CLI Tools for Reconnaissance",
  "component": "endpoint",
  "stage": "Discovery and Lateral Movement",
  "description": "Attacker invokes AI CLI tools with permission-bypass flags to scan filesystem and catalog sensitive files for exfiltration",
  "risks": [
    "AI CLI tools support dangerous permission-bypass flags",
    "No restrictions on AI tool command-line invocation",
    "AI tools have broad filesystem access",
    "No monitoring of AI tool execution patterns",
    "AI tools can be invoked non-interactively by scripts"
  ],
  "controls": {
    "protective": [
      {
        "name": "Disable dangerous permission-bypass flags",
        "description": "Remove or disable flags like --dangerously-skip-permissions from AI tools",
        "frameworks": ["V1.4"]
      },
      {
        "name": "Filesystem access restrictions for AI processes",
        "description": "Limit AI tool access to specific directories",
        "frameworks": ["V1.2"]
      },
      {
        "name": "Require interactive confirmation for sensitive operations",
        "description": "Force user approval for filesystem scanning operations",
        "frameworks": ["V1.4"]
      },
      {
        "name": "Application allowlisting for AI tool binaries",
        "description": "Only allow approved AI tool versions to execute",
        "frameworks": ["V1.2"]
      }
    ],
    "detective": [
      {
        "name": "AI tool invocation monitoring",
        "description": "Monitor and alert on AI CLI tool execution patterns",
        "frameworks": ["V5.4"],
        "detectionRules": [
          {
            "source": "sigma",
            "ruleId": "proc_creation_ai_tool_bypass_flag",
            "ruleName": "AI Tool Executed with Permission Bypass Flag",
            "description": "Detects AI CLI tools invoked with dangerous flags"
          }
        ]
      },
      {
        "name": "EDR detection rules for AI tool abuse",
        "description": "EDR rules to detect malicious AI tool usage patterns",
        "frameworks": ["V5.4"]
      }
    ]
  },
  "frameworkMappings": {
    "mitre_attack": [
      {
        "techniqueId": "T1083",
        "techniqueName": "File and Directory Discovery",
        "tactic": "Discovery"
      },
      {
        "techniqueId": "T1119",
        "techniqueName": "Automated Collection",
        "tactic": "Collection"
      }
    ],
    "owasp_spvs": ["V1.2", "V1.4", "V5.4"]
  }
}

### Controls Summary

| Control | Type | OWASP SPVS |
|---------|------|------------|
| Disable dangerous permission-bypass flags | Protective | V1.4 |
| Filesystem access restrictions for AI processes | Protective | V1.2 |
| Require interactive confirmation for sensitive operations | Protective | V1.4 |
| Application allowlisting for AI tool binaries | Protective | V1.2 |
| AI tool invocation monitoring | Detective | V5.4 |
| EDR detection rules for AI tool abuse | Detective | V5.4 |

### PR Description

**Add technique T-E019: Weaponize AI CLI Tools for Reconnaissance**

This PR adds a new endpoint technique to cover the weaponization of AI CLI
tools for automated reconnaissance, as demonstrated in the s1ngularity
supply chain attack (August 2025).

**Controls:**
| Type | Count |
|------|-------|
| Protective | 4 |
| Detective | 2 |

**Framework Mappings:**
- OWASP SPVS: V1.2, V1.4, V5.4
- MITRE ATT&CK: T1083 (File and Directory Discovery), T1119 (Automated Collection)

**References:**
- https://www.wiz.io/blog/s1ngularity-supply-chain-attack

**Related:** sample-flows/s1ngularity.json
```

## Control Classification Guidelines

### Protective Controls - Characteristics
- **Configuration-based**: Settings, policies, permissions
- **Preventive**: Stops attacks before they happen
- **Static**: Doesn't require active monitoring
- **Examples**:
  - MFA enforcement
  - Branch protection rules
  - Network segmentation
  - Access control policies
  - Encryption at rest
  - Package version pinning
  - Sandboxing

### Detective Controls - Characteristics
- **Monitoring-based**: Requires active observation
- **Reactive**: Identifies attacks in progress or after
- **Dynamic**: Generates alerts and events
- **Examples**:
  - EDR alerts
  - Audit log monitoring
  - Secret scanning
  - Runtime agents
  - Network traffic analysis
  - Anomaly detection

### Dual-Purpose Controls

Some controls can exist in both categories. The distinction is:
- **Protective**: The existence/deployment of the control (configuration)
- **Detective**: The specific rules/signatures that detect TTPs

**Example: EDR on endpoint**
- Protective: "EDR deployed on endpoint" - the configuration
- Detective: "EDR detection rule for suspicious process execution" - the specific rule

## Workflow Integration

This skill is typically used after `/attack-flow` identifies technique gaps:

```
/attack-flow <attack-name>
    ↓
[Gaps identified with type: "technique-gap"]
    ↓
/technique-proposal "<gap description>" <component>
    ↓
[Submit PR with proposed technique]
    ↓
[After merge, update attack-flow to use new technique]
```
