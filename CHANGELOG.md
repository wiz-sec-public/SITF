# SITF Updates

This page documents changes to SITF organized by release version.

---

## Current Version: SITF v1.6 (November 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-V013](techniques.json) | VCS Evidence Destruction | VCS |

#### Major Version Changes
_None_

#### Minor Version Changes

New risks and controls from the LiteLLM 1.107.0 compromise (October 2026):

| ID | Added Risks | Added Controls |
|----|-------------|----------------|
| T-V001 | Broad-scope CLI OAuth tokens without expiry; privileged accounts used for daily work | Dedicated admin accounts for org owners; IP allow list for token access (protective). Token usage anomaly detection (detective) |
| T-V003 | Leaked secrets deleted but not revoked; secret scanning limited to the primary org | Revoke leaked secrets, not just delete them (protective) |
| T-V010 | Admins can bypass branch protection | Branch rulesets with no bypass actors (protective). Branch protection override alerting (detective) |
| T-C001 | Release approval satisfiable by any developer account | Dedicated release approver accounts (protective) |
| T-C002 | Build source controllable through workflow inputs | Build source validation against protected branches (protective) |
| T-C005 | Secrets available to workflows on any branch; personal tokens or signing keys stored as CI secrets | Environment-scoped secrets with branch policies; network-level runner egress allow-list (protective). Exfiltration workflow detection on new branches (detective) |
| T-R004 | Trusted publisher not bound to a protected environment; provenance not verified before publishing | Pre-publish provenance verification (protective) |
| T-R005 | Provenance not verified before publishing | Pre-publish provenance verification (protective) |
| T-P011 | Services configured with personal or admin credentials; admin APIs return stored secrets | Service identities instead of personal credentials; write-only secret storage (redact on read) (protective) |

Renamed controls:
- "Secret scanning on org" → "Secret scanning on all orgs" (T-V001, T-V003), to cover sibling and legacy orgs the producer controls

#### Deprecations
_None_

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [LiteLLM October 2026](flows/incidents/litellm-oct-2026.json) | Incident | Leaked admin key leads to an org owner's GitHub token, CI secret theft and a hijacked release of `litellm` 1.107.0 |

### Other Changes
- LiteLLM flow rewritten to follow BerriAI's root-cause analysis (2026-10-23). The entry point is now a leaked, never-revoked admin key rather than an internet-exposed gateway, and the flow adds CI secret exfiltration (T-C005), the lookalike fork (T-V008) and evidence destruction (T-V013)

---

## SITF v1.5 (July 2026)

### Framework Integrations

#### New Framework Mappings

Added MITRE ATT&CK Enterprise v15.0 and AWS Threat Technique Catalog v1.0 mappings to 18 techniques across all pillars:

| Component | Techniques with Mappings |
|-----------|-------------------------|
| Endpoint | T-E001, T-E003 |
| VCS | T-V001, T-V010 |
| CI/CD | T-C003, T-C005 |
| Registry | T-R004, T-R010, T-R011 |
| Production | T-P001, T-P005, T-P006, T-P007, T-P008, T-P009, T-P011, T-P013, T-P014 |

Framework mappings are now displayed in both the Techniques Library and Flow Visualizer with clickable links to MITRE/AWS documentation.

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [AsyncAPI Generator July 2026](flows/incidents/asyncapi-generator-2026.json) | Incident | PWN Request supply chain attack via pull_request_target |
| [Miasma Campaign](flows/incidents/miasma-redhat.json) | Campaign | Multi-channel C2 RAT framework targeting developers |

---

## SITF v1.4 (May 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-V012](techniques.json) | Cross-Fork Object Reference Abuse | VCS |
| [T-R013](techniques.json) | Version String Impersonation | Registry |

#### Major Version Changes
_None_

#### Minor Version Changes
_None_

#### Deprecations
_None_

### Attack Flows

#### New Flows
_None_

### Other Changes
- Added CHANGELOG.md

---

## SITF v1.3 (May 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-E019](techniques.json) | OAuth Token Abuse for Cross-Organizational Access | Endpoint |
| [T-C021](techniques.json) | AI Agent Prompt Injection in Workflow | CI/CD |

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [Vercel April 2026](flows/incidents/vercel-april-2026.json) | Incident | OAuth token compromise affecting Vercel infrastructure |

---

## SITF v1.2 (April 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-R012](techniques.json) | Package Lifecycle Script Abuse | Registry |
| [T-E016](techniques.json) | Blockchain-Based C2 Infrastructure | Endpoint |
| [T-E017](techniques.json) | Legitimate Service Abuse for C2 | Endpoint |
| [T-E018](techniques.json) | BitTorrent DHT for C2 | Endpoint |

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [TeamPCP Campaign](flows/incidents/teampcp-campaign.json) | Incident | Multi-ecosystem supply chain campaign |
| [Trivy Act II](flows/incidents/trivy-act-ii.json) | Incident | GitHub Actions cache poisoning |
| [Synacktiv CI/CD](flows/red-team/synacktiv-cicd-red-team-engagement.json) | Red Team | CI/CD pipeline penetration test |

### Other Changes
- Added victim zones feature to visualizer
- New `/attack-flow` and `/red-team-flow` Claude skills
- Flow files reorganized under `flows/incidents/` and `flows/red-team/`

---

## SITF v1.1 (March 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-V011](techniques.json) | Git Tag/Reference Manipulation | VCS |

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [Aqua Trivy VSCode](flows/incidents/aqua-trivy-vscode.json) | Incident | VSCode extension supply chain attack |

### Other Changes
- Added link anchors to technique library for direct linking

---

## SITF v1.0 (February 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-C020](techniques.json) | CI/CD Misconfiguration Exploitation | CI/CD |

#### Minor Version Changes
- Added OWASP SPVS framework mappings to all techniques
- Split controls into protective and detective categories

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [Clinejection](flows/incidents/clinejection.json) | Incident | AI coding assistant prompt injection |
| [Ultralytics](flows/incidents/ultralytics.json) | Incident | PyPI account compromise |

### Other Changes
- Added `/technique-proposal` Claude skill
- Extended techniques schema with framework mappings

---

## SITF v0.9 (January 2026)

### Techniques

#### New Techniques

| ID | Name | Component |
|----|------|-----------|
| [T-E010](techniques.json) | Endpoint Infrastructure Destruction | Endpoint |
| [T-V009](techniques.json) | Mass Deletion of Repositories | VCS |
| [T-C019](techniques.json) | CI/CD Infrastructure Destruction | CI/CD |
| [T-R009](techniques.json) | Registry Infrastructure Destruction | Registry |
| [T-P014](techniques.json) | Production Infrastructure Destruction | Production |

### Attack Flows

#### New Flows

| Name | Type | Reference |
|------|------|-----------|
| [tj-actions](flows/incidents/tj-actions.json) | Incident | GitHub Actions supply chain compromise |
| [s1ngularity](flows/incidents/s1ngularity.json) | Incident | AI tool weaponization attack |

### Other Changes
- Added interactive visualizer (`visualizer.html`)
- Added technique library browser (`techniques-library.html`)

---

## SITF v0.1 (December 2025)

Initial release of SITF framework.

### Techniques

Initial set of 70 techniques across 5 components:

| Component | Count | Coverage |
|-----------|-------|----------|
| Endpoint | 9 | Developer workstations and IDEs |
| VCS | 8 | Version Control Systems |
| CI/CD | 18 | Build and deployment pipelines |
| Registry | 8 | Package and container registries |
| Production | 13 | Production infrastructure |

### Attack Flows

#### Initial Flows

| Name | Type | Reference |
|------|------|-----------|
| [CircleCI](flows/incidents/circleci-flow.json) | Incident | 2023 CircleCI breach |
| [SolarWinds](flows/incidents/solarwinds.json) | Incident | 2020 SolarWinds supply chain attack |
| [Shai-Hulud-2](flows/incidents/shai-hulud-2-flow.json) | Incident | npm worm propagation |
| [CodeBreach](flows/incidents/codebreach.json) | Incident | Source code exfiltration |
| [TrustWallet](flows/incidents/trustwallet.json) | Incident | Wallet app supply chain |

### Other Changes
- Initial framework documentation
- IMPLEMENTATION_GUIDE.md
- TECHNIQUE_LIBRARY.md

---

## Update Categories

Following [MITRE ATT&CK conventions](https://attack.mitre.org/resources/updates/):

### Techniques

| Category | Description |
|----------|-------------|
| **New Techniques** | Techniques appearing for the first time |
| **Major Version Changes** | Significant scope or definition changes (v1.0→v2.0) |
| **Minor Version Changes** | Control updates, risk additions, clarifications (v1.0→v1.1) |
| **Deprecations** | Techniques no longer recommended for use |
| **Revocations** | Techniques replaced by or merged into another technique |

### Attack Flows

| Type | Description |
|------|-------------|
| **Incident** | Documented public breaches and supply chain attacks |
| **Red Team** | Sanitized penetration test and red team engagement reports |

### Components

| ID | Name |
|----|------|
| Endpoint | Developer workstations and IDEs |
| VCS | Version Control Systems |
| CI/CD | Continuous Integration/Deployment |
| Registry | Package and container registries |
| Production | Production infrastructure |
