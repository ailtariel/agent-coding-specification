---
name: pinia
description: Implement or debug Pinia stores, actions, subscriptions, and store lifecycle.
metadata:
  author: Anthony Fu
  source: References originally adapted from https://github.com/antfu/skills
  updated: "2026-09-25"
---

# Pinia

Apply [Vue personal conventions](../SKILL.md) when not already loaded; they define setup-store default exports, store-owned processing, state consumption, and composable boundaries. Do not load every reference for an ordinary store change.

## References On Demand

- State exposure, reset, subscriptions: [stores](references/core-stores.md).
- Cross-store dependencies and async SSR context: [composition](references/features-composing-stores.md).
- VueUse/composable integration and hydration: [composables](references/features-composables.md).
- Plugin augmentation: [plugins](references/features-plugins.md).
- Store instance selection outside components: [outside components](references/best-practices-outside-component.md).
- SSR serialization: [SSR](references/advanced-ssr.md); Nuxt integration: [Nuxt](references/advanced-nuxt.md).
- Store behavior tests or action stubs: [testing](references/best-practices-testing.md).
- HMR configuration: [HMR](references/advanced-hmr.md).

Upstream references may describe Options API compatibility; personal new stores use setup syntax. Read installed-version documentation when API behavior is uncertain.
