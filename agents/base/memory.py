"""
Memory Management System for AI Flywheel Agents

Two-tier memory system:
1. Short-term: In-memory (volatile, current session)
2. Long-term: Persistent (PostgreSQL + ChromaDB for semantic search)

Following Anthropic's best practices:
- Just-in-time retrieval (don't load everything)
- Semantic search for relevant context
- Automatic consolidation
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import uuid

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not available. Semantic search will be limited.")


class ShortTermMemory:
    """
    In-memory storage for active session data.

    Fast access, but lost when agent restarts.
    Used for current conversations and working data.
    """

    def __init__(self, max_size_mb: int = 50):
        self.max_size_mb = max_size_mb
        self.conversations: Dict[str, Any] = {}
        self.working_memory: Dict[str, Any] = {}
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, datetime] = {}

    def store(self, key: str, value: Any, category: str = 'working'):
        """
        Store data in short-term memory.

        Args:
            key: Unique identifier
            value: Data to store
            category: 'conversation', 'working', or 'cache'
        """
        # Check size limit
        if self._check_size_limit():
            self._evict_oldest()

        if category == 'conversation':
            self.conversations[key] = value
        elif category == 'working':
            self.working_memory[key] = value
        elif category == 'cache':
            self.cache[key] = value
        else:
            raise ValueError(f"Unknown category: {category}")

        self.timestamps[key] = datetime.now()

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve from short-term memory."""
        # Check all categories
        for storage in [self.conversations, self.working_memory, self.cache]:
            if key in storage:
                # Update LRU timestamp
                self.timestamps[key] = datetime.now()
                return storage[key]

        return None

    def get_all_conversations(self) -> Dict[str, Any]:
        """Get all active conversations."""
        return self.conversations.copy()

    def clear_category(self, category: str):
        """Clear a specific category."""
        if category == 'conversation':
            keys = list(self.conversations.keys())
            for key in keys:
                del self.conversations[key]
                if key in self.timestamps:
                    del self.timestamps[key]
        elif category == 'working':
            keys = list(self.working_memory.keys())
            for key in keys:
                del self.working_memory[key]
                if key in self.timestamps:
                    del self.timestamps[key]
        elif category == 'cache':
            keys = list(self.cache.keys())
            for key in keys:
                del self.cache[key]
                if key in self.timestamps:
                    del self.timestamps[key]

    def clear_old_data(self, before: datetime):
        """Clear data older than specified time."""
        old_keys = [
            key for key, ts in self.timestamps.items()
            if ts < before
        ]

        for key in old_keys:
            self._remove(key)

    def _check_size_limit(self) -> bool:
        """Check if memory exceeds limit."""
        current_size = self._get_size_mb()
        return current_size > self.max_size_mb

    def _get_size_mb(self) -> float:
        """Estimate memory size in MB."""
        import sys

        total_size = 0
        total_size += sys.getsizeof(self.conversations)
        total_size += sys.getsizeof(self.working_memory)
        total_size += sys.getsizeof(self.cache)

        return total_size / (1024 * 1024)

    def _evict_oldest(self):
        """Remove least recently used item."""
        if not self.timestamps:
            return

        oldest_key = min(self.timestamps, key=self.timestamps.get)
        self._remove(oldest_key)

    def _remove(self, key: str):
        """Remove a key from all storages."""
        if key in self.conversations:
            del self.conversations[key]
        if key in self.working_memory:
            del self.working_memory[key]
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            'size_mb': self._get_size_mb(),
            'max_size_mb': self.max_size_mb,
            'conversations': len(self.conversations),
            'working_items': len(self.working_memory),
            'cached_items': len(self.cache),
            'total_items': len(self.timestamps)
        }


class LongTermMemory:
    """
    Persistent memory using SQLite + ChromaDB.

    Stores:
    - Conversation history (structured)
    - Decisions and outcomes
    - Patterns and learnings
    - Semantic memory (for similarity search)
    """

    def __init__(self, agent_id: str, db_path: str = "./data/memory"):
        self.agent_id = agent_id
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)

        # SQLite for structured data
        self.db_file = self.db_path / f"{agent_id}.db"
        self.conn = sqlite3.connect(str(self.db_file), check_same_thread=False)
        self._init_database()

        # ChromaDB for semantic search
        if CHROMA_AVAILABLE:
            self.chroma_path = self.db_path / "vector" / agent_id
            self.chroma_path.mkdir(parents=True, exist_ok=True)

            self.chroma_client = chromadb.PersistentClient(
                path=str(self.chroma_path),
                settings=Settings(anonymized_telemetry=False)
            )

            self.collection = self.chroma_client.get_or_create_collection(
                name=f"{agent_id}_memories",
                metadata={"hnsw:space": "cosine"}
            )
        else:
            self.chroma_client = None
            self.collection = None

    def _init_database(self):
        """Initialize SQLite database schema."""
        cursor = self.conn.cursor()

        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                participants TEXT,
                summary TEXT,
                outcome TEXT,
                key_insights TEXT,
                metadata TEXT
            )
        ''')

        # Individual interactions/messages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                interaction_id TEXT PRIMARY KEY,
                conversation_id TEXT,
                timestamp TIMESTAMP,
                message_from TEXT,
                message_to TEXT,
                message_type TEXT,
                content TEXT,
                response TEXT,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        ''')

        # Decisions made by agent
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                decision_type TEXT,
                context TEXT,
                decision TEXT,
                rationale TEXT,
                outcome_metric TEXT,
                outcome_value REAL,
                timestamp TIMESTAMP,
                metadata TEXT
            )
        ''')

        # Patterns and learnings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT,
                description TEXT,
                confidence REAL,
                examples TEXT,
                last_validated TIMESTAMP,
                metadata TEXT
            )
        ''')

        # Generic key-value store for flexibility
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_store (
                key TEXT PRIMARY KEY,
                value TEXT,
                category TEXT,
                timestamp TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')

        self.conn.commit()

    def store_interaction(self,
                         message: Any,
                         response: Any,
                         conversation_id: str):
        """
        Store an interaction (message + response).

        Args:
            message: The incoming message
            response: The agent's response
            conversation_id: ID of the conversation
        """
        interaction_id = str(uuid.uuid4())

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO interactions
            (interaction_id, conversation_id, timestamp, message_from, message_to,
             message_type, content, response, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            interaction_id,
            conversation_id,
            datetime.now(),
            getattr(message, 'sender', 'unknown'),
            getattr(message, 'receiver', self.agent_id),
            getattr(message, 'message_type', 'unknown'),
            getattr(message, 'content', str(message)),
            getattr(response, 'content', str(response)),
            json.dumps(getattr(message, 'metadata', {}))
        ))

        self.conn.commit()

        # Also store in semantic memory for retrieval
        if self.collection is not None:
            combined_text = f"{message.content}\n\nResponse: {response.content}"
            self._store_semantic(
                text=combined_text,
                metadata={
                    'type': 'interaction',
                    'conversation_id': conversation_id,
                    'timestamp': datetime.now().isoformat()
                }
            )

    def store_conversation(self,
                          conversation_id: str,
                          summary: str,
                          participants: List[str],
                          key_insights: List[str],
                          outcome: Optional[str] = None):
        """Store conversation summary."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO conversations
            (conversation_id, started_at, completed_at, participants,
             summary, outcome, key_insights)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            conversation_id,
            datetime.now(),
            datetime.now(),
            json.dumps(participants),
            summary,
            outcome,
            json.dumps(key_insights)
        ))

        self.conn.commit()

        # Store in semantic memory
        if self.collection is not None:
            self._store_semantic(
                text=f"{summary}\n\nKey insights: {'; '.join(key_insights)}",
                metadata={
                    'type': 'conversation',
                    'conversation_id': conversation_id,
                    'timestamp': datetime.now().isoformat()
                }
            )

    def store_decision(self,
                      decision_type: str,
                      context: str,
                      decision: str,
                      rationale: str,
                      outcome_metric: Optional[str] = None,
                      outcome_value: Optional[float] = None):
        """Store a decision made by the agent."""
        decision_id = str(uuid.uuid4())

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO decisions
            (decision_id, decision_type, context, decision, rationale,
             outcome_metric, outcome_value, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            decision_id,
            decision_type,
            context,
            decision,
            rationale,
            outcome_metric,
            outcome_value,
            datetime.now()
        ))

        self.conn.commit()

        # Store in semantic memory
        if self.collection is not None:
            self._store_semantic(
                text=f"Decision: {decision}\nContext: {context}\nRationale: {rationale}",
                metadata={
                    'type': 'decision',
                    'decision_type': decision_type,
                    'timestamp': datetime.now().isoformat()
                }
            )

        return decision_id

    def store_pattern(self,
                     pattern_type: str,
                     description: str,
                     confidence: float,
                     examples: List[str]):
        """Store a learned pattern."""
        pattern_id = str(uuid.uuid4())

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO patterns
            (pattern_id, pattern_type, description, confidence, examples, last_validated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pattern_id,
            pattern_type,
            description,
            confidence,
            json.dumps(examples),
            datetime.now()
        ))

        self.conn.commit()

        return pattern_id

    def _store_semantic(self, text: str, metadata: Dict[str, Any]):
        """Store text in vector database for semantic search."""
        if self.collection is None:
            return

        doc_id = f"{self.agent_id}_{datetime.now().timestamp()}_{uuid.uuid4().hex[:8]}"

        try:
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            print(f"⚠️  Error storing in ChromaDB: {e}")

    def retrieve_semantic(self,
                         query: str,
                         n_results: int = 5,
                         filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Semantic search in long-term memory.

        Args:
            query: Search query
            n_results: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of relevant memories
        """
        if self.collection is None:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filters if filters else None
            )

            # Format results
            memories = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    memories.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })

            return memories

        except Exception as e:
            print(f"⚠️  Error in semantic search: {e}")
            return []

    def retrieve_conversations(self,
                              participant: Optional[str] = None,
                              limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve conversation history."""
        cursor = self.conn.cursor()

        if participant:
            cursor.execute('''
                SELECT * FROM conversations
                WHERE participants LIKE ?
                ORDER BY completed_at DESC
                LIMIT ?
            ''', (f'%{participant}%', limit))
        else:
            cursor.execute('''
                SELECT * FROM conversations
                ORDER BY completed_at DESC
                LIMIT ?
            ''', (limit,))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def retrieve_decisions(self,
                          decision_type: Optional[str] = None,
                          limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve decision history."""
        cursor = self.conn.cursor()

        if decision_type:
            cursor.execute('''
                SELECT * FROM decisions
                WHERE decision_type = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (decision_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM decisions
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def retrieve_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve learned patterns."""
        cursor = self.conn.cursor()

        if pattern_type:
            cursor.execute('''
                SELECT * FROM patterns
                WHERE pattern_type = ?
                ORDER BY confidence DESC
            ''', (pattern_type,))
        else:
            cursor.execute('''
                SELECT * FROM patterns
                ORDER BY confidence DESC
            ''')

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    def get_conversation_history(self, conversation_id: str) -> str:
        """Get full conversation history as formatted string."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, message_from, content, response
            FROM interactions
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        ''', (conversation_id,))

        rows = cursor.fetchall()

        if not rows:
            return ""

        history_parts = []
        for timestamp, msg_from, content, response in rows:
            history_parts.append(f"[{timestamp}] {msg_from}: {content}")
            if response:
                history_parts.append(f"Response: {response}")

        return "\n".join(history_parts)

    def clear(self):
        """Clear all memory (use with caution!)."""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM conversations')
        cursor.execute('DELETE FROM interactions')
        cursor.execute('DELETE FROM decisions')
        cursor.execute('DELETE FROM patterns')
        cursor.execute('DELETE FROM memory_store')
        self.conn.commit()

        if self.collection is not None:
            try:
                self.chroma_client.delete_collection(f"{self.agent_id}_memories")
                self.collection = self.chroma_client.create_collection(
                    name=f"{self.agent_id}_memories"
                )
            except:
                pass

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        cursor = self.conn.cursor()

        stats = {}

        cursor.execute('SELECT COUNT(*) FROM conversations')
        stats['total_conversations'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM interactions')
        stats['total_interactions'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM decisions')
        stats['total_decisions'] = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM patterns')
        stats['total_patterns'] = cursor.fetchone()[0]

        if self.collection is not None:
            try:
                stats['semantic_memories'] = self.collection.count()
            except:
                stats['semantic_memories'] = 0

        return stats


class MemoryManager:
    """
    Orchestrates short-term and long-term memory.

    This is the main interface agents use for memory.
    """

    def __init__(self, agent_id: str, db_path: str = "./data/memory"):
        self.agent_id = agent_id
        self.short_term = ShortTermMemory(max_size_mb=50)
        self.long_term = LongTermMemory(agent_id, db_path)

    def store_interaction(self, message: Any, response: Any, conversation_id: str):
        """
        Store an interaction in both short and long-term memory.
        """
        # Short-term: Store full objects for quick access
        key = f"interaction_{conversation_id}_{datetime.now().timestamp()}"
        self.short_term.store(key, {
            'message': message,
            'response': response,
            'timestamp': datetime.now()
        }, category='conversation')

        # Long-term: Persist for learning
        self.long_term.store_interaction(message, response, conversation_id)

    def retrieve_relevant(self,
                         query: str,
                         conversation_id: Optional[str] = None,
                         limit: int = 5) -> str:
        """
        Retrieve relevant context from memory.

        Uses semantic search to find the most relevant past interactions.
        """
        # Try semantic search first
        results = self.long_term.retrieve_semantic(query, n_results=limit)

        if not results:
            return ""

        # Format as context
        context_parts = ["## Relevant Past Context\n"]
        for i, result in enumerate(results, 1):
            context_parts.append(f"### Memory {i}")
            context_parts.append(result['content'])
            if result.get('metadata'):
                context_parts.append(f"_Timestamp: {result['metadata'].get('timestamp', 'unknown')}_")
            context_parts.append("")

        return "\n".join(context_parts)

    def get_conversation_history(self, conversation_id: str) -> str:
        """Get full conversation history."""
        # Check short-term first
        history = self.short_term.retrieve(f"conversation_{conversation_id}")
        if history:
            return str(history)

        # Fall back to long-term
        return self.long_term.get_conversation_history(conversation_id)

    def consolidate(self):
        """
        Consolidate short-term memories to long-term.

        Called periodically (e.g., end of day) to:
        - Move completed conversations to long-term
        - Extract patterns from recent data
        - Summarize and archive
        """
        # Get all conversations from short-term
        conversations = self.short_term.get_all_conversations()

        for conv_id, conv_data in conversations.items():
            # TODO: Implement summarization logic
            # For now, just mark as consolidated
            pass

        # Clear old short-term data (older than 1 day)
        self.short_term.clear_old_data(datetime.now() - timedelta(days=1))

    def get_stats(self) -> Dict[str, Any]:
        """Get combined memory statistics."""
        return {
            'short_term': self.short_term.get_stats(),
            'long_term': self.long_term.get_stats(),
            'agent_id': self.agent_id
        }

    def get_size_mb(self) -> float:
        """Get total memory size in MB."""
        return self.short_term._get_size_mb()

    def get_interaction_count(self) -> int:
        """Get total number of interactions stored."""
        return self.long_term.get_stats().get('total_interactions', 0)

    def clear(self):
        """Clear all memory (use with caution!)."""
        self.short_term.clear_category('conversation')
        self.short_term.clear_category('working')
        self.short_term.clear_category('cache')
        self.long_term.clear()
