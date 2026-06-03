---
name: skill-marketing
description: 3-layer organic growth engine for aims-sg.com (Agentic Business Transformation consultancy targeting Singapore SMEs/enterprises). Builds lead-capture funnels, visibility channels, and AI-discoverability (AEO/GEO) with $0 ad spend.
mode: auto
---

# skill-marketing

A **3-layer organic growth engine** for aims-sg.com (Agentic Business Transformation targeting Singapore SMEs and enterprises). Builds and runs the full marketing stack from the plan in `marketing.md` with $0 ad spend.

## Layers

| Layer | Goal | Tools |
|-------|------|-------|
| **Layer 1 — Convert** | Lead capture + nurture | Assessment generator, chatbot, 4-email sequence |
| **Layer 2 — Visibility** | LinkedIn, cold email, SEO, directories, PR, communities | Content generator, outreach tool, checklists |
| **Layer 3 — Discoverability** | Get cited by AI engines | Technical SEO tools, SoM tracker, answer-first templates |

## Quick Start

```bash
# 1. Copy and configure
cp .env.sample .env
# Fill in AI_ENDPOINT, AI_API_KEY, AI_MODEL (optional — templates work offline)

# 2. Load the skill in opencode
# Add to opencode.json:
# {
#   "skills": ["file:///path/to/skill-marketing/skill.md"]
# }
```

## How the Agent Should Use This Skill

### 1. Understand Context
- Read `marketing.md` for the full strategy
- Check `config/` for keywords, personas, and grant reference material
- Know the user's track is **Track B — AI Transformation** (Singapore SME/enterprise)

### 2. Execute the Roadmap
Follow the 90-day arc from `checklists/90-day-roadmap.md`:

**Month 1 — Foundation:**
1. Run `tools/generate-content templates/lead-assessment/landing-page-sections.md -o output/landing-page.md`
2. Run `tools/generate-content templates/lead-assessment/form-template.md -o output/assessment-form.md`
3. Generate nurture emails: run once per template in `templates/nurture/`
4. Run `tools/setup-technical-seo -o output/technical-seo`
5. Run `tools/track-som` for baseline

**Month 2 — Acceleration:**
1. Generate first month of LinkedIn posts from `templates/linkedin/`
2. Prepare prospect CSV → `tools/generate-outreach prospects.csv`
3. Walk user through directory listings (`checklists/directory-listings.md` + templates)
4. Create SEO blog posts from `templates/seo/long-tail-post.md`

**Month 3 — Maturation:**
1. Rewrite top pages with answer-first blocks (`templates/seo/answer-block.md`)
2. Deploy schema JSON-LD (`templates/schema/`)
3. Track SoM weekly, report trends
4. Review monthly with `checklists/monthly-review.md`

### 3. Content Generation Flow
- **Without AI:** Templates render directly with `{{VARS}}` from `.env` — useful standalone
- **With AI:** Add `-a` flag to `tools/generate-content` to enhance via your endpoint
- **Custom prompts:** Use `-p "make this more specific to retail SMEs"`

### 4. Available Tools

| Tool | What it does |
|------|-------------|
| `tools/generate-content` | Fill templates + optional AI enhancement |
| `tools/generate-outreach` | Batch-generate personalised cold emails from CSV |
| `tools/setup-technical-seo` | Generate robots.txt, llms.txt, schema stubs |
| `tools/track-som` | Create Share of Model tracking sheet |

### 5. Reference Files

- `marketing.md` — Full strategy document (authoritative reference)
- `config/keywords-track-b.md` — SEO keywords Track B
- `config/persona-cto.md` — Buyer persona
- `config/grants-reference.md` — Singapore grants for content hooks
- `.env.sample` — Configurable variables

## Template Variables

All `{{VARS}}` in templates are replaced from:
1. `.env` file values
2. Environment variables
3. Data file passed via `-d` flag

Key variables to set: `COMPANY_NAME`, `COMPANY_DOMAIN`, `PRIMARY_COUNTRY`, `TARGET_AUDIENCE`, `SUPPORT_EMAIL`, `CALENDLY_LINK`

## Rules for the Agent

1. Always reference `marketing.md` for strategic context before executing.
2. Never send automated content without human review — all outreach is "draft for human review."
3. Use templates as the default path; AI enhancement is optional (`-a` flag).
4. Log all generated content and activity to the `logs/` directory.
5. Run `tools/track-som` at least once per week from week 4 onwards.
6. When user asks "what should I do next", reference `checklists/90-day-roadmap.md` and their current week.
