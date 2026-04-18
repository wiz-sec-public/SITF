# SDLC Infrastructure Threat Framework - Technique Library

## How to Use This Library

This library contains **technique triplets** - each entry shows:
1. **The Technique** - The attack method
2. **The Risks** - Underlying conditions that enable this technique
3. **The Controls** - Security measures that prevent or detect this technique

Controls are split into two categories:
- 🛡️ **Protective Controls** - Configuration-based measures that prevent attacks
- 🔍 **Detective Controls** - Monitoring and detection rules that identify attacks

**To analyze an attack:** Find the techniques used in this library, and you'll immediately see what risks enabled them and what controls would have prevented them.

---

## Technique Triplets by Component

### ENDPOINT / IDE

#### T-E001: Malicious Execution on Endpoint

**Technique:** Attacker executes malicious code on developer workstation

**Risks:**
- Using untrusted IDE extensions
- Using untrusted software packages on endpoints
- No EDR
- Lack of application sandboxing
- Package installation scripts enabled
- Direct downloads from public registries

**Protective Controls:** 🛡️
- Local registry proxy with filtering
- IDE sandboxing
- Mandating signed extensions
- Package version pinning
- Automated maintainer reputation and hygiene checks
- Application whitelisting
- Disable package installation scripts (--ignore-scripts)

**Detective Controls:** 🔍
- EDR on endpoint

---

#### T-E002: Endpoint Phishing

**Technique:** Attacker phishes developer to steal credentials or install malware

**Risks:**
- Lack of 2FA / phishing protection
- No security awareness training
- Credentials stored in plaintext
- No email security controls

**Protective Controls:** 🛡️
- Mandatory MFA
- Phishing-resistant authentication
- Security awareness training
- Email security (SPF, DMARC, DKIM)

**Detective Controls:** 🔍
- EDR on endpoint

---

#### T-E003: Harvest Local Secrets / Credentials from Endpoint

**Technique:** Attacker extracts credentials stored on developer machine

**Risks:**
- Credentials stored in plaintext
- Production credentials on developer machines
- No local DLP
- SSH keys without passwords
- Cloud credentials in environment variables

**Protective Controls:** 🛡️
- Credential manager enforcement
- No production credentials on endpoints
- Encrypted credential storage

**Detective Controls:** 🔍
- Local DLP
- EDR on endpoint

---

#### T-E004: Harvest Local Data from Endpoint

**Technique:** Attacker exfiltrates source code, documents, or other sensitive data from endpoint

**Risks:**
- No local DLP
- No EDR
- Sensitive data stored locally
- No encryption at rest

**Protective Controls:** 🛡️
- Data classification and handling policies
- Encryption at rest

**Detective Controls:** 🔍
- Local DLP
- EDR on endpoint
- Network monitoring

---

#### T-E005: Cryptomining on Endpoints

**Technique:** Attacker uses endpoint resources for cryptocurrency mining

**Risks:**
- No EDR
- Untrusted software packages
- No resource monitoring

**Protective Controls:** 🛡️
- Application whitelisting

**Detective Controls:** 🔍
- EDR on endpoint
- Resource monitoring and alerting
- Network monitoring (detect mining pool connections)

---

#### T-E006: Register Local Machine as CI Runner

**Technique:** Attacker registers compromised endpoint as self-hosted CI/CD runner

**Risks:**
- Ability to register arbitrary machines as runners
- No runner registration approval process
- Runner registration tokens not protected

**Protective Controls:** 🛡️
- Using managed runners only
- Runner registration approval workflow
- Runner registration token protection
- Network segmentation (runners isolated from endpoints)

**Detective Controls:** 🔍
- (none)

---

#### T-E007: Abuse Local VCS Access from Endpoint

**Technique:** Attacker uses local git credentials to access VCS

**Risks:**
- VCS credentials stored on endpoint
- No credential rotation
- Overprivileged VCS access

**Protective Controls:** 🛡️
- Credential manager enforcement
- Fine-grained PATs with expiration
- Mandatory MFA for VCS

**Detective Controls:** 🔍
- Audit log monitoring

---

#### T-E008: Abuse Local CI/CD Access from Endpoint

**Technique:** Attacker uses local CI/CD credentials to access CI/CD system

**Risks:**
- CI/CD credentials stored on endpoint
- No credential rotation
- Overprivileged CI/CD access

**Protective Controls:** 🛡️
- Credential manager enforcement
- OIDC instead of long-lived tokens
- Mandatory MFA for CI/CD

**Detective Controls:** 🔍
- Audit log monitoring

---

#### T-E009: Abuse Local AI Tools

**Technique:** Attacker uses AI coding assistants to exfiltrate code or inject malicious suggestions

**Risks:**
- Using untrusted AI tools
- No acceptable use policy
- AI tools with excessive permissions
- Sensitive code sent to AI services

**Protective Controls:** 🛡️
- Acceptable use policy against unapproved AI tools
- Approved AI tools with data protection
- Code review for AI-generated code

**Detective Controls:** 🔍
- Network monitoring for AI service connections

---

#### T-E010: Endpoint Infrastructure Destruction

**Technique:** Attacker destroys or corrupts endpoint systems, data, or configurations to cause operational disruption

**Risks:**
- No backup and recovery
- Overprivileged local user accounts
- No EDR
- Lack of system integrity monitoring
- Insufficient access controls on critical system files

**Protective Controls:** 🛡️
- Regular endpoint backups
- Minimal local user privileges
- Offline backup storage
- File system access controls
- Endpoint recovery procedures

**Detective Controls:** 🔍
- EDR on endpoint
- System integrity monitoring

---

#### T-E011: Unicode Stealth Code Injection

**Technique:** Attacker uses invisible Unicode characters (variation selectors, zero-width characters) to hide malicious code that doesn't render in code editors but executes normally

**Risks:**
- Using untrusted IDE extensions
- No code review detection of invisible characters
- Static analysis tools miss unprintable characters
- Diff tools don't highlight invisible code
- Developer trust in visual code inspection

**Protective Controls:** 🛡️
- IDE plugins to visualize invisible characters
- Static analysis with Unicode normalization
- Extension code signing and verification
- Mandatory code review with specialized tools

**Detective Controls:** 🔍
- Unicode character detection in code review tools
- Automated detection of unprintable characters in commits

---

#### T-E012: SOCKS Proxy Deployment on Endpoint

**Technique:** Attacker deploys SOCKS proxy server on compromised endpoint to route malicious traffic through victim's network and IP address

**Risks:**
- No EDR
- No network egress monitoring
- Unrestricted outbound connections
- Endpoint inside corporate network
- No process monitoring

**Protective Controls:** 🛡️
- Application whitelisting
- Network segmentation (endpoints from production)
- Outbound connection restrictions

**Detective Controls:** 🔍
- EDR on endpoint
- Network egress monitoring and filtering
- Anomalous network behavior detection

---

#### T-E013: Hidden VNC (HVNC) Deployment

**Technique:** Attacker deploys hidden Virtual Network Computing that provides invisible remote desktop access without user awareness

**Risks:**
- No EDR
- No process monitoring
- Lack of application sandboxing
- Privileged user accounts

**Protective Controls:** 🛡️
- Minimal local user privileges

**Detective Controls:** 🔍
- EDR on endpoint
- Process monitoring and whitelisting
- Session activity monitoring
- Behavioral analysis for hidden processes
- Virtual desktop detection

---

#### T-E014: WebRTC P2P Control Channel Establishment

**Technique:** Attacker establishes WebRTC peer-to-peer connections for direct control that bypasses traditional firewalls via NAT traversal

**Risks:**
- WebRTC enabled in browsers/applications
- No network monitoring of WebRTC traffic
- NAT traversal bypasses firewall rules
- No EDR
- P2P connections not logged

**Protective Controls:** 🛡️
- Network behavior analysis
- WebRTC restrictions in corporate browsers
- STUN/TURN server whitelisting

**Detective Controls:** 🔍
- EDR on endpoint
- WebRTC traffic monitoring
- Deep packet inspection

---

#### T-E015: Extension Auto-Update Exploitation

**Technique:** Attacker exploits automatic extension update mechanisms to silently deploy malicious updates to all users without interaction

**Risks:**
- Auto-updates enabled for extensions
- No update verification
- Compromised extension publisher accounts
- No extension version pinning
- Silent updates without user notification

**Protective Controls:** 🛡️
- Extension update approval workflow
- Extension version pinning
- Update signature verification
- Delayed update deployment (canary testing)

**Detective Controls:** 🔍
- Extension update monitoring and alerting
- Extension marketplace security monitoring

---

#### T-E016: Blockchain-Based C2 Infrastructure

**Technique:** Attacker uses blockchain transactions (e.g., Solana, Bitcoin) as immutable command and control infrastructure that cannot be taken down or censored

**Risks:**
- Immutable C2 instructions on blockchain
- No EDR
- Cryptocurrency node connections not restricted

**Protective Controls:** 🛡️
- Network behavior analysis
- Cryptocurrency-related traffic restrictions
- Application whitelisting

**Detective Controls:** 🔍
- EDR on endpoint
- Blockchain RPC connection monitoring
- Anomalous blockchain query detection

---

#### T-E017: Legitimate Service Abuse for C2

**Technique:** Attacker uses legitimate cloud services (Google Calendar, Pastebin, social media, cloud storage) as command and control channels to evade detection

**Risks:**
- Legitimate services not monitored for C2 abuse
- No content inspection of legitimate service traffic
- Services whitelisted in security controls
- No EDR
- Encoded payloads in legitimate service data

**Protective Controls:** 🛡️
- Deep content inspection of legitimate service traffic

**Detective Controls:** 🔍
- EDR on endpoint
- Behavioral analysis for unusual service usage patterns
- Network traffic anomaly detection
- Application-level monitoring
- Data exfiltration detection

---

#### T-E018: BitTorrent DHT for C2

**Technique:** Attacker uses BitTorrent Distributed Hash Table network for decentralized command distribution that cannot be shut down

**Risks:**
- BitTorrent/P2P traffic not monitored
- DHT network connections appear as normal P2P traffic
- No EDR
- Decentralized C2 cannot be taken down
- P2P protocols not restricted

**Protective Controls:** 🛡️
- P2P protocol blocking
- Network behavior analysis
- Application whitelisting

**Detective Controls:** 🔍
- EDR on endpoint
- BitTorrent traffic monitoring and blocking
- DHT network connection detection

---

### VCS (Version Control System)

#### T-V001: Abuse Credentials for VCS Access

**Technique:** Attacker uses stolen credentials to access VCS

**Risks:**
- Lack of 2FA / phishing protection
- Credentials in org public repos
- Credentials in public repos of org members
- Credentials in workflow logs
- Previous breaches
- Fine-grained PATs not enforced
- PATs without expiration

**Protective Controls:** 🛡️
- Mandatory MFA
- IDP / SSO setup
- Enforcing fine-grained PATs
- Enforcing PAT expiration

**Detective Controls:** 🔍
- Secret scanning on org
- Secret scanning on personal repos

---

#### T-V002: Imposter Commits

**Technique:** Attacker commits code impersonating another developer

**Risks:**
- No commit signing required
- Email verification not enforced
- No code review process

**Protective Controls:** 🛡️
- Commit signing
- Requiring code owner approval
- Branch protection rules
- Email verification enforcement

**Detective Controls:** 🔍
- (none)

---

#### T-V003: Secret Exfiltration from Repo

**Technique:** Attacker extracts secrets from repository content or history

**Risks:**
- Misconfigured repo - visibility (public when should be private)
- Misconfigured VCS access - external contributors
- Using untrusted webhooks
- Dangling webhooks
- Secrets committed to repo

**Protective Controls:** 🛡️
- Private repo visibility
- Webhook security review
- Branch protection rules

**Detective Controls:** 🔍
- Secret scanning on org
- Secret scanning on personal repos
- Detection infra on audit logs

---

#### T-V004: Secret Exfiltration from Personal Repo

**Technique:** Attacker finds secrets in personal repos of org members

**Risks:**
- Misconfigured repo - visibility
- Using personal repos for work
- Org members with public repos containing work content

**Protective Controls:** 🛡️
- Policy against using personal repos for work
- Security awareness training

**Detective Controls:** 🔍
- Secret scanning on personal repos
- Detection infra on audit logs

---

#### T-V005: VCS Vulnerability Exploitation

**Technique:** Attacker exploits vulnerability in VCS platform

**Risks:**
- Non-patched VCS instance
- Known CVEs not addressed
- Self-hosted VCS without security updates

**Protective Controls:** 🛡️
- Using managed VCS instances
- Patching schedule

**Detective Controls:** 🔍
- Vulnerability scanning
- Security update monitoring

---

#### T-V006: Turn Private Repos Public

**Technique:** Attacker changes repository visibility to public

**Risks:**
- Overprivileged VCS access
- No approval for visibility changes
- No audit log monitoring

**Protective Controls:** 🛡️
- Minimal VCS permissions
- Approval workflow for visibility changes
- CSPM/CNAPP

**Detective Controls:** 🔍
- Detection infra on audit logs

---

#### T-V007: Clone Sensitive Repositories

**Technique:** Attacker clones private repositories to steal IP and source code

**Risks:**
- Overprivileged VCS access
- No audit log monitoring
- No DLP on network

**Protective Controls:** 🛡️
- Minimal VCS permissions
- Repository access reviews

**Detective Controls:** 🔍
- Detection infra on audit logs
- Network DLP

---

#### T-V008: Malicious Repo Hosting

**Technique:** Attacker uses compromised VCS to host malicious repositories

**Risks:**
- Overprivileged VCS access
- No repository review process
- Unlimited repository creation

**Protective Controls:** 🛡️
- Repository creation approval
- Resource quotas

**Detective Controls:** 🔍
- Repository security scanning
- Detection infra on audit logs

---

#### T-V009: Mass Deletion of Repositories

**Technique:** Attacker deletes multiple repositories to cause data loss and operational disruption

**Risks:**
- Overprivileged VCS access
- No backup and recovery
- No audit log monitoring
- Insufficient access controls on critical repositories
- No repository deletion approval process
- Lack of deletion protection

**Protective Controls:** 🛡️
- Minimal VCS user permissions
- Regular repository backups
- Repository deletion approval workflow
- Repository recovery procedures
- Deletion protection on critical repositories

**Detective Controls:** 🔍
- Detection infra on audit logs (VCS)
- Immutable audit logs

---

#### T-V010: Malicious Code Modification in Repository

**Technique:** Attacker with repository access directly modifies source code to inject backdoors, malicious logic, or vulnerabilities into the codebase

**Risks:**
- Overprivileged VCS access
- No code review requirements
- Direct push to protected branches allowed
- Lack of commit signing
- No automated code security scanning
- Insufficient branch protection rules
- No detection of suspicious code patterns

**Protective Controls:** 🛡️
- Branch protection rules (VCS)
- Require code owner approval
- Mandatory code review by multiple reviewers
- Commit signing enforcement
- Minimal VCS permissions (principle of least privilege)
- Pre-commit hooks for security checks

**Detective Controls:** 🔍
- Automated code security scanning (SAST)
- Detection infra on audit logs (VCS)
- Code change anomaly detection

---

### CI/CD

#### T-C001: Abuse Credentials for CI/CD Access

**Technique:** Attacker uses stolen credentials to access CI/CD system

**Risks:**
- Lack of 2FA / phishing protection
- Default credentials / bad out-of-the-box config
- Credentials in org public repos
- Previous breaches

**Protective Controls:** 🛡️
- Mandatory MFA
- IDP / SSO setup
- Enforcing fine-grained PATs (VCS)
- Enforcing PAT expiration (VCS)

**Detective Controls:** 🔍
- Secret scanning

---

#### T-C002: Malicious Execution in Workflow Context

**Technique:** Attacker executes malicious code within CI/CD workflow

**Risks:**
- Using untrusted GitHub actions
- Using untrusted GitHub Apps
- Using untrusted reusable workflows
- Using untrusted SW packages on runners
- Using untrusted container / VM image for runners
- Lack of GitHub action pinning

**Protective Controls:** 🛡️
- Pinning 3rd-party actions
- Action whitelisting
- Automated maintainer reputation and hygiene checks
- Requiring code owner approval (VCS)
- Branch protection rules (VCS)
- Runner SBOM

**Detective Controls:** 🔍
- Image scanning

---

#### T-C003: PWN Request / Poisoned Pipeline Execution

**Technique:** Attacker submits malicious PR that triggers workflow with elevated privileges

**Risks:**
- Misconfigured repo - visibility
- Misconfigured VCS access - external contributors
- Allowing PRs from forks
- Usage of pull_request_target/workflow_run
- Default workflow permissions set to WRITE
- Default workflow permissions set to approve PR
- Workflows with access to secrets

**Protective Controls:** 🛡️
- Branch protection rules (VCS)
- Private repo (VCS)
- Require explicit approval/ disallow workflows from forks (VCS)
- Minimal workflow permissions
- Default workflow permissions not set to approve PRs

**Detective Controls:** 🔍
- CICD scanning tools

---

#### T-C004: Workflow Script Injection

**Technique:** Attacker injects malicious code into workflow through user-controlled input

**Risks:**
- Misconfigured repo - visibility
- Misconfigured workflow - script injection
- Default workflow permissions set to WRITE
- Default workflow permissions set to approve PR
- Workflow with excessive permissions
- Workflow with access to secrets

**Protective Controls:** 🛡️
- Branch protection rules (VCS)
- Private repo (VCS)
- Minimal workflow permissions
- Code review for workflows

**Detective Controls:** 🔍
- CICD scanning tools

---

#### T-C005: Secret Exfiltration from Workflow

**Technique:** Attacker extracts secrets from CI/CD workflow execution

**Risks:**
- Workflow with access to secrets
- No runtime monitoring
- Secrets in workflow logs
- Overprivileged secrets

**Protective Controls:** 🛡️
- OIDC setup in workflows
- Minimal workflow permissions
- Log sanitization

**Detective Controls:** 🔍
- Runtime agent on runner
- Secret scanning

---

#### T-C006: Secret Enumeration in Workflows Using GitHub Search

**Technique:** Attacker searches public workflows for exposed secrets

**Risks:**
- Workflow with access to secrets
- Public repositories
- Secrets in workflow files

**Protective Controls:** 🛡️
- OIDC setup in workflows
- Private repositories
- Code review for workflows

**Detective Controls:** 🔍
- Secret scanning

---

#### T-C007: Action Cache Poisoning

**Technique:** Attacker poisons shared action cache to inject malicious code

**Risks:**
- Shared actions cache
- No cache isolation
- No cache verification

**Protective Controls:** 🛡️
- Don't use actions cache
- Workflow ordering
- Cache artifact signing / verification
- Cache isolation per repository

**Detective Controls:** 🔍
- (none)

---

#### T-C008: Malicious Workflow Performing Code Modification

**Technique:** Attacker uses workflow to modify code or approve PRs

**Risks:**
- Default workflow permissions set to WRITE
- Default workflow permissions set to approve PR
- Workflow with excessive permissions

**Protective Controls:** 🛡️
- Minimal workflow permissions
- Default workflow permissions not set to approve PRs
- Code review requirements

**Detective Controls:** 🔍
- CICD scanning tools

---

#### T-C009: CI/CD Vulnerability Exploitation

**Technique:** Attacker exploits vulnerability in CI/CD platform

**Risks:**
- Non-patched CI/CD instance
- Known CVEs not addressed
- Self-hosted CI/CD without security updates

**Protective Controls:** 🛡️
- Using managed CI/CD instances
- Patching schedule

**Detective Controls:** 🔍
- Vulnerability scanning
- Security update monitoring

---

#### T-C010: Runner Executing Malicious Package

**Technique:** Malicious package executes on CI/CD runner

**Risks:**
- Using untrusted SW packages on runners
- No package verification
- No runtime monitoring
- Package installation scripts enabled
- Direct downloads from public registries

**Protective Controls:** 🛡️
- Local registry proxy with filtering
- Runner SBOM
- Package version pinning
- Package signature verification
- Disable package installation scripts (--ignore-scripts)

**Detective Controls:** 🔍
- Runtime agent on runner

---

#### T-C011: Stealing Registry Tokens

**Technique:** Attacker extracts registry publishing tokens from workflow

**Risks:**
- Workflow with access to secrets
- Overprivileged registry tokens
- Long-lived credentials

**Protective Controls:** 🛡️
- OIDC setup in workflows
- Trusted publishing (registry)

**Detective Controls:** 🔍
- Runtime agent on runner
- Secret scanning

---

#### T-C012: PR from Malicious Workflow

**Technique:** Workflow creates malicious pull request

**Risks:**
- Default workflow permissions set to WRITE
- Default workflow permissions set to approve PR
- No PR review requirements

**Protective Controls:** 🛡️
- Minimal workflow permissions
- Branch protection rules (VCS)
- Require code owner approval (VCS)

**Detective Controls:** 🔍
- CICD scanning tools

---

#### T-C013: Persistence on Self-Hosted Runners

**Technique:** Attacker establishes persistence on self-hosted runner

**Risks:**
- Misconfigured self-hosted runner
- Non-ephemeral self-hosted runner
- Overshared self-hosted runner
- No runtime monitoring

**Protective Controls:** 🛡️
- Using managed runners only
- Ephemeral runners
- Runner isolation

**Detective Controls:** 🔍
- Runtime agent on runner

---

#### T-C014: Cryptomining on Runners

**Technique:** Attacker uses runner resources for cryptocurrency mining

**Risks:**
- No runtime monitoring
- No resource limits
- Self-hosted runners

**Protective Controls:** 🛡️
- Using managed runners only

**Detective Controls:** 🔍
- Runtime agent on runner
- Resource monitoring and limits
- Network monitoring

---

#### T-C015: Harvest Secrets from Workflows Using ${{toJson(secrets)}}

**Technique:** Attacker uses toJson() to dump all secrets from workflow

**Risks:**
- Workflow with access to secrets
- No CICD scanning
- No runtime monitoring

**Protective Controls:** 🛡️
- OIDC setup in workflows
- Minimal workflow permissions

**Detective Controls:** 🔍
- CICD scanning tools
- Runtime agent on runner

---

#### T-C016: Pivot from Self-Hosted VM Runner into Local Network / Cloud

**Technique:** Attacker uses runner network access to pivot into production

**Risks:**
- Overprivileged runner pod identity
- Misconfigured runner cluster
- Self-hosted runner in production network
- No network segmentation

**Protective Controls:** 🛡️
- Minimal runner pod privileges
- Network segmentation
- Using managed runners only

**Detective Controls:** 🔍
- K8s sensor on runner cluster
- KSPM on runner cluster

---

#### T-C017: Pivot from Self-Hosted Container Runner into K8s Cluster

**Technique:** Attacker escapes container runner to access Kubernetes cluster

**Risks:**
- Overprivileged runner pod identity
- Misconfigured runner cluster
- No pod security policies
- Privileged containers allowed

**Protective Controls:** 🛡️
- Minimal runner pod privileges
- Pod security policies
- Using managed runners only

**Detective Controls:** 🔍
- K8s sensor on runner cluster
- KSPM on runner cluster

---

#### T-C018: Data Exfiltration from CI/CD

**Technique:** Attacker exfiltrates build artifacts, logs, secrets, and sensitive data from CI/CD system over network

**Risks:**
- No network egress monitoring
- Unrestricted outbound network access from runners
- Build artifacts contain sensitive data
- Logs contain secrets or sensitive information
- No DLP on CI/CD network

**Protective Controls:** 🛡️
- Log sanitization
- Artifact encryption
- Network segmentation (CI/CD from internet)

**Detective Controls:** 🔍
- Network DLP
- Egress traffic monitoring and filtering
- Runtime agent on runner
- Large data transfer detection
- Detection infra on audit logs (CI/CD)

---

#### T-C019: CI/CD Infrastructure Destruction

**Technique:** Attacker destroys CI/CD pipelines, workflows, runners, or build artifacts to disrupt development and deployment operations

**Risks:**
- Overprivileged workflow permissions
- No backup and recovery
- Lack of workflow protection
- No audit log monitoring
- Insufficient access controls on critical workflows
- No approval process for infrastructure changes

**Protective Controls:** 🛡️
- Minimal workflow permissions
- Regular CI/CD configuration backups
- Workflow protection rules
- Infrastructure change approval workflow
- CI/CD recovery procedures
- Using managed runners only

**Detective Controls:** 🔍
- Detection infra on audit logs (CI/CD)
- Immutable audit logs

---

#### T-C020: CI/CD Misconfiguration Exploitation

**Technique:** Attacker exploits misconfiguration in CI/CD platform

**Risks:**
- Misconfigured CI/CD instances

**Protective Controls:** 🛡️
- CSPM/CNAPP

**Detective Controls:** 🔍
- (none)

---

#### T-C021: AI Agent Prompt Injection in Workflow

**Technique:** Attacker crafts malicious input (issue titles, PR descriptions, comments) that manipulates an AI coding agent running in CI/CD to execute arbitrary commands or exfiltrate data

**Risks:**
- AI agents with Bash/shell execution capabilities in workflows
- AI agents with Write/Edit file permissions
- User-controlled input passed to AI prompts without sanitization
- Overly permissive AI tool configurations (allowedTools includes Bash)
- AI workflows triggered by any GitHub user (no write-access requirement)
- No input validation or content filtering for AI context
- AI agents with access to workflow secrets
- No human approval gates for AI-suggested actions

**Protective Controls:** 🛡️
- Restrict AI agent tool permissions
- Input sanitization before AI context injection
- Require write access to trigger AI-powered workflows
- Sandboxed AI execution environment
- Human approval gates for AI-suggested actions
- Separate AI workflows from release/publish workflows
- Rate limiting for AI workflow triggers

**Detective Controls:** 🔍
- AI prompt injection detection
- Audit logging of AI agent actions
- Anomaly detection for AI workflow behavior
- Runtime agent on runner (1 detection rules)

---

### REGISTRY (Container / Artifact Registry)

#### T-R001: Abuse Credentials for Registry Access

**Technique:** Attacker uses stolen credentials to access registry

**Risks:**
- Lack of 2FA / phishing protection
- Default credentials / bad out-of-the-box config
- Credentials in public images
- Credentials in workflow logs
- Previous breaches

**Protective Controls:** 🛡️
- Mandatory MFA
- IDP / SSO setup
- CSPM/CNAPP

**Detective Controls:** 🔍
- Secret scanning

---

#### T-R002: Misconfigured / Anonymous Access

**Technique:** Attacker exploits misconfigured registry permissions

**Risks:**
- Misconfigured registry access
- Anonymous access enabled
- Overly permissive access controls

**Protective Controls:** 🛡️
- IDP / SSO setup
- Access control reviews
- Principle of least privilege
- CSPM/CNAPP

**Detective Controls:** 🔍
- (none)

---

#### T-R003: Registry Vulnerability Exploitation

**Technique:** Attacker exploits vulnerability in registry platform

**Risks:**
- Non-patched artifact/container registry
- Known CVEs not addressed
- Self-hosted registry without security updates

**Protective Controls:** 🛡️
- Using managed registry instances
- Patching schedule

**Detective Controls:** 🔍
- Vulnerability scanning
- Security update monitoring

---

#### T-R004: Publishing Malicious Package

**Technique:** Attacker publishes malicious package to registry

**Risks:**
- Overprivileged NPM token
- Lack of provenance
- Lack of trusted publishing
- No package signing

**Protective Controls:** 🛡️
- Trusted publishing
- Provenance attestation
- MFA for registry account
- Package signing and verification
- OIDC for publishing

**Detective Controls:** 🔍
- (none)

---

#### T-R005: Publishing Malicious Container/VM Image

**Technique:** Attacker publishes malicious container or VM image

**Risks:**
- Overprivileged registry credentials
- No image signing
- No provenance attestation
- No image scanning

**Protective Controls:** 🛡️
- Trusted publishing
- Provenance attestation
- Image signing and verification
- OIDC for publishing

**Detective Controls:** 🔍
- Image vulnerability scanning

---

#### T-R006: Publishing Malicious IDE/Browser Extension

**Technique:** Attacker publishes malicious extension to extension marketplace

**Risks:**
- Overprivileged publishing credentials
- No extension review process
- No signing requirements

**Protective Controls:** 🛡️
- Extension signing requirements
- Extension review process
- MFA for publisher account
- Trusted publishing

**Detective Controls:** 🔍
- (none)

---

#### T-R007: Harvest Data from Private Artifacts

**Technique:** Attacker extracts sensitive data from private artifacts

**Risks:**
- Overprivileged registry access
- Secrets in artifacts
- No audit log monitoring

**Protective Controls:** 🛡️
- Minimal registry permissions
- Artifact encryption

**Detective Controls:** 🔍
- Secret scanning
- Detection infra on audit logs

---

#### T-R008: Malicious Images Hosting

**Technique:** Attacker uses compromised registry to host malicious images

**Risks:**
- Overprivileged registry access
- No image scanning
- No resource quotas

**Protective Controls:** 🛡️
- Resource quotas
- Access control reviews

**Detective Controls:** 🔍
- Image vulnerability scanning
- Detection infra on audit logs

---

#### T-R009: Registry Infrastructure Destruction

**Technique:** Attacker deletes packages, images, or corrupts registry infrastructure to disrupt software distribution and deployment

**Risks:**
- Overprivileged registry access
- No backup and recovery
- Lack of deletion protection
- No audit log monitoring
- Insufficient access controls on critical artifacts
- No artifact deletion approval process

**Protective Controls:** 🛡️
- Minimal user permissions (registry)
- Regular artifact backups
- Artifact deletion protection
- Artifact deletion approval workflow
- Immutable artifact storage
- Registry recovery procedures
- Artifact retention policies

**Detective Controls:** 🔍
- Detection infra on audit logs (registry)

---

#### T-R010: Typosquatting

**Technique:** Attacker publishes malicious packages with names similar to legitimate ones to trick developers into installing them by mistake

**Risks:**
- No package name verification
- Lack of typosquatting detection
- Developer mistakes during package installation
- No package naming policies
- Lack of security awareness training
- Direct downloads from public registries

**Protective Controls:** 🛡️
- Local registry proxy with filtering
- Package name similarity checks
- Automated maintainer reputation and hygiene checks
- Security awareness training on package verification
- Package installation verification workflows
- Dependency review and approval process
- Package popularity and reputation scoring

**Detective Controls:** 🔍
- Typosquatting detection and prevention

---

#### T-R011: Namespace/Dependency Confusion

**Technique:** Attacker publishes malicious packages with same names as private packages but higher version numbers, tricking package managers into fetching the public version instead of the private package

**Risks:**
- Lack of internal repository enforcement
- Package managers prioritize public repositories
- No namespace isolation between internal and public packages
- Automatic dependency resolution without verification
- Higher version numbers in public repositories
- Direct downloads from public registries

**Protective Controls:** 🛡️
- Local registry proxy with filtering
- Internal repository enforcement and prioritization
- Namespace isolation and scoping
- Package version pinning
- Automated maintainer reputation and hygiene checks
- Private package registry configuration
- Dependency resolution policies
- Package source verification

**Detective Controls:** 🔍
- (none)

---

### PRODUCTION / CLOUD

#### T-P001: Abuse Production Credentials from CI/CD

**Technique:** Attacker extracts production credentials from CI/CD and uses them to access production

**Risks:**
- Production credentials in CI/CD workflows
- Long-lived production credentials
- Overprivileged cloud service accounts
- No credential rotation

**Protective Controls:** 🛡️
- OIDC for deployment (no long-lived credentials)
- Minimal IAM permissions
- Credential rotation
- Network segmentation from SDLC

**Detective Controls:** 🔍
- Secret scanning

---

#### T-P002: Malicious Deployment via Compromised Pipeline

**Technique:** Attacker modifies CI/CD pipeline to deploy malicious code to production

**Risks:**
- No deployment approval gates
- Overprivileged deployment credentials
- No code signing verification
- Insufficient workflow permissions review

**Protective Controls:** 🛡️
- Deployment approval gates
- Code signing and verification
- Minimal workflow permissions
- Branch protection rules (VCS)

**Detective Controls:** 🔍
- Deployment monitoring

---

#### T-P003: Pivot from Self-Hosted Runner to Production Network

**Technique:** Attacker uses self-hosted runner network access to pivot into production

**Risks:**
- Self-hosted runner in production network
- Weak network segmentation
- Overprivileged runner identity
- No network monitoring

**Protective Controls:** 🛡️
- Network segmentation from SDLC
- Using managed runners only
- Runner isolation
- Minimal runner privileges

**Detective Controls:** 🔍
- Network monitoring

---

#### T-P004: Container Image Poisoning to Production

**Technique:** Attacker publishes malicious container image that gets deployed to production

**Risks:**
- Lack of image signing/verification
- No provenance attestation
- Automatic deployment without review
- No image scanning

**Protective Controls:** 🛡️
- Image signing and verification
- Provenance attestation
- Deployment approval gates

**Detective Controls:** 🔍
- Image vulnerability scanning
- Runtime security monitoring

---

#### T-P005: Infrastructure-as-Code Manipulation

**Technique:** Attacker modifies IaC to create backdoors in production infrastructure

**Risks:**
- Insufficient IaC review process
- Lack of drift detection
- Overprivileged deployment credentials

**Protective Controls:** 🛡️
- Code review for IaC changes
- Deployment approval gates
- Minimal deployment permissions
- CSPM/CNAPP

**Detective Controls:** 🔍
- Drift detection

---

#### T-P006: Kubernetes Service Account Token Theft

**Technique:** Attacker extracts Kubernetes service account tokens from CI/CD

**Risks:**
- Overprivileged service accounts
- Long-lived tokens
- Lack of token rotation
- Tokens in CI/CD secrets

**Protective Controls:** 🛡️
- OIDC for K8s access
- Minimal service account permissions
- Token rotation

**Detective Controls:** 🔍
- Secret scanning
- Runtime security monitoring

---

#### T-P007: Cloud Metadata Service Exploitation

**Technique:** Attacker accesses cloud metadata service to steal additional credentials

**Risks:**
- Metadata service not restricted
- Overprivileged IAM roles
- No network segmentation
- Compromised workload with metadata access

**Protective Controls:** 🛡️
- Metadata service restrictions
- Minimal IAM permissions
- Network segmentation
- IMDSv2 enforcement (AWS)

**Detective Controls:** 🔍
- Runtime security monitoring

---

#### T-P008: Kubernetes Pod Escape

**Technique:** Attacker escapes from container to underlying node

**Risks:**
- Privileged containers allowed
- No pod security policies
- Overprivileged pod identity
- Host filesystem mounted

**Protective Controls:** 🛡️
- Pod security policies
- Minimal pod privileges

**Detective Controls:** 🔍
- K8s sensor on cluster
- KSPM
- Runtime security monitoring

---

#### T-P009: Cloud Service Lateral Movement

**Technique:** Attacker uses compromised cloud credentials to access other cloud services

**Risks:**
- Overprivileged IAM roles
- No network segmentation
- Lack of service-to-service authentication
- No audit log monitoring

**Protective Controls:** 🛡️
- Minimal IAM permissions
- Network segmentation
- Service mesh / zero trust
- CSPM/CNAPP

**Detective Controls:** 🔍
- Detection infra on audit logs

---

#### T-P010: Network Lateral Movement Within Production

**Technique:** Attacker moves between production systems via network

**Risks:**
- Weak network segmentation
- Overly permissive security groups
- No network monitoring
- Unpatched systems

**Protective Controls:** 🛡️
- Network segmentation
- Micro-segmentation
- Security group hardening
- Vulnerability management

**Detective Controls:** 🔍
- Network monitoring

---

#### T-P011: Steal Secrets from Production Environment

**Technique:** Attacker accesses production secrets store and exfiltrates customer secrets, tokens, and credentials

**Risks:**
- Encryption keys accessible in process memory
- Lack of hardware security module (HSM) for key storage
- No secrets rotation policies
- Centralized storage of all customer secrets
- No data loss prevention (DLP) on production systems
- Lack of egress traffic monitoring

**Protective Controls:** 🛡️
- Store encryption keys in HSM (Hardware Security Module)
- Envelope encryption with key hierarchy
- Customer-managed encryption keys (CMEK)
- Automatic secrets rotation (30-90 days)
- Secrets segmentation (per-customer isolation)
- Memory protection and anti-dumping controls

**Detective Controls:** 🔍
- DLP on production systems
- Egress traffic monitoring and filtering
- Detection infra on audit logs (production)
- Large data transfer detection

---

#### T-P012: Production Infrastructure Reconnaissance

**Technique:** Attacker enumerates production infrastructure, services, and resources to identify targets and plan attacks

**Risks:**
- Overprivileged IAM roles allowing enumeration
- No detection of reconnaissance activities
- Publicly exposed cloud metadata
- Insufficient network segmentation allowing scanning
- Verbose error messages revealing infrastructure details
- Lack of honeypots or deception technology
- No rate limiting on API calls

**Protective Controls:** 🛡️
- Minimal IAM permissions
- API rate limiting and throttling
- Network segmentation (production internal)
- Metadata service restrictions
- Generic error messages (no infrastructure details)

**Detective Controls:** 🔍
- Detection infra on audit logs (production)
- Honeypots and deception technology
- Anomaly detection for enumeration patterns

---

#### T-P013: Data Exfiltration from Production

**Technique:** Attacker exfiltrates customer data, application data, databases, and sensitive information from production environment over network

**Risks:**
- No network egress monitoring
- Unrestricted outbound network access
- No DLP on production systems
- Backup data accessible and unmonitored
- Use of encrypted channels to bypass DLP
- Cloud storage buckets with public access

**Protective Controls:** 🛡️
- Backup encryption and access controls
- SSL/TLS inspection
- Data classification and handling policies
- Network segmentation (production from internet)
- CSPM/CNAPP

**Detective Controls:** 🔍
- Network DLP
- Egress traffic monitoring and filtering
- Large data transfer detection
- Database activity monitoring
- Detection infra on audit logs (production)

---

#### T-P014: Production Infrastructure Destruction

**Technique:** Attacker destroys production infrastructure, databases, storage, or configurations to cause severe operational disruption and data loss

**Risks:**
- Overprivileged IAM roles allowing destructive actions
- No backup and disaster recovery plan
- Lack of deletion protection on critical resources
- No audit log monitoring
- Insufficient access controls on critical infrastructure
- No approval process for destructive operations
- Backup data not isolated from production

**Protective Controls:** 🛡️
- Minimal IAM permissions
- Regular backups with offsite/offline storage
- Deletion protection on critical resources
- Destructive operation approval workflow
- Immutable backups
- Disaster recovery procedures and testing
- Resource tagging and protection policies
- Backup isolation from production network
- CSPM/CNAPP

**Detective Controls:** 🔍
- Detection infra on audit logs (production)

---

#### T-P015: Malicious Service Provisioning for Persistence

**Technique:** Attacker provisions new malicious services or backdoors existing services in orchestration platform (e.g., ArgoCD, Kubernetes) to establish persistence

**Risks:**
- No approval gates for service provisioning
- Developers can create arbitrary services
- Service definitions not audited
- No anomaly detection for new service creation
- Persistent backdoor services remain undetected

**Protective Controls:** 🛡️
- Deployment approval gates for new services
- Code review for all IaC changes
- Baseline approved services list
- CSPM/CNAPP

**Detective Controls:** 🔍
- Detection infra on audit logs (production)
- Anomaly detection for new service creation patterns
- Immutable audit logs
- Regular service inventory audits

---

#### T-P016: Supply Chain Backdoor (Sensor/Agent Poisoning)

**Technique:** Attacker injects backdoor into security sensors, agents, or client-distributed software, causing downstream supply chain compromise affecting all customers

**Risks:**
- No binary signing verification for distributed software
- Customer updates automatically deployed without verification
- No provenance attestation for sensor binaries
- No multi-party approval for releases

**Protective Controls:** 🛡️
- Code signing and verification for all distributed binaries
- Provenance attestation (SLSA Level 3+)
- Customer-controlled update policies with verification
- Separation of duties for release signing
- Immutable build logs and attestations

**Detective Controls:** 🔍
- Multi-party approval for sensor/agent releases
- Regular security audits of build infrastructure

---

## Quick Reference: Technique Index by Attack Stage

### Initial Access Techniques
- T-C001: Abuse Credentials for CI/CD Access
- T-C002: Malicious Execution in Workflow Context
- T-C003: PWN Request / Poisoned Pipeline Execution
- T-C004: Workflow Script Injection
- T-C009: CI/CD Vulnerability Exploitation
- T-C020: CI/CD Misconfiguration Exploitation
- T-C021: AI Agent Prompt Injection in Workflow
- T-E001: Malicious Execution on Endpoint
- T-E002: Endpoint Phishing
- T-E011: Unicode Stealth Code Injection
- T-E015: Extension Auto-Update Exploitation
- T-P001: Abuse Production Credentials from CI/CD
- T-R001: Abuse Credentials for Registry Access
- T-R002: Misconfigured / Anonymous Access
- T-R003: Registry Vulnerability Exploitation
- T-R010: Typosquatting
- T-R011: Namespace/Dependency Confusion
- T-V001: Abuse Credentials for VCS Access
- T-V005: VCS Vulnerability Exploitation

### Post-Compromise Techniques
- T-C007: Action Cache Poisoning
- T-C008: Malicious Workflow Performing Code Modification
- T-C013: Persistence on Self-Hosted Runners
- T-C014: Cryptomining on Runners
- T-C018: Data Exfiltration from CI/CD
- T-C019: CI/CD Infrastructure Destruction
- T-E004: Harvest Local Data from Endpoint
- T-E005: Cryptomining on Endpoints
- T-E010: Endpoint Infrastructure Destruction
- T-E012: SOCKS Proxy Deployment on Endpoint
- T-E013: Hidden VNC (HVNC) Deployment
- T-E014: WebRTC P2P Control Channel Establishment
- T-E016: Blockchain-Based C2 Infrastructure
- T-E017: Legitimate Service Abuse for C2
- T-E018: BitTorrent DHT for C2
- T-P011: Steal Secrets from Production Environment
- T-P013: Data Exfiltration from Production
- T-P014: Production Infrastructure Destruction
- T-P015: Malicious Service Provisioning for Persistence
- T-R007: Harvest Data from Private Artifacts
- T-R008: Malicious Images Hosting
- T-R009: Registry Infrastructure Destruction
- T-V002: Imposter Commits
- T-V006: Turn Private Repos Public
- T-V007: Clone Sensitive Repositories
- T-V008: Malicious Repo Hosting
- T-V009: Mass Deletion of Repositories
- T-V010: Malicious Code Modification in Repository

---

## How to Use This Library for Attack Analysis

### Example: Analyzing the Shai-Hulud-2 Attack

**Step 1: Identify the techniques used**
- T-C003: PWN Request / Poisoned Pipeline Execution
- T-C005: Secret Exfiltration from Workflow
- T-R004: Publishing Malicious Package
- T-E001: Malicious Execution on Endpoint
- T-E003: Harvest Local Secrets / Credentials from Endpoint
- T-E006: Register Local Machine as CI Runner

**Step 2: Look up each technique in the library**

Each technique entry shows you:
- The risks that enabled it
- The controls that would have prevented it

**Step 3: Create your defense plan**

Map all the controls from the techniques used:
- Branch protection rules (VCS)
- Require explicit approval for workflows from forks (VCS)
- OIDC setup in workflows
- Runtime agent on runner
- Trusted publishing
- EDR on endpoint
- Local DLP
- Using managed runners only

**Step 4: Prioritize based on attack path**

Focus on controls that break the most critical pivot points:
1. OIDC (prevents secret theft from CI/CD)
2. Trusted publishing (prevents registry compromise)
3. EDR (detects endpoint compromise)
4. Network segmentation (prevents production pivot)