# Contributing to Rosenix

Thanks for considering contributing. This project is pre-alpha — expect
rough edges, and expect this guide to change as tooling solidifies.

## Local setup

```bash
git clone https://github.com/rosenix-project/rosenix.git
cd rosenix
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,openai]"
```

## Running checks

```bash
pytest --cov=rosenix --cov-report=term-missing   # tests + coverage
mypy src/rosenix                                  # type checking
ruff check src/ tests/ examples/                  # lint
ruff check --fix src/ tests/ examples/             # auto-fix what's fixable
```

All four must pass before a PR is merged. CI runs these on every push.

## Known coverage gaps (good first contributions)

As of the last audit, these modules have little or no test coverage.
Picking one of these up is one of the most valuable things a new
contributor can do:

- `kits/agent.py` — the `Agent` run loop and tool-call handling
- `kits/workflow.py`, `kits/tool_decorator.py`
- `providers/openai_provider.py`, `providers/local_provider.py`
- `runtime/executor.py` — specifically retry-exhaustion and
  cancellation-propagation paths
- `runtime/tracing.py` — the OpenTelemetry integration branch
- `kernel/lifecycle.py` — the shutdown-error `ExceptionGroup` path
- `kernel/config.py` — file/env layering precedence

## Architecture ground rules

Before adding code, understand which of the four layers it belongs in
— see the README's architecture section. In short:

- **kernel/** — zero AI-specific code, ever. If you're tempted to import
  `protocols` or `kits` from here, the code belongs elsewhere.
- **protocols/** — contracts only (`typing.Protocol`), no implementations
  beyond the built-in `providers/` package.
- **runtime/** — execution primitives; still no AI-specific logic.
- **kits/** — the only layer allowed to have opinions. Keep it thin —
  if a kit class is getting large, the abstraction below it is probably
  wrong and should absorb the complexity instead.

## Commit / PR conventions

- One logical change per PR. Large refactors should be discussed in an
  issue first.
- Add or update tests for any behavior change.
- Update `CHANGELOG.md` under `[Unreleased]`.

## Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
