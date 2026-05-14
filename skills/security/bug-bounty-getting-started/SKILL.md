# SKILL.md

```markdown
---
name: bug-bounty-getting-started
description: A step-by-step guide to breaking into bug bounty hunting by building the right knowledge, mindset, and program selection strategy.
category: security
---

# Getting Started in Bug Bounty Hunting

## Step 1: Assess Your Current Background
- Identify where you're coming from: app sec, pen testing, IT support, networking, or general hacking
- Recognize transferable skills (e.g., threat hunting, CTF experience, malware analysis)
- Understand that your path into bug bounty will differ based on your existing expertise

## Step 2: Build Deep Vulnerability Knowledge
- Study common vulnerability classes in depth (XSS, SQLi, IDOR, SSRF, etc.)
- Go beyond surface-level scanner output — understand *why* and *how* vulnerabilities work
- Learn to manually identify and confirm bugs that automated tools miss
- Study frameworks, security libraries, and how developers (mis)use them

## Step 3: Develop the Hacker Mindset
- Cultivate curiosity: always ask "is this app supposed to do this, or can I make it do something else?"
- Practice creative, problem-solving thinking when interacting with targets
- Approach applications as an adversary, not just a user

## Step 4: Find and Sustain Your Passion
- Reflect honestly on whether you enjoy the process, not just the payout
- Recognize that large bounties ($5k–$30k+) are possible but rarely immediate
- Avoid burnout by focusing on programs and vulnerability types you genuinely enjoy
- Track your progress and celebrate small wins to maintain motivation

## Step 5: Choose Your Target Surface
Select a specialization that matches your skills and interests:
- **Web applications** — most accessible starting point
- **Mobile apps** — iOS and Android security testing
- **IoT / Connected devices** — cameras, vehicles, embedded systems
- **AI/ML systems** — prompt injection, model abuse, data exposure
- **Blockchain / Web3** — smart contract vulnerabilities
- **Open source projects** — code review and dependency analysis

## Step 6: Select a Bug Bounty Program
- Start on platforms such as HackerOne, Bugcrowd, Intigriti, or YesWeHack
- Begin with programs that have a wide scope and clear rules of engagement
- Read the program policy carefully — understand what is in scope and out of scope
- Prefer programs with responsive triage teams when starting out

## Step 7: Start Hunting
- Perform manual reconnaissance on your target before scanning
- Use tools (Burp Suite, ffuf, nuclei, etc.) to assist — not replace — manual testing
- Document every step of your testing process
- When you find something, reproduce it reliably before reporting

## Step 8: Write a Strong Report
- Clearly describe the vulnerability type and affected endpoint
- Provide a concise proof-of-concept (PoC) with steps to reproduce
- Explain the business impact in plain language
- Attach screenshots, videos, or request/response captures as evidence

## Step 9: Iterate and Improve
- Review triage feedback, even on duplicates or informatives
- Study public bug bounty disclosures (write-ups) on platforms like HackerOne Hacktivity
- Revisit targets after new features ship — new code introduces new bugs
- Engage with the bug bounty community for tips, collaboration, and motivation