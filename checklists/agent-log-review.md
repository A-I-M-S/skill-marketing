# Agent Log Review Checklist

Use this when asking OpenCode, OpenClaw, or another agent to review whether the marketing automation is running correctly.

## Files to Read

- `output/status/latest-status.md`
- `logs/marketing-combined.log`
- `logs/pm2-out.log` if PM2 process output needs inspection
- `logs/pm2-error.log` if PM2 errors are reported
- Recent generated drafts under `output/posts/`, `output/seo/`, `output/outreach/`, and `output/reviews/`
- `output/som-tracker.md`

## Process Health

- [ ] Confirm the daemon has recent `DAEMON_CYCLE_START` and `DAEMON_CYCLE_END` entries.
- [ ] Confirm there are no recent `TASK_FAILED`, `DAEMON_CYCLE_ERROR`, or repeated `ERROR` entries.
- [ ] If status is `configuration required`, identify the missing `.env` variables before reviewing marketing output.
- [ ] Confirm skipped tasks have expected reasons, such as `already_ran_today` or `outreach_drafts reason=disabled`.
- [ ] Confirm `output/status/latest-status.md` has a recent timestamp.

## Marketing Output Review

- [ ] Check whether LinkedIn drafts were generated on the correct cadence: Monday, Wednesday, Friday.
- [ ] Review draft quality, specificity to Singapore SMEs, and relevance to Agentic AI transformation.
- [ ] Check whether SEO drafts include answer-first structure, data, grant context, and clear calls to action.
- [ ] If outreach is enabled, verify generated emails are drafts only and still require human review before sending.
- [ ] Check the SoM tracker and identify which manual AI-engine results are missing.

## Results Review

- [ ] Compare generated output against real marketing metrics if available: impressions, replies, booked calls, signups, citations.
- [ ] Identify which channel has the strongest evidence of progress.
- [ ] Identify missing data that prevents a proper performance review.
- [ ] Recommend the next 1-3 actions based on the 90-day roadmap.

## Review Response Format

1. Process status: running correctly / degraded / failed.
2. Recent tasks: list completed, skipped, and failed tasks.
3. Marketing outputs: list drafts generated and whether they are usable.
4. Results: summarize available metrics and missing metrics.
5. Next actions: recommend the highest-leverage fixes or marketing actions.
