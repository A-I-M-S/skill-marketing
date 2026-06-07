---
name: skill-marketing
description: Automated Lead Generation & Outreach Engine for AIMS. Automatically harvests leads from Apollo, PDL, Snov, Hunter, and Clay, researches recipient websites, synchronizes contacts to Attio CRM, and delivers customized marketing emails via Brevo.
mode: auto
---

# skill-marketing

The **skill-marketing** engine runs a highly automated, zero-budget outbound marketing stack for **AIMS** (Agentic AI Business Transformation for Singapore SMEs). The engine integrates multiple business lead databases, tracks prospect progress in **Attio CRM**, and leverages an **AI-driven domain research loop** to send highly customized cold emails with a Calendly CTA via **Brevo**.

---

## 🛠️ Execution Playbook for the Agent

As an autonomous agent, you should follow this execution playbook to run lead generation and outbound tasks for the user.

### 1. Step 1: Ingest Prospects (Harvesting & Imports)
When the user asks you to "Harvest leads" or "Generate new prospects", call the harvest API crawler:
```bash
./tools/run-outbound --harvest 100
```
If the user uploads their own custom CSV list of prospects:
```bash
./tools/run-outbound --import /path/to/user_prospects.csv
```
This automatically parses their name and email, filters out existing duplicates from `leads.csv` and `contacted.csv`, strictly excludes CTO positions, and appends the new unique leads to `output/leads/leads.csv` (pending pool).

---

### 2. Step 2: Run a Safe Test Campaign (Testing)
Before running a live campaign, always recommend running a test redirect to verify the personalization quality:
```bash
./tools/run-outbound --count 1 --test your-test-email@domain.com
```
This will:
1. Pull the top lead from `output/leads/leads.csv`.
2. Perform domain trade-level research.
3. Call the LLM to write a hyper-personalized email featuring the Calendly CTA.
4. Sync the contact to Attio CRM.
5. Deliver the customized email *only* to the specified test email address.
6. Archive the lead to `output/leads/contacted.csv`.

---

### 3. Step 2: Dry-Run Draft Mode (Local Review)
Compile personalized pitches for your pending prospects list and save them locally without sending emails or updating lists:
```bash
./tools/run-outbound --count 20 --draft-only
```
Generated content is saved directly to `output/leads/drafts_today.json` for human review.

---

### 4. Step 2: Executing Live Deliveries (Live Campaign)
Once the user is ready to start live outreach, trigger the delivery cycle:
```bash
./tools/run-outbound --count 200 --send
```
This will execute actual live email deliveries to prospects via Brevo SMTP, synchronize contacts directly into **Attio CRM** with status set to `"contacted"`, and move processed prospects from `leads.csv` to `contacted.csv`.

---

## ⚙️ Configuration Variables (.env)

The tool reads its credentials directly from `.env`:
*   `APOLLO_API_KEY`, `HUNTER_API_KEY`, `PDL_API_KEY`, `SNOV_ID`, `SNOV_API_KEY`, `CLAY_API_KEY` (Lead Generation)
*   `BREVO_API_KEY`, `BREVO_SENDER` (Delivery)
*   `ATTIO_API_KEY` (CRM Tracking)
*   `CALENDLY_URL` (Call-To-Action Booking Link)
*   `AI_ENDPOINT`, `AI_API_KEY`, `AI_MODEL` (Personalization AI)
