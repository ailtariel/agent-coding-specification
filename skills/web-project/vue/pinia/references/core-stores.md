# Pinia Store Boundaries

Follow [Vue](../../SKILL.md) for ownership and exports. A module's `store.ts` default-exports its setup store; consumers default-import it.

```ts
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function $reset() {
    count.value = 0
  }

  return { count, doubled, increment, $reset }
})

export default useCounterStore
```

- Return all Pinia-managed state so SSR, devtools, and plugins can track it. Internal helper functions need not be exposed. Do not return an injected router or app-level dependency as store-owned state.
- Setup stores define their own `$reset`; the built-in implementation belongs to option stores.
- Read state directly or use `storeToRefs`. Actions are bound and may be destructured. A getter returning a function does not cache every set of function arguments.
- Use `$patch` when a grouped mutation is useful. `$subscribe` observes state mutations; `$onAction` observes action completion/failure. A detached subscription needs explicit cleanup by its longer-lived owner.
- Async actions call the module service and preserve its failure contract. Only success permits dependent mutations; returning a caught Error as an ordinary result does not preserve a rejecting contract.

Sources: [core concepts](https://pinia.vuejs.org/core-concepts/), [state](https://pinia.vuejs.org/core-concepts/state.html), [getters](https://pinia.vuejs.org/core-concepts/getters.html), [actions](https://pinia.vuejs.org/core-concepts/actions.html).
