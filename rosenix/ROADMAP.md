# Roadmap

Rosenix is pre-alpha. This roadmap tracks what's needed before a `1.0`
release, roughly in priority order. Not a commitment to dates.

## Before `0.2.0`
- [ ] Bring `kits/` and `providers/` test coverage up (currently 0%)
- [ ] Add `runtime/test_executor.py` covering retries, cancellation, cycles
- [ ] Real structured tool-calling in `Agent` (replace the current
      placeholder `_extract_tool_call`)
- [ ] GitHub Actions CI (lint, type-check, test, coverage gate)
- [ ] `httpx`-based async `OllamaProvider` streaming (currently
      thread-offloaded, not true streaming)

## Before `1.0.0`
- [ ] Stable public API — explicit `__all__` audit, mark internal-only
      modules clearly
- [ ] Documentation site (architecture, provider authoring guide,
      plugin authoring guide)
- [ ] Benchmarks directory with tracked startup-time / memory numbers
- [ ] At least one additional built-in `VectorStore` and `Memory`
      implementation beyond the defaults
- [ ] Security review of the entry-points plugin loading mechanism

## Post-`1.0`
- [ ] Multi-agent orchestration kit built on `runtime.executor`
- [ ] First-party OpenTelemetry exporter integration example
- [ ] Community plugin directory / marketplace listing

Have an idea that's missing? Open an issue.
