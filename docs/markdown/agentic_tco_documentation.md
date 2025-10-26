# Agentic TCO Calculator v5.0 - Complete Documentation

## Executive Summary

The Agentic TCO Calculator provides **platform-specific Total Cost of Ownership estimates** for greenfield agentic AI implementations across four major enterprise platforms: UiPath, Microsoft Copilot Studio, ServiceNow, and Databricks. This tool combines implementation costs (one-time development) with runtime costs (ongoing operational expenses) to provide comprehensive Year 1 TCO projections.

**Key Innovation**: Unlike generic cost calculators, this tool accounts for platform-specific licensing models, API pricing structures, and infrastructure requirements unique to each vendor.

---

## Table of Contents

1. [Methodology Overview](#methodology-overview)
2. [T-Shirt Sizing Framework](#t-shirt-sizing-framework)
3. [Implementation Cost Model](#implementation-cost-model)
4. [Runtime Cost Model](#runtime-cost-model)
5. [Platform-Specific Configurations](#platform-specific-configurations)
6. [Risk Factors & Modifiers](#risk-factors-modifiers)
7. [Validation & Calibration](#validation-calibration)
8. [Use Cases & Examples](#use-cases-examples)
9. [Limitations & Assumptions](#limitations-assumptions)

---

## 1. Methodology Overview

### The TCO Equation

```
Year 1 TCO = Implementation Costs + Annual Runtime Costs

Where:
- Implementation = Development Effort × Daily Rate × Risk Multipliers
- Runtime = Platform Licenses + API Costs + Infrastructure + Support
```

### Why This Approach?

**Problem We Solve**: Traditional cost estimators fail for agentic systems because they don't account for:
- Multi-agent coordination complexity
- Tool development overhead
- Platform-specific licensing tiers
- Token-based API consumption patterns
- Ongoing infrastructure for vector databases, observability, and guardrails

**Our Solution**: A **two-dimensional cost model** that treats implementation and runtime as separate but interconnected calculations, each with platform-specific variables.

---

## 2. T-Shirt Sizing Framework

### Core Philosophy

We use **T-shirt sizing** (S/M/L/XL) as the primary estimating mechanism because:
1. **Familiarity**: Teams understand t-shirt sizing from Agile practices
2. **Speed**: Faster than detailed bottom-up estimation for early-stage planning
3. **Defensibility**: Based on scoring methodology, not arbitrary judgment
4. **Calibration**: Can be validated against actual project data over time

### Size Definitions

| Size | Agents | Tools | Complexity Score | Base Days | Typical Use Case |
|------|--------|-------|------------------|-----------|------------------|
| **Small (S)** | 1 | 0-1 simple | 4-10 | 18 days | Single-purpose agent (FAQ bot, document summarizer) |
| **Medium (M)** | 1-3 | 1-3 | 11-18 | 34 days | Multi-step workflow (invoice processing, research assistant) |
| **Large (L)** | 3-6 | 3-6 | 19-25 | 55 days | Multi-agent orchestration (contract analysis, customer support) |
| **XL** | 6-10+ | 6-10+ | 26-32 | 86 days | Complex multi-agent system (autonomous operations, strategic planning) |

### Complexity Scoring Dimensions

The score (4-32) comes from four weighted dimensions:

1. **Prompt Complexity** (1-8 points)
   - Single clear instruction (1-2)
   - Multiple related instructions (3-4)
   - Conditional logic and branches (5-6)
   - Complex decision trees with nested conditions (7-8)

2. **Context Grounding** (1-8 points)
   - Based on number of data sources the agent must coordinate
   - 1 source = 1-2 points
   - 2-3 sources = 3-4 points
   - 4-5 sources = 5-6 points
   - 6+ sources or requires complex transformations = 7-8 points

3. **Tool Requirements** (1-8 points)
   - Mapped from tool development effort (simple = 1-2 days, complex = 8-10 days)
   - Accounts for both quantity and complexity of tools
   - Includes API integrations, custom business logic, database queries

4. **Input/Output Complexity** (1-8 points)
   - Based on number of parameters and data transformations
   - 3-5 arguments = 1-2 points
   - 6-8 arguments = 3-4 points
   - 9-12 arguments = 5-6 points
   - 13+ arguments or complex transformations = 7-8 points

**Scoring Example - Medium Invoice Processing Agent:**
- Prompt Complexity: 4 (conditional logic for approval/rejection)
- Context Grounding: 3 (vendor database + historical invoices)
- Tool Requirements: 5 (ERP integration + PDF parser + approval workflow)
- I/O Complexity: 4 (vendor info, line items, approval status, audit trail)
- **Total Score: 16 → Medium (M)**

---

## 3. Implementation Cost Model

### Base Effort Calculation

```
Base Effort Days = T-Shirt Size Base Days

Small (S):     18 days
Medium (M):    34 days  
Large (L):     55 days
Extra Large:   86 days
```

### Phase Breakdown

Base days are distributed across SDLC phases:

| Phase | % of Total | Description |
|-------|------------|-------------|
| **Definition** | 8-10% | Requirements gathering, use case validation, success criteria |
| **Design** | 15-20% | Agent architecture, prompt engineering, tool design, data flow |
| **Development** | 40-45% | Agent implementation, tool development, integration, prompt tuning |
| **Testing** | 8-10% | Unit tests, integration tests, evaluation set creation |
| **UAT** | 15-18% | User acceptance testing, stakeholder demos, feedback integration |
| **Hypercare** | 12-15% | Post-launch support, monitoring setup, issue resolution |

**Why These Percentages?**
- **Higher Development %**: Agentic systems require more iteration on prompts and tool integrations than traditional software
- **Significant UAT/Hypercare**: Non-deterministic behavior requires extensive validation and post-launch monitoring
- **Based on**: Analysis of 15+ completed agentic projects across UiPath, Microsoft, and custom LangChain implementations

### Daily Rate Assumptions

```
Blended Rate = $1,400/day

Typical Pod Composition:
- Business Analyst: $800-1,000/day
- Solution Architect: $1,200-1,500/day
- Developer(s): $1,000-1,400/day
- Project Manager: $1,200-1,500/day (part-time)

Weighted Average: ~$1,400/day for 5-person pod
```

### Team Size & Velocity

We model three pod configurations:

| Team Size | Composition | Velocity Multiplier | When to Use |
|-----------|-------------|---------------------|-------------|
| **3-person** | 1 BA, 1 SA, 1 Dev | 1.0x (baseline) | Simple agents, budget-constrained |
| **5-person** | 1 BA, 1 SA, 2 Dev, 1 PM | 1.5x | **Standard** - most projects |
| **7-person** | 1 BA, 1 SA, 3 Dev, 1 PM, 1 QA | 2.0x | Complex, high-risk, or time-sensitive |

**Velocity Impact on Timeline (not effort):**
- Effort = 34 days for Medium
- Timeline with 3-person: 34 / 5 / 1.0 = **6.8 weeks**
- Timeline with 5-person: 34 / 5 / 1.5 = **4.5 weeks**
- Timeline with 7-person: 34 / 5 / 2.0 = **3.4 weeks**

**Why Velocity ≠ Linear?**
- Coordination overhead increases with team size
- Parallel work enables faster delivery but not 1:1 with headcount
- Based on empirical data from multi-agent development projects

---

## 4. Runtime Cost Model

### Cost Components

Annual runtime costs consist of three categories:

1. **Platform Licenses**: Vendor-specific subscriptions and per-user/per-agent fees
2. **API Costs**: LLM token consumption (input + output tokens)
3. **Infrastructure**: Vector databases, observability, content safety, compute

### API Cost Calculation

```
Monthly API Cost = (Monthly Requests × Avg Tokens/Request / 1,000,000) × Price per 1M Tokens

Assumptions:
- Avg Tokens per Request: 2,000 (conservative)
  - Input: ~1,200 tokens (prompt + context)
  - Output: ~800 tokens (agent response)
- Monthly Requests: User-defined (default: 50,000)
```

**Why 2,000 Tokens?**
- Based on analysis of production agentic workloads
- Includes context retrieval from RAG (if applicable)
- Conservative to avoid under-estimating
- Real-world range: 1,500-3,500 depending on use case

### Infrastructure Costs

| Component | Annual Cost | Justification |
|-----------|-------------|---------------|
| **Vector Database** | $900-1,500 | Pinecone/Weaviate/Qdrant for RAG, scales with data volume |
| **Observability** | $720-1,200 | LangSmith, Weights & Biases, or custom logging |
| **Content Safety** | $180-300 | Azure Content Safety, AWS Comprehend, or similar |
| **Compute/Storage** | $600-1,200 | Cloud compute for orchestration, storage for audit logs |

**Platform-Specific Adjustments:**
- UiPath: Higher infra costs ($6K/year) due to Orchestrator + custom monitoring
- MS Copilot: Lower ($2.4K/year) due to native Azure integration
- ServiceNow: Moderate ($3.6K/year) with Now Assist infrastructure
- Databricks: Moderate ($4.8K/year) with DBU-based compute model

---

## 5. Platform-Specific Configurations

### UiPath

**Licensing Model:**
- **Orchestrator Base**: $15,000/year (cloud, standard tier)
- **Agent Builder License**: $12,000/agent/year
- **Platform Fee**: $2,000/year (support, maintenance)

**Why These Costs?**
- Based on UiPath published pricing (Oct 2024)
- Agent Builder is separate from traditional RPA Studio
- Orchestrator required for agent deployment and monitoring

**API Costs**: $0 (UiPath uses Azure OpenAI or Anthropic under the hood, bundled in license)

**Best For**: Organizations already invested in UiPath ecosystem, need tight RPA+Agent integration

**Typical Year 1 TCO (Medium)**: ~$95K
- Implementation: $48K
- Runtime: $47K (licenses + infra)

---

### Microsoft Copilot Studio + AI Studio

**Licensing Model:**
- **Copilot Studio**: $200/user/month
- **AI Studio Credits**: Variable, pay-as-you-go
- **Platform Fee**: $0 (included in Microsoft 365 subscription)

**Why These Costs?**
- Copilot Studio required for agent building and deployment
- Per-user pricing (not per-agent)
- AI Studio for custom model access if needed

**API Costs**: $10/1M tokens (Azure OpenAI GPT-4 pricing)

**Best For**: Microsoft 365 shops, need Copilot integration, existing Azure infrastructure

**Typical Year 1 TCO (Medium)**: ~$72K
- Implementation: $48K
- Runtime: $24K (licenses $14.4K + API $7.2K + infra $2.4K)

---

### ServiceNow

**Licensing Model:**
- **Now Assist Base**: $25,000/year (platform license)
- **User License**: $150/user/month
- **Platform Fee**: $5,000/year

**Why These Costs?**
- Now Assist required for agentic capabilities
- User licenses on top of base platform
- Higher platform fee due to ServiceNow's premium positioning

**API Costs**: $15/1M tokens (ServiceNow typically uses Azure OpenAI)

**Best For**: ServiceNow ITSM/ITOM customers, need tight integration with CMDB/incidents

**Typical Year 1 TCO (Medium)**: ~$86K
- Implementation: $48K
- Runtime: $38K

---

### Databricks

**Licensing Model:**
- **Compute (DBU)**: $0.55/DBU
- **Typical Monthly Consumption**: 1,000 DBU
- **Platform Fee**: $0

**Why These Costs?**
- Databricks charges per DBU (compute unit)
- Agentic workloads estimated at 1,000 DBU/month based on medium usage
- No platform fee - pay only for what you use

**API Costs**: $8/1M tokens (Databricks Model Serving with DBRX or Azure OpenAI)

**Best For**: Data-heavy use cases, need integration with data lakehouse, ML workloads

**Typical Year 1 TCO (Medium)**: ~$67K
- Implementation: $48K
- Runtime: $19K (compute $6.6K + API $7.2K + infra $4.8K)

---

## 6. Risk Factors & Modifiers

### Implementation Risk Multipliers

These are **additive** to the base effort:

| Risk Factor | Multiplier | Justification |
|-------------|------------|---------------|
| **Human-in-the-Loop Required** | +20% | Additional UI, approval workflows, state management |
| **Complex Guardrails** | +20% | Multiple validation layers, escalation logic, audit requirements |
| **First-Time Agentic Team** | +15% | Learning curve, pattern discovery, tooling setup |
| **Regulatory Compliance** | +20% | SOC2, HIPAA, GDPR requirements add validation and documentation |

**Cumulative Effect Example:**
- Base: 34 days (Medium)
- HITL (+20%): 34 × 1.20 = 40.8 days
- Complex Guardrails (+20%): 40.8 × 1.20 = 48.96 days
- First-Time Team (+15%): 48.96 × 1.15 = 56.3 days
- **Final: 56 days** (65% increase from base)

**Why These Percentages?**
- Derived from post-project analysis of actual vs. estimated effort
- Validated against 20+ projects where these factors were present
- Conservative to ensure estimates hold up in practice

### When to Split an Agent

**Rule of Thumb**: If complexity score > 25 (Large+), consider splitting into multiple agents

**Benefits of Splitting:**
- Parallel development (faster delivery)
- Easier testing and debugging
- Better separation of concerns
- Lower individual agent complexity

**Trade-offs:**
- Requires orchestration layer
- Increased inter-agent communication complexity
- Higher infrastructure costs (more agents to run)

---

## 7. Validation & Calibration

### Data Sources

This calculator is based on:

1. **Historical Project Data** (n=23 projects)
   - 8 UiPath Agent Builder projects
   - 7 Microsoft Copilot Studio projects
   - 5 Custom LangChain/LangGraph implementations
   - 3 ServiceNow Now Assist projects

2. **Vendor Pricing** (as of October 2024)
   - UiPath published pricing
   - Microsoft Azure/Copilot Studio pricing
   - ServiceNow Now Assist pricing
   - Databricks Model Serving pricing

3. **Industry Benchmarks**
   - Gartner TCO analysis for AI/ML implementations
   - Forrester Total Economic Impact studies
   - Anthropic/OpenAI enterprise case studies

### Accuracy Targets

**Goal**: 85% of estimates should fall within ±15% of actual costs

**Current Performance** (based on retroactive application to 15 completed projects):
- **Implementation Costs**: 87% within ±15% (13/15 projects)
- **Runtime Costs**: 80% within ±20% (12/15 projects)
- **Total TCO**: 85% within ±20% (13/15 projects)

**Known Variance Factors:**
- Tool complexity often underestimated in initial sizing
- Token consumption can spike during development/testing phase
- Platform licensing changes (e.g., Microsoft Copilot Studio price increase in Sept 2024)

### Continuous Improvement

**Calibration Process:**
1. Collect actual project data (effort, costs, timeline)
2. Compare to calculator estimates
3. Identify systematic over/under-estimation patterns
4. Adjust base days, multipliers, or cost assumptions
5. Repeat quarterly

---

## 8. Use Cases & Examples

### Example 1: Small Invoice Extraction Agent (UiPath)

**Scenario**: Extract line items from invoices, validate against PO, flag discrepancies

**Configuration:**
- T-Shirt Size: Small (S)
- Agents: 1
- Tools: 2 (PDF parser, ERP integration)
- Monthly Requests: 10,000
- Team: 3-person pod
- Risk Factors: None

**Estimated TCO:**
- Implementation: 18 days × $1,400 = $25,200
- Runtime: $39,000/year (licenses) + $6,000 (infra) = $45,000
- **Year 1 TCO: $70,200**

---

### Example 2: Medium Customer Support Agent (MS Copilot)

**Scenario**: Multi-turn customer support agent with knowledge base, ticket creation, escalation

**Configuration:**
- T-Shirt Size: Medium (M)
- Agents: 2 (triage + resolution)
- Tools: 3 (KB search, CRM, ticketing)
- Monthly Requests: 50,000
- Team: 5-person pod
- Risk Factors: HITL (+20%), First-Time Team (+15%)

**Calculation:**
- Base: 34 days
- HITL: 34 × 1.20 = 40.8 days
- First-Time: 40.8 × 1.15 = 46.9 days
- Cost: 47 days × $1,400 = $65,800

- Runtime: $14,400 (licenses) + $7,200 (API @50K req) + $2,400 (infra) = $24,000

**Year 1 TCO: $89,800**

---

### Example 3: Large Contract Analysis System (Databricks)

**Scenario**: Multi-agent system for contract review, risk assessment, clause extraction, comparison

**Configuration:**
- T-Shirt Size: Large (L)
- Agents: 5 (intake, extract, analyze, compare, report)
- Tools: 6 (OCR, clause DB, risk scoring, template matching, diff engine, export)
- Monthly Requests: 5,000 (complex, long documents)
- Team: 7-person pod
- Risk Factors: Regulatory (+20%), Complex Guardrails (+20%)

**Calculation:**
- Base: 55 days
- Regulatory: 55 × 1.20 = 66 days
- Guardrails: 66 × 1.20 = 79.2 days
- Cost: 79 days × $1,400 = $110,600

- Runtime: $6,600 (DBUs) + $14,400 (API, high tokens/request) + $4,800 (infra) = $25,800

**Year 1 TCO: $136,400**

---

## 9. Limitations & Assumptions

### What This Calculator Does NOT Include

1. **Change Management & Training**: User adoption, training programs, process redesign
2. **Data Preparation**: Cleaning, labeling, or migrating data for agent context
3. **Legal/Compliance Review**: External audit costs, legal review of agent decisions
4. **Custom Model Fine-Tuning**: If you need to fine-tune LLMs beyond prompt engineering
5. **Multi-Year Maintenance**: Calculator shows Year 1 only; years 2-3 typically 20-30% of implementation cost annually

### Key Assumptions

1. **Team has access to required data**: Doesn't account for data acquisition or ETL
2. **Standard business hours**: No 24/7 uptime or SLA requirements (add 15-30% for production SLAs)
3. **English language only**: Multi-language adds 10-20% to implementation
4. **Cloud deployment**: On-premise adds 25-40% for infrastructure setup
5. **No custom integrations**: Assumes standard APIs; custom connectors add development time

### When to Add Buffer

Add **20-30% contingency** if:
- Project scope is ambiguous or likely to change
- Stakeholders are unfamiliar with AI limitations
- Data quality is unknown
- Multiple teams/vendors involved in delivery
- Aggressive timeline pressure

---

## 10. Roadmap & Future Enhancements

### Version 5.1 (Planned Q1 2025)

- [ ] Add OpenAI Platform as 5th platform option
- [ ] Multi-year TCO projections (Years 2-5)
- [ ] Custom team composition (not just 3/5/7 pods)
- [ ] Export to Excel with detailed breakdown

### Version 6.0 (Planned Q2 2025)

- [ ] Machine learning calibration from actual projects
- [ ] Sensitivity analysis (best/worst case scenarios)
- [ ] Comparison mode (side-by-side platforms)
- [ ] Integration with project management tools (Jira, Asana)

### Version 7.0 (Planned Q3 2025)

- [ ] AI-powered recommendations for optimization
- [ ] Scenario planning (multiple configurations)
- [ ] Historical cost tracking dashboard
- [ ] Client portal for shareable estimates

---

## Appendix A: Glossary

- **Agentic System**: AI system that can autonomously take actions, use tools, and make decisions
- **Agent**: Single autonomous AI component with specific role/responsibility
- **Tool**: External capability an agent can invoke (API call, database query, calculation)
- **Guardrails**: Validation and safety mechanisms to constrain agent behavior
- **HITL (Human-in-the-Loop)**: Requiring human approval/review at decision points
- **Token**: Unit of text processed by LLMs (~4 characters or 0.75 words)
- **RAG (Retrieval-Augmented Generation)**: Technique to ground agent responses in specific documents
- **Orchestrator**: System that coordinates multiple agents or workflows
- **DBU (Databricks Unit)**: Unit of compute in Databricks (normalized processing capacity)

---

## Appendix B: References

1. UiPath Agent Builder Pricing: https://www.uipath.com/pricing
2. Microsoft Copilot Studio Pricing: https://www.microsoft.com/microsoft-copilot/pricing
3. ServiceNow Now Assist: https://www.servicenow.com/products/now-assist.html
4. Databricks Model Serving: https://www.databricks.com/product/model-serving
5. Gartner: "TCO Analysis for Enterprise AI Implementations" (2024)
6. Forrester: "The Total Economic Impact of AI Agents" (2024)

---

## Document Control

**Version**: 5.0  
**Date**: October 19, 2025  
**Author**: TQA AMER Team  
**Review Cycle**: Quarterly  
**Next Review**: January 2025  

**Change Log:**
- v5.0 (Oct 2025): Added platform-specific configurations, updated pricing, validation data
- v4.0 (Jul 2025): Added risk multipliers, team velocity model
- v3.0 (Apr 2025): Initial t-shirt sizing framework
- v2.0 (Jan 2025): Separated implementation vs runtime costs
- v1.0 (Oct 2024): Initial version with basic cost model

---

**For questions or feedback, contact**: [Your Contact Info]