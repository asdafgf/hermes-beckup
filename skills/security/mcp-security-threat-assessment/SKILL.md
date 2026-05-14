# SKILL.md

```markdown
---
name: mcp-security-threat-assessment
description: Assess and identify security threats and risks associated with Model Context Protocol (MCP) server integrations in AI-assisted environments.
category: security
---

# MCP Security Threat Assessment

## Overview
Model Context Protocol (MCP) servers extend AI assistants with external tool access, creating significant attack surface. This skill guides you through systematically evaluating MCP security risks before and during deployment.

## Steps

### 1. Understand the MCP Attack Surface
- Recognize that MCP servers act as a bridge between an LLM (e.g., Claude, Cursor) and external systems (filesystems, APIs, databases, Kubernetes, etc.)
- Map every tool and resource exposed by each MCP server in use
- Identify what permissions and credentials the MCP server holds or can invoke
- Ask: "What is the worst possible action this server could take if fully compromised or manipulated?"

### 2. Inventory All Connected MCP Servers
- List every MCP server configured in your AI client (Claude Desktop, Cursor, etc.)
- Check configuration files (e.g., `claude_desktop_config.json`, `.cursor/mcp.json`) for registered servers
- Flag any server with access to:
  - Production infrastructure (Kubernetes, cloud APIs)
  - Sensitive credentials or secret stores
  - Code repositories with write access
  - Email, calendar, or communication tools
  - Databases with write/delete permissions

### 3. Evaluate Prompt Injection Risk
- Understand that MCP tools return data that the LLM reads directly — malicious content in that data can hijack the agent's behavior
- Test for prompt injection by reviewing what external data sources feed into tool responses (web pages, files, API responses, emails)
- Treat any externally sourced text as untrusted input that could contain adversarial instructions
- Example threat: a malicious webpage fetched by a browser MCP tool containing hidden instructions to exfiltrate files

### 4. Assess Tool Permission Scope (Principle of Least Privilege)
- Review each tool's declared actions and compare against what is actually needed
- Downscope credentials: use read-only API keys where writes are not required
- Avoid granting MCP servers access to production systems when dev/staging suffices
- Never connect an AI agent directly to production infrastructure (e.g., Kubernetes clusters) with write/exec privileges for automated hotfixes

### 5. Review MCP Server Source and Supply Chain
- Prefer MCP servers from verified, audited sources over arbitrary third-party npm/PyPI packages
- Read the source code of any MCP server before installing — they are typically small and auditable
- Check for suspicious behaviors: outbound network calls, credential harvesting, excessive filesystem access
- Pin dependency versions to avoid dependency confusion or hijacking attacks

### 6. Audit Agent Actions in Real Time
- Enable logging for all MCP tool calls, including inputs and outputs
- Route AI agent actions through a human-in-the-loop approval step for any destructive or irreversible operations (file deletion, API writes, deployments)
- Use AI-assisted audit log analysis to detect anomalous tool call patterns at scale

### 7. Define and Enforce Blast Radius Boundaries
- Segment MCP server access so a single compromised or manipulated server cannot affect unrelated systems
- Use separate API keys per MCP server with scoped permissions
- Apply network-level restrictions so MCP server processes cannot reach unexpected internal endpoints

### 8. Test Your MCP Setup Adversarially
- Simulate a prompt injection attack: craft a malicious document or web page and have your agent process it; observe whether it executes unintended tool calls
- Attempt to escalate privileges through chained tool calls (e.g., read a secret via one tool, use it in another)
- Verify that destructive tool calls (delete, deploy, send) require explicit user confirmation

### 9. Document Risk Acceptance
- For any MCP integration that cannot be fully hardened, formally document the accepted risk
- Include: what the server accesses, what the worst-case scenario is, and what compensating controls are in place
- Review and update this documentation when adding new MCP servers or expanding permissions

### 10. Stay Current on MCP Vulnerability Research
- Follow security researchers publishing MCP-specific threat findings (e.g., tool poisoning, rug-pull attacks, cross-server escalation)
- Subscribe to advisories from the MCP specification maintainers (Anthropic) and community security channels
- Re-evaluate your MCP security posture whenever the protocol specification or your AI client updates