# Question Bank

Proven question patterns for GenAI platform evaluations, organized by domain. These are drawn from real enterprise evaluations and are designed to surface specific, actionable information rather than general capability confirmations.

Use these as templates. Adapt the specifics (system names, tenant structures, use cases) to the organization being evaluated for.

---

## Platform Identity and Sandbox

- Does the sandbox environment connect to live production data (read-only), or does it require a separate copy?
- What isolation guarantees exist in the sandbox? Can a prototyped agent write back to production accidentally?
- How does sandboxing work with sensitive data (PHI, PII)? Are there masking or tokenization options?

## Development Experience

- For the pro-code path, what does the developer experience look like: CLI, SDK, or API?
- Can developers build agents in existing tools (Cursor, Claude Code, VS Code) and deploy/govern them through the platform?
- How does the platform handle version control and code review for pro-code agents? Git integration?

## Integration Depth

**Per data platform component, confirm or investigate:**
- Is there a native connector, or would we route through a generic integration?
- What authentication methods does the connector support (key-pair, OAuth, service account JSON, Workload Identity)?
- Can the connector target specific schemas, databases, or sub-accounts per tenant?

**For transformation and movement layers:**
- Can agents invoke transformation runs (e.g., dbt jobs) or read from transformation metadata to understand data lineage?
- Can agents check ETL sync status or trigger syncs? This matters for data freshness guarantees.
- Can agents subscribe to event streaming topics for real-time processing, or is the platform strictly request-response?

**For custom integrations:**
- Can we point the platform's gateway at our own integration endpoints, or must all integrations be registered through the vendor's catalog?
- If we register a custom integration, does it receive the full governance layer (audit, policy enforcement, sandboxed execution)?

## Governance and Identity

- Can a single agent use named-user credentials for interactive requests and switch to a service account for batch operations on the same service?
- How are credentials managed and rotated? Does the platform store them, or delegate to our identity provider?
- Can every action in the audit trail be traced back to the specific user credential that authorized it?

## Multi-Tenancy and Data Isolation

- Is multi-tenancy at the agent level or only at the platform level? Can one agent definition serve N tenants with per-tenant data isolation?
- Can the policy engine enforce row-level or schema-level data isolation at the individual location level, the parent organization level, and across internal business lines at runtime?
- How does the platform model a multi-tier access pattern: tenant users see only their own data, group admins see data across their tenants but not other groups, internal business lines are walled off, and corporate admins can aggregate across all tiers?
- Does the platform support passing a tenant context (user identity, org ID) into agent execution that downstream tools can use for scoping?
- Are governance rules auditable? Can we prove to a downstream customer that their data was never exposed to another tenant?
- How does platform-level isolation interact with the data platform's own role-based access control?
- How are data connections scoped per tenant? Separate schemas, separate sub-accounts, or does the platform handle tenant routing natively?
- What does the deployment model look like at 1,000+ tenants? One platform instance with tenant partitioning, or separate environments?

## Portability and Exit Strategy

- What format are agent definitions stored in? Exportable as code (YAML, JSON, Python) or proprietary?
- Can we export governance policies and audit logs to our own systems (data warehouse, SIEM) for independent analysis?
- What does an exit look like? If we need to migrate off the platform in 18 months, what are we left with?
- How granular are the audit trails? Do they capture full prompt/response pairs, tool call parameters, and the specific policy rules that were evaluated?
- Is the policy engine a black box, or can we inspect and version-control the policy rules ourselves?

## Knowledge Management

- Where does agent knowledge physically live? The platform's internal store, or can it point to an external repository?
- Can we maintain knowledge as files in a Git repository and have agents read from and write to that repo?
- If we leave the platform, can we export all agent knowledge in a portable format?
- Is there version control or change tracking on knowledge updates made by agents?

## Pricing and Commercial Model

- Does the platform offer an OEM or embedded/white-label pricing model for B2B SaaS vendors reselling agent capabilities?
- How are "agent executions" (or the billing unit) defined and metered? Is a single message one execution, or is an entire conversation one execution?
- At 1,000+ tenants each generating 50-500 executions per month, what does the cost model look like? Volume pricing?
- Are LLM inference costs passed through separately, or bundled into the platform fee?

## Compliance and Data Protection

- Will the vendor sign a BAA (Business Associate Agreement) if needed?
- Is any customer data used to train or fine-tune models, even in aggregate?
- Where does data reside geographically? Can we restrict data residency to specific regions?
- What SOC 2 or ISO 27001 certifications does the vendor hold?
- Does the platform store or log prompt/response data? For how long, and who has access?

## API and Embedding

- Can we provision new tenants, bind data sources, and deploy agents entirely through the API, with no manual UI steps?
- Is the SDK designed for end-user embedding (white-label), or primarily for internal developer use?
- Can we fully brand the agent experience so downstream customers never see the vendor's name or UI?
- What rate limits apply? At thousands of concurrent tenants, are there throughput caps?

## Accuracy and Hallucination Controls

- What guardrails exist to detect and prevent hallucinated responses? Confidence scoring, citation/source attribution, or human-in-the-loop approval?
- For text-to-SQL agents, does the platform validate generated queries against the schema before execution? Can it surface the SQL to the user for verification?
- Can we configure "fallback to human" routing when confidence is below a threshold?

## Rollback and Change Management

- Does the platform support versioned agent deployments with instant rollback to a previous version?
- Can we do canary or staged rollouts: deploy a change to a subset of tenants before going broad?
- Is there an approval workflow for promoting agent changes from staging to production?

## Latency and Performance

- What is the typical end-to-end latency for an agent execution involving an LLM call and one tool invocation?
- How does latency scale with concurrent users? At 500 simultaneous requests, what queuing or throttling behavior should we expect?
- Does the platform support streaming responses (partial answers appearing as they are generated)?

## Company Viability

- What is the vendor's current funding status and runway? Series A, B, later?
- How many enterprise customers are currently in production (not pilot or POC)?
- What is the largest deployment by number of end users or agent executions per month?
- Is there a source code escrow arrangement or business continuity provision in the enterprise contract?

## Build vs. Buy

- For our use case, what would we lose if we built the orchestration layer ourselves on open standards (MCP, LangGraph, A2A) vs. using this platform? Be specific.
- Can the vendor point to a customer with a similar deployment model who is running in production?
- What is the realistic time-to-production for a representative use case: on this platform vs. self-built?

## Use Case Walkthrough

For at least one representative use case, ask the vendor to walk through the full lifecycle:

- Building the agent (what tools, what steps)
- Connecting to the data source (auth, scoping, governance)
- Deploying to the interaction surface (Slack, web, mobile, API)
- Handling a real request end-to-end (user input, policy check, LLM call, tool call, response)
- Guardrails: what prevents the agent from returning sensitive data in an inappropriate context?
- State management: can the agent maintain conversation context across a thread?

This walkthrough often reveals more about the platform's maturity than any feature checklist.
