# Vuetify Integration Details

Shared personal practices, including inline/scoped/global style placement, are defined in [Vue](../../SKILL.md). These details supplement them only when the corresponding capability is needed.

## Application Layout

In the personal app -> layout -> page structure, app owns `VApp`; layout owns `VLayout`, registered shell regions, and `RouterView`; each routed page owns its `VMain` and primary content/scroll region. This is a personal ownership convention, not a framework requirement. Preserve an explicitly established alternative project architecture.

Use `VMain` for content affected by registered application-layout offsets rather than imitating offsets with margins or fixed positioning. Use a distinct layout for a distinct shell. `VContainer` supplies standard width/gutters when needed; full-width content may use an appropriate child directly within `VMain`. Use `VRow`/`VCol` for responsive page grids and utilities for small local groups.

Prefer layout props such as `order`, `location`, and `permanent` over manual positioning. Registration/template order affects layout priority; `order` can make it explicit.

Sources: [application layout](docs/src/pages/en/features/application-layout.md), [grid](docs/src/pages/en/components/grids.md).

## Components And Interaction

Use `VToolbar` for a title/action region, `VCard` for grouped content, `VSheet` for lightweight surfaces, and `VCardActions` for card actions. Keep spacing on the owning component. Native elements remain appropriate for document content, browser measurement, native workflows, and fragments without a Vuetify-owned structure.

Bind overlay activator-slot `props` to the trigger so focus, keyboard, and ARIA behavior survive customization. Use Vuetify form/input states and validation instead of reimplementing them on generic containers. Consult the [component index](docs/_INDEX.md) for the installed version's contract.

## Theme, Defaults, And SASS

- Global Defaults configure public props. A local `VDefaultsProvider` or contextual nested defaults can express region-specific behavior without changing the entire app. Default prop names use camelCase.
- `class` and `style` belong under specific component keys, not the `global` defaults key. Some controls forward them to internal elements; inspect the actual target when it matters.
- Use existing theme colors for visual semantics. Do not introduce SASS compilation just to apply a local style; check that the project has configured the pipeline before changing SASS variables.
- SASS settings files contain variables, mixins, and functions, not emitted CSS or regular stylesheet imports. Do not `@use 'vuetify/styles'` in settings; use `vuetify/settings` as documented.

Sources: [theme](docs/src/pages/en/features/theme.md), [defaults](docs/src/pages/en/features/global-configuration.md), [SASS](docs/src/pages/en/features/sass-variables.md).

## Specific API Questions

- Cross-platform shortcuts: [`useHotkey` and `cmd`](docs/src/pages/en/features/hotkey.md).
- Date adapter parsing/serialization: [`useDate`, `parseISO`, `toISO`](docs/src/pages/en/components/date-inputs.md); confirm the configured adapter's date type.
- Precision-sensitive numeric input: [number inputs](docs/src/pages/en/components/number-inputs.md); a UI number control does not establish an exact-decimal arithmetic contract.
- Existing Tailwind/Vuetify CSS layer conflicts: [layer-order discussion](discussions/discussion-21241.md). This does not authorize adding another styling system.
- Version-specific components, props, slots, and fixes: [release API index](releases/v4.0.1-to-v4.1.0-api-index.md).
