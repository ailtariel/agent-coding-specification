---
name: vue
description: Implement Vue SFCs, reactivity, lifecycle, and composables using the personal Composition API and TypeScript conventions.
metadata:
  author: Anthony Fu
  version: "2026.1.31"
  source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills
---

# Vue

> Based on Vue 3.5. Always use Composition API with `<script setup lang="ts">`.

## Vue Ecosystem Index

- **Core Vue**: continue with this file and its `references/` directory for Composition API, SFC macros, reactivity, lifecycle, and built-in components.
- **Pinia**: read [pinia/SKILL.md](pinia/SKILL.md) for stores, getters, actions, plugins, SSR, testing, and store composition.
- **Vue Router**: read [vue-router/SKILL.md](vue-router/SKILL.md) for guards, params, navigation loops, same-route updates, and lifecycle interactions.
- **Vuetify**: read [vuetify/SKILL.md](vuetify/SKILL.md) when code imports `vuetify` or uses Vuetify components, layout, theming, or migration behavior.

## Personal Preferences

- Prefer TypeScript over JavaScript
- Prefer `<script setup lang="ts">` over `<script>`
- For performance, prefer `shallowRef` over `ref` if deep reactivity is not needed
- Always use Composition API over Options API
- Discourage Reactive Props Destructure; use `props.x` and `withDefaults` even on versions that support reactive destructuring.
- These are deliberate personal preferences for code written in this task; they do not authorize unrelated rewrites. Higher-priority project constraints and current user instructions still apply.

## Application And Component Ownership

Use clear ownership boundaries in routed Vue applications:

- **App root**: owns providers, global initialization, themes, locale setup,
  top-level overlays, and capabilities shared across all routes. It should not
  contain feature-page content or page-local workflows.
- **Route layout**: owns stable application chrome, shared shell components, and
  the child `RouterView`. It should not branch on route names to implement page
  business behavior.
- **Route page**: owns route-specific data orchestration, page composition,
  page-local state, actions, and the primary content or scroll region.
- **Feature component**: owns a focused business UI responsibility within one
  feature and may remain private to that feature.
- **Shared component**: owns a stable responsibility reused across features. It
  exposes variation through typed props, slots, models, and emits instead of
  reading route names or unrelated global state.

Do not create a wrapper component for one call site unless it materially
reduces complexity. Prefer slots and component attributes over wrapper nodes
whose only purpose is spacing or forwarding props.

If a project uses feature modules, colocate feature pages, private components,
types, stores, services, and composables. Move an artifact to a shared
directory only after it has real cross-feature consumers and no longer depends
on one feature's internal contract.

## State And Data Flow

- Treat Vue or store state as the reactive source of truth for UI rendering.
  Do not manually reload data merely to make Vue notice a state change.
- Use `computed` for derived state. Use `watch` or `watchEffect` for side
  effects, synchronization with external systems, or lifecycle-sensitive work,
  not as a replacement for computed values.
- Keep local UI state in the owning component. Use Pinia only for state shared
  across owners; use the project's query/data layer for server-state caching.
- Keep a form editing buffer distinct from authoritative persisted state when
  the workflow supports cancel, reset, dirty state, or deferred saving.
- A successful mutation should update or invalidate the authoritative reactive
  source and any directly related source through its owning store or data
  layer.
- Avoid destructuring reactive objects in ways that lose reactivity. Follow the
  target Vue version's supported props and reactivity patterns.

## Composable And Type Boundaries

- Use a composable to encapsulate reusable stateful Vue logic, not merely to
  move a few lines out of a component.
- Name composables with `use`, accept reactive inputs when callers need them,
  clean up effects and external resources, and return refs in a plain object so
  destructuring preserves reactivity.
- Module-level singleton state in a composable is global state. Use it only
  when shared lifetime is intentional and explicit; keep feature-scoped caches
  inside the feature boundary.
- Types used by one SFC may stay in that SFC. Shared types should move to the
  nearest feature-level or responsibility-specific type module rather than a
  catch-all global types file.

## Template And Formatting Guidance

- Keep templates readable and let the project's configured formatter determine
  wrapping, indentation, and attribute layout.
- Avoid dense one-line component trees. Use named slots and focused child
  components when they clarify stable responsibilities.
- When interpolation content spans multiple lines, place the opening tag,
  interpolation, and closing tag on separate lines. Avoid `>{{` or
  `}}</...>` at a multiline boundary.
- Keep Prettier's default `htmlWhitespaceSensitivity: "css"` unless the
  project has a deliberate alternative. Changing it to normalize one template
  can alter meaningful whitespace between inline elements.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Script Setup & Macros | `<script setup>`, defineProps, defineEmits, defineModel, defineExpose, defineOptions, defineSlots, generics | [script-setup-macros](references/script-setup-macros.md) |
| Reactivity & Lifecycle | ref, shallowRef, computed, watch, watchEffect, effectScope, lifecycle hooks, composables | [core-new-apis](references/core-new-apis.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Built-in Components & Directives | Transition, Teleport, Suspense, KeepAlive, v-memo, custom directives | [advanced-patterns](references/advanced-patterns.md) |

## Quick Reference

### Component Template

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps<{
  title: string
  count?: number
}>()

const emit = defineEmits<{
  update: [value: string]
}>()

const model = defineModel<string>()

const doubled = computed(() => (props.count ?? 0) * 2)

watch(() => props.title, (newVal) => {
  console.log('Title changed:', newVal)
})

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>{{ title }} - {{ doubled }}</div>
</template>
```

### Key Imports

```ts
// Reactivity
import { ref, shallowRef, computed, reactive, readonly, toRef, toRefs, toValue } from 'vue'

// Watchers
import { watch, watchEffect, watchPostEffect, onWatcherCleanup } from 'vue'

// Lifecycle
import { onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

// Utilities
import { nextTick, defineComponent, defineAsyncComponent } from 'vue'
```
