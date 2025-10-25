"""
Context Builder - Assembles full context for agent reasoning

Combines:
1. Shared context (the hymn book - what everyone knows)
2. Domain expertise (role-specific knowledge)
3. Personal memory (past interactions and learnings)
4. Current message (the task at hand)
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import os


class ContextBuilder:
    """
    Builds the complete context for an agent to reason with.

    Following Anthropic's best practices:
    - Just-in-time retrieval (don't load everything)
    - Progressive disclosure (load more as needed)
    - Context efficiency (high signal, low noise)
    """

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.agency_root = Path(__file__).parent.parent.parent

    def build(self,
              message: Any,
              conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Build full context for processing a message.

        Args:
            message: The incoming message
            conversation_id: Optional conversation ID for context retrieval

        Returns:
            Dictionary with all context components
        """
        context = {}

        # 1. Load shared context (the hymn book)
        context['shared_context'] = self._load_shared_context()

        # 2. Load domain expertise
        context['expertise'] = self._load_expertise_files()

        # 3. Load relevant memory
        # TODO: Implement smart memory retrieval
        context['memory'] = self._load_relevant_memory(message, conversation_id)

        # 4. Load conversation history if applicable
        if conversation_id:
            context['conversation_history'] = self._load_conversation_history(conversation_id)

        return context

    def _load_shared_context(self) -> Dict[str, str]:
        """
        Load the shared context (hymn book) that all agents should know.

        This includes:
        - Strategic objectives
        - Brand voice
        - Quality standards
        - Student personas
        - Success metrics
        - Current initiatives
        """
        shared_context_dir = self.agency_root / "shared-context"
        shared_context = {}

        if not shared_context_dir.exists():
            print(f"⚠️  Shared context directory not found: {shared_context_dir}")
            return shared_context

        # Load all markdown files in shared-context/
        for file_path in shared_context_dir.glob("*.md"):
            doc_name = file_path.stem.replace('-', ' ').title()
            with open(file_path, 'r') as f:
                shared_context[doc_name] = f.read()

        return shared_context

    def _load_expertise_files(self) -> Dict[str, str]:
        """
        Load domain expertise files specific to this agent's role.

        Based on the agent's configuration, load relevant .claude/expertise/ files.
        """
        expertise = {}

        if 'context_files' not in self.config:
            return expertise

        for file_path in self.config['context_files']:
            full_path = self.agency_root / file_path

            if not full_path.exists():
                print(f"⚠️  Expertise file not found: {file_path}")
                continue

            doc_name = full_path.stem.replace('-', ' ').title()
            with open(full_path, 'r') as f:
                expertise[doc_name] = f.read()

        return expertise

    def _load_relevant_memory(self,
                              message: Any,
                              conversation_id: Optional[str]) -> str:
        """
        Load relevant past context from agent's memory.

        This should be smart:
        - Semantic search for similar past interactions
        - Recency (prioritize recent over old)
        - Relevance (match to current message topic)

        Following Anthropic's just-in-time retrieval principle.
        """
        # TODO: Implement semantic search in memory
        # For now, return placeholder
        return ""

    def _load_conversation_history(self, conversation_id: str) -> str:
        """
        Load the history of the current conversation.

        This allows agents to maintain context across multi-turn interactions.
        """
        # TODO: Retrieve conversation from memory
        # For now, return placeholder
        return ""

    def refresh_shared_context(self) -> Dict[str, str]:
        """
        Force reload of shared context.

        Call this when strategic objectives or other shared context changes.
        """
        return self._load_shared_context()

    def validate_context_size(self, context: Dict[str, Any]) -> Dict[str, int]:
        """
        Check the token count of the context.

        Returns sizes for each component to ensure we're not exceeding limits.
        """
        # Rough estimation: 1 token ≈ 4 characters
        sizes = {}

        if 'shared_context' in context:
            total_chars = sum(len(v) for v in context['shared_context'].values())
            sizes['shared_context_tokens'] = total_chars // 4

        if 'expertise' in context:
            total_chars = sum(len(v) for v in context['expertise'].values())
            sizes['expertise_tokens'] = total_chars // 4

        if 'memory' in context:
            sizes['memory_tokens'] = len(context['memory']) // 4

        if 'conversation_history' in context:
            sizes['conversation_tokens'] = len(context['conversation_history']) // 4

        sizes['total_tokens'] = sum(sizes.values())

        return sizes

    def compress_context_if_needed(self,
                                   context: Dict[str, Any],
                                   max_tokens: int = 100000) -> Dict[str, Any]:
        """
        Compress context if it exceeds token limits.

        Strategies:
        1. Summarize older conversation history
        2. Remove less relevant memory
        3. Keep shared context and expertise (always needed)
        """
        sizes = self.validate_context_size(context)

        if sizes['total_tokens'] < max_tokens:
            return context  # No compression needed

        print(f"⚠️  Context too large ({sizes['total_tokens']} tokens), compressing...")

        # TODO: Implement compression strategies
        # For now, just warn
        print("⚠️  Context compression not yet implemented")

        return context
