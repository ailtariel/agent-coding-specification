# Reactivity And Effect Boundaries

Apply the personal choices in [Vue](../SKILL.md). For condition callbacks and one-time waits, prefer [VueUse](../vueuse/SKILL.md).

- Use `computed` for derived values, including filtering, formatting, and selections. A getter must not perform requests or mutate its dependencies.
- `shallowRef` tracks replacement of `.value`, not mutations of raw nested objects. Choose it from the update model, not a blanket claim that `ref` is slow.
- Destructuring primitive properties of a reactive object disconnects those bindings. Use property access or `toRefs`; nested reactive proxies do not become raw merely because they were destructured.
- Watch a ref or getter, not its current value. For reactive composable inputs, read `toValue(input)` inside the watched getter or computed.
- Use `immediate` when initial execution is needed. DOM-dependent effects may require mounted timing or `flush: 'post'`; `flush: 'sync'` is unbatched and should match an actual timing need.
- An async watcher must invalidate obsolete work before it can commit results. Register cleanup before awaiting. Use the existing service's cancellation contract when supported; otherwise prevent obsolete results from updating state. Let the established error owner handle failures.
- `onWatcherCleanup` is Vue 3.5+ and must be called synchronously. The watch callback's `onCleanup` parameter can express cleanup on earlier supported versions.
- Create component-bound watchers synchronously in setup. Watchers created later need an explicit lifetime owner. Composables dispose timers, listeners, subscriptions, and owned effect scopes; browser globals are accessed only on the client.

Sources: [reactivity](https://vuejs.org/api/reactivity-core.html), [watch cleanup](https://vuejs.org/guide/essentials/watchers.html#side-effect-cleanup), [composables](https://vuejs.org/guide/reusability/composables.html), [SSR](https://vuejs.org/guide/scaling-up/ssr.html#access-to-platform-specific-apis).
