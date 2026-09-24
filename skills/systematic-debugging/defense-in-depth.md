# Validation At Real Boundaries

Validate untrusted input at its entry or trust boundary. Within the same trusted flow, reuse the established contract instead of duplicating identical checks at each function or layer.

A new check is justified when data crosses another trust boundary, when an operation has a distinct business invariant, or when the original guarantee no longer holds. For example, syntactic request validation does not establish authorization to modify the requested resource.

Trace the invalid value and identify which boundary owns the missing guarantee. Fix that owner and verify the affected contract. Add downstream checks only when they protect a different, concrete boundary; mocks or the possibility of future refactoring alone do not justify checks everywhere.

Use focused, temporary diagnostics when needed. Log presence, types, identifiers safe to disclose, or sanitized summaries. Never dump credentials or the entire environment. In shell, an explicit conditional can report SET/UNSET without interpolating the variable's value.

For filesystem containment, compare resolved path components against the allowed root, accounting for symlinks. A string prefix match is not a containment check.
