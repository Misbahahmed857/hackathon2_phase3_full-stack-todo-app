"""
MCP tools framework for task operations.

This module sets up the foundation for MCP tools that will be used by the AI agent
to perform task operations while maintaining statelessness and using only MCP tools
for data access, in compliance with constitutional requirements.
"""
from typing import Dict, Any, Callable
import json


class MCPTaskTools:
    """Container for MCP task tools."""

    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, func: Callable, schema: Dict[str, Any]):
        """
        Register an MCP tool with its function and schema.

        Args:
            name: Name of the tool
            func: Function that implements the tool
            schema: JSON schema defining the tool's input parameters
        """
        self.tools[name] = {
            'function': func,
            'schema': schema
        }

    def get_tool(self, name: str):
        """Get a registered tool by name."""
        return self.tools.get(name)

    def get_all_tools(self) -> Dict[str, Any]:
        """Get all registered tools."""
        return self.tools


# Global instance of MCP tools
mcp_tools_instance = MCPTaskTools()


def get_mcp_tools():
    """Get the global MCP tools instance."""
    return mcp_tools_instance