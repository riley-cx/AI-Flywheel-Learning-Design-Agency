# AI Flywheel Elite Learning Design Agency
## FIPA ACL Communication Protocol & Message Templates

### Document Version: 1.0
### Last Updated: 2025-10-24
### Status: Foundation Phase

---

## Table of Contents
1. [Introduction to FIPA ACL](#introduction-to-fipa-acl)
2. [Message Structure Standard](#message-structure-standard)
3. [Performatives Reference](#performatives-reference)
4. [Ontology Definitions](#ontology-definitions)
5. [Communication Protocols](#communication-protocols)
6. [Message Templates by Agent](#message-templates-by-agent)
7. [Error Handling in Communication](#error-handling-in-communication)
8. [Implementation Guidelines](#implementation-guidelines)

---

## Introduction to FIPA ACL

### What is FIPA ACL?

**FIPA** (Foundation for Intelligent Physical Agents) **ACL** (Agent Communication Language) is a standardized protocol for agent-to-agent communication based on speech act theory. It ensures interoperability, structured message exchange, and clear semantic meaning.

### Why Use FIPA ACL for Our Agency?

1. **Standardization**: All agents speak the same language, reducing miscommunication
2. **Semantic Clarity**: Performatives (REQUEST, INFORM, etc.) clearly indicate intent
3. **Conversation Management**: Built-in support for multi-turn conversations
4. **Interoperability**: Can integrate with external agent systems
5. **Auditability**: Structured logs for all communications

### Core Principles

- **Speech Act Theory**: Every message is an action (requesting, informing, proposing)
- **Explicit Semantics**: Meaning is clear from message structure
- **Asynchronous**: Agents don't block waiting for responses (unless designed to)
- **Traceable**: Every message has unique ID and conversation context

---

## Message Structure Standard

### Complete FIPA ACL Message Format

```json
{
  "performative": "REQUEST",           // REQUIRED: Type of communicative act
  "sender": "agent-id:chief-learning-strategist",  // REQUIRED: Sending agent
  "receiver": ["agent-id:market-research-analyst"],  // REQUIRED: Recipient(s)
  "content": "Analyze competitor completion rates for AI/ML courses Q4 2024",  // REQUIRED: Message content
  "language": "natural-language",      // Content representation language
  "encoding": "UTF-8",                 // Character encoding
  "ontology": "competitive-intelligence",  // Domain/topic classification
  "protocol": "request-response",      // Interaction pattern
  "conversation-id": "conv-2024-1024-001",  // Unique conversation identifier
  "reply-with": "req-001",            // Reference for replies
  "in-reply-to": null,                // Reference to previous message (if reply)
  "reply-by": "2024-10-25T14:00:00Z", // Deadline for response (ISO 8601)
  "timestamp": "2024-10-24T10:30:00Z",  // Message creation time
  "priority": "MEDIUM",               // CRITICAL, HIGH, MEDIUM, LOW
  "metadata": {                       // Optional additional context
    "urgency": "standard",
    "budget": 5000,
    "requesting-context": "quarterly-strategy-review"
  }
}
```

### Field Definitions

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `performative` | ✅ Yes | Enum | Communicative act type (see Performatives Reference) |
| `sender` | ✅ Yes | String | Unique agent identifier |
| `receiver` | ✅ Yes | Array | One or more recipient agent IDs |
| `content` | ✅ Yes | String/Object | Actual message payload |
| `language` | Optional | String | Content representation (natural-language, JSON, etc.) |
| `encoding` | Optional | String | Character encoding (default: UTF-8) |
| `ontology` | ✅ Yes | String | Domain classification (see Ontology Definitions) |
| `protocol` | ✅ Yes | String | Interaction pattern (see Communication Protocols) |
| `conversation-id` | ✅ Yes | String | Unique ID for conversation thread |
| `reply-with` | Optional | String | Reference ID for tracking replies |
| `in-reply-to` | Optional | String | Reference to previous message in conversation |
| `reply-by` | Optional | ISO 8601 | Deadline for response |
| `timestamp` | ✅ Yes | ISO 8601 | Message creation timestamp |
| `priority` | Optional | Enum | CRITICAL, HIGH, MEDIUM, LOW (default: MEDIUM) |
| `metadata` | Optional | Object | Additional context (flexible structure) |

---

## Performatives Reference

### Standard FIPA ACL Performatives

| Performative | Purpose | When to Use | Expected Response |
|-------------|---------|-------------|-------------------|
| **REQUEST** | Ask another agent to perform an action | Need another agent to do something | AGREE + INFORM (result) or REFUSE |
| **INFORM** | Share information without expecting action | Provide update, alert, or data | None (or CONFIRM acknowledgment) |
| **PROPOSE** | Suggest an action or approach | Offer recommendation that needs agreement | ACCEPT-PROPOSAL or REJECT-PROPOSAL |
| **QUERY-IF** | Ask a yes/no question | Need boolean verification | INFORM (with boolean answer) |
| **QUERY-REF** | Ask for specific data reference | Need specific value or object | INFORM (with requested data) |
| **CONFIRM** | Verify a belief or fact | Validate something another agent stated | CONFIRM or DISCONFIRM |
| **AGREE** | Accept to perform a requested action | Accepting a REQUEST | (Later: INFORM with result) |
| **REFUSE** | Decline to perform a requested action | Cannot or will not fulfill REQUEST | None |
| **ACCEPT-PROPOSAL** | Agree to a proposed action | Accepting a PROPOSE | (Later: INFORM with result) |
| **REJECT-PROPOSAL** | Decline a proposed action | Not accepting a PROPOSE | None (may include reason) |
| **WARN** | Alert about a problem or risk | Notify of issue requiring attention | None (or CONFIRM acknowledgment) |
| **CANCEL** | Revoke a previous request | No longer need previously requested action | INFORM (cancellation acknowledged) |
| **FAILURE** | Notify that action failed | Could not complete agreed-upon action | None (may trigger retry or escalation) |

### Extended Performatives for Learning Agency

We add these domain-specific performatives:

| Performative | Purpose | Example |
|-------------|---------|---------|
| **ESCALATE** | Elevate issue to higher authority | Community Manager → Chief Community Strategist (crisis) |
| **VALIDATE** | Request quality or accuracy check | Learning Designer → Quality Assurance Specialist |
| **APPROVE** | Grant permission to proceed | Chief Learning Strategist → Learning Designer (course launch) |
| **REJECT** | Deny permission to proceed | Quality Assurance Specialist → Experience Designer (accessibility fail) |

---

## Ontology Definitions

Ontologies classify the domain/topic of communication. This enables agents to route, filter, and prioritize messages.

### Primary Ontologies

| Ontology | Description | Typical Agents Involved |
|----------|-------------|------------------------|
| `learning-strategy` | Strategic planning for learning initiatives | Chiefs, Market Research Analyst |
| `course-design` | Instructional design and curriculum | Learning Designer, Behavioral Scientist, QA |
| `experience-design` | UX/UI design and student experience | Chief Experience Strategist, Experience Designer |
| `community-engagement` | Community building and activation | Chief Community Strategist, Community Manager |
| `competitive-intelligence` | Market research and competitor analysis | Market Research Analyst, Chief Learning Strategist |
| `behavioral-insights` | Behavioral science research and interventions | Behavioral Scientist, Experience Strategist |
| `learning-analytics` | Data analysis and student outcomes | Data Analyst, all agents (consumers) |
| `quality-assurance` | Validation and approval processes | QA Specialist, all agents (submit artifacts) |
| `operational-coordination` | Cross-agent coordination and task management | All agents |
| `ethical-oversight` | Ethics review and compliance | Behavioral Scientist, QA Specialist |

### Sub-Ontologies

More specific classifications within primary ontologies:

```
learning-strategy
  ├── strategic-planning
  ├── goal-setting
  └── resource-allocation

course-design
  ├── instructional-strategy
  ├── assessment-design
  ├── content-creation
  └── curriculum-mapping

experience-design
  ├── ux-patterns
  ├── accessibility
  ├── interaction-design
  └── usability-testing

community-engagement
  ├── community-health-metrics
  ├── moderation
  ├── advocacy-programs
  └── event-management

competitive-intelligence
  ├── competitor-tracking
  ├── market-trends
  ├── pricing-analysis
  └── feature-comparison

behavioral-insights
  ├── motivation-research
  ├── habit-formation
  ├── intervention-design
  └── ab-testing

learning-analytics
  ├── performance-metrics
  ├── engagement-analytics
  ├── predictive-modeling
  └── data-visualization

quality-assurance
  ├── validation-requests
  ├── compliance-checks
  ├── defect-tracking
  └── approval-workflows
```

---

## Communication Protocols

Protocols define the interaction pattern and expected message sequence.

### 1. Request-Response Protocol

**Pattern**: Simple request → response
**Use Case**: One agent needs another to perform a task or provide information

```
A: REQUEST [action]
B: AGREE / REFUSE
[if AGREE]
B: INFORM [result] or FAILURE
A: CONFIRM (acknowledgment)
```

**Example**:
```json
// Message 1: Request
{
  "performative": "REQUEST",
  "sender": "chief-learning-strategist",
  "receiver": ["market-research-analyst"],
  "content": "Analyze competitor pricing for data science courses",
  "protocol": "request-response",
  "conversation-id": "conv-pricing-2024-q4",
  "reply-with": "req-001"
}

// Message 2: Agreement
{
  "performative": "AGREE",
  "sender": "market-research-analyst",
  "receiver": ["chief-learning-strategist"],
  "content": "Starting competitor pricing analysis. ETA: 48 hours",
  "protocol": "request-response",
  "conversation-id": "conv-pricing-2024-q4",
  "in-reply-to": "req-001",
  "reply-with": "agree-001"
}

// Message 3: Result
{
  "performative": "INFORM",
  "sender": "market-research-analyst",
  "receiver": ["chief-learning-strategist"],
  "content": {
    "analysis": "Competitor average: $599. Our price: $799 (+33%). Details: [report-url]"
  },
  "protocol": "request-response",
  "conversation-id": "conv-pricing-2024-q4",
  "in-reply-to": "agree-001"
}
```

### 2. Propose-Accept Protocol

**Pattern**: Proposal → acceptance/rejection → action
**Use Case**: Agent suggests an approach that requires approval

```
A: PROPOSE [action]
B: ACCEPT-PROPOSAL / REJECT-PROPOSAL
[if ACCEPT]
A: INFORM [implementation] or FAILURE
```

**Example**:
```json
// Message 1: Proposal
{
  "performative": "PROPOSE",
  "sender": "behavioral-scientist",
  "receiver": ["chief-experience-strategist"],
  "content": "Implement social proof (show peer progress) to increase completion rates. Expected lift: +18%",
  "protocol": "propose-accept",
  "conversation-id": "conv-engagement-boost",
  "reply-with": "prop-001",
  "metadata": {
    "evidence": "3 peer-reviewed studies + internal A/B test",
    "effort": "2 weeks implementation",
    "risk": "low"
  }
}

// Message 2: Acceptance
{
  "performative": "ACCEPT-PROPOSAL",
  "sender": "chief-experience-strategist",
  "receiver": ["behavioral-scientist"],
  "content": "Approved. Experience Designer will implement. Please coordinate on specs.",
  "protocol": "propose-accept",
  "conversation-id": "conv-engagement-boost",
  "in-reply-to": "prop-001"
}
```

### 3. Query Protocol

**Pattern**: Question → answer
**Use Case**: Agent needs specific information

```
A: QUERY-IF / QUERY-REF [question]
B: INFORM [answer]
```

**Example**:
```json
// QUERY-IF (Boolean question)
{
  "performative": "QUERY-IF",
  "sender": "learning-designer",
  "receiver": ["data-analyst"],
  "content": "Do students who complete practice exercises have higher assessment scores?",
  "protocol": "query",
  "conversation-id": "conv-exercise-effectiveness",
  "reply-with": "query-001"
}

// Response
{
  "performative": "INFORM",
  "sender": "data-analyst",
  "receiver": ["learning-designer"],
  "content": {
    "answer": true,
    "details": "Yes. +15% average assessment score (p<0.001, n=1,250 students)",
    "confidence": 0.99
  },
  "protocol": "query",
  "conversation-id": "conv-exercise-effectiveness",
  "in-reply-to": "query-001"
}

// QUERY-REF (Specific data request)
{
  "performative": "QUERY-REF",
  "sender": "community-manager",
  "receiver": ["data-analyst"],
  "content": "Who are the top 10 community contributors this week?",
  "protocol": "query",
  "conversation-id": "conv-advocate-recognition",
  "reply-with": "query-002"
}

// Response
{
  "performative": "INFORM",
  "sender": "data-analyst",
  "receiver": ["community-manager"],
  "content": {
    "top-contributors": [
      {"id": "student-anon-001", "posts": 12, "helpful-votes": 45},
      {"id": "student-anon-002", "posts": 10, "helpful-votes": 38},
      // ... 8 more
    ]
  },
  "protocol": "query",
  "conversation-id": "conv-advocate-recognition",
  "in-reply-to": "query-002"
}
```

### 4. Publish-Subscribe Protocol

**Pattern**: Publisher broadcasts → subscribers receive
**Use Case**: One agent shares updates with multiple interested agents

```
Publisher: INFORM [event/update] (to all subscribers)
Subscribers: (No response required, but may act on information)
```

**Example**:
```json
// Community Manager publishes engagement alert
{
  "performative": "INFORM",
  "sender": "community-manager",
  "receiver": ["chief-community-strategist", "data-analyst", "behavioral-scientist"],
  "content": {
    "event": "participation-drop",
    "details": "Weekly participation down 25% in course-cohort:2024-q4-ai",
    "baseline": 150,
    "current": 112,
    "change": -25.3
  },
  "protocol": "publish-subscribe",
  "ontology": "community-health-metrics",
  "conversation-id": "pubsub-community-health",
  "priority": "HIGH",
  "timestamp": "2024-10-24T10:00:00Z"
}
```

**Subscription Management** (meta-protocol):
```json
// Agent subscribes to topic
{
  "performative": "REQUEST",
  "sender": "behavioral-scientist",
  "receiver": ["message-broker"],  // Central pub/sub coordinator
  "content": {
    "action": "subscribe",
    "topic": "community-health-metrics",
    "filter": {
      "event-type": ["participation-drop", "sentiment-negative"],
      "severity": ["HIGH", "CRITICAL"]
    }
  },
  "protocol": "subscription-management"
}
```

### 5. Validation Protocol

**Pattern**: Submit for review → approve/reject → (if reject) fix → resubmit
**Use Case**: Quality assurance and approval workflows

```
A: VALIDATE [artifact]
QA: APPROVE / REJECT (with issues)
[if REJECT]
A: INFORM [fixes applied]
A: VALIDATE [artifact] (resubmit)
QA: APPROVE
```

**Example**:
```json
// Message 1: Validation Request
{
  "performative": "VALIDATE",
  "sender": "learning-designer",
  "receiver": ["qa-specialist"],
  "content": {
    "artifact-type": "course",
    "artifact-id": "course-789",
    "artifact-url": "https://lms.ai-flywheel.com/courses/789/preview",
    "quality-criteria": ["accessibility", "content-accuracy", "instructional-design", "assessment-alignment"]
  },
  "protocol": "validation",
  "conversation-id": "conv-qa-course-789",
  "reply-with": "val-001",
  "priority": "HIGH",
  "metadata": {
    "deployment-deadline": "2024-11-01T00:00:00Z"
  }
}

// Message 2: Rejection with Issues
{
  "performative": "REJECT",
  "sender": "qa-specialist",
  "receiver": ["learning-designer"],
  "content": {
    "decision": "CONDITIONAL PASS",
    "score": 78,
    "critical-issues": [
      {
        "id": "issue-001",
        "type": "accessibility",
        "severity": "CRITICAL",
        "description": "3 images missing alt text in Lesson 2",
        "location": "lesson-2, slides 5, 7, 12",
        "fix-guidance": "Add descriptive alt text (not 'image' or 'photo')"
      },
      {
        "id": "issue-002",
        "type": "assessment-alignment",
        "severity": "CRITICAL",
        "description": "Quiz 3, Q5: Tests 'Analyze' level but objective is 'Apply'",
        "fix-guidance": "Adjust question to application level or update objective"
      }
    ],
    "minor-issues": [
      {
        "id": "issue-003",
        "type": "instructional-design",
        "severity": "MINOR",
        "description": "Lesson 4 has high cognitive load (9 new concepts)",
        "recommendation": "Consider splitting into 2 lessons"
      }
    ],
    "conditions": "Fix 2 critical issues. Minor issue is recommendation only.",
    "re-review-required": true
  },
  "protocol": "validation",
  "conversation-id": "conv-qa-course-789",
  "in-reply-to": "val-001"
}

// Message 3: Fixes Applied
{
  "performative": "INFORM",
  "sender": "learning-designer",
  "receiver": ["qa-specialist"],
  "content": {
    "fixes-applied": [
      {
        "issue-id": "issue-001",
        "resolution": "Added descriptive alt text to all 3 images"
      },
      {
        "issue-id": "issue-002",
        "resolution": "Adjusted Q5 to application level (scenario-based question)"
      },
      {
        "issue-id": "issue-003",
        "resolution": "Split Lesson 4 into Lessons 4A and 4B (6+3 concepts)"
      }
    ],
    "ready-for-revalidation": true
  },
  "protocol": "validation",
  "conversation-id": "conv-qa-course-789"
}

// Message 4: Re-validation Request
{
  "performative": "VALIDATE",
  "sender": "learning-designer",
  "receiver": ["qa-specialist"],
  "content": {
    "artifact-type": "course",
    "artifact-id": "course-789",
    "artifact-url": "https://lms.ai-flywheel.com/courses/789/preview",
    "previous-review-id": "val-001",
    "changes-made": "Fixed issues 001, 002, 003"
  },
  "protocol": "validation",
  "conversation-id": "conv-qa-course-789",
  "reply-with": "val-002"
}

// Message 5: Approval
{
  "performative": "APPROVE",
  "sender": "qa-specialist",
  "receiver": ["learning-designer"],
  "content": {
    "decision": "PASS",
    "score": 94,
    "critical-issues-resolved": 2,
    "approval-conditions": "None. Ready for deployment.",
    "commendations": "Excellent resolution of cognitive load issue. Course structure improved."
  },
  "protocol": "validation",
  "conversation-id": "conv-qa-course-789",
  "in-reply-to": "val-002",
  "timestamp": "2024-10-25T16:30:00Z"
}
```

### 6. Escalation Protocol

**Pattern**: Issue detected → escalate → response/resolution
**Use Case**: Critical issues requiring immediate attention or higher authority

```
A: ESCALATE [issue]
Authority: CONFIRM (acknowledgment)
Authority: INFORM [resolution] or REQUEST [additional action]
```

**Example**:
```json
// Message 1: Escalation
{
  "performative": "ESCALATE",
  "sender": "community-manager",
  "receiver": ["chief-community-strategist"],
  "content": {
    "incident-type": "moderation-crisis",
    "severity": "CRITICAL",
    "description": "Hate speech incident in public forum. User suspended. 5 students reported feeling unsafe.",
    "incident-id": "mod-incident-2024-1024-001",
    "actions-taken": [
      "User suspended immediately",
      "Content removed",
      "Affected students contacted privately"
    ],
    "recommendation": "Public statement from leadership + community safety reinforcement",
    "urgency": "Immediate response required"
  },
  "protocol": "escalation",
  "conversation-id": "conv-crisis-2024-1024",
  "priority": "CRITICAL",
  "timestamp": "2024-10-24T14:15:00Z"
}

// Message 2: Acknowledgment
{
  "performative": "CONFIRM",
  "sender": "chief-community-strategist",
  "receiver": ["community-manager"],
  "content": "Incident acknowledged. Coordinating with leadership. ETA on public statement: 2 hours.",
  "protocol": "escalation",
  "conversation-id": "conv-crisis-2024-1024",
  "timestamp": "2024-10-24T14:18:00Z"
}

// Message 3: Resolution
{
  "performative": "INFORM",
  "sender": "chief-community-strategist",
  "receiver": ["community-manager"],
  "content": {
    "resolution": "Public statement issued. Reinforced community guidelines. Enhanced moderation filters deployed.",
    "follow-up-actions": [
      "Monitor community sentiment for 7 days",
      "Conduct listening session with affected students (scheduled: Oct 26)",
      "Review and update moderation training"
    ],
    "incident-status": "Resolved. Post-incident review scheduled."
  },
  "protocol": "escalation",
  "conversation-id": "conv-crisis-2024-1024",
  "timestamp": "2024-10-24T16:30:00Z"
}
```

---

## Message Templates by Agent

### Chief Learning Strategist

#### 1. Requesting Market Research
```json
{
  "performative": "REQUEST",
  "sender": "chief-learning-strategist",
  "receiver": ["market-research-analyst"],
  "content": "Analyze [TOPIC] for [AUDIENCE] in [GEOGRAPHY/MARKET]. Focus on [SPECIFIC ASPECTS].",
  "ontology": "competitive-intelligence",
  "protocol": "request-response",
  "conversation-id": "conv-research-[TOPIC]-[DATE]",
  "reply-with": "req-[ID]",
  "reply-by": "[DEADLINE]",
  "priority": "MEDIUM",
  "metadata": {
    "context": "[WHY_NEEDED]",
    "budget": "[BUDGET_IF_APPLICABLE]",
    "deliverable-format": "brief | full-report | dashboard"
  }
}
```

#### 2. Broadcasting Strategic Direction
```json
{
  "performative": "INFORM",
  "sender": "chief-learning-strategist",
  "receiver": ["chief-experience-strategist", "chief-community-strategist", "learning-designer", "data-analyst"],
  "content": {
    "announcement-type": "strategic-priority",
    "priority": "[PRIORITY_NAME]",
    "rationale": "[WHY]",
    "objectives": ["[OBJECTIVE_1]", "[OBJECTIVE_2]"],
    "timeline": "[TIMEFRAME]",
    "success-metrics": ["[METRIC_1]", "[METRIC_2]"],
    "actions-required": {
      "chief-experience-strategist": "[ACTION]",
      "learning-designer": "[ACTION]"
    }
  },
  "ontology": "learning-strategy",
  "protocol": "publish-subscribe",
  "conversation-id": "pubsub-strategic-updates",
  "priority": "HIGH",
  "timestamp": "[ISO_8601]"
}
```

#### 3. Approving Course Launch
```json
{
  "performative": "APPROVE",
  "sender": "chief-learning-strategist",
  "receiver": ["learning-designer"],
  "content": {
    "approval-type": "course-launch",
    "course-id": "[COURSE_ID]",
    "course-name": "[NAME]",
    "launch-date": "[DATE]",
    "conditions": "[ANY_CONDITIONS_OR_NONE]",
    "congratulations": "[POSITIVE_FEEDBACK]"
  },
  "ontology": "learning-strategy",
  "protocol": "validation",
  "conversation-id": "conv-launch-[COURSE_ID]",
  "in-reply-to": "[ORIGINAL_REQUEST]",
  "timestamp": "[ISO_8601]"
}
```

### Market Research Analyst

#### 1. Delivering Research Findings
```json
{
  "performative": "INFORM",
  "sender": "market-research-analyst",
  "receiver": ["chief-learning-strategist"],
  "content": {
    "research-topic": "[TOPIC]",
    "executive-summary": "[3-5_BULLET_POINTS]",
    "key-findings": [
      {
        "finding": "[FINDING_1]",
        "evidence": "[DATA_SOURCE]",
        "confidence": "high | medium | low"
      }
    ],
    "recommendations": ["[REC_1]", "[REC_2]"],
    "full-report-url": "[URL]",
    "data-recency": "[DATE_OF_LATEST_DATA]"
  },
  "ontology": "competitive-intelligence",
  "protocol": "request-response",
  "conversation-id": "[CONVERSATION_ID]",
  "in-reply-to": "[REQUEST_ID]",
  "timestamp": "[ISO_8601]"
}
```

#### 2. Alerting to Competitive Threat
```json
{
  "performative": "WARN",
  "sender": "market-research-analyst",
  "receiver": ["chief-learning-strategist"],
  "content": {
    "alert-type": "competitive-threat",
    "competitor": "[COMPETITOR_NAME]",
    "action": "[WHAT_THEY_DID]",
    "impact-assessment": "[POTENTIAL_IMPACT_ON_US]",
    "urgency": "immediate | soon | monitor",
    "recommended-response": "[SUGGESTION]"
  },
  "ontology": "competitive-intelligence",
  "protocol": "alert-notification",
  "conversation-id": "pubsub-competitive-alerts",
  "priority": "HIGH",
  "timestamp": "[ISO_8601]"
}
```

### Learning Designer

#### 1. Submitting Course for QA
```json
{
  "performative": "VALIDATE",
  "sender": "learning-designer",
  "receiver": ["qa-specialist"],
  "content": {
    "artifact-type": "course",
    "artifact-id": "[COURSE_ID]",
    "artifact-name": "[COURSE_NAME]",
    "artifact-url": "[PREVIEW_URL]",
    "quality-criteria": ["accessibility", "content-accuracy", "instructional-design", "assessment-alignment"],
    "notes": "[ANY_CONTEXT_FOR_REVIEWER]"
  },
  "ontology": "quality-assurance",
  "protocol": "validation",
  "conversation-id": "conv-qa-[ARTIFACT_ID]",
  "reply-with": "val-[ID]",
  "priority": "MEDIUM",
  "metadata": {
    "deployment-deadline": "[DATE_IF_APPLICABLE]",
    "target-audience": "[PERSONA]"
  }
}
```

#### 2. Querying Behavioral Scientist
```json
{
  "performative": "REQUEST",
  "sender": "learning-designer",
  "receiver": ["behavioral-scientist"],
  "content": {
    "request-type": "behavioral-consultation",
    "challenge": "[SPECIFIC_PROBLEM]",
    "context": {
      "audience": "[PERSONA]",
      "current-performance": "[BASELINE_METRIC]",
      "desired-outcome": "[TARGET_METRIC]"
    },
    "constraints": "[TECHNICAL_OR_RESOURCE_CONSTRAINTS]"
  },
  "ontology": "behavioral-insights",
  "protocol": "request-response",
  "conversation-id": "conv-behavioral-consult-[TOPIC]",
  "reply-with": "req-[ID]",
  "reply-by": "[DEADLINE]"
}
```

### Behavioral Scientist

#### 1. Recommending Intervention
```json
{
  "performative": "PROPOSE",
  "sender": "behavioral-scientist",
  "receiver": ["chief-experience-strategist"],
  "content": {
    "intervention-type": "[TYPE]",
    "intervention-name": "[NAME]",
    "description": "[WHAT_IT_IS]",
    "behavioral-principle": "[WHICH_PRINCIPLE_APPLIED]",
    "expected-impact": {
      "metric": "[METRIC_NAME]",
      "expected-lift": "[PERCENTAGE_OR_ABSOLUTE]",
      "confidence-interval": "[LOWER-UPPER]"
    },
    "evidence": ["[STUDY_1]", "[STUDY_2]", "[INTERNAL_DATA]"],
    "implementation-requirements": {
      "effort": "[TIME_OR_RESOURCES]",
      "technical-feasibility": "easy | moderate | complex",
      "stakeholders": ["[AGENT_1]", "[AGENT_2]"]
    },
    "ethical-review": "passed",
    "ab-test-design": "[URL_TO_TEST_PLAN]"
  },
  "ontology": "behavioral-insights",
  "protocol": "propose-accept",
  "conversation-id": "conv-intervention-[NAME]",
  "reply-with": "prop-[ID]",
  "priority": "MEDIUM"
}
```

#### 2. Warning About Ethical Concern
```json
{
  "performative": "WARN",
  "sender": "behavioral-scientist",
  "receiver": ["chief-experience-strategist", "experience-designer"],
  "content": {
    "concern-type": "ethical-issue",
    "issue": "[SPECIFIC_CONCERN]",
    "affected-feature": "[FEATURE_OR_DESIGN]",
    "ethical-principle-violated": "[TRANSPARENCY_AUTONOMY_ETC]",
    "severity": "critical | high | medium",
    "recommendation": "[WHAT_TO_DO_INSTEAD]"
  },
  "ontology": "ethical-oversight",
  "protocol": "ethics-alert",
  "conversation-id": "conv-ethics-[FEATURE]",
  "priority": "CRITICAL",
  "timestamp": "[ISO_8601]"
}
```

### Data Analyst

#### 1. Delivering Analysis Results
```json
{
  "performative": "INFORM",
  "sender": "data-analyst",
  "receiver": ["[REQUESTING_AGENT]"],
  "content": {
    "analysis-type": "descriptive | diagnostic | predictive | prescriptive",
    "research-question": "[ORIGINAL_QUESTION]",
    "executive-summary": "[KEY_FINDINGS_3-5_BULLETS]",
    "methodology": {
      "data-sources": ["[SOURCE_1]", "[SOURCE_2]"],
      "sample-size": "[N]",
      "techniques": ["[TECHNIQUE_1]"]
    },
    "results": [
      {
        "finding": "[FINDING]",
        "statistic": "[VALUE]",
        "confidence-interval": "[LOWER-UPPER]",
        "p-value": "[VALUE_IF_APPLICABLE]",
        "effect-size": "[COHENS_D_OR_OTHER]"
      }
    ],
    "visualizations": ["[CHART_URL_1]", "[CHART_URL_2]"],
    "recommendations": ["[REC_1]", "[REC_2]"],
    "limitations": "[DATA_QUALITY_OR_SCOPE_LIMITATIONS]",
    "full-report-url": "[URL]"
  },
  "ontology": "learning-analytics",
  "protocol": "request-response",
  "conversation-id": "[CONVERSATION_ID]",
  "in-reply-to": "[REQUEST_ID]",
  "timestamp": "[ISO_8601]"
}
```

#### 2. Alerting to Anomaly
```json
{
  "performative": "WARN",
  "sender": "data-analyst",
  "receiver": ["[RELEVANT_AGENTS]"],
  "content": {
    "alert-type": "metric-anomaly",
    "metric-name": "[METRIC]",
    "current-value": "[VALUE]",
    "expected-range": "[LOWER-UPPER]",
    "deviation": "[PERCENTAGE_OR_ABSOLUTE]",
    "affected-entity": "[COURSE_COHORT_SEGMENT]",
    "timeframe": "[WHEN_DETECTED]",
    "possible-causes": ["[HYPOTHESIS_1]", "[HYPOTHESIS_2]"],
    "recommended-action": "[INVESTIGATE_FIX_MONITOR]"
  },
  "ontology": "learning-analytics",
  "protocol": "alert-notification",
  "conversation-id": "pubsub-metric-alerts",
  "priority": "HIGH",
  "timestamp": "[ISO_8601]"
}
```

### Community Manager

#### 1. Escalating Community Crisis
```json
{
  "performative": "ESCALATE",
  "sender": "community-manager",
  "receiver": ["chief-community-strategist"],
  "content": {
    "incident-type": "moderation-crisis | sentiment-crisis | participation-crisis",
    "severity": "CRITICAL | HIGH",
    "description": "[WHAT_HAPPENED]",
    "incident-id": "[ID]",
    "affected-scope": "[NUMBER_OF_STUDENTS_OR_COURSES]",
    "actions-taken": ["[ACTION_1]", "[ACTION_2]"],
    "current-status": "[CONTAINED_ESCALATING_RESOLVED]",
    "recommendation": "[WHAT_LEADERSHIP_SHOULD_DO]",
    "urgency": "[IMMEDIATE_WITHIN_24H_ETC]"
  },
  "ontology": "community-engagement",
  "protocol": "escalation",
  "conversation-id": "conv-crisis-[INCIDENT_ID]",
  "priority": "CRITICAL",
  "timestamp": "[ISO_8601]"
}
```

#### 2. Requesting Advocate Recognition
```json
{
  "performative": "REQUEST",
  "sender": "community-manager",
  "receiver": ["data-analyst"],
  "content": {
    "request-type": "advocate-identification",
    "criteria": {
      "min-contributions": "[NUMBER]",
      "min-helpfulness-score": "[SCORE]",
      "timeframe": "[PERIOD]",
      "segment": "[ALL_OR_SPECIFIC_COHORT]"
    },
    "deliverable": "List of top contributors with stats for recognition program"
  },
  "ontology": "community-engagement",
  "protocol": "request-response",
  "conversation-id": "conv-advocate-recognition-[MONTH]",
  "reply-with": "req-[ID]",
  "reply-by": "[DEADLINE]"
}
```

### Quality Assurance Specialist

#### 1. Rejecting Artifact with Issues
```json
{
  "performative": "REJECT",
  "sender": "qa-specialist",
  "receiver": ["[SUBMITTING_AGENT]"],
  "content": {
    "decision": "FAIL | CONDITIONAL PASS",
    "artifact-id": "[ID]",
    "quality-score": "[0-100]",
    "critical-issues": [
      {
        "id": "[ISSUE_ID]",
        "type": "[CATEGORY]",
        "severity": "CRITICAL",
        "description": "[WHAT_IS_WRONG]",
        "location": "[WHERE_IN_ARTIFACT]",
        "fix-guidance": "[HOW_TO_FIX]"
      }
    ],
    "minor-issues": [
      {
        "id": "[ISSUE_ID]",
        "type": "[CATEGORY]",
        "severity": "MINOR",
        "description": "[WHAT_COULD_BE_BETTER]",
        "recommendation": "[SUGGESTION]"
      }
    ],
    "conditions": "[WHAT_MUST_BE_FIXED_FOR_APPROVAL]",
    "re-review-required": true
  },
  "ontology": "quality-assurance",
  "protocol": "validation",
  "conversation-id": "[CONVERSATION_ID]",
  "in-reply-to": "[VALIDATION_REQUEST_ID]",
  "timestamp": "[ISO_8601]"
}
```

#### 2. Approving Artifact
```json
{
  "performative": "APPROVE",
  "sender": "qa-specialist",
  "receiver": ["[SUBMITTING_AGENT]"],
  "content": {
    "decision": "PASS",
    "artifact-id": "[ID]",
    "quality-score": "[0-100]",
    "strengths": ["[POSITIVE_1]", "[POSITIVE_2]"],
    "approval-conditions": "None. Ready for deployment.",
    "recommendations": ["[OPTIONAL_IMPROVEMENT_1]"],
    "commendations": "[POSITIVE_FEEDBACK]"
  },
  "ontology": "quality-assurance",
  "protocol": "validation",
  "conversation-id": "[CONVERSATION_ID]",
  "in-reply-to": "[VALIDATION_REQUEST_ID]",
  "timestamp": "[ISO_8601]"
}
```

---

## Error Handling in Communication

### 1. Message Delivery Failures

**Problem**: Receiver agent is unavailable or message fails to deliver

**Solution**: Dead Letter Queue + Retry Logic

```json
// Original message fails to deliver
{
  "performative": "REQUEST",
  "sender": "chief-learning-strategist",
  "receiver": ["market-research-analyst"],  // UNAVAILABLE
  "content": "...",
  "conversation-id": "conv-001",
  "delivery-attempts": 1,
  "max-delivery-attempts": 3
}

// After 3 failed attempts → Dead Letter Queue
{
  "performative": "FAILURE",
  "sender": "message-broker",
  "receiver": ["chief-learning-strategist"],
  "content": {
    "failure-type": "delivery-failure",
    "original-message-id": "msg-001",
    "intended-receiver": "market-research-analyst",
    "attempts": 3,
    "last-error": "Agent unavailable: timeout after 30s",
    "recommendation": "Check agent status or contact human operator"
  },
  "ontology": "operational-coordination",
  "priority": "HIGH",
  "timestamp": "[ISO_8601]"
}
```

### 2. Timeout Handling

**Problem**: Agent doesn't respond within expected timeframe

**Solution**: Timeout + Notification

```json
// Request with deadline
{
  "performative": "REQUEST",
  "sender": "learning-designer",
  "receiver": ["data-analyst"],
  "content": "Analyze engagement for course-123",
  "conversation-id": "conv-002",
  "reply-with": "req-002",
  "reply-by": "2024-10-24T12:00:00Z",  // DEADLINE
  "timeout-action": "notify-sender"
}

// If no response by deadline
{
  "performative": "WARN",
  "sender": "message-broker",
  "receiver": ["learning-designer"],
  "content": {
    "warning-type": "timeout",
    "original-request-id": "req-002",
    "requested-agent": "data-analyst",
    "reply-by": "2024-10-24T12:00:00Z",
    "current-time": "2024-10-24T12:15:00Z",
    "recommendation": "Follow up directly or cancel request"
  },
  "ontology": "operational-coordination",
  "priority": "MEDIUM",
  "timestamp": "2024-10-24T12:15:00Z"
}
```

### 3. Malformed Message Handling

**Problem**: Message doesn't conform to FIPA ACL standard

**Solution**: Validation + Error Response

```json
// Malformed message (missing required field)
{
  "performative": "REQUEST",
  "sender": "learning-designer",
  // MISSING "receiver" field
  "content": "...",
  "conversation-id": "conv-003"
}

// Validation error response
{
  "performative": "FAILURE",
  "sender": "message-broker",
  "receiver": ["learning-designer"],
  "content": {
    "failure-type": "validation-error",
    "original-message-id": "msg-003",
    "errors": [
      {
        "field": "receiver",
        "error": "Required field missing",
        "fix": "Add 'receiver' array with at least one agent ID"
      }
    ],
    "message-rejected": true
  },
  "ontology": "operational-coordination",
  "priority": "LOW",
  "timestamp": "[ISO_8601]"
}
```

### 4. Conversation Tracking Errors

**Problem**: Message references unknown conversation

**Solution**: Conversation Not Found Error

```json
// Message with unknown conversation-id
{
  "performative": "INFORM",
  "sender": "data-analyst",
  "receiver": ["learning-designer"],
  "content": "Analysis results: ...",
  "conversation-id": "conv-unknown-999",  // NOT FOUND
  "in-reply-to": "req-999"
}

// Error response
{
  "performative": "WARN",
  "sender": "message-broker",
  "receiver": ["data-analyst"],
  "content": {
    "warning-type": "conversation-not-found",
    "conversation-id": "conv-unknown-999",
    "recommendation": "Verify conversation ID or start new conversation"
  },
  "ontology": "operational-coordination",
  "priority": "LOW",
  "timestamp": "[ISO_8601]"
}
```

---

## Implementation Guidelines

### 1. Message Broker Architecture

**Centralized vs Peer-to-Peer**:
- **Recommended**: Centralized message broker for our agency
- **Benefits**: Central logging, routing, validation, retry logic, dead letter queue
- **Technology Options**: RabbitMQ, Apache Kafka, AWS SQS + SNS, Google Pub/Sub

**Message Broker Responsibilities**:
1. **Validation**: Check FIPA ACL format compliance
2. **Routing**: Deliver messages to correct recipient(s)
3. **Logging**: Audit trail of all messages
4. **Retry**: Handle delivery failures
5. **Priority Queue**: CRITICAL messages processed first
6. **Pub/Sub Management**: Subscription registry and filtering
7. **Monitoring**: Track message throughput and latency

### 2. Agent Implementation

**Every agent must implement**:

```python
class Agent:
    def __init__(self, agent_id, message_broker):
        self.agent_id = agent_id
        self.broker = message_broker
        self.subscriptions = []

    def send_message(self, message):
        """Send FIPA ACL message via broker"""
        # Validate message format
        self.validate_fipa_acl(message)
        # Add sender ID
        message['sender'] = self.agent_id
        # Add timestamp
        message['timestamp'] = datetime.now().isoformat()
        # Send via broker
        self.broker.send(message)

    def receive_message(self, message):
        """Receive and route incoming message based on performative"""
        performative = message['performative']

        if performative == 'REQUEST':
            self.handle_request(message)
        elif performative == 'INFORM':
            self.handle_inform(message)
        elif performative == 'PROPOSE':
            self.handle_propose(message)
        # ... etc for all performatives

    def handle_request(self, message):
        """Subclass implements specific logic"""
        raise NotImplementedError

    def subscribe(self, ontology, filters=None):
        """Subscribe to pub/sub topic"""
        self.broker.subscribe(self.agent_id, ontology, filters)
        self.subscriptions.append(ontology)
```

### 3. Conversation Management

**Conversation ID Format**: `conv-[TOPIC]-[DATE]-[SEQUENCE]`
- Example: `conv-pricing-analysis-2024-1024-001`

**Conversation State Tracking**:
```python
conversation_state = {
    'conversation-id': 'conv-001',
    'participants': ['agent-1', 'agent-2'],
    'initiated-by': 'agent-1',
    'started-at': '2024-10-24T10:00:00Z',
    'protocol': 'request-response',
    'status': 'active | completed | abandoned',
    'message-history': [
        {'message-id': 'msg-001', 'performative': 'REQUEST', ...},
        {'message-id': 'msg-002', 'performative': 'AGREE', ...}
    ],
    'awaiting-response-from': 'agent-2',
    'last-activity': '2024-10-24T10:05:00Z'
}
```

### 4. Logging and Monitoring

**Log Every Message**:
```json
{
  "log-id": "log-2024-1024-100001",
  "timestamp": "2024-10-24T10:00:00Z",
  "direction": "sent | received",
  "message": {
    "performative": "REQUEST",
    "sender": "chief-learning-strategist",
    "receiver": ["market-research-analyst"],
    "conversation-id": "conv-001",
    // ... full message
  },
  "delivery-status": "delivered | pending | failed",
  "delivery-latency-ms": 45
}
```

**Monitoring Dashboards**:
1. **Message Throughput**: Messages per minute/hour by performative type
2. **Delivery Success Rate**: % of messages delivered successfully
3. **Average Latency**: Time from send to receive
4. **Active Conversations**: Count and age distribution
5. **Error Rate**: Failed deliveries, validation errors, timeouts
6. **Agent Health**: Each agent's message send/receive rates

### 5. Security Considerations

**Authentication**:
- Every message must have valid sender ID
- Broker validates sender identity (token/certificate)

**Authorization**:
- Agents can only send messages as themselves
- Agents can only receive messages addressed to them (or pub/sub subscriptions)

**Encryption**:
- Messages containing sensitive data should be encrypted in transit (TLS)
- Consider message-level encryption for highly sensitive content

**Rate Limiting**:
- Prevent message flooding (max 100 messages/minute per agent)
- Different limits for different performatives (e.g., INFORM unlimited, REQUEST limited)

### 6. Testing Communication

**Unit Tests**:
```python
def test_send_request_message():
    agent = ChiefLearningStrategist()
    message = agent.create_request(
        receiver='market-research-analyst',
        content='Analyze competitor pricing',
        ontology='competitive-intelligence'
    )

    assert message['performative'] == 'REQUEST'
    assert message['sender'] == 'chief-learning-strategist'
    assert 'conversation-id' in message
    assert 'timestamp' in message
```

**Integration Tests**:
```python
def test_request_response_flow():
    cls = ChiefLearningStrategist()
    mra = MarketResearchAnalyst()

    # CLS sends request
    request = cls.request_research('competitor pricing')

    # MRA receives and agrees
    agree = mra.receive_message(request)
    assert agree['performative'] == 'AGREE'

    # MRA sends results
    results = mra.send_research_results(request['conversation-id'])

    # CLS receives results
    cls.receive_message(results)
    assert cls.conversations[request['conversation-id']]['status'] == 'completed'
```

---

## Summary

This FIPA ACL Communication Protocol provides:

1. ✅ **Standardized Message Format**: All agents use same structure
2. ✅ **Clear Semantics**: Performatives make intent explicit
3. ✅ **Flexible Protocols**: Request-response, pub/sub, validation, escalation, etc.
4. ✅ **Robust Error Handling**: Timeouts, delivery failures, validation errors
5. ✅ **Auditability**: Complete message logging and conversation tracking
6. ✅ **Scalability**: Message broker handles routing and load
7. ✅ **Security**: Authentication, authorization, encryption

**Next Steps**:
- ✅ **COMPLETE**: Agent Specifications
- ✅ **COMPLETE**: FIPA ACL Communication Protocol
- ⏭️ **NEXT**: Implementation Templates (memory, error handling, logging)
- **THEN**: Security & Privacy Implementation Plan
- **FINALLY**: Testing & Validation Framework

---
