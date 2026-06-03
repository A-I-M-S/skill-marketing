# Week 1 Sprint — Foundation & Lead Capture

## Day 1-2: Build the AI Audit / Assessment Generator

- [ ] Set up the assessment form using Google Forms, Typeform (free tier), or embed directly on your site
- [ ] Use `templates/lead-assessment/form-template.md` as the question set
- [ ] Create the landing page using `templates/lead-assessment/landing-page-sections.md`
- [ ] Connect form responses to Google Sheets
- [ ] Set up email notification (Gmail filter or Brevo) when a new lead submits

## Day 3: Lead Capture + Notifications

- [ ] Configure Google Sheets to capture all form submissions automatically
- [ ] Set up Brevo (free tier, 300 emails/day) for confirmation email
- [ ] Use `templates/nurture/email-1-welcome.md` as the auto-reply template
- [ ] Test the full flow: submit form → receive email → data in Sheets → notification
- [ ] Add Calendly booking link to the confirmation email

## Day 4: Build the Outreach Helper

- [ ] Prepare your first prospect list (CSV format: first_name, last_name, title, company, industry, email, linkedin_url, notes)
- [ ] Run `tools/generate-outreach prospects.csv -o output/outreach-wave1`
- [ ] Review all generated emails — personalise further before sending
- [ ] Create a tracking sheet for outreach responses (Sheets)

## Day 5: Create 10 LinkedIn Posts

- [ ] Use `tools/generate-content templates/linkedin/monday-insight.md -o output/posts/monday-1.md`
- [ ] Use `tools/generate-content templates/linkedin/wednesday-tip.md -o output/posts/wednesday-1.md`
- [ ] Use `tools/generate-content templates/linkedin/friday-case-study.md -o output/posts/friday-1.md`
- [ ] Create 7 reserve posts for the following week
- [ ] Schedule posts in LinkedIn scheduler or Buffer (free tier)
- [ ] Prepare 10 engagement comments for your target audience's posts

## Day 6: Contact 50 Prospects

- [ ] Send 10-15 personalised cold emails from your wave 1 list
- [ ] Send 20 LinkedIn connection requests with personalised note
- [ ] Engage with 15 target prospects' LinkedIn posts (meaningful comments)
- [ ] Log all outreach in your tracking sheet
- [ ] Set reminders for follow-ups (Day 4, Day 8)

## Day 7: Review & Iterate

- [ ] Review week 1 metrics:
  - [ ] Assessment submissions received: ____
  - [ ] LinkedIn post impressions: ____
  - [ ] Cold email open rate: ____
  - [ ] Connection requests accepted: ____
- [ ] Refine messaging based on what resonated
- [ ] Plan week 2 priorities
- [ ] Update `config/persona-cto.md` with any new insights
