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
│   ├── marketing-daemon            # PM2 background scheduler + combined logging
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
│   ├── agent-log-review.md         # Agent checklist for daemon/log review
│   ├── technical-seo.md            # SSR, robots.txt, llms.txt, schema checklist
│   ├── pr-outreach.md              # Journalists, HARO, press release targets
│   └── directory-listings.md       # Directory listing priority checklist
├── config/                         # Reference data for content
│   ├── keywords-track-b.md         # SEO keywords (Track B — Agentic AI Transformation)
│   ├── persona-cto.md              # Buyer persona (SME/Enterprise CTOs)
│   ├── grants-reference.md         # Singapore grants (PSG, EDG, SFEC)
│   └── default-campaign.env        # Default scheduled-draft variables
├── ecosystem.config.js             # PM2 process definition
└── logs/                           # Activity logs (created at runtime)
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

## Background Automation with PM2

The repository includes a safe background marketing daemon that runs under PM2 and generates draft marketing assets on a schedule. It does **not** send emails or publish posts automatically. Generated content and outreach remain human-review only.

### Configure

Set these values in `.env` as needed:

```bash
MARKETING_DAEMON_INTERVAL_SECONDS=300
MARKETING_ENV_FILE=.env
MARKETING_LOG_FILE=logs/marketing-combined.log
MARKETING_STATUS_FILE=output/status/latest-status.md
MARKETING_OUTPUT_DIR=output
MARKETING_STATE_DIR=output/status/daemon-state
MARKETING_ENABLE_AI=false
MARKETING_ENABLE_OUTREACH=false
MARKETING_PROSPECTS_CSV=prospects.csv
```

Recommended defaults keep AI enhancement and outreach draft generation disabled. Set `MARKETING_ENABLE_AI=true` only after `AI_ENDPOINT`, `AI_API_KEY`, and `AI_MODEL` are configured. Set `MARKETING_ENABLE_OUTREACH=true` only when a reviewed prospects CSV exists.

### Run Once for Testing

```bash
MARKETING_DAEMON_ONCE=true ./tools/marketing-daemon
```

This writes to:

- `logs/marketing-combined.log`
- `output/status/latest-status.md`
- generated output under `output/`

### Run in the Background with PM2

```bash
pm2 start ecosystem.config.js
pm2 status
pm2 logs skill-marketing
```

To stop it:

```bash
pm2 stop skill-marketing
```

### Default Schedule

| Cadence | Task | Output |
|---------|------|--------|
| Every daemon cycle | Health/status check | `output/status/latest-status.md` |
| Monday | LinkedIn insight draft | `output/posts/YYYY-MM-DD-monday-insight.md` |
| Monday | Share of Model tracker refresh | `output/som-tracker.md` |
| Wednesday | LinkedIn tip draft | `output/posts/YYYY-MM-DD-wednesday-tip.md` |
| Friday | LinkedIn case-study draft | `output/posts/YYYY-MM-DD-friday-case-study.md` |
| Friday | SEO long-tail draft | `output/seo/YYYY-MM-DD-long-tail-post.md` |
| First day of month | Monthly review draft | `output/reviews/YYYY-MM-DD-monthly-review.md` |
| Optional | Outreach drafts if enabled and CSV exists | `output/outreach/YYYY-MM-DD/` |

Each scheduled task runs at most once per day. PM2 keeps the daemon alive; the daemon itself tracks whether a task has already run. Scheduled LinkedIn and SEO drafts use `config/default-campaign.env` for template-specific placeholders, while `.env` supplies your company details.

## Agent Log Review

For hybrid monitoring, ask OpenCode/OpenClaw to review:

- `output/status/latest-status.md`
- `logs/marketing-combined.log`
- recent files under `output/`
- `checklists/agent-log-review.md`

Example prompt:

```text
Review the marketing daemon logs and outputs. Tell me if it is running correctly, what marketing drafts were generated, what needs human review, and what I should do next.
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
- **PM2** — optional, for background daemon management
- **AI endpoint** — optional, set via `AI_ENDPOINT` + `AI_API_KEY` in `.env`

Everything else is template-based and works fully offline without API calls.
