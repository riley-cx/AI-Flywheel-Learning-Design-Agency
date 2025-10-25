# AI Flywheel Learning Design Agency
## REVISED ARCHITECTURE - Based on Anthropic Best Practices

**Date**: 2025-10-25
**Status**: Foundation Phase - Architecture Redesign
**Basis**: Anthropic's guidance on effective AI agent systems

---

## 🎯 Core Architectural Principle

**Instead of building 10 separate AI agents, we use:**
- **Claude Code** as the intelligent orchestrator (adopting different roles/perspectives)
- **MCP Servers** for specialized data access and API operations (5 servers)
- **Slash Commands** for workflows (7 main workflows)
- **CLAUDE.md files** for domain expertise (4 knowledge domains)

**Why this approach:**
- ✅ Leverages Claude Code's native capabilities
- ✅ Avoids reinventing message passing, memory, orchestration
- ✅ Simpler to build and maintain
- ✅ More context-efficient (per Anthropic's guidance)
- ✅ Uses proven patterns (MCP, slash commands)

---

## 📊 Mapping: Original Agents → New Architecture

| Original Agent | New Implementation | Reasoning |
|----------------|-------------------|-----------|
| **Data Analyst** | MCP Server: Learning Analytics | Needs persistent DB connections, performs stateless queries |
| **Market Research Analyst** | MCP Server: Market Intelligence | Makes external API calls, web scraping, returns structured data |
| **Learning Designer** | Slash Command + CLAUDE.md | Content creation via Claude's native capabilities + domain expertise |
| **Experience Designer** | Slash Command + CLAUDE.md | UI/UX design via Claude + expertise files |
| **Behavioral Scientist** | Slash Command + CLAUDE.md | Research-backed recommendations via Claude + psychology expertise |
| **Chief Learning Strategist** | Slash Command (strategic role) | High-level reasoning, uses MCP servers for data |
| **Chief Experience Strategist** | Slash Command (UX strategy role) | Strategic UX decisions, coordinates with other workflows |
| **Chief Community Strategist** | Slash Command (community role) | Community strategy, uses Community Platform MCP |
| **Quality Assurance Specialist** | MCP Server: Quality Validation | Automated validation rules, accessibility checks |
| **Community Manager** | MCP Server: Community Platform | API interactions for posting, moderation |

---

## 🔧 Component 1: MCP Servers (5 Total)

### MCP Server 1: Learning Analytics
**Purpose**: Access and analyze student/course data
**Replaces**: Data Analyst agent

**Why MCP?**
- Needs persistent database connections (PostgreSQL)
- Performs stateless operations (query → result)
- Returns structured data for Claude to reason about
- Standard MCP pattern for data access

**Tools Provided:**
```typescript
// Get course performance metrics
get_course_metrics(
  course_id: string,
  metric_type: "completion" | "satisfaction" | "engagement",
  date_range?: {start: string, end: string}
) → {value: number, trend: string, comparisons: object}

// Analyze student cohorts
analyze_student_cohort(
  filters: {
    enrollment_date?: string,
    course_id?: string,
    demographics?: object
  }
) → {cohort_size: number, metrics: object, insights: string[]}

// Query engagement patterns
query_engagement_data(
  date_range: {start: string, end: string},
  segment?: string
) → {daily_active: number[], patterns: object, anomalies: object[]}

// Get completion rates by segment
get_completion_rates(
  segment: "course" | "module" | "lesson",
  filters?: object
) → {rates: object[], benchmarks: object, trends: object}

// Run predictive analysis
predict_student_outcomes(
  student_id: string,
  model_type: "completion" | "satisfaction" | "churn"
) → {prediction: number, confidence: number, factors: string[]}
```

**Data Sources:**
- PostgreSQL database (student data, course data, engagement metrics)
- Redis cache (for frequently accessed metrics)

**Response Format**: JSON with semantic meaning (human-readable labels, not just UUIDs)

---

### MCP Server 2: Market Intelligence
**Purpose**: Gather market research and competitive intelligence
**Replaces**: Market Research Analyst agent

**Why MCP?**
- Makes external API calls (research databases, competitor sites)
- Web scraping for public data
- Returns structured research findings
- Stateless operations

**Tools Provided:**
```typescript
// Search market trends
search_market_trends(
  topic: string,
  timeframe: "week" | "month" | "quarter" | "year",
  sources?: string[]
) → {trend_score: number, search_volume: object, insights: string[], sources: string[]}

// Get competitor analysis
get_competitor_pricing(
  competitors: string[],
  course_category?: string
) → {competitor: string, price_range: object, features: string[], positioning: string}[]

// Analyze search volume
analyze_search_volume(
  keywords: string[],
  platform: "google" | "youtube" | "reddit" | "all"
) → {keyword: string, volume: number, trend: string, competition: string}[]

// Fetch industry reports
fetch_industry_reports(
  topic: string,
  date_range?: {start: string, end: string}
) → {report_title: string, source: string, key_findings: string[], url: string}[]

// Validate course opportunity
validate_course_opportunity(
  course_concept: string,
  target_price: number
) → {demand_score: number, competition_level: string, recommendations: string[], confidence: number}
```

**Data Sources:**
- Google Trends API
- Competitor websites (web scraping)
- Research databases (if available)
- Social media APIs (Reddit, Twitter)

**Response Format**: Concise summaries with actionable insights, not raw data dumps

---

### MCP Server 3: Content Management
**Purpose**: CRUD operations for course content and files
**Replaces**: File management aspects of Learning Designer, Experience Designer

**Why MCP?**
- File system operations
- Version control (git) integration
- Template management
- Stateless CRUD operations

**Tools Provided:**
```typescript
// Create course structure
create_course_structure(
  course_outline: {
    title: string,
    modules: {title: string, lessons: string[]}[],
    metadata: object
  }
) → {course_id: string, file_paths: string[], status: "created"}

// Save lesson content
save_lesson_content(
  course_id: string,
  lesson_id: string,
  content: {
    markdown: string,
    assets?: {type: string, path: string}[],
    metadata: object
  }
) → {lesson_path: string, version: string, status: "saved"}

// Get course template
get_course_template(
  course_type: "technical" | "leadership" | "creative",
  format: "markdown" | "json"
) → {template: string, instructions: string, best_practices: string[]}

// Validate course structure
validate_course_structure(
  course_data: object
) → {valid: boolean, errors: string[], warnings: string[], suggestions: string[]}

// Version control operations
commit_course_changes(
  course_id: string,
  commit_message: string
) → {commit_hash: string, files_changed: number, status: "committed"}

// Search existing content
search_course_library(
  query: string,
  filters?: {course_type?: string, topic?: string}
) → {course_id: string, title: string, relevance_score: number, excerpt: string}[]
```

**Data Sources:**
- Local file system (course content)
- Git repository
- Template library

**Response Format**: File paths and status messages, not full content (context-efficient)

---

### MCP Server 4: Community Platform
**Purpose**: Interact with community platform (forum, discussions)
**Replaces**: Execution aspects of Community Manager agent

**Why MCP?**
- API calls to community platform (Discourse, Circle, custom)
- Posting, moderation, notifications
- Retrieve community health data
- Stateless operations

**Tools Provided:**
```typescript
// Post to community
post_to_community(
  message: string,
  channel: string,
  options?: {pin?: boolean, notify?: boolean}
) → {post_id: string, url: string, status: "posted"}

// Moderate content
moderate_content(
  content_id: string,
  action: "approve" | "remove" | "flag" | "warn_user",
  reason?: string
) → {status: "moderated", action_taken: string, user_notified: boolean}

// Get community health metrics
get_community_health_metrics(
  timeframe?: {start: string, end: string}
) → {
  participation_rate: number,
  active_users: number,
  sentiment_score: number,
  top_topics: string[],
  alerts: object[]
}

// Send notification
send_notification(
  user_ids: string[],
  message: string,
  notification_type: "email" | "platform" | "both"
) → {sent_count: number, failed: string[], status: "sent"}

// Get discussion thread
get_discussion_thread(
  thread_id: string,
  include_replies?: boolean
) → {
  title: string,
  posts: {author: string, content: string, timestamp: string}[],
  sentiment: string,
  engagement_level: string
}

// Identify potential advocates
identify_advocates(
  criteria: {min_contributions?: number, min_helpful_score?: number}
) → {user_id: string, contribution_score: number, influence_level: string}[]
```

**Data Sources:**
- Community platform API (Discourse, Circle, etc.)
- Email service (SendGrid, etc.)

**Response Format**: Action confirmations and summaries, not full thread dumps

---

### MCP Server 5: Quality Validation
**Purpose**: Automated quality checks and validation
**Replaces**: Automated aspects of QA Specialist agent

**Why MCP?**
- Runs automated validation rules
- Accessibility checking (WCAG)
- Content quality checks
- Returns structured pass/fail results

**Tools Provided:**
```typescript
// Validate accessibility
validate_accessibility(
  content_url: string,
  standard: "WCAG-AA" | "WCAG-AAA"
) → {
  passed: boolean,
  score: number,
  violations: {type: string, severity: string, location: string, fix: string}[],
  warnings: string[]
}

// Check learning objectives alignment
check_learning_objectives(
  course_data: {
    objectives: string[],
    assessments: object[],
    content: string[]
  }
) → {
  aligned: boolean,
  alignment_score: number,
  mismatches: {objective: string, issue: string, suggestion: string}[]
}

// Validate cognitive load
validate_cognitive_load(
  lesson_content: string
) → {
  concept_count: number,
  cognitive_load: "low" | "optimal" | "high",
  recommendations: string[]
}

// Run quality checklist
run_quality_checklist(
  artifact_type: "course" | "lesson" | "assessment",
  artifact_data: object
) → {
  overall_score: number,
  passed_checks: string[],
  failed_checks: {check: string, severity: string, details: string}[],
  decision: "PASS" | "FAIL" | "CONDITIONAL_PASS"
}

// Check readability
check_readability(
  content: string,
  target_audience: "beginner" | "intermediate" | "advanced"
) → {
  flesch_kincaid: number,
  appropriate: boolean,
  suggestions: string[]
}
```

**Data Sources:**
- Accessibility testing libraries (axe-core, pa11y)
- Content analysis tools
- Custom validation rules

**Response Format**: Structured results with actionable fixes, not just error codes

---

## 🔀 Component 2: Slash Commands (7 Main Workflows)

### Slash Command 1: `/new-course`
**Purpose**: Design and create a new course from concept to outline
**Replaces**: Chief Learning Strategist + Market Research Analyst + Learning Designer coordination

**Workflow:**
```
1. User provides: Topic, Target audience, Desired outcomes
2. Claude loads: learning-design.md expertise
3. Claude uses: Market Intelligence MCP (validate demand)
4. Claude uses: Learning Analytics MCP (check similar courses)
5. Claude reasons: Strategic fit, market opportunity
6. Claude creates: Course outline (via Content Management MCP)
7. Claude returns: Complete course design + strategic recommendation
```

**Implementation:**
```bash
# .claude/commands/new-course.md

You are acting as the Chief Learning Strategist and Learning Designer for an elite learning design agency.

Your task: Design a new course from concept to detailed outline.

WORKFLOW:
1. Gather Information
   - Course topic: $TOPIC
   - Target audience: $AUDIENCE
   - Learning outcomes: $OUTCOMES

2. Market Validation
   - Use search_market_trends() to validate demand
   - Use get_competitor_pricing() to understand pricing landscape
   - Use validate_course_opportunity() for go/no-go decision

3. Internal Analysis
   - Use get_course_metrics() to analyze similar existing courses
   - Use analyze_student_cohort() to understand target audience performance

4. Strategic Decision
   - Synthesize market + internal data
   - Make recommendation: PROCEED / MODIFY / NO-GO
   - If PROCEED, determine pricing, positioning, differentiation

5. Course Design
   - Load expertise from learning-design.md
   - Create course outline (modules, lessons, assessments)
   - Apply instructional design best practices
   - Validate with check_learning_objectives()

6. Save & Report
   - Use create_course_structure() to save outline
   - Generate executive summary
   - Provide next steps

EXPERTISE: Load from .claude/expertise/learning-design.md
TONE: Strategic, data-driven, actionable
OUTPUT: Structured markdown report + saved course outline
```

---

### Slash Command 2: `/analyze-engagement`
**Purpose**: Diagnose and fix low engagement issues
**Replaces**: Data Analyst + Behavioral Scientist + Learning Designer coordination

**Workflow:**
```
1. User provides: Course ID or describes issue
2. Claude uses: Learning Analytics MCP (deep dive on engagement data)
3. Claude loads: behavioral-science.md expertise
4. Claude diagnoses: Root cause (cognitive overload, motivation, etc.)
5. Claude proposes: Evidence-based interventions
6. Claude creates: Fix plan with expected impact
```

**Implementation:**
```bash
# .claude/commands/analyze-engagement.md

You are acting as the Data Analyst and Behavioral Scientist.

Your task: Diagnose and solve engagement issues.

WORKFLOW:
1. Gather Data
   - Course: $COURSE_ID
   - Use query_engagement_data() for patterns
   - Use get_completion_rates() for drop-off points
   - Use analyze_student_cohort() for segment analysis

2. Diagnose Root Cause
   - Load expertise from behavioral-science.md
   - Analyze patterns (when do students drop off?)
   - Identify barriers (cognitive load, motivation, clarity, technical)
   - Validate hypotheses with data

3. Design Intervention
   - Apply behavioral science principles
   - Design specific, testable interventions
   - Estimate expected impact (with confidence intervals)
   - Use validate_cognitive_load() to check fixes

4. Create Action Plan
   - Prioritize interventions by impact/effort
   - Specify implementation steps
   - Set up measurement plan
   - Timeline and owners

EXPERTISE: Load from .claude/expertise/behavioral-science.md
TONE: Analytical, evidence-based, specific
OUTPUT: Diagnosis report + intervention plan with expected impact
```

---

### Slash Command 3: `/optimize-experience`
**Purpose**: Improve student experience and satisfaction
**Replaces**: Chief Experience Strategist + Experience Designer + Behavioral Scientist

**Workflow:**
```
1. User provides: Experience goal (satisfaction, onboarding, etc.)
2. Claude uses: Learning Analytics MCP (current satisfaction, friction points)
3. Claude loads: ux-design.md + behavioral-science.md expertise
4. Claude designs: UX improvements + behavioral interventions
5. Claude validates: Accessibility, usability
6. Claude creates: Implementation plan
```

---

### Slash Command 4: `/quarterly-planning`
**Purpose**: Strategic planning session with all "Chiefs"
**Replaces**: All three Chief agents coordination

**Workflow:**
```
1. Claude uses: Learning Analytics MCP (performance review)
2. Claude uses: Market Intelligence MCP (market analysis)
3. Claude adopts: Chief Learning Strategist perspective (overall strategy)
4. Claude adopts: Chief Experience Strategist perspective (UX priorities)
5. Claude adopts: Chief Community Strategist perspective (community priorities)
6. Claude synthesizes: Integrated strategic plan
```

---

### Slash Command 5: `/design-intervention`
**Purpose**: Create behavioral intervention based on research
**Replaces**: Behavioral Scientist agent

**Implementation:**
```bash
# .claude/commands/design-intervention.md

You are a Behavioral Scientist specializing in learning motivation and habit formation.

Your task: Design an evidence-based behavioral intervention.

WORKFLOW:
1. Understand the Problem
   - Behavior to change: $BEHAVIOR
   - Current state data (use Learning Analytics MCP)
   - Target state / goal

2. Behavioral Diagnosis
   - Load expertise from behavioral-science.md
   - Apply Fogg Behavior Model (Motivation, Ability, Trigger)
   - Identify which component is lacking
   - Find root cause

3. Design Intervention
   - Select evidence-based tactics
   - Design for sustainability (not just short-term)
   - Consider ethical implications
   - Specify implementation details

4. A/B Test Design
   - Control vs. treatment
   - Sample size calculation
   - Success metrics
   - Analysis plan

5. Expected Impact
   - Estimate effect size (with confidence intervals)
   - Timeline to results
   - Risks and mitigation

EXPERTISE: Load from .claude/expertise/behavioral-science.md
CONSTRAINTS: No dark patterns, must be ethical and transparent
OUTPUT: Intervention design + A/B test plan + expected impact
```

---

### Slash Command 6: `/community-campaign`
**Purpose**: Plan and launch community engagement campaign
**Replaces**: Chief Community Strategist + Community Manager coordination

**Workflow:**
```
1. User provides: Campaign goal (participation, advocacy, etc.)
2. Claude loads: community-strategy.md expertise
3. Claude uses: Community Platform MCP (current health metrics)
4. Claude designs: Campaign (tactics, content, timeline)
5. Claude uses: Community Platform MCP (set up campaign infrastructure)
6. Claude creates: Execution plan and success metrics
```

---

### Slash Command 7: `/quality-review`
**Purpose**: Comprehensive quality review before launch
**Replaces**: Quality Assurance Specialist agent

**Workflow:**
```
1. User provides: Course/artifact to review
2. Claude uses: Quality Validation MCP (automated checks)
3. Claude manually reviews: Strategic alignment, pedagogical quality
4. Claude uses: validate_accessibility() for WCAG compliance
5. Claude uses: check_learning_objectives() for alignment
6. Claude generates: Quality report with pass/fail decision
```

---

## 📚 Component 3: CLAUDE.md Expertise Files

### File 1: `.claude/expertise/learning-design.md`
**Purpose**: Provide instructional design expertise

**Contents:**
```markdown
# Instructional Design Expertise

## Frameworks We Use

### ADDIE Model
- Analysis: Needs assessment, learner analysis
- Design: Learning objectives, assessment strategy
- Development: Content creation, materials
- Implementation: Delivery
- Evaluation: Formative and summative

### Backward Design (Wiggins & McTighe)
1. Identify desired results (learning objectives)
2. Determine acceptable evidence (assessments)
3. Plan learning experiences and instruction

### SAM (Successive Approximation Model)
- Iterative design process
- Rapid prototyping
- Continuous evaluation

## Learning Science Principles

### Cognitive Load Theory
- Intrinsic load: Inherent difficulty of material
- Extraneous load: How information is presented
- Germane load: Processing that builds schemas
- **Rule**: Limit new concepts to 7±2 per lesson

### Spaced Repetition
- Space learning over time (not cramming)
- Retrieve information at increasing intervals
- Use active recall, not passive review

### Multimedia Learning (Mayer's Principles)
- Coherence: Exclude extraneous material
- Signaling: Highlight key information
- Redundancy: Don't repeat identical info
- Spatial contiguity: Place related text/images together
- Temporal contiguity: Present narration with animation simultaneously

## Bloom's Taxonomy (Revised)

**Remember**: Recall facts (define, list, name)
**Understand**: Explain concepts (describe, explain, summarize)
**Apply**: Use in new situations (apply, demonstrate, solve)
**Analyze**: Break into parts (analyze, compare, distinguish)
**Evaluate**: Make judgments (assess, critique, evaluate)
**Create**: Produce new work (create, design, develop)

**Rule**: Learning objectives and assessments must align at same Bloom's level

## Assessment Design

### Formative Assessment
- Low stakes
- Frequent feedback
- Guides learning

### Summative Assessment
- High stakes
- Measures mastery
- Certifies completion

### Authentic Assessment
- Real-world application
- Performance-based
- Transfer of learning

## Common Patterns for Course Types

### Technical/Skills Courses
- Structure: Concept → Example → Practice → Project
- Assessments: Hands-on coding/application
- Success factor: Immediate application

### Leadership/Soft Skills
- Structure: Framework → Case study → Reflection → Practice
- Assessments: Scenario-based, peer feedback
- Success factor: Personal relevance

### Theoretical/Conceptual
- Structure: Foundation → Depth → Application → Integration
- Assessments: Analysis, synthesis tasks
- Success factor: Clear mental models

## Target Completion Rates by Course Type
- Beginner: 75-85%
- Intermediate: 80-90%
- Advanced: 85-95% (self-selected, motivated audience)

## Quality Checklist
- [ ] Learning objectives are SMART and measurable
- [ ] Assessments align with objectives (Bloom's level match)
- [ ] Cognitive load optimized (<7 new concepts per lesson)
- [ ] Accessibility compliance (WCAG 2.1 AA)
- [ ] Readability appropriate for audience
- [ ] Scaffolding for complex topics
- [ ] Active learning, not passive consumption
- [ ] Feedback loops throughout
```

---

### File 2: `.claude/expertise/behavioral-science.md`
**Purpose**: Behavioral psychology and motivation expertise

**Contents:**
```markdown
# Behavioral Science Expertise

## Core Frameworks

### Fogg Behavior Model (B = MAT)
**Behavior occurs when:**
- **Motivation** is sufficient (desire to act)
- **Ability** is present (can do it easily)
- **Trigger** prompts action (reminder, cue)

**Diagnosis**: When behavior doesn't happen, identify which component is missing

### Self-Determination Theory (Deci & Ryan)
**Intrinsic motivation requires:**
- **Autonomy**: Sense of choice and control
- **Competence**: Feeling effective and capable
- **Relatedness**: Connection to others

**Rule**: Design for intrinsic motivation first, extrinsic carefully

### Habit Loop (Duhigg)
1. **Cue**: Trigger for the routine
2. **Routine**: The behavior itself
3. **Reward**: Benefit reinforcing the habit

**Application**: To build study habits, design consistent cues and immediate rewards

## Motivation Tactics

### Increase Motivation
- **Connect to goals**: Show relevance to student's aspirations
- **Social proof**: "X students completed this week"
- **Progress visualization**: Show how far they've come
- **Quick wins**: Easy early successes

### Increase Ability (Make It Easy)
- **Tiny habits**: Start with 2-minute commitment
- **Remove friction**: One-click to start learning
- **Scaffolding**: Break complex tasks into steps
- **Templates and examples**: Reduce starting from scratch

### Effective Triggers
- **Time-based**: "Study every weekday at 7am"
- **Implementation intentions**: "When X happens, I will Y"
- **Context-based**: "After coffee, I review flashcards"

## Common Barriers and Solutions

### Procrastination
**Causes**: Task aversion, perfectionism, overwhelm
**Solutions**:
- Make starting ridiculously easy (2-minute rule)
- Implementation intentions ("I will study at [time] in [place]")
- Accountability (social commitment, study partners)

### Low Engagement
**Causes**: Irrelevance, too difficult, boring delivery
**Solutions**:
- Demonstrate immediate value
- Adjust difficulty (optimal challenge: slightly above current skill)
- Vary formats (video, interactive, discussion)

### Drop-off After Initial Excitement
**Causes**: Motivation decays, difficulty increases, competing priorities
**Solutions**:
- Habit formation focus (build routine before motivation fades)
- Community support (accountability)
- Micro-commitments (small, achievable milestones)

## Persuasive Design Patterns

### Ethical Patterns (Use These)
- **Progress tracking**: Visual representation of advancement
- **Commitment devices**: Public goals, pre-commitment
- **Social influence**: Peer learning, community
- **Recognition**: Celebrate achievements
- **Personalization**: Tailored content and paths

### Dark Patterns (NEVER Use)
- **False scarcity**: Fake urgency ("Only 2 spots left!")
- **Hidden costs**: Surprise fees or requirements
- **Confirmshaming**: Guilt-tripping ("No thanks, I don't want to succeed")
- **Forced continuity**: Hard to cancel or opt-out
- **Disguised ads**: Unclear what's promotional

**Ethical Standard**: Transparency, respect for autonomy, no manipulation

## A/B Test Design

### Hypothesis Template
"We believe that [intervention] will cause [behavior change] for [audience] because [theory/mechanism]"

### Metrics
- **Primary**: The main behavior you want to change
- **Secondary**: Leading indicators
- **Guardrail**: Metrics that shouldn't decrease

### Sample Size
- Use power analysis (80% power, p<0.05)
- Minimum detectable effect: 10-20% improvement
- Run for 2-4 weeks minimum

### Analysis
- Statistical significance (p-value)
- **Effect size** (more important than p-value!)
- Confidence intervals
- Segmentation analysis

## Effect Sizes (Benchmarks)
- **Small**: 5-10% improvement
- **Medium**: 10-20% improvement
- **Large**: >20% improvement

Most interventions: 10-15% expected lift
```

---

### File 3: `.claude/expertise/ux-design.md`
**Purpose**: UX/UI design and experience optimization

**Contents:**
```markdown
# UX Design Expertise

## Core Principles

### Nielsen's 10 Usability Heuristics
1. **Visibility of system status**: Keep users informed
2. **Match system to real world**: Use familiar language
3. **User control and freedom**: Easy undo/redo
4. **Consistency and standards**: Follow conventions
5. **Error prevention**: Better than good error messages
6. **Recognition over recall**: Minimize memory load
7. **Flexibility and efficiency**: Shortcuts for experts
8. **Aesthetic and minimalist design**: No clutter
9. **Help users recognize errors**: Clear error messages
10. **Help and documentation**: Searchable, concise

### Don Norman's Design Principles
- **Discoverability**: Can users find what they need?
- **Feedback**: Does the system respond to actions?
- **Conceptual model**: Do users understand how it works?
- **Affordances**: Are interactive elements obvious?
- **Signifiers**: Are there cues to indicate functionality?
- **Mapping**: Do controls relate logically to effects?
- **Constraints**: Are there guardrails against errors?

## Accessibility Standards (WCAG 2.1 AA)

### Perceivable
- **Text alternatives**: Alt text for images
- **Captions**: For audio/video content
- **Adaptable**: Content works at 200% zoom
- **Distinguishable**: 4.5:1 color contrast ratio for text

### Operable
- **Keyboard accessible**: All functions via keyboard
- **Enough time**: No tight time limits
- **Seizures**: No flashing content >3 times/second
- **Navigable**: Clear headings, skip links, focus indicators

### Understandable
- **Readable**: Clear language, readability appropriate for audience
- **Predictable**: Consistent navigation and behavior
- **Input assistance**: Clear labels, error prevention, suggestions

### Robust
- **Compatible**: Works with assistive technologies
- **Valid HTML**: Proper semantic markup

## User Research Methods

### Discovery
- **User interviews**: Understand needs, motivations, pain points
- **Surveys**: Quantitative data at scale
- **Analytics**: Behavioral data (what users actually do)
- **Competitive analysis**: Learn from others

### Validation
- **Usability testing**: Watch users complete tasks
- **A/B testing**: Compare variants
- **Heuristic evaluation**: Expert review against principles
- **Accessibility audit**: WCAG compliance check

## Interaction Patterns for Learning

### Onboarding
- **Progressive disclosure**: Reveal features gradually
- **Contextual help**: Just-in-time guidance
- **Reduce time to "aha moment"**: Quick win within 5 minutes

### Navigation
- **Breadcrumbs**: Show location in course structure
- **Progress indicators**: "Lesson 3 of 12"
- **Next/Previous**: Easy sequential navigation
- **Jump to section**: For non-linear exploration

### Feedback
- **Immediate**: Real-time validation (correct/incorrect)
- **Specific**: Not just "wrong" but "why wrong"
- **Constructive**: Guidance on how to improve
- **Positive**: Celebrate successes

### Engagement
- **Interactive elements**: Quizzes, simulations, exercises
- **Multimedia**: Mix of text, video, audio, interactive
- **Social**: Discussion, peer feedback, community
- **Gamification** (careful): Progress, achievements, leaderboards

## Performance Budgets

- **Page load**: <3 seconds on 3G
- **Time to interactive**: <5 seconds
- **First contentful paint**: <1.5 seconds
- **Video load**: Start playing within 2 seconds

## Responsive Design Breakpoints

- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px+
- **Mobile-first**: Design for smallest screen first

## Common UX Patterns

### Error States
- Clear, human-friendly message
- Explain what went wrong
- Suggest how to fix
- Provide support contact if needed

### Empty States
- Don't just show blank screen
- Explain why it's empty
- Guide user to first action
- Show example of filled state

### Loading States
- Show progress indicator for >1 second waits
- Skeleton screens for content loading
- Optimistic UI updates when possible

## Usability Testing Protocol

1. **Define tasks**: 5-7 realistic scenarios
2. **Recruit participants**: 5-8 users (80% of issues found)
3. **Moderate**: "Think aloud" protocol
4. **Observe**: Note struggles, confusion, errors
5. **Measure**: Task success rate, time on task, satisfaction
6. **Iterate**: Fix issues, re-test

**Success criteria**: >80% task completion, >4.0/5.0 satisfaction
```

---

### File 4: `.claude/expertise/community-strategy.md`
**Purpose**: Community building and engagement tactics

**Contents:**
```markdown
# Community Strategy Expertise

## Community of Practice (CoP) Theory (Wenger)

### Three Core Elements
1. **Domain**: Shared interest or passion
2. **Community**: Relationships and trust
3. **Practice**: Shared repertoire of resources, experiences, tools

**Application**: Successful learning communities need all three

## Community Lifecycle Stages

### 1. Inception (Weeks 1-4)
**Goal**: Establish foundation
- Welcome rituals for new members
- Set norms and expectations
- Create initial connections
- **Key metric**: 50% of members make first post

### 2. Growth (Months 2-6)
**Goal**: Build engagement
- Activate lurkers (90-9-1 rule: 90% lurk, 9% contribute occasionally, 1% create most)
- Develop core contributors
- Establish regular rhythms (weekly discussions, monthly events)
- **Key metric**: 40% weekly active participation

### 3. Maturity (6+ months)
**Goal**: Sustain and deepen
- Student-led initiatives
- Peer mentorship
- Alumni engagement
- **Key metric**: 60% participation, high NPS (>40)

### 4. Renewal
**Goal**: Prevent decline
- Refresh content and activities
- Recognize long-time members
- Recruit new leadership
- **Key metric**: Retention of core contributors

## Engagement Tactics by Goal

### Increase Participation (Lurkers → Contributors)
- **Lower the bar**: Make first contribution easy ("introduce yourself")
- **Direct invites**: Personal outreach to inactive members
- **Recognition**: Highlight helpful posts
- **Prompts**: Specific, answerable questions

### Build Connection (Isolated → Connected)
- **Cohort formation**: Start together, shared identity
- **Pair/small groups**: Study partners, accountability buddies
- **Synchronous events**: Live sessions, office hours
- **Shared challenges**: Collective goals

### Develop Advocates (Contributors → Champions)
- **Leadership opportunities**: Moderator, mentor, ambassador roles
- **Public recognition**: Spotlight, badges, leaderboards
- **Exclusive access**: Early access, special events
- **Co-creation**: Involve in content creation, feature decisions

## Moderation Best Practices

### Proactive Moderation
- **Set clear guidelines**: Code of conduct, posting rules
- **Model behavior**: Moderators exemplify desired norms
- **Welcome newcomers**: Personal greeting within 24 hours
- **Encourage positive**: Recognize helpful, constructive posts

### Reactive Moderation
**Escalation ladder**:
1. **Gentle reminder**: Assume good intent, point to guidelines
2. **Warning**: Direct message, explain issue
3. **Temporary mute**: 24-48 hour cooling-off period
4. **Ban**: Persistent violations (requires approval)

**Response times**:
- Hate speech / harassment: <30 minutes
- Off-topic / spam: <2 hours
- Quality issues: <24 hours

### Crisis Management
**Types of crises**:
- Hate speech or discrimination
- Conflict between members
- Misinformation spreading
- Negative sentiment spiral

**Response protocol**:
1. **Immediate**: Remove harmful content, protect affected members
2. **Communicate**: Acknowledge issue, explain actions taken
3. **Listen**: Understand root cause
4. **Act**: Address underlying issue, not just symptom
5. **Follow up**: Check in with affected members, update community

## Community Health Metrics

### Participation
- **Weekly active rate**: Target 60%+
- **Post frequency**: 10+ posts per 100 members per week
- **Response time**: Average <2 hours for member questions

### Sentiment
- **Positive sentiment**: Target >70%
- **Net Promoter Score**: Target >40
- **Support tickets about community**: Trending down

### Network Density
- **Average connections**: Target 5+ per member
- **Isolated members**: <10% with 0 connections
- **Central nodes**: Identify and support key connectors

### Advocacy
- **Advocates** (NPS 9-10): Target 30%+
- **Content creators**: Target 15% create content
- **Referrals**: Advocates bring 2+ new members

## Engagement Campaign Patterns

### Challenge-Based
- **Format**: Daily/weekly tasks for 30 days
- **Mechanics**: Public commitment, peer accountability, leaderboard
- **Examples**: "30-Day AI Builder Challenge", "Ship It Week"
- **Success rate**: 40-60% completion

### Event-Based
- **Format**: Live sessions, AMAs, workshops
- **Mechanics**: Limited-time, high-value, interactive
- **Examples**: "Office Hours with Expert", "Live Build Session"
- **Attendance rate**: 20-40% of invited

### Recognition-Based
- **Format**: Spotlight members, achievements, contributions
- **Mechanics**: Nomination, curation, public celebration
- **Examples**: "Member of the Month", "Top Contributors"
- **Engagement lift**: 15-25% post-recognition

### Co-Creation
- **Format**: Community input on product, content, features
- **Mechanics**: Voting, feedback sessions, beta testing
- **Examples**: "What should we build next?", "Beta tester program"
- **Participation**: 30-50% of active members

## Network Effects & Flywheels

### Value Flywheel
1. Great content attracts students
2. Students create community discussions
3. Discussions create more value (beyond content)
4. Value attracts more students
5. Loop accelerates

**Metric to watch**: Student lifetime value (LTV) increases as community matures

### Advocacy Flywheel
1. Great experience creates advocates
2. Advocates refer new students
3. Referred students have higher success (trust from advocate)
4. High success creates more advocates
5. Loop accelerates

**Metric to watch**: % of new students from referrals (target 20%+)

## Anti-Patterns (Avoid These)

### Forced Engagement
- Requiring posts for course completion
- Punishing non-participation
- **Why bad**: Creates low-quality, resentful contributions

### Over-Moderation
- Removing posts for minor issues
- Heavy-handed enforcement
- **Why bad**: Chills authentic discussion, feels oppressive

### Favoritism
- Always highlighting same members
- Insider language/jokes that exclude
- **Why bad**: Creates in-group/out-group, discourages new members

### Letting Negativity Fester
- Ignoring toxic behavior "because they're a paying customer"
- Allowing derails and off-topic rants
- **Why bad**: Good members leave, community quality spirals down
```

---

## 📋 Revised Implementation Plan

### Phase 1: Foundation (Week 1-2)
**Build the 5 MCP Servers**

**Week 1: Infrastructure MCP Servers**
- Learning Analytics Server (connects to PostgreSQL)
- Content Management Server (file operations, git)

**Week 2: Integration MCP Servers**
- Market Intelligence Server (web scraping, APIs)
- Community Platform Server (API integration)
- Quality Validation Server (automated checks)

**Deliverables**: 5 working MCP servers, testable independently

---

### Phase 2: Workflows (Week 3-4)
**Build Slash Commands + CLAUDE.md Files**

**Week 3: Core Workflows**
- Create 4 CLAUDE.md expertise files
- Implement `/new-course` slash command
- Implement `/analyze-engagement` slash command
- Test end-to-end workflow

**Week 4: Additional Workflows**
- Implement `/optimize-experience` slash command
- Implement `/design-intervention` slash command
- Implement `/community-campaign` slash command
- Implement `/quality-review` slash command
- Implement `/quarterly-planning` slash command

**Deliverables**: 7 working slash commands, all calling MCP servers

---

### Phase 3: Polish & Documentation (Week 5-6)
**Production Ready**

**Week 5: User Experience**
- Improve CLI experience
- Add web dashboard (optional)
- Error handling and helpful messages
- Performance optimization

**Week 6: Documentation & Launch**
- User guide for each workflow
- MCP server API documentation
- Video tutorials
- Deploy and test with real use cases

**Deliverables**: Production-ready system, complete documentation

---

## 🎯 Comparison: Original vs. Revised

| Aspect | Original Plan | Revised Plan | Reasoning |
|--------|--------------|--------------|-----------|
| **Development Time** | 10-12 weeks | 5-6 weeks | Leverage Claude Code, don't rebuild it |
| **Infrastructure** | RabbitMQ, custom message broker, supervisor | Just PostgreSQL + MCP protocol | MCP is standard, proven |
| **Agent Count** | 10 separate Python processes | 0 (Claude Code is the agent) | Anthropic best practice |
| **Communication** | Custom FIPA ACL implementation | Native Claude Code tool calling | Built-in, reliable |
| **Memory System** | Custom short-term + long-term + MCP | MCP servers + context management | Simpler, context-efficient |
| **Complexity** | High (distributed system) | Medium (tool orchestration) | Easier to maintain |
| **Lines of Code** | ~15,000-20,000 | ~3,000-5,000 | Less code = fewer bugs |
| **Testing Surface** | Large (10 agents, message broker, etc.) | Small (5 MCP servers + workflows) | Easier to test |

---

## 🚀 Why This Approach is Better

### 1. **Follows Anthropic Best Practices**
- ✅ Minimal viable toolset (5 MCP servers vs. 10 agents)
- ✅ Context efficiency (just-in-time retrieval via MCP)
- ✅ Clear, non-overlapping functionality
- ✅ Right altitude for instructions (slash commands vs. vague "be an agent")

### 2. **Faster to Build**
- Leverage existing infrastructure (Claude Code)
- Standard protocols (MCP)
- Less custom code

### 3. **Easier to Maintain**
- Fewer moving parts
- Standard patterns
- Better debugging (Claude Code's built-in tools)

### 4. **More Powerful**
- Claude Code's full reasoning capability
- Can adopt any "role" dynamically
- Better context management
- Native tool calling

### 5. **Proven Pattern**
- MCP is Anthropic's recommended approach
- Slash commands are battle-tested
- CLAUDE.md works for complex domains

---

## 📚 Next Steps

**Immediate (This Week):**
1. ✅ Review and approve this architecture
2. Set up MCP development environment
3. Build first MCP server (Learning Analytics)
4. Test with Claude Code

**Next Week:**
1. Build remaining 4 MCP servers
2. Create first CLAUDE.md file
3. Build first slash command (`/new-course`)
4. Validate end-to-end workflow

**Questions to Answer:**
- Which MCP server should we build first? (I recommend Learning Analytics - most critical for most workflows)
- Do you have existing databases/APIs to connect to, or should we mock data initially?
- What's your development environment preference? (VS Code? Other?)

---

**This architecture is achievable, maintainable, and follows industry best practices. Ready to start building?** 🚀
