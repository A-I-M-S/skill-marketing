# skill-marketing

**3-layer organic growth engine** for AI transformation consultancies targeting Singapore SMEs. $0 ad spend.

Built from the strategy in `marketing.md` — a comprehensive playbook covering lead capture, visibility channels (LinkedIn, cold email, SEO, directories, PR, communities), and AI-discoverability (AEO/GEO, Share of Model tracking).

## Architecture

```
skill-marketing/
├── skill.md                        # Opencode agent skill definition
├── marketing.md                    # Full strategy reference (source)
├── .env.sample                     # Config template (AI endpoint, company info)
├── lib/
│   ├── helpers.sh                  # Shared bash functions
│   └── ai.sh                       # AI endpoint caller (OpenAI-compatible)
├── tools/                          # Executable automation scripts
│   ├── generate-content            # Template renderer + optional AI enhance
│   ├── generate-outreach           # Batch cold email generator from CSV
│   ├── setup-technical-seo         # robots.txt, llms.txt, schema stub generator
│   └── track-som                   # Share of Model tracking sheet creator
├── templates/                      # Markdown templates with {{VARIABLES}}
│   ├── lead-assessment/            # AI Audit form + landing page sections
│   ├── nurture/                    # 4-email automated nurture sequence
│   ├── linkedin/                   # Mon/Wed/Fri LinkedIn post templates
│   ├── cold-email/                 # 3-email outreach sequence
│   ├── seo/                        # Long-tail blog post + answer-block format
│   ├── schema/                     # JSON-LD schemas (FAQPage, QAPage, ProfessionalService)
│   └── directory-listings/         # Global + Singapore directory registries
├── checklists/                     # Executable markdown checklists
│   ├── week1-sprint.md             # Days 1-7
│   ├── 90-day-roadmap.md           # Full quarter plan (Months 1-3)
│   ├── monthly-review.md           # Monthly KPI review template
│   ├── technical-seo.md            # SSR, robots.txt, llms.txt, schema checklist
│   ├── pr-outreach.md              # Journalists, HARO, press release targets
│   └── directory-listings.md       # Not yet created
├── config/                         # Reference data for content
│   ├── keywords-track-b.md         # SEO keywords (Track B — AI Transformation)
│   ├── persona-cto.md              # Buyer persona
│   └── grants-reference.md         # Singapore grants (PSG, EDG, SFEC)
└── logs/                           # Activity logs
```

## Quick Start

```bash
# 1. Configure
cp .env.sample .env
# Edit .env with your AI endpoint, API key, and company details

# 2. Generate lead capture content
./tools/generate-content templates/lead-assessment/landing-page-sections.md -o output/landing-page.md

# 3. Set up technical SEO foundation
./tools/setup-technical-seo -o output/technical-seo

# 4. Generate LinkedIn posts
./tools/generate-content templates/linkedin/monday-insight.md -o output/posts/monday-week1.md

# 5. Prepare prospect list and generate outreach
# Create prospects.csv, then:
./tools/generate-outreach prospects.csv -o output/campaign-w1

# 6. Track Share of Model (AI discoverability baseline)
./tools/track-som
```

## Using with Opencode

Add to your `opencode.json`:

```json
{
  "skills": ["file:///path/to/skill-marketing/skill.md"]
}
```

Then ask the agent:

- "Run the marketing skill — I need my week 1 sprint"
- "Generate this week's LinkedIn posts"
- "Set up my technical SEO foundation"
- "Create a cold email campaign for these prospects"
- "Track my Share of Model this week"

## Dependencies

- **Bash 4+** — all tools are shell scripts
- **curl + jq** — for AI endpoint calls (optional, only if using AI enhancement)
- **AI endpoint** — optional, set via `AI_ENDPOINT` + `AI_API_KEY` in `.env`

Everything else is template-based and works fully offline without API calls.

## Track B

This repo is configured for **Track B — AI Transformation** (Singapore SME/enterprise decision-makers). See `marketing.md` Section 9 for switching to Track A (Immigration & Relocation).
