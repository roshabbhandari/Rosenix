# Security Policy

## Supported Versions

Rosenix is currently pre-alpha (`0.x`). Until a `1.0` release, only the
latest published version receives security fixes.

| Version | Supported |
| ------- | --------- |
| 0.x     | ✅        |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security
vulnerabilities. Instead, report privately via GitHub's
["Report a vulnerability"](https://github.com/rosenix-project/rosenix/security/advisories/new)
feature, or email the maintainers (see repository contact info).

Include:
- A description of the vulnerability and its potential impact
- Steps to reproduce, or a minimal proof-of-concept
- Any known mitigations

We aim to acknowledge reports within 5 business days.

## Scope Notes

Rosenix wraps LLM provider APIs (OpenAI, Ollama) but does not itself
store or transmit credentials beyond passing them to the underlying
provider SDK/HTTP call. If you find an issue in how API keys are
handled, or in the plugin/entry-points loading mechanism (arbitrary
code execution risk from untrusted installed packages), that is
in scope and should be reported as above rather than filed publicly.
