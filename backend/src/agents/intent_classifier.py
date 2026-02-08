"""
Intent detection and classification logic for the AI agent.

This module implements intent classification to detect user intentions from natural language
input using the OpenAI Agents SDK's built-in capabilities for flexible language handling.
"""
from typing import Dict, Any, Optional
import re


def classify_intent(user_input: str) -> Dict[str, Any]:
    """
    Classify the intent from user input.

    Args:
        user_input: Natural language input from user

    Returns:
        Dictionary containing intent type and extracted parameters
    """
    user_input_lower = user_input.lower().strip()

    # Simple pattern matching for MVP - in production, we'd use the OpenAI LLM for this
    if any(word in user_input_lower for word in ['add', 'create', 'remember', 'make', 'new task']):
        # Extract task title using regex
        title_match = re.search(r'(?:to|that|for)\s+(.+?)(?:\s+tomorrow|\s+today|\s+next|\s+later|$)', user_input_lower)
        if not title_match:
            title_match = re.search(r'(?:add|create|remember|make)\s+(?:a\s+|an\s+)?(.+?)(?:\s+for|\s+that|\s+to|$)', user_input_lower)

        title = title_match.group(1).strip() if title_match else user_input

        return {
            'intent_type': 'CREATE_TASK',
            'confidence_score': 0.9,
            'extracted_parameters': {
                'title': title,
                'description': '',
                'due_date': None
            }
        }

    elif any(word in user_input_lower for word in ['show', 'list', 'my tasks', 'what do i have', 'view', 'all tasks']):
        status_filter = 'all'
        if 'pending' in user_input_lower or 'incomplete' in user_input_lower:
            status_filter = 'pending'
        elif 'completed' in user_input_lower or 'done' in user_input_lower:
            status_filter = 'completed'

        return {
            'intent_type': 'LIST_TASKS',
            'confidence_score': 0.9,
            'extracted_parameters': {
                'status': status_filter
            }
        }

    elif any(word in user_input_lower for word in ['complete', 'done', 'finish', 'mark as', 'check off']):
        # Extract task identifier
        task_identifier = extract_task_identifier(user_input_lower)

        return {
            'intent_type': 'COMPLETE_TASK',
            'confidence_score': 0.9,
            'extracted_parameters': {
                'task_identifier': task_identifier
            }
        }

    elif any(word in user_input_lower for word in ['update', 'change', 'modify', 'edit', 'rename', 'alter']):
        # Extract task identifier and new details
        task_identifier = extract_task_identifier(user_input_lower)

        return {
            'intent_type': 'UPDATE_TASK',
            'confidence_score': 0.9,
            'extracted_parameters': {
                'task_identifier': task_identifier,
                'updates': {}
            }
        }

    elif any(word in user_input_lower for word in ['delete', 'remove', 'cancel', 'get rid of', 'eliminate']):
        # Extract task identifier
        task_identifier = extract_task_identifier(user_input_lower)

        return {
            'intent_type': 'DELETE_TASK',
            'confidence_score': 0.9,
            'extracted_parameters': {
                'task_identifier': task_identifier
            }
        }

    else:
        return {
            'intent_type': 'UNKNOWN',
            'confidence_score': 0.1,
            'extracted_parameters': {}
        }


def extract_task_identifier(text: str) -> Optional[str]:
    """
    Extract task identifier from text.

    Args:
        text: Input text containing task reference

    Returns:
        Task identifier (could be title, ID, or other identifier)
    """
    # Look for common patterns indicating a specific task
    patterns = [
        r'(?:task|the)\s+(.+?)(?:\s+is|\s+as|\s+be|\s+done|\s+complete|\s+finished)',
        r'(?:the\s+)?(.+?)\s+(?:task)',
        r'"([^"]+)"',
        r"'([^']+)'",
        r'(\w+)\s+task',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return None


def is_ambiguous_request(text: str) -> bool:
    """
    Check if a request is ambiguous and needs clarification.

    Args:
        text: Input text to check for ambiguity

    Returns:
        Boolean indicating if the request is ambiguous
    """
    # Check for ambiguous terms that refer to tasks without specific identification
    ambiguous_terms = [
        r'\b(the|that|this)\s+(task|one)\b',
        r'\b(remove|delete|complete|finish|update)\s+(it|that|this)\b',
        r'\ball\s+of\s+them\b',
        r'\bthose\s+tasks\b',
        r'\bsome\s+task\b',
    ]

    for term_pattern in ambiguous_terms:
        if re.search(term_pattern, text.lower()):
            return True

    return False


def get_ambiguity_response(text: str) -> str:
    """
    Get an appropriate response for ambiguous requests.

    Args:
        text: Input text that was identified as ambiguous

    Returns:
        Appropriate response to request clarification
    """
    text_lower = text.lower()

    if any(word in text_lower for word in ['complete', 'finish', 'done', 'mark']):
        return "I'm not sure which task you want to complete. Could you please specify the task title?"
    elif any(word in text_lower for word in ['delete', 'remove', 'cancel']):
        return "I'm not sure which task you want to delete. Could you please specify the task title?"
    elif any(word in text_lower for word in ['update', 'change', 'modify']):
        return "I'm not sure which task you want to update. Could you please specify the task title?"
    else:
        return "I'm not sure which task you mean. Could you please specify the task title or give more details?"