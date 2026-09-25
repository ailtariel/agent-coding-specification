# Built-in Component Boundaries

Consult the relevant official page when using one of these features; they are not a default implementation checklist.

- [KeepAlive](https://vuejs.org/guide/built-ins/keep-alive.html): cached components deactivate without unmounting. Pause work in `onDeactivated` when it should not continue offscreen; include/exclude match component names.
- [Teleport](https://vuejs.org/guide/built-ins/teleport.html): the target must exist. Vue 3.5+ `defer` delays target resolution within the same mount/update tick, not until arbitrary future asynchronous work completes.
- [Suspense](https://vuejs.org/guide/built-ins/suspense.html): experimental; coordinates async setup and suspensible async components, not every request made after mounting. It does not supply an error boundary by itself.
- [Transition](https://vuejs.org/guide/built-ins/transition.html) / [TransitionGroup](https://vuejs.org/guide/built-ins/transition-group.html): use stable keys for identity; JavaScript transitions must complete their `done` callback.
- [v-memo](https://vuejs.org/api/built-in-directives.html#v-memo): use only for a demonstrated update bottleneck and include every dependency needed to keep rendered output current. An incomplete dependency list can freeze stale UI.
- [Directives](https://vuejs.org/guide/reusability/custom-directives.html): use for reusable low-level DOM behavior when an existing component or utility does not own it; release resources on unmount.
