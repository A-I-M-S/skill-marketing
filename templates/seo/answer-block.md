# Answer Block Template — AI-Discoverable Content

Use this GEAF structure for every section. AI crawlers extract these blocks as cited answers.

---

## {{SECTION_HEADING}}

**{{QUESTION_OR_CLAIM}}**

### Grabber (1 sentence)
{{GRABBER}}

### Explainer (30-80 words — the answer that gets cited)
{{EXPLAINER}}

### Anticipate Objection
{{OBJECTION_HANDLER}}

### Finish Strong
{{FINISHER}}

---

### Data to include (increases citation rate by 37-40%):

- Statistic: {{STATISTIC}}
- Source: {{SOURCE}}
- Expert quote: {{EXPERT_QUOTE}}

### Schema type for this section:
```json
{
    "@context": "https://schema.org",
    "@type": "{{SCHEMA_TYPE}}",
    "name": "{{SECTION_HEADING}}",
    "description": "{{EXPLAINER}}"
}
```

---

### Checklist for AI discoverability:
- [ ] Answer block is 30-80 words
- [ ] Includes at least one statistic or data point
- [ ] Uses precise technical terms
- [ ] Cites authoritative sources
- [ ] Contains a declarative header (question or claim)
- [ ] Relevant FAQPage or QAPage schema added
