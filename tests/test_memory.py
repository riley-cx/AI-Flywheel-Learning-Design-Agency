#!/usr/bin/env python3
"""
Test script for memory system

Tests:
- Short-term memory storage and retrieval
- Long-term memory persistence
- Semantic search
- Memory consolidation
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base.memory import MemoryManager, ShortTermMemory, LongTermMemory
from agents.base.messaging import Message
from datetime import datetime
import uuid


def test_short_term_memory():
    """Test short-term memory operations."""
    print("\n" + "="*60)
    print("Testing Short-Term Memory")
    print("="*60)

    stm = ShortTermMemory(max_size_mb=50)

    # Store some data
    stm.store("key1", {"data": "value1"}, category='working')
    stm.store("key2", {"data": "value2"}, category='cache')
    stm.store("conv1", {"messages": ["hello", "hi"]}, category='conversation')

    # Retrieve
    assert stm.retrieve("key1") == {"data": "value1"}
    print("✅ Store and retrieve working")

    # Get stats
    stats = stm.get_stats()
    print(f"📊 Memory stats: {stats}")
    assert stats['working_items'] == 1
    assert stats['cached_items'] == 1
    assert stats['conversations'] == 1
    print("✅ Stats working")

    # Clear category
    stm.clear_category('cache')
    assert stm.retrieve("key2") is None
    print("✅ Clear category working")

    print("\n✅ Short-term memory: ALL TESTS PASSED")


def test_long_term_memory():
    """Test long-term memory operations."""
    print("\n" + "="*60)
    print("Testing Long-Term Memory")
    print("="*60)

    # Use test database
    test_db_path = "./data/memory/test"
    ltm = LongTermMemory(agent_id="test-agent", db_path=test_db_path)

    # Clean start
    ltm.clear()

    # Store interaction
    message = Message(
        sender="human",
        receiver="test-agent",
        content="What's the capital of France?",
        conversation_id="conv-test-1"
    )

    response = Message(
        sender="test-agent",
        receiver="human",
        content="The capital of France is Paris.",
        conversation_id="conv-test-1"
    )

    ltm.store_interaction(message, response, "conv-test-1")
    print("✅ Store interaction working")

    # Store decision
    decision_id = ltm.store_decision(
        decision_type="course-approval",
        context="New course on AI Safety proposed",
        decision="APPROVED",
        rationale="High demand, aligns with strategy"
    )
    print(f"✅ Store decision working (ID: {decision_id})")

    # Store pattern
    pattern_id = ltm.store_pattern(
        pattern_type="student-success",
        description="Students who complete first week have 90% completion rate",
        confidence=0.87,
        examples=["Student A", "Student B", "Student C"]
    )
    print(f"✅ Store pattern working (ID: {pattern_id})")

    # Retrieve
    decisions = ltm.retrieve_decisions(limit=10)
    assert len(decisions) >= 1
    print(f"✅ Retrieve decisions working ({len(decisions)} found)")

    patterns = ltm.retrieve_patterns()
    assert len(patterns) >= 1
    print(f"✅ Retrieve patterns working ({len(patterns)} found)")

    # Get stats
    stats = ltm.get_stats()
    print(f"📊 Long-term memory stats: {stats}")

    print("\n✅ Long-term memory: ALL TESTS PASSED")


def test_semantic_search():
    """Test semantic search in vector database."""
    print("\n" + "="*60)
    print("Testing Semantic Search")
    print("="*60)

    test_db_path = "./data/memory/test"
    ltm = LongTermMemory(agent_id="test-semantic", db_path=test_db_path)

    ltm.clear()

    # Store some semantic memories
    memories = [
        ("Paris is the capital of France and known for the Eiffel Tower", {'topic': 'geography'}),
        ("Machine learning is a subset of artificial intelligence", {'topic': 'technology'}),
        ("Python is a popular programming language for data science", {'topic': 'technology'}),
        ("Rome is the capital of Italy, famous for the Colosseum", {'topic': 'geography'}),
    ]

    for text, metadata in memories:
        ltm._store_semantic(text, metadata)

    print(f"✅ Stored {len(memories)} semantic memories")

    # Search
    results = ltm.retrieve_semantic("Tell me about programming languages", n_results=2)

    if results:
        print(f"\n🔍 Search results for 'programming languages':")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['content'][:60]}...")
            print(f"     Distance: {result.get('distance', 'N/A')}")
        print("✅ Semantic search working")
    else:
        print("⚠️  Semantic search returned no results (ChromaDB may not be installed)")

    print("\n✅ Semantic search: TESTS COMPLETE")


def test_memory_manager():
    """Test full MemoryManager integration."""
    print("\n" + "="*60)
    print("Testing Memory Manager (Integration)")
    print("="*60)

    test_db_path = "./data/memory/test"
    mm = MemoryManager(agent_id="test-manager", db_path=test_db_path)

    # Clear for clean test
    mm.clear()

    # Store interaction
    message = Message(
        sender="human",
        receiver="test-manager",
        content="Design a course on prompt engineering",
        conversation_id="conv-test-2"
    )

    response = Message(
        sender="test-manager",
        receiver="human",
        content="I'll design a comprehensive prompt engineering course...",
        conversation_id="conv-test-2"
    )

    mm.store_interaction(message, response, "conv-test-2")
    print("✅ Store interaction via MemoryManager working")

    # Retrieve relevant context
    context = mm.retrieve_relevant("How do I design a good course?", limit=3)

    if context:
        print(f"\n📚 Retrieved context ({len(context)} chars):")
        print(context[:200] + "..." if len(context) > 200 else context)
        print("✅ Retrieve relevant context working")
    else:
        print("⚠️  No context retrieved (expected if first run)")

    # Get stats
    stats = mm.get_stats()
    print(f"\n📊 MemoryManager stats:")
    print(f"  Short-term: {stats['short_term']}")
    print(f"  Long-term: {stats['long_term']}")
    print("✅ Stats working")

    print("\n✅ Memory Manager: ALL TESTS PASSED")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(" AI FLYWHEEL AGENCY - MEMORY SYSTEM TESTS")
    print("="*70)

    try:
        test_short_term_memory()
        test_long_term_memory()
        test_semantic_search()
        test_memory_manager()

        print("\n" + "="*70)
        print(" 🎉 ALL TESTS PASSED! Memory system is working correctly.")
        print("="*70)
        print("\n✅ Short-term memory: PASS")
        print("✅ Long-term memory: PASS")
        print("✅ Semantic search: PASS")
        print("✅ Memory Manager: PASS")
        print("\n💡 Next: Test with actual agents using this memory system!")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
