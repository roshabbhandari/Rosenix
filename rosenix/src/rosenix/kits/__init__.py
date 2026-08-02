"""Layer 4: Application Kits.

The only layer with opinions. Agent, Workflow, and the `@tool` decorator
are thin, composed entirely from Layers 1-3 — if this layer ever gets
fat, it's a signal the abstractions below it were wrong.
"""

from rosenix.kits.agent import Agent
from rosenix.kits.tool_decorator import tool
from rosenix.kits.workflow import Workflow

__all__ = ["Agent", "tool", "Workflow"]
