---
name: systematic-debugging
description: Diagnose bugs, failed checks, or unexpected behavior using evidence before selecting a fix; scale investigation to uncertainty.
---

# Systematic Debugging

Identify a supported cause before choosing a repair. Investigation depth follows uncertainty and impact: an exact error and clear localized cause may be enough to proceed directly. Complex or intermittent faults need focused reproduction, hypothesis testing, or tracing. These are techniques, not mandatory sequential phases.

- Read the relevant error, surrounding implementation, and directly related changes. Reproduce when it adds evidence; state limits when reproduction is unavailable.
- Investigate the smallest boundary that can distinguish plausible causes. Add temporary instrumentation only when existing evidence is insufficient; avoid dumping environments, secrets, or full request payloads.
- Test a specific hypothesis with a discriminating observation or bounded change. Learn from failures rather than accumulating speculative patches.
- Fix the cause within the authorized scope. Reuse an existing regression or add the smallest meaningful test when the failure mechanism warrants it. A failing automated test is useful evidence, not a prerequisite for every typo, tool/configuration repair, or visual fix.
- Complete relevant checks and repair failures introduced by the fix. Do not repeatedly run passing checks or broaden verification without a concrete reason.

Repeated failures call for reassessing assumptions and gathering new evidence. Three attempts do not prove an architecture defect. Request a user decision only when investigation exposes a material unauthorized architecture/behavior choice or a blocker requiring user input; continue independent work.

For environment failures, fix authorized environment/configuration issues or report the precise blocker. Do not silently add retries, fallback behavior, or new infrastructure to hide the failure.

## Focused Techniques

- Deep call-stack failures: [root-cause-tracing.md](root-cause-tracing.md).
- Input or trust-boundary failures: [defense-in-depth.md](defense-in-depth.md).
- Timing-sensitive checks: [condition-based-waiting.md](condition-based-waiting.md).

Report the root cause and evidence, repair, impact, and actual verification. No companion skill or testing framework is required.
