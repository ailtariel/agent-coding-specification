# Composing Stores

Use default imports for personal stores, with setup definitions as specified in [Vue](../../SKILL.md).

- Avoid mutually reading each other's state during store setup. Defer cross-store reads to computed getters or actions where necessary, rather than introducing a second copy of the data.
- In async actions used with SSR, obtain dependent store instances before the first await so they bind to the correct active Pinia context. Outside injection context, pass the intended Pinia instance explicitly.
- Each store remains responsible for its own data. Coordinate through its actions and the module service; do not swallow a service failure and then continue a dependent mutation.

Source: [composing stores](https://pinia.vuejs.org/cookbook/composing-stores.html).
