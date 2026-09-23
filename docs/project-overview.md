# Rosenix Project Overview

Rosenix is designed as a modular agent platform for connecting models, tools, memory, automation, and application features behind one developer-friendly interface.

## Core direction

- Support local and cloud model providers through a common interface.
- Keep tool integrations isolated so MCP and other adapters can evolve independently.
- Separate agent orchestration from the user interface.
- Prefer small, testable modules over provider-specific logic spread across the codebase.
- Keep configuration explicit so developers can inspect which model and tools are active.

## Development priorities

1. Stable provider and tool interfaces.
2. Reliable agent execution and error handling.
3. Persistent memory and automation primitives.
4. Fast local development with clear defaults.
5. Documentation and examples that make new integrations predictable.

This document is a lightweight architectural reference for future contributors.