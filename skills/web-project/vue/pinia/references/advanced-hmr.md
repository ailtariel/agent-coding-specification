# Store HMR

When the project uses store HMR, keep the setup store's default export and register the existing bundler's HMR hook after its definition:

```ts
import { acceptHMRUpdate, defineStore } from 'pinia'
import { ref } from 'vue'

const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  return { count }
})

export default useCounterStore

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCounterStore, import.meta.hot))
}
```

This example uses Vite's `import.meta.hot`; check the target bundler's interface. HMR is a development integration, not a reason to refactor unrelated stores.

Source: [Pinia HMR](https://pinia.vuejs.org/cookbook/hot-module-replacement.html).
