# Technical SEO Checklist — Layer 3 (AI Discoverability)

## Server-Side Rendering (SSR)
- [ ] Verify site uses SSR (not client-side-only rendering)
- [ ] Test: `curl -s https://yourdomain.com | head -50` — HTML content should be present
- [ ] If using React/Next.js: enable SSR or Static Site Generation
- [ ] If using SPA (Vue/React CSR): switch to Nuxt/Next.js or prerender.io
- [ ] Critical: 69% of AI crawlers cannot run JavaScript

## robots.txt
- [ ] Run `tools/setup-technical-seo` to generate
- [ ] Deploy to `https://{{COMPANY_DOMAIN}}/robots.txt`
- [ ] Verify: curl returns the file with status 200
- [ ] Allow: OAI-SearchBot, Claude-SearchBot, PerplexityBot
- [ ] Optionally block: GPTBot, ClaudeBot, Google-Extended
- [ ] Reference sitemap.xml

## llms.txt
- [ ] Deploy to `https://{{COMPANY_DOMAIN}}/llms.txt`
- [ ] Served as `text/markdown` content type
- [ ] Include: company name, about, key pages, core topics
- [ ] Deploy `llms-full.txt` for detailed reference
- [ ] Test with: `curl -s -H "Accept: text/markdown" https://yourdomain.com/llms.txt`

## JSON-LD Schema
- [ ] `ProfessionalService` schema on homepage
- [ ] `FAQPage` schema on FAQ page
- [ ] `QAPage` schema on Q&A content
- [ ] `Article` schema on blog posts
- [ ] `BreadcrumbList` schema on all pages
- [ ] Validate all schemas with Google Rich Results Test
- [ ] Use templates from `templates/schema/` as starting point

## Content Structure (Answer-First)
- [ ] Every section opens with a 30-80 word answer block
- [ ] Use declarative/question headers (e.g., "How to Implement AI in Singapore SMEs")
- [ ] Include at least 1 statistic per major section
- [ ] Use comparison tables and structured lists
- [ ] Cite authoritative sources (+40% visibility)
- [ ] Follow GEAF layout: Grabber → Explainer → Anticipate → Finish
- [ ] Use `templates/seo/answer-block.md` as reference

## URL Structure
- [ ] Use prompt-style URLs (e.g., `/how-to-implement-ai-in-singapore-smes`)
- [ ] Use descriptive, keyword-rich slugs
- [ ] Keep URLs clean (no params, no underscores)
- [ ] Use hyphens as word separators

## Technical
- [ ] Submit sitemap.xml to Google Search Console
- [ ] Submit sitemap.xml to Bing Webmaster Tools
- [ ] Ensure fast page load speed (< 2s)
- [ ] Mobile-responsive design
- [ ] SSL/HTTPS enabled
- [ ] No broken links (run a crawler check)
