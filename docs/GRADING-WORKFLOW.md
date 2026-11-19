# Operational grading process

1. Student submits work through an appropriately permissioned Google Drive folder.
2. Operator records cohort, track, week, student ID, assignment spec version and submission timestamp.
3. Authorized reviewer/integration inventories folder files; confirms which were actually opened.
4. Grade engine selects the **instructor-approved** track/week rubric and evaluates each criterion with evidence references.
5. Validator recalculates totals, checks all required criteria and flags missing artifacts.
6. Instructor reviews the proposed grades and feedback. If rejected, send back for revision; if approved, record who approved and when.
7. Approved grade is synced to the correct GHL record; idempotency key prevents repeat notifications.
8. Only approved feedback is released to the student and progress record updated.
9. Instructor separately confirms course completion and certification eligibility according to written policy.

## State transitions
`received → evidence_collected → pending_instructor_review → approved → released`

Exceptional states: `needs_evidence`, `revision_requested`, `sync_failed`.

## Rollback and dispute handling
Keep immutable report versions, source citations and approval audit events. Corrections require a new version and renewed instructor approval. Never silently overwrite a prior released score.
