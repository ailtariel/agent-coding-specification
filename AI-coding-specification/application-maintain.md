# Application Maintenance

## Variable Management

Before adding, reading, moving, or removing any configuration value, first
classify it as either a bootstrap environment variable or a managed runtime
setting.

The classification decision comes before choosing files, APIs, migrations, or UI
changes. Do not start from "which `.env` file should this go into?" or "which
Settings tab should this go into?" Start from what the value is used for and
when it must be available.

Use this decision rule:

1. If the value is required before the backend can connect to the database or
   read `system_settings`, keep it as a bootstrap environment variable.
2. If the value identifies the deployment/process, controls local dev tooling,
   or must be injected by the runtime platform before application startup, keep
   it as a bootstrap environment variable.
3. If the value controls application feature behavior after startup, can be
   shown or edited in Admin Settings, or should be returned to the browser by
   `/config/web`, make it a managed runtime setting.
4. If the value is sensitive, still classify it by lifecycle first. Sensitive
   runtime-managed values belong in the settings registry with backend masking,
   not in frontend env files or catalog metadata.
5. If uncertain, default to a managed runtime setting unless the value is needed
   before DB access is possible.

### Bootstrap Environment Variables

Environment variables are only for values that must be available before the
database and `system_settings` can be read, or for deployment/process identity.
Valid examples include:

- `ENV` selection, dotenv loading, server process settings, and local dev-server
  wiring.
- Database connection and schema settings.
- Deployment-injected identity or process-level values needed during startup.
- Values intentionally passed through to child process environments.

Runtime feature modules must not call `os.getenv`, `os.environ.get`,
`process.env`, or `import.meta.env` directly for feature behavior. If a value
can reasonably be edited in Admin Settings, or if it should be visible through
the Settings page, it must be represented as a managed runtime setting instead.

Bootstrap environment variables must be documented in the deployment or local
development template that actually supplies them. Do not add managed runtime
settings to `.env`, Helm values, Docker compose, or generated frontend env
config just to make them configurable; put them in the settings registry
instead.

Common bootstrap config locations include:

- Local development examples in `README.md` or checked-in `.env*` templates when
  such templates exist.
- Frontend build/dev bootstrap files only for build-time or dev-server concerns.
- Backend bootstrap settings in `backend/src/shared/settings.py`.
- Deployment templates such as Helm values and Docker compose files when the
  variable is required by that deployment path.

Bootstrap sync rules:

1. Optional variables:
   - Value can be empty.
   - Key must exist.
2. Required variables:
   - Must be added to every applicable checked-in local/deployment template that
     exists for the affected runtime path.
   - Add comments in the corresponding files or documentation.

Value conventions:

1. Production deployment templates should avoid committing real secret values.
2. Development templates may include safe local defaults.
3. If no safe default is available, keep the value empty and document what must
   be supplied.

### Managed Runtime Settings

Managed runtime settings are DB-backed values defined by the backend settings
registry and optionally shown in the Admin Settings UI. The `system_settings`
table stores only user-changed overrides. Defaults belong in code, not in eager
seed rows. Resetting a setting should delete the DB override and reveal the
registry default again.

Feature modules must read managed values through the shared registry accessors,
for example `get_setting_value(...)` or `get_setting_values(...)` from
`backend/src/module/system_setting/runtime_settings.py`. Do not read
`system_settings` directly for feature configuration unless implementing the
registry itself.

Sensitive managed values must be marked sensitive in the backend registry and
must not be exposed through admin responses, `/config/web`, logs, placeholders,
or frontend-only metadata.

`restart_required` is a user-facing hint, not a write constraint. Set it to
`true` only when the new value cannot take effect until process restart. If the
system can apply or reinitialize the value live, use `restart_required=false`
and wire the appropriate runtime reinitialization behavior.

### Registry and Catalog Locations

Backend authoritative registry:

- File: `backend/src/module/system_setting/runtime_settings.py`
- Main definitions: `SettingSpec`, `_spec(...)`, `UNIFIED_SETTINGS`
- Public read/apply helpers: `get_setting_value(...)`,
  `get_setting_values(...)`, admin settings payload builders, `/config/web`
  payload builder, and runtime reinitialization dispatch.

The backend registry owns backend-relevant facts only:

- stable domain key such as `logging.log_level`
- storage category/key used in `system_settings`
- default source, either a constant, `Settings` attribute, or resolver
- value type, editability, sensitivity, validation, allowed values
- restart and runtime reinitialization behavior
- whether the value is exposed to admin settings and whether it is client-visible

Frontend Settings catalog:

- File: `web/src/settings/settingsCatalog.ts`
- Purpose: Settings page grouping, labels, descriptions, placeholders, controls,
  and frontend-only validation hints.

The frontend catalog is not authoritative for security, validation, persistence,
or client exposure. It must not introduce a setting key that is missing from the
backend registry. It must not duplicate backend sensitivity decisions or backend
validation as the only enforcement.

Admin Settings API:

- `GET /api/v1/admin/settings`
- `PUT /api/v1/admin/settings/{domain_key}`
- `DELETE /api/v1/admin/settings/{domain_key}`

Client runtime config API:

- `GET /config/web`
- Returned keys come only from backend registry entries marked `client=true`.
- Client-visible settings must not include credentials, tokens, private paths,
  private connection strings, or server-only values.

### Adding or Maintaining a Variable

Use this checklist for every new or changed variable:

1. Classify the value with the decision rule above. Record the reason in the
   implementation notes when the choice is not obvious.
2. For bootstrap environment variables, add the field to
   `backend/src/shared/settings.py` or the relevant frontend/build bootstrap
   path, then update only the applicable checked-in local/deployment templates
   and docs according to the rules above.
3. For managed runtime settings, add a `SettingSpec` entry in
   `backend/src/module/system_setting/runtime_settings.py` with the correct
   domain key, storage category/key, value type, default source, editability,
   sensitivity, restart behavior, runtime reinitialization behavior, and
   `client` exposure.
4. Add backend validation or `allowed_values` in the registry when valid values
   are constrained. If values are discovered dynamically, the backend should
   expose `allowed_values` so the frontend does not hard-code stale options.
5. Update feature code to read through registry helpers. Remove direct
   environment reads and direct `system_settings` queries for that value.
6. If the setting should appear on the Admin Settings page, add or update the
   matching item in `web/src/settings/settingsCatalog.ts` after the backend
   registry key exists.
7. If the browser needs the value at runtime, mark the backend spec
   `client=true` and verify `/config/web` returns only the public key/value
   shape expected by the frontend. Do not expose a value to the browser just
   because it appears in the Admin Settings page.
8. If renaming or migrating legacy rows, add a database migration under
   `backend/src/shared/db/migration/`. Migrations may rename or delete legacy
   overrides, but should not seed default rows for managed settings.
9. Add or update targeted tests when behavior, API shape, masking, validation,
   runtime reinitialization, migration behavior, or frontend rendering changes.

### Settings UI Text Rules

Use these wording rules when maintaining `settingsCatalog.ts`:

- `placeholder` should answer "what should I enter here?" Include the expected
  format and a sample when useful.
- `description` should explain the runtime effect, when the change takes
  effect, and any notable side effect.
- Select controls generally do not need placeholders.
- Do not put secrets, real credentials, internal-only paths, or hidden policy
  details in labels, descriptions, or placeholders.
- Keep labels concise and stable. Changing a label should not change the backend
  key or storage key.

## Unit Testing

- Python test tool priority:
  1. `.venv` `pytest`
  2. Workspace default `pytest`
  3. Global `pytest`
