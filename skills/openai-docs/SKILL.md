---
name: openai-docs
description: Look up official OpenAI product, API, model, and Codex guidance; inspect local configuration for installation and troubleshooting tasks.
metadata:
  short-description: Official OpenAI documentation and local Codex configuration diagnosis
---

# OpenAI Docs

For local installation, configuration, skill discovery, or troubleshooting, inspect the actual installed version, relevant files, and command help first. Public documentation does not prove account access or effective local configuration.

For current product, model, API, pricing, or migration facts, use official documentation tools or targeted search of official OpenAI sites. Fetch the relevant source, match it to the requested product/version, and cite it. Do not store a latest-model fallback, API schema, pricing table, or product manual in this skill. If current evidence is unavailable, identify the unresolved fact rather than substituting an old bundled answer.

For a migration, preserve an explicit target and each workload's cost, latency, quality, endpoint, tools, and output-contract role. Resolve an unspecified target from current official guidance. Update active configuration and directly affected code; historical examples and intentionally pinned fallbacks are not migration targets by default.

Use current tool or client documentation for MCP integration when setup is requested. A documentation question does not require installing an integration or obtaining an API key. Live API execution needs credentials appropriate to the environment; do not infer them from a ChatGPT subscription or connector session.

Official sources: [developer documentation](https://developers.openai.com/), [API documentation](https://platform.openai.com/docs/), [ChatGPT guidance](https://learn.chatgpt.com/), and [OpenAI repositories](https://github.com/openai). Follow the source relevant to the question rather than a fixed manual/resolver sequence.
