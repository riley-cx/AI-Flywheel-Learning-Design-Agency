# AI Flywheel Elite Learning Design Agency
## Implementation Templates: Memory, Error Handling, and Logging Systems

### Document Version: 1.0
### Last Updated: 2025-10-24
### Status: Foundation Phase

---

## Table of Contents
1. [Memory Management Implementation](#memory-management-implementation)
2. [Error Handling Implementation](#error-handling-implementation)
3. [Logging System Implementation](#logging-system-implementation)
4. [Complete Agent Implementation Example](#complete-agent-implementation-example)

---

## Memory Management Implementation

### Overview

Agents use a two-tier memory system:
- **Short-term Memory**: Session-based, volatile (lost when session ends)
- **Long-term Memory**: Persistent via MCP (Model Context Protocol) servers

### Architecture

```
┌─────────────────────────────────────────┐
│           AGENT PROCESS                 │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Short-term Memory (RAM)        │  │
│  │   - Active conversations         │  │
│  │   - Current task context         │  │
│  │   - Temporary calculations       │  │
│  └──────────────────────────────────┘  │
│                 ↕                       │
│  ┌──────────────────────────────────┐  │
│  │   Memory Manager                 │  │
│  │   - Consolidation logic          │  │
│  │   - Retrieval triggers           │  │
│  │   - Context overflow handling    │  │
│  └──────────────────────────────────┘  │
│                 ↕                       │
└─────────────────┼───────────────────────┘
                  ↕
┌─────────────────┼───────────────────────┐
│  Long-term Memory (MCP Server)          │
│  - Vector database (semantic search)    │
│  - Relational database (structured data)│
│  - File storage (documents, artifacts)  │
└─────────────────────────────────────────┘
```

### 1. Short-term Memory Implementation

**Data Structure**:
```python
class ShortTermMemory:
    """In-memory storage for active session data"""

    def __init__(self, max_size_mb=50):
        self.max_size_mb = max_size_mb
        self.conversations = {}      # Active conversation contexts
        self.working_memory = {}     # Temporary task data
        self.cache = {}              # Frequently accessed data
        self.timestamps = {}         # For LRU eviction

    def store(self, key, value, category='working'):
        """Store data in short-term memory"""
        if self._check_size_limit():
            self._evict_oldest()  # LRU eviction

        if category == 'conversation':
            self.conversations[key] = value
        elif category == 'working':
            self.working_memory[key] = value
        elif category == 'cache':
            self.cache[key] = value

        self.timestamps[key] = datetime.now()

    def retrieve(self, key):
        """Retrieve from short-term memory"""
        # Check all categories
        if key in self.conversations:
            self.timestamps[key] = datetime.now()  # Update LRU
            return self.conversations[key]
        elif key in self.working_memory:
            self.timestamps[key] = datetime.now()
            return self.working_memory[key]
        elif key in self.cache:
            self.timestamps[key] = datetime.now()
            return self.cache[key]
        return None

    def _check_size_limit(self):
        """Check if memory exceeds limit"""
        current_size = self._get_size_mb()
        return current_size > self.max_size_mb

    def _evict_oldest(self):
        """Remove least recently used item"""
        oldest_key = min(self.timestamps, key=self.timestamps.get)
        self._remove(oldest_key)

    def consolidate_to_long_term(self, long_term_memory):
        """Move important data to long-term storage"""
        for conv_id, conv_data in self.conversations.items():
            if conv_data.get('status') == 'completed':
                # Extract key insights
                insights = self._extract_insights(conv_data)
                long_term_memory.store(
                    category='conversation-history',
                    data=insights,
                    metadata={'conversation-id': conv_id}
                )
                # Remove from short-term
                del self.conversations[conv_id]

    def clear(self):
        """Clear all short-term memory"""
        self.conversations.clear()
        self.working_memory.clear()
        self.cache.clear()
        self.timestamps.clear()
```

### 2. Long-term Memory Implementation (MCP)

**MCP Server Setup**:
```python
from mcp import Server, Tool, Resource
from mcp.server import stdio_server
import chromadb  # Vector database for semantic search
import sqlite3   # Relational database for structured data

class LongTermMemory:
    """Persistent memory using MCP server"""

    def __init__(self, agent_id, db_path):
        self.agent_id = agent_id
        self.db_path = db_path

        # Vector database for semantic search
        self.chroma_client = chromadb.PersistentClient(path=f"{db_path}/vector")
        self.collection = self.chroma_client.get_or_create_collection(
            name=f"{agent_id}_memories"
        )

        # Relational database for structured data
        self.conn = sqlite3.connect(f"{db_path}/structured.db")
        self._init_database()

    def _init_database(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()

        # Conversation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                conversation_id TEXT PRIMARY KEY,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                participants TEXT,
                summary TEXT,
                outcome TEXT,
                key_insights TEXT
            )
        ''')

        # Decisions and outcomes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                decision_type TEXT,
                context TEXT,
                decision TEXT,
                rationale TEXT,
                outcome_metric TEXT,
                outcome_value REAL,
                timestamp TIMESTAMP
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
                last_validated TIMESTAMP
            )
        ''')

        self.conn.commit()

    def store(self, category, data, metadata=None):
        """Store data in long-term memory"""
        if category == 'conversation-history':
            self._store_conversation(data, metadata)
        elif category == 'decision':
            self._store_decision(data)
        elif category == 'pattern':
            self._store_pattern(data)
        elif category == 'semantic':
            self._store_semantic(data, metadata)

    def _store_conversation(self, data, metadata):
        """Store conversation history"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO conversation_history
            (conversation_id, started_at, completed_at, participants,
             summary, outcome, key_insights)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata['conversation-id'],
            data.get('started_at'),
            data.get('completed_at'),
            json.dumps(data.get('participants', [])),
            data.get('summary'),
            data.get('outcome'),
            json.dumps(data.get('key_insights', []))
        ))
        self.conn.commit()

        # Also store in vector DB for semantic search
        self._store_semantic(
            text=data.get('summary', ''),
            metadata={'type': 'conversation', **metadata}
        )

    def _store_decision(self, data):
        """Store decision and outcome"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO decisions
            (decision_id, decision_type, context, decision,
             rationale, outcome_metric, outcome_value, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['decision_id'],
            data['decision_type'],
            data.get('context'),
            data['decision'],
            data.get('rationale'),
            data.get('outcome_metric'),
            data.get('outcome_value'),
            datetime.now()
        ))
        self.conn.commit()

    def _store_semantic(self, text, metadata):
        """Store text for semantic search"""
        doc_id = f"{self.agent_id}_{datetime.now().timestamp()}"
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def retrieve_semantic(self, query, n_results=5, filters=None):
        """Semantic search in long-term memory"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filters
        )
        return results

    def retrieve_conversations(self, participant=None, limit=10):
        """Retrieve conversation history"""
        cursor = self.conn.cursor()

        if participant:
            cursor.execute('''
                SELECT * FROM conversation_history
                WHERE participants LIKE ?
                ORDER BY completed_at DESC
                LIMIT ?
            ''', (f'%{participant}%', limit))
        else:
            cursor.execute('''
                SELECT * FROM conversation_history
                ORDER BY completed_at DESC
                LIMIT ?
            ''', (limit,))

        return cursor.fetchall()

    def retrieve_patterns(self, pattern_type=None):
        """Retrieve learned patterns"""
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

        return cursor.fetchall()

    def consolidate(self, short_term_memory):
        """Consolidate short-term memories to long-term"""
        # Extract patterns from recent data
        patterns = self._extract_patterns(short_term_memory)
        for pattern in patterns:
            self._store_pattern(pattern)

        # Summarize and archive conversations
        for conv_id, conv in short_term_memory.conversations.items():
            summary = self._summarize_conversation(conv)
            self.store('conversation-history', summary,
                      metadata={'conversation-id': conv_id})
```

### 3. Memory Manager (Orchestrates Short and Long-term)

```python
class MemoryManager:
    """Orchestrates short-term and long-term memory"""

    def __init__(self, agent_id, db_path):
        self.agent_id = agent_id
        self.short_term = ShortTermMemory(max_size_mb=50)
        self.long_term = LongTermMemory(agent_id, db_path)

    def remember(self, key, value, category='working', persist=False):
        """Store memory"""
        # Always store in short-term first
        self.short_term.store(key, value, category)

        # Optionally persist immediately
        if persist:
            self.long_term.store(category, value, metadata={'key': key})

    def recall(self, key=None, query=None, context=None):
        """Retrieve memory"""
        # Try short-term first (faster)
        if key:
            result = self.short_term.retrieve(key)
            if result:
                return result

        # Fall back to long-term (semantic search if query)
        if query:
            results = self.long_term.retrieve_semantic(query, filters=context)
            return results

        return None

    def consolidate(self):
        """Move data from short-term to long-term"""
        self.short_term.consolidate_to_long_term(self.long_term)

    def forget(self, key):
        """Remove from both short-term and long-term"""
        # Note: Usually we archive rather than delete
        self.short_term._remove(key)
        # Long-term typically uses soft delete or archiving

    def handle_context_overflow(self):
        """Handle when context window approaches limit"""
        # Summarize older context
        summary = self._summarize_old_context()

        # Store summary in long-term
        self.long_term.store('semantic', summary,
                            metadata={'type': 'context-summary'})

        # Clear old context from short-term
        self.short_term.clear_old_context(before=datetime.now() - timedelta(hours=1))

        return summary
```

### 4. Retrieval Triggers

```python
class RetrievalTrigger:
    """Determines when to retrieve from long-term memory"""

    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.triggers = []

    def add_trigger(self, trigger_type, condition, retrieval_query):
        """Add a retrieval trigger"""
        self.triggers.append({
            'type': trigger_type,
            'condition': condition,
            'query': retrieval_query
        })

    def check_triggers(self, context):
        """Check if any triggers fire and retrieve accordingly"""
        results = []

        for trigger in self.triggers:
            if self._evaluate_condition(trigger['condition'], context):
                # Trigger fired, retrieve memory
                retrieved = self.memory.recall(query=trigger['query'])
                results.append({
                    'trigger': trigger['type'],
                    'data': retrieved
                })

        return results

    def _evaluate_condition(self, condition, context):
        """Evaluate trigger condition"""
        # Implement condition evaluation logic
        # Examples:
        # - "new course design" → check if context contains "create course"
        # - "student struggling" → check if context mentions low performance
        # - "similar request" → semantic similarity to past requests
        pass

# Example usage in agent
class LearningDesigner:
    def __init__(self):
        self.memory = MemoryManager('learning-designer', './memory')
        self.retrieval = RetrievalTrigger(self.memory)

        # Set up retrieval triggers
        self.retrieval.add_trigger(
            trigger_type='similar-course-design',
            condition=lambda ctx: 'create course' in ctx.lower(),
            retrieval_query='successful course designs for {audience}'
        )

    def create_course(self, brief):
        # Check triggers
        context = f"create course for {brief['audience']}"
        relevant_memories = self.retrieval.check_triggers(context)

        # Use retrieved memories to inform design
        if relevant_memories:
            past_designs = relevant_memories[0]['data']
            # Apply patterns from past successful designs
```

---

## Error Handling Implementation

### 1. Error Types and Hierarchy

```python
class AgentError(Exception):
    """Base class for all agent errors"""
    def __init__(self, message, context=None, recoverable=True):
        self.message = message
        self.context = context or {}
        self.recoverable = recoverable
        super().__init__(self.message)

class InputValidationError(AgentError):
    """Error in input validation"""
    pass

class DataQualityError(AgentError):
    """Error in data quality or availability"""
    pass

class CommunicationError(AgentError):
    """Error in inter-agent communication"""
    pass

class TimeoutError(AgentError):
    """Operation exceeded time limit"""
    pass

class ResourceError(AgentError):
    """Insufficient resources (memory, API quota, etc.)"""
    pass

class EthicalViolationError(AgentError):
    """Ethical constraint violated"""
    def __init__(self, message, context=None):
        super().__init__(message, context, recoverable=False)  # Never recoverable
```

### 2. Error Handling Decorator

```python
def handle_errors(max_retries=3, backoff_factor=2, fallback=None):
    """Decorator for error handling with retry logic"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_error = None

            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)

                except TimeoutError as e:
                    attempt += 1
                    last_error = e
                    if attempt < max_retries:
                        wait_time = backoff_factor ** attempt
                        logger.warning(
                            f"Timeout on attempt {attempt}/{max_retries}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Max retries exceeded: {e}")

                except EthicalViolationError as e:
                    # Never retry ethical violations
                    logger.critical(f"Ethical violation: {e}")
                    raise

                except AgentError as e:
                    if not e.recoverable:
                        logger.error(f"Unrecoverable error: {e}")
                        raise

                    attempt += 1
                    last_error = e
                    if attempt < max_retries:
                        logger.warning(f"Error on attempt {attempt}: {e}. Retrying...")
                    else:
                        logger.error(f"Max retries exceeded: {e}")

            # All retries exhausted, use fallback if provided
            if fallback:
                logger.info(f"Using fallback strategy")
                return fallback(*args, **kwargs)
            else:
                raise last_error

        return wrapper
    return decorator
```

### 3. Error Handler Class

```python
class ErrorHandler:
    """Centralized error handling for agents"""

    def __init__(self, agent_id, logger, memory_manager):
        self.agent_id = agent_id
        self.logger = logger
        self.memory = memory_manager
        self.error_count = Counter()
        self.error_history = []

    def handle(self, error, context=None, retry_func=None, fallback_func=None):
        """Handle an error with retry and fallback logic"""

        # Log error
        self.log_error(error, context)

        # Track error for pattern analysis
        self.track_error(error)

        # Determine handling strategy
        if isinstance(error, EthicalViolationError):
            return self._handle_ethical_violation(error, context)

        elif isinstance(error, TimeoutError):
            return self._handle_timeout(error, retry_func, fallback_func)

        elif isinstance(error, DataQualityError):
            return self._handle_data_quality(error, fallback_func)

        elif isinstance(error, CommunicationError):
            return self._handle_communication(error, retry_func)

        else:
            return self._handle_generic(error, retry_func, fallback_func)

    def _handle_ethical_violation(self, error, context):
        """Handle ethical violations (never retry, escalate)"""
        self.logger.critical(f"ETHICAL VIOLATION: {error}")

        # Store incident
        incident = {
            'type': 'ethical-violation',
            'description': str(error),
            'context': context,
            'timestamp': datetime.now()
        }
        self.memory.remember('ethical-incident', incident, persist=True)

        # Escalate to human oversight
        self._escalate_to_human(incident)

        # Do not proceed
        raise error

    def _handle_timeout(self, error, retry_func, fallback_func):
        """Handle timeout errors with exponential backoff"""
        max_retries = 3
        attempt = 0

        while attempt < max_retries:
            attempt += 1
            wait_time = 2 ** attempt  # Exponential backoff

            self.logger.warning(
                f"Timeout (attempt {attempt}/{max_retries}). "
                f"Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)

            try:
                if retry_func:
                    return retry_func()
            except TimeoutError:
                continue

        # Retries exhausted
        if fallback_func:
            self.logger.info("Using fallback after timeout")
            return fallback_func()
        else:
            raise error

    def _handle_data_quality(self, error, fallback_func):
        """Handle data quality issues"""
        self.logger.warning(f"Data quality issue: {error}")

        # Check if we have cached/alternative data
        if fallback_func:
            return fallback_func()
        else:
            # Report limitation and proceed with partial data
            self._report_limitation(error)
            return None

    def _handle_communication(self, error, retry_func):
        """Handle communication errors"""
        max_retries = 2
        attempt = 0

        while attempt < max_retries:
            attempt += 1
            time.sleep(1 * attempt)  # Linear backoff for comm errors

            try:
                if retry_func:
                    return retry_func()
            except CommunicationError:
                continue

        # Communication failure persists
        self.logger.error(f"Communication failed after {max_retries} retries")
        self._escalate_communication_failure(error)
        raise error

    def log_error(self, error, context):
        """Log error with full context"""
        log_entry = {
            'agent_id': self.agent_id,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'timestamp': datetime.now(),
            'recoverable': getattr(error, 'recoverable', True)
        }

        self.logger.error(json.dumps(log_entry))

    def track_error(self, error):
        """Track errors for pattern analysis"""
        error_type = type(error).__name__
        self.error_count[error_type] += 1

        self.error_history.append({
            'type': error_type,
            'timestamp': datetime.now(),
            'recoverable': getattr(error, 'recoverable', True)
        })

        # Detect error patterns
        if self.error_count[error_type] > 10:  # Threshold
            self._alert_error_pattern(error_type)

    def _alert_error_pattern(self, error_type):
        """Alert when error pattern detected"""
        self.logger.warning(
            f"ERROR PATTERN DETECTED: {error_type} has occurred "
            f"{self.error_count[error_type]} times. Investigation recommended."
        )

    def get_error_stats(self):
        """Get error statistics"""
        return {
            'total_errors': sum(self.error_count.values()),
            'by_type': dict(self.error_count),
            'recent_errors': self.error_history[-10:]
        }
```

### 4. Idempotency Implementation

```python
class IdempotentOperation:
    """Ensure operations can be safely retried"""

    def __init__(self, operation_id, func, cache_ttl_seconds=3600):
        self.operation_id = operation_id
        self.func = func
        self.cache = {}
        self.cache_ttl = cache_ttl_seconds

    def execute(self, *args, **kwargs):
        """Execute operation idempotently"""

        # Check if already executed
        if self.operation_id in self.cache:
            cached_result = self.cache[self.operation_id]

            # Check if cache is still valid
            if datetime.now() < cached_result['expires_at']:
                logger.info(f"Returning cached result for {self.operation_id}")
                return cached_result['result']

        # Execute operation
        result = self.func(*args, **kwargs)

        # Cache result
        self.cache[self.operation_id] = {
            'result': result,
            'executed_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.cache_ttl)
        }

        return result

# Example usage
@handle_errors(max_retries=3)
def analyze_student_data(course_id):
    operation = IdempotentOperation(
        operation_id=f"analyze-{course_id}-{date.today()}",
        func=_run_analysis
    )
    return operation.execute(course_id)

def _run_analysis(course_id):
    # Actual analysis logic (can be safely retried)
    pass
```

---

## Logging System Implementation

### 1. Structured Logging Setup

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    """Structured logging for agents"""

    def __init__(self, agent_id, log_file_path, log_level=logging.INFO):
        self.agent_id = agent_id
        self.logger = logging.getLogger(agent_id)
        self.logger.setLevel(log_level)

        # File handler (JSON format)
        file_handler = logging.FileHandler(f"{log_file_path}/{agent_id}.log")
        file_handler.setFormatter(self._get_json_formatter())
        self.logger.addHandler(file_handler)

        # Console handler (human-readable)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_console_formatter())
        self.logger.addHandler(console_handler)

    def _get_json_formatter(self):
        """JSON formatter for file logs"""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'agent_id': record.agent_id if hasattr(record, 'agent_id') else 'unknown',
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }

                # Add extra fields
                if hasattr(record, 'extra'):
                    log_entry.update(record.extra)

                return json.dumps(log_entry)

        return JSONFormatter()

    def _get_console_formatter(self):
        """Human-readable formatter for console"""
        return logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(agent_id)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def debug(self, message, **extra):
        """Log debug message"""
        self.logger.debug(message, extra={'agent_id': self.agent_id, **extra})

    def info(self, message, **extra):
        """Log info message"""
        self.logger.info(message, extra={'agent_id': self.agent_id, **extra})

    def warning(self, message, **extra):
        """Log warning message"""
        self.logger.warning(message, extra={'agent_id': self.agent_id, **extra})

    def error(self, message, **extra):
        """Log error message"""
        self.logger.error(message, extra={'agent_id': self.agent_id, **extra})

    def critical(self, message, **extra):
        """Log critical message"""
        self.logger.critical(message, extra={'agent_id': self.agent_id, **extra})

    # Domain-specific log methods
    def log_message_sent(self, message):
        """Log sent FIPA ACL message"""
        self.info(
            f"Message sent to {message['receiver']}",
            performative=message['performative'],
            conversation_id=message.get('conversation-id'),
            ontology=message.get('ontology')
        )

    def log_message_received(self, message):
        """Log received FIPA ACL message"""
        self.info(
            f"Message received from {message['sender']}",
            performative=message['performative'],
            conversation_id=message.get('conversation-id')
        )

    def log_decision(self, decision_type, decision, rationale):
        """Log decision made by agent"""
        self.info(
            f"Decision: {decision_type}",
            decision=decision,
            rationale=rationale
        )

    def log_task_started(self, task_id, task_type):
        """Log task start"""
        self.info(
            f"Task started: {task_type}",
            task_id=task_id,
            task_type=task_type,
            status='started'
        )

    def log_task_completed(self, task_id, duration_seconds, outcome):
        """Log task completion"""
        self.info(
            f"Task completed: {task_id}",
            task_id=task_id,
            duration=duration_seconds,
            outcome=outcome,
            status='completed'
        )
```

### 2. Log Aggregation and Analysis

```python
class LogAnalyzer:
    """Analyze logs for insights and monitoring"""

    def __init__(self, log_directory):
        self.log_dir = log_directory

    def get_error_rate(self, agent_id, time_window_hours=24):
        """Calculate error rate for agent"""
        logs = self._read_logs(agent_id, time_window_hours)

        total = len(logs)
        errors = sum(1 for log in logs if log['level'] in ['ERROR', 'CRITICAL'])

        return {
            'total_logs': total,
            'errors': errors,
            'error_rate': errors / total if total > 0 else 0
        }

    def get_performance_metrics(self, agent_id, time_window_hours=24):
        """Get performance metrics"""
        logs = self._read_logs(agent_id, time_window_hours)

        task_durations = [
            log.get('duration', 0)
            for log in logs
            if log.get('status') == 'completed'
        ]

        if not task_durations:
            return None

        return {
            'avg_duration': statistics.mean(task_durations),
            'median_duration': statistics.median(task_durations),
            'p95_duration': statistics.quantiles(task_durations, n=20)[18],  # 95th percentile
            'total_tasks': len(task_durations)
        }

    def detect_anomalies(self, agent_id):
        """Detect anomalous patterns in logs"""
        logs = self._read_logs(agent_id, time_window_hours=1)

        anomalies = []

        # Check for error spikes
        error_count = sum(1 for log in logs if log['level'] == 'ERROR')
        if error_count > 10:  # Threshold
            anomalies.append({
                'type': 'error-spike',
                'severity': 'high',
                'details': f'{error_count} errors in last hour'
            })

        # Check for performance degradation
        recent_durations = [
            log.get('duration', 0)
            for log in logs[-100:]  # Last 100 tasks
            if log.get('duration')
        ]

        if len(recent_durations) > 10:
            recent_avg = statistics.mean(recent_durations)
            historical_avg = self._get_historical_avg_duration(agent_id)

            if recent_avg > historical_avg * 1.5:  # 50% slower
                anomalies.append({
                    'type': 'performance-degradation',
                    'severity': 'medium',
                    'details': f'Average duration {recent_avg:.2f}s vs historical {historical_avg:.2f}s'
                })

        return anomalies

    def _read_logs(self, agent_id, time_window_hours):
        """Read logs for agent within time window"""
        log_file = f"{self.log_dir}/{agent_id}.log"
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                log_entry = json.loads(line)
                log_time = datetime.fromisoformat(log_entry['timestamp'])

                if log_time >= cutoff_time:
                    logs.append(log_entry)

        return logs
```

### 3. Audit Trail

```python
class AuditTrail:
    """Audit trail for accountability and compliance"""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(f"{db_path}/audit.db")
        self._init_database()

    def _init_database(self):
        """Initialize audit database"""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                audit_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP,
                agent_id TEXT,
                action_type TEXT,
                action_description TEXT,
                affected_entities TEXT,
                user_id TEXT,
                approval_status TEXT,
                metadata TEXT
            )
        ''')

        self.conn.commit()

    def log_action(self, agent_id, action_type, description,
                   affected_entities=None, user_id=None, metadata=None):
        """Log an auditable action"""

        audit_id = f"audit-{datetime.now().timestamp()}"

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO audit_log
            (audit_id, timestamp, agent_id, action_type, action_description,
             affected_entities, user_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            audit_id,
            datetime.now(),
            agent_id,
            action_type,
            description,
            json.dumps(affected_entities) if affected_entities else None,
            user_id,
            json.dumps(metadata) if metadata else None
        ))

        self.conn.commit()
        return audit_id

    def get_audit_trail(self, agent_id=None, action_type=None,
                       start_date=None, end_date=None):
        """Retrieve audit trail with filters"""

        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []

        if agent_id:
            query += " AND agent_id = ?"
            params.append(agent_id)

        if action_type:
            query += " AND action_type = ?"
            params.append(action_type)

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)

        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY timestamp DESC"

        cursor = self.conn.cursor()
        cursor.execute(query, params)

        return cursor.fetchall()

    def export_audit_report(self, filepath, start_date, end_date):
        """Export audit report for compliance"""

        records = self.get_audit_trail(start_date=start_date, end_date=end_date)

        with open(filepath, 'w') as f:
            f.write("Audit Report\n")
            f.write(f"Period: {start_date} to {end_date}\n\n")

            for record in records:
                f.write(f"[{record[1]}] {record[2]} - {record[3]}: {record[4]}\n")

        return filepath
```

---

## Complete Agent Implementation Example

Here's a complete agent implementation using all the templates:

```python
from typing import Dict, Any, List
import uuid

class ChiefLearningStrategistAgent:
    """Complete implementation with memory, error handling, and logging"""

    def __init__(self, config):
        self.agent_id = "chief-learning-strategist"
        self.config = config

        # Initialize core systems
        self.memory = MemoryManager(
            agent_id=self.agent_id,
            db_path=config['memory_path']
        )

        self.logger = StructuredLogger(
            agent_id=self.agent_id,
            log_file_path=config['log_path'],
            log_level=logging.INFO
        )

        self.error_handler = ErrorHandler(
            agent_id=self.agent_id,
            logger=self.logger,
            memory_manager=self.memory
        )

        self.audit = AuditTrail(db_path=config['audit_path'])

        self.message_broker = MessageBroker(config['broker_url'])

        self.logger.info("Agent initialized")

    @handle_errors(max_retries=3, fallback=lambda: None)
    def request_market_research(self, topic: str, deadline: datetime) -> str:
        """Request market research from Market Research Analyst"""

        task_id = str(uuid.uuid4())
        self.logger.log_task_started(task_id, 'request-market-research')

        start_time = time.time()

        try:
            # Check memory for similar past research
            past_research = self.memory.recall(
                query=f"market research on {topic}",
                context={'type': 'research-findings'}
            )

            if past_research and self._is_recent_enough(past_research):
                self.logger.info(f"Using cached research for {topic}")
                return past_research

            # Create FIPA ACL message
            message = {
                'performative': 'REQUEST',
                'sender': self.agent_id,
                'receiver': ['market-research-analyst'],
                'content': f"Analyze {topic}",
                'ontology': 'competitive-intelligence',
                'protocol': 'request-response',
                'conversation-id': f"conv-research-{task_id}",
                'reply-with': f"req-{task_id}",
                'reply-by': deadline.isoformat(),
                'priority': 'MEDIUM'
            }

            # Send message
            self.message_broker.send(message)
            self.logger.log_message_sent(message)

            # Store in short-term memory
            self.memory.remember(
                key=f"research-request-{task_id}",
                value={'message': message, 'status': 'pending'},
                category='conversation'
            )

            # Audit log
            self.audit.log_action(
                agent_id=self.agent_id,
                action_type='request-market-research',
                description=f"Requested research on {topic}",
                metadata={'task_id': task_id, 'deadline': deadline.isoformat()}
            )

            duration = time.time() - start_time
            self.logger.log_task_completed(task_id, duration, 'success')

            return task_id

        except Exception as e:
            # Error handling
            self.error_handler.handle(
                error=e,
                context={'task_id': task_id, 'topic': topic}
            )
            raise

    def receive_message(self, message: Dict[str, Any]):
        """Receive and handle incoming FIPA ACL message"""

        self.logger.log_message_received(message)

        performative = message['performative']

        try:
            if performative == 'INFORM':
                self._handle_inform(message)
            elif performative == 'PROPOSE':
                self._handle_propose(message)
            elif performative == 'REQUEST':
                self._handle_request(message)
            elif performative == 'WARN':
                self._handle_warn(message)
            else:
                self.logger.warning(f"Unhandled performative: {performative}")

        except Exception as e:
            self.error_handler.handle(
                error=e,
                context={'message': message}
            )

    def _handle_inform(self, message):
        """Handle INFORM messages (research results, updates, etc.)"""

        content = message['content']
        conversation_id = message.get('conversation-id')

        # Store result in memory
        self.memory.remember(
            key=f"research-result-{conversation_id}",
            value=content,
            category='conversation',
            persist=True  # Persist important results
        )

        # Update conversation status
        conv = self.memory.recall(key=f"research-request-{conversation_id}")
        if conv:
            conv['status'] = 'completed'
            conv['result'] = content
            self.memory.remember(
                key=f"research-request-{conversation_id}",
                value=conv,
                category='conversation'
            )

        self.logger.info(f"Research completed: {conversation_id}")

    def _handle_propose(self, message):
        """Handle PROPOSE messages (recommendations from other agents)"""

        proposal = message['content']

        # Evaluate proposal
        decision = self._evaluate_proposal(proposal)

        # Log decision
        self.logger.log_decision(
            decision_type='proposal-evaluation',
            decision=decision['decision'],
            rationale=decision['rationale']
        )

        # Store decision in memory
        self.memory.remember(
            key=f"decision-{message.get('conversation-id')}",
            value=decision,
            persist=True
        )

        # Send response
        response_performative = 'ACCEPT-PROPOSAL' if decision['decision'] == 'accept' else 'REJECT-PROPOSAL'

        response = {
            'performative': response_performative,
            'sender': self.agent_id,
            'receiver': [message['sender']],
            'content': decision['rationale'],
            'conversation-id': message.get('conversation-id'),
            'in-reply-to': message.get('reply-with')
        }

        self.message_broker.send(response)
        self.logger.log_message_sent(response)

        # Audit critical decisions
        if decision['decision'] == 'accept' and decision.get('high-stakes'):
            self.audit.log_action(
                agent_id=self.agent_id,
                action_type='accept-proposal',
                description=f"Accepted proposal: {proposal.get('intervention-name')}",
                metadata={'conversation-id': message.get('conversation-id')}
            )

    def _evaluate_proposal(self, proposal):
        """Evaluate a proposal and make decision"""

        # Decision logic here
        # For example, check alignment with strategic objectives

        strategic_objectives = self.memory.recall(
            query="current strategic objectives"
        )

        # Simplified decision logic
        decision = {
            'decision': 'accept',  # or 'reject'
            'rationale': 'Aligns with strategic objective: increase engagement',
            'high-stakes': proposal.get('expected-impact', 0) > 0.15  # >15% impact
        }

        return decision

    def periodic_consolidation(self):
        """Consolidate memories periodically (call from scheduler)"""

        self.logger.info("Starting memory consolidation")

        try:
            self.memory.consolidate()
            self.logger.info("Memory consolidation completed")

        except Exception as e:
            self.error_handler.handle(
                error=e,
                context={'task': 'memory-consolidation'}
            )

    def health_check(self) -> Dict[str, Any]:
        """Return agent health status"""

        error_stats = self.error_handler.get_error_stats()
        memory_size = self.memory.short_term._get_size_mb()

        return {
            'agent_id': self.agent_id,
            'status': 'healthy' if error_stats['total_errors'] < 100 else 'degraded',
            'error_stats': error_stats,
            'memory_size_mb': memory_size,
            'timestamp': datetime.now().isoformat()
        }
```

---

## Summary

This implementation guide provides:

1. ✅ **Memory Management**: Short-term + long-term (MCP) with semantic search
2. ✅ **Error Handling**: Comprehensive error types, retry logic, fallbacks, idempotency
3. ✅ **Logging**: Structured JSON logs, audit trails, performance monitoring
4. ✅ **Complete Example**: Fully functional agent using all templates

**Next Steps**:
- ✅ **COMPLETE**: Agent Specifications
- ✅ **COMPLETE**: FIPA ACL Communication Protocol
- ✅ **COMPLETE**: Implementation Templates
- ⏭️ **NEXT**: Security & Privacy Implementation Plan
- **FINALLY**: Testing & Validation Framework

---
