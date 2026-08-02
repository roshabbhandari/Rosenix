"""Layer 1: Kernel.

Generic application foundation with zero AI-specific code: dependency
injection, plugin registry, lifecycle management, and layered config.
Everything above this layer is built on top of these four primitives.
"""

from rosenix.kernel.config import Config
from rosenix.kernel.container import Container
from rosenix.kernel.lifecycle import Lifecycle
from rosenix.kernel.registry import Registry

__all__ = ["Container", "Registry", "Lifecycle", "Config"]
