# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial four-layer architecture: kernel (DI, plugin registry, lifecycle,
  config), protocols (LLM/embedding/vector-store/tool/memory), runtime
  (event bus, task executor, tracing), kits (Agent, Workflow, `@tool`).
- Built-in providers: `OpenAIProvider`, `EchoProvider`, `OllamaProvider`.
- `py.typed` marker for downstream type-checking support.

### Fixed
- `Config` is now correctly `Generic[ConfigT]`, so `build()` returns the
  actual schema type instead of an unbound `TypeVar` (mypy-clean).
- `OllamaProvider` no longer blocks the event loop during HTTP calls
  (offloaded via `asyncio.to_thread`).
- `Container.register`/`register_instance` and `Executor.add` now return
  `Self` instead of a string-quoted class name, so subclassing works
  correctly with method chaining.

### Known limitations
- `Agent._extract_tool_call` is a placeholder; real structured tool-call
  parsing from provider responses is not yet implemented.
- Test coverage on `kits/` and `providers/` is incomplete — see the
  project audit notes in `CONTRIBUTING.md` before relying on these in
  production.

## [0.1.0] - Unreleased
- First tagged pre-release, not yet published to PyPI.
