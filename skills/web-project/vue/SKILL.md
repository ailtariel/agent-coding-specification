---
name: vue
description: Apply personal Vue, Pinia, and Vuetify conventions to components, state, and views.
metadata:
  author: Personal revision; original Vue references by Anthony Fu
  source: Personal conventions, with references originally adapted from https://github.com/antfu/skills
  updated: "2026-09-25"
---

# Vue

Personal practices for Vue development. Apply them to the requested work; they do not authorize unrelated rewrites. Current user instructions and higher-priority project requirements take precedence. Confirm installed versions before using version-specific APIs.

## Code And Ownership

- Use Composition API, TypeScript, and `<script setup lang="ts">`. Keep props as `props.x`; use `withDefaults` instead of Reactive Props Destructure. Prefer `shallowRef` when deep reactivity is unnecessary.
- App owns providers and global initialization; layout owns shared application chrome and `RouterView`; page owns its data orchestration, actions, content, and primary scroll region. Shared components express variation through props, slots, models, and emits, not route-name branches.
- Keep feature-private files together. Extract for independent responsibility, actual reuse, or meaningful complexity reduction; do not add wrappers that only forward props or supply spacing.
- `service.ts` owns API calls through the existing HTTP client and preserves its result/error contract. Components, stores, and composables call the service; it does not own UI loading or dialogs. For result-based clients, callers check success without adding rejection wrappers or duplicate error feedback.
- `store.ts` default-exports one Pinia setup store exposing its related shared state and actions together. Keep store-specific processing inside the store, even when it is pure computation; helpers need not all be public. Return all Pinia-managed state. Logic reuse alone does not justify shared state.
- Shared module types belong in its `types.ts`; component-only props, emits, and local types stay in setup. Use `import type`. Promote files to shared scope only for real cross-feature use.

## Reactivity And State

- When A changes reactively as a derived value of B, use `computed`, never an extra writable ref synchronized by a watcher. Use explicit-source `watch` only for requirements that computed cannot express, such as asynchronous work or external side effects; complex calculations alone do not justify it.
- Do not use `watchEffect`, `watchPostEffect`, or `watchSyncEffect` in personal code. This preference does not prohibit third-party implementations from using them internally.
- VueUse supplies reactive data utilities. For reacting to API data becoming ready, prefer `whenever` for conditional callbacks and `until` for an awaited one-time condition over handwritten watcher/Promise wrappers. These handle effects and waiting; derived values still use computed. See [VueUse](vueuse/SKILL.md) for readiness, failure, and lifetime details.
- Keep local input, loading, and interaction state in setup. Share an operation's state only when multiple consumers must observe the same operation. Editing drafts are independent state with explicit initialization, submission, and discard; do not overwrite unsaved edits through unconditional synchronization.
- Read store state directly or through `storeToRefs`; actions may be destructured. Do not create detached copies with ordinary state destructuring or `ref(store.value)`, except intentional editing drafts.
- Mutations update or invalidate the authoritative source through its owner. Do not reload data merely to make Vue notice a change.

## Reusable Logic

- Reusable reactive logic outside the relevant store belongs in `use{ModuleName}.ts` with a same-named exported function. Merely being asynchronous or calling an API does not justify the `use` prefix. This naming convention does not rename third-party APIs.
- Each composable call owns its local state by default. Avoid implicit module-level singletons; intentional shared state needs an explicit owner and lifetime. Accept refs/getters when inputs must stay reactive, read them inside computed/watch, and return refs/computed in a plain object rather than `.value` snapshots.
- A composable owns cleanup of its timers, listeners, and subscriptions in the valid setup/effect scope where it is used. Do not add lifecycle wrappers to ordinary data functions.
- Non-reactive reusable functions unrelated to a store belong in module `utils.ts`, accept plain inputs, and do not use the `use` prefix. Simple single-component helpers stay in setup; store-owned computations stay in the store.

## Views And Styles

- Templates express declarative props, models, events, and slots. Simple display expressions may stay inline; business calculations and multi-step operations belong in setup or the data owner.
- When using Vuetify, first check whether component and view functionality can use existing project components or Vuetify components, props, slots, composables, and built-in classes before writing custom UI or CSS. Preserve defaults unless an actual requirement calls for customization.
- When custom CSS is needed and no Vuetify API/class fits, use inline `style` for simple one-off declarations and `:style` for dynamic values. Do not invent a class, file, or wrapper for one declaration or repeat the same inline group across consumers.
- `<style scoped>` holds repeated component-local classes or necessary, narrowly targeted `:deep()` overrides after checking public APIs/slots. Do not use unbounded `.v-*` overrides.
- Confirmed global semantic colors belong in theme; framework styling variables in the existing SASS entry; component prop defaults in `defaults`. Keep page exceptions local and do not create global configuration without a requirement.
- Follow the configured formatter. Keep multiline interpolation's opening tag, interpolation, and closing tag on separate lines; avoid `>{{` or `}}</...>` at multiline boundaries. Keep Prettier `htmlWhitespaceSensitivity: "css"` unless the project deliberately chooses otherwise.

## References On Demand

Read only what resolves the current question; do not load every reference or child skill.

- SFC macros and version boundaries: [script setup](references/script-setup-macros.md).
- Watch timing, asynchronous invalidation, and effect lifetime: [reactivity](references/core-new-apis.md).
- Built-in component caveats: [advanced patterns](references/advanced-patterns.md).
- Pinia-specific APIs: [Pinia](pinia/SKILL.md); route guards and component reuse: [Vue Router](vue-router/SKILL.md).
- Vuetify layout/configuration and version-specific APIs: [Vuetify](vuetify/SKILL.md).
- Reactive utilities and waiting for data: [VueUse](vueuse/SKILL.md).
