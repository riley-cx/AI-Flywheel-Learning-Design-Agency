# AI Flywheel Agency - Project Structure
## Complete File Organization

```
ai-flywheel-agency/
│
├── .env                                    # Configuration
├── .env.example                           # Template
├── requirements.txt                       # Python dependencies
├── start-agency.sh                        # Startup script ✅
├── stop-agency.sh                         # Shutdown script
├── README.md                              # Getting started
│
├── .claude/                               # Claude Code integration
│   ├── commands/                          # Slash commands
│   │   ├── new-course.md                 # /new-course workflow
│   │   ├── analyze-engagement.md         # /analyze-engagement
│   │   ├── optimize-experience.md        # /optimize-experience
│   │   ├── design-intervention.md        # /design-intervention
│   │   ├── community-campaign.md         # /community-campaign
│   │   ├── quality-review.md             # /quality-review
│   │   └── quarterly-planning.md         # /quarterly-planning
│   │
│   └── expertise/                         # Domain knowledge (shared context)
│       ├── learning-design.md            # Instructional design expertise
│       ├── behavioral-science.md         # Psychology & motivation
│       ├── ux-design.md                  # UX/UI best practices
│       └── community-strategy.md         # Community building
│
├── shared-context/                        # THE HYMN BOOK (all agents read this)
│   ├── strategic-objectives.md           # Current goals & priorities
│   ├── brand-voice.md                    # Communication standards
│   ├── quality-standards.md              # What "good" looks like
│   ├── student-personas.md               # Who we serve
│   ├── success-metrics.md                # KPIs we optimize for
│   └── current-initiatives.md            # Active projects
│
├── agents/                                # The Agent System
│   ├── __init__.py
│   │
│   ├── base/                             # Base framework
│   │   ├── __init__.py
│   │   ├── agent.py                      # BaseAgent class
│   │   ├── memory.py                     # MemoryManager
│   │   ├── context.py                    # ContextBuilder
│   │   ├── messaging.py                  # Agent-to-agent messages
│   │   └── errors.py                     # Error handling
│   │
│   ├── definitions/                      # Agent "DNA"
│   │   ├── chief_learning_strategist.yaml
│   │   ├── chief_experience_strategist.yaml
│   │   ├── chief_community_strategist.yaml
│   │   ├── market_research_analyst.yaml
│   │   ├── learning_designer.yaml
│   │   ├── behavioral_scientist.yaml
│   │   ├── experience_designer.yaml
│   │   ├── community_manager.yaml
│   │   ├── data_analyst.yaml
│   │   └── quality_assurance_specialist.yaml
│   │
│   ├── implementations/                  # Agent-specific code
│   │   ├── __init__.py
│   │   ├── chief_learning_strategist.py
│   │   ├── learning_designer.py
│   │   ├── data_analyst.py
│   │   └── ... (10 total)
│   │
│   └── server.py                         # Agent server (runs all agents)
│
├── mcp-servers/                          # The 5 MCP Tool Servers
│   ├── learning-analytics/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── tools.py
│   │   └── queries/
│   │       ├── course_metrics.sql
│   │       ├── cohort_analysis.sql
│   │       └── engagement_patterns.sql
│   │
│   ├── market-intelligence/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── tools.py
│   │   ├── scrapers/
│   │   └── apis/
│   │
│   ├── content-management/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── tools.py
│   │   └── templates/
│   │
│   ├── community-platform/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── tools.py
│   │
│   └── quality-validation/
│       ├── __init__.py
│       ├── server.py
│       ├── tools.py
│       └── validators/
│           ├── accessibility.py
│           ├── cognitive_load.py
│           └── objectives.py
│
├── orchestrator/                         # Coordination layer
│   ├── __init__.py
│   ├── coordinator.py                   # Routes messages between agents
│   ├── workflows.py                     # Pre-defined workflows
│   └── scheduler.py                     # Background tasks
│
├── cli/                                 # Command-line interface
│   ├── __init__.py
│   ├── main.py                          # CLI entry point
│   ├── commands.py                      # CLI commands
│   └── display.py                       # Pretty output
│
├── api/                                 # Web API (optional)
│   ├── __init__.py
│   └── main.py                          # FastAPI server
│
├── data/                                # Data storage
│   ├── memory/                          # Agent memory stores
│   │   ├── chief-learning-strategist/
│   │   ├── learning-designer/
│   │   └── ... (per agent)
│   ├── shared/                          # Shared knowledge base
│   ├── courses/                         # Course content
│   └── analytics/                       # Cached analytics
│
├── logs/                                # Log files
│   ├── agents/
│   │   ├── chief-learning-strategist.log
│   │   └── ... (per agent)
│   ├── mcp-servers/
│   └── system.log
│
├── tests/                               # Test suite
│   ├── unit/
│   │   ├── test_agents/
│   │   └── test_mcp_servers/
│   ├── integration/
│   │   ├── test_workflows/
│   │   └── test_agent_coordination/
│   └── fixtures/
│
├── scripts/                             # Utility scripts
│   ├── init_database.py                # Setup database
│   ├── seed_data.py                    # Load sample data
│   ├── generate_keys.py                # Security keys
│   └── backup.py                       # Backup system
│
└── docs/                                # Documentation
    ├── specifications/                  # Original specs ✅
    ├── architecture/                    # Architecture docs
    ├── api/                            # API documentation
    └── guides/                         # User guides
```

## Key Components Explained

### **shared-context/** - The Hymn Book
- All agents read these files on startup and when context changes
- Ensures everyone is aligned on goals, standards, voice
- Updated by Chief Learning Strategist or you

### **agents/definitions/** - Agent DNA
- YAML files defining each agent's:
  - System prompt (role & expertise)
  - Tools they can use
  - Who can call them
  - Memory settings
  - Success metrics

### **agents/implementations/** - Agent Code
- Python classes inheriting from BaseAgent
- Agent-specific logic and behaviors
- How they use tools and make decisions

### **mcp-servers/** - The Tools
- 5 specialized servers providing data access
- Standard MCP protocol
- Agents call these for capabilities

### **orchestrator/** - The Coordinator
- Routes messages between agents
- Manages workflows
- Handles background tasks

### **data/memory/** - Individual Context
- Each agent has their own memory store
- Persistent across sessions
- Learns from experience

---

## How Context Works

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT CONTEXT BUILDER                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SHARED CONTEXT (Everyone reads)                         │
│     ├─ Strategic objectives                                 │
│     ├─ Brand voice & values                                 │
│     ├─ Quality standards                                    │
│     ├─ Student personas                                     │
│     └─ Current initiatives                                  │
│                                                              │
│  2. DOMAIN EXPERTISE (Role-specific)                        │
│     └─ Learning Designer reads: learning-design.md          │
│                                                              │
│  3. PERSONAL MEMORY (Individual)                            │
│     └─ Past courses designed, patterns learned              │
│                                                              │
│  4. CURRENT MESSAGE (The task at hand)                      │
│     └─ "Design a course on AI Safety for ML engineers"      │
│                                                              │
│  5. TOOL ACCESS (What they can do)                          │
│     ├─ get_course_metrics()                                 │
│     ├─ create_course_structure()                            │
│     └─ validate_cognitive_load()                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
              Full context sent to Claude API
                           ↓
              Agent reasons and takes action
```
