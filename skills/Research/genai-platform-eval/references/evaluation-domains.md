# Evaluation Domains

This reference contains the full taxonomy of evaluation domains for GenAI platform assessments. Each domain includes what to research, what good looks like, and which deployment models make the domain critical.

Domains are grouped into three tiers based on how universally they apply:

- **Tier 1 (Always Evaluate)** — These apply regardless of deployment model.
- **Tier 2 (Deployment-Dependent)** — Importance varies significantly by deployment model. The notes under each domain indicate when it becomes primary.
- **Tier 3 (Augmented Concerns)** — Often missed in initial evaluations but can surface deal-shaping information. Always include these, even if the original question set did not.

---

## Tier 1: Always Evaluate

### 1. Platform Identity and Market Position

Understand what the platform actually is and is not. AI platforms occupy different categories — orchestration, inference, development tools, governance — and conflating them leads to mismatched expectations.

**What to research:**
- What category does the vendor claim? Orchestration, gateway, development platform, governance layer?
- What analyst coverage exists (Gartner, Forrester, independent)?
- What is the founding date, funding history, and headcount trajectory?
- AWS/Azure/GCP marketplace availability and deployment models (multi-tenant SaaS, dedicated, on-premise)

**What good looks like:** Clear category positioning with evidence of production deployments, not just pilots. Marketplace availability signals enterprise readiness. Analyst coverage is a positive signal but not a substitute for customer references.

### 2. Development Experience

How do teams build on this platform? The answer determines whether adoption is realistic for the organization's engineering culture.

**What to research:**
- No-code, low-code, and pro-code paths — what does each look like?
- Developer tooling: CLI, SDK, API surface, language support
- Can teams build in existing tools (IDEs, AI coding assistants) and deploy/govern through the platform?
- Version control integration: Git, CI/CD pipeline support
- Prototyping and sandbox capabilities: can prototypes run against production-representative data in isolation?

**What good looks like:** Multiple development tiers that match the organization's team composition. Pro-code path should feel native to developers, not like a workaround. Sandbox environments should provide real isolation guarantees, not just marketing language about "mirroring production."

### 3. Integration and Connector Ecosystem

What systems can the platform connect to, and how deep do those connections go?

**What to research:**
- Total connector count and growth trajectory
- Specific connectors for the organization's data stack (name each component and confirm or note absence)
- Authentication methods supported per connector (OAuth, key-pair, service account, Workload Identity)
- Custom connector framework: can the organization bring its own integrations?
- For gateway-style platforms: does routing through the gateway add governance (audit, policy, sandboxing) to custom connectors?

**What good looks like:** Confirmed connectors for the organization's primary data platform. A framework for custom connectors that still receive the full governance layer. Clear documentation on auth methods per connector. Absence of a connector for a critical system is a yellow flag that needs a mitigation plan.

**Deployment-specific notes:**
- For organizations with hybrid data stacks (e.g., a primary data warehouse plus a secondary data lake, a transformation layer, an ingestion/ETL layer, and event streaming), map each component to its layer (storage, transformation, movement, streaming) and assess integration depth at each layer. If the platform only connects at the storage/query layer, the organization carries the integration burden for transformation and movement.

### 4. Governance, Policy Enforcement, and Identity

How does the platform enforce rules about what agents can and cannot do?

**What to research:**
- Policy engine architecture: where in the execution path are policies evaluated?
- Identity model: named-user credentials vs. service accounts vs. both
- Can a single agent switch between identity contexts (e.g., named-user OAuth for interactive use, service account for batch operations)?
- Credential management: stored by the platform, or delegated to the organization's identity provider?
- Tool-level authorization: can policies restrict which tools an agent can call, and with what parameters?
- Audit trail granularity: does it capture prompt/response pairs, tool call parameters, policy rules evaluated, latency, token usage?

**What good looks like:** Runtime policy evaluation that intercepts agent-to-tool interactions before execution. Identity handled through the organization's existing IdP, not a parallel credential store. Audit trails granular enough to reconstruct any agent decision after the fact.

### 5. Vendor Lock-In, Portability, and Exit Strategy

What happens if the organization needs to leave?

**What to research:**
- Agent definition format: proprietary or exportable (YAML, JSON, Python)?
- Knowledge base portability: can stored knowledge be exported in standard formats?
- Governance policy portability: can rules be exported and version-controlled independently?
- Audit log export: can logs be streamed or exported to the organization's own systems (data warehouse, SIEM)?
- Model portability: is the platform model-agnostic, or does it favor specific providers?

**What good looks like:** Model portability (switch LLM providers without platform changes) is necessary but not sufficient. Platform portability — the ability to take agent definitions, knowledge, policies, and audit data with you — is what actually protects against lock-in. If the vendor's answer to "what does an exit look like?" is vague, that is a significant risk.

### 6. Compliance, Data Residency, and Data Training

What contractual and technical protections exist for the organization's data?

**What to research:**
- Certifications: SOC 2, ISO 27001, HIPAA, GDPR, FedRAMP
- Business Associate Agreement (BAA) availability if regulated data is involved
- Data residency: geographic restrictions on where data is processed and stored
- Data training: is any customer data used to train or fine-tune models, even in aggregate?
- Prompt/response logging: does the platform store prompt/response data? For how long? Who has access?
- Encryption: at rest, in transit, and in the policy evaluation pipeline

**What good looks like:** Clear, written commitments on data training (ideally a contractual guarantee that customer data is never used for model training). Data residency controls that match the organization's requirements. Certifications appropriate to the industry. Prompt/response retention policies that the organization can audit.

**Deployment-specific notes:**
- For B2B SaaS embedding: the organization's downstream customers (tenants) will want their own assurances. The platform's commitments need to be strong enough that the organization can make binding promises to its customers. Consider whether the platform's data protections extend to parent organizations and business lines within the organization, not just the organization as a whole.

---

## Tier 2: Deployment-Dependent

### 7. Multi-Tenancy and Data Isolation

**Primary for:** B2B SaaS embedding, any multi-tenant deployment
**Secondary for:** Internal enterprise (relevant if multiple business units need isolation)

This is often the most architecturally complex domain. The evaluation must address isolation at every tier the organization requires.

**Common isolation tiers:**
- **Entity-level** — Tenant A must never see Tenant B's data (e.g., Location A vs. Location B)
- **Group-level** — Parent Organization X must never see Parent Organization Y's data (e.g., groups of tenants under one corporate owner)
- **Business line-level** — The organization's own business lines must be walled off from each other (data from Business Line E must not inform or enhance Business Line F)
- **Aggregation** — Despite the above isolation, the organization's internal teams may need to aggregate data across all tiers for analytics and operations

**What to research:**
- Is multi-tenancy at the platform level only, or at the agent level (one agent definition serving N tenants)?
- Can the policy engine enforce row-level or schema-level isolation at runtime?
- How is tenant context passed into agent execution? Can downstream tools use it for scoping?
- Does the platform support multiple data connection patterns per tenant (separate schemas, sub-accounts, role-based access)?
- Can governance rules be audited to prove to a downstream customer that their data was never exposed to another tenant?
- How does platform-level isolation interact with the data platform's own RBAC (e.g., data warehouse roles)?

**What good looks like:** The platform can express isolation rules at every tier the organization needs, enforce them at runtime, and produce audit evidence that isolation was maintained. The tenant context should flow through the entire execution path, from agent invocation through policy evaluation to tool call parameterization.

### 8. Pricing and Commercial Model

**Primary for:** B2B SaaS embedding (OEM/white-label pricing is critical)
**Secondary for:** Internal enterprise, consumer-facing

**What to research:**
- Published pricing tiers and what each includes
- How "agent executions" (or the platform's billing unit) are defined and metered
- OEM, embedded, or white-label pricing for organizations reselling agent capabilities
- LLM inference cost model: bundled into platform fee, or passed through separately?
- Volume pricing at scale (thousands of tenants, hundreds of thousands of executions/month)

**What good looks like:** A pricing model that scales predictably with the organization's business model, not one designed for a different buyer profile. For B2B SaaS embedding, the critical question is whether the platform offers an OEM model — standard enterprise SaaS pricing assumes the buyer is the end user, which breaks when the buyer is a platform serving thousands of tenants.

### 9. API-First Architecture and Product Embedding

**Primary for:** B2B SaaS embedding, consumer-facing
**Secondary for:** Internal enterprise

**What to research:**
- API surface depth: can agents be created, tenants provisioned, data sources bound, and executions triggered entirely through APIs?
- SDK availability: languages, platforms (web, mobile), maturity
- White-label capability: can the organization fully brand the agent experience so downstream customers never see the vendor's UI?
- Rate limits and throughput caps at scale
- Webhook and event support for integrating agent activity into the organization's own monitoring and workflows

**What good looks like:** Full programmatic control over every operation that would otherwise require the vendor's UI. Rate limits documented and appropriate for the organization's scale. White-label support if downstream customers should not know the platform exists.

---

## Tier 3: Augmented Concerns

These domains are frequently overlooked in initial evaluations but can surface deal-shaping information. Include them even if they were not part of the original question set.

### 10. Agent Accuracy and Hallucination Controls

A confidently wrong answer is worse than no answer. This is especially acute for agents that generate SQL (a syntactically valid query that returns the wrong result set is hard to catch without guardrails) or answer data questions where downstream decisions depend on accuracy.

**What to research:**
- Confidence scoring, citation, or source attribution on agent responses
- Schema validation for generated SQL before execution
- Human-in-the-loop approval workflows for high-stakes answers
- Fallback routing: can the platform route to a human when confidence is below a threshold?
- Can generated queries be surfaced to the user for verification before execution?

### 11. Rollback and Change Management

When serving many tenants, a bad agent deployment needs to be rolled back in minutes, not hours. Standard expectations for production SaaS infrastructure include blue/green deployments, canary releases, and instant rollback.

**What to research:**
- Versioned agent deployments with rollback to a previous version
- Canary or staged rollouts: deploy to a subset of tenants before going broad
- Approval workflows for promoting changes from staging to production
- Change history and diff visibility for agent definitions

### 12. Latency and Performance at Scale

Uptime matters, and so does response time. Agent response time is a function of multiple hops (user to platform, policy evaluation, LLM inference, tool call, data query, return path), and at scale the queuing behavior matters.

**What to research:**
- Typical end-to-end latency for an agent execution involving an LLM call and one tool invocation
- Latency behavior under load (hundreds of simultaneous requests): queuing, throttling, degradation patterns
- Streaming response support for better perceived performance
- Geographic distribution of inference and tool execution

### 13. Company Maturity and Viability

Embedding a startup into the critical path of a product is a business risk. Technical fit is necessary but not sufficient if the vendor's runway, customer base, or product direction is uncertain.

**What to research:**
- Funding status and investors
- Number of enterprise customers in production (not pilot or POC)
- Largest deployment by end users or executions per month
- Source code escrow or business continuity provisions in enterprise contracts
- Product roadmap alignment with the organization's needs over 12-24 months

### 14. Build vs. Buy

This is not a domain to research about the vendor — it is a question the organization must ask itself. The core components most AI platforms provide (LLM routing, gateway, policy enforcement, audit logging) are implementable with open-source tools. The tradeoff is development time vs. dependency risk.

**What to frame for the meeting:**
- What specifically would the organization lose by building on open standards instead?
- Can the vendor point to a customer with a similar deployment model running in production?
- What is the realistic time-to-production for a representative use case: on the platform vs. self-built?

---

## Priority Ranking by Deployment Model

When synthesizing the evaluation into a prioritized gap list, use deployment model to weight the domains:

### B2B SaaS Embedding (most demanding)
1. Multi-tenancy and data isolation (all tiers)
2. Pricing and commercial model (OEM/embedded)
3. Data stack integration depth
4. Platform portability and exit strategy
5. API-first architecture and white-label
6. Audit trail depth and independence
7. Compliance and data training guarantees
8. DevOps maturity (CI/CD, rollback, monitoring)
9. Accuracy and hallucination controls
10. Company maturity and viability
11. Build vs. buy framing

### Internal Enterprise
1. Governance, policy enforcement, and identity
2. Data stack integration depth
3. Development experience
4. Compliance and data training guarantees
5. Platform portability and exit strategy
6. Accuracy and hallucination controls
7. Latency and performance
8. Company maturity and viability
9. Pricing (standard enterprise tiers)
10. Build vs. buy framing

### Consumer-Facing Product
1. Latency and performance at scale
2. Accuracy and hallucination controls
3. API-first architecture
4. Compliance and data residency
5. Rollback and change management
6. Multi-tenancy (user-level isolation)
7. Pricing (usage-based scaling)
8. Platform portability
9. Company maturity and viability
10. Build vs. buy framing
