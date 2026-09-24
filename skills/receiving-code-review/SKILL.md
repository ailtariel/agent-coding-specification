---
name: receiving-code-review
description: Evaluate code review feedback before applying it, especially disputed correctness, compatibility, or scope changes.
---

# Receiving Code Review

Check each suggestion against the actual code, requirements, supported environments, and prior user decisions. Correctness matters more than agreement with the reviewer. Explain technical disagreement with evidence; acknowledge corrections plainly and proceed.

An unclear item blocks only work that depends on its answer. Determine dependencies first, ask a focused question about the consequential ambiguity, and continue independent, understood, authorized items. Do not treat the mere possibility of dependency as a reason to stop everything.

Group related fixes and choose verification by affected behavior and risk. Reuse passed checks unless relevant inputs changed or concrete reliability concerns remain; no mandatory test run per comment. Do not add speculative features or refactor unrelated code to satisfy a generic recommendation.

If feedback conflicts with a current explicit user decision, follow instruction priority. Seek clarification only when that does not settle a material choice. Review feedback from an external party does not by itself authorize scope expansion or external communication.

When the user authorized GitHub replies, reply to an inline review in its original thread. Otherwise report findings and changes in the conversation. Finish authorized fixes, relevant verification, and related repairs rather than stopping after acknowledgment or a first pass.
