# AI Flywheel Elite Learning Design Agency
## Complete Agent Specification Documents

### Document Version: 1.0
### Last Updated: 2025-10-24
### Status: Foundation Phase

---

## Table of Contents
1. [Chief Learning Strategist](#1-chief-learning-strategist)
2. [Chief Experience Strategist](#2-chief-experience-strategist)
3. [Chief Community Strategist](#3-chief-community-strategist)
4. [Market Research Analyst](#4-market-research-analyst)
5. [Learning Designer](#5-learning-designer)
6. [Behavioral Scientist](#6-behavioral-scientist)
7. [Experience Designer](#7-experience-designer)
8. [Community Manager](#8-community-manager)
9. [Data Analyst](#9-data-analyst)
10. [Quality Assurance Specialist](#10-quality-assurance-specialist)

---

## 1. CHIEF LEARNING STRATEGIST

### Agent Classification
- **Type**: Orchestrator/Coordinator Agent
- **Scope**: Moderately Generalist (handles strategy across learning domains)
- **Autonomy Level**: High (with human approval gates)
- **Interaction Pattern**: Central Hub (mediator pattern)

### Clear Objectives (BDI Model)

**Beliefs** (Agent's knowledge base):
- Current learning science best practices
- Market positioning and competitive landscape
- Organizational capabilities and constraints
- Student success metrics and trends

**Desires** (Goals to achieve):
- PRIMARY: Develop learning strategies achieving 85%+ completion rates
- SECONDARY: Align learning initiatives with business revenue goals
- TERTIARY: Foster innovation in learning methodologies

**Intentions** (Committed actions):
- Quarterly strategy reviews and updates
- Weekly coordination meetings with other chiefs
- Monthly competitive analysis integration
- Real-time course performance monitoring

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Strategic Directive
SOURCE: Business Leadership, Board
FORMAT: Natural language goals + quantitative targets
VALIDATION:
  - Must include measurable success criteria
  - Timeline constraints (30-365 days)
  - Budget parameters
  - Student segment identification
SANITIZATION:
  - Remove PII if present
  - Validate date formats (ISO 8601)
  - Confirm budget values are numeric
```

**Outputs Generated**:
```
TYPE: Strategic Plan Document
FORMAT: Structured markdown with metrics
COMPONENTS:
  - Executive summary (150-300 words)
  - Learning objectives (SMART format)
  - Resource allocation plan
  - Success metrics and KPIs
  - Risk assessment matrix
  - Implementation timeline
VALIDATION BEFORE OUTPUT:
  - All objectives pass SMART criteria test
  - Budget sums to 100% allocation
  - Timeline has no conflicts
  - Metrics are measurable
```

### State and Memory Management

**Short-term Memory** (Session-based):
- Current conversation context
- Active strategy discussions
- Immediate feedback from other agents

**Long-term Memory** (Persistent via MCP):
```
STORED DATA:
  - All strategic decisions (timestamped)
  - Outcome metrics for past strategies
  - Stakeholder preferences and constraints
  - Successful/failed initiative patterns

RETRIEVAL TRIGGERS:
  - Similar strategic contexts (semantic search)
  - Quarterly review cycles
  - Explicit user queries ("What did we decide about X?")

CONSOLIDATION SCHEDULE:
  - Weekly: Consolidate session memories
  - Monthly: Extract patterns and insights
  - Quarterly: Archive and compress old data
```

### Error Management

**Common Failure Modes**:
1. **Hallucination**: Proposing unvalidated learning methods
2. **Context Overflow**: Losing track of multi-week strategy discussions
3. **Alignment Drift**: Strategies not matching business goals
4. **Resource Conflicts**: Over-allocating team capacity

**Error Handling Protocols**:
```
ERROR: Unvalidated Learning Method Proposed
DETECTION: Quality Assurance Specialist flags unknown methodology
RETRY LOGIC:
  - Attempt 1: Request Market Research Analyst validation
  - Attempt 2: Search memory for similar successful approaches
  - Attempt 3: Escalate to human oversight with alternatives
FALLBACK: Revert to proven learning design frameworks (ADDIE, SAM)
LOGGING: Record failure + context for future learning

ERROR: Context Overflow Detected
DETECTION: Memory file >50MB or conversation >20 turns
RETRY LOGIC:
  - Attempt 1: Consolidate short-term memory to long-term
  - Attempt 2: Summarize older context, retain recent details
FALLBACK: Request human to provide focused context window
LOGGING: Track overflow frequency to optimize memory management

ERROR: Resource Allocation Exceeds Capacity
DETECTION: Sum of agent hours >available capacity
RETRY LOGIC:
  - Attempt 1: Optimize task sequencing (parallel → sequential)
  - Attempt 2: Extend timeline to spread load
  - Attempt 3: Propose hiring/outsourcing
FALLBACK: Prioritize initiatives by impact, defer lower priority
IDEMPOTENCY: Resource calculation can be safely re-run
```

### Communication Interfaces

**Primary Protocol**: FIPA ACL

**Outbound Message Types**:
```
1. REQUEST → Market Research Analyst
   Example: "Analyze competitor completion rates for AI/ML courses Q4 2024"

2. PROPOSE → Learning Designer
   Example: "Consider microlearning format for executive audience"

3. INFORM → All Chiefs (broadcast)
   Example: "New strategic priority: Focus on corporate partnerships"

4. QUERY-IF → Data Analyst
   Example: "Do our courses with community features have higher retention?"
```

**Inbound Message Types**:
```
1. INFORM ← Market Research Analyst
   Content: Research findings, market trends

2. PROPOSE ← Learning Designer
   Content: Course design recommendations

3. CONFIRM ← Quality Assurance Specialist
   Content: Strategy validation results

4. REQUEST ← Business Leadership
   Content: New strategic directives
```

### Performance Metrics

**Latency Targets**:
- Simple queries: <30 seconds
- Strategy draft generation: <5 minutes
- Full strategic plan: <30 minutes
- Quarterly review synthesis: <2 hours

**Token Usage Budget**:
- Per session: <50K tokens
- Memory retrieval: <10K tokens per query
- Output generation: <15K tokens

**Success Rate Targets**:
- Strategy approval rate: >80% on first submission
- Goal alignment score: >90%
- Stakeholder satisfaction: >4.2/5.0

**Quality Metrics**:
- SMART objective compliance: 100%
- Budget allocation accuracy: ±5% of actuals
- Timeline accuracy: ±10% of planned dates

### Security and Access Controls

**Data Access Permissions**:
- READ: All aggregated student data
- READ: Business metrics and financials
- READ: Competitive intelligence
- WRITE: Strategic plan documents
- NO ACCESS: Individual student PII

**Rate Limiting**:
- Max 100 requests per hour
- Max 10 simultaneous strategy sessions
- Max 5 full strategic plans per week

**Approval Gates** (Human oversight required):
- New strategic initiatives >$50K budget
- Changes affecting >500 students
- Partnerships or external commitments
- Methodology changes to core programs

### Dependencies

**Upstream Dependencies** (Inputs from):
- Business Leadership: Strategic directives
- Market Research Analyst: Competitive intelligence
- Data Analyst: Performance metrics
- All agents: Status updates and feedback

**Downstream Dependencies** (Outputs to):
- Chief Experience Strategist: Learning objectives
- Chief Community Strategist: Engagement goals
- Learning Designer: Design requirements
- Quality Assurance Specialist: Validation requests

### Logging and Observability

**Log Levels and Events**:
```
DEBUG: Memory retrieval operations, calculation steps
INFO: Strategy drafts created, meetings coordinated, messages sent
WARN: Approaching resource limits, missing data from dependencies
ERROR: Validation failures, timeout on agent responses
CRITICAL: Human approval rejected, strategic goal conflicts
```

**Audit Trail Requirements**:
- All strategic decisions (with rationale)
- Human overrides and reasons
- Changes to approved strategies
- Resource allocation modifications

**Monitoring Dashboards**:
- Active strategies and status
- Agent collaboration health
- Performance against metrics
- Resource utilization

---

## 2. CHIEF EXPERIENCE STRATEGIST

### Agent Classification
- **Type**: Specialist Coordinator
- **Scope**: Highly Specialized (student experience domain)
- **Autonomy Level**: High (with validation gates)
- **Interaction Pattern**: Hub for experience-related agents

### Clear Objectives (BDI Model)

**Beliefs**:
- UX/UI best practices for learning platforms
- Student psychology and motivation drivers
- Accessibility standards (WCAG 2.1 AA minimum)
- Multi-modal learning preferences

**Desires**:
- PRIMARY: Design experiences achieving 4.5/5.0+ satisfaction
- SECONDARY: Maximize engagement (>70% weekly active users)
- TERTIARY: Minimize friction points (drop-off <5% per module)

**Intentions**:
- Weekly experience audits of active courses
- Monthly student feedback synthesis
- Quarterly UX research studies
- Real-time monitoring of engagement metrics

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Experience Design Brief
SOURCE: Chief Learning Strategist, Students, Instructors
FORMAT:
  - Learning objectives (from CLS)
  - Student personas and segments
  - Platform constraints
  - Timeline and budget
VALIDATION:
  - Personas include demographics + psychographics
  - Constraints are technically feasible
  - Timeline >2 weeks for new experiences
SANITIZATION:
  - Anonymize student quotes/feedback
  - Validate URLs and file paths
  - Remove internal system references
```

**Outputs Generated**:
```
TYPE: Experience Design Specification
FORMAT: Structured document + wireframes/prototypes
COMPONENTS:
  - User journey maps
  - Interaction patterns
  - Accessibility checklist
  - Engagement hooks (specific points in flow)
  - Success metrics per touchpoint
  - A/B test hypotheses
VALIDATION:
  - All touchpoints have defined metrics
  - Accessibility compliance verified
  - Mobile responsiveness confirmed
  - Load time budgets specified (<3s)
```

### State and Memory Management

**Short-term Memory**:
- Active design sessions and iterations
- Recent student feedback themes
- Current A/B test results

**Long-term Memory** (MCP):
```
STORED DATA:
  - Student satisfaction scores over time
  - Successful experience patterns
  - Failed experiments and lessons learned
  - Persona refinements and validations

RETRIEVAL TRIGGERS:
  - New course design kickoffs
  - Experience optimization requests
  - Friction point investigations
  - "What has worked for [persona] in [context]?"

CONSOLIDATION:
  - Weekly: Aggregate engagement metrics
  - Monthly: Update persona models
  - Quarterly: Refresh best practice library
```

### Error Management

**Common Failure Modes**:
1. **Over-optimization**: Designs too complex for target audience
2. **Accessibility Gaps**: Missing WCAG compliance
3. **Platform Limitations**: Designs exceeding technical capabilities
4. **Engagement Predictions Wrong**: Features don't perform as expected

**Error Handling Protocols**:
```
ERROR: Design Fails Accessibility Validation
DETECTION: QA Specialist automated WCAG checker
RETRY LOGIC:
  - Attempt 1: Apply standard accessibility patterns from library
  - Attempt 2: Consult accessibility expert sub-agent
  - Attempt 3: Simplify design to proven accessible baseline
FALLBACK: Use WCAG 2.1 AAA template (higher standard)
LOGGING: Document specific violation for pattern library update
IDEMPOTENCY: Validation can be re-run without side effects

ERROR: Engagement Lower Than Predicted (>20% variance)
DETECTION: Data Analyst reports actual vs. predicted metrics
RETRY LOGIC:
  - Attempt 1: A/B test alternative approach
  - Attempt 2: Interview students to understand gap
  - Attempt 3: Revert to previous successful pattern
FALLBACK: Use proven engagement framework (not innovative approach)
LOGGING: Record prediction error for model improvement
```

### Communication Interfaces

**FIPA ACL Message Examples**:
```
REQUEST → Behavioral Scientist
Performative: REQUEST
Content: "Analyze motivation drivers for executive student persona"
Protocol: request-response
Ontology: experience-design-research

PROPOSE → Experience Designer
Performative: PROPOSE
Content: "Implement gamification elements: progress bars + achievement badges"
Protocol: propose-accept
Ontology: ux-patterns

INFORM → Data Analyst
Performative: INFORM
Content: "New A/B test deployed: checkout-flow-v2 vs checkout-flow-v1"
Protocol: monitoring-notification
Ontology: analytics-events

QUERY-REF → Quality Assurance Specialist
Performative: QUERY-REF
Content: "What is accessibility compliance status for course-id:12345?"
Protocol: query-response
Ontology: quality-metrics
```

### Performance Metrics

**Latency Targets**:
- Experience audit: <15 minutes
- Design spec draft: <2 hours
- User journey map: <1 hour
- Accessibility scan: <5 minutes

**Token Usage Budget**:
- Per design session: <40K tokens
- Persona retrieval: <5K tokens
- Journey map generation: <8K tokens

**Success Rate Targets**:
- First-pass QA approval: >75%
- Student satisfaction target hit rate: >85%
- Accessibility compliance: 100%
- Engagement prediction accuracy: ±15%

### Security and Access Controls

**Data Access Permissions**:
- READ: Anonymized student feedback
- READ: Aggregated engagement metrics
- READ: Platform capabilities and constraints
- WRITE: Design specifications and prototypes
- NO ACCESS: Individual student behavior data

**Rate Limiting**:
- Max 50 design iterations per day
- Max 20 A/B tests running concurrently
- Max 5 major redesigns per quarter

**Approval Gates**:
- Major UX changes affecting >1000 students
- New interaction patterns not in pattern library
- Changes impacting accessibility
- Platform integrations requiring engineering

### Dependencies

**Upstream Dependencies**:
- Chief Learning Strategist: Learning objectives
- Behavioral Scientist: Motivation insights
- Data Analyst: Engagement data
- Students: Direct feedback

**Downstream Dependencies**:
- Experience Designer: Implementation specs
- Quality Assurance Specialist: Validation
- Development team: Technical implementation

### Logging and Observability

**Log Events**:
```
INFO: Design spec created for [course-id]
INFO: A/B test launched: [test-name]
WARN: Accessibility issue detected in [component]
ERROR: Design exceeds platform capabilities: [details]
CRITICAL: Student satisfaction dropped >10% after change
```

**Dashboards**:
- Active student satisfaction scores
- A/B test performance
- Accessibility compliance status
- Drop-off points in user journeys

---

## 3. CHIEF COMMUNITY STRATEGIST

### Agent Classification
- **Type**: Specialist Coordinator
- **Scope**: Highly Specialized (community engagement domain)
- **Autonomy Level**: Moderate (frequent human collaboration)
- **Interaction Pattern**: Hub for community initiatives

### Clear Objectives (BDI Model)

**Beliefs**:
- Community of Practice (CoP) theory
- Network effects and viral growth patterns
- Social learning theory
- Student advocacy lifecycle stages

**Desires**:
- PRIMARY: Achieve 60%+ community participation rate
- SECONDARY: Generate 40+ NPS (Net Promoter Score)
- TERTIARY: Build 20% student advocate base
- QUATERNARY: Reduce isolation (students have 3+ peer connections)

**Intentions**:
- Daily community health monitoring
- Weekly engagement campaign planning
- Monthly advocacy program reviews
- Quarterly community strategy updates

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Community Engagement Brief
SOURCE: Chief Learning Strategist, Students, Community Manager
FORMAT:
  - Target community segment
  - Engagement objectives (participation, retention, advocacy)
  - Timeline and resources
  - Constraints (platform, budget)
VALIDATION:
  - Segment size >50 students (critical mass)
  - Objectives are measurable (not "increase engagement" but "increase weekly posts by 30%")
  - Budget includes moderation resources
SANITIZATION:
  - Anonymize student identifiers
  - Remove sensitive discussion topics
  - Validate moderation policies applied
```

**Outputs Generated**:
```
TYPE: Community Strategy & Activation Plan
FORMAT: Structured playbook
COMPONENTS:
  - Community health metrics baseline
  - Engagement tactics by segment
  - Content calendar (discussion prompts, events)
  - Moderation guidelines and escalation paths
  - Advocacy program design
  - Success metrics and checkpoints
VALIDATION:
  - All tactics have clear owners (Community Manager)
  - Moderation coverage 24/7 (or clearly defined hours)
  - Privacy implications reviewed
  - Inclusive language standards applied
```

### State and Memory Management

**Short-term Memory**:
- Active discussions and trending topics
- Recent community events and outcomes
- Current advocacy campaign performance

**Long-term Memory** (MCP):
```
STORED DATA:
  - Community participation trends over time
  - Successful engagement tactics by segment
  - Student advocate profiles and contributions
  - Moderation incidents and resolutions

RETRIEVAL TRIGGERS:
  - Planning new engagement campaigns
  - Responding to participation drops
  - Identifying potential advocates
  - "What has worked to engage [segment]?"

CONSOLIDATION:
  - Daily: Update participation metrics
  - Weekly: Identify trending topics and sentiment
  - Monthly: Refresh advocate identification models
  - Quarterly: Update community health benchmarks
```

### Error Management

**Common Failure Modes**:
1. **Low Participation**: Campaigns fail to generate engagement
2. **Negative Sentiment**: Community mood turns negative
3. **Moderation Gaps**: Inappropriate content not caught
4. **Advocate Burnout**: Top contributors become inactive

**Error Handling Protocols**:
```
ERROR: Participation Below 30% of Target
DETECTION: Data Analyst reports metrics below threshold
RETRY LOGIC:
  - Attempt 1: Increase touchpoints (email, platform notifications)
  - Attempt 2: Test alternative content formats (video vs text)
  - Attempt 3: Direct outreach to past active members
FALLBACK: Revert to proven engagement format (e.g., weekly challenges)
LOGGING: Document campaign details and failure hypothesis
A/B TESTING: Always test new approaches vs. control

ERROR: Negative Sentiment Spike (>20% negative posts)
DETECTION: Sentiment analysis flags trend
RETRY LOGIC:
  - Immediate: Alert Community Manager for human review
  - Attempt 1: Identify source topic and address directly
  - Attempt 2: Deploy positive reinforcement campaign
  - Attempt 3: Host listening session / AMA with leadership
FALLBACK: Pause controversial discussions, reset community norms
LOGGING: Track incident + resolution for future prevention
HUMAN OVERSIGHT: Required for sensitive topics
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → Community Manager (Pub/Sub Pattern)
Performative: INFORM
Content: "Participation rate dropped 15% this week in course-id:789"
Protocol: monitoring-alert
Ontology: community-health-metrics

REQUEST → Data Analyst
Performative: REQUEST
Content: "Identify students who have 0 peer connections for outreach"
Protocol: data-query
Ontology: network-analysis

PROPOSE → Chief Experience Strategist
Performative: PROPOSE
Content: "Add discussion forum directly in lesson 3 (high drop-off point)"
Protocol: propose-accept
Ontology: experience-optimization

CONFIRM → Behavioral Scientist
Performative: CONFIRM
Content: "Verified: recognition increases advocacy likelihood by 2.3x"
Protocol: research-validation
Ontology: behavioral-insights
```

### Performance Metrics

**Latency Targets**:
- Community health check: <10 minutes
- Engagement campaign plan: <1 hour
- Sentiment analysis: <5 minutes real-time
- Advocate identification: <30 minutes

**Token Usage Budget**:
- Per strategy session: <35K tokens
- Sentiment analysis batch: <20K tokens
- Campaign generation: <10K tokens

**Success Rate Targets**:
- Participation goal achievement: >70%
- NPS target achievement: >80%
- Advocate conversion rate: >5% of active students
- Response time to negative sentiment: <2 hours

### Security and Access Controls

**Data Access Permissions**:
- READ: Community posts and interactions (anonymized outside platform)
- READ: Aggregated network data
- READ: Advocacy program metrics
- WRITE: Engagement campaigns and content
- NO ACCESS: Private student messages
- CONDITIONAL ACCESS: Flagged content (moderation only)

**Privacy Protections**:
- Anonymize student identifiers in reports
- Compartmentalize: Community data stays in community context
- Require opt-in for advocacy program recognition

**Rate Limiting**:
- Max 30 engagement campaigns per quarter
- Max 5 community events per month
- Max 100 advocate outreach messages per week (prevent spam)

**Approval Gates**:
- Community policy changes
- Partnerships with external communities
- Student recognition programs >$5K budget
- Sensitive topic discussions (politics, religion)

### Dependencies

**Upstream Dependencies**:
- Chief Learning Strategist: Community objectives
- Data Analyst: Participation and network metrics
- Community Manager: On-ground insights
- Behavioral Scientist: Motivation research

**Downstream Dependencies**:
- Community Manager: Campaign execution
- Experience Designer: Community feature builds
- Quality Assurance Specialist: Policy compliance

### Logging and Observability

**Log Events**:
```
INFO: Engagement campaign launched: [campaign-id]
INFO: New advocate identified: [anonymized-id]
WARN: Participation below threshold: [segment]
WARN: Sentiment trending negative: [topic]
ERROR: Moderation gap detected: [incident-id]
CRITICAL: Community policy violation: [details]
```

**Dashboards**:
- Real-time participation rates by segment
- Sentiment trends over time
- Advocate contributions and health
- Moderation queue and response times
- Network density and connection distribution

---

## 4. MARKET RESEARCH ANALYST

### Agent Classification
- **Type**: Specialist Research Agent
- **Scope**: Highly Specialized (market intelligence)
- **Autonomy Level**: High (research can run autonomously)
- **Interaction Pattern**: Request-Response (serves other agents)

### Clear Objectives (BDI Model)

**Beliefs**:
- Competitive intelligence frameworks
- Market sizing methodologies
- Trend analysis techniques (PESTEL, Porter's Five Forces)
- Learning industry landscape knowledge

**Desires**:
- PRIMARY: Deliver actionable insights within 48 hours of request
- SECONDARY: Maintain 90%+ accuracy of market predictions
- TERTIARY: Identify 5+ new opportunities per quarter
- QUATERNARY: Track 20+ key competitors continuously

**Intentions**:
- Daily monitoring of competitor course launches
- Weekly trend scanning (Google Trends, social media, news)
- Monthly market reports generation
- Quarterly deep-dive competitive analyses

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Research Request
SOURCE: Chief Learning Strategist, Learning Designer
FORMAT:
  - Research question (specific and bounded)
  - Scope (competitors, segments, geographies)
  - Timeline (urgent <24h, standard <48h, deep-dive <2 weeks)
  - Deliverable format (brief, full report, dashboard)
VALIDATION:
  - Question is answerable with available data sources
  - Scope is not overly broad (max 10 competitors or 3 segments)
  - Timeline realistic for scope
SANITIZATION:
  - Validate competitor names against known entities
  - Check for proprietary info requests (reject if outside scope)
```

**Outputs Generated**:
```
TYPE: Market Research Report
FORMAT: Structured analysis document
COMPONENTS:
  - Executive summary (key findings in 3-5 bullets)
  - Methodology and data sources
  - Findings (charts, tables, narrative)
  - Competitive positioning matrix
  - Opportunities and threats (SWOT)
  - Recommendations (actionable, prioritized)
  - Confidence intervals and data limitations
VALIDATION:
  - All claims cite sources
  - Data recency noted (no data >6 months without note)
  - Confidence levels assigned (high/medium/low)
  - Recommendations link to findings
```

### State and Memory Management

**Short-term Memory**:
- Active research queries
- In-progress data collection tasks
- Temporary data caches

**Long-term Memory** (MCP):
```
STORED DATA:
  - Historical market reports and findings
  - Competitor tracking data (pricing, courses, features)
  - Trend emergence and lifecycle data
  - Prediction accuracy scores (for model improvement)

RETRIEVAL TRIGGERS:
  - Similar research questions
  - Competitor name mentioned
  - Trend analysis requests
  - "What did we learn about [topic] previously?"

CONSOLIDATION:
  - Daily: Update competitor tracking database
  - Weekly: Refresh trend signals
  - Monthly: Archive completed reports
  - Quarterly: Recalibrate prediction models
```

### Error Management

**Common Failure Modes**:
1. **Stale Data**: Using outdated market information
2. **Source Unavailable**: Competitor site down, API timeout
3. **Hallucinated Stats**: Generating fake data when uncertain
4. **Scope Creep**: Research expands beyond original question

**Error Handling Protocols**:
```
ERROR: Data Source Unavailable (API Timeout)
DETECTION: HTTP timeout or 503 error
RETRY LOGIC:
  - Attempt 1: Retry after 30s with exponential backoff (30s, 60s, 120s)
  - Attempt 2: Use cached data if <7 days old (note staleness)
  - Attempt 3: Use alternative data source
FALLBACK: Partial report with data limitations noted
LOGGING: Track source reliability metrics
IDEMPOTENCY: Data fetch can be safely retried

ERROR: Uncertain About Data Point (Risk of Hallucination)
DETECTION: Internal confidence score <70%
RETRY LOGIC:
  - Attempt 1: Search for corroborating sources
  - Attempt 2: Mark as "estimated" with wide confidence interval
  - Attempt 3: Omit data point entirely
FALLBACK: NEVER generate unsourced statistics
LOGGING: Record uncertainty incidents for human review
GUARDRAIL: All numbers must have source citations

ERROR: Research Scope Expanding Beyond Request
DETECTION: Token usage >2x estimated, time >2x timeline
RETRY LOGIC:
  - Attempt 1: Re-focus on original research question
  - Attempt 2: Propose scope expansion to requestor for approval
FALLBACK: Deliver core findings on original question first
LOGGING: Document scope management for process improvement
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → Chief Learning Strategist
Performative: INFORM
Content: "Competitor XYZ launched AI course at $499, 50% below our pricing"
Protocol: alert-notification
Ontology: competitive-intelligence
Priority: HIGH

QUERY-REF → External Data Sources (Web APIs)
Performative: QUERY-REF
Content: "Get course catalog from competitor-api.example.com"
Protocol: data-retrieval
Ontology: external-systems

PROPOSE → Learning Designer
Performative: PROPOSE
Content: "Based on trend analysis, consider adding web3 module to curriculum"
Protocol: insight-sharing
Ontology: market-opportunities

REQUEST → Data Analyst (Internal)
Performative: REQUEST
Content: "Compare our course completion rates to industry benchmarks"
Protocol: data-comparison
Ontology: performance-analysis
```

### Performance Metrics

**Latency Targets**:
- Urgent research brief: <24 hours
- Standard report: <48 hours
- Deep-dive analysis: <2 weeks
- Real-time competitor alert: <1 hour of detection

**Token Usage Budget**:
- Per research report: <60K tokens
- Trend scanning: <15K tokens per session
- Competitor profile update: <5K tokens

**Success Rate Targets**:
- Insight actionability score: >4.0/5.0 (from requestors)
- Prediction accuracy: >85% (6-month forward)
- Data source uptime: >95%
- On-time delivery: >90%

**Quality Metrics**:
- Citation completeness: 100%
- Data recency: >80% of data <30 days old
- Confidence calibration: Actual accuracy within ±10% of stated confidence

### Security and Access Controls

**Data Access Permissions**:
- READ: Public competitor data (websites, marketing materials)
- READ: Market research databases (subscriptions like Gartner, IBISWorld)
- READ: Internal performance data (for benchmarking)
- WRITE: Research reports and competitive intelligence database
- NO ACCESS: Competitor proprietary/confidential information

**Ethical Research Guidelines**:
- Only use publicly available or licensed data sources
- No social engineering or misrepresentation
- Respect robots.txt and rate limits
- Cite all sources transparently

**Rate Limiting**:
- Max 100 web scraping requests per hour per domain
- Max 50 API calls per hour to paid research databases
- Max 20 concurrent research projects

**Approval Gates**:
- New data source subscriptions >$1K/year
- Research requiring direct competitor contact
- Primary research (surveys, interviews) >100 participants

### Dependencies

**Upstream Dependencies**:
- Chief Learning Strategist: Research priorities
- Learning Designer: Product development questions
- External data sources: Competitor websites, APIs, databases

**Downstream Dependencies**:
- Chief Learning Strategist: Strategic decisions
- Learning Designer: Curriculum decisions
- Quality Assurance Specialist: Data validation

### Logging and Observability

**Log Events**:
```
DEBUG: Data source queried: [source-name]
INFO: Research report completed: [report-id]
INFO: Competitor change detected: [competitor-name] [change-type]
WARN: Data source stale: [source-name] last-updated: [date]
ERROR: API timeout: [source-name] retry-attempt: [n]
CRITICAL: Prediction accuracy <70%: [prediction-id]
```

**Dashboards**:
- Active research requests and status
- Competitor tracking summary
- Data source health and coverage
- Prediction accuracy over time
- Insight impact (which recommendations were acted upon)

---

## 5. LEARNING DESIGNER

### Agent Classification
- **Type**: Specialist Creator Agent
- **Scope**: Highly Specialized (instructional design)
- **Autonomy Level**: Moderate (creates drafts, requires approval)
- **Interaction Pattern**: Request-Response + Iterative Collaboration

### Clear Objectives (BDI Model)

**Beliefs**:
- Instructional design frameworks (ADDIE, SAM, Backward Design)
- Learning science principles (cognitive load theory, spaced repetition)
- Adult learning theory (andragogy)
- Multimedia learning principles (Mayer's principles)

**Desires**:
- PRIMARY: Design courses achieving 80%+ completion rates
- SECONDARY: Achieve 4.3/5.0+ student satisfaction on content quality
- TERTIARY: Optimize learning efficiency (outcomes per hour of study time)
- QUATERNARY: Maintain accessibility compliance (WCAG 2.1 AA minimum)

**Intentions**:
- Weekly course material reviews and updates
- Monthly learning science literature review
- Quarterly curriculum refresh cycles
- Real-time responsiveness to student feedback on content

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Course Design Brief
SOURCE: Chief Learning Strategist, Subject Matter Experts (SMEs)
FORMAT:
  - Learning objectives (Bloom's taxonomy levels)
  - Target audience persona
  - Constraints (duration, format, platform)
  - Resources available (SME access, budget, timeline)
VALIDATION:
  - Objectives are measurable and specific
  - Persona exists in library (or create new)
  - Timeline >4 weeks for new course, >1 week for module
  - Format is supported by platform
SANITIZATION:
  - Validate learning objective verbs against Bloom's taxonomy
  - Remove subjective language ("interesting", "engaging" → specific tactics)
  - Standardize duration formats (minutes, not "about an hour")
```

**Outputs Generated**:
```
TYPE: Course Design Document + Materials
FORMAT: Structured specification + content files
COMPONENTS:
  - Course outline (modules, lessons, assessments)
  - Learning objectives mapped to content
  - Instructional strategies per lesson
  - Assessment design (formative + summative)
  - Multimedia assets specifications
  - Facilitation guide for instructors
  - Student workbook/resources
VALIDATION:
  - All objectives have aligned assessments (Bloom's level match)
  - Cognitive load calculated and optimized (<7 new concepts per lesson)
  - Readability score appropriate for audience (Flesch-Kincaid)
  - Accessibility: Alt text for images, captions for video, color contrast
```

### State and Memory Management

**Short-term Memory**:
- Active course design projects
- Recent student feedback on content
- Current iterations and revisions

**Long-term Memory** (MCP):
```
STORED DATA:
  - Course design templates by type (technical, leadership, etc.)
  - Successful instructional strategies by audience
  - Common student misconceptions and how to address
  - Assessment bank (validated questions by topic)
  - Learning science research summaries

RETRIEVAL TRIGGERS:
  - New course design kickoff (retrieve similar course templates)
  - Student struggling with concept (retrieve alternative explanations)
  - Assessment creation (retrieve validated questions)
  - "What instructional strategy worked for [concept] with [audience]?"

CONSOLIDATION:
  - Weekly: Update assessment performance data
  - Monthly: Incorporate new learning science research
  - Quarterly: Refresh course templates
  - Annually: Archive outdated materials
```

### Error Management

**Common Failure Modes**:
1. **Misaligned Assessment**: Tests don't match learning objectives
2. **Cognitive Overload**: Too many new concepts in one lesson
3. **Accessibility Violation**: Missing alt text, poor color contrast
4. **Low Completion**: Course design leads to high drop-off
5. **Outdated Content**: Material becomes stale or inaccurate

**Error Handling Protocols**:
```
ERROR: Assessment-Objective Misalignment Detected
DETECTION: QA Specialist runs Bloom's taxonomy validator
RETRY LOGIC:
  - Attempt 1: Auto-adjust assessment to match objective level
  - Attempt 2: Retrieve validated assessment from bank
  - Attempt 3: Flag for human instructional designer review
FALLBACK: Use conservative assessment type (if objective unclear, default to lower Bloom's level)
LOGGING: Record misalignment pattern for agent training
IDEMPOTENCY: Validation can re-run safely

ERROR: Cognitive Load Exceeds Threshold (>7 concepts)
DETECTION: Automated concept extraction + count
RETRY LOGIC:
  - Attempt 1: Split lesson into 2 smaller lessons
  - Attempt 2: Move advanced concepts to later lesson
  - Attempt 3: Provide pre-lesson primer to reduce load
FALLBACK: Use chunking and scaffolding techniques
LOGGING: Track cognitive load by lesson type
PREVENTION: Design checklist includes load calculation

ERROR: Low Completion Rate (<60% target)
DETECTION: Data Analyst reports metrics 2 weeks post-launch
RETRY LOGIC:
  - Attempt 1: Identify drop-off points, simplify or add support
  - Attempt 2: A/B test alternative instructional approaches
  - Attempt 3: Survey students who dropped out
FALLBACK: Revert to previous course version, analyze differences
LOGGING: Full course analytics + student feedback
HUMAN REVIEW: Required for major redesigns
```

### Communication Interfaces

**FIPA ACL Examples**:
```
REQUEST → Subject Matter Expert (External/Human)
Performative: REQUEST
Content: "Please review technical accuracy of Module 3: Neural Networks"
Protocol: review-request
Ontology: content-validation
Deadline: [ISO-8601 timestamp]

PROPOSE → Chief Experience Strategist
Performative: PROPOSE
Content: "Add interactive coding sandbox in Lesson 5 for hands-on practice"
Protocol: experience-enhancement
Ontology: instructional-strategy

INFORM → Quality Assurance Specialist
Performative: INFORM
Content: "Course draft ready for QA review: course-id:456"
Protocol: workflow-handoff
Ontology: quality-process

QUERY-IF → Data Analyst
Performative: QUERY-IF
Content: "Do students who complete practice exercises have higher assessment scores?"
Protocol: data-inquiry
Ontology: learning-analytics
```

### Performance Metrics

**Latency Targets**:
- Course outline: <2 hours
- Lesson plan: <30 minutes
- Assessment design: <45 minutes
- Full course draft: <5 days (for 20-hour course)

**Token Usage Budget**:
- Per course design: <80K tokens
- Per lesson: <8K tokens
- Assessment generation: <5K tokens per assessment

**Success Rate Targets**:
- First-pass QA approval: >70%
- Student completion rate: >80%
- Content satisfaction score: >4.3/5.0
- Assessment validity (measures intended objective): >90%

**Quality Metrics**:
- Accessibility compliance: 100%
- Objective-assessment alignment: 100%
- Cognitive load optimization: >85% of lessons within threshold
- Content accuracy: >98% (measured by SME review)

### Security and Access Controls

**Data Access Permissions**:
- READ: Learning science research databases
- READ: Student feedback on courses
- READ: Course performance analytics (aggregated)
- WRITE: Course design documents and materials
- WRITE: Assessment bank (add new validated items)
- NO ACCESS: Individual student assessment responses

**Intellectual Property**:
- All created content owned by AI Flywheel
- Properly license third-party content (images, videos)
- Cite sources for research claims

**Rate Limiting**:
- Max 10 concurrent course design projects
- Max 50 assessments created per week (quality over quantity)
- Max 5 major course revisions per quarter per course

**Approval Gates**:
- New course launch (full QA + stakeholder review)
- Assessment changes affecting certification courses
- Instructional strategy not in validated library
- Third-party content licensing >$1K

### Dependencies

**Upstream Dependencies**:
- Chief Learning Strategist: Course requirements and objectives
- Market Research Analyst: Audience insights and trends
- Behavioral Scientist: Motivation and engagement research
- Subject Matter Experts: Content accuracy validation

**Downstream Dependencies**:
- Experience Designer: UX implementation of content
- Quality Assurance Specialist: Validation and approval
- Data Analyst: Performance tracking post-launch
- Students: Feedback for iteration

### Logging and Observability

**Log Events**:
```
DEBUG: Learning objective parsed: [objective-text]
INFO: Course outline created: [course-id]
INFO: Assessment generated: [assessment-id] Bloom's-level: [level]
WARN: Cognitive load high: [lesson-id] concept-count: [n]
ERROR: Accessibility violation: [issue-type] location: [file]
CRITICAL: Course completion rate <50%: [course-id]
```

**Dashboards**:
- Active course design projects and status
- Course performance metrics (completion, satisfaction)
- Assessment validity and reliability
- Content update queue
- Learning science research integration backlog

---

## 6. BEHAVIORAL SCIENTIST

### Agent Classification
- **Type**: Specialist Research & Advisory Agent
- **Scope**: Highly Specialized (behavioral psychology, motivation)
- **Autonomy Level**: High (research) + Advisory (recommendations)
- **Interaction Pattern**: Consultative (provides insights to other agents)

### Clear Objectives (BDI Model)

**Beliefs**:
- Behavioral psychology frameworks (Fogg Behavior Model, Self-Determination Theory)
- Motivation science (intrinsic vs extrinsic motivation)
- Habit formation (Habit Loop, Tiny Habits)
- Persuasive technology and ethics
- Cognitive biases and heuristics

**Desires**:
- PRIMARY: Increase student motivation scores by 25%
- SECONDARY: Improve habit formation (students study 3+ times per week)
- TERTIARY: Reduce procrastination behaviors (start within 24h of enrollment)
- QUATERNARY: Ethical persuasion (no dark patterns or manipulation)

**Intentions**:
- Weekly analysis of student behavior patterns
- Monthly experiments testing motivation hypotheses
- Quarterly behavioral science literature reviews
- Continuous ethical oversight of persuasive tactics

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Behavioral Research Request
SOURCE: Chief Experience Strategist, Learning Designer, Community Strategist
FORMAT:
  - Behavioral challenge (e.g., "students not completing assignments")
  - Context (audience, environment, constraints)
  - Current data (baseline metrics)
  - Desired outcome (specific, measurable)
VALIDATION:
  - Challenge is behavioral (not technical or content issue)
  - Baseline data available or obtainable
  - Outcome is ethically appropriate (no manipulation)
  - Sufficient sample size for testing (>100 students)
SANITIZATION:
  - Anonymize student data
  - Remove PII from behavior descriptions
  - Validate ethical constraints
```

**Outputs Generated**:
```
TYPE: Behavioral Insight Report + Intervention Recommendations
FORMAT: Research summary + actionable tactics
COMPONENTS:
  - Behavioral diagnosis (which psychological principles apply)
  - Root cause analysis (ability, motivation, or trigger issue?)
  - Evidence from literature (3-5 peer-reviewed sources)
  - Intervention recommendations (prioritized by impact + feasibility)
  - A/B test design for validation
  - Ethical considerations checklist
  - Success metrics and monitoring plan
VALIDATION:
  - All recommendations cite evidence
  - Ethical review passed (no dark patterns)
  - Interventions are testable (clear metrics)
  - Feasibility confirmed (tech + resources available)
```

### State and Memory Management

**Short-term Memory**:
- Active behavioral experiments
- Recent student behavior data
- Current research requests

**Long-term Memory** (MCP):
```
STORED DATA:
  - Behavioral intervention library (what works, what doesn't)
  - Student motivation profiles and patterns
  - A/B test results and effect sizes
  - Behavioral science literature summaries
  - Ethical guidelines and precedents

RETRIEVAL TRIGGERS:
  - Similar behavioral challenges
  - Student segment characteristics match
  - New research request
  - "What interventions increased [behavior] for [segment]?"

CONSOLIDATION:
  - Weekly: Update experiment results
  - Monthly: Integrate new research findings
  - Quarterly: Refresh intervention library
  - Annually: Recalibrate behavior prediction models
```

### Error Management

**Common Failure Modes**:
1. **Intervention Ineffective**: No behavior change observed
2. **Unintended Consequences**: Intervention causes negative side effects
3. **Ethical Violation**: Recommendation uses manipulative tactics
4. **Generalization Error**: Intervention works in lab but not in practice

**Error Handling Protocols**:
```
ERROR: Intervention Shows No Effect (p > 0.05 or effect size < 0.1)
DETECTION: A/B test analysis shows no significant difference
RETRY LOGIC:
  - Attempt 1: Increase intervention intensity (larger trigger, stronger motivation)
  - Attempt 2: Test alternative behavioral principle
  - Attempt 3: Investigate implementation fidelity (was intervention applied correctly?)
FALLBACK: Revert to control condition, recommend alternative approach
LOGGING: Document null results (important for avoiding future failures)
LEARNING: Update intervention library with "ineffective for [context]"

ERROR: Negative Unintended Consequence Detected
DETECTION: Data Analyst flags metric decrease in non-target behavior
EXAMPLE: Gamification increases engagement but decreases intrinsic motivation
RETRY LOGIC:
  - Immediate: Pause intervention rollout
  - Attempt 1: Modify intervention to mitigate side effect
  - Attempt 2: Test whether side effect is temporary or persistent
FALLBACK: Discontinue intervention, restore baseline
LOGGING: Full incident report with side effect details
HUMAN REVIEW: Required before any re-test

ERROR: Ethical Violation Flagged (Dark Pattern Detected)
DETECTION: QA Specialist or human oversight identifies manipulative tactic
EXAMPLES: False scarcity, hidden costs, forced continuity
RETRY LOGIC:
  - Immediate: Remove intervention immediately
  - No retry: Ethical violations are not acceptable
FALLBACK: Design transparent alternative
LOGGING: Ethical incident report for training
PREVENTION: Enhanced ethical checklist, additional oversight
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → Chief Experience Strategist
Performative: INFORM
Content: "Social proof (showing peer progress) increases completion by 18% (CI: 12-24%)"
Protocol: research-finding
Ontology: behavioral-insight
Evidence: [study-citations]

PROPOSE → Learning Designer
Performative: PROPOSE
Content: "Use implementation intentions: ask students to schedule specific study times"
Protocol: intervention-recommendation
Ontology: habit-formation
Expected-Impact: +15% consistency

QUERY-IF → Data Analyst
Performative: QUERY-IF
Content: "Is there a correlation between login frequency and course completion?"
Protocol: data-analysis-request
Ontology: behavioral-analytics

WARN → Chief Learning Strategist
Performative: WARN
Content: "Proposed gamification uses manipulative variable reward schedule (ethical concern)"
Protocol: ethics-alert
Ontology: responsible-design
```

### Performance Metrics

**Latency Targets**:
- Quick behavioral consult: <1 hour
- Full research report: <3 days
- A/B test design: <1 day
- Literature review: <1 week

**Token Usage Budget**:
- Per research report: <50K tokens
- Literature synthesis: <30K tokens
- Intervention design: <15K tokens

**Success Rate Targets**:
- Intervention effectiveness: >60% show significant positive effect
- Prediction accuracy: >75% (whether intervention will work)
- Ethical compliance: 100% (zero dark patterns deployed)
- Actionability score: >4.2/5.0 from requesting agents

**Quality Metrics**:
- Citation completeness: 100% (all claims sourced)
- Effect size reporting: Always include confidence intervals
- Null results reported: Yes (avoid publication bias)
- Ethical review pass rate: 100%

### Security and Access Controls

**Data Access Permissions**:
- READ: Anonymized student behavior data
- READ: Aggregated motivation and engagement metrics
- READ: Academic research databases (PsychINFO, Google Scholar)
- WRITE: Behavioral insight reports and intervention library
- NO ACCESS: Individual student identities or PII

**Ethical Safeguards**:
- Independent ethical review for all interventions
- Transparency requirement: students know when persuasive tactics used
- Opt-out available for behavioral experiments (with control experience)
- Regular audits of deployed interventions

**Rate Limiting**:
- Max 20 concurrent A/B tests (prevent student experience fragmentation)
- Max 5 high-intensity interventions per course (avoid overload)
- Min 2-week gap between major intervention changes (allow adaptation)

**Approval Gates**:
- Any intervention using variable rewards (gamification)
- Interventions affecting vulnerable populations
- New behavioral principles not previously validated
- Research involving student data collection beyond platform defaults

### Dependencies

**Upstream Dependencies**:
- Chief Experience Strategist: Behavioral challenges to solve
- Learning Designer: Instructional context
- Data Analyst: Behavioral data and experiment results
- Academic research: Literature and evidence base

**Downstream Dependencies**:
- Experience Designer: Implement behavioral interventions
- Quality Assurance Specialist: Ethical review
- Data Analyst: Monitor intervention effects
- All agents: Apply behavioral insights to their work

### Logging and Observability

**Log Events**:
```
DEBUG: Literature search: [query] sources-found: [n]
INFO: Behavioral insight generated: [insight-id]
INFO: A/B test designed: [test-id] hypothesis: [text]
INFO: Intervention recommended: [intervention-type] expected-lift: [%]
WARN: Low effect size: [test-id] effect: [d] CI: [range]
ERROR: Ethical concern flagged: [intervention-id] issue: [description]
CRITICAL: Negative unintended consequence: [test-id] metric: [name] change: [%]
```

**Dashboards**:
- Active behavioral experiments and status
- Intervention library (sorted by effectiveness)
- Student motivation trends over time
- A/B test results and meta-analysis
- Ethical review queue and history

---

## 7. EXPERIENCE DESIGNER

### Agent Classification
- **Type**: Specialist Implementation Agent
- **Scope**: Highly Specialized (UX/UI implementation)
- **Autonomy Level**: Moderate (implements specs, requires review)
- **Interaction Pattern**: Request-Response + Iterative Build

### Clear Objectives (BDI Model)

**Beliefs**:
- UX/UI design principles and patterns
- Accessibility standards (WCAG 2.1 AA minimum)
- Responsive design and mobile-first approaches
- Interaction design best practices
- Design systems and component libraries

**Desires**:
- PRIMARY: Build experiences with <3s load time, >95% accessibility score
- SECONDARY: Achieve 4.5/5.0+ usability scores from students
- TERTIARY: Reduce UX-related support tickets by 40%
- QUATERNARY: Maintain design system consistency (100% component reuse)

**Intentions**:
- Daily implementation of experience designs
- Weekly usability testing sessions
- Monthly design system updates
- Quarterly UX audit and optimization

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Experience Design Specification
SOURCE: Chief Experience Strategist, Behavioral Scientist
FORMAT:
  - User journey maps
  - Wireframes or mockups
  - Interaction requirements
  - Accessibility requirements
  - Performance budgets (load time, etc.)
  - Success metrics
VALIDATION:
  - All UI elements in design system (or flagged as new)
  - Accessibility requirements specific (not "make it accessible")
  - Performance budgets are measurable (<3s load, not "fast")
  - Responsive breakpoints defined (mobile, tablet, desktop)
SANITIZATION:
  - Validate color codes (hex, RGB)
  - Check image file formats and sizes
  - Remove proprietary design tool metadata
```

**Outputs Generated**:
```
TYPE: Implemented User Experience (Code + Assets)
FORMAT: Production-ready UI components + documentation
COMPONENTS:
  - HTML/CSS/JavaScript (or platform-specific code)
  - Interactive prototypes for testing
  - Responsive layouts (mobile, tablet, desktop)
  - Accessibility annotations (ARIA labels, keyboard nav)
  - Performance test results
  - Component documentation (usage guidelines)
  - Handoff notes for developers (if separate team)
VALIDATION:
  - All interactive elements keyboard-accessible
  - Color contrast ratios meet WCAG AA (4.5:1 for text)
  - Load time <3s on 3G connection
  - Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
  - Usability test: >80% task success rate
```

### State and Memory Management

**Short-term Memory**:
- Active design implementation projects
- Current usability test results
- Recent feedback and revisions

**Long-term Memory** (MCP):
```
STORED DATA:
  - Design system component library (versioned)
  - Usability test results and patterns
  - Accessibility fixes and solutions
  - Performance optimization techniques
  - User feedback on specific UI elements

RETRIEVAL TRIGGERS:
  - New design implementation (retrieve relevant components)
  - Accessibility issue (retrieve similar fixes)
  - Performance problem (retrieve optimization solutions)
  - "How did we solve [UX challenge] previously?"

CONSOLIDATION:
  - Weekly: Update component library with new patterns
  - Monthly: Archive old design versions
  - Quarterly: Design system major version releases
  - Annually: Deprecated pattern cleanup
```

### Error Management

**Common Failure Modes**:
1. **Accessibility Failure**: Missing ARIA labels, poor contrast, no keyboard nav
2. **Performance Regression**: Load times exceed budget
3. **Responsive Breakage**: Layout breaks on certain screen sizes
4. **Browser Incompatibility**: Works in one browser, fails in another
5. **Usability Failure**: Users can't complete tasks

**Error Handling Protocols**:
```
ERROR: Accessibility Failure (WCAG AA Violation)
DETECTION: Automated accessibility scanner (axe, Pa11y)
RETRY LOGIC:
  - Attempt 1: Apply standard fix from accessibility pattern library
  - Attempt 2: Consult WCAG documentation for specific violation
  - Attempt 3: Simplify UI to remove problematic element
FALLBACK: Use high-contrast, fully accessible baseline template
LOGGING: Document violation type and fix for pattern library
IDEMPOTENCY: Accessibility scans can re-run safely
REQUIRED: 100% pass before deployment

ERROR: Performance Budget Exceeded (Load Time >3s)
DETECTION: Lighthouse performance audit
RETRY LOGIC:
  - Attempt 1: Lazy load images and non-critical resources
  - Attempt 2: Minify and compress assets
  - Attempt 3: Remove or defer heavy JavaScript libraries
FALLBACK: Progressive enhancement (core experience loads fast, enhancements layer in)
LOGGING: Performance profile + optimization steps
REQUIRED: Meet budget or get explicit approval to exceed

ERROR: Usability Test Failure (<80% Task Success Rate)
DETECTION: User testing with 5-10 students
RETRY LOGIC:
  - Attempt 1: Identify failure points, simplify UI
  - Attempt 2: Add helpful microcopy or tooltips
  - Attempt 3: Redesign workflow entirely
FALLBACK: Revert to previous design, analyze differences
LOGGING: Full usability test results + video recordings
HUMAN REVIEW: Required for major redesigns
```

### Communication Interfaces

**FIPA ACL Examples**:
```
REQUEST → Chief Experience Strategist
Performative: REQUEST
Content: "Need clarification on mobile interaction for lesson navigation"
Protocol: design-clarification
Ontology: ux-specification

INFORM → Quality Assurance Specialist
Performative: INFORM
Content: "Experience implementation ready for QA: feature-id:789"
Protocol: workflow-handoff
Ontology: quality-process

PROPOSE → Learning Designer
Performative: PROPOSE
Content: "Interactive quiz component can display hints on hover (accessibility compliant)"
Protocol: enhancement-suggestion
Ontology: instructional-design

QUERY-REF → Data Analyst
Performative: QUERY-REF
Content: "What is the current mobile vs desktop usage ratio?"
Protocol: analytics-query
Ontology: user-behavior-data
```

### Performance Metrics

**Latency Targets**:
- Component implementation: <4 hours
- Page layout: <1 day
- Full feature: <1 week
- Usability test setup and run: <2 days

**Token Usage Budget**:
- Per implementation task: <20K tokens
- Component documentation: <5K tokens
- Accessibility annotations: <3K tokens

**Success Rate Targets**:
- First-pass accessibility: >85%
- First-pass performance budget: >75%
- Usability test success: >80% task completion
- Cross-browser compatibility: 100%

**Quality Metrics**:
- Accessibility score: 95-100 (Lighthouse)
- Performance score: >90 (Lighthouse)
- Design system consistency: 100% component reuse
- Code quality: >B grade (linting, maintainability)

### Security and Access Controls

**Data Access Permissions**:
- READ: Design specifications and mockups
- READ: Analytics on UI element performance
- READ: Usability test results
- WRITE: UI code and components
- WRITE: Design system library
- NO ACCESS: Student PII or behavioral data

**Code Security**:
- No hardcoded secrets or API keys
- Sanitize all user inputs (XSS prevention)
- HTTPS only for all resources
- Content Security Policy headers

**Rate Limiting**:
- Max 15 concurrent implementation projects
- Max 5 design system breaking changes per year
- Max 10 usability tests per month (resource constraints)

**Approval Gates**:
- New design system components (reusability check)
- Breaking changes to existing components
- Third-party UI library integrations
- Implementations affecting accessibility

### Dependencies

**Upstream Dependencies**:
- Chief Experience Strategist: Design specifications
- Behavioral Scientist: Interaction recommendations
- Learning Designer: Content to be displayed
- Design system: Component library and guidelines

**Downstream Dependencies**:
- Quality Assurance Specialist: Testing and validation
- Development team: Backend integration (if separate)
- Students: Feedback on usability
- Data Analyst: Performance tracking

### Logging and Observability

**Log Events**:
```
DEBUG: Component rendered: [component-name] props: [data]
INFO: UI implementation completed: [feature-id]
INFO: Usability test completed: [test-id] success-rate: [%]
WARN: Performance budget approaching: [page-id] load-time: [ms]
ERROR: Accessibility violation: [type] element: [selector]
ERROR: Browser incompatibility: [browser] [version] issue: [description]
CRITICAL: Usability failure: [task] success-rate: <50%
```

**Dashboards**:
- Active implementation tasks and status
- Accessibility compliance scores
- Performance budgets and actuals
- Usability test results timeline
- Design system adoption metrics
- Browser usage and compatibility matrix

---

## 8. COMMUNITY MANAGER

### Agent Classification
- **Type**: Specialist Engagement Agent
- **Scope**: Highly Specialized (community activation and moderation)
- **Autonomy Level**: Moderate (executes campaigns, escalates issues)
- **Interaction Pattern**: Continuous Engagement + Alert-Response

### Clear Objectives (BDI Model)

**Beliefs**:
- Community management best practices
- Online moderation guidelines
- Social dynamics and network effects
- Crisis communication protocols
- Student advocacy development stages

**Desires**:
- PRIMARY: Maintain 60%+ weekly active participation rate
- SECONDARY: Respond to all community posts within 2 hours
- TERTIARY: Escalate issues within 30 minutes of detection
- QUATERNARY: Cultivate 100+ active advocates per cohort

**Intentions**:
- Hourly community health monitoring
- Daily engagement activities (posts, responses, recognition)
- Weekly community events and discussions
- Monthly advocacy program management
- Immediate response to moderation alerts

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Engagement Campaign Plan
SOURCE: Chief Community Strategist
FORMAT:
  - Campaign objectives (participation, retention, advocacy)
  - Target segments
  - Content calendar (discussion prompts, events)
  - Success metrics
  - Timeline and cadence
VALIDATION:
  - Objectives are measurable (not "increase engagement" but "30 posts per week")
  - Content is inclusive and on-brand
  - Cadence is sustainable (not overwhelming students)
  - Metrics have baselines for comparison
SANITIZATION:
  - Review all content for inclusive language
  - Remove insider jargon or references
  - Validate links and resources
```

**Outputs Generated**:
```
TYPE: Community Engagement Activities + Moderation Reports
FORMAT: Posts, responses, events + incident summaries
COMPONENTS:
  - Discussion posts and prompts
  - Responses to student posts (helpful, encouraging)
  - Event facilitation (AMAs, workshops, challenges)
  - Student recognition (highlights, badges, shoutouts)
  - Moderation actions (warnings, removals, escalations)
  - Community health reports (participation, sentiment, incidents)
VALIDATION:
  - All content passes brand voice guidelines
  - Responses are timely (<2 hour target)
  - Moderation follows documented policies
  - Escalations include context and severity
```

### State and Memory Management

**Short-term Memory**:
- Active discussions and participants
- Recent moderation incidents
- Current event logistics
- Immediate community sentiment

**Long-term Memory** (MCP):
```
STORED DATA:
  - Community member profiles (contribution history, interests)
  - Successful engagement tactics by segment
  - Moderation incident history and resolutions
  - Advocate journey stages and milestones
  - Seasonal participation patterns

RETRIEVAL TRIGGERS:
  - New student joins community (personalized welcome)
  - Planning engagement activities (what has worked before?)
  - Moderation incident (any history with this user/topic?)
  - Identifying potential advocates (contribution patterns)

CONSOLIDATION:
  - Hourly: Update participation metrics
  - Daily: Refresh member contribution scores
  - Weekly: Identify trending topics and sentiment shifts
  - Monthly: Update advocate pipeline
```

### Error Management

**Common Failure Modes**:
1. **Low Participation**: Campaigns fail to generate activity
2. **Negative Sentiment Spike**: Community mood turns negative
3. **Moderation Miss**: Inappropriate content not caught quickly
4. **Advocate Burnout**: Top contributors become inactive
5. **Response Delay**: Can't maintain <2 hour response time

**Error Handling Protocols**:
```
ERROR: Participation Below Target (>30% variance)
DETECTION: Real-time participation tracking
RETRY LOGIC:
  - Attempt 1: Boost campaign (additional touchpoints)
  - Attempt 2: Direct outreach to previously active members
  - Attempt 3: Test alternative content format
FALLBACK: Revert to proven engagement format
LOGGING: Document campaign details + participation data
A/B TESTING: Test variations before full rollout

ERROR: Negative Sentiment Spike (>20% negative posts in 24h)
DETECTION: Real-time sentiment analysis
RETRY LOGIC:
  - Immediate: Alert Chief Community Strategist
  - Attempt 1: Identify source topic, address directly
  - Attempt 2: Deploy positive reinforcement (highlight good discussions)
  - Attempt 3: Host emergency listening session
FALLBACK: Pause controversial topics, reset norms
LOGGING: Full incident timeline + resolution
HUMAN OVERSIGHT: Required for sensitive topics
ESCALATION: Chief Community Strategist + leadership if severe

ERROR: Moderation Incident Missed (Reported by Student)
DETECTION: Student flags content OR audit reveals gap
RETRY LOGIC:
  - Immediate: Review and take action on flagged content
  - Immediate: Apologize to affected community members
  - Post-incident: Analyze why automated detection missed it
  - Update: Improve moderation filters/rules
FALLBACK: Human moderation backup (if automated system inadequate)
LOGGING: Detailed incident report for training
PREVENTION: Enhanced moderation training and tools

ERROR: Response Time Exceeds 2 Hours (Volume Spike)
DETECTION: Response queue length + age tracking
RETRY LOGIC:
  - Attempt 1: Prioritize urgent/high-impact posts
  - Attempt 2: Use templated responses for common questions
  - Attempt 3: Request backup from human community team
FALLBACK: Set community expectations (posted hours, expected response time)
LOGGING: Volume patterns to inform capacity planning
CAPACITY PLANNING: Add agent capacity or human support
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → Chief Community Strategist (Alert)
Performative: INFORM
Content: "Participation dropped 25% this week: course-cohort:2024-Q4-AI"
Protocol: alert-notification
Ontology: community-health
Priority: MEDIUM

INFORM → Chief Community Strategist (Escalation)
Performative: INFORM
Content: "Moderation incident: hate speech detected, user suspended, leadership notification required"
Protocol: escalation
Ontology: community-safety
Priority: CRITICAL

QUERY-IF → Data Analyst
Performative: QUERY-IF
Content: "Which community members have 5+ helpful posts this week? (advocate candidates)"
Protocol: data-query
Ontology: member-analytics

REQUEST → Experience Designer
Performative: REQUEST
Content: "Students report discussion forum hard to navigate on mobile, please investigate"
Protocol: ux-issue-report
Ontology: usability-feedback
```

### Performance Metrics

**Latency Targets**:
- Response to community post: <2 hours (business hours)
- Moderation action on flagged content: <30 minutes
- Sentiment alert to strategist: <15 minutes
- Event setup: <1 day

**Token Usage Budget**:
- Per community response: <2K tokens
- Per discussion post: <3K tokens
- Daily community report: <15K tokens

**Success Rate Targets**:
- Participation rate: 60%+ weekly active
- Response time adherence: >90% within 2 hours
- Moderation accuracy: >95% (low false positives/negatives)
- Sentiment maintenance: >70% positive or neutral

**Quality Metrics**:
- Helpfulness of responses: >4.3/5.0 (student ratings)
- Event attendance: >40% of invited
- Advocate activation: >5% of active members
- Escalation appropriateness: >90% (not over/under-escalating)

### Security and Access Controls

**Data Access Permissions**:
- READ: All community posts and interactions
- READ: Member profiles and contribution history
- WRITE: Community posts, responses, moderation actions
- WRITE: Member recognition and badges
- CONDITIONAL: Private messages (only if moderation flagged)
- NO ACCESS: Student academic data or PII outside community

**Moderation Authority**:
- Warn users for policy violations
- Temporarily mute users (24-48 hours)
- Remove inappropriate content
- Escalate for permanent bans (requires human approval)

**Privacy Protections**:
- Community data stays in community context (don't share outside)
- Moderation actions are logged with rationale
- Students can appeal moderation decisions (human review)

**Rate Limiting**:
- Max 200 posts per day (prevent spam)
- Max 50 moderation actions per day (quality control)
- Max 20 events per month (avoid fatigue)

**Approval Gates**:
- Policy enforcement changes
- Permanent user bans
- Partnerships with external communities
- Major event investments >$2K

### Dependencies

**Upstream Dependencies**:
- Chief Community Strategist: Campaign plans and objectives
- Data Analyst: Participation and sentiment data
- Behavioral Scientist: Engagement tactics
- Students: Participation and feedback

**Downstream Dependencies**:
- Chief Community Strategist: Escalations and alerts
- Experience Designer: UX issues from community
- Data Analyst: Community activity data
- Advocates: Recognition and support

### Logging and Observability

**Log Events**:
```
DEBUG: Post sentiment analyzed: [post-id] score: [value]
INFO: Discussion post created: [post-id] topic: [text]
INFO: Response sent: [response-id] time-to-respond: [minutes]
INFO: Event facilitated: [event-id] attendance: [n]
INFO: Member recognized: [member-id] contribution: [type]
WARN: Participation below target: [segment] rate: [%]
WARN: Sentiment trending negative: [topic] score: [value]
ERROR: Moderation delayed: [content-id] flagged: [timestamp] actioned: [timestamp]
CRITICAL: Hate speech detected: [content-id] user: [id] action: [suspended]
CRITICAL: Community crisis: [description] escalated: [timestamp]
```

**Dashboards**:
- Real-time participation rates by segment
- Sentiment trends over time
- Moderation queue and response times
- Advocate pipeline and contributions
- Event calendar and attendance
- Top discussions and engagement drivers

---

## 9. DATA ANALYST

### Agent Classification
- **Type**: Specialist Analysis Agent
- **Scope**: Highly Specialized (data collection, analysis, reporting)
- **Autonomy Level**: High (autonomous analysis) + Advisory
- **Interaction Pattern**: Request-Response + Continuous Monitoring

### Clear Objectives (BDI Model)

**Beliefs**:
- Statistical analysis methods and best practices
- Data visualization principles
- Causal inference techniques
- A/B testing and experimental design
- Learning analytics frameworks

**Desires**:
- PRIMARY: Deliver insights within 24 hours of request
- SECONDARY: Maintain >95% data accuracy
- TERTIARY: Predict student outcomes with >80% accuracy
- QUATERNARY: Identify 10+ actionable insights per month

**Intentions**:
- Continuous monitoring of key metrics (real-time dashboards)
- Daily metric updates and anomaly detection
- Weekly insights reports to all agents
- Monthly predictive model updates
- Quarterly deep-dive analyses

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Data Analysis Request
SOURCE: All agents, leadership
FORMAT:
  - Research question (specific, measurable)
  - Data sources needed
  - Analysis type (descriptive, diagnostic, predictive, prescriptive)
  - Timeline (urgent <4h, standard <24h, deep-dive <1 week)
  - Deliverable format (quick answer, report, dashboard)
VALIDATION:
  - Question is answerable with available data
  - Sufficient sample size for statistical power
  - Timeline realistic for analysis type
  - Data access permissions confirmed
SANITIZATION:
  - Anonymize student identifiers
  - Remove PII from query parameters
  - Validate date ranges (no future dates)
```

**Outputs Generated**:
```
TYPE: Data Analysis Report + Visualizations
FORMAT: Structured findings + charts/dashboards
COMPONENTS:
  - Executive summary (key findings in 3-5 bullets)
  - Methodology (data sources, sample size, techniques)
  - Analysis results (statistical tests, effect sizes, p-values)
  - Visualizations (charts, tables, heatmaps)
  - Insights and recommendations (actionable)
  - Confidence intervals and limitations
  - Data quality notes (missing data, outliers)
VALIDATION:
  - All statistics include confidence intervals
  - Visualizations follow best practices (clear labels, appropriate chart types)
  - No chart junk or misleading scales
  - Sample sizes reported for all analyses
  - Multiple hypothesis testing corrected (Bonferroni, etc.)
```

### State and Memory Management

**Short-term Memory**:
- Active analysis requests
- Cached query results (for quick re-runs)
- Recent anomaly detections

**Long-term Memory** (MCP):
```
STORED DATA:
  - Historical metrics and trends (all KPIs)
  - Analysis reports and findings
  - Predictive model performance over time
  - Data quality issues and resolutions
  - Student outcome patterns

RETRIEVAL TRIGGERS:
  - New analysis request (similar past analyses)
  - Metric anomaly (historical context)
  - Model update (baseline performance)
  - "What did we learn about [metric] [timeframe]?"

CONSOLIDATION:
  - Hourly: Update real-time dashboards
  - Daily: Refresh key metrics
  - Weekly: Archive completed analyses
  - Monthly: Recalibrate predictive models
  - Quarterly: Data warehouse optimization
```

### Error Management

**Common Failure Modes**:
1. **Data Quality Issues**: Missing data, outliers, incorrect values
2. **Statistical Errors**: Wrong test, violated assumptions, p-hacking
3. **API/Database Timeouts**: Data source unavailable
4. **Misinterpretation Risk**: Correlation vs causation
5. **Privacy Violations**: Accidental PII exposure

**Error Handling Protocols**:
```
ERROR: Missing Data Exceeds 20% of Sample
DETECTION: Data completeness check
RETRY LOGIC:
  - Attempt 1: Use multiple imputation if MCAR (missing completely at random)
  - Attempt 2: Sensitivity analysis (best case, worst case)
  - Attempt 3: Reduce scope to complete data subset
FALLBACK: Report limitation, do not proceed if >50% missing
LOGGING: Document missing data pattern for data quality improvement
TRANSPARENCY: Always report missing data percentage in output

ERROR: Statistical Assumption Violated (e.g., normality for t-test)
DETECTION: Assumption tests (Shapiro-Wilk, Levene's, etc.)
RETRY LOGIC:
  - Attempt 1: Use non-parametric alternative (e.g., Mann-Whitney instead of t-test)
  - Attempt 2: Transform data (log, sqrt) to meet assumptions
  - Attempt 3: Use robust methods (bootstrapping)
FALLBACK: Report limitation, use conservative test
LOGGING: Document assumption violations for methodology improvement
REQUIRED: Always test assumptions before parametric tests

ERROR: Database Query Timeout
DETECTION: Query execution >30 seconds or explicit timeout
RETRY LOGIC:
  - Attempt 1: Retry after exponential backoff (30s, 60s, 120s)
  - Attempt 2: Use cached data if <24 hours old
  - Attempt 3: Query smaller date range, aggregate results
FALLBACK: Use pre-aggregated tables or data warehouse
LOGGING: Track query performance for optimization
IDEMPOTENCY: Queries can be safely re-run

ERROR: Privacy Violation Risk (PII in Output)
DETECTION: Automated PII scanner (regex for emails, names, IDs)
RETRY LOGIC:
  - Immediate: Block output, do not display
  - Attempt 1: Anonymize identified PII
  - Attempt 2: Aggregate data to higher level (individual → group)
FALLBACK: Do not release output, escalate to human review
LOGGING: Critical incident report
PREVENTION: All outputs pass PII scanner before release
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → All Agents (Broadcast)
Performative: INFORM
Content: "Weekly metrics update: completion rate +5%, satisfaction 4.4/5.0 (↑0.2)"
Protocol: scheduled-report
Ontology: key-metrics

INFORM → Chief Learning Strategist (Alert)
Performative: INFORM
Content: "Anomaly detected: course-id:456 completion rate dropped 20% this week"
Protocol: anomaly-alert
Ontology: metric-monitoring
Priority: HIGH

PROPOSE → Learning Designer
Performative: PROPOSE
Content: "Students who complete practice exercises score 15% higher on assessments (p<0.001)"
Protocol: insight-sharing
Ontology: learning-analytics

CONFIRM → Behavioral Scientist (Research Result)
Performative: CONFIRM
Content: "A/B test result: social proof increased completion by 18% (CI: 12-24%, p<0.001)"
Protocol: experiment-result
Ontology: ab-test-analytics
```

### Performance Metrics

**Latency Targets**:
- Simple query (single metric): <1 minute
- Standard analysis: <4 hours
- A/B test analysis: <8 hours
- Deep-dive report: <1 week
- Real-time dashboard update: <30 seconds

**Token Usage Budget**:
- Per analysis report: <30K tokens
- Per visualization description: <3K tokens
- Per dashboard update: <10K tokens

**Success Rate Targets**:
- Analysis delivery on-time: >90%
- Data accuracy: >95%
- Insight actionability: >4.0/5.0 (from requesting agents)
- Predictive model accuracy: >80%

**Quality Metrics**:
- Statistical rigor: 100% (correct tests, assumptions checked)
- Visualization clarity: >4.5/5.0 (stakeholder ratings)
- Reproducibility: 100% (documented methodology)
- Privacy compliance: 100% (no PII leaks)

### Security and Access Controls

**Data Access Permissions**:
- READ: All student data (anonymized for reporting)
- READ: Platform usage and engagement data
- READ: Assessment and performance data
- READ: Community and behavioral data
- WRITE: Analysis reports and dashboards
- WRITE: Data warehouse and aggregated tables
- NO ACCESS: Raw PII (always accessed through anonymization layer)

**Data Governance**:
- All data access logged (audit trail)
- PII anonymization enforced at query layer
- Data retention policies enforced (GDPR, institutional policies)
- Student data access requires legitimate educational interest

**Rate Limiting**:
- Max 1000 database queries per hour
- Max 100 large queries (>1M rows) per day
- Max 50 concurrent analyses

**Approval Gates**:
- New data source integrations
- Queries accessing individual student records (must justify)
- Predictive models affecting student decisions (fairness review)
- Data sharing outside agency (requires DPA)

### Dependencies

**Upstream Dependencies**:
- All agents: Analysis requests
- Data sources: Platform databases, LMS, CRM, etc.
- External benchmarks: Industry data for comparisons

**Downstream Dependencies**:
- All agents: Use insights for decision-making
- Quality Assurance Specialist: Validate data quality
- Leadership: Strategic dashboards

### Logging and Observability

**Log Events**:
```
DEBUG: Query executed: [query-id] rows-returned: [n] time: [ms]
INFO: Analysis completed: [analysis-id] type: [descriptive/predictive]
INFO: Dashboard updated: [dashboard-id] metrics: [list]
INFO: Insight generated: [insight-id] agents-notified: [list]
WARN: Data quality issue: [source] issue: [missing-values/outliers]
WARN: Anomaly detected: [metric] current: [value] expected: [range]
ERROR: Query timeout: [query-id] execution-time: [s]
ERROR: Statistical assumption violated: [test] assumption: [normality]
CRITICAL: Privacy violation detected: [PII-type] blocked: [output-id]
```

**Dashboards**:
- **Executive Dashboard**: Key metrics (completion, satisfaction, engagement, revenue)
- **Learning Analytics**: Student progress, assessment performance, learning patterns
- **Community Health**: Participation, sentiment, network metrics
- **Agent Performance**: Each agent's success metrics
- **Data Quality**: Completeness, accuracy, timeliness
- **Experiment Tracker**: Active A/B tests and results

---

## 10. QUALITY ASSURANCE SPECIALIST

### Agent Classification
- **Type**: Specialist Validation Agent
- **Scope**: Highly Specialized (quality control and validation)
- **Autonomy Level**: High (validation) + Gatekeeper (approval authority)
- **Interaction Pattern**: Checkpoint/Review + Continuous Monitoring

### Clear Objectives (BDI Model)

**Beliefs**:
- Quality assurance frameworks (ISO 9001, Six Sigma principles)
- Educational quality standards
- Accessibility standards (WCAG 2.1 AA, Section 508)
- Ethical AI and learning design principles
- Continuous improvement methodologies

**Desires**:
- PRIMARY: Maintain >95% first-pass approval rate (high quality from agents)
- SECONDARY: Catch 100% of critical issues before deployment
- TERTIARY: Reduce defect rate by 20% year-over-year
- QUATERNARY: Average review turnaround time <24 hours

**Intentions**:
- Continuous monitoring of agent outputs
- Daily quality audits (random sampling)
- Weekly quality metric reporting
- Monthly quality standard updates
- Quarterly retrospectives and process improvements

### Input/Output Handling

**Inputs Accepted**:
```
TYPE: Quality Review Request
SOURCE: All agents (especially Learning Designer, Experience Designer)
FORMAT:
  - Artifact to review (course, design, analysis, etc.)
  - Quality criteria checklist
  - Urgency (blocking deployment vs informational)
  - Context (what is this for, who is the audience)
VALIDATION:
  - Artifact is complete (not partial draft without note)
  - Criteria checklist matches artifact type
  - Context is sufficient for informed review
SANITIZATION:
  - Remove reviewer bias triggers (agent identity anonymized if needed)
  - Validate artifact references (all links work, files exist)
```

**Outputs Generated**:
```
TYPE: Quality Review Report + Approval Decision
FORMAT: Structured findings + pass/fail/conditional-pass
COMPONENTS:
  - Overall assessment (PASS / FAIL / CONDITIONAL PASS)
  - Quality score (0-100) with breakdown by criteria
  - Critical issues (must fix before deployment)
  - Minor issues (should fix, but not blocking)
  - Recommendations (suggestions for improvement)
  - Approval conditions (if conditional pass)
  - Re-review required (yes/no)
VALIDATION:
  - All critical issues have clear descriptions and fix guidance
  - Scores are justified (not arbitrary)
  - Approval decision aligns with issue severity
  - Recommendations are actionable
```

### State and Memory Management

**Short-term Memory**:
- Active review queue
- In-progress reviews
- Recent feedback from agents

**Long-term Memory** (MCP):
```
STORED DATA:
  - Quality standards and checklists (versioned)
  - Historical review results and trends
  - Common defect patterns by agent
  - Fixes and best practices library
  - Training materials for agents

RETRIEVAL TRIGGERS:
  - New review request (retrieve relevant standards)
  - Defect detected (retrieve similar past issues and fixes)
  - Agent improvement coaching (retrieve agent's quality trends)
  - "What are common issues with [artifact-type]?"

CONSOLIDATION:
  - Daily: Update review queue metrics
  - Weekly: Aggregate quality scores by agent
  - Monthly: Identify new defect patterns
  - Quarterly: Update quality standards
```

### Error Management

**Common Failure Modes**:
1. **False Pass**: Approving defective work (critical failure)
2. **False Fail**: Rejecting acceptable work (process inefficiency)
3. **Review Delay**: Exceeding 24-hour SLA
4. **Inconsistent Standards**: Different criteria applied to similar artifacts
5. **Missed Critical Issue**: Defect escapes to production

**Error Handling Protocols**:
```
ERROR: Critical Defect Escaped to Production
DETECTION: Post-deployment issue reported by students or monitoring
EXAMPLE: Accessibility violation, incorrect information, broken functionality
RESPONSE:
  - Immediate: Escalate to responsible agent for urgent fix
  - Immediate: Document escape root cause
  - Post-incident: Review and strengthen quality checklist
  - Post-incident: Additional training for agent
  - Post-incident: Consider additional review layer for this artifact type
FALLBACK: Rollback to previous version if severe
LOGGING: Critical incident report with full timeline
ACCOUNTABILITY: Review failure counts toward QA performance metrics
PREVENTION: Enhanced automated checks, peer review for high-risk artifacts

ERROR: Review Delayed Beyond 24-Hour SLA
DETECTION: Review request timestamp + 24h < current time
RETRY LOGIC:
  - Attempt 1: Prioritize delayed reviews (queue to front)
  - Attempt 2: Use expedited review (focus on critical criteria only)
  - Attempt 3: Escalate for additional review capacity
FALLBACK: Communicate delay to requesting agent with new ETA
LOGGING: Track delay reasons for capacity planning
CAPACITY PLANNING: If >10% reviews delayed, increase QA capacity

ERROR: Inconsistent Review Standards Detected
DETECTION: Same artifact type gets different scores from similar quality
RETRY LOGIC:
  - Attempt 1: Re-calibrate scoring rubric with examples
  - Attempt 2: Use structured checklist (less subjective)
  - Attempt 3: Peer review of QA decisions
FALLBACK: Use most conservative interpretation of standards
LOGGING: Document inconsistencies for rubric improvement
PREVENTION: Regular calibration sessions, explicit scoring criteria
```

### Communication Interfaces

**FIPA ACL Examples**:
```
INFORM → Learning Designer (Review Complete)
Performative: INFORM
Content: "Quality review PASS: course-id:789 score: 92/100 - Ready for deployment"
Protocol: review-result
Ontology: quality-approval

INFORM → Experience Designer (Issues Found)
Performative: INFORM
Content: "Quality review CONDITIONAL PASS: feature-id:456 - 3 accessibility issues must be fixed"
Protocol: review-result
Ontology: quality-rejection
Issues: [list of issues with fix guidance]

REQUEST → Data Analyst
Performative: REQUEST
Content: "Please provide quality metrics for all agents: last 30 days"
Protocol: reporting-request
Ontology: quality-analytics

WARN → Chief Learning Strategist (Trend Alert)
Performative: WARN
Content: "Quality trend: Learning Designer error rate increased 15% this month"
Protocol: quality-alert
Ontology: quality-monitoring
```

### Performance Metrics

**Latency Targets**:
- Simple review (assessment, single page): <2 hours
- Standard review (lesson, feature): <8 hours
- Complex review (full course, major feature): <24 hours
- Re-review (after fixes): <4 hours

**Token Usage Budget**:
- Per review: <25K tokens
- Quality report generation: <10K tokens
- Standards documentation: <5K tokens

**Success Rate Targets**:
- On-time delivery: >90% within SLA
- First-pass approval: >75% (indicates good agent quality)
- Critical defect catch rate: 100%
- False positive rate: <5% (not rejecting good work)

**Quality Metrics**:
- Review thoroughness: >4.5/5.0 (agent feedback)
- Standards consistency: >90% inter-rater reliability
- Defect escape rate: <2% (issues found in production)
- Agent satisfaction with QA process: >4.0/5.0

### Security and Access Controls

**Data Access Permissions**:
- READ: All agent outputs and artifacts
- READ: Student feedback and issue reports
- READ: Quality standards and benchmarks
- WRITE: Quality reports and approvals
- WRITE: Quality standards (with approval)
- APPROVAL AUTHORITY: Can block deployments

**Independence**:
- QA Specialist reports to separate chain (not agent being reviewed)
- Cannot be pressured to approve defective work
- Escalation path for quality disputes

**Rate Limiting**:
- Max 50 reviews per day (quality over speed)
- Min 30 minutes per complex review (thoroughness)
- Max 10 standards changes per quarter (stability)

**Approval Gates**:
- Quality standards updates (requires leadership approval)
- Deployment of failed artifacts (requires exception process)
- Changes to review criteria (requires documentation)

### Dependencies

**Upstream Dependencies**:
- All agents: Submit artifacts for review
- Data Analyst: Quality metrics and trends
- External standards: WCAG, learning science best practices

**Downstream Dependencies**:
- All agents: Receive feedback and approvals
- Students: Benefit from quality assurance
- Leadership: Quality reporting for decision-making

### Logging and Observability

**Log Events**:
```
DEBUG: Review started: [artifact-id] type: [course/feature/analysis]
INFO: Review completed: [artifact-id] result: [PASS/FAIL/CONDITIONAL] score: [n]
INFO: Critical issue found: [artifact-id] issue: [description]
INFO: Re-review completed: [artifact-id] issues-resolved: [n/total]
WARN: Review delayed: [artifact-id] age: [hours] reason: [text]
ERROR: Defect escaped to production: [artifact-id] issue: [description]
CRITICAL: Quality trend deteriorating: [agent-id] error-rate: [%] change: [+n%]
```

**Dashboards**:
- **Review Queue**: Active reviews, status, age, priority
- **Quality Scores**: By agent, artifact type, over time
- **Defect Tracking**: Types, frequency, trends, time to fix
- **SLA Performance**: On-time rates, average turnaround
- **Agent Quality Trends**: First-pass rates, improvement over time
- **Standards Compliance**: Accessibility, accuracy, effectiveness

---

## SUMMARY: KEY DESIGN PRINCIPLES ACROSS ALL AGENTS

### 1. BDI Model (Beliefs-Desires-Intentions)
All agents have explicit:
- **Beliefs**: Knowledge base and frameworks they operate from
- **Desires**: Measurable goals and success metrics
- **Intentions**: Committed actions and rhythms

### 2. Input/Output Handling
All agents:
- Define accepted input formats with validation rules
- Sanitize inputs to prevent errors and security issues
- Produce structured outputs with validation before release
- Document expected formats and constraints

### 3. Memory Management
All agents implement:
- **Short-term memory**: Active session context
- **Long-term memory** (MCP): Persistent knowledge and patterns
- **Retrieval triggers**: When to access stored information
- **Consolidation schedules**: When to update and archive

### 4. Error Management
All agents have:
- **Common failure modes** documented
- **Detection mechanisms** for each failure type
- **Retry logic** with exponential backoff and limits
- **Fallback strategies** when retries exhausted
- **Idempotency** where operations can be safely retried
- **Logging** of all errors for learning and improvement

### 5. Communication (FIPA ACL)
All agents use standardized message structure:
- **Performative**: REQUEST, PROPOSE, INFORM, QUERY-IF, CONFIRM, WARN
- **Sender/Receiver**: Clear agent identification
- **Content**: Specific, actionable message
- **Protocol**: Interaction pattern (request-response, pub/sub, etc.)
- **Ontology**: Domain/topic classification

### 6. Performance Metrics
All agents track:
- **Latency**: Response times for different task types
- **Token usage**: Budget management
- **Success rate**: Task completion without errors
- **Quality metrics**: Domain-specific quality indicators

### 7. Security and Access Controls
All agents implement:
- **Data access permissions**: READ/WRITE/NO ACCESS clearly defined
- **Rate limiting**: Prevent abuse and overload
- **Approval gates**: Human oversight for high-stakes decisions
- **Privacy protections**: PII anonymization and compartmentalization

### 8. Dependencies
All agents document:
- **Upstream dependencies**: What they need as input
- **Downstream dependencies**: Who consumes their output
- **Coordination patterns**: How they interact with other agents

### 9. Logging and Observability
All agents provide:
- **Structured logs**: DEBUG, INFO, WARN, ERROR, CRITICAL levels
- **Dashboards**: Real-time visibility into status and performance
- **Audit trails**: For accountability and debugging

### 10. Ethical Considerations
All agents adhere to:
- **Transparency**: Explain reasoning and decisions
- **Fairness**: No bias or discrimination
- **Privacy**: Protect student data
- **Safety**: Avoid harmful outputs or actions
- **Human oversight**: Appropriate approval gates

---

## NEXT STEPS

This document provides the complete technical specifications for all 10 agents in the AI Flywheel Elite Learning Design Agency.

**Recommended Actions**:
1. ✅ **COMPLETE**: Agent Specifications
2. ⏭️ **NEXT**: Design FIPA ACL Communication Protocol (detailed message templates)
3. **THEN**: Implementation Templates (memory, error handling, logging)
4. **THEN**: Security & Privacy Implementation Plan
5. **FINALLY**: Testing & Validation Framework

**Document Status**: Ready for review and implementation planning.

---
