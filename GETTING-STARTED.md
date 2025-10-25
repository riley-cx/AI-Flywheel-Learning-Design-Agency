# Getting Started with AI Flywheel Agency
## Your Multi-Agent Learning Design System

**Welcome!** You now have the foundation of a powerful multi-agent system. Here's what exists and how to proceed.

---

## ✅ What's Been Built (Foundation Complete!)

### 1. **Core Agent Framework** ✅
Located in: `agents/base/`

**`agent.py`** - The heart of the system
- `BaseAgent` class that all agents inherit from
- Integration with Claude API for reasoning
- Tool use capability (ready for MCP)
- Message passing between agents
- Context management
- Three specialized base classes:
  - `ChiefAgent` - for strategic coordinators
  - `SpecialistAgent` - for domain experts
  - `ExecutionAgent` - for implementers

**`context.py`** - Smart context management
- Loads shared context (the hymn book)
- Loads domain expertise per agent
- Retrieves relevant memory
- Manages token limits
- Just-in-time retrieval (Anthropic best practice)

**`messaging.py`** - Inter-agent communication
- Message class with multiple types (request, response, inform, etc.)
- MessageBus for routing messages between agents
- Conversation tracking
- Message logging and history

### 2. **Shared Context (The Hymn Book)** ✅
Located in: `shared-context/`

**`strategic-objectives.md`** - Everyone sings from this!
- Current Q4 2024 goals
- Strategic priorities (ranked 1-4)
- Brand positioning
- Target student personas
- Success metrics
- What we're NOT focusing on
- Key dates and milestones

This ensures all agents are aligned on:
- What we're trying to achieve
- Who we serve
- How we communicate
- What "good" looks like

### 3. **First Agent Definition** ✅
Located in: `agents/definitions/`

**`chief_learning_strategist.yaml`** - Complete example
- Full system prompt (role, expertise, decision framework)
- Tool access permissions
- Coordination capabilities
- Success metrics
- Proactive behaviors
- Escalation rules

This serves as the template for the other 9 agents.

### 4. **Project Infrastructure** ✅

**`requirements.txt`** - All Python dependencies
- Anthropic Claude API
- Database connectors (PostgreSQL, Redis)
- Vector database (ChromaDB for semantic memory)
- Web framework (FastAPI)
- CLI tools (Click, Rich)
- Testing frameworks
- Everything you need!

**`.env.example`** - Configuration template
- API keys
- Database settings
- Agent configuration
- MCP server settings
- Feature flags
- Comprehensive and well-documented

**`start-agency.sh`** - Startup script (ready to enhance)
- Pre-flight checks
- Service startup
- Agent initialization
- Status reporting

### 5. **Documentation** ✅

**`README.md`** - Project overview
**`REVISED-ARCHITECTURE.md`** - Complete architecture explanation
**`PROJECT-STRUCTURE.md`** - File organization guide
**`GETTING-STARTED.md`** - This file!

Plus your original 3 specification documents.

---

## 🎯 What This Gives You

### A Working Foundation
You can now:
1. Define agents with YAML configs
2. Agents load shared context automatically
3. Agents can message each other
4. Agents reason using Claude API
5. Context is managed efficiently

### The "Hymn Book" Concept
All agents read `shared-context/` on startup, ensuring:
- Strategic alignment
- Consistent brand voice
- Shared understanding of goals
- Common quality standards

### Extensible Architecture
Easy to:
- Add new agents (just create YAML + optional custom logic)
- Add new tools (via MCP servers)
- Update shared context (all agents get it)
- Track all interactions (message bus logs everything)

---

## 🚀 Next Steps (In Order)

### Phase 1: Complete the Agent Definitions (1-2 days)

**Task**: Create the remaining 9 agent YAML files

**Template to follow**: `chief_learning_strategist.yaml`

**The 9 agents to create**:
1. `chief_experience_strategist.yaml`
2. `chief_community_strategist.yaml`
3. `market_research_analyst.yaml`
4. `learning_designer.yaml`
5. `behavioral_scientist.yaml`
6. `experience_designer.yaml`
7. `community_manager.yaml`
8. `data_analyst.yaml`
9. `quality_assurance_specialist.yaml`

**For each agent, define**:
- System prompt (role, expertise, decision framework)
- Context files they load
- Tools they can use
- Who can call them
- Who they can coordinate
- Memory configuration
- Success metrics
- Proactive behaviors

**Tip**: Reference the original specifications for each agent's responsibilities.

---

### Phase 2: Complete Shared Context (1 day)

**Task**: Create the remaining shared context files

**Files needed in `shared-context/`**:
1. `brand-voice.md` - How we communicate
   - Tone and style guidelines
   - Example good/bad communications
   - Key phrases and terminology

2. `quality-standards.md` - What "excellent" looks like
   - Course quality criteria
   - Code quality standards
   - Accessibility requirements (WCAG 2.1 AA)
   - Assessment standards

3. `student-personas.md` - Detailed personas
   - Expand on the 3 personas from strategic objectives
   - Demographics, goals, pain points
   - How each persona learns best
   - Success criteria per persona

4. `success-metrics.md` - How we measure everything
   - Detailed KPI definitions
   - Measurement methodologies
   - Dashboards and reports
   - Thresholds for alerts

5. `current-initiatives.md` - What's in flight
   - Active projects
   - Owners and timelines
   - Dependencies
   - Status updates (keep this current!)

---

### Phase 3: Implement Memory System (2-3 days)

**Task**: Build `agents/base/memory.py`

**What it needs**:
```python
class MemoryManager:
    """
    Manages agent memory (short-term + long-term)

    Short-term: In-memory (current session)
    Long-term: PostgreSQL + ChromaDB (persistent)
    """

    def __init__(self, agent_id: str):
        pass

    def store_interaction(self, message, response, conversation_id):
        """Store interaction for learning"""
        pass

    def retrieve_relevant(self, query: str, limit: int = 5):
        """Semantic search for relevant past context"""
        pass

    def consolidate(self):
        """Move short-term to long-term, summarize"""
        pass
```

**Components**:
1. **Short-term memory**: Python dict/list (volatile)
2. **Long-term memory**: PostgreSQL for structured data
3. **Semantic memory**: ChromaDB for similarity search
4. **Consolidation**: Periodic summarization

**Reference**: `AI-Flywheel-Implementation-Templates.md` (lines 56-385) has detailed memory code

---

### Phase 4: Build First MCP Server (3-4 days)

**Task**: Implement Learning Analytics MCP server

**Location**: `mcp-servers/learning-analytics/`

**What it needs**:
```
learning-analytics/
├── server.py          # MCP server implementation
├── tools.py           # Tool definitions
└── queries/           # SQL queries
    ├── course_metrics.sql
    ├── cohort_analysis.sql
    └── engagement_patterns.sql
```

**Tools to implement** (from agent definitions):
1. `get_course_metrics(course_id, metric_type, date_range)`
2. `analyze_student_cohort(filters)`
3. `query_engagement_data(date_range, segment)`
4. `get_completion_rates(segment, filters)`
5. `predict_student_outcomes(student_id, model_type)`

**For now**: Use mock data (don't need real database yet)

**MCP Protocol**: Follow Anthropic's MCP specification
- Tool registration
- Parameter validation
- Result formatting
- Error handling

---

### Phase 5: Build Orchestrator (2-3 days)

**Task**: Create `orchestrator/coordinator.py`

**What it needs**:
```python
class AgentCoordinator:
    """
    Coordinates multi-agent workflows
    """

    def __init__(self):
        self.agents = {}  # All active agents
        self.message_bus = MessageBus()

    def register_agent(self, agent):
        """Add agent to the system"""
        pass

    def execute_workflow(self, workflow_name, params):
        """Run a predefined workflow"""
        pass

    def start_all_agents(self):
        """Initialize all 10 agents"""
        pass
```

**Workflows to support**:
- `/new-course` - Full course creation pipeline
- `/analyze-engagement` - Diagnose and fix issues
- `/quarterly-planning` - Strategic review

---

### Phase 6: Create CLI Interface (2-3 days)

**Task**: Build `cli/main.py`

**What it should do**:
```bash
./agency-cli

AI Flywheel Agency - Command Center
Type 'help' for available commands

> status all
✅ Chief Learning Strategist: Healthy (0 errors, 12.3MB memory)
✅ Learning Designer: Healthy (0 errors, 8.7MB memory)
... (all 10 agents)

> /new-course topic="AI Safety" audience="ML Engineers"
🎯 Chief Learning Strategist coordinating...
📊 Market Research Analyst: Analyzing demand...
... (workflow progress)

> help
Available commands:
- status [agent|all]     : Check agent health
- /new-course           : Create new course
- /analyze-engagement   : Fix engagement issues
...
```

**Use**: Click for CLI framework, Rich for beautiful output

---

## 📅 Timeline Summary

**Week 1** (Foundation - ✅ DONE!)
- ✅ Agent framework
- ✅ Context system
- ✅ Messaging
- ✅ First agent definition
- ✅ Shared context started

**Week 2** (Agents & Context)
- Create 9 more agent definitions
- Complete shared context files
- Test agent initialization

**Week 3** (Memory & First MCP)
- Implement memory system
- Build Learning Analytics MCP
- Test agents with mock data

**Week 4** (Orchestration)
- Build remaining 4 MCP servers
- Create orchestrator
- Implement first workflow

**Week 5** (Interface & Testing)
- Build CLI
- End-to-end workflow testing
- Bug fixes

**Week 6** (Polish & Launch)
- Documentation
- Error handling improvements
- First real use cases!

---

## 🛠️ Development Workflow

### Daily Development Cycle

**1. Morning**
```bash
cd ai-flywheel-agency
source venv/bin/activate
git pull
```

**2. Make changes**
```bash
# Edit files
# Test locally
python -m pytest tests/
```

**3. Commit progress**
```bash
git add .
git commit -m "Implemented X"
git push
```

**4. Track progress**
Update: `shared-context/current-initiatives.md`

### Testing as You Go

**Unit tests** (per component):
```bash
pytest tests/unit/test_agent.py
pytest tests/unit/test_memory.py
```

**Integration tests** (workflows):
```bash
pytest tests/integration/test_new_course_workflow.py
```

**Manual testing**:
```python
# Quick test script
from agents.base.agent import BaseAgent

agent = BaseAgent('test-agent', 'agents/definitions/learning_designer.yaml')
agent.start()
```

---

## 💡 Tips for Success

### 1. Start Simple, Then Enhance
- Get basic versions working first
- Add sophistication incrementally
- Don't try to perfect everything at once

### 2. Use the Specifications
Your original spec documents are gold:
- Agent responsibilities and interfaces
- FIPA ACL message formats
- Memory system architecture
- Implementation code templates

Reference them constantly!

### 3. Test with Mock Data First
- Don't wait for real databases
- Use hardcoded responses initially
- Focus on workflows, not data plumbing
- Replace mocks incrementally

### 4. Keep Shared Context Current
- Update `strategic-objectives.md` as goals change
- Keep `current-initiatives.md` fresh
- Agents are only as aligned as the hymn book!

### 5. Leverage Claude Code
- Use Claude Code to help build this system
- Ask: "Implement the memory consolidation method following the spec"
- Have Claude review your agent definitions
- Use it to generate test cases

---

## 🐛 Common Issues & Solutions

### Issue: "Agent not found"
**Cause**: Agent not registered with message bus
**Fix**: Call `agent.start()` before sending messages

### Issue: "Context too large"
**Cause**: Loading too much into context
**Fix**: Implement context compression in `context.py`

### Issue: "Tool not found"
**Cause**: MCP server not running or tool not registered
**Fix**: Check MCP server status, verify tool definitions

### Issue: "Memory not persisting"
**Cause**: Memory system not fully implemented
**Fix**: Complete `memory.py` implementation

---

## 📚 Key Files Reference

**Most Important Files**:
1. `agents/base/agent.py` - How agents work
2. `shared-context/strategic-objectives.md` - The hymn book
3. `agents/definitions/*.yaml` - Agent personalities
4. `README.md` - Project overview

**When stuck, read**:
- `REVISED-ARCHITECTURE.md` - Understand the design
- Original specs - Detailed requirements
- Anthropic's best practices docs

---

## 🎉 You're Ready!

You have:
- ✅ Solid foundation built
- ✅ Clear architecture
- ✅ Detailed roadmap
- ✅ All the tools needed

**Next action**: Create the 9 remaining agent YAML files using `chief_learning_strategist.yaml` as your template.

**Questions?** Reference the docs or ask Claude Code for help!

**Let's build something amazing! 🚀**

---

*Created: 2025-10-25*
*Status: Foundation Complete, Ready for Phase 1*
