"""
Base Agent Framework for AI Flywheel Agency
Provides the foundation that all 10 agents inherit from
"""

import os
import yaml
import anthropic
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .context import ContextBuilder
from .memory import MemoryManager
from .messaging import Message, MessageBus


class BaseAgent:
    """
    Base class for all AI Flywheel agents.

    Each agent:
    - Has a unique identity and role
    - Maintains persistent memory
    - Accesses shared context (the hymn book)
    - Can use MCP tools
    - Can message other agents
    - Reasons using Claude API
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        """
        Initialize the agent.

        Args:
            agent_id: Unique identifier (e.g., "learning-designer")
            config_path: Path to agent definition YAML file
        """
        self.agent_id = agent_id
        self.config = self._load_config(config_path or f"agents/definitions/{agent_id}.yaml")

        # Initialize core components
        self.memory = MemoryManager(agent_id=agent_id)
        self.context_builder = ContextBuilder(agent_id=agent_id, config=self.config)
        self.message_bus = MessageBus()

        # Claude API client
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        # Agent state
        self.active = False
        self.current_conversation_id = None

        print(f"✅ {self.config['name']} initialized")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file."""
        full_path = Path(__file__).parent.parent.parent / config_path

        if not full_path.exists():
            raise FileNotFoundError(f"Agent config not found: {config_path}")

        with open(full_path, 'r') as f:
            return yaml.safe_load(f)

    def start(self):
        """Start the agent (make it active and ready to receive messages)."""
        self.active = True
        self.message_bus.subscribe(self.agent_id, self.handle_message)
        print(f"🟢 {self.config['name']} is now active")

    def stop(self):
        """Stop the agent."""
        self.active = False
        self.message_bus.unsubscribe(self.agent_id)
        print(f"🔴 {self.config['name']} stopped")

    def handle_message(self, message: Message) -> Message:
        """
        Handle incoming message from another agent or human.

        This is the main entry point for agent interactions.
        """
        if not self.active:
            return Message.error(f"{self.config['name']} is not active")

        print(f"📨 {self.config['name']} received message from {message.sender}")

        try:
            # Build full context for this request
            context = self.context_builder.build(
                message=message,
                conversation_id=message.conversation_id
            )

            # Reason and act using Claude
            response = self.reason_and_act(context, message)

            # Store in memory
            self.memory.store_interaction(
                message=message,
                response=response,
                conversation_id=message.conversation_id
            )

            return response

        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(f"❌ {self.config['name']}: {error_msg}")
            return Message.error(error_msg, conversation_id=message.conversation_id)

    def reason_and_act(self, context: Dict[str, Any], message: Message) -> Message:
        """
        Core reasoning loop: given context and a message, figure out what to do.

        This method:
        1. Constructs the full prompt for Claude
        2. Calls Claude API with tool use capability
        3. Executes any tool calls
        4. Returns response
        """
        # Construct system prompt
        system_prompt = self._build_system_prompt(context)

        # Construct user message
        user_message = self._build_user_message(context, message)

        # Get available tools
        tools = self._get_available_tools()

        # Call Claude with tool use
        messages = [{"role": "user", "content": user_message}]

        response_content = []

        # Agentic loop: Claude can use tools multiple times
        while True:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # Latest model
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tools if tools else None
            )

            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                # Execute tool calls
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        })
                        response_content.append(f"[Used tool: {block.name}]")

                # Add assistant response and tool results to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            else:
                # Claude is done reasoning, extract final response
                for block in response.content:
                    if hasattr(block, 'text'):
                        response_content.append(block.text)
                break

        # Create response message
        return Message(
            sender=self.agent_id,
            receiver=message.sender,
            content="\n".join(response_content),
            conversation_id=message.conversation_id,
            message_type="response"
        )

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build the full system prompt including shared context and agent role."""
        parts = []

        # Agent's core role and expertise (from config)
        parts.append(self.config['system_prompt'])

        # Shared context (the hymn book)
        if context.get('shared_context'):
            parts.append("\n## SHARED CONTEXT (The Hymn Book)")
            parts.append("All agents at AI Flywheel share this context:\n")
            for doc_name, doc_content in context['shared_context'].items():
                parts.append(f"### {doc_name}")
                parts.append(doc_content)

        # Domain expertise files
        if context.get('expertise'):
            parts.append("\n## YOUR EXPERTISE")
            for doc_name, doc_content in context['expertise'].items():
                parts.append(f"### {doc_name}")
                parts.append(doc_content)

        # Relevant memory from past interactions
        if context.get('memory'):
            parts.append("\n## RELEVANT PAST CONTEXT")
            parts.append(context['memory'])

        # Current date/time
        parts.append(f"\n## CURRENT CONTEXT")
        parts.append(f"Today's date: {datetime.now().strftime('%Y-%m-%d')}")
        parts.append(f"Agent: {self.config['name']}")
        parts.append(f"Role: {self.config['type']}")

        return "\n".join(parts)

    def _build_user_message(self, context: Dict[str, Any], message: Message) -> str:
        """Build the user message with task context."""
        parts = []

        # The actual request/message
        parts.append(f"## REQUEST FROM {message.sender.upper()}")
        parts.append(message.content)

        # Conversation context if this is part of ongoing discussion
        if message.conversation_id and context.get('conversation_history'):
            parts.append("\n## CONVERSATION HISTORY")
            parts.append(context['conversation_history'])

        # Any additional context
        if message.metadata:
            parts.append("\n## ADDITIONAL CONTEXT")
            parts.append(json.dumps(message.metadata, indent=2))

        return "\n".join(parts)

    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of tools this agent can use (MCP servers).

        Returns tool definitions in Anthropic tool format.
        """
        if 'tools' not in self.config:
            return []

        # TODO: Dynamically load tool definitions from MCP servers
        # For now, return empty list (will implement with MCP servers)
        return []

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a tool call (call to MCP server).

        Args:
            tool_name: Name of the tool (e.g., "get_course_metrics")
            tool_input: Arguments for the tool

        Returns:
            Tool result
        """
        # TODO: Implement MCP tool calling
        # For now, return placeholder
        return {
            "status": "placeholder",
            "message": f"Tool '{tool_name}' not yet implemented"
        }

    def send_message(self,
                    receiver: str,
                    content: str,
                    conversation_id: Optional[str] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> Message:
        """
        Send a message to another agent or human.

        Args:
            receiver: Agent ID or 'human'
            content: Message content
            conversation_id: Optional conversation ID to maintain context
            metadata: Optional additional data

        Returns:
            Response message
        """
        message = Message(
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            conversation_id=conversation_id or self._generate_conversation_id(),
            metadata=metadata
        )

        print(f"📤 {self.config['name']} sending message to {receiver}")

        return self.message_bus.send(message)

    def _generate_conversation_id(self) -> str:
        """Generate a unique conversation ID."""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        return f"conv-{self.agent_id}-{timestamp}"

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.config['name'],
            "type": self.config['type'],
            "active": self.active,
            "memory_size_mb": self.memory.get_size_mb(),
            "total_interactions": self.memory.get_interaction_count(),
            "timestamp": datetime.now().isoformat()
        }

    def reset_memory(self):
        """Clear agent's memory (use with caution!)."""
        confirm = input(f"⚠️  Reset memory for {self.config['name']}? (yes/no): ")
        if confirm.lower() == 'yes':
            self.memory.clear()
            print(f"🧹 {self.config['name']} memory cleared")
        else:
            print("❌ Memory reset cancelled")


class ChiefAgent(BaseAgent):
    """
    Base class for Chief-level agents (strategists/coordinators).

    Chiefs have additional capabilities:
    - Can coordinate other agents
    - Make strategic decisions
    - Have broader authority
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        super().__init__(agent_id, config_path)
        self.coordinated_agents = self.config.get('coordinates', [])

    def coordinate_agents(self, agents: List[str], task: str) -> List[Message]:
        """
        Coordinate multiple agents to work on a task together.

        Args:
            agents: List of agent IDs to coordinate
            task: The task description

        Returns:
            List of responses from coordinated agents
        """
        conversation_id = self._generate_conversation_id()
        responses = []

        print(f"🎯 {self.config['name']} coordinating: {', '.join(agents)}")

        for agent_id in agents:
            response = self.send_message(
                receiver=agent_id,
                content=task,
                conversation_id=conversation_id,
                metadata={"coordinated_by": self.agent_id}
            )
            responses.append(response)

        return responses


class SpecialistAgent(BaseAgent):
    """
    Base class for specialist agents (designers, analysts, scientists).

    Specialists focus deeply on their domain.
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        super().__init__(agent_id, config_path)

    # Specialists use the standard BaseAgent capabilities
    # Subclasses can override specific methods for specialized behavior


class ExecutionAgent(BaseAgent):
    """
    Base class for execution-focused agents (managers, designers).

    Execution agents implement plans and take action.
    """

    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        super().__init__(agent_id, config_path)

    # Execution agents use standard BaseAgent capabilities
    # Subclasses can add specific execution methods
