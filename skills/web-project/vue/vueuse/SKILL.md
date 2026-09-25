---
name: vueuse
description: Select VueUse utilities for reactive data, condition waits, and browser effects.
metadata:
  source: https://github.com/vueuse/vueuse
  updated: "2026-09-25"
---

# VueUse

Use [Vue personal conventions](../SKILL.md) when not already loaded. VueUse provides reactive utilities; prefer an existing matching utility over a custom implementation. Inspect installed Vue/VueUse versions and package exports before adopting an API. Adding this skill does not install packages in target projects; dependency changes follow their existing authorization.

For component/view functionality in a Vuetify project, check the project's components and Vuetify capabilities first. VueUse complements them for reactive data and browser effects. Derived values remain `computed`; VueUse does not justify watcher-maintained mirrors or new global state.

## Waiting For API Data

Prefer `whenever` / `until` over handwritten `watch` + Promise / conditional callback wrappers for waiting on reactive API readiness.

| Need | Preferred utility |
| --- | --- |
| Run a callback when a watched condition becomes truthy | `whenever(condition, callback)` |
| Also run if already ready at registration | `whenever(condition, callback, { immediate: true })` |
| Run only once when ready | `whenever(condition, callback, { immediate: true, once: true })`, when supported by the installed version |
| Await readiness once in an async flow | `await until(condition).toBeTruthy()` |

Pass a ref or getter, not a `.value` snapshot. `whenever` follows source changes; it is not polling. `until` checks immediately and stops its watcher when the condition matches.

Readiness must mean successful data for the intended request/entity. `!loading` alone also includes not-started and failed requests. For a wait that can fail, observe a terminal state and handle its failure before continuing; do not leave an async flow waiting only for success forever. If the current flow owns the request Promise, await it directly and apply its result contract instead of creating a second reactive wait.

Choose timeout/cancellation policy from the operation's lifetime. `until` timeouts resolve by default; use `throwOnTimeout: true` if timeout must prevent the next operation. Stopping a scope's watcher does not itself settle a pending Promise or cancel an already-running callback. Dispose owned watchers and suppress obsolete post-await work when the owner or request changes. Do not assume an `AbortSignal` option exists without checking the installed API.

These utilities preserve explicit sources and are compatible with the personal no-`watchEffect` convention; third-party internals are outside that convention.

## Other Utilities On Demand

Look up only the capability needed in the [function index](https://vueuse.org/functions.html): reactive storage, event listeners, element observers, debounce/throttle, and async state. Keep requests through the existing service/client and preserve error semantics; a fetch utility is not a reason to bypass that layer. Do not add a wrapper whose only purpose is renaming a VueUse function.

Sources: [repository](https://github.com/vueuse/vueuse), [whenever](https://vueuse.org/shared/whenever/), [until](https://vueuse.org/shared/until/), [guidelines](https://vueuse.org/guidelines.html). The upstream [function skill](https://github.com/vueuse/vueuse/tree/main/skills/vueuse-functions) is available for comparison; its broad trigger and exhaustive catalog are intentionally not copied here.
