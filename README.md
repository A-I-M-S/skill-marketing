# skill-marketing

**3-layer organic growth engine** for **aims-sg.com** — an Agentic Business Transformation consultancy targeting Singapore SMEs and enterprises. $0 ad spend.

This repository implements the strategy from [marketing.md](file:///home/openclaw/skill-marketing/marketing.md) (Track B — AI/Agentic Transformation) to build lead-capture funnels, run outreach campaigns, generate thought leadership content, and optimize for AI-discoverability (AEO/GEO) using AI agents.

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
│   ├── lead-assessment/            # Agentic AI Audit form + landing page sections
│   ├── nurture/                    # 4-email automated nurture sequence
│   ├── linkedin/                   # Mon/Wed/Fri LinkedIn post templates
│   ├── cold-email/                 # 3-email outreach sequence
│   ├── seo/                        # Long-tail blog post + answer-block format
│   ├── schema/                     # JSON-LD schemas (FAQPage, QAPage, ProfessionalService)
│   └── directory-listings/         # Global + Singapore directory registries
├── checklists/                     # Executable markdown checklists
│   ├── week1-sprint.md             # Days 1-7 starting actions
│   ├── 90-day-roadmap.md           # Full quarter plan (Months 1-3)
│   ├── monthly-review.md           # Monthly KPI review template
│   ├── technical-seo.md            # SSR, robots.txt, llms.txt, schema checklist
│   ├── pr-outreach.md              # Journalists, HARO, press release targets
│   └── directory-listings.md       # Directory listing priority checklist
├── config/                         # Reference data for content
│   ├── keywords-track-b.md         # SEO keywords (Track B — Agentic AI Transformation)
│   ├── persona-cto.md              # Buyer persona (SME/Enterprise CTOs)
│   └── grants-reference.md         # Singapore grants (PSG, EDG, SFEC)
└── logs/                           # Activity logs
```

## Quick Start

```bash
# 1. Configure
cp .env.sample .env
# Edit .env with your AI endpoint, API key, and aims-sg.com company details

# 2. Generate lead capture content (Agentic AI Audit)
./tools/generate-content templates/lead-assessment/landing-page-sections.md -o output/landing-page.md

# 3. Set up technical SEO/AEO/GEO foundation
./tools/setup-technical-seo -o output/technical-seo

# 4. Generate LinkedIn posts focusing on Agentic AI
./tools/generate-content templates/linkedin/monday-insight.md -o output/posts/monday-week1.md

# 5. Prepare prospect list and generate outreach campaigns
# Create prospects.csv, then:
./tools/generate-outreach prospects.csv -o output/campaign-w1

# 6. Track Share of Model (AI discoverability baseline)
./tools/track-som
```

## Using with Opencode

Add to your `opencode.json`:

```json
{
  "skills": ["file:///home/openclaw/skill-marketing/skill.md"]
}
```

Then ask the agent:

- "Run the marketing skill — I need my week 1 sprint"
- "Generate this week's LinkedIn posts targeting SG CTOs"
- "Set up my technical SEO and llms.txt files"
- "Create a cold email campaign for these prospects"
- "Track my Share of Model (SoM) this week"

## Target Positioning: Track B (Agentic Transformation)

This repository is permanently configured for **Track B — AI/Agentic Transformation** targeting Singapore SME/enterprise decision-makers. The marketing goals focus on positioning aims-sg.com as the leading authority in deploying multi-agent architectures and autonomous workflow automation under Singapore government grants (EDG/PSG).

## Dependencies

- **Bash 4+** — all tools are shell scripts
- **curl + jq** — for AI endpoint calls (optional, only if using AI enhancement)
- **AI endpoint** — optional, set via `AI_ENDPOINT` + `AI_API_KEY` in `.env`

Everything else is template-based and works fully offline without API calls.
