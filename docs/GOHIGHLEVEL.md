# GoHighLevel (GHL) integration plan

**This file is a proposed mapping, not a claim that the fields or API operations already exist in your GHL account.** Confirm exact GHL APIs, custom object support, IDs, and field names before implementing.

## Recommended student identity
Store a stable `student_id` in your system and map it to one unique `ghl_contact_id`. Never rely on name alone; email/phone may change.

## Suggested GHL custom object: Academic Grade
| Proposed field | Meaning |
| --- | --- |
| `grade_record_id` | Internal stable grade ID |
| `student_id` | Stable student reference |
| `ghl_contact_id` | GHL contact match |
| `track` / `cohort` / `week` | Course context |
| `assignment_id` / `rubric_version` | Reproducibility |
| `score_earned` / `score_possible` / `percentage` | Validated outcome |
| `status` | pending/approved/released/etc. |
| `reviewer_id` / `approved_at` | Human authorization |
| `feedback_link` | Authorized report link (not public) |
| `released_at` | Date of student notification |
| `idempotency_key` | Deduplicate sync/events |

If GHL custom objects are unsuitable, create a documented equivalent in your own app/database and sync only summary custom fields to contacts.

## Suggested GHL workflow events
- `assignment_received`: internal receipt (not a grading decision).
- `grade_approved`: update record and enqueue student feedback.
- `grade_released`: update latest grade/progress summary.
- `needs_evidence`: internal request for missing access.

## Safety requirements
Only emit `grade_approved` after authorized instructor approval; only notify for `approved` records. Validate contact match, deduplicate by `(student_id, cohort, track, week, assignment_id, report_version)`, rate-limit retries, log errors and prevent cross-student notifications.

## Credentials
Store GHL tokens/keys in deployment secrets, **never** in GitHub or `.env` commits. Verify permissions and consent to student messages.
