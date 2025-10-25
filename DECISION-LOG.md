# AI Flywheel Agency - Decision Log
## Strategic and Architectural Decisions

**Purpose**: Track all major decisions that shaped the architecture and direction of this project.

**Last Updated**: 2025-10-25

---

## 📋 Decision Framework

Each decision includes:
- **Context**: Why was this decision needed?
- **Options Considered**: What alternatives did we evaluate?
- **Decision**: What did we choose?
- **Rationale**: Why did we choose this?
- **Impact**: What does this enable/constrain?
- **Status**: Active, Superseded, or Under Review

---

## 🎯 Strategic Decisions

### Decision 1: Use Real Agents, Not Just Slash Commands
**Date**: 2025-10-25
**Context**: Initial architecture could have been just slash commands calling Claude Code directly
**Decision**: Build persistent agents with memory and identity
**Rationale**:
- Agents need persistent memory across sessions
- Agents should build expertise over time
- Agents need to collaborate autonomously (not just when human initiates)
- Enables proactive behavior (agents can initiate actions)

**Impact**:
- ✅ Enables: True multi-agent collaboration, learning from experience, proactive monitoring
- ⚠️ Constrains: More complex to build (but still achievable in 6-8 weeks)

**Status**: ✅ Active

---

### Decision 2: Shared Context (The Hymn Book)
**Date**: 2025-10-25
**Context**: Agents need to be aligned on goals, standards, and strategy
**Decision**: All agents load shared context files on startup
**Rationale**:
- Prevents contradictions between agents
- Ensures strategic alignment
- Easy to update all agents at once (change one file)
- Follows Anthropic's context efficiency principles

**Impact**:
- ✅ Enables: Consistent decision-making, easy strategy updates, reduced token usage
- ⚠️ Constrains: Shared context must be maintained and kept current

**Status**: ✅ Active

**Files Created**:
- `shared-context/strategic-objectives.md` (complete)
- `shared-context/brand-voice.md` (pending)
- `shared-context/quality-standards.md` (pending)
- `shared-context/student-personas.md` (pending)
- `shared-context/success-metrics.md` (pending)

---

### Decision 3: MCP Servers for Tools, Not Custom APIs
**Date**: 2025-10-25
**Context**: Agents need data access and specialized capabilities
**Decision**: Use Anthropic's MCP (Model Context Protocol) for all tool servers
**Rationale**:
- Standard protocol (Anthropic recommended)
- Well-documented and supported
- Easier to maintain than custom APIs
- Can be reused across different agents
- Future-proof (MCP is the standard)

**Impact**:
- ✅ Enables: Standard tooling, easier debugging, community support
- ⚠️ Constrains: Must follow MCP patterns (but this is good constraint)

**Status**: ✅ Active

**MCP Servers Planned**:
1. Learning Analytics (data queries)
2. Market Intelligence (research, competitor tracking)
3. Content Management (file operations, git)
4. Community Platform (forum API)
5. Quality Validation (automated checks)

---

## 🏗️ Architectural Decisions

### Decision 4: Single System, Not 10 Separate Processes
**Date**: 2025-10-25
**Context**: Could run each agent as separate process with message broker
**Options Considered**:
- A: 10 separate Python processes + RabbitMQ message broker
- B: Single system running all agents + simple message bus
- C: Hybrid (Chiefs as processes, specialists as libraries)

**Decision**: Option B - Single system
**Rationale**:
- Simpler to build and debug
- Efficient resource usage (shared memory, context loading)
- Fast message passing (just method calls, not network)
- Easier deployment (one process vs 10)
- Still achieves agent autonomy and collaboration
- Can scale later if needed (not premature optimization)

**Impact**:
- ✅ Enables: Faster development, easier testing, simpler deployment
- ⚠️ Constrains: All agents in one process (acceptable for this use case)

**Status**: ✅ Active

---

### Decision 5: Two-Tier Memory System
**Date**: 2025-10-25
**Context**: Agents need memory that's both fast and persistent
**Options Considered**:
- A: Only short-term (in-memory) - fast but lost on restart
- B: Only long-term (database) - persistent but slow
- C: Two-tier (short + long) - best of both

**Decision**: Option C - Two-tier memory
**Rationale**:
- Short-term: Fast access for current session
- Long-term: Persistence and semantic search
- Automatic consolidation (move short → long periodically)
- Follows Anthropic's "just-in-time retrieval" principle
- Scales well (hot data in memory, cold data on disk)

**Implementation Details**:
- Short-term: Python dicts (in-memory, LRU eviction)
- Long-term structured: SQLite (conversations, decisions, patterns)
- Long-term semantic: ChromaDB (vector search for similar contexts)

**Impact**:
- ✅ Enables: Fast retrieval + long-term learning, semantic search
- ⚠️ Constrains: Must manage consolidation (but automated)

**Status**: ✅ Active - Fully Implemented

---

### Decision 6: SQLite + ChromaDB (Not PostgreSQL)
**Date**: 2025-10-25
**Context**: Originally specified PostgreSQL for agent memory
**Decision**: Use SQLite for structured data, ChromaDB for semantic
**Rationale**:
- SQLite: Simpler setup (no server), perfect for agent-level data
- File-based: Each agent has own .db file (isolation)
- PostgreSQL overkill for this use case
- ChromaDB: Best-in-class for semantic search, easy setup
- Can migrate to PostgreSQL later if needed (abstraction layer exists)

**Impact**:
- ✅ Enables: Easier development, simpler deployment, good performance
- ⚠️ Constrains: Not suitable for massive scale (but not needed here)

**Status**: ✅ Active

**Migration Path**: If needed later, swap SQLite → PostgreSQL (MemoryManager interface stays same)

---

## 🛠️ Implementation Decisions

### Decision 7: Agent Definitions as YAML
**Date**: 2025-10-25
**Context**: How should agent configurations be defined?
**Options Considered**:
- A: Python classes with hardcoded values
- B: JSON configuration files
- C: YAML configuration files

**Decision**: Option C - YAML files
**Rationale**:
- Human-readable and easy to edit
- Supports comments (JSON doesn't)
- Clear structure for complex nested data
- Can be version controlled effectively
- Standard format for configuration

**Impact**:
- ✅ Enables: Easy agent creation, clear configuration, version control
- ⚠️ Constrains: Must parse YAML (but standard library available)

**Status**: ✅ Active

**Files Created**: 10 agent YAML files in `agents/definitions/`

---

### Decision 8: Claude Sonnet 4 (Latest Model)
**Date**: 2025-10-25
**Context**: Which Claude model should agents use for reasoning?
**Decision**: Claude Sonnet 4 (claude-sonnet-4-20250514)
**Rationale**:
- Latest and most capable model
- Best reasoning capabilities
- Tool use (MCP) support
- Good balance of speed and intelligence
- Can swap models per agent if needed (Chiefs use Sonnet, others use Haiku)

**Impact**:
- ✅ Enables: Best possible agent reasoning
- ⚠️ Constrains: API costs (but worth it for quality)

**Status**: ✅ Active

**Future Optimization**: Could use Haiku for simple tasks, Sonnet for complex reasoning

---

### Decision 9: Proactive Behaviors in Agent Configs
**Date**: 2025-10-25
**Context**: Should agents only respond, or also initiate?
**Decision**: Agents have proactive behaviors (defined in YAML)
**Rationale**:
- Enables autonomous operation (don't need human to prompt everything)
- Data Analyst can detect anomalies and alert
- Chiefs can monitor progress and flag risks
- Community Manager can welcome new members automatically
- Aligns with "agents, not just tools" philosophy

**Examples**:
- Data Analyst: `monitor_key_metrics: "daily"`
- Chief Learning Strategist: `monitor_strategic_progress: "weekly"`
- Community Manager: `welcome_new_members: "daily"`

**Impact**:
- ✅ Enables: Autonomous operation, proactive issue detection, reduced human workload
- ⚠️ Constrains: Must implement scheduler (but straightforward)

**Status**: ✅ Active (defined in agent configs, implementation pending in Phase 3)

---

## 🔄 Process Decisions

### Decision 10: Test Before Moving Forward
**Date**: 2025-10-25
**Context**: Should we build everything then test, or test as we go?
**Decision**: Test each phase before proceeding to next
**Rationale**:
- Catch issues early (cheaper to fix)
- Validate assumptions (does architecture work?)
- Build confidence (know what works)
- Avoid compounding errors (bad foundation = bad everything)

**Impact**:
- ✅ Enables: Higher quality, fewer bugs, validated architecture
- ⚠️ Constrains: Slightly slower progress (but better final result)

**Status**: ✅ Active - Testing memory system before Phase 3

---

### Decision 11: Phase-Based Development
**Date**: 2025-10-25
**Context**: How should we structure the development?
**Decision**: 6 clear phases, each with deliverables
**Rationale**:
- Clear milestones and progress tracking
- Each phase builds on previous
- Easy to pause/resume work
- Clear communication of progress
- Manageable chunks (not overwhelming)

**Phases**:
1. ✅ Foundation (agent framework, first agent, shared context)
2. ✅ Agent Definitions (all 10 agents defined)
3. ✅ Memory System (two-tier memory implemented)
4. 📋 MCP Servers (5 tool servers)
5. 📋 Orchestration (workflows, CLI)
6. 📋 Polish & Launch

**Impact**:
- ✅ Enables: Clear progress, manageable work, easy communication
- ⚠️ Constrains: Must complete each phase (but good constraint)

**Status**: ✅ Active - Currently completing Phase 2 testing

---

## 📝 Design Pattern Decisions

### Decision 12: Three Agent Tiers
**Date**: 2025-10-25
**Context**: How should the 10 agents be organized?
**Decision**: Three tiers based on role
**Rationale**:
- Clear hierarchy and responsibilities
- Chiefs coordinate, Specialists advise, Execution implements
- Matches real organizational structure
- Prevents circular dependencies

**Tiers**:
1. **Chiefs (3)**: Strategic coordination, make decisions, coordinate others
2. **Specialists (4)**: Domain expertise, research, analysis, design
3. **Execution (3)**: Implementation, moderation, validation

**Impact**:
- ✅ Enables: Clear responsibilities, efficient coordination
- ⚠️ Constrains: Chiefs can't implement, Execution can't strategize (good constraint)

**Status**: ✅ Active

---

### Decision 13: Escalation Rules in Agent Configs
**Date**: 2025-10-25
**Context**: When should agents escalate to human?
**Decision**: Define escalation rules in each agent's YAML config
**Rationale**:
- Clear boundaries for agent autonomy
- Prevents agents making decisions beyond authority
- Easy to adjust (change YAML, not code)
- Transparent (human knows when they'll be asked)

**Examples**:
- Chief Learning Strategist: Escalate if budget > $50K
- Quality Assurance: Escalate if accessibility violations
- Community Manager: Escalate if crisis or legal concerns

**Impact**:
- ✅ Enables: Safe autonomy, clear boundaries, adjustable authority
- ⚠️ Constrains: Some decisions must go to human (acceptable)

**Status**: ✅ Active

---

## 🎯 Scope Decisions

### Decision 14: What We're NOT Building
**Date**: 2025-10-25
**Context**: Need to limit scope to ship in 6-8 weeks
**Decision**: Explicitly define what's out of scope
**Items NOT Building**:
- ❌ Custom message broker (use simple MessageBus instead of RabbitMQ)
- ❌ Web dashboard (CLI first, web later if needed)
- ❌ Mobile app (web-first)
- ❌ Enterprise features (focus on core functionality)
- ❌ Internationalization (English only)
- ❌ Custom LLM training (use Claude API)

**Rationale**:
- Focus on core value (intelligent agents that work)
- Ship faster (6-8 weeks vs 6 months)
- Validate concept before adding features
- Can add later if needed

**Impact**:
- ✅ Enables: Faster delivery, focused effort, manageable scope
- ⚠️ Constrains: Limited features initially (acceptable for v1)

**Status**: ✅ Active

---

## 🔮 Future Decisions (To Be Made)

### Decision TBD-1: Real Data vs Mock Data for Testing
**Status**: Under Review
**Context**: MCP servers need data. Use real DB or mocks?
**Options**:
- A: Mock data for development, real data for production
- B: Real data from day 1
- C: Mix (some real, some mock)

**Leaning Toward**: Option A (mocks for dev speed, real data for validation)

---

### Decision TBD-2: Scheduler Implementation
**Status**: Pending
**Context**: Proactive behaviors need scheduling
**Options**:
- A: Python `schedule` library (simple)
- B: Celery (powerful, complex)
- C: Simple cron-like implementation

**Leaning Toward**: Option A (simple, sufficient for v1)

---

### Decision TBD-3: API Keys Management
**Status**: Pending
**Context**: Agents need API keys (Anthropic, external services)
**Options**:
- A: .env file (simple, not secure for production)
- B: Secrets manager (AWS Secrets, HashiCorp Vault)
- C: Encrypted key store

**Leaning Toward**: Option A for dev, Option B for production

---

## 📊 Decision Metrics

**Total Decisions Made**: 14 major + 3 pending
**Architectural**: 6
**Implementation**: 4
**Strategic**: 3
**Process**: 2
**Design Patterns**: 2

**Decision Velocity**: All major decisions made in 1 day (2025-10-25)
**Reversals**: 0 (no decisions reversed yet)
**Under Review**: 3

---

## 🔄 Decision Review Process

**Review Frequency**: End of each phase
**Review Criteria**:
- Is decision still valid?
- Did we learn something that changes it?
- Should we reverse or modify?

**Next Review**: End of Phase 3 (after MCP servers built)

---

## ✅ Decision Quality Indicators

**Good Signs**:
- ✅ Clear rationale for each decision
- ✅ Considered alternatives
- ✅ Aligned with Anthropic best practices
- ✅ Enabled by specifications (not arbitrary)
- ✅ Testable (can validate decision was right)

**Areas to Watch**:
- ⚠️ Some decisions pending real-world testing
- ⚠️ 3 decisions still to be made
- ⚠️ May need to adjust based on Phase 3 learnings

---

## 📚 References

**Decisions Informed By**:
1. Anthropic's Best Practices:
   - Effective Context Engineering for AI Agents
   - Claude Code Best Practices
   - Writing Tools for Agents
2. Original Specifications:
   - AI-Flywheel-Agent-Specifications.md
   - AI-Flywheel-Implementation-Templates.md
3. Your Strategic Direction:
   - "Agents should work together autonomously"
   - "Singing from the same hymn book"
   - "Test before moving forward"

---

**This decision log is a living document. Update as we learn and evolve.** 📝

**Last Major Decision**: Decision 14 (Scope) - 2025-10-25
**Next Decision Point**: Phase 3 - MCP Server architecture details
