# AI Flywheel Elite Learning Design Agency
## Multi-Agent System for World-Class Course Creation

**Status**: ✅ Phase 2 Complete - Memory System Implemented!
**Architecture**: Agent-based system following Anthropic best practices
**Version**: 0.2.0

---

## 🎯 What Is This?

A multi-agent AI system that works like an elite learning design agency:
- **10 specialized AI agents** (strategists, designers, analysts, specialists)
- **Shared context** ("hymn book") - all agents aligned on goals, standards, voice
- **Individual expertise** - each agent has deep domain knowledge
- **Autonomous collaboration** - agents work together with minimal human intervention
- **Persistent memory** - agents learn and improve over time

## ✅ What's Built (So Far)

### Core Framework
- [x] **Base Agent Framework** (`agents/base/agent.py`)
  - BaseAgent class all agents inherit from
  - Integration with Claude API for reasoning
  - Tool use capability (MCP)
  - Memory management
  - Message passing

- [x] **Memory System** (`agents/base/memory.py`) ✨ NEW!
  - ShortTermMemory (in-memory, LRU eviction)
  - LongTermMemory (SQLite + ChromaDB)
  - MemoryManager (unified interface)
  - Semantic search for relevant context
  - Decision tracking and learning
  - Pattern recognition
  - Conversation history
  - Comprehensive test suite

- [x] **Context Builder** (`agents/base/context.py`)
  - Loads shared context (the hymn book)
  - Loads domain expertise
  - Retrieves relevant memory
  - Manages token limits

- [x] **Messaging System** (`agents/base/messaging.py`)
  - Agent-to-agent communication
  - Conversation tracking
  - Message bus for routing
  - Multiple message types (request, response, inform, etc.)

### Shared Context (The Hymn Book)
- [x] **Strategic Objectives** (`shared-context/strategic-objectives.md`)
  - Current goals and priorities
  - Target personas
  - Success metrics
  - What we're focusing on (and NOT focusing on)

### All 10 Agent Definitions ✅ COMPLETE!
- [x] **Chief Learning Strategist** - Strategic leader and orchestrator
- [x] **Chief Experience Strategist** - UX and experience strategy
- [x] **Chief Community Strategist** - Community building and engagement
- [x] **Market Research Analyst** - Competitive intelligence and trends
- [x] **Learning Designer** - Instructional design and course creation
- [x] **Behavioral Scientist** - Psychology and motivation expert
- [x] **Data Analyst** - Internal analytics and insights
- [x] **Experience Designer** - UX/UI implementation
- [x] **Community Manager** - Community execution and moderation
- [x] **Quality Assurance Specialist** - Quality validation and standards

Each agent has:
- Complete system prompt (role, expertise, decision framework)
- Context files they load (shared + domain expertise)
- MCP tools they can use
- Coordination capabilities
- Success metrics
- Proactive behaviors

### Documentation
- [x] **Revised Architecture** (REVISED-ARCHITECTURE.md)
- [x] **Project Structure** (PROJECT-STRUCTURE.md)
- [x] **Decision Log** (DECISION-LOG.md) ✨ NEW!
- [x] **Memory System Guide** (MEMORY-SYSTEM-COMPLETE.md) ✨ NEW!
- [x] **Changelog** (CHANGELOG.md) ✨ NEW!
- [x] **Original Specifications** (3 comprehensive spec documents)

---

## 🏗️ What's Next

### ✅ Completed (Phase 1)
1. ✅ **All 10 agent definitions** (YAML files complete!)
2. ✅ **Base agent framework** (agent.py, context.py, messaging.py)
3. ✅ **Shared context** (strategic-objectives.md)
4. ✅ **Requirements.txt** and .env.example
5. ✅ **Complete documentation**

### ✅ Completed (Phase 2)
1. ✅ **Memory system implemented** (memory.py with full two-tier architecture)
2. ✅ **Comprehensive test suite** (test_memory.py)
3. ✅ **Decision log created** (all architectural decisions documented)
4. ✅ **Changelog maintained** (version 0.2.0)
5. ✅ **Complete documentation** (MEMORY-SYSTEM-COMPLETE.md)

### Next (Phase 3 - MCP Servers & Complete Context)
1. **Complete shared context files** (4 more .md files needed)
2. **Build first MCP server** (Learning Analytics)
3. **Test full agent workflow** with memory and tools
4. **Build remaining MCP servers** (Market Intelligence, Content Management, etc.)

### Short-term (Next 2-3 Weeks)
1. **Build all 5 MCP servers**
   - Learning Analytics
   - Market Intelligence
   - Content Management
   - Community Platform
   - Quality Validation

2. **Implement orchestrator**
   - Workflow coordination
   - Background tasks
   - Scheduling

3. **Create CLI interface**
   - Interactive shell
   - Slash commands
   - Status displays

### Medium-term (Weeks 4-6)
1. **Memory implementation** (persistent storage)
2. **Complete agent implementations** (agent-specific logic)
3. **Workflow testing** (end-to-end scenarios)
4. **Web dashboard** (optional monitoring UI)

---

## 🚀 Quick Start (When Ready)

```bash
# 1. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Initialize
python scripts/init_database.py

# 4. Start the agency
./start-agency.sh

# 5. Interact
./agency-cli
> /new-course topic="AI Safety" audience="ML Engineers"
```

---

## 📁 Project Structure

```
ai-flywheel-agency/
├── agents/                      # The Agent System
│   ├── base/                    # ✅ Base framework (DONE)
│   │   ├── agent.py            # ✅ BaseAgent class
│   │   ├── context.py          # ✅ Context builder
│   │   ├── messaging.py        # ✅ Messaging system
│   │   └── memory.py           # ✅ Memory system (DONE!)
│   ├── definitions/             # Agent configurations
│   │   ├── chief_learning_strategist.yaml  # ✅ DONE
│   │   └── ... (9 more)        # ✅ ALL DONE!
│   └── server.py               # ⏳ TODO
│
├── shared-context/              # The Hymn Book
│   ├── strategic-objectives.md # ✅ DONE
│   ├── brand-voice.md          # ⏳ TODO
│   ├── quality-standards.md    # ⏳ TODO
│   └── student-personas.md     # ⏳ TODO
│
├── mcp-servers/                 # ⏳ TODO (5 servers)
├── orchestrator/                # ⏳ TODO
├── cli/                         # ⏳ TODO
└── .claude/                     # ⏳ TODO
    ├── commands/                # Slash commands
    └── expertise/               # Domain knowledge
```

---

## 🎨 Architecture Overview

### The Agent System

**10 Agents in 3 Tiers:**

**Tier 1: Strategic Chiefs (Coordinators)**
1. Chief Learning Strategist ✅
2. Chief Experience Strategist ⏳
3. Chief Community Strategist ⏳

**Tier 2: Specialists (Domain Experts)**
4. Market Research Analyst ⏳
5. Learning Designer ⏳
6. Behavioral Scientist ⏳
7. Data Analyst ⏳

**Tier 3: Execution (Implementers)**
8. Experience Designer ⏳
9. Community Manager ⏳
10. Quality Assurance Specialist ⏳

### How It Works

```
Human
  ↕
CLI / Slash Commands
  ↕
Chief Learning Strategist (orchestrator)
  ↕
Other Agents (specialists)
  ↕
MCP Servers (tools/data)
  ↕
External APIs & Databases
```

**Key Principles:**
- **Shared Context**: All agents read the same hymn book (strategic objectives, standards, etc.)
- **Individual Memory**: Each agent remembers their own past work and learnings
- **Autonomous Collaboration**: Agents can work together without human mediation (but human can always intervene)
- **Tool Use**: Agents call MCP servers for data and capabilities
- **Persistent**: Agents maintain state across sessions

---

## 💡 Design Philosophy

### Why This Architecture?

**Based on Anthropic's Best Practices:**
1. **Use Claude Code** - don't rebuild what exists
2. **MCP for tools** - standard protocol for capabilities
3. **Context efficiency** - just-in-time retrieval, not everything all the time
4. **Clear roles** - each agent has non-overlapping responsibilities
5. **Right altitude** - specific enough to be useful, flexible enough to handle variation

**Balancing Simplicity vs. Power:**
- ✅ Real persistent agents (not just slash commands)
- ✅ Agents can collaborate autonomously
- ✅ Shared context keeps everyone aligned
- ✅ But all in one system (not 10 separate services)
- ✅ Standard protocols (MCP, not custom)
- ✅ Practical to build and maintain

---

## 📊 Expected Outcomes

When complete, this system will:

**For You (Human Director):**
- ⏱️ Save 80% of time on course creation and management
- 🎯 Get data-driven strategic recommendations
- 🤖 Have expert AI team that learns and improves
- 📈 Scale quality output without scaling human team

**For Students:**
- ⭐ 85%+ completion rates (vs 65% industry avg)
- 😊 4.5/5.0+ satisfaction
- 📚 Consistently excellent course quality
- 👥 Thriving community and support

**For Business:**
- 💰 Higher revenue per course (quality = premium pricing)
- 📉 Lower CAC (happy students refer others)
- ⚡ Faster time to market (6 weeks vs 12+ weeks)
- 🏆 Top 1% market position

---

## 🤝 Contributing

This is a personal project currently, but contributions welcome:
- Agent definitions improvements
- MCP server implementations
- Workflow ideas
- Bug reports

---

## 📚 Documentation

- **Architecture**: [REVISED-ARCHITECTURE.md](REVISED-ARCHITECTURE.md)
- **Structure**: [PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md)
- **Specifications**:
  - [Agent Specifications](AI-Flywheel-Agent-Specifications.md)
  - [Implementation Templates](AI-Flywheel-Implementation-Templates.md)
  - [User Guide](AI-Flywheel-User-Guide-For-Dummies.md)

---

## ⚖️ License

Private / Proprietary (for now)

---

## 🙏 Acknowledgments

- **Anthropic** - Claude API and architectural guidance
- **MCP Protocol** - Standard for AI tool integration
- Original agent specifications and workflows

---

**Built with ❤️ and Claude Code**

*Last Updated: 2025-10-25 | Version: 0.2.0*
