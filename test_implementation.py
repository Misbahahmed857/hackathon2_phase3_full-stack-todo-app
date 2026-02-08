#!/usr/bin/env python3
"""
Quick test script to verify the AI agent implementation.
"""
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        from agents.ai_agent import AIAgent
        from agents.intent_classifier import classify_intent
        from mcp_tools.task_tools import create_add_task_tool
        from mcp_tools.tool_registry import ToolRegistry
        from api.chat_endpoint import router
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_intent_classification():
    """Test intent classification functionality."""
    try:
        # Test CREATE_TASK intent
        result = classify_intent("Add a task to buy groceries")
        assert result['intent_type'] == 'CREATE_TASK'
        print("✓ CREATE_TASK intent classified correctly")

        # Test LIST_TASKS intent
        result = classify_intent("Show me my tasks")
        assert result['intent_type'] == 'LIST_TASKS'
        print("✓ LIST_TASKS intent classified correctly")

        # Test UNKNOWN intent
        result = classify_intent("This is not a valid task command")
        assert result['intent_type'] == 'UNKNOWN'
        print("✓ UNKNOWN intent classified correctly")

        return True
    except Exception as e:
        print(f"✗ Intent classification test failed: {e}")
        return False

def test_agent_creation():
    """Test AI agent creation (without actual API key)."""
    try:
        # We'll test that the agent can be initialized with a mock key
        import os
        os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'

        agent = AIAgent()
        assert agent is not None
        assert hasattr(agent, 'system_prompt')
        print("✓ AI Agent created successfully")

        # Clean up
        del os.environ['OPENAI_API_KEY']
        return True
    except Exception as e:
        print(f"✗ AI Agent creation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing AI Agent Implementation...")
    print("=" * 40)

    all_passed = True

    all_passed &= test_imports()
    all_passed &= test_intent_classification()
    all_passed &= test_agent_creation()

    print("=" * 40)
    if all_passed:
        print("✓ All tests passed! AI Agent implementation is working.")
        return 0
    else:
        print("✗ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())