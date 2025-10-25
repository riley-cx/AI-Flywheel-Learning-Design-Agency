"""
Messaging System - Agent-to-agent communication

Simplified version of FIPA ACL for agent coordination.
Agents can send messages to each other asynchronously.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from enum import Enum
import uuid


class MessageType(Enum):
    """Types of messages agents can send."""
    REQUEST = "request"          # Ask another agent to do something
    RESPONSE = "response"         # Reply to a request
    INFORM = "inform"            # Share information
    PROPOSE = "propose"          # Suggest an action
    ACCEPT = "accept"            # Accept a proposal
    REJECT = "reject"            # Reject a proposal
    ERROR = "error"              # Error occurred
    STATUS = "status"            # Status update


@dataclass
class Message:
    """
    A message between agents (or human).

    Simplified FIPA ACL structure optimized for our use case.
    """
    sender: str                                    # Agent ID or 'human'
    receiver: str                                  # Agent ID or 'human'
    content: str                                   # The actual message
    message_type: str = "request"                  # Type of message
    conversation_id: Optional[str] = None          # Group related messages
    in_reply_to: Optional[str] = None             # Message this responds to
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional data
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def request(cls,
                sender: str,
                receiver: str,
                content: str,
                conversation_id: Optional[str] = None,
                **kwargs):
        """Create a REQUEST message."""
        return cls(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=MessageType.REQUEST.value,
            conversation_id=conversation_id,
            **kwargs
        )

    @classmethod
    def response(cls,
                 sender: str,
                 receiver: str,
                 content: str,
                 in_reply_to: str,
                 conversation_id: Optional[str] = None,
                 **kwargs):
        """Create a RESPONSE message."""
        return cls(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=MessageType.RESPONSE.value,
            in_reply_to=in_reply_to,
            conversation_id=conversation_id,
            **kwargs
        )

    @classmethod
    def inform(cls,
               sender: str,
               receiver: str,
               content: str,
               conversation_id: Optional[str] = None,
               **kwargs):
        """Create an INFORM message."""
        return cls(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=MessageType.INFORM.value,
            conversation_id=conversation_id,
            **kwargs
        )

    @classmethod
    def error(cls,
              content: str,
              sender: str = "system",
              receiver: str = "human",
              conversation_id: Optional[str] = None,
              **kwargs):
        """Create an ERROR message."""
        return cls(
            sender=sender,
            receiver=receiver,
            content=content,
            message_type=MessageType.ERROR.value,
            conversation_id=conversation_id,
            **kwargs
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'message_id': self.message_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content,
            'message_type': self.message_type,
            'conversation_id': self.conversation_id,
            'in_reply_to': self.in_reply_to,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }


class MessageBus:
    """
    Central message routing system.

    Agents register with the bus and can send messages to each other.
    The bus routes messages to the appropriate agent's handler.
    """

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.message_log: List[Message] = []
        self.max_log_size = 1000

    def subscribe(self, agent_id: str, handler: Callable):
        """
        Register an agent to receive messages.

        Args:
            agent_id: Unique agent identifier
            handler: Function to call when message arrives (agent.handle_message)
        """
        self.handlers[agent_id] = handler
        print(f"📡 {agent_id} subscribed to message bus")

    def unsubscribe(self, agent_id: str):
        """Unregister an agent."""
        if agent_id in self.handlers:
            del self.handlers[agent_id]
            print(f"📡 {agent_id} unsubscribed from message bus")

    def send(self, message: Message) -> Message:
        """
        Send a message to its receiver.

        Args:
            message: The message to send

        Returns:
            Response message from the receiver
        """
        # Log the message
        self._log_message(message)

        # Find the handler for the receiver
        if message.receiver not in self.handlers:
            error_msg = f"Agent '{message.receiver}' not found or not active"
            print(f"❌ {error_msg}")
            return Message.error(
                content=error_msg,
                conversation_id=message.conversation_id
            )

        # Route to handler (synchronous for now)
        try:
            response = self.handlers[message.receiver](message)
            self._log_message(response)
            return response

        except Exception as e:
            error_msg = f"Error delivering message to {message.receiver}: {str(e)}"
            print(f"❌ {error_msg}")
            return Message.error(
                content=error_msg,
                conversation_id=message.conversation_id
            )

    def broadcast(self, message: Message, receivers: List[str]) -> List[Message]:
        """
        Send a message to multiple receivers.

        Args:
            message: The message to broadcast
            receivers: List of agent IDs

        Returns:
            List of responses
        """
        responses = []

        for receiver in receivers:
            # Create a copy of the message for each receiver
            msg = Message(
                sender=message.sender,
                receiver=receiver,
                content=message.content,
                message_type=message.message_type,
                conversation_id=message.conversation_id,
                metadata=message.metadata
            )
            response = self.send(msg)
            responses.append(response)

        return responses

    def get_conversation(self, conversation_id: str) -> List[Message]:
        """
        Retrieve all messages in a conversation.

        Args:
            conversation_id: The conversation ID

        Returns:
            List of messages in chronological order
        """
        return [
            msg for msg in self.message_log
            if msg.conversation_id == conversation_id
        ]

    def get_recent_messages(self, limit: int = 50) -> List[Message]:
        """Get recent messages (for debugging/monitoring)."""
        return self.message_log[-limit:]

    def _log_message(self, message: Message):
        """Log a message to the message history."""
        self.message_log.append(message)

        # Trim log if too large
        if len(self.message_log) > self.max_log_size:
            self.message_log = self.message_log[-self.max_log_size:]

    def clear_log(self):
        """Clear message log (use with caution!)."""
        self.message_log = []
        print("🧹 Message log cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get message bus statistics."""
        return {
            "total_agents": len(self.handlers),
            "active_agents": list(self.handlers.keys()),
            "total_messages": len(self.message_log),
            "message_types": self._count_message_types()
        }

    def _count_message_types(self) -> Dict[str, int]:
        """Count messages by type."""
        counts = {}
        for msg in self.message_log:
            counts[msg.message_type] = counts.get(msg.message_type, 0) + 1
        return counts


# Global message bus instance (singleton pattern)
_global_message_bus = None


def get_message_bus() -> MessageBus:
    """Get the global message bus instance."""
    global _global_message_bus
    if _global_message_bus is None:
        _global_message_bus = MessageBus()
    return _global_message_bus
