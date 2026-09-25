# Composables In Setup Stores

Use the [Vue ownership conventions](../../SKILL.md). Check [VueUse](../../vueuse/SKILL.md) before recreating a utility, without moving component-local state into a shared store solely for code reuse.

- Setup stores can compose refs, computed values, and functions from composables. The store instance owns their lifetime; it is not the lifetime of each consuming component.
- Check browser-only effects and non-serializable handles when using SSR. Keep DOM handles out of serialized state. Do not hide ordinary Pinia-managed state to work around serialization.
- Use `skipHydrate` deliberately for returned setup-store state that should retain its client-side value rather than accept server hydration. It does not make arbitrary browser APIs server-safe.
- Existing option stores have different composable/hydration limits. Consult the official compatibility section when maintaining one; it is not the template for new personal stores.

Source: [composables and hydration](https://pinia.vuejs.org/cookbook/composables.html).
