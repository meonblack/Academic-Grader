# Google Drive integration plan

## Proposed folder pattern
`Bootcamp Submissions / Cohort-04 / Productivity Engineer / Student-ID / Week-03 /`

Use internal student IDs in folder names where possible. Avoid unnecessary personal details in paths.

## Metadata to collect
`student_id`, `course_id`, `cohort_id`, `week`, `drive_folder_id`, `file_id`, `name`, `mime_type`, `modified_time`, `web_view_link`, `access_status`, `content_hash_if_available`, `retrieved_at`.

## Controls
- Use the minimal Drive scopes and authorized organization policy.
- Verify Google Docs/export support and file types before extraction.
- Capture a stable snapshot/version of evidence for reproducible regrading, consistent with retention policy.
- On inaccessible links, mark `needs_evidence` and contact instructor/operator rather than guessing.
- Exclude files unrelated to the assignment and do not index confidential third-party information.

## Future implementation
Configure Google OAuth credentials outside version control. Build a read-only Drive adapter that lists permitted files, exports supported Docs and records durable evidence references; test permission revocation and rate limiting.
