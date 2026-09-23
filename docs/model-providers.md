# Model Provider Integration Notes

Rosenix should treat model providers as interchangeable adapters rather than making the agent depend on one vendor.

## Adapter responsibilities

A provider adapter should own:

- Base URL and authentication configuration.
- Model selection.
- Request and response translation.
- Provider-specific error normalization.
- Optional capability metadata such as tool calling or vision support.

The agent layer should receive a consistent result shape and should not need provider-specific branching for ordinary requests.

## Configuration

Keep secrets outside source control. Provider settings should be configurable through environment variables or the application's settings layer.

## Fallbacks

When multiple providers are configured, fallback behavior should be explicit and observable. Log the provider transition and the reason for a fallback without exposing API keys.

New providers should include at least one focused integration test and a short example in the documentation.