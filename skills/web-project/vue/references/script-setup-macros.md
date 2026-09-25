# Script Setup Boundaries

Use the personal conventions in [Vue](../SKILL.md); check the installed Vue version before selecting a macro.

- Keep the props object and use `withDefaults` for defaults. Mutable array/object defaults need factories. Pass `() => props.value` to APIs expecting a reactive source, not `props.value`.
- Use typed `defineProps` and `defineEmits`; component-only types stay in setup. Named-tuple emits syntax, `defineOptions`, `defineSlots`, and SFC generics require Vue 3.3+.
- `defineModel` requires Vue 3.4+. A child model default can diverge from an undefined parent value; establish initialization ownership instead of relying on a child-only default.
- `defineExpose` defines the deliberate imperative surface of a child and must run before an await. Prefer declarative props/models/events for data flow.
- Vue 3.5+ supports `useTemplateRef`; refs can still be null before mounting or after conditional removal.
- Top-level await makes setup async and requires a suitable Suspense boundary. Do not add async setup just to wait for an ordinary user action.

Sources: [script setup](https://vuejs.org/api/sfc-script-setup.html), [component models](https://vuejs.org/guide/components/v-model.html), [template refs](https://vuejs.org/guide/essentials/template-refs.html).
