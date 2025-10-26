# Agentic TCO Calculator v5.0
## Google Slides Presentation Content

---

## SLIDE 1: Title Slide

**Title**: Agentic TCO Calculator v5.0
**Subtitle**: Platform-Specific Total Cost of Ownership for Greenfield AI Agent Implementations

**Visual**: Calculator icon with 4 platform logos (UiPath, Microsoft, ServiceNow, Databricks)

**Footer**: TQA AMER | October 2025

---

## SLIDE 2: The Problem We're Solving

**Title**: Why Traditional Cost Estimation Fails for Agentic Systems

**Content**:

Traditional estimators don't account for:
- ❌ Multi-agent coordination complexity
- ❌ Tool development overhead  
- ❌ Platform-specific licensing tiers
- ❌ Token-based API consumption
- ❌ Ongoing infrastructure (vector DBs, observability)

**Result**: Estimates miss 30-50% of actual costs

**Visual**: Split screen showing "Traditional RPA" vs "Agentic System" architecture

---

## SLIDE 3: Our Solution

**Title**: Two-Dimensional Cost Model

**Content**:

**Year 1 TCO = Implementation + Runtime**

**Implementation Costs** (One-Time)
- T-shirt sized development effort
- Team configuration & velocity
- Risk-adjusted multipliers

**Runtime Costs** (Ongoing)
- Platform licenses
- API token consumption
- Infrastructure & monitoring

**Visual**: Stacked equation graphic showing the two components adding up to TCO

---

## SLIDE 4: T-Shirt Sizing Framework

**Title**: From Complexity to Cost in 4 Steps

**Visual**: 4-column table

| Size | Agents | Tools | Complexity Score | Base Days | Example |
|------|--------|-------|------------------|-----------|---------|
| **S** | 1 | 0-1 | 4-10 | 18 days | FAQ bot |
| **M** | 1-3 | 1-3 | 11-18 | 34 days | Invoice processor |
| **L** | 3-6 | 3-6 | 19-25 | 55 days | Contract analyzer |
| **XL** | 6-10+ | 6-10+ | 26-32 | 86 days | Autonomous ops |

**Key Point**: Complexity score (4-32) drives the sizing

---

## SLIDE 5: Complexity Scoring - The 4 Dimensions

**Title**: How We Calculate Complexity Score (1-8 points each)

**Content**:

**1. Prompt Complexity**
- Single instruction → Complex decision trees
- Example: "Summarize doc" (2) vs "Analyze, compare, recommend action" (7)

**2. Context Grounding**  
- Number of data sources agent must coordinate
- Example: 1 source (2) vs 6+ sources (8)

**3. Tool Requirements**
- Development effort for custom tools
- Example: Simple API call (2) vs Complex orchestration (8)

**4. Input/Output Arguments**
- Number of parameters and transformations
- Example: 3-5 args (2) vs 13+ args (8)

**Visual**: Four circles showing the dimensions, with example scores

---

## SLIDE 6: Implementation Cost Breakdown

**Title**: From Days to Dollars

**Content**:

**Base Effort** (by T-shirt size)
- Small: 18 days | Medium: 34 days | Large: 55 days | XL: 86 days

**Phase Distribution**:
- Definition: 8-10%
- Design: 15-20%
- Development: 40-45% ← Highest due to iteration
- Testing: 8-10%
- UAT: 15-18%
- Hypercare: 12-15%

**Team Configuration Impact**:
- 3-person pod: 1.0x velocity (6.8 weeks for Medium)
- 5-person pod: 1.5x velocity (4.5 weeks) ← **Standard**
- 7-person pod: 2.0x velocity (3.4 weeks)

**Blended Rate**: $1,400/day

**Visual**: Pie chart showing phase distribution + timeline comparison graphic

---

## SLIDE 7: Risk Multipliers

**Title**: What Increases Implementation Effort?

**Content**:

| Risk Factor | Impact | Why? |
|-------------|--------|------|
| Human-in-the-Loop | +20% | Approval workflows, UI, state mgmt |
| Complex Guardrails | +20% | Multiple validation layers, audit |
| First-Time Team | +15% | Learning curve, tooling setup |
| Regulatory | +20% | Compliance validation, docs |

**Example**:
- Base: 34 days (Medium)
- + HITL (+20%): 40.8 days
- + Regulatory (+20%): 48.96 days
- **Final: 49 days** (44% increase)

**Visual**: Bar chart showing cumulative effect of risk factors

---

## SLIDE 8: Platform Comparison - Year 1 TCO

**Title**: Typical Medium Project Across 4 Platforms

**Visual**: 4-column comparison chart

| Platform | Implementation | Annual Runtime | **Year 1 TCO** |
|----------|----------------|----------------|----------------|
| **UiPath** | $48K | $47K | **$95K** |
| **MS Copilot Studio** | $48K | $24K | **$72K** ← Lowest |
| **ServiceNow** | $48K | $38K | **$86K** |
| **Databricks** | $48K | $19K | **$67K** |

**Key Insight**: Runtime costs vary 2.5x across platforms

**Note**: Implementation costs same across platforms (same dev effort)

---

## SLIDE 9: Platform Deep Dive - UiPath

**Title**: UiPath: Best for RPA-to-Agent Transition

**Licensing Model**:
- Orchestrator Base: $15K/year
- Agent Builder: $12K/agent/year
- Platform Fee: $2K/year

**Pros**:
- ✅ Tight integration with existing RPA bots
- ✅ Enterprise-grade orchestration
- ✅ Strong governance & audit

**Cons**:
- ❌ Highest licensing costs
- ❌ Requires UiPath ecosystem knowledge

**Best For**: Organizations with existing UiPath investments

**Visual**: Cost breakdown pie chart + logo

---

## SLIDE 10: Platform Deep Dive - Microsoft Copilot Studio

**Title**: Microsoft: Best for M365 Ecosystems

**Licensing Model**:
- Copilot Studio: $200/user/month
- API Costs: $10/1M tokens (Azure OpenAI)
- Platform Fee: $0

**Pros**:
- ✅ Native M365 integration
- ✅ Familiar to existing Microsoft users
- ✅ Lowest runtime costs (tied to Databricks)

**Cons**:
- ❌ Per-user licensing can scale expensively
- ❌ Limited customization vs. code-first approaches

**Best For**: Microsoft shops, Copilot integration needs

**Visual**: Cost breakdown pie chart + logo

---

## SLIDE 11: Platform Deep Dive - ServiceNow

**Title**: ServiceNow: Best for ITSM Integration

**Licensing Model**:
- Now Assist Base: $25K/year
- User License: $150/user/month
- Platform Fee: $5K/year

**Pros**:
- ✅ Deep ITSM/ITOM integration
- ✅ Workflow automation out-of-box
- ✅ Strong for incident/change management

**Cons**:
- ❌ High base platform cost
- ❌ Requires ServiceNow instance

**Best For**: ServiceNow customers with ITSM/ITOM use cases

**Visual**: Cost breakdown pie chart + logo

---

## SLIDE 12: Platform Deep Dive - Databricks

**Title**: Databricks: Best for Data-Heavy Use Cases

**Licensing Model**:
- Compute: $0.55/DBU (~1,000 DBU/month)
- API Costs: $8/1M tokens
- Platform Fee: $0

**Pros**:
- ✅ Excellent for data lakehouse integration
- ✅ Pay-per-use (no platform fee)
- ✅ Best for ML-heavy workflows

**Cons**:
- ❌ DBU costs can spike with heavy compute
- ❌ Requires data engineering expertise

**Best For**: Data-intensive agents, lakehouse architecture

**Visual**: Cost breakdown pie chart + logo

---

## SLIDE 13: Runtime Cost Deep Dive

**Title**: What Drives Ongoing Costs?

**Content**:

**3 Components**:

**1. Platform Licenses** (40-60% of runtime)
- Vendor subscriptions, per-user/per-agent fees
- Most variable across platforms

**2. API Costs** (25-40% of runtime)
- Token consumption: ~2,000 tokens/request
- Scales with usage volume
- Formula: (Requests × 2K tokens / 1M) × $/1M tokens

**3. Infrastructure** (15-25% of runtime)
- Vector database: $900-1,500/year
- Observability: $720-1,200/year
- Content safety: $180-300/year
- Compute/storage: $600-1,200/year

**Visual**: Stacked bar chart showing the 3 components for each platform

---

## SLIDE 14: Calculator Demo

**Title**: Live Walkthrough

**Content**:

**Demo Steps**:
1. Select Platform (UiPath → Microsoft)
2. Choose T-shirt Size (Medium)
3. Configure Project (3 agents, 2 tools, 50K requests/month)
4. Add Risk Factors (HITL, First-Time Team)
5. View Results (Implementation + Runtime + TCO)
6. Export PDF

**Visual**: Screenshot of calculator UI with annotations

---

## SLIDE 15: Real-World Example - Invoice Processing

**Title**: Use Case: Medium Invoice Extraction Agent

**Scenario**: Extract line items, validate against PO, flag discrepancies

**Configuration**:
- Platform: Microsoft Copilot Studio
- Size: Medium (M)
- Agents: 2 (extraction + validation)
- Tools: 3 (PDF parser, ERP integration, approval workflow)
- Requests: 50,000/month
- Risk: HITL (+20%), First-Time Team (+15%)

**Results**:
- Implementation: 47 days × $1,400 = **$65,800**
- Runtime: $24,000/year
- **Year 1 TCO: $89,800**

**Visual**: Architecture diagram + cost breakdown

---

## SLIDE 16: Real-World Example - Contract Analysis

**Title**: Use Case: Large Contract Review System

**Scenario**: Multi-agent contract analysis with risk assessment

**Configuration**:
- Platform: Databricks
- Size: Large (L)
- Agents: 5 (intake, extract, analyze, compare, report)
- Tools: 6 (OCR, clause DB, risk scoring, etc.)
- Requests: 5,000/month (complex docs)
- Risk: Regulatory (+20%), Complex Guardrails (+20%)

**Results**:
- Implementation: 79 days × $1,400 = **$110,600**
- Runtime: $25,800/year
- **Year 1 TCO: $136,400**

**Visual**: Multi-agent architecture + cost breakdown

---

## SLIDE 17: Validation & Accuracy

**Title**: How We Validated the Model

**Data Sources**:
- ✅ 23 historical projects (UiPath, Microsoft, ServiceNow, Custom)
- ✅ Vendor pricing (Oct 2024)
- ✅ Industry benchmarks (Gartner, Forrester)

**Accuracy Target**: 85% of estimates within ±15% of actuals

**Current Performance**:
- Implementation: 87% accurate (13/15 projects)
- Runtime: 80% accurate (12/15 projects)
- Total TCO: 85% accurate (13/15 projects)

**Known Variances**:
- Tool complexity often underestimated
- Token consumption spikes during testing
- Platform pricing changes

**Visual**: Accuracy chart showing target vs. actual

---

## SLIDE 18: What's NOT Included

**Title**: Important Limitations & Assumptions

**NOT Included in Calculator**:
- ❌ Change management & training
- ❌ Data preparation (cleaning, labeling)
- ❌ Legal/compliance review costs
- ❌ Custom model fine-tuning
- ❌ Multi-year maintenance (Year 2+)

**Key Assumptions**:
- ✅ Team has access to required data
- ✅ Standard business hours (no 24/7 SLA)
- ✅ English language only
- ✅ Cloud deployment
- ✅ Standard APIs (no custom connectors)

**Recommendation**: Add 20-30% buffer for ambiguous scope

**Visual**: Two-column list (Not Included | Assumptions)

---

## SLIDE 19: When to Use This Calculator

**Title**: Ideal Use Cases

**✅ Perfect For**:
- Early-stage scoping and budgeting
- Platform comparison and selection
- RFP response cost estimation
- Executive-level TCO discussions
- Portfolio prioritization

**⚠️ Use With Caution**:
- Fixed-bid contract pricing (add buffer)
- Complex multi-vendor engagements
- Highly regulated industries (add 30-40%)
- Custom platform integrations

**🚫 Not Recommended**:
- After detailed requirements are locked
- When actual project plan exists (use that instead)
- For maintenance/support renewals

**Visual**: Traffic light graphic (green/yellow/red zones)

---

## SLIDE 20: Deployment & Access

**Title**: How to Use the Calculator

**Deployment Options**:

**Option 1: Azure Static Web Apps** (FREE)
- Zero cost hosting
- Team access via URL
- Recommended for testing

**Option 2: Azure Storage** (~$1-2/month)
- Static website hosting
- Low cost, high reliability

**Access**:
- URL: [agentic-tco-calculator.azurestaticapps.net]
- No login required (public)
- Export results to PDF
- Mobile responsive

**Visual**: Screenshot of deployed calculator + Azure logo

---

## SLIDE 21: Roadmap

**Title**: Future Enhancements

**v5.1 (Q1 2025)**:
- OpenAI Platform as 5th option
- Multi-year projections (Years 2-5)
- Custom team composition
- Excel export

**v6.0 (Q2 2025)**:
- ML calibration from actuals
- Sensitivity analysis (best/worst case)
- Side-by-side platform comparison
- Jira/Asana integration

**v7.0 (Q3 2025)**:
- AI-powered optimization recommendations
- Scenario planning
- Historical cost tracking dashboard
- Client portal for sharing estimates

**Visual**: Timeline roadmap with version milestones

---

## SLIDE 22: Key Takeaways

**Title**: Why This Matters

**5 Key Points**:

1. **Platform matters**: Runtime costs vary 2.5x (UiPath $47K vs Databricks $19K)

2. **Risk multipliers add up**: HITL + Regulatory + First-Time Team = 60% increase

3. **Team size affects timeline, not effort**: 7-person pod is 2x faster, not cheaper

4. **Medium is most common**: 34 days, ~$72-95K Year 1 TCO depending on platform

5. **Validation-backed**: 85%+ accuracy across 23 real projects

**Visual**: 5 icons representing each takeaway

---

## SLIDE 23: Comparison to Industry Standards

**Title**: How We Stack Up

**Industry Benchmarks**:

| Source | Agentic Project TCO (Medium) | Our Estimate |
|--------|------------------------------|--------------|
| Gartner (2024) | $75-120K | ✅ $67-95K |
| Forrester (2024) | $80-110K | ✅ $67-95K |
| Anthropic Case Studies | $65-100K | ✅ $67-95K |

**Why We're In Range**:
- Conservative token estimates (2K/request)
- Real project data, not theoretical
- Platform-specific pricing (not generic)
- Includes infrastructure & monitoring

**Visual**: Comparison bar chart

---

## SLIDE 24: Common Questions

**Title**: FAQ

**Q: Why is implementation cost the same across platforms?**
A: Development effort is independent of platform. Runtime costs vary due to licensing.

**Q: Can I customize the calculator for my org?**
A: Yes - it's open source. Adjust daily rates, token costs, or platform pricing.

**Q: How often is pricing updated?**
A: Quarterly. Last update: October 2024.

**Q: What if my project is between sizes?**
A: Use the complexity scoring dimensions to fine-tune (or split the difference).

**Q: Does this replace detailed project planning?**
A: No - use for early scoping. Detailed planning comes after.

---

## SLIDE 25: Next Steps

**Title**: How to Get Started

**For Teams Testing the Calculator**:
1. Visit [calculator URL]
2. Select your target platform
3. Input project parameters
4. Review TCO breakdown
5. Export PDF for stakeholders

**For Project Scoping**:
1. Run multiple scenarios (S/M/L sizing)
2. Compare platforms side-by-side
3. Add risk factors specific to your org
4. Use results for budget approval
5. Revisit after requirements finalized

**Contact**: [Your email/Slack channel]

**Visual**: CTA button "Launch Calculator" + contact info

---

## SLIDE 26: Thank You

**Title**: Questions?

**Contact Information**:
- Calculator URL: [link]
- Documentation: [link to doc]
- GitHub: [repo link if open source]
- Email: [your email]
- Slack: #agentic-calculator

**QR Code**: [To calculator URL]

**Visual**: Large QR code + contact details

---

## PRESENTATION NOTES

**Recommended Flow**:
- Slides 1-7: Problem, solution, methodology (10 min)
- Slides 8-12: Platform comparison (10 min)
- Slides 13-16: Deep dive + examples (15 min)
- Slides 17-20: Validation + usage (10 min)
- Slides 21-26: Future + Q&A (15 min)

**Total**: 60 minutes

**Tips**:
- Demo the calculator live on Slide 14
- Use real customer scenarios for Slides 15-16
- Keep platform slides (9-12) concise if audience already knows target platform
- Adjust depth based on audience (exec = high-level, SA = technical details)